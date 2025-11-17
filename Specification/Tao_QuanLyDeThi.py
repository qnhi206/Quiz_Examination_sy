class Teacher(User):
    def __init__(self, user_id = str, fullname = str, email = str, passwordhash = str, employeecode = str):
        self.id = user_id
        self.fullname = fullname
        self.email = email
        self.passwordhash = passwordhash
        self.employeecode = employeecode
        self.quizzes = []   # danh sách các Quiz mà teacher quản lý

    # tìm vị trí quiz theo id
    def find_quiz_index(self, quizid: str) -> int:
        for i, q in enumerate(self.quizzes):
            if q.quizid == quizid:
                return i
        return -1
    # Tạo đề thi
    def create_quiz(self, quizid: str, title: str, description: str,
                    timelimit: int, maxattempts: int) -> bool:
        if self.find_quiz_index(quizid) != -1:
            print(f"Quiz id {quizid} đã tồn tại.")
            return False
        else:
            quiz = Quiz(quizid, title, description, timelimit, maxattempts)
            self.quizzes.append(quiz)
            print(f"Đã tạo quiz {quizid} thành công.")
            return True
    # Sửa đề thi 
    def edit_quiz(self, quizid: str, new_title: str, new_description: str,
                  new_timelimit: int, new_maxattempts: int) -> bool:
        idx = self.find_quiz_index(quizid)
        if idx == -1:
            print(f"Không tìm thấy quiz {quizid}.")
            return False
        else:
            q = self.quizzes[idx]
            q.title = new_title
            q.description = new_description
            q.timelimit = new_timelimit
            q.maxattempts = new_maxattempts
            print(f"Đã cập nhật quiz {quizid} thành công.")
            return True

    # Xóa đề thi
    def delete_quiz(self, quizid: str) -> bool:
        idx = self.find_quiz_index(quizid)
        if idx == -1:
            print(f"Không tìm thấy quiz {quizid}.")
            return False
        self.quizzes.pop(idx)
        print(f"Đã xóa quiz {quizid} thành công.")
        return True

    #  Publish / Unpublish đề thi
    def publish_quiz(self, quizid: str, publish: bool = True) -> bool:
        idx = self.find_quiz_index(quizid)
        if idx == -1:
            print(f"Không tìm thấy quiz {quizid}.")
            return False
        self.quizzes[idx].ispublished = publish
        if publish:
            print(f"Quiz {quizid} đã được publish.")
        else:
            print(f"Quiz {quizid} đã được unpublish.")
        return True

    # In danh sách đề
    def print_quizzes(self) -> None:
        print("\nDanh sách đề thi")
        if not self.quizzes:
            print("Chưa có quiz nào.")
            return
        for q in self.quizzes:
            print(
                f"ID: {q.quizid}"
                f" | Title: {q.title}"
                f" | Time: {q.timelimit} phút"
                f" | MaxAttempts: {q.maxattempts}"
                f" | Published: {'Yes' if q.ispublished else 'No'}"
            )
            
