# EIP-ESR0061-003 - Provider Strategy: Ollama First and Claude Escalation

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0061-003 |
| Title | Engineering Implementation Package: WP3 Provider Strategy, Ollama First and Claude Escalation |
| Version | 0.3 |
| Status | Draft - design only, drafted ahead under D22; design review Pass (Gemini) with one correction applied; Programme Sponsor decisions S1-S6 approved (chat, 8 October 2026); nothing built, build waits for Session B |
| Session | ESR-0061 (drafting only). WP3 belongs to Session B (WP3-WP4) in the plan; its build and commits happen when that session opens. The EIP identifier does not change when it does |
| Work Package | WP3 |
| Plan | [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]] Section 5 and Section 7, WP3 |
| Decision | [[ADR-0023_VERSION_1_0_PROVIDER_STRATEGY|ADR-0023]] |
| Risk class | **High-risk** (plan Section 7: WP2, WP3, WP5, WP6): sends household data to a third party and handles a spend cap. Antigravity reviews it alongside Copilot, or alone while Copilot's quota is out (resets 1 November 2026) |

---

# 2. Purpose

Make a fresh install converse without any API key, and put Claude behind a visible, confirmed, capped escalation, as ADR-0023 decides. Backlog: EBG-0163 (the strategy), EBG-0161 (whitespace model variable), EBG-0157 item (6) (deadline-capped timeouts; closes EBG-0157), EBG-0110 backend half (per-profile memory-to-cloud control; the UI half and closure are WP5), EBG-0090 (closed by the plan's discussion of subscription tools).

This package is the **backend and its protocol**. The first-run screens, settings and the key store are WP5; the redesigned UI is WP4. WP3 adds only the smallest UI needed to make escalation usable and honest (see 6.7).

# 3. Decomposition

| Sub-WP | Content | Effort |
|---|---|---|
| **WP3a** | Foundations: deadline-capped timeouts (EBG-0157 6); `sentinel/anthropic_provider.py`; route split; unregister OpenAI and Gemini; whitespace-variable fix (EBG-0161) | 1.5-2 d |
| **WP3b** | Escalation: spend ledger and cap; suggest-then-confirm protocol; policy gate and per-profile memory control (EBG-0110 backend); "answered by Claude" indicator | 1.5-2 d |
| **WP3c** | Ollama first: detection, status, hardware recommendation, guided install, in-app pull; measurements on both machines | 1-1.5 d |

Total 4-5.5 days, as the plan estimates (4-5 d). Each sub-WP is a gated commit (two gates, rule A6).

# 4. Repository Context Investigated

* **Adapter shape** - `sentinel/gemini_provider.py` and `sentinel/ollama_provider.py`: `urllib` with an injectable `transport`, configuration validated in `__init__`, `remaining_timeout()` for the deadline, errors that name the exception type or HTTP status and never content, `ProviderError(transient=...)` for retry, a `retry_policy` property read by the orchestrator.
* **Failover is automatic today** - `build_default_runtime()` (`jarvis/interfaces/stdio_rpc.py:485`) builds **one** route `text-generation` = primary cloud, secondary cloud, then Ollama. `ProviderOrchestrator.execute` walks it in order. So a failing local model would silently fall over to a cloud provider. That contradicts D28 ("never automatic") and must be removed, not just supplemented.
* **Orchestrator semantics** (`sentinel/orchestrator.py`) - per-provider retry only on `transient` failures, a 30-second circuit after any other failure, `DeadlineExceededError` leaves health untouched, durable audit events carry names and counts only.
* **Deadline gap (EBG-0157 6)** - `remaining_timeout()` returns the smaller of the provider timeout and what is left of the turn, but the adapter cannot tell which applied; a timeout caused by the shortened budget is reported as a transient provider fault and marks a healthy provider degraded.
* **Cloud wiring and tests** - `_REAL_PROVIDER_SPECS`, `_build_real_provider`, the primary/secondary variables and 37 mentions in `jarvis/tests/test_stdio_rpc.py`, plus `test_openai_provider.py`, `test_gemini_provider.py`, `test_sentinel_provider_config.py`, and two scripts. `stdio_rpc.py:293`: `environ.get(spec["model_env_var"]) or spec["default_model"]` accepts a whitespace-only value (EBG-0161).
* **Conversation path** - `GuardianRuntime.converse()` builds `memory_notes` from the profile's visible memories and passes them with the profile's history to `SentinelGatedConversationProvider.generate()`; the response carries `provider` and `is_model_reply`. Nothing records whether a profile may send memory to a cloud provider (EBG-0110).
* **Sentinel policy has no concept of roles** (`sentinel/policy.py`) - `TrustTierPolicy.classify()` reads only `payload_type`, `capability`, `risk_category` and `requires_approval`; the household role is enforced elsewhere, at the RPC layer from the server-held active profile (as for memory, EIP-ESR0059-014). A role check in the policy is therefore **new work**, not a setting (v0.2, correction found by the Engineering Implementer after design review; see 6.8).
* **Bounds already in place** - one message is capped at 4,000 characters (`MAX_MESSAGE_CHARS`), memory notes at 1,500 (`MEMORY_NOTES_CHAR_BUDGET`), and recent history is a fixed-length `deque` (`history_limit`), so a worst-case input for the ledger is computable from constants.
* **Roles** - `HOUSEHOLD_ROLES = ("Administrator", "Adult", "Child", "Guest")` (`jarvis/identity/store.py:47`). Consent and moderation for Child are WP6.
* **Claude API facts** (from the API reference read 8 October 2026, to be re-confirmed live in WP3a): `POST https://api.anthropic.com/v1/messages` with `x-api-key`, `anthropic-version: 2023-06-01`, `content-type: application/json`; `claude-sonnet-5-5` is $2 / $10 per million input / output tokens, `claude-opus-5-5` $4 / $20, `claude-haiku-4-5` $1 / $5. On Sonnet 5.5 thinking cannot be switched off (`{"type": "disabled"}` returns 400), non-default `temperature`/`top_p`/`top_k` return 400, assistant prefill returns 400, and `effort` (default `high`) is set in `output_config`. Thinking is billed as output. A safety decline is HTTP 200 with `stop_reason: "refusal"`. Overload is HTTP 529; a billing problem is 402.

# 5. Decisions Needed From the Programme Sponsor

Each has a recommendation, so a bare "approved" settles it.

| # | Decision | Recommendation |
|---|---|---|
| S1 | Default Claude model | **`claude-sonnet-5-5`** ($2 / $10), at `effort: low` for chat. Opus 5.5 costs twice as much; Haiku 4.5 is cheaper but a generation behind for "research and harder questions". One setting (`JARVIS_CLAUDE_MODEL`) changes it |
| S2 | Raw `urllib` or the `anthropic` SDK | **`urllib`**, like every existing adapter. The SDK would add a dependency tree to the PyInstaller sidecar and bring its own retries on top of the orchestrator's. Cost of choosing `urllib`: the adapter owns request and error shapes, covered by tests and the live check. The API reference prefers the SDK by default; this is a deliberate project-convention override, stated here so the reviewer can contest it |
| S3 | What makes JARVIS *suggest* escalation (6.6) | **v1: (a) the local model is unavailable or failed, (b) a short list of research cues, (c) a manual "Ask Claude" button always present.** No model-judged confidence in v1 |
| S4 | Cap in pounds against a dollar price list | £30 per month, enforced as **US$37.50** (a deliberately low fixed rate of US$1.25 per £, adjustable by one setting), with a warning at 80 percent. The Console limit you set stays the hard backstop |
| S5 | Permission for live API spend while building | Up to **US$2** in total across WP3's live checks (the adapter, the refusal path, the Console limit's behaviour) |
| S6 | Child escalation before WP6 | **Denied** until WP6 delivers consent and moderation. Adult and Administrator can escalate; Guest cannot |

# 6. Design

**6.1 Two routes, so cloud is never reached by failover (WP3a).** `text-generation` becomes **Ollama only**. A new capability `text-generation-cloud` is routed to the Anthropic provider and is reachable **only** through the escalation path (6.5). If Ollama fails, the user sees the honest "could not reach an AI provider" reply with a suggestion to escalate - never a silent cloud call. A test asserts that with Ollama failing and a Claude key present, no cloud request is made on an ordinary turn.

**6.2 `sentinel/anthropic_provider.py` (WP3a).** Same shape as the Gemini adapter.
* Configuration requires a credential reference and a model; the key is read from the named environment variable at call time (`ANTHROPIC_API_KEY`, STD-0006 indirection; WP5 moves it to the OS keychain). Sent only in `x-api-key`.
* Request: `system` = the approved persona; history as role-tagged `messages`; the current message through `framed_prompt()`; `max_tokens` from configuration (existing `JARVIS_MAX_OUTPUT_TOKENS`, with a default that bounds the worst case); `output_config: {"effort": "low"}`; **no** `temperature`, `top_p`, prefill or `thinking` field. `anthropic-version` pinned.
* Response: join the `text` blocks only (thinking blocks, empty by default, are never shown); anything else, including an empty result, is a `RuntimeError` naming the shape.
* Refusal (`stop_reason: "refusal"`): a new `ProviderDeclinedError(RuntimeError)`, treated by the orchestrator like `DeadlineExceededError` - **not a provider fault**, health and circuit untouched - and answered to the user honestly ("Claude declined to answer this"), not by silently asking another model. (Gemini's safety block today degrades the provider for 30 seconds; this does not repeat that.)
* Errors: HTTP status only, never body or `str(exc)`. Transient: the shared set plus **529**. 400, 401, 402, 403, 404, 413 permanent. Usage (`input_tokens`, `output_tokens`, cache fields) is returned in `ProviderResponse.metadata` for the ledger, as strings.
* `retry_policy`: the cloud policy already in `stdio_rpc.py` (two attempts, one second).

**6.3 Spend ledger and cap (WP3b).** `jarvis/shared/spend_ledger.py`, a small SQLite store beside the other databases (same WAL helper), holding per calendar month (UTC): micro-dollars spent, request count, token totals. **No content, no profile text.**
* Price table in code, keyed by model id, with the date it was read; an unknown model is priced at the highest known rate (fail towards overspending *less*).
* **Before** each call, `reserve()` estimates the worst case (input tokens from a character-based upper bound, plus `max_tokens` at the output price) under a lock and refuses when `spent + reserved + worst case` exceeds the cap; **after** a response, the reservation is replaced by the real cost from `usage`. A failed call releases it. A call that times out after the server started generating may still be billed and is not seen; the Console limit covers that.
* At the cap the escalation is refused with a clear message and the conversation stays local. `provider.status` reports spent, cap, month, and the 80 percent warning.
* With S4, one turn costs at most about US$0.03 at the defaults, so the cap is about 1,400 worst-case turns a month; typical turns cost far less.

**6.4 Per-profile memory-to-cloud control (EBG-0110 backend, WP3b).** A boolean on the profile, default **false for everyone**: whether that profile's retained memory notes may accompany an escalated question. When false the cloud request carries **no** `context_notes`. Recent history of the current conversation does travel (the question cannot be answered without it) and the confirmation text says so. Stored in the identity database with a schema migration; set through an Administrator-only RPC. WP5 adds the screen; WP6 pins Child to false.

**6.5 Suggest, then confirm, then answer (WP3b).**
1. `guardian.message` runs locally as today. Its response gains `escalation: {"offered": bool, "reason": "local_unavailable" | "research_cue" | null, "token": str | null}`. A token is a random one-time value bound to the profile and the exact user message, expiring after ten minutes.
2. The UI shows the offer with plain disclosure (what is sent, to whom, that it costs money, the remaining allowance). The user may also press "Ask Claude" at any time, which requests an offer for the last message.
3. `guardian.escalate {token}` re-checks the token, the profile's role (S6), the cap and the Sentinel decision, then runs the **same** message through `text-generation-cloud`. The reply carries `answeredBy: "claude"` and the provider name. A replayed, expired or foreign token is refused.
4. Every escalation is recorded in the durable audit log as a category and count (profile role, outcome, token counts), never content.

**6.6 When JARVIS offers (S3).** Deterministic and testable: (a) the local route failed or Ollama is not running; (b) the message contains a cue from a short, documented list (for example "latest", "news", "research", "look up", "compare", "in depth", a URL); (c) the user asks. A cue list is easy to tune and to explain to a parent; it is not a model's judgement, which would itself need testing against minors.

**6.7 Smallest UI (WP3b).** In `src/App.jsx`: a visible "Claude" badge on any message with `answeredBy: "claude"`; the confirm dialog of 6.5; an "Ask Claude" action. WP4 restyles all of it; these are functional and tested, not designed.

**6.8 Who may escalate: two independent checks (WP3b).** The household role is not something `TrustTierPolicy` knows today, so the gate is built in two places, either of which alone refuses a forbidden caller:
1. **At the RPC layer** (`guardian.escalate`, and the offer in 6.5): the role comes from the **server-held active profile**, never from a request parameter, exactly as memory role enforcement does. Administrator and Adult proceed; Guest is refused; Child is refused until WP6 supplies consent and moderation (S6). No role, no escalation.
2. **In Sentinel**: the request is evaluated under intent `conversation.escalate`, capability `text-generation-cloud`, with the server-derived role in metadata. A new rule in `TrustTierPolicy` (a new category, `CLOUD_ESCALATION_NOT_PERMITTED`, in the deny branch) refuses any `text-generation-cloud` request whose role is not Administrator or Adult, and refuses one with **no** role. This is new policy code with its own tests, and the denial reaches the audit trail.
A refusal returns the existing user-facing denied reply. Tests include a Child and a Guest profile attempting every path to the cloud route (the escalate RPC, a forged token, a token from another profile, a profile switch between offer and confirmation, the ordinary message path with a failing Ollama).

**6.9 Ollama first (WP3c).**
* **Status**: `provider.status` (Ollama installed, running, endpoint, models present, the active model; Claude configured, cap and spend). "Running" is a short-timeout `GET /api/version`; "installed" is the executable on `PATH` or in each platform's standard location; neither starts anything.
* **Recommendation**: reads RAM (psutil), and on Windows/Linux the GPU's memory from `nvidia-smi` when present; on Apple Silicon unified memory is the RAM. A **data file** (`jarvis/config/ollama_models.json`: tag, approximate download size, minimum memory, licence note) maps hardware to a recommended model and a smaller fallback. **The specific tags are chosen in WP3c from current benchmarks and licences** (the plan's hardware section), not here; the mechanism and the file format are what this design fixes. The recommendation shows the download size and checks free disk space first.
* **Guided install**: JARVIS never downloads or runs an installer for you. It reports "Ollama is not installed", gives the exact steps for the platform and an "Open download page" action; it re-checks when asked.
* **Pull**: `ollama.pull {model}` calls `POST /api/pull` with streaming and emits progress as `jarvis://notification` events; it runs on the slow lane, accepts **only models in the data file**, and can be cancelled. No other model name can be pulled through JARVIS.
* **Measurement** (plan acceptance): response time and memory on the Windows PC and the Mac with the chosen model loaded, plus a small co-loaded model standing in for the moderation model, recorded per machine. See the dependency note in Section 7.

**6.10 Deadline-capped timeouts (EBG-0157 item 6, WP3a).** A new `remaining_timeout_budget()` returns the timeout and whether the deadline shortened it; `remaining_timeout()` keeps its signature. Each adapter, on a timeout when the deadline did the shortening, raises `DeadlineExceededError` instead of a transient `ProviderError`. Applies to Ollama, Anthropic, and (kept, unregistered) OpenAI and Gemini, so all four stay consistent. Closes EBG-0157.

**6.11 Unregister OpenAI and Gemini (WP3a).** `_REAL_PROVIDER_SPECS`, the primary/secondary variables and `_build_real_provider` leave the runtime; the adapters, their tests and the two scripts stay (the Piper precedent, ESR-0053). The tests that built a runtime with those keys are rewritten around the new routes; the old behaviours they covered (case-insensitive primary name, unknown-name warning) leave with the variables. Setting an old variable is ignored with one logged warning. EBG-0161 is fixed by a shared helper that strips and treats blank as unset, used for every model variable.

# 7. Cross-Work-Package Flags

* **WP6 (moderation) and the acceptance measurement.** The plan's WP3 acceptance asks for measurements "with the Child-profile moderation path active", but the moderation model is built in WP6. WP3c therefore measures the chat model with a stand-in co-loaded small model, and the **final** figure with the real moderation model is taken in WP6. This is a sequencing dependency, named rather than absorbed.
* **WP5.** First-run screens, the settings UI, the OS keychain for the key, and the memory-sharing screen. WP3 exposes RPCs only; until WP5 the key comes from `ANTHROPIC_API_KEY`.
* **WP4.** Restyles the badge, dialog and button of 6.7.
* **Policy change.** The new rule in `TrustTierPolicy` (6.8) is a change to the Sentinel boundary, not a configuration: it is reviewed as such.
* **WP6.** Child consent, moderation of the cloud reply, the AI disclosure. WP3 denies Child escalation until then.
* **Timing.** WP3 builds in Session B (plan weeks 3-4); the Mac visits cover the Mac half of the WP3c measurement.

# 8. Evidence Pack (TPL-0001 Section 6)

| Item | Content |
|---|---|
| API facts | Section 4, last bullet, to be re-confirmed against the live API in WP3a (headers, usage fields, error shapes, the refusal and 529 behaviour). Ollama: `/api/version`, `/api/tags`, `/api/pull` (streamed JSON lines with `status`, `total`, `completed`) - verified live against the installed Ollama in WP3c. |
| Platform coverage | Adapter, ledger, routes and policy are pure Python, identical on Windows and macOS. Detection paths and `nvidia-smi` are per platform and tested with injected readers; real behaviour on the Mac at Mac visit 1 or 2. |
| CI | Existing jobs; no workflow change. The Linux check runs in Docker before each commit. |
| Tests | Adapter with injected transport (request shape, text-only parsing, refusal, 529 and 4xx mapping, no credential in errors); two-route behaviour (no cloud call on local failure); ledger (reserve, settle, release, cap, month roll-over, concurrency); escalation (token binding, expiry, replay, the role matrix at both layers, a missing role, cap refusal, memory notes omitted by default); deadline-capped timeout for all four adapters; recommendation from injected hardware; pull allow-list; the rewritten runtime tests. |
| Live checks (S5) | A real call (reply, usage, cost within expectation); the refusal path if reproducible; the **Console limit's behaviour** (the plan asks WP3 to verify it): a test workspace with a very small limit, recording the status and error type returned at the limit. Total spend at most US$2. |
| New dependencies and features | None (`urllib`). No new OS permission. No new crate. |
| Privacy (D23) | The ledger and audit store counts and categories only. Memory notes are off by default. The confirmation states what is sent. Nothing is sent without a confirmation. |

# 9. Commit Contents (expected, per sub-WP; finalised at build)

**WP3a:** `sentinel/anthropic_provider.py`, `sentinel/providers.py`, `sentinel/ollama_provider.py`, `sentinel/openai_provider.py`, `sentinel/gemini_provider.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/tests/test_anthropic_provider.py`, and the changed provider and runtime tests, plus the record files.
**WP3b:** `jarvis/shared/spend_ledger.py`, `jarvis/interfaces/escalation.py`, `jarvis/identity/` (migration, setting), `jarvis/guardian/runtime.py`, `sentinel/policy.py` (new cloud-escalation rule), `src/App.jsx` and its Playwright tests, with tests and records.
**WP3c:** `jarvis/interfaces/ollama_setup.py`, `jarvis/config/ollama_models.json`, `jarvis/interfaces/stdio_rpc.py`, tests and records.

# 10. Questions for the Engineering Reviewer

1. Is splitting local and cloud into two capabilities, with cloud reachable only by confirmed escalation, the right way to honour "never automatic" (6.1)?
2. Is `urllib` against the Messages API acceptable for the Anthropic adapter (S2), given the SDK is the default recommendation?
3. Is the reserve-then-settle ledger sound under the slow lane's threads, and is "unknown model priced at the highest rate" the right failure direction (6.3)?
4. Does treating a refusal as "not a provider fault" and answering honestly (6.2) have a hole - for a Child profile especially?
5. Is a one-time, profile-bound, expiring token the right confirmation mechanism for escalation (6.5), and what can a hostile caller do with it?
6. Is the WP3a/b/c split sound, and is the moderation dependency (Section 7) handled honestly?

# 11. Version History

| Version | Date | Author | Summary |
|---|---|---|---|
| 0.3 | 8 October 2026 | Claude Engineering Implementer | Programme Sponsor approved decisions S1-S6 as recommended (chat, 8 October 2026): Sonnet 5.5 at low effort; `urllib`; v1 suggestion rules; cap US$37.50 with 80 percent warning; up to US$2 live spend; Child escalation denied until WP6. This is the design approval of rule A6; nothing is built, and the build waits for Session B to open. |
| 0.2 | 8 October 2026 | Claude Engineering Implementer | Design review Pass (Gemini, single reviewer, no web access). Correction found afterwards by the Engineering Implementer: Sentinel's policy has no role concept, so the gate (6.8) is now two independent checks and the policy rule is named as new work; existing history and message bounds recorded (Section 4); Section 12 review record. |
| 0.1 | 8 October 2026 | Claude Engineering Implementer | Initial design draft, ahead of Session B under D22: two-route split, Anthropic adapter on `urllib`, spend ledger, suggest-then-confirm escalation, per-profile memory control, Ollama detection and pull, deadline-capped timeouts, unregistering OpenAI and Gemini. Six Programme Sponsor decisions with recommendations. Nothing built. |

# 12. Design Review Record

**Review 1** (Antigravity CLI, Gemini, through `run_reviewer.py`; 2026-10-08T11:36Z, `sender: reviewer`, no resumes): **Pass.** It answered the six questions in Section 10 affirmatively: two capabilities is the right fix for "never automatic"; `urllib` is acceptable and preferred; the reserve-then-settle ledger is sound and pricing an unknown model at the highest rate fails in the safe direction; treating a refusal as not a provider fault is correct, including for a Child; the one-time profile-bound token resists replay and profile switching; the split and the moderation dependency are handled honestly. It found Section 4's claims about current behaviour true and nothing missing, and judged all six Sponsor decisions sound. It could not check any Anthropic API fact (endpoint, headers, model names, prices, `output_config`, disabled-thinking and sampling rejections, `stop_reason`, 529 and 402); those are verified live in WP3a.

**Caveats, disclosed:** a single reviewer, entirely affirmative, with no web access. **One statement of its is wrong about the code as it stands:** it said "the TrustTierPolicy explicitly denies [Child and Guest] for the escalation intent". No such rule exists; it was describing the design. The Engineering Implementer read `sentinel/policy.py`, confirmed the policy has no role input, and rewrote 6.8 accordingly (v0.2). Because the reviewer accepted the unbuilt rule as present, the role gate should get a second look in the implementation review, with the Child and Guest tests of 6.8 as the evidence.
