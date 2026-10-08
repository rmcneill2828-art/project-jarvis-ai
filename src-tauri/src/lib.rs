//! Tauri sidecar process management and commands for the JARVIS UXP-backend
//! bridge (ADR-0019, ESR-0017 WP9 - foundation scope).
//!
//! EIP-ESR0032-001 (Guardian Desktop Distribution Foundation) introduced a
//! second backend spawn path alongside the original dev-mode one:
//!
//! - **Dev builds** (`cfg!(debug_assertions)` true - `cargo build`/`tauri dev`,
//!   any debug-profile build regardless of how it is launched): unchanged
//!   from the original foundation scope. `std::process::Command::new("python")`
//!   spawns `python -m jarvis --ipc-stdio` directly against the repository
//!   checkout - fast iteration, no packaging step required.
//! - **Release builds** (`cfg!(debug_assertions)` false - `tauri build`'s
//!   bundled output): spawns the PyInstaller-packaged standalone executable
//!   (`scripts/build_backend_sidecar.py`'s output, registered as a Tauri
//!   `externalBin` sidecar) via `tauri-plugin-shell`'s async `Command::sidecar`
//!   API instead - no local Python installation is required on the end
//!   user's machine.
//!
//! The branch is keyed on the Cargo build profile, not on whether a sidecar
//! binary happens to exist on disk - a debug-profile packaged build (were one
//! ever produced) still takes the raw `python -m jarvis` path, and a
//! release-profile run always takes the sidecar path regardless of whether a
//! local Python install is also present (EIP-ESR0032-001 Implementation
//! Requirement 6).
//!
//! Both paths funnel every line of backend output through the same
//! `dispatch_line()` - the JSON-RPC classification and routing logic (is this
//! a response or a notification, per EIP-ESR0031-002) is written once and
//! shared, only the mechanism for *obtaining* each line differs: a
//! synchronous `BufReader` over a `std::process::Child`'s stdout for dev, an
//! async `CommandEvent` channel (consumed via `blocking_recv()` from a plain
//! spawned thread) for the sidecar.
//!
//! The Python backend process is spawned once (lazily, on first use) and
//! reused across calls, not respawned per request. If it becomes unavailable
//! (write/read failure, malformed response, closed pipe), the error is
//! surfaced to the caller and the process handle is dropped so the *next*
//! call attempts a fresh spawn - there is no silent fallback to mock data.

use serde_json::{json, Value};
use std::collections::HashMap;
use std::io::{BufRead, BufReader, Write};
#[cfg(unix)]
use std::os::unix::process::CommandExt;
use std::path::Path;
use std::process::{Child, ChildStdin, ChildStdout, Command, Stdio};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use std::time::{Duration, Instant};
use tauri::{AppHandle, Emitter, Manager, State};
use tauri_plugin_shell::process::{CommandChild, CommandEvent};
use tauri_plugin_shell::ShellExt;

type PendingMap = Arc<Mutex<HashMap<u64, mpsc::Sender<Result<Value, String>>>>>;
type SharedBackend = Arc<Mutex<Option<BackendProcess>>>;

/// EBG-0109 Finding 2(c): call_backend() previously waited on an unbounded
/// channel receive, so a stalled backend produced an indefinite freeze with no
/// user-visible error (the OS's own "(Not Responding)" state, not this app's).
/// 120s gives 30s of headroom over the Python side's own OLLAMA_TIMEOUT_SECONDS
/// (90s) for JSON-RPC marshalling/process-scheduling overhead, while still
/// bounding the wait so a genuine stall surfaces a clear error instead of never
/// resolving. This does not root-cause why a request can fail to reach Ollama
/// at all (Finding 2(b), still open) - it only bounds the symptom.
const BACKEND_CALL_TIMEOUT: Duration = Duration::from_secs(120);
const BACKEND_TIMEOUT_MESSAGE: &str =
    "JARVIS backend did not respond in time. The request may still complete in the background; try again.";

/// Unifies the two possible backend handle shapes so `call_backend()` and the
/// app-exit cleanup handler do not need to duplicate write/kill logic per path.
enum BackendHandle {
    Dev { child: Child, stdin: ChildStdin },
    Sidecar { child: CommandChild },
}

impl BackendHandle {
    fn write_line(&mut self, line: &str) -> std::io::Result<()> {
        match self {
            BackendHandle::Dev { stdin, .. } => {
                stdin.write_all(line.as_bytes()).and_then(|_| stdin.flush())
            }
            BackendHandle::Sidecar { child } => child
                .write(line.as_bytes())
                .map_err(|e| std::io::Error::other(e.to_string())),
        }
    }

    /// Ends the backend's whole process tree (EBG-0154, EIP-ESR0060-002):
    /// gracefully first, then by force.
    ///
    /// 1. Close stdin, so an idle backend's `serve_forever()` sees EOF and
    ///    exits on its own. For the sidecar this means dropping the
    ///    `CommandChild` - the plugin offers no other way to close stdin.
    /// 2. Wait up to `BACKEND_SHUTDOWN_GRACE` for it to finish.
    /// 3. Force: terminate the job (every process in the tree), or without
    ///    one, the direct child alone - today's behaviour.
    ///
    /// Previously `CommandChild::kill()` ended only PyInstaller's bootloader,
    /// so a busy backend kept running beside its replacement, and a hung one
    /// never ended. Blocks for at most the grace period plus a forced kill,
    /// so callers must not hold the shared-state lock. Errors are swallowed:
    /// this runs during teardown, where there is no caller left to report to.
    fn shutdown(self, guard: ProcessGuard) {
        let deadline = Instant::now() + BACKEND_SHUTDOWN_GRACE;
        match self {
            BackendHandle::Dev { mut child, stdin } => {
                drop(stdin);
                let exited = guard.wait_until(deadline, || matches!(child.try_wait(), Ok(Some(_))));
                if !exited && !guard.force() {
                    let _ = child.kill();
                }
                reap(&mut child);
            }
            BackendHandle::Sidecar { child } => {
                if guard.is_empty() {
                    // Nothing to wait on or force with once the
                    // `CommandChild` is gone, so keep today's behaviour:
                    // kill the bootloader, which also closes stdin.
                    let _ = child.kill();
                    return;
                }
                drop(child);
                let exited = guard.wait_until(deadline, || false);
                if !exited {
                    guard.force();
                }
            }
        }
    }
}

/// Reaps a dev-path child so it does not linger as a zombie on Unix-like
/// platforms (ESR-0059 WP1) - but never waits unboundedly (implementation
/// review finding, EIP-ESR0060-002 v0.6): if the forced termination itself
/// failed, a plain `wait()` would block teardown forever, the very hang this
/// package removes. After `REAP_TIMEOUT` it tries `kill()` once more, logs,
/// and gives up rather than hang.
fn reap(child: &mut Child) {
    let deadline = Instant::now() + REAP_TIMEOUT;
    loop {
        match child.try_wait() {
            Ok(Some(_)) | Err(_) => return,
            Ok(None) if Instant::now() >= deadline => {
                let _ = child.kill();
                eprintln!(
                    "JARVIS backend process {} did not exit after being terminated.",
                    child.id()
                );
                return;
            }
            Ok(None) => thread::sleep(SHUTDOWN_POLL_INTERVAL),
        }
    }
}

/// How long `reap()` waits for a terminated child to exit. Termination is
/// normally immediate; this only bounds the case where it failed.
const REAP_TIMEOUT: Duration = Duration::from_secs(2);

/// How long `BackendHandle::shutdown()` waits for a backend to exit on stdin
/// EOF before ending it by force (EIP-ESR0060-002 Section 4B). About five
/// times the 637 ms a real packaged backend took to exit cleanly; queued
/// turns are not waited for, since `fail_all_pending()` has already answered
/// their callers.
const BACKEND_SHUTDOWN_GRACE: Duration = Duration::from_secs(3);
const SHUTDOWN_POLL_INTERVAL: Duration = Duration::from_millis(50);

/// What the host holds on to so it can end a backend's whole process tree
/// (EIP-ESR0060-002 Sections 4A/4B): a job object, and a handle to the
/// direct child. Either can be missing - attaching never fails a spawn - and
/// on non-Windows platforms both always are.
struct ProcessGuard {
    tree: Option<process_tree::ProcessTree>,
    process: Option<process_tree::ProcessHandle>,
}

impl ProcessGuard {
    #[cfg(test)]
    fn none() -> Self {
        ProcessGuard {
            tree: None,
            process: None,
        }
    }

    /// Called right after spawning, before the backend has had time to start
    /// its own children (the gap is disclosed in EIP-ESR0060-002 Section 4G).
    /// A failure is logged and leaves that part `None`: a process-tree guard
    /// must never be the reason JARVIS cannot start.
    fn attach(pid: u32) -> Self {
        let tree = process_tree::ProcessTree::adopt(pid)
            .map_err(|e| eprintln!("JARVIS backend process-tree guard unavailable: {e}"))
            .ok();
        let process = process_tree::ProcessHandle::open(pid)
            .map_err(|e| eprintln!("JARVIS backend process handle unavailable: {e}"))
            .ok();
        ProcessGuard { tree, process }
    }

    fn is_empty(&self) -> bool {
        self.tree.is_none() && self.process.is_none()
    }

    /// Waits until the backend has exited or `deadline` passes; returns
    /// whether it exited. With a job, "exited" means the whole tree is
    /// empty. Without one, it means the direct child has exited (for the
    /// sidecar, PyInstaller's bootloader, which itself waits for the real
    /// backend) - via the held handle, or `child_exited` on the dev path.
    fn wait_until(&self, deadline: Instant, mut child_exited: impl FnMut() -> bool) -> bool {
        loop {
            let done = match (&self.tree, &self.process) {
                // The tree alone decides. `child_exited` is still called, for
                // its side effect: `try_wait` reaps the direct child, and on
                // Unix a zombie group leader keeps its group from reading empty.
                (Some(tree), _) => {
                    let _ = child_exited();
                    tree.is_empty()
                }
                (None, Some(process)) => child_exited() || process.wait(Duration::ZERO),
                (None, None) => child_exited(),
            };
            if done {
                return true;
            }
            let now = Instant::now();
            if now >= deadline {
                return false;
            }
            thread::sleep(SHUTDOWN_POLL_INTERVAL.min(deadline - now));
        }
    }

    /// Ends the tree by force; returns whether a termination actually
    /// succeeded. Tries the job (the whole tree), then the held handle (the
    /// direct child). False, when there was nothing to force with or every
    /// attempt failed, leaves the caller to fall back on what it has
    /// (implementation review finding, v0.6: success used to be assumed).
    fn force(&self) -> bool {
        if let Some(tree) = &self.tree {
            match tree.terminate() {
                Ok(()) => return true,
                Err(e) => eprintln!("JARVIS backend job termination failed: {e}"),
            }
        }
        if let Some(process) = &self.process {
            match process.terminate() {
                Ok(()) => return true,
                Err(e) => eprintln!("JARVIS backend process termination failed: {e}"),
            }
        }
        false
    }
}

/// Windows job objects and process handles (EBG-0154, EIP-ESR0060-002).
///
/// A job created with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` takes every
/// process the backend later starts - including PyInstaller's real
/// interpreter - and the OS ends them all when the job handle closes. That
/// also covers a killed or crashed host, since the OS closes its handles.
#[cfg(windows)]
mod process_tree {
    use std::io;
    use std::mem::{size_of, zeroed};
    use std::ptr::{null, null_mut};
    use std::time::Duration;
    use windows_sys::Win32::Foundation::{CloseHandle, HANDLE, WAIT_OBJECT_0};
    use windows_sys::Win32::System::JobObjects::{
        AssignProcessToJobObject, CreateJobObjectW, JobObjectBasicAccountingInformation,
        JobObjectExtendedLimitInformation, QueryInformationJobObject, SetInformationJobObject,
        TerminateJobObject, JOBOBJECT_BASIC_ACCOUNTING_INFORMATION,
        JOBOBJECT_EXTENDED_LIMIT_INFORMATION, JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE,
    };
    use windows_sys::Win32::System::Threading::{
        OpenProcess, TerminateProcess, WaitForSingleObject, PROCESS_SET_QUOTA, PROCESS_SYNCHRONIZE,
        PROCESS_TERMINATE,
    };

    /// Exit code given to processes ended by force.
    const FORCED_EXIT_CODE: u32 = 1;

    /// An owned kernel handle, closed on drop - so neither the job nor the
    /// process handle can leak on any path that drops a `BackendProcess`.
    struct OwnedHandle(HANDLE);

    // SAFETY: a Windows kernel handle is a process-wide value, valid on any
    // thread; it is never shared mutably, only used by the one owner.
    unsafe impl Send for OwnedHandle {}

    impl OwnedHandle {
        fn new(handle: HANDLE) -> io::Result<Self> {
            if handle.is_null() {
                Err(io::Error::last_os_error())
            } else {
                Ok(OwnedHandle(handle))
            }
        }
    }

    impl Drop for OwnedHandle {
        fn drop(&mut self) {
            // SAFETY: the handle is valid and owned solely by this value.
            unsafe { CloseHandle(self.0) };
        }
    }

    fn check(ok: windows_sys::core::BOOL) -> io::Result<()> {
        if ok == 0 {
            Err(io::Error::last_os_error())
        } else {
            Ok(())
        }
    }

    pub struct ProcessTree {
        job: OwnedHandle,
    }

    impl ProcessTree {
        /// Puts the process `pid`, and everything it starts from now on, in a
        /// new job that the OS ends when this value is dropped.
        pub fn adopt(pid: u32) -> io::Result<Self> {
            // SAFETY: plain FFI calls with valid arguments; every handle
            // returned is owned by an `OwnedHandle` before anything can fail.
            unsafe {
                let job = OwnedHandle::new(CreateJobObjectW(null(), null()))?;
                let mut limits: JOBOBJECT_EXTENDED_LIMIT_INFORMATION = zeroed();
                limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE;
                check(SetInformationJobObject(
                    job.0,
                    JobObjectExtendedLimitInformation,
                    &limits as *const _ as *const _,
                    size_of::<JOBOBJECT_EXTENDED_LIMIT_INFORMATION>() as u32,
                ))?;
                let process =
                    OwnedHandle::new(OpenProcess(PROCESS_SET_QUOTA | PROCESS_TERMINATE, 0, pid))?;
                check(AssignProcessToJobObject(job.0, process.0))?;
                Ok(ProcessTree { job })
            }
        }

        /// True once no process is left in the job. A failed query counts as
        /// not empty, so the caller falls through to a forced termination.
        pub fn is_empty(&self) -> bool {
            self.active_processes() == Some(0)
        }

        /// How many processes are in the job, or None if the query failed.
        pub fn active_processes(&self) -> Option<u32> {
            // SAFETY: the job handle is valid; the buffer is correctly sized.
            unsafe {
                let mut info: JOBOBJECT_BASIC_ACCOUNTING_INFORMATION = zeroed();
                let ok = QueryInformationJobObject(
                    self.job.0,
                    JobObjectBasicAccountingInformation,
                    &mut info as *mut _ as *mut _,
                    size_of::<JOBOBJECT_BASIC_ACCOUNTING_INFORMATION>() as u32,
                    null_mut(),
                );
                (ok != 0).then_some(info.ActiveProcesses)
            }
        }

        /// Ends every process in the job. Harmless when it is already empty.
        pub fn terminate(&self) -> io::Result<()> {
            // SAFETY: the job handle is valid.
            check(unsafe { TerminateJobObject(self.job.0, FORCED_EXIT_CODE) })
        }
    }

    /// A handle to one process, held from spawn (EIP-ESR0060-002 Section
    /// 4A): lets shutdown wait for it without a job, and end it without
    /// risking an unrelated process - Windows does not reuse a process ID
    /// while any handle to that process is open.
    pub struct ProcessHandle {
        process: OwnedHandle,
    }

    impl ProcessHandle {
        pub fn open(pid: u32) -> io::Result<Self> {
            // SAFETY: plain FFI call; the result is owned immediately.
            let handle = unsafe { OpenProcess(PROCESS_SYNCHRONIZE | PROCESS_TERMINATE, 0, pid) };
            Ok(ProcessHandle {
                process: OwnedHandle::new(handle)?,
            })
        }

        /// Waits up to `timeout` for the process to exit; true if it has.
        pub fn wait(&self, timeout: Duration) -> bool {
            // Capped below u32::MAX, which WaitForSingleObject reads as
            // INFINITE - an over-long timeout must not become no timeout.
            let millis = u32::try_from(timeout.as_millis()).unwrap_or(u32::MAX - 1);
            // SAFETY: the process handle is valid and has SYNCHRONIZE access.
            unsafe { WaitForSingleObject(self.process.0, millis) == WAIT_OBJECT_0 }
        }

        pub fn terminate(&self) -> io::Result<()> {
            // SAFETY: the process handle is valid and has TERMINATE access.
            check(unsafe { TerminateProcess(self.process.0, FORCED_EXIT_CODE) })
        }
    }
}

/// Unix process groups (ESR-0061 WP2b, EBG-0162, EIP-ESR0061-002 Section 6.2).
///
/// The host spawns the backend as a process-group leader (`process_group(0)`),
/// so the group is the whole tree: PyInstaller's resident bootloader and the
/// interpreter it forks (the bootloader creates no group of its own). The host
/// holds the leader's `Child` until it is reaped, so the leader's PID cannot be
/// reused while `killpg` can still be called. A host `SIGKILL` cannot run any
/// of this - the backend's orphan watchdog covers that case.
#[cfg(unix)]
mod process_tree {
    use std::io;
    use std::time::{Duration, Instant};

    fn check(rc: libc::c_int) -> io::Result<()> {
        if rc == 0 {
            Ok(())
        } else {
            Err(io::Error::last_os_error())
        }
    }

    fn pid_of(pid: u32) -> io::Result<libc::pid_t> {
        libc::pid_t::try_from(pid).map_err(|_| io::Error::other("PID out of range"))
    }

    pub struct ProcessTree {
        pgid: libc::pid_t,
    }

    impl ProcessTree {
        /// Fails unless `pid` really leads its own group: killing a group the
        /// backend merely belongs to would kill the host as well.
        pub fn adopt(pid: u32) -> io::Result<Self> {
            let pid = pid_of(pid)?;
            // SAFETY: getpgid takes no pointers and has no memory effects.
            let pgid = unsafe { libc::getpgid(pid) };
            if pgid < 0 {
                return Err(io::Error::last_os_error());
            }
            if pgid != pid {
                return Err(io::Error::other(
                    "backend is not a process-group leader; refusing to adopt its group",
                ));
            }
            Ok(ProcessTree { pgid })
        }

        /// True once no process remains in the group (an unreaped zombie
        /// leader still counts, so the caller reaps its child first).
        pub fn is_empty(&self) -> bool {
            // SAFETY: killpg with signal 0 only tests for existence.
            let rc = unsafe { libc::killpg(self.pgid, 0) };
            rc != 0 && io::Error::last_os_error().raw_os_error() == Some(libc::ESRCH)
        }

        pub fn terminate(&self) -> io::Result<()> {
            // SAFETY: killpg takes no pointers; the group is the backend's own.
            check(unsafe { libc::killpg(self.pgid, libc::SIGKILL) })
        }
    }

    /// The direct child (PyInstaller's bootloader for the sidecar).
    pub struct ProcessHandle {
        pid: libc::pid_t,
    }

    impl ProcessHandle {
        pub fn open(pid: u32) -> io::Result<Self> {
            let pid = pid_of(pid)?;
            // SAFETY: signal 0 only tests for existence.
            check(unsafe { libc::kill(pid, 0) })?;
            Ok(ProcessHandle { pid })
        }

        /// Whether the process is gone, polling for up to `timeout`.
        pub fn wait(&self, timeout: Duration) -> bool {
            let deadline = Instant::now() + timeout;
            loop {
                // SAFETY: signal 0 only tests for existence.
                let gone = unsafe { libc::kill(self.pid, 0) } != 0
                    && io::Error::last_os_error().raw_os_error() == Some(libc::ESRCH);
                if gone {
                    return true;
                }
                if Instant::now() >= deadline {
                    return false;
                }
                std::thread::sleep(Duration::from_millis(10));
            }
        }

        pub fn terminate(&self) -> io::Result<()> {
            // SAFETY: kill takes no pointers.
            check(unsafe { libc::kill(self.pid, libc::SIGKILL) })
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;
        use std::os::unix::process::CommandExt;
        use std::process::{Child, Command};

        /// A shell leading its own group, with a background `sleep` beside its
        /// foreground one: a two-process tree like the packaged backend's.
        fn spawn_tree() -> Child {
            Command::new("sh")
                .args(["-c", "sleep 60 & sleep 60"])
                .process_group(0)
                .spawn()
                .expect("spawn sh")
        }

        fn wait_until(mut done: impl FnMut() -> bool) -> bool {
            let deadline = Instant::now() + Duration::from_secs(5);
            while Instant::now() < deadline {
                if done() {
                    return true;
                }
                std::thread::sleep(Duration::from_millis(20));
            }
            false
        }

        #[test]
        fn terminating_the_group_ends_every_process_in_it() {
            let mut child = spawn_tree();
            let tree = ProcessTree::adopt(child.id()).expect("leader adopts");
            assert!(!tree.is_empty());

            tree.terminate().expect("killpg");

            // The leader is a zombie until reaped; reaping is the caller's job
            // (BackendHandle::shutdown does it through wait_until).
            assert!(wait_until(|| {
                let _ = child.try_wait();
                tree.is_empty()
            }));
        }

        #[test]
        fn a_process_that_does_not_lead_its_group_is_refused() {
            let mut child = Command::new("sleep")
                .arg("60")
                .spawn()
                .expect("spawn sleep");
            let result = ProcessTree::adopt(child.id());
            let _ = child.kill();
            let _ = child.wait();
            assert!(result.is_err(), "must not adopt the host's own group");
        }

        #[test]
        fn the_handle_sees_the_direct_child_end() {
            let mut child = Command::new("sleep")
                .arg("60")
                .spawn()
                .expect("spawn sleep");
            let handle = ProcessHandle::open(child.id()).expect("open");
            assert!(!handle.wait(Duration::ZERO));

            handle.terminate().expect("kill");
            let _ = child.wait();

            assert!(handle.wait(Duration::from_secs(5)));
        }
    }
}

/// Stand-in for platforms with neither job objects nor process groups.
/// Attaching always fails, so every `ProcessGuard` is empty and shutdown
/// behaves as before. Exists so the crate still builds everywhere.
#[cfg(not(any(windows, unix)))]
mod process_tree {
    use std::io;
    use std::time::Duration;

    fn unsupported() -> io::Error {
        io::Error::new(
            io::ErrorKind::Unsupported,
            "process-tree termination is not supported on this platform",
        )
    }

    pub enum ProcessTree {}

    impl ProcessTree {
        pub fn adopt(_pid: u32) -> io::Result<Self> {
            Err(unsupported())
        }

        pub fn is_empty(&self) -> bool {
            match *self {}
        }

        pub fn terminate(&self) -> io::Result<()> {
            match *self {}
        }
    }

    pub enum ProcessHandle {}

    impl ProcessHandle {
        pub fn open(_pid: u32) -> io::Result<Self> {
            Err(unsupported())
        }

        pub fn wait(&self, _timeout: Duration) -> bool {
            match *self {}
        }

        pub fn terminate(&self) -> io::Result<()> {
            match *self {}
        }
    }
}

struct BackendProcess {
    handle: BackendHandle,
    /// Job object and process handle for ending the whole tree (EBG-0154).
    guard: ProcessGuard,
    next_id: u64,
    pending: PendingMap,
    /// Identifies which spawned process this is (ESR-0059 WP1). A reader
    /// thread or a failed call only ever tears down the process it belongs
    /// to - never a newer one spawned after it, which a stale reader's EOF
    /// handling would otherwise silently drop (and orphan).
    generation: u64,
}

impl BackendProcess {
    /// Ends this backend's whole process tree. Must not be called while the
    /// shared-state lock is held - see `BackendHandle::shutdown()`.
    fn shut_down(self) {
        self.handle.shutdown(self.guard);
    }
}

static NEXT_GENERATION: AtomicU64 = AtomicU64::new(1);

fn next_generation() -> u64 {
    NEXT_GENERATION.fetch_add(1, Ordering::Relaxed)
}

/// True only when the currently-held backend is the one identified by
/// `generation` - the pure decision behind `tear_down_if_current()`, kept
/// separate so it is unit-testable without spawning a real process.
fn is_current_generation(current: Option<u64>, generation: u64) -> bool {
    current == Some(generation)
}

/// Tears down the shared backend state, and terminates its process, only if
/// it is still the process identified by `generation` (ESR-0059 WP1).
///
/// Previously every teardown path set the shared state to `None` without
/// killing the child: `std::process::Child` does not terminate on drop, so a
/// malformed-output teardown left the old Python process running (holding
/// the SQLite stores and possibly mid-provider-call) while the next call
/// spawned a second one. It also never checked which process it was tearing
/// down, so a stale reader reaching EOF after a respawn could drop the new,
/// healthy backend instead of its own.
fn tear_down_if_current(shared_state: &SharedBackend, generation: u64) {
    let Ok(mut guard) = shared_state.lock() else {
        return;
    };
    let current = guard.as_ref().map(|backend| backend.generation);
    if !is_current_generation(current, generation) {
        return;
    }
    let backend = guard.take();
    // Released before shutting down (EIP-ESR0060-002 Section 4B): the
    // graceful wait can take up to BACKEND_SHUTDOWN_GRACE, and a request
    // arriving meanwhile must be able to spawn its replacement at once.
    drop(guard);
    if let Some(backend) = backend {
        backend.shut_down();
    }
}

struct BackendState(SharedBackend);

const MALFORMED_RESPONSE_MESSAGE: &str =
    "Malformed response from JARVIS backend. The next request will attempt to restart it.";
const CONNECTION_CLOSED_MESSAGE: &str =
    "JARVIS backend closed the connection unexpectedly. The next request will attempt to restart it.";

fn fail_all_pending(pending: &PendingMap, message: &str) {
    let mut pending_guard = pending
        .lock()
        .unwrap_or_else(|poisoned| poisoned.into_inner());
    for (_, sender) in pending_guard.drain() {
        let _ = sender.send(Err(message.to_string()));
    }
}

/// Drops a single pending call's entry (EBG-0109 Finding 2(c) timeout cleanup).
/// If the backend's response for this id ever does arrive afterwards,
/// dispatch_line()'s existing "no pending call for this id" branch already
/// drops it safely - removing the entry here is what makes that the case,
/// rather than leaving a sender nothing will ever receive from.
fn remove_pending(pending: &PendingMap, id: u64) {
    pending
        .lock()
        .unwrap_or_else(|poisoned| poisoned.into_inner())
        .remove(&id);
}

/// What to do after processing one line of backend output.
enum LineOutcome {
    Continue,
    TearDown,
}

/// Routes one already-parsed JSON-RPC response (a line carrying an `id` key)
/// to its matching pending call, if one is still waiting. Extracted from
/// dispatch_line() so this path is unit-testable without a full `AppHandle`
/// (only needed by dispatch_line's other, notification branch) - in
/// particular EBG-0109's "a late response arrives after timeout cleanup
/// already removed the pending entry" case, which must be a harmless no-op.
fn route_response(id: u64, parsed: &Value, pending: &PendingMap) {
    let sender = {
        let mut pending_guard = pending
            .lock()
            .unwrap_or_else(|poisoned| poisoned.into_inner());
        pending_guard.remove(&id)
    };
    if let Some(sender) = sender {
        let result = if let Some(error) = parsed.get("error") {
            let message = error
                .get("message")
                .and_then(Value::as_str)
                .unwrap_or("Unknown JARVIS backend error.");
            Err(message.to_string())
        } else {
            parsed
                .get("result")
                .cloned()
                .ok_or_else(|| "JARVIS backend response was missing a result.".to_string())
        };
        let _ = sender.send(result);
    }
    // No pending call for this id: nothing is waiting - a stale or unexpected
    // id, e.g. one EBG-0109's client-side timeout cleanup already removed -
    // nothing to route to.
}

/// Classifies and routes a single already-trimmed, non-empty line of backend
/// stdout - shared by both the dev (synchronous `BufReader`) and sidecar
/// (async `CommandEvent`) reader implementations, so the JSON-RPC
/// response/notification handling logic (EIP-ESR0031-002) is written once.
fn dispatch_line(trimmed: &str, pending: &PendingMap, app_handle: &AppHandle) -> LineOutcome {
    let parsed: Value = match serde_json::from_str(trimmed) {
        Ok(value) => value,
        Err(_) => {
            // Cannot tell whether this unparsable line was meant to be a
            // response or a notification - no id can be recovered from
            // invalid JSON. Treat as connection-level corruption rather
            // than guessing which single pending call (if any) it
            // belonged to (EIP-ESR0031-002 Implementation Requirement 3).
            fail_all_pending(pending, MALFORMED_RESPONSE_MESSAGE);
            return LineOutcome::TearDown;
        }
    };

    match parsed.get("id") {
        Some(id_value) => {
            // A response - JSON-RPC responses always carry an `id` key,
            // even when its value is null. Route to the matching
            // pending call if one is still waiting.
            if let Some(id) = id_value.as_u64() {
                route_response(id, &parsed, pending);
            }
        }
        None => {
            // No `id` key at all - a genuine notification.
            let method = parsed
                .get("method")
                .and_then(Value::as_str)
                .unwrap_or("")
                .to_string();
            let params = parsed.get("params").cloned().unwrap_or_else(|| json!({}));
            let _ = app_handle.emit(
                "jarvis://notification",
                json!({"method": method, "params": params}),
            );
        }
    }

    LineOutcome::Continue
}

/// Dev-mode background reader: continuously reads lines from the child's
/// stdout via a synchronous `BufReader`. Runs until stdout closes (EOF), a
/// read error occurs, or a line fails to parse - each of which tears down the
/// shared backend state so the next call respawns a fresh process.
fn run_dev_reader(
    stdout: ChildStdout,
    pending: PendingMap,
    shared_state: SharedBackend,
    app_handle: AppHandle,
    generation: u64,
) {
    let mut reader = BufReader::new(stdout);
    loop {
        let mut line = String::new();
        match reader.read_line(&mut line) {
            Ok(0) => {
                fail_all_pending(&pending, CONNECTION_CLOSED_MESSAGE);
                tear_down_if_current(&shared_state, generation);
                break;
            }
            Err(_) => {
                fail_all_pending(&pending, CONNECTION_CLOSED_MESSAGE);
                tear_down_if_current(&shared_state, generation);
                break;
            }
            Ok(_) => {
                let trimmed = line.trim();
                if trimmed.is_empty() {
                    continue;
                }
                if let LineOutcome::TearDown = dispatch_line(trimmed, &pending, &app_handle) {
                    tear_down_if_current(&shared_state, generation);
                    break;
                }
            }
        }
    }
}

/// Sidecar background reader: consumes `tauri-plugin-shell`'s async
/// `CommandEvent` channel from a plain spawned thread via `blocking_recv()`.
/// Each `CommandEvent::Stdout` payload is already one line (the plugin
/// line-buffers internally), so no additional buffering is needed here.
/// `CommandEvent::Terminated`/channel closure is treated the same as EOF on
/// the dev path; `CommandEvent::Error` is treated the same as a read error.
fn run_sidecar_reader(
    mut receiver: tokio::sync::mpsc::Receiver<CommandEvent>,
    pending: PendingMap,
    shared_state: SharedBackend,
    app_handle: AppHandle,
    generation: u64,
) {
    loop {
        match receiver.blocking_recv() {
            None => {
                fail_all_pending(&pending, CONNECTION_CLOSED_MESSAGE);
                tear_down_if_current(&shared_state, generation);
                break;
            }
            Some(CommandEvent::Stdout(bytes)) => {
                let line = String::from_utf8_lossy(&bytes);
                let trimmed = line.trim();
                if trimmed.is_empty() {
                    continue;
                }
                if let LineOutcome::TearDown = dispatch_line(trimmed, &pending, &app_handle) {
                    tear_down_if_current(&shared_state, generation);
                    break;
                }
            }
            Some(CommandEvent::Error(_)) | Some(CommandEvent::Terminated(_)) => {
                fail_all_pending(&pending, CONNECTION_CLOSED_MESSAGE);
                tear_down_if_current(&shared_state, generation);
                break;
            }
            Some(CommandEvent::Stderr(_)) => {
                // Backend stderr is not part of the JSON-RPC stream - the dev
                // path inherits stderr straight to the parent's own stderr
                // (Stdio::inherit()); the sidecar path has no equivalent
                // passthrough, so stderr lines are simply not forwarded
                // anywhere. Not a regression in observable RPC behaviour.
            }
            _ => {}
        }
    }
}

fn spawn_backend(
    app_handle: &AppHandle,
    shared_state: SharedBackend,
) -> Result<BackendProcess, String> {
    if cfg!(debug_assertions) {
        spawn_dev_backend(app_handle, shared_state)
    } else if cfg!(unix) {
        spawn_unix_sidecar_backend(app_handle, shared_state)
    } else {
        spawn_sidecar_backend(app_handle, shared_state)
    }
}

/// Environment variable carrying the host's PID to the backend, whose orphan
/// watchdog (`jarvis/interfaces/orphan_watchdog.py`, ESR-0061 WP2b) ends the
/// backend if the host disappears.
const HOST_PID_ENV: &str = "JARVIS_HOST_PID";

fn spawn_dev_backend(
    app_handle: &AppHandle,
    shared_state: SharedBackend,
) -> Result<BackendProcess, String> {
    // `jarvis` is not pip-installed in this dev setup - `python -m jarvis` only
    // resolves it via the cwd-based sys.path entry `-m` adds, so the child
    // process's working directory must be anchored to the repository root
    // (this crate's parent directory) regardless of where `cargo run`/`tauri
    // dev` itself was launched from. CARGO_MANIFEST_DIR is a compile-time
    // constant (this crate's directory, `src-tauri/`), not launch-time state.
    let repo_root = Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .ok_or_else(|| "Failed to resolve repository root from CARGO_MANIFEST_DIR.".to_string())?;

    let mut command = Command::new("python");
    command
        .args(["-m", "jarvis", "--ipc-stdio"])
        .current_dir(repo_root);
    spawn_child_backend(command, app_handle, shared_state)
}

/// Starts `command` as the backend and wires its pipes to a reader thread.
/// Shared by the dev backend and, on Unix, the packaged sidecar (ESR-0061
/// WP2b): both are plain `std::process::Child` processes, so the host holds
/// the child handle from spawn and, on Unix, can make the child a process-
/// group leader before it runs - which `tauri-plugin-shell` cannot do, and
/// which `setpgid` cannot do after `exec` (EIP-ESR0061-002 Section 6.2).
fn spawn_child_backend(
    mut command: Command,
    app_handle: &AppHandle,
    shared_state: SharedBackend,
) -> Result<BackendProcess, String> {
    command
        .env(HOST_PID_ENV, std::process::id().to_string())
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::inherit());
    #[cfg(unix)]
    command.process_group(0);
    let mut child = command
        .spawn()
        .map_err(|e| format!("Failed to start JARVIS backend process: {e}"))?;
    // Immediately, so the job takes the venv launcher's real interpreter.
    let guard = ProcessGuard::attach(child.id());

    let stdin = child
        .stdin
        .take()
        .ok_or_else(|| "Failed to open JARVIS backend stdin.".to_string())?;
    let stdout = child
        .stdout
        .take()
        .ok_or_else(|| "Failed to open JARVIS backend stdout.".to_string())?;

    let pending: PendingMap = Arc::new(Mutex::new(HashMap::new()));

    let generation = next_generation();
    let reader_pending = Arc::clone(&pending);
    let reader_app_handle = app_handle.clone();
    thread::spawn(move || {
        run_dev_reader(
            stdout,
            reader_pending,
            shared_state,
            reader_app_handle,
            generation,
        )
    });

    Ok(BackendProcess {
        handle: BackendHandle::Dev { child, stdin },
        guard,
        next_id: 1,
        pending,
        generation,
    })
}

/// Where Tauri places an `externalBin` sidecar: beside the application
/// executable (`Contents/MacOS/` in a macOS bundle), under its plain name -
/// the target triple is dropped at bundle time.
fn unix_sidecar_path() -> Result<std::path::PathBuf, String> {
    let exe = std::env::current_exe()
        .map_err(|e| format!("Failed to locate the JARVIS application: {e}"))?;
    let dir = exe
        .parent()
        .ok_or_else(|| "The JARVIS application has no parent directory.".to_string())?;
    Ok(dir.join("jarvis-backend"))
}

/// Unix packaged sidecar (ESR-0061 WP2b, EBG-0162): spawned directly, in its
/// own process group, so the whole tree - PyInstaller's resident bootloader
/// and the interpreter it forks - can be ended with one `killpg`.
fn spawn_unix_sidecar_backend(
    app_handle: &AppHandle,
    shared_state: SharedBackend,
) -> Result<BackendProcess, String> {
    spawn_child_backend(Command::new(unix_sidecar_path()?), app_handle, shared_state)
}

fn spawn_sidecar_backend(
    app_handle: &AppHandle,
    shared_state: SharedBackend,
) -> Result<BackendProcess, String> {
    let sidecar_command = app_handle
        .shell()
        .sidecar("jarvis-backend")
        .map_err(|e| format!("Failed to resolve JARVIS backend sidecar: {e}"))?
        .env(HOST_PID_ENV, std::process::id().to_string());

    let (receiver, child) = sidecar_command
        .spawn()
        .map_err(|e| format!("Failed to start JARVIS backend sidecar: {e}"))?;
    // Immediately, so the job takes PyInstaller's real interpreter, which the
    // bootloader starts only after unpacking its archive.
    let guard = ProcessGuard::attach(child.pid());

    let pending: PendingMap = Arc::new(Mutex::new(HashMap::new()));

    let generation = next_generation();
    let reader_pending = Arc::clone(&pending);
    let reader_app_handle = app_handle.clone();
    thread::spawn(move || {
        run_sidecar_reader(
            receiver,
            reader_pending,
            shared_state,
            reader_app_handle,
            generation,
        )
    });

    Ok(BackendProcess {
        handle: BackendHandle::Sidecar { child },
        guard,
        next_id: 1,
        pending,
        generation,
    })
}

/// Blocking JSON-RPC round trip to the backend. Must never run on Tauri's
/// main thread - every command reaches it through
/// `call_backend_off_main_thread()` (ESR-0059 WP1).
fn call_backend(
    shared_state: &SharedBackend,
    app_handle: &AppHandle,
    method: &str,
    params: Value,
) -> Result<Value, String> {
    let (id, generation, pending, write_result, receiver) = {
        let mut guard = shared_state
            .lock()
            .map_err(|_| "JARVIS backend state lock was poisoned by a prior panic.".to_string())?;

        if guard.is_none() {
            *guard = Some(spawn_backend(app_handle, Arc::clone(shared_state))?);
        }

        let backend = guard.as_mut().expect("just ensured Some above");
        let id = backend.next_id;
        backend.next_id += 1;

        let (tx, rx) = mpsc::channel();
        backend
            .pending
            .lock()
            .unwrap_or_else(|poisoned| poisoned.into_inner())
            .insert(id, tx);

        let request = json!({"jsonrpc": "2.0", "id": id, "method": method, "params": params});
        let line = format!("{request}\n");
        let write_result = backend.handle.write_line(&line);

        // Captured while the lock is held, so every cleanup path below acts
        // on *this* call's own process and pending map (ESR-0059 WP1) - never
        // on whichever process happens to be current by the time it runs.
        // Request ids restart at 1 per process, so re-reading the current
        // backend's pending map later could remove a newer process's live
        // entry with the same id.
        (
            id,
            backend.generation,
            Arc::clone(&backend.pending),
            write_result,
            rx,
        )
    };

    if write_result.is_err() {
        // The write itself failed - no response will ever arrive for this id.
        // Remove our own pending entry and tear down (and terminate) this
        // process so the next call attempts a fresh spawn.
        remove_pending(&pending, id);
        tear_down_if_current(shared_state, generation);
        return Err(
            "JARVIS backend is unavailable (write failed). The next request will attempt to restart it."
                .to_string(),
        );
    }

    match receiver.recv_timeout(BACKEND_CALL_TIMEOUT) {
        Ok(result) => result,
        Err(mpsc::RecvTimeoutError::Timeout) => {
            // Deliberately does not tear down or respawn the backend: the
            // process may still be genuinely working (e.g. a slow model), and
            // a late response arriving after this cleanup is already handled
            // safely by dispatch_line()'s "no pending call for this id" branch.
            remove_pending(&pending, id);
            Err(BACKEND_TIMEOUT_MESSAGE.to_string())
        }
        Err(mpsc::RecvTimeoutError::Disconnected) => {
            Err("JARVIS backend connection was lost while waiting for a response.".to_string())
        }
    }
}

/// Runs `call_backend()` on Tauri's blocking thread pool (ESR-0059 WP1).
///
/// Every command below was previously a plain synchronous `fn`, which Tauri 2
/// executes on the main thread - so `call_backend()`'s up-to-120s
/// `recv_timeout` froze the whole window (the OS's own "Not Responding"
/// state) for as long as a slow provider call or failover took. EBG-0109's
/// timeout bounded that freeze; this removes it.
async fn call_backend_off_main_thread(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    method: &'static str,
    params: Value,
) -> Result<Value, String> {
    let shared_state = Arc::clone(&state.0);
    tauri::async_runtime::spawn_blocking(move || {
        call_backend(&shared_state, &app_handle, method, params)
    })
    .await
    .map_err(|e| format!("JARVIS backend call could not be scheduled: {e}"))?
}

#[tauri::command]
async fn send_message(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    message: String,
) -> Result<Value, String> {
    call_backend_off_main_thread(
        state,
        app_handle,
        "guardian.converse",
        json!({ "message": message }),
    )
    .await
}

/// Claude escalation (ESR-0061 WP3b, EIP-ESR0061-003 6.5): an offer for a
/// message the person chose ("Ask Claude").
#[tauri::command]
async fn offer_escalation(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    message: String,
) -> Result<Value, String> {
    call_backend_off_main_thread(
        state,
        app_handle,
        "guardian.escalation.offer",
        json!({ "message": message }),
    )
    .await
}

/// Sends an offered question to Claude, after the person confirmed it.
#[tauri::command]
async fn escalate_message(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    token: String,
) -> Result<Value, String> {
    call_backend_off_main_thread(
        state,
        app_handle,
        "guardian.escalate",
        json!({ "token": token }),
    )
    .await
}

#[tauri::command]
async fn provider_status(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "provider.status", json!({})).await
}

/// Administrator only (the backend enforces it): whether a profile's retained
/// memory may accompany a question sent to Claude.
#[tauri::command]
async fn set_profile_cloud_memory(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    profile_id: String,
    enabled: bool,
) -> Result<Value, String> {
    call_backend_off_main_thread(
        state,
        app_handle,
        "profile.setCloudMemory",
        json!({ "profileId": profile_id, "enabled": enabled }),
    )
    .await
}

/// Local model setup (ESR-0061 WP3c, EIP-ESR0061-003 6.9). The backend does the
/// work and enforces who may download or change the model; these only relay.
#[tauri::command]
async fn ollama_status(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "ollama.status", json!({})).await
}

#[tauri::command]
async fn ollama_recommendation(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "ollama.recommendation", json!({})).await
}

/// Starts a background download of a catalog model; progress arrives as
/// `ollama.pullProgress` notifications. The backend refuses any other name.
#[tauri::command]
async fn ollama_pull(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    model: String,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "ollama.pull", json!({ "model": model })).await
}

#[tauri::command]
async fn ollama_cancel_pull(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "ollama.cancelPull", json!({})).await
}

#[tauri::command]
async fn ollama_use_model(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    model: String,
) -> Result<Value, String> {
    call_backend_off_main_thread(
        state,
        app_handle,
        "ollama.useModel",
        json!({ "model": model }),
    )
    .await
}

/// The one page JARVIS will open for the person: Ollama's download page. A
/// fixed address, never one the UI supplies, so this cannot be made to open
/// anything else. JARVIS does not download or run the installer itself.
const OLLAMA_DOWNLOAD_URL: &str = "https://ollama.com/download";

fn open_in_default_browser(url: &str) -> std::io::Result<()> {
    #[cfg(target_os = "windows")]
    let mut command = {
        use std::os::windows::process::CommandExt;
        const CREATE_NO_WINDOW: u32 = 0x0800_0000;
        let mut command = Command::new("rundll32");
        command
            .args(["url.dll,FileProtocolHandler", url])
            .creation_flags(CREATE_NO_WINDOW);
        command
    };
    #[cfg(target_os = "macos")]
    let mut command = {
        let mut command = Command::new("open");
        command.arg(url);
        command
    };
    #[cfg(all(unix, not(target_os = "macos")))]
    let mut command = {
        let mut command = Command::new("xdg-open");
        command.arg(url);
        command
    };
    let mut child = command.spawn()?;
    // Reap it so it cannot linger as a zombie; the opener returns at once.
    thread::spawn(move || {
        let _ = child.wait();
    });
    Ok(())
}

#[tauri::command]
fn open_ollama_download_page() -> Result<(), String> {
    open_in_default_browser(OLLAMA_DOWNLOAD_URL)
        .map_err(|e| format!("Could not open the download page: {e}"))
}

#[tauri::command]
async fn speak_message(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    text: String,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "guardian.speak", json!({ "text": text })).await
}

#[tauri::command]
async fn transcribe_audio(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    audio_base64: String,
    mime_type: String,
) -> Result<Value, String> {
    call_backend_off_main_thread(
        state,
        app_handle,
        "guardian.transcribe",
        json!({ "audioBase64": audio_base64, "mimeType": mime_type }),
    )
    .await
}

#[tauri::command]
async fn platform_status(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "platform.status", json!({})).await
}

#[tauri::command]
async fn knowledge_graph(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "knowledge.graph", json!({})).await
}

#[tauri::command]
async fn list_profiles(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "profile.list", json!({})).await
}

#[tauri::command]
async fn create_profile(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    display_name: String,
    role: String,
) -> Result<Value, String> {
    call_backend_off_main_thread(
        state,
        app_handle,
        "profile.create",
        json!({ "displayName": display_name, "role": role }),
    )
    .await
}

#[tauri::command]
async fn select_profile(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    profile_id: String,
) -> Result<Value, String> {
    call_backend_off_main_thread(
        state,
        app_handle,
        "profile.select",
        json!({ "profileId": profile_id }),
    )
    .await
}

#[tauri::command]
async fn active_profile(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "profile.active", json!({})).await
}

#[tauri::command]
async fn list_agents(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "guardian.agent.list", json!({})).await
}

#[tauri::command]
async fn invoke_agent(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    agent: String,
    task: String,
) -> Result<Value, String> {
    call_backend_off_main_thread(
        state,
        app_handle,
        "guardian.agent.invoke",
        json!({ "agent": agent, "task": task, "parameters": {} }),
    )
    .await
}

/// EBG-0131 (Memory Management UXP Surface): a record count only, never
/// full record content - matches `memory.status`'s own deliberately
/// narrow backend response shape.
#[tauri::command]
async fn memory_status(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "memory.status", json!({})).await
}

/// Lists stored memories with their content (EBG-0145, ESR-0059 WP10) - the
/// UXP asks only when the user explicitly opens the list, so memory text is
/// never on screen by default.
#[tauri::command]
async fn list_memory(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
) -> Result<Value, String> {
    call_backend_off_main_thread(state, app_handle, "memory.list", json!({})).await
}

/// Revokes one stored memory by id (EBG-0145, ESR-0059 WP10).
#[tauri::command]
async fn delete_memory(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    record_id: String,
) -> Result<Value, String> {
    call_backend_off_main_thread(
        state,
        app_handle,
        "memory.delete",
        json!({ "recordId": record_id }),
    )
    .await
}

/// `backup_dir` is a real, human-chosen directory (via the frontend's own
/// `tauri-plugin-dialog` folder picker) - the backend's `memory.backup`
/// always names the file itself (a timestamped filename inside whatever
/// directory it is given, see `PersonalMemoryService.export_backup()`), so
/// this deliberately exposes a folder picker rather than a save-file
/// picker: offering the user an exact filename the backend would then
/// silently ignore would be misleading. The written file's real path is
/// returned to the caller.
#[tauri::command]
async fn backup_memory(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    backup_dir: String,
) -> Result<Value, String> {
    call_backend_off_main_thread(
        state,
        app_handle,
        "memory.backup",
        json!({ "backupDir": backup_dir }),
    )
    .await
}

#[tauri::command]
async fn restore_memory(
    state: State<'_, BackendState>,
    app_handle: AppHandle,
    backup_path: String,
    confirm_overwrite: bool,
) -> Result<Value, String> {
    call_backend_off_main_thread(
        state,
        app_handle,
        "memory.restore",
        json!({ "backupPath": backup_path, "confirmOverwrite": confirm_overwrite }),
    )
    .await
}

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .manage(BackendState(Arc::new(Mutex::new(None))))
        .invoke_handler(tauri::generate_handler![
            send_message,
            offer_escalation,
            escalate_message,
            provider_status,
            set_profile_cloud_memory,
            ollama_status,
            ollama_recommendation,
            ollama_pull,
            ollama_cancel_pull,
            ollama_use_model,
            open_ollama_download_page,
            speak_message,
            transcribe_audio,
            platform_status,
            knowledge_graph,
            list_profiles,
            create_profile,
            select_profile,
            active_profile,
            list_agents,
            invoke_agent,
            memory_status,
            list_memory,
            delete_memory,
            backup_memory,
            restore_memory
        ])
        .build(tauri::generate_context!())
        .expect("error while building JARVIS Guardian desktop shell")
        .run(|app_handle, event| {
            // End the backend's whole process tree on app exit: gracefully,
            // then by force after BACKEND_SHUTDOWN_GRACE (EBG-0154,
            // EIP-ESR0060-002). A killed or crashed host is covered too, on
            // Windows: the OS closes the job handle, and the job's
            // KILL_ON_JOB_CLOSE limit ends the tree. This wait runs on the
            // main thread, normally after the last window has closed (Section
            // 4C). Crash/restart policy remains deferred to EBG-0050. The
            // reader thread is not explicitly joined - as a plain spawned
            // thread, it is terminated by the OS along with the rest of the
            // process, equivalent to a daemon thread.
            if let tauri::RunEvent::Exit = event {
                if let Some(state) = app_handle.try_state::<BackendState>() {
                    // Taken under the lock, shut down after releasing it.
                    let backend = state.0.lock().ok().and_then(|mut guard| guard.take());
                    if let Some(backend) = backend {
                        backend.shut_down();
                    }
                }
            }
        });
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    fn empty_pending() -> PendingMap {
        Arc::new(Mutex::new(HashMap::new()))
    }

    #[test]
    fn remove_pending_drops_the_entry() {
        let pending = empty_pending();
        let (tx, _rx) = mpsc::channel();
        pending.lock().unwrap().insert(1, tx);

        remove_pending(&pending, 1);

        assert!(pending.lock().unwrap().is_empty());
    }

    #[test]
    fn remove_pending_on_an_unknown_id_is_a_no_op() {
        let pending = empty_pending();

        remove_pending(&pending, 42);

        assert!(pending.lock().unwrap().is_empty());
    }

    #[test]
    fn route_response_delivers_a_result_to_the_matching_pending_call() {
        let pending = empty_pending();
        let (tx, rx) = mpsc::channel();
        pending.lock().unwrap().insert(1, tx);
        let parsed = json!({"jsonrpc": "2.0", "id": 1, "result": {"ok": true}});

        route_response(1, &parsed, &pending);

        assert_eq!(rx.recv().unwrap(), Ok(json!({"ok": true})));
        assert!(pending.lock().unwrap().is_empty());
    }

    #[test]
    fn route_response_delivers_an_error_message_to_the_matching_pending_call() {
        let pending = empty_pending();
        let (tx, rx) = mpsc::channel();
        pending.lock().unwrap().insert(1, tx);
        let parsed =
            json!({"jsonrpc": "2.0", "id": 1, "error": {"code": -32000, "message": "boom"}});

        route_response(1, &parsed, &pending);

        assert_eq!(rx.recv().unwrap(), Err("boom".to_string()));
    }

    /// EBG-0109 Finding 2(c): simulates a response arriving for an id whose
    /// pending entry was already removed by remove_pending() (e.g. after a
    /// client-side call_backend() timeout). Must be a harmless no-op, not a
    /// panic - there is simply nothing left to route the late response to.
    #[test]
    fn route_response_after_pending_entry_already_removed_is_harmless() {
        let pending = empty_pending();
        let parsed = json!({"jsonrpc": "2.0", "id": 1, "result": {"ok": true}});

        route_response(1, &parsed, &pending);

        assert!(pending.lock().unwrap().is_empty());
    }

    #[test]
    fn is_current_generation_matches_only_the_same_process() {
        assert!(is_current_generation(Some(3), 3));
        assert!(!is_current_generation(Some(4), 3));
        assert!(!is_current_generation(None, 3));
    }

    /// Spawns a real, idle child (it blocks reading stdin) so teardown is
    /// exercised against a genuine `BackendHandle::Dev`, not a stand-in.
    /// Requires `python` on PATH - true on every CI job that runs these
    /// tests (the `rust` job installs it to build the sidecar).
    fn backend_with_generation(generation: u64) -> BackendProcess {
        let mut child = Command::new("python")
            .args(["-c", "import sys; sys.stdin.read()"])
            .stdin(Stdio::piped())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .expect("python must be on PATH for this test");
        let stdin = child.stdin.take().expect("stdin was piped");
        BackendProcess {
            handle: BackendHandle::Dev { child, stdin },
            guard: ProcessGuard::none(),
            next_id: 1,
            pending: empty_pending(),
            generation,
        }
    }

    /// ESR-0059 WP1: a stale reader (or failed call) belonging to an older
    /// process must never tear down a newer backend spawned after it.
    #[test]
    fn tear_down_leaves_a_newer_backend_in_place() {
        let shared: SharedBackend = Arc::new(Mutex::new(Some(backend_with_generation(7))));

        tear_down_if_current(&shared, 6);
        assert!(shared.lock().unwrap().is_some());

        tear_down_if_current(&shared, 7);
        assert!(shared.lock().unwrap().is_none());
    }

    #[test]
    fn tear_down_with_no_backend_is_a_no_op() {
        let shared: SharedBackend = Arc::new(Mutex::new(None));

        tear_down_if_current(&shared, 1);

        assert!(shared.lock().unwrap().is_none());
    }

    /// A real dev-path backend running `script`, for the shutdown tests.
    fn dev_backend(script: &str) -> (Child, ChildStdin) {
        let mut child = Command::new("python")
            .args(["-c", script])
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::null())
            .spawn()
            .expect("python must be on PATH for this test");
        let stdin = child.stdin.take().expect("stdin was piped");
        (child, stdin)
    }

    /// Ignores stdin EOF entirely, like a backend busy draining slow turns.
    const IGNORES_EOF: &str = "import time; time.sleep(60)";
    /// Exits as soon as stdin closes, like an idle backend.
    const EXITS_ON_EOF: &str = "import sys; sys.stdin.read()";

    /// EIP-ESR0060-002 Section 4D: with no guard at all (every non-Windows
    /// build, or a Windows build whose guard could not attach), shutdown
    /// still ends a dev child that ignores EOF - today's behaviour.
    #[test]
    fn shutdown_without_a_guard_still_ends_the_child() {
        let (child, stdin) = dev_backend(IGNORES_EOF);
        let started = Instant::now();

        // Returns only after the child has been killed and reaped.
        BackendHandle::Dev { child, stdin }.shutdown(ProcessGuard::none());

        assert!(started.elapsed() < BACKEND_SHUTDOWN_GRACE + Duration::from_secs(5));
    }

    /// The idle case: closing stdin is enough, so no force is needed and
    /// shutdown returns well before the grace period ends.
    #[test]
    fn shutdown_of_an_idle_child_returns_early() {
        let (child, stdin) = dev_backend(EXITS_ON_EOF);
        let started = Instant::now();

        BackendHandle::Dev { child, stdin }.shutdown(ProcessGuard::none());

        assert!(started.elapsed() < BACKEND_SHUTDOWN_GRACE);
    }

    /// Implementation review finding (v0.6): reaping is bounded. Even for a
    /// child that was never terminated - standing in for a forced
    /// termination that failed - `reap()` gives up after REAP_TIMEOUT
    /// (killing it on the way out) instead of blocking teardown forever.
    #[test]
    fn reap_never_blocks_forever_on_a_live_child() {
        let (mut child, _stdin) = dev_backend(IGNORES_EOF);
        let started = Instant::now();

        reap(&mut child);

        let elapsed = started.elapsed();
        assert!(elapsed >= REAP_TIMEOUT);
        assert!(elapsed < REAP_TIMEOUT + Duration::from_secs(2));
        // The parting kill() took effect.
        let _ = child.wait();
    }

    /// Section 4B: the graceful wait never holds the shared-state lock, so a
    /// request arriving while an EOF-ignoring backend is being ended can take
    /// the lock (and spawn a replacement) at once.
    #[test]
    fn tear_down_releases_the_lock_before_waiting() {
        let (child, stdin) = dev_backend(IGNORES_EOF);
        let shared: SharedBackend = Arc::new(Mutex::new(Some(BackendProcess {
            handle: BackendHandle::Dev { child, stdin },
            guard: ProcessGuard::none(),
            next_id: 1,
            pending: empty_pending(),
            generation: 9,
        })));

        let teardown_state = Arc::clone(&shared);
        let teardown = thread::spawn(move || tear_down_if_current(&teardown_state, 9));
        // Let the teardown take the backend and enter its grace wait.
        thread::sleep(Duration::from_millis(500));

        let started = Instant::now();
        let guard = shared.lock().unwrap();
        assert!(started.elapsed() < Duration::from_millis(500));
        assert!(guard.is_none());
        assert!(
            !teardown.is_finished(),
            "teardown should still be in its grace wait"
        );
        drop(guard);

        teardown.join().unwrap();
    }

    /// Windows-only: these drive real job objects (EIP-ESR0060-002 Section
    /// 4D). The CI `rust` job runs on Linux, so they run locally only.
    #[cfg(windows)]
    mod windows_process_tree {
        use super::*;
        use process_tree::{ProcessHandle, ProcessTree};

        /// A child that waits for "go" on stdin, then starts a grandchild
        /// and reports the grandchild's PID - so the grandchild is created
        /// only after the child has been adopted into the job, as
        /// PyInstaller's real interpreter is.
        const SPAWNS_GRANDCHILD: &str = "import subprocess, sys, time\n\
sys.stdin.readline()\n\
g = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\n\
print(g.pid, flush=True)\n\
time.sleep(60)";

        /// Starts the child, adopts it, then lets it start its grandchild;
        /// returns the child, its stdin, the job and a handle to the
        /// grandchild (held so its PID cannot be reused while we check it).
        fn tree_with_grandchild() -> (Child, ChildStdin, ProcessTree, ProcessHandle) {
            let (mut child, mut stdin) = dev_backend(SPAWNS_GRANDCHILD);
            let tree = ProcessTree::adopt(child.id()).expect("adopt the child");
            writeln!(stdin, "go").unwrap();
            stdin.flush().unwrap();
            let mut line = String::new();
            BufReader::new(child.stdout.take().unwrap())
                .read_line(&mut line)
                .unwrap();
            let grandchild_pid: u32 = line.trim().parse().expect("grandchild pid");
            let grandchild = ProcessHandle::open(grandchild_pid).expect("open grandchild");
            (child, stdin, tree, grandchild)
        }

        #[test]
        fn terminating_the_job_ends_child_and_grandchild() {
            let (mut child, _stdin, tree, grandchild) = tree_with_grandchild();
            assert!(!tree.is_empty());

            tree.terminate().expect("terminate the job");

            assert!(grandchild.wait(Duration::from_secs(5)));
            child.wait().unwrap();
            assert!(tree.is_empty());
        }

        /// Stands in for the host being killed: the OS closing the job handle
        /// ends the tree through KILL_ON_JOB_CLOSE.
        #[test]
        fn dropping_the_job_ends_child_and_grandchild() {
            let (mut child, _stdin, tree, grandchild) = tree_with_grandchild();

            drop(tree);

            assert!(grandchild.wait(Duration::from_secs(5)));
            child.wait().unwrap();
        }

        /// Forced path: a tree that ignores EOF is ended within the grace
        /// period plus a margin, grandchild included.
        #[test]
        fn shutdown_forces_a_tree_that_ignores_eof() {
            let (child, stdin, tree, grandchild) = tree_with_grandchild();
            let started = Instant::now();

            BackendHandle::Dev { child, stdin }.shutdown(ProcessGuard {
                tree: Some(tree),
                process: None,
            });

            let elapsed = started.elapsed();
            assert!(elapsed >= BACKEND_SHUTDOWN_GRACE);
            assert!(elapsed < BACKEND_SHUTDOWN_GRACE + Duration::from_secs(2));
            assert!(grandchild.wait(Duration::from_secs(1)));
        }

        /// Graceful path: a child that writes a marker on EOF and exits gets
        /// to do so, and shutdown returns well inside the grace period.
        #[test]
        fn shutdown_lets_an_idle_child_exit_gracefully() {
            let marker = std::env::temp_dir().join(format!(
                "jarvis-graceful-shutdown-{}.marker",
                std::process::id()
            ));
            let _ = std::fs::remove_file(&marker);
            let script = format!(
                "import sys; sys.stdin.read(); open(r'{}', 'w').write('eof')",
                marker.display()
            );
            let (child, stdin) = dev_backend(&script);
            let guard = ProcessGuard::attach(child.id());
            assert!(guard.tree.is_some() && guard.process.is_some());
            let started = Instant::now();

            BackendHandle::Dev { child, stdin }.shutdown(guard);

            assert!(started.elapsed() < BACKEND_SHUTDOWN_GRACE);
            assert!(
                marker.exists(),
                "child should have exited on EOF, not by force"
            );
            let _ = std::fs::remove_file(&marker);
        }

        /// No job, but a held handle: the early return still works, rather
        /// than a blind sleep through the whole grace period.
        #[test]
        fn shutdown_without_a_job_returns_early_via_the_handle() {
            let (child, stdin) = dev_backend(EXITS_ON_EOF);
            let process = ProcessHandle::open(child.id()).unwrap();
            let started = Instant::now();

            BackendHandle::Dev { child, stdin }.shutdown(ProcessGuard {
                tree: None,
                process: Some(process),
            });

            assert!(started.elapsed() < BACKEND_SHUTDOWN_GRACE);
        }

        /// No job, held handle, EOF ignored: forced through the handle.
        #[test]
        fn shutdown_without_a_job_forces_through_the_handle() {
            let (child, stdin) = dev_backend(IGNORES_EOF);
            let pid = child.id();
            let process = ProcessHandle::open(pid).unwrap();
            let observer = ProcessHandle::open(pid).unwrap();

            BackendHandle::Dev { child, stdin }.shutdown(ProcessGuard {
                tree: None,
                process: Some(process),
            });

            assert!(observer.wait(Duration::from_secs(1)));
        }

        /// Section 4D, corrected at design review v0.4: OpenProcess on PID 0,
        /// the System Idle Process, is documented to fail at every privilege
        /// level - a genuine attach failure with no timing involved.
        #[test]
        fn adopting_pid_zero_fails_and_attach_degrades() {
            assert!(ProcessTree::adopt(0).is_err());
            assert!(ProcessHandle::open(0).is_err());

            let guard = ProcessGuard::attach(0);
            assert!(guard.is_empty());
        }

        /// Live check (b) of EIP-ESR0060-002 Section 5, against the real
        /// packaged sidecar: a backend torn down while a slow turn is in
        /// flight - the case EBG-0154 found surviving teardown - is ended,
        /// whole tree, within the grace period. Ignored by default: it needs
        /// a built sidecar, named by JARVIS_LIVE_SIDECAR. Run with
        /// `cargo test -- --ignored live_packaged_sidecar --nocapture`.
        #[test]
        #[ignore = "needs a packaged sidecar: set JARVIS_LIVE_SIDECAR"]
        fn live_packaged_sidecar_busy_tree_is_ended_within_the_grace() {
            let sidecar = std::env::var("JARVIS_LIVE_SIDECAR").expect("set JARVIS_LIVE_SIDECAR");
            let scratch = std::env::temp_dir().join(format!("jarvis-live-{}", std::process::id()));
            std::fs::create_dir_all(&scratch).unwrap();
            let mut child = Command::new(sidecar)
                // Isolated stores, and an Ollama endpoint that never answers,
                // so the turn stays in flight on the slow lane.
                .env("JARVIS_MEMORY_DB_PATH", scratch.join("personal.db"))
                .env("JARVIS_IDENTITY_DB_PATH", scratch.join("identity.db"))
                .env("JARVIS_LOG_DIR", scratch.join("logs"))
                .env("JARVIS_OLLAMA_ENDPOINT", "http://10.255.255.1:11434")
                .env_remove("OPENAI_API_KEY")
                .env_remove("GEMINI_API_KEY")
                .stdin(Stdio::piped())
                .stdout(Stdio::piped())
                .stderr(Stdio::null())
                .spawn()
                .expect("start the packaged sidecar");
            let guard = ProcessGuard::attach(child.id());
            assert!(
                guard.tree.is_some(),
                "job object must attach to the sidecar"
            );
            let mut stdin = child.stdin.take().unwrap();
            let mut stdout = BufReader::new(child.stdout.take().unwrap());

            writeln!(
                stdin,
                r#"{{"jsonrpc":"2.0","id":1,"method":"platform.status","params":{{}}}}"#
            )
            .unwrap();
            stdin.flush().unwrap();
            let mut line = String::new();
            loop {
                line.clear();
                stdout.read_line(&mut line).unwrap();
                if line.contains("\"id\": 1") || line.contains("\"id\":1") {
                    break;
                }
            }
            // The real interpreter must have been caught by the job despite
            // the spawn-to-adopt gap (Section 4G): bootloader plus child.
            let active = guard.tree.as_ref().unwrap().active_processes().unwrap();
            println!("processes in the job once the backend answered: {active}");
            assert!(
                active >= 2,
                "PyInstaller's real interpreter escaped the job"
            );

            writeln!(stdin, r#"{{"jsonrpc":"2.0","id":2,"method":"guardian.converse","params":{{"message":"hello"}}}}"#).unwrap();
            stdin.flush().unwrap();
            thread::sleep(Duration::from_secs(2));

            let started = Instant::now();
            BackendHandle::Dev { child, stdin }.shutdown(guard);
            let elapsed = started.elapsed();
            println!("busy packaged backend shut down in {elapsed:?}");
            assert!(elapsed < BACKEND_SHUTDOWN_GRACE + Duration::from_secs(2));
            let _ = std::fs::remove_dir_all(&scratch);
        }
    }
}
