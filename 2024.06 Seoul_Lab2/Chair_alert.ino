const int trigPin1 = 11;  const int trigPin2 = 10;  const int trigPin2 = 8;
const int echoPin1 = 12;  const int echoPin2 = 9;   const int echoPin2 = 7;

const int buzzerPin = 13;

const long limit_distance = 50;

void beep(int frequency, int duration) 
{
    // 주기 (반복 시간)을 계산
    int period = 1000000 / frequency;
    int halfPeriod = period / 2;
    
    // duration 동안 소리를 냅니다.
    for (long i = 0; i < duration * 1000L; i += period) 
    {
        digitalWrite(buzzerPin, HIGH);  // 부저를 켭니다.
        delayMicroseconds(halfPeriod);  // halfPeriod 동안 대기합니다.
        digitalWrite(buzzerPin, LOW);   // 부저를 끕니다.
        delayMicroseconds(halfPeriod);  // 나머지 halfPeriod 동안 대기합니다.
    }
}

long readUltrasonicDistance(int trig, int echo) 
{
    // Trig 핀을 LOW로 설정하여 센서를 초기화
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    
    // Trig 핀을 HIGH로 설정하여 초음파 펄스를 보냄
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW);
    
    // Echo 핀에서 펄스가 반환되는 시간을 측정
    long duration = pulseIn(echo, HIGH);
    
    // 측정된 시간을 통해 거리를 계산
    // 음파가 왕복하는 시간(μs)을 cm로 변환
    long distance = duration * 0.034 / 2;
    
    return distance;
}

void setup() 
{
    // 시리얼 통신 시작
    Serial.begin(9600);

    // 부저 핀을 출력 모드로 설정
    pinMode(buzzerPin, OUTPUT);
    
    // 초음파 센서 핀 설정
    pinMode(trigPin1, OUTPUT);
    pinMode(echoPin1, INPUT);
    pinMode(trigPin2, OUTPUT);
    pinMode(echoPin2, INPUT);  
}

void loop() 
{
  // Reset count num
  int count = 0;
  
  // 거리 측정
  long distance1 = readUltrasonicDistance(trigPin1, echoPin1);
  long distance2 = readUltrasonicDistance(trigPin2, echoPin2);
  long distance3 = readUltrasonicDistance(trigPin3, echoPin3);


  // 거리 조건 확인
  if (distance1 < limit_distance)  {count =+ 1;}
  if (distance2 < limit_distance)  {count =+ 1;}
  if (distance3 < limit_distance)  {count =+ 1;}

  if (count == 2 || count == 3)
  {beep(1000,1000);}

  // 거리 출력
  Serial.print("Distance1: ");
  Serial.print(distance1);
  Serial.println(" cm");

  Serial.print("Distance2: ");
  Serial.print(distance2);
  Serial.println(" cm");

  Serial.print("Distance3: ");
  Serial.print(distance3);
  Serial.println(" cm");

  // 잠시 대기
  delay(500);
}
