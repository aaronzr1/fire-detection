# fire-detection

Cheap wireless fire detection system without WiFi dependency. Two ESP8266 nodes communicating over ESP-NOW — one reads sensors, the other sounds a buzzer.

## Architecture

- **Sensor node** (`esp8266_sensor/`) — reads IR flame, MLX90614 temp, MQ-2 gas; broadcasts via ESP-NOW; outputs CSV over serial
- **Buzzer node** (`esp8266_buzzer/`) — receives ESP-NOW data, drives active-low buzzer on alarm

## Sensors

Sensor node:
| Sensor | Type | Interface |
|--------|------|-----------|
| MH-B IR flame | Digital (LOW = flame) | D6 |
| MLX90614 | I2C thermopile | D2/D1 (SDA/SCL) |
| MQ-2 | Analog + digital gas | A0 / D5 |

Buzzer node: 
Active-low buzzer on D5 (GPIO14).

## Dev Setup (macOS)

```bash
# ESP8266 board package
arduino-cli config add board_manager.additional_urls https://arduino.esp8266.com/stable/package_esp8266com_index.json
arduino-cli core install esp8266:esp8266

# Flash (one at a time via USB)
./flash.sh esp8266_buzzer
./flash.sh esp8266_sensor

# Record data for calibration
uv run record.py normal
uv run record.py flame
```

## Files

| File | Purpose |
|------|---------|
| `esp8266_sensor/` | Sensor node firmware |
| `esp8266_buzzer/` | Buzzer node firmware |
| `fire_monitor/` | Arduino Mega standalone reference |
| `record.py` | Serial data logger (CSV) |
| `flash.sh` | Compile + upload + monitor (macOS) |
| `windows/` | PowerShell scripts for Windows deployment |

## Troubleshooting

Update the port in `flash.sh` / ps1 scripts if the device enumerates differently. Check with `ls /dev/cu.usb*` (macOS) or Device Manager (Windows).
