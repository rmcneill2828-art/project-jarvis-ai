# PST-0001 - Programme Status

> *"A programme moves faster when its current state is clear, trusted and easy to reload."*

**Version:** 2.20

---

# Document Control

| Field | Value |
|-------|-------|
| Artefact ID | PST-0001 |
| Title | Programme Status |
| Version | 2.20 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Review Frequency | At phase closure or engineering session transition |
| Effective Date | 8 July 2026 |
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
| Current Mode | [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] closed; Sentinel execution pipeline (audit, policy, provider, Guardian integration) delivered and proven with a live, audited, policy-gated conversation. |
| Current Repository Baseline | [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] remains the accepted repository baseline; [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] recommended and drafted, Programme Sponsor acceptance pending. |
| Current Product Capability Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] accepted as current operational JARVIS product baseline. |
| Repository Product Capability Assessment | [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] completed and accepted. |
| Current Phase | ESR-0015 closed: Sentinel execution pipeline complete and validated end to end. |
| Current Workflow | AIEMS Engineering Workflow v3 with Engineering Ecosystem Synchronisation working practice, operating under the EE-0001 Lead/Reviewer trial (ESR-0016: ChatGPT leads, Claude reviews). |
| Current Engineering Objective | No future engineering objective is created by this status update. ESR-0016 entry recommendation recorded in [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] section 17 remains a Programme Sponsor decision. |

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

[[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] is closed. This was the first Engineering Session run under the EE-0001 Lead/Reviewer trial: Claude as Engineering Implementer, ChatGPT as Engineering Reviewer, Programme Sponsor gating every step.

ESR-0015 delivered the Sentinel execution pipeline in full: `sentinel/audit.py` (AuditRecorder infrastructure), `sentinel/policy.py` (PolicyEngine abstraction), `sentinel/openai_provider.py` (first external provider adapter), and `jarvis/interfaces/sentinel_conversation.py` (Guardian/Sentinel integration) - proven end to end with a live, audited, policy-gated Guardian conversation against OpenAI.

[[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] remains the accepted repository baseline. [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] has been drafted and recommended, reflecting that ESR-0015 is judged a qualitatively different milestone (architecture proven operational, not just designed) - Programme Sponsor acceptance is pending, not presumed.

PST-0001 records the ESR-0015 closed state. It does not accept a repository baseline or create ESR-0016.

---

# 5. Current Capability Roadmap

| Capability | Status | Maturity | Notes |
|------------|--------|----------|-------|
| Repository Architecture | Complete | Complete | Repository structure, package layout and governance separation are established. |
| Governance Framework | In Progress | High | Core AIEMS governance artefacts support controlled product delivery and are ready to be tested through implementation-led engineering. |
| Engineering Standards | In Progress | High | Approved standards remain in place; RFEP, RFDP and Continuous Repository Synchronisation are working practices pending any future standards review. |
| JARVIS Product Architecture | Complete | High | [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] remains the product architecture authority. |
| JARVIS Platform Architecture | Draft | High | [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] validated JARVIS Platform, Sentinel, Platform Services, UXP, Provider Architecture, Agent Framework and GIA positioning for implementation readiness. |
| Sentinel AI Execution and Security Platform | Implemented | High | [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] positions Sentinel as the AI Execution and Security Platform; Sentinel Core, provider abstraction, local provider, provider configuration and health-aware provider orchestration with failover are implemented under `sentinel/` with 100 passing tests. |
| Guardian Cognitive Architecture | Draft | High | [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] records Guardian identity and cognitive architecture; ESR-0013 established a bounded runtime foundation without implementing full Guardian cognition. |
| Guardian Experience Architecture | Approved Baseline | High | [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] records Guardian Experience Architecture v1.0; [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] confirms Guardian Orb should consume real observable state. |
| Engineering Ecosystem Architecture | Implementation Validated | High | [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] records Obsidian/OSE and Engineering Ecosystem Synchronisation; ESR-0012 validated AIEMS operationally through implementation. |
| Guardian Instrumentation Agent | Proof of Concept Complete | Early | [[ESR-0012_ENGINEERING_SESSION_REPORT|ESR-0012]] completed GIA-BOOT as a Proof of Concept; further GIA implementation is deferred. |
| User Experience Platform | Established | Foundation | [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]] records Tauri + React as the UXP direction; ESR-0009 adopted it as the UXP implementation baseline. |
| JARVIS Product Capability Baseline | Accepted | Foundation | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] records the accepted operational product baseline. |
| JARVIS Capability Maturity | Maintained | Early | [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] remains the authoritative maturity model. |
| JARVIS Development | In Progress | Early | Guardian Desktop Platform Shell, Guardian Experience v1.0, GIA-BOOT Proof of Concept and Guardian Runtime Foundation exist; unimplemented runtime capabilities remain outside the accepted operational product baseline. |
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

---

# 7. Current Engineering Standards Position

Approved standards remain current. ESR-0007 methodology outcomes are working practices only and shall not be treated as standards unless promoted through future approved standards review.

---

# 8. Active and Next Planned Work

| Item | Status | Notes |
|------|--------|-------|
| Current Engineering Session | None active | [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] closed; next session not yet created. |
| Current Repository Baseline | [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] | Accepted repository baseline; RBL-0011 drafted and recommended, Programme Sponsor acceptance pending. |
| Current Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational JARVIS product baseline. |
| Current Review State | ESR-0015 closed | Sentinel execution pipeline complete, proven end to end with a live conversation. |
| Next Required Closure Activity | None outstanding | ESR-0015 is closed. |
| Next Engineering Session | Not created by this status update | ESR-0016 entry recommended (ChatGPT leads, Claude reviews per EE-0001) but not created; requires separate approval and repository synchronisation. |
| ESR-0015 Implementation Scope | Sentinel execution pipeline | Completed: WP1 AuditRecorder, WP2 PolicyEngine, WP3a/b provider scoring and adapter, WP4 Guardian integration, WP5 live validation, WP6 closure. |
| GIA-BOOT Proof of Concept | Complete | Accepted as Proof of Concept; further GIA implementation deferred. |
| Deferred Work | Recorded | Guardian Memory, Conversation Engine expansion, Guardian Developer Console, Guardian Orb, Automation, persistent storage, EAC and GDP-0001 implementation remain deferred. Gemini/Anthropic/OpenRouter/Ollama provider adapters approved in principle (PEM-001) but not yet implemented. Richer trust-tier policy engine deferred to ESR-0016. |
| Authoritative Backlog Source | [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Future engineering priorities remain governed by the backlog register. |
| Runtime Evidence Archive | `logs/chats/` | Prototype JARVIS chat exports remain archived under runtime evidence archive. |

---

# 9. Repository Health

| Item | Status |
|------|--------|
| Repository Health | Good |
| Repository Acceptance | Accepted through [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] |
| Current Repository Baseline | [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] |
| Product Capability Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Latest Repository Product Capability Assessment | [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] |
| Current Activity | ESR-0015 closed; Sentinel execution pipeline complete and validated. RBL-0011 drafted, Programme Sponsor acceptance pending. |

---

# 10. Outstanding Observations

The following observations remain open for future engineering consideration:

- [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] remains accepted as the current repository baseline pending any future controlled baseline creation.
- [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] established the Guardian Platform Foundation through runtime boundary, lifecycle integration, status snapshot and observability work.
- [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] is closed. Sentinel Core, provider abstraction, local provider, provider configuration and provider orchestration are implemented under `sentinel/` with 100 passing tests. [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] positions Sentinel as the AI Execution and Security Platform.
- [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] is closed. [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] introduces knowledge tiering for Engineering Session initialisation.
- Guardian Runtime is not yet connected through Sentinel.
- PEM-001 provider scoring against current provider information remains pending, per ESR-0014 outstanding work.
- ESR-0015 is not created by this status update.
- GIA-BOOT is accepted as a Proof of Concept.
- Further GIA implementation is deferred.
- AIEMS Engineering Agent is adopted to support the Engineering Reviewer role.
- Remaining Engineering Agent validation is deferred.
- Future EAC implementation is deferred.
- Guardian Memory remains deferred.
- Conversation Engine expansion remains deferred.
- Guardian Developer Console remains deferred.
- Guardian Orb implementation remains deferred until real observable platform state is ready for presentation-layer consumption.
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
6. Recommended and drafted [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]]; retained [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] pending Programme Sponsor acceptance decision.
7. Created [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] as the formal session closure report, including an Engineering Implementer draft of the EE-0001 trial scorecard pending independent Reviewer scoring.

---

# 21. Session Start Guidance

At the start of the next separately approved engineering session or approved implementation activity, follow [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] knowledge tiering:

1. Review README.md for repository orientation and platform context.
2. Review [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] and, if accepted in the interim, [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]].
3. Review [[PST-0001_PROGRAMME_STATUS|PST-0001]] (Current State tier).
4. Review the Architecture tier as referenced by PST-0001.
5. Review Active Standards (STD-0001 through STD-0004) where the session's work touches artefact creation or modification.
6. Review [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] (Current ESR tier).
7. Review [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
8. Review [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]].
9. Review [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]].
10. Review [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] to confirm current Lead/Reviewer rotation before beginning work.
11. Search the Historical Archive (AIEMS History and Full Chat artefacts) only where deeper context is required.
12. Confirm Programme Sponsor approval before creating any future Engineering Session Report, future repository baseline or future engineering objective.

This guidance records the ESR-0015 closed state. PST-0001 does not create ESR-0016, accept a repository baseline or approve implementation outside separately authorised engineering work.

---

# 22. Maintenance

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
| [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] | Closed engineering session report recording the Sentinel execution pipeline delivered and proven end to end. |
| [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] | Recommended repository baseline reflecting ESR-0015; Programme Sponsor acceptance pending. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial ESR-0015 operated under; governs role rotation for ESR-0016 onward. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Provider evaluation matrix; decision outcome recorded during ESR-0015 WP3a. |
| [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] | Closed engineering session report recording Sentinel AI Execution and Security Platform implementation. |
| [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] | Closed post-closure addendum recording GDE-0001 knowledge tiering. |
| [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] | Defines the knowledge tier structure this status update's Session Start Guidance now follows. |
| [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] | Engineering session report recording the Guardian Platform Foundation. |
| [[ESR-0012_ENGINEERING_SESSION_REPORT|ESR-0012]] | Engineering session report recording ESR-0012 closure, GIA-BOOT Proof of Concept completion and AIEMS Engineering Agent validation. |
| [[ESR-0011_ENGINEERING_SESSION_REPORT|ESR-0011]] | Engineering session report recording ESR-0011 closure, Architecture Validation and Implementation Readiness outcomes and ESR-0012 implementation handover. |
| [[ESR-0010_ENGINEERING_SESSION_REPORT|ESR-0010]] | Engineering session report recording ESR-0010 closure and ESR-0011 handover state. |
| [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]] | Engineering session report recording ESR-0009 closure and ESR-0010 handover. |
| [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] | Current accepted repository baseline, retained through ESR-0015 closure pending RBL-0011 acceptance decision. |
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
| [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] | Current accepted repository baseline, retained through ESR-0015 closure pending RBL-0011 acceptance decision. |
| [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] | Recommended repository baseline reflecting ESR-0015; Programme Sponsor acceptance pending. |
| [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] | Closed engineering session report recording the Sentinel execution pipeline delivered and proven end to end. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial ESR-0015 operated under; governs role rotation for ESR-0016 onward. |
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
