#include <Servo.h>

int motorPin1 = 7;  // IN1
int motorPin2 = 6;  // IN2
int motorPin3 = 5;  // IN3
int motorPin4 = 4;  // IN4
int enablePin = 9;  // ENA/ENB (PWM)
int servoPin = 11;  // Servo signal pin
Servo myServo;

void setup() {
  // Initialize motor control pins
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(motorPin3, OUTPUT);
  pinMode(motorPin4, OUTPUT);
  pinMode(enablePin, OUTPUT);
  
  // Initialize Servo pin
  myServo.attach(servoPin);
  
  // Start serial communication for monitor
  Serial.begin(9600);  // Set baud rate to match Serial Monitor
  Serial.println("Robot Motor Control - Ready");
}

void loop() {
    if (Serial.available()) {
      char command = Serial.read();  // Read incoming data from Serial Monitor
  
      // Default speed, you can modify this as needed
      int motorSpeed = 255;  // Full speed (0 to 255, where 255 is max speed)
      
      // Check for the command received and control motors accordingly
      if (command == 'F') {
        // Move Forward
        Serial.println("Moving Forward");
        digitalWrite(motorPin1, HIGH);
        digitalWrite(motorPin2, LOW);
        digitalWrite(motorPin3, HIGH);
        digitalWrite(motorPin4, LOW);
        analogWrite(enablePin, motorSpeed);  // Set motor speed (PWM)
      } 
      else if (command == 'B') {
        // Move Backward
        Serial.println("Moving Backward");
        digitalWrite(motorPin1, LOW);
        digitalWrite(motorPin2, HIGH);
        digitalWrite(motorPin3, LOW);
        digitalWrite(motorPin4, HIGH);
        analogWrite(enablePin, motorSpeed);  // Set motor speed (PWM)
      } 
      else if (command == 'L') {
        // Turn Left
        Serial.println("Turning Left");
        digitalWrite(motorPin1, HIGH);
        digitalWrite(motorPin2, LOW);
        digitalWrite(motorPin3, LOW);
        digitalWrite(motorPin4, HIGH);
        analogWrite(enablePin, motorSpeed);  // Set motor speed (PWM)
      } 
      else if (command == 'R') {
        // Turn Right
        Serial.println("Turning Right");
        digitalWrite(motorPin1, LOW);
        digitalWrite(motorPin2, HIGH);
        digitalWrite(motorPin3, HIGH);
        digitalWrite(motorPin4, LOW);
        analogWrite(enablePin, motorSpeed);  // Set motor speed (PWM)
      } 
      else if (command == 'S') {
        // Stop Motors
        Serial.println("Stopping");
        digitalWrite(motorPin1, LOW);
        digitalWrite(motorPin2, LOW);
        digitalWrite(motorPin3, LOW);
        digitalWrite(motorPin4, LOW);
        analogWrite(enablePin, 0);  // Stop the motors by sending 0 to PWM
      }
    }
  }
