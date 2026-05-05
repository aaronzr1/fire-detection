#!/usr/bin/env python3
"""Record sensor data from ESP8266 serial to CSV."""

import sys
import time
from datetime import datetime
from pathlib import Path

import serial

PORT = "/dev/cu.usbserial-1130"
BAUD = 115200
OUT_DIR = Path("recordings")


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run record.py <label>")
        print("  e.g: uv run record.py normal")
        print("       uv run record.py flame")
        sys.exit(1)

    label = sys.argv[1]
    OUT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUT_DIR / f"{label}_{timestamp}.csv"

    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # wait for ESP boot
    ser.reset_input_buffer()

    print(f"Recording to {filename} (label={label})")
    print("Press Ctrl+C to stop\n")

    count = 0
    with open(filename, "w") as f:
        f.write("timestamp,flame,gas,gasRaw,ambientC,objectC\n")

        while True:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                continue

            # Skip non-CSV lines (boot messages, headers)
            parts = line.split(",")
            if len(parts) != 5:
                print(f"[skip] {line}")
                continue

            ts = datetime.now().isoformat()
            f.write(f"{ts},{line}\n")
            f.flush()
            count += 1
            print(f"[{count}] {line}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDone.")
