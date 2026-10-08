# EIP-ESR0061-002 - Platform Hardening and macOS

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0061-002 |
| Title | Engineering Implementation Package: WP2 Platform Hardening and macOS |
| Version | 0.13 |
| Status | Draft - WP2a, WP2a-fix and WP2b committed (post-commit reviews Pass; WP2b real-Mac checks at Mac visit 1); WP2c follow-ups built, implementation review Pass, awaiting Programme Sponsor approval of the built result |
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

# 6. WP2b - Design (macOS, EBG-0162, and non-Windows setup, EBG-0054)

Risk class: **High-risk** (process lifecycle, new platform, release pipeline). Reviewed by Antigravity alone under the D19 override for WP2. Real macOS testing is **Mac visit 1** (week of 20 October 2026); everything below is built and tested on CI's `macos-latest` (Apple Silicon) runner first.

**6.1 PyInstaller on macOS - verified, not assumed** (bootloader source `v6.22.3`, `bootloader/src/pyi_utils_posix.c` and `pyi_main.c`; the project pins `pyinstaller>=6.22.3` since WP2a).

| Fact | Evidence | Consequence |
|---|---|---|
| **Onefile keeps a resident parent.** The bootloader extracts to `_MEI*`, then `fork()`s a child that runs the program (`pyi_utils_create_child`, `child_pid = fork()`); the parent waits and cleans up. macOS is not an exception. | `pyi_utils_posix.c` around the `fork()` call; `pyi_main.c` `_pyi_main_onefile_parent()` | The backend is **two processes** on macOS, as on Windows (EBG-0154's finding). |
| **The parent forwards signals; it cannot forward SIGKILL.** `_signal_handler()` does `kill(child_pid, signum)` for every catchable signal except `SIGCHLD`/`SIGTSTP`. | `_signal_handler`, and the loop that installs it | A host `SIGTERM` to the parent reaches the Python child. A host `SIGKILL` of the parent does not: the child is **orphaned**. |
| **No process group or session is created.** The source has no `setpgid`, `setsid` or `PDEATHSIG` (macOS has no `PDEATHSIG` at all). | grep of `pyi_utils_posix.c` | The child shares the parent's group, so a **group kill from the host reaches both** - if the host made the parent a group leader. |
| **Re-raise after cleanup.** If the child dies from a signal, the parent cleans `_MEI*` then re-raises it. | `child_signalled` / `raise(child_signal)` | A graceful stop leaves no temp directory behind. |
| **Onedir does not fork on macOS** (the `execvp` restart is Linux-only); Python runs in the bootloader's own process. | `pyi_main.c` | Onedir would be one process, but Tauri's `externalBin` ships a single file, so onedir needs the bundle `resources` route and per-dylib signing. **Decision: keep onefile on macOS, as on Windows** (one build recipe, one code path). Startup time is measured on Mac visit 1; onedir is a fallback only if it is too slow. |

**6.2 Host side: own process group, group kill** (`src-tauri/src/lib.rs`). The existing `#[cfg(not(windows))]` stubs for `ProcessTree` and `ProcessHandle` (lib.rs:401-444) become a real Unix implementation.

* **Spawn.** `tauri-plugin-shell` starts the sidecar with `std::process::Command` but exposes no hook to set the process group, and `setpgid` on a child that has already `exec`ed fails (`EACCES`), so the group cannot be set after the fact. On Unix the sidecar is therefore spawned directly with `std::process::Command` and `CommandExt::process_group(0)`, the way the development backend already is (`spawn_dev_backend`), reusing `run_dev_reader`. The sidecar path is resolved beside the application executable (Tauri's `externalBin` places it there, name without the target triple). Windows keeps the plugin path unchanged. The dev backend also gets `process_group(0)`.
* **Guard.** `ProcessTree::adopt(pid)` records the group (`pgid == pid`). `is_empty()` is `killpg(pgid, 0)` returning `ESRCH`. `terminate()` is `killpg(pgid, SIGKILL)`. `ProcessHandle` waits on the direct child. The graceful sequence is unchanged: close stdin, wait the grace period, then force the group. The host keeps the `Child` handle from spawn, so the PID-reuse reasoning of 5.6 holds on macOS too (`killpg` is only called while the leader is still unreaped, and `reap()` runs after).
* **Dependency.** `libc` as a `cfg(unix)` dependency (a crate already in the lockfile transitively; direct use is the only addition).

**6.3 Backend side: orphan watchdog** (`jarvis/interfaces/`, new small module, wired in `jarvis_backend_entry.py`). A host `SIGKILL` (or crash) cannot reach a busy backend: stdin EOF is only seen when the read loop runs. The host passes its PID (`JARVIS_HOST_PID`); a daemon thread checks every second that the host process exists (`os.kill(pid, 0)`); if it is gone, it logs "host gone" and ends the process with `os._exit(1)`. The bootloader parent then sees its child exit, cleans `_MEI*` and exits, so nothing is left. Watching the host's PID, not `getppid()`, is deliberate: under onefile the Python process's parent is the bootloader, not the host. Active only when `JARVIS_HOST_PID` is set, on every platform (harmless on Windows, where the job object already covers it). Tests: the watchdog ends a helper process when its "host" PID dies; it does nothing when the variable is absent or the host is alive.

**6.4 Build.** `scripts/build_backend_sidecar.py` already reads the host triple from `rustc -vV` and builds extension-less on non-Windows; WP2b adds a test for the `aarch64-apple-darwin` name and confirms the produced file is executable and ad-hoc signed (PyInstaller signs arm64 output ad hoc; an unsigned arm64 binary will not run). No change to the PyInstaller options is expected; a hidden-import or data-file gap found on the macOS runner is fixed in this WP.

**6.5 CI and release.**
* `ci.yml`: a `python-macos` job (`macos-latest`: ruff, pytest, validator) and a `rust-macos` job (clippy `-D warnings`, `cargo test` including the new Unix guard tests: spawn a process tree in a group, `killpg`, assert empty).
* Playwright: add a **WebKit** project to `playwright.config.js` (`devices["Desktop Safari"]`), run on the macOS runner (WKWebView is WebKit; this is the closest CI proxy for Mac visit 1, and the first check of UAM-0001's "one look on both engines" goal).
* `release.yml`: a macOS job builds the `.dmg` for `aarch64-apple-darwin` and publishes it with a SHA-256 checksum beside the Windows installer.

**6.6 Bundle** (`src-tauri/tauri.macos.conf.json`, merged on macOS; `tauri.conf.json` keeps `"targets": ["nsis"]` for Windows). `bundle.targets: ["app", "dmg"]`; `bundle.macOS.minimumSystemVersion` (proposed `13.0`, to be confirmed against the Mac visit machine and the Tahoe 26 target) and an `Info.plist` with `NSMicrophoneUsageDescription` (push-to-talk voice, EBG-0112). Signing: ad hoc (`signingIdentity: "-"`), no Apple Developer account, no notarisation; the user-facing one-time "Open Anyway" step (D15) is documented in WP8. **A Programme Sponsor cost decision, if ever wanted: notarisation needs the US$99/year Apple Developer Program; not proposed (no discretionary budget).**

**6.7 GIA.** `jarvis/gia/observability.py` maps tools to Windows process names (`Code.exe`...). macOS equivalents are not guessed: the map becomes per-platform, macOS entries are added only if verified on Mac visit 1, and until then GIA reports "not observable on this platform" honestly (a tested path), never a wrong "not running".

**6.8 EBG-0054.** `scripts/setup-dev-environment.sh`, a bash equivalent of `setup-dev-environment.ps1` for macOS and Linux (checks Node, Rust, Python 3.12, creates the venv, `npm install`, editable install, hook activation, runs the validator and tests), idempotent, with a `--doctor` flag that only reports. Tested by shellcheck in CI (`apt`/preinstalled on `ubuntu-latest`) and run for real on the macOS runner.

**6.9 Tooling touch (follow-up from WP2a-fix, reviewer Info).** `scripts/post_commit_precheck.py`: a bold-label block ends at the next bold label as well as the next heading. This EIP's own commit list sits under its own heading (13.1) meanwhile.

**6.10 What is not tested until Mac visit 1.** Real `killpg` on a running packaged backend; `_MEI*` cleanup after SIGKILL and SIGTERM on a Mac; sidecar startup time; the `.dmg` install and first launch past Gatekeeper; microphone permission prompt; WKWebView look; GIA macOS process names. WP2b closes as "built, CI-verified on macOS runner" and these are the Mac visit 1 checklist, recorded in the session report.

**6.11 Questions for the Engineering Reviewer.**
1. Is spawning the sidecar through `std::process::Command` on Unix (instead of the plugin) the right way to get a process group, given `setpgid` after `exec` fails?
2. Is the watchdog watching the host PID the right choice under onefile, and is a 1-second poll plus `os._exit(1)` acceptable?
3. Is keeping onefile on macOS sound, given the two-process tree is now handled?
4. Is ad-hoc signing with documented "Open Anyway" adequate for Version 1.0 under D15?

---

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
| 0.13 | 8 October 2026 | Claude Engineering Implementer | WP2c implementation review Pass (Gemini, Info only); Linux Docker run on the final tree 890 passed. Awaiting approval of the built result. |
| 0.12 | 8 October 2026 | Claude Engineering Implementer | WP2a-fix and WP2b post-commit reviews recorded (Pass); CI result for `dd946a2`; Section 16 (WP2c): the three queued follow-ups (WebKit job installs Chromium, pre-check recognises `.plist` and a "Differences" paragraph, record trail) built. |
| 0.11 | 8 October 2026 | Claude Engineering Implementer | WP2b re-review Pass (Gemini, all Info) after the two fixes; Section 15 completed. Linux full run on the final tree recorded in Section 14. Awaiting Programme Sponsor approval of the built result. |
| 0.10 | 8 October 2026 | Claude Engineering Implementer | WP2b implementation review Fail (Gemini: 1 High, 1 Medium, 3 Info); both fixed (setup script no longer uses `sort -V`; smoke test checks the backend is alive before the host is killed); the Windows `os.kill(pid, 0)` wording corrected after checking; Section 15 review record. Awaiting re-review. |
| 0.9 | 8 October 2026 | Claude Engineering Implementer | WP2b design review Pass (Gemini, all Info) and approved by the Programme Sponsor (chat); built. Section 14 build record: Unix process-group guard, orphan watchdog (POSIX-only - corrected from the design), real-sidecar smoke test (not in the design), macOS CI and release jobs, bundle config, GIA, setup script, pre-check fix. Section 13 commit contents finalised. Awaiting implementation review. |
| 0.8 | 8 October 2026 | Claude Engineering Implementer | WP2b full design (Section 6): PyInstaller macOS behaviour verified in bootloader source (onefile = resident parent plus forked child, signals forwarded, no process group, SIGKILL orphans the child); Unix process-group guard, backend orphan watchdog, macOS CI/release/bundle/GIA/setup script, Mac visit 1 checklist; Section 13 commit contents. Awaiting design review. |
| 0.7 | 8 October 2026 | Claude Engineering Implementer | WP2a-fix design approved (Programme Sponsor, chat), built; implementation review Pass (Gemini); Linux Docker run 871 passed. Awaiting approval of the built result. |
| 0.6 | 8 October 2026 | Claude Engineering Implementer | WP2a-fix design review Conditional Pass (Gemini): "Not changed" cut now applies only after the first listed path; two tests added (12.1, 12.2, 12.6). Awaiting Programme Sponsor design approval. |
| 0.5 | 8 October 2026 | Claude Engineering Implementer | Added Section 12, WP2a-fix: three defects in `scripts/post_commit_precheck.py` found by its first code-commit run and confirmed by the WP2a post-commit review (Pass, Info). Design awaiting review. WP2a post-commit review Pass recorded. |
| 0.4 | 6 October 2026 | Claude Engineering Implementer | WP2a implementation review Pass (Gemini only); its one note checked, which led to converting a blank agent-task error; Linux CI steps run in Docker on the final tree (866 passed). Commit contents now include jarvis/agents/contracts.py. Awaiting Programme Sponsor approval of the built result. |
| 0.3 | 6 October 2026 | Claude Engineering Implementer | WP2a design approved (Programme Sponsor, chat) and built; build record 8A: privacy defect found and fixed (restore errors echoed memory content), fast-lane gap corrected, logging stricter than designed (type and location, never the message), item 8 closed by reasoning, live EBG-0158 checks pass, 0 npm vulnerabilities. Final commit contents fixed (Section 8). Awaiting implementation review. |
| 0.2 | 6 October 2026 | Claude Engineering Implementer | WP2a design review Fail (Gemini): backup checkpoint step removed (backups are logical); audit keeps type and transient flag, full message to backend.log; fast-lane broken pipe ends the loop; PID-reuse check removed - the race is impossible while the child's handle is held, verified in source. Awaiting re-review. |
| 0.1 | 6 October 2026 | Claude Engineering Implementer | Initial draft: WP2 split into WP2a (shared hardening and dependency settlement, full design) and WP2b (macOS, outline pending PyInstaller verification). Programme Sponsor override of D19 for WP2 recorded (Gemini-only review). |

# 12. WP2a-fix - Post-Commit Pre-Check Defects

Found on the pre-check's first code-commit run (WP2a, `b14c6a0`) and agreed by the WP2a post-commit review (Antigravity, Pass, Info finding). The commit was correct; the script was wrong. Risk class: low (a read-only reporting script), reviewed by Antigravity under the D19 override for WP2.

**12.1 Defects and fixes** (all in `scripts/post_commit_precheck.py`)

| # | Defect | Fix |
|---|---|---|
| 1 | `_PATH_TOKEN` omits `.lock`, so `src-tauri/Cargo.lock` reads as unlisted. | Add `lock`, `sh`, `ps1`, `bat`, `html`, `css` to the extension list, so WP2b's setup script and bundle files are recognised too. |
| 2 | `eip_commit_contents` reads the whole block, including a "Not changed" paragraph, so paths the design listed but the build did not change count as listed. | End the list at the first line that starts with "Not changed" **and comes after at least one listed path** (v0.6, design review finding 2: a leading "Not changed" line must not empty the list). From WP2b on, EIPs put "Not changed" under its own heading, which the parser already excludes; the line rule only keeps existing EIPs such as Section 8 working. |
| 3 | `advisory_figures` compares every "N passed" or "N skipped" in the commit message with pytest's count, so cargo's "19 passed" and the Linux "866 passed" are flagged wrongly. | Compare only a figure that follows the word "pytest" within the same clause. Unlabelled figures are not compared, and the advisory line says how many were left out. |

**12.2 Tests** (`scripts/tests/test_post_commit_precheck.py`): a `Cargo.lock` path is parsed; a "Not changed" paragraph is excluded; a cargo or Linux figure raises no advisory; a pytest-labelled mismatch still does; a block with no "Not changed" paragraph is read whole; a "Not changed" line before the first path does not truncate the list; a message with counts but no "pytest" word raises no advisory.

**12.3 Evidence pack.** No new dependency, OS permission, feature or CI change. Platform coverage: pure Python, identical on Windows and Linux; the Linux check runs in Docker before the commit. Re-running the pre-check on `b14c6a0` after the fix must give PASS.

**12.4 Commit contents (expected).** Changed: `scripts/post_commit_precheck.py`, `scripts/tests/test_post_commit_precheck.py`, `aiems/governance/reviews/EIP-ESR0061-002_PLATFORM_HARDENING_AND_MACOS.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`.

**12.5 Questions for the Engineering Reviewer.** Is ending the block at "Not changed" robust enough, or should the list carry an explicit end marker? Is comparing only "pytest"-labelled figures the right balance between noise and missed mismatches?

**12.6 Design review record** (Antigravity CLI, Gemini, through `run_reviewer.py`; 2026-10-08T08:2xZ, `sender: reviewer`): **Conditional Pass**. (1, Info) the three fixes address the defects and work on Section 8's real text. (2, Medium) truncating at the first "Not changed" line is brittle if that line precedes the list - **accepted**, fixed as above; it also suggested a separate heading, adopted as the convention for new EIPs. Q2: pytest-labelled comparison is the right balance for an advisory check. (3, Info) edge cases: a message without "pytest" skips the comparison, acceptable for an advisory. (4, Low) two extra tests - **accepted** (12.2).

**12.7 Implementation review** (Antigravity CLI, Gemini, through `run_reviewer.py`; 2026-10-08T08:4xZ, `sender: reviewer`): **Pass**, all Info. The three fixes are as designed including the accepted finding; the tests listed in 12.2 are present and pass; `eip_commit_contents` on Section 8 matches the 24 files of `b14c6a0` and no false advisory lines remain; no regressions. Two resumes: `python -m pytest` with the path before `-q` (refused; the allow-list wants `-q` first) and `git show --format` with escaped quotes (refused). **Engineering Implementer's own evidence:** the Linux run in `python:3.12-slim` (ruff clean, version sync, pytest 871 passed, validator 0 errors) and the real-data check of the fixed functions against `b14c6a0`.

# 13. WP2b Commit Contents (as built)

New: `jarvis/interfaces/orphan_watchdog.py`, `jarvis/tests/test_orphan_watchdog.py`, `scripts/setup-dev-environment.sh`, `scripts/smoke_unix_sidecar.py`, `scripts/tests/test_build_backend_sidecar.py`, `src-tauri/Info.plist`, `src-tauri/tauri.macos.conf.json`. Changed: `.github/workflows/ci.yml`, `.github/workflows/release.yml`, `jarvis/gia/observability.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/tests/test_gia_observability.py`, `playwright.config.js`, `scripts/post_commit_precheck.py`, `scripts/tests/test_post_commit_precheck.py`, `src-tauri/Cargo.lock`, `src-tauri/Cargo.toml`, `src-tauri/src/lib.rs`, `aiems/governance/reviews/EIP-ESR0061-002_PLATFORM_HARDENING_AND_MACOS.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`.

Differences from the design-time estimate: `scripts/jarvis_backend_entry.py` is not changed (the watchdog starts in `stdio_rpc.run()`, which serves both the dev and the packaged backend); `jarvis/gia/observability.py` and its test are added; `scripts/smoke_unix_sidecar.py` is new; the `.sh` setup script is committed with the executable bit.

# 14. WP2b Build Record (8 October 2026)

| Item | Result |
|---|---|
| 6.2 Host | `src-tauri/src/lib.rs`: the dev spawn became `spawn_child_backend()`, shared with the new `spawn_unix_sidecar_backend()` (path: beside the executable, plain name). On Unix it sets `process_group(0)` and `JARVIS_HOST_PID`; the Windows plugin path also passes `JARVIS_HOST_PID`. The `cfg(not(windows))` stub is now a real `cfg(unix)` `process_tree` (`adopt` refuses a process that does not lead its own group, so the host's group can never be killed by mistake; `is_empty` is `killpg(0)` returning `ESRCH`; `terminate` is `killpg(SIGKILL)`), with a stub left only for platforms that are neither. `libc` is now a direct `cfg(unix)` dependency (already in the lockfile). **One change to shared logic:** `ProcessGuard::wait_until` now calls the child-exited closure first for its side effect (`try_wait` reaps the leader), because an unreaped zombie leader keeps its group non-empty on Unix; the tree still decides, so Windows behaviour is unchanged. |
| 6.3 Watchdog | `jarvis/interfaces/orphan_watchdog.py`, started from `stdio_rpc.run()`. **Correction to the design:** it is POSIX-only and does nothing on Windows - the design said it was "harmless on Windows", but signal 0 is `CTRL_C_EVENT` on Windows (`signal.CTRL_C_EVENT == 0`), so `os.kill(pid, 0)` there sends a Ctrl+C to a console process group instead of testing for existence. (v0.9 first said `TerminateProcess`; the reviewer disputed that and claimed an existence check, which is also wrong - corrected here after checking.) Tests cover that guard, an unusable PID, the exit and no-exit cases, and a real process killed when its real host is killed. |
| 6.4 Build | `scripts/tests/test_build_backend_sidecar.py`: the `aarch64-apple-darwin` name has no suffix, the executable bit survives the copy, Windows keeps `.exe`, a missing artefact is an error. No PyInstaller option changed. |
| 6.5 CI and release | `ci.yml`: `python-macos`, `rust-macos` (builds the real sidecar, runs the smoke test, clippy, fmt, `cargo test`, bundles the app and checks `Info.plist`, the minimum version and the sidecar in `Contents/MacOS`), `playwright-webkit`. All three run on pushes to main and manual runs only (macOS minutes cost more, as for `rust-windows`). **Deviation, disclosed:** `playwright-webkit` is `continue-on-error` - the suite was written against Chromium, so WebKit-only failures are expected to need triage; WP4 (UI redesign, "one look on both webviews") makes it blocking. WebKit is opt-in through `PW_WEBKIT=1` so the existing jobs are unchanged. `release.yml`: `release-macos` builds the `.dmg`, runs the smoke test, writes a SHA-256 beside it and publishes to the same release (portable shell: macOS's bash is 3.2, no `mapfile`). |
| 6.6 Bundle | `tauri.macos.conf.json` (`app` and `dmg`, minimum macOS 13.0 - approved by the Programme Sponsor with the design - and ad-hoc signing) and `Info.plist` (`NSMicrophoneUsageDescription`). `tauri.conf.json` is unchanged, so Windows still builds only NSIS. |
| 6.7 GIA | `engineering_tools_for()` returns the Windows process names on Windows and an empty map elsewhere, so a Mac reports "no tools observable" instead of every tool "not running". `LocalResourceObserver` takes the map as an optional argument; existing tests pass it explicitly. |
| 6.8 Setup script | `scripts/setup-dev-environment.sh` with `--doctor` (reports only) and Node 18 / Python 3.12 minimums, compared in plain bash arithmetic (not `sort -V`; review finding 1). shellcheck clean; `--doctor` exercised in Linux (correctly reports npm and cargo missing there). |
| 6.9 Pre-check | `post_commit_precheck.py`: a bold-label block now ends at the next bold label; test added. |
| **Not in the design - added** | `scripts/smoke_unix_sidecar.py`, run by `rust-macos` and `release-macos`: with the real built sidecar it checks a `platform.status` answer, that graceful stop ends the tree and leaves no `_MEI*` directory, that a force-killed host's backend (stdin held open, so only the watchdog can end it) ends its whole tree with no `_MEI*` left, and that a group kill ends the tree. |
| Linux evidence (Docker) | **Real PyInstaller 6.22 onefile sidecar built in `python:3.12-slim` and the smoke test passed with `--expect-tree`: the group held 2 processes** (bootloader plus forked interpreter - confirming 6.1 on a real binary), the answer came back, graceful stop and the orphan case both ended the whole tree with no `_MEI*` left, group kill ended it. Rust (`rust:1` with Tauri's Linux packages): `cargo fmt --check`, `clippy --tests -D warnings` clean, `cargo test` 15 passed including the 3 new process-group tests. Python: ruff clean, version sync, pytest **888 passed**, validator 0 errors, shellcheck clean. |
| Windows evidence | pytest **884 passed, 4 skipped** (POSIX-only tests skip), ruff clean, validator 0 errors (303 warnings, unchanged), `cargo test` 19 passed (+1 ignored), `cargo fmt --check` and clippy `-D warnings` clean, Playwright 26/26. The ignored live harness for the Windows job object was not re-run: only the order of two calls inside `wait_until` changed there, covered by the existing shutdown tests. |
| **Not verified, and why** | Everything in 6.10 needs a real Mac (Mac visit 1). Also unverified: the three new macOS CI jobs and the `release-macos` job have never run (they first run on the push; a failure there is fixed forward and reported), the Tauri spawn path under a real `.app` bundle, and the WebKit results. The Linux run proves the process-group logic and the PyInstaller behaviour on Linux; macOS differs in details (`pgrep -g`, temp paths, signing). |

# 15. WP2b Implementation Review Record

**Review 1** (Antigravity CLI, Gemini, through `run_reviewer.py`; 2026-10-08T10:2xZ, `sender: reviewer`): **Fail**.

| # | Finding | Engineering Implementer assessment | Disposition |
|---|---|---|---|
| 1 (High) | `setup-dev-environment.sh` uses `sort -V`; macOS's older BSD `sort` may not support it, breaking the script on macOS | **Accepted as a precaution.** Whether a given macOS `sort` has `-V` could not be checked here (no Mac), so the dependency is removed rather than argued about | Version comparison rewritten in plain bash arithmetic (bash 3.2 syntax); ten cases checked, shellcheck clean |
| 2 (Medium) | The orphan check in the smoke test could pass if the backend had crashed on its own before the host was killed | **Correct** | The smoke test now asserts the backend is alive and its group non-empty just before the host is killed (and before the group kill) |
| 3 (Info) | The claim that `os.kill(pid, 0)` on Windows calls `TerminateProcess` is incorrect for modern Python; it is an existence check | **Both statements are wrong.** Signal 0 is `CTRL_C_EVENT`; the call sends a Ctrl+C to a console process group. POSIX-only stands | Wording corrected in the EIP, the module docstring and a test comment |
| 4 (Info) | `lib.rs` changes are safe: `wait_until` reaps the zombie leader, `adopt` refuses the host's own group, the Windows fallback is preserved | Agreed | None |
| 5 (Info) | The provided pytest, ruff and validator checks pass; the Docker and Windows evidence could not be reproduced | Stated in Section 14 | None |

**Review 2 - re-review** (Antigravity CLI, Gemini; 2026-10-08T10:4xZ, `sender: reviewer`): **Pass**, all Info. `version_at_least` is plain bash arithmetic valid in bash 3.2 and nothing else in the script is missing on stock macOS; the two new smoke assertions remove the false-pass path and the orphan test is sound; it agreed that signal 0 is `CTRL_C_EVENT` on Windows, so the watchdog stays POSIX-only; its local pytest, ruff and validator runs passed. **Process note, disclosed:** it needed four resumes (refused: `dir`, a `cat` of its own task log, a `cat` with a quoted absolute path) and, once finished, gave its Pass in its reply without recording it; a final resume made it record the verdict, and the Engineering Implementer wrote no reviewer entry. **Caveats:** a single reviewer with no web access; it cannot run any macOS or Docker evidence.

# 16. WP2c - Follow-ups After WP2b

Small, queued at the WP2b post-commit review and announced to the Programme Sponsor on 8 October 2026; no new behaviour. Risk class: low (a CI job, a read-only reporting script, records), reviewed by Antigravity under the D19 override for WP2.

**16.1 Post-commit record, not previously written down.**

| Commit | CI | Post-commit review (Antigravity, Gemini; `sender: reviewer`) |
|---|---|---|
| `65c4100` WP2a-fix | run 37753668213: all five jobs passed | **Pass**, Info. Noted the commit message said four new tests when five were added; not amended (pushed), disclosed here |
| `dd946a2` WP2b | run 37765878232: `python`, `rust`, `frontend-build`, `playwright`, `rust-windows`, **`python-macos`** and **`rust-macos`** passed; `playwright-webkit` (informational) failed | **Pass**, Info. Confirmed the 22 files match Section 13, the script is mode 100755, and the pre-check FAIL (`.plist` unknown to the extension list; the "Differences" paragraph read as part of the list) is a script defect, not a commit defect. One resume (`git ls-tree` is not on its allow-list) |

`rust-macos` was the first run on a real Apple-Silicon runner: the real packaged sidecar was a tree of two processes, all nine smoke checks passed (graceful stop, force-killed host, group kill, no `_MEI*` left), 15 cargo tests passed, and the `.app` bundle carried `NSMicrophoneUsageDescription` and minimum macOS 13.0. `playwright-webkit` ran **no test**: it installed only WebKit, but `tests/e2e/global-setup.js` launches Chromium to warm Vite, so it failed before the first test.

**16.2 Changes.**
* `.github/workflows/ci.yml`: `playwright-webkit` installs Chromium as well as WebKit, so the WebKit project actually runs. It stays `continue-on-error` until WP4.
* `scripts/post_commit_precheck.py`: `plist`, `ini`, `cfg` and `xml` join the path extensions; a paragraph starting "Differences" ends the list exactly as "Not changed" does. Tests added. Re-run on `dd946a2` with Section 13, the file lists now match (they did not before).
* Records: this section, ESR-0061, REG-0001, and the WP3 design EIP-ESR0061-003 v0.3 (a new file, committed here because it is the approved design the next work package builds from).

**16.3 Not verified.** The corrected job has not run; it first runs on the push, and any WebKit failures it then reveals are findings for WP4, not defects in this change.

**16.4 Implementation review** (Antigravity CLI, Gemini; 2026-10-08T12:1xZ, `sender: reviewer`, no resumes): **Pass**. Confirmed Chromium is needed by the global setup, the job stays `continue-on-error`, the 16.1 statements match git and the bridge transcripts, and the Section 17 list equals `git status`. One Info: the "Differences" rule would truncate a list whose own first line started with that word - accepted, the convention is to put such notes after the list. Evidence of the Engineering Implementer's own: Linux Docker run on the final tree (ruff clean, 890 passed, validator 0 errors).

# 17. WP2c Commit Contents

New: `aiems/governance/reviews/EIP-ESR0061-003_PROVIDER_STRATEGY_OLLAMA_FIRST_AND_CLAUDE_ESCALATION.md`. Changed: `.github/workflows/ci.yml`, `scripts/post_commit_precheck.py`, `scripts/tests/test_post_commit_precheck.py`, `aiems/governance/reviews/EIP-ESR0061-002_PLATFORM_HARDENING_AND_MACOS.md`, `aiems/governance/sessions/ESR-0061_ENGINEERING_SESSION_REPORT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`.
