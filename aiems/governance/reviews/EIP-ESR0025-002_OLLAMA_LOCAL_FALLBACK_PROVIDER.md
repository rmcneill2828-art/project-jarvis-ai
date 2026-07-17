# EIP-ESR0025-002 - Ollama Local Fallback Provider

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0025-002 |
| Artefact ID | EIP-ESR0025-002 |
| Title | Ollama Local Fallback Provider |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0075) |
| Intended Session | ESR-0025 |
| Effective Date | 17 July 2026 |

---

# 2. Purpose

Implements **EBG-0075** (Implement Ollama Local Fallback Provider). PEM-001's Decision Outcome (ESR-0015 WP3a) already named Ollama as the local fallback path and Resilience Principle 5 already requires "local fallback should exist for degraded operation even if quality is reduced" - but this was never implemented. `sentinel/` has only `openai_provider.py` and `gemini_provider.py`; there is no local model adapter at all, so today's only "fallback" is `LocalEchoProvider`, a deterministic stub that echoes text back rather than generating anything.

This session confirmed, conversationally, that the intended role is **resilience fallback**, not complexity-based routing (routine-vs-hard-task tiering is a separate, deferred idea mapping to EBG-0045/EBG-0049 Cost-Aware Provider Routing, pending real usage data) - Ollama sits in the route between the primary cloud provider and `LocalEchoProvider`, exactly as PEM-001 already specifies.

---

# 3. Objective

Give Sentinel a real local-model execution option so a cloud provider outage or missing credential degrades to genuine (if lower-capability) local generation before falling all the way back to the local-echo stub - implemented and tested against the Programme Sponsor's actual running Ollama installation, not assumed.

---

# 4. Repository Context

| Item | Current State |
|------|---------------|
| `sentinel/openai_provider.py` / `gemini_provider.py` | Existing adapter pattern to mirror: configuration validation in `__init__`, injectable `transport` callable for testability, conservative error handling (HTTP status codes surfaced, raw exception messages never surfaced or persisted to audit). |
| `sentinel/local_provider.py` | The current absolute-last-resort fallback (`LocalEchoProvider`) - remains unchanged, stays last in the route. |
| `sentinel/orchestrator.py` | `ProviderOrchestrator.execute()` already fails over to the next provider in a `ProviderRoute` on any exception, marking the failed provider `DEGRADED`. No new health-check or startup-probe mechanism is needed - registering Ollama unconditionally and letting a connection failure hit this existing failover path is consistent with how cloud provider failures are already handled. |
| Ollama, confirmed live at ESR-0025 | Installed (`C:\Users\rober\AppData\Local\Programs\Ollama\ollama.exe`), running, four models pulled (`qwen2.5:7b`, `qwen3:8b`, `qwen3.5:2b`, `qwen3.5:4b`), storage correctly migrated to `I:\Ollama Models` (verified directly - not assumed from the app's settings field alone). A real `/api/generate` call against `qwen3.5:2b` returned `{"response": "pong", "thinking": "...", "done": true, ...}` - confirming the response field is `response`, and reasoning-capable models additionally return a `thinking` field that must not leak into visible content. |
| Confirmed live performance | Cold start (model not yet loaded): ~64s total (`load_duration` ~34s, `prompt_eval_duration` ~23s). Warm (model already loaded): ~6s total (`load_duration` ~0.4s). No credential/API key required - local HTTP server, default `http://localhost:11434`. |
| Cost | None - local compute only, no billed API calls, no new recurring spend (consistent with the Programme Sponsor's no-discretionary-budget constraint). |

---

# 5. Scope

This package authorises a future implementation to:

1. Create `sentinel/ollama_provider.py`, an `OllamaProvider` class mirroring the `OpenAIProvider`/`GeminiProvider` shape: configuration validation, injectable `transport`, conservative error handling. Unlike the two existing adapters, **no `CredentialReference` is required or accepted** - Ollama's local HTTP API has no authentication by default.
2. Call `POST {endpoint}/api/generate` with `{"model": ..., "prompt": ..., "stream": false}`, parse `response["response"]` as the returned content, and explicitly discard `response["thinking"]` if present - it must never be surfaced as conversation content.
3. Configuration defaults: `endpoint` defaults to `http://localhost:11434` (overridable via `ProviderConfiguration.endpoint`, matching the existing pattern); `default_model` has no hardcoded default in the adapter itself - it must be supplied by the caller (`build_default_runtime()`), matching how `OpenAIProvider`/`GeminiProvider` require an explicit model.
4. Wire into `jarvis/interfaces/stdio_rpc.py`'s `build_default_runtime()`: register `OllamaProvider` unconditionally (no credential-presence gate, since none applies) in the `text-generation` route, positioned **between** the primary cloud provider (if registered) and `LocalEchoProvider`. Model selection via a new `JARVIS_OLLAMA_MODEL` environment variable, default `qwen3.5:2b` (the fastest of the four confirmed-installed models - latency matters more than peak capability for a fallback role, per Resilience Principle 5's own "even if quality is reduced"). Endpoint overridable via `JARVIS_OLLAMA_ENDPOINT`.
5. Add `jarvis/tests/test_ollama_provider.py`, mirroring `test_gemini_provider.py`'s structure and coverage (success path, missing-field/malformed-response handling, error wrapping, the `thinking`-field-discarded case specifically).
6. Update `jarvis/tests/test_stdio_rpc.py`'s `configured_providers()` expectations to account for Ollama's presence in the route where relevant.
7. Mark EBG-0075 `Complete` in EBR-0001 only once actually implemented, validated and committed - with corresponding updates to PST-0001 and REG-0001.

No other files are authorised to change. No product UXP changes (`src/`) are in scope - this is a Sentinel-layer capability, not a UI change.

---

# 6. Authorised Files

1. `sentinel/ollama_provider.py`
2. `jarvis/interfaces/stdio_rpc.py`
3. `jarvis/tests/test_ollama_provider.py`
4. `jarvis/tests/test_stdio_rpc.py`
5. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
6. `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`
7. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. `OllamaProvider.__init__`: raise `ValueError` if `configuration.credential is not None` (Ollama must never be configured with a credential - a future accidental copy-paste from the OpenAI/Gemini pattern must fail loudly, not silently ignore a supplied credential) and if `configuration.default_model` is falsy.
2. `execute()`: build the request body `{"model": self._configuration.default_model, "prompt": request.prompt, "stream": False}`; parse `data["response"]` as content; if `"response"` key is missing or not a string, raise `RuntimeError` with a message naming the unexpected shape, matching `OpenAIProvider`/`GeminiProvider`'s "Unexpected {provider} response shape" convention.
3. Timeout: `ProviderConfiguration.timeout_seconds` default (30.0) is too short for a cold-start Ollama load (~64s confirmed). `build_default_runtime()` must construct Ollama's `ProviderConfiguration` with an explicit longer `timeout_seconds` (recommend 90.0) - a cold-start timeout still fails over cleanly to `LocalEchoProvider` via the orchestrator's existing mechanism, so this is a quality-of-experience tuning, not a safety requirement.
4. Error handling: same conservative pattern as the existing adapters - surface HTTP status codes and exception types, never raw exception messages or response bodies (audit trail persistence risk).
5. `build_default_runtime()`: `OllamaProvider` registered and added to the `text-generation` route's provider tuple in position order `[primary_cloud_if_present, "ollama", "local-echo"]`.
6. Tests must not make a real network call to Ollama - `transport` is mocked, matching every existing provider adapter test in this codebase. The confirmed real request/response shapes (Section 4) are the ground truth the mocked tests assert against, not invented data.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Complexity-based / cost-aware routing (routine chat to Ollama, hard reasoning to cloud) - that is EBG-0045/EBG-0049's separate, still-unscoped territory, deferred pending real usage data per this session's own discussion.
2. Any change to `LocalEchoProvider` or its position as the final fallback.
3. A startup reachability probe for Ollama (e.g. pinging `/api/tags` before registering) - registration is unconditional; the orchestrator's existing failover-on-exception handles an unreachable Ollama identically to an unreachable cloud provider.
4. Streaming responses (`"stream": true`) - `stream: false` only, matching this codebase's synchronous request/response model throughout.
5. Any change to which model Ollama uses beyond the `JARVIS_OLLAMA_MODEL` default - not an evaluation of which of the four installed models is "best," simply the fastest for a fallback role.

---

# 9. Constraints

1. `OllamaProvider` must reject any configuration carrying a `CredentialReference` - structurally prevents a future accidental credential leak toward a local, unauthenticated endpoint.
2. The `thinking` field, when present in a model's response, must never appear in `ProviderResponse.content` - a dedicated test must assert this directly using the real confirmed response shape.
3. No implementation shall begin until this package reaches Approved status.

---

# 10. Validation

After implementation, run:

```powershell
python -m pytest
python scripts/validate_repository.py
```

Validation should confirm:

1. Full pytest suite passes, including new `OllamaProvider` tests.
2. A live smoke check (run by the Engineering Implementer directly - unlike the OpenAI/Gemini smoke tests, this makes no billed external call, so it does not require the Programme Sponsor's own "type RUN" confirmation gate) against the Programme Sponsor's actual running Ollama instance, confirming a real `execute()` call returns real generated content.
3. `validate_repository.py` (full mode) passes with the same pre-existing warning count, 0 errors.
4. No unauthorised files changed.

---

# 11. Risks and Dependencies

## Dependencies

1. Ollama installed and running on the Programme Sponsor's machine - confirmed, not assumed, at ESR-0025.
2. `ProviderOrchestrator`'s existing failover-on-exception mechanism (`sentinel/orchestrator.py`), unchanged by this package.

## Risks

1. **This adapter only works on machines with Ollama actually installed and running.** On any other machine (a future production deployment, a colleague's laptop), Ollama registration will simply fail over to `LocalEchoProvider` immediately via the orchestrator's existing mechanism - honest degradation, not a defect, but worth stating plainly rather than implying universal availability.
2. **Cold-start latency (~64s) is real and noticeable** if a user's first request happens to hit Ollama after cloud failure. The 90s timeout recommendation (Section 7 item 3) accepts this rather than hiding it; a future iteration could pre-warm the model at startup if this proves annoying in practice - not in this package's scope.
3. Local model quality (2-8B parameter range) is materially lower than the cloud providers' - acceptable and expected for a fallback role per PEM-001's own Resilience Principle 5, not a defect to fix here.

---

# 12. Approval Request

**Approved and implemented at ESR-0026 WP1.** Engineering Reviewer (Codex) reviewed the full technical scope via the now-working AIEMS Exchange Bridge (`scripts/aiems_bridge.py`) - the first genuine, real (non-manual-relay) review this project has used: no blocking findings; one non-blocking observation (keep the no-credential-rejection and `thinking`-field-discard tests explicit) already satisfied by Sections 7/9's own requirements. Programme Sponsor approved via `sponsor-decision`.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0075 (this package's parent). |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Decision Outcome (ESR-0015 WP3a) naming Ollama as the local fallback path; Resilience Principle 5 this package implements. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status, to record EBG-0075 completion once implemented. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 17 July 2026 | Claude Engineering Implementer | ESR-0026 WP1: Engineering Reviewer (Codex) reviewed via the real AIEMS Exchange Bridge - no blocking findings. Programme Sponsor approved. Implemented exactly as scoped: `sentinel/ollama_provider.py`, wired into `build_default_runtime()`, 11 new tests. Found and fixed a genuine test-isolation defect (a shared test helper was making real network calls to the Programme Sponsor's actual Ollama server, since Ollama needs no credential gate). Live smoke check disclosed: the recommended 90s timeout (Section 7 item 3) actually timed out once, only succeeding at 180s - implemented as approved regardless, noted as a future tuning candidate in Section 11. 249 tests total (was 238), `validate_repository.py` 0 errors, 104 warnings (matching baseline). Status Draft to Approved, version 0.1 to 1.0. |
