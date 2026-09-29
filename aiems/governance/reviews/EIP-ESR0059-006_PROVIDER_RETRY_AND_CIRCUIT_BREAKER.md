# EIP-ESR0059-006 - Provider Retry and Circuit Breaker

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-006 |
| Title | Engineering Implementation Package: WP6 Provider Retry and Circuit Breaker |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP6 |

---

# 2. Purpose

Implements ESR-0059 WP6, completing [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0140 (its routing part was delivered at WP4), under the Programme Sponsor's standing instruction to proceed with the production code review's action plan.

EBG-0140's remaining defects:

* `RetryPolicy` was defined, exported and configurable, but nothing read it - a rate limit or server error failed over immediately.
* A failed provider was marked `DEGRADED`, but `DEGRADED` stayed eligible and never recovered, so health had no effect: a provider that was down cost its full timeout on every turn.
* A non-ALLOW Sentinel decision reaching `ProviderOrchestrator.execute()` was caught as a provider failure and degraded every provider on the route (confirmed by live probe at the review; latent because the conversation provider checks ALLOW first).
* The OpenAI adapter recorded no token usage, and a null `content` (refusal, tool call) surfaced as an `AttributeError` from `ProviderResponse` validation rather than a clear failure.

---

# 3. Repository Context Investigated

* `sentinel/orchestrator.py` - `execute()` and `eligible_providers()`; the latter also feeds `platform.status`'s provider list, so it is deliberately left unchanged (no flicker in the UXP while a circuit is open).
* `sentinel/provider_config.py` `RetryPolicy`/`ProviderConfiguration.retry_policy` - already carried by every adapter's configuration.
* The three text adapters - HTTP errors, network errors and response-shape errors all raised plain `RuntimeError`.
* `aiems/architecture/CURRENT_ARCHITECTURE.md` already listed "Retry and failover" and a "Retry policy model" as Sentinel capabilities. Retry was not actually implemented; after this package those entries are accurate. No document change needed.

---

# 4. Scope

## 4A. Error classification (`sentinel/providers.py`)

* `ProviderError(RuntimeError)` with a `transient` flag - a `RuntimeError` subclass, so the adapters' established failure contract and every existing test are unaffected.
* `TRANSIENT_HTTP_STATUSES` = 408, 425, 429, 500, 502, 503, 504. Other 4xx (bad key, bad model, model not pulled) are permanent. Network failures and timeouts are transient. Response-shape and safety failures stay plain `RuntimeError`, which the orchestrator treats as permanent.
* Each adapter exposes `retry_policy` from its configuration.

## 4B. Orchestrator (`sentinel/orchestrator.py`)

* **Deny short-circuit**: a non-ALLOW decision raises `PermissionError` before any provider is touched; nothing is degraded or recorded as a provider failure (the gateway has already audited the decision).
* **Retry**: up to the provider's `max_attempts`, only for transient failures, with exponential backoff and +/-50% jitter. A retry whose backoff would pass the turn deadline (WP5) is not attempted.
* **Circuit breaker**: a provider that fails is skipped for `circuit_cooldown_seconds` (default 30s), then tried again; a success restores `HEALTHY` and closes the circuit. When every eligible provider is cooling down, the turn fails immediately with a reason naming them. Only failures open a circuit - a health set by an operator via `set_health()` is untouched.
* Success audit events record the number of attempts. Clock, sleep and jitter are injectable for deterministic tests.

## 4C. Wiring and OpenAI adapter

* `build_default_runtime()`: OpenAI and Gemini get `CLOUD_RETRY_POLICY` (2 attempts, ~1s backoff). Ollama keeps a single attempt - it is local, and retrying a cold start that already used its whole timeout would only double the wait.
* OpenAI: null or empty `content` raises `OpenAI returned no text content (finish_reason: X).` - never echoing refusal or tool-call text. Token usage (`usage_prompt_tokens` and so on) and `finish_reason` are recorded in response metadata, matching Gemini.

## 4D. Tests

* Orchestrator: transient failure retried then succeeds, with the exact backoff; permanent failure not retried and fails over; plain `RuntimeError` not retried; retries stop at `max_attempts` with doubling backoff; no retry when the backoff would pass the deadline; circuit skips a failed provider during cooldown and retries it afterwards, restoring `HEALTHY`; every provider cooling down fails fast with no calls; operator-set health untouched; negative cooldown rejected. The existing deny test now asserts the up-front `PermissionError` with no provider called and health untouched.
* Adapters: HTTP status classification for OpenAI (5 statuses), Gemini and Ollama; network errors transient; OpenAI null/empty content; usage metadata; `retry_policy` from configuration.
* RPC: cloud providers carry the one-retry policy, Ollama none. WP4's end-to-end failover test now also shows the retry: OpenAI 503, OpenAI retried, then Gemini.

## 4E. Explicitly out of scope

* A 429 caused by exhausted billing quota is indistinguishable from a rate limit without reading the response body, which the adapters deliberately never surface. It is retried once, then the circuit breaker stops it costing time on every turn.
* A provider whose call timed out only because the turn deadline capped it (WP5) also opens its circuit. With the default 100s budget this can only affect Ollama after both cloud providers used their full timeouts.
* Circuit state lives in memory and resets on restart.

## 4F. Review

**Review - disclosed self-review** (GitHub Copilot CLI quota re-probed, still exhausted; EBG-0153 applies). Checked: circuit state (`_open_until`) is read and written only inside `execute()`, which since WP5 runs only on the single slow-lane worker, so no new cross-thread state is introduced; retry backoff sleeps on that worker, never blocking status, memory or profile calls; the up-front deny check raises before any retry or circuit logic runs; the deadline comparison in the retry path uses real `time.monotonic()`, matching the deadline's own clock even when a test injects a fake circuit clock; a permanent 404 from Ollama (model not pulled) now costs one fast failed call per 30s instead of one per turn.

---

# 5. Validation Requirements

* `python -m pytest -q` (two consecutive runs), `ruff check .`, `python scripts/validate_repository.py`.

## 5A. Live check - performed against the real backend process

`python -m jarvis --ipc-stdio` with Ollama pointed at a non-routable address, no cloud keys and a 6s test deadline, two conversation turns in a row:

* Turn 1: honest provider-unavailable reply at **6.3s** (the deadline), opening Ollama's circuit.
* Turn 2: the same honest reply in **0.0s** - Ollama skipped while cooling down, instead of costing the turn another full wait.
* The backend exited cleanly.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* Transient failures are retried within policy and deadline; permanent ones are not.
* A failed provider stops costing time on every turn, and recovers automatically.
* A Sentinel denial never touches or degrades a provider.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** on the disclosed self-review. Implemented exactly as at v0.2. Pending commit/push through `submit-response`. |
| 0.2 | 29 September 2026 | Claude Engineering Implementer | Disclosed self-review recorded in Section 4F (Copilot CLI quota still exhausted). Retrospective Copilot review owed (EBG-0153). Not yet approved or committed. |
| 0.1 | 29 September 2026 | Claude Engineering Implementer | ESR-0059 WP6 draft. Transient/permanent error classification, deadline-aware retry with backoff and jitter, cooldown circuit breaker, up-front deny check, OpenAI null-content handling and usage metadata. pytest 660 passed/1 skipped (two runs), ruff clean. Live-verified: second turn skipped a failed provider in 0.0s instead of waiting again. Not yet reviewed, approved or committed. |
