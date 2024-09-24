// int sensor_pins[] = {A0, A1, A2, A3, A4};
int servo_pins[]  = {2, 3, 4, 5, 6};
int LED_pins[]    = {13,12,11,10,9};

int feedback_switch[3] ;

// int sensor_val[5];  
// int current_angle[5];

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

void feed_back(int switch_pin, int servo_pin, int LED_pin) // 센서 각도가 현재 서보모터 각도보다 크면 피드백 제공
{
      if (switch_pin == 1)  // 센서 값이 현재 각도보다 크면
      {
        Serial.print(servo_pin-1); Serial.println(" finger feedback on");
        set_servo_angle(180, servo_pin);  // 서보모터를 180도로 움직임
        digitalWrite(LED_pin,HIGH);
      }
      else
      {
        Serial.print(servo_pin-1); Serial.println(" finger feedback off");
        set_servo_angle(0, servo_pin);    // 서보모터를 0도로 움직임
        digitalWrite(LED_pin,LOW);
      }
}

void get_data()
{
  if (Serial.available() > 0) 
  {
    String input = Serial.readStringUntil('\n');

    // Verify that input contains exactly 9 commas (10 values)
    int commas = 0;
    for (int j = 0; j < input.length(); j++) {
      if (input.charAt(j) == ',') {
        commas++;
      }
    }

    if (commas == 3) {  // Only proceed if we have 10 values
      int startIdx = 0;
      int endIdx = 0;
      for (int i = 0; i < 4; i++) {
        endIdx = input.indexOf(',', startIdx);
        if (endIdx == -1) {
          feedback_switch[i] = input.substring(startIdx).toInt();
          break;
        } else {
          feedback_switch[i] = input.substring(startIdx, endIdx).toInt();
          startIdx = endIdx + 1;
        }
      }
    } else {
      // Serial.println("Error: Invalid input. Please enter 10 comma-separated values.");
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
    // sensor_val[i] = analogRead(sensor_pins[i]); // 저항 센서 값 읽기
    get_data();// Serial 통신으로 값 읽어오기 (향후 추가)
  }
  
  feed_back(feedback_switch[0],servo_pins[0],LED_pins[0]);
  feed_back(feedback_switch[1],servo_pins[1],LED_pins[1]);
  feed_back(feedback_switch[1],servo_pins[2],LED_pins[2]);
  feed_back(feedback_switch[2],servo_pins[3],LED_pins[3]);
  feed_back(feedback_switch[2],servo_pins[4],LED_pins[4]);  
  // delay(1000);  // 피드백 후 1초 대기 
}
