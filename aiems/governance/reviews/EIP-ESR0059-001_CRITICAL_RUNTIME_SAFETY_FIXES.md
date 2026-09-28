# EIP-ESR0059-001 - Critical Runtime Safety Fixes

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-001 |
| Title | Engineering Implementation Package: WP1 Critical Runtime Safety Fixes |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP1 |

---

# 2. Purpose

Implements ESR-0059 WP1: the "Critical / Blockers" tier of the Claude Engineering Implementer's production code review (28 September 2026, delivered in chat at the Programme Sponsor's request, then directed into implementation: "proceed with the action plan"), limited to the four items that require no Programme Sponsor product decision. Also registers every other finding from that review in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] (EBG-0135 to EBG-0151), so none of them lives only in chat.

The four fixes, each registered and closed by this package:

* **EBG-0135** - every Tauri command ran on the main thread, freezing the window for up to 120 seconds during slow provider calls.
* **EBG-0136** - the backend process was orphaned on teardown, and a stale reader could tear down a newer backend.
* **EBG-0137** - `memory.restore` accepted content backed by a *denied* consent decision, and unvalidated fields that broke every later conversation turn.
* **EBG-0138** - the Home Assistant agent interpolated `entityId` into the request path unvalidated, reaching other Home Assistant endpoints with the admin token.

---

# 3. Repository Context Investigated

* `src-tauri/src/lib.rs` - all fourteen `#[tauri::command]` handlers were plain synchronous `fn`s. Tauri 2 executes non-`async` commands on the main thread, and each blocked in `call_backend()`'s `recv_timeout(BACKEND_CALL_TIMEOUT)` (120s, EBG-0109). The teardown paths in `run_dev_reader()`/`run_sidecar_reader()`/`call_backend()` set the shared state to `None` without terminating the child, and without checking which process they belonged to. The timeout path removed the pending entry from whichever backend was *current*, not the one the call was made against - and request ids restart at 1 per process.
* EBG-0109 (Complete) - Finding 2(b)'s "hung indefinitely" GUI symptom was closed as most likely a diagnostic confound. The main-thread blocking found here is a plausible mechanism for the *freeze* part of that symptom; this package does not claim to have reproduced 2(b).
* `jarvis/memory/store.py` `import_snapshot()` (ESR-0058 WP3) - checked that every `personal_memory` row's `consent_decision_id` was *present* in the snapshot, not that it was *approved*, unlike `add()`, which enforces approval for live writes. No field-type or timestamp validation. Confirmed by a live probe during the review: a snapshot with a denied decision imported successfully, and a restored `created_at` of `"not-a-date"` made `list_all()` raise on every call. `GuardianRuntime.converse()` reads memory on every turn, so every conversation request then failed.
* `jarvis/guardian/cognitive_core.py` - restored memory content is rendered into the system prompt on every turn, which is why the consent bypass above is also a prompt-injection path.
* `jarvis/agents/home_assistant_agent.py` (ESR-0058 WP4) - `f"{base_url}/api/states/{entity_id}"` with no validation. A value such as `../config` resolves to a different Home Assistant GET endpoint.

---

# 4. Scope

## 4A. Tauri host (`src-tauri/src/lib.rs`)

* All fourteen commands converted to `async fn`, each routing through a new `call_backend_off_main_thread()` helper that runs the unchanged blocking `call_backend()` on `tauri::async_runtime::spawn_blocking`. Command names, argument names and return shapes are unchanged, so no frontend change is needed.
* `BackendProcess` gains a `generation` identifier (a process-wide `AtomicU64` counter). A new `tear_down_if_current()` tears down, and terminates, the shared backend only if it is still the process the caller belongs to. All six reader teardown sites and the write-failure path use it.
* `BackendHandle::kill()` now reaps the Dev-path child after killing it (`child.wait()`), so no zombie is left on Unix-like platforms.
* `call_backend()` captures its own process's `generation` and pending map while holding the lock, so the write-failure and timeout cleanup paths act on that process only.

## 4B. Memory restore (`jarvis/memory/store.py`)

* `import_snapshot()` additionally requires, before any write: every content row references an **approved** decision; `decision` is `approved` or `denied`; text fields are non-blank strings; `created_at`/`decided_at` parse with `datetime.fromisoformat()`. Two small module-level helpers, `_require_text_fields()` and `_require_timestamp()`. All validation still completes before the transaction opens, so a refused backup never wipes an existing store, even with `confirm_overwrite=True`.

## 4C. Home Assistant agent (`jarvis/agents/home_assistant_agent.py`)

* `is_valid_entity_id()` - full match of `[a-z0-9_]+\.[a-z0-9_]+`. Enforced in both `HomeAssistantStateQueryAgent.execute()` and `HomeAssistantClient.get_state()`, the latter before any request is built.
* `get_state()` raises the client's established `RuntimeError` for a non-JSON body or a JSON value that is not an object, rather than letting the agent's `.get()` raise `AttributeError`.

## 4D. Governance

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]: EBG-0135 to EBG-0138 registered and closed Complete by this package. EBG-0139 to EBG-0151 registered as Candidate Backlog - the review's remaining findings, cross-referenced to existing items where they overlap (EBG-0050, EBG-0051, EBG-0070, EBG-0110, EBG-0132) rather than duplicating them.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]: EBG-0152 registered as Candidate Backlog - a new finding made while running this package's own validation, not part of the original review. The CI `python` job has failed on every push to `main` since 29 July 2026 because its first step, `ruff check .`, fails; `pytest`, `validate_repository.py` and `pip-audit` have therefore not run in CI for two months. Flagged as a scope decision for the Programme Sponsor rather than silently fixed inside this package.
* [[ESR-0059_ENGINEERING_SESSION_REPORT|ESR-0059]] opened (WP0A/WP0B) and WP1 recorded.

## 4E. Tests

* `src-tauri/src/lib.rs` (3 new Rust tests): the generation predicate; a real idle `python` child placed in shared state survives a stale-generation teardown and is removed by a matching one; teardown with no backend is a no-op.
* `jarvis/tests/test_memory_store.py` (10 new cases): denied-decision content refused; unparseable `created_at` and non-string `decided_at` refused; five non-text or blank `content` values refused; unknown `decision` value refused; a refused backup leaves a non-empty store intact even with overwrite confirmed.
* `jarvis/tests/test_agents.py` (19 new cases): ten malformed entity ids refused by the client with no request made; five non-object or non-JSON bodies raise `RuntimeError`; four malformed ids refused at the agent before the client is called.

## 4F. Explicitly out of scope

* **The rest of the action plan.** Backend request concurrency and a per-turn deadline (EBG-0139), provider retry and circuit breaking (EBG-0140), non-model-reply handling (EBG-0141), prompt structure (EBG-0142), token budgets (EBG-0143), observability (EBG-0144) and memory revocation (EBG-0145) are each their own later Work Package.
* **Anything needing a Programme Sponsor product decision.** Wiring Gemini into the production route (EBG-0051's own "separate decision"), replacing the local-echo final fallback (EBG-0070's design), and paid code signing (EBG-0146, a recurring cost under the no-discretionary-budget constraint).
* **Backend-side request concurrency.** After this package the *window* stays responsive, but a second backend request still waits behind a slow one in `stdio_rpc.py`'s single-threaded loop. That is EBG-0139.
* **Frontend changes.** None needed; the command surface is unchanged.

## 4G. Disclosed observation - process trees (open, not fixed here)

During the live smoke check, the dev-mode backend appeared as **two** processes: `"python" -m jarvis --ipc-stdio` and `C:\Program Files\Python312\python.exe -m jarvis --ipc-stdio`, consistent with `python` on this machine resolving to a launcher that starts the real interpreter as a child. `Child::kill()` terminates only the direct child, so on such a machine the fix in 4A may still leave the real interpreter running in dev mode. The release sidecar is a PyInstaller build, and a onefile PyInstaller executable is likewise a bootloader plus a child process on Windows; whether killing the bootloader also ends the child was not verified here. Both need a verified process-tree termination (a Windows job object, or an equivalent) - recorded for EBG-0136's follow-up rather than widened into this package.

---

# 5. Validation Requirements

* `python -m pytest -q` - full Python suite.
* `ruff check .` - no new errors beyond the 13 pre-existing ones recorded in EBG-0152 (three `TRY004` hits introduced by this package are suppressed with the codebase's established documented-`noqa` pattern: two in `store.py`, where `ValueError` is `import_snapshot()`'s public contract, and one in `home_assistant_agent.py`, where `RuntimeError` is the client's established failure contract - count corrected at v0.2 per the design review).
* `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test` (`src-tauri/`).
* `npx playwright test` - confirms the unchanged command surface against the frontend.
* `python scripts/validate_repository.py` - 0 errors, warning count disclosed.
* Live smoke check: the real dev shell starts, and a conversation round trip completes through the new async command path.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* No Tauri command executes `call_backend()` on the main thread.
* No teardown path leaves a backend process running, or tears down a process other than its own.
* `import_snapshot()` refuses content without an approved decision, and refuses any row that would fail to read back, before any write.
* No Home Assistant request path can be built from a malformed entity id.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 28 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** after reviewing the change summary directly. Implemented exactly as design-reviewed at v0.2 - no further content change. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 0.2 | 28 September 2026 | Claude Engineering Implementer | Design-reviewed via a genuine scoped GitHub Copilot CLI invocation routed through the real bridge (`ESR-0059`/`WP1`, complete 9-file scope) - **Pass**, single `return-findings` entry. Independently counted all 14 async commands and all 7 `tear_down_if_current` call sites; confirmed no lock is held across the cleanup branches; confirmed all restore validation precedes the transaction; confirmed entity-id validation in both agent and client; read all 18 new EBR-0001 rows and their cross-referenced items; independently confirmed EBG-0152 from GitHub Actions history (last green `main` run 2026-07-29T11:35Z, every push since red, `ruff check .` the failing step). Re-ran pytest (616 passed/1 skipped), `validate_repository.py` (0 errors/333 warnings), ruff (13 pre-existing only), cargo test (8 passed) and clippy (clean). One documentation nit fixed: the suppressed-`TRY004` count was three, not two. Not yet approved or committed. |
| 0.1 | 28 September 2026 | Claude Engineering Implementer | ESR-0059 WP1 draft. Four Critical-tier fixes implemented and tested against the working tree; seventeen review findings registered in EBR-0001 (EBG-0135 to EBG-0151), plus EBG-0152 (CI `python` job red since 29 July 2026) found during WP1's own validation. Drafted and implemented directly against the working tree before Programme Sponsor review of this specific content - the same disclosed process note as every Work Package at ESR-0058. Not yet reviewed, approved or committed. |
