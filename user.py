class User:
    # id, fullname, email, password
    def __init__(self, user_id = str, fullname = str, email = str, passwordhash = str, role = str):
        self.id = user_id
        self.fullname = fullname
        self.email = email
        self.passwordhash = passwordhash
        self.role = role
    #login
    def login(self, id, password):
        if self.id == id and self.passwordhash == password:
            print("dang nhap thanh cong\n")
            return True
        print("sai id hoac mat khau\n")
        return False
    #updateprofile
    def updateprofile(self, field, new_value):
        allowed_fields = ["fullname", "email", "passwordhash"]

        if field not in allowed_fields:
            print("khong duoc phep")
            return False

        setattr(self, field, new_value)
        print(f"cap nhat {field} thanh {new_value}")
        return True
