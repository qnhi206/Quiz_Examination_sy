import json
import getpass
import os
#đường dẫn đến file json
data_file = r"C:\CNPM\quiz\Models\account.json"
class UserManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.users = {} 
        self.load_users()

    def load_users(self):
        if not os.path.exists(self.data_file):
            print(f"File {self.data_file} không tồn tại. Khởi tạo danh sách người dùng rỗng.")
            self.users = {}
            return
            
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
            print(f"Đã tải {len(self.users)} tài khoản từ JSON.")
        except json.JSONDecodeError:
            print("Lỗi đọc file JSON. Dữ liệu người dùng sẽ được khởi tạo rỗng.")
            self.users = {}
        except Exception as e:
            print(f"Lỗi khi tải file JSON: {e}")
            self.users = {}

    def save_users(self):
        try:
            os.makedirs(os.path.dirname(self.data_file) or '.', exist_ok=True)
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=4)
            print("Đã lưu thay đổi vào file JSON thành công.")
        except Exception as e:
            print(f"Lỗi khi lưu file JSON: {e}")

    def find_user_by_id(self, user_id):
        for username, info in self.users.items():
            if info.get('id') == user_id:
                return username, info 
        return None, None
    
    def get_user_data(self, username):
        return self.users.get(username)

class User:
    # Thêm user_manager để có thể lưu dữ liệu khi cập nhật profile
    def __init__(self, user_manager, username, info):
        self.user_manager = user_manager
        self.username = username 
        self.id = info.get('id')
        self.fullname = info.get('fullname')
        self.email = info.get('email')
        self.passwordhash = info.get('password') 
        self.role = info.get('role')

    def login(self, username, password):
        if self.username == username and self.passwordhash == password:
            print(f"Đăng nhập thành công với vai trò {self.role}.")
            return True
        print("Sai username hoặc mật khẩu.")
        return False
    def updateprofile(self, field, new_value):
        allowed_fields = ["fullname", "email", "passwordhash"]

        if field not in allowed_fields:
            print("Không được phép cập nhật trường này.")
            return False
        setattr(self, field, new_value)
        self.user_manager.users[self.username][field] = new_value
        self.user_manager.save_users()       
        print(f"Cập nhật {field} thành '{new_value}' thành công.")
        return True
    def to_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "email": self.email,
            "password": self.passwordhash,
            "role": self.role
        }

class Admin:
    def __init__(self, user_manager):
        self.user_manager = user_manager
    def login(self, username, password):
        user_info = self.user_manager.get_user_data(username)
        
        if user_info and user_info.get('role') == 'Admin':
            stored_password = user_info.get('password')
            
            if stored_password == password:
                print(f"\nĐăng nhập thành công với vai trò Admin.\n")
                self.admin_menu()
                return True
            else:
                print("\nMật khẩu không chính xác.\n")
                return False
        
        print("\nTên đăng nhập không tồn tại hoặc không phải là Admin.\n")
        return False

    def admin_menu(self):
        while True:
            print("\n========== ADMIN MENU ==========") 
            print("1. Manage user account (List/View)")
            print("2. Assign roles")
            print("3. Delete user")
            print("0. Logout")

            choice = input("Lựa chọn: ")

            if choice == "1":
                print("\n----- DANH SÁCH USER -----")
                for username, info in self.user_manager.users.items():
                    print(f"User: {username} | ID: {info.get('id')} | Role: {info.get('role')} | Fullname: {info.get('fullname')}")

            elif choice == "2":
                self.assign_role()
            elif choice == "3":
                self.delete_user()
            elif choice == "0":
                self.user_manager.save_users()
                print("\nĐã thoát. Dữ liệu đã được lưu vào JSON.\n")
                return

            else:
                print("Lựa chọn không hợp lệ.\n")
    def assign_role(self):
        username = input("Nhập username cần cập nhật role: ")

        if username not in self.user_manager.users:
            print("User không tồn tại.\n")
            return

        new_role = input("Role mới (Student/Teacher/Admin): ").strip().capitalize()

        if new_role not in ["Student", "Teacher", "Admin"]:
             print("Vai trò không hợp lệ.\n")
             return
             
        self.user_manager.users[username]["role"] = new_role
        self.user_manager.save_users()
        print(f"Đã gán role '{new_role}' cho user '{username}' thành công.\n")
    def delete_user(self):
        username = input("Nhập username cần xóa: ")

        if username not in self.user_manager.users:
            print("User không tồn tại!\n")
            return

        confirm = input(f"Chắc chắn muốn xóa user '{username}'? (y/n): ")

        if confirm.lower() == "y":
            del self.user_manager.users[username]
            self.user_manager.save_users()
            print(f"Đã xóa user '{username}' thành công!\n")
        else:
            print("Đã hủy thao tác xóa!\n")




