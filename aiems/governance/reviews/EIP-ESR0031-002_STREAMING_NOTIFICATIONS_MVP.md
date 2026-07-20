# EIP-ESR0031-002 - Streaming Notifications MVP (EBG-0050 Remaining Scope)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0031-002 |
| Artefact ID | EIP-ESR0031-002 |
| Title | Streaming Notifications MVP |
| Version | 0.2 |
| Status | Draft |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0050's remaining scope, closing that portion of it) |
| Intended Session | ESR-0031 |
| Effective Date | Pending approval |

---

# 2. Purpose

EBG-0050 (UXP-Backend Bridge, Completed Foundation Scope at ESR-0017 WP9) deliberately adopted the full JSON-RPC 2.0 envelope specifically so streaming notifications could be added later without a breaking change - `jarvis/interfaces/stdio_rpc.py`'s own module docstring says so directly. That remaining scope has sat open since ESR-0017. JRM-0001 Track C names it as the natural next increment now that a production provider is genuinely wired into the default runtime (EBG-0070, ESR-0022) - the trigger it was waiting on has already happened.

Direct repository evidence, confirmed while scoping this package: `src/App.jsx`'s `useEffect` calls `invoke("platform_status")` and `invoke("knowledge_graph")` exactly once, on mount - there is no polling interval anywhere in the UXP today. This package is not replacing polling with push; it is building the UXP's *first* live-update mechanism of any kind.

---

# 3. Objective

Prove the full server-push architecture end to end - Python backend emits an unsolicited JSON-RPC notification, the Rust sidecar correctly distinguishes it from a request/response and forwards it to the frontend via Tauri's event system, and the React UXP displays it live - using one deliberately simple notification (a periodic heartbeat) as the proof, not a real business-logic-driven notification yet.

---

# 4. Repository Context

| Item | Current State |
|------|---------------|
| `jarvis/interfaces/stdio_rpc.py` | `StdioRpcServer.serve_forever()` is a strictly synchronous loop: block-read one line from `in_stream`, call the matching handler, write exactly one response line to `out_stream`. Nothing in this loop can proactively write to `out_stream` outside of directly answering the line it just read. |
| `src-tauri/src/lib.rs` | `call_backend()` writes one request line to the child's stdin, then synchronously calls `backend.stdout.read_line()` once, assuming the very next line is that request's response. There is no mechanism to distinguish an unsolicited notification line from a response line, and no background reader - if the Python side wrote a notification line at an arbitrary moment, whatever `call_backend()` call happened to be blocked in `read_line()` at that moment would wrongly consume it as its own response, corrupting that call's result. |
| `src/App.jsx` | Fetches `platform_status`/`knowledge_graph` exactly once, in a mount-only `useEffect` with `invoke()`. No polling interval, no live-update mechanism of any kind exists in the UXP today - confirmed directly, not assumed. |
| `@tauri-apps/api` (`package.json`) | Already a dependency (`^2.2.0`), includes the `event` module (`listen`) needed on the React side. No new frontend dependency required. |
| `tauri` Rust crate (`Cargo.toml`) | Already provides `AppHandle::emit()` via the `Manager` trait, already imported in `lib.rs`. No new Rust dependency required. |

---

# 5. Scope

This package authorises a future implementation to:

1. **Python (`jarvis/interfaces/stdio_rpc.py`)**: Add a `NotificationEmitter`-style mechanism to `StdioRpcServer`:
   - A `threading.Lock` shared between the main request-handling loop's response writes and a new background daemon thread's notification writes, so the two can never interleave partial JSON onto the same line.
   - A background daemon thread, started by `serve_forever()`, that every `heartbeat_interval_seconds` (constructor parameter, defaulting to reading `JARVIS_HEARTBEAT_INTERVAL_SECONDS`, itself defaulting to `30` if unset - matching the `JARVIS_MEMORY_DB_PATH`-style override convention already established) writes a JSON-RPC notification object - `{"jsonrpc": "2.0", "method": "system.heartbeat", "params": {"timestamp": "<ISO8601 UTC>"}}` - with **no `id` key at all**, the JSON-RPC 2.0 signal that distinguishes a notification from a response (which always includes `id`, even `null` for certain error cases).
   - The thread must be a daemon thread (does not block process exit) and must stop cleanly when `serve_forever()`'s main loop exits (stdin closes/EOF).
2. **Rust (`src-tauri/src/lib.rs`)**: Restructure the backend I/O from synchronous per-call reading to a background-reader-plus-dispatch model:
   - `spawn_backend()` additionally spawns a background thread that continuously reads lines from the child's stdout.
   - A shared `Arc<Mutex<HashMap<u64, mpsc::Sender<Value>>>>` (or equivalent) tracks pending calls by request id.
   - For each line the reader thread parses: if the parsed JSON object has an `"id"` key, look up the matching pending sender and deliver the response (matching `call_backend`'s existing error/result handling, just relocated). If the object has **no** `"id"` key, treat it as a notification - extract `method`/`params` and call `app_handle.emit("jarvis://notification", json!({"method": method, "params": params}))`.
   - `call_backend()` is restructured to register a pending sender for its id, write the request, then block receiving on that call's own channel rather than calling `read_line()` directly.
3. **React (`src/App.jsx`)**: Add a `useEffect` that calls `listen("jarvis://notification", callback)` (from `@tauri-apps/api/event`) once on mount, storing the latest notification's `method`/`params`/receipt-time in state, and unlistening on unmount (the `listen()` call returns an unlisten function per the Tauri v2 API).
4. Add a small, honest UI element displaying the latest heartbeat receipt time (e.g., "Backend heartbeat: HH:MM:SS" near the existing System Health panel) - satisfying PBK-0001's Incremental Visual Convergence practice with a genuinely live, real-data-backed element, not a decorative placeholder.
5. Add `jarvis/tests/test_stdio_rpc.py` coverage for the new notification-emitting behaviour (a fake/injectable clock or a short test interval, not a real 30-second sleep in the test suite).
6. Add a Rust-side test (or, if Tauri's test harness makes a true integration test impractical within this package's scope, a documented manual verification step per Section 10) confirming: (a) a notification line is correctly routed to `emit` and not mistaken for a pending call's response, and (b) per Implementation Requirement 3, an unparsable line while two or more calls are genuinely in flight fails *all* of them with the existing "malformed response" error, rather than leaving any one hanging indefinitely.
7. Register **EBG-0099** (this package's own backlog entry, closing EBG-0050's "streaming notifications" remaining-scope line) in EBR-0001 as `Complete` only once actually implemented, validated and committed.

No other files are authorised to change. This is a real, visible UXP-facing increment satisfying PBK-0001's live-UXP-progress requirement directly, not merely a backend-only change.

---

# 6. Authorised Files

1. `jarvis/interfaces/stdio_rpc.py`
2. `jarvis/tests/test_stdio_rpc.py`
3. `src-tauri/src/lib.rs`
4. `src/App.jsx`
5. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
6. `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`
7. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. The Python-side write lock must guard *every* write to `out_stream` - both the main loop's response writes and the heartbeat thread's notification writes - so a response and a notification can never partially interleave into one corrupted line.
2. The heartbeat thread must not hold the lock while sleeping - only while performing the actual write - so it cannot block the main loop's ability to respond to real requests during its sleep interval.
3. **The reader thread cannot distinguish "a malformed notification" from "the malformed response some pending call is waiting on"** - a line that fails to parse as JSON has no `id` to correlate against anything, by definition (Codex pre-implementation review finding, v0.1). Silently ignoring an unparsable line would leave whichever call it was actually meant to answer (if any) blocked on its channel forever - a real regression from today's behaviour, where a malformed line fails that call immediately and visibly. The reader thread must therefore treat **any** unparsable line as connection-level corruption, not a per-line skip: fail every currently-pending call's channel with the existing "malformed response" error, and reset the shared backend state so the next call attempts a fresh respawn - extending today's single-call teardown behaviour to the multi-call-in-flight case this restructuring introduces, rather than trying to guess which call was affected.
4. `call_backend()`'s existing error semantics (write failure, EOF, malformed response, backend-reported error) must be preserved exactly for actual request/response calls - this package changes *how* the response is delivered to the waiting call (via channel instead of direct `read_line`) and, per Requirement 3 above, generalises single-call teardown to all-pending-calls teardown now that multiple calls can genuinely be in flight at once, but changes nothing about what any individual call observes when its own response is malformed.
5. The React `useEffect`'s unlisten function must actually be called on unmount - a leaked listener across component remounts would accumulate duplicate heartbeat handlers over time.
6. No notification content shall imply a capability or state more complete than what is actually implemented - the heartbeat notification is exactly what it claims to be (proof the plumbing works), not dressed up as a richer "live activity feed."

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any real business-logic-driven notification (Guardian state changes, memory events, knowledge-graph updates) - the heartbeat is the only notification type this package wires end to end. A future package would add real notification sources on top of this proven plumbing.
2. Removing or replacing the existing one-time mount fetch in `App.jsx` - `platform_status`/`knowledge_graph` remain request/response, fetched once on mount, exactly as today. This package adds a second, independent channel; it does not migrate existing functionality onto it.
3. Production sidecar packaging (`tauri-plugin-shell`) or full crash-restart policy - both remain separately named in EBG-0050's still-open remainder, not touched here.
4. Any change to `jarvis/guardian/runtime.py`, Sentinel, or memory - this package is UXP-backend plumbing only.
5. A generic pub/sub or multi-subscriber notification framework - one notification type (heartbeat), one Tauri event channel, one React listener. Generalising this is a future package's decision once real notification sources exist to motivate the generalisation.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. The background threads (Python heartbeat, Rust reader) must not prevent clean process shutdown - `serve_forever()` exiting and the Tauri app's existing exit-time backend-kill logic (`lib.rs`'s `RunEvent::Exit` handler) must both continue to work exactly as today.

---

# 10. Validation

After implementation, run:

```powershell
python -m pytest
python scripts/validate_repository.py
npm run build
cargo build --manifest-path src-tauri/Cargo.toml
```

Validation should confirm:

1. Full pytest suite passes, including new `test_stdio_rpc.py` heartbeat-notification coverage.
2. `validate_repository.py` (full mode) passes with 0 errors.
3. A live smoke check (run by the Engineering Implementer directly, per PBK-0001's Operational Verification Before Reporting) through a real `npm run tauri dev` session: confirm the heartbeat display actually updates live in the running window without a page reload, and that `send_message`/`platform_status`/`knowledge_graph` all continue to work correctly (proving the reader-thread restructuring did not break existing request/response calls).
4. No unauthorised files changed.

---

# 11. Risks and Dependencies

## Dependencies

1. `@tauri-apps/api`'s `event` module (already a dependency, `^2.2.0`) for `listen()` on the React side.
2. Tauri's `AppHandle::emit()` (already available via the already-imported `Manager` trait) on the Rust side.

## Risks

1. **This is a genuine architectural restructuring of the Rust sidecar's I/O model, not an additive change.** `call_backend()`'s read path changes from direct synchronous `read_line()` to channel-based delivery from a background reader thread. Implementation Requirement 4 exists specifically to keep this restructuring behaviourally invisible to every existing call; the live smoke check (Section 10 item 3) is the actual proof of that, not just the unit tests.
2. **Heartbeat-only scope means this package proves plumbing, not utility.** The Programme Sponsor should expect a small, honest "it works" increment (a live timestamp), not a materially different user experience yet - real value arrives with future notification sources built on top of this.
3. **Thread lifecycle correctness (Python daemon thread, Rust reader thread) is easy to get subtly wrong** (a thread that outlives the process it should die with, a lock held across a blocking operation). Both are called out explicitly in Implementation Requirements 2 and 9, and Constraint 2 requires clean-shutdown behaviour to be explicitly verified, not assumed.

---

# 12. Approval Request

Draft v0.1 - not yet reviewed by the Engineering Reviewer or approved by the Programme Sponsor.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] | Decision this package extends - the JSON-RPC 2.0 envelope was adopted specifically to allow this without a breaking change. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0050's remaining "streaming notifications" scope, closed by this package as EBG-0099. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track C Near-term item this package delivers. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Feature-First Delivery Discipline (this is the session's product-moving WP) and Incremental Visual Convergence (the heartbeat display is a small, genuinely live UXP element). |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 20 July 2026 | Claude Engineering Implementer | Addressed a Codex Medium finding on v0.1: Implementation Requirements 3 and 4 directly contradicted each other - Requirement 3 said an unparsable line should be logged/ignored as non-fatal, but the reader thread has no way to know whether that line was a broken notification or the response a pending call is waiting on, so ignoring it could leave that call blocked forever. Rewrote Requirement 3 to treat any unparsable line as connection-level corruption - failing all currently-pending calls and resetting backend state, extending today's single-call teardown behaviour to the multi-call-in-flight case this restructuring introduces. Scope item 6's test-coverage requirement extended to cover this scenario explicitly. |
| 0.1 | 20 July 2026 | Claude Engineering Implementer | Initial draft. Not yet reviewed or approved. |
