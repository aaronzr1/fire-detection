// ESP8266 Buzzer Node - receives data via ESP-NOW
// Buzzes when alert is true

#include <ESP8266WiFi.h>
#include <espnow.h>

#define BUZZER_PIN D5  // GPIO4 - boots low, safe for buzzer

typedef struct {
  bool alert;
  float temperature;
} SensorData;

void onReceive(uint8_t *mac, uint8_t *data, uint8_t len) {
  if (len != sizeof(SensorData)) return;

  SensorData received;
  memcpy(&received, data, sizeof(received));

  Serial.print("Received: alert=");
  Serial.print(received.alert);
  Serial.print(" temp=");
  Serial.println(received.temperature);

  digitalWrite(BUZZER_PIN, received.alert ? LOW : HIGH);
}

void setup() {
  digitalWrite(BUZZER_PIN, HIGH); // Assuming active-low
  pinMode(BUZZER_PIN, OUTPUT);

  Serial.begin(115200);
  delay(1000);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  Serial.print("Buzzer MAC: ");
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != 0) {
    Serial.println("ESP-NOW init failed");
    return;
  }

  esp_now_set_self_role(ESP_NOW_ROLE_SLAVE);
  esp_now_register_recv_cb(onReceive);

  Serial.println("Buzzer node ready - waiting for data");
}

void loop() {
  // Nothing to do - onReceive handles everything
}
