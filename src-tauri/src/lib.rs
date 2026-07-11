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

use serde_json::{json, Value};
use std::io::{BufRead, BufReader, Write};
use std::process::{Child, ChildStdin, ChildStdout, Command, Stdio};
use std::sync::Mutex;
use tauri::{Manager, State};

struct BackendProcess {
    child: Child,
    stdin: ChildStdin,
    stdout: BufReader<ChildStdout>,
    next_id: u64,
}

struct BackendState(Mutex<Option<BackendProcess>>);

fn spawn_backend() -> Result<BackendProcess, String> {
    let mut child = Command::new("python")
        .args(["-m", "jarvis", "--ipc-stdio"])
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

    Ok(BackendProcess {
        child,
        stdin,
        stdout: BufReader::new(stdout),
        next_id: 1,
    })
}

fn call_backend(state: &BackendState, method: &str, params: Value) -> Result<Value, String> {
    let mut guard = state
        .0
        .lock()
        .map_err(|_| "JARVIS backend state lock was poisoned by a prior panic.".to_string())?;

    if guard.is_none() {
        *guard = Some(spawn_backend()?);
    }

    let backend = guard.as_mut().expect("just ensured Some above");
    let id = backend.next_id;
    backend.next_id += 1;

    let request = json!({"jsonrpc": "2.0", "id": id, "method": method, "params": params});
    let line = format!("{request}\n");

    if backend.stdin.write_all(line.as_bytes()).is_err() || backend.stdin.flush().is_err() {
        *guard = None;
        return Err(
            "JARVIS backend is unavailable (write failed). The next request will attempt to restart it."
                .to_string(),
        );
    }

    let mut response_line = String::new();
    match backend.stdout.read_line(&mut response_line) {
        Ok(0) => {
            // EOF: the child closed its stdout, meaning it has exited.
            *guard = None;
            return Err(
                "JARVIS backend closed the connection unexpectedly. The next request will attempt to restart it."
                    .to_string(),
            );
        }
        Err(e) => {
            *guard = None;
            return Err(format!(
                "JARVIS backend read failed: {e}. The next request will attempt to restart it."
            ));
        }
        Ok(_) => {}
    }

    let response: Value = match serde_json::from_str(response_line.trim()) {
        Ok(value) => value,
        Err(e) => {
            // A malformed line means the stdio framing can no longer be trusted
            // for this process - clear state so the next call restarts it,
            // matching the write/EOF/read failure handling above.
            *guard = None;
            return Err(format!("Malformed response from JARVIS backend: {e}. The next request will attempt to restart it."));
        }
    };

    if let Some(error) = response.get("error") {
        let message = error
            .get("message")
            .and_then(Value::as_str)
            .unwrap_or("Unknown JARVIS backend error.");
        return Err(message.to_string());
    }

    response
        .get("result")
        .cloned()
        .ok_or_else(|| "JARVIS backend response was missing a result.".to_string())
}

#[tauri::command]
fn send_message(state: State<BackendState>, message: String) -> Result<Value, String> {
    call_backend(&state, "guardian.converse", json!({ "message": message }))
}

#[tauri::command]
fn platform_status(state: State<BackendState>) -> Result<Value, String> {
    call_backend(&state, "platform.status", json!({}))
}

#[tauri::command]
fn knowledge_graph(state: State<BackendState>) -> Result<Value, String> {
    call_backend(&state, "knowledge.graph", json!({}))
}

pub fn run() {
    tauri::Builder::default()
        .manage(BackendState(Mutex::new(None)))
        .invoke_handler(tauri::generate_handler![send_message, platform_status, knowledge_graph])
        .build(tauri::generate_context!())
        .expect("error while building JARVIS Guardian desktop shell")
        .run(|app_handle, event| {
            // Terminate the backend child process on app exit where possible -
            // best-effort cleanup, not a guarantee against every ungraceful
            // termination path (e.g. a killed parent process). Full
            // crash/restart policy remains deferred to EBG-0050.
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
