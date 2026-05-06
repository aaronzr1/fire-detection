#!/usr/bin/env python3
"""Record sensor data from ESP8266 serial to CSV."""

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

import serial
import serial.serialwin32
import ctypes
from serial import win32 as _win32

DEFAULT_PORT = "COM19" if sys.platform == "win32" else "/dev/cu.usbserial-1130"


def _ch340_reconfigure_port(self):
    # CH340 on Windows fails SetCommState when opened with FILE_FLAG_OVERLAPPED.
    # Workaround: open a second non-overlapped handle, apply settings there, close it.
    port = self.name
    if port.upper().startswith('COM') and int(port[3:]) > 8:
        port = r'\\.\{}'.format(port)
    tmp = _win32.CreateFile(port, _win32.GENERIC_READ | _win32.GENERIC_WRITE,
                            0, None, _win32.OPEN_EXISTING, 0, 0)
    if tmp != _win32.INVALID_HANDLE_VALUE:
        dcb = _win32.DCB()
        _win32.GetCommState(tmp, ctypes.byref(dcb))
        dcb.BaudRate = self._baudrate
        dcb.ByteSize = 8
        dcb.Parity = _win32.NOPARITY
        dcb.StopBits = _win32.ONESTOPBIT
        dcb.fBinary = 1
        dcb.fParity = 0
        dcb.fOutxCtsFlow = 0
        dcb.fOutxDsrFlow = 0
        dcb.fDtrControl = _win32.DTR_CONTROL_ENABLE
        dcb.fRtsControl = _win32.RTS_CONTROL_ENABLE
        dcb.fOutX = 0
        dcb.fInX = 0
        dcb.fNull = 0
        dcb.fErrorChar = 0
        dcb.fAbortOnError = 0
        _win32.SetCommState(tmp, ctypes.byref(dcb))
        _win32.CloseHandle(tmp)
    # Set timeouts on the overlapped handle (safe)
    timeouts = _win32.COMMTIMEOUTS()
    if self._timeout is not None and self._timeout != 0:
        timeouts.ReadTotalTimeoutConstant = max(int(self._timeout * 1000), 1)
    _win32.SetCommTimeouts(self._port_handle, ctypes.byref(timeouts))
    _win32.SetCommMask(self._port_handle, _win32.EV_ERR)


if sys.platform == "win32":
    serial.serialwin32.Serial._reconfigure_port = _ch340_reconfigure_port
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

    ser = serial.Serial(args.port, args.baud, timeout=1, dsrdtr=False)
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
