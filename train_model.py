import os
import numpy as np
import cv2
from sklearn.preprocessing import LabelEncoder
from deepface import DeepFace
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import f1_score

# دالة لتحميل الصور من المجلد
def load_images_from_folder(folder, model_name='ArcFace'):
    images = []
    labels = []

    for subdir in os.listdir(folder):
        subdir_path = os.path.join(folder, subdir)
        if os.path.isdir(subdir_path):
            for img_name in os.listdir(subdir_path):
                img_path = os.path.join(subdir_path, img_name)
                if img_path.endswith('.jpg') or img_path.endswith('.png'):
                    try:
                        # استخراج التمثيلات باستخدام ArcFace
                        img = DeepFace.represent(img_path=img_path, model_name=model_name, enforce_detection=False)
                        if img:
                            # إضافة التمثيل للصورة
                            images.append(img[0]['embedding'])
                            labels.append(subdir)  # استخدام اسم المجلد كالتسمية
                    except Exception as e:
                        print(f"Error processing image {img_path}: {e}")

    return np.array(images), labels

# دالة لتدريب النموذج
def train_model(model_name='ArcFace'):
    dataset_path = 'dataset'  # مسار مجلد البيانات
    print("[+] Loading data...")
    images, labels = load_images_from_folder(dataset_path, model_name)

    # التحقق من وجود بيانات
    if len(images) == 0 or len(labels) == 0:
        print("[!] No data for training.")
        return

    # تحويل التسميات إلى أرقام باستخدام LabelEncoder
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)

    # تقسيم البيانات إلى بيانات تدريب واختبار
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(images, labels_encoded, test_size=0.2, random_state=42)

    # إنشاء نموذج Keras بسيط
    model = Sequential([
        Dense(512, input_dim=X_train.shape[1], activation='relu'),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(len(np.unique(labels_encoded)), activation='softmax')
    ])

    # تجميع النموذج
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # تدريب النموذج
    print("[+] Training the model...")
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

    # طباعة نتائج التدريب والتحقق
    print("\nTraining Accuracy: ", history.history['accuracy'][-1])
    print("Training Loss: ", history.history['loss'][-1])
    print("Validation Accuracy: ", history.history['val_accuracy'][-1])
    print("Validation Loss: ", history.history['val_loss'][-1])

    # حساب F1-Score
    y_pred = np.argmax(model.predict(X_test), axis=1)
    f1 = f1_score(y_test, y_pred, average='weighted')
    print("F1-Score: ", f1)

    # حفظ النموذج المدرب
    model.save("face_recognition_model.h5")
    print("[+] The trained model has been saved.")

if __name__ == "__main__":
    # هنا يمكن تحديد النموذج الذي تريد استخدامه، سواء كان "ArcFace" أو "VGG-Face"
    train_model(model_name='ArcFace')  # لاستخدام ArcFace
    #train_model(model_name='VGG-Face')  # لاستخدام VGG-Face
