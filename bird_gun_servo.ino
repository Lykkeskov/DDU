#include <Servo.h>

// servos
Servo sl1;
Servo sl2;

// joystick pins
int xPin = A0;   // VRx
int yPin = A1;   // VRy
int knap = 2;    // SW button

// joystick values
int xVal;
int yVal;
int trykknap;

void setup() {
  sl1.attach(3);   // Servo 1
  sl2.attach(5);   // Servo 2

  Serial.begin(9600);
  pinMode(knap, INPUT_PULLUP);  // button is active LOW
}

void loop() {
  // read joystick
  xVal = analogRead(xPin);   // 0–1023
  yVal = analogRead(yPin);   // 0–1023
  trykknap = digitalRead(knap);

  // map joystick range to servo angle (0–180)
  int servo1Pos = map(xVal, 0, 1023, 0, 180);
  int servo2Pos = map(yVal, 0, 1023, 0, 180);

  // move servos
  sl1.write(servo1Pos);
  sl2.write(servo2Pos);

  // print for debugging
  Serial.print("X: ");
  Serial.print(xVal);
  Serial.print(" (Servo1: ");
  Serial.print(servo1Pos);
  Serial.print(")\tY: ");
  Serial.print(yVal);
  Serial.print(" (Servo2: ");
  Serial.print(servo2Pos);
  Serial.print(")\tButton: ");
  Serial.println(trykknap);

  delay(100);
}
