#!/bin/bash
set -e

FQBN="esp8266:esp8266:nodemcuv2"
PORT="/dev/cu.usbserial-1130"

if [ -z "$1" ]; then
  echo "Usage: ./flash.sh <sketch>"
  echo "  ./flash.sh esp8266_sensor"
  echo "  ./flash.sh esp8266_buzzer"
  exit 1
fi

SKETCH="$1"

if [ ! -d "$SKETCH" ]; then
  echo "Error: sketch folder '$SKETCH' not found"
  exit 1
fi

echo "==> Compiling $SKETCH..."
arduino-cli compile --fqbn "$FQBN" "$SKETCH"

echo "==> Uploading to $PORT..."
arduino-cli upload --fqbn "$FQBN" --port "$PORT" "$SKETCH"

echo "==> Done! Opening serial monitor (Ctrl+C to exit)..."
arduino-cli monitor --port "$PORT" --config baudrate=115200
