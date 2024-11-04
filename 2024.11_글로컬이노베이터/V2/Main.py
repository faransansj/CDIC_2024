import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import hashlib
import numpy as np
import os

# 메인 윈도우 생성
root = tk.Tk()
root.title("LSB 워터마킹 프로그램")

# 전역 변수 초기화
uploaded_image = None
encoded_image = None
hash_value = None

# 이미지 업로드 함수
def upload_image():
    global uploaded_image, img_display
    file_path = filedialog.askopenfilename()
    if file_path:
        uploaded_image = Image.open(file_path)
        uploaded_image.thumbnail((300, 300))
        img_display = ImageTk.PhotoImage(uploaded_image)
        img_label.configure(image=img_display)
        img_label.image = img_display
        hash_label.config(text="")
        messagebox.showinfo("이미지 업로드", "이미지가 성공적으로 업로드되었습니다.")

# 이미지 인코딩 함수
def encode_image():
    global uploaded_image, encoded_image, hash_value
    if uploaded_image:
        # 이미지 해시값 생성
        img_bytes = uploaded_image.tobytes()
        hash_value = hashlib.sha256(img_bytes).hexdigest()
        
        # 해시 값을 이진 데이터로 변환
        binary_hash = ''.join(format(ord(char), '08b') for char in hash_value)
        
        # 워터마킹을 위한 이미지 변환
        img_array = np.array(uploaded_image.convert('RGB'))
        img_flat = img_array.flatten()
        
        # 이미지의 크기 확인
        if len(binary_hash) > len(img_flat):
            messagebox.showerror("오류", "이미지에 해시 값을 숨기기에 크기가 부족합니다.")
            return
        
        # LSB를 통한 워터마킹
        for i in range(len(binary_hash)):
            img_flat[i] = (img_flat[i] & 0b11111110) | int(binary_hash[i])
        
        encoded_array = img_flat.reshape(img_array.shape)
        encoded_image = Image.fromarray(encoded_array.astype('uint8'), 'RGB')
        
        # 인코딩된 이미지 표시
        encoded_display = ImageTk.PhotoImage(encoded_image.resize((300, 300)))
        img_label.configure(image=encoded_display)
        img_label.image = encoded_display
        
        # 해시값 표시
        hash_label.config(text=f"해시값: {hash_value}")
        messagebox.showinfo("인코딩 완료", "이미지에 해시 값이 성공적으로 숨겨졌습니다.")
    else:
        messagebox.showerror("오류", "먼저 이미지를 업로드하세요.")

# 인코딩된 이미지 다운로드 함수
def download_image():
    if encoded_image:
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            encoded_image.save(file_path)
            messagebox.showinfo("저장 완료", "이미지가 성공적으로 저장되었습니다.")
    else:
        messagebox.showerror("오류", "인코딩된 이미지가 없습니다.")

# 이미지 디코딩 함수
def decode_image():
    global uploaded_image
    if uploaded_image:
        img_array = np.array(uploaded_image.convert('RGB'))
        img_flat = img_array.flatten()
        
        # LSB로부터 이진 데이터 추출
        binary_data = ''
        for i in range(len(img_flat)):
            binary_data += str(img_flat[i] & 0b00000001)
            
            # 해시 값의 길이에 도달하면 중지
            if len(binary_data) >= 256 * 4:  # SHA-256 해시값은 64자, 각 문자당 8비트
                break
        
        # 이진 데이터를 텍스트로 변환
        decoded_chars = []
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            decoded_chars.append(chr(int(byte, 2)))
        
        decoded_hash = ''.join(decoded_chars).rstrip('\x00')
        
        # 해시값 출력
        messagebox.showinfo("디코딩 결과", f"숨겨진 해시 값: {decoded_hash}")
    else:
        messagebox.showerror("오류", "먼저 이미지를 업로드하세요.")

# GUI 구성 요소 배치
upload_btn = tk.Button(root, text="Upload Image", command=upload_image)
upload_btn.pack(pady=5)

encode_btn = tk.Button(root, text="Encode Image", command=encode_image)
encode_btn.pack(pady=5)

download_btn = tk.Button(root, text="Download Encoded Image", command=download_image)
download_btn.pack(pady=5)

decode_btn = tk.Button(root, text="Decode Image", command=decode_image)
decode_btn.pack(pady=5)

img_label = tk.Label(root)
img_label.pack(pady=5)

hash_label = tk.Label(root, text="")
hash_label.pack(pady=5)

root.mainloop()
