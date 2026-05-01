#define BUZZER_PIN 8

void setup() {
  Serial.begin(9600);
  pinMode(BUZZER_PIN, OUTPUT);

  Serial.println("Buzzer test: 3 beeps");
  for (int i = 0; i < 3; i++) {
    Serial.print("Beep ");
    Serial.println(i + 1);
    digitalWrite(BUZZER_PIN, HIGH);
    delay(300);
    digitalWrite(BUZZER_PIN, LOW);
    delay(300);
  }
  Serial.println("Done");
}

void loop() {}
