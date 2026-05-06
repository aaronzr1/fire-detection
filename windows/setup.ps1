# One-time setup: install Python + uv from binaries/, create venv, install deps
# Usage: .\setup.ps1

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path $PSScriptRoot -Parent
$binDir = Join-Path $projectRoot "binaries"

# --- Install Python ---
$pythonInstaller = Join-Path $binDir "python-3.13.13.exe"
if (-not (Test-Path $pythonInstaller)) {
    Write-Host "Error: $pythonInstaller not found" -ForegroundColor Red
    exit 1
}

# Check if Python is already installed
$pythonPath = $null
try { $pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source } catch {}

if (-not $pythonPath) {
    Write-Host "Installing Python 3.13..."
    Start-Process -Wait -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=0", "PrependPath=1", "Include_launcher=1"
    Write-Host "Python installed. You may need to restart your terminal for PATH changes." -ForegroundColor Yellow
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "User") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "Machine")
} else {
    Write-Host "Python already installed: $pythonPath"
}

# --- Set up uv ---
$uvSrc = Join-Path $binDir "uv.exe"
$uvDest = Join-Path $projectRoot "uv.exe"
if (-not (Test-Path $uvDest)) {
    Copy-Item $uvSrc $uvDest
}
$uvxSrc = Join-Path $binDir "uvx.exe"
if (Test-Path $uvxSrc) {
    Copy-Item $uvxSrc (Join-Path $projectRoot "uvx.exe") -Force
}

# --- Create venv and install deps ---
Push-Location $projectRoot
Write-Host "Creating virtual environment..."
& "$uvDest" venv .venv

Write-Host "Installing dependencies..."
$wheelPath = Join-Path $binDir "pyserial-3.5-py2.py3-none-any.whl"
& "$uvDest" pip install --python .venv\Scripts\python.exe $wheelPath
Pop-Location

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "Usage (from windows/ folder):"
Write-Host "  .\monitor.ps1           # monitor serial output"
Write-Host "  .\record.ps1 normal     # record sensor data"
Write-Host "  .\record.ps1 flame      # record with 'flame' label"
