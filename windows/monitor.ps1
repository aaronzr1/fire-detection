param(
    [string]$Port = "COM19",
    [int]$Baud = 115200
)

$python = Join-Path $PSScriptRoot ".." ".venv\Scripts\python.exe"
& $python -m serial.tools.miniterm $Port $Baud --raw
