# Checks that the tools required to build and run Project JARVIS AI are present
# on this machine, and offers to install anything missing via winget.
# See scripts/PREREQUISITES.md for what each tool is used for.
#
# Exit code: 0 if every tool is present (or was just installed and verified),
# 1 if anything is still missing (declined, failed to install, or needs a
# fresh terminal session before it will be detected).

$ErrorActionPreference = "Stop"

function Refresh-Path {
    $machine = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    $user = [System.Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path = @($machine, $user) -join ";"
}

$tools = @(
    @{
        Name      = "Git"
        Check     = { [bool](Get-Command git -ErrorAction SilentlyContinue) }
        WingetId  = "Git.Git"
        ManualUrl = "https://git-scm.com/download/win"
    },
    @{
        Name      = "Node.js LTS (includes npm)"
        Check     = { [bool](Get-Command node -ErrorAction SilentlyContinue) }
        WingetId  = "OpenJS.NodeJS.LTS"
        ManualUrl = "https://nodejs.org/"
    },
    @{
        Name      = "Rust toolchain (rustup + cargo)"
        Check     = { [bool](Get-Command cargo -ErrorAction SilentlyContinue) }
        WingetId  = "Rustlang.Rustup"
        WingetOverride = "-y"
        ManualUrl = "https://rustup.rs/"
        Note      = "Install Microsoft C++ Build Tools first - rustup needs the MSVC linker on Windows."
    },
    @{
        Name      = "Python 3.12+"
        Check     = {
            $cmd = Get-Command python -ErrorAction SilentlyContinue
            if (-not $cmd -or $cmd.Source -match '\\WindowsApps\\python(\.exe)?$') {
                # Not installed - Windows ships a "python" shim under WindowsApps that
                # just opens the Microsoft Store when invoked, so don't run it.
                return $false
            }
            try {
                $verOutput = & python --version
            } catch {
                return $false
            }
            if ($verOutput -match '(\d+)\.(\d+)\.(\d+)') {
                $major = [int]$Matches[1]; $minor = [int]$Matches[2]
                return ($major -gt 3) -or ($major -eq 3 -and $minor -ge 12)
            }
            return $false
        }
        WingetId  = "Python.Python.3.12"
        ManualUrl = "https://www.python.org/downloads/"
    },
    @{
        Name      = "Microsoft C++ Build Tools (MSVC, required by Rust/Tauri)"
        Check     = {
            $vswhere = Join-Path ${env:ProgramFiles(x86)} "Microsoft Visual Studio\Installer\vswhere.exe"
            if (-not (Test-Path $vswhere)) { return $false }
            $found = & $vswhere -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
            return [bool]$found
        }
        WingetId  = "Microsoft.VisualStudio.2022.BuildTools"
        WingetOverride = "--wait --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
        ManualUrl = "https://visualstudio.microsoft.com/visual-cpp-build-tools/"
        Note      = "This install can take several minutes. If installing manually, select the 'Desktop development with C++' workload."
    },
    @{
        Name      = "WebView2 Runtime (renders the Tauri UI)"
        Check     = {
            $guid = "{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
            foreach ($root in @(
                "HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\$guid",
                "HKLM:\SOFTWARE\Microsoft\EdgeUpdate\Clients\$guid",
                "HKCU:\SOFTWARE\Microsoft\EdgeUpdate\Clients\$guid"
            )) {
                if (Test-Path $root) {
                    $pv = (Get-ItemProperty -Path $root -ErrorAction SilentlyContinue).pv
                    if ($pv -and $pv -ne "0.0.0.0") { return $true }
                }
            }
            return $false
        }
        WingetId  = "Microsoft.EdgeWebView2Runtime"
        ManualUrl = "https://developer.microsoft.com/microsoft-edge/webview2/"
        Note      = "Usually preinstalled on Windows 10 21H2+ and Windows 11 - only missing on older or stripped-down images."
    }
)

Write-Host "==> Checking prerequisites..." -ForegroundColor Cyan

$wingetAvailable = [bool](Get-Command winget -ErrorAction SilentlyContinue)
if (-not $wingetAvailable) {
    Write-Host "    winget was not found, so missing tools can't be auto-installed." -ForegroundColor Yellow
    Write-Host "    Get it via 'App Installer' in the Microsoft Store: https://aka.ms/getwinget" -ForegroundColor Yellow
}

$missing = @()
$needsRestart = $false

foreach ($tool in $tools) {
    if (& $tool.Check) {
        Write-Host "  [OK]      $($tool.Name)" -ForegroundColor Green
        continue
    }

    Write-Host "  [MISSING] $($tool.Name)" -ForegroundColor Yellow
    if ($tool.Note) {
        Write-Host "            $($tool.Note)" -ForegroundColor DarkGray
    }

    if (-not $wingetAvailable) {
        Write-Host "            Install manually: $($tool.ManualUrl)" -ForegroundColor DarkGray
        $missing += $tool.Name
        continue
    }

    $answer = Read-Host "            Install now via winget? [Y/n]"
    if ($answer -match '^(n|no)$') {
        Write-Host "            Skipped. Install manually: $($tool.ManualUrl)" -ForegroundColor DarkGray
        $missing += $tool.Name
        continue
    }

    Write-Host "            Installing via winget (id: $($tool.WingetId))..." -ForegroundColor Cyan
    $installArgs = @("install", "--id", $tool.WingetId, "-e", "--source", "winget", "--accept-package-agreements", "--accept-source-agreements")
    if ($tool.WingetOverride) {
        $installArgs += @("--override", $tool.WingetOverride)
    }
    & winget @installArgs
    $installExitCode = $LASTEXITCODE

    if ($installExitCode -ne 0) {
        Write-Host "            winget install failed (exit $installExitCode). Install manually: $($tool.ManualUrl)" -ForegroundColor Red
        $missing += $tool.Name
        continue
    }

    Refresh-Path
    if (& $tool.Check) {
        Write-Host "            Installed and detected." -ForegroundColor Green
    } else {
        Write-Host "            Installed, but not detected in this session yet. Close and reopen your terminal, then re-run this script." -ForegroundColor Yellow
        $needsRestart = $true
        $missing += $tool.Name
    }
}

Write-Host ""
if ($missing.Count -eq 0) {
    Write-Host "All prerequisites satisfied." -ForegroundColor Green
    exit 0
}

Write-Host "Still missing: $($missing -join ', ')" -ForegroundColor Red
if ($needsRestart) {
    Write-Host "One or more tools were installed but need a fresh terminal session to be detected on PATH." -ForegroundColor Yellow
}
exit 1
