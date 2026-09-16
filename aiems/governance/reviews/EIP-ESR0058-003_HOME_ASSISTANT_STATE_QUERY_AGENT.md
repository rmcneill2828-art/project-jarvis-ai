# EIP-ESR0058-003 - Home Assistant State Query Agent

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0058-003 |
| Title | Engineering Implementation Package: WP4 Home Assistant State Query Agent |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0058 |
| Work Package | WP4 |

---

# 2. Purpose

Implements ESR-0058 WP4, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0127: a read-only Home Assistant state-query specialist agent, the narrower candidate [[WR-ESR0057-001_HOME_ASSISTANT_SMART_HOME_INTEGRATION_ASSESSMENT|WR-ESR0057-001]] identified as genuinely buildable independent of Track B Phase 3 (Action faculty, EBG-0128).

---

# 3. Repository Context Investigated

* [[WR-ESR0057-001_HOME_ASSISTANT_SMART_HOME_INTEGRATION_ASSESSMENT|WR-ESR0057-001]] Section 3 - Home Assistant's REST API shape (`GET /api/states/<entity_id>`, Bearer long-lived-token auth) identified as the lowest-friction integration surface.
* `jarvis/agents/contracts.py`, `jarvis/agents/gia_agent.py` - the existing `SpecialistAgent` contract and `GiaObservabilityAgent`'s constructor-injection pattern, followed exactly for the new agent (a client object injected, never constructed internally, keeping the agent unit-testable without a real network call).
* `jarvis/interfaces/stdio_rpc.py` `_build_speech_provider()`/`_build_transcription_provider()` - the absent-credential-means-invisible pattern (Kokoro/Whisper), followed for this agent's own optional registration, since (unlike GIA) it has a genuine external dependency most deployments will not have configured.
* [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8.3 - confirmed observation/monitoring capabilities are distinct from `LOCAL_AGENT_ACTION`; this agent only reads and reports a single named entity's state, never controlling or configuring anything.
* `aiems/models/MOD-0001_PLATFORM_ARCHITECTURE_MODEL.md` "Agent Framework" section - found a stale claim ("no other specific agent (Home Assistant, smart-home, or otherwise) is named or authorised by this section") directly contradicted by this Work Package's own delivery; corrected in the same edit (Documentation Debt Discipline, Whole-Document Staleness Sweep on Edit).

---

# 4. Scope

## 4A. Implement the agent

* `jarvis/agents/home_assistant_agent.py` (new file): `HomeAssistantClient` (thin `urllib`-based REST wrapper - no new third-party HTTP dependency, matching `scripts/aiems_bridge.py`'s own `fetch_latest_decision` precedent) and `HomeAssistantStateQueryAgent` (the `SpecialistAgent` implementation, `name = "home-assistant-state-query"`, requires `parameters["entityId"]`, classified `ROUTINE_INTERACTION` by the existing `SentinelGatedAgentService`'s uniform gating).
* `jarvis/interfaces/stdio_rpc.py`: new `HOME_ASSISTANT_URL_ENV_VAR`/`HOME_ASSISTANT_TOKEN_ENV_VAR` constants; `_build_home_assistant_agent(environ)` helper (absent-credential returns `None`, mirroring `_build_speech_provider()`); `build_default_runtime()`'s `agents` dict construction changed from a literal to a mutable dict so the agent can be conditionally added. **No new RPC method** - reachable through the existing `guardian.agent.invoke`/`guardian.agent.list` methods, unlike WP2/WP3's each-needing-a-new-method shape.

## 4B. Documentation

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0127 closed Complete.
* `aiems/models/MOD-0001_PLATFORM_ARCHITECTURE_MODEL.md` "Agent Framework" section updated: records this as the third specialist agent delivered, and corrects the stale "Home Assistant... not yet authorised" example sentence.

## 4C. Tests

New tests in `jarvis/tests/test_agents.py` (7: two `HomeAssistantClient` constructor-validation rejections, Bearer-header/URL-construction confirmation via a fake `urlopen`, a connection-failure-raises test, agent name, agent reports requested entity, agent requires `entityId`) and `jarvis/tests/test_stdio_rpc.py` (2: absent-configuration means invisible, present-configuration means registered-and-invokable through the real `guardian.agent.invoke` RPC path with a fake `urlopen`).

## 4D. Explicitly out of scope

* Device *control* of any kind - this agent only reads state; `LOCAL_AGENT_ACTION`/Track B Phase 3 remain completely untouched, per WR-ESR0057-001's own finding that the platform gate is independent of this narrower capability.
* A UXP surface - reachable via `guardian.agent.invoke` only, matching the Agent Framework's existing precedent (GIA agents also have no dedicated UXP panel beyond the generic `AgentFrameworkPanel`).
* Multi-entity/bulk state queries, event subscription (WebSocket), or any MQTT integration - WR-ESR0057-001 Section 3 named REST + single-entity query as the lowest-friction starting point; the other surfaces remain future work if ever needed.
* Any actual Home Assistant instance credentials - this Work Package builds and tests the integration path; it does not configure, and the Programme Sponsor has not confirmed, a real deployed Home Assistant instance to point it at.

---

# 5. Validation Requirements

* `python -m pytest jarvis/tests scripts/tests -q` - full suite.
* `python scripts/validate_repository.py` - 0 errors, warning count disclosed.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* `home-assistant-state-query` does not appear in `available_agents()` when unconfigured (no startup failure).
* When `JARVIS_HOME_ASSISTANT_URL`/`JARVIS_HOME_ASSISTANT_TOKEN` are both set, the agent registers and is genuinely invokable through `guardian.agent.invoke`, returning the queried entity's real state (a fake `urlopen` stands in for the actual Home Assistant instance in tests, never a hand-fabricated agent response).
* `GAM-0001`/`sentinel/policy.py`'s `LOCAL_AGENT_ACTION` boundary remains completely untouched.
* Full test suite passes; `validate_repository.py` remains clean.
* MOD-0001's stale "Home Assistant not yet authorised" claim is corrected.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 16 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** after reviewing the full change summary directly. Implemented exactly as drafted at v0.2 - no further content change. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 0.2 | 16 September 2026 | Claude Engineering Implementer | Design-reviewed via a genuine scoped GitHub Copilot CLI invocation, routed through the real bridge (`ESR-0058`/`WP4`, complete 9-file `files_in_scope`) - **Pass**: traced into `sentinel/policy.py`'s `TrustTierPolicy.classify()` itself confirming `ROUTINE_INTERACTION` only, confirmed `_build_home_assistant_agent()`'s absent-credential-returns-`None` behaviour, confirmed `HomeAssistantClient.get_state()` raises rather than fabricates on failure, confirmed all 9 files match with no scope creep. Re-ran the full test suite (583 passed/1 skipped) and `validate_repository.py` (0 errors) independently. Not yet approved or implemented/committed. |
| 0.1 | 16 September 2026 | Claude Engineering Implementer | ESR-0058 WP4 draft. Home Assistant read-only state-query agent implemented and tested (583 passed/1 skipped, up from 574). Drafted directly against the working tree, same disclosed process note as every prior Work Package this session. Not yet reviewed, approved or implemented/committed. |
