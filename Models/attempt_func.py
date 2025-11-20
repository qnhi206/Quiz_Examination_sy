class Attempt_Answer:
    def __init__(self, question_id, selected_choice):
        self.question_id = question_id
        self.selected_choice = selected_choice


class Attempt:
    def __init__(self, user_id, quiz_id, answers, score):
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.answers = answers 
        self.score = score


class AttemptManager:
    def __init__(self):
        self.attempts = []  

    def save_attempt(self, user_id, quiz_id, answers, score):
        attempt = Attempt(
            user_id=user_id,
            quiz_id=quiz_id,
            answers=answers,
            score=score
        )
        self.attempts.append(attempt)
        print("Đã lưu kết quả làm bài!\n")

    def get_attempts_by_user(self, user_id):
        return [a for a in self.attempts if a.user_id == user_id]

    def get_attempts_by_quiz(self, quiz_id):
        return [a for a in self.attempts if a.quiz_id == quiz_id]
