const int SwitchPin1 = 12; const int SwitchPin2 = 11; 
const int buzzerPin = 13;

void beep(int frequency, int duration) 
{
    // 주기 (반복 시간)을 계산
    int period = 1000000 / frequency;
    int halfPeriod = period / 2;
    
    // duration 동안 소리를 냅니다.
    for (long i = 0; i < duration * 1000; i += period) 
    {
        digitalWrite(buzzerPin, HIGH);  // 부저를 켭니다.
        delayMicroseconds(halfPeriod);  // halfPeriod 동안 대기합니다.
        digitalWrite(buzzerPin, LOW);   // 부저를 끕니다.
        delayMicroseconds(halfPeriod);  // 나머지 halfPeriod 동안 대기합니다.
    }
}

void setup() 
{
  Serial.begin(9600);
  pinMode(SwitchPin1,INPUT);
  pinMode(SwitchPin2,INPUT);
  pinMode(buzzerPin, OUTPUT);
}

void loop() 
{
  int count = 0;
  int Switch1_frag = 0;
  int Switch2_frag = 0;

  Switch1_frag = digitalRead(SwitchPin1);
  Switch2_frag = digitalRead(SwitchPin2);
  if (Switch1_frag == 0)
  {count = count + 1;}
  if (Switch2_frag == 0)
  {count = count + 1;}

  if (count == 2)
  {
    beep(1000,1000); delay(10); beep(1000,1000); delay(10); beep(1000,1000); delay(10);
    beep(1000,1000); delay(10); beep(1000,1000); delay(10); beep(1000,1000); delay(10);
    beep(1000,1000); delay(10); beep(1000,1000); delay(10); beep(1000,1000); delay(10);
    beep(1000,1000); delay(10); beep(1000,1000); delay(10); beep(1000,1000); delay(10);
    beep(1000,1000); delay(10); beep(1000,1000); delay(10); beep(1000,1000); delay(10);
  }

  Serial.print("count : ");   Serial.println(count);
  Serial.print("switch1 : "); Serial.println(Switch1_frag);
  Serial.print("switch2 : "); Serial.println(Switch2_frag);

  delay(1000);
}
