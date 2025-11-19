# student.py
from quiz import Quiz
from attempt import Attempt

class Student:
    def __init__(self, user, quiz_manager, attempt_manager):
        self.user = user
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

    # --------------------------------------------------

    def list_quiz(self):
        print("\n=== DANH SÁCH QUIZ ===")
        for quiz_id, quiz in self.quiz_manager.quizzes.items():
            print(f"{quiz_id} - {quiz.title}")

    # --------------------------------------------------

    def take_quiz(self):
        quiz_id = input("Nhập ID quiz: ")

        if quiz_id not in self.quiz_manager.quizzes:
            print("Quiz không tồn tại!")
            return

        quiz = self.quiz_manager.quizzes[quiz_id]
        print(f"\n=== BẮT ĐẦU QUIZ: {quiz.title} ===")

        answers = {}
        score = 0

        for q_id, question in quiz.questions.items():
            print(f"\nCâu {q_id}: {question.text}")

            for idx, choice in enumerate(question.choices):
                print(f"{idx+1}. {choice}")

            ans = input("Chọn đáp án: ")

            try:
                ans_idx = int(ans) - 1
            except:
                ans_idx = -1

            answers[q_id] = ans_idx

            if ans_idx == question.correct_choice:
                score += 1

        print(f"\n=== HOÀN THÀNH! Điểm: {score}/{len(quiz.questions)} ===")

        self.attempt_manager.save_attempt(
            user_id=self.user.id,
            quiz_id=quiz_id,
            answers=answers,
            score=score
        )

    # --------------------------------------------------

    def view_history(self):
        print("\n=== LỊCH SỬ LÀM BÀI ===")

        history = self.attempt_manager.get_attempts_by_user(self.user.id)

        if not history:
            print("Bạn chưa làm bài nào.")
            return

        for at in history:
            print(f"Quiz: {at.quiz_id}, Điểm: {at.score}")
