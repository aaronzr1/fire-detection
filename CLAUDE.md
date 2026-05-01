# Arduino Upload (Mega 2560, macOS)

avrdude 8.x on macOS fails to upload to Arduino Mega due to broken DTR reset timing. Workaround: toggle DTR via stty before calling avrdude directly:

```bash
stty -f /dev/cu.usbmodem141021 115200 hupcl; sleep 0.5; stty -f /dev/cu.usbmodem141021 -hupcl; sleep 0.5; stty -f /dev/cu.usbmodem141021 hupcl; sleep 2
avrdude -patmega2560 -cwiring -P/dev/cu.usbmodem141021 -b115200 -D -Uflash:w:$HEX:i
```

Do NOT use `arduino-cli upload` — it will timeout. Compile with `arduino-cli compile`, then find the .hex in `~/Library/Caches/arduino/sketches/` and upload with avrdude directly.
