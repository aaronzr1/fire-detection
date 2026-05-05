# fire

Cheap wireless fire detection system without WiFi dependency. Uses two ESP8266 nodes communicating over ESP-NOW — one with sensor input, the other sounds a buzzer.

## Sensors

- **IR flame sensor** (MH-B) — digital flame detection
- **MLX90614** — non-contact IR temperature (ambient & object)
- **MQ-2** — smoke/gas (analog + digital)

## Files

- `esp8266_sensor/` — sensor node: reads all sensors, broadcasts via ESP-NOW
- `esp8266_buzzer/` — buzzer node: receives ESP-NOW, buzzes on flame/gas
- `record.py` — serial logger, saves sensor data to CSV
- `flash.sh` — compile + upload + serial monitor

## Setup

```bash
# Install ESP8266 board package
arduino-cli config add board_manager.additional_urls https://arduino.esp8266.com/stable/package_esp8266com_index.json
arduino-cli core install esp8266:esp8266

# Flash (one ESP at a time via /dev/cu.usbserial-1130)
./flash.sh esp8266_buzzer   # flash buzzer node first, then swap USB
./flash.sh esp8266_sensor

# Record sensor data for sensitivity calibration (edit corresponding variables in `*_buzzer.ino`)
uv run record.py normal     # baseline recording
uv run record.py flame      # flame recording
```

## Wiring

### Sensor Node — NodeMCU

| Sensor | Pin | NodeMCU |
|--------|-----|---------|
| Flame OUT | D6 | GPIO12 |
| MQ-2 A0 | A0 | ADC |
| MQ-2 D0 | D5 | GPIO14 |
| MLX SDA | D2 | GPIO4 |
| MLX SCL | D1 | GPIO5 |

### Buzzer Node

Active buzzer on D5 (GPIO14).

## Troubleshooting

you may need to update the port in `flash.sh` before flashing; ask claude to check on it if there's an issue