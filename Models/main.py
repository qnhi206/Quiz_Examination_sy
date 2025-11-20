import teacher_func
# Thêm import hash_password và verify_password
from admin_func import UserManager, Admin, data_file, hash_password, verify_password
import student_func
import attempt_func
import getpass
import os 
from teacher_func import QuizManager, Question, Choice

def run_teacher_menu(teacher, quiz_manager):
    while True:
        print("\n==== MENU QUẢN LÝ QUIZ ====")
        print("1. Tạo quiz")
        print("2. Sửa quiz")
        print("3. Xóa quiz")
        print("4. Publish / Unpublish quiz")
        print("5. Xem danh sách quiz")
        print("6. Thêm câu hỏi vào quiz")
        print("7. Thoát")
        choice = input("Chọn chức năng: ")
        
        if choice == "1":
            quizid = input("Nhập ID quiz: ")
            title = input("Nhập tiêu đề: ")
            des = input("Nhập mô tả: ")
            try:
                time = int(input("Nhập thời gian (phút): "))
                max_attempt = int(input("Nhập số lần làm tối đa: "))
                # Hàm create_quiz trả về object hoặc None
                new_quiz = teacher.create_quiz(quizid, title, des, time, max_attempt)
            except ValueError:
                print("Lỗi: Thời gian và số lần làm tối đa phải là số nguyên.")
        
        elif choice == "2":
            quizid = input("Nhập ID quiz cần sửa: ")
            try:
                new_title = input("Tiêu đề mới: ")
                new_des = input("Mô tả mới: ")
                new_time = int(input("Thời gian mới (phút): "))
                new_max_attempt = int(input("Số lần làm tối đa mới: "))
                teacher.edit_quiz(quizid, new_title, new_des, new_time, new_max_attempt)
            except ValueError:
                print("Lỗi: Thời gian và số lần làm tối đa phải là số nguyên.")
        
        elif choice == "3":
            quizid = input("Nhập ID quiz cần xóa: ")
            teacher.delete_quiz(quizid)
        
        elif choice == "4":
            quizid = input("Nhập ID quiz: ")
            pub = input("Publish? (y/n): ")
            teacher.publish_quiz(quizid, publish=(pub.lower() == "y"))
        
        elif choice == "5":
            teacher.print_quizzes()
        
        elif choice == "6":
            quizid = input("Nhập ID quiz muốn thêm câu hỏi: ")
            # Sửa: Lấy quiz từ manager chung
            if quizid not in quiz_manager.quizzes:
                 print("Quiz không tồn tại!")
                 continue
            
            qid = input("ID câu hỏi: ")
            text = input("Nội dung câu hỏi: ")
            try:
                points = float(input("Điểm: "))
                qtype = input("Loại câu hỏi (MCQ/TF/...): ")
                
                question = Question(qid, text, points, qtype)
                
                n = int(input("Số lượng lựa chọn: "))
                for i in range(n):
                    cid = f"{qid}_C{i+1}"
                    ctext = input(f"Nội dung lựa chọn {i+1}: ")
                    is_correct = input("Đáp án đúng? (y/n): ").lower() == "y"
                    
                    choice_obj = Choice(cid, ctext, is_correct)
                    question.add_choice(choice_obj)

                if not question.validate():
                    print("Câu hỏi không hợp lệ (phải có ít nhất 1 đáp án đúng và điểm > 0).")
                    continue
                
                # Thêm câu hỏi vào quiz trong manager
                quiz_manager.quizzes[quizid].add_question(question)
                print("Đã thêm câu hỏi thành công!")
            
            except ValueError:
                print("Lỗi nhập liệu.")
                continue

        elif choice == "7":
            print("Đã đăng xuất khỏi Teacher Menu.")
            return 

        else:
            print("Lựa chọn không hợp lệ! Vui lòng nhập lại.")

def main():
    manager = UserManager(data_file)
    admin_system = Admin(manager)
    quiz_manager = QuizManager()      
    attempt_manager = attempt_func.AttemptManager()
    
    while True:
        print("\n--- HỆ THỐNG ĐĂNG NHẬP ---")
        username_input = input("USER: ")
        password_input = getpass.getpass(prompt='PASSWORD: ')
        
        user_info = manager.get_user_data(username_input)
        
        # SỬA: Sử dụng verify_password để kiểm tra Hash
        if user_info is None or not verify_password(user_info.get('password'), password_input):
            print("Tên đăng nhập hoặc mật khẩu không chính xác. Vui lòng thử lại.")
            continue
            
        role = user_info.get('role')
        print(f"Đăng nhập thành công: {user_info.get('fullname')} ({role})")
        
        if role == 'Admin':
            admin_system.login(username_input, password_input) # Lưu ý: hàm login trong Admin chưa sửa nhận hash, nhưng chỉ để in menu
        elif role == 'Teacher':
            # SỬA: Khởi tạo Teacher đúng tham số mới
            current_user_obj = teacher_func.Teacher(manager, username_input, user_info, quiz_manager) 
            run_teacher_menu(current_user_obj, quiz_manager)
        elif role == 'Student':
            current_user_obj = student_func.Student(
                user=user_info, 
                quiz_manager=quiz_manager, 
                attempt_manager=attempt_manager
            )
            current_user_obj.menu() 
        else:
            print("Lỗi vai trò không xác định.")

if __name__ == "__main__":
    main()