# ESR-0049 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0049 |
| Title | Engineering Session Report |
| Version | 1.6 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0049 |
| Date Opened | 5 August 2026 |
| Date Closed | - |
| Closure Status | Open - WP1-WP2 complete, session-wide WP6 (Pass) and WP7 (Establish RBL-0030) complete |

---

# 2. Purpose

This report records the opening and execution of ESR-0049, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex as Engineering Reviewer, Programme Sponsor gating every step.

Opened directly from [[ESR-0048_ENGINEERING_SESSION_REPORT|ESR-0048]]'s closure via WP0A/WP0B session initialisation per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]]. Created at WP0B, before WP1 began.

---

# 3. Scope

WP0A repository synchronisation confirmed: [[ESR-0048_ENGINEERING_SESSION_REPORT|ESR-0048]] closed (4 August 2026), [[RBL-0029_REPOSITORY_BASELINE|RBL-0029]] the current accepted baseline, working tree clean at `7928626`, pre-commit governance hook active (`core.hooksPath` = `scripts/hooks`).

WP0A also found that [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] still cites RBL-0028 as the current accepted repository baseline in three places (Session Start Checklist, Related Artefacts, OSE Relationships) - one baseline stale. ESR-0048 WP1's Documentation Debt Discipline sync corrected the equivalent reference in PBK-0001 but did not include COC-0001, an identical-pattern artefact, in its target list.

The Programme Sponsor selected this session's objective via an explicit two-part objective-selection question at session open: **WP1** corrects COC-0001's stale baseline references, per PBK-0001's Documentation-Debt Priority Until Backlog Cleared rule; **WP2 onward** scopes [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Track B Phase 3 (Action faculty implementation) - the next item in the roadmap's dependency chain, both of whose prerequisites (Phase 1 Guardian Cognitive Core, Phase 2 Local Agent Permission Boundary) are already delivered, but which JRM-0001 itself notes has no backlog item yet authorising its build.

---

# 4. Engineering Authority

ESR-0049 opening was authorised by direct Programme Sponsor instruction on 5 August 2026, following review of PBK-0001, WP0A repository synchronisation findings, and an explicit two-part objective-selection question confirming this session's WP1/WP2 plan.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

WP1: Documentation Debt Discipline fix - correct COC-0001's stale RBL-0028 references (Session Start Checklist, Related Artefacts, OSE Relationships) to RBL-0029, found at this session's own WP0A.

WP2 onward: scope [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Track B Phase 3 (Action faculty implementation) against [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A's Local Agent Permission Boundary and the Agent Framework Architecture delivered at [[ESR-0048_ENGINEERING_SESSION_REPORT|ESR-0048]] WP2.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP1 | Documentation Debt Discipline fix: COC-0001 stale RBL-0028 references | Complete |
| WP2 | Scope and implement Track B Phase 3 (Action faculty implementation) | Complete |

Further Work Packages will be added if the Programme Sponsor directs the session remain open beyond WP2.

---

# 6A. WP1 - COC-0001 Documentation Debt Discipline Fix

Approved directly by the Programme Sponsor via the two-part objective-selection question at session open.

Corrected COC-0001's stale RBL-0028 current-baseline references to RBL-0029 (accepted at ESR-0047 WP7, retained at ESR-0048 WP7) in three places: Session Start Checklist, Related Artefacts, OSE Relationships. This is the same fix pattern PBK-0001 received at ESR-0048 WP1, which did not include COC-0001 despite it carrying the identical reference.

Whole-Document Staleness Sweep on Edit performed across the rest of COC-0001: no further stale claims found - role bindings (Engineering Implementer/Claude, Engineering Reviewer/ChatGPT), EE-0001 terminology and GDE-0001 cross-references all remain current.

Validation: `python scripts/validate_repository.py` (full mode) - pending, see below.

Files: `aiems/governance/conversation/COC-0001_HUMAN_AI_COLLABORATION_CONTEXT.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, `aiems/governance/sessions/ESR-0049_ENGINEERING_SESSION_REPORT.md` (this report).

---

# 6B. WP2 - EBG-0119: Agent Framework Phase 3, First Specialist Agent

Programme Sponsor selected Track B Phase 3 (Action faculty implementation) as WP2's objective, per the two-part objective-selection question at session open - the next item in the roadmap's dependency chain, now that Phase 1 (Guardian Cognitive Core), Phase 2 (Local Agent Permission Boundary) and the Agent Framework's contract architecture ([[EIP-ESR0048-001_AGENT_FRAMEWORK_ARCHITECTURE_SCOPE|EIP-ESR0048-001]], ESR-0048) are all delivered.

Registered [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0119 (Agent Framework Phase 3: First Specialist Agent Implementation, Approved Backlog, High).

Investigated the existing architecture and code before drafting scope: [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]]'s Agent Framework subsection (the contract to implement), `jarvis/gia/observability.py` (`LocalResourceObserver.snapshot()`, the read-only capability to wire as the first agent), `sentinel/policy.py`'s `TrustTierPolicy.classify()` (confirming a non-`local_agent`/`device_control` request classifies `ROUTINE_INTERACTION`), the existing `SentinelGatedConversationProvider` and `SpeechOutcome`/`TranscriptionOutcome` patterns (the concrete templates this package's service/outcome types mirror), `build_default_runtime()`'s shared-gateway construction, `GuardianRuntime`'s optional-capability pattern, and `jarvis/platform/shell.py`'s stale `PLACEHOLDER` Agent Framework status entry.

Produced [[EIP-ESR0049-001_AGENT_FRAMEWORK_PHASE3_FIRST_SPECIALIST_AGENT|EIP-ESR0049-001]] (v0.1, Draft) - real code this time, not architecture-only: a new `jarvis/agents/` module (`SpecialistAgent`/`AgentRequest`/`AgentResult`, `GiaObservabilityAgent`), a `SentinelGatedAgentService` (`jarvis/interfaces/sentinel_agent.py`) evaluated through the same shared Sentinel gateway every other capability uses, `GuardianRuntime`/`build_default_runtime()` wiring, two new `guardian.agent.*` RPC methods, and an honest `platform.status` capability-state correction. `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` hard `DENY` is untouched throughout - the wired agent is read-only and classifies `ROUTINE_INTERACTION` only.

Submitted for Codex design review via direct `codex exec -s read-only` invocation - **v0.1: Pass with non-blocking findings.** Codex independently verified every Repository Context claim against the live code and confirmed the scope "soundly bounded... does not authorise or approach LOCAL_AGENT_ACTION." Two non-blocking findings folded into v0.2: `AgentOutcome`'s success status now echoes the agent's own reported status rather than hardcoding `"reported"` as a universal contract value; the `platform.status` capability-state summary narrowed to explicitly state one read-only agent only.

**Approval-to-implement requested and granted via the AIEMS Exchange Bridge, verified against the real Sponsor Approval Service** (`submit-response`, ESR-0049/WP2) before any code was written - the first chat-only "approved" was correctly refused by the gate (no recorded decision yet); the second succeeded once a real decision existed.

**Implemented exactly as scoped.** New `jarvis/agents/` module (`contracts.py`: `AgentRequest`/`AgentResult`/`SpecialistAgent`; `gia_agent.py`: `GiaObservabilityAgent`, wrapping `jarvis/gia/observability.py`'s existing read-only `LocalResourceObserver.snapshot()`). New `jarvis/interfaces/sentinel_agent.py` (`AgentOutcome`, `SentinelGatedAgentService`) mirroring `SentinelGatedConversationProvider`'s gateway-evaluate-then-proceed flow and `SpeechOutcome`/`TranscriptionOutcome`'s named-status envelope pattern exactly. `GuardianRuntime` gains an `agent_service` constructor parameter and `invoke_agent()`/`available_agents()` methods, mirroring `speak()`/`transcribe()`'s boundary-response discipline. `build_default_runtime()` (`jarvis/interfaces/stdio_rpc.py`) constructs `SentinelGatedAgentService` reusing the same shared `gateway` every other capability already uses, registering `gia-observability` unconditionally (no external credential dependency, unlike Piper/Whisper). Two new JSON-RPC methods, `guardian.agent.list` and `guardian.agent.invoke`. `jarvis/platform/shell.py`'s "Agent Framework" capability entry corrected `PLACEHOLDER` to `AVAILABLE`, narrowly worded per Codex's finding. GAM-0001 Section 8A's `LOCAL_AGENT_ACTION` hard `DENY` untouched throughout; `sentinel/policy.py` not modified.

27 new tests added: `jarvis/tests/test_agents.py` (contract validation, `GiaObservabilityAgent`), `jarvis/tests/test_sentinel_agent.py` (`SentinelGatedAgentService` - unknown-agent short-circuit, `ALLOW` path against the real `TrustTierPolicy` confirming genuine `ROUTINE_INTERACTION` classification, Sentinel-denial path hiding internal reason), new cases added to `jarvis/tests/test_guardian_runtime.py` (`invoke_agent()` boundary behaviour) and `jarvis/tests/test_stdio_rpc.py` (RPC-level shape, including the shared-gateway regression the existing speech/transcription tests already have). `jarvis/tests/test_guardian_shell.py` updated for the real `AVAILABLE` state.

Validation: `python -m pytest jarvis/tests sentinel scripts/tests` - 512 passed, 1 skipped (was 485 passed, 1 skipped before this package). `python scripts/validate_repository.py` (full mode) - 0 errors.

Files: `jarvis/agents/__init__.py` (new), `jarvis/agents/contracts.py` (new), `jarvis/agents/gia_agent.py` (new), `jarvis/interfaces/sentinel_agent.py` (new), `jarvis/guardian/runtime.py`, `jarvis/interfaces/stdio_rpc.py`, `jarvis/platform/shell.py`, `jarvis/tests/test_agents.py` (new), `jarvis/tests/test_sentinel_agent.py` (new), `jarvis/tests/test_guardian_runtime.py`, `jarvis/tests/test_stdio_rpc.py`, `jarvis/tests/test_guardian_shell.py`, `aiems/models/MOD-0001_PLATFORM_ARCHITECTURE_MODEL.md`, `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, [[EIP-ESR0049-001_AGENT_FRAMEWORK_PHASE3_FIRST_SPECIALIST_AGENT|EIP-ESR0049-001]].

---

# 6C. Session-Wide WP6 - Independent Repository Verification

Following WP2's implementation and push, the Programme Sponsor selected moving to session-wide Independent Repository Verification.

Ran a genuine independent Codex review (`codex exec -s read-only`, background invocation, real inspection of `git diff 7928626..e9d2929` - both `--stat`/`--name-status` and full content) covering both WP1 and WP2's committed changes against the current baseline [[RBL-0029_REPOSITORY_BASELINE|RBL-0029]] (commit `7928626`, established at ESR-0047 WP7, retained at ESR-0048 WP7). Verified independently: (1) `--name-status` shows exactly the expected 18 files changed across both Work Packages, no unexpected path; (2) [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 8A and `sentinel/policy.py` are byte-identical/untouched across the whole session; (3) 27 new `def test_` cases confirmed by direct diff count across the five test files, matching the 485-to-512 test-count claim; (4) REG-0001's version rows match every touched artefact's own current file version exactly; (5) every governance claim (EIP-ESR0049-001 "Implemented as scoped", EBR-0001 EBG-0119 Completed, MOD-0001 version history) matches the actual code diff.

**Verdict: Pass, no findings.**

Codex's own baseline assessment (advisory, not a determination): this is a genuine live product-capability change - WP2 adds a new backend specialist-agent capability exposed through runtime and JSON-RPC - not documentation-only, and recommends WP7 Establish a new baseline. The Programme Sponsor makes the actual WP7 determination.

---

# 6D. Session-Wide WP7 - Repository Baseline Determination

**Programme Sponsor determination: Establish [[RBL-0030_REPOSITORY_BASELINE|RBL-0030]]**, superseding [[RBL-0029_REPOSITORY_BASELINE|RBL-0029]]. WP2 delivered a genuine, live product-capability change - Guardian's Agent Framework moved from architecture-only (MOD-0001's subsection, ESR-0048) to a real, Sentinel-gated, JSON-RPC-reachable specialist-agent capability (GIA's read-only observability, classified `ROUTINE_INTERACTION`) - matching the Establish threshold applied at RBL-0025/RBL-0027/RBL-0028/RBL-0029 rather than the Retain threshold applied at architecture/documentation-only sessions such as ESR-0048. WP1's documentation fix alone would not have crossed this threshold; WP2's real code does.

[[RBL-0030_REPOSITORY_BASELINE|RBL-0030]] created (HEAD at baseline creation: `e9d2929`), registered in REG-0001. Every controlled artefact citing the "current accepted repository baseline" propagated from RBL-0029 to RBL-0030: [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] (1.18 to 1.19), [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (1.36 to 1.37), [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] (1.7 to 1.8), [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] (2.4 to 2.5, pointer only), [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] (2.3 to 2.4, pointer only), README.md (3.28 to 3.29) and [[PST-0001_PROGRAMME_STATUS|PST-0001]] (3.27 to 3.28). README and PST-0001 also corrected their stale "no session currently open" framing (both had remained keyed to ESR-0048's closure throughout ESR-0049's WP1/WP2, per the Whole-Document Staleness Sweep on Edit discipline triggered by opening these documents for the baseline-pointer fix). PCB-0001's and the Capability Matrix's own capability-content refresh for the new Agent Framework capability is disclosed as not yet done, deferred to a future Documentation Debt sync.

Files: `aiems/governance/baselines/RBL-0030_REPOSITORY_BASELINE.md` (new), `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`, `aiems/governance/conversation/COC-0001_HUMAN_AI_COLLABORATION_CONTEXT.md`, `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md`, `aiems/models/MOD-0001_PLATFORM_ARCHITECTURE_MODEL.md`, `aiems/governance/baselines/PCB-0001_PRODUCT_CAPABILITY_BASELINE.md`, `jarvis/architecture/JARVIS_CAPABILITY_READINESS_MATRIX.md`, `README.md`, `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`.

---

# 7. Related Artefacts

* [[ESR-0048_ENGINEERING_SESSION_REPORT|ESR-0048]] - prior closed session, immediate predecessor.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - Session Initialisation, Engineering Session Lifecycle and Documentation Debt Discipline guidance followed; source of the WP1 priority rule.
* [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] - WP1 target artefact.
* [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] - Track B Phase 3, WP2 objective source.
* [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] - Section 8A, the permission boundary WP2's scoping must obey.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0119, WP2's registered backlog item.
* [[EIP-ESR0049-001_AGENT_FRAMEWORK_PHASE3_FIRST_SPECIALIST_AGENT|EIP-ESR0049-001]] - approved, implemented Engineering Implementation Package for WP2.
* [[RBL-0030_REPOSITORY_BASELINE|RBL-0030]] - repository baseline established at this session's WP7, superseding RBL-0029.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.6 | 5 August 2026 | Claude Engineering Implementer | Session-wide WP7 (Repository Baseline Determination): **Establish [[RBL-0030_REPOSITORY_BASELINE|RBL-0030]]**, superseding RBL-0029 - WP2's Agent Framework Phase 3 delivery is a genuine live product-capability change. Every controlled artefact's "current accepted repository baseline" reference propagated to RBL-0030 (COC-0001, PBK-0001, MOD-0001, PCB-0001, JARVIS Capability Readiness Matrix, README, PST-0001); README/PST-0001's stale "no session currently open" framing also corrected. |
| 1.5 | 5 August 2026 | Claude Engineering Implementer | Session-wide WP6 (Independent Repository Verification): genuine background Codex review of the full `7928626..e9d2929` diff (WP1 + WP2) - **Pass, no findings**. Codex's own advisory baseline assessment: genuine live product-capability change, recommends WP7 Establish. WP7 determination pending. |
| 1.4 | 5 August 2026 | Claude Engineering Implementer | WP2 Complete: EBG-0119 (Agent Framework Phase 3: First Specialist Agent Implementation) resolved per EIP-ESR0049-001 (Codex design review Pass with findings folded in; Programme Sponsor approval verified via the real Sponsor Approval Service). New `jarvis/agents/` module, `SentinelGatedAgentService`, GuardianRuntime/stdio_rpc wiring, two new `guardian.agent.*` RPC methods, honest `platform.status` correction. GIA wired as first live `ROUTINE_INTERACTION` specialist agent - `LOCAL_AGENT_ACTION` untouched. 27 new tests (512 passed/1 skipped, up from 485/1). `validate_repository.py` 0 errors. |
| 1.3 | 5 August 2026 | Claude Engineering Implementer | WP2 reviewed: EIP-ESR0049-001 v0.1 Codex design review Pass with non-blocking findings, folded into v0.2. Awaiting Programme Sponsor approval before implementation. |
| 1.2 | 5 August 2026 | Claude Engineering Implementer | WP2 in progress: registered EBG-0119, produced draft EIP-ESR0049-001 (v0.1, Agent Framework Phase 3 - real `SpecialistAgent` implementation, GIA-BOOT wired as the first `ROUTINE_INTERACTION` agent). Submitted for Codex design review. Not yet approved or implemented. |
| 1.1 | 5 August 2026 | Claude Engineering Implementer | WP1 Complete: corrected COC-0001's stale RBL-0028 references (Session Start Checklist, Related Artefacts, OSE Relationships) to RBL-0029. Whole-Document Staleness Sweep found no further staleness. |
| 1.0 | 5 August 2026 | Claude Engineering Implementer | ESR-0049 opened at WP0B, before WP1 began. WP0A found COC-0001 one baseline stale (RBL-0028, should be RBL-0029) in three places. Objective: WP1 corrects COC-0001; WP2 onward scopes JRM-0001 Track B Phase 3 (Action faculty implementation). Selected by the Programme Sponsor via explicit two-part objective-selection question. |
