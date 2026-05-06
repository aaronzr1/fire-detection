param(
    [string]$Port = "COM18",
    [int]$Baud = 115200
)

$root = Split-Path $PSScriptRoot -Parent
$python = Join-Path $root ".venv\Scripts\python.exe"
& $python (Join-Path $root "monitor.py") --port $Port --baud $Baud
