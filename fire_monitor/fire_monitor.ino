#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include "buzzer.h"

#define FLAME_PIN 31

Adafruit_MLX90614 mlx = Adafruit_MLX90614();
bool sensorReady = false;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  pinMode(FLAME_PIN, INPUT);
  buzzerSetup();

  Wire.begin();
  delay(500);

  sensorReady = mlx.begin();
  if (!sensorReady) {
    Serial.println("MLX90614 not found, will retry...");
  }

  Serial.println("Fire monitor ready");
  Serial.println("==================");
}

void loop() {
  if (!sensorReady) {
    sensorReady = mlx.begin();
    if (!sensorReady) {
      Serial.println("MLX90614 not ready, retrying...");
      delay(2000);
      return;
    }
    Serial.println("MLX90614 connected!");
  }

  int flame = digitalRead(FLAME_PIN);
  double ambientC = mlx.readAmbientTempC();
  double objectC = mlx.readObjectTempC();

  if (flame == LOW) {
    buzzerOn();
  } else {
    buzzerOff();
  }

  Serial.print(flame == LOW ? "FLAME" : "    ");
  Serial.print("  | Ambient: ");
  Serial.print(ambientC, 1);
  Serial.print(" C | Object: ");
  Serial.print(objectC, 1);
  Serial.println(" C");

  delay(500);
}
