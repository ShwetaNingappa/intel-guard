param(
  [switch]$Install
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$backendDir = Join-Path $repoRoot 'backend'

Write-Host "[backend] Working dir: $backendDir"
Set-Location $backendDir

# Optional one-time install
if ($Install -or -not (Test-Path (Join-Path $backendDir '.venv'))) {
  Write-Host "[backend] Creating venv and installing requirements..."
  & py -m venv .venv
  & .\.venv\Scripts\python -m pip install --upgrade pip
  & .\.venv\Scripts\pip install -r requirements.txt
}

# Launch API server
$pythonExe = if (Test-Path (Join-Path $backendDir '.venv\Scripts\python.exe')) { '.\.venv\Scripts\python' } else { 'py' }
Write-Host "[backend] Starting Uvicorn on http://localhost:8000 ..."
& $pythonExe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload