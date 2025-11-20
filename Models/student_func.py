from teacher_func import Quiz
from attempt_func import Attempt

class Student:
    def __init__(self, user, quiz_manager, attempt_manager):
        self.user = user # user ở đây là dictionary (user_info)
        self.quiz_manager = quiz_manager
        self.attempt_manager = attempt_manager

    def menu(self):
        while True:
            print("\n===== STUDENT MENU =====")
            print("1. Danh sách quiz")
            print("2. Làm bài")
            print("3. Xem lịch sử làm bài")
            print("0. Đăng xuất")

            choice = input("Chọn: ")
            if choice == "1":
                self.list_quiz()
            elif choice == "2":
                self.take_quiz()
            elif choice == "3":
                self.view_history()
            elif choice == "0":
                print("Đăng xuất...\n")
                return
            else:
                print("Không hợp lệ!")

    def list_quiz(self):
        print("\n=== DANH SÁCH QUIZ KHẢ DỤNG ===")
        published_quizzes = self.quiz_manager.get_published_quizzes()
        if not published_quizzes:
            print("Hiện chưa có quiz nào.")
            return
        for quiz_id, quiz in published_quizzes.items():
            print(f"{quiz_id} - {quiz.title} (Thời gian: {quiz.timelimit} phút)")

    def take_quiz(self):
        quiz_id = input("Nhập ID quiz: ")

        if quiz_id not in self.quiz_manager.quizzes:
            print("Quiz không tồn tại!")
            return

        quiz = self.quiz_manager.quizzes[quiz_id]
        if not quiz.ispublished:
            print("Quiz này chưa được mở.")
            return

        print(f"\n=== BẮT ĐẦU QUIZ: {quiz.title} ===")

        answers = {}
        # SỬA: questions là List, phải duyệt theo kiểu list
        for i, question in enumerate(quiz.questions):
            print(f"\nCâu {i+1}: {question.text} ({question.points} điểm)")

            for idx, choice in enumerate(question.choices):
                print(f"  {idx+1}. {choice.text}") # In nội dung choice

            ans = input("Chọn đáp án (số): ")
            try:
                ans_idx = int(ans) - 1
            except:
                ans_idx = -1

            # Lưu index đáp án user chọn cho câu hỏi ID này
            answers[question.id] = ans_idx

        # Tính điểm bằng hàm grade của Quiz
        score, correct_count = quiz.grade(answers)
        
        # Tính tổng điểm tối đa
        total_points = sum(q.points for q in quiz.questions)

        print(f"\n=== HOÀN THÀNH! ===")
        print(f"Số câu đúng: {correct_count}/{len(quiz.questions)}")
        print(f"Tổng điểm: {score}/{total_points}")

        # SỬA: Truy cập ID bằng dictionary key ['id']
        self.attempt_manager.save_attempt(
            user_id=self.user['id'],
            quiz_id=quiz_id,
            answers=answers,
            score=score
        )    

    def view_history(self):
        print("\n=== LỊCH SỬ LÀM BÀI ===")
        # SỬA: Truy cập ID bằng dictionary key ['id']
        history = self.attempt_manager.get_attempts_by_user(self.user['id'])

        if not history:
            print("Bạn chưa làm bài nào.")
            return

        for at in history:
            print(f"Quiz: {at.quiz_id}, Điểm: {at.score}")