import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import hashlib

# GUI 및 이미지 업로드 기능 구현
def upload_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    # 이미지 열기
    img = Image.open(file_path)

    # 해시 값을 추출하여 GUI에 표시
    extracted_hash = extract_watermark(img)
    if extracted_hash:
        hash_label.config(text=f"Extracted Image Hash: {extracted_hash}")
    else:
        hash_label.config(text="No watermark detected or extraction failed.")


def extract_watermark(img):
    # OpenCV로 이미지 변환
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # 워터마크가 삽입된 위치 추정 (이미지 오른쪽 아래에 위치한다고 가정)
    watermark_width = cv_img.shape[1] // 50
    watermark_height = cv_img.shape[0] // 50
    x_offset = cv_img.shape[1] - watermark_width - 10
    y_offset = cv_img.shape[0] - watermark_height - 10

    # 워터마크 영역 추출
    watermark_region = cv_img[y_offset:y_offset+watermark_height, x_offset:x_offset+watermark_width]

    # 추출된 워터마크를 명확하게 하기 위해 대비 조정
    watermark_region = cv2.convertScaleAbs(watermark_region, alpha=2.0, beta=50)

    # 추출된 워터마크를 바이너리 형태로 변환
    _, binary_watermark = cv2.threshold(cv2.cvtColor(watermark_region, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)

    # 바이너리 데이터를 해시값 문자열로 변환 (단순화된 예시)
    extracted_bits = (binary_watermark.flatten() > 0).astype(int)
    extracted_hash = ''.join(map(str, extracted_bits))

    # 해시 값이 유효한지 확인 (SHA-256 해시의 길이는 64자)
    if len(extracted_hash) >= 64:
        return extracted_hash[:64]
    else:
        return None

# GUI 설정
root = tk.Tk()
root.title("Extract Watermark from Image")

# 업로드 버튼
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack()

# 해시값 표시 라벨
hash_label = tk.Label(root, text="Extracted Image Hash: ")
hash_label.pack()

root.mainloop()