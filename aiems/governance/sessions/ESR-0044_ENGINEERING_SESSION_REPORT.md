# ESR-0044 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0044 |
| Title | Engineering Session Report |
| Version | 1.2 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0044 |
| Date Opened | 30 July 2026 |
| Date Closed | 30 July 2026 |
| Closure Status | Closed - WP1 complete, session-wide WP2 Pass, WP3 Establish (RBL-0027) |

---

# 2. Purpose

This report records the opening and execution of ESR-0044, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0043_ENGINEERING_SESSION_REPORT|ESR-0043]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]]. Created at WP0B, before WP1 began.

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0043_ENGINEERING_SESSION_REPORT|ESR-0043]] closed (30 July 2026), [[RBL-0026_REPOSITORY_BASELINE|RBL-0026]] the current accepted baseline, working tree clean, pre-commit governance hook active (`core.hooksPath` = `scripts/hooks`), PBK-0001 confirmed unchanged since last read (still last touched at ESR-0036).

`scripts/session_launcher.py` was run to surface candidate objectives. Presented to the Programme Sponsor: EBG-0114 (Voice faculty not wired into `build_default_runtime()`, Medium, registered at ESR-0042 closure), EBG-0115 (Evaluate Kokoro TTS, Low, registered following ESR-0043), EBG-0065 (STD-0006, High, Approved), EBG-0038/0046/0042 (architecture-only candidates), and the remaining Section 5A theme candidates. **The Programme Sponsor selected EBG-0114 (Wire Voice into the live UXP)** - real product-moving work, directly progressing the live UXP per PBK-0001's Feature-First Delivery Discipline.

EBG-0114's own registration text withholds implementation authority: no implementation is authorised by the registration itself. This session's objective is therefore to scope and implement the wiring, producing an Engineering Implementation Package for Codex design review and Programme Sponsor approval before any code changes.

---

# 4. Engineering Authority

ESR-0044 opening was authorised by direct Programme Sponsor instruction on 30 July 2026, following review of PBK-0001, README.md, PST-0001 and ESR-0043, confirming [[RBL-0026_REPOSITORY_BASELINE|RBL-0026]] as the accepted repository baseline at session open, and a direct choice between the session_launcher.py-surfaced candidates via an explicit objective-selection question.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Wire [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0114: connect Guardian's existing Voice faculty (`GuardianRuntime.speak()`, `PiperProvider`, EBG-0112) into `jarvis/interfaces/stdio_rpc.py`'s `build_default_runtime()` and expose a "speak this response" affordance through the live Tauri UXP, so Guardian's speech output is reachable through the actual running product rather than only standalone validation scripts. Produce an Engineering Implementation Package for Codex design review and Programme Sponsor approval before implementation.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | EBG-0114: wire Voice faculty into the live runtime/UXP; Codex design review; Programme Sponsor approval | Complete |
| WP2 | Session-wide Independent Repository Verification | Complete - Pass, no blocking findings |
| WP3 | Session-wide Repository Baseline Determination | Complete - Establish (RBL-0027) |

---

# 6A. WP1 - EBG-0114: Wire Voice into the Live Runtime and UXP

Reviewed `jarvis/interfaces/stdio_rpc.py`'s `build_default_runtime()`/`_build_real_provider()`, `jarvis/guardian/runtime.py`'s `GuardianRuntime` (already accepts an optional `speech_provider`), `jarvis/interfaces/voice.py`'s `SpeechOutcome`/`SentinelGatedSpeechProvider`, `sentinel/piper_provider.py`, and `src-tauri/src/lib.rs`'s `send_message`/`call_backend` pattern before drafting scope. Confirmed the toolchain could genuinely build and test this change: `cargo check` succeeded cleanly, Playwright and the existing `tests/e2e/app.spec.js` IPC-mocking pattern were confirmed available.

Produced [[EIP-ESR0044-001_WIRE_VOICE_INTO_LIVE_RUNTIME_AND_UXP|EIP-ESR0044-001]] (v0.1, Draft): a 3-layer wiring package - backend (`JARVIS_PIPER_VOICE_PATH`-gated speech provider construction, new `guardian.speak` RPC method), Tauri (`speak_message` command mirroring `send_message`), and frontend (a minimal per-message speak button with audio playback and non-blocking error notes) - with no change to any of the already-approved Voice faculty components themselves.

Submitted to Codex for design review via direct `codex exec -s read-only` invocation, per the established EBG-0096 pattern - **Pass, with non-blocking findings**. Codex confirmed the credential-gated `JARVIS_PIPER_VOICE_PATH` pattern was correct, reusing the single `SentinelTrustGateway` instance was correct, the `guardian.speak` RPC shape was sound, and the frontend scope was appropriately minimal. Three non-blocking findings folded into v0.2: the frontend must also catch its own failures (rejected `invoke`, malformed data URI, rejected `Audio.play()`); a configured-but-invalid path causing backend startup failure was explicitly disclosed as deliberate and unchanged; tests should assert observable behaviour, not internals too tightly.

Programme Sponsor approval obtained and verified via `submit-response` directly against the real Sponsor Approval Service before implementation began.

**Implemented exactly as scoped, across all three layers.** Backend: `PIPER_VOICE_PATH_ENV_VAR`, `_build_speech_provider()` (reusing the existing `gateway`), `speech_provider` wired into `GuardianRuntime(...)`, and `guardian.speak` RPC method. 6 new tests in `jarvis/tests/test_stdio_rpc.py` using a `_FakePiperProvider` patched over the real class - never loading a real model or importing `piper`. Tauri: `speak_message` command, byte-for-byte matching `send_message`'s shape, registered in `generate_handler!`; `cargo build`/`cargo clippy -- -D warnings`/`cargo fmt --check`/`cargo test` all pass cleanly (one formatting fix applied via `cargo fmt`). Frontend: a per-message speak button in `src/App.jsx`, decoding base64 audio into a data URI and playing it via `Audio`, with non-blocking inline error notes for both backend and frontend failure modes; `src/styles.css` was also touched - a minor, disclosed dependency (button styling) discovered during implementation, not in the original authorised file list. `npm run build` succeeds; 2 new Playwright specs added to `tests/e2e/app.spec.js`, full e2e suite (7 tests) passes.

**Live smoke check performed, not merely mocked.** A real Piper voice model was downloaded via `piper-tts`'s own `download_voices` CLI to an uncommitted local path (removed afterward); a genuine `guardian.speak` call through the real `build_default_runtime()` + RPC wiring produced a real 161,836-byte `audio/wav` payload; the unconfigured case correctly returned `not_connected`. Real audio-hardware playback through the live Tauri app was not performed in this implementation environment - disclosed honestly per PBK-0001's Operational Verification Before Reporting, and remains available for the Programme Sponsor to confirm.

[[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] updated to record Voice as reachable through the live product. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]: EBG-0114 marked Completed.

- Files: `jarvis/interfaces/stdio_rpc.py`, `jarvis/tests/test_stdio_rpc.py`, `src-tauri/src/lib.rs`, `src/App.jsx`, `src/styles.css` (discovered dependency), `tests/e2e/app.spec.js`, `aiems/models/AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE.md`, `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, [[EIP-ESR0044-001_WIRE_VOICE_INTO_LIVE_RUNTIME_AND_UXP|EIP-ESR0044-001]] (new).
- `python -m pytest`: 424 passed, 1 skipped (was 418/1, 6 new).
- `cargo build`/`cargo clippy -- -D warnings`/`cargo fmt --check`/`cargo test`: all clean.
- `npx playwright test`: 7 passed (2 new).
- `python scripts/validate_repository.py` (full mode): 0 errors (warning count reported at session close).
- Committed as `899e67f`, pushed to `origin/main`.

---

# 6B. Session-Wide WP2 - Independent Repository Verification

**Pass, no blocking findings.** Codex independently reviewed the real pushed commit `899e67f` via a fresh `codex exec -s read-only` pass: confirmed via `git show --stat` and `git diff --name-only` that the diff touches exactly the 11 claimed files and none outside that scope; confirmed via `git diff` against `jarvis/guardian/runtime.py`, `jarvis/interfaces/voice.py`, `sentinel/piper_provider.py` and `sentinel/speech_providers.py` (all empty output) that every already-approved Voice component is genuinely untouched; confirmed the `guardian.speak` RPC and `speak_message` Tauri command match the claimed shapes, reusing the existing gateway and gating audio inclusion on `status == "synthesized"`; confirmed the new unit tests patch a fake `PiperProvider`, never constructing or loading a real model.

**One non-blocking observation**: `_build_speech_provider`'s `if not voice_path` check treats a whitespace-only string as "configured" rather than absent - consistent with the existing codebase convention (`_build_real_provider`'s identical credential check has the same property), not a new gap this package introduces. Disclosed, not fixed, to stay consistent with established convention rather than gold-plating one new function differently from the rest of the file.

Codex's own sandbox hit the same disclosed `CreateProcessAsUserW failed: 1920` spawn error recorded in EBG-0096's history when attempting `validate_repository.py`/`pytest` directly - a pre-existing environment limitation, not a finding against this change. The Engineering Implementer independently re-ran both against the real pushed HEAD (`899e67f`) to complete the evidence: `python scripts/validate_repository.py` (full mode) - 0 errors, 258 warnings, matching this session's own WP1 evidence exactly; `python -m pytest -q` - 424 passed, 1 skipped, unchanged.

- `python scripts/validate_repository.py` (full mode): 0 errors, 258 warnings - unchanged from WP1's close.

---

# 6C. Session-Wide WP3 - Repository Baseline Determination (RBL-0027 Established)

This session delivered a genuine, live product-capability change: Guardian's Voice faculty is now reachable through the actual running Tauri UXP for the first time (backend RPC wiring, a new Tauri command, and a working UI speak button), live-verified with a real 161,836-byte `audio/wav` payload through the exact new wiring. The Programme Sponsor's determination: **establish** - [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] is accepted as the new current repository baseline, superseding [[RBL-0026_REPOSITORY_BASELINE|RBL-0026]].

- `python -m pytest`: 424 passed, 1 skipped throughout. `python scripts/validate_repository.py` (full mode): 0 errors throughout; warning count held at 258 across this WP.

---

# 7. Related Artefacts

* [[ESR-0043_ENGINEERING_SESSION_REPORT|ESR-0043]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation, Engineering Session Lifecycle and Feature-First Delivery Discipline guidance followed.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0114 (this session's objective).
* [[ESR-0040_ENGINEERING_SESSION_REPORT|ESR-0040]] / [[ESR-0042_ENGINEERING_SESSION_REPORT|ESR-0042]] - delivered and evaluated the Voice faculty this session wires into the live product.
* [[RBL-0026_REPOSITORY_BASELINE|RBL-0026]] - repository baseline at session open.
* [[EIP-ESR0044-001_WIRE_VOICE_INTO_LIVE_RUNTIME_AND_UXP|EIP-ESR0044-001]] - this session's WP1 deliverable, Codex design-reviewed (Pass, with non-blocking findings) and Programme Sponsor-approved via the real Sponsor Approval Service.
* [[RBL-0027_REPOSITORY_BASELINE|RBL-0027]] - repository baseline established at this session's WP3.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.2 | 30 July 2026 | Claude Engineering Implementer | ESR-0044 formally closed. Session-wide WP2 (Independent Repository Verification: Pass, no blocking findings - Codex verified commit scope/content directly; validate_repository.py and pytest independently re-run by the Engineering Implementer after Codex's own sandbox hit the disclosed EBG-0096 spawn-error limitation) and WP3 (Repository Baseline Determination: Establish, RBL-0027, per explicit Programme Sponsor decision - a genuine, live-verified product capability change) complete. |
| 1.1 | 30 July 2026 | Claude Engineering Implementer | WP1 Complete: EBG-0114 (Voice faculty wiring) implemented via EIP-ESR0044-001 (Codex design review Pass, non-blocking findings folded into v0.2) - a 3-layer change (Python backend, Rust Tauri bridge, React frontend) with no change to any already-approved Voice component itself. Live-verified end to end with a real 161,836-byte `audio/wav` payload. 424 tests pass, 1 skipped (6 new); Rust build/clippy/fmt/test clean; e2e suite (7, 2 new) passes. `src/styles.css` touched as a disclosed discovered dependency. |
| 1.0 | 30 July 2026 | Claude Engineering Implementer | ESR-0044 opened at WP0B, before WP1 began. Objective: wire Guardian's Voice faculty into the live runtime/UXP (EBG-0114), producing an Engineering Implementation Package for Codex review and Programme Sponsor approval before implementation. |
