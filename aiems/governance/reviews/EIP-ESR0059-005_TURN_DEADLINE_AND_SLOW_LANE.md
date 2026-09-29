# EIP-ESR0059-005 - Turn Deadline and Slow-Request Lane

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-005 |
| Title | Engineering Implementation Package: WP5 Turn Deadline and Slow-Request Lane |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP5 |

---

# 2. Purpose

Implements ESR-0059 WP5, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0139, the next High-priority item of the production code review's action plan, under the Programme Sponsor's standing instruction to proceed with that plan. WP4 made it more pressing.

Two defects:

* **No overall turn budget.** Each provider had only its own timeout, so a full failover chain - OpenAI 30s, Gemini 30s (since WP4), Ollama 90s - could run 150s. That is past the Tauri host's 120s `BACKEND_CALL_TIMEOUT`, so the user saw a backend timeout instead of the honest provider-unavailable reply, and the late reply was discarded.
* **Head-of-line blocking.** `StdioRpcServer.serve_forever()` handled one request at a time, so `platform.status`, memory, profile and knowledge calls queued behind a slow `guardian.converse`.

---

# 3. Repository Context Investigated

* `jarvis/interfaces/stdio_rpc.py` `serve_forever()` - synchronous loop; responses already carry their request id.
* `src-tauri/src/lib.rs` - routes responses to waiting calls by id (`route_response()`), so responses arriving out of request order are already handled; `BACKEND_CALL_TIMEOUT` is 120s.
* `jarvis/interfaces/activity_tracker.py` - already guards its own state with a lock, so it can be drained from two threads.
* `sentinel/providers.py` `ProviderRequest`, `sentinel/orchestrator.py`, and the three text adapters - each adapter passed its configured timeout straight to `urlopen`.
* `GuardianRuntime` conversation state (Cognitive Core history) is touched only by `converse()`, which after this package runs on exactly one thread.

---

# 4. Scope

## 4A. Per-turn deadline

* `ProviderRequest.deadline: float | None = None` - a `time.monotonic()` instant. `None` keeps the previous behaviour.
* `remaining_timeout()` (`sentinel/providers.py`) - the provider's configured timeout, capped by what remains of the deadline; raises the adapters' established `RuntimeError` if it has already passed. Used by the OpenAI, Gemini and Ollama adapters.
* `ProviderOrchestrator.execute()` starts no further provider once the deadline has passed. A provider skipped for time is not marked `DEGRADED` - it did not fail. The failure reason names the providers actually attempted.
* `SentinelGatedConversationProvider(turn_deadline_seconds=...)` sets the deadline per turn; `build_default_runtime()` wires it from `JARVIS_TURN_DEADLINE_SECONDS`, default **100s** (20s under the Tauri timeout). An absent, blank, non-numeric, non-positive, `nan` or `inf` value uses the default rather than failing startup.

## 4B. Slow-request lane

* `SLOW_METHODS` = `guardian.converse`, `guardian.speak`, `guardian.transcribe`, `guardian.agent.invoke`. `serve_forever()` runs these on a dedicated **single-worker** executor; everything else stays inline.
* One worker, deliberately: slow calls still run one at a time in arrival order, so conversation turns cannot overtake each other, and `GuardianRuntime`'s conversation state is only touched from one thread.
* When stdin closes, the loop waits for queued and in-flight slow requests to finish and write their responses before the heartbeat stops and `run()` stops the runtime.
* A failure to *write* a slow-lane response is logged rather than lost inside the executor.
* Malformed lines take the inline path, where `handle_line()` returns the proper JSON-RPC error.

## 4C. Tests

* Orchestrator: nothing attempted after the deadline, health untouched; failover stops mid-chain when the deadline expires; unchanged failover without a deadline.
* Ollama adapter: timeout capped by the deadline; configured timeout without one; no call started after the deadline.
* Conversation provider: deadline set per turn; none when unconfigured; non-positive budget rejected.
* RPC: deadline configuration parsing, including `nan`/`inf`; `platform.status` answered while a slow `guardian.converse` is still running, and the slow turn still answered; slow requests keep their order; malformed lines still get an inline error.
* Full suite run three times consecutively to check the timing-based tests: stable.

## 4D. Explicitly out of scope

* Retry, backoff and circuit breaking (rest of EBG-0140).
* Deadlines for speech, transcription and agent calls - they run on the slow lane, so they no longer block other methods, but have no overall budget of their own.
* Cancelling an in-flight provider call: the deadline bounds each call's timeout rather than interrupting it.

## 4E. Review

**Design review - disclosed self-review** (GitHub Copilot CLI's monthly quota still exhausted, re-probed before this review; the Programme Sponsor's WP4 decision to self-verify with a retrospective Copilot review applies, EBG-0153). Because this package introduces the backend's first concurrency, the review enumerated every piece of mutable state touched after startup: the gateway's decision list and both in-memory audit recorders are appended from both threads (single `list.append` calls, atomic under CPython's GIL); the orchestrator's health map is written only by the worker and only for existing keys, while `platform.status` iterates the route tuple, never the map; Cognitive Core history, the speech/transcription providers and the agent service are touched only by the single worker; pending memory proposals and profiles only by the main thread; SQLite opens a connection per call and serialises writers itself. **Disclosed limitation**: this relies on CPython's GIL. A free-threaded (no-GIL) Python build would need explicit locks on the shared lists and the health map. Also disclosed: speech, transcription and agent calls share the one worker, so a long speech synthesis delays the next conversation turn (they no longer delay anything else).

---

# 5. Validation Requirements

* `python -m pytest -q` (three consecutive runs), `ruff check .`, `python scripts/validate_repository.py`.

## 5A. Live check - performed against the real backend process

`python -m jarvis --ipc-stdio` spawned as the Tauri host does, with Ollama pointed at a non-routable address (a connection that hangs rather than refusing), no cloud keys, and a 6s test deadline. `guardian.converse` then `platform.status` written back to back:

* `platform.status` answered at **0.3s**, while the conversation turn was still waiting.
* `guardian.converse` answered at **6.4s** with the honest provider-unavailable reply - bounded by the deadline, where Ollama's own 90s timeout would otherwise have applied.
* The backend exited cleanly (code 0) when stdin closed.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* No conversation turn outlasts the configured deadline plus a small margin.
* Non-slow methods are answered while a slow one is in flight.
* Slow requests stay in order, and every accepted request is answered.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** on the disclosed self-review. Implemented exactly as at v0.2. Pending commit/push through `submit-response`. |
| 0.2 | 29 September 2026 | Claude Engineering Implementer | Disclosed self-review recorded in Section 4E (Copilot CLI quota still exhausted): every piece of post-startup shared state enumerated; reliance on CPython's GIL and the shared single worker disclosed. Retrospective Copilot review owed (EBG-0153). Not yet approved or committed. |
| 0.1 | 29 September 2026 | Claude Engineering Implementer | ESR-0059 WP5 draft. Per-turn deadline (default 100s, `JARVIS_TURN_DEADLINE_SECONDS`) enforced by the orchestrator and every text adapter; single-worker slow-request lane in `serve_forever()`. pytest 637 passed/1 skipped (three runs), ruff clean. Live-verified against the real backend process: status in 0.3s during a hung turn, turn bounded to its 6s test deadline, clean exit. Not yet reviewed, approved or committed. |
