# ESR-0025A - Post-Closure Engineering Addendum

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0025A |
| Title | Post-Closure Engineering Addendum - AIEMS Exchange Bridge Preflight Fix |
| Version | 1.0 |
| Status | Complete |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Parent Session | [[ESR-0025_ENGINEERING_SESSION_REPORT|ESR-0025]] |
| Repository Baseline | [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] |
| Classification | Internal |
| Date Opened | 17 July 2026 |

---

# 2. Executive Summary

Following ESR-0025's formal closure, the Programme Sponsor asked whether EIP-ESR0025-001 v1.2's disclosed gap - "neither `claude` nor `codex` is on the Engineering Implementer's sandboxed shell `PATH`" - meant the AIEMS Exchange Bridge (`scripts/aiems_bridge.py`, EBG-0057) simply could not be used for its intended purpose. The honest answer required testing, not speculation: three of the bridge's five commands (`submit-to-review`, `return-findings`, `submit-response`) hard-require both CLIs to be present via a preflight check, and neither existed on this machine, so those commands were confirmed to fail outright.

The Programme Sponsor then authorised installing and authenticating both CLIs live to determine whether this was a fixable environment gap or a fundamental design mismatch. Doing so surfaced a **second, genuine defect**, invisible until both tools actually existed on a Windows machine: `run_preflight()`'s `subprocess.run([tool, "--version"], ...)` call crashed with an unhandled `FileNotFoundError` (Windows error code 2), because npm installs global Node CLI tools as `.CMD` batch-file shims, and Windows' process-creation API cannot launch a `.CMD` file directly without going through the command shell.

The Programme Sponsor explicitly authorised fixing this immediately - **a deliberate, disclosed deviation from PBK-0001's standard Working Report Lifecycle** (Engineering Implementer drafts an Engineering Implementation Package, Engineering Reviewer reviews it, Programme Sponsor approves, only then is it implemented). No EIP was drafted and the Engineering Reviewer has not reviewed this specific diff. This is recorded here in full rather than folded silently into EIP-ESR0025-001's version history, consistent with this project's established practice of disclosing process deviations rather than normalising them (see ESR-0023 Section 9.1/10.1-10.2, EE-0001 Section 7.4).

This work is folded into ESR-0025 as a post-closure addendum rather than opening ESR-0026, consistent with the [[ESR-0016A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0016A]]/[[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] precedent: this is a small, well-understood bug fix directly continuing ESR-0025's own bridge work, not a new engineering objective warranting a fresh session.

---

# 3. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP1 | Install and authenticate `codex`/`claude` CLIs; diagnose and fix the resulting `run_preflight()` Windows subprocess bug; verify the full five-command bridge cycle live | Complete (this addendum) |

---

# 4. WP1 - Preflight Windows Subprocess Invocation Fix

**No EIP - Programme Sponsor-authorised direct implementation.** The Programme Sponsor's own words: "Fix it now - I am authorising the break from standard procedure." This is recorded as an explicit, one-off authorisation, not a standing precedent for skipping the Working Report Lifecycle in future sessions.

**Diagnosis, in order:**

1. `codex` CLI installed via `npm install -g @openai/codex` (`codex-cli 0.144.5`). Authenticated via `codex login` (browser-based ChatGPT sign-in, run by the Programme Sponsor directly since it requires an interactive terminal and browser neither available to the Engineering Implementer's sandboxed shell). `codex login status` confirmed: "Logged in using ChatGPT" - the Programme Sponsor's existing Business plan allowance, not separate billed API usage, matching the cost preference already recorded in EBG-0057's own note (ESR-0019 finding).
2. `claude` CLI (`@anthropic-ai/claude-code`) installed the same way for symmetry with the preflight's own requirement; `claude --version` confirmed `2.1.212 (Claude Code)`.
3. With both binaries genuinely on `PATH`, `scripts/aiems_bridge.py submit-to-review` was retried and crashed: `FileNotFoundError: [WinError 2] The system cannot find the file specified`, inside `run_preflight()`'s `subprocess.run([tool, "--version"], ...)` call.
4. Root-caused directly: `shutil.which("codex")` resolves to `...\npm\codex.CMD` on this machine (confirmed via a Python one-liner) - an npm-generated batch-file shim, not a native executable. Windows' `CreateProcess` API (which `subprocess.run` calls without `shell=True`) cannot launch `.CMD` files directly; only `.exe` files or invocation through `cmd.exe` (`shell=True`) work. Reproduced in isolation with a minimal `subprocess.run(['codex', '--version'])` call before touching any bridge code, confirming the bug was in the invocation method, not the tool itself.
5. A second, independent issue was found while fixing the first: the existing code called `["codex", "login-status"]` (one hyphenated argument), which is not a real Codex CLI subcommand - it returns `Error: stdin is not a terminal` rather than the login status. The real subcommand is `codex login status` (two separate arguments, confirmed via `codex login --help`).

**Fix delivered**, `scripts/aiems_bridge.py`, `run_preflight()`:

- Both `subprocess.run` calls now pass `shell=(sys.platform == "win32")`. Since the invoked tool names (`"claude"`, `"codex"`) are hardcoded literals, never derived from user or repository input, this introduces no shell-injection risk.
- `["codex", "login-status"]` corrected to `["codex", "login", "status"]`.

**Test added**, `scripts/tests/test_aiems_bridge.py`: `test_run_preflight_invokes_subprocess_with_shell_true_on_windows` mocks `shutil.which` and `subprocess.run` directly and asserts the real `run_preflight()` implementation is exercised (not the file's autouse stub, which replaces `run_preflight` for every other test) via a module-level reference (`_real_run_preflight`) captured at import time, before the autouse fixture patches the module attribute. Asserts `shell` matches `sys.platform == "win32"` and that all three expected subprocess calls (`claude --version`, `codex --version`, `codex login status`) occur. One authoring mistake self-caught during this work: the new test was initially inserted mid-file, silently absorbing the *previous* test's final assertion line into itself - caught by the test failing with a `NameError` for an undefined fixture variable, then corrected by restoring the assertion to its original test.

**Live verification, full five-command cycle**, disposable test sessions (`PREFLIGHT-TEST`/`WP0`, `SMOKE-TEST`/`WP1`), cleaned up afterward (`.aiems-exchange/` is gitignored, not part of the repository):

- `init`, `submit-to-review`, `return-findings`, `sponsor-decision --decision approve`, and `submit-response` all completed without error - including `submit-response`, the most heavily gated command (authorisation, repository-drift and validation-pass checks, all under the Work Package lock).
- This proves the commands no longer crash and the gating logic functions correctly against the real, authenticated CLIs. It does **not** prove Codex will autonomously act on its own turn without the Programme Sponsor prompting it - the Engineering Implementer ran all five commands directly for this test, standing in for both roles. Achieving genuinely unattended handover would additionally require the Programme Sponsor to run the `codex` CLI as an agent pointed at this repository and instruct it to check the exchange itself - not yet attempted.

**Validation:** `python -m pytest` 238 passed (was 237). `python scripts/validate_repository.py` 0 errors, 104 pre-existing warnings (unchanged).

**Self-review:** the fix is scoped to exactly the two lines that construct the `subprocess.run` calls inside `run_preflight()`, plus the one incorrect argument list; no other bridge behaviour touched. `capture_evidence()`'s own `subprocess.run` calls (`python -m pytest`, `python scripts/validate_repository.py`) invoke the real Python interpreter (`sys.executable`), a native `.exe`, and were never affected by this bug.

---

# 5. Engineering Reviewer Retroactive Confirmation

This diff was implemented without a prior EIP or Engineering Reviewer review, per the Programme Sponsor's explicit real-time authorisation (Section 4). That gap is now substantially closed: once the cross-device session issue (Section 6) was resolved, the Engineering Reviewer (Codex) independently confirmed, from its own environment, without relying on this addendum's own account:

- `codex` installed, on `PATH`, `codex --help`/`codex exec --help` both functional.
- `codex login status`: "Logged in using ChatGPT."
- `codex --cd 'I:\Project AI' doctor` correctly detects this repository (`repo detected: true`, correct repo root).
- `scripts/aiems_bridge.py`'s real `run_preflight()` called directly, returning `ok=True` - the actual fix, exercised for real, not re-derived from reading the diff alone.
- Independently cited the same source locations this addendum describes (`run_preflight()`, `cmd_submit_to_review()`, `cmd_return_findings()`, `cmd_submit_response()`, and the relevant test functions), confirming its read of the code matches what was actually changed.
- Explicitly disclosed the boundary of its own check: no real `submit-to-review`/`return-findings`/`submit-response` exchange was executed - only help output and the read-only preflight probe. Conclusion offered as "based on current inspection," not asserted beyond what was actually run - the same evidentiary discipline this project expects of the Engineering Implementer.

No findings were raised. This is not a substitute for reviewing the diff itself line-by-line, but it is a genuine, independent, tool-verified confirmation that the fix works as claimed, closing the practical part of the gap even though the formal EIP-review step was skipped.

**Still not exercised, by either side:** a real, non-simulated `submit-to-review` -> `return-findings` -> `sponsor-decision` -> `submit-response` cycle where Codex plays its role autonomously (reading the transcript itself and acting on its own turn), rather than the Engineering Implementer running all five commands directly (as in Section 4's smoke test) or the Engineering Reviewer probing read-only paths (this section). Not backlogged as its own item; revisit if the Programme Sponsor wants to pursue full automation further.

---

# 6. Observed Operational Risk - Cross-Device Session Invalidation

Shortly after the fresh `codex login` on this machine, the Programme Sponsor reported a separate Codex session erroring with "Your access token could not be refreshed because you have since logged out or signed in to another account" - on a machine other than this one (a work laptop), not something running locally that this machine's testing directly touched.

This is consistent with Codex CLI (via ChatGPT login) enforcing a single active session per account: authenticating fresh on one device appears to invalidate the refresh token another device was holding. Not a defect in `scripts/aiems_bridge.py` or this addendum's fix, and not data loss.

**Resolved**: logging out of Codex within the work laptop's VS Code integration and logging back in restored it - confirming the affected session was Codex's VS Code extension specifically, not a bare CLI terminal session, and that the fix is a simple re-authentication, exactly as predicted.

**Material to future planning**, not actioned here: if this single-session behaviour is consistent, using the bridge's Codex side from more than one machine (or from both a VS Code integration and a separate CLI terminal) means each fresh login on one will silently log out the other. Worth keeping in mind when deciding where Codex CLI actually runs for this workflow, rather than assuming independent, simultaneously-valid sessions across devices or integrations. Not backlogged as its own item pending confirmation this pattern repeats.

---

# 7. Closing Statement

ESR-0025A records one authorised, disclosed deviation from the standard Working Report Lifecycle: a small, well-understood Windows subprocess bug in `scripts/aiems_bridge.py`'s preflight check, found only once both `claude` and `codex` CLIs were actually installed and authenticated on this machine for the first time, fixed directly at the Programme Sponsor's explicit real-time authorisation, and live-verified across the bridge's full five-command cycle. [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] is preserved as the current repository baseline; this addendum does not reopen [[ESR-0025_ENGINEERING_SESSION_REPORT|ESR-0025]].

---

# 8. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0025_ENGINEERING_SESSION_REPORT|ESR-0025]] | Parent closed engineering session. |
| [[ESR-0016A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0016A]] | Precedent for post-closure engineering addenda. |
| [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] | Governing implementation package for `scripts/aiems_bridge.py`, bumped 1.2 to 1.3 to record this fix. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0057's completion note updated. |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] | Current repository baseline, preserved by this addendum. |
| `scripts/aiems_bridge.py` | Fixed by this addendum (`run_preflight()`). |
| `scripts/tests/test_aiems_bridge.py` | New regression test added. |

---

# 9. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 17 July 2026 | Claude Engineering Implementer | ESR-0025A complete. Installed and authenticated `codex`/`claude` CLIs; diagnosed and fixed the resulting Windows `subprocess.run`/`.CMD`-shim preflight crash and a separate wrong-subcommand bug; added a regression test; live-verified the full five-command bridge cycle end-to-end. Programme Sponsor-authorised deviation from the standard Working Report Lifecycle, disclosed in full. Recorded an observed operational risk (Section 6, resolved): the fresh `codex login` on this machine invalidated a separate Codex session in the Programme Sponsor's work laptop VS Code integration, consistent with Codex CLI enforcing a single active session per account - resolved by logging out/back in there. Section 5 records the Engineering Reviewer's own independent retroactive confirmation (real `run_preflight()` call returning `ok=True`, environment/repo-detection checks, source citations matching this addendum, no findings raised) - substantially closing the no-review gap, though a real autonomous exchange cycle remains unexercised by either side. |
