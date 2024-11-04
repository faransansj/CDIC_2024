# CDIC 2024 
## Robot Arm 
Robot Arm의 구동부는 크게 두개로 나뉜다. 손가락 + 팔  
손가락은 MG90와 같은 서보모터를 이용한다.  

팔은 높은 토크를 요하기 때문에 손가락과 다른모터를 사용하며 이때 필요한 전원이 크기 때문에 Servomotor driver에 연결하고 PSU로 부터 전원을 공급받고자 한다.  


---

## feedback glove
1) 시리얼 통신으로 값 받기 (serial_get)  
  시리얼 통신을 통해 각 서보 모터의 각도 값을 받아옵니다. 데이터가 없을 경우 에러 처리를 위해 999 값을 반환합니다.  
2) 피드백 제어 (feed_back)  
  센서 값이 현재 서보 모터의 각도보다 크면, 서보를 180도로 이동시키고 LED를 켭니다. 그렇지 않으면 서보를 0도로 이동시키고 LED를 끕니다.  
  각 서보 모터별로 피드백을 제공하며, 시리얼 통신에서 값을 읽지 못한 경우 에러 처리를 진행합니다.  

### value
  sensor_pins[]    : 각 가변저항 센서가 연결된 아날로그 핀 배열입니다.  
  servo_pins[]     : 서보 모터가 연결된 디지털 출력 핀 배열입니다.  
  LED_pins[]       : LED가 연결된 디지털 출력 핀 배열입니다.  
  sensor_val[]     : sensor pins 에서 읽어들인 값을 저장하는 배열입니다.  
  current_angle[]  : 시리얼 통신을 통해 받은 각도를 저장하는 배열입니다.  
  
### pin map 
|    |새끼  |약지 |중지 |검지 |엄지  |
|---  |---  |---  |---  |---  |---  |
|servo|12   |11   |10   |9    |8    | 
|LED  |6    |5    |3    |4    |2    |

-> pin map은 바뀔 수 있음 

### To do 

[] 에러 처리: 각 서보 모터별로 에러를 독립적으로 처리해 시스템이 중단되지 않도록 수정하는 것이 바람직합니다.  
[] 비차단 방식 코드: delay() 대신 millis()를 사용해 비차단 방식으로 코드를 작성하면 다른 작업이 동시에 진행될 수 있습니다.  
[] 디버깅 강화: 시리얼 통신과 센서 입력에 대한 추가적인 디버깅 메시지를 추가해 문제를 파악하기 쉽게 만들 수 있습니다.  
[] 블루투스 통신 : HC-06 모듈 이용해서 블루투스 통신으로 데이터값 받아오는 거 구현 

---

## Raspberry pi server
- 개요  
이 파이썬 스크립트는 TCP 소켓 서버를 설정하여 클라이언트로부터 데이터를 수신하고, 받은 데이터에서 서보 모터 값을 추출한 뒤, 이를 시리얼 연결을 통해 아두이노로 전송합니다. 또한, 아두이노로부터의 응답을 받을 수 있는 기능도 포함되어 있습니다. 이 스크립트는 지정된 IP 주소와 포트에서 연결을 수락하고, 클라이언트의 메시지에서 서보 데이터를 추출하여 아두이노와 시리얼 통신을 진행합니다.  
- request  
socket: 서버와 클라이언트 간 TCP 소켓 통신을 위한 모듈.  
serial: 아두이노와의 시리얼 통신을 위한 pySerial 패키지의 일부.  
re: 수신된 데이터를 정규 표현식으로 처리하기 위한 모듈.  
note) Pyserial만 설치 진행하면 됩니다. 나머지는 기본 RPI 라이브러리  

```powershell
pip install pyserial
```

### Setup
getData.py를 RPI에서 수정할려면 해당 파일이 있는 디렉터리로 이동후 아래 명령어를 입력해 수정을 합니다.  
```
sudo nano getData.py
```
여기서 수정할 부분은 start_server 함수입니다.  
start_server(host='192.xxx.xxx.xxx', port=65432, serial_port='/dev/ttyUSB0', baudrate=9600):  
host : RPI에 할당된 IP 주소 입력    
port : 나도 뭔지 모름   
serial_port : MCU와 USB로 연결된 포트, 가끔 포트가 다른걸로 인식되는 경우 있음 이때 ttyUSB0에서 숫자 바꿔주셈   
-> 숫자 확인하는 방법  
```
lsusb
```
위의 명령어 입력하면 현재 RPI가 연결된 USB port가 뜰거임 그걸로 바꾸면 됩니다.  
baudrate : Arudino의 통신속도 9600이 국밥임  