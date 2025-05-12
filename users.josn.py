import json
from getpass import getpass

def login_with_credentials():
    try:
        # تحميل بيانات المستخدمين من ملف JSON
        with open('users.json', 'r') as file:
            users = json.load(file)

        # طلب اسم المستخدم وكلمة المرور
        username = input("Enter username: ")
        password = getpass("Enter password: ")  # هنا تم تعديل السطر لطلب كلمة مرور مخفية

        # التحقق من صحة اسم المستخدم وكلمة المرور
        if username in users and users[username]["password"] == password:
            print(f"[+] Welcome {username}!")
        else:
            print("[!] Invalid username or password.")
    except FileNotFoundError:
        print("[!] users.json not found.")

# استدعاء دالة تسجيل الدخول
login_with_credentials()
