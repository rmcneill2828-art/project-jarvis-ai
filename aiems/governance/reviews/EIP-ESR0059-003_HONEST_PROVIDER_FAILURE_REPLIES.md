# EIP-ESR0059-003 - Honest Provider-Failure Replies

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-003 |
| Title | Engineering Implementation Package: WP3 Honest Provider-Failure Replies |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP3 |

---

# 2. Purpose

Implements ESR-0059 WP3, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0141, on the Programme Sponsor's decision to replace the local-echo fallback with an honest failure reply ("start from 1. and work your way down", accepting the recommendation on decision 2).

Two defects, one root cause - the runtime could not tell a model reply from any other text:

* When every real provider failed, `LocalEchoProvider` answered with `local-echo: <the user's own message>`, which the user saw as Guardian's reply (also observed live in EBG-0109 Finding 2(a)).
* `GuardianRuntime.converse()` decided what entered Cognitive Core history by matching the reply against a copied list of error strings. The echo and the empty-message prompt were not on that list, so both were recorded as if Guardian had said them, and fed back into the next turn's prompt.

---

# 3. Repository Context Investigated

* `jarvis/guardian/runtime.py` - `_NON_RECORDABLE_RESPONSES`, four literals duplicated from `sentinel_conversation.py` under a comment asking a future change to promote them to shared constants instead.
* `jarvis/interfaces/sentinel_conversation.py` - the only producer of genuine model replies (its orchestrator success path); every other return is a denial, failure or empty-message prompt.
* `jarvis/interfaces/stdio_rpc.py` `build_default_runtime()` - route `[primary cloud provider?, ollama, local-echo]`. EBG-0070 (ESR-0022) chose the echo tail deliberately as an always-working path; changing it is the Programme Sponsor decision this package implements.
* `ProviderOrchestrator.execute()` already raises when no route provider succeeds, and `SentinelGatedConversationProvider` already turns that into `"JARVIS could not reach an AI provider right now. Please try again."` - so removing the echo tail needs no new failure path.
* Current-state documents claiming echo is the production final failover: README, CURRENT_ARCHITECTURE (two places), PCB-0001, PST-0001, JARVIS Capability Readiness Matrix.

---

# 4. Scope

## 4A. A typed model-reply flag

* `ConversationResponse.is_model_reply: bool = False` (`jarvis/interfaces/conversation.py`). Defaults to `False`, so an unmarked response is never treated as a model reply.
* `SentinelGatedConversationProvider` sets it `True` only on the orchestrator success path. Its denial and provider-unavailable texts are promoted to the named constants `SENTINEL_DENIED_RESPONSE` and `PROVIDER_UNAVAILABLE_RESPONSE`, as the runtime's old comment requested.
* `GuardianRuntime.converse()` records history only when `response.is_model_reply` is true. `_NON_RECORDABLE_RESPONSES` and its duplicated literals are deleted.

## 4B. No echo in the production route

* `build_default_runtime()` no longer registers `LocalEchoProvider`. The route is `[primary cloud provider if credentialled, ollama]`. When every route provider fails, the user gets `PROVIDER_UNAVAILABLE_RESPONSE`.
* `LocalEchoProvider` itself stays in `sentinel/` - still exported, still used by tests and tooling.
* The `guardian.converse` RPC response shape is unchanged (`message`, `provider`).

## 4C. Documentation (Documentation Debt Discipline)

The six echo-is-the-final-failover claims corrected: README (uncontrolled); CURRENT_ARCHITECTURE 1.0 to 1.1 (two places); PCB-0001 2.14 to 2.15; PST-0001 3.41 to 3.42; JARVIS Capability Readiness Matrix 2.13 to 2.14. `stdio_rpc.py` module and function docstrings updated.

## 4D. Tests

* `jarvis/tests/test_guardian_runtime.py`: test doubles now state `is_model_reply` explicitly. Two new tests - a non-model reply is never recorded whatever its text (including a `local-echo:` reply and the empty-message prompt), and a model reply is recorded even when its text equals a failure message (proving text no longer decides).
* `jarvis/tests/test_sentinel_conversation.py`: the flag asserted on each path - empty-message prompt, allow path, review/deny, provider failure.
* `jarvis/tests/test_stdio_rpc.py`: route assertions no longer include `local-echo`; the converse and `serve_forever` tests now assert the honest failure reply when every provider is unreachable, and that the user's message is not echoed.

## 4E. Explicitly out of scope

* Surfacing `is_model_reply` over RPC or styling failure replies differently in the UXP.
* Gemini as a secondary route provider - the next Work Package (EBG-0140/EBG-0051 decision 3).
* Retry, backoff and circuit breaking (EBG-0140).
* Playwright's mocked Tauri IPC still returns `local-echo: <message>` as sample data. It is mock data in the E2E suite, not product behaviour, and the suite passes unchanged; updating the mock text is left out to keep this package's scope to product code.

---

# 5. Validation Requirements

* `python -m pytest -q`, `ruff check .`, `python scripts/validate_repository.py`, `npx playwright test`.
* Live check against the real `build_default_runtime()`.

## 5A. Live check - performed, with a disclosed gap

* **Failure path, verified live**: with Ollama unreachable, `converse()` returned `PROVIDER_UNAVAILABLE_RESPONSE` via `sentinel-gated`, `is_model_reply=False`, and nothing entered history. Previously the same call returned the echo.
* **Success path, not verified live on this machine**: no OpenAI or Gemini key is set in this environment, and the local Ollama installation, started temporarily for this check and stopped afterwards, has **no models installed** (not even the default `qwen3.5:2b`). No model was downloaded without being asked. The success path is covered by the unit tests above, and the provider-adapter path it runs through is unchanged by this package.
* **Consequence the Programme Sponsor should know**: on a machine with no provider key and no Ollama model, every conversation turn now returns the honest failure reply. Before this package it returned the user's own message echoed back. The desktop app needs a provider key in its environment, or an installed Ollama model, to converse.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* No reply the user sees is their own message echoed back as Guardian's answer.
* Only provider-generated replies enter Cognitive Core history, decided by the typed flag.
* No current-state document still claims an echo fallback in production.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 28 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** after being told the disclosed consequence (no provider key and no Ollama model means every turn returns the honest failure reply). Implemented exactly as design-reviewed at v0.2. Pending commit/push through `submit-response`. |
| 0.2 | 28 September 2026 | Claude Engineering Implementer | Design-reviewed via a genuine scoped GitHub Copilot CLI invocation routed through the real bridge (`ESR-0059`/`WP3`, complete 16-file scope) - **Pass**, no findings. Confirmed by search that the provider's orchestrator success path is the only place `is_model_reply=True` is set; the string list fully deleted; `LocalEchoProvider` out of the production route but intact for tests; RPC shape unchanged; all five documents corrected with REG-0001 rows matching and no placeholder history entries; the new tests prove the flag decides history in both directions; exactly 16 files changed. Re-ran pytest (618 passed/1 skipped), ruff (clean) and the validator (0 errors/333 warnings). Not yet approved or committed. |
| 0.1 | 28 September 2026 | Claude Engineering Implementer | ESR-0059 WP3 draft. Typed `is_model_reply` flag replaces string-matched history recording; `LocalEchoProvider` removed from the production route; six stale documentation claims corrected. pytest 618 passed/1 skipped, ruff clean, validator 0 errors, Playwright 23/23. Live failure path verified; live success path not verifiable on this machine (no provider key, no Ollama model), disclosed. Not yet reviewed, approved or committed. |
