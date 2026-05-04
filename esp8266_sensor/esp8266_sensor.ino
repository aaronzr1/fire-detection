// ESP8266 Sensor Node - sends data via ESP-NOW
// Test mode: press FLASH button (GPIO0) to send alert

#include <ESP8266WiFi.h>
#include <espnow.h>

#define BUTTON_PIN 0  // FLASH button on NodeMCU (active-low)

uint8_t broadcastAddr[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

typedef struct {
  bool alert;
  float temperature;
} SensorData;

SensorData data;

void onSent(uint8_t *mac, uint8_t status) {
  Serial.print("Send: ");
  Serial.println(status == 0 ? "OK" : "FAIL");
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(BUTTON_PIN, INPUT_PULLUP);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  Serial.print("Sensor MAC: ");
  Serial.println(WiFi.macAddress());

  if (esp_now_init() != 0) {
    Serial.println("ESP-NOW init failed");
    return;
  }

  esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);
  esp_now_register_send_cb(onSent);
  esp_now_add_peer(broadcastAddr, ESP_NOW_ROLE_SLAVE, 0, NULL, 0);

  Serial.println("Ready - press FLASH button to send alert");
}

void loop() {
  bool pressed = digitalRead(BUTTON_PIN) == LOW;

  data.alert = pressed;
  data.temperature = 25.0;

  esp_now_send(broadcastAddr, (uint8_t *)&data, sizeof(data));

  if (pressed) {
    Serial.println(">>> ALERT sent");
  }

  delay(100);
}
