# Arduino Upload (Mega 2560, macOS)

avrdude 8.x on macOS fails to upload to Arduino Mega due to broken DTR reset timing. Workaround: toggle DTR via stty before calling avrdude directly:

```bash
stty -f /dev/cu.usbmodem141021 115200 hupcl; sleep 0.5; stty -f /dev/cu.usbmodem141021 -hupcl; sleep 0.5; stty -f /dev/cu.usbmodem141021 hupcl; sleep 2
avrdude -patmega2560 -cwiring -P/dev/cu.usbmodem141021 -b115200 -D -Uflash:w:$HEX:i
```

Do NOT use `arduino-cli upload` — it will timeout. Compile with `arduino-cli compile`, then find the .hex in `~/Library/Caches/arduino/sketches/` and upload with avrdude directly.

# ESP8266 (NodeMCU base)

Two NodeMCU boards (ESP8266). FQBN: `esp8266:esp8266:nodemcuv2`. Connected via ESP-NOW (broadcast).

- `esp8266_sensor/` — reads sensors, sends data via ESP-NOW
- `esp8266_buzzer/` — receives data, drives buzzer on D1 (GPIO5)
- `fire_monitor/` — Arduino Mega reference code (sensors + buzzer, standalone)

Note that the buzzer is active-low

# Deployment

- **Sensor node** is deployed on an offline Windows laptop (no WiFi/internet). All dependencies are bundled in `binaries/` for offline install.
- **Buzzer node** is deployed separately, receives data wirelessly via ESP-NOW (no WiFi network needed).
- Windows scripts live in `windows/` (`setup.ps1`, `monitor.ps1`, `record.ps1`) and handle serial monitoring and data recording on the deployment laptop.
- `record.py` is the canonical recording logic; `record.ps1` is a thin wrapper that activates the venv and calls it.
- Serial output format from sensor node: `flame,gas,gasRaw,ambientC,objectC` (5 CSV fields per line, 115200 baud, 500ms interval).
