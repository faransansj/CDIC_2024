import cv2
import numpy as np
from scipy.fftpack import dct, idct
from tkinter import Tk, filedialog

# 이미지를 로드합니다.
def load_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    return image

# DCT(이산 코사인 변환)를 사용하여 이미지에서 워터마크 정보를 추출합니다.
def extract_watermark_dct(image):
    # 이미지에 DCT를 적용하여 주파수 성분을 분리합니다.
    dct_transformed = dct(dct(image.T, norm='ortho').T, norm='ortho')
    
    # 일반적으로 워터마크는 고주파 성분에 숨겨져 있으므로, 해당 부분을 추출합니다.
    watermark = dct_transformed[-10:, -10:]  # 고주파 성분 추출
    return watermark

# 해시 값을 계산합니다.
def calculate_hash(watermark):
    # 워터마크 이미지를 이진화하기 전에 데이터 타입을 uint8로 변환합니다.
    watermark_uint8 = np.uint8(cv2.normalize(watermark, None, 0, 255, cv2.NORM_MINMAX))
    
    # 워터마크 이미지를 이진화하여 해시를 계산합니다.
    _, binary_watermark = cv2.threshold(watermark_uint8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 해시 값을 계산하기 위해 이미지를 플래튼(flatten)하고 해시 생성
    hash_value = hash(binary_watermark.tobytes())
    return hash_value

# 메인 함수
def main():
    # 파일 다이얼로그를 사용하여 이미지 경로 선택
    root = Tk()
    root.withdraw()  # GUI 창 숨기기
    image_path = filedialog.askopenfilename(title="이미지 파일 선택", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    
    if not image_path:
        print("이미지 파일이 선택되지 않았습니다.")
        return

    # 이미지 로드
    image = load_image(image_path)
    
    # 워터마크 추출
    watermark = extract_watermark_dct(image)
    
    # 해시 값 계산
    hash_value = calculate_hash(watermark)
    
    print(f"Extracted Watermark Hash: {hash_value}")

# 메인 함수 호출
main()