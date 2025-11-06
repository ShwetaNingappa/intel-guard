param(
  [switch]$Install
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$startBackend = Join-Path $PSScriptRoot 'Start-Backend.ps1'
$startFrontend = Join-Path $PSScriptRoot 'Start-Frontend.ps1'

# Choose shell executable (fallback to Windows PowerShell if pwsh is unavailable)
$shellExe = if (Get-Command pwsh -ErrorAction SilentlyContinue) { 'pwsh' } else { 'powershell' }

Write-Host "[all] Launching backend and frontend in separate terminals using $shellExe..."

# Backend window
$backendArgs = if ($Install) { '-ExecutionPolicy Bypass -NoExit -File', "`"$startBackend`"", '-Install' } else { '-ExecutionPolicy Bypass -NoExit -File', "`"$startBackend`"" }
Start-Process $shellExe -ArgumentList $backendArgs -WorkingDirectory $repoRoot -WindowStyle Normal

# Frontend window
$frontendArgs = if ($Install) { '-ExecutionPolicy Bypass -NoExit -File', "`"$startFrontend`"", '-Install' } else { '-ExecutionPolicy Bypass -NoExit -File', "`"$startFrontend`"" }
Start-Process $shellExe -ArgumentList $frontendArgs -WorkingDirectory $repoRoot -WindowStyle Normal

Write-Host "[all] Done. Backend: http://localhost:8000  |  Frontend: http://localhost:5173"
