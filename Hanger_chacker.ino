const int SeatSwitchPin = 12; const int HandleSwitchPin = 11; 

void setup() 
{
  Serial.begin(9600);
  pinMode(SeatSwitchPin,INPUT_PULLUP);
  pinMode(HandleSwitchPin,INPUT_PULLUP);
}

float seat_count = 0;
float handle_count = 0;

void loop() 
{
  
  int Switch1_frag = 0;
  int Switch2_frag = 0;

  Switch1_frag = digitalRead(SeatSwitchPin);
  Switch2_frag = digitalRead(HandleSwitchPin);
  if (Switch1_frag == 0)
  {seat_count = seat_count + 1;}
  if (Switch2_frag == 0)
  {handle_count = handle_count + 1;}

  Serial.print("Switch1 : ");  Serial.println(Switch1_frag);
  Serial.print("Switch2 : ");  Serial.println(Switch2_frag);

  Serial.print("seat_count : ");    Serial.println(seat_count);
  Serial.print("handle_cound : ");  Serial.println(handle_count);
  Serial.print("percent : ");       Serial.print(handle_count/seat_count * 100);  Serial.println("%");
  delay(1000);
}
