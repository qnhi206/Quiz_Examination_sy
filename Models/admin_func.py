import json
import os
import hashlib


data_file = "account.json"

# Hàm mã hóa mật khẩu
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Hàm kiểm tra mật khẩu
def verify_password(stored_hash, provided_password):
    return stored_hash == hash_password(provided_password)

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
    def __init__(self, user_manager, username, info):
        self.user_manager = user_manager
        self.username = username 
        self.id = info.get('id')
        self.fullname = info.get('fullname')
        self.email = info.get('email')
        self.passwordhash = info.get('password') 
        self.role = info.get('role')

    def updateprofile(self, field, new_value):
        allowed_fields = ["fullname", "email"] # Không cho update pass ở đây để tránh lỗi hash
        if field not in allowed_fields:
            print("Không được phép cập nhật trường này hoặc cần chức năng đổi mật khẩu riêng.")
            return False
        setattr(self, field, new_value)
        self.user_manager.users[self.username][field] = new_value
        self.user_manager.save_users()       
        print(f"Cập nhật {field} thành '{new_value}' thành công.")
        return True

class Admin:
    def __init__(self, user_manager):
        self.user_manager = user_manager

    def login(self, username, password):
        # Logic login đã được xử lý ở main, hàm này chủ yếu để gọi menu
        print(f"\nĐăng nhập thành công với vai trò Admin.\n")
        self.admin_menu()
        return True

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