void serial_get(int finger)
{
  if(Serial.available())
  { 
    int angle_val = Serial.read(); 
    Serial.print("success to read angle value"); Serial.println(angle_val);
  }
  else
    Serial.print(finger); Serial.println("fail get angle value");
    int angle_val = 999; //error handling
  return angle_val;
}
