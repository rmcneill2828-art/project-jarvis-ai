# ESR-0039 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0039 |
| Title | Engineering Session Report |
| Version | 1.2 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0039 |
| Date Opened | 29 July 2026 |
| Date Closed | - |
| Closure Status | Open - WP1 Complete; session-wide WP2/WP3 not yet run |

---

# 2. Purpose

This report records the opening and execution of ESR-0039, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0038_ENGINEERING_SESSION_REPORT|ESR-0038]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]]. Created at WP0B, before WP1 began.

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0038_ENGINEERING_SESSION_REPORT|ESR-0038]] closed (28 July 2026), [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]] the current accepted baseline, working tree clean, pre-commit governance hook active (`core.hooksPath` = `scripts/hooks`). No open [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] item concerns documentation staleness as its own category, so PBK-0001's Documentation-Debt Priority discipline does not constrain WP0/WP1 selection this session.

`scripts/session_launcher.py` was run to surface candidate objectives. The Programme Sponsor selected **EBG-0108 (Guardian Cognitive Core Implementation)** - flagged since ESR-0034 WP3 as "the single most consequential gap in the whole roadmap" (JRM-0001 Track B Section 7.1/7.3, Phase 1 of the dependency chain) - over smaller Theme 6/7/8 governance-process candidates, consistent with PBK-0001's Feature-First Delivery Discipline.

EBG-0108's own registration text is explicit that "no implementation is authorised by this registration - a future Engineering Implementation Package must define the actual cognitive-core build (reasoning loop, persona persistence, provider-routing integration) against AAM-0001's existing architecture before any code is written." This session's objective is therefore scoping: produce that Engineering Implementation Package for Codex design review and Programme Sponsor approval. Whether implementation proceeds within this same session depends on what that review and approval actually authorise.

---

# 4. Engineering Authority

ESR-0039 opening was authorised by direct Programme Sponsor instruction on 29 July 2026, following review of PBK-0001, README.md and PST-0001, confirming [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]] as the accepted repository baseline at session open, and a direct choice between the session_launcher.py-surfaced candidates via an explicit scoping question.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Scope [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0108 (Guardian Cognitive Core Implementation): define, against [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]]'s existing architecture, the concrete Phase 1 cognitive-core build that closes the gap AAM-0001 and EBG-0108 both name - Guardian's live conversation path (`GuardianRuntime.converse()`) is single-turn and stateless, with no conversation history threaded to the provider and no connection to the already-implemented Personal Memory service (`PersonalMemoryService.list_records()` is never consulted during conversation) - and produce an Engineering Implementation Package for Codex design review and Programme Sponsor approval before any code is written.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | EBG-0108: scope, design and implement the Guardian Cognitive Core Phase 1 build; Codex design review; Programme Sponsor approval | Complete |

---

# 6A. WP1 - EBG-0108: Guardian Cognitive Core Phase 1 Scoping

Reviewed `jarvis/guardian/runtime.py`, `jarvis/guardian/config.py`, `jarvis/interfaces/conversation.py`, `jarvis/interfaces/sentinel_conversation.py`, `sentinel/providers.py` and `jarvis/memory/service.py`/`store.py` in full before drafting scope. Confirmed directly against the live code: `GuardianRuntime.converse()` is stateless and single-turn (no history), and `PersonalMemoryService.list_records()` is never called anywhere in the live `guardian.converse` IPC path - Personal Memory has no influence on Guardian's responses today, despite being fully implemented and tested since ESR-0027.

Produced [[EIP-ESR0039-001_GUARDIAN_COGNITIVE_CORE_PHASE1_SCOPE|EIP-ESR0039-001]] (v0.1, Draft): scopes a new `GuardianCognitiveCore` component that composes persona, retained Personal Memory content and a bounded (default 6-exchange) conversation history into the existing `persona` string before each provider call - deliberately folded into the existing single-turn `ConversationRequest`/`ProviderRequest` shape rather than restructuring the provider abstraction, to keep this first increment's blast radius to `jarvis/guardian/` alone. Explicitly excludes Action/Voice/Vision, any relevance-ranked memory retrieval, and any Sentinel policy change.

The draft discloses a risk it cannot resolve alone (Risk 2): folding Personal Memory content into every provider-bound request means that content will now reach whichever provider is configured as primary, including external cloud providers, with no policy layer (`TrustTierPolicy` remains additive/opt-in; `SimpleApprovalPolicy` is production default, EBG-0074 still open) distinguishing memory-sensitivity from ordinary conversation content. Registered **EBG-0110** (Candidate Backlog) for the underlying gap, and surfaced the proceed-as-scoped-vs-restrict-to-local-provider choice as an explicit Programme Sponsor approval decision rather than deciding it by default.

Submitted to Codex for design review via the AIEMS Exchange Bridge, run in `-s read-only` sandbox mode per the established EBG-0096 pattern - **PASS, no blocking findings**; two non-blocking clarifications (history-exclusion scope widened to all four known non-successful response strings; retained-memory rendering scoped to content-only, no-memory-service behaviour stated directly) folded into v0.2 before Programme Sponsor approval. Codex's findings were relayed verbatim into the bridge transcript under explicit per-instance Programme Sponsor approval for that relay act.

Programme Sponsor approval obtained and verified via `submit-response` directly against the real Sponsor Approval Service (not merely asserted in chat) - including the Risk 2/EBG-0110 decision: proceed as scoped, accepting that memory-informed context reaches whichever provider is configured, with EBG-0110 tracking the underlying policy gap separately.

**Implemented exactly as scoped.** `jarvis/guardian/cognitive_core.py` (new): `GuardianCognitiveCore` composes persona + retained Personal Memory content (read fresh every turn) + bounded 6-exchange conversation history into the existing persona/system-prompt channel - no change to `ConversationRequest`, `ProviderRequest`, `SentinelGatedConversationProvider` or any provider adapter. `jarvis/guardian/runtime.py`: `GuardianRuntime.converse()` composes via the cognitive core and records only semantically successful exchanges (excluding both `GuardianRuntime` boundary-error strings and `SentinelGatedConversationProvider`'s Sentinel-denial/provider-failure strings - the latter two duplicated as local constants since `sentinel_conversation.py` is outside this package's authorised file scope, disclosed as minor tech debt for a future refactor). 14 new/extended tests (9 in `jarvis/tests/test_guardian_cognitive_core.py`, 5 in `jarvis/tests/test_guardian_runtime.py`, covering memory inclusion, fresh-per-turn memory reads, history threading, history bounding, and exclusion of all four non-recordable response strings from history). Full suite: 396 passed, 1 skipped (was 382 passed, 1 skipped - 14 new tests, no regressions).

A standalone `python -m jarvis --ipc-stdio` subprocess smoke check was attempted but abandoned after the test harness itself hung on stdout read with no output - disclosed as a probable issue in the throwaway test script (unrelated to this change, which touches no IPC-layer code), not chased further given effort budget. Confidence instead rests on the existing `jarvis/tests/test_stdio_rpc.py` suite, which already exercises `guardian.converse` through the real in-process dispatch path and passed unchanged, plus this WP's own integration tests exercising the real `GuardianRuntime.converse()` -> `SentinelGatedConversationProvider` -> real Sentinel gateway chain.

[[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] updated (0.4 to 0.5) to record the Reasoning/Memory faculties as Phase 1 implemented. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0108 marked Complete (Phase 1) - Action, Voice, Vision and memory relevance-ranking remain out of scope for future Phase 3/4/5/6 items.

- Files: `jarvis/guardian/cognitive_core.py` (new), `jarvis/guardian/runtime.py`, `jarvis/tests/test_guardian_cognitive_core.py` (new), `jarvis/tests/test_guardian_runtime.py`, [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]], [[EIP-ESR0039-001_GUARDIAN_COGNITIVE_CORE_PHASE1_SCOPE|EIP-ESR0039-001]], [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
- `python -m pytest`: 396 passed, 1 skipped (was 382 passed, 1 skipped - 14 new tests, no regressions).

---

# 7. Related Artefacts

* [[ESR-0038_ENGINEERING_SESSION_REPORT|ESR-0038]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation and Engineering Session Lifecycle guidance followed for WP0A/WP0B.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0108 (this session's objective).
* [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] - the approved architecture the cognitive-core build must be scoped against.
* [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] - Track B Section 7.1/7.3, the roadmap placement motivating this session's objective selection.
* [[RBL-0023_REPOSITORY_BASELINE|RBL-0023]] - current accepted repository baseline at session open.
* [[EIP-ESR0039-001_GUARDIAN_COGNITIVE_CORE_PHASE1_SCOPE|EIP-ESR0039-001]] - this session's WP1 scoping deliverable, produced against AAM-0001's architecture.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.2 | 29 July 2026 | Claude Engineering Implementer | WP1 Complete: Codex design review Pass (two non-blocking clarifications folded into v0.2), Programme Sponsor approval verified via submit-response against the real Sponsor Approval Service, Guardian Cognitive Core implemented exactly as scoped (jarvis/guardian/cognitive_core.py new, jarvis/guardian/runtime.py wired). 14 new/extended tests, full suite 396 passed/1 skipped. AAM-0001 and EBR-0001 (EBG-0108 Phase 1 Complete) updated. |
| 1.1 | 29 July 2026 | Claude Engineering Implementer | WP1 In Progress: drafted [[EIP-ESR0039-001_GUARDIAN_COGNITIVE_CORE_PHASE1_SCOPE|EIP-ESR0039-001]] v0.1 scoping the Guardian Cognitive Core Phase 1 build, registered EBG-0110 (Candidate Backlog) for a disclosed memory-content/external-provider policy gap, submitted to Codex for design review. No source code changed. |
| 1.0 | 29 July 2026 | Claude Engineering Implementer | ESR-0039 opened at WP0B, before WP1 began. Objective: scope EBG-0108 (Guardian Cognitive Core Implementation) and produce an Engineering Implementation Package for Codex review and Programme Sponsor approval. |
