# EIP-ESR0059-009 - Durable Audit Trail and Backend Logging

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-009 |
| Title | Engineering Implementation Package: WP9 Durable Audit Trail and Backend Logging |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP9 |

---

# 2. Purpose

Implements ESR-0059 WP9, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0144, the next Medium-priority action-plan item, under the Programme Sponsor's standing instruction.

* `build_default_runtime()` used in-memory audit recorders for both the Sentinel gateway and the orchestrator, so the audit trail was lost on every restart.
* Gateway decisions, orchestrator history, in-memory audit events and unresolved memory proposals grew without bound in a long-running backend.
* The packaged sidecar's stderr is not captured by the Tauri host (`run_sidecar_reader`), so a release build kept no logs at all - including any startup failure.

---

# 3. Repository Context Investigated

* `sentinel/audit.py` - `MemoryAuditRecorder` (unbounded list) and `JsonAuditRecorder` (append-only, no rotation, no locking); only the manual smoke-test scripts used the latter.
* Audit event contents: Sentinel decisions record source, intent and policy reason; provider executions record capability, provider names, attempts and failure reasons, which since EBG-0140 carry only status codes and exception types. **No event carries conversation or memory text**, so persisting them does not persist user content.
* Since WP5 the backend records from two threads (EBG-0139), so a shared file recorder needs a lock.
* `jarvis/app.py` `configure_logging()` - stderr only, level INFO.
* `~/.jarvis/logs/` already exists on the development machine and holds unrelated June 2026 files (`backend-DATE.log`, `electron-...`, `nextjs-...`, a `backend` folder), apparently from another application, alongside JARVIS's own earlier smoke-test audit logs. The new files (`audit.jsonl`, `backend.log`) do not clash with any of them; noted rather than changed.

---

# 4. Scope

## 4A. Durable, rotating audit trail

* `JsonAuditRecorder` rotates at `max_bytes` (default 5 MB), keeping `backup_count` copies (default 3), and serialises writes and rotation with a lock.
* `build_default_runtime()` gives the gateway and the orchestrator one shared `JsonAuditRecorder` at `<log dir>/audit.jsonl`.

## 4B. Bounded in-process history

* `MemoryAuditRecorder`, the gateway's decision list and the orchestrator's execution history keep the most recent 1,000 entries.
* At most 100 unresolved memory proposals are held; past that the oldest is dropped, logged, and never stored - as if the process had restarted.

## 4C. Backend log file

* `run()` adds a rotating file handler (`<log dir>/backend.log`, 5 MB, 3 copies) alongside stderr, and logs startup, shutdown, and any startup or serve-loop failure with its traceback. stdout is never used: it carries the JSON-RPC stream.

## 4D. Log directory

`JARVIS_LOG_DIR`; unset, the `logs` directory beside the Personal Memory store's directory - `~/.jarvis/logs` by default. Deriving it from `JARVIS_MEMORY_DB_PATH` keeps all local data under one root and means tests, which already point that variable at a temporary directory, never write into the real home directory (the ESR-0026 WP1 isolation lesson). Verified: a full test run left `~/.jarvis/logs` untouched.

## 4E. Tests

New `jarvis/tests/test_audit_and_logging.py`: bounded memory recorder; rotation with the right number of backups and every file within its size; persistence across instances; 800 concurrent writes from four threads all whole JSON lines; bounded gateway history; bounded pending proposals (the oldest cannot be approved and nothing is stored); log-directory resolution; a runtime conversation turn producing `sentinel_decision` and `provider_execution` audit events with the message text absent from the audit log; the backend log file receiving records.

## 4F. Explicitly out of scope

* Crash reporting or remote telemetry - everything stays on the local machine.
* Capturing the sidecar's raw stderr in the Tauri host; the backend now writes its own log instead.
* Retention beyond rotation, and any UXP log viewer.

## 4G. Review

**Review - disclosed self-review** (GitHub Copilot CLI quota re-probed, still exhausted; EBG-0153 applies). Checked: every audit event's fields were traced to their source and none carries conversation or memory text - confirmed by a test and the live check; rotation runs under the same lock as writes, so two threads cannot rotate twice or interleave a line; the backend log goes to a file and stderr only, never stdout; the log directory's default keeps test runs out of the home directory (verified); dropping the oldest unresolved proposal stores nothing, so no content is retained without consent. Real finding during implementation, fixed before testing: `sentinel/core.py` was missing its `deque` import (174 tests failed until added). No further change needed.

---

# 5. Validation Requirements

* `python -m pytest -q`, `ruff check .`, `python scripts/validate_repository.py`.

## 5A. Live check - performed against the real backend process

With `JARVIS_LOG_DIR` pointed at a temporary directory, a message containing a fake PIN and a memory proposal containing a fake passport number were sent through the real backend: `audit.jsonl` and `backend.log` were both created; the audit trail recorded `sentinel_decision`, `provider_execution`, `sentinel_decision`; neither file contained either secret. A second run showed `backend.log` recording startup and shutdown.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* The Sentinel audit trail survives restarts, bounded by rotation, and contains no conversation or memory text.
* No in-process history grows without bound.
* A release build keeps its own backend log, including startup failures.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** on the disclosed self-review. Implemented exactly as at v0.2. Pending commit/push through `submit-response`. |
| 0.2 | 29 September 2026 | Claude Engineering Implementer | Disclosed self-review recorded in Section 4G (Copilot CLI quota still exhausted). Retrospective Copilot review owed (EBG-0153). Not yet approved or committed. |
| 0.1 | 29 September 2026 | Claude Engineering Implementer | ESR-0059 WP9 draft. Durable rotating locked audit trail, bounded in-process histories and pending proposals, rotating backend log file with startup/failure logging, `JARVIS_LOG_DIR`. pytest 698 passed/1 skipped, ruff clean; home log directory untouched by tests. Live-checked: both files written, no user text in either. Not yet reviewed, approved or committed. |
