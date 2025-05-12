# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 20:29:55 2025

@author: Obaid
"""

import os
import cv2
import numpy as np
import datetime
import pyttsx3

# تهيئة محرك الصوت
engine = pyttsx3.init()

# دالة لتحويل النص إلى صوت
def speak(text):
    engine.say(text)
    engine.runAndWait()

# دالة لتدوير الصورة بشكل دائري
def circular_crop(img, size=300):
    h, w = img.shape[:2]
    center = (w // 2, h // 2)
    radius = min(center[0], center[1], size // 2)

    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)

    circular_img = cv2.bitwise_and(img, img, mask=mask)
    return circular_img

# دالة لاستخراج الإطارات من الفيديو
def extract_frames_from_video(video_path, output_dir, frame_count=157):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = max(1, total_frames // frame_count)

    count = 0
    saved_count = 0

    while saved_count < frame_count:
        ret, frame = cap.read()
        if not ret:
            break
        if count % interval == 0:
            img_path = os.path.join(output_dir, f"frame_{saved_count}.jpg")
            cv2.imwrite(img_path, frame)
            saved_count += 1
        count += 1

    cap.release()
    print(f"[+] Extracted {saved_count} images.")

# دالة لتسجيل فيديو الوجه بدون حركة
def record_face_video(person_name):
    duration = 40
    dataset_dir = "dataset"
    video_dir = "videos"  # مسار مجلد الفيديوهات خارج dataset
    os.makedirs(video_dir, exist_ok=True)  # التأكد من وجود المجلد

    # تحديد مسار حفظ الفيديو
    video_path = os.path.join(video_dir, f"{person_name}_face_video.mp4")

    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

    start_time = datetime.datetime.now()

    while (datetime.datetime.now() - start_time).seconds < duration:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Recording - Keep still", frame)
        cv2.waitKey(1)
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # استخراج الصور من الفيديو المسجل
    extract_frames_from_video(video_path, os.path.join(dataset_dir, person_name))  # حفظ الصور داخل dataset
    return True


# دالة لإضافة شخص جديد إلى النظام
def add_new_person_to_dataset():
    person_name = input("[+] Enter the name of the person: ")

    if not person_name.strip():
        print("[!] Name cannot be empty. Exiting...")
        return

    print(f"[+] Recording a 10-second video for {person_name}. Please remain still.")
    if record_face_video(person_name):
        print(f"[+] {person_name} registered successfully.")
    else:
        print(f"[!] Registration failed for {person_name}.")
