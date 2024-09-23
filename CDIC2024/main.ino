#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// PCA9685 드라이버 객체 생성
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// 서보모터 각도에 따른 펄스 길이 설정 (서보모터의 특성에 따라 조정 가능)
#define SERVOMIN  150  // 0도
#define SERVOMAX  600  // 180도

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60);  // 60Hz 설정
}

void loop() {
  // 시리얼 데이터가 들어왔는지 확인
  if (Serial.available() > 0) {
    // 시리얼 데이터를 읽어와서 저장
    String input = Serial.readStringUntil('\n');

    // 각 서보모터에 해당하는 각도 값 추출
    int angles[10];  // 10개의 서보모터 각도 값을 저장할 배열
    int startIdx = 0;
    int endIdx = 0;
    for (int i = 0; i < 10; i++) {
      endIdx = input.indexOf(',', startIdx);
      if (endIdx == -1) {
        angles[i] = input.substring(startIdx).toInt();
        break;
      } else {
        angles[i] = input.substring(startIdx, endIdx).toInt();
        startIdx = endIdx + 1;
      }
    }


    for (int i = 0; i < 10; i++) {
      int pulseLen = map(angles[i], 0, 180, SERVOMIN, SERVOMAX);
      pwm.setPWM(i, 0, pulseLen);  // i 번째 서보모터 제어
    }
  }
}
