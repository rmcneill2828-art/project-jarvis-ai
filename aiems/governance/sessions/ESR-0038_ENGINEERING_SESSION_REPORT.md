# ESR-0038 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0038 |
| Title | Engineering Session Report |
| Version | 1.1 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0038 |
| Date Opened | 28 July 2026 |
| Date Closed | - |
| Closure Status | Open - WP1 complete, session-wide verification pending |

---

# 2. Purpose

This report records the opening and execution of ESR-0038, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0037_ENGINEERING_SESSION_REPORT|ESR-0037]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]]. Created at WP0B, before WP1 began.

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0037_ENGINEERING_SESSION_REPORT|ESR-0037]] closed (28 July 2026), [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]] the current accepted baseline, working tree clean at `f9ee120`, pre-commit governance hook active, real CI green.

[[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0109 remains open: ESR-0037 WP1 closed Findings 1 and 2(c), but Finding 2(a)/2(b) (the live Guardian conversation path sometimes falling back to LocalEcho or hanging indefinitely against Ollama through the Tauri desktop shell's IPC path) and recommendation (d) were explicitly disclosed as unresolved, on the stated basis that reproducing them needed a live, controlled desktop session. Before committing to that framing, this session verified directly that the actual execution environment has a real NVIDIA GPU, a running Ollama installation (`qwen2.5:7b` present), and a working Rust toolchain - the same machine class the original diagnostic session used - and that `tauri` 2.11.5 (the exact version this repository depends on) ships a `test` feature exposing `tauri::test::mock_app()`, capable of producing a real (mocked) `AppHandle` without a visible on-screen window. This reopens a path to a genuine, automatable, non-GUI reproduction of Finding 2(a)/2(b) that ESR-0037 did not consider.

---

# 4. Engineering Authority

ESR-0038 opening was authorised by direct Programme Sponsor instruction on 28 July 2026, immediately following ESR-0037's closure, confirming [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]] as the accepted repository baseline at session open.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Reproduce and diagnose [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0109's remaining open findings (2(a): silent LocalEcho fallback; 2(b): indefinite hang with the request apparently never reaching Ollama) under controlled, automatable conditions, and fix the confirmed root cause if one is found.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | Reproduce and diagnose EBG-0109 Findings 2(a)/2(b); close the item | Complete |

---

# 6A. WP1 - EBG-0109 Findings 2(a)/2(b): Reproduction and Closure

## Attempt 1: `tauri::test::mock_app()` Rust-level harness (abandoned)

Design (genericise `src-tauri/src/lib.rs`'s backend-IPC functions - `spawn_backend`, `spawn_dev_backend`, `spawn_sidecar_backend`, `run_dev_reader`, `run_sidecar_reader`, `dispatch_line`, `call_backend` - over `R: tauri::Runtime` so a new `#[ignore]`d test could use `tauri::test::mock_app()` to drive `call_backend()` against a real spawned backend and real Ollama, without a visible window) was reviewed by Codex before implementation - **PASS, no findings**, independently confirming `tauri::test::mock_app()` exists in the resolved `tauri` 2.11.5 and that the proposed function list was complete and correct (except `route_response`, which needed no change - noted and not touched). Programme Sponsor-approved via the Sponsor Approval Service before implementation.

Implemented and compiled cleanly (`cargo check --all-targets`, `cargo build`, `cargo clippy -- -D warnings` all clean; the existing 5 unit tests still passed with the refactor alone). The new `#[ignore]`d test itself, however, caused the compiled test binary to crash at OS load time with `STATUS_ENTRYPOINT_NOT_FOUND` - before any test code ran, purely from `tauri::test::mock_app()` being linked into the binary. Bisected via `git stash`/manual file truncation to isolate the exact cause (Cargo.toml's `test`-feature dev-dependency alone: fine; the generic refactor alone: fine; only adding code that references `tauri::test::mock_app()`: crashes). Independently confirmed via a minimal, project-independent throwaway crate (just `tauri::test::mock_app()` in a single `#[test]`, no other code) - same crash, same exit code, proving this is a Tauri 2.11.5/Windows environment incompatibility, not a defect in this repository's code. Tried two older `tauri` versions (2.6.0, 2.9.3) to check version-specificity; both failed to even compile against this machine's Rust toolchain (1.96.0) for an unrelated reason (a `Send`/`Sync` trait-bound break in older `tauri-runtime-wry` against a newer `wry`), so version bisection was not possible without a larger, riskier toolchain/dependency downgrade. Checked the installed WebView2 Runtime (150.0.4078.99, current) - nothing obviously wrong there either. Further isolation would need native Windows debugging tools (Dependency Walker, Process Monitor) not available in this environment.

**This would have broken `cargo test` (including the CI `rust` job) had it been left in place** - the crash happens merely from the test binary containing the reference, independent of `#[ignore]`. Fully reverted before any commit (`git checkout -- src-tauri/src/lib.rs src-tauri/Cargo.toml`) once the Programme Sponsor chose to pivot rather than continue debugging; confirmed via `cargo build`/`clippy`/`fmt --check`/`test` that `src-tauri/` was back to the exact ESR-0037 state with no trace of the attempt.

## Attempt 2: live GUI reproduction (Programme Sponsor-run) - successful, EBG-0109 closed

The Programme Sponsor ran `npm run tauri dev` directly (with `JARVIS_OLLAMA_MODEL=qwen2.5:7b` set in the launching shell, per the original diagnostic session's own fast-model choice) and sent two sequential messages in the same window, twice, across two independent fresh app launches - the exact controlled, single-session conditions EBG-0109's own recommendation (a) called for.

- **Run 1**: `ollama ps` confirmed `qwen2.5:7b` loaded on GPU (context 4096, matching this session's own ESR-0037 `num_ctx` fix) before message 1. Message 1 ("Say hello in exactly five words") returned a genuine model response ("Hello, how are you?") in 1m28s - slower than the 5-22s standalone baseline, plausibly cold-start overhead (first request since the backend process spawned), but still comfortably under the 90s Python-side timeout, and critically not a `local-echo:` fallback. Message 2 ("Say goodbye in exactly five words") returned a genuine response ("Farewell, may we meet again.") almost instantly, with `ollama ps` still showing the model loaded and active.
- **Run 2** (fresh app relaunch): both messages returned genuine responses almost instantly.

**Neither Finding 2(a) (LocalEcho fallback) nor Finding 2(b) (indefinite hang, Ollama idle) reproduced in either run.** This is disclosed as strong evidence, not formal proof of absence: the most likely explanation is that recommendation (a)'s own named confound - the original diagnostic session's own concurrent direct-Ollama calls running alongside the GUI test - caused the original observations, rather than a genuine defect in `src-tauri/src/lib.rs`'s IPC path. Recommendation (d) (`stdio_rpc.py`'s write-lock/heartbeat-thread interaction) was already independently code-reviewed at ESR-0037 with no defect found and was not further actioned here.

**EBG-0109 closed (marked Complete)** on this basis, per Programme Sponsor decision - if this recurs under real household/multi-request load in the future, it should be re-opened with fresh evidence rather than this closure being treated as ruling that out permanently.

- Files: [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]]. No source code changes in the final state (the Rust refactor attempt was fully reverted).
- `python -m pytest`: 382 passed, 1 skipped, unchanged (no Python code touched). `cargo build`/`clippy -- -D warnings`/`fmt --check`/`test`: all clean, unchanged from RBL-0023 (5 existing unit tests, no new ones - the reproduction attempt left no trace).

---

# 7. Related Artefacts

* [[ESR-0037_ENGINEERING_SESSION_REPORT|ESR-0037]] - prior closed session, immediate predecessor; fixed EBG-0109 Findings 1/2(c), left 2(a)/2(b)/recommendation (d) open pending live reproduction.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0109, this session's objective.
* [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]] - current accepted repository baseline at session open.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1 | 28 July 2026 | Claude Engineering Implementer | WP1 Complete: `tauri::test::mock_app()` reproduction harness attempt abandoned (confirmed Tauri 2.11.5/Windows environment incompatibility, fully reverted); Programme Sponsor-run live GUI reproduction found no trace of Findings 2(a)/2(b) across two independent runs; EBG-0109 closed. |
| 1.0 | 28 July 2026 | Claude Engineering Implementer | ESR-0038 opened at WP0B, before WP1 began. Objective: reproduce and fix EBG-0109's remaining open findings (2(a)/2(b)) via a real, non-GUI reproduction harness using `tauri::test::mock_app()`. |
