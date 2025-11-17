# file main chỉ cần sử dụng 2 lệnh ở dưới nha
#from user import UserManager
#from admin import AdminManager

from user import UserManager

class AdminManager:
    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.admins = {
            "duong": "admin1",
            "nhi": "admin2",
            "chung": "admin3",
            "dat": "admin4"
        }
    def login_admin(self, username, password):
        return self.admins.get(username) == password

    def approve_user(self, username):
        if username not in self.user_manager.users:
            return False, "Không tìm thấy user"

        self.user_manager.users[username].approved = True
        return True, "User đã được duyệt"

    def update_user(self, username, new_pass):
        if username not in self.user_manager.users:
            return False, "Không tìm thấy user"

        self.user_manager.users[username].password = new_pass
        return True, "Cập nhật mật khẩu thành công"
    
def run_program():
    user_manager = UserManager()
    admin_manager = AdminManager(user_manager)

    while True:
        print("\n MENU ")
        print("1. Đăng ký")
        print("2. Đăng nhập User")
        print("3. Đăng nhập Admin")
        print("0. Thoát")

        choice = input("Chọn: ")

        if choice == "1":
            u = input("Username: ")
            p = input("Password: ")
            ok, msg = user_manager.register(u, p)
            print(msg)

        elif choice == "2":
            u = input("Username: ")
            p = input("Password: ")
            ok, msg = user_manager.login(u, p)
            print(msg)

        elif choice == "3":
            u = input("Admin username: ")
            p = input("Admin password: ")

            if admin_manager.login_admin(u, p):
                print("Admin đăng nhập thành công!")

                while True:
                    print("\ ADMIN MENU")
                    print("1. Duyệt user")
                    print("2. Update user password")
                    print("0. Thoát admin")

                    c = input("Chọn: ")

                    if c == "1":
                        name = input("User cần duyệt: ")
                        ok, msg = admin_manager.approve_user(name)
                        print(msg)

                    elif c == "2":
                        name = input("User: ")
                        newpw = input("New password: ")
                        ok, msg = admin_manager.update_user(name, newpw)
                        print(msg)

                    elif c == "0":
                        break
            else:
                print("Sai thông tin admin")

        elif choice == "0":
            break


if __name__ == "__main__":
    run_program()
