# Windows Deployment Guide

This guide covers running the fire detection sensor node from a Windows laptop (no internet required).

## What You Need

- Windows laptop with a USB port
- ESP8266 sensor node (already flashed) plugged in via USB
- This repo copied to the laptop (USB stick is fine)

## First-Time Setup

1. Open PowerShell (search "PowerShell" in Start menu)

2. If you get a script execution error, run this once:
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. Navigate to the windows scripts folder:
   ```powershell
   cd C:\path\to\fire-detection\windows
   ```

4. Run the setup script (installs Python + dependencies offline from `binaries/`):
   ```powershell
   .\setup.ps1
   ```

5. Close and reopen PowerShell after setup (so Python is on your PATH).

## Find Your COM Port

1. Open **Device Manager** (search it in Start menu)
2. Expand **Ports (COM & LPT)**
3. Look for something like "USB-SERIAL CH340 (COM3)" — note the COM number
4. If you don't see it, the USB cable may be charge-only or drivers missing

## Monitor Serial Output (live view)

From the `windows/` folder:

```powershell
.\monitor.ps1
```

Or specify a different port:
```powershell
.\monitor.ps1 -Port COM4
```

You should see lines like:
```
0,0,312,24.5,25.1
```
Format: `flame,gas,gasRaw,ambientC,objectC`

Press **Ctrl+C** to stop.

## Record Data to CSV

```powershell
.\record.ps1 normal
```

This saves timestamped sensor readings to `recordings/normal_20260505_143022.csv`.

To record with a flame present:
```powershell
.\record.ps1 flame
```

To use a different port:
```powershell
.\record.ps1 flame -Port COM4
```

Press **Ctrl+C** to stop recording.

## CSV Format

Files are saved in the `recordings/` folder (at the project root):
```
timestamp,flame,gas,gasRaw,ambientC,objectC
2026-05-05T14:30:22.123456,0,0,312,24.5,25.1
```

| Column | Meaning |
|--------|---------|
| flame | 1 = flame detected, 0 = no flame |
| gas | 1 = gas/smoke detected, 0 = clear |
| gasRaw | Raw analog value (0–1024) |
| ambientC | Ambient temperature (°C) |
| objectC | Object/surface temperature (°C) |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "No COM ports detected" | Plug in the ESP8266, try a different USB cable |
| Wrong COM port | Check Device Manager, use `-Port COM4` (or whichever) |
| ".venv not found" | Run `.\setup.ps1` first |
| Script won't run | Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Garbled output | Make sure baud is 115200 (the default) |
