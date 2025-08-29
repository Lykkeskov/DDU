#include <Wire.h>
#include <Nunchuk.h>
#include <Servo.h>

Servo sl1;
Servo sl2;

// Deadzone size (adjust until servos reliably stop when joystick is centered)
const int DEADZONE = 10;

void setup() {
  sl1.attach(5);   // Servo 1 pin
  sl2.attach(9);   // Servo 2 pin

  Serial.begin(9600);
  Wire.begin();
  nunchuk_init();  // start communication with Nunchuk
}

void loop() {
  if (nunchuk_read()) {
    int joyX = nunchuk_joystickX(); // ~30–220 in practice
    int joyY = nunchuk_joystickY();
    int btnZ = nunchuk_buttonZ();
    int btnC = nunchuk_buttonC();

    // Map joystick range (0–255) to servo command (0–180)
    int servo1Cmd = map(joyY, -128, 128, 0, 180);
    int servo2Cmd = map(joyX, -128, 128, 0, 180);

    // Apply deadzone around 90 (stop position for continuous servos)
    if (abs(servo1Cmd - 90) < DEADZONE) servo1Cmd = 90;
    if (abs(servo2Cmd - 90) < DEADZONE) servo2Cmd = 90;

    // Write commands to servos
    sl1.write(servo1Cmd);
    sl2.write(servo2Cmd);

    // If Z button is pressed → tell Python to show "BANG!"
    if (btnZ == 1) {
      Serial.println("BANG");
    }

    // Debug print (optional, can be removed)
    Serial.print("X: "); Serial.print(joyX);
    Serial.print(" -> Servo2: "); Serial.print(servo2Cmd);
    Serial.print("\tY: "); Serial.print(joyY);
    Serial.print(" -> Servo1: "); Serial.print(servo1Cmd);
    Serial.print("\tZ: "); Serial.print(btnZ);
    Serial.print("\tC: "); Serial.println(btnC);
  }

  delay(50); // smoother updates
}
