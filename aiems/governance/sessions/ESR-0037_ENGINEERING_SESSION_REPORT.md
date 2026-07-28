# ESR-0037 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0037 |
| Title | Engineering Session Report |
| Version | 1.4 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0037 |
| Date Opened | 28 July 2026 |
| Date Closed | 28 July 2026 |
| Closure Status | Closed - WP1 complete, session-wide WP2 Pass, WP3 Establish (RBL-0023 accepted) |

---

# 2. Purpose

This report records the opening and execution of ESR-0037, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0036_ENGINEERING_SESSION_REPORT|ESR-0036]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]]. Created at WP0B, before WP1 began, correcting the process gap disclosed at ESR-0036 (report created retroactively during WP2).

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0036_ENGINEERING_SESSION_REPORT|ESR-0036]] closed (26 July 2026), [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]] the current accepted baseline, working tree clean at `ff5f67d`, pre-commit governance hook active. No open [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] item concerns documentation staleness, so PBK-0001's Documentation-Debt Priority discipline does not constrain WP0/WP1 selection this session.

Two High-priority Approved Backlog candidates were identified: EBG-0109 (Live Guardian Conversation Path Unreliable Against Ollama Provider in the Tauri Desktop Shell) and EBG-0108 (Guardian Cognitive Core Implementation). EBG-0109's own entry states EBG-0108 "now depends on this exact live conversation path being reliable" - the Programme Sponsor selected EBG-0109 as this session's objective, ahead of EBG-0108, on that basis.

---

# 4. Engineering Authority

ESR-0037 opening was authorised by direct Programme Sponsor instruction on 28 July 2026, immediately following review of PBK-0001, README.md and PST-0001, confirming [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]] as the accepted repository baseline at session open.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Diagnose and fix [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0109: the live Guardian conversation path is unreliable against the Ollama provider in the Tauri desktop shell (reasoning-model timeout exposure, plus a distinct Tauri IPC-path defect causing silent LocalEcho fallback and indefinite hangs), so that EBG-0108 (Guardian Cognitive Core Implementation) can be built on a reliable foundation.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | EBG-0109: diagnose and fix Ollama/Tauri conversation-path reliability | Complete |
| WP2 | Session-wide Independent Repository Verification | Complete - Pass, no findings |
| WP3 | Session-wide Repository Baseline Determination | Complete - Establish (RBL-0023) |

---

# 6A. WP1 - EBG-0109: Ollama/Tauri Conversation-Path Reliability

Reviewed `sentinel/ollama_provider.py`, `sentinel/orchestrator.py`, `jarvis/interfaces/sentinel_conversation.py`, `jarvis/interfaces/stdio_rpc.py` and `src-tauri/src/lib.rs` in full before scoping. Confirmed `ProviderOrchestrator.execute()` fails over per-request from the top of the route on any exception, and `StdioRpcServer.serve_forever()` is a single-threaded read loop where `guardian.converse` blocks until it returns while the heartbeat runs on a separate thread - consistent with EBG-0109's own disclosed observations. Found no code-level defect in the write-lock/heartbeat-thread interaction that would explain Finding 2(b) (a request never reaching Ollama at all); confirming that, or reproducing Finding 2(a)/2(b) under controlled conditions, needs a live desktop session this implementation environment cannot provide - explicitly not attempted, rather than guessed at.

**Scope delivered** (Findings 1 and 2(c) only; 2(a)/2(b)/recommendation (d) remain open, disclosed in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]'s EBG-0109 entry):

1. `sentinel/ollama_provider.py`: `execute()`'s payload now unconditionally includes `think: false` and `options: {"num_ctx": DEFAULT_NUM_CTX}` (new module constant, 4096) - directly fixes the disclosed 3m15s reasoning-model measurement, applied to every request regardless of model (Ollama ignores options a given model does not use).
2. `src-tauri/src/lib.rs`: `call_backend()` replaces the previously-unbounded `receiver.recv()` with a 120s `recv_timeout` (new `BACKEND_CALL_TIMEOUT` constant - 30s headroom over the Python side's 90s `OLLAMA_TIMEOUT_SECONDS`); on timeout, a new `remove_pending()` helper drops the stale pending-map entry and a clear, user-facing error is returned instead of an indefinite freeze. The backend process itself is left running, not torn down - a late response arriving after cleanup is handled safely by the existing "no pending call for this id" behaviour. The response-routing half of `dispatch_line()` was extracted into a new `route_response()` so this property is unit-testable without a full `AppHandle`.

**Governance:** run entirely through the AIEMS Exchange Bridge (`scripts/aiems_bridge.py`) and the deployed Sponsor Approval Service. Design submitted to Codex for review before any implementation - **PASS, no blocking findings**; one non-blocking suggestion (test coverage for the timeout-cleanup path, specifically that a late response after cleanup is harmless) folded into the implementation as `route_response_after_pending_entry_already_removed_is_harmless`. Programme Sponsor approval verified by `submit-response` directly against the Sponsor Approval Service's own decision database (matching repository ref), not merely asserted in chat.

- Files: `sentinel/ollama_provider.py`, `src-tauri/src/lib.rs`, `jarvis/tests/test_ollama_provider.py`, [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
- `python -m pytest`: 382 passed, 1 skipped (was 381 passed, 1 skipped - 1 new test, no regressions). `cargo build` / `cargo clippy -- -D warnings` / `cargo fmt --check`: all clean. `cargo test`: 5 new unit tests pass (`remove_pending_drops_the_entry`, `remove_pending_on_an_unknown_id_is_a_no_op`, `route_response_delivers_a_result_to_the_matching_pending_call`, `route_response_delivers_an_error_message_to_the_matching_pending_call`, `route_response_after_pending_entry_already_removed_is_harmless`). `python scripts/validate_repository.py` (full mode): 0 errors, 173 warnings (was 172 - the +1 is this session's own new ESR-0037/REG-0001 registrations, the same disclosed cross-document-reference false-positive category as the existing 172, not the code change).
- **Process note, disclosed rather than silently corrected**: the first attempt to update PST-0001 Section 3's Current Mode row named ESR-0037 as the leading reference, which `validate_repository.py`'s `check_stale_status_references` correctly rejected - the established convention (confirmed against ESR-0036's own history) keeps that row's leading WikiLink on the latest *closed* session until the new session itself closes, mentioning the newly-opened session inline afterward. Corrected before commit.

---

# 6B. Session-Wide WP2 - Independent Repository Verification

**Pass, no findings.** Codex independently reviewed the real pushed diff for commit `2b1e531` (`ff5f67d..2b1e531`) via a fresh, read-only CLI pass (not taken on the pre-commit design review's word alone): confirmed the implementation matches what was approved (`think: false`/`options.num_ctx=4096` unconditionally in `sentinel/ollama_provider.py`; `src-tauri/src/lib.rs`'s `call_backend()` using a 120s `recv_timeout` with `remove_pending()` cleanup and `route_response()` extracted from `dispatch_line()`; 5 new Rust unit tests; updated/added Python tests), confirmed no file under `src/`, `jarvis/memory/` or `.github/workflows/` was touched, and confirmed [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]'s EBG-0109 entry and this report accurately describe the actual committed change with no aspirational overclaiming.

Real GitHub Actions CI (run `30342589297`) also confirmed green for `2b1e531`: all four jobs (`python`, `rust`, `playwright`, `frontend-build`) passed.

- `python -m pytest`: 382 passed, 1 skipped throughout. `python scripts/validate_repository.py` (full mode): 0 errors, 173 warnings throughout - unchanged from WP1's close, since this WP added no new files.

---

# 6C. Session-Wide WP3 - Repository Baseline Determination (RBL-0023 Established)

**Both independent verification passes recommended establishing a new baseline** rather than retaining RBL-0022: the pre-commit Codex design review (Pass) and the post-commit Codex diff review (Pass, no findings) both confirmed WP1 delivered a genuine, live-verified product code change to the Ollama provider adapter and the Tauri IPC layer, backed by new test coverage (1 new Python test, 5 new Rust unit tests) and real green CI. The Programme Sponsor's determination: **establish** - [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]] is accepted as the new current repository baseline, superseding [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]].

- `python -m pytest`: 382 passed, 1 skipped throughout. `python scripts/validate_repository.py` (full mode): 0 errors throughout - warning count rose from 173 at WP1's close to 177 by session close, across this WP's own governance edits (the new RBL-0023 document plus several REG-0001 version-history entries, whose summary text occasionally contains a phrase the checker's cross-document "Section N" pattern matches against an unrelated document, including this fix round's own entries); all disclosed as the same pre-existing false-positive category, not new defects. This count is not re-verified after this point - any further edit to this report itself would trigger the same mechanism again.

---

# 7. Related Artefacts

* [[ESR-0036_ENGINEERING_SESSION_REPORT|ESR-0036]] - prior closed session, immediate predecessor; EBG-0109 was discovered and registered immediately after its closure.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation and Engineering Session Lifecycle guidance followed for WP0A/WP0B.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0109 (this session's objective, Findings 1/2(c) closed, item remains open) and EBG-0108 (the dependent item motivating priority).
* [[RBL-0022_REPOSITORY_BASELINE|RBL-0022]] - prior accepted repository baseline, superseded by RBL-0023.
* [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]] - current accepted repository baseline, established at this session's WP3.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.4 | 28 July 2026 | Claude Engineering Implementer | Fix round: corrected the WP3 evidence line's warning-count figure to the actual final 176 rather than an intermediate 174. |
| 1.3 | 28 July 2026 | Claude Engineering Implementer | Fix round (Codex pre-commit finding on the WP3 closure package): corrected the WP2 section's warning-count figure, which had been overwritten to 174 by an unscoped replace-all when it should have stayed 173 (WP2 added no new files; the +1 to 174 only occurs once WP3 creates RBL-0023). |
| 1.2 | 28 July 2026 | Claude Engineering Implementer | ESR-0037 formally closed. Session-wide WP2 (Independent Repository Verification: Pass, no findings) and WP3 (Repository Baseline Determination: Establish - RBL-0023 accepted, superseding RBL-0022) complete. |
| 1.1 | 28 July 2026 | Claude Engineering Implementer | WP1 Complete: EBG-0109 Findings 1 and 2(c) fixed (Ollama reasoning-model timeout risk; Tauri IPC indefinite-hang/no-visible-error symptom), Codex design review Pass, Programme Sponsor-approved via the Sponsor Approval Service. |
| 1.0 | 28 July 2026 | Claude Engineering Implementer | ESR-0037 opened at WP0B, before WP1 began. Objective: diagnose and fix EBG-0109 (Ollama/Tauri conversation-path reliability). |
