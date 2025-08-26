const int buttonPin = 2;
int buttonState = 0;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);  // enable internal pull-up
  Serial.begin(9600);
}

void loop() {
  buttonState = digitalRead(buttonPin);

  // logic is inverted now: LOW means pressed, HIGH means not pressed
  if (buttonState == LOW) {
    Serial.println("Button is PRESSED!");
  } else {
    Serial.println("Button is NOT pressed.");
  }

  delay(200);
}
