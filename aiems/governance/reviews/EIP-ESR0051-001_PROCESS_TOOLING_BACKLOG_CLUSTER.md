# EIP-ESR0051-001 - Process/Tooling Backlog Cluster (EBG-0090 through EBG-0096)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0051-001 |
| Title | Engineering Implementation Package: WP1 Process/Tooling Backlog Cluster |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0051 |
| Work Package | WP1 |

---

# 2. Purpose

Implements ESR-0051 WP1: clears the EBG-0090 through EBG-0096 Approved Backlog process/tooling cluster, per the Programme Sponsor's session-open objective selection and two follow-up decisions (include the four home-directory items; proceed with Windows Credential Manager for EBG-0095, documented as a partial improvement rather than a full agent-proof boundary).

---

# 3. Repository Context Investigated

* `~/approve` / `~/reject` (Sponsor's home directory, outside this repository): bash wrappers, currently `source ~/.sponsor_env; cd "/i/Project AI" && git pull --quiet; python scripts/sponsor_client.py "$1" "$2" --decision approve --note "${3:-}"` - session identifier is `$1`, work package `$2`.
* `~/.sponsor_env`: two `export` lines (values not inspected), sourced by both wrappers.
* `~/.current_session`: does not currently exist.
* `scripts/sponsor_client.py`: CLI unchanged by this package - `<session> <work_package> --decision approve|reject [--note]`, reads `AIEMS_SPONSOR_TOKEN`/`AIEMS_SPONSOR_URL` from environment only, POSTs to `/decisions`.
* `scripts/sponsor_approval_service.py`: exposes exactly two routes - `GET /decisions/latest` (agent-token gated) and `POST /decisions` (sponsor-token gated). No existing unauthenticated health route.
* `scripts/start-jarvis.bat`: existing repo-committed launcher precedent (EBG-0078) that EBG-0093 mirrors.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] WP0B Session Initialisation guidance: currently has no step for a per-session local-state file.

---

# 4. Scope by Item

## 4A. EBG-0090 - CLI-Driven Coding Agent Cost-Avoidance Investigation

**Investigation only, no production wiring** (per the backlog item's own explicit constraint). Scope: run one concrete research-type task side-by-side through (a) Sentinel's existing direct-API route and (b) a non-interactive `claude -p --no-session-persistence` invocation; compare cost, latency and output quality; record findings and a recommendation directly in EBG-0090's own EBR-0001 entry (Investigated, not Completed - no code changes result from an investigation). No new script is added to the repository for a one-time spike.

## 4B. EBG-0091 - Streamline Daily Sponsor Approval Command

* Update `~/approve` and `~/reject` (Sponsor's home directory) to drop the explicit session argument, reading it instead from `~/.current_session`:
  ```bash
  #!/usr/bin/env bash
  source ~/.sponsor_env
  cd "/i/Project AI" && git pull --quiet
  session="$(cat ~/.current_session 2>/dev/null)"
  if [ -z "$session" ]; then
    echo "ERROR: no current session in ~/.current_session - run WP0B's session-open step, or edit this file to pass a session explicitly." >&2
    exit 1
  fi
  python scripts/sponsor_client.py "$session" "$1" --decision approve --note "${2:-}"
  ```
  (reject identical, `--decision reject`). New usage: `~/approve <work_package> "note"`.
* Create `~/.current_session` now, containing `ESR-0051`.
* Add a new WP0B step to [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]]'s Engineering Session Lifecycle section: update `~/.current_session` (Sponsor-side file, outside the repository) to the active session identifier as part of WP0B.
* `sponsor_client.py` itself is unchanged - keeps the security-relevant script's interface stable, all the change is in the outer wrapper.

## 4C. EBG-0092 - Formalise Scope-Creep-Flagging Discipline into PBK-0001

Add a new PBK-0001 section (alongside Feature-First Delivery Discipline and Operational Verification Before Reporting) recording the already-adopted practice: the Engineering Implementer shall flag, plainly and by name, any proposed mid-Work-Package addition that would expand that WP's scope or create a dependency on another still-pending WP, and shall require explicit Programme Sponsor override before proceeding rather than silently accommodating it. Documentation only.

## 4D. EBG-0093 - PC-Side Installer Script for the Sponsor Approval Service

New repository script `scripts/install-sponsor-approval-service.ps1` (mirrors `start-jarvis.bat`'s precedent): checks for Tailscale (`Get-Command tailscale`), offers `winget install tailscale.tailscale` if absent; prompts interactively (`Read-Host -AsSecureString` where applicable) for `AIEMS_SPONSOR_TOKEN`/`AIEMS_AGENT_TOKEN` for this session only (never written to disk by this script); starts `python scripts/sponsor_approval_service.py` and `tailscale serve`. No credential persistence in this item - that is EBG-0095's separate, explicitly-scoped concern.

## 4E. EBG-0094 - Self-Service Sponsor Approval Service Status Check

New home-directory script `~/bridge-status`: a bare, unauthenticated HTTP connectivity probe against `$AIEMS_SPONSOR_URL` (e.g. `curl -s -o /dev/null -w "%{http_code}"` against the base URL or `/decisions/latest` with no token) - reports reachable/unreachable and the raw status code, revealing nothing an unauthenticated passive observer of that same route couldn't already see. No changes to `sponsor_approval_service.py`.

## 4F. EBG-0095 - Auto-Start the Sponsor Approval Service on Windows Login

**Explicitly documented as a deliberate, accepted exception, not a resolved boundary** (per Programme Sponsor decision, confirmed correct by Codex design review): Windows Credential Manager / DPAPI protects the stored token against a different Windows user account or copying the file to another machine, but **does not** protect against another process running under the same Windows account - including a future Claude Code or Codex CLI session on this machine. This is a deliberate relaxation of the original hard "must never be agent-reachable" boundary STD-0006/ADR-0022 otherwise require for authority-bearing credentials, accepted here specifically for the auto-start convenience this item provides, and must not be characterised in implementation, EBR-0001, or any future artefact as fully satisfying STD-0006/ADR-0022's original strong no-agent-reachable-token bar. It is recorded here and in EBG-0095's own EBR-0001 entry as a known, accepted, partial improvement (reduced exposure surface versus a plaintext file or an always-inherited environment variable), and as an explicit, named exception to that standard - not a claim that the gap is closed.

Scope:
* New repository script `scripts/start_sponsor_approval_service_autostart.ps1`: reads `AIEMS_SPONSOR_TOKEN`/`AIEMS_AGENT_TOKEN` from Windows Credential Manager via a small self-contained inline-C#/P-Invoke `CredRead` wrapper (no third-party module dependency, matching the no-discretionary-spend/self-hosted default), sets them as process-scoped environment variables, and starts `scripts/sponsor_approval_service.py` plus `tailscale serve`.
* One-time host-side setup (performed directly on this machine, not committed to the repository): store both tokens in Windows Credential Manager (generic credentials, e.g. `cmdkey /generic:AIEMS_SPONSOR_TOKEN /user:sponsor /pass:...`, or the same P/Invoke wrapper's write path) and register a Windows Scheduled Task that runs the new script at user login.

## 4G. EBG-0096 - Automate the Claude<->Codex Review Handoff

Primarily a documentation update, not new code: today's live round trip (this session's own `submit-to-review` -> `codex exec -s workspace-write` -> `return-findings`, twice, both fully unattended after the `default.rules` execpolicy fix) is genuine new evidence beyond what EBG-0096's own text anticipated - a fully automated round trip via `workspace-write`, not only the read-only-plus-Claude-relay fallback it previously recommended. Update EBG-0096's EBR-0001 entry to record this evidence and revise its recommendation: `workspace-write` plus a correctly-populated `default.rules` allowlist is now the primary recommended mode; the read-only-plus-relay pattern remains documented as the fallback if execpolicy issues recur. No new script - the automation already exists (`scripts/aiems_bridge.py`, `codex exec`); this closes the item by recording that it now works end-to-end, twice, live.

---

# 5. Validation

* `python scripts/validate_repository.py` (full mode) after all changes.
* `python -m pytest jarvis/tests sentinel scripts/tests` - no production code touched by this WP, so the count should remain unchanged (512 passed, 1 skipped).
* Live smoke test of `~/approve`/`~/reject`'s new argument shape and `~/bridge-status` against the real running Sponsor Approval Service, on this machine, before considering EBG-0091/0094 Complete.
* Live verification that the EBG-0095 Scheduled Task actually starts the service correctly, before considering it Complete.

---

# 6. Explicitly Excluded

* Any change to `sponsor_client.py`'s or `sponsor_approval_service.py`'s security-relevant interfaces or token-gating logic.
* Any credential value appearing in this document, a commit message, or a log.
* A full low-privilege-account redesign for EBG-0095 (scoped as a separate future item if ever pursued).
* Any production wiring of EBG-0090's investigated capability into Guardian's conversational path.

---

# 7. Codex Design Review

Submitted via the AIEMS Exchange Bridge (`ESR-0051`/`WP1`). **Verdict: Pass with one non-blocking governance note**, timestamp 2026-08-22T11:23:17Z. Codex independently re-verified Section 3's file claims and confirmed Section 4's scope matches each EBG's own ask without exceeding it, and found no hidden WP-independence-violating dependency between the seven items. The one note - that EBG-0095 is a deliberate, named exception to STD-0006/ADR-0022's original strong boundary, not a resolved instance of it - is folded into Section 4F above.

---

# 8. Related Artefacts

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0090 through EBG-0096, all updated by this package.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - gains the WP0B `~/.current_session` step (EBG-0091) and the new scope-creep-flagging section (EBG-0092).
* [[ESR-0051_ENGINEERING_SESSION_REPORT|ESR-0051]] - this session's report, WP1.
* ADR-0022 / EIP-ESR0030-001 - Sponsor Approval Service separation-of-duties design this package must not weaken.
* STD-0006 - Configuration and Secrets Standard governing the token-handling constraints throughout.
