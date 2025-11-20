import admin_func

class Choice:
    def __init__(self, choice_id, text, is_correct):
        self.id = choice_id   
        self.text = text      
        self.is_correct = is_correct

class Question:
    def __init__(self, question_id, text, points, qtype):
        self.id = question_id    
        self.text = text       
        self.points = points   
        self.type = qtype    
        self.choices = []      

    def add_choice(self, choice):
        self.choices.append(choice)

    # SỬA: Thêm hàm lấy index đáp án đúng
    def get_correct_choice_index(self):
        for i, choice in enumerate(self.choices):
            if choice.is_correct:
                return i
        return -1

    def validate(self):
        if self.points <= 0:
            return False
        has_correct = False
        for c in self.choices:
            if c.is_correct:
                has_correct = True
                break
        if not has_correct:
            return False
        return True

class QuizManager:
    def __init__(self):
        self.quizzes = {} 

    def add_quiz(self, quiz):
        self.quizzes[quiz.quizid] = quiz
        
    def get_published_quizzes(self):
        return {q_id: q for q_id, q in self.quizzes.items() if q.ispublished}

class Quiz:
    def __init__(self, quiz_id, title, description, timelimit, maxattempts):
        self.quizid = quiz_id         
        self.title = title             
        self.description = description 
        self.timelimit = timelimit     
        self.maxattempts = maxattempts 
        self.ispublished = False       
        self.questions = []           

    def add_question(self, question):
        self.questions.append(question)

    # SỬA: Logic chấm điểm dựa trên point
    def grade(self, answers):
        total_score = 0
        correct_count = 0
        for q in self.questions:
            chosen_index = answers.get(q.id, -1)
            if chosen_index != -1 and chosen_index == q.get_correct_choice_index():
                total_score += q.points
                correct_count += 1
        return total_score, correct_count

class Teacher(admin_func.User):
    # SỬA: Init nhận quiz_manager và gọi super() đúng cách
    def __init__(self, user_manager, username, info, quiz_manager):
        super().__init__(user_manager, username, info)
        self.employeecode = info.get('employeecode')
        self.quizzes = []   # Lưu ID các quiz teacher này tạo
        self.quiz_manager = quiz_manager # Lưu tham chiếu global

    def find_quiz_index(self, quizid: str) -> int:
        try:
            return self.quizzes.index(quizid)
        except ValueError:
            return -1

    def create_quiz(self, quizid: str, title: str, description: str,
                    timelimit: int, maxattempts: int):
        if quizid in self.quiz_manager.quizzes:
            print(f"Quiz id {quizid} đã tồn tại.")
            return None
        else:
            quiz = Quiz(quizid, title, description, timelimit, maxattempts)
            self.quizzes.append(quiz.quizid)
            self.quiz_manager.add_quiz(quiz) # Thêm vào kho chung
            print(f"Đã tạo quiz {quizid} thành công.")
            return quiz

    def edit_quiz(self, quizid: str, new_title: str, new_description: str,
                  new_timelimit: int, new_maxattempts: int) -> bool:
        if quizid not in self.quiz_manager.quizzes:
            print(f"Không tìm thấy quiz {quizid}.")
            return False
        
        q = self.quiz_manager.quizzes[quizid]
        q.title = new_title
        q.description = new_description
        q.timelimit = new_timelimit
        q.maxattempts = new_maxattempts
        print(f"Đã cập nhật quiz {quizid} thành công.")
        return True

    def delete_quiz(self, quizid: str) -> bool:
        if quizid not in self.quiz_manager.quizzes:
            print(f"Không tìm thấy quiz {quizid}.")
            return False
        
        del self.quiz_manager.quizzes[quizid] # Xóa khỏi kho chung
        
        idx = self.find_quiz_index(quizid)
        if idx != -1:
            self.quizzes.pop(idx) # Xóa khỏi danh sách riêng
            
        print(f"Đã xóa quiz {quizid} thành công.")
        return True

    def publish_quiz(self, quizid: str, publish: bool = True) -> bool:
        if quizid not in self.quiz_manager.quizzes:
            print(f"Không tìm thấy quiz {quizid}.")
            return False
        
        self.quiz_manager.quizzes[quizid].ispublished = publish
        state = "publish" if publish else "unpublish"
        print(f"Quiz {quizid} đã được {state}.")
        return True

    def print_quizzes(self) -> None:
        print("\nDanh sách đề thi của bạn:")
        if not self.quizzes:
            print("Chưa có quiz nào.")
            return
        for q_id in self.quizzes:
            q = self.quiz_manager.quizzes.get(q_id)
            if q:
                print(
                    f"ID: {q.quizid}"
                    f" | Title: {q.title}"
                    f" | Time: {q.timelimit} phút"
                    f" | MaxAttempts: {q.maxattempts}"
                    f" | Published: {'Yes' if q.ispublished else 'No'}"
                )