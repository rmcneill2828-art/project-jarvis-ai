# EIP-ESR0039-001 - Guardian Cognitive Core: Phase 1 Memory-Informed Conversation Loop

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0039-001 |
| Artefact ID | EIP-ESR0039-001 |
| Title | Guardian Cognitive Core: Phase 1 Memory-Informed Conversation Loop |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0108 |
| Intended Session | ESR-0039 |
| Effective Date | Pending approval |

---

# 2. Purpose

[[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0108 (Guardian Cognitive Core Implementation) was registered directly to Approved Backlog at ESR-0035 WP2 as "the single most consequential gap in the whole roadmap" (JRM-0001 Track B Section 7.1/7.3, Phase 1 of the dependency chain), but its own registration text explicitly withholds implementation authority: "a future Engineering Implementation Package must define the actual cognitive-core build (reasoning loop, persona persistence, provider-routing integration) against AAM-0001's existing architecture before any code is written." This package is that definition.

Persona persistence and provider-routing integration are already delivered (AAM-0001 v0.4, ESR-0036 WP1; `GuardianRuntimeConfig.persona` statically injected as `ConversationRequest.persona` on every call). What remains, confirmed directly against the live code this session (not inferred from architecture documents alone):

- `GuardianRuntime.converse(message: str)` (`jarvis/guardian/runtime.py`) is stateless and single-turn - it takes no history, and each call is independent of every other.
- `PersonalMemoryService.list_records()` (`jarvis/memory/service.py`) exists and is fully implemented, but nothing in the live conversation path (`guardian.converse`, the JSON-RPC method the Tauri UXP actually calls per `jarvis/interfaces/stdio_rpc.py`) ever calls it. Retained Personal Memory has no influence on Guardian's responses today.

This is the literal, code-confirmed gap AAM-0001 and EBG-0108 both describe as "no memory-informed reasoning loop and no cognitive core sitting between the UXP and the provider layer."

---

# 3. Objective

Define and scope a Guardian Cognitive Core component that composes each conversation turn from three inputs - persona (existing), recent conversation history (new), and retained Personal Memory content (new) - before the request reaches Sentinel/the provider layer, replacing today's direct single-turn pass-through.

---

# 4. Repository Context

| Item | Current State |
|------|----------------|
| `jarvis/guardian/runtime.py` `GuardianRuntime.converse()` | Builds `ConversationRequest(message=message, persona=self._config.persona)` and returns whatever `self._conversation_provider.generate()` returns. No history, no memory lookup, no state carried between calls. |
| `jarvis/interfaces/conversation.py` `ConversationRequest` | Frozen dataclass: `message: str`, `persona: str | None = None`. No history or memory field exists. `ConversationService`'s own in-memory transcript (`_transcript`) is a separate, unrelated code path used by the legacy First Light Tkinter shell, not by `GuardianRuntime` or the live Tauri UXP bridge. |
| `jarvis/interfaces/sentinel_conversation.py` `SentinelGatedConversationProvider.generate()` | Builds `ProviderRequest(prompt=request.message, capability=self._capability, system_prompt=request.persona)`. Passes `persona` straight through as `system_prompt` with no transformation. |
| `sentinel/providers.py` `ProviderRequest` | Frozen dataclass: `prompt: str`, `capability: str`, `metadata: dict`, `system_prompt: str | None`. No structured multi-turn message field - single-turn only, and shared by every provider adapter (OpenAI, Gemini, Ollama, LocalEcho). |
| `jarvis/memory/service.py` `PersonalMemoryService` | `propose()`/`approve()`/`deny()`/`list_records()` fully implemented and tested (ESR-0027). `list_records()` returns all stored records with no filtering, pagination or relevance ranking - a full read of the personal store every time it is called. |
| `jarvis/guardian/config.py` `GuardianRuntimeConfig` | `persona: str = DEFAULT_GUARDIAN_PERSONA` - static, approved verbatim by the Programme Sponsor (AAM-0001 v0.4). Not to be altered by this package. |
| Sentinel policy | `TrustTierPolicy` remains additive/opt-in only; `SimpleApprovalPolicy` is `SentinelCore`'s production default (confirmed at ESR-0023 WP5, tracked as EBG-0074, still open). No policy layer currently distinguishes "ordinary conversation content" from "retained personal memory content" in what reaches a provider. |

---

# 5. Scope

This package authorises a future implementation to:

1. Create `jarvis/guardian/cognitive_core.py`:
   - `GuardianCognitiveCore` - composes the final system-prompt text sent for a turn from three parts, each clearly delimited so persona, memory and history remain visually distinguishable in the composed text (supports debugging and any future policy inspection): (a) the existing static persona text, unchanged; (b) a "Retained Memory" section built from `PersonalMemoryService.list_records()` when a memory service is connected and at least one record exists; (c) a "Recent Conversation" section built from a bounded in-memory history of prior exchanges (default last 6 exchanges - a plain constant, not user-configurable in Phase 1).
   - History is held only in memory, scoped to the running process, exactly like the existing runtime state (`GuardianRuntimeState`, diagnostics list) - no new persistence, no new database table. It is lost on restart, matching every other piece of Guardian's current in-process state.
   - Only a semantically successful model exchange is recorded into history - a response that is none of `GuardianRuntime`'s boundary-error strings (`NOT_CONNECTED_RESPONSE`/`NOT_RUNNING_RESPONSE`) **and** none of `SentinelGatedConversationProvider`'s own non-boundary failure responses ("Sentinel did not allow this request to proceed." on policy denial; "JARVIS could not reach an AI provider right now. Please try again." on provider execution failure) - matching by exact string equality against these four known constants, not by any heuristic. None of these four cases is recorded, so a policy-denied, provider-unreachable or runtime-boundary turn never pollutes future context (Codex design review finding, v0.1: the original wording named only the two boundary-error strings and left the two Sentinel/provider-failure strings ambiguous).
   - Retained-memory rendering is content only: each `PersonalMemoryRecord.content` value, one per line, in `list_records()`'s existing creation-time order. No `id`, `created_at` or `consent_decision_id` field is ever rendered into the composed text - those are internal traceability metadata, not conversational content, and have no reason to reach a provider (Codex design review finding, v0.1).
   - When no memory service is connected, the Retained Memory section is omitted entirely, identically to the already-stated no-records case (Section 7 Implementation Requirement 2) - connection state and empty-result state produce the same observable output (Codex design review finding, v0.1: this package's v0.1 draft left the no-service case only inferable from Section 7, not stated directly in Scope).
2. `jarvis/guardian/runtime.py`: `GuardianRuntime.__init__` gains an internally-constructed `GuardianCognitiveCore` (no new constructor parameter unless testability requires one - to be confirmed during design review, not pre-decided here). `converse()` asks the cognitive core to compose the turn's persona/context text, passes that composed text as `ConversationRequest.persona` exactly as today (no change to `ConversationRequest`'s shape, `SentinelGatedConversationProvider`, `ProviderRequest`, or any provider adapter), and records the exchange afterward.
3. Add `jarvis/tests/test_guardian_cognitive_core.py` and extend `jarvis/tests/test_guardian_runtime.py` covering: composed-text structure (persona always present; memory section present only when records exist; history section present only after a prior successful exchange and bounded at 6); a boundary-error response is never recorded into history; memory records are read fresh on every turn (no stale caching) so an approval that lands between two turns is reflected on the next one.
4. Update [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]]'s Cognitive Architecture section to record that the Guardian Cognitive Core (Reasoning + Memory faculties, Phase 1 scope) now exists in the live runtime, distinct from the still-unbuilt Action/Voice/Vision faculties.
5. Mark [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0108 Complete for this Phase 1 scope only, explicitly recording that Action, Voice, Vision and any relevance-ranked/summarised memory retrieval remain separate, not-yet-authorised future increments - EBG-0108's own text already frames the roadmap this way (Phase 3 Action, Phase 4 Memory expansion, Phase 6 Voice/Vision).

No other files are authorised to change. No product UXP changes (`src/`, `src-tauri/`) are required or in scope - this is a backend cognitive-loop change; the UXP already calls `guardian.converse` unchanged and will simply receive better-informed responses.

---

# 6. Authorised Files

1. `jarvis/guardian/cognitive_core.py` (new)
2. `jarvis/guardian/runtime.py`
3. `jarvis/tests/test_guardian_cognitive_core.py` (new)
4. `jarvis/tests/test_guardian_runtime.py`
5. `aiems/models/AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE.md`
6. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
7. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. `GuardianCognitiveCore` must not mutate or reformat `DEFAULT_GUARDIAN_PERSONA` (`jarvis/guardian/config.py`) - that text was approved verbatim by the Programme Sponsor (AAM-0001 v0.4) and is out of this package's scope to reword. It is prepended, not rewritten.
2. Memory and history sections must be omitted entirely (not rendered as an empty labelled section) when there is nothing to include, so a fresh runtime with no retained memory and no prior exchanges composes byte-identical persona text to today's behaviour - Phase 1 must not change observable behaviour for a user with no retained memory and no conversation history yet.
3. `list_records()` must be called freshly on every turn, not cached across turns within `GuardianCognitiveCore` - a memory approval landing between two conversation turns must be visible on the very next turn.
4. History must be bounded (Section 5 item 1's default of 6) by construction, not by an unenforced convention - the implementation must make it structurally impossible to accumulate unbounded history within a single runtime lifetime.
5. `GuardianRuntime.converse()`'s existing boundary-check behaviour (`NOT_CONNECTED_RESPONSE`, `NOT_RUNNING_RESPONSE`) must be preserved exactly - the cognitive core is only consulted once those checks have already passed.
6. History recording must exclude all four known non-successful response strings (the two `GuardianRuntime` boundary errors and `SentinelGatedConversationProvider`'s Sentinel-denial and provider-failure messages), matched by exact string equality against the existing named constants - not a broader heuristic (e.g. "any short response") that could misclassify a genuinely short but successful model reply.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any Action, Voice or Vision faculty work (AAM-0001's remaining faculties) - Phase 1 is Reasoning and Memory only, per JRM-0001's own phasing.
2. Any change to `ConversationRequest`, `ProviderRequest`, `SentinelGatedConversationProvider` or any provider adapter (`sentinel/providers.py` and its OpenAI/Gemini/Ollama/LocalEcho implementations) - composed context is folded entirely into the existing `persona` string, deliberately avoiding a wider-blast-radius refactor of the provider abstraction for this first increment.
3. Any relevance ranking, summarisation, embedding-based retrieval or size-bounding of Personal Memory content - `list_records()`'s full, unfiltered result is used as-is. This is knowingly not scalable past a small personal store and is disclosed, not solved, by this package (see Section 11, Risk 1).
4. Any new persistence for conversation history - history remains in-process, in-memory, lost on restart, exactly matching every other piece of Guardian's current runtime state.
5. Any Sentinel/`TrustTierPolicy` policy change - Section 11, Risk 2 discloses a real, load-bearing question this package cannot resolve alone, and asks the Programme Sponsor to decide it explicitly as part of approval rather than this package deciding it by default.
6. Any UXP (`src/`, `src-tauri/`) change.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status, per PBK-0001 Principle 3 and EBG-0108's own registration text.
2. Implementation must be reviewed by the Engineering Reviewer (Codex) both at design stage (this package) and post-commit against the real pushed diff, per the standing WP template (draft, review, Programme Sponsor approval, implement, commit, post-commit review) confirmed repeatable across ESR-0026 through ESR-0038.

---

# 10. Validation

After implementation, run:

```powershell
python -m pytest
python scripts/validate_repository.py
```

Validation should confirm:

1. Full pytest suite passes, including the new `test_guardian_cognitive_core.py` cases and extended `test_guardian_runtime.py` cases, with no regression to existing tests.
2. `validate_repository.py` (full mode) passes with 0 errors.
3. A live smoke check (standalone `python -m jarvis --ipc-stdio` invocation, or the real Tauri GUI where available) confirms: a first message with no retained memory behaves identically to today; approving a Personal Memory item and then sending a follow-up message produces a response that is plausibly informed by that memory; a multi-turn exchange shows evidence the prior turn's content reached the provider (e.g. correctly referencing something said two messages earlier).
4. No unauthorised files changed.

---

# 11. Risks and Dependencies

## Dependencies

None new. This package builds on already-implemented, already-tested capability (`PersonalMemoryService`, the persona injection delivered at ESR-0036 WP1, the live `guardian.converse` IPC path hardened at ESR-0037/ESR-0038).

## Risks

1. **Unbounded prompt growth as the personal memory store grows.** `list_records()` returns every stored record with no limit. Acceptable for Phase 1 given the store is new and small, but this will not scale - a future increment (already anticipated by EBG-0108's own Phase 4 "Memory expansion beyond storage" framing) must add relevance filtering or summarisation before the store grows large. Disclosed, not solved.
2. **Retained Personal Memory content will now reach whichever provider is configured as primary - including external cloud providers (OpenAI/Gemini) if the Programme Sponsor has set API keys - with no policy layer distinguishing memory-sensitivity from ordinary conversation content**, because `TrustTierPolicy` remains additive/opt-in and `SimpleApprovalPolicy` (the production default) has no such awareness (EBG-0074, open since ESR-0023). This is not a new gap this package creates - the persona text and every user message already leave the local machine the same way today - but it materially increases what leaves the machine, since Personal Memory content is, by definition, content the Programme Sponsor deliberately chose to retain rather than let pass through unrecorded. **This is a decision this package surfaces for explicit Programme Sponsor approval, not one it makes by default**: proceed with memory-informed context reaching whatever provider is active exactly as scoped above, or restrict Phase 1 to local-provider-only until EBG-0074 is resolved. Recommend registering a new Candidate Backlog item (below, EBG-0110) for the underlying policy gap regardless of which option is chosen, since EBG-0074 already covers the general case and this package's own approval should not silently stand in for closing it.
3. **Bounded history (default 6) is a plain constant, not tuned against real usage** - too short loses useful context, too long grows prompt cost/latency. Acceptable as a defensible starting default for Phase 1; not claimed to be optimal.

## New Backlog Item Registered by This Draft

**EBG-0110** (Candidate Backlog, registered at draft time per the established EIP-ESR0031-001 pattern): Guardian conversation path has no policy-level distinction between ordinary conversation content and retained Personal Memory content when routing to external providers - once EBG-0108 Phase 1 folds memory content into every provider-bound request, this becomes a live data-flow question rather than a purely theoretical one. Related to EBG-0074 (GAM-0001/TrustTierPolicy not operationally connected). No implementation authorised by this registration.

---

# 12. Approval Request

Draft v0.1 submitted to Codex via the AIEMS Exchange Bridge (`ESR-0039`/`WP1`) for design review, run in `-s read-only` sandbox mode per the established EBG-0096 pattern. **Result: Pass, no blocking findings.** Codex confirmed the persona-string composition scope boundary is the right Phase 1 call given `ProviderRequest`'s existing single-turn shape, confirmed Sections 5/7 are otherwise sufficient to prevent scope creep, and explicitly agreed Risk 2/EBG-0110 is correctly framed as a Programme Sponsor decision rather than one this package should resolve itself. Two non-blocking clarifications were raised and folded into v0.2 above: (1) history-exclusion scope widened from the two `GuardianRuntime` boundary-error strings to all four known non-successful response strings, including Sentinel-denial and provider-failure; (2) retained-memory rendering explicitly scoped to record content only (no id/timestamp/consent metadata), and the no-memory-service case stated directly in Scope rather than left inferable from Section 7 alone. Also independently re-ran `python scripts/validate_repository.py`: 0 errors, 184 warnings, matching this session's own evidence.

**Programme Sponsor approved for implementation**, including the Risk 2/EBG-0110 decision: proceed as scoped, accepting that memory-informed context reaches whichever provider is configured, with EBG-0110 tracking the underlying policy gap as separate future work. Verified against the real Sponsor Approval Service via `submit-response` (not merely asserted in chat) before implementation began.

**Implemented exactly as scoped.** `jarvis/guardian/cognitive_core.py` (new): `GuardianCognitiveCore` composes persona + retained memory + bounded history per Section 5, with the Codex-recommended history-exclusion widening and content-only memory rendering from v0.2. `jarvis/guardian/runtime.py`: `GuardianRuntime.converse()` now composes via the cognitive core and records only semantically successful exchanges, matched against all four known non-recordable response strings (two duplicated as local constants from `sentinel_conversation.py`, since that file is outside this package's authorised scope - disclosed as minor tech debt for a future refactor to promote to shared constants). 14 new/extended tests (9 in `jarvis/tests/test_guardian_cognitive_core.py`, 5 in `jarvis/tests/test_guardian_runtime.py`); full suite 396 passed/1 skipped (was 382/1, no regressions). `AAM-0001` and `EBR-0001` (EBG-0108 marked Complete for this Phase 1 scope) updated per Section 5 items 4-5.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Architecture this package builds against; updated by this package once implemented. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0108 (this package's parent item); EBG-0110 (new, registered by this draft). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track B Section 7.1/7.3 phasing this package's scope boundaries follow. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Authority/boundary model relevant to Risk 2; not itself changed by this package. |
| [[ESR-0039_ENGINEERING_SESSION_REPORT|ESR-0039]] | Session this package is drafted within. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Approval-before-change and Working Report Lifecycle discipline this package follows. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 July 2026 | Claude Engineering Implementer | Programme Sponsor approved for implementation (Risk 2/EBG-0110 decision: proceed as scoped), verified via `submit-response` against the real Sponsor Approval Service. Implemented exactly as scoped in `jarvis/guardian/cognitive_core.py` and `jarvis/guardian/runtime.py`; 14 new/extended tests, full suite 396 passed/1 skipped. EBG-0108 marked Complete (Phase 1) in EBR-0001; AAM-0001 updated. |
| 0.2 | 29 July 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) design review via AIEMS Exchange Bridge: Pass, no blocking findings. Folded two non-blocking clarifications: history-exclusion widened to all four known non-successful response strings (Section 5/7), retained-memory rendering scoped to content-only and no-memory-service behaviour stated directly (Section 5). Pending Programme Sponsor approval. |
| 0.1 | 29 July 2026 | Claude Engineering Implementer | Initial draft, produced at ESR-0039 WP1. Registers EBG-0110 (Candidate Backlog) in EBR-0001. Not yet reviewed or approved. |
