#include <Wire.h>
#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614();
bool sensorReady = false;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("MLX90614 IR Temperature Sensor Test");
  Serial.println("====================================");

  Wire.begin();
  delay(500);

  sensorReady = mlx.begin();
  if (!sensorReady) {
    Serial.println("WARNING: mlx.begin() failed, will retry in loop...");
  } else {
    Serial.println("Sensor found! Reading every 1 second...");
  }
  Serial.println();
}

void loop() {
  if (!sensorReady) {
    sensorReady = mlx.begin();
    if (!sensorReady) {
      Serial.println("Sensor not ready, retrying...");
      delay(2000);
      return;
    }
    Serial.println("Sensor connected!");
  }

  double ambientC = mlx.readAmbientTempC();
  double objectC = mlx.readObjectTempC();
  double objectF = mlx.readObjectTempF();

  Serial.print("Ambient: ");
  Serial.print(ambientC, 2);
  Serial.print(" C  |  Object: ");
  Serial.print(objectC, 2);
  Serial.print(" C (");
  Serial.print(objectF, 2);
  Serial.println(" F)");

  delay(1000);
}
