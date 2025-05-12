# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 20:04:50 2025

@author: Obaid
"""

import cv2
import os
import datetime
import time

# تحديد المسار الذي سيتم تخزين الصور فيه
output_dir = 'captured_images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# تحميل نموذج كشف الوجه
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# فتح الكاميرا
cap = cv2.VideoCapture(0)

# تسجيل الوقت الحالي
start_time = time.time()

while True:
    # التقاط صورة من الكاميرا
    ret, frame = cap.read()

    if not ret:
        print("فشل في التقاط الصورة")
        break

    # تحويل الصورة إلى صورة رمادية (للتعرف على الوجه)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # اكتشاف الوجوه
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # رسم مستطيل حول الوجه المكتشف
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # استخراج الصورة الملتقطة
        face_img = frame[y:y+h, x:x+w]

        # الحصول على اسم الشخص (في هذا المثال سيكون اسمًا ثابتًا، يمكن تعديله بناءً على التعرف)
        person_name = "person_name"  # يمكن تعديل هذا حسب نظام التعرف على الوجه

        # الحصول على التاريخ والوقت الحالي
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

        # حفظ الصورة في المسار المحدد مع اسم الشخص وتاريخ ووقت الصورة
        filename = f"{output_dir}/{person_name}_{timestamp}.jpg"
        cv2.imwrite(filename, face_img)

    # عرض الصورة في نافذة
    cv2.imshow("Captured Image", frame)

    # التحقق إذا مر 10 ثوانٍ
    if time.time() - start_time > 10:
        print("تم التقاط الصور لمدة 10 ثوانٍ، سيتم إغلاق الكاميرا.")
        break

    # إغلاق الكاميرا عند الضغط على مفتاح 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# إغلاق الكاميرا
cap.release()
cv2.destroyAllWindows()
