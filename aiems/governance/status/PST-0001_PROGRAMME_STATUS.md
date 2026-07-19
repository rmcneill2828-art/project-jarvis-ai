# PST-0001 - Programme Status

> *"A programme moves faster when its current state is clear, trusted and easy to reload."*

**Version:** 2.62

---

# Document Control

| Field | Value |
|-------|-------|
| Artefact ID | PST-0001 |
| Title | Programme Status |
| Version | 2.58 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Review Frequency | At phase closure or engineering session transition |
| Effective Date | 9 July 2026 |
| Next Review | At next approved engineering session or next baseline review |

---

# 1. Purpose

This artefact records the current programme status for Project JARVIS AI.

It exists to provide a concise engineering context snapshot at the start of future engineering sessions.

PST-0001 supports faster session start-up by preserving the current programme state without requiring long conversation history to be reloaded.

Repository evidence remains authoritative over conversational memory.

---

# 2. Scope

This artefact records:

- current programme phase;
- current engineering workflow;
- current capability roadmap;
- completed engineering milestones;
- active and next planned engineering work;
- current repository and product baselines;
- outstanding observations;
- session start guidance.

This artefact does not record detailed engineering decisions. Detailed decisions remain in controlled artefacts, accepted baselines, registers, standards, reviews and session reports.

---

# 3. Current Programme State

| Item | Current State |
|------|---------------|
| Project | Project JARVIS AI |
| Engineering System | AI Engineering Management System (AIEMS) |
| Repository | project-jarvis-ai |
| Primary Branch | main |
| Current Mode | [[ESR-0029_ENGINEERING_SESSION_REPORT|ESR-0029]] is the latest **closed** session (19 July 2026). No further session has yet been opened. ESR-0029 was the fourth session run entirely through the AIEMS Exchange Bridge (`scripts/aiems_bridge.py`) with no manual relay anywhere, across seven Work Packages: WP1 (EBG-0082 cross-module resource-interaction research, following the Programme Sponsor's own research-first redirection), WP2 (Guardian Orb Canvas 2D rendering migration, ADR-0021 implemented, including a genuine live-verified performance-regression fix), WP3/WP4/WP6/WP7 (GIA Phase 1a-1d local resource observability, closing EBG-0083 Phase 1 in full), and WP5 (ADR-0022, Sponsor Approval Service decision - decision only, no implementation). Session-wide WP8 (Pass, no findings) and WP9 (Accept - new baseline [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] established, superseding RBL-0016, after two post-commit fix rounds) both closed via the bridge. 295 tests total (up from 286). Full detail in [[ESR-0029_ENGINEERING_SESSION_REPORT|ESR-0029]]. |
| Current Repository Baseline | [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]], accepted at ESR-0029 WP9, superseding RBL-0016 - the Guardian Orb's Canvas 2D rendering-engine migration and GIA's first real observability capability (Phase 1 complete) judged at least comparable in substance to RBL-0016's own trigger, both independent WP8 views converging with the Programme Sponsor's determination. |
| Current Product Capability Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] v2.1, refreshed and accepted at ESR-0020 WP4 - not yet refreshed to reflect ESR-0027 WP1's Personal Memory implementation; still shows Memory as not implemented pending a future refresh pass. [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] was refreshed to v2.2 at ESR-0028 WP2/WP4 (registered in REG-0001 for the first time, Memory and Provider Architecture rows corrected). |
| Repository Product Capability Assessment | [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] completed and accepted. |
| Current Phase | No engineering session currently open; ESR-0029 closed 19 July 2026, under the permanent [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7 appointment (Claude Engineering Implementer, ChatGPT/Codex Engineering Reviewer, Programme Sponsor gating). |
| Current Workflow | AIEMS Engineering Workflow v3 with Engineering Ecosystem Synchronisation working practice. ESR-0029 continued the standing draft/review/approval/implementation/commit/post-commit-review template entirely through `scripts/aiems_bridge.py` across seven Work Packages plus session-wide WP8/WP9 - now confirmed repeatable across a fourth consecutive session (ESR-0026, ESR-0027, ESR-0028, ESR-0029). |
| Current Engineering Objective | ESR-0029 closed (EBG-0082, EBG-0083 Phase 1, ADR-0021 implementation and ADR-0022 decision all Complete/Approved; RBL-0017 accepted). No new session is opened by this status update - the next Engineering Session's objective is for the Programme Sponsor to select. |

---

# 4. Current Engineering Workflow

The current approved workflow remains AIEMS Engineering Workflow v3 with clarified authority, validation, verification and acceptance lifecycle.

Workflow sequence:

1. Engineering Planning
2. Programme Sponsor Approval
3. Implementation
4. Programme Sponsor Validation
5. Commit and Push
6. Independent Repository Verification
7. Programme Sponsor Baseline Acceptance
8. Phase Closure

ESR-0007 and ESR-0008 added the following accepted working practices pending future standards review:

| Working Practice | Status | Notes |
|------------------|--------|-------|
| Repository-First Engineering Protocol (RFEP) | Accepted ESR-0007 working practice | Repository evidence is the primary engineering memory. |
| Repository-First Decision Protocol (RFDP) | Accepted ESR-0007 working practice | Engineering decisions are grounded in controlled artefacts and executable evidence. |
| Continuous Repository Synchronisation | Accepted ESR-0007 working practice | Session, status, register and baseline artefacts are synchronised at closure. |
| Engineering Ecosystem Synchronisation | Accepted ESR-0008 working practice | GitHub, AIEMS, OSE, Obsidian, controlled artefacts, registers, previous ESRs and summaries are considered during synchronisation. |

These practices are not formal AIEMS standards unless separately reviewed and standardised through future approved work.

---

# 4A. Current Engineering Focus

[[ESR-0029_ENGINEERING_SESSION_REPORT|ESR-0029]] is **Closed** (19 July 2026), run under the permanent Lead/Reviewer appointment: Claude as Engineering Implementer, Codex (ChatGPT) as Engineering Reviewer, Programme Sponsor gating every step. **The fourth session run entirely through the AIEMS Exchange Bridge with no manual relay anywhere.**

**WP1** closed **EBG-0082** (cross-module resource-interaction research) - real external research (VS Code Extension Host, Electron/Tauri process models, Home Assistant, Mycroft) mapped against JARVIS's own architecture, following the Programme Sponsor's own redirection away from the offered WP0B options toward checking for a missing pattern rather than picking a feature.

**WP2** delivered **Guardian Orb Canvas 2D rendering migration** per [[EIP-ESR0029-001_GUARDIAN_ORB_CANVAS_MIGRATION|EIP-ESR0029-001]] v1.2 - implementing [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]]'s decision from ESR-0028. A genuine performance regression was found during live verification (initial Canvas measured worse than the SVG baseline it was meant to improve on) and fixed by proving edges are mathematically guaranteed within the circular clip boundary and scoping the clip to only the node-drawing pass - final result confirmed below the SVG baseline via both CDP measurement and the Programme Sponsor's own Windows Task Manager check.

**WP3/WP4/WP6/WP7** delivered **GIA (Guardian Instrumentation Agent) Phase 1** in four small, separately-approved slices - CPU/memory (WP3), storage (WP4), process health/self-observation (WP6), and local engineering-environment tool presence (WP7) - closing **EBG-0083 Phase 1 in full**. First real GIA observability capability: a new `jarvis/gia/observability.py` module, the project's first-ever declared runtime dependency (`psutil`), and a new `gia.status` JSON-RPC method, live-verified against real host data throughout.

**WP5** approved **[[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]]** (decision only, no implementation) - replacing the AIEMS Exchange Bridge's file-based `sponsor-decision` with a remote agent-read/sponsor-write approval service behind Tailscale, following a detailed proposal the Programme Sponsor pasted directly into conversation. Also surfaced and recorded a binding operational-practice requirement: `submit-response` had never actually been used as the real commit gate this session, a genuine gap found during the Engineering Implementer's own review.

Session-wide **WP8** (Independent Repository Verification): **Pass**, no findings. Session-wide **WP9** (Repository Baseline Acceptance): **Accept**, new baseline [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] established, superseding RBL-0016 - both independent views converging that the Guardian Orb rendering-engine migration and GIA's new observability capability are at least comparable in substance to RBL-0016's own trigger. Two rounds of post-commit fixes were needed on PST-0001's own bookkeeping before Codex's final Pass.

295 tests pass (up from 286 - 9 net-new GIA tests) and `validate_repository.py` (full mode) passes clean throughout (129 warnings baseline, +3 disclosed cross-document false positives from this session's own new EIP/EBR prose). Full detail in [[ESR-0029_ENGINEERING_SESSION_REPORT|ESR-0029]].

**Deferred, not resolved this session**: README.md, PBK-0001, and JRM-0001 all still carry stale ESR-0028/RBL-0016-era (or earlier) references, explicitly deferred by the Programme Sponsor at WP0A - worth prioritising early in a future session.

---

## Prior Session: ESR-0027

[[ESR-0027_ENGINEERING_SESSION_REPORT|ESR-0027]] is **Closed** (18 July 2026). **The second session run entirely through the AIEMS Exchange Bridge with no manual relay anywhere.** WP1 implemented **EBG-0080** (Personal Memory Implementation) per [[EIP-ESR0027-001_PERSONAL_MEMORY_IMPLEMENTATION|EIP-ESR0027-001]] v1.1 - a working minimal consent gate for Personal Memory, the first Sentinel `REVIEW` decision anywhere in this codebase actually resolved by a human, surfacing and fixing four genuine issues across two review rounds. WP2 implemented **EBG-0077** (UXP DiagnosticsPanel Reconciliation) per [[EIP-ESR0027-002_UXP_DIAGNOSTICS_PANEL_RECONCILIATION|EIP-ESR0027-002]] v1.0, clean on both review passes. Session-wide WP6 Pass (two Low findings fixed), WP7 Accept ([[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained). 286 tests pass (was 254). Full detail in [[ESR-0027_ENGINEERING_SESSION_REPORT|ESR-0027]].

---

## Prior Session: ESR-0026

[[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]] is **Closed** (17 July 2026). **The first session run entirely through the AIEMS Exchange Bridge with no manual relay anywhere**, following ESR-0025A's preflight fix. WP1 implemented **EBG-0075** (Ollama Local Fallback Provider) per [[EIP-ESR0025-002_OLLAMA_LOCAL_FALLBACK_PROVIDER|EIP-ESR0025-002]] v1.1, surfacing and fixing two real defects (a test-isolation bug, an `AttributeError` on non-object JSON) plus a Programme Sponsor-authorised tooling deviation (EBG-0079). WP2 approved **[[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]]** v1.0 (EBG-0019), WP3 approved **[[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]]** v1.0 (EBG-0076), both scoped as specifications following a WP0 scope check. Session-wide WP6 Pass, WP7 Accept ([[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained). 254 tests pass (was 238). Full detail in [[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]].

---

PST-0001 records ESR-0028 as the currently open session (WP6 in progress) and ESR-0027 as the latest closed session. It does not itself approve implementation outside separately authorised engineering work. Full historical detail remains in each session's own report and [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]]'s version history.

---

# 5. Current Capability Roadmap

| Capability | Status | Maturity | Notes |
|------------|--------|----------|-------|
| Repository Architecture | Complete | Complete | Repository structure, package layout and governance separation are established. |
| Governance Framework | In Progress | High | Core AIEMS governance artefacts support controlled product delivery and are ready to be tested through implementation-led engineering. |
| Engineering Standards | In Progress | High | Approved standards remain in place; RFEP, RFDP and Continuous Repository Synchronisation are working practices pending any future standards review. |
| JARVIS Product Architecture | Complete | High | [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] remains the product architecture authority. |
| JARVIS Platform Architecture | Draft | High | [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] validated JARVIS Platform, Sentinel, Platform Services, UXP, Provider Architecture, Agent Framework and GIA positioning for implementation readiness. |
| Sentinel AI Execution and Security Platform | Implemented | High | [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] positions Sentinel as the AI Execution and Security Platform; Sentinel Core, provider abstraction, local/OpenAI/Gemini providers, health-aware provider orchestration with failover, audit, policy and a trust-tier policy model are implemented under `sentinel/`, now reachable through the live UXP via `GuardianRuntime` (204 passing tests repository-wide). **Gemini live-validated at ESR-0020 WP3** (EBG-0051 Complete) - real API call, real generated response, Policy decision Allow. **A real provider is now wired into the default runtime conversation path** (EBG-0070, Complete, ESR-0022 WP1 per EIP-ESR0022-001 v1.0): `build_default_runtime()` registers OpenAI or Gemini (configurable, credential-gated, blank-value safe) as primary, `LocalEchoProvider` retained as failover. |
| Guardian Cognitive Architecture | Draft | High | [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] records Guardian identity and cognitive architecture; ESR-0013 established a bounded runtime foundation without implementing full Guardian cognition. |
| Guardian Experience Architecture | Approved Baseline, Phase 1 Implemented | High | [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] records Guardian Experience Architecture v1.0; [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] confirmed Guardian Orb should consume real observable state - **ESR-0019 delivered Section 8.1's Phase 1**: the Guardian Orb now renders the live repository knowledge graph. Phases 2-4 (cluster illumination, agent-traversal animation, Guardian reasoning connection) remain not started. |
| Engineering Ecosystem Architecture | Implementation Validated | High | [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] records Obsidian/OSE and Engineering Ecosystem Synchronisation; ESR-0012 validated AIEMS operationally through implementation. |
| Guardian Instrumentation Agent | Proof of Concept Complete | Early | [[ESR-0012_ENGINEERING_SESSION_REPORT|ESR-0012]] completed GIA-BOOT as a Proof of Concept; further GIA implementation is deferred. |
| User Experience Platform | Live, Foundation Scope | Foundation | [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]] records Tauri + React as the UXP direction; [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] decided the backend bridge pattern; ESR-0017 WP9 implemented and verified it live - the UXP is no longer a disconnected static shell. The chat input is enabled and calls the real backend; capability/diagnostics panels derive from live `platform.status` data. **ESR-0019 delivered the Guardian Orb knowledge-graph vision's Phase 1** ([[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] 8.1) - the Orb now renders the live `knowledge.graph` data as a sphere, replacing the placeholder glow/ring/label animation. **ESR-0022 WP1 added the System Health panel** (EBG-0072, Complete, per EIP-ESR0022-001 v1.0) - Guardian/Sentinel/Providers, real `platform.status` fields only. Streaming notifications, production sidecar packaging, true 3D/rotation and Phases 2-4 of the knowledge-graph vision remain not yet implemented (EBG-0050 remaining scope, EBG-0055 continuation). |
| JARVIS Product Capability Baseline | Accepted, Current | Foundation | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] v2.1 - refreshed and accepted at ESR-0020 WP4, closing EBG-0056. No longer stale. |
| JARVIS Capability Maturity | Maintained, Current | Foundation | [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] refreshed to v2.0 at ESR-0021 WP7 (closing EBG-0069) - no longer stale. Guardian, Sentinel, Platform Services, UXP, Knowledge and Provider Architecture now correctly shown as Implemented (Foundation); Memory, Voice, Vision, Home Automation, Productivity, Multi-device and a JARVIS-internal Engineering Agent remain correctly Not Started. |
| JARVIS Development | In Progress | Early | Guardian Desktop Platform Shell, Guardian Experience v1.0, GIA-BOOT Proof of Concept, Guardian Runtime Foundation, Guardian&harr;Sentinel connection (ESR-0017 WP2), the UXP-backend bridge (ESR-0017 WP9) and the Guardian Orb knowledge-graph rendering (ESR-0019 WP2, EBG-0055 Phase 1) exist. **Guardian is now reachable through the running UXP, and its own visual presence reflects live repository state** - both verified via real running sessions - though this remains outside PCB-0001's still-unrefreshed accepted operational baseline (EBG-0056). |
| Runtime Chat Archive | Complete | Foundation | Prototype chat exports are archived under `logs/chats/`; EBG-0039 is completed in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]. |

---

# 6. Completed Programme Milestones

| Milestone | Status |
|-----------|--------|
| Repository Architecture established | Complete |
| Repository Integrity Review completed | Complete |
| AIEMS Engineering Workflow v3 established | Complete |
| Engineering standards baseline established | Complete |
| JARVIS product architecture established | Complete |
| JARVIS First Light executable skeleton established | Complete |
| JARVIS Conversation Workspace operationally validated | Complete |
| Repository baseline accepted through [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Complete |
| [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] Repository Product Capability Assessment completed | Complete |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] Product Capability Baseline accepted | Complete |
| Repository-First Engineering Protocol adopted as ESR-0007 working practice | Complete |
| Repository-First Decision Protocol adopted as ESR-0007 working practice | Complete |
| Continuous Repository Synchronisation adopted as ESR-0007 working practice | Complete |
| [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] accepted as ESR-0007 repository baseline | Complete |
| ESR-0007 closed | Complete |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] Product Vision Traceability Model created | Complete |
| [[ERR-0001_ENGINEERING_RECOVERY_REPORT|ERR-0001]] Engineering Recovery Report created | Complete |
| [[EIR-0001_ENGINEERING_IMPLEMENTATION_RECOMMENDATION|EIR-0001]] Engineering Implementation Recommendation created | Complete |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] Guardian Identity and Cognitive Architecture created | Complete |
| ADR-0007 through ADR-0013 created for ESR-0008 architecture decisions | Complete |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] closure report created | Complete |
| [[TPL-0001_ENGINEERING_EXECUTION_PACKAGE_TEMPLATE|TPL-0001]] Engineering Execution Package Template created | Complete |
| Guardian Desktop Platform Shell established | Complete |
| Tauri + React adopted as UXP implementation baseline | Complete |
| [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] Sentinel Trust Architecture established | Complete |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Guardian Experience Architecture v1.0 established | Complete |
| Guardian Experience v1.0 implemented | Complete |
| [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]] Engineering Session Report created | Complete |
| ESR-0009 closed | Complete |
| [[RBR-ESR0009-001_REPOSITORY_BASELINE_REVIEW|RBR-ESR0009-001]] Repository Baseline Review completed | Complete |
| [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] accepted as ESR-0009 repository baseline | Complete |
| ESR-0010 Engineering Ecosystem Modernisation completed | Complete |
| ChatGPT Desktop adopted as preferred Engineering Reasoning Environment | Complete |
| GitHub Desktop adopted as preferred Local Repository Management / Programme Sponsor Review Tool | Complete |
| Guardian UXP Orb design direction approved | Complete |
| ESR-0010 Repository Baseline Review accepted | Complete |
| [[ESR-0010_ENGINEERING_SESSION_REPORT|ESR-0010]] Engineering Session Report created | Complete |
| ESR-0011 Architecture Validation and Implementation Readiness completed | Complete |
| GIA local observability direction approved | Complete |
| ESR-0012 implementation phase handover approved | Complete |
| [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] Engineering Session Report created | Complete |
| ESR-0012 Implementation Phase Initiation completed | Complete |
| AIEMS implementation workflow validated through ESR-0012 | Complete |
| Codex implementation workflow validated through ESR-0012 | Complete |
| Independent engineering review workflow validated through ESR-0012 | Complete |
| GIA-BOOT Proof of Concept completed | Complete |
| AIEMS Engineering Agent created and live validated | Complete |
| ChatGPT and Guardian operating environments separated | Complete |
| [[ESR-0012_ENGINEERING_SESSION_REPORT|ESR-0012]] Engineering Session Report created | Complete |
| ESR-0013 Guardian Runtime Foundation established | Complete |
| ESR-0013 Guardian Runtime integrated into JARVIS lifecycle | Complete |
| ESR-0013 Guardian runtime status and observability established | Complete |
| [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] closure review package prepared | Complete |
| Sentinel Core, provider abstraction, local provider, provider configuration and provider orchestration implemented | Complete |
| [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] Sentinel AI Execution and Security Platform approved | Complete |
| [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] Engineering Session Report created | Complete |
| [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] Project Knowledge Map created | Complete |
| [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] Post-Closure Engineering Addendum created | Complete |
| ESR-0015 Sentinel execution pipeline delivered and proven live | Complete |
| [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] accepted as the ESR-0015 repository baseline | Complete |
| EE-0001 Independent AI Peer Review Trial established | Complete |
| [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] Engineering Session Report created | Complete |
| ESR-0016 Sentinel trust-tier policy model (WP1) delivered and independently verified | Complete |
| ESR-0016 architecture alignment (WP2: CURRENT_ARCHITECTURE.md, SAM-0001) delivered and independently verified | Complete |
| EE-0001 findings-count definition clarified (Section 8, dated entry) | Complete |
| [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] Engineering Session Report created and closed | Complete |
| ESR-0017 UXP-backend integration architecture decided ([[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]], WP1) | Complete |
| ESR-0017 Guardian&harr;Sentinel connection delivered (`GuardianRuntime.converse()`, WP2) | Complete |
| ESR-0017 second external Sentinel provider adapter delivered (`GeminiProvider`, WP3) | Complete |
| ESR-0017 five-session backlog progression roadmap produced (WP4), later revised at closure | Complete |
| ESR-0017 Feature-First Delivery Discipline added to PBK-0001 (WP8) | Complete |
| ESR-0017 first genuinely interactive UXP delivered and verified live (WP9) | Complete |
| ESR-0017 Guardian Orb knowledge-graph design direction recovered into [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Complete |
| [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] accepted as the ESR-0017 refreshed repository baseline | Complete |
| [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] Engineering Session Report created and closed | Complete |
| ESR-0018 Gemini provider production-readiness hardening delivered ([[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0051, WP1) | Complete |
| ESR-0017 EE-0001 trial scorecard formally accepted by the Programme Sponsor (ESR-0018 WP2) | Complete |
| EE-0001 Section 5.12 "Review Gate Compliance" criterion adopted (ESR-0018) | Complete |
| EE-0001 Lead/Reviewer trial concluded: permanent appointment made - Claude Lead Engineer, ChatGPT Lead Reviewer | Complete |
| Claude&harr;Codex engineering bridge architecture and cost decision recorded ([[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0057, not implemented) | Complete |
| [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] Engineering Session Report created and closed | Complete |
| ESR-0019 role-binding: PBK-0001/COC-0001 formally bound to the permanent EE-0001 appointment (WP1) | Complete |
| ESR-0019 EBG-0055 Phase 1 delivered: repository knowledge-graph backend and JSON-RPC method (WP2) | Complete |
| ESR-0019 Guardian Orb integration: the Orb's visual presence is now the live knowledge graph (WP2) | Complete |
| [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] accepted as the ESR-0019 repository baseline | Complete |
| ESR-0019 new PBK-0001 practice adopted: Incremental Visual Convergence Toward the Reference Mock-up | Complete |
| [[ESR-0019_ENGINEERING_SESSION_REPORT|ESR-0019]] Engineering Session Report created and closed | Complete |
| ESR-0020 EBG-0004 resolved: PBK-0001/COC-0001 promoted Draft to Approved (open since ESR-0001) | Complete |
| ESR-0020 PBK-0001 corrected: stale RBL-0009 baseline reference, retired Engineering Architect term, Version History ordering | Complete |
| ESR-0020 EBG-0051 (Gemini Provider Production Readiness) closed: live API validation, real generated response | Complete |
| ESR-0020 EBG-0056 (PCB-0001 refresh) closed: v2.1 refreshed and accepted, correcting materially stale capability claims | Complete |
| ESR-0020 Incremental Visual Convergence step: UXP background colour, visually confirmed | Complete |
| ESR-0020 EBG-0026 (transcript export UX) closed | Complete |
| [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] retained at ESR-0020 closure (incremental relative to its establishing session) | Complete |
| [[ESR-0020_ENGINEERING_SESSION_REPORT|ESR-0020]] Engineering Session Report created and closed | Complete |
| ESR-0021 PBK-0001 corrected: Version History sort order ([[EIP-ESR0021-001_PBK-0001_VERSION_HISTORY_SORT_ORDER_CORRECTION|EIP-ESR0021-001]]) and historical-archive breadcrumb ([[EIP-ESR0021-002_PBK-0001_HISTORICAL_ARCHIVE_BREADCRUMB_ALIGNMENT|EIP-ESR0021-002]]) | Complete |
| ESR-0021 Knowledge Metrics and Active Clusters panels added to the live UXP | Complete |
| ESR-0021 [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Project Roadmap created and Programme Sponsor-approved, closing EBG-0012/0027/0028 (open since ESR-0002/ESR-0005) | Complete |
| ESR-0021 PBK-0001 cross-referenced to JRM-0001 ([[EIP-ESR0021-003_PBK-0001_JRM-0001_CROSS_REFERENCE_ADDITION|EIP-ESR0021-003]]) | Complete |
| ESR-0021 full historical HST/FCH audit completed; 11 Tier 1 backlog items added (EBG-0059-0069) | Complete |
| ESR-0021 [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] refreshed to v2.0, closing EBG-0069 - first backlog item selected via JRM-0001 horizon guidance | Complete |
| [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] retained at ESR-0021 closure (incremental relative to its establishing session) | Complete |
| [[ESR-0021_ENGINEERING_SESSION_REPORT|ESR-0021]] Engineering Session Report created and closed | Complete |
| ESR-0022 WP1 delivered: production provider wiring (EBG-0070) and System Health panel (EBG-0072) per EIP-ESR0022-001 v1.0 | Complete |
| ESR-0022 WP6 Independent Repository Verification: Pass | Complete |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] accepted at ESR-0022 WP7, superseding RBL-0014 (production provider wiring judged a materially new operational capability, not an incremental UI refresh) | Complete |
| [[ESR-0022_ENGINEERING_SESSION_REPORT|ESR-0022]] Engineering Session Report created and closed | Complete |
| ESR-0023 WP1 closed EBG-0018 (Provider Abstraction Architecture) and EBG-0067 (Dropped ADR-0007 Topics, split disposition) | Complete |
| ESR-0023 WP2-WP4 created and twice-extended [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] (Guardian Authority and Boundary Model, v1.0-v1.2), closing the entire Guardian authority/boundary cluster: EBG-0031, EBG-0020, EBG-0048 | Complete |
| ESR-0023 WP2 promoted MOD-0001 (Platform Architecture Model) from In Review to Approved | Complete |
| ESR-0023 WP5 validated and promoted AAM-0001 (Guardian Identity and Cognitive Architecture) to Approved, closing EBG-0041; surfaced new backlog item EBG-0074 (TrustTierPolicy not wired as production default) | Complete |
| ESR-0023 WP6 removed UXP Guardian/Sentinel/Providers duplication, closing EBG-0073 - session's Feature-First Delivery Discipline product-code change | Complete |
| ESR-0023 repository write-boundary deviation (occurred twice) root-caused and fixed at the tool-configuration level; recorded in EE-0001 Section 7.4 | Complete |
| ESR-0023 WP6 Independent Repository Verification: Pass | Complete |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained at ESR-0023 WP7 (governance/architecture-maturity work, not a runtime capability change) | Complete |
| [[ESR-0023_ENGINEERING_SESSION_REPORT|ESR-0023]] Engineering Session Report created and closed | Complete |
| ESR-0024 WP1 closed EBG-0074 (Wire TrustTierPolicy as SentinelCore's Production Default) per [[EIP-ESR0024-001_TRUSTTIERPOLICY_PRODUCTION_WIRING|EIP-ESR0024-001]] v1.0 | Complete |
| ESR-0024 WP2 delivered PBK-0001's Incremental Visual Convergence practice (System Health Sentinel row names the live policy engine) per [[EIP-ESR0024-002_SYSTEM_HEALTH_POLICY_ENGINE_DETAIL|EIP-ESR0024-002]] v1.0 | Complete |
| ESR-0024 WP6 Independent Repository Verification: Pass | Complete |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained at ESR-0024 WP7 (WP1 stays within the existing runtime path, WP2 presentation-only) | Complete |
| [[ESR-0024_ENGINEERING_SESSION_REPORT|ESR-0024]] Engineering Session Report created and closed | Complete |
| ESR-0025 WP1 resolved the EBG-0060/EBG-0057 overlap and closed EBG-0057 (Claude<->Codex Engineering Bridge MVP) per [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] v1.2 | Complete |
| ESR-0025 registered EBG-0075 (Ollama Local Fallback Provider, Approved Backlog) and drafted [[EIP-ESR0025-002_OLLAMA_LOCAL_FALLBACK_PROVIDER|EIP-ESR0025-002]] v0.1 (Draft, carried forward unimplemented) | Complete |
| ESR-0025 registered EBG-0076 (Sentinel Network Exposure Security Hardening) and EBG-0077 (UXP Static Placeholder Row Reconciliation), both Approved Backlog | Complete |
| ESR-0025 delivered `scripts/start-jarvis.bat` (JARVIS/Guardian desktop launcher), recorded as EBG-0078 (Completed) | Complete |
| ESR-0025 WP6 Independent Repository Verification: Pass (Engineering Reviewer verified via full-diff review after its own local sandbox failed) | Complete |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained at ESR-0025 WP7 (bridge tooling, backlog registration and an unimplemented EIP draft - no product runtime change) | Complete |
| [[ESR-0025_ENGINEERING_SESSION_REPORT|ESR-0025]] Engineering Session Report created and closed | Complete |
| [[ESR-0025A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0025A]] fixed the AIEMS Exchange Bridge's Windows preflight crash (`.CMD` shim/`subprocess.run` issue), a Programme Sponsor-authorised deviation, enabling genuine real bridge usage | Complete |
| ESR-0026 WP1 implemented EBG-0075 (Ollama Local Fallback Provider) per [[EIP-ESR0025-002_OLLAMA_LOCAL_FALLBACK_PROVIDER|EIP-ESR0025-002]] v1.1 - first Work Package to complete the full real Claude<->Codex bridge cycle, including a post-implementation `AttributeError` fix | Complete |
| ESR-0026 registered EBG-0079 (`validate_repository.py` `.aiems-exchange/` scan-exclusion fix), a Programme Sponsor-authorised mid-session deviation | Complete |
| ESR-0026 WP2 approved [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] v1.0, closing EBG-0019 (open since ESR-0004) | Complete |
| ESR-0026 WP3 approved [[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]] v1.0, closing EBG-0076 | Complete |
| ESR-0026 WP6 Independent Repository Verification: Pass (Engineering Reviewer verified via the bridge) | Complete |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained at ESR-0026 WP7 (Ollama provider adapter, two governance specifications, a tooling fix - no product UXP change) | Complete |
| [[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]] Engineering Session Report created and closed | Complete |

---

# 7. Current Engineering Standards Position

Approved standards remain current. ESR-0007 methodology outcomes are working practices only and shall not be treated as standards unless promoted through future approved standards review.

---

# 8. Active and Next Planned Work

| Item | Status | Notes |
|------|--------|-------|
| Current Engineering Session | [[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]] - **Closed** (17 July 2026) | WP1-WP3 complete: EBG-0075 (Ollama provider), EBG-0019 (MDS-0001 spec), EBG-0076 (ADR-0020) - all via the fully real AIEMS Exchange Bridge. Session-wide WP6 Pass, WP7 Accept (RBL-0015 retained). |
| Current Repository Baseline | [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] | Accepted at ESR-0029 WP9 (new baseline, superseding RBL-0016), both independent views (Engineering Reviewer, Engineering Implementer) converging. Session-wide WP8 also Pass. See [[ESR-0029_WP8_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0029 WP8 handover]] v0.2. **The rest of this Section 8 table below still describes ESR-0026 as the "Current Engineering Session" - stale since ESR-0027, ESR-0028 and now ESR-0029 all closed/progressed since; disclosed here rather than silently left, full rewrite deferred to a future catch-up pass given its scope.** |
| Current Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | v2.1 - refreshed and accepted at ESR-0020 WP4, closing EBG-0056. No longer stale. Sibling [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] refreshed to v2.0 at ESR-0021 WP7. Memory's maturity (Not Started for implementation) is unchanged by MDS-0001 - a specification, not code. |
| Current Roadmap | [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | v1.13, Approved - EBG-0019 and EBG-0076 both resolved at spec/decision level at ESR-0026 WP2/WP3. The programme's forward-looking sequencing artefact, cross-referenced from PBK-0001's Backlog Progression Analysis. |
| Current Review State | ESR-0026 session-wide WP6 (Independent Repository Verification) Pass and WP7 (Repository Baseline Acceptance) Accept/Retain RBL-0015 both complete, per Engineering Reviewer (Codex, via the real bridge) and Programme Sponsor determination | Session closed; WP6/WP7 cover the full diff through `9058f5c`. |
| Next Required Activity | Open a new engineering session | No session currently open. A real Memory implementation package building against MDS-0001, or any other ready JRM-0001 candidate, are both open options. Not decided by this status update. |
| Next Work Package Candidate | A real Engineering Implementation Package building `jarvis/memory/` against MDS-0001's architecture is a natural next Track B candidate, now that the specification exists. EBG-0057's own REA future-phase scope (execution-automation agent) remains a further Track A candidate once the MVP core has been proven in more real use. | Not selected by this status update. |
| ESR-0026 Delivered Scope | EBG-0075 (Ollama Local Fallback Provider) implemented per EIP-ESR0025-002 v1.1, including a post-implementation `AttributeError` fix. EBG-0079 (`validate_repository.py` scan-exclusion fix) Completed. EBG-0019 resolved via MDS-0001 v1.0 (specification). EBG-0076 resolved via ADR-0020 v1.0 (decision record). All four via full real Claude<->Codex bridge cycles (pre-commit review, approval, commit, post-commit review, final confirmation). Session-wide WP6 Pass, WP7 Accept (RBL-0015 retained). 254 tests total (was 238). | Complete and reviewed - see [[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]]. |
| GIA-BOOT Proof of Concept | Complete | Accepted as Proof of Concept; further GIA implementation deferred - blocks Knowledge Graph Phases 3-4 (EBG-0055 note). |
| Deferred Work | Recorded | Guardian Memory implementation (architecture now defined by MDS-0001, code not yet started - `jarvis/memory/` remains an empty stub), Conversation Engine expansion, Guardian Developer Console, Guardian Orb knowledge-graph Phases 2-4 ([[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0055 - Phase 1-2 delivered), true 3D rendering and live animation of the Orb (explicitly deferred), a real network-facing Guardian interface (requirements now defined by ADR-0020, none built) remain deferred. **EAC and GDP-0001** tracked as EBG-0059/GDP-0001 per the ESR-0021 WP6 historical audit, superseded in intent by JRM-0001. Both OpenAI and Gemini are live-validated and one is wired into the default production route (EBG-0070, Complete); Ollama is now also wired as a local fallback (EBG-0075, ESR-0026 WP1, Complete); Sentinel's `TrustTierPolicy` classification model is now wired into that same production runtime as of ESR-0024 WP1 (EBG-0074, Complete), so [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]]'s authority model is genuinely in the decision path - though no production call site yet varies request shape per Guardian action, so this is not yet observable as a live behaviour change (Guardian's Action faculty remains Not Started, gated behind EBG-0021). Anthropic/OpenRouter provider adapters approved in principle (PEM-001) but not yet implemented. Claude&harr;Codex engineering bridge (EBG-0057) is now proven in genuine real use across an entire session (ESR-0026); REA (execution-automation agent) remains its own future-phase scope, not yet actioned. |
| Authoritative Backlog Source | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Future engineering priorities remain governed by the backlog register, sequenced via [[JRM-0001_PROJECT_ROADMAP|JRM-0001]]; EBG-0075/EBG-0079/EBG-0019/EBG-0076 marked Complete at ESR-0026. |
| Runtime Evidence Archive | `logs/chats/` | Prototype JARVIS chat exports remain archived under runtime evidence archive. |

---

# 9. Repository Health

| Item | Status |
|------|--------|
| Repository Health | Good |
| Repository Acceptance | Accepted through [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] |
| Current Repository Baseline | [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] |
| Product Capability Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] v2.1 (ESR-0020); sibling [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] v2.0 (ESR-0021 WP7, closing EBG-0069) |
| Latest Repository Product Capability Assessment | [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] |
| Current Activity | ESR-0025 open (17 July 2026); WP1 complete (EBG-0060/EBG-0057 overlap resolved, EBG-0057 MVP implemented and hardened across three post-implementation Engineering Reviewer findings, per EIP-ESR0025-001 v1.2). `python scripts/validate_repository.py` (full mode): 0 errors, 104 pre-existing warnings (+2 from EIP-ESR0025-001's own cross-document Section-reference mentions, the same harmless pattern already present throughout the corpus). `python -m pytest`: 237/237 passing (25 new `scripts/aiems_bridge.py` tests). |

---

# 10. Outstanding Observations

The following observations remain open for future engineering consideration:

- [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] (accepted ESR-0015, retained through ESR-0016) was superseded by [[RBL-0012_REPOSITORY_BASELINE|RBL-0012]] mid-ESR-0017, in turn superseded by [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] at ESR-0017 closure (retained through ESR-0018), in turn superseded by [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] at ESR-0019 closure - all historical now, kept for baseline lineage.
- [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] established the Guardian Platform Foundation through runtime boundary, lifecycle integration, status snapshot and observability work.
- [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] is closed. [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] positions Sentinel as the AI Execution and Security Platform. Sentinel Core, provider abstraction, local provider, provider configuration, provider orchestration, audit, policy and (since ESR-0016) a trust-tier policy model are implemented under `sentinel/` with 144 passing tests.
- [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] is closed. [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] introduces knowledge tiering for Engineering Session initialisation.
- Guardian Runtime **is now connected through Sentinel** (`GuardianRuntime.converse()`, ESR-0017 WP2) and reachable through the live UXP (ESR-0017 WP9) - the candidate focus per ESR-0016 Section 16 is delivered.
- PEM-001 provider scoring is complete (ESR-0015): Primary OpenAI (implemented, live-validated), Secondary Gemini (implemented, hardened at ESR-0018, **live-validated at ESR-0020 WP3** - EBG-0051 Complete), reasoning/coding comparison Anthropic, Gateway OpenRouter, local fallback Ollama - the latter three remain not implemented. Neither OpenAI nor Gemini is wired into a default/production runtime route - both remain opt-in manual-script validation only.
- [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] through [[ESR-0020_ENGINEERING_SESSION_REPORT|ESR-0020]] are all closed. **The EE-0001 Lead/Reviewer trial is concluded** (all four trial sessions run: Claude led ESR-0015/ESR-0017, ChatGPT led ESR-0016/ESR-0018; Sponsor arbitration required was assessed Low, High, Low-Medium and High respectively). At the Section 7 decision point, both AIs independently converged on the same recommendation without sight of each other's answers; the Programme Sponsor made it formal on 10 July 2026: **Claude permanent Lead Engineer, ChatGPT permanent Lead Reviewer**, replacing the alternating rotation. `PBK-0001`/`COC-0001` were formally bound to this appointment at ESR-0019 WP1, then **promoted from Draft to Approved status at ESR-0020** (resolving EBG-0004, open since ESR-0001) - no longer an unactioned flag or a Draft-status artefact governing every session.
- ESR-0018 recorded the trial's longest capability-self-assessment incident, including a new named sub-pattern ("confession as substitute for compliance" - accurate self-diagnosis produced instead of the required action) - resolved only after an explicit, action-forcing Programme Sponsor instruction. Recorded in full in [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 9 and [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] Section 13.
- A Claude&harr;Codex engineering-communication bridge was discussed post-appointment, explicitly out of ESR-0018 scope: architecture (file-based, command-driven, Sponsor-gated handovers) and cost decision (Claude Pro unchanged; a new personal ChatGPT Plus subscription for Codex) recorded as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0057. No implementation authorised; requires its own future ESR and EIP. **ESR-0021's historical audit surfaced a conceptually overlapping item, EBG-0060** (Direct ChatGPT Execution / Repository Execution Agent, from ESR-0010/0011) - [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] recommends a combined judgement on whether EBG-0057's architecture already supersedes it when either is next actioned.
- GIA-BOOT is accepted as a Proof of Concept.
- Further GIA implementation is deferred.
- AIEMS Engineering Agent is adopted to support the Engineering Reviewer role.
- Remaining Engineering Agent validation is deferred.
- Future EAC (Engineering Assurance Capability) implementation is deferred, now tracked as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0059 following ESR-0021 WP6's historical audit, which recovered the full ESR-0012 architecture spec (EAC/EAA/EAR) that had never been captured as a backlog item.
- Guardian Memory remains deferred.
- Conversation Engine expansion remains deferred.
- Guardian Developer Console remains deferred.
- Real observable platform state (ESR-0017 WP9's `platform.status`) unblocked Guardian Orb implementation in principle, and **ESR-0019 delivered it**: the Orb now renders the live repository knowledge graph ([[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8.1, [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0055 Phase 1, completed). Phases 2-4 (cluster illumination, agent-traversal animation, Guardian reasoning connection), true 3D rendering and live animation remain not started - the latter two explicitly deferred by Programme Sponsor decision, not attempted in one pass.
- Automation remains deferred.
- Persistent storage remains deferred.
- GDP-0001 implementation remains deferred - the idea itself (a roadmap-type controlled artefact, floated at ESR-0012/0013 and never created or backlogged, recovered at ESR-0021 WP6) is now substantially superseded in intent by [[JRM-0001_PROJECT_ROADMAP|JRM-0001]], created and approved at ESR-0021 WP5.
- [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] (Project Roadmap) was created and approved at ESR-0021 WP5, the programme's first forward-looking sequencing artefact - closes EBG-0012 (open since ESR-0002), EBG-0027 and EBG-0028 (open since ESR-0005). PBK-0001's Backlog Progression Analysis now cross-references it directly (ESR-0021 WP5, EIP-ESR0021-003).
- ESR-0021 WP6 conducted a full historical audit of all HST/FCH chat history (338,393 lines, 44 files) and added 11 Tier 1 backlog items (EBG-0059 through EBG-0069); Tier 2 (15 items) and Tier 3 findings remain recorded only in that session's conversational record, not in EBR-0001.
- [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] was refreshed to v2.0 at ESR-0021 WP7 (closing EBG-0069) after 13 sessions of staleness - no longer stale, but still not registered in REG-0001 as a controlled artefact, unlike its sibling PCB-0001 (flagged, not actioned).
- Repository First is reinforced by ESR-0012 operational evidence.
- Look Inward Before Looking Outward is identified as an engineering principle derived from operational evidence, but is not introduced as a new AIEMS standard by this status update.
- The Engineering Reviewer and Guardian operating environments remain separated.
- Resilience Before Disablement / local fallback remains accepted as an engineering direction pending implementation evidence.
- External AI providers, persistent memory, voice, vision and internet-backed assistance remain outside the accepted operational product baseline.
- RFEP, RFDP, Continuous Repository Synchronisation and Engineering Ecosystem Synchronisation may be considered in a future formal AIEMS standards review.
- Obsidian is recognised as the human-facing Engineering Knowledge Workspace for OSE while GitHub remains the source of truth.
- A new PBK-0001 practice, "Incremental Visual Convergence Toward the Reference Mock-up," was adopted at ESR-0019: future sessions should include a small UXP change moving toward `aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg` where natural opportunity exists, with cosmetic elements freely adjustable and data-bearing elements gated on real observed data.
- A pre-existing Vite/Tauri scaffolding gap (missing `server.watch.ignored` for `src-tauri/target`, causing `EBUSY` crashes on Windows during `npm run tauri dev`) was found and fixed at ESR-0019, unrelated to that session's planned scope.
- **ESR-0023 closed the entire Guardian authority/boundary architecture cluster** via a new controlled artefact, [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] (Guardian Authority and Boundary Model, v1.0-v1.2), resolving EBG-0031 (open since ESR-0005), EBG-0020 (open since ESR-0004) and EBG-0048 (extending ADR-0010's decision). [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] and [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] were both promoted to Approved after full content re-validation found no contradictions.
- **The Sentinel `TrustTierPolicy` classification model is now wired into `build_default_runtime()`'s production gateway** - resolved at ESR-0024 WP1 per [[EIP-ESR0024-001_TRUSTTIERPOLICY_PRODUCTION_WIRING|EIP-ESR0024-001]] v1.0, closing [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0074. `SentinelTrustGateway`'s own class-level default remains `SimpleApprovalPolicy`, deliberately unchanged to confine the wiring to the one runtime object the live UXP actually runs. GAM-0001's authority/boundary policy model is therefore now genuinely in the production runtime's decision path - though no production call site yet varies request shape per Guardian action, so this is not yet observable as a live behaviour change; the natural next Guardian faculty per JRM-0001 is EBG-0019 (Memory and Data Storage Architecture).
- **A repository write-boundary deviation occurred twice during ESR-0023** (the Engineering Reviewer performing repository writes directly, against PBK-0001 Separation of Duties) and was root-caused and fixed at the tool-configuration level: a `trust_level = "trusted"` project-specific override in Codex's local `~/.codex/config.toml` was removed, restoring the tool's general `OnRequest` approval policy for this repository specifically. Recorded in full in [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7.4 and [[ESR-0023_ENGINEERING_SESSION_REPORT|ESR-0023]] Sections 9.1/10.1/10.2. This is direct empirical evidence strengthening the case for EBG-0057's role-locked-permissions design.
- `gh` CLI (GitHub CLI) was installed (`winget install GitHub.cli`) and authenticated on the Programme Sponsor's machine during ESR-0023, enabling direct GitHub API checks (collaborator lists, branch protection) from future sessions without manual web-UI steps.
- **Remaining ungated architecture gaps**, High priority, ready for a future session per JRM-0001: EBG-0019 (Memory and Data Storage Architecture - the natural next Guardian faculty per ESR-0023 WP5's sequencing judgement), EBG-0046 (Device Independence and Restore Architecture, large scope), EBG-0045/EBG-0049 (Cost and Strategic Value Framework, now live-relevant since real billed provider usage exists via EBG-0070).
- **ESR-0024 closed EBG-0074** (Wire TrustTierPolicy as SentinelCore's Production Default, discovered at ESR-0023 WP5): `build_default_runtime()` now wires `TrustTierPolicy` into the production Guardian runtime per [[EIP-ESR0024-001_TRUSTTIERPOLICY_PRODUCTION_WIRING|EIP-ESR0024-001]] v1.0, ending the "operationally inert" gap in the classification-wiring sense - though no production call site yet varies request shape per Guardian action, so this remains not yet observable as a live behaviour change (Guardian's Action faculty stays Not Started, gated behind EBG-0021). `SentinelTrustGateway`'s own class-level default is deliberately left unchanged (still `SimpleApprovalPolicy`), confining the wiring to the one runtime object the live UXP actually runs.
- **ESR-0024 WP2 delivered PBK-0001's Incremental Visual Convergence practice**: the System Health panel's Sentinel row now names the live-wired policy engine, per [[EIP-ESR0024-002_SYSTEM_HEALTH_POLICY_ENGINE_DETAIL|EIP-ESR0024-002]] v1.0 - the first session in which a WP2 was added mid-session specifically because the Programme Sponsor flagged the session had so far been backend-only, per PBK-0001's Feature-First Delivery Discipline. `policyEngine` is now part of the `platform.status` RPC contract (Codex post-implementation finding, accepted, not actioned): a future `TrustTierPolicy` rename would be a user-visible change, not merely internal.
- **The Claude<->Codex Engineering Bridge (EBG-0057) is implemented as of ESR-0025 WP1**, run deliberately as a separate AIEMS/engineering-tooling workstream (JRM-0001 Track A) rather than a JARVIS/Guardian product item, per the Programme Sponsor's post-ESR-0024 decision - it governs how the two AI engineering collaborators exchange work during sessions on this repository, not any Guardian/Sentinel/UXP capability. The JRM-0001-flagged EBG-0060 overlap was resolved first (`fdb82f7`): DCE (single-AI direct execution) marked Superseded, citing ESR-0023's write-boundary incidents as direct empirical evidence against it; REA (execution-automation agent) folded into EBG-0057's own future-phase scope, not yet actioned. `scripts/aiems_bridge.py` implements all five commands (`init`, `submit-to-review`, `return-findings`, `sponsor-decision`, `submit-response`) per [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] v1.2. Role-locking is enforced as a real code gate, not only a documented convention: `return-findings` (Codex's only command) has no code path capable of writing outside `.aiems-exchange/`, and `submit-response` (the only command that can proceed with real changes) hard-refuses - before any file write - unless the transcript's most recent `sponsor-decision` approves, the current repository HEAD matches the exact state that decision approved (repository drift since approval blocks, rather than only warns, per an Engineering Reviewer finding on the draft EIP), and validation (`pytest`/`validate_repository.py`) passed cleanly (a second Engineering Reviewer finding, on the implemented diff, addressed at v1.1 - a failing run can no longer produce a handover that looks successful). A post-implementation review also found `session`/`work_package` could escape `.aiems-exchange/` via path-traversal injection if left unsanitised - fixed by validating both identifiers at the single point (`_wp_key()`) every path-building function goes through. **A third review found the authorisation/drift checks, preflight and evidence capture in `submit-response` all ran before the Work Package lock was acquired (TOCTOU) - a concurrent `sponsor-decision` could land in that window and the response would still proceed on the stale approval already read; fixed at v1.2 by moving the entire sequence inside the lock**, proven by a test injecting a concurrent `sponsor-decision` during evidence capture and confirming it is genuinely blocked. A live dry run and smoke check confirmed the authorisation-refusal, approval-success, preflight-refusal and path-traversal-refusal paths for real; the full successful cycle with real `claude`/`codex` CLI presence remains for the Programme Sponsor's own terminal to exercise, since neither binary is on the Engineering Implementer's sandboxed shell `PATH` - disclosed as an honest gap, not asserted as tested.

---

# 11. ESR-0008 Outcomes

1. Completed WP1 Product Vision Recovery.
2. Created [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]], [[ERR-0001_ENGINEERING_RECOVERY_REPORT|ERR-0001]] and [[EIR-0001_ENGINEERING_IMPLEMENTATION_RECOMMENDATION|EIR-0001]].
3. Completed WP2 Service / Application / Architecture Evaluation as a documentation and architecture decision activity.
4. Created [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]].
5. Created ADR-0007 through ADR-0013 for UXP, hybrid runtime, Sentinel, Guardian, Agent Framework, device independence and Engineering Ecosystem Synchronisation.
6. Aligned [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] and [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] with ESR-0008 architecture outcomes.
7. Updated [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] and [[REG-0002_ADR_REGISTER|REG-0002]].
8. Created [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]].
9. Accepted [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] as the ESR-0008 repository baseline.
10. Completed EBG-0039 JARVIS Runtime Chat Archive by moving prototype exports into `logs/chats/`.

---

# 12. ESR-0008 Success Criteria

ESR-0008 success criteria have been met for local documentation implementation:

- product vision recovery was recorded in controlled artefacts;
- JARVIS Platform Architecture was recorded for review;
- Guardian Cognitive Architecture was recorded for review;
- AIEMS Engineering Ecosystem Architecture was recorded for review;
- approved ESR-0008 decisions were captured in ADRs;
- Obsidian/OSE was explicitly accounted for;
- no product source code, tests, runtime functionality or baselines were created.

---

# 13. ESR-0009 Outcomes

1. Created [[TPL-0001_ENGINEERING_EXECUTION_PACKAGE_TEMPLATE|TPL-0001]] as the Engineering Execution Package Template.
2. Adopted Tauri + React as the UXP implementation baseline following [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]].
3. Established the Guardian Desktop Platform Shell.
4. Established [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]].
5. Established [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]].
6. Implemented Guardian Experience v1.0.
7. Created [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]].
8. Approved ESR-0010 as AIEMS Engineering Ecosystem Modernisation.
9. Completed [[RBR-ESR0009-001_REPOSITORY_BASELINE_REVIEW|RBR-ESR0009-001]], which recommended RBL-0010 creation.
10. Accepted [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] as the ESR-0009 repository baseline.

---

# 14. ESR-0010 Outcomes

1. Completed AIEMS Engineering Ecosystem Modernisation.
2. Validated ChatGPT Desktop as the preferred Engineering Reasoning Environment.
3. Validated GitHub Desktop as the preferred Local Repository Management / Programme Sponsor Review Tool.
4. Approved Guardian UXP Orb design direction as a future implementation direction.
5. Recorded GitHub connector / DCE findings as observations only.
6. Accepted ESR-0010 Repository Baseline Review outcome.
7. Created [[ESR-0010_ENGINEERING_SESSION_REPORT|ESR-0010]] as the formal session closure report.
8. Retained [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] as the current accepted repository baseline.

---

# 15. ESR-0011 Outcomes

1. Completed Architecture Validation and Implementation Readiness.
2. Validated Sentinel, Platform Services, Guardian, UXP, Guardian Orb and GIA positioning.
3. Confirmed GIA as the local-first observability and instrumentation capability.
4. Confirmed Guardian Orb as a UXP composition surface that should consume observable state rather than own authoritative platform state.
5. Accepted Resilience Before Disablement / local fallback as an engineering direction pending implementation evidence.
6. Found no mandatory AIEMS governance changes required before implementation.
7. Approved transition from architecture validation into implementation-led engineering from ESR-0012 onward.
8. Created [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] as the formal session closure report.
9. Retained [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] as the current accepted repository baseline.

---

# 16. ESR-0012 Outcomes

1. Validated AIEMS implementation workflow.
2. Validated Codex implementation workflow.
3. Validated independent engineering review workflow.
4. Completed GIA-BOOT Proof of Concept.
5. Created AIEMS Engineering Agent.
6. Completed Engineering Agent live validation.
7. Demonstrated repository-first engineering.
8. Separated ChatGPT and Guardian operating environments.
9. Accepted GIA-BOOT as a Proof of Concept.
10. Deferred further GIA implementation.
11. Adopted AIEMS Engineering Agent for ChatGPT engineering.
12. Reinforced Repository First.
13. Identified Look Inward Before Looking Outward as an engineering principle derived from operational evidence.
14. Created [[ESR-0012_ENGINEERING_SESSION_REPORT|ESR-0012]] as the formal session closure report.
15. Retained [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] as the current accepted repository baseline.

---

# 17. ESR-0013 Outcomes

1. Established Guardian Runtime Foundation.
2. Integrated Guardian runtime ownership into the JARVIS lifecycle.
3. Added Guardian runtime service registration and status snapshots.
4. Added bounded Guardian runtime observability through diagnostics, events and lifecycle history.
5. Preserved Guardian Memory, Provider Framework, Sentinel, Conversation Engine expansion, Guardian Developer Console, Guardian Orb, Automation, persistent storage, EAC and GDP-0001 implementation as deferred capabilities.
6. Prepared [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] for Programme Sponsor closure review.
7. Retained [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] as the current accepted repository baseline pending any separate baseline acceptance.

---

# 18. ESR-0014 Outcomes

1. Established Sentinel as a standalone top-level package.
2. Implemented Sentinel Core trust boundary primitives.
3. Implemented provider abstraction, provider registry and capability resolution.
4. Implemented the local deterministic provider.
5. Implemented provider configuration, credential references and retry policies.
6. Implemented the provider orchestrator foundation with health states, health-aware capability routing, automatic failover and execution history.
7. Added dedicated test suites for Sentinel Core, providers, provider configuration and provider orchestration, taking coverage from 58 to 100 passing tests.
8. Created [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] to support evidence-based AI provider ecosystem selection.
9. Approved [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]], positioning Sentinel as the AI Execution and Security Platform for AIEMS.
10. Created [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] as the formal session closure report.
11. Retained [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] as the current accepted repository baseline.

---

# 19. ESR-0014A Outcomes

1. Identified, through an AI-followability review of AIEMS, that mandatory Engineering Session initialisation reading grows without bound as sessions accumulate.
2. Created [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]], defining a tiered knowledge structure (Current State, Architecture, Active Standards, Current ESR, Historical Archive).
3. Amended [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] Session Initialisation and WP0A guidance to reference GDE-0001 rather than enumerating the full AIEMS History and Full Chat archive.
4. Amended [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] and README.md for consistency with GDE-0001.
5. Registered GDE-0001, ESR-0014A and ESR-0014 itself in [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
6. Did not retire, delete or modify any AIEMS History or Full Chat artefact.
7. Created [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] as a post-closure addendum, preserving [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] and [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] without reopening them.

---

# 20. ESR-0015 Outcomes

1. Established the Sentinel execution pipeline in full: `sentinel/audit.py` (AuditRecorder infrastructure), `sentinel/policy.py` (PolicyEngine abstraction), `sentinel/openai_provider.py` (first external provider adapter), `jarvis/interfaces/sentinel_conversation.py` (Guardian/Sentinel integration).
2. Completed [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] provider scoring; approved Primary OpenAI, Secondary Gemini, reasoning/coding comparison Anthropic, Gateway OpenRouter (experimentation only), local fallback Ollama.
3. Demonstrated the first live, policy-gated, audited Guardian conversation against a real external AI provider, run by the Programme Sponsor.
4. Grew test coverage from 105 to 133 passing tests with zero regressions.
5. Ran under the [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Lead/Reviewer trial (Claude Lead, ChatGPT Reviewer); 10 Reviewer findings raised, 10 accepted.
6. Recommended and drafted [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]]; the Programme Sponsor accepted it on 8 July 2026, superseding [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]].
7. Created [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] as the formal session closure report, including an Engineering Implementer draft of the EE-0001 trial scorecard pending independent Reviewer scoring.

---

# 21. ESR-0016 Outcomes

1. Established the Sentinel trust-tier policy model: `TrustTier` (routine/sensitive/restricted), `TrustCategory` (five categories), `TrustTierPolicy` implementing the existing `PolicyEngine` seam, with `SimpleApprovalPolicy` retained as the unchanged production default.
2. Corrected a classification-precedence defect found in review (deny-worthy categories could be softened to human review by also setting approval-required) before merge, with a permanent regression test.
3. Updated [[CURRENT_ARCHITECTURE|CURRENT_ARCHITECTURE.md]] (WP2A) and [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] (WP2B) to reflect the implemented model, following an Engineering Reviewer redirect of the original EIP (which had targeted SAM-0001 alone) to preserve SAM-0001's architecture-only scope.
4. Identified and corrected one genuine scope non-conformance: an unapproved substitute governance artefact created during WP2, including a self-exempting review-avoidance rule proposal - detected by the Engineering Reviewer, removed by the Engineering Lead, and the proposed rule explicitly rejected by the Programme Sponsor.
5. Ran under the [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Lead/Reviewer trial with the rotation reversed from ESR-0015 (ChatGPT Lead, Claude Reviewer); reconciled scorecard shows both sides independently assessing Sponsor arbitration required as High, against ESR-0015's Low.
6. Added a dated EE-0001 Section 8 entry clarifying the "findings" metric's scope (submitted-work defects only), recomputing ESR-0016 to 7 findings / average discovery weight 3.0; confirmed ESR-0015's existing figures required no correction.
7. Retained [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] as the current accepted repository baseline; ESR-0016's changes judged incremental, not warranting a new baseline.
8. Grew test coverage from 133 to 144 passing tests with zero regressions.
9. Created [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] as the formal session closure report.

---

# 22. Session Start Guidance

At the start of the next separately approved engineering session or approved implementation activity, follow [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] knowledge tiering:

1. Review README.md for repository orientation and platform context.
2. Review [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]], the repository baseline the Programme Sponsor has accepted as current (established at ESR-0029 WP9, superseding RBL-0016).
3. Review [[PST-0001_PROGRAMME_STATUS|PST-0001]] (Current State tier).
4. Review [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] (Project Roadmap) for horizon-placement guidance before selecting the next Work Package - per PBK-0001's Backlog Progression Analysis, an item's existing JRM-0001 placement should inform the recommendation rather than being re-derived from scratch. **Note JRM-0001's own Track A/B tables are themselves stale, not reflecting ESR-0028's or ESR-0029's progress - a deferred gap, flagged rather than silently left. ESR-0029 closed EBG-0082 (cross-module resource research) and EBG-0083 Phase 1 in full (GIA local observability)**. Remaining open items include EBG-0083 Phases 2-4, EBG-0084's implementation half (Sponsor Approval Service), EBG-0081's shared-animation-scheduler half (Candidate Backlog), EBG-0046, EBG-0023 (Backup/Recovery, unblocked since EBG-0080). **Track A (AIEMS process): EBG-0057 (Claude<->Codex Engineering Bridge) is now proven in genuine real use across four consecutive entire sessions (ESR-0026, ESR-0027, ESR-0028, ESR-0029)** - REA (its own future-phase scope) is a candidate once the MVP core has been proven in more real use.
5. Review the Architecture tier as referenced by PST-0001 - for Guardian authority/permission/safety work specifically, review [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] (v1.2, Approved) and [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] (v0.3, Approved) before touching Guardian/Sentinel enforcement code - note GAM-0001's policy model is now wired into the production runtime (`build_default_runtime()`, EBG-0074, ESR-0024 WP1) though no production call site yet varies request shape per Guardian action. For UXP/Guardian-experience work specifically, review [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8.1 before touching `src/GuardianOrbGraph.jsx`, `src/KnowledgeGraphPanels.jsx` or `src/App.jsx` - the `SystemHealthPanel`/`DiagnosticsPanel` duplication (EBG-0073) was resolved at ESR-0023 WP6.
6. Review Active Standards (STD-0001 through STD-0004) where the session's work touches artefact creation or modification.
7. Review [[ESR-0029_ENGINEERING_SESSION_REPORT|ESR-0029]] (Current ESR tier, Closed) - the fourth session run entirely through `scripts/aiems_bridge.py` with no manual relay, confirming the draft/review/approval/implementation/commit/post-commit-review template is genuinely repeatable across a fourth session, delivering the Guardian Orb Canvas 2D migration and GIA Phase 1, and establishing a new repository baseline (RBL-0017) superseding RBL-0016. Also review [[ESR-0023_ENGINEERING_SESSION_REPORT|ESR-0023]] Sections 9.1/10.1/10.2 as a live example of a repository write-boundary deviation, its root cause, and how it was found and fixed - directly relevant to the bridge's role-locked-permissions design.
8. Review [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
9. Review [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (v1.25, **Approved** status) - cross-references JRM-0001 directly from Backlog Progression Analysis (ESR-0021 WP5); unchanged this session.
10. Review [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] (v1.13, **Approved** status) - same role-binding as PBK-0001; already states the Engineering Reviewer "does not modify the repository directly," confirmed unambiguous and not re-worded at ESR-0023 (see [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7.4).
11. Confirm the permanent Lead/Reviewer appointment (Claude Engineering Implementer, Codex/ChatGPT Engineering Reviewer, EE-0001 Section 7) has not been separately revisited - no rotation confirmation is required.
12. Search the Historical Archive (AIEMS History and Full Chat artefacts) only where deeper context is required - ESR-0021 WP6 already conducted a full audit of this archive; check [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0059 through EBG-0069 (and that session's Tier 2/3 conversational record) before re-deriving the same findings.
13. Confirm Programme Sponsor approval before creating any future Engineering Session Report, future repository baseline or future engineering objective - and before beginning any implementation, confirm an Engineering Implementation Package (or equivalent reviewed Working Report) has actually been drafted, reviewed and approved first, not implemented then retrofitted with paperwork.
14. If the Engineering Reviewer's environment has local shell/tool access (as Codex's does), confirm it is not configured with elevated/trusted permissions for this repository before the session begins - `codex doctor`'s `approval policy` should read `OnRequest` for this project, per the ESR-0023 root-cause fix (Section 10.2).

This guidance records the ESR-0029 closed state and RBL-0017's acceptance at ESR-0029 WP9 (superseding RBL-0016). PST-0001 does not create a new engineering session or approve implementation outside separately authorised engineering work.

---

# 23. Maintenance

[[PST-0001_PROGRAMME_STATUS|PST-0001]] shall be reviewed and updated:

- at phase closure;
- when the active engineering phase changes;
- when the next planned engineering activity changes materially;
- when the capability roadmap changes;
- when a major baseline is accepted;
- when the Programme Sponsor directs an update.

PST-0001 should remain concise and must not duplicate detailed controlled artefacts.

---
# Guiding Principle

> *"The repository is the programme memory. PST-0001 is the session reload point."*

---

## OSE Relationships

| Artefact | OSE Relationship |
|----------|------------------|
| [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]] | Defines the retrospective relationship-only enrichment rule applied to this programme status artefact. |
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Establishes Engineering Ecosystem Synchronisation and the repository-compatible OSE context for current-state reload. |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Provides product vision traceability context for programme status interpretation. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Records authoritative artefact identity, ownership, status and current version. |
| [[REG-0002_ADR_REGISTER|REG-0002]] | Records architectural decision context relevant to programme status. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records backlog context that informs current and next engineering work. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Forward-looking sequencing artefact, created and approved at ESR-0021 WP5 - closes EBG-0012/0027/0028; cross-referenced directly from PBK-0001's Backlog Progression Analysis; updated at ESR-0022 WP1/WP6/WP7 (EBG-0070/0072/0073). |
| [[ESR-0029_ENGINEERING_SESSION_REPORT|ESR-0029]] | Current closed engineering session report (19 July 2026) - the fourth session run entirely through the AIEMS Exchange Bridge with no manual relay, across seven Work Packages: WP1 (cross-module resource-interaction research, EBG-0082), WP2 (Guardian Orb Canvas 2D rendering migration, ADR-0021 implemented, with a live-verified performance-regression fix), WP3/WP4/WP6/WP7 (GIA Phase 1a-1d, closing EBG-0083 Phase 1 in full), WP5 (Sponsor Approval Service decision, ADR-0022). Session-wide WP8 Pass, WP9 Accept - new baseline RBL-0017 established, superseding RBL-0016, after two post-commit fix rounds. |
| [[ESR-0028_ENGINEERING_SESSION_REPORT|ESR-0028]] | Prior closed engineering session report (18 July 2026) - the third session run entirely through the AIEMS Exchange Bridge with no manual relay, across five Work Packages: WP1 (process hygiene batch, EBG-0058/0005/0068/0071), WP2 (product requirements backlog identification, EBG-0017), WP3 (cost and strategic value framework, EBG-0045/0049/0024), WP4 (Guardian Orb 3D rotation, EBG-0055 Phase 1.5, seven post-implementation fix rounds), WP5 (Guardian Orb rendering engine decision, ADR-0021). Session-wide WP6 Pass, WP7 Accept - new baseline RBL-0016 established, superseding RBL-0015. |
| [[ESR-0027_ENGINEERING_SESSION_REPORT|ESR-0027]] | Prior closed engineering session report (18 July 2026) - the second session run entirely through the AIEMS Exchange Bridge with no manual relay. WP1 implemented EBG-0080 (Personal Memory Implementation, EIP-ESR0027-001 v1.1). WP2 implemented EBG-0077 (UXP DiagnosticsPanel Reconciliation, EIP-ESR0027-002 v1.0). Session-wide WP6 Pass, WP7 Accept - RBL-0015 retained. |
| [[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]] | Prior closed engineering session report (17 July 2026) - the first session run entirely through the AIEMS Exchange Bridge with no manual relay. WP1 implemented EBG-0075 (Ollama Local Fallback Provider, EIP-ESR0025-002 v1.1), including a post-implementation `AttributeError` fix and a mid-session tooling deviation (EBG-0079). WP2 approved MDS-0001 v1.0 (EBG-0019). WP3 approved ADR-0020 v1.0 (EBG-0076). Session-wide WP6 Pass, WP7 Accept - RBL-0015 retained. |
| [[ESR-0025A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0025A]] | Prior post-closure engineering addendum (17 July 2026) - fixed the AIEMS Exchange Bridge's Windows preflight crash, a Programme Sponsor-authorised deviation, enabling ESR-0026's fully-real bridge usage. |
| [[ESR-0025_ENGINEERING_SESSION_REPORT|ESR-0025]] | Prior closed engineering session report (17 July 2026) - WP1 resolved the EBG-0060/EBG-0057 overlap and implemented EBG-0057 (Claude<->Codex Engineering Bridge) per [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] v1.2, hardened across three post-implementation review rounds. Also drafted EIP-ESR0025-002 (Ollama Local Fallback Provider, carried forward, Draft), completed a desktop launcher (EBG-0078), and registered EBG-0076/EBG-0077. Session-wide WP6 Pass, WP7 Accept - RBL-0015 retained. |
| [[ESR-0024_ENGINEERING_SESSION_REPORT|ESR-0024]] | Prior closed engineering session report (17 July 2026) - WP1 wired `TrustTierPolicy` into `build_default_runtime()` per [[EIP-ESR0024-001_TRUSTTIERPOLICY_PRODUCTION_WIRING|EIP-ESR0024-001]] v1.0, closing EBG-0074; WP2 delivered Incremental Visual Convergence per [[EIP-ESR0024-002_SYSTEM_HEALTH_POLICY_ENGINE_DETAIL|EIP-ESR0024-002]] v1.0. Session-wide WP6 Pass, WP7 RBL-0015 retained. |
| [[ESR-0023_ENGINEERING_SESSION_REPORT|ESR-0023]] | Prior closed engineering session report (17 July 2026) - closed the Guardian authority/boundary cluster via GAM-0001 (EBG-0031/0020/0048), AAM-0001/MOD-0001 promoted to Approved (EBG-0041), UXP diagnostics deduplication (EBG-0073), a repository write-boundary deviation root-caused and fixed. RBL-0015 retained. |
| [[ESR-0022_ENGINEERING_SESSION_REPORT|ESR-0022]] | Prior closed engineering session report (16 July 2026) - production provider wiring and System Health panel (WP1, EIP-ESR0022-001), a self-disclosed and corrected process deviation, a separately-authorised sidecar `cwd` fix, and a new repository baseline (RBL-0015, session-wide WP7). |
| [[ESR-0021_ENGINEERING_SESSION_REPORT|ESR-0021]] | Prior closed engineering session report (15 July 2026) - PBK-0001 corrections (WP2/WP3), Knowledge Metrics/Active Clusters UXP panels (WP4), JRM-0001 creation and approval (WP5), full historical HST/FCH audit adding 11 backlog items (WP6), Capability Readiness Matrix refresh (WP7). |
| [[ESR-0020_ENGINEERING_SESSION_REPORT|ESR-0020]] | Prior closed engineering session report (13 July 2026) - PBK-0001/COC-0001 promoted to Approved (EBG-0004), EBG-0051 Gemini live validation, PCB-0001 v2.1 refresh/acceptance (EBG-0056), UXP convergence, EBG-0026 transcript export. |
| [[ESR-0019_ENGINEERING_SESSION_REPORT|ESR-0019]] | Prior closed engineering session report (11 July 2026) - PBK-0001/COC-0001 role-binding (WP1) and the Guardian Orb knowledge-graph delivery (WP2, EBG-0055 Phase 1). |
| [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] | Prior closed engineering session report (10 July 2026) - Gemini provider production-readiness hardening (EBG-0051) and the EE-0001 Section 7 decision/permanent appointment. |
| [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] | Closed engineering session report - nine Work Packages including the first live interactive UXP and a Guardian Orb design-baseline recovery. |
| [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] | Closed engineering session report recording the Sentinel trust-tier policy model and its architecture alignment, delivered and independently verified. |
| [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] | Closed engineering session report recording the Sentinel execution pipeline delivered and proven end to end. |
| [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] | Current accepted repository baseline, accepted at ESR-0029 WP9, superseding RBL-0016. |
| [[RBL-0016_REPOSITORY_BASELINE|RBL-0016]] | Previous accepted repository baseline, accepted at ESR-0028 WP7 (retained through no intervening session), superseding RBL-0015. |
| [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] | Previous accepted repository baseline, accepted at ESR-0019 closure (retained through ESR-0020 and ESR-0021), superseding RBL-0013. |
| [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] | Prior accepted repository baseline, accepted at ESR-0017 closure (retained through ESR-0018), superseding RBL-0012 (mid-ESR-0017) and RBL-0011 (ESR-0015-ESR-0016). |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Approved Guardian Experience Architecture; Section 8.1's Guardian Orb knowledge-graph design direction (recovered at ESR-0017) had its Phase 1 implemented at ESR-0019. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial, concluded at ESR-0018 (Section 7): all four sessions closed (ESR-0015 Claude Lead, ESR-0016 ChatGPT Lead, ESR-0017 Claude Lead/Cold Start, ESR-0018 ChatGPT Lead/decision point); permanent appointment made - Claude Lead Engineer, ChatGPT Lead Reviewer, formally bound into PBK-0001/COC-0001 at ESR-0019 WP1. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Provider evaluation matrix; decision outcome recorded during ESR-0015 WP3a. |
| [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] | Closed engineering session report recording Sentinel AI Execution and Security Platform implementation. |
| [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] | Closed post-closure addendum recording GDE-0001 knowledge tiering. |
| [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] | Defines the knowledge tier structure this status update's Session Start Guidance now follows. |
| [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] | Engineering session report recording the Guardian Platform Foundation. |
| [[ESR-0012_ENGINEERING_SESSION_REPORT|ESR-0012]] | Engineering session report recording ESR-0012 closure, GIA-BOOT Proof of Concept completion and AIEMS Engineering Agent validation. |
| [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] | Engineering session report recording ESR-0011 closure, Architecture Validation and Implementation Readiness outcomes and ESR-0012 implementation handover. |
| [[ESR-0010_ENGINEERING_SESSION_REPORT|ESR-0010]] | Engineering session report recording ESR-0010 closure and ESR-0011 handover state. |
| [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]] | Engineering session report recording ESR-0009 closure and ESR-0010 handover. |
| [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] | Previous accepted repository baseline, superseded by [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] on 8 July 2026. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Previous accepted repository baseline and ESR-0009 starting point. |
| [[RBR-ESR0009-001_REPOSITORY_BASELINE_REVIEW|RBR-ESR0009-001]] | Repository baseline review that recommended RBL-0010 creation. |
| [[TPL-0001_ENGINEERING_EXECUTION_PACKAGE_TEMPLATE|TPL-0001]] | Engineering Execution Package Template established during ESR-0009. |
| [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] | Sentinel Trust Architecture established during ESR-0009. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Guardian Experience Architecture v1.0 established during ESR-0009. |
| [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]] | Decision authority for Tauri + React UXP direction. |

---
## Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] | Closed engineering session report recording the Sentinel trust-tier policy model and its architecture alignment. |
| [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] | Current accepted repository baseline, accepted at ESR-0015 closure, retained through ESR-0016; supersedes RBL-0010. |
| [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] | Closed engineering session report recording the Sentinel execution pipeline delivered and proven end to end. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial; ESR-0015 and ESR-0016 both closed; governs ESR-0017's Cold Start rotation next. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Provider evaluation matrix; decision outcome recorded during ESR-0015 WP3a. |
| [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] | Closed engineering session report recording Sentinel AI Execution and Security Platform implementation. |
| [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] | Closed post-closure addendum recording GDE-0001 knowledge tiering. |
| [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] | Defines the knowledge tier structure this status update's Session Start Guidance now follows. |
| [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] | Engineering session report recording the Guardian Platform Foundation. |
| [[ESR-0012_ENGINEERING_SESSION_REPORT|ESR-0012]] | Engineering session report recording ESR-0012 closure, GIA-BOOT Proof of Concept completion and AIEMS Engineering Agent validation. |
| [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] | Engineering session report recording ESR-0011 closure, Architecture Validation and Implementation Readiness outcomes and ESR-0012 implementation handover. |
| [[ESR-0010_ENGINEERING_SESSION_REPORT|ESR-0010]] | Engineering session report recording ESR-0010 closure, Engineering Ecosystem Modernisation outcomes and ESR-0011 handover state. |
| [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]] | Engineering session report recording ESR-0009 closure, delivered artefacts and ESR-0010 handover. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Previous accepted ESR-0008 repository baseline and ESR-0009 starting point. |
| [[RBR-ESR0009-001_REPOSITORY_BASELINE_REVIEW|RBR-ESR0009-001]] | Repository baseline readiness review that recommended RBL-0010 creation. |
| [[TPL-0001_ENGINEERING_EXECUTION_PACKAGE_TEMPLATE|TPL-0001]] | Engineering Execution Package Template established during ESR-0009. |
| [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] | Sentinel Trust Architecture established during ESR-0009. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Guardian Experience Architecture v1.0 established during ESR-0009. |
| [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]] | Tauri + React UXP decision authority. |
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Engineering Ecosystem Synchronisation decision authority for ESR-0010 preparation. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Engineering session report recording ESR-0008 architecture evaluation and closure outputs. |
| [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] | Closed engineering session that established ESR-0008 readiness. |
| [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] | Previous accepted repository baseline. |
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Previous accepted repository baseline and ESR-0007 starting point. |
| [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] | Repository product capability assessment completed during ESR-0007. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Current accepted product capability baseline. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Authoritative backlog source and EBG-0039 completion record. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity and cognitive architecture created during ESR-0008. |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Product vision traceability model created during ESR-0008 WP1. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product architecture context for JARVIS engineering. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Authoritative capability maturity model. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Controlled artefact register updated for ESR-0010 closure and current metadata alignment. |

---

# Version History

| 2.62 | 19 July 2026 | Claude Engineering Implementer | ESR-0029 formally closed (19 July 2026). Authored [[ESR-0029_ENGINEERING_SESSION_REPORT|ESR-0029]] Engineering Session Report v1.0 covering WP0 (research-first objective redirection), WP1-WP7 (cross-module resource research, Guardian Orb Canvas 2D migration with a live-verified performance-regression fix, GIA Phase 1's four-slice staged delivery, Sponsor Approval Service decision), and session-wide WP8 (Pass)/WP9 (Accept, new baseline RBL-0017 established after two post-commit fix rounds). Updated Current Mode/Phase/Workflow/Objective (ESR-0029 closed, no session currently open), Current Engineering Focus (full session summary replacing ESR-0028's), Session Start Guidance (items 4/7 and closing line retargeted to ESR-0029/RBL-0017), and OSE Relationships (ESR-0029 added as current, ESR-0028 relabeled prior). |
| 2.61 | 19 July 2026 | Claude Engineering Implementer | ESR-0029 WP9 second post-commit fix - addressed a further Codex Medium finding: Current Workflow and Current Engineering Objective still described ESR-0028 as the current/closed session with no new session opened, directly conflicting with the Current Mode/Phase rows already corrected in 2.60. Both rows rewritten to describe ESR-0029 as the current, not-yet-formally-closed session through WP9. |
| 2.60 | 19 July 2026 | Claude Engineering Implementer | ESR-0029 WP9 post-commit fix - addressed a Codex Medium finding: Current Mode and Current Phase still said ESR-0028 was the latest closed session and no further session had been opened, directly contradicting the adjacent Current Repository Baseline row (RBL-0017, accepted at ESR-0029 WP9) added in 2.59. Both rows rewritten to state ESR-0029 is the current, not-yet-formally-closed session, through WP9 (baseline accepted), with its Engineering Session Report still pending. |
| 2.59 | 19 July 2026 | Claude Engineering Implementer | ESR-0029 WP9: RBL-0017 accepted (new baseline, superseding RBL-0016) - Programme Sponsor determination, agreeing with both independent WP8 views (Guardian Orb Canvas 2D migration + GIA Phase 1 observability judged at least comparable in substance to RBL-0016's own trigger). Updated Current Repository Baseline references (Current Repository Baseline field, Section 8, Section 9, Session Start Guidance item 2/closing line, OSE Relationships row). Disclosed but not fixed: Section 8's "Current Engineering Session" narrative rows still describe ESR-0026, stale since ESR-0027/ESR-0028/ESR-0029 - flagged for a future catch-up given its scope. |
| 2.58 | 18 July 2026 | Claude Engineering Implementer | ESR-0028 formally closed (18 July 2026). Authored [[ESR-0028_ENGINEERING_SESSION_REPORT|ESR-0028]] Engineering Session Report v1.0 covering WP0 (two pre-WP1 corrections, four-WP objective selection), WP1-WP5 (process hygiene, product requirements backlog identification, cost framework, Guardian Orb 3D rotation with seven fix rounds, rendering-engine decision), and session-wide WP6 (Pass)/WP7 (Accept, new baseline RBL-0016 established). Updated Current Mode/Phase/Workflow/Objective (ESR-0028 closed, no session currently open), Current Engineering Focus (full session summary), Session Start Guidance (items 2/7 and closing line retargeted to ESR-0028/RBL-0016), and OSE Relationships (ESR-0028 and ESR-0027 both added, closing a pre-existing gap where ESR-0027 had never been added). |
| 2.57 | 18 July 2026 | Claude Engineering Implementer | ESR-0028 WP7: RBL-0016 accepted (new baseline, superseding RBL-0015) - Programme Sponsor determination, agreeing with both independent WP6 views (Guardian Orb rotation/visual cleanup judged a materially new user-visible product change). Updated Current Repository Baseline references throughout (Current Mode field, Section 8, Section 9, Session Start Guidance item 2/closing line, OSE Relationships). Disclosed but not fixed: Section 8's "Current Engineering Session" narrative rows still describe ESR-0026, stale since ESR-0027/ESR-0028 - flagged for a future catch-up given its scope. |
| 2.56 | 18 July 2026 | Claude Engineering Implementer | ESR-0028 WP1-WP5 catch-up: PST-0001 had not been updated throughout ESR-0028 (a gap found ahead of WP6). Updated Current Mode/Baseline/Phase/Workflow/Objective (ESR-0028 open, WP6 in progress, WP1-WP5 summarised), Current Engineering Focus (full WP1-WP5 summary promoted to current, ESR-0027 demoted to Prior Session, oldest Prior Session ESR-0025 trimmed), Session Start Guidance (items 4/7 and closing line retargeted to ESR-0028/WP6-in-progress). |
| 2.55 | 18 July 2026 | Claude Engineering Implementer | ESR-0027 formally closed (18 July 2026). Authored [[ESR-0027_ENGINEERING_SESSION_REPORT|ESR-0027]] Engineering Session Report v1.0 covering WP0 (scope check expanding WP1 to a working consent gate), WP1-WP2 (Personal Memory, UXP DiagnosticsPanel reconciliation, both via the fully real AIEMS Exchange Bridge with no manual relay), and session-wide WP6 (Pass)/WP7 (Accept, RBL-0015 retained). Updated Current Mode/Phase/Workflow/Objective (ESR-0027 closed, no session currently open), Current Engineering Focus (full session summary, ESR-0026 remains next Prior Session), Session Start Guidance (items 2/4/7 and closing line retargeted to ESR-0027/RBL-0015 retention, EBG-0080/EBG-0077 marked resolved). |
| 2.54 | 18 July 2026 | Claude Engineering Implementer | ESR-0027 session-wide WP6 (Independent Repository Verification, Pass - two Low findings fixed) and WP7 (Repository Baseline Acceptance, Accept - retain RBL-0015) both closed against the full session diff (`f4a96a0`..`d7ab1f7`). Engineering Reviewer (Codex) verified via the bridge, both independent baseline views converged, Programme Sponsor made the WP7 determination. See ESR-0027 WP6 handover v0.3. Updated Current Mode/Baseline/Objective. |
| 2.53 | 18 July 2026 | Claude Engineering Implementer | ESR-0027 WP2 fully closed - Engineering Reviewer (Codex) post-implementation review via the bridge: Pass, no blocking findings against committed diff f29cf66. Both of ESR-0027's Work Packages (WP1 Memory, WP2 UXP reconciliation) now fully closed with clean final confirmations. |
| 2.52 | 18 July 2026 | Claude Engineering Implementer | ESR-0027 WP2 complete: EBG-0077 (UXP static placeholder reconciliation) implemented per EIP-ESR0027-002 v0.2 - Engineering Reviewer confirmed no blocking findings, Programme Sponsor approved. first-light removed from DiagnosticsPanel; boundary/shell/agents kept as honest, roadmap-grounded diagnostics. Verified live, npm run build clean. Both of ESR-0027's Work Packages (WP1 Memory, WP2 UXP reconciliation) now complete. Updated Current Mode and Current Engineering Focus. |
| 2.51 | 18 July 2026 | Claude Engineering Implementer | ESR-0027 WP1 fully closed - Engineering Reviewer (Codex) final confirmation via the bridge: Pass, both Medium post-commit findings resolved against fix commit dbd8424, no new blocking findings, one non-blocking advisory recorded. Updated Current Mode and Current Engineering Focus. WP2 (EBG-0077) next. |
| 2.50 | 18 July 2026 | Claude Engineering Implementer | ESR-0027 WP1 post-commit review (Engineering Reviewer/Codex, via the bridge) of committed diff 505023c found two Medium blocking findings, both fixed: GuardianRuntime memory methods now also require RUNNING state; PersonalMemoryStore.add() now enforces durable consent traceability at the storage layer. Aligned EIP-ESR0027-001 (1.0 to 1.1). Updated Current Mode and Current Engineering Focus. 286 tests total (was 282). Resubmitted for Engineering Reviewer final confirmation. |
| 2.49 | 18 July 2026 | Claude Engineering Implementer | ESR-0027 opened, WP1 delivered: EBG-0080 (Personal Memory Implementation) implemented and closed per [[EIP-ESR0027-001_PERSONAL_MEMORY_IMPLEMENTATION|EIP-ESR0027-001]] v1.0 (Engineering Reviewer/Codex reviewed across two rounds - two Medium and one Low finding on v0.1 addressed at v0.2 and confirmed resolved, one further Low/editorial finding corrected at v0.3 - Programme Sponsor approved via `sponsor-decision`). Updated Current Mode/Phase/Workflow/Objective (per PBK-0001 WP0B, Current Mode still anchors to latest-closed ESR-0026 until ESR-0027 itself closes), Current Engineering Focus (ESR-0027 WP1 summary including the live-smoke-check-found SQLite connection-leak fix and the retroactive test-isolation fix across pre-existing `test_stdio_rpc.py` tests, ESR-0026 demoted to Prior Session). 282 tests total (was 254), validator clean (120 warnings, 111 pre-existing plus 9 known disclosed). WP2 (EBG-0077) not yet started. |
| 2.48 | 17 July 2026 | Claude Engineering Implementer | ESR-0026 formally closed (17 July 2026). Authored [[ESR-0026_ENGINEERING_SESSION_REPORT|ESR-0026]] Engineering Session Report v1.0 covering WP0 (scope check reframing EBG-0019/EBG-0076 as specifications), WP1-WP3 (Ollama provider, MDS-0001, ADR-0020, all via the fully real AIEMS Exchange Bridge with no manual relay), and session-wide WP6 (Pass)/WP7 (Accept, RBL-0015 retained). Updated Current Mode/Phase/Workflow/Objective (ESR-0026 closed, no session currently open), Current Engineering Focus (full session summary, ESR-0025/ESR-0025A demoted to Prior Session), Section 6 Completed Milestones (7 new closure rows), Section 8 Active/Next Planned Work, Session Start Guidance (items 2/4/7 and closing line retargeted), and OSE Relationships (ESR-0026 and ESR-0025A added, ESR-0025 demoted). |
| 2.47 | 17 July 2026 | Claude Engineering Implementer | ESR-0026 session-wide WP6 (Independent Repository Verification, Pass) and WP7 (Repository Baseline Acceptance, Accept - retain RBL-0015) both closed against the full session diff (`85e62c3`..`9058f5c`). Engineering Reviewer (Codex) verified via the bridge, both independent baseline views converged, Programme Sponsor made the WP7 determination. See ESR-0026 WP6 handover v0.3. Updated Current Engineering Objective. |
| 2.46 | 17 July 2026 | Claude Engineering Implementer | ESR-0026 WP3 complete: closed EBG-0076 per [[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS|ADR-0020]] v1.0 (Approved) - a binding three-part security gate (authentication, rate limiting, TLS) any future network-facing Guardian/Sentinel interface must satisfy before approval, grounded in ADR-0019, `sentinel/policy.py` and PEM-001. Engineering Reviewer (Codex) confirmed no blocking findings via the bridge, Programme Sponsor approved. All three of ESR-0026's Work Packages now complete. Updated Current Mode/Objective. |
| 2.45 | 17 July 2026 | Claude Engineering Implementer | ESR-0026 WP1 fully closed (post-implementation `AttributeError` fix, Codex's final confirmation, no manual relay throughout) and WP2 complete: closed EBG-0019 per [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] v1.0 (Approved) - Session/Personal/Shared-Family memory taxonomy and storage architecture specification, staying within the boundary GAM-0001 Section 9.2 reserved for it. Engineering Reviewer (Codex) confirmed no blocking findings via the bridge, Programme Sponsor approved. 254 tests total. Updated Current Mode/Objective for both closures. |
| 2.44 | 17 July 2026 | Claude Engineering Implementer | ESR-0026 opened (three-WP objective: Ollama implementation, EBG-0019 spec, ADR-0020 spec). WP1 complete: closed EBG-0075 (Ollama Local Fallback Provider) per [[EIP-ESR0025-002_OLLAMA_LOCAL_FALLBACK_PROVIDER|EIP-ESR0025-002]] v1.0 - the first genuine, real Engineering Reviewer review via the now-working AIEMS Exchange Bridge (no blocking findings), Programme Sponsor approved via `sponsor-decision`. `sentinel/ollama_provider.py` implemented; a genuine test-isolation defect (real network calls to the Sponsor's actual Ollama server during automated tests) found and fixed; a live smoke check disclosed the EIP's 90s timeout recommendation timed out once, succeeding only at 180s - implemented as approved, flagged for future tuning. 249 tests total (was 238). Updated Current Mode/Phase/Workflow/Objective for ESR-0026's open state and WP1 completion. |
| 2.43 | 17 July 2026 | Claude Engineering Implementer | ESR-0025 formally closed (17 July 2026). Authored [[ESR-0025_ENGINEERING_SESSION_REPORT|ESR-0025]] Engineering Session Report v1.0 covering WP1 (EBG-0060/EBG-0057 overlap resolution, EBG-0057 bridge implementation and three-round hardening), session activities beyond WP1 (Ollama investigation/EIP-ESR0025-002 draft carried forward, desktop launcher EBG-0078, backlog registrations EBG-0076/EBG-0077), and session-wide WP6 (Pass)/WP7 (Accept, RBL-0015 retained). Updated Current Mode/Phase/Workflow/Objective (ESR-0025 closed, no session currently open), Current Engineering Focus (full session summary, ESR-0024 remains the two-deep Prior Session window), Section 6 Completed Milestones (6 new closure rows), Section 8 Active/Next Planned Work (Current Engineering Session Closed, Next Required Activity retargeted to opening a new session), Session Start Guidance (items 2/4/7 and closing line retargeted to ESR-0025/RBL-0015 WP7) and OSE Relationships (ESR-0025 added as prior closed session). |
| 2.42 | 17 July 2026 | Claude Engineering Implementer | ESR-0025 session-wide WP6 (Independent Repository Verification) and WP7 (Repository Baseline Acceptance) both closed against the diff through `b803996`: Engineering Reviewer (Codex) confirmed repository state, diff scope, and the fix of both a scope-leak question (`scripts/start-jarvis.bat`, resolved via EBG-0078) and a malformed EBR-0001 version-history row - by reading the full commit diff directly after its own sandbox/shell failed. One wording finding (Sections 7/8 of the WP6 handover overstated "clean" without qualifying the handover document's own untracked status) addressed. Both independent baseline views (Engineering Reviewer, Engineering Implementer) converged on retaining RBL-0015; Programme Sponsor's own WP7 determination: **Accept - retain RBL-0015**. See [[ESR-0025_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0025 WP6 handover]] v0.5 for full detail. Updated Current Mode/Baseline, Current Engineering Focus review state and Section 8 Current Review State/Next Required Activity. Session remains open - continuing or closing ESR-0025 is a separate, not-yet-taken decision. |
| 2.41 | 17 July 2026 | Claude Engineering Implementer | ESR-0025 WP1 hardened further: a third Engineering Reviewer (Codex) post-implementation review found one Medium (TOCTOU) finding - `submit-response`'s authorisation/drift checks, preflight and evidence capture all ran before the Work Package lock was acquired, only locking for the final write - addressed at [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] v1.2 by moving the entire sequence inside the lock, matching every other command's lock-before-write discipline. Proven by a test injecting a concurrent `sponsor-decision` during evidence capture and confirming it is genuinely blocked. 237 tests total (was 236). Updated Current Mode, Current Engineering Focus, Section 9 Repository Health and Outstanding Observations throughout. ESR-0025 WP1. |
| 2.40 | 17 July 2026 | Claude Engineering Implementer | ESR-0025 WP1 hardened: Engineering Reviewer (Codex) post-implementation review of the `scripts/aiems_bridge.py` diff found one High (path-traversal via unsanitised `session`/`work_package`) and one Medium (`submit-to-review`/`submit-response` not checking validation exit codes) finding, both addressed at [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] v1.2 - identifiers now validated inside `_wp_key()`; `submit-response` hard-refuses on validation failure; `submit-to-review` stays non-blocking but its evidence carries an unmissable `VALIDATION: PASSED`/`FAILED` marker. 25 new tests (237 total, was 227). Updated Current Mode, Current Engineering Focus, Completed Milestones, Section 9 Repository Health and Outstanding Observations test counts/EIP version references throughout. ESR-0025 WP1. |
| 2.39 | 17 July 2026 | Claude Engineering Implementer | ESR-0025 opened, WP1 delivered: resolved the JRM-0001-flagged EBG-0060/EBG-0057 overlap (`fdb82f7`) and implemented EBG-0057 (Claude<->Codex Engineering Bridge MVP) per [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] v1.0 (Engineering Reviewer/Codex reviewed - one High, one Medium finding on v0.1 addressed at v0.2 - Programme Sponsor approved). Updated Current Mode/Phase/Workflow/Objective (ESR-0025 open, RBL-0015 unchanged pending its own WP7), Current Engineering Focus (ESR-0025 WP1 summary, ESR-0024 demoted to Prior Session), Completed Milestones (1 new row), Section 8 Active/Next Planned Work (JRM-0001 version corrected to v1.13), Section 9 Repository Health (227/227 tests, 104 warnings), Section 10 Outstanding Observations (EBG-0057 bullet updated from discussion to implemented), Session Start Guidance (items 4/7 and closing line retargeted) and OSE Relationships (ESR-0025 added as current, ESR-0024 demoted to prior). ESR-0025 WP1. |
| 2.38 | 17 July 2026 | Claude Engineering Implementer | ESR-0024 formally closed (17 July 2026). Updated Current Mode/Baseline/Phase/Workflow/Objective (RBL-0015 retained, ESR-0024 closed, EBG-0057 recorded as the Programme Sponsor's stated next-session candidate and judged a separate AIEMS/tooling workstream from JRM-0001's product tracks), Current Engineering Focus (full WP1-WP2 and session-wide WP6/WP7 summary, ESR-0023 demoted to Prior Session, ESR-0021's paragraph-level detail remains dropped from the two-deep window), Completed Milestones (3 new closure rows), Section 8 Active/Next Planned Work, Section 9 Repository Health, Section 10 Outstanding Observations (3 new entries: EBG-0074 closure, WP2 Incremental Visual Convergence delivery, the EBG-0057 workstream-categorisation discussion and rough workload estimate), Session Start Guidance (retargeted to ESR-0024 as Current ESR tier, item 7 connected to EBG-0057's role-locked-permissions rationale) and OSE Relationships (ESR-0024 now closed). ESR-0024 session-wide WP7. |
| 2.37 | 17 July 2026 | Claude Engineering Implementer | ESR-0024 WP2 delivered: PBK-0001's Incremental Visual Convergence practice satisfied via [[EIP-ESR0024-002_SYSTEM_HEALTH_POLICY_ENGINE_DETAIL|EIP-ESR0024-002]] v1.0 (Engineering Reviewer/Codex reviewed - no blocking findings - Programme Sponsor approved): System Health panel's Sentinel row now names the live policy engine (e.g. "Trust gateway active (TrustTierPolicy)"), using only real data WP1 itself produced. Updated Current Mode, Section 8 (Current Engineering Session, ESR-0024 Delivered Scope), Completed Milestones (1 new row). 212 tests pass (was 211), validator clean, `npm run build` clean; verified via a Playwright check against the real Vite dev server across connecting/offline/running states, zero console errors. ESR-0024 WP2. |
| 2.36 | 17 July 2026 | Claude Engineering Implementer | ESR-0024 opened, WP1 delivered: EBG-0074 (Wire TrustTierPolicy as SentinelCore's Production Default) resolved per [[EIP-ESR0024-001_TRUSTTIERPOLICY_PRODUCTION_WIRING|EIP-ESR0024-001]] v1.0 (Engineering Reviewer/Codex reviewed - two Medium findings on v0.1 addressed at v0.2 - Programme Sponsor approved). Updated Current Mode/Baseline/Phase/Workflow/Objective (ESR-0024 open, RBL-0015 unchanged pending its own WP7), Current Engineering Focus (ESR-0024 WP1 summary, ESR-0023 demoted to Prior Session, ESR-0021's detailed paragraph dropped to keep the two-deep window), Completed Milestones (1 new row), Section 8 Active/Next Planned Work (JRM-0001 version corrected to v1.11, Authoritative Backlog Source updated for EBG-0074), Section 9 Repository Health (211/211 tests; corrected the stale 85-warning count to the confirmed-actual 103, verified unrelated to this session's changes via a stash comparison against `main`), Section 10 Outstanding Observations (EBG-0074 bullet updated from gap to resolved), Session Start Guidance (items 4/5/7 and closing line retargeted to ESR-0024/JRM-0001 v1.11/EBG-0019-leads-Near-term) and OSE Relationships (ESR-0024 added as current, ESR-0023 added as prior). ESR-0024 WP1. |
| 2.35 | 17 July 2026 | Claude Engineering Implementer | ESR-0023 formally closed (17 July 2026). Updated Current Mode/Baseline/Phase/Workflow/Objective (RBL-0015 retained, ESR-0023 closed), Current Engineering Focus (full WP1-WP6 and session-wide WP6/WP7 summary, ESR-0022 demoted to Prior Session, ESR-0020 dropped from the two-deep window), Completed Milestones (9 new closure rows), Section 8 Active/Next Planned Work (Current Roadmap version corrected to v1.10, Authoritative Backlog Source updated for all 7 closures plus EBG-0074), Section 9 Repository Health, Section 10 Outstanding Observations (5 new entries: Guardian cluster closure, the TrustTierPolicy wiring gap, the write-boundary deviation and fix, gh CLI installation, remaining ungated architecture gaps) and Session Start Guidance (fully retargeted to ESR-0023/RBL-0015/JRM-0001 v1.10, EBG-0074 leading Near-term, new item 14 on Reviewer tool-permission verification). ESR-0023 session-wide WP7. |

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.34 | 16 July 2026 | Claude Engineering Implementer | ESR-0022 formally closed (16 July 2026). Updated Current Mode/Baseline/Phase/Workflow/Objective (RBL-0015 accepted, ESR-0022 closed), Current Engineering Focus (WP1/WP6/WP7 full summary, ESR-0021 demoted to Prior Session), Section 8 Active/Next Planned Work (Current Roadmap version corrected to v1.4, Authoritative Backlog Source updated for EBG-0073), Completed Milestones (1 new closure row), Session Start Guidance (fully retargeted to ESR-0022/RBL-0015/JRM-0001 v1.4, EBG-0073 flagged) and OSE Relationships (ESR-0022 added as current, ESR-0021 demoted to prior). ESR-0022 session-wide WP7. |
| 2.33 | 16 July 2026 | Claude Engineering Implementer | ESR-0022 WP6/WP7: Engineering Reviewer WP6 Pass; Programme Sponsor WP7 determination to establish a new baseline (RBL-0015) rather than retain RBL-0014, judging production provider wiring a materially new operational capability. Updated Current Mode/Baseline, Section 8 Active/Next Planned Work, Section 9 Repository Health, Completed Milestones (3 new rows), Session Start Guidance item 2, and OSE Relationships to reference RBL-0015. Session Start Guidance items 5-10 remain targeted at ESR-0021, not yet retargeted since ESR-0022 has not closed. ESR-0022 WP6/WP7. |
| 2.32 | 16 July 2026 | Claude Engineering Implementer | ESR-0022 WP1 implemented and delivered following Engineering Reviewer and Programme Sponsor approval of EIP-ESR0022-001 v1.0: EBG-0070 (production provider wiring) and EBG-0072 (System Health panel) marked Complete. Updated Current Mode, Current Engineering Focus, Section 5 Sentinel/UXP rows, Section 8 and Section 9 Repository Health (209/209 tests, full validator 0 errors/85 warnings). ESR-0022 WP1. |
| 2.31 | 16 July 2026 | Claude Engineering Implementer | Following an Engineering Reviewer High finding on EIP-ESR0022-001 v0.1 (a retroactive package cannot be genuinely approved), fully reverted the premature implementation (nothing was ever committed) and reworded Current Mode, Current Engineering Focus, Section 5 Sentinel/UXP rows and Section 8 throughout: EBG-0070/EBG-0072 now `Approved Backlog` (not `In Progress`), described as a genuine prospective proposal via EIP-ESR0022-001 v0.2 with no code written, incorporating the Reviewer's Medium finding (blank model env var handling) directly into the design. ESR-0022 WP1. |
| 2.30 | 16 July 2026 | Claude Engineering Implementer | ESR-0022 opened, WP1 proposed (EBG-0070 production provider wiring, EBG-0072 System Health panel, selected via JRM-0001 horizon guidance). **Self-disclosed process deviation, corrected same-day**: both were drafted and locally tested before an Engineering Implementation Package existed - reworded throughout (Current Mode, Current Engineering Focus, Section 5 Sentinel/UXP rows, Section 8) from "delivered/Complete" to "proposed/In Progress, pending Engineering Reviewer review" of [[EIP-ESR0022-001_PROVIDER_WIRING_AND_SYSTEM_HEALTH_PANEL|EIP-ESR0022-001]], drafted retroactively for that review. Nothing committed or pushed. ESR-0022 WP1. |
| 2.29 | 15 July 2026 | Claude Engineering Implementer | ESR-0021 formally closed (15 July 2026). Updated Current Mode/Baseline/Roadmap/Phase/Workflow/Objective (RBL-0014 retained, JRM-0001 v1.0 approved), Current Engineering Focus (WP1-WP7 summary, ESR-0020 demoted to Prior Session), Completed Milestones (7 new ESR-0021 rows), Active/Next Planned Work (EAC/GDP-0001/EBG-0057 observations updated to reflect the WP6 historical audit's EBG-0059/EBG-0060 discoveries), Repository Health, Outstanding Observations (JRM-0001, historical audit, Capability Readiness Matrix refresh), Session Start Guidance (retargeted to ESR-0021/JRM-0001, Codex-venue clarification) and OSE Relationships retargeted from ESR-0020/RBL-0014 to ESR-0021/RBL-0014-retained. |
| 2.28 | 15 July 2026 | Claude Engineering Implementer | Updated the JARVIS Capability Maturity row (Section 5) following ESR-0021 WP7's refresh of JARVIS_CAPABILITY_READINESS_MATRIX.md (v2.0, closing EBG-0069): no longer stale, Guardian/Sentinel/Platform Services/UXP/Knowledge/Provider Architecture correctly shown as Implemented (Foundation). ESR-0021 WP7. |
| 2.27 | 13 July 2026 | Claude Engineering Implementer | ESR-0020 formally closed (13 July 2026). Updated Current Mode/Baseline/Product Baseline/Phase/Workflow/Objective (RBL-0014 retained, PCB-0001 v2.1 accepted), Current Engineering Focus (WP1-WP6 summary, ESR-0019 demoted to Prior Session), Sentinel/JARVIS Product Capability Baseline capability rows (Gemini live-validated, PCB-0001 no longer stale), Completed Milestones (8 new ESR-0020 rows), Active/Next Planned Work, Repository Health (204/204 tests), Outstanding Observations (PBK-0001/COC-0001 Draft to Approved, Gemini live-validated), Session Start Guidance (added explicit implementation-follows-review note per Sections 9A/9B) and OSE Relationships retargeted from ESR-0019/RBL-0014-accepted to ESR-0020/RBL-0014-retained. |
| 2.26 | 11 July 2026 | Claude Engineering Implementer | ESR-0019 formally closed (11 July 2026), the first full session under the permanent Lead/Reviewer appointment. Updated Current Mode/Baseline/Phase/Workflow/Objective (RBL-0014 accepted, superseding RBL-0013), Current Engineering Focus (WP1 role-binding, WP2 Guardian Orb knowledge-graph delivery, ESR-0018 demoted to Prior Session), Guardian Experience/UXP/JARVIS Development capability rows (Guardian Orb Phase 1 delivered), Completed Milestones (6 new ESR-0019 rows), Active/Next Planned Work, Repository Health (204/204 tests), Outstanding Observations (PBK-0001/COC-0001 role-binding actioned not flagged, Guardian Orb Phase 1 delivered, new Incremental Visual Convergence practice, Vite/Tauri scaffolding fix), Session Start Guidance and OSE Relationships retargeted from ESR-0018/RBL-0013 to ESR-0019/RBL-0014. |
| 2.25 | 10 July 2026 | Claude Engineering Reviewer | ESR-0018 formally closed (10 July 2026). Updated Current Mode/Phase/Workflow/Objective, Current Engineering Focus (ESR-0018 WP0 incident chain and WP1/WP2 outcomes, ESR-0017 detail retained as prior-session history), Sentinel/Gemini capability row (EBG-0051 hardening, live smoke test still pending), Completed Milestones (6 new ESR-0018 rows), Active/Next Planned Work, Repository Health (192/192 tests), Outstanding Observations (EE-0001 trial concluded - Claude permanent Lead Engineer, ChatGPT permanent Lead Reviewer; Claude<->Codex bridge EBG-0057 recorded), Session Start Guidance and OSE Relationships retargeted from ESR-0017/rotation-confirmation to ESR-0018/permanent-appointment confirmation. |
| 2.24 | 10 July 2026 | Claude Engineering Lead | ESR-0017 formally closed (10 July 2026). Updated Current Mode, Current Repository Baseline (RBL-0013, superseding RBL-0012), Current Product Capability Baseline (flagged stale, EBG-0056), Current Phase/Workflow/Objective, Section 4A narrative (full closure summary including WP8/WP9/post-WP9 work and the two Sponsor closure-scope decisions), UXP/Sentinel/JARVIS Development capability rows (UXP now live, not disconnected), Completed Milestones (9 new ESR-0017 rows), Active/Next Planned Work, Repository Health (184/184 tests), Outstanding Observations (Guardian-Sentinel connection delivered, Gemini implemented, three EE-0001 sessions closed, Guardian Orb unblocked in principle), Session Start Guidance and OSE Relationships (both retargeted from ESR-0016/RBL-0011 to ESR-0017/RBL-0013 as the current onboarding tier for ESR-0018). |
| 2.23 | 9 July 2026 | Claude Engineering Lead | Recorded RBL-0012 acceptance (superseding RBL-0011) and ESR-0017 in-progress state: WP1-WP4 complete and reviewed, WP6/WP7 complete, WP8/WP9 pending Programme Sponsor scope definition. Current Mode correctly retained as ESR-0016 (latest closed session) per WP0B, with ESR-0017 progress described separately in the same field. Updated Sections 3, 4A, 5 (Sentinel/UXP/JARVIS Development rows), 8 and 9. |
| 2.22 | 9 July 2026 | Claude Engineering Reviewer | Recorded ESR-0016 closure: Sentinel trust-tier policy model and architecture alignment delivered and independently verified under the EE-0001 trial's reversed rotation (ChatGPT Lead, Claude Reviewer). Retained RBL-0011 (no new baseline). Added Section 21 ESR-0016 Outcomes; renumbered Session Start Guidance/Maintenance to 22/23; updated Current State, Capability Roadmap, Milestones, Active Work, Repository Health, Outstanding Observations and Related Artefacts for ESR-0017 (Cold Start Validation Session, Claude leads) readiness. |
| 2.21 | 8 July 2026 | Claude Engineering Implementer | Recorded Programme Sponsor acceptance of RBL-0011 as the current repository baseline, superseding RBL-0010. Updated Current State, Active Work, Repository Health, Session Start Guidance and Related Artefacts accordingly. |
| 2.20 | 8 July 2026 | Claude Engineering Implementer | Recorded ESR-0015 closure: Sentinel execution pipeline delivered and proven with a live conversation. Added ESR-0015 Outcomes section, updated Session Start Guidance to Current ESR-0015, recorded RBL-0011 recommendation (Programme Sponsor acceptance pending) and ESR-0016 entry (ChatGPT leads per EE-0001). |
| 2.19 | 8 July 2026 | Claude Engineering Implementer | Recorded ESR-0015 opening under the EE-0001 Lead/Reviewer trial: Current Mode, Phase, Objective, Active Work and Repository Health updated to reflect the session and its WP1-WP6 work package plan. |
| 2.18 | 8 July 2026 | Claude Engineering Implementer | Removed residual ChatGPT product-naming from Outstanding Observations (aligned with Engineering Reviewer/Engineering Implementer terminology); extended Session Start Guidance to explicitly cover README.md and Active Standards, fully mirroring GDE-0001's tier list. |
| 2.17 | 8 July 2026 | Claude Engineering Implementer | Recorded ESR-0014 closure (Sentinel AI Execution and Security Platform implemented, ADR-0018 approved) and ESR-0014A closure (GDE-0001 knowledge tiering); removed stale "Sentinel implementation remains deferred" observation; retained RBL-0010 baseline position. |
| 2.16 | 7 July 2026 | Engineering Agent | Updated programme status for ESR-0013 Guardian Platform Foundation closure review, deferred capability status and retained RBL-0010 baseline position. |
| 2.15 | 6 July 2026 | Codex Engineering Implementer | Recorded ESR-0012 closure, GIA-BOOT Proof of Concept completion, AIEMS Engineering Agent validation, deferred work and retained RBL-0010 as the current accepted repository baseline. |
| 2.14 | 5 July 2026 | Codex Engineering Implementer | Recorded ESR-0011 closure, Architecture Validation and Implementation Readiness outcomes, ESR-0012 implementation handover and retained RBL-0010 as the current accepted repository baseline. |
| 2.13 | 4 July 2026 | Codex Engineering Implementer | Recorded ESR-0010 closure, Engineering Ecosystem Modernisation outcomes, accepted repository review state and next-session handover guidance. |
| 2.12 | 3 July 2026 | Codex Engineering Implementer | Recorded RBL-0010 acceptance as the ESR-0009 repository baseline and updated ESR-0010 handover state. |
| 2.11 | 3 July 2026 | Codex Engineering Implementer | Updated programme status for ESR-0009 closure, ESR-0010 approval, Guardian Desktop Platform Shell, TPL-0001, SAM-0001, UAM-0001 and Guardian Experience v1.0. |
| 2.10 | 2 July 2026 | Codex Engineering Implementer | Added retrospective OSE relationships to improve semantic traceability without changing programme status. |
| 2.9 | 2 July 2026 | Codex Engineering Implementer | Aligned related artefact wording following OSE repository pass for ESR-0009 readiness. |
| 2.8 | 2 July 2026 | Codex Engineering Implementer | Recorded completion of EBG-0039 JARVIS Runtime Chat Archive and movement of prototype chat exports into `logs/chats/`. |
| 2.7 | 2 July 2026 | Codex Engineering Implementer | Recorded ESR-0008 baseline acceptance through RBL-0009 and updated ESR-0009 handover guidance. |
| 2.6 | 2 July 2026 | Codex Engineering Implementer | Recorded ESR-0008 closure, Guardian identity, JARVIS Platform architecture, Engineering Ecosystem Synchronisation and ESR-0009 readiness. |
| 2.5 | 1 July 2026 | Codex Engineering Implementer | Recorded ESR-0007 closure, RBL-0008 acceptance, PCB-0001 acceptance, RPCA-0001 completion, repository-first working practices and ESR-0008 readiness. |
| 2.4 | 1 July 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0006 outcomes, RBL-0007 accepted baseline, validated working practices and ESR-0007 product engineering handover position. |
| 2.3 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0005 closure, RBL-0006 accepted baseline and ESR-0006 planning readiness. |
| 2.2 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Corrected authority lifecycle diagram so Programme Sponsor Validation occurs before Engineering Implementer commit and push. |
| 2.1 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Clarified current workflow distinction between engineering approval, validation, independent verification and Programme Sponsor baseline acceptance. |
| 2.0 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added ESR-0005 opening objectives and success criteria for engineering readiness. |
| 1.9 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded RBL-0004 accepted ESR-0004 repository baseline and ESR-0005 readiness. |
| 1.8 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded RBA-0001 ESR-0004 repository baseline assessment and ESR-0005 handover recommendation. |
| 1.7 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded STD-0004 Validation and Quality Assurance Standard as approved. |
| 1.6 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added README.md as the first WP0 review artefact before controlled governance artefacts. |
| 1.5 | 28 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0003 closure and repository baseline acceptance for ESR-0004. |
| 1.4 | 28 June 2026 | Programme Sponsor & Chief Engineering Advisor | Refreshed programme status following ESR-0003 completion, repository lifecycle alignment, ADR recovery and EBR-0002 baseline review. |
| 1.3 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded AIEMS Execution Mode default behaviour, temporary context switching and live workflow change control. |
| 1.2 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded final ESR-0002 closure wording and Engineering Session Archive reference position. |
| 1.1 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded ESR-0002 closure, repository health outcome, ESR-0003 handover and next recommended activity. |
| 1.0 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Programme Status artefact created to preserve session continuity and reduce dependency on long conversation history. |
