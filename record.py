#!/usr/bin/env python3
"""Record sensor data from ESP8266 serial to CSV."""

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

import serial

DEFAULT_PORT = "COM3" if sys.platform == "win32" else "/dev/cu.usbserial-1130"
BAUD = 115200
OUT_DIR = Path("recordings")


def main():
    parser = argparse.ArgumentParser(description="Record sensor data from ESP8266 serial to CSV.")
    parser.add_argument("label", help="Recording label (e.g. normal, flame)")
    parser.add_argument("--port", default=DEFAULT_PORT, help=f"Serial port (default: {DEFAULT_PORT})")
    parser.add_argument("--baud", type=int, default=BAUD, help=f"Baud rate (default: {BAUD})")
    args = parser.parse_args()

    label = args.label
    OUT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUT_DIR / f"{label}_{timestamp}.csv"

    ser = serial.Serial(args.port, args.baud, timeout=1)
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
