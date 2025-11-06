param(
  [switch]$Install
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$backendDir = Join-Path $repoRoot 'backend'
$frontendDir = Join-Path $repoRoot 'frontend'

Write-Host "[combined] Starting backend and frontend in this window...`n"

# Backend job
$backendJob = Start-Job -Name backend -ScriptBlock {
  param($dir, $Install)
  Set-Location $dir
  if ($Install -or -not (Test-Path (Join-Path $dir '.venv'))) {
    try { & py -m venv .venv } catch {}
    try { & .\.venv\Scripts\python -m pip install --upgrade pip } catch {}
    try { & .\.venv\Scripts\pip install -r requirements.txt } catch {}
  }
  $python = if (Test-Path '.venv\Scripts\python.exe') { '.\\.venv\\Scripts\\python' } else { 'py' }
  Write-Host "[backend] Uvicorn on http://localhost:8000"
  & $python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
} -ArgumentList $backendDir, $Install

# Frontend job
$frontendJob = Start-Job -Name frontend -ScriptBlock {
  param($dir, $Install)
  Set-Location $dir
  $npmCmd = (Get-Command npm.cmd -ErrorAction SilentlyContinue)
  if (-not $npmCmd) { $npmCmd = (Get-Command npm -ErrorAction SilentlyContinue) }
  if (-not $npmCmd) { throw "npm not found in PATH" }
  $npm = $npmCmd.Source
  if ($Install -or -not (Test-Path (Join-Path $dir 'node_modules'))) {
    & $npm 'ci'
  }
  Write-Host "[frontend] Vite on http://localhost:5173"
  & $npm 'run' 'dev'
} -ArgumentList $frontendDir, $Install

try {
  Write-Host "[combined] Press Ctrl+C to stop. Streaming logs...`n"
  while ($true) {
    foreach ($j in @($backendJob, $frontendJob)) {
      $o = Receive-Job -Job $j -Keep
      if ($o) {
        $prefix = "[$($j.Name)]"
        $o | ForEach-Object { Write-Host "$prefix $_" }
      }
    }
    Start-Sleep -Milliseconds 500
  }
} finally {
  Get-Job | Stop-Job -ErrorAction SilentlyContinue | Out-Null
  Get-Job | Remove-Job -Force -ErrorAction SilentlyContinue | Out-Null
}
