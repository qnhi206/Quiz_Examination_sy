class AdminManager:
    def __init__(self, user_manager):
        self.admins = {"admin": "admin123"} #tk mk admin
        self.user_manager = user_manager
        self.pending_update_requests = []
    #login
    def login(self, username, password):
        if username in self.admins and self.admins[username] == password:
            print(f"\ndang nhap thanh cong\n")
            self.admin_menu()
            return True
        return False

    def admin_menu(self):
        while True:
            print("ADMIN MENU") 
            print("1. manage user account")
            print("2. assign roles")
            print("3. duyet update")
            print("4. delete user")
            print("0. logout")

            choice = input("")

            if choice == "1":
                print("\nDANH SACH USER")
                print("ID | Fullname | Email | Role")

                for username, info in self.user_manager.users.items():
                    print(f"{info['id']} | {info['fullname']} | {info['email']} | {info['role']}")

            elif choice == "2":
                self.assign_role()

            elif choice == "3":
                self.process_update_requests()

            elif choice == "4":
                self.delete_user()

            elif choice == "0":
                print("\nda thoat\n")
                return

            else:
                print("khong hop le\n")
    #assign roles
    def assign_role(self):
        username = input("username update role ")

        if username not in self.user_manager.users:
            print("User khong ton tai\n")
            return

        new_role = input("role moi (student/teacher): ")
        self.user_manager.users[username]["role"] = new_role
        print("thanh cong\n")
    #duyet update
    def process_update_requests(self):
        if not self.pending_update_requests:
            print("\nkhong co update\n")
            return
        
        print("\ndanh sach update\n")
        for req in self.pending_update_requests:
            user = req["username"]
            field = req["field"]
            value = req["value"]

            print(f"{user} yeu cau doi {field} thanh: {value}")

            decision = input("duyet (y/n): ")

            if decision.lower() == "y":
                self.user_manager.users[user][field] = value
                print("duyet\n")
            else:
                print("tu choi\n")
        #xoa danh sach yeu cau khi duyet xong
        self.pending_update_requests.clear()
    #delete user
    def delete_user(self):
        username = input("Nhap username can xoa: ")

        if username not in self.user_manager.users:
            print("User khong ton tai!\n")
            return

        confirm = input(f"chac chan? '{username}'? (y/n): ")

        if confirm.lower() == "y":
            del self.user_manager.users[username]
            print("Da xoa thanh cong!\n")
        else:
            print("Da huy xoa!\n")
