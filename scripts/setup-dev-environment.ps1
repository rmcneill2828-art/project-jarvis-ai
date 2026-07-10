# Bootstraps a fresh clone of Project JARVIS AI for local development:
# installs npm and Rust dependencies, creates/updates the Python virtual
# environment, and activates the tracked pre-commit hook. Safe to re-run.

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

& "$PSScriptRoot\check-prerequisites.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "One or more prerequisites are missing. See scripts\PREREQUISITES.md, then re-run setup.bat." -ForegroundColor Red
    exit 1
}

Write-Host "==> Installing npm dependencies (from package-lock.json)..." -ForegroundColor Cyan
npm install

Write-Host "==> Building Rust/Tauri backend (from Cargo.lock - first build compiles the full dependency tree, this can take a minute or two)..." -ForegroundColor Cyan
Push-Location src-tauri
try {
    cargo build
} finally {
    Pop-Location
}

Write-Host "==> Setting up Python virtual environment (.venv)..." -ForegroundColor Cyan
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e ".[dev]"

Write-Host "==> Activating tracked pre-commit hook (git config core.hooksPath scripts/hooks)..." -ForegroundColor Cyan
git config core.hooksPath scripts/hooks

Write-Host "==> Running repository validation and the test suite as a smoke test..." -ForegroundColor Cyan
& .\.venv\Scripts\python.exe scripts\validate_repository.py
& .\.venv\Scripts\python.exe -m pytest -q

Write-Host ""
Write-Host "Setup complete." -ForegroundColor Green
Write-Host "Activate the Python environment in new shells with: .\.venv\Scripts\Activate.ps1"
