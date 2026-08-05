# EIP-ESR0050-001 - Agent Framework UXP Wiring

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0050-001 |
| Title | Agent Framework UXP Wiring |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0050 WP2 |

---

# 2. Purpose

This package wires the Agent Framework - implemented as real backend code at [[ESR-0049_ENGINEERING_SESSION_REPORT|ESR-0049]] (`jarvis/agents/`, `SentinelGatedAgentService`, `guardian.agent.list`/`guardian.agent.invoke` JSON-RPC methods) - into the live User Experience Platform. It closes the gap both README.md and PCB-0001 currently disclose explicitly: "no UXP surface exists for invoking it yet."

---

# 3. Objective

Add a live, real UXP surface that lists the Agent Framework's registered specialist agents and lets a household member invoke one (`gia-observability`, the only agent currently registered) and see its real returned result - not a static mock-up, matching every prior UXP wiring package's own no-mock-fallback discipline (ESR-0017 WP9).

This directly satisfies PBK-0001's Feature-First Delivery Discipline's live-UXP-progress requirement more directly than any other candidate considered at this session's WP0B objective-selection question.

---

# 4. Repository Context

Investigated before drafting scope:

- `jarvis/interfaces/sentinel_agent.py` (`SentinelGatedAgentService`, `AgentOutcome`) and `jarvis/guardian/runtime.py` (`GuardianRuntime.invoke_agent()`/`available_agents()`) - the backend surface this package calls through, unchanged by this package.
- `jarvis/interfaces/stdio_rpc.py`'s `_guardian_agent_list`/`_guardian_agent_invoke` handlers - confirm the exact JSON-RPC param/response shape (`guardian.agent.list` takes no params, returns `{"agents": [...]}`; `guardian.agent.invoke` takes `{"agent": str, "task": str, "parameters": object}`, returns `{"status": str, "message": str|None, "payload"?: object}`).
- `jarvis/agents/gia_agent.py`'s `GiaObservabilityAgent.execute()` - confirms `task`/`parameters` are accepted for contract conformance but ignored; the agent always returns the same GIA snapshot payload (`cpuPercent`, `memoryPercent`, `memoryUsedMb`, `memoryTotalMb`, `diskPercent`, `diskUsedGb`, `diskTotalGb`, `processStatus`, `processUptimeSeconds`, `processCpuPercent`, `processMemoryMb`, `capturedAt`, all strings), so the UXP can invoke it with an arbitrary non-empty task string and no parameters.
- `src-tauri/src/lib.rs`'s existing `#[tauri::command]` functions (`list_profiles`, `create_profile`, `select_profile`, `speak_message`, `transcribe_audio`) - the exact pattern every existing backend-calling Tauri command follows: thin wrapper around the shared `call_backend(state, app_handle, "<rpc.method>", json!({...}))` helper, registered in `tauri::generate_handler![...]`.
- `src/App.jsx` - `deriveCapabilityStatuses()` (the existing live-derivation pattern for sidebar capability rows, currently covering `memory`/`sentinel`/`providers`), `SystemHealthPanel`/`DiagnosticsPanel` (existing side-column panel component pattern), and the pre-existing static `agent-framework` capability-sidebar row (`src/platformStatus.js`, currently hardcoded `STATUS.PLACEHOLDER`, "Specialist capabilities will extend Guardian").
- `src/KnowledgeGraphPanels.jsx` - the existing pattern for a dedicated side-column panel file with its own `dt`/`dd` metric-row rendering (`.metrics-list`/`.metric-row` CSS classes), reused by this package rather than duplicated.
- `src/styles.css` - confirms `.diagnostics-panel`/`.system-health-panel`/`.knowledge-metrics-panel` already share a common bordered-card base style and `.metrics-list`/`.metric-row` styling this package's new panel reuses directly.
- `tests/e2e/app.spec.js`'s `mockTauriIpc()` helper - the existing in-page Tauri IPC mock pattern (`window.__TAURI_INTERNALS__.invoke`), which every existing Tauri command must be added to or its rejection ("Unmocked Tauri command") will surface as an honest `agentsError` state rather than breaking unrelated tests, since this package's new `useEffect` call is caught the same way `list_profiles`/`active_profile` already are.

---

# 5. Scope

## 5.1 Two new Tauri commands: `src-tauri/src/lib.rs`

- `list_agents(state, app_handle) -> Result<Value, String>` - thin wrapper calling `call_backend(&state, &app_handle, "guardian.agent.list", json!({}))`, matching `list_profiles`'s exact shape.
- `invoke_agent(state, app_handle, agent: String, task: String) -> Result<Value, String>` - thin wrapper calling `call_backend(&state, &app_handle, "guardian.agent.invoke", json!({ "agent": agent, "task": task, "parameters": {} }))`. `parameters` is hardcoded empty - `GiaObservabilityAgent` (the only registered agent) ignores it, and no UI input for arbitrary parameters is in scope (see Exclusions).
- Both registered in `tauri::generate_handler![...]`.

## 5.2 Live capability-sidebar row: `src/App.jsx`

`deriveCapabilityStatuses(platformState, platformError, agents, agentsError)` gains two new parameters (`agents`, `agentsError`) and an `agent-framework` branch, mirroring the existing `memory`/`sentinel`/`providers` connecting/offline/live pattern: `STATUS.CONNECTING` before the first `list_agents` response resolves (`agents === null`), `STATUS.OFFLINE` on error (`agentsError` set), `STATUS.AVAILABLE` with a count/name detail when one or more agents are registered, `STATUS.PLACEHOLDER` (existing static default, unchanged wording) if the list resolves empty (`agents.length === 0`). This is the first live use of the existing `STATUS.AVAILABLE` enum value. The call site (`deriveCapabilityStatuses(platformState, platformError)` in `App()`'s render) is updated to pass the two new arguments.

## 5.3 New side-column panel: `src/AgentFrameworkPanel.jsx`

A new file, mirroring `KnowledgeGraphPanels.jsx`'s pattern (a small file exporting one or more related panel components). Exports `AgentFrameworkPanel({ agents, agentsError, agentBusy, agentResult, agentInvokeError, onInvokeAgent })`:

- Connecting/error/empty states mirror `KnowledgeMetricsPanel`'s `PanelStatusMessage` pattern exactly.
- One row per available agent name, each with a "Run" button (disabled while `agentBusy`).
- On successful invocation, renders the returned `payload` as a `dt`/`dd` list reusing the existing `.metrics-list`/`.metric-row` classes - no new metric-rendering CSS, no fabricated figures, exactly the real key/value pairs GIA's snapshot returns.
- A denied/unknown-agent/error outcome renders an inline error message (reusing `.conversation-error`/`.profile-error`'s existing error-text pattern), never silently dropped.

Rendered in `App()`'s existing side-column, before `DiagnosticsPanel` (Codex design-review recommendation: groups the new live panel with the other live-data panels - `SystemHealthPanel`, `KnowledgeMetricsPanel`, `ActiveClustersPanel` - ahead of `DiagnosticsPanel`'s permanently-static rows, rather than after them).

## 5.4 `App()` state and handlers: `src/App.jsx`

New state: `agents` (`null` = connecting, `[]` = empty, otherwise the real name list), `agentsError`, `agentBusy`, `agentResult` (`{ agent, status, payload }` of the last successful invocation), `agentInvokeError`.

New mount-time effect calling `invoke("list_agents")`, following the exact `list_profiles`/`active_profile` pattern already in the same effect block (cancelled-guard, `.then`/`.catch`).

New `handleInvokeAgent(agentName)` handler: sets `agentBusy`, clears `agentInvokeError`, calls `invoke("invoke_agent", { agent: agentName, task: "status" })`. A `"denied"`/`"unknown_agent"` (or any non-success) `status` in the response sets `agentInvokeError` from the response's own `message` rather than treating it as a JS-level rejection (mirroring `handleSpeak`'s `result.status !== "synthesized"` pattern exactly) - it is a valid, honestly-reported `AgentOutcome`, not a transport failure. A genuine rejection (backend unreachable) sets `agentInvokeError` from the caught error, mirroring every other handler in this file.

## 5.5 Test coverage

- `tests/e2e/app.spec.js`'s `mockTauriIpc()` gains `list_agents`/`invoke_agent` mock branches (new optional parameters, sensible defaults so every existing test keeps passing unchanged).
- New Playwright tests: the capability row reflects a real registered agent; the empty-agent-list `STATUS.PLACEHOLDER` state (Section 5.2's fourth branch, explicitly covered here per Codex design-review finding); clicking "Run" renders the real returned payload; a denied/error outcome renders inline rather than silently failing.

---

# 6. Authorised Files

- `src-tauri/src/lib.rs`
- `src/App.jsx`
- `src/AgentFrameworkPanel.jsx` (new)
- `src/platformStatus.js` (only if the static `agent-framework` row's default wording needs adjustment for the new live states - investigate during implementation, not assumed)
- `src/styles.css`
- `tests/e2e/app.spec.js`
- `aiems/governance/sessions/ESR-0050_ENGINEERING_SESSION_REPORT.md`
- `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`
- `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md` (registering this package's backlog item, see Section 11)
- This package, `EIP-ESR0050-001_AGENT_FRAMEWORK_UXP_WIRING.md`

---

# 7. Implementation Requirements

1. `list_agents`/`invoke_agent` Tauri commands must be thin `call_backend()` wrappers only - no new backend logic, no bypass of the existing Sentinel-gated `guardian.agent.invoke` RPC path.
2. `parameters` sent to `guardian.agent.invoke` must be an empty object - no UI-driven arbitrary parameter input in this package (see Exclusions).
3. A denied/unknown-agent outcome must render the outcome's own `message` field to the household member, never a generic fallback that hides the real reason, matching `AgentOutcome`'s own design intent (Sentinel-denial detail hidden internally, but the boundary-response message itself is meant to be shown).
4. The capability-sidebar `agent-framework` row and the new panel must both derive from the same real `list_agents`/`invoke_agent` calls - no static/hardcoded agent name or result anywhere in this package.
5. No existing Playwright test may be broken by this package; `mockTauriIpc()`'s new parameters must default to values that keep every current test passing unchanged.
6. `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` boundary is not touched, approached, or implemented by any new UI affordance or code path - this package only surfaces the already-implemented, already-gated `ROUTINE_INTERACTION` `gia-observability` agent.

---

# 8. Explicit Exclusions

This package does not:

- Add a UI for arbitrary task text or parameters - the "Run" button always sends a fixed task string and empty parameters, matching `GiaObservabilityAgent`'s own no-parameters shape. A free-form task/parameter input is future scope if a second, parameterised agent is ever registered.
- Register, wire, or authorise any new specialist agent beyond the one (`gia-observability`) already implemented at ESR-0049.
- Modify `jarvis/agents/`, `jarvis/interfaces/sentinel_agent.py`, `jarvis/guardian/runtime.py`, `jarvis/interfaces/stdio_rpc.py`'s RPC handlers, or any backend Agent Framework code - this package is UXP-side wiring only, against the existing backend contract.
- Implement, expose, or modify behaviour related to `TrustCategory.LOCAL_AGENT_ACTION` or `GAM-0001` Section 8A in any capacity (this package's own text necessarily *names* that boundary, as this section does, to state what it does not do - the constraint is on behaviour and code, not on the words "LOCAL_AGENT_ACTION" appearing in prose; Codex design-review finding, EIP v0.1 to v0.2).
- Redesign or touch `DiagnosticsPanel`'s existing static "Agents" row (`src/platformStatus.js`'s `diagnostics` array) - that row is a permanently-static UXP-shell self-diagnostic (per its own existing code comment), a different concept from the Agent Framework's live specialist-agent capability this package surfaces elsewhere. Left as a disclosed, out-of-scope naming overlap, not fixed by this package.
- Add production sidecar packaging, streaming updates for agent results, or any change to the UXP-backend bridge's process/crash-restart model - all remain EBG-0050's own separate scope.

---

# 9. Constraints

- `GiaObservabilityAgent` is read-only and reports only already-collected local resource metrics (CPU/memory/disk/process health) - no new data source, no write path, no local-device control of any kind.
- This package depends entirely on the Agent Framework backend delivered at ESR-0049 - no backend behaviour is assumed beyond what that session's tests already verify.
- The new panel is additive UI, following the same rendering-safety discipline every prior UXP package has used (React's default JSX text-escaping; no `dangerouslySetInnerHTML`; the existing CSP-compliant `ClusterSwatch` CSSOM pattern is not needed here, since this panel uses no dynamic inline styling).

---

# 10. Validation

- `npm run build` (Vite production build, clean) - confirms no bundler/syntax errors across the new/modified frontend files.
- `npx playwright test tests/e2e/app.spec.js` - confirms every existing test still passes plus the new Agent Framework tests.
- `cargo build` (or `cargo check`) within `src-tauri/` - confirms the two new Tauri commands compile cleanly.
- `python -m pytest jarvis/tests sentinel scripts/tests` - confirms no backend regression (none expected; no backend file is in the Authorised Files list).
- `python scripts/validate_repository.py` (full mode) - 0 errors expected.

---

# 11. Risks and Dependencies

## Dependencies

- The Agent Framework backend delivered at ESR-0049 (`jarvis/agents/`, `SentinelGatedAgentService`, `guardian.agent.*` RPC methods) - already implemented, tested and pushed; this package only calls it.
- A running JARVIS backend process (`python -m jarvis --ipc-stdio`) for any live (non-mocked) manual verification - the existing `npm run tauri dev` development flow already provides this, unchanged by this package.

## Risks

- **Low**: the new panel could visually crowd the side-column if not carefully sized - mitigated by reusing existing `.diagnostics-panel`/`.system-health-panel` sizing conventions rather than introducing new layout rules.
- **Low**: a stale/cached `list_agents` result could show an agent that a future session removes - accepted as the same staleness window every other `useEffect`-mounted, one-time-fetch panel in this app already has (`platform_status`, `knowledge_graph`, `list_profiles`), not a new risk class introduced by this package.

## New Backlog Item Registered by This Draft

`EBG-0120` - Agent Framework UXP Wiring, Approved Backlog, High (registered in EBR-0001 alongside this draft).

---

# 12. Approval Request

Requesting Codex design review of this draft, followed by Programme Sponsor approval-to-implement (verified via the real Sponsor Approval Service, per the standing session gate discipline) before any code is written.

---

# 13. Related Artefacts

* [[ESR-0049_ENGINEERING_SESSION_REPORT|ESR-0049]] - delivered the Agent Framework backend this package wires into the UXP.
* [[EIP-ESR0049-001_AGENT_FRAMEWORK_PHASE3_FIRST_SPECIALIST_AGENT|EIP-ESR0049-001]] - the backend implementation package this package builds on, unmodified.
* [[ESR-0050_ENGINEERING_SESSION_REPORT|ESR-0050]] - this session, WP2.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0120, this package's registered backlog item.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Feature-First Delivery Discipline, the live-UXP-progress requirement this package satisfies.
* [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] - Section 8A, the boundary this package does not approach.

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 5 August 2026 | Claude Engineering Implementer | **Implemented exactly as scoped in v0.2.** Programme Sponsor approval-to-implement verified via `submit-response` against the real Sponsor Approval Service. New `list_agents`/`invoke_agent` Tauri commands (`src-tauri/src/lib.rs`, thin `call_backend()` wrappers, registered in `generate_handler!`). `deriveCapabilityStatuses()` (`src/App.jsx`) gains `agents`/`agentsError` parameters and an `agent-framework` branch (connecting/offline/available states, first live use of `STATUS.AVAILABLE`). New `src/AgentFrameworkPanel.jsx` (list agents, "Run" button per agent, real returned payload rendered via `.metrics-list`/`.metric-row`, denied/error outcomes shown inline via `.conversation-error`) rendered before `DiagnosticsPanel`. New `App()` state/mount-effect/`handleInvokeAgent` handler mirroring `handleSpeak`'s outcome-status pattern. `src/styles.css` gains `.agent-framework-panel`/`.agent-list`/`.agent-row`/`.agent-name`/`.agent-invoke-button`/`.agent-result-list`, reusing the existing shared panel/metric-row base styles. `tests/e2e/app.spec.js`'s `mockTauriIpc()` gains `agents`/`invokeAgentResult` parameters (defaulting to empty/a representative payload, every existing test unchanged) plus 4 new tests (empty state, registered-agent live state, successful run, denied outcome). Validation: `npm run build` clean; `npx playwright test tests/e2e/app.spec.js` 13/13 passed (9 existing unchanged, 4 new); `cargo check` (`src-tauri/`) clean; `python -m pytest jarvis/tests sentinel scripts/tests` 512 passed/1 skipped (unchanged, no backend file touched); `python scripts/validate_repository.py` 0 errors, 285 warnings. `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` untouched throughout; `sentinel/policy.py` not modified. |
| 0.2 | 5 August 2026 | Claude Engineering Implementer | Codex design review: Pass with 3 non-blocking findings, folded in. Section 8's exclusion wording narrowed from "does not reference LOCAL_AGENT_ACTION" (contradicted by the section's own necessary use of the term) to "does not implement, expose, or modify behaviour related to" it - same for Implementation Requirement 6. Section 5.2 made explicit that `deriveCapabilityStatuses()` gains two new parameters (`agents`, `agentsError`), not just a branch. Section 5.3's panel placement moved from after to before `DiagnosticsPanel`, grouping it with the other live-data panels. Section 5.5 explicitly lists the empty-agent-list test case. |
| 0.1 | 5 August 2026 | Claude Engineering Implementer | Initial draft. Scopes wiring the ESR-0049 Agent Framework backend into the live UXP: two new Tauri commands, a live capability-sidebar row, a new AgentFrameworkPanel side-column panel, App() state/handlers, and Playwright test coverage. Submitted for Codex design review. |
