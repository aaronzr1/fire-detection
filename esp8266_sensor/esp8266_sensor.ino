// ESP8266 Sensor Node - sends data via ESP-NOW
// Sensors: IR flame (D6), MLX90614 (I2C), MQ-2 gas (A0/D5)

#include <ESP8266WiFi.h>
#include <espnow.h>
#include <Wire.h>
#include <Adafruit_MLX90614.h>

#define FLAME_PIN D6  // IR flame sensor (LOW = flame)
#define MQ2_APIN  A0  // MQ-2 analog
#define MQ2_DPIN  D5  // MQ-2 digital (LOW = gas detected)

Adafruit_MLX90614 mlx;
bool mlxReady = false;

uint8_t broadcastAddr[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

typedef struct {
  bool flame;
  bool gas;
  int gasRaw;
  float ambientC;
  float objectC;
} SensorData;

SensorData data;

void onSent(uint8_t *mac, uint8_t status) {
  if (status != 0) Serial.println("ESP-NOW send failed");
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(FLAME_PIN, INPUT);
  pinMode(MQ2_DPIN, INPUT);

  Wire.begin(D2, D1);  // SDA=D2, SCL=D1
  mlxReady = mlx.begin();
  if (!mlxReady) Serial.println("MLX90614 not found");

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  Serial.print("MAC: ");
  Serial.println(WiFi.macAddress());

  esp_now_init();
  esp_now_set_self_role(ESP_NOW_ROLE_CONTROLLER);
  esp_now_register_send_cb(onSent);
  esp_now_add_peer(broadcastAddr, ESP_NOW_ROLE_SLAVE, 0, NULL, 0);

  Serial.println("Sensor node ready");
  Serial.println("flame,gas,gasRaw,ambientC,objectC");
}

void loop() {
  data.flame    = digitalRead(FLAME_PIN) == LOW;
  data.gas      = digitalRead(MQ2_DPIN) == LOW;
  data.gasRaw   = analogRead(MQ2_APIN);
  data.ambientC = mlxReady ? mlx.readAmbientTempC() : -1;
  data.objectC  = mlxReady ? mlx.readObjectTempC()  : -1;

  esp_now_send(broadcastAddr, (uint8_t *)&data, sizeof(data));

  // CSV output
  Serial.print(data.flame);
  Serial.print(",");
  Serial.print(data.gas);
  Serial.print(",");
  Serial.print(data.gasRaw);
  Serial.print(",");
  Serial.print(data.ambientC, 1);
  Serial.print(",");
  Serial.println(data.objectC, 1);

  delay(500);
}
