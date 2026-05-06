param(
    [Parameter(Mandatory=$true)][string]$Sketch,
    [string]$Port = "COM19"
)

$FQBN = "esp8266:esp8266:nodemcuv2"
$root = Split-Path $PSScriptRoot -Parent
$cli = Join-Path $root "binaries\arduino-cli.exe"
if (-not (Test-Path $cli)) { $cli = "arduino-cli" }

if (-not (Test-Path (Join-Path $root $Sketch) -PathType Container)) {
    Write-Error "Sketch folder '$Sketch' not found"
    exit 1
}

Write-Host "==> Compiling $Sketch..."
& $cli compile --fqbn $FQBN (Join-Path $root $Sketch)
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Uploading to $Port..."
& $cli upload --fqbn $FQBN --port $Port (Join-Path $root $Sketch)
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Done!"
