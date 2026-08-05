# EIP-ESR0049-001 - Agent Framework Phase 3: First Specialist Agent Implementation

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0049-001 |
| Artefact ID | EIP-ESR0049-001 |
| Title | Agent Framework Phase 3: First Specialist Agent Implementation |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0119 |
| Intended Session | ESR-0049 |
| Effective Date | Pending approval |

---

# 2. Purpose

[[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Track B Phase 3 (the Action faculty) is the next item in the roadmap's dependency chain. Its prerequisites are delivered: Phase 1 (Guardian Cognitive Core, ESR-0039), Phase 2 (Local Agent Permission Boundary, [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A, ESR-0041), and the contract architecture itself ([[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]]'s Agent Framework subsection, [[EIP-ESR0048-001_AGENT_FRAMEWORK_ARCHITECTURE_SCOPE|EIP-ESR0048-001]], ESR-0048).

EIP-ESR0048-001 was deliberately architecture-only: it named `SpecialistAgent`/`AgentRequest`/`AgentResult` as a proposed contract shape "for a future implementation package to build against," and explicitly stated no file should claim to contain those names "until a future package actually creates them." This is that future package - the first real code.

The Programme Sponsor selected this as ESR-0049 WP2's objective directly, via the two-part objective-selection question at session open.

---

# 3. Objective

Implement the `SpecialistAgent` contract as real code, and wire GIA's existing read-only local resource observability (`jarvis/gia/observability.py`, a Proof of Concept since ESR-0012) as the first concrete specialist agent - classified `ROUTINE_INTERACTION` per MOD-0001's own rule, evaluated through the mandatory, shared Sentinel gate before every invocation - without touching, narrowing, or otherwise authorising anything under GAM-0001 Section 8A's `LOCAL_AGENT_ACTION` boundary.

---

# 4. Repository Context

| Item | Current State |
|------|----------------|
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] Agent Framework subsection | Defines the contract shape this package builds: a `SpecialistAgent` Protocol (`name: str`, `execute(request: AgentRequest) -> AgentResult`), the mandatory shared-gateway Sentinel gate, and the `ROUTINE_INTERACTION`/`LOCAL_AGENT_ACTION` classification split. Names GIA-BOOT as the plausible first `ROUTINE_INTERACTION` example, "a future decision not made" by that package. This package makes that decision. |
| `jarvis/gia/observability.py` `LocalResourceObserver.snapshot() -> GiaSnapshot` | Confirmed directly against the live code: reads CPU/memory/disk/process-health state via `psutil`, never modifies anything, does not go through Sentinel's request path today at all (per GAM-0001 Section 8A.1: "Observation is not control... does not go through Sentinel's request path at all"). This package adds a Sentinel-gated wrapper around it; it does not change `LocalResourceObserver` itself. |
| `sentinel/policy.py` `TrustTierPolicy.classify()` | Returns `TrustCategory.ROUTINE_INTERACTION` (the fallthrough case) for any `SentinelRequest` whose `payload_type` is not in `{"local_agent", "device_control"}`, whose `metadata["capability"]` is not `"local_agent"`/`"emergency_control"`, and whose `requires_approval` is `False`. Confirmed directly against the live code. This package's agent-invocation request uses a distinct `payload_type`/`capability` that does not match any denied or reviewed category, and `requires_approval=False` - it will classify `ROUTINE_INTERACTION` and evaluate `ALLOW`. This package does not change `sentinel/policy.py`. |
| `jarvis/interfaces/sentinel_conversation.py` `SentinelGatedConversationProvider` | The concrete pattern this package's `SentinelGatedAgentService` mirrors: constructs one `SentinelRequest` per invocation with a fixed `source`/`intent` and `metadata={"capability": ...}`, calls `self._gateway.evaluate()`, and only proceeds on `SentinelDecisionOutcome.ALLOW` - otherwise returns a named non-`None` denial outcome, never raising or silently failing. |
| `jarvis/interfaces/voice.py` `SpeechOutcome`/`TranscriptionOutcome` | The concrete pattern this package's `AgentOutcome` mirrors: a frozen dataclass with a mandatory non-empty `status` string covering every real outcome (success, not-connected, denied, unavailable) as a distinct, separately assertable value - never `None` or a raised exception standing in for a boundary failure. |
| `jarvis/interfaces/stdio_rpc.py` `build_default_runtime()` | Constructs one shared `SentinelTrustGateway(policy_engine=TrustTierPolicy())` instance and passes it into every gated capability (conversation, memory, speech, transcription) - MOD-0001's "reuse the existing shared gateway, not a freshly constructed one" requirement. This package's agent service is constructed the same way, in the same function, from the same `gateway` variable. |
| `jarvis/guardian/runtime.py` `GuardianRuntime` | Currently takes `conversation_provider`, `memory_service`, `speech_provider`, `transcription_provider` as constructor arguments, with `speak()`/`transcribe()` as the pattern for an optional capability that degrades honestly (`not_connected`) when absent. This package adds an `agent_service` parameter and an `invoke_agent()` method following that same optional-capability pattern - though the GIA agent is always registered when `build_default_runtime()` runs (it has no external credential/model dependency, unlike Piper/Whisper), so in practice `invoke_agent("gia-observability", ...)` is always available once the runtime starts. |
| `jarvis/platform/shell.py` `GuardianShellCapability` | Contains a static status entry named `"Agent Framework"` with `state=PLACEHOLDER`, "Future specialists extend Guardian without separate AI identities." Once a real agent is wired, this becomes stale under PBK-0001's no-mock-fallback rule (a placeholder implying less capability than actually exists, the inverse of the more commonly-caught overstatement case) - this package corrects it to `AVAILABLE` with an accurate summary, surfaced live to the UXP capability panel via the existing `platform.status` RPC method (no `src/`/`src-tauri/` file change required - the panel already renders whatever `platform.status` reports). |
| GAM-0001 Section 8A | Unaffected. No `SentinelRequest` this package constructs ever sets `payload_type` to `"local_agent"`/`"device_control"` or `metadata["capability"]` to `"local_agent"`/`"emergency_control"`. `TrustCategory.LOCAL_AGENT_ACTION` remains hard `DENY`, exactly as before this package. |

---

# 5. Scope

## 5.1 New module: `jarvis/agents/`

- `jarvis/agents/__init__.py` - package marker.
- `jarvis/agents/contracts.py`:
  - `AgentRequest` (frozen dataclass): `task: str`, `parameters: Mapping[str, str] = field(default_factory=dict)`.
  - `AgentResult` (frozen dataclass): `status: str`, `payload: Mapping[str, str] = field(default_factory=dict)`, `message: str | None = None` - mirroring `SentinelRequest`'s own non-empty-string validation pattern in `__post_init__`.
  - `SpecialistAgent` (Protocol): `name: str` (property), `execute(request: AgentRequest) -> AgentResult` (method) - exactly as MOD-0001 named it, no shape change.
- `jarvis/agents/gia_agent.py`:
  - `GiaObservabilityAgent`, implementing `SpecialistAgent`. `name = "gia-observability"`. `execute()` calls `LocalResourceObserver.snapshot()` (constructor-injected, not constructed internally - matches the existing dependency-injection pattern used for providers) and serialises the returned `GiaSnapshot`'s fields into `AgentResult.payload` (all values as `str`, matching `Mapping[str, str]`), with `status="reported"`.

## 5.2 Sentinel-gated invocation: `jarvis/interfaces/sentinel_agent.py`

- `AgentOutcome` (frozen dataclass), mirroring `SpeechOutcome`/`TranscriptionOutcome`: `status: str` (`"reported"`, `"denied"`, `"unknown_agent"`, `"not_running"`), `result: AgentResult | None`, `message: str | None`. `__post_init__` enforces `result` is present only when `status == "reported"`, matching the existing speech/transcription pattern exactly. **`"reported"` is `GiaObservabilityAgent`'s own chosen success status for this first agent, not a fixed universal contract value** (Codex design-review finding, folded in) - `AgentResult.status`/`AgentOutcome.status` remain general string fields; a future agent may define a different successful-status string appropriate to its own capability. `SentinelGatedAgentService.invoke()` treats any status the agent itself returns as success and wraps it into `AgentOutcome(status=result.status, result=result)` - it does not hardcode `"reported"` as the only valid success value.
- `SentinelGatedAgentService`: constructor takes `gateway: SentinelTrustGateway` and `agents: Mapping[str, SpecialistAgent]`. `invoke(agent_name: str, request: AgentRequest) -> AgentOutcome`:
  1. If `agent_name` not in the registry, return `AgentOutcome(status="unknown_agent", ...)` - no Sentinel call made, since there is nothing to evaluate.
  2. Otherwise construct one `SentinelRequest(source="jarvis.agents", intent=f"agent.invoke.{agent_name}", metadata={"capability": "routine_interaction"})` and call `gateway.evaluate()`.
  3. If the decision is not `ALLOW`, return `AgentOutcome(status="denied", ...)` - never raises, matching the conversation/speech/transcription denial pattern.
  4. Otherwise call the agent's `execute()` and wrap its `AgentResult` in `AgentOutcome(status=result.status, result=result)` - the boundary-level status (`denied`/`unknown_agent`/`not_running`) is `SentinelGatedAgentService`'s own concern; a successful invocation's status is whatever the agent itself reports (`GiaObservabilityAgent` reports `"reported"`; a future agent may report a different value appropriate to its own capability).
  - `available_agents() -> tuple[str, ...]` - registered agent names, for the `guardian.agent.list` RPC method below.

## 5.3 `GuardianRuntime` wiring

- New optional constructor parameter `agent_service: SentinelGatedAgentService | None = None`, following the existing `speech_provider`/`transcription_provider` optional-capability pattern.
- New method `invoke_agent(agent_name: str, task: str, parameters: Mapping[str, str] | None = None) -> AgentOutcome`, returning `AgentOutcome(status="not_running", ...)` when the runtime has not started (mirroring `speak()`'s `not_running` handling) or when `agent_service` is `None`.
- `build_default_runtime()` (`jarvis/interfaces/stdio_rpc.py`) constructs `SentinelGatedAgentService(gateway=gateway, agents={"gia-observability": GiaObservabilityAgent(LocalResourceObserver(...))})` using the same shared `gateway` variable every other gated capability already uses, and passes it into `GuardianRuntime`.

## 5.4 JSON-RPC surface

Two new methods on `StdioRpcServer`, matching the existing `guardian.*` namespace convention (`guardian.speak`, `guardian.transcribe`):

- `guardian.agent.list` - returns `{"agents": [...]}`, the runtime's `available_agents()`.
- `guardian.agent.invoke` - params `{"agent": str, "task": str, "parameters": {...}}`; returns `{"status": ..., "payload": {...}, "message": ...}` from the resulting `AgentOutcome`.

## 5.5 `platform.status` / capability surface

`jarvis/platform/shell.py`'s `"Agent Framework"` `GuardianShellCapability` entry corrected from `state=PLACEHOLDER` to `state=AVAILABLE`, summary narrowly worded to state exactly what exists and no more (Codex design-review finding, folded in): one read-only specialist agent (`gia-observability`), explicitly not implying local action, automation, or device control - for example "One specialist agent available (gia-observability, read-only local resource reporting). No local-agent action capability." Surfaced automatically to the live UXP capability panel through the existing `platform.status` RPC method - no `src/`/`src-tauri/` change required or proposed.

---

# 6. Authorised Files

1. `jarvis/agents/__init__.py` (new)
2. `jarvis/agents/contracts.py` (new) - `AgentRequest`, `AgentResult`, `SpecialistAgent`.
3. `jarvis/agents/gia_agent.py` (new) - `GiaObservabilityAgent`.
4. `jarvis/interfaces/sentinel_agent.py` (new) - `AgentOutcome`, `SentinelGatedAgentService`.
5. `jarvis/guardian/runtime.py` - `agent_service` constructor parameter, `invoke_agent()` method.
6. `jarvis/interfaces/stdio_rpc.py` - `build_default_runtime()` wiring; `guardian.agent.list`/`guardian.agent.invoke` RPC methods.
7. `jarvis/platform/shell.py` - "Agent Framework" capability entry, `PLACEHOLDER` to `AVAILABLE`.
8. `jarvis/tests/` - new test module(s) for the agent contract, `GiaObservabilityAgent`, `SentinelGatedAgentService` (`ALLOW`/`unknown_agent` paths), and new RPC method cases added to the existing stdio-bridge test file.
9. `aiems/models/MOD-0001_PLATFORM_ARCHITECTURE_MODEL.md` - Version History entry only, recording that Section "Agent Framework"'s contract is now implemented (no change to the section's own text, which remains an accurate description of what was built).
10. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md` - EBG-0119 marked Completed.
11. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md` - version sync.

No `sentinel/` file is touched. No `src/`/`src-tauri/` file is touched. No `TrustCategory.LOCAL_AGENT_ACTION` handling is touched.

---

# 7. Implementation Requirements

1. Every `AgentRequest`/`AgentResult`/`AgentOutcome` field must be validated in `__post_init__` exactly as `SentinelRequest`/`SpeechOutcome` already are (non-empty `status`, consistency between `status` and the presence/absence of `result`) - no bare `None`-means-failure pattern.
2. `SentinelGatedAgentService.invoke()` must construct exactly one `SentinelRequest` per call and never set `payload_type`/`metadata["capability"]` to any `LOCAL_AGENT_ACTION`-matching value (`"local_agent"`, `"device_control"`) - confirmed against `sentinel/policy.py`'s live `classify()` at implementation time, not merely carried over from this draft.
3. `GiaObservabilityAgent` must take its `LocalResourceObserver` by constructor injection, not construct one internally - matching every existing provider's dependency-injection pattern and keeping the agent unit-testable with a fake observer.
4. `build_default_runtime()` must pass the same `gateway` variable already used for conversation/memory/speech/transcription into `SentinelGatedAgentService` - not a freshly constructed `SentinelTrustGateway`.
5. The `jarvis/platform/shell.py` capability-state correction (Section 5.5) must accurately describe only what this package actually delivers (one read-only agent) - it must not imply the Action faculty, `LOCAL_AGENT_ACTION`, or any device-control capability now exists.

---

# 8. Explicit Exclusions

This package does not authorise:

1. **Any `LOCAL_AGENT_ACTION`-classified capability.** No agent this package builds can control, configure or modify local device or system state. `sentinel/policy.py` is not touched; the hard `DENY` for `LOCAL_AGENT_ACTION` remains exactly as before.
2. **Any additional specialist agent beyond `gia-observability`.** No Home Assistant, smart-home, Engineering Agent (beyond the read-only GIA example already named in EIP-ESR0048-001), or other capability is implemented or authorised.
3. **Any `src/`/`src-tauri/` (UXP) change.** The new capability is reachable via JSON-RPC and reflected honestly in `platform.status`; a UXP surface for invoking agents directly remains future, separately-scoped work.
4. **Any change to `GAM-0001` Section 8A** or its Action Tiers, Approval Authority, or Non-Goals content.
5. **Any change to the `SpecialistAgent`/`AgentRequest`/`AgentResult` contract shape** beyond what MOD-0001 already scoped - this package implements that shape, it does not revise it (a revision, if needed, would itself be a disclosed deviation requiring its own review, not made silently here).

---

# 9. Constraints

1. No file change shall be made until this package reaches Approved status, per PBK-0001 Principle 3.
2. This package must be reviewed by the Engineering Reviewer (Codex) before implementation, per the standing WP template.
3. `pytest` (jarvis/sentinel test suites) and `python scripts/validate_repository.py` must both pass cleanly before this package is considered complete - unlike EIP-ESR0048-001, this package touches real code and is not exempt from the test suite.

---

# 10. Validation

After implementation, run:

```powershell
python -m pytest jarvis/tests sentinel scripts/tests
python scripts/validate_repository.py
```

Validation should confirm:

1. All existing and new automated tests pass.
2. `validate_repository.py` (full mode) passes with 0 errors.
3. No unauthorised files changed - `git diff --name-only` matches exactly the Section 6 Authorised Files list.
4. Manual cross-check: a live invocation of `guardian.agent.invoke` (`{"agent": "gia-observability", "task": "snapshot"}`) against a running `--ipc-stdio` sidecar returns a real, current local-resource reading, not a stub - and a live invocation with an unknown agent name returns `unknown_agent`, not an error or crash.
5. Manual cross-check: `sentinel/policy.py`'s `TrustCategory.LOCAL_AGENT_ACTION` classification is re-verified unchanged and still hard-`DENY` after implementation.

---

# 11. Risks and Dependencies

## Dependencies

None new. Builds entirely on already-delivered architecture (MOD-0001 Agent Framework, GAM-0001 Section 8A, the shared Sentinel gateway pattern) and an already-existing capability (`jarvis/gia/observability.py`).

## Risks

1. **First real code built against a contract that was itself speculative.** EIP-ESR0048-001 disclosed the `SpecialistAgent` shape as "a starting point... not a settled final contract." This package is the first test of that shape against a real (if simple, synchronous, non-failing) capability - a genuinely longer-running or partially-failing future agent may still expose a shape gap this package's synchronous, always-succeeding GIA wrapper cannot surface. Disclosed as a known limit of this package's validation, not claimed as proof the shape is fully settled.
2. **`jarvis/platform/shell.py`'s capability-state correction is a judgement call about what "Available" should mean** for a one-agent, read-only Agent Framework - flagged explicitly for Engineering Reviewer and Programme Sponsor scrutiny rather than assumed uncontroversial.
3. **No agent-invocation UXP surface is delivered.** The capability is real and live-reachable via RPC and honestly reflected in `platform.status`, but a household member cannot yet trigger it through the interface - consistent with Feature-First Delivery Discipline's allowance for backend-only sessions that demonstrably advance toward the live UXP, but disclosed as a real gap, not treated as already closed.

## New Backlog Item Registered by This Draft

None anticipated beyond EBG-0119 itself, already registered at ESR-0049 WP2 opening.

---

# 12. Approval Request

Draft v0.1 submitted to Codex via direct `codex exec -s read-only` invocation. **Result: Pass with non-blocking findings.** Codex independently verified every Section 4 Repository Context claim against the live cited files (`sentinel/core.py`'s `SentinelRequest.payload_type` default of `"generic"`, `sentinel/policy.py`'s `TrustTierPolicy.classify()`/`evaluate()` behaviour, GAM-0001 Section 8A, `sentinel_conversation.py`, `voice.py`, `jarvis/gia/observability.py`'s `GiaSnapshot` fields, `stdio_rpc.py`/`GuardianRuntime`'s shared-gateway and optional-capability patterns, `shell.py`'s capability entry and state enum), confirmed the proposed scope is "soundly bounded for a first implementation increment" that "does not authorise or approach `LOCAL_AGENT_ACTION`." Two non-blocking findings - (1) `AgentOutcome`'s `"reported"` success status is `GiaObservabilityAgent`'s own chosen value, not a fixed universal contract, so `SentinelGatedAgentService.invoke()` must echo the agent's own reported status rather than hardcoding `"reported"`; (2) the `platform.status` capability-state summary must narrowly state exactly what exists (one read-only agent) and must not imply local action, automation, or device control - both folded into v0.2.

**Programme Sponsor approved.** Verified via `submit-response` directly against the real Sponsor Approval Service (ESR-0049/WP2) before implementation began.

**Implemented as scoped.** Full detail recorded in [[ESR-0049_ENGINEERING_SESSION_REPORT|ESR-0049]] Section 6B. `python -m pytest jarvis/tests sentinel scripts/tests` - 512 passed, 1 skipped (up from 485 passed, 1 skipped before this package - 27 new tests). `python scripts/validate_repository.py` (full mode) - 0 errors.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0119 (this package's parent item). |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Agent Framework subsection - the contract this package implements as real code. |
| [[EIP-ESR0048-001_AGENT_FRAMEWORK_ARCHITECTURE_SCOPE|EIP-ESR0048-001]] | The architecture-only predecessor package this one implements. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8A - the boundary this package's `ROUTINE_INTERACTION` classification stays inside, untouched. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track B Phase 3 (Action faculty) - this package delivers the first real capability under that phase. |
| [[ESR-0049_ENGINEERING_SESSION_REPORT|ESR-0049]] | Session this package is drafted within. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Approval-before-change discipline and Feature-First Delivery Discipline this package follows. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 5 August 2026 | Claude Engineering Implementer | **Implemented as scoped.** Programme Sponsor approval verified via the real Sponsor Approval Service (ESR-0049/WP2). New `jarvis/agents/` module, `SentinelGatedAgentService`, `GuardianRuntime`/`build_default_runtime()` wiring, two new `guardian.agent.*` RPC methods, `platform.status` correction, and 27 new tests delivered exactly as scoped. `pytest` 512 passed/1 skipped; `validate_repository.py` 0 errors. EBR-0001 EBG-0119 marked Completed. |
| 0.2 | 5 August 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) design review via direct `codex exec -s read-only` invocation: **Pass with non-blocking findings.** Every Repository Context claim independently verified against live code; scope confirmed soundly bounded, no approach toward `LOCAL_AGENT_ACTION`. Folded two non-blocking findings: `AgentOutcome`'s success status now echoes the agent's own reported status rather than hardcoding `"reported"` as a universal contract value (Section 5.2); `platform.status` capability-state summary narrowed to explicitly state one read-only agent only, no local-action/automation/device-control implication (Section 5.5). Awaiting Programme Sponsor approval. |
| 0.1 | 5 August 2026 | Claude Engineering Implementer | Initial draft, produced at ESR-0049 WP2. Scopes real implementation of the `SpecialistAgent` contract (`jarvis/agents/`), a Sentinel-gated invocation service mirroring the existing conversation/speech/transcription pattern, `GuardianRuntime`/`build_default_runtime()` wiring, two new `guardian.agent.*` RPC methods, and an honest `platform.status` capability-state correction - wiring GIA's existing read-only observability as the first specialist agent, classified `ROUTINE_INTERACTION`. `LOCAL_AGENT_ACTION` untouched. Not yet reviewed or approved. |
