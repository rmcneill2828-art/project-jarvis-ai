<#
.SYNOPSIS
    One-time interactive setup convenience for scripts/sponsor_approval_service.py
    (ADR-0022 / EIP-ESR0030-001), mirroring scripts/start-jarvis.bat's existing
    committed-launcher precedent (EBG-0078). Registered as EBG-0093.

.DESCRIPTION
    Checks for Tailscale, offers to install it via winget if missing, prompts
    interactively (this session only - nothing is written to disk by this
    script) for AIEMS_SPONSOR_TOKEN and AIEMS_AGENT_TOKEN, then starts the
    Sponsor Approval Service and exposes it via `tailscale serve`.

    This script never hardcodes, auto-generates, or silently persists either
    token. Persisted, unattended startup is EBG-0095's separate, explicitly
    scoped concern (scripts/start_sponsor_approval_service_autostart.ps1) -
    this script is for an interactive foreground session only.
#>

$ErrorActionPreference = "Stop"

Write-Host "== Sponsor Approval Service Setup ==" -ForegroundColor Cyan

$tailscale = Get-Command tailscale -ErrorAction SilentlyContinue
if (-not $tailscale) {
    Write-Host "Tailscale not found." -ForegroundColor Yellow
    $answer = Read-Host "Install it now via winget? (y/N)"
    if ($answer -match '^[Yy]') {
        winget install tailscale.tailscale
        Write-Host "Tailscale installed. You may need to open a new shell for PATH changes to take effect." -ForegroundColor Yellow
    } else {
        Write-Host "Tailscale is required to expose the Sponsor Approval Service. Exiting." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Tailscale found: $($tailscale.Source)" -ForegroundColor Green
}

if (-not $env:AIEMS_SPONSOR_TOKEN) {
    $secureSponsorToken = Read-Host "Enter AIEMS_SPONSOR_TOKEN (input hidden)" -AsSecureString
    $env:AIEMS_SPONSOR_TOKEN = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureSponsorToken)
    )
}

if (-not $env:AIEMS_AGENT_TOKEN) {
    $secureAgentToken = Read-Host "Enter AIEMS_AGENT_TOKEN (input hidden)" -AsSecureString
    $env:AIEMS_AGENT_TOKEN = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureAgentToken)
    )
}

Write-Host "Neither token is written to disk by this script - set for this session only." -ForegroundColor DarkGray

$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    Write-Host "Starting Sponsor Approval Service..." -ForegroundColor Cyan
    Start-Process -FilePath "python" -ArgumentList "scripts/sponsor_approval_service.py" -NoNewWindow
    Start-Sleep -Seconds 2

    Write-Host "Starting tailscale serve..." -ForegroundColor Cyan
    Start-Process -FilePath "tailscale" -ArgumentList "serve" -NoNewWindow

    Write-Host "Setup complete. The service and tailscale serve are running in this session." -ForegroundColor Green
} finally {
    Pop-Location
}
