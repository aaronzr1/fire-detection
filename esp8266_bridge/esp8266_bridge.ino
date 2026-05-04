// ESP8266 Bridge - Hello World
// Will eventually receive sensor data from Arduino Mega via Serial

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("ESP8266 Bridge - Hello World!");
}

void loop() {
  Serial.println("Hello from ESP8266!");
  delay(1000);
}
