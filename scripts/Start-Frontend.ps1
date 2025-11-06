param(
  [switch]$Install
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$frontendDir = Join-Path $repoRoot 'frontend'

Write-Host "[frontend] Working dir: $frontendDir"
Set-Location $frontendDir

# Resolve npm executable explicitly (npm.cmd on Windows)
$npmCmd = (Get-Command npm.cmd -ErrorAction SilentlyContinue)
if (-not $npmCmd) { $npmCmd = (Get-Command npm -ErrorAction SilentlyContinue) }
if (-not $npmCmd) {
  Write-Error "npm was not found in PATH. Please install Node.js from https://nodejs.org and ensure npm is on PATH."
  exit 1
}
$npm = $npmCmd.Source

if ($Install -or -not (Test-Path (Join-Path $frontendDir 'node_modules'))) {
  Write-Host "[frontend] Installing dependencies (npm ci)..."
  & $npm 'ci'
}

Write-Host "[frontend] Starting Vite dev server on http://localhost:5173 ..."
& $npm 'run' 'dev'
