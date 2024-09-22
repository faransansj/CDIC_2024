int servo_pins[]  = {12,11,10,9,8};
int LED_pins[]    = {6,5,3,4,2};

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
    Serial.print(i); Serial.println(" finger feedback on");
    set_servo_angle(180, servo_pins[i]);  // 서보모터를 180도로 움직임
    digitalWrite(LED_pins[i],HIGH);
      delay(500);
    Serial.print(i); Serial.println(" finger feedback off");
    set_servo_angle(0, servo_pins[i]);    // 서보모터를 0도로 움직임
    digitalWrite(LED_pins[i],LOW);
      delay(00);
  }
}
