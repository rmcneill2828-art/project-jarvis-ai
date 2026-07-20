//! Tauri sidecar process management and commands for the JARVIS UXP-backend
//! bridge (ADR-0019, ESR-0017 WP9 - foundation scope).
//!
//! `std::process::Command` with piped stdio is used directly here rather than
//! `tauri-plugin-shell`'s bundled-binary "sidecar" packaging - this is
//! explicitly dev-mode process spawn only, not production packaging.
//! `tauri-plugin-shell` and Tauri v2 capability/permission handling for a
//! bundled binary remain EBG-0050 work, not this foundation.
//!
//! The Python backend process is spawned once (lazily, on first use) and
//! reused across calls, not respawned per request. If it becomes unavailable
//! (write/read failure, malformed response, closed pipe), the error is
//! surfaced to the caller and the process handle is dropped so the *next*
//! call attempts a fresh spawn - there is no silent fallback to mock data.
//!
//! EIP-ESR0031-002 (Streaming Notifications MVP) restructures backend I/O
//! from a single synchronous write-then-read per call into a background
//! reader thread plus a pending-call dispatch table, so the Python backend
//! can also emit unsolicited JSON-RPC notifications (currently: a periodic
//! heartbeat) alongside ordinary request/response traffic. A line with an
//! `id` key (even `null`) is a response, routed to whichever call is
//! waiting on it; a line with no `id` key at all is a notification, forwarded
//! to the frontend via `app_handle.emit("jarvis://notification", ...)`. A
//! line that fails to parse as JSON cannot be classified either way, so it is
//! treated as connection-level corruption: every currently-pending call fails
//! with the same "malformed response" error request/response calls have
//! always used, and the connection is torn down for a fresh respawn - the
//! multi-call generalisation of the single-call teardown behaviour that
//! existed before this package.

use serde_json::{json, Value};
use std::collections::HashMap;
use std::io::{BufRead, BufReader, Write};
use std::path::Path;
use std::process::{Child, ChildStdin, ChildStdout, Command, Stdio};
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use tauri::{AppHandle, Emitter, Manager, State};

type PendingMap = Arc<Mutex<HashMap<u64, mpsc::Sender<Result<Value, String>>>>>;
type SharedBackend = Arc<Mutex<Option<BackendProcess>>>;

struct BackendProcess {
    child: Child,
    stdin: ChildStdin,
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

/// Background reader: continuously reads lines from the child's stdout,
/// dispatching each as a response (routed to the matching pending call) or a
/// notification (forwarded via `emit`). Runs until stdout closes (EOF), a
/// read error occurs, or a line fails to parse - each of which tears down the
/// shared backend state so the next call respawns a fresh process.
fn run_reader(
    stdout: ChildStdout,
    pending: PendingMap,
    shared_state: SharedBackend,
    app_handle: AppHandle,
) {
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

                let parsed: Value = match serde_json::from_str(trimmed) {
                    Ok(value) => value,
                    Err(_) => {
                        // Cannot tell whether this unparsable line was meant to be a
                        // response or a notification - no id can be recovered from
                        // invalid JSON. Treat as connection-level corruption rather
                        // than guessing which single pending call (if any) it
                        // belonged to (EIP-ESR0031-002 Implementation Requirement 3).
                        fail_all_pending(&pending, MALFORMED_RESPONSE_MESSAGE);
                        if let Ok(mut guard) = shared_state.lock() {
                            *guard = None;
                        }
                        break;
                    }
                };

                match parsed.get("id") {
                    Some(id_value) => {
                        // A response - JSON-RPC responses always carry an `id` key,
                        // even when its value is null. Route to the matching
                        // pending call if one is still waiting.
                        if let Some(id) = id_value.as_u64() {
                            let sender = {
                                let mut pending_guard =
                                    pending.lock().unwrap_or_else(|poisoned| poisoned.into_inner());
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
            }
        }
    }
}

fn spawn_backend(app_handle: &AppHandle, shared_state: SharedBackend) -> Result<BackendProcess, String> {
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
    thread::spawn(move || run_reader(stdout, reader_pending, shared_state, reader_app_handle));

    Ok(BackendProcess {
        child,
        stdin,
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
        let write_result = backend.stdin.write_all(line.as_bytes()).and_then(|_| backend.stdin.flush());

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
                        if let Some(mut backend) = guard.take() {
                            let _ = backend.child.kill();
                        }
                    }
                }
            }
        });
}
