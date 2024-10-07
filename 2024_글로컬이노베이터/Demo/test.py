import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import hashlib
import uuid
import cv2
import numpy as np
import torch

# GUI 및 이미지 업로드 기능 구현
def upload_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # 이미지 열기
    img = Image.open(file_path)
    
    # 이미지 ID 및 해시 생성
    img_id = str(uuid.uuid4())
    img_hash = hashlib.sha256(img.tobytes()).hexdigest()

    # 해시 값을 워터마크로 삽입하기 위한 작업
    img_with_watermark = add_watermark(img, img_hash)

    # Tkinter에서 표시할 수 있는 형식으로 변환
    img_tk = ImageTk.PhotoImage(img_with_watermark)
    image_label.config(image=img_tk)
    image_label.image = img_tk

    # ID와 해시값을 GUI에 표시
    id_label.config(text=f"Image ID: {img_id}")
    hash_label.config(text=f"Image Hash: {img_hash}")


def add_watermark(img, text):
    # OpenCV로 이미지 변환
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    # 워터마크 추가 - 사람의 눈에 보이지 않도록 매우 작은 패턴으로 삽입
    # 워터마크로 사용할 작은 패턴 생성 (예: 랜덤한 비트 패턴)
    watermark = np.random.randint(0, 2, (2, 2), dtype=np.uint8) * 255
    watermark = cv2.resize(watermark, (cv_img.shape[1] // 50, cv_img.shape[0] // 50), interpolation=cv2.INTER_NEAREST)

    # 워터마크를 이미지의 특정 위치에 투명하게 삽입
    x_offset = cv_img.shape[1] - watermark.shape[1] - 10
    y_offset = cv_img.shape[0] - watermark.shape[0] - 10
    alpha = 0.1  # 워터마크의 투명도 (사람의 눈에 보이지 않게 매우 낮게 설정)
    for c in range(0, 3):
        cv_img[y_offset:y_offset+watermark.shape[0], x_offset:x_offset+watermark.shape[1], c] = (
            (1 - alpha) * cv_img[y_offset:y_offset+watermark.shape[0], x_offset:x_offset+watermark.shape[1], c] +
            alpha * watermark
        )

    # 다시 PIL 이미지로 변환
    img_with_watermark = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))
    return img_with_watermark

# AI 학습 방해 패턴 적용 (논문 기반으로 단순화된 예시)
def apply_adversarial_pattern(img):
    # OpenCV로 이미지 변환
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # 간단한 학습 방해 패턴 적용 (랜덤 노이즈)
    noise = np.random.normal(0, 25, cv_img.shape).astype(np.uint8)
    adversarial_img = cv2.add(cv_img, noise)

    # 다시 PIL 이미지로 변환
    return Image.fromarray(cv2.cvtColor(adversarial_img, cv2.COLOR_BGR2RGB))


# GUI 설정
root = tk.Tk()
root.title("Image Upload and Watermark")

# 업로드 버튼
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack()

# 이미지 표시 라벨
image_label = tk.Label(root)
image_label.pack()

# ID 및 해시값 표시 라벨
id_label = tk.Label(root, text="Image ID: ")
id_label.pack()

hash_label = tk.Label(root, text="Image Hash: ")
hash_label.pack()

root.mainloop()