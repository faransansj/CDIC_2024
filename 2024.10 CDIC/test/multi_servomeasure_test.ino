int servo_pins[]  = {12, 10, 11, 9, 8};  // 서보모터 핀 번호
int servo_analogue_pins[] = {A0, 0, A1, 0, A2};  // 아날로그 입력 핀

int servoValue0Deg[5];  // 0도에서의 아날로그 값
int servoValue180Deg[5];  // 180도에서의 아날로그 값

void set_servo_angle(int angle, int servoPin)  // 서보모터 각도 제어 함수
{
  int pulseWidth = map(angle, 0, 180, 1000, 2000);  // 각도에 따른 펄스 폭 계산

  for (int i = 0; i < 50; i++)  // 50Hz 신호 생성: 20ms 주기
  {  
    digitalWrite(servoPin, HIGH);           
    delayMicroseconds(pulseWidth);          
    digitalWrite(servoPin, LOW);            
    delayMicroseconds(20000 - pulseWidth);  
  }
}

void calibration(int pin, int Apin, int i) 
{
  // 0도에서 캘리브레이션
  set_servo_angle(0, pin);
  delay(1000);  // 서보 모터가 0도에 도달할 시간을 줌
  servoValue0Deg[i] = analogRead(Apin);  // 0도에서의 아날로그 값 저장
  Serial.println("Pot value for 0 deg: " + String(servoValue0Deg[i]));

  // 180도에서 캘리브레이션
  set_servo_angle(180, pin);
  delay(1000);  // 서보 모터가 180도에 도달할 시간을 줌
  servoValue180Deg[i] = analogRead(Apin);  // 180도에서의 아날로그 값 저장
  Serial.println("Pot value for 180 deg: " + String(servoValue180Deg[i]));

  // 서보 모터를 초기 위치로 되돌림
  set_servo_angle(0, pin);
}

float estimateAngle(int analogValue, int i) 
{
  // 캘리브레이션 값이 유효한지 확인
  if (servoValue0Deg[i] == servoValue180Deg[i]) {
    return -1;  // 분모가 0이 되는 경우를 방지
  }
  
  // 0도와 180도의 캘리브레이션 값을 기반으로 기울기(m)와 절편(b) 계산
  float m = 180.0 / (servoValue0Deg[i] - servoValue180Deg[i]);  // 아날로그 값의 변화에 따른 각도 변화량
  float b = -m * servoValue180Deg[i];  // 절편 계산
  return m * analogValue + b;  // 아날로그 값을 이용해 추정 각도 계산
}

void setup()
{
  Serial.begin(9600);  // 시리얼 통신 시작
  for (int i = 0; i < 5; i++) {  // 서보 핀을 출력 모드로 설정
    pinMode(servo_pins[i], OUTPUT);
  }

  // 서보 모터의 캘리브레이션 실행 (0도와 180도의 아날로그 값을 읽음)
  for (int i = 0; i < 5; i += 2) {
    if (servo_analogue_pins[i] != 0) {  // 아날로그 핀 값이 유효한지 확인
      calibration(servo_pins[i], servo_analogue_pins[i], i);
    }
  }
}

void loop()
{
  for (int i = 0; i < 5; i += 2) {
    if (servo_analogue_pins[i] != 0) {  // 아날로그 핀 값이 유효한지 확인
      for (int angle = 0; angle <= 180; angle += 45) {
        set_servo_angle(angle, servo_pins[i]);  // 서보 모터 각도 제어

        int analogValue = analogRead(servo_analogue_pins[i]);  // 아날로그 값 읽기
        float estimatedAngle = estimateAngle(analogValue, i);  // 추정 각도 계산

        // 실제 각도, 아날로그 값 및 추정 각도 출력
        Serial.print("Actual Angle: ");
        Serial.print(angle);
        Serial.print(" | Analog Value: ");
        Serial.print(analogValue);
        Serial.print(" | Estimated Angle: ");
        Serial.println(estimatedAngle);

        delay(500);  // 약간의 지연을 줘서 출력이 너무 빠르지 않게 함
      }
    }
  }
}
