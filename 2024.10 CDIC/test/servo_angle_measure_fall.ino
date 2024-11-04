#include <Servo.h>

Servo myservo;  // create servo object to control a servo

const int servoAnalogOut = A1;  // The new Servo Pin
unsigned int servoValue0Deg, servoValue180Deg;  // Variables to store min and max values of servo's pot
int pos = 0;  // variable to store the servo position

void setup() {
  myservo.attach(7);  // attaches the servo on pin 7 to the servo object
  Serial.begin(9600);
  calibration();  // Calibrate the servo at startup
}

void loop() {
  for (int angle = 0; angle <= 180; angle += 10) {
    myservo.write(angle);  // Move the servo to the current angle
    delay(1000);  // Wait for the servo to reach the desired position

    int analogValue = analogRead(servoAnalogOut);  // Read the analog value
    float estimatedAngle = estimateAngle(analogValue);  // Calculate the angle using the linear equation

    // Output the measured analog value and the estimated angle
    Serial.print("Actual Angle: ");
    Serial.print(angle);
    Serial.print(" | Analog Value: ");
    Serial.print(analogValue);
    Serial.print(" | Estimated Angle: ");
    Serial.println(estimatedAngle);
    
    delay(1000);  // Slight delay before moving to the next position
  }
}

// Calibration function to read the analog values at 0 and 180 degrees
void calibration() {
  myservo.write(0);
  delay(1000);  // Give time for the servo to reach 0 degrees
  servoValue0Deg = analogRead(servoAnalogOut);  // Store the analog value at 0 degrees
  Serial.println("Pot value for 0 deg: " + String(servoValue0Deg));

  myservo.write(180);
  delay(1000);  // Give time for the servo to reach 180 degrees
  servoValue180Deg = analogRead(servoAnalogOut);  // Store the analog value at 180 degrees
  Serial.println("Pot value for 180 deg: " + String(servoValue180Deg));

  // Return the servo to the initial position
  myservo.write(0);
}

// Function to estimate the angle based on the input analog value using the linear equation
float estimateAngle(int analogValue) {
  // Check if the calibration values are valid
  if (servoValue0Deg == servoValue180Deg) {
    return -1;  // Avoid division by zero
  }
  
  // Calculate slope (m) and intercept (b) based on the 0 and 180 degree calibration values
  float m = 180.0 / (servoValue0Deg - servoValue180Deg);  // Slope (change in angle per change in analog value)
  float b = -m * servoValue180Deg;  // Adjust the intercept based on the calibration
  return m * analogValue + b;  // Calculate the estimated angle
}
