# ESR-0053 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0053 |
| Title | Engineering Session Report |
| Version | 1.9 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0053 |
| Date Opened | 27 August 2026 |
| Date Closed | 27 August 2026 |
| Closure Status | Closed - WP1/WP2 complete, session-wide WP6 (Pass, no findings) and WP7 (Establish RBL-0033) complete |

---

# 2. Purpose

This report records the opening of ESR-0053, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened at the Programme Sponsor's direct request. WP0A/WP0B session initialisation followed [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (re-read in full at the Programme Sponsor's explicit request opening this session) and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]].

---

# 3. Scope

**WP0A - Repository Synchronisation (Complete):** README.md, [[PST-0001_PROGRAMME_STATUS|PST-0001]] (v3.35), [[ESR-0052_ENGINEERING_SESSION_REPORT|ESR-0052]] (latest closed session), [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] tiers and [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] (v1.21) reviewed. Repository baseline confirmed as [[RBL-0032_REPOSITORY_BASELINE|RBL-0032]] (accepted ESR-0051 WP7, retained ESR-0052 WP7). Pre-commit governance hook confirmed active (`core.hooksPath` = `scripts/hooks`). `~/.current_session` updated to `ESR-0053`.

**WP0B - Engineering Session Initialisation (Complete):** ESR-0052 confirmed formally Closed; ESR-0053 opened as the next session identifier.

**Documentation-Debt Priority check (PBK-0001):** [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] reviewed against the standing rule that documentation-debt backlog items take priority ahead of new capability work until cleared. Found: EBR-0001 Section 5A (the "Active Backlog View" manual snapshot) is currently stale - it still lists EBG-0115 (Kokoro TTS) and EBG-0111 (Composio) as open Theme 8 items, though both were resolved at ESR-0052 WP2/WP3. This is a live, second instance of the exact drift EBG-0106 (Approved Backlog, Medium, open) was registered to fix. Flagged to the Programme Sponsor, who selected clearing EBG-0106 as WP1, ahead of new capability work.

**WP1 - EBG-0106: Active Backlog View Generation (Implemented):** replaces Section 5A's hand-maintained theme-grouped snapshot with a view mechanically generated from Section 5's own Status/Priority columns via `scripts/session_launcher.py`, removing the second source of truth that has now drifted twice. Drafted in [[EIP-ESR0053-001_ACTIVE_BACKLOG_VIEW_GENERATION|EIP-ESR0053-001]] v0.1, submitted to Codex Engineering Reviewer via the AIEMS Exchange Bridge (`ESR-0053`/`WP1`) - **Conditional Pass with corrections**, both folded into v0.2: (1) the refactor's backward-compatibility claim narrowed to only the `read_high_priority_backlog`/`read_open_backlog` half, since `read_active_backlog_snapshot()`/`ActiveBacklogItem` are intentionally, breakingly retired; (2) validation wording corrected to distinguish unchanged test behaviour from necessarily-changed test wiring. **Programme Sponsor approved via direct chat instruction ("Approved")**, and **implemented exactly as scoped in v0.2** (v1.0):

* `scripts/session_launcher.py`: `read_high_priority_backlog()` refactored into `read_open_backlog(ebr_path, priority=None)` with a backward-compatible wrapper; new `generate_active_backlog_view()` groups open items by Priority (High/Medium/Low, unrecognised values under "Other"); `read_active_backlog_snapshot()`/`ActiveBacklogItem`/the three Section-5A-specific regex constants removed; `build_report()` rebuilt around the new grouping; module docstring updated.
* `scripts/tests/test_session_launcher.py`: four Section-5A-era tests removed, seven new tests added (net +2) covering `read_open_backlog`'s full-priority/filtered behaviour, the `read_high_priority_backlog` wrapper's exact equivalence, and `generate_active_backlog_view`'s ordering/empty-group/unrecognised-priority handling.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]: Section 5A's theme-grouped snapshot replaced with a short pointer paragraph to `scripts/session_launcher.py`; EBG-0106's own Section 5 row closed `Completed`.

Validation: `python -m pytest scripts/tests/test_session_launcher.py` - 16 passed (was 14; a net +2 test-wiring gain, disclosed as a deviation from the pre-implementation "unchanged" prediction). Full suite `python -m pytest jarvis/tests sentinel scripts/tests` - **532 passed, 1 skipped** (up from ESR-0052's closing 530/1, matching). `python scripts/validate_repository.py` (full mode) - 0 errors, 298 warnings (unchanged, none newly introduced). Live `python scripts/session_launcher.py` run against the real repository confirmed the new Active Backlog View correctly Priority-groups the real open Section 5 rows.

**Committed and pushed** (`274a6b9`, `b46c296..274a6b9`), gated through the real Sponsor Approval Service via `submit-response` (`AIEMS_AGENT_TOKEN`/`AIEMS_SPONSOR_URL` supplied directly by the Programme Sponsor for this call).

**Post-commit independent review** (direct `codex exec -s workspace-write` invocation against the real pushed commit `274a6b9`, diff `b46c296..274a6b9`): **Pass, no findings.** Codex independently re-ran `git show --stat`/`git diff` and confirmed exactly the six expected files changed, no unexpected `jarvis/`/`sentinel/`/`src/` path touched; independently re-ran `pytest` (532 passed, 1 skipped, matching) and `validate_repository.py` (0 errors, 298 warnings, matching); spot-checked EBG-0106 marked `Completed` and Section 5A no longer holding a static per-theme table; confirmed REG-0001's version-history/row entries internally consistent with the actual diff.

---

**WP2 - EBG-0125: Kokoro Production Voice Wiring (Complete):** following the Programme Sponsor's selection of a product-moving WP2, per PBK-0001's Feature-First Delivery Discipline (WP1 alone was process/tooling-only). A live UK-voice comparison was performed first: the real `KokoroProvider` synthesized the same fixed test utterance used at EBG-0113/EBG-0115 through each of Kokoro's four confirmed British voices (`bf_emma`, `bf_isabella`, `bm_george`, `bm_lewis`), writing four genuine `.wav` files to the Programme Sponsor's Desktop; the comparison script and downloaded model files were never committed, deleted immediately after use (confirmed via `git status`). **Programme Sponsor's verdict**: `bm_george` (primary), `bf_isabella` (automatic fallback if primary synthesis fails at runtime); **Kokoro replaces Piper outright** as Guardian's sole production speech-synthesis provider - not a second selectable option. Drafted in [[EIP-ESR0053-002_KOKORO_PRODUCTION_VOICE_WIRING|EIP-ESR0053-002]], submitted to Codex Engineering Reviewer via the AIEMS Exchange Bridge (`ESR-0053`/`WP2`) - **Conditional Pass with correction**, folded into v0.2: EBG-0125's own `EBR-0001` row still read "no implementation, provider selection or voice choice is authorised," stale relative to the Programme Sponsor's actual decision recorded above - corrected with a dated authorisation note. Scoping: a dual-voice fallback extension to `sentinel/kokoro_provider.py` (a disclosed breaking change to its internal `VoiceSynthesizer` seam, from a single fixed voice to a `(text, voice)`-parameterised one, so a single loaded engine can serve both voices); `jarvis/interfaces/stdio_rpc.py`'s `_build_speech_provider()` rewritten to construct `KokoroProvider` instead of `PiperProvider`, gated on two new required env vars (`JARVIS_KOKORO_MODEL_PATH`/`JARVIS_KOKORO_VOICES_PATH`); `pyproject.toml`'s `voice-eval` optional dependency group promoted to base `dependencies`; corresponding test updates. `sentinel/piper_provider.py` itself is explicitly left untouched - unregistered from production, not deleted. No `src/`/`src-tauri/` change - `guardian.speak`'s UXP call site confirmed already provider-agnostic (Codex independently verified this too). **Programme Sponsor approved via direct chat instruction ("Approved")**, and **implemented exactly as scoped in v0.2** (v1.0):

* `sentinel/kokoro_provider.py`: `VoiceSynthesizer` changed from a single fixed voice bound at construction (`Callable[[str], bytes]`) to a voice-parameterised callable (`Callable[[str, str], bytes]`) - one loaded Kokoro engine now serves both voices without a second ~90 MB model load. New optional `fallback_voice` metadata key; `synthesize()` retries once with the fallback on a primary-voice failure, raising only if both fail; response metadata gains `voice_used` for audit traceability.
* `jarvis/interfaces/stdio_rpc.py`: `PiperProvider` import/wiring removed from `_build_speech_provider()`; `KokoroProvider` constructed instead, gated on two new required env vars (`JARVIS_KOKORO_MODEL_PATH`/`JARVIS_KOKORO_VOICES_PATH`), with `bm_george`/`bf_isabella`/`en-gb` as hardcoded module constants.
* `pyproject.toml`: `kokoro-onnx`/`espeakng-loader`/`phonemizer-fork` moved from the `voice-eval` optional group (now removed) into base `dependencies`. `piper-tts` untouched.
* `jarvis/tests/test_kokoro_provider.py`/`test_stdio_rpc.py`: seam/wiring tests updated; 5 new tests added covering fallback behaviour and both-paths-required gating.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]: EBG-0125 closed `Completed`.

Validation: `pytest jarvis/tests/test_stdio_rpc.py jarvis/tests/test_kokoro_provider.py` - 79 passed. Full suite - **537 passed, 1 skipped** (up from 532/1, +5). `validate_repository.py` - 0 errors, 298 warnings (unchanged). **Live end-to-end verification against the real engine, not fake seams**: a genuine `build_default_runtime()` + `runtime.speak()` call (real downloaded model files) returned synthesized `bm_george` audio (229,420 bytes); a second real call with a deliberately invalid primary voice confirmed the automatic fallback genuinely engages, producing real `bf_isabella` audio (65,580 bytes). Model files never committed, deleted after verification.

**Committed and pushed** (`061c914`, `248924a..061c914`), gated through the real Sponsor Approval Service via `submit-response`.

**Post-commit independent review** (direct `codex exec -s workspace-write` invocation against the real pushed commit `061c914`, diff `248924a..061c914`): **Pass, no findings.** Codex independently re-ran `git show --stat`/`git diff` and confirmed exactly the nine expected files changed, no unexpected `src/`/`src-tauri/` path touched; independently re-ran `pytest` (537 passed, 1 skipped, matching) and `validate_repository.py` (0 errors, 298 warnings, matching); read `sentinel/kokoro_provider.py` directly and confirmed the fallback logic genuinely matches the claim (primary tried first, fallback only on exception, raises if both fail, exception chaining preserved); read `jarvis/interfaces/stdio_rpc.py` directly and confirmed `PiperProvider` is genuinely no longer imported/wired and both Kokoro env vars are required; confirmed `sentinel/piper_provider.py` untouched by the diff; spot-checked EBG-0125 marked `Completed`; confirmed REG-0001 internally consistent.

---

# 4. Engineering Authority

ESR-0053 opening was authorised by direct Programme Sponsor instruction on 27 August 2026, following ESR-0052's formal closure.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

WP1 (complete): resolve EBG-0106 by replacing EBR-0001 Section 5A's manually-maintained snapshot with a mechanically-generated Priority-grouped view, per PBK-0001's Documentation-Debt Priority discipline.

WP2 (complete): resolve EBG-0125 by wiring Kokoro into Guardian's production speech-output path, replacing Piper, per the Programme Sponsor's decision following a live UK-voice listening comparison.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP0A | Repository Synchronisation | Complete |
| WP0B | Engineering Session Initialisation | Complete |
| WP1 | EBG-0106: Active Backlog View Generation | Complete (EIP-ESR0053-001 v1.0) - committed `274a6b9`, pushed, post-commit reviewed (Pass) |
| WP2 | EBG-0125: Kokoro Production Voice Wiring | Complete (EIP-ESR0053-002 v1.0) - committed `061c914`, pushed, post-commit reviewed (Pass) |
| WP6 | Session-wide Independent Repository Verification | Complete - Pass, no findings |
| WP7 | Session-wide Repository Baseline Determination | Pending Programme Sponsor determination |

---

# 6A. Session-Wide WP6 - Independent Repository Verification

Following WP2's implementation, push and post-commit review, the Programme Sponsor selected moving to session-wide Independent Repository Verification.

Ran a genuine independent Codex review (`codex exec -s workspace-write`, background invocation) against the full session diff, `b46c296..HEAD` (`b46c296`, ESR-0052's own final closure commit - independently confirmed by Codex itself via `git log --oneline b46c296..HEAD` before reviewing, rather than trusted blindly, learning directly from ESR-0052 WP6's own diff-boundary mistake). Confirmed exactly ESR-0053's four commits (`274a6b9`, `248924a`, `061c914`, `1db5547`) and 12 changed files across both Work Packages, no scope creep, no unexpected `src/`/`src-tauri/`/`jarvis/`/`sentinel/` path beyond WP2's legitimate Kokoro wiring. Independently re-ran `pytest jarvis/tests sentinel scripts/tests` (537 passed, 1 skipped, matching) and `validate_repository.py` (0 errors, 298 warnings, matching); confirmed EBG-0106 and EBG-0125 both genuinely `Completed` in EBR-0001; confirmed Section 5A no longer holds a stale static snapshot; confirmed the Piper-to-Kokoro production substitution and fallback logic directly against source; confirmed `sentinel/piper_provider.py`, `sentinel/policy.py` and `GAM-0001` untouched across the whole session; confirmed REG-0001/EBR-0001/ESR-0053 version-history entries internally consistent with the actual diff.

**Verdict: Pass, no findings.**

Codex's own advisory baseline assessment: **Establish** a new RBL, superseding [[RBL-0032_REPOSITORY_BASELINE|RBL-0032]] - WP2 is a genuine live product-capability change (Guardian's actual production speech-synthesis provider changed from Piper to Kokoro, with new runtime dependency/wiring and primary/fallback UK voice behaviour); retaining RBL-0032 would understate the accepted repository state. The Programme Sponsor makes the actual WP7 determination.

---

# 6B. Session-Wide WP7 - Repository Baseline Determination

**Programme Sponsor determination: Establish [[RBL-0033_REPOSITORY_BASELINE|RBL-0033]]** (superseding [[RBL-0032_REPOSITORY_BASELINE|RBL-0032]]), matching Codex's own advisory assessment. WP2's real, live-verified Kokoro production-voice delivery changes Guardian's actual live product behaviour: the production speech-synthesis provider is now Kokoro (`bm_george` primary, `bf_isabella` automatic fallback), not Piper - live-verified against the real engine, not merely unit-tested. This matches the Establish threshold applied at ESR-0049/ESR-0050/ESR-0051 rather than the Retain threshold applied at ESR-0041/ESR-0042/ESR-0045/ESR-0048/ESR-0052.

Files: `README.md`, `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`, `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md`, `aiems/governance/conversation/COC-0001_HUMAN_AI_COLLABORATION_CONTEXT.md`, `aiems/governance/baselines/PCB-0001_PRODUCT_CAPABILITY_BASELINE.md`, `jarvis/architecture/JARVIS_CAPABILITY_READINESS_MATRIX.md`, `aiems/governance/baselines/RBL-0033_REPOSITORY_BASELINE.md` (new), `aiems/governance/sessions/ESR-0053_ENGINEERING_SESSION_REPORT.md` (this report, closure), `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`.

---

# 7. Related Artefacts

* [[ESR-0052_ENGINEERING_SESSION_REPORT|ESR-0052]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation, Engineering Session Lifecycle and Documentation-Debt Priority guidance followed; re-read in full at the Programme Sponsor's explicit request opening this session.
* [[RBL-0032_REPOSITORY_BASELINE|RBL-0032]] - current accepted repository baseline.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0106 (WP1 scope), Section 5A (currently stale, the finding that selected WP1).
* [[EIP-ESR0053-001_ACTIVE_BACKLOG_VIEW_GENERATION|EIP-ESR0053-001]] - Engineering Implementation Package for WP1, approved and implemented.
* `scripts/session_launcher.py` / `scripts/tests/test_session_launcher.py` - modified by WP1.
* [[EIP-ESR0053-002_KOKORO_PRODUCTION_VOICE_WIRING|EIP-ESR0053-002]] - Engineering Implementation Package for WP2, drafted.
* [[EIP-ESR0052-002_KOKORO_TTS_LIVE_COMPARISON|EIP-ESR0052-002]] - built and tested the `KokoroProvider` adapter WP2 wires into production.
* [[RBL-0033_REPOSITORY_BASELINE|RBL-0033]] - repository baseline established at this session's WP7.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.9 | 27 August 2026 | Claude Engineering Implementer | **ESR-0053 formally closed.** Session-wide WP7 (Repository Baseline Determination): **Programme Sponsor determination: Establish RBL-0033**, matching Codex's own advisory - WP2's real, live-verified Kokoro production-voice delivery changes Guardian's actual live product behaviour. RBL-0033 created; README.md, PST-0001, PBK-0001, COC-0001, PCB-0001 and JARVIS_CAPABILITY_READINESS_MATRIX all updated to reference it as the current accepted baseline. |
| 1.8 | 27 August 2026 | Claude Engineering Implementer | ESR-0053 session-wide WP6 (Independent Repository Verification): genuine background Codex review of the full session diff (`b46c296..HEAD`) - **Pass, no findings**. Diff boundary independently self-confirmed by Codex before reviewing (learning directly from ESR-0052 WP6's own diff-boundary mistake). Codex's own advisory: **Establish** a new RBL, superseding RBL-0032 - WP2 is a genuine live product-capability change. WP7 determination pending Programme Sponsor decision. Whole-document staleness sweep: two stale "not yet approved/drafted" headers (WP2's own heading, Section 5's objective) corrected to reflect completion, found while editing for this WP6 recording. |
| 1.7 | 27 August 2026 | Claude Engineering Implementer | ESR-0053 WP2 post-commit review: genuine `codex exec -s workspace-write` review of the real pushed commit `061c914` (diff `248924a..061c914`) - **Pass, no findings**. All inspectable scope/registration/pytest/validation checks independently re-run and matched, including a direct read of the fallback logic and the Piper-to-Kokoro wiring substitution. |
| 1.6 | 27 August 2026 | Claude Engineering Implementer | ESR-0053 WP2 Complete: EIP-ESR0053-002 (0.2 to 1.0, Approved - implemented) - EBG-0125 resolved, Kokoro wired into production replacing Piper. Programme Sponsor approved via direct chat instruction ("Approved"). `pytest` 537 passed/1 skipped (up from 532/1), `validate_repository.py` 0 errors/298 warnings. Live-verified against the real Kokoro engine (both primary voice and genuine fallback trigger), not merely unit-tested. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 1.5 | 27 August 2026 | Claude Engineering Implementer | ESR-0053 WP2: EIP-ESR0053-002 Codex design-reviewed via the AIEMS Exchange Bridge - Conditional Pass with correction (0.1 to 0.2), folded in: EBG-0125's stale authorisation wording corrected with a dated Sponsor-decision note. Not yet approved by the Programme Sponsor or implemented. |
| 1.4 | 27 August 2026 | Claude Engineering Implementer | ESR-0053 WP2: live UK-voice comparison performed (four real `.wav` samples, never committed); Programme Sponsor selected `bm_george` primary/`bf_isabella` automatic fallback, Kokoro replacing Piper outright. Drafted [[EIP-ESR0053-002_KOKORO_PRODUCTION_VOICE_WIRING|EIP-ESR0053-002]] v0.1. Not yet reviewed, approved or implemented. |
| 1.3 | 27 August 2026 | Claude Engineering Implementer | ESR-0053 WP1 post-commit review: genuine `codex exec -s workspace-write` review of the real pushed commit `274a6b9` (diff `b46c296..274a6b9`) - **Pass, no findings**. All inspectable scope/registration/pytest/validation checks independently re-run and matched. |
| 1.2 | 27 August 2026 | Claude Engineering Implementer | ESR-0053 WP1 Complete: EIP-ESR0053-001 (0.2 to 1.0, Approved - implemented) - EBG-0106 resolved. Programme Sponsor approved via direct chat instruction ("Approved"). `pytest` 532 passed/1 skipped (up from 530/1), `validate_repository.py` 0 errors/298 warnings. Committed and pushed (`274a6b9`) through `submit-response` and the real Sponsor Approval Service. |
| 1.1 | 27 August 2026 | Claude Engineering Implementer | ESR-0053 WP1: EIP-ESR0053-001 Codex design-reviewed via the AIEMS Exchange Bridge - Conditional Pass with corrections (0.1 to 0.2), both folded in. Not yet approved by the Programme Sponsor or implemented. |
| 1.0 | 27 August 2026 | Claude Engineering Implementer | ESR-0053 opened at WP0B. WP0A/WP0B complete. Documentation-Debt Priority check found EBR-0001 Section 5A stale (a live second instance of the drift EBG-0106 exists to fix) - flagged to the Programme Sponsor, who selected clearing EBG-0106 as WP1. WP1 drafted per [[EIP-ESR0053-001_ACTIVE_BACKLOG_VIEW_GENERATION|EIP-ESR0053-001]] v0.1 - not yet reviewed, approved or implemented. |
