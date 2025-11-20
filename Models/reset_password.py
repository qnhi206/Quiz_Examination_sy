import json
import hashlib

data_file = "account.json"

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Load dữ liệu hiện tại
try:
    with open(data_file, 'r', encoding='utf-8') as f:
        users = json.load(f)
    
    # Reset lại toàn bộ mật khẩu về mặc định và Hash lại
    users['admin']['password'] = hash_password("adminpass")
    users['teacher']['password'] = hash_password("teacherpass")
    users['student']['password'] = hash_password("studentpass")
    
    # Lưu lại vào file
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)
        
    print("Đã reset và hash lại mật khẩu thành công!")
    print(f"Admin hash mới: {users['admin']['password']}")

except Exception as e:
    print(f"Lỗi: {e}")