#!/usr/bin/env python3
"""Print ESP8266 serial output to stdout."""

import argparse
import sys
import serial
import serial.serialwin32
import ctypes
from serial import win32 as _win32

DEFAULT_PORT = "COM18" if sys.platform == "win32" else "/dev/cu.usbserial-1130"


def _ch340_reconfigure_port(self):
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
    timeouts = _win32.COMMTIMEOUTS()
    if self._timeout is not None and self._timeout != 0:
        timeouts.ReadTotalTimeoutConstant = max(int(self._timeout * 1000), 1)
    _win32.SetCommTimeouts(self._port_handle, ctypes.byref(timeouts))
    _win32.SetCommMask(self._port_handle, _win32.EV_ERR)


if sys.platform == "win32":
    serial.serialwin32.Serial._reconfigure_port = _ch340_reconfigure_port


def main():
    parser = argparse.ArgumentParser(description="Monitor ESP8266 serial output.")
    parser.add_argument("--port", default=DEFAULT_PORT, help=f"Serial port (default: {DEFAULT_PORT})")
    parser.add_argument("--baud", type=int, default=115200)
    args = parser.parse_args()

    ser = serial.Serial(args.port, args.baud, timeout=1, dsrdtr=False)
    print(f"Monitoring {args.port} at {args.baud} baud (Ctrl+C to stop)\n")

    while True:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        if line:
            print(line)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDone.")
