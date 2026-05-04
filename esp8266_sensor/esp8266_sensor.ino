// ESP8266 Sensor Node - sends data via ESP-NOW
// IR flame sensor on D6 (active-low: LOW = flame detected)

#include <ESP8266WiFi.h>
#include <espnow.h>

#define FLAME_PIN D6  // GPIO12

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

  pinMode(FLAME_PIN, INPUT);

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

  Serial.println("Sensor node ready");
}

void loop() {
  bool flame = digitalRead(FLAME_PIN) == LOW;

  data.alert = flame;
  data.temperature = 25.0;

  esp_now_send(broadcastAddr, (uint8_t *)&data, sizeof(data));

  Serial.println(flame ? "FLAME detected!" : "clear");

  delay(200);
}
