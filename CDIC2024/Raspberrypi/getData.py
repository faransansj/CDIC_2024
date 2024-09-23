getData.py
import socket
import serial
import re

def start_server(host='192.168.0.12', port=65432, serial_port='/dev/ttyUSB0', baudrate=9600):
    # 아두이노와 시리얼 통신 설정
    ser = serial.Serial(serial_port, baudrate, timeout=0.4)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")

                # 데이터를 지속적으로 수신
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break  # 클라이언트가 연결을 닫으면 루프를 종료
                    #print(f"Received raw data: \n{data}")

                    # 데이터를 슬라이싱하여 서보모터 값 추출
                    servo_values = parse_servo_data(data)
                    if servo_values:
                        # 가장 최근데이터 읽어오기
                        servo_values = servo_values[-10:]
                        # 데이터를 아두이노에 보내기 위한 문자열로 변환
                        servo_command = ",".join(servo_values) + "\n"
                        print(f"Sending to Arduino: {servo_command}")

                        # 아두이노로 시리얼 데이터 전송
                        ser.write(servo_command.encode())
                        #print(servo_command.encode())

                        # 아두이노로부터의 응답(필요한 경우)
                        arduino_response = ser.readline().decode().strip()
                        if arduino_response:
                            print(f"Arduino response: {arduino_response}")

def parse_servo_data(data):
    # 정규 표현식을 사용하여 "servoN : X" 패턴을 찾아 숫자 값만 추출
    matches = re.findall(r"servo\d+\s*:\s*(\d+)", data)
    return matches

if __name__ == "__main__":
    start_server()
