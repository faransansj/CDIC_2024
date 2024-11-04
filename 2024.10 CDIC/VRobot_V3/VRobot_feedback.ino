#include <SoftwareSerial.h>

// Define Bluetooth RX and TX pins for HC-06 module
SoftwareSerial BTSerial(0, 1); // RX, TX (Choose appropriate pins)

// Pin configurations
int servo_pins[]  = {2, 3, 4, 5, 6};
int LED_pins[]    = {13, 12, 11, 10, 9};
int feedback_switch[3];

void set_servo_angle(int angle, int servoPin) {
  int pulseWidth = map(angle, 0, 180, 1000, 2000);

  for (int i = 0; i < 50; i++) {
    digitalWrite(servoPin, HIGH);
    delayMicroseconds(pulseWidth);
    digitalWrite(servoPin, LOW);
    delayMicroseconds(20000 - pulseWidth);
  }
}

void feed_back(int switch_pin, int servo_pin, int LED_pin) {
  if (switch_pin == 1) {
    Serial.print(servo_pin - 1); Serial.println(" finger feedback on");
    set_servo_angle(180, servo_pin);
    digitalWrite(LED_pin, HIGH);
  } else {
    Serial.print(servo_pin - 1); Serial.println(" finger feedback off");
    set_servo_angle(0, servo_pin);
    digitalWrite(LED_pin, LOW);
  }
}

void get_data() {
  String input;
  
  // Check if data is available from Bluetooth or Serial Monitor
  if (BTSerial.available() > 0) {
    input = BTSerial.readStringUntil('\n');  // Read from Bluetooth
  } else if (Serial.available() > 0) {
    input = Serial.readStringUntil('\n');  // Read from Serial Monitor
  }

  if (input.length() > 0) {
    // Verify that input contains exactly 2 commas (3 values)
    int commas = 0;
    for (int j = 0; j < input.length(); j++) {
      if (input.charAt(j) == ',') {
        commas++;
      }
    }

    if (commas == 2) {  // Expecting 3 values, so 2 commas
      int startIdx = 0;
      int endIdx = 0;
      for (int i = 0; i < 3; i++) {
        endIdx = input.indexOf(',', startIdx);
        if (endIdx == -1) {
          feedback_switch[i] = input.substring(startIdx).toInt();
        } else {
          feedback_switch[i] = input.substring(startIdx, endIdx).toInt();
          startIdx = endIdx + 1;
        }
      }
    } else {
      Serial.println("Error: Invalid input. Please enter 3 comma-separated values.");
    }
  }
}

void setup() {
  Serial.begin(9600);
  BTSerial.begin(9600);  // Begin communication with HC-06 module

  for (int i = 0; i < 5; i++) {
    pinMode(servo_pins[i], OUTPUT);
    pinMode(LED_pins[i], OUTPUT);
  }
}

void loop() {
  get_data();  // Get feedback_switch values from Bluetooth or Serial Monitor

  // Provide feedback based on the received data
  feed_back(feedback_switch[0], servo_pins[0], LED_pins[0]);
  feed_back(feedback_switch[1], servo_pins[1], LED_pins[1]);
  feed_back(feedback_switch[1], servo_pins[2], LED_pins[2]);
  feed_back(feedback_switch[2], servo_pins[3], LED_pins[3]);
  feed_back(feedback_switch[2], servo_pins[4], LED_pins[4]);
  
  delay(1000);  // Optional delay for feedback control
}
