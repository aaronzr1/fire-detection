#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
  while (!Serial);
  Serial.println("I2C Scanner");
  Serial.println("Scanning...");

  int count = 0;
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    byte error = Wire.endTransmission();
    if (error == 0) {
      Serial.print("  Device found at 0x");
      if (addr < 16) Serial.print("0");
      Serial.println(addr, HEX);
      count++;
    }
  }

  if (count == 0)
    Serial.println("  No I2C devices found! Check wiring.");
  else {
    Serial.print("Done. Found ");
    Serial.print(count);
    Serial.println(" device(s).");
  }
  Serial.println("MLX90614 default address is 0x5A");
}

void loop() {
  delay(5000);
}
