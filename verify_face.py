import os
import cv2
from deepface import DeepFace
import shutil

def verify_face():
    print("[+] Choose an image to verify...")

    # طلب مسار الصورة
    img_path = input("Enter the image path for verification: ")

    if not os.path.exists(img_path):
        print("[!] The path is incorrect. Please try again.")
        return

    # خيارات طريقة حساب المسافة
    distance_metrics = ["cosine", "euclidean", "euclidean_l2"]
    print("\nChoose a distance metric:")
    for i, metric in enumerate(distance_metrics, start=1):
        print(f"{i}. {metric}")
    
    metric_choice = input("Enter the number corresponding to the distance metric: ")

    try:
        distance_metric = distance_metrics[int(metric_choice) - 1]
    except (IndexError, ValueError):
        print("[!] Invalid choice. Defaulting to cosine.")
        distance_metric = "cosine"

    # التحقق من الوجه باستخدام ArcFace
    try:
        print(f"\n[+] Verifying using ArcFace model and metric: {distance_metric}")

        result = DeepFace.find(
            img_path=img_path,
            db_path="dataset",  # Ensure the dataset path is correct
            model_name="ArcFace",  # تغيير من OpenFace إلى ArcFace
            distance_metric=distance_metric,
            enforce_detection=True  # Ensure detection before comparison
        )

        if len(result) > 0:
            print("[✓] Face recognized.")
            # استخراج أول نتيجة مطابقة
            best_match = result.iloc[0]
            identity_path = best_match.identity
            person_name = os.path.basename(os.path.dirname(identity_path))

            print(f"Person identified: {person_name}")

            # تخزين الصورة في مجلد الشخص
            person_dir = os.path.join("dataset", person_name)
            os.makedirs(person_dir, exist_ok=True)
            filename = os.path.basename(img_path)
            save_path = os.path.join(person_dir, filename)
            shutil.copy(img_path, save_path)

            print(f"[+] Image saved to: {save_path}")

        else:
            print("[!] No match found.")
            # إذا لم يتم التعرف على الشخص، تخزن الصورة في مجلد "unknown"
            unknown_dir = os.path.join("dataset", "unknown")
            os.makedirs(unknown_dir, exist_ok=True)
            filename = os.path.basename(img_path)
            unknown_img_path = os.path.join(unknown_dir, filename)
            shutil.copy(img_path, unknown_img_path)

            print(f"[+] Image saved to: {unknown_img_path}")

    except Exception as e:
        print(f"[!] Verification failed: {e}")

if __name__ == "__main__":
    verify_face()
