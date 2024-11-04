import cv2
from ultralytics import YOLO
import RPi.GPIO as GPIO 

import alert

import time

# pin map
lock_pin = 23

tilt_switch = 4

boozer = 14
led_Rsig = 15
led_Gsig = 17
led_Bsig = 27
led_gnd = 18

# setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(tilt_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(boozer, GPIO.OUT)

GPIO.setup(led_Rsig, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_Gsig, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_Bsig, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_gnd, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(lock_pin, GPIO.OUT)

GPIO.setwarnings(False) 

if GPIO.input(tilt_switch) == GPIO.LOW:
    while GPIO.input(tilt_switch) == GPIO.HIGH:
        alert.alert_tilt()
    
def capture_and_save(cam_index, file_name):
    # Initialize a VideoCapture object for the given webcam index
    cap = cv2.VideoCapture(cam_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

    if not cap.isOpened():
        print(f"Failed to open camera at index {cam_index}")
        return  # Exit the function if the camera can't be opened

    # Read from the webcam
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(file_name, frame)  # Save the frame as a JPEG file

    # Release the VideoCapture object
    cap.release()

# Capture and save images from webcams 3, 4, 1, and 2 in sequence
capture_and_save(0, 'a14.jpg')
capture_and_save(4, 'a24.jpg')
capture_and_save(2, 'a34.jpg')
capture_and_save(6, 'a44.jpg')


def analyze_environment(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    roi = gray[int(height/2):height, int(width/2):width]
    blurred = cv2.GaussianBlur(roi, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    patterns = analyze_contours(contours)
    return "Sidewalk" if len(patterns) > 600000 else "Road"

def analyze_contours(contours):
    patterns = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        patterns.append((x, y, w, h))
    return patterns
def draw_boxes(image, boxes):
    if not boxes:  # 탐지된 객체가 없는 경우
        cv2.putText(image, "No detection", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        for box in boxes:
            x1, y1, x2, y2 = box
            # cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 녹색 상자
    return image


def draw_text(image, text):
    cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # 빨간색 텍스트
    return image

# 모델 및 이미지 경로 설정
model_path = '/home/pi/kick200.pt'
model_path2 = '/home/pi/kickleft200.pt'
image_paths = ['a14.jpg', 'a24.jpg', 'a34.jpg', 'a44.jpg']

# YOLO 모델 로드
model = YOLO(model_path)
model2 = YOLO(model_path2)

# 킥보드 및 주차 가능 여부 확인
kickboard_detected = False
parking_possible = False

# 각 이미지 처리 및 결과 출력
for i, image_path in enumerate(image_paths):
    image = cv2.imread(image_path)

    if i < 3:  # 첫 세 이미지에 대한 처리
        results = model(image)
        boxes = [box.xyxy[0] for box in results[0].boxes]  # xyxy 포맷으로 상자 좌표 가져오기
        image_with_boxes = draw_boxes(image, boxes)
        cv2.imwrite(f'detected_{image_path}', image_with_boxes)  # 객체가 탐지된 이미지 저장

        if len(results[0].boxes) > 0:
            kickboard_detected = True
            if image_path in ['a14.jpg', 'a34.jpg']:  # model2 사용
                results2 = model2(image)
                boxes2 = [box.xyxy[0] for box in results2[0].boxes]
                image_with_boxes2 = draw_boxes(image, boxes2)
                cv2.imwrite(f'detected2_{image_path}', image_with_boxes2)

                if len(results2[0].boxes) > 0:
                    parking_possible = True

    else:  # a4.jpg에 대한 처리
        area_type = analyze_environment(image)
        text = "ROAD" if area_type == "Road" else "SIDEWALK"
        image_with_text = draw_text(image, text)
        cv2.imwrite(f'detected_{image_path}', image_with_text)

# 결과 요약 출력
if kickboard_detected:
    print("1, 2, 3번 이미지: 주변에 킥보드가 있습니다")
    if parking_possible:
        print("1, 3번 이미지: 주차 OK")
        alert.alert_park(1)
        GPIO.output(lock_pin,1)
        # GPIO.output(led_sig,1)
        # time.sleep(3)
        # GPIO.output(led_sig,0)  
    else:
        print("1, 3번 이미지: 킥보드 옆에 주차하세요!")
else:
    print("1, 2, 3번 이미지: 주변에 킥보드가 없습니다")
    image_path = image_paths[3]
    image = cv2.imread(image_path)
    area_type = analyze_environment(image)
    if area_type == "Road":
        print(f"{image_path}: 차도에 주차하지 마세요!")
        alert.alert_park(1)
        GPIO.output(lock_pin,0)
            # GPIO.output(led_sig,1)
            # time.sleep(3)
            # GPIO.output(led_sig,0)  
    else:
        print(f"{image_path}: 주차가능")
        alert.alert_park(0)
        GPIO.output(lock_pin,1)
            # GPIO.output(led_sig,1)
            # time.sleep(3)
            # GPIO.output(led_sig,0)  
# a4.jpg에 대한 처리

# 이미지 파일 이름
detected_image_paths = ['detected_a1.jpg', 'detected_a2.jpg', 'detected_a3.jpg', 'detected_a4.jpg']

# 각 이미지 파일을 순차적으로 열고 표시
for i, img_path in enumerate(detected_image_paths):
    image = cv2.imread(img_path)
    if image is not None:
        cv2.imshow(f"Image {i+1}", image)
    else:
        print(f"Image {img_path} not found.")

# 모든 이미지가 열린 후에 키보드 입력을 기다림
cv2.waitKey(0)

# 모든 창 닫기
cv2.destroyAllWindows()

# 프로그램이 종료될 떄 gpioclean이 구현 안됨 이거 추가하는게 좋음