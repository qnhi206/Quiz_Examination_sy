class User:
    def __init__(self, username, password, approved=False):
        self.username = username
        self.password = password
        self.approved = approved

class UserManager:
    def __init__(self):
        self.users = {}

    def register(self, username, password):
        if username in self.users:
            return False, "Username đã tồn tại"

        new_user = User(username, password, False)
        self.users[username] = new_user
        return True, "Đăng ký thành công, chờ duyệt"

    def login(self, username, password):
        if username not in self.users:
            return False, "Sai tài khoản hoặc mật khẩu"

        user = self.users[username]

        if user.password != password:
            return False, "Sai tài khoản hoặc mật khẩu"

        if not user.approved:
            return False, "Tài khoản chưa được duyệt"

        return True, "Đăng nhập thành công"
