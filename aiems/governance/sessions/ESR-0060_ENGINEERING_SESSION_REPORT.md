# ESR-0060 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0060 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0060 |
| Date Opened | 30 September 2026 |
| Date Closed | 1 October 2026 |
| Closure Status | Closed - WP1, WP1b and WP2 complete; RBL-0040 established, superseding RBL-0039 |

---

# 2. Purpose

This report records the opening of ESR-0060, at the Programme Sponsor's direct request ("start next ESR"), following ESR-0059's formal closure and the establishment of [[RBL-0039_REPOSITORY_BASELINE|RBL-0039]].

The session runs **review-first**, by Programme Sponsor decision: no independent Engineering Reviewer was available at opening (Section 3, WP0A), so the session's first Work Package is the retrospective GitHub Copilot CLI review owed under EBG-0153, run once Copilot's monthly quota resets on 1 October 2026, and no implementation is made until that review has run. Until then, work is limited to session opening and design drafting.

WP0A/WP0B session initialisation followed PBK-0001 and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]].

---

# 3. Scope

**WP0A - Repository Synchronisation (Complete):** Working tree clean at session open. HEAD `cd8c06e` (ESR-0059 WP16), in sync with `origin/main`; that commit's CI run (36601728449) green on all jobs. Repository baseline confirmed as [[RBL-0039_REPOSITORY_BASELINE|RBL-0039]] (accepted ESR-0059 WP16). Pre-commit governance hook confirmed active (`core.hooksPath` = `scripts/hooks`). Full Python suite confirmed green at open: 751 passed, 1 skipped. `scripts/session_launcher.py` run for WP0B: PST-0001's Next Work Package Candidate lists EBG-0153, process-tree termination for the packaged backend (EIP-ESR0059-001 Section 4G), EBG-0149 to EBG-0151, and EBG-0130.

**Reviewer availability probed at open - neither independent reviewer is available:**

* **GitHub Copilot CLI** (permanent Engineering Reviewer since ESR-0058): `copilot -p "Reply with the single word OK." -s --deny-tool='write'` still returns "You have exceeded your monthly quota". The Programme Sponsor confirmed the quota resets on 1 October 2026 (the 1st of each month).
* **Codex CLI** (considered as a same-day substitute): `codex exec -s read-only` fails with `402 Payment Required`, auth error code `deactivated_workspace` - the ChatGPT workspace behind it is no longer active. This is new: Codex was last used successfully at ESR-0047. Out-of-repository account state; not investigated further without Programme Sponsor direction. It means EBG-0153's single-reviewer risk currently has no fallback at all.

**WP0B - Engineering Session Initialisation (Complete):** ESR-0059 confirmed formally Closed. ESR-0060 opened as the next session identifier. `~/.current_session` updated to `ESR-0060`. Objective set by Programme Sponsor decision among presented options - **"Open now, review-first"**: WP1 is the EBG-0153 retrospective Copilot review of ESR-0059 WP4 to WP14 once the quota resets; WP2 is process-tree termination for the packaged backend, design-reviewed by Copilot before any implementation. Today's work is limited to opening the session and drafting WP2's design.

**WP1 - EBG-0153 Retrospective Engineering Review (Complete):** GitHub Copilot CLI quota confirmed reset on 1 October 2026 (one-line probe returned "OK"). Routed through the real bridge (`init`/`submit-to-review` for `ESR-0060`/`WP1`, 46-file scope = the committed code diff `f33286a^..61f1712`, governance documents excluded). Review-only: no code change proposed. Run as three genuine scoped Copilot CLI invocations (`--allow-tool='shell(git:*)' --allow-tool='shell(python:*)' --deny-tool='write'`), one per batch, each briefed to test every ESR-0059 self-review claim against the code rather than accept it, and each recording its own `return-findings` entry - all three independently verified against the transcript (`sender: reviewer`, `repository_ref: 5fbfff9...`).

* **Batch A, WP4-WP6 - Conditional Pass.** WP5's GIL-reliant thread-safety claim **holds** for the paths it covers: every stdout write (main thread, slow lane, heartbeat) is under one `_write_lock`, so JSON lines cannot interleave; per-profile Cognitive Cores are touched only by the single slow-lane worker; health-map reads racing worker writes are benign one-step-stale reads. Retry backoff never sleeps past the deadline; a non-ALLOW Sentinel decision raises before any provider is touched; transient-status classification matches across all three adapters. **Finding 1 (High), reproduced live by the reviewer**: `JARVIS_PRIMARY_PROVIDER` is matched case-sensitively - `Gemini` with a valid key registers only `ollama`, silently, with no log line. Registered EBG-0155. **Finding 2 (Medium), reproduced by the reviewer and confirmed by the Engineering Implementer in code**: a deadline that expires inside a provider's own `remaining_timeout()` raises a plain `RuntimeError`, which `execute()` treats as a genuine fault - the provider is marked DEGRADED and its circuit opened for 30 seconds, contrary to EIP-ESR0059-005/006. Registered EBG-0156. Findings 3-5 (concurrent SQLite access with no `busy_timeout`; an unguarded fast-lane write failure; no automated real-thread test) registered in EBG-0157. On finding 3 the Engineering Implementer disagrees with the reviewer's Medium rating: memory writes are short single transactions and Python's 5-second default lock wait applies, so it is hardening, not a live defect.
* **Batch B, WP7-WP10 - Pass.** Strict user/assistant alternation for OpenAI and Gemini; persona-only system prompts; every text-accepting RPC limited before any runtime call, with the UXP limit matching; no conversation or memory content on any audit or log path (every `AuditEvent` traced); rotation under one lock; nothing logged to stdout; a revoked memory is absent from the very next turn. Re-ran the full suite: 751 passed, 1 skipped; ruff clean; validator 0 errors. Two Low findings (raw `str(exc)` in RPC error replies and in persisted provider-failure audit reasons - safe today only by adapter discipline) registered in EBG-0157.
* **Batch C, WP11-WP14 - Pass.** Exactly three subprocess call sites, all list-form with closed stdin; the frozen executable is never re-invoked as an interpreter; a newer-than-code database is refused untouched and five concurrent first-opens migrate correctly (both verified with throwaway scripts); every memory handler takes the profile from the identity service, never from parameters; another profile's memory is indistinguishable from a missing one. One Low finding (the 100 pending-proposal cap is shared across profiles) registered in EBG-0157.

EBG-0153 closed Completed. **Programme Sponsor decision (option (a), direct chat instruction)**: close WP1, and fix the High finding as a separate Work Package before WP2. Read as taking the recommendation in full, so WP1b covers EBG-0156 as well as EBG-0155. This adds a Work Package to the session plan, recorded as an explicit Programme Sponsor scope change. Single-reviewer risk unchanged: Codex remains unavailable.

**WP1b - Provider-Selection and Deadline-Health Fixes (Complete):** [[EIP-ESR0060-001_PROVIDER_SELECTION_AND_DEADLINE_HEALTH_FIXES|EIP-ESR0060-001]] v1.0. EBG-0155: `JARVIS_PRIMARY_PROVIDER` is now stripped and lower-cased like the secondary, and unknown primary or secondary names are logged as a warning instead of being dropped silently. **Second defect found while reading the code, not raised by the review**: a set-but-blank primary bypassed the default and also built no cloud provider; blank now means the default. EBG-0156: `remaining_timeout()` raises a new `DeadlineExceededError` (still a `RuntimeError`), which `ProviderOrchestrator.execute()` treats as out of time, leaving health and circuit untouched. 8 new tests; five of the six provider-selection tests were run against the old code and fail there. pytest 759 passed/1 skipped, ruff clean, validator 0 errors. Disclosed residual, raised for the design review: a network timeout shortened by the deadline still counts as a fault.

**Design review**: routed through the real bridge (`init`/`submit-to-review` for `ESR-0060`/`WP1b`, 9-file scope) and reviewed by GitHub Copilot CLI with scoped, write-denied tools. **Verdict: Pass**, with no blocking findings, independently verified against the transcript (`sender: reviewer`). The reviewer traced every primary/secondary combination (mixed case, blank, `none`, unknown, same as primary, missing credential), confirmed against `git show HEAD` that five of the six provider-selection tests fail on the old code, and confirmed that `DeadlineExceededError` is raised only by `remaining_timeout()`, reaches the orchestrator unwrapped from all three adapters, is never retried, and leaves health and circuit untouched. It re-ran pytest (759 passed/1 skipped), ruff (clean) and the validator (0 errors). Two informational notes: a provider stopped by the deadline is listed as attempted, which matches the existing pre-call path, so no change was made; and the EBG-0155 row named the wrong function, now corrected. On the open question, the reviewer recommended leaving the deadline-capped-timeout residual in the backlog and suggested a design; recorded as EBG-0157 item (6).

**Programme Sponsor approved** in direct chat ("Approved") and via the Sponsor Approval Service (`approve`, `repository_ref: 7fd5279`, 2026-10-01T09:32:59Z). The approval arrived just before the design review returned. The review then passed with no code change, so it covers what was reviewed; only the record-keeping above (EIP v1.0, this section, two EBR-0001 text edits) changed afterwards.

**Committed** as `e1d31a4` through `submit-response` (2026-10-01T09:35:08Z) and pushed. CI run 36843717345 on `main` green on all four jobs (python, rust, frontend-build, playwright).

**Post-commit independent review**: a further genuine scoped `copilot` invocation against the real pushed commit - **Pass**, no findings, independently verified against the transcript (`repository_ref: e1d31a4...`). It confirmed the exact 9-file changed-set, that the committed code is identical to what was design-reviewed and that the later changes were record-keeping only, every commit-message claim, the REG-0001 rows against each document's own version, and a clean working tree. It re-ran pytest (759 passed/1 skipped), ruff (clean) and the validator (0 errors) against the committed state. **WP1b closed.**

**WP2 - Backend Process-Tree Termination (Complete):** [[EIP-ESR0060-002_BACKEND_PROCESS_TREE_TERMINATION|EIP-ESR0060-002]] drafted (v0.1). No code changed. EBG-0154 registered in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] (Candidate Backlog, Medium). **Programme Sponsor approved the new direct `windows-sys` dependency** (EIP Section 4F) via direct chat instruction ("Approved"). This approves the dependency only; implementation still waits for the design review, and EIP-ESR0060-002 is synced to v0.2.

**Real finding made while investigating, before drafting** - EIP-ESR0059-001 Section 4G recorded that terminating the backend's direct child might not reach the real interpreter, "not verified". Verified on this machine today against the real packaged sidecar (`src-tauri/binaries/jarvis-backend-x86_64-pc-windows-msvc.exe`, built 29 September 2026 at ESR-0059 WP11):

* The onefile sidecar runs as a bootloader plus a child process. Killing only the bootloader, with stdin held open, **leaves the child - the real backend - running**.
* But `CommandChild::kill()` consumes the handle, which also drops its stdin writer. Killing the bootloader *and* closing stdin ended an idle backend in 58 ms; closing stdin alone ended bootloader and child cleanly in 637 ms ("Guardian runtime foundation stopped" logged).
* The dev path (`python` resolving to the repository's `.venv` launcher) did **not** orphan: the launcher's child ended with it.
* So the real exposure is narrower than 4G implied: `serve_forever()` deliberately drains every in-flight and queued slow request on stdin EOF (ESR-0059 WP5, "a request accepted is always answered"), each bounded by the 100-second per-turn deadline, and a fast-lane handler blocks EOF handling entirely while it runs. A backend torn down while busy - the malformed-output, connection and write-failure teardown paths, often exactly when it is misbehaving - keeps running on the same SQLite stores until that work ends, while `call_backend()` spawns a replacement beside it. A genuinely hung backend is never ended.

Recorded as EBG-0154 rather than overstated: this is not "every app close leaks a backend".

**Design review (1 October 2026)**: routed through the real bridge (`init`/`submit-to-review` for `ESR-0060`/`WP2`, design only) and reviewed by GitHub Copilot CLI with scoped, write-denied tools, with the `tauri-plugin-shell` 2.3.5 and `windows-sys` 0.60.2 sources available to check API claims. **Verdict: Conditional Pass**, independently verified against the transcript (`sender: reviewer`). The core mechanism was confirmed: dropping `CommandChild` closes the backend's stdin (also checked independently by the Engineering Implementer in the plugin source: `stdin_writer` is owned only by `CommandChild`); every `tear_down_if_current()` caller runs on a reader thread or Tokio's blocking pool, so the grace wait is harmless there, and releasing the lock before it reopens no orphan path; the feature list covers every API used; PyInstaller's bootloader never breaks away from a job. Five findings, all addressed in EIP-ESR0060-002 v0.3: (1, Medium) the no-job fallback would sleep the full 3 s blindly, and (4, Low) its PID-based `TerminateProcess` contradicted the PID-reuse argument against `taskkill` - both fixed by holding a process handle from spawn, which gives an early return and a reuse-safe kill; (2, Medium) suspended spawning recorded as considered and deferred rather than unavailable; (3, Medium) the exit handler's wait runs on the main thread - disclosed, and added to the live check, since windows are normally already closed by then; (5, Low) a test for a genuine `adopt()` failure added.

**Design re-review**: **Conditional Pass**, independently verified against the transcript. All five findings confirmed resolved - the held handle judged a stronger fix than the one the reviewer had suggested. One new Low finding: v0.3's way of forcing an `adopt()` failure (an already-exited child's PID) is unreliable and could adopt an unrelated process after PID reuse. Corrected in v0.4 to `adopt(0)`, which `OpenProcess` is documented to reject at every privilege level (CI runners are elevated, so the reviewer's suggested PID 4 was not used). Advisory adopted: the held handle gets an explicit `Drop` owner. The reviewer's sandbox could not read the cargo registry this run, so it relied on docs.rs for the new APIs' feature coverage; the Engineering Implementer had already confirmed it in the local source.

**Final design re-review**: **Pass**, no findings, independently verified against the transcript.

**Programme Sponsor approved the design for implementation** via direct chat instruction ("Approved").

**Implementation** (EIP-ESR0060-002 v0.5, Section 4I). `src-tauri/src/lib.rs`: `ProcessGuard` (optional job object and held process handle, both closed in `Drop`), `BackendHandle::shutdown()` replacing `kill()`, teardown and app exit shutting down after releasing the lock, and non-Windows stand-ins so Linux still builds. **Two real gaps that the design and all three review rounds missed, found while implementing:**

* `windows-sys` 0.60.2 compiles `CreateJobObjectW` only with a fourth feature, `Win32_Security`. Same crate and copy, no new package, but beyond the three features the Programme Sponsor approved - **flagged for the Programme Sponsor**.
* The CI `rust` job runs on **Linux**, not Windows, so the seven Windows job-object tests run locally only. CI compiles and tests the non-Windows path (verified on WSL Ubuntu: clippy clean, 11 tests passed). Whether to add a Windows CI job is **raised for the Programme Sponsor**, not done here.

**Live checks**, sidecar rebuilt from the current code and release app built: (a) normal close - both backend processes gone in 826 ms, graceful (clean "stopped" logged); (b) the real packaged sidecar torn down with a slow turn in flight - the job held both processes (the spawn-to-adopt gap did not let the interpreter escape) and the whole tree was ended by force at 3.006 s, where before this package it survived for up to 100 s per queued turn; (c) host force-killed - tree gone in 96 ms; dev path - forced at 3.09 s when closed while still busy with startup calls, graceful in 161 ms once settled. Validation: cargo test 18 passed/1 ignored, clippy and fmt clean; pytest 759 passed/1 skipped; Playwright 26/26; ruff clean; validator 0 errors. A leaked Vite dev-server process from the dev-path check was found and stopped.

**Implementation review**: genuine scoped GitHub Copilot CLI invocation (cargo allowed, writes denied) - **Conditional Pass**, independently verified against the transcript. Confirmed the FFI (struct sizes, NULL checks, each handle closed exactly once), every guard/path combination, the lock released before shutdown, and re-ran cargo fmt/clippy/test (all 7 Windows tests genuinely executed), pytest and the validator. **One real Medium finding, fixed (EIP v0.6)**: `force()` assumed termination succeeded, and the dev path then called an unbounded `wait()` - a failed termination could have hung teardown forever. Termination results are now checked with fallback, and reaping is bounded. Advisories adopted (a `WAIT_INFINITE` comment; a spawn-to-attach PID-reuse race recorded). The reviewer recommends a Windows CI job running `cargo test` on pushes to `main`, and `--tests` on CI's clippy step - **raised for the Programme Sponsor** with the `Win32_Security` question. cargo test 19 passed/1 ignored, Linux 12 passed; live harness (b) re-run on v0.6 unchanged (3.05 s).

**Implementation re-review**: **Pass**, no findings, independently verified against the transcript. It traced every shutdown path for an unbounded wait and found none, and re-ran the new bounded-reap test three more times (2.03-2.04 s each, not flaky).

**Programme Sponsor decision 2(a)** (direct chat instruction): add the Windows CI job now, as part of WP2. `.github/workflows/ci.yml` gains `rust-windows` (`cargo test` on `windows-latest`, on pushes to `main` and on demand only) and `--tests` on the Linux clippy step (EIP-ESR0060-002 v0.7). 
**CI-change review**: **Pass**, independently verified against the transcript (steps match the working Linux and release jobs, gating correct, no new third-party action). Two notes: the Windows tests' timing margins were sized on this machine, so the first shared-runner runs will be watched; and the job builds no frontend, which is confirmed only by symmetry with the Linux job until its first run.

**Programme Sponsor approved** via direct chat instruction ("Approved") and the Sponsor Approval Service (`approve`, `repository_ref: e2eb0f5`, 2026-10-01T15:22:26Z, after the CI-change review). The request covered both the `Win32_Security` feature and the commit; read as approving both. EIP-ESR0060-002 synced to v1.0.

**Committed** as `5f1693b` through `submit-response` (2026-10-01T15:26:03Z) and pushed. CI run 36884252081 on `main` green on all five jobs. **The new `rust-windows` job passed on its first run**: all seven Windows job-object tests executed and passed on a GitHub-hosted Windows runner, which runs jobs inside its own job object, so nested job objects work there. The test timing margins the CI-change review flagged held on this run.

**Post-commit independent review**: a further genuine scoped `copilot` invocation against the real pushed commit - **Pass**, no findings, independently verified against the transcript (`repository_ref: 5f1693b...`). It confirmed the exact 8-file changed-set, that the committed code and CI file are identical to what was reviewed with only record-keeping changed since, every commit-message claim, the REG-0001 rows and a clean tree. **Disclosed gap**: this review's tool permissions refused every validation command, so it re-ran none. It instead cited earlier transcript results, attributing them to the wrong review round and misquoting pytest as 760 passed. The Engineering Implementer therefore re-ran everything against the committed state: cargo fmt and clippy `--tests` clean, cargo test 19 passed/1 ignored, pytest 759 passed/1 skipped, ruff clean, validator 0 errors. CI ran the same on both platforms. **WP2 closed.**

---

# 3A. Session-Wide WP3 - Independent Repository Verification

The Programme Sponsor directed closing the session with a new baseline after WP2. Unlike ESR-0059, the Engineering Reviewer was available: a genuine scoped GitHub Copilot CLI review ran through the real bridge (`ESR-0060`/`WP3`) over the whole session range.

Range `cd8c06e..679c7dd` (ESR-0059's closing commit to WP2's closure):

* **6 commits**, 14 files changed, 1,420 insertions, 42 deletions. Every commit gated through `submit-response` against an approval recorded at its parent commit - confirmed by the reviewer for all six.
* **CI on `main`**: every session run green on all jobs; the new `rust-windows` job passed on both of its runs (`5f1693b`, `679c7dd`).
* **`sentinel/policy.py`**: zero lines changed all session.
* **Fresh re-run by the Engineering Implementer against the final state**: pytest 759 passed/1 skipped, run against a fake home directory with no files written there; Playwright 26/26; cargo test 19 passed/1 ignored, clippy `--tests` and fmt clean; ruff clean; `validate_repository.py` 0 errors/333 warnings (unchanged); `sync_product_version.py --check` agrees; `npm run build` clean; `pip-audit` in a fresh virtual environment no known vulnerabilities. (This machine's own `.venv` still has urllib3 2.7.0, which three new advisories flag; a fresh install resolves 2.8.0 - a local environment matter, not a repository one.)

**Reviewer verdict: Pass**, independently verified against the transcript (`sender: reviewer`). No findings against gating, claim accuracy or register consistency, and no interaction between WP1b's provider changes and WP2's host changes. Its tool permissions again refused its validation commands (as at WP2's post-commit review), so the results above are the Engineering Implementer's own re-run. Three findings, all about carrying open items visibly into the handover, all addressed:

1. (Low) The `rust-windows` job does not run on pull requests, so a Windows regression surfaces only after merging - recorded in RBL-0040's handover as an accepted risk of the Programme Sponsor's decision 2(a).
2. (Low) Two WP2 residuals lived only in EIP prose: the spawn-to-attach PID-reuse race, and the manual "Not Responding" check during exit - added to EBG-0157 as items (7) and (8).
3. (Info) Codex still being unavailable appeared only in prose - added to Section 6 and RBL-0040's handover.

**Added by the Engineering Implementer at closure**: Dependabot has opened pull requests bumping `tauri-plugin-shell` 2.3.5 to 2.4.0 and `tauri` to 2.12.0. WP2's graceful path relies on 2.3.5's `CommandChild` closing stdin when dropped, so EBG-0158 is registered: re-verify that before merging either bump.

**Advisory baseline assessment: Establish** - the independent review RBL-0039 owed is discharged, the two real defects it found are fixed, and the last open runtime-safety item from ESR-0059 is delivered and live-verified, every step genuinely reviewed.

---

# 3B. Session-Wide WP4 - Repository Baseline Determination

**The Programme Sponsor's determination**: **establish a new baseline**, by direct instruction ("yes please close ESR-0060 with new baseline"). [[RBL-0040_REPOSITORY_BASELINE|RBL-0040]] created and accepted, superseding RBL-0039.

Every controlled artefact's "current accepted repository baseline" pointer updated to RBL-0040: [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]], [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]], [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]], the [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] and [[PST-0001_PROGRAMME_STATUS|PST-0001]] (full closure sweep - Current Mode, Baseline, Phase, Workflow and Objective; Section 4A rewritten for ESR-0060; the Prior Session rolling window shifted, ESR-0059 added and ESR-0056 dropped; Next Required Activity and Next Work Package Candidate refreshed). **Documentation Debt found during the sweep and corrected**: README.md still said ESR-0058 was the latest closed session (missed at ESR-0059's closure); PST-0001 Section 9's "Latest figures" still quoted ESR-0058's test counts. README.md (uncontrolled) updated to match.

**ESR-0060 formally closed.**

---

# 4. Engineering Authority

ESR-0060 opening was authorised by direct Programme Sponsor instruction on 30 September 2026, following ESR-0059's formal closure.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Review-first: discharge EBG-0153's retrospective independent review of ESR-0059 WP4 to WP14 as soon as GitHub Copilot CLI's quota resets, fix what it finds that matters (WP1b), then deliver backend process-tree termination (EBG-0154) through the standing design-review, Programme Sponsor approval, `submit-response` and post-commit-review template, with a genuine independent reviewer at every step.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP0A | Repository Synchronisation | Complete |
| WP0B | Engineering Session Initialisation | Complete |
| WP1 | EBG-0153 retrospective Copilot CLI review of ESR-0059 WP4 to WP14 | Complete - A Conditional Pass, B Pass, C Pass; EBG-0155 to EBG-0157 registered |
| WP1b | Provider-selection case fix and deadline-health fix (EBG-0155, EBG-0156) | Complete - `e1d31a4`, CI green, post-commit review Pass |
| WP2 | Backend process-tree termination (EBG-0154) | Complete - `5f1693b`, CI green incl. first `rust-windows` run, post-commit review Pass |
| WP3 | Session-wide independent repository verification | Complete - genuine Copilot CLI review, Pass; three handover findings addressed |
| WP4 | Repository baseline determination | Complete - Establish; RBL-0040 accepted |
| Carried forward | EBG-0158 (re-verify before the `tauri-plugin-shell` 2.4.0 bump); EBG-0149, EBG-0150, EBG-0151, EBG-0157 (Low); EBG-0130 (Programme Sponsor judgement). Codex CLI still unavailable (402), so Copilot's monthly quota is the only independent review path | Not started |

---

# 7. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 1 October 2026 | Programme Sponsor | ESR-0060 formally closed. WP3 session-wide verification: genuine GitHub Copilot CLI review - Pass, three handover findings addressed, EBG-0158 registered. WP4: Establish RBL-0040, superseding RBL-0039, by Programme Sponsor direction. |
| 0.13 | 1 October 2026 | Claude Engineering Implementer | WP2 closed: 5f1693b CI green on all five jobs (run 36884252081), including the first rust-windows run with all seven job-object tests passing; genuine Copilot CLI post-commit review Pass (its validation re-runs were refused by tool permissions, so re-run by the Engineering Implementer, all green). |
| 0.12 | 1 October 2026 | Claude Engineering Implementer | WP2 CI-change review Pass; Programme Sponsor approved the Win32_Security feature and the commit via the Sponsor Approval Service; EIP-ESR0060-002 synced to 1.0 (REG-0001 row synced by hand). Pending commit. |
| 0.11 | 1 October 2026 | Claude Engineering Implementer | WP2 implementation re-review Pass; Programme Sponsor decision 2(a): rust-windows CI job and clippy --tests added (EIP-ESR0060-002 v0.7, REG-0001 row synced by hand); awaiting review of the CI change. |
| 0.10 | 1 October 2026 | Claude Engineering Implementer | WP2 implementation review Conditional Pass; Medium finding (unchecked termination plus unbounded reap) fixed in EIP-ESR0060-002 v0.6 (REG-0001 row synced by hand); Windows CI job and clippy --tests recommendations raised for the Programme Sponsor; awaiting re-review. |
| 0.9 | 1 October 2026 | Claude Engineering Implementer | WP2 final design re-review Pass; Programme Sponsor approved implementation; implemented per EIP-ESR0060-002 v0.5 (REG-0001 row synced by hand). Two gaps missed by the design reviews flagged: Win32_Security feature needed; CI rust job runs on Linux. Live checks passed. Awaiting implementation review. |
| 0.8 | 1 October 2026 | Claude Engineering Implementer | WP2 design re-review Conditional Pass (one new Low finding: unreliable adopt() failure test); EIP-ESR0060-002 v0.4 corrects it to adopt(0) and adds an explicit Drop owner for the held handle (REG-0001 row synced by hand); awaiting final re-review. |
| 0.7 | 1 October 2026 | Claude Engineering Implementer | WP2 design review Conditional Pass (genuine Copilot CLI); EIP-ESR0060-002 revised to v0.3 addressing all five findings (REG-0001 row synced by hand); awaiting re-review. |
| 0.6 | 1 October 2026 | Claude Engineering Implementer | WP1b closed: e1d31a4 CI green (run 36843717345, all four jobs); genuine Copilot CLI post-commit review Pass. WP2 next. |
| 0.5 | 1 October 2026 | Claude Engineering Implementer | WP1b design review Pass (genuine Copilot CLI, no blocking findings); Programme Sponsor approved via the Sponsor Approval Service; EIP-ESR0060-001 synced to 1.0 (Approved - implemented; REG-0001 row synced by hand). Pending commit. |
| 0.4 | 1 October 2026 | Claude Engineering Implementer | WP1b implemented per EIP-ESR0060-001 v0.1 (registered by hand in REG-0001, EIP-ESR*-style id): EBG-0155 provider-name normalisation plus a second blank-primary defect found while reading the code; EBG-0156 DeadlineExceededError. 8 new tests; pytest 759 passed/1 skipped. Awaiting design review. |
| 0.3 | 1 October 2026 | Claude Engineering Implementer | WP1 complete: EBG-0153 retrospective review of ESR-0059 WP4-WP14 ran as three genuine scoped Copilot CLI reviews through the bridge (A Conditional Pass, B Pass, C Pass); WP5's GIL-reliant thread safety confirmed; EBG-0155 to EBG-0157 registered. Programme Sponsor decision (a): WP1b added before WP2 to fix EBG-0155 and EBG-0156. |
| 0.2 | 30 September 2026 | Claude Engineering Implementer | Programme Sponsor approved the new direct windows-sys dependency for WP2 (EIP-ESR0060-002 Section 4F), via direct chat instruction ("Approved"). Dependency only; implementation still waits for the design review. EIP-ESR0060-002 synced to v0.2. |
| 0.1 | 30 September 2026 | Claude Engineering Implementer | ESR-0060 opened. WP0A/WP0B complete. Neither independent reviewer available (Copilot CLI quota exhausted until 1 October 2026; Codex CLI workspace deactivated). Objective set by Programme Sponsor decision: review-first. WP2 design drafted per EIP-ESR0060-002 v0.1 after verifying EIP-ESR0059-001 Section 4G live; EBG-0154 registered. No code changed. |
