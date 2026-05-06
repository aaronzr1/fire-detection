# Monitor serial output from ESP8266 sensor node
# Usage: .\monitor.ps1
#        .\monitor.ps1 -Port COM4

param(
    [string]$Port = "COM3",
    [int]$Baud = 115200
)

$ErrorActionPreference = "Stop"

# Show available COM ports
$ports = [System.IO.Ports.SerialPort]::GetPortNames()
if ($ports.Count -eq 0) {
    Write-Host "Error: No COM ports detected. Is the ESP8266 plugged in?" -ForegroundColor Red
    exit 1
}
if ($ports.Count -gt 0) {
    Write-Host "Available ports: $($ports -join ', ')"
}
if ($Port -notin $ports) {
    Write-Host "Warning: $Port not found in available ports" -ForegroundColor Yellow
}

$serial = New-Object System.IO.Ports.SerialPort $Port, $Baud
$serial.ReadTimeout = 1000
$serial.Open()
Start-Sleep -Seconds 2
$serial.DiscardInBuffer()

Write-Host "Monitoring $Port at $Baud baud"
Write-Host "Press Ctrl+C to stop`n"

try {
    while ($true) {
        try {
            $line = $serial.ReadLine().Trim()
            Write-Host $line
        } catch [System.TimeoutException] {
            continue
        }
    }
} finally {
    $serial.Close()
}
