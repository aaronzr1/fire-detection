# Activate the virtual environment for this project
# Usage: . .\venv.ps1  (note the dot-source)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
$projectRoot = Split-Path $PSScriptRoot -Parent
$activate = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"
if (-not (Test-Path $activate)) {
    Write-Host "Error: .venv not found. Run .\setup.ps1 first." -ForegroundColor Red
    return
}
. $activate
