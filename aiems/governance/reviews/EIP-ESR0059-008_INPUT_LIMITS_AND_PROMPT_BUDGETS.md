# EIP-ESR0059-008 - Input Limits and Prompt Budgets

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-008 |
| Title | Engineering Implementation Package: WP8 Input Limits and Prompt Budgets |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP8 |

---

# 2. Purpose

Implements ESR-0059 WP8, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0143, the first Medium-priority item of the production code review's action plan, under the Programme Sponsor's standing instruction to proceed with the plan.

Nothing bounded what went into a turn: RPC `message`, `text`, `audioBase64` and memory `content` had no size limit (memory could also be blank), every retained memory went into every turn, history entries had no length cap, and no provider call capped its output. With Ollama's 4096-token context, an oversized prompt is silently truncated from the start.

---

# 3. Repository Context Investigated

* `jarvis/interfaces/stdio_rpc.py` handlers for `guardian.converse`, `guardian.speak`, `guardian.transcribe`, `memory.propose` - type checks only.
* `jarvis/guardian/cognitive_core.py` - `history()` and `memory_notes()` (WP7) returned everything.
* `sentinel/ollama_provider.py` `DEFAULT_NUM_CTX = 4096` (EBG-0109) - covers prompt and output together.
* The persona (`GuardianRuntimeConfig().persona`) is 1,746 characters and is sent on every turn.
* `src/App.jsx` - the chat input had no length limit.
* Output caps: OpenAI's gpt-5 family rejects the older `max_tokens` and takes `max_completion_tokens`; on reasoning models (OpenAI gpt-5, Gemini 2.5) internal thinking tokens can count against the cap. No provider key or Ollama model is available in this environment to test a default cap live.

---

# 4. Scope

## 4A. Input limits (RPC boundary)

| Input | Limit |
|---|---|
| `guardian.converse` message | 4,000 characters |
| `guardian.speak` text | 5,000 characters |
| `guardian.transcribe` audio | 20,000,000 base64 characters (about 15 MB) |
| `memory.propose` content | 2,000 characters, not blank |

Oversized input is refused with a clear JSON-RPC error naming the field, its length and the limit. The UXP chat input stops accepting typing at the same 4,000 characters (`MAX_MESSAGE_CHARS`, kept equal to the backend by a test).

## 4B. Prompt budgets (Cognitive Core)

* Each history entry is truncated to 400 characters, with a visible `[truncated]` marker.
* Retained memory notes are kept newest first up to 1,500 characters in total; the oldest are left out of the turn once memory outgrows the budget, never cut mid-note. Nothing is deleted from the store.
* Worst case - persona, 4,000-character message, six full history exchanges, full memory budget and framing - is about 12,650 characters, which at a conservative 3.5 characters per token leaves about 400 tokens of Ollama's context for the reply. A test checks this bound. Initial budgets of 600 and 2,000 were tightened after this calculation showed too little room once the persona is counted.

## 4C. Optional output cap

* `ProviderConfiguration.max_output_tokens` (positive, or None). When set: OpenAI `max_completion_tokens`, Gemini `generationConfig.maxOutputTokens`, Ollama `options.num_predict`.
* `JARVIS_MAX_OUTPUT_TOKENS` configures it for all three. **Off by default, deliberately**: a cap on a reasoning model can be consumed by thinking tokens and leave replies empty, and no model is available here to test a safe default. The Programme Sponsor can enable it once verified with the configured keys; an absent, non-integer or non-positive value leaves output uncapped.

## 4D. Tests

New `jarvis/tests/test_input_limits_and_budgets.py`: every oversized RPC input refused, input at the limit accepted, blank memory refused, frontend and backend message limits equal, history truncation with marker, newest-first whole-note memory budget, the worst-case context bound, output-cap parsing and validation, and the cap reaching each provider's payload only when set (never the older `max_tokens`).

## 4E. Explicitly out of scope

* A default output cap (see 4C).
* Dropping memory by relevance rather than age - there is no retrieval layer yet.
* Raising Ollama's `num_ctx`, which EBG-0109 set for speed.

## 4F. Review

**Review - disclosed self-review** (GitHub Copilot CLI quota re-probed, still exhausted; EBG-0153 applies). Checked: the limits are enforced at the RPC boundary before any runtime call, so an oversized request touches no provider, voice model or store; `len()` counts characters, matching the UXP's `maxLength`; the memory budget only affects what one turn carries - nothing is deleted from the store; the output cap is sent under `max_completion_tokens`, never the `max_tokens` the gpt-5 family rejects; the context bound was recalculated with the real persona length, which is what led to tightening the budgets. No further change needed.

---

# 5. Validation Requirements

* `python -m pytest -q`, `ruff check .`, `python scripts/validate_repository.py`, `npm run build`, `npx playwright test`.
* **Live check against the real backend process**: a 4,001-character message returned `params.message is too long (4001 characters; the limit is 4000).`; a normal message was still answered; a blank memory proposal was refused.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* No oversized input reaches a provider, voice model or the memory store.
* A worst-case turn stays inside Ollama's context with room for a reply.
* Output capping is available per deployment without changing default behaviour.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** on the disclosed self-review. Implemented exactly as at v0.2. Pending commit/push through `submit-response`. |
| 0.2 | 29 September 2026 | Claude Engineering Implementer | Disclosed self-review recorded in Section 4F (Copilot CLI quota still exhausted). Retrospective Copilot review owed (EBG-0153). Not yet approved or committed. |
| 0.1 | 29 September 2026 | Claude Engineering Implementer | ESR-0059 WP8 draft. RPC input limits, UXP chat-input limit, history and memory prompt budgets, optional per-deployment output cap (off by default, disclosed). pytest 689 passed/1 skipped, ruff clean, Playwright 23/23, frontend build clean. Live-checked against the real backend process. Not yet reviewed, approved or committed. |
