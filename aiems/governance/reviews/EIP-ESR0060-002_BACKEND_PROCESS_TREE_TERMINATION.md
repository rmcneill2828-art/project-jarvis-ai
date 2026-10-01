# EIP-ESR0060-002 - Backend Process-Tree Termination

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0060-002 |
| Title | Engineering Implementation Package: WP2 Backend Process-Tree Termination |
| Version | 0.2 |
| Status | Draft - design only, not implemented |
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
* **If `adopt` fails, spawning does not fail.** The failure is logged to stderr and the backend runs with `None`, which is exactly today's behaviour. A process-tree guard must never be the reason JARVIS cannot start.
* On non-Windows platforms, `ProcessTree` does not exist and the field is always `None`. JARVIS ships a Windows installer only; Unix process groups are out of scope (4E).

## 4B. Graceful, then forced, shutdown

`BackendHandle::kill(self)` becomes `shutdown(self, tree: Option<ProcessTree>)`:

1. **Close stdin.**
   * Dev path: drop `ChildStdin`.
   * Sidecar path: drop `CommandChild`. That is the only way the plugin allows closing stdin, and it gives up `CommandChild::kill()`, so any forced kill afterwards goes through the job (step 3).
2. **Wait up to `BACKEND_SHUTDOWN_GRACE` (3 s)** for the tree to empty. Poll `active_processes() == 0` every 50 ms; on the dev path, `try_wait()` also returns early.
   * 3 s is about five times the 637 ms clean-exit time measured above.
   * An idle backend exits almost at once.
   * A busy one gets a chance to finish flushing, but its queued turns are not waited for: the host has already failed those calls with `fail_all_pending()`, so no one is left to receive the answers.
3. **Force.** Call `terminate()` on the job. If there is no job:
   * dev path: `Child::kill()`, then `wait()` (today's behaviour);
   * sidecar path: a best-effort `TerminateProcess` on the recorded bootloader PID. Without the job this is no worse than today.

**The wait never holds the shared-state lock.** Today `tear_down_if_current()` and the exit handler call `kill()` while holding the lock. Under the new design, both take the `BackendProcess` out under the lock, release it, and then call `shutdown()`. So a request arriving during the grace period spawns its replacement immediately rather than waiting up to 3 s.

This does not change what can overlap. Old and new backends already overlap today, for as long as the old one's work takes to drain. The grace period bounds that overlap at 3 s instead of up to 100 s per queued turn, or forever.

## 4C. The `RunEvent::Exit` handler

The handler uses `shutdown()`, so closing the app waits at most 3 s and then ends the tree. Its comment is updated: a killed host is now covered by `KILL_ON_JOB_CLOSE`. Crash and restart *policy* stays with EBG-0050.

## 4D. Tests (`src-tauri/src/lib.rs`, Windows-only where a job object is involved)

The tests spawn real `python -c` processes, matching the existing idle-child teardown test from ESR-0059 WP1. They do not use the sidecar, so they need no packaged build.

* **Tree termination:** the child spawns a grandchild that sleeps and prints its PID. After `adopt()` and `terminate()`, both are gone.
* **Kill on handle close:** the same setup, but the `ProcessTree` is dropped rather than terminated. Both processes are gone. This stands in for the host being killed.
* **Graceful path taken:** a child that writes a marker file on stdin EOF and exits. After `shutdown()`, the marker exists and it returned well within the grace period.
* **Forced path bounded:** a child that ignores EOF and sleeps. `shutdown()` returns within the grace period plus a margin, and the process is gone.
* **Degraded mode:** `shutdown(handle, None)` still ends a dev child, which is today's behaviour.
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

Closing the gap fully would mean spawning suspended, which neither `std::process::Command` nor the shell plugin exposes. The limitation is recorded rather than engineered around.

## 4H. Governance

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]: EBG-0154 is registered (Candidate Backlog, Medium) at ESR-0060 opening and closed as Completed by this package once it is implemented.
* [[ESR-0060_ENGINEERING_SESSION_REPORT|ESR-0060]] records WP2.

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
* If job-object setup fails, JARVIS still starts and behaves exactly as it does today.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 30 September 2026 | Claude Engineering Implementer | Section 4F: new direct `windows-sys` dependency approved by the Programme Sponsor via direct chat instruction ("Approved"). Dependency only; implementation still waits for the independent design review. Not yet reviewed or committed. |
| 0.1 | 30 September 2026 | Claude Engineering Implementer | ESR-0060 WP2 design draft, review-first by Programme Sponsor decision. EIP-ESR0059-001 Section 4G verified live on the real packaged sidecar: a busy or hung backend survives teardown, while an idle one exits on stdin EOF. Job-object-per-backend design, with graceful-then-forced shutdown outside the lock. New direct `windows-sys` dependency flagged for decision. No code changed. Not yet reviewed, approved or committed. |
