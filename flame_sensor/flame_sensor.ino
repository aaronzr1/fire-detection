#define FLAME_PIN 31

void setup() {
  Serial.begin(9600);
  pinMode(FLAME_PIN, INPUT);
  Serial.println("Flying-fish flame sensor ready");
}

void loop() {
  int val = digitalRead(FLAME_PIN);
  if (val == LOW) {
    Serial.println("FLAME DETECTED");
  } else {
    Serial.println("No flame");
  }
  delay(500);
}
