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
use std::path::Path;
use std::process::{Child, ChildStdin, ChildStdout, Command, Stdio};
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use tauri::{AppHandle, Emitter, Manager, State};
use tauri_plugin_shell::process::{CommandChild, CommandEvent};
use tauri_plugin_shell::ShellExt;

type PendingMap = Arc<Mutex<HashMap<u64, mpsc::Sender<Result<Value, String>>>>>;
type SharedBackend = Arc<Mutex<Option<BackendProcess>>>;

/// Unifies the two possible backend handle shapes so `call_backend()` and the
/// app-exit cleanup handler do not need to duplicate write/kill logic per path.
enum BackendHandle {
    Dev { child: Child, stdin: ChildStdin },
    Sidecar { child: CommandChild },
}

impl BackendHandle {
    fn write_line(&mut self, line: &str) -> std::io::Result<()> {
        match self {
            BackendHandle::Dev { stdin, .. } => stdin.write_all(line.as_bytes()).and_then(|_| stdin.flush()),
            BackendHandle::Sidecar { child } => child
                .write(line.as_bytes())
                .map_err(|e| std::io::Error::other(e.to_string())),
        }
    }

    /// Best-effort termination on app exit - mirrors the original
    /// `backend.child.kill()` behaviour for both paths (EIP-ESR0032-001
    /// Implementation Requirement 7). Errors are intentionally swallowed:
    /// this runs during shutdown, where there is no caller left to report to.
    fn kill(self) {
        match self {
            BackendHandle::Dev { mut child, .. } => {
                let _ = child.kill();
            }
            BackendHandle::Sidecar { child } => {
                let _ = child.kill();
            }
        }
    }
}

struct BackendProcess {
    handle: BackendHandle,
    next_id: u64,
    pending: PendingMap,
}

struct BackendState(SharedBackend);

const MALFORMED_RESPONSE_MESSAGE: &str =
    "Malformed response from JARVIS backend. The next request will attempt to restart it.";
const CONNECTION_CLOSED_MESSAGE: &str =
    "JARVIS backend closed the connection unexpectedly. The next request will attempt to restart it.";

fn fail_all_pending(pending: &PendingMap, message: &str) {
    let mut pending_guard = pending.lock().unwrap_or_else(|poisoned| poisoned.into_inner());
    for (_, sender) in pending_guard.drain() {
        let _ = sender.send(Err(message.to_string()));
    }
}

/// What to do after processing one line of backend output.
enum LineOutcome {
    Continue,
    TearDown,
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
                let sender = {
                    let mut pending_guard = pending.lock().unwrap_or_else(|poisoned| poisoned.into_inner());
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
                // No pending call for this id: nothing is waiting (a
                // stale or unexpected id) - nothing to route to.
            }
        }
        None => {
            // No `id` key at all - a genuine notification.
            let method = parsed.get("method").and_then(Value::as_str).unwrap_or("").to_string();
            let params = parsed.get("params").cloned().unwrap_or_else(|| json!({}));
            let _ = app_handle.emit("jarvis://notification", json!({"method": method, "params": params}));
        }
    }

    LineOutcome::Continue
}

/// Dev-mode background reader: continuously reads lines from the child's
/// stdout via a synchronous `BufReader`. Runs until stdout closes (EOF), a
/// read error occurs, or a line fails to parse - each of which tears down the
/// shared backend state so the next call respawns a fresh process.
fn run_dev_reader(stdout: ChildStdout, pending: PendingMap, shared_state: SharedBackend, app_handle: AppHandle) {
    let mut reader = BufReader::new(stdout);
    loop {
        let mut line = String::new();
        match reader.read_line(&mut line) {
            Ok(0) => {
                fail_all_pending(&pending, CONNECTION_CLOSED_MESSAGE);
                if let Ok(mut guard) = shared_state.lock() {
                    *guard = None;
                }
                break;
            }
            Err(_) => {
                fail_all_pending(&pending, CONNECTION_CLOSED_MESSAGE);
                if let Ok(mut guard) = shared_state.lock() {
                    *guard = None;
                }
                break;
            }
            Ok(_) => {
                let trimmed = line.trim();
                if trimmed.is_empty() {
                    continue;
                }
                if let LineOutcome::TearDown = dispatch_line(trimmed, &pending, &app_handle) {
                    if let Ok(mut guard) = shared_state.lock() {
                        *guard = None;
                    }
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
) {
    loop {
        match receiver.blocking_recv() {
            None => {
                fail_all_pending(&pending, CONNECTION_CLOSED_MESSAGE);
                if let Ok(mut guard) = shared_state.lock() {
                    *guard = None;
                }
                break;
            }
            Some(CommandEvent::Stdout(bytes)) => {
                let line = String::from_utf8_lossy(&bytes);
                let trimmed = line.trim();
                if trimmed.is_empty() {
                    continue;
                }
                if let LineOutcome::TearDown = dispatch_line(trimmed, &pending, &app_handle) {
                    if let Ok(mut guard) = shared_state.lock() {
                        *guard = None;
                    }
                    break;
                }
            }
            Some(CommandEvent::Error(_)) | Some(CommandEvent::Terminated(_)) => {
                fail_all_pending(&pending, CONNECTION_CLOSED_MESSAGE);
                if let Ok(mut guard) = shared_state.lock() {
                    *guard = None;
                }
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

fn spawn_backend(app_handle: &AppHandle, shared_state: SharedBackend) -> Result<BackendProcess, String> {
    if cfg!(debug_assertions) {
        spawn_dev_backend(app_handle, shared_state)
    } else {
        spawn_sidecar_backend(app_handle, shared_state)
    }
}

fn spawn_dev_backend(app_handle: &AppHandle, shared_state: SharedBackend) -> Result<BackendProcess, String> {
    // `jarvis` is not pip-installed in this dev setup - `python -m jarvis` only
    // resolves it via the cwd-based sys.path entry `-m` adds, so the child
    // process's working directory must be anchored to the repository root
    // (this crate's parent directory) regardless of where `cargo run`/`tauri
    // dev` itself was launched from. CARGO_MANIFEST_DIR is a compile-time
    // constant (this crate's directory, `src-tauri/`), not launch-time state.
    let repo_root = Path::new(env!("CARGO_MANIFEST_DIR"))
        .parent()
        .ok_or_else(|| "Failed to resolve repository root from CARGO_MANIFEST_DIR.".to_string())?;

    let mut child = Command::new("python")
        .args(["-m", "jarvis", "--ipc-stdio"])
        .current_dir(repo_root)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::inherit())
        .spawn()
        .map_err(|e| format!("Failed to start JARVIS backend process: {e}"))?;

    let stdin = child
        .stdin
        .take()
        .ok_or_else(|| "Failed to open JARVIS backend stdin.".to_string())?;
    let stdout = child
        .stdout
        .take()
        .ok_or_else(|| "Failed to open JARVIS backend stdout.".to_string())?;

    let pending: PendingMap = Arc::new(Mutex::new(HashMap::new()));

    let reader_pending = Arc::clone(&pending);
    let reader_app_handle = app_handle.clone();
    thread::spawn(move || run_dev_reader(stdout, reader_pending, shared_state, reader_app_handle));

    Ok(BackendProcess {
        handle: BackendHandle::Dev { child, stdin },
        next_id: 1,
        pending,
    })
}

fn spawn_sidecar_backend(app_handle: &AppHandle, shared_state: SharedBackend) -> Result<BackendProcess, String> {
    let sidecar_command = app_handle
        .shell()
        .sidecar("jarvis-backend")
        .map_err(|e| format!("Failed to resolve JARVIS backend sidecar: {e}"))?;

    let (receiver, child) = sidecar_command
        .spawn()
        .map_err(|e| format!("Failed to start JARVIS backend sidecar: {e}"))?;

    let pending: PendingMap = Arc::new(Mutex::new(HashMap::new()));

    let reader_pending = Arc::clone(&pending);
    let reader_app_handle = app_handle.clone();
    thread::spawn(move || run_sidecar_reader(receiver, reader_pending, shared_state, reader_app_handle));

    Ok(BackendProcess {
        handle: BackendHandle::Sidecar { child },
        next_id: 1,
        pending,
    })
}

fn call_backend(state: &BackendState, app_handle: &AppHandle, method: &str, params: Value) -> Result<Value, String> {
    let (id, write_result, receiver) = {
        let mut guard = state
            .0
            .lock()
            .map_err(|_| "JARVIS backend state lock was poisoned by a prior panic.".to_string())?;

        if guard.is_none() {
            *guard = Some(spawn_backend(app_handle, Arc::clone(&state.0))?);
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

        (id, write_result, rx)
    };

    if write_result.is_err() {
        // The write itself failed - no response will ever arrive for this id.
        // Remove our own pending entry and reset state so the next call
        // attempts a fresh spawn, matching the pre-existing write-failure
        // semantics.
        if let Ok(mut guard) = state.0.lock() {
            if let Some(backend) = guard.as_ref() {
                backend
                    .pending
                    .lock()
                    .unwrap_or_else(|poisoned| poisoned.into_inner())
                    .remove(&id);
            }
            *guard = None;
        }
        return Err(
            "JARVIS backend is unavailable (write failed). The next request will attempt to restart it."
                .to_string(),
        );
    }

    receiver
        .recv()
        .map_err(|_| "JARVIS backend connection was lost while waiting for a response.".to_string())?
}

#[tauri::command]
fn send_message(state: State<BackendState>, app_handle: AppHandle, message: String) -> Result<Value, String> {
    call_backend(&state, &app_handle, "guardian.converse", json!({ "message": message }))
}

#[tauri::command]
fn platform_status(state: State<BackendState>, app_handle: AppHandle) -> Result<Value, String> {
    call_backend(&state, &app_handle, "platform.status", json!({}))
}

#[tauri::command]
fn knowledge_graph(state: State<BackendState>, app_handle: AppHandle) -> Result<Value, String> {
    call_backend(&state, &app_handle, "knowledge.graph", json!({}))
}

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(BackendState(Arc::new(Mutex::new(None))))
        .invoke_handler(tauri::generate_handler![send_message, platform_status, knowledge_graph])
        .build(tauri::generate_context!())
        .expect("error while building JARVIS Guardian desktop shell")
        .run(|app_handle, event| {
            // Terminate the backend child process on app exit where possible -
            // best-effort cleanup, not a guarantee against every ungraceful
            // termination path (e.g. a killed parent process). Full
            // crash/restart policy remains deferred to EBG-0050. The reader
            // thread is not explicitly joined - as a plain spawned thread, it
            // is terminated by the OS along with the rest of the process,
            // equivalent to a daemon thread.
            if let tauri::RunEvent::Exit = event {
                if let Some(state) = app_handle.try_state::<BackendState>() {
                    if let Ok(mut guard) = state.0.lock() {
                        if let Some(backend) = guard.take() {
                            backend.handle.kill();
                        }
                    }
                }
            }
        });
}
