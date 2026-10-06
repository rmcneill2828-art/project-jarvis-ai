# EIP-ESR0061-002 - Platform Hardening and macOS

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0061-002 |
| Title | Engineering Implementation Package: WP2 Platform Hardening and macOS |
| Version | 0.4 |
| Status | Draft - WP2a built; implementation review Pass; awaiting Programme Sponsor approval of the built result |
| Session | ESR-0061 |
| Work Package | WP2 (WP2a, WP2b) |
| Plan | [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]] Section 7, WP2 |
| Risk class | **High-risk** (plan Section 7). **Programme Sponsor override of D19 for WP2** (direct chat decision "1", 6 October 2026): Antigravity CLI (Gemini) is the only independent reviewer, because Copilot's quota is exhausted until 1 November 2026. A High finding from it still blocks. |

---

# 2. Purpose

Implements go-live plan WP2: harden the shared platform, settle the dependency set for Version 1.0, and bring up macOS on Apple Silicon. Backlog: EBG-0158, EBG-0149, EBG-0157 items (1)-(5), (7), (8), EBG-0054 (non-Windows setup), EBG-0162 (macOS). Item (6) of EBG-0157 belongs to WP3.

# 3. Proposed Decomposition

| Sub-WP | Content | Kind | Effort |
|---|---|---|---|
| **WP2a** | Shared hardening and dependency settlement: EBG-0157 (1)-(5), (7), (8); EBG-0149; EBG-0158; the open Dependabot updates | Code (two gates, rule A6) | 2-2.5 d |
| **WP2b** | macOS (EBG-0162) and the non-Windows setup script (EBG-0054) | Code (two gates) | 2.75-3.75 d |

WP2b's process-tree design depends on how PyInstaller's bootloader behaves on macOS (Section 6), verified against its documentation and source before that design is drafted. WP2a is independent of it.

---

# 4. Repository Context Investigated (WP2a)

* **SQLite** - `jarvis/memory/store.py:104` and `jarvis/identity/store.py:85` call `sqlite3.connect(db_path)` with Python's defaults: rollback journal, a 5-second busy timeout, no WAL. Since ESR-0059 WP5 the slow lane (conversation, which reads memory) and the main thread (memory writes) can open the same file at once.
* **RPC error replies** - `StdioRpcServer.handle_line()` (`jarvis/interfaces/stdio_rpc.py:1015`) returns `f"{type(exc).__name__}: {exc}"` for any handler exception. **The UI shows these messages** (`src/App.jsx:847, 913, 989` render `result.message`), and several are deliberately user-facing (for example `PersonalMemoryService`'s "Memory retention request was denied by Sentinel policy ..."). So "exception type only" for every error would degrade the experience. `ProviderOrchestrator` (`sentinel/orchestrator.py:265`) persists `f"Provider execution failed: {last_error}"` into the durable audit record.
* **Fast lane** - `serve_forever()` runs fast methods on the read loop's thread via `_process_line()`; a write failure there raises out of the loop and ends the backend. The slow lane uses `_process_line_logged()`, which logs and survives.
* **Pending proposals** - `PersonalMemoryService` keeps one dict, capped at `MAX_PENDING_PROPOSALS = 100` (`jarvis/memory/service.py:39, 108`), shared by every profile.
* **Spawn-to-attach race** - `spawn_sidecar_backend()` and `spawn_dev_backend()` call `ProcessGuard::attach(pid)` straight after spawning (`src-tauri/src/lib.rs:741, 790`); `attach` opens handles by PID. If the child had already died and its PID been reused, the guard could adopt an unrelated process.
* **Capability** - `src-tauri/capabilities/default.json` grants the webview `shell:allow-execute` for the `jarvis-backend` sidecar, though the sidecar is spawned from Rust via `ShellExt`.
* **Open Dependabot pull requests** (6 October 2026): #17 `tauri-plugin-shell` 2.3.5 to 2.4.0; #26 `tauri` 2.11.5 to 2.12.0; #19 `@tauri-apps/plugin-shell` 2.3.5 to 2.3.6; #21 `@playwright/test` 1.61.1 to 1.63.0; #22 `pyinstaller` >=6.21 to >=6.22.3; #23 `react-dom` 18.3.1 to 19.3.0; #24 `lucide-react` 1.23.0 to 1.45.0; #25 `vite` 8.2.2 to 8.3.0; #27 `ruff` 0.16.0 to 0.16.9; #18 `piper-tts` requirement. **Merging them on GitHub would bypass the Sponsor Approval Service gate**, so WP2a applies the chosen updates in its own gated commit instead.

# 5. WP2a - Design

**5.1 SQLite (EBG-0157 item 1).** Both stores open connections through one shared helper that sets `PRAGMA busy_timeout = 5000` explicitly and puts the database in WAL mode once, at migration time (`PRAGMA journal_mode = WAL`; persistent per file). WAL lets readers proceed while a writer commits, which is the slow-lane/main-thread case. Backup and restore need no change: `export_snapshot()`/`import_snapshot()` (`jarvis/memory/store.py:289, 339`) are a logical JSON export/import inside a transaction, which already sees a consistent snapshot under WAL (v0.2, design review finding 1 - v0.1 wrongly proposed a checkpoint). Nothing in the repository copies the database file itself; the build confirms this by search. Test: two real threads write and read concurrently without `database is locked`.

**5.2 Error replies and the audit reason (EBG-0157 item 2).** A new `ClientFacingError(RuntimeError)` in `jarvis/shared/` marks a message as written for the user. `handle_line()` returns its message unchanged; for **any other exception it returns only the exception type** plus a fixed sentence ("Guardian hit an internal error (TypeName)."), and logs the full exception to `backend.log` (never to the client). Every deliberate user-facing `raise` reachable from an RPC handler is converted to `ClientFacingError`, found by a full audit of `raise` sites under `jarvis/` and `sentinel/` reachable from the handlers; the list goes into the evidence pack. `ProviderOrchestrator`'s durable audit reason records the exception type and, for a `ProviderError`, whether it was transient (for example "Provider execution failed: ProviderError (transient)") - no free text, per EBG-0157 item 2 and D23 - while the full message is written to the local rotating `backend.log`, so diagnostic detail is kept (v0.2, design review finding 2). A future user-facing error raised without `ClientFacingError` fails safe: the user sees the generic sentence, never internal detail. Tests: an unexpected exception carrying sensitive-looking text never reaches the reply; each converted message still does.

**5.3 Fast-lane write guard (item 3).** `serve_forever()` routes fast methods through a guarded wrapper too. **Broken output** (`BrokenPipeError` or any `OSError` raised by the write itself) is re-raised and ends the loop cleanly - no reply can ever be delivered, so continuing would only fail again on every line. **Any other exception** while processing a line is logged and the loop continues, as on the slow lane today. (v0.2, design review finding 3: v0.1 said both lanes use the existing logged wrapper, which would swallow a broken pipe.) Tests: a write raising `BrokenPipeError` ends `serve_forever()`; a handler-side failure on a fast method does not.

**5.4 Real-thread slow-lane test (item 4).** A pytest test drives `serve_forever()` with real threads over in-memory pipes: a slow request that blocks on an event, then fast requests, asserting the fast replies arrive first and the slow reply arrives after the event is set; and that closing input still answers the in-flight slow request.

**5.5 Per-profile proposal cap (item 5).** The cap becomes per profile (100 per profile; the oldest of that profile is dropped), so one profile cannot evict another's proposals.

**5.6 Spawn-to-attach race (item 7) - closed by verification, no code change.** v0.1's creation-time check was backwards (a reused PID's process is created *after* the spawn, so it could never be caught - design review finding 4). Verified in source instead: `tauri-plugin-shell` 2.3.5's `CommandChild` holds `Arc<SharedChild>` (`src/process/mod.rs:65-67`), and `shared_child` 1.1.1's `SharedChildInner` holds the `std::process::Child` (`src/lib.rs:86-87`), which owns the Windows process handle from spawn until drop; the dev path holds `std::process::Child` directly. `ProcessGuard::attach` runs while that child is alive (`src-tauri/src/lib.rs:741, 790`), and Windows does not reuse a PID while any handle to it is open - so the race cannot occur. The build re-confirms this in the `tauri-plugin-shell` 2.4.0 source if that update is taken (5.9). EBG-0157 item 7 closes with this evidence.

**5.7 Not Responding check (item 8).** A live manual check, recorded with the build: close the app during a long reply and observe whether the window shows "Not Responding" during the up-to-3-second shutdown. If it does, the wait moves off the main thread in this WP; if not, item 8 closes as verified.

**5.8 Capability (EBG-0149).** `shell:allow-execute` is removed from `capabilities/default.json`. A release build is run to confirm the Rust-side spawn still works and conversation still flows.

**5.9 Dependency settlement and EBG-0158.** Applied in this WP's commit (Dependabot then closes its pull requests as superseded):

| Update | Disposition |
|---|---|
| `tauri-plugin-shell` 2.4.0 (#17), `tauri` 2.12.0 (#26), `@tauri-apps/plugin-shell` 2.3.6 (#19) | **Take**, after EBG-0158's checks: confirm in the 2.4.0 source that dropping `CommandChild` still closes the child's stdin; `cargo test`; the ignored live harness `live_packaged_sidecar_busy_tree_is_ended_within_the_grace` against a rebuilt sidecar; live check that a normal close exits gracefully ("JARVIS backend stopped" in `backend.log`). If stdin no longer closes on drop, keep 2.3.5 and record why |
| `ruff` 0.16.9 (#27), `vite` 8.3.0 (#25), `@playwright/test` 1.63.0 (#21), `lucide-react` 1.45.0 (#24), `pyinstaller` >=6.22.3 (#22) | **Take** - minor/patch updates; full test suites and a frontend build must stay green |
| `react-dom` 19.3.0 (#23) | **Defer** - Programme Sponsor decision D8 (no React 19 before Version 1.0); the pull request is closed with that reason |
| `piper-tts` (#18) | **Defer** - Piper is unregistered (Kokoro is the production voice since ESR-0053); closed with that reason |

After this, dependency updates before Version 1.0 are taken only for security fixes or a confirmed defect (the "freeze" in the plan's WP2 title).

# 6. WP2b - Outline (full design in a later version)

* **Build:** an `aarch64-apple-darwin` sidecar built by `scripts/build_backend_sidecar.py` on GitHub's Apple-Silicon runner (`macos-latest`); consider PyInstaller onedir mode for startup time.
* **Process tree on macOS** - to be designed after verifying, from PyInstaller's documentation and bootloader source: whether onefile mode forks a child interpreter on macOS and forwards signals to it, and whether onedir mode runs the interpreter in the bootloader's own process. Candidate design: own process group plus group kill from the host (`libc::killpg`), and an orphan watchdog in the backend (exit when the parent process changes), so EBG-0154's guarantee holds on the Mac. No macOS process-tree code is written before that check.
* **CI and release:** `macos` jobs for pytest and `cargo test`; a Playwright WebKit project; `.dmg` plus checksum in `release.yml`.
* **Bundle:** `NSMicrophoneUsageDescription`; minimum macOS version; Gatekeeper's one-time "Open Anyway" (D15) documented in WP8.
* **GIA:** macOS process names, or an honest "not applicable".
* **EBG-0054:** a `setup-dev-environment.sh` equivalent for macOS (and Linux).
* **Live check:** Mac visit 1 (week of 20 October 2026).

# 7. Evidence Pack (WP2a, TPL-0001 1.0 Section 6)

| Item | Content |
|---|---|
| API facts | SQLite: WAL is persistent per database file and allows concurrent readers with one writer; `busy_timeout` is per connection (sqlite.org/wal.html, sqlite.org/pragma.html). Python `sqlite3.connect(timeout=5.0)` default. `GetProcessTimes` returns the creation time as a FILETIME (Win32 docs). `tauri-plugin-shell` 2.4.0 `CommandChild` stdin-on-drop - **to be verified in source during the build** (EBG-0158). |
| Platform coverage | 5.1-5.5 are pure Python, identical on Windows and macOS. 5.6 is Windows-only code (macOS gets its own guard in WP2b). 5.8 applies to all platforms. |
| CI | Existing jobs (python, rust, rust-windows, frontend-build, playwright) run every change; no workflow change in WP2a. The Linux check is also run locally in Docker before commit (lesson from CI run 37448647822). |
| Tests | New: SQLite concurrent threads; `ClientFacingError` reply and audit tests; fast-lane broken pipe ends the loop, handler failure does not; real-thread slow lane; per-profile cap. (No Rust change for item 7.) Existing suites must stay green, including the job-object tests and the ignored live harness for EBG-0158. |
| New dependencies and features | None for the hardening (item 7 needs no code). The dependency updates in 5.9 are listed there. No new OS permission. |

# 8. Commit Contents (WP2a, final, as built)

New: `jarvis/shared/errors.py`, `jarvis/tests/test_sqlite_concurrency.py`.

Changed: `jarvis/agents/contracts.py`, `jarvis/shared/schema_migrations.py`, `jarvis/memory/store.py`, `jarvis/memory/service.py`, `jarvis/identity/store.py`, `jarvis/identity/service.py`, `jarvis/guardian/runtime.py`, `jarvis/repository.py`, `jarvis/interfaces/stdio_rpc.py`, `sentinel/orchestrator.py`, `jarvis/tests/test_stdio_rpc.py`, `jarvis/tests/test_audit_and_logging.py`, `jarvis/tests/test_sentinel_orchestrator.py`, `src-tauri/capabilities/default.json`, `src-tauri/Cargo.lock`, `package.json`, `package-lock.json`, `pyproject.toml`, `aiems/governance/reviews/EIP-ESR0061-002_PLATFORM_HARDENING_AND_MACOS.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`.

Not changed (the design listed them; the build did not need them): `jarvis/identity/` and `src-tauri/src/lib.rs` carry no item-7 code, and `src-tauri/Cargo.toml` needed no edit - its version requirements (`"2"`) already admit the updates, which `Cargo.lock` records.

# 8A. WP2a Build Record (6 October 2026)

| Item | Result |
|---|---|
| 5.1 SQLite | `jarvis/shared/schema_migrations.connect()` sets an explicit 5-second busy timeout on every connection; `apply_migrations()` puts each store in WAL mode after migrating. Both stores use it; nothing else opens SQLite, and nothing copies a database file (searched). New `jarvis/tests/test_sqlite_concurrency.py`: WAL on both stores, the busy timeout, a reader not blocked by an open write transaction, and three real threads reading and writing 200 rows each with no lock errors. |
| 5.2 Error replies | `jarvis/shared/errors.py`: `ClientFacingError` plus `ClientFacing{Type,Value,Key,Permission,Runtime}Error`, each also subclassing the builtin it replaces, so existing `except` clauses behave as before. A reply names the builtin type (`TypeError: ...`), so the text the UI shows is unchanged. Converted, found by running the suite (each conversion fixed a failing test): all 23 raises in `stdio_rpc.py` (parameter and role errors), the user-facing raises in `memory/service.py`, `memory/store.py`'s restore validation, `identity/service.py`, `identity/store.py`, `guardian/runtime.py`'s "not running" and "no memory service", and `RepositoryUnavailableError` (keeps its own name). **Privacy defect found and fixed:** two restore-validation messages embedded the whole backup row (`{row!r}`) and a third the field value - memory *content* - in text shown to the UI; they now name the missing fields or the value's type. **Deviation from the reviewed design, stricter, disclosed:** for an unexpected exception `backend.log` records the type and where it was raised (`file:line in function`), never the message, because a message built from user data would otherwise put conversation or memory content in the log (D23); the orchestrator's provider-failure message is still logged, as reviewed (adapter messages carry no content). The durable audit reason is now e.g. "Provider execution failed: ProviderError (transient)". |
| 5.3 Fast lane | **Correction to Section 4:** handler failures were already caught by `handle_line()`, and a broken pipe already ended the loop; the real gap was a failure while *producing or writing* a reply (shown with a result JSON cannot serialise), which ended the backend on the fast lane. `_process_line_guarded()` logs it and continues; `OSError` from the write still ends the loop. Tests: the unserialisable-reply case (failed on the old code) and the broken pipe. |
| 5.4 Real threads | New deterministic test, no sleeps: a slow conversation turn reads the memory store continuously on the worker thread while the main thread proposes and approves ten memories in the same file; released only once those writes are answered. Passes repeatedly (6 runs). |
| 5.5 Cap | Per profile; test shows 105 proposals from one profile no longer evict another's. |
| 5.6 Item 7 | No code (verification in 5.6). Re-confirmed in `tauri-plugin-shell` **2.4.0** source: `CommandChild` still holds `Arc<SharedChild>` and the only `stdin_writer` (`src/process/mod.rs:65-67, 310, 363`); `shared_child` stays 1.1.1. |
| 5.7 Item 8 | **Closed by reasoning:** Windows marks a window "Not Responding" only after it has not processed messages for 5 seconds (`IsHungAppWindow`), and the exit wait is bounded at about 3 seconds - so it cannot show. The Programme Sponsor may still try it (close during a long reply). |
| 5.8 Capability | `shell:allow-execute` removed. Release build (`tauri build --no-bundle`) started its backend normally (the Rust-side spawn is not governed by capabilities). |
| 5.9 Dependencies | Rust: `tauri-plugin-shell` 2.4.0, `tauri` 2.12.0 (with their transitive updates, e.g. `wry` 0.57). npm: `@tauri-apps/plugin-shell` ^2.4.0, `lucide-react` ^1.52.0, `@playwright/test` ^1.63.0, `vite` ^8.3.3 - **newer than Dependabot's proposals** (npm resolved the latest matching versions; the JS shell plugin now matches the Rust 2.4.0). Python: `ruff==0.16.9` (no new findings), `pyinstaller>=6.22.3`. **Security fix:** `npm audit fix` updated the transitive dev dependency `source-map-js` (GHSA-68fv-2mgg-jv7q, high, already present before these updates); `npm audit` now reports 0. Deferred: `react-dom` 19 (D8), `piper-tts`. New harmless warning from `tauri-build` 2.12: "STATIC_VCRUNTIME is deprecated" - nothing in the repository sets it. |
| EBG-0158 live checks | Ignored harness against a rebuilt sidecar: busy packaged backend, 2 processes in its job, ended in **3.05 s**. Release app, normal close: both backend processes gone in **640 ms**, "JARVIS backend stopped" logged (graceful). Release app force-killed: tree gone in **66 ms**. |
| Review follow-up | The implementation review (Section 10) asked whether any user-reachable message is now hidden behind the generic sentence. Checked: chat provider failures are caught in `sentinel_conversation.py` and answered with the honest "could not reach an AI provider" reply, so users never see the generic sentence there; agent "not connected/running" cases are returned as outcomes, not raised. One reachable validation was found and converted: a blank `task` to `guardian.agent.invoke` (`jarvis/agents/contracts.py`), with a test shown failing without the conversion. The remaining plain `ValueError`s are internal constructor validation the UI does not trigger. |
| Validation | pytest **865 passed, 1 skipped**; cargo test 19 passed (+1 ignored, run live); clippy `-D warnings` clean; `cargo fmt` clean; ruff clean; Playwright **26/26**; frontend build clean; validator 0 errors. |

# 9. Questions for the Engineering Reviewer

1. Is WAL plus an explicit busy timeout the right fix for item 1, and is the backup/restore checkpoint concern real?
2. Is `ClientFacingError` the right shape for item 2, given the UI shows messages? Is anything lost?
3. Is the verification closing item 7 (handle held from spawn) sound?
4. Is the dependency settlement sound, including applying updates in a gated commit rather than merging Dependabot's pull requests?
5. Is the WP2a/WP2b split sound, and is it right to hold the macOS process-tree design until PyInstaller's behaviour is verified?

# 10. Review Record

**v0.1 design review** (Antigravity CLI, Gemini 3.1 Pro, through `run_reviewer.py`; 2026-10-06T12:5xZ, `sender: reviewer`): **Fail**.

| # | Finding | Engineering Implementer assessment | Disposition in v0.2 |
|---|---|---|---|
| 1 (High) | The backup checkpoint concern is not real: backup/restore are logical JSON export/import | **Correct** (verified, `store.py:289, 339`); a superfluous step rather than a defect, so High overstates it | Step removed (5.1) |
| 2 (High) | Type-only audit reason destroys diagnostic value; a raise-site audit is brittle | **Partly accepted.** EBG-0157 item 2 and D23 keep free text out of the durable audit, but diagnostics move to the local `backend.log`, and the transient flag is kept. A forgotten wrapper fails safe (generic message), so the brittleness is Low | 5.2 revised |
| 3 (Medium) | Using the logged wrapper for fast methods would swallow a broken pipe and loop | **Correct** - v0.1 contradicted itself | 5.3 specifies pipe errors end the loop, other failures are logged |
| 4 (High) | The creation-time check is backwards, and the race cannot occur because the child's handle is held | **Correct on both counts** - verified in the plugin and `shared_child` source | 5.6 replaced by verification; no code for item 7 |
| 5, 6 | Capability removal and gated dependency updates are sound; the WP2a/WP2b split and the PyInstaller check first are right | Agreed | None |

**v0.2 design re-review** (Antigravity CLI, Gemini 3.1 Pro, fresh conversation; 2026-10-06T12:58Z, `sender: reviewer`): **Pass**, information-only. Confirmed nothing copies the database file; provider exception messages carry generic errors or HTTP status, never conversation text, so `backend.log` keeps D23; 5.3 correct and testable. On item 7 it **could not read the cargo registry** (outside its read permission) and judged the reasoning sound; the source verification in 5.6 is the Engineering Implementer's own. Two resumes: `sed -n` (refused - `sed` can write; used the file viewer instead) and an attempt to read the cargo registry (outside scope).


**WP2a implementation review** (Antigravity CLI, Gemini 3.1 Pro, through `run_reviewer.py`; 2026-10-06T14:0xZ, `sender: reviewer`; the only independent reviewer, by Programme Sponsor decision): **Pass**, information-only, and no resume needed. It re-ran pytest, ruff and the validator; judged the connection helper, WAL, the fast-lane split, the per-profile cap (including no profile), the real-thread test (deterministic), the capability removal and the stricter logging sound; and confirmed no other SQLite path or database copy exists. **Its one substantive note** - that provider exhaustion "now becomes a generic Guardian internal error" - was checked by the Engineering Implementer and does not hold for chat (see the review follow-up in 8A), but it led to finding and fixing the blank-task message. **Caveats, disclosed:** the review is brief and entirely affirmative with a single reviewer; it could not read the Rust lock-file effects or the cargo registry; and the live checks, the Rust tests and the Linux run (Docker `python:3.12-slim` with Tk and git added, run on the exact final tree, matching CI's steps: ruff clean, version sync, pytest 866 passed with the Tk test that Windows skips, validator 0 errors; `pip-audit` flags only `pip` itself, the known PYSEC-2026-3721, because CI's upgrade-pip step was skipped in the container) are the Engineering Implementer's own.

# 11. Version History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.4 | 6 October 2026 | Claude Engineering Implementer | WP2a implementation review Pass (Gemini only); its one note checked, which led to converting a blank agent-task error; Linux CI steps run in Docker on the final tree (866 passed). Commit contents now include jarvis/agents/contracts.py. Awaiting Programme Sponsor approval of the built result. |
| 0.3 | 6 October 2026 | Claude Engineering Implementer | WP2a design approved (Programme Sponsor, chat) and built; build record 8A: privacy defect found and fixed (restore errors echoed memory content), fast-lane gap corrected, logging stricter than designed (type and location, never the message), item 8 closed by reasoning, live EBG-0158 checks pass, 0 npm vulnerabilities. Final commit contents fixed (Section 8). Awaiting implementation review. |
| 0.2 | 6 October 2026 | Claude Engineering Implementer | WP2a design review Fail (Gemini): backup checkpoint step removed (backups are logical); audit keeps type and transient flag, full message to backend.log; fast-lane broken pipe ends the loop; PID-reuse check removed - the race is impossible while the child's handle is held, verified in source. Awaiting re-review. |
| 0.1 | 6 October 2026 | Claude Engineering Implementer | Initial draft: WP2 split into WP2a (shared hardening and dependency settlement, full design) and WP2b (macOS, outline pending PyInstaller verification). Programme Sponsor override of D19 for WP2 recorded (Gemini-only review). |
