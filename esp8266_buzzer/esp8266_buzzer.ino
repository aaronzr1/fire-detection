// ESP8266 Buzzer Node - receives data via ESP-NOW
// Buzzes on flame/gas/high temp, beeps if no data received

#include <ESP8266WiFi.h>
#include <espnow.h>

#define BUZZER_PIN D5
#define MAX_NORM_TEMP 50.0       // object temp threshold (°C)
#define NO_DATA_TIMEOUT 5000     // ms before "no data" beeping starts
#define BEEP_INTERVAL 500        // ms on/off cycle for no-data beep

volatile unsigned long lastReceive = 0;

typedef struct {
  bool flame;
  bool gas;
  int gasRaw;
  float ambientC;
  float objectC;
} SensorData;

void onReceive(uint8_t *mac, uint8_t *data, uint8_t len) {
  if (len != sizeof(SensorData)) return;

  lastReceive = millis();

  SensorData d;
  memcpy(&d, data, sizeof(d));

  bool alert = d.flame || d.gas || d.objectC > MAX_NORM_TEMP;
  digitalWrite(BUZZER_PIN, alert ? LOW : HIGH);
}

void setup() {
  digitalWrite(BUZZER_PIN, HIGH);
  pinMode(BUZZER_PIN, OUTPUT);

  Serial.begin(115200);
  delay(1000);

  lastReceive = millis();

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  esp_now_init();
  esp_now_set_self_role(ESP_NOW_ROLE_SLAVE);
  esp_now_register_recv_cb(onReceive);

  Serial.println("Buzzer node ready");
}

void loop() {
  if (millis() - lastReceive > NO_DATA_TIMEOUT) {
    // Beep on/off pattern
    bool on = (millis() / BEEP_INTERVAL) % 2 == 0;
    digitalWrite(BUZZER_PIN, on ? LOW : HIGH);
  }
  delay(50);
}
