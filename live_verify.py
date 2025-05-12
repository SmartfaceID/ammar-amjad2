import cv2
import os
import numpy as np
from deepface import DeepFace
import datetime
import pyttsx3

# دالة لتحويل النص إلى صوت
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# دالة لقص الصورة بشكل دائري
def circular_crop(img, size=300):
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    radius = min(center[0], center[1], size // 2)

    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)

    circular_img = cv2.bitwise_and(img, img, mask=mask)
    return circular_img

# دالة للتحقق من الوجه عبر الكاميرا باستخدام ArcFace و DeepFace
def verify_live_face():
    print("[+] Opening the camera now...")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[!] Could not open the camera.")
        return

    start_time = datetime.datetime.now()
    detected = False
    frame = None

    while (datetime.datetime.now() - start_time).seconds < 15:
        ret, frame = cap.read()
        if not ret:
            print("[!] Failed to grab frame.")
            continue

        frame_resized = cv2.resize(frame, (300, 300))
        circ_frame = circular_crop(frame_resized)

        black_bg = np.zeros((400, 400, 3), dtype=np.uint8)
        x_offset = (400 - circ_frame.shape[1]) // 2
        y_offset = (400 - circ_frame.shape[0]) // 2
        black_bg[y_offset:y_offset+circ_frame.shape[0], x_offset:x_offset+circ_frame.shape[1]] = circ_frame

        cv2.imshow("Capturing Face...", black_bg)
        cv2.waitKey(1)

        # محاولة التحقق من الوجه باستخدام DeepFace و ArcFace
        try:
            temp_img_path = "captured_face.jpg"
            cv2.imwrite(temp_img_path, frame)

            # التحقق باستخدام ArcFace و DeepFace
            result_deepface = DeepFace.find(img_path=temp_img_path, db_path="dataset", model_name="ArcFace", enforce_detection=True)
            
            if len(result_deepface) > 0:
                identity_path = result_deepface[0].identity.values[0]
                person_name = os.path.basename(os.path.dirname(identity_path))
                print(f"[✓] The person was identified by ArcFace: {person_name}")
                speak(f"The person has been identified as {person_name}")

                # تخزين الصورة في مجلد الشخص
                person_dir = os.path.join("dataset", person_name)
                os.makedirs(person_dir, exist_ok=True)

                now = datetime.datetime.now()
                timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
                save_path = os.path.join(person_dir, f"{timestamp}.jpg")
                cv2.imwrite(save_path, frame)

                print(f"[+] Image saved at: {save_path}")
                detected = True
                break

            else:
                print("[!] No match found in ArcFace. Trying DeepFace...")

                result_deepface = DeepFace.find(img_path=temp_img_path, db_path="dataset", enforce_detection=True)
                
                if len(result_deepface) > 0:
                    identity_path = result_deepface[0].identity.values[0]
                    person_name = os.path.basename(os.path.dirname(identity_path))
                    print(f"[✓] The person was identified by DeepFace: {person_name}")
                    speak(f"The person has been identified as {person_name}")

                    # تخزين الصورة في مجلد الشخص
                    person_dir = os.path.join("dataset", person_name)
                    os.makedirs(person_dir, exist_ok=True)

                    now = datetime.datetime.now()
                    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
                    save_path = os.path.join(person_dir, f"{timestamp}.jpg")
                    cv2.imwrite(save_path, frame)

                    print(f"[+] Image saved at: {save_path}")
                    detected = True
                    break
                else:
                    print("[!] No match found in DeepFace either.")
                    speak("No match found")

        except Exception as e:
            print(f"[!] Error during verification: {e}")

    cap.release()
    cv2.destroyAllWindows()

    # إذا لم يتم التعرف على الشخص
    if not detected:
        print("[!] No match found. Saving to 'unknown' folder.")
        speak("No match found")
        
        # مجلد unknown داخل dataset
        unknown_dir = os.path.join("dataset", "unknown")
        os.makedirs(unknown_dir, exist_ok=True)

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        save_path = os.path.join(unknown_dir, f"{timestamp}.jpg")
        cv2.imwrite(save_path, frame)

        print(f"[+] Unknown image saved at: {save_path}")

    # حذف الصورة المؤقتة
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)

# الدالة الرئيسية لتشغيل البرنامج
def main():
    while True:
        print("\nChoose an option:")
        print("1. Verify identity via camera")
        print("2. Exit")

        choice = input("Enter the appropriate number: ")

        if choice == "1":
            print("[+] Starting identity verification via camera...")
            verify_live_face()
        elif choice == "2":
            print("[!] Program terminated.")
            break
        else:
            print("[!] Invalid option. Please try again.")

if __name__ == "__main__":
    main()
