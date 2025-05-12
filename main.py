import speech_recognition as sr
import pyttsx3
import time
from train_model import train_model
from verify_face import verify_face
from models.extract_frames import extract_all_videos
from live_verify import verify_live_face
from add_person import add_new_person_to_dataset
from login_auth import login_with_credentials

# تهيئة مكتبة الصوت
engine = pyttsx3.init()

# دالة لتحويل النص إلى صوت
def speak(text):
    engine.say(text)
    engine.runAndWait()

# دالة لاكتشاف الكلمة المفتاحية "Hey System"
def listen_for_keyword():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("[INFO] Listening for ''Hi System'...")
    speak("I am listening. Say 'Hi System'")

    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=10)
                command = recognizer.recognize_google(audio, language='en-US').lower()
                print(f"[DEBUG] Detected command: {command}")
                if "hey system" in command or "hi system" in command:
                    speak("Hello, welcome to the Face Authentication System. How can I assist you?")
                    return True
            except sr.WaitTimeoutError:
                print("[INFO] Timeout. No voice detected.")
            except sr.UnknownValueError:
                print("[INFO] Could not understand the audio.")
            except Exception as e:
                print(f"[ERROR] {str(e)}")
            except sr.WaitTimeoutError:
                print("[INFO] Timeout. لم يتم الكشف عن أي صوت.")
            except sr.UnknownValueError:
                print("[INFO] لم أتمكن من فهم الصوت.")
            except Exception as e:
                print(f"[ERROR] {str(e)}")

# دالة الاستماع للأوامر
def listen_for_commands():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    commands = {
        "login": "تسجيل الدخول",
        "verify face": "التحقق عن طريق الكاميرا",
        "train model": "تدريب النموذج",
        "add person": "إضافة شخص جديد"
    }

    while True:
        speak("ما الذي تريد فعله؟ يمكنك قول: تسجيل الدخول، التحقق عن طريق الكاميرا، تدريب النموذج، أو إضافة شخص جديد")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=10)
                command = recognizer.recognize_google(audio, language='en-US').lower()
                print(f"[DEBUG] Detected command: {command}")

                for key, value in commands.items():
                    if key in command:
                        speak(f"تم اختيار {value}")
                        return key

                speak("لم أفهم الأمر. حاول مرة أخرى.")
            except sr.WaitTimeoutError:
                speak("لم أسمع أي أمر. هل تريد محاولة أخرى؟")
            except sr.UnknownValueError:
                speak("لم أتمكن من فهم الصوت. حاول مرة أخرى.")
            except Exception as e:
                print(f"[ERROR] {str(e)}")

# دالة تنفيذ الأوامر
def execute_command(command):
    if command == "login":
        speak("Do you want to login using username and password or via camera?")
        # Listen for the login method
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=10)
                method = recognizer.recognize_google(audio, language='en-US').lower()
                print(f"[DEBUG] Detected login method: {method}")
                if "username" in method or "password" in method:
                    speak("Logging in using username and password")
                    login_with_credentials()
                elif "camera" in method:
                    speak("Logging in using camera")
                    verify_live_face()
                else:
                    speak("Invalid login method. Try again.")
            except sr.WaitTimeoutError:
                speak("No response detected. Try again.")
            except sr.UnknownValueError:
                speak("Could not understand the audio. Try again.")
            except Exception as e:
                print(f"[ERROR] {str(e)}")
    elif command == "verify face":
        speak("Verifying face via camera...")
        verify_live_face()
    elif command == "train model":
        speak("Training the model...")
        train_model()
    elif command == "add person":
        speak("Adding a new person to the system...")
        add_new_person_to_dataset()
    else:
        speak("Unknown command. Try again.")
        speak("الأمر غير معروف. حاول مرة أخرى.")

# القائمة النصية
def main_menu():
    while True:
        print("\nChoose an option:")
        print("1. Extract images from videos")
        print("2. Train the model")
        print("3. Verify identity from an image")
        print("4. Verify identity via camera")
        print("5. Add new person to the system")
        print("6. Login to the system")   
        print("7. Use Voice Control")

        choice = input("Enter the appropriate number (1 to 7): ")

        if choice == "1":
            extract_all_videos()
        elif choice == "2":
            train_model()
        elif choice == "3":
            verify_face()
        elif choice == "4":
            verify_live_face()
        elif choice == "5":
            add_new_person_to_dataset()
        elif choice == "6":
            login_with_credentials()
        elif choice == "7":
            if listen_for_keyword():
                command = listen_for_commands()
                execute_command(command)
        else:
            print("[!] Invalid option. Please try again.")

        continue_choice = input("\nDo you want to continue (yes/no): ")
        if continue_choice.lower() != "yes":
            print("[!] Program terminated.")
            break

if __name__ == "__main__":
    main_menu()