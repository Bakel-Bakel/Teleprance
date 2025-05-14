#include <Servo.h>

int motorPin1 = 7;  // IN1
int motorPin2 = 6;  // IN2
int motorPin3 = 5;  // IN3
int motorPin4 = 4;  // IN4
int enablePin = 9;  // ENA/ENB (PWM)
int servoPin = 11;  // Servo signal pin

Servo myServo;

void setup() {
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  pinMode(enablePin, OUTPUT);
  
  myServo.attach(servoPin);  // Attach servo to pin 11
  Serial.begin(9600);  // Start serial communication
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();  // Read command from Raspberry Pi
    
    if (command == 'F') {
      // Move Forward
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, LOW);
      digitalWrite(motorPin3, HIGH);
      digitalWrite(motorPin4, LOW);
    } else if (command == 'B') {
      // Move Backward
      digitalWrite(motorPin1, LOW);
      digitalWrite(motorPin2, HIGH);
      digitalWrite(motorPin3, LOW);
      digitalWrite(motorPin4, HIGH);
    } else if (command == 'L') {
      // Turn Left
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, LOW);
      digitalWrite(motorPin3, LOW);
      digitalWrite(motorPin4, HIGH);
    } else if (command == 'R') {
      // Turn Right
      digitalWrite(motorPin1, LOW);
      digitalWrite(motorPin2, HIGH);
      digitalWrite(motorPin3, HIGH);
      digitalWrite(motorPin4, LOW);
    } else if (command == 'S') {
      // Stop
      digitalWrite(motorPin1, LOW);
      digitalWrite(motorPin2, LOW);
      digitalWrite(motorPin3, LOW);
      digitalWrite(motorPin4, LOW);
    }
  }
}
