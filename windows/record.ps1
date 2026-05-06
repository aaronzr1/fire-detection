# Record sensor data via record.py
# Usage: .\record.ps1 <label> [-Port COM3] [-Baud 115200]
#   e.g: .\record.ps1 normal
#        .\record.ps1 flame -Port COM4

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Label,
    [string]$Port = "COM3",
    [int]$Baud = 115200
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path $PSScriptRoot -Parent

# Activate venv
$venvActivate = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"
if (-not (Test-Path $venvActivate)) {
    Write-Host "Error: .venv not found. Run .\setup.ps1 first." -ForegroundColor Red
    exit 1
}
. $venvActivate

Push-Location $projectRoot
python record.py $Label --port $Port --baud $Baud
Pop-Location
