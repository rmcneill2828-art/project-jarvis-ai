# EIP-ESR0060-002 - Backend Process-Tree Termination

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0060-002 |
| Title | Engineering Implementation Package: WP2 Backend Process-Tree Termination |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0060 |
| Work Package | WP2 |

---

# 2. Purpose

Implements ESR-0060 WP2: closes EBG-0154. When the Tauri host tears down or exits the backend, the whole backend process tree ends promptly: first gracefully, and then by force if it has not exited within a short grace period. This includes the case where the host itself dies.

EIP-ESR0059-001 Section 4G left this open as "not verified". It has now been verified (Section 3). **Drafted before implementation, by Programme Sponsor decision ("review-first")**: no code is changed until this design has had a genuine independent review, after the Copilot CLI quota resets on 1 October 2026.

---

# 3. Repository Context Investigated

**Live verification, 30 September 2026.** Run against the real packaged sidecar, `src-tauri/binaries/jarvis-backend-x86_64-pc-windows-msvc.exe`, which was built at ESR-0059 WP11 and so represents the current code:

| Probe | Result |
|-------|--------|
| Sidecar started; process tree inspected | Bootloader plus one child (PyInstaller onefile) |
| Kill the bootloader only, with stdin held open | **Child (the real backend) still running** 3 s later |
| Kill the bootloader, then close stdin (what `CommandChild::kill()` does in effect: it consumes the handle, which drops its stdin writer) | Idle child exited 58 ms later |
| Close stdin only | Bootloader and child exited cleanly in 637 ms; "Guardian runtime foundation stopped" was logged |
| Dev path: `python -m jarvis --ipc-stdio` (resolves to the repository's `.venv` launcher); kill the launcher | Child exited with it. No orphan on this machine |

**Why the idle result is not the whole story.** `jarvis/interfaces/stdio_rpc.py` `serve_forever()` deliberately handles stdin EOF with `slow_lane.shutdown(wait=True)`. That rule came from ESR-0059 WP5: "a request accepted is always answered". So on EOF the backend first finishes every in-flight and queued slow request, and each one can run up to the 100-second per-turn deadline (`DEFAULT_TURN_DEADLINE_SECONDS`). Meanwhile, a fast-lane handler running inline blocks the EOF from being seen at all.

`src-tauri/src/lib.rs` tears the backend down in the following situations:
* on reader EOF or error;
* on malformed output;
* on a write failure (`tear_down_if_current()`, 7 call sites);
* on app exit (`RunEvent::Exit`).

In each case it calls `BackendHandle::kill()`. For the sidecar, that kills only the bootloader. A backend that is busy at teardown therefore keeps running, holding the same SQLite stores, until its work drains. Meanwhile `call_backend()` spawns a replacement beside it. A genuinely hung backend never ends.

The same applies after the app closes, and after the host is killed or crashes. The `RunEvent::Exit` comment already concedes the last case: "not a guarantee against ... a killed parent process". The timeout path deliberately does not tear down (EBG-0109) and is unchanged here.

**Available API surface:**
* `tauri-plugin-shell` 2.3.5 `CommandChild` exposes `write()`, `kill(self)` and `pid()`. It has no wait method and no way to close stdin without dropping the handle.
* `std::process::Child` (dev path) supports dropping stdin separately, plus `try_wait()`.
* `windows-sys` 0.60.2 is already in `src-tauri/Cargo.lock` as a transitive dependency of Tauri.

---

# 4. Scope

## 4A. A job object per backend (Windows)

A new private `ProcessTree` type in `src-tauri/src/lib.rs`, compiled only on Windows (`#[cfg(windows)]`):

* `ProcessTree::adopt(pid)`:
  * creates an unnamed job object;
  * sets `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` via `SetInformationJobObject(JobObjectExtendedLimitInformation)`;
  * opens the process with `PROCESS_SET_QUOTA | PROCESS_TERMINATE`;
  * assigns the process to the job, then closes the process handle.
  * Processes the backend spawns afterwards, including PyInstaller's real interpreter, are in the job automatically.
* `ProcessTree::active_processes()` reads `ActiveProcesses` from `QueryInformationJobObject(JobObjectBasicAccountingInformation)`.
* `ProcessTree::terminate()` calls `TerminateJobObject`.
* `Drop` closes the job handle. Because of `KILL_ON_JOB_CLOSE`, the OS then ends whatever is still in the job. This also covers the host being killed or crashing, since the OS closes the host's handles.
* It is called right after spawning, on both the dev and sidecar paths, and stored as `Option<ProcessTree>` on `BackendProcess`.
* **If `adopt` fails, spawning does not fail.** The failure is logged to stderr and the backend runs without a job. A process-tree guard must never be the reason JARVIS cannot start.
* **A held process handle, in every case** (design review finding 1 and 4, v0.3). Right after spawning, the host also opens the backend's direct child with `PROCESS_SYNCHRONIZE | PROCESS_TERMINATE` and keeps that handle on `BackendProcess` until shutdown. It gives the no-job fallback an early return (`WaitForSingleObject` with a timeout, instead of a blind sleep) and a safe forced kill: Windows does not reuse a process ID while any handle to that process is open, so `TerminateProcess` through it cannot hit an unrelated process. If even this `OpenProcess` fails, the backend runs exactly as today. `WaitForSingleObject`, `TerminateProcess` and `PROCESS_SYNCHRONIZE` are all in `Win32_System_Threading`, so the approved feature list (4F) is unchanged (confirmed by the Engineering Implementer in the local `windows-sys` 0.60.2 source, `src/Windows/Win32/System/Threading/mod.rs`). The handle is wrapped in a small private owner type whose `Drop` closes it, exactly as `ProcessTree` closes the job handle, so it is released on every path that drops a `BackendProcess` - including any future path that drops one without calling `shutdown()` (re-review advisory, v0.4).
* On non-Windows platforms, `ProcessTree` does not exist and the field is always `None`. JARVIS ships a Windows installer only; Unix process groups are out of scope (4E).

## 4B. Graceful, then forced, shutdown

`BackendHandle::kill(self)` becomes `shutdown(self, tree: Option<ProcessTree>)`:

1. **Close stdin.**
   * Dev path: drop `ChildStdin`.
   * Sidecar path: drop `CommandChild`. That is the only way the plugin allows closing stdin, and it gives up `CommandChild::kill()`, so any forced kill afterwards goes through the job (step 3).
2. **Wait up to `BACKEND_SHUTDOWN_GRACE` (3 s)** for the tree to empty. With a job, poll `active_processes() == 0` every 50 ms. Without one, wait on the held process handle (`WaitForSingleObject`), which returns as soon as the direct child exits; the PyInstaller bootloader waits for its own child, so its exit marks the end of the backend in the graceful case. On the dev path, `try_wait()` also returns early.
   * 3 s is about five times the 637 ms clean-exit time measured above.
   * An idle backend exits almost at once.
   * A busy one gets a chance to finish flushing, but its queued turns are not waited for: the host has already failed those calls with `fail_all_pending()`, so no one is left to receive the answers.
3. **Force.** Call `terminate()` on the job. If there is no job:
   * dev path: `Child::kill()`, then `wait()` (today's behaviour);
   * sidecar path: `TerminateProcess` through the held handle (never by PID number, so no PID-reuse risk). Without the job this ends only the bootloader, which is today's behaviour and no worse.

**The wait never holds the shared-state lock.** Today `tear_down_if_current()` and the exit handler call `kill()` while holding the lock. Under the new design, both take the `BackendProcess` out under the lock, release it, and then call `shutdown()`. So a request arriving during the grace period spawns its replacement immediately rather than waiting up to 3 s.

This does not change what can overlap. Old and new backends already overlap today, for as long as the old one's work takes to drain. The grace period bounds that overlap at 3 s instead of up to 100 s per queued turn, or forever.

## 4C. The `RunEvent::Exit` handler

The handler uses `shutdown()`, so closing the app waits at most 3 s and then ends the tree. Its comment is updated: a killed host is now covered by `KILL_ON_JOB_CLOSE`. Crash and restart *policy* stays with EBG-0050.

**This wait blocks the main (event-loop) thread** (design review finding 3, v0.3). Every other teardown path runs on a reader thread or Tokio's blocking pool, where a 3-second wait is harmless; the exit handler alone runs on the main thread. `RunEvent::Exit` normally fires after the last window has closed, so no window should be left to show "Not Responding" while it waits. That is not verified for every exit route, so the live check (Section 5) watches for it explicitly. An idle backend, the usual case, returns in well under a second.

## 4D. Tests (`src-tauri/src/lib.rs`, Windows-only where a job object is involved)

The tests spawn real `python -c` processes, matching the existing idle-child teardown test from ESR-0059 WP1. They do not use the sidecar, so they need no packaged build.

* **Tree termination:** the child spawns a grandchild that sleeps and prints its PID. After `adopt()` and `terminate()`, both are gone.
* **Kill on handle close:** the same setup, but the `ProcessTree` is dropped rather than terminated. Both processes are gone. This stands in for the host being killed.
* **Graceful path taken:** a child that writes a marker file on stdin EOF and exits. After `shutdown()`, the marker exists and it returned well within the grace period.
* **Forced path bounded:** a child that ignores EOF and sleeps. `shutdown()` returns within the grace period plus a margin, and the process is gone.
* **Degraded mode:** `shutdown(handle, None)` still ends a dev child, which is today's behaviour.
* **Real `adopt()` failure** (design review finding 5, v0.3; corrected v0.4): `adopt(0)`. Microsoft documents that `OpenProcess` on PID 0, the System Idle Process, always fails with `ERROR_INVALID_PARAMETER`, whatever the caller's privileges - which matters because GitHub's Windows runners run elevated. `adopt()` returns an error rather than panicking, and the spawn path carries on without a job. v0.3 proposed an already-exited child's PID instead; the re-review showed that is unreliable (a still-held handle keeps the process object alive, so `OpenProcess` succeeds; a released one lets the PID be reused, so the test could adopt and terminate an unrelated process).
* **No-job early return:** with no job but a held handle, `shutdown()` of a child that exits on EOF returns well inside the grace period, not after it.
* **Lock not held:** the backend is taken from the shared state before `shutdown()` runs. Asserted structurally: a test locks the state from inside a slow child's grace window.

## 4E. Explicitly out of scope

* **Python-side EOF behaviour.** `serve_forever()` keeps WP5's drain-on-EOF. The host now bounds how long it waits instead. An alternative, `shutdown(cancel_futures=True)` on EOF, would change WP5's documented contract, and it would not help a hung fast-lane handler.
* **Unix process groups.** No non-Windows build is shipped.
* **Timeout-driven teardown.** The 120-second timeout path still deliberately does not tear down the backend (EBG-0109).
* **Crash and restart policy (EBG-0050), and the unused shell-execute capability (EBG-0149).**

## 4F. Dependency - flagged for Programme Sponsor decision

This package adds **one new direct dependency**, Windows only:

```toml
[target.'cfg(windows)'.dependencies]
windows-sys = { version = "0.60", features = ["Win32_Foundation", "Win32_System_JobObjects", "Win32_System_Threading"] }
```

`windows-sys` 0.60.2 is already compiled into every Windows build through Tauri, so no new crate is downloaded or audited. It is still a new *direct* dependency and a small `unsafe` surface of four FFI calls, so it needs an explicit approval rather than going in silently (PBK-0001 scope-creep and dependency rule).

**Programme Sponsor decision (30 September 2026): approved** via direct chat instruction ("Approved"), in reply to the dependency decision put to them at ESR-0060 opening. This approves the dependency only, not implementation of this package, which still waits for its independent design review.

The alternative with no new dependency is to run `taskkill /T /F /PID <pid>` as a child process at teardown. It is rejected because:
* it cannot cover a killed or crashed host;
* it races against PID reuse;
* it depends on a system executable being on `PATH`.

## 4G. Disclosed residual risk

`AssignProcessToJobObject` runs just *after* `spawn()`. A grandchild created in that gap would escape the job.

In practice, PyInstaller's bootloader unpacks its archive before starting the interpreter, and a 115 MB archive takes well over a second. The venv launcher starts its child sooner, but on this machine it already ends that child itself.

Closing the gap fully would mean spawning suspended (`CREATE_SUSPENDED`), assigning the job, then resuming the primary thread. Neither `std::process::Command` nor the shell plugin can do this, because neither exposes the primary thread handle that `ResumeThread` needs. **Considered and deferred** (design review finding 2, v0.3): with `windows-sys` now a direct dependency, the host could call `CreateProcessW` itself, but that means replacing the spawn mechanism on both paths - the shell plugin's pipe readers and event channel on the sidecar path included - for a gap that the timing above makes unlikely to matter. Recorded here, and revisited only if an escaped process is ever observed.

## 4H. Governance

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]: EBG-0154 is registered (Candidate Backlog, Medium) at ESR-0060 opening and closed as Completed by this package once it is implemented.
* [[ESR-0060_ENGINEERING_SESSION_REPORT|ESR-0060]] records WP2.

## 4I. Implementation Notes (v0.5)

Implemented in `src-tauri/src/lib.rs` and `src-tauri/Cargo.toml` after the Programme Sponsor approved the reviewed design (v0.4) for implementation. Where the implementation departs from, or adds to, Sections 4A to 4D:

* **A fourth `windows-sys` feature, `Win32_Security`** - found while implementing, missed by the design and by both design-review rounds. `windows-sys` 0.60.2 compiles `CreateJobObjectW` only under `#[cfg(feature = "Win32_Security")]`, because its signature names `SECURITY_ATTRIBUTES`. Same crate, same already-compiled 0.60.2 copy (`Cargo.lock` gains one dependency line, no new package). Flagged to the Programme Sponsor rather than treated as covered by the 4F approval of three features; **approved** (v1.0).
* **The CI `rust` job runs on Linux, not Windows** - also missed by the design and both review rounds, which assumed GitHub's Windows runners, so the seven Windows job-object tests compiled out in CI. **Resolved by Programme Sponsor decision 2(a) (v0.7)**, following the implementation reviewer's recommendation: `.github/workflows/ci.yml` gains a `rust-windows` job (`windows-latest`: toolchain, Python 3.12, `pip install -e .[dev]`, sidecar build, `cargo test`) that runs on pushes to `main` and on demand (`workflow_dispatch`, added to the workflow's triggers), not on pull requests, to limit Windows runner minutes; and the existing Linux clippy step gains `--tests`, so test code is linted in CI too. The new job is not added to branch protection's required checks. It cannot be run before the commit is pushed; its first real run is checked after the push.
* **Non-Windows stand-ins.** Rather than `#[cfg]` on every use, `process_tree` has a non-Windows version whose `ProcessTree` and `ProcessHandle` are uninhabited enums and whose constructors always fail, so every `ProcessGuard` is empty there - Section 4A's "the field is always `None`", enforced by the type system. Verified on Linux (WSL Ubuntu): `cargo clippy --tests -D warnings` clean, `cargo test` 11 passed.
* **`ProcessGuard`** holds the optional job (`ProcessTree`) and the optional held handle (`ProcessHandle`); both close their kernel handle in `Drop` through one private `OwnedHandle`. `BackendHandle::shutdown(self, guard)` replaces `kill(self)`; `BackendProcess::shut_down()` wraps it.
* **With a job, "exited" means the job is empty**, not that the direct child has exited: on the dev path the venv launcher can exit before its interpreter does. A failed job query counts as not empty, so it falls through to the forced kill.
* **Sidecar with neither a job nor a handle** keeps today's `CommandChild::kill()` and does not wait: once the `CommandChild` is dropped there would be nothing left to wait on or force with. This needs both `OpenProcess` calls to fail, so it should not occur in practice.
* **An ignored live harness** (`live_packaged_sidecar_busy_tree_is_ended_within_the_grace`) drives the real packaged sidecar through the same code, for live check (b); it needs `JARVIS_LIVE_SIDECAR` and does not run in normal test runs.
* **Forced termination is checked, and reaping is bounded** (implementation review finding, v0.6). `terminate()` now returns whether `TerminateJobObject`/`TerminateProcess` succeeded; `force()` tries the job, then the held handle, and reports real success, so a failure falls back to `child.kill()`. The dev path's final reap is a bounded poll (`REAP_TIMEOUT`, 2 s) that kills once more and logs if the child still has not exited - previously an unconditional `wait()`, which would have hung teardown forever had a termination failed.
* **A PID-reuse race between `spawn()` and `attach()`** (review, informational): if a freshly spawned child died and its PID were reused before `attach()` opened its handles, the guard could adopt an unrelated process. Sub-millisecond, and the child is alive in every real case; the same class as the Section 4G gap, recorded rather than engineered around.
* **Tests.** Section 4D as designed, plus: `reap()` gives up after `REAP_TIMEOUT` on a live child that was never terminated; an idle child returns early with no guard; no job but a held handle forces through the handle; `tear_down_if_current()` releases the lock while its backend is still inside the grace wait. 19 tests, 12 of them cross-platform.

**Live verification (1 October 2026), sidecar rebuilt from the current code, release app built with `tauri build --no-bundle`, isolated stores:**

| Check | Result |
|-------|--------|
| (a) Release app, close normally | Both backend processes gone **826 ms** after close; backend log shows a clean "JARVIS backend stopped" (graceful, not forced) |
| (b) Real packaged sidecar torn down with a slow turn in flight (Ollama pointed at an unreachable address), via the harness | The job held **2 processes** (bootloader and real interpreter - the Section 4G gap did not let it escape); whole tree ended by force at **3.006 s**; no JARVIS process left. Before this package this case survived for up to 100 s per queued turn |
| (c) Release app, host force-killed | Whole backend tree gone **96 ms** later (`KILL_ON_JOB_CLOSE`) |
| (a) repeated on the dev path (debug app, `python -m jarvis`) | Closed 4 s after start: **forced at 3.09 s** - the backend was still busy with its startup calls (a fast-lane handler blocks EOF handling, EBG-0154's own mechanism), and the bound held. Closed after 25 s: **graceful in 161 ms**, clean "stopped" logged |

"Not Responding" during the exit wait could not be observed by these scripted checks (Section 4C): the window had closed in every case before the host process exited, but whether a window was briefly unresponsive was not visible. Left for a manual check by the Programme Sponsor if wanted.

---

# 5. Validation Requirements

* `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test` (`src-tauri/`), including the Section 4D tests.
* `python -m pytest -q`, `ruff check .` and `npx playwright test`. These are unchanged surfaces, run as regression checks.
* `python scripts/validate_repository.py`: 0 errors, with the warning count disclosed.
* **Live check on a real packaged build**, using the same method as ESR-0059 WP11:
  * Start the installed or bundled app and complete one conversation round trip.
  * (a) Close the app normally. Confirm no `jarvis-backend` process remains.
  * (b) Start a slow request, then close the app. Confirm the tree is gone within about 3 s.
  * (c) Force-kill the host process. Confirm the tree is gone.
  * During (a) and (b), watch for any window showing "Not Responding" while the exit handler waits (design review finding 3).
  * Repeat (a) in the dev shell.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, review findings, observations, outstanding issues, and the commit SHA, message and repository status once authorised.

---

# 7. Success Criteria

* No teardown path, and no app exit, leaves any process from the backend's tree running for more than `BACKEND_SHUTDOWN_GRACE` plus a small margin. This includes a backend that is busy or hung.
* A killed or crashed host leaves no backend process running (Windows).
* An idle backend is still shut down gracefully (stdin EOF), not by force.
* No shared-state lock is held during the grace wait.
* If job-object setup fails, JARVIS still starts, and shutdown still returns early for a backend that exits on EOF.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 1 October 2026 | Claude Engineering Implementer | CI-change review (genuine Copilot CLI) - **Pass**; two notes: the Windows tests' timing margins were sized on the Engineering Implementer's machine, so the first shared-runner runs are to be watched; and the job builds no frontend, by symmetry with the working Linux job. **Programme Sponsor approved** via direct chat instruction ("Approved") and the Sponsor Approval Service (`approve`, `repository_ref: e2eb0f5`, 2026-10-01T15:22:26Z), in reply to a request for both the `Win32_Security` feature and the commit - read as approving both. Pending commit through `submit-response`. |
| 0.7 | 1 October 2026 | Claude Engineering Implementer | Implementation re-review (genuine Copilot CLI) - **Pass**, no findings. Programme Sponsor decision 2(a): a `rust-windows` CI job running `cargo test` on pushes to `main` and on demand, plus `--tests` on the Linux clippy step (Section 4I). The `Win32_Security` feature still awaits explicit Programme Sponsor confirmation. Not yet reviewed (CI change), approved or committed. |
| 0.6 | 1 October 2026 | Claude Engineering Implementer | Implementation review (genuine Copilot CLI, cargo allowed) - **Conditional Pass**. One Medium finding fixed: `force()` assumed termination succeeded and the dev path then called an unbounded `wait()`, so a failed termination could hang teardown forever - termination results are now checked with fallback, and reaping is bounded (`reap()`, 2 s). Advisories: `WAIT_INFINITE` comment added; spawn-to-attach PID-reuse race recorded (4I). The reviewer recommends a Windows CI job for `cargo test`, limited to pushes to `main`, and `--tests` on the CI clippy step - both raised for the Programme Sponsor, not done here. cargo test 19 passed/1 ignored (Linux 12 passed), clippy and fmt clean on both; live harness (b) re-run on v0.6: 2 processes in the job, busy tree ended at 3.05 s. Live checks (a) and (c) ran on v0.5; the paths they exercise (graceful exit, kill-on-close) are unchanged. Not yet re-reviewed, approved or committed. |
| 0.5 | 1 October 2026 | Claude Engineering Implementer | Implemented, after Programme Sponsor approval of v0.4 for implementation (direct chat instruction, "Approved"). Section 4I added. Two real gaps the design reviews missed, found while implementing: `CreateJobObjectW` needs a fourth `windows-sys` feature, `Win32_Security` (flagged to the Programme Sponsor); and the CI `rust` job runs on Linux, so the Windows job-object tests run locally only (raised as a question). Live checks (a), (b), (c) and dev-path (a) all passed on a freshly rebuilt packaged build. cargo test 18 passed/1 ignored (Linux via WSL 11 passed), clippy and fmt clean on both; pytest 759/1, Playwright 26/26, ruff clean, validator 0 errors. Not yet reviewed, approved or committed. |
| 0.4 | 1 October 2026 | Claude Engineering Implementer | Design re-review (genuine Copilot CLI) - **Conditional Pass**: all five v0.2 findings confirmed resolved; one new Low finding - the real `adopt()` failure test's already-exited-PID approach is unreliable and could touch an unrelated process. Corrected to `adopt(0)` (documented to fail on every privilege level; the reviewer suggested PID 4, which depends on elevation). Advisory adopted: the held process handle gets an explicit owner type with `Drop`. Feature coverage for the new APIs confirmed in the local source by the Engineering Implementer, since the reviewer's sandbox could not read the cargo registry this run. Not yet re-reviewed, approved or implemented. |
| 0.3 | 1 October 2026 | Claude Engineering Implementer | Design-reviewed via a genuine scoped GitHub Copilot CLI invocation through the real bridge (`ESR-0060`/`WP2`) - **Conditional Pass**: core mechanism confirmed (dropping `CommandChild` closes stdin, verified in the plugin source and independently by the Engineering Implementer; teardown threading race-free; feature list complete; PyInstaller never breaks away from a job). Five findings addressed: a held process handle gives the no-job fallback an early return and a PID-reuse-safe kill (findings 1 and 4); suspended spawning recorded as considered and deferred (2); the main-thread wait in the exit handler disclosed and added to the live check (3); a test for a real `adopt()` failure added (5). Not yet re-reviewed, approved or implemented. |
| 0.2 | 30 September 2026 | Claude Engineering Implementer | Section 4F: new direct `windows-sys` dependency approved by the Programme Sponsor via direct chat instruction ("Approved"). Dependency only; implementation still waits for the independent design review. Not yet reviewed or committed. |
| 0.1 | 30 September 2026 | Claude Engineering Implementer | ESR-0060 WP2 design draft, review-first by Programme Sponsor decision. EIP-ESR0059-001 Section 4G verified live on the real packaged sidecar: a busy or hung backend survives teardown, while an idle one exits on stdin EOF. Job-object-per-backend design, with graceful-then-forced shutdown outside the lock. New direct `windows-sys` dependency flagged for decision. No code changed. Not yet reviewed, approved or committed. |
