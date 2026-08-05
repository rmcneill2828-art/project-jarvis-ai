# ESR-0050 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0050 |
| Title | Engineering Session Report |
| Version | 1.3 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0050 |
| Date Opened | 5 August 2026 |
| Date Closed | - |
| Closure Status | Open - WP1-WP2 complete |

---

# 2. Purpose

This report records the opening and execution of ESR-0050, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0049_ENGINEERING_SESSION_REPORT|ESR-0049]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]]. Created at WP0B, before WP1 began.

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0049_ENGINEERING_SESSION_REPORT|ESR-0049]] closed (5 August 2026), [[RBL-0030_REPOSITORY_BASELINE|RBL-0030]] the current accepted baseline, working tree clean at `0d614e0`, pre-commit governance hook active (`core.hooksPath` = `scripts/hooks`), `HEAD` matching `origin/main`.

Unlike the preceding several sessions, WP0A found no stale baseline references anywhere checked (PBK-0001, COC-0001, README, PST-0001 all already correctly point to RBL-0030) - the first WP0A pass in some time with nothing to fix in this category.

The Programme Sponsor selected this session's objective via an explicit two-part objective-selection question at session open: **WP1** content-refreshes [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] and [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] for the Agent Framework Phase 3 capability delivered at ESR-0049 - both were only baseline-pointer-synced at ESR-0049 WP7, with their capability content explicitly disclosed as deferred; **WP2** wires the Agent Framework into the live UXP - adding a `src/` surface that invokes `guardian.agent.list`/`guardian.agent.invoke` against the real `gia-observability` agent, closing README's own disclosed gap ("no UXP surface for it yet") and delivering PBK-0001's Feature-First Delivery Discipline's live-UXP-progress requirement more directly than any other candidate considered.

---

# 4. Engineering Authority

ESR-0050 opening was authorised by direct Programme Sponsor instruction on 5 August 2026, following review of PBK-0001, WP0A repository synchronisation findings, and an explicit two-part objective-selection question confirming this session's WP1/WP2 plan.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

WP1: content-refresh PCB-0001 and the JARVIS Capability Readiness Matrix for the Agent Framework Phase 3 capability (real `jarvis/agents/` module, GIA's read-only observability wired as the first live specialist agent) delivered at [[ESR-0049_ENGINEERING_SESSION_REPORT|ESR-0049]] - disclosed as deferred at that session's WP7.

WP2 onward: wire the Agent Framework into the live UXP - a `src/` surface invoking `guardian.agent.*` against the real backend, replacing the current no-UXP-surface gap.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | PCB-0001 + Capability Readiness Matrix content refresh for Agent Framework | Complete |
| WP2 | Wire Agent Framework into the UXP | Complete |

Further Work Packages will be added if the Programme Sponsor directs the session remain open beyond WP2.

---

# 6A. WP1 - PCB-0001 and Capability Readiness Matrix Content Refresh

Approved directly by the Programme Sponsor via the two-part objective-selection question at session open.

**PCB-0001** (v2.5 to v2.6): Section 4 gains a new Agent Framework row - `jarvis/agents/` contract, GIA's read-only observability wired as the first live `ROUTINE_INTERACTION` specialist agent, reachable via `guardian.agent.*` RPC, no UXP surface yet. Section 6's "Local agent capability is not implemented" constraint reworded to distinguish the now-implemented Agent Framework (one read-only specialist agent) from the still-untouched `LOCAL_AGENT_ACTION`/Action faculty hard `DENY` boundary.

**JARVIS Capability Readiness Matrix** (v2.4 to v2.5): renamed the "Engineering Agent (JARVIS-internal specialist agent)" row to "Agent Framework (specialist agents serving Guardian)" and updated it from Proof of Concept (GIA-BOOT) to Implemented (Foundation), matching the real ESR-0049 delivery. Overall Programme Capability Summary updated to match; the stale "JARVIS-internal specialist Engineering Agent remain not implemented" claim removed.

**Whole-Document Staleness Sweep on Edit**: opening PST-0001 to sync its own Capability Maturity row surfaced further drift unrelated to this WP's own PCB-0001/Matrix scope - Section 5's JARVIS Product Capability Baseline row, Section 8's Current Product Baseline row and Section 9's Repository Health block (Repository Acceptance still citing RBL-0023, seven baselines stale; Product Capability Baseline still citing v2.3/v2.2; Current Activity test/validation figures still citing 382/382 passing and 177 warnings, both many sessions out of date). All corrected in the same pass.

Validation: `python scripts/validate_repository.py` (governance-only mode, no source touched this WP) - 0 errors, 285 warnings (283 pre-existing plus 2 new stray same-document "Section N" cross-references in this report's own prose, non-blocking, consistent with the existing pattern across dozens of other artefacts in this repository).

Files: `aiems/governance/baselines/PCB-0001_PRODUCT_CAPABILITY_BASELINE.md`, `jarvis/architecture/JARVIS_CAPABILITY_READINESS_MATRIX.md`, `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, `aiems/governance/sessions/ESR-0050_ENGINEERING_SESSION_REPORT.md` (this report).

---

# 6B. WP2 - EBG-0120: Agent Framework UXP Wiring

Programme Sponsor selected wiring the Agent Framework into the live UXP as WP2's objective, per the two-part objective-selection question at session open - closing the gap EBG-0119's own EIP-ESR0049-001 disclosed as excluded ("any UXP surface for triggering agents") and README/PCB-0001 disclose as still open.

Registered [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0120 (Agent Framework UXP Wiring, Draft Backlog, High).

Investigated the existing architecture and code before drafting scope: `jarvis/interfaces/stdio_rpc.py`'s `guardian.agent.list`/`guardian.agent.invoke` handlers (the exact param/response shape to wire against), `jarvis/agents/gia_agent.py`'s `GiaObservabilityAgent.execute()` (confirms task/parameters are accepted but ignored), `src-tauri/src/lib.rs`'s existing `#[tauri::command]` pattern (`list_profiles`, `speak_message` et al., all thin `call_backend()` wrappers), `src/App.jsx`'s `deriveCapabilityStatuses()` and existing side-column panel components, `src/KnowledgeGraphPanels.jsx`'s dedicated-panel-file pattern, `src/styles.css`'s shared panel/metric-row classes, and `tests/e2e/app.spec.js`'s `mockTauriIpc()` Tauri IPC mock pattern.

Produced [[EIP-ESR0050-001_AGENT_FRAMEWORK_UXP_WIRING|EIP-ESR0050-001]] (v0.1, Draft): two new Tauri commands (`list_agents`/`invoke_agent`, thin `call_backend()` wrappers, no new backend logic), a live `agent-framework` capability-sidebar row (`deriveCapabilityStatuses()`), a new `src/AgentFrameworkPanel.jsx` side-column panel (list agents, Run button per agent, real returned payload rendered via the existing `.metrics-list`/`.metric-row` classes), `App()` state/handlers mirroring `handleSpeak`'s outcome-status pattern, and Playwright test coverage. Explicitly excludes: arbitrary task/parameter UI input, any new specialist agent, any backend Agent Framework code change, and any approach to `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION`.

Submitted for Codex design review via direct `codex exec -s read-only` invocation - **v0.1: Pass with 3 non-blocking findings.** Codex independently confirmed every Repository Context claim against the real cited source files and found the scope achievable, UXP/Tauri-side only, not requiring backend Agent Framework changes. Findings folded into v0.2: Section 8's exclusion wording narrowed from "does not reference LOCAL_AGENT_ACTION" (contradicted by the section's own necessary use of the term) to "does not implement, expose, or modify behaviour related to" it; Section 5.2 made explicit that `deriveCapabilityStatuses()` gains two new parameters; the new panel's placement moved from after to before `DiagnosticsPanel`, grouping it with the other live-data panels; Section 5.5 now explicitly lists the empty-agent-list test case.

**Approval-to-implement requested and granted via the AIEMS Exchange Bridge, verified against the real Sponsor Approval Service** (`submit-response`, ESR-0050/WP2) before any code was written.

**Implemented exactly as scoped in v0.2.** Two new Tauri commands (`list_agents`/`invoke_agent`, `src-tauri/src/lib.rs`, thin `call_backend()` wrappers). `deriveCapabilityStatuses()` (`src/App.jsx`) gains `agents`/`agentsError` parameters and an `agent-framework` branch - the first live use of the existing `STATUS.AVAILABLE` enum value. New `src/AgentFrameworkPanel.jsx` (list agents, "Run" button, real returned payload rendered via the existing `.metrics-list`/`.metric-row` classes, denied/error outcomes shown inline via `.conversation-error`), rendered before `DiagnosticsPanel`. New `App()` state, mount-effect `list_agents` call, and `handleInvokeAgent` handler mirroring `handleSpeak`'s outcome-status pattern exactly. `src/styles.css` gains the new panel's classes, reusing the existing shared panel/metric-row base styles. `tests/e2e/app.spec.js`'s `mockTauriIpc()` gains `agents`/`invokeAgentResult` parameters (defaulting to values that keep every existing test passing unchanged) plus 4 new tests.

Validation: `npm run build` clean; `npx playwright test tests/e2e/app.spec.js` - 13/13 passed (9 existing unchanged, 4 new); `cargo check` (`src-tauri/`) clean; `python -m pytest jarvis/tests sentinel scripts/tests` - 512 passed, 1 skipped (unchanged, no backend file touched); `python scripts/validate_repository.py` (full mode) - 0 errors, 285 warnings.

`GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` hard `DENY` is untouched throughout; `sentinel/policy.py` not modified; no backend Agent Framework code changed.

Files: `src-tauri/src/lib.rs`, `src/App.jsx`, `src/AgentFrameworkPanel.jsx` (new), `src/styles.css`, `tests/e2e/app.spec.js`, `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, `aiems/governance/sessions/ESR-0050_ENGINEERING_SESSION_REPORT.md` (this report), [[EIP-ESR0050-001_AGENT_FRAMEWORK_UXP_WIRING|EIP-ESR0050-001]].

---

# 7. Related Artefacts

* [[ESR-0049_ENGINEERING_SESSION_REPORT|ESR-0049]] - prior closed session, immediate predecessor; source of both WP1's disclosed deferred content-refresh and WP2's Agent Framework capability.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation, Engineering Session Lifecycle and Feature-First Delivery Discipline guidance followed.
* [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - WP1 target artefact.
* [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] - WP1 target artefact.
* [[PST-0001_PROGRAMME_STATUS|PST-0001]] - swept for further staleness while open for WP1's own sync.
* [[RBL-0030_REPOSITORY_BASELINE|RBL-0030]] - current accepted repository baseline at session open.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0120, WP2's registered backlog item.
* [[EIP-ESR0050-001_AGENT_FRAMEWORK_UXP_WIRING|EIP-ESR0050-001]] - draft Engineering Implementation Package for WP2.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.3 | 5 August 2026 | Claude Engineering Implementer | WP2 Complete: EBG-0120 (Agent Framework UXP Wiring) resolved per EIP-ESR0050-001 (Codex design review Pass with 3 non-blocking findings folded in; Programme Sponsor approval verified via the real Sponsor Approval Service). Two new Tauri commands, live capability-sidebar row, new AgentFrameworkPanel, App() state/handlers, 4 new Playwright tests (13/13 passed). `cargo check` clean, `npm run build` clean, `python -m pytest` 512/1 unchanged, `validate_repository.py` 0 errors. GIA's specialist agent is now invokable live through the UXP. `LOCAL_AGENT_ACTION` untouched. |
| 1.2 | 5 August 2026 | Claude Engineering Implementer | WP2 in progress: registered EBG-0120, produced draft EIP-ESR0050-001 (v0.1, Agent Framework UXP Wiring - two new Tauri commands, live capability-sidebar row, new AgentFrameworkPanel, App() state/handlers, Playwright coverage). Submitted for Codex design review. Not yet approved or implemented. |
| 1.1 | 5 August 2026 | Claude Engineering Implementer | WP1 Complete: PCB-0001 (2.5 to 2.6) and JARVIS Capability Readiness Matrix (2.4 to 2.5) content-refreshed for the Agent Framework Phase 3 capability delivered at ESR-0049. Whole-Document Staleness Sweep on Edit found further PST-0001 drift beyond this WP's own scope (Repository Acceptance still cited RBL-0023, Product Capability Baseline still cited v2.3/v2.2, test/validation figures many sessions stale) - corrected in the same pass. |
| 1.0 | 5 August 2026 | Claude Engineering Implementer | ESR-0050 opened at WP0B, before WP1 began. WP0A found no stale baseline references anywhere checked - first clean WP0A pass in some time. Objective: WP1 content-refreshes PCB-0001/Capability Readiness Matrix for Agent Framework Phase 3; WP2 onward wires the Agent Framework into the live UXP. Selected by the Programme Sponsor via explicit two-part objective-selection question. |
