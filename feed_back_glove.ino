int sensor_pins[] = {A0, A1, A2, A3, A4};
int servo_pins[]  = {2, 3, 4, 5, 6};
int LED_pins[]    = {13,12,11,10,9};

int sensor_val[5];  
int current_angle[5] = {};

void set_servo_angle(int angle, int servoPin) // 서보모터 각도 제어 함수
{
  int pulseWidth = map(angle, 0, 180, 1000, 2000);  // 각도에 따라 1000us에서 2000us 사이의 펄스 폭 계산

  for (int i = 0; i < 50; i++)  // 50Hz 신호 생성: 20ms 주기 
  {  
    digitalWrite(servoPin, HIGH);           
    delayMicroseconds(pulseWidth);          
    digitalWrite(servoPin, LOW);            
    delayMicroseconds(20000 - pulseWidth);  
  }
}

void feed_back() // 센서 각도가 현재 서보모터 각도보다 크면 피드백 제공
{
  for (int i = 0; i < 5; i++)
  {
    if (current_angle[i] == 999) // 값 읽을때 에러핸들링 
    {break;}
    else
    {
      if (sensor_val[i] > current_angle[i])  // 센서 값이 현재 각도보다 크면
      {
        Serial.print(i); Serial.println(" finger feedback on");
        set_servo_angle(180, servo_pins[i]);  // 서보모터를 180도로 움직임
        digitalWrite(LED_pins[i],HIHG);
      }
      else
      {
        Serial.print(i); Serial.println(" finger feedback off");
        set_servo_angle(0, servo_pins[i]);    // 서보모터를 0도로 움직임
        digitalWrite(LED_pins[i],LOW);
      }
    }
  }
}

void setup()
{
  Serial.begin(9600);
  for (int i = 0; i < 5; i++) // set Servo,LED pins output mode
  {pinMode(servo_pins[i], OUTPUT); pinMode(LED_pins[i],OUTPUT);}
}

void loop()
{
  for (int i = 0; i < 5; i++) 
  {
    sensor_val[i] = analogRead(sensor_pins[i]); // 저항 센서 값 읽기
    // Serial 통신으로 값 읽어오기 (향후 추가)
  }

  feed_back();  // 피드백 함수 호출
  delay(1000);  // 피드백 후 1초 대기 
}
