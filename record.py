#!/usr/bin/env python3
"""Record serial data from data_logger sketch to CSV files."""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path

import serial


def main():
    parser = argparse.ArgumentParser(description="Record sensor data to CSV")
    parser.add_argument(
        "-p", "--port", default="/dev/cu.usbmodem141021", help="Serial port"
    )
    parser.add_argument("-b", "--baud", type=int, default=9600, help="Baud rate")
    parser.add_argument(
        "-l", "--label", default="baseline", help="Label for this recording session (e.g. 'baseline', 'candle_1m', 'sunlight')"
    )
    parser.add_argument(
        "-o", "--output-dir", default="recordings", help="Output directory"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print every line to terminal"
    )
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = out_dir / f"{args.label}_{timestamp}.csv"

    print(f"Recording to: {filename}", flush=True)
    print(f"Port: {args.port} @ {args.baud}", flush=True)
    print(f"Label: {args.label}", flush=True)
    print("Press Ctrl+C to stop.\n", flush=True)

    ser = serial.Serial(args.port, args.baud, timeout=2)
    # Wait for Arduino to reset after serial connection
    import time
    time.sleep(2)

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "millis", "flame_analog", "ambient_c", "object_c", "label"])

        line_count = 0
        try:
            while True:
                raw = ser.readline().decode("utf-8", errors="replace").strip()
                if not raw:
                    continue
                # Skip comment/status lines
                if raw.startswith("#"):
                    print(raw, flush=True)
                    continue
                # Skip the CSV header from Arduino
                if raw.startswith("millis,"):
                    print(f"[connected] {raw}", flush=True)
                    continue

                parts = raw.split(",")
                if len(parts) != 4:
                    continue

                now = datetime.now().isoformat()
                writer.writerow([now] + parts + [args.label])
                line_count += 1

                if args.verbose:
                    print(raw, flush=True)
                elif line_count % 10 == 0 or line_count <= 5:
                    print(f"[{line_count}] {raw}", flush=True)

        except KeyboardInterrupt:
            print(f"\nStopped. Recorded {line_count} samples to {filename}")
        finally:
            ser.close()


if __name__ == "__main__":
    main()
