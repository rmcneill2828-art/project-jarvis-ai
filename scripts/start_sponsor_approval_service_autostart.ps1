<#
.SYNOPSIS
    Unattended, login-time starter for scripts/sponsor_approval_service.py
    (EBG-0095), reading credentials from Windows Credential Manager instead
    of requiring interactive entry at every boot.

.DESCRIPTION
    EXPLICIT SECURITY NOTE (Programme Sponsor decision, ESR-0051 WP1,
    Codex-confirmed at design review): Windows Credential Manager / DPAPI
    protects the stored token against a different Windows user account, or
    against the credential being copied to another machine. It does NOT
    protect against another process running under the SAME Windows account
    reading it - including a future Claude Code or Codex CLI session on
    this machine. This is a deliberate, named, accepted EXCEPTION to
    STD-0006/ADR-0022's original hard "must never be agent-reachable"
    boundary for authority-bearing credentials, made specifically to gain
    unattended login-time startup. It is NOT a claim that this script
    closes that gap, and must never be described as such in any future
    artefact.

    Two modes:

    -Setup   : prompts interactively for AIEMS_SPONSOR_TOKEN and
               AIEMS_AGENT_TOKEN and stores them as generic credentials in
               Windows Credential Manager. MUST be run directly by the
               Programme Sponsor, from their own interactive terminal -
               never from an agent-reachable environment - since it is the
               one place either token's plaintext value passes through the
               invoking process. Run once (or whenever tokens rotate).

    (default): reads both tokens back from Credential Manager via a
               self-contained inline P/Invoke CredRead wrapper (no
               third-party module dependency), sets them as this process's
               own environment variables, and starts
               scripts/sponsor_approval_service.py and `tailscale serve`.
               This is the mode a Windows Scheduled Task should invoke at
               login.

.EXAMPLE
    # One-time, run by the Programme Sponsor personally:
    .\start_sponsor_approval_service_autostart.ps1 -Setup

    # What the Scheduled Task actually runs at login:
    .\start_sponsor_approval_service_autostart.ps1
#>

param(
    [switch]$Setup
)

$ErrorActionPreference = "Stop"

$credTargetSponsor = "AIEMS_SPONSOR_TOKEN"
$credTargetAgent = "AIEMS_AGENT_TOKEN"

Add-Type -Namespace AiemsCred -Name Native -MemberDefinition @'
using System;
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Sequential)]
public struct CREDENTIAL {
    public int Flags;
    public int Type;
    public IntPtr TargetName;
    public IntPtr Comment;
    public long LastWritten;
    public int CredentialBlobSize;
    public IntPtr CredentialBlob;
    public int Persist;
    public int AttributeCount;
    public IntPtr Attributes;
    public IntPtr TargetAlias;
    public IntPtr UserName;
}

[DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
public static extern bool CredRead(string target, int type, int reservedFlag, out IntPtr credentialPtr);

[DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
public static extern bool CredWrite(ref CREDENTIAL credential, int flags);

[DllImport("advapi32.dll", SetLastError = true)]
public static extern void CredFree(IntPtr cred);
'@ -PassThru | Out-Null

function Read-GenericCredentialSecret {
    param([string]$Target)
    $credPtr = [IntPtr]::Zero
    $ok = [AiemsCred.Native]::CredRead($Target, 1, 0, [ref]$credPtr) # 1 = CRED_TYPE_GENERIC
    if (-not $ok) {
        throw "No Credential Manager entry found for '$Target'. Run this script with -Setup first."
    }
    try {
        $cred = [System.Runtime.InteropServices.Marshal]::PtrToStructure($credPtr, [type][AiemsCred.Native+CREDENTIAL])
        if ($cred.CredentialBlobSize -eq 0) { return "" }
        $bytes = New-Object byte[] $cred.CredentialBlobSize
        [System.Runtime.InteropServices.Marshal]::Copy($cred.CredentialBlob, $bytes, 0, $cred.CredentialBlobSize)
        return [System.Text.Encoding]::Unicode.GetString($bytes)
    } finally {
        [AiemsCred.Native]::CredFree($credPtr)
    }
}

function Write-GenericCredentialSecret {
    param([string]$Target, [string]$Secret)
    $bytes = [System.Text.Encoding]::Unicode.GetBytes($Secret)
    $blobPtr = [System.Runtime.InteropServices.Marshal]::AllocHGlobal($bytes.Length)
    try {
        [System.Runtime.InteropServices.Marshal]::Copy($bytes, 0, $blobPtr, $bytes.Length)
        $cred = New-Object AiemsCred.Native+CREDENTIAL
        $cred.Type = 1 # CRED_TYPE_GENERIC
        $cred.TargetName = [System.Runtime.InteropServices.Marshal]::StringToCoTaskMemUni($Target)
        $cred.CredentialBlobSize = $bytes.Length
        $cred.CredentialBlob = $blobPtr
        $cred.Persist = 2 # CRED_PERSIST_LOCAL_MACHINE
        $cred.UserName = [System.Runtime.InteropServices.Marshal]::StringToCoTaskMemUni("aiems")
        $ok = [AiemsCred.Native]::CredWrite([ref]$cred, 0)
        [System.Runtime.InteropServices.Marshal]::FreeCoTaskMem($cred.TargetName)
        [System.Runtime.InteropServices.Marshal]::FreeCoTaskMem($cred.UserName)
        if (-not $ok) { throw "CredWrite failed for '$Target' (Win32 error $([System.Runtime.InteropServices.Marshal]::GetLastWin32Error()))." }
    } finally {
        [System.Runtime.InteropServices.Marshal]::FreeHGlobal($blobPtr)
    }
}

if ($Setup) {
    Write-Host "== Storing AIEMS tokens in Windows Credential Manager ==" -ForegroundColor Cyan
    Write-Host "SECURITY NOTE: this is a deliberate exception to the normal 'never agent-reachable' rule for these tokens - see this script's own header comment." -ForegroundColor Yellow
    $sponsorSecure = Read-Host "Enter AIEMS_SPONSOR_TOKEN (input hidden)" -AsSecureString
    $agentSecure = Read-Host "Enter AIEMS_AGENT_TOKEN (input hidden)" -AsSecureString
    $sponsorPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($sponsorSecure))
    $agentPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($agentSecure))
    Write-GenericCredentialSecret -Target $credTargetSponsor -Secret $sponsorPlain
    Write-GenericCredentialSecret -Target $credTargetAgent -Secret $agentPlain
    Write-Host "Stored. Register a Windows Scheduled Task to run this script (without -Setup) at login." -ForegroundColor Green
    exit 0
}

$env:AIEMS_SPONSOR_TOKEN = Read-GenericCredentialSecret -Target $credTargetSponsor
$env:AIEMS_AGENT_TOKEN = Read-GenericCredentialSecret -Target $credTargetAgent

$repoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repoRoot
try {
    Start-Process -FilePath "python" -ArgumentList "scripts/sponsor_approval_service.py" -NoNewWindow
    Start-Sleep -Seconds 2
    Start-Process -FilePath "tailscale" -ArgumentList "serve" -NoNewWindow
} finally {
    Pop-Location
}
