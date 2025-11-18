class UserManager:
    def __init__(self):
        self.users = {
            #danh sach user
            "u01": {
                "id": "U01",
                "fullname": "Nguyen Van A",
                "email": "user1@gmail.com",
                "password": "123",
                "role": "student"
            },
            "u02": {
                "id": "U02",
                "fullname": "Nguyen Van B",
                "email": "user2@gmail.com",
                "password": "456",
                "role": "teacher"
            }
        }
    #login
    def login(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            print(f"\ndang nhap thanh cong!\n")
            return self.user_menu(username)
        return False

    def user_menu(self, username):
        while True:
            print("USER MENU")
            print("1. updateprofile")
            print("0. thoat ra")

            choice = input("")
            if choice == "1": #update
                print("\nUPDATE")
                print("update: fullname / email / role")

                field = input("ban muon thay doi gi?").lower()

                if field not in ["fullname", "email", "role"]:
                    print("khong hop le\n")
                    continue

                new_value = input(f"nhap {field} moi: ")

                return {
                    "username": username,
                    "field": field,
                    "value": new_value
                }

            elif choice == "0":
                print("\ndang xuat thanh cong\n")
                return None

            else:
                print("khong hop le\n")