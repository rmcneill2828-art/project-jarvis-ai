# PST-0001 - Programme Status

> *"A programme moves faster when its current state is clear, trusted and easy to reload."*

**Version:** 2.25

---

# Document Control

| Field | Value |
|-------|-------|
| Artefact ID | PST-0001 |
| Title | Programme Status |
| Version | 2.25 |
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
| Current Mode | [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] is the latest **closed** session (10 July 2026). EBG-0051 (Gemini Provider Production Readiness) delivered and independently verified; the EE-0001 Lead/Reviewer trial concluded with a permanent appointment. |
| Current Repository Baseline | [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] retained at ESR-0018 closure - ESR-0018's changes judged incremental, not warranting a new baseline, per the ESR-0016 precedent. |
| Current Product Capability Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] accepted as current operational JARVIS product baseline - **flagged materially stale at RBL-0013** (still states "Guardian capability is not implemented," describes only the Tkinter GUI). Not yet refreshed; tracked as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0056. |
| Repository Product Capability Assessment | [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] completed and accepted. |
| Current Phase | ESR-0018 closed. The [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Lead/Reviewer trial has concluded (Section 7): Claude appointed permanent Lead Engineer, ChatGPT permanent Lead Reviewer, replacing the frozen four-session alternating rotation. Ready for a new engineering session under the standing appointment. |
| Current Workflow | AIEMS Engineering Workflow v3 with Engineering Ecosystem Synchronisation working practice. The EE-0001 Lead/Reviewer trial (ESR-0015 through ESR-0018) is closed; its outcome - permanent role specialisation rather than continued alternation - is now the standing operating model, pending `PBK-0001`/`COC-0001` updates to reflect it explicitly (flagged, not yet actioned). |
| Current Engineering Objective | ESR-0018 closed. No next-session objective is created by this status update - opening the next session is a separate action. |

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

[[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] is **Closed** (10 July 2026), the fourth and final Engineering Session run under the [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Lead/Reviewer trial and its designated decision-point session. ChatGPT as Engineering Lead, Claude as Independent Reviewer, Programme Sponsor gating every step. WP0 (session opening) recorded a significant, extended incident: the Engineering Lead repeatedly asserted the GitHub connector was unavailable without attempting to invoke it, including a distinct new sub-pattern ("confession as substitute for compliance" - accurate self-diagnosis produced instead of, not converting into, the required action) - resolved only after an explicit, action-forcing Programme Sponsor instruction, after which WP0 completed accurately. WP1 delivered [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0051 (Gemini Provider Production Readiness) cleanly, independently verified at 192/192 tests with zero regressions. WP2 resolved ESR-0017's outstanding EE-0001 scorecard acceptance and carried the trial to its Section 7 decision point.

At that decision point, the Programme Sponsor posed the same question independently to both AIs - given four sessions of recorded evidence, who should be permanently appointed Lead Engineer and who Lead Reviewer - without either seeing the other's answer. Both converged on the identical assignment. **The Programme Sponsor made this appointment formal on 10 July 2026: Claude as permanent Lead Engineer, ChatGPT as permanent Lead Reviewer**, replacing the trial's frozen four-session alternating rotation. Full detail, including both AIs' answers verbatim, is in [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Sections 7-7.3 and [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] Section 15.

A subsequent, explicitly out-of-scope exercise of the new roles (a Claude&harr;Codex engineering-communication bridge, discussed after appointment) produced a reconciled architecture and cost decision - recorded as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0057 for a future ESR, not built within ESR-0018. `PBK-0001` and `COC-0001` still describe Engineering Implementer/Reviewer as generic, session-assignable roles rather than bound to a specific AI - flagged as outstanding following the permanent appointment, not yet actioned.

---

## Prior Session: ESR-0017

[[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] is **Closed** (10 July 2026). This was the third Engineering Session run under the EE-0001 Lead/Reviewer trial, and the designated **Cold Start Validation Session** (EE-0001 Section 3.4): Claude as Engineering Lead, ChatGPT as Independent Reviewer, Programme Sponsor gating every step, the session begun in a fresh conversation using only README.md, PST-0001, the Current ESR and referenced artefacts - the first empirical proof in the trial that a fresh AI Lead can onboard from repository documentation alone (verified **&check;**).

ESR-0017 delivered nine Work Packages, each independently reviewed. **WP1-WP4** (0 Blocking, 0 Major findings across all four, 10 Minor/Observation-severity findings, all accepted): WP1 decided the UXP-to-backend integration architecture ([[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] - Tauri sidecar-managed Python process, duplex stdio JSON-RPC); WP2 connected `GuardianRuntime` through Sentinel for the first time; WP3 added a second external Sentinel provider adapter (`GeminiProvider`); WP4 produced a five-session backlog progression roadmap. **WP6/WP7** completed mid-session ([[RBL-0012_REPOSITORY_BASELINE|RBL-0012]] accepted), then **refreshed at closure** after WP8/WP9 landed - see below. **WP8** added PBK-0001's Feature-First Delivery Discipline (minimise controlled artefact creation; every session delivers product-moving work and demonstrable UXP progress). **WP9** delivered the first genuinely interactive UXP in the project's history: a JSON-RPC 2.0 stdio bridge (`jarvis/interfaces/stdio_rpc.py`), Tauri sidecar process management (`src-tauri/src/lib.rs`), and live React frontend wiring (`src/App.jsx`) - verified end-to-end through a real running windowed desktop session with a live Guardian conversation, not only through tests. ChatGPT Engineering Reviewer approved WP9 with 4 Minor findings (2 fixed immediately, 2 deliberately deferred).

Substantial work followed WP9, all recorded in the session report's Sections 15.2-15.7: automated dev-environment setup tooling (`setup.bat`); recovery of a previously-approved-but-never-merged Guardian Orb knowledge-graph design direction (from ESR-0010/FCH-0010) into [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] (now v1.5), including the actual reference mock-up image and a corrected scale assessment (~135 real repository artefacts, not the mock-up's illustrated thousands); a revision to the WP4 five-session roadmap recording that EBG-0050 (the UXP-backend bridge) completed two sessions early, freeing capacity for a new EBG-0055 (Knowledge Graph Phase 1).

At closure, the Programme Sponsor made two explicit scope decisions: (1) refresh the repository baseline, since RBL-0012 had named WP8/WP9 as its own trigger for reconsideration - actioned as a WP6/WP7 refresh, resulting in [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] (Accepted by ChatGPT Engineering Reviewer with one non-blocking discrepancy, then by the Programme Sponsor); (2) **not** expand the EE-0001 trial scorecard beyond its existing WP1-WP4 scope - that entry (see [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 9) stands as the final ESR-0017 trial record, recording the Lead's draft self-assessment reviewed and refined by the Engineering Reviewer, who substantially agreed and contributed four refinements plus two new joint recommendations for future EE-0001/PBK-0001 changes (EBG-0052, EBG-0053) - neither adopted, both logged as candidates. The adopt/reject/modify decision on the Lead/Reviewer rotation itself remains reserved for ESR-0018 closure per EE-0001 Section 7.

RBL-0013 flagged [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] as materially stale (still states Guardian capability is not implemented, describes only the Tkinter GUI) rather than silently carrying it forward - tracked as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0056, not refreshed by this session.

PST-0001 records the ESR-0018 closed state and the concluded EE-0001 trial appointment. It does not create a new engineering session, or approve implementation outside separately authorised engineering work.

---

# 5. Current Capability Roadmap

| Capability | Status | Maturity | Notes |
|------------|--------|----------|-------|
| Repository Architecture | Complete | Complete | Repository structure, package layout and governance separation are established. |
| Governance Framework | In Progress | High | Core AIEMS governance artefacts support controlled product delivery and are ready to be tested through implementation-led engineering. |
| Engineering Standards | In Progress | High | Approved standards remain in place; RFEP, RFDP and Continuous Repository Synchronisation are working practices pending any future standards review. |
| JARVIS Product Architecture | Complete | High | [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] remains the product architecture authority. |
| JARVIS Platform Architecture | Draft | High | [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] validated JARVIS Platform, Sentinel, Platform Services, UXP, Provider Architecture, Agent Framework and GIA positioning for implementation readiness. |
| Sentinel AI Execution and Security Platform | Implemented | High | [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] positions Sentinel as the AI Execution and Security Platform; Sentinel Core, provider abstraction, local/OpenAI/Gemini providers, health-aware provider orchestration with failover, audit, policy and a trust-tier policy model are implemented under `sentinel/`, now reachable through the live UXP via `GuardianRuntime` (192 passing tests repository-wide). Gemini's response parsing hardened at ESR-0018 (EBG-0051: distinguishable safety-block/tool-response errors, multi-part text, string-serialised metadata) but remains unwired by default - the required Sponsor-run live smoke test against the real API has not yet been performed. |
| Guardian Cognitive Architecture | Draft | High | [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] records Guardian identity and cognitive architecture; ESR-0013 established a bounded runtime foundation without implementing full Guardian cognition. |
| Guardian Experience Architecture | Approved Baseline | High | [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] records Guardian Experience Architecture v1.0; [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] confirms Guardian Orb should consume real observable state. |
| Engineering Ecosystem Architecture | Implementation Validated | High | [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] records Obsidian/OSE and Engineering Ecosystem Synchronisation; ESR-0012 validated AIEMS operationally through implementation. |
| Guardian Instrumentation Agent | Proof of Concept Complete | Early | [[ESR-0012_ENGINEERING_SESSION_REPORT|ESR-0012]] completed GIA-BOOT as a Proof of Concept; further GIA implementation is deferred. |
| User Experience Platform | Live, Foundation Scope | Foundation | [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]] records Tauri + React as the UXP direction; [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] decided the backend bridge pattern; ESR-0017 WP9 **implemented and verified it live** - the UXP is no longer a disconnected static shell. The chat input is enabled and calls the real backend; capability/diagnostics panels derive from live `platform.status` data. Streaming notifications, production sidecar packaging and the Guardian Orb knowledge-graph vision ([[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] 8.1-8.3) remain not yet implemented (EBG-0050 remaining scope, EBG-0055). |
| JARVIS Product Capability Baseline | Accepted, Stale | Foundation | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] records the accepted operational product baseline, but is materially stale after ESR-0017 - flagged at [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]], tracked as EBG-0056. |
| JARVIS Capability Maturity | Maintained, Stale | Early | [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] remains the nominal authoritative maturity model but pre-dates WP2/WP9 (noted at ESR-0017 Section 15.3, not yet refreshed). |
| JARVIS Development | In Progress | Early | Guardian Desktop Platform Shell, Guardian Experience v1.0, GIA-BOOT Proof of Concept, Guardian Runtime Foundation, Guardian&harr;Sentinel connection (ESR-0017 WP2) and the UXP-backend bridge (ESR-0017 WP9) exist. **Guardian is now reachable through the running UXP** - verified via a real windowed session - though this remains outside PCB-0001's still-unrefreshed accepted operational baseline (EBG-0056). |
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

---

# 7. Current Engineering Standards Position

Approved standards remain current. ESR-0007 methodology outcomes are working practices only and shall not be treated as standards unless promoted through future approved standards review.

---

# 8. Active and Next Planned Work

| Item | Status | Notes |
|------|--------|-------|
| Current Engineering Session | [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] - **Closed** (10 July 2026) | WP1 (EBG-0051) and WP2 (EE-0001 Review) complete and reviewed. |
| Current Repository Baseline | [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] | Retained at ESR-0018 closure - incremental change, no new baseline warranted, per the ESR-0016 precedent. |
| Current Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational JARVIS product baseline - flagged materially stale at RBL-0013 (EBG-0056), not refreshed. |
| Current Review State | ESR-0018 fully reviewed and closed | Gemini provider production-readiness hardening (WP1), ESR-0017 scorecard acceptance and EE-0001 Section 7 decision (WP2) - all independently verified. |
| Next Required Activity | Open the next engineering session | Under the permanent Lead/Reviewer appointment (Claude Lead Engineer, ChatGPT Lead Reviewer) - the EE-0001 rotation no longer applies. Not opened by this status update. |
| Next Engineering Session | Not created by this status update | Opening the next session is a separate action. |
| ESR-0018 Delivered Scope (WP0-WP2) | Gemini provider production-readiness hardening (EBG-0051), ESR-0017 scorecard acceptance, EE-0001 Section 5.12 criterion adoption, the EE-0001 Section 7 decision and permanent appointment | Complete and reviewed. |
| GIA-BOOT Proof of Concept | Complete | Accepted as Proof of Concept; further GIA implementation deferred - blocks Knowledge Graph Phases 3-4 (EBG-0055 note). |
| Deferred Work | Recorded | Guardian Memory, Conversation Engine expansion, Guardian Developer Console, full Guardian Orb knowledge-graph rendering (Phases 2-4, [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0055), Automation, persistent storage, EAC and GDP-0001 implementation remain deferred. Gemini's response parsing is hardened (EBG-0051, ESR-0018) but still unwired and unvalidated against the real API. Anthropic/OpenRouter/Ollama provider adapters approved in principle (PEM-001) but not yet implemented. Claude&harr;Codex engineering bridge (EBG-0057) architecture and cost decided, not implemented. |
| Authoritative Backlog Source | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Future engineering priorities remain governed by the backlog register; EBG-0053 adopted and EBG-0057 added at ESR-0018. |
| Runtime Evidence Archive | `logs/chats/` | Prototype JARVIS chat exports remain archived under runtime evidence archive. |

---

# 9. Repository Health

| Item | Status |
|------|--------|
| Repository Health | Good |
| Repository Acceptance | Accepted through [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] |
| Current Repository Baseline | [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] |
| Product Capability Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - stale, flagged at RBL-0013 (EBG-0056) |
| Latest Repository Product Capability Assessment | [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] |
| Current Activity | ESR-0018 closed 10 July 2026; WP1 and WP2 complete, reviewed, RBL-0013 retained. 192/192 tests passing, 0 validator errors. EE-0001 trial concluded with permanent appointment. Ready for the next engineering session. |

---

# 10. Outstanding Observations

The following observations remain open for future engineering consideration:

- [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] (accepted ESR-0015, retained through ESR-0016) was superseded by [[RBL-0012_REPOSITORY_BASELINE|RBL-0012]] mid-ESR-0017, in turn superseded by [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] at ESR-0017 closure - both historical now, kept for baseline lineage.
- [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] established the Guardian Platform Foundation through runtime boundary, lifecycle integration, status snapshot and observability work.
- [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] is closed. [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] positions Sentinel as the AI Execution and Security Platform. Sentinel Core, provider abstraction, local provider, provider configuration, provider orchestration, audit, policy and (since ESR-0016) a trust-tier policy model are implemented under `sentinel/` with 144 passing tests.
- [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] is closed. [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] introduces knowledge tiering for Engineering Session initialisation.
- Guardian Runtime **is now connected through Sentinel** (`GuardianRuntime.converse()`, ESR-0017 WP2) and reachable through the live UXP (ESR-0017 WP9) - the candidate focus per ESR-0016 Section 16 is delivered.
- PEM-001 provider scoring is complete (ESR-0015): Primary OpenAI (implemented), Secondary Gemini (implemented, response parsing hardened at ESR-0018 - EBG-0051, still unwired and unvalidated against the real API pending the required Sponsor-run live smoke test), reasoning/coding comparison Anthropic, Gateway OpenRouter, local fallback Ollama - the latter three remain not implemented.
- [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]], [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]], [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] and [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] are all closed. **The EE-0001 Lead/Reviewer trial is concluded** (all four sessions run: Claude led ESR-0015/ESR-0017, ChatGPT led ESR-0016/ESR-0018; Sponsor arbitration required was assessed Low, High, Low-Medium and High respectively). At the Section 7 decision point, both AIs independently converged on the same recommendation without sight of each other's answers; the Programme Sponsor made it formal on 10 July 2026: **Claude permanent Lead Engineer, ChatGPT permanent Lead Reviewer**, replacing the alternating rotation. `PBK-0001`/`COC-0001` still describe the roles generically rather than bound to a specific AI - flagged, not yet actioned.
- ESR-0018 recorded the trial's longest capability-self-assessment incident, including a new named sub-pattern ("confession as substitute for compliance" - accurate self-diagnosis produced instead of the required action) - resolved only after an explicit, action-forcing Programme Sponsor instruction. Recorded in full in [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 9 and [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] Section 13.
- A Claude&harr;Codex engineering-communication bridge was discussed post-appointment, explicitly out of ESR-0018 scope: architecture (file-based, command-driven, Sponsor-gated handovers) and cost decision (Claude Pro unchanged; a new personal ChatGPT Plus subscription for Codex) recorded as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0057. No implementation authorised; requires its own future ESR and EIP.
- GIA-BOOT is accepted as a Proof of Concept.
- Further GIA implementation is deferred.
- AIEMS Engineering Agent is adopted to support the Engineering Reviewer role.
- Remaining Engineering Agent validation is deferred.
- Future EAC implementation is deferred.
- Guardian Memory remains deferred.
- Conversation Engine expansion remains deferred.
- Guardian Developer Console remains deferred.
- Real observable platform state now exists (ESR-0017 WP9's `platform.status`), unblocking Guardian Orb implementation in principle - the knowledge-graph Orb design itself ([[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] 8.1-8.3) remains not started; [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0055 (Phase 1) is the recommended next step.
- Automation remains deferred.
- Persistent storage remains deferred.
- GDP-0001 implementation remains deferred.
- Repository First is reinforced by ESR-0012 operational evidence.
- Look Inward Before Looking Outward is identified as an engineering principle derived from operational evidence, but is not introduced as a new AIEMS standard by this status update.
- The Engineering Reviewer and Guardian operating environments remain separated.
- Guardian Orb implementation remains deferred until real observable platform state exists.
- Resilience Before Disablement / local fallback remains accepted as an engineering direction pending implementation evidence.
- External AI providers, persistent memory, voice, vision and internet-backed assistance remain outside the accepted operational product baseline.
- RFEP, RFDP, Continuous Repository Synchronisation and Engineering Ecosystem Synchronisation may be considered in a future formal AIEMS standards review.
- Obsidian is recognised as the human-facing Engineering Knowledge Workspace for OSE while GitHub remains the source of truth.

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
2. Review [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]], the repository baseline the Programme Sponsor has accepted as current.
3. Review [[PST-0001_PROGRAMME_STATUS|PST-0001]] (Current State tier).
4. Review the Architecture tier as referenced by PST-0001 - for UXP/Guardian-experience work specifically, also review [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] (now includes the Guardian Orb knowledge-graph design direction, Sections 8.1-8.3) before touching `src/App.jsx`.
5. Review Active Standards (STD-0001 through STD-0004) where the session's work touches artefact creation or modification.
6. Review [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] (Current ESR tier) - the EE-0001 trial's concluding session; Section 13 records the WP0 incident chain and Section 15 the final trial scorecard, worth reading in full, not just the WP table.
7. Review [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
8. Review [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - includes the Feature-First Delivery Discipline (v1.19, ESR-0017 WP8); still describes Engineering Implementer/Reviewer generically and has not yet been updated to reflect the permanent appointment below.
9. Review [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] - same outstanding update as PBK-0001.
10. Review [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7 for the concluded trial's outcome - **the Lead/Reviewer rotation is retired. Claude is the permanent Lead Engineer, ChatGPT the permanent Lead Reviewer, appointed by the Programme Sponsor on 10 July 2026, informed by all four closed trial sessions (ESR-0015 through ESR-0018).** No rotation confirmation is required at future session start; confirm the appointment itself has not been separately revisited instead.
11. Search the Historical Archive (AIEMS History and Full Chat artefacts) only where deeper context is required.
12. Confirm Programme Sponsor approval before creating any future Engineering Session Report, future repository baseline or future engineering objective.

This guidance records the ESR-0018 closed state and the concluded EE-0001 appointment. PST-0001 does not create a new engineering session, accept a repository baseline or approve implementation outside separately authorised engineering work.

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
| [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] | Current closed engineering session report (10 July 2026) - Gemini provider production-readiness hardening (EBG-0051) and the EE-0001 Section 7 decision/permanent appointment. |
| [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] | Prior closed engineering session report - nine Work Packages including the first live interactive UXP and a Guardian Orb design-baseline recovery. |
| [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] | Closed engineering session report recording the Sentinel trust-tier policy model and its architecture alignment, delivered and independently verified. |
| [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] | Closed engineering session report recording the Sentinel execution pipeline delivered and proven end to end. |
| [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] | Current accepted repository baseline, accepted at ESR-0017 closure, superseding RBL-0012 (mid-ESR-0017) and RBL-0011 (ESR-0015-ESR-0016). |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Approved Guardian Experience Architecture; now includes the recovered Guardian Orb knowledge-graph design direction (ESR-0017). |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial, concluded at ESR-0018 (Section 7): all four sessions closed (ESR-0015 Claude Lead, ESR-0016 ChatGPT Lead, ESR-0017 Claude Lead/Cold Start, ESR-0018 ChatGPT Lead/decision point); permanent appointment made - Claude Lead Engineer, ChatGPT Lead Reviewer. |
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

| Version | Date | Author | Summary |
|---------|------|--------|---------|
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
