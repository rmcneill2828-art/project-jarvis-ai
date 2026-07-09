# EBR-0001 - Engineering Backlog Register

> *"Deferred work remains governed work."*

**Version:** 1.21

---

# 1. Document Control

| Field | Value |
|------|-------|
| Artefact ID | EBR-0001 |
| Title | Engineering Backlog Register |
| Version | 1.21 |
| Status | Draft |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | CHR-0001 |
| Effective Date | 27 June 2026 |
| Review Frequency | At engineering session transition or backlog review |

---

# 2. Purpose

The Engineering Backlog Register is the authoritative register for approved, deferred, planned and candidate engineering backlog items within Project JARVIS AI.

It preserves engineering work that has been identified but not yet implemented, ensuring that deferred items remain visible, traceable and subject to Programme Sponsor review.

This register supports AIEMS by separating approved implementation scope from future engineering recommendations, technical debt, observations and candidate backlog intake.

---

# 3. Scope

This register records engineering backlog items that may require future Engineering Implementation Packages, engineering review, recovery, supersession, lifecycle assessment or controlled implementation.

It includes:

- Approved backlog items.
- Deferred engineering work.
- Planned engineering activities.
- Candidate backlog items awaiting review.
- Backlog status and priority information.

This register does not itself authorise implementation.

Backlog items shall not be implemented unless included within an approved Engineering Implementation Package or otherwise explicitly authorised by the Programme Sponsor.

---

# 4. Backlog Management Principles

Engineering backlog management shall follow these principles:

- Every backlog item shall have a unique backlog identifier.
- Approved backlog items shall remain traceable to their source where known.
- Candidate items shall remain separate from approved backlog items until reviewed.
- Backlog status shall reflect current engineering authority and disposition.
- Recommendations, observations, defects and technical debt shall not become implementation scope until approved.
- Backlog maintenance shall preserve repository-first engineering and AIEMS scope control.

---

# 5. Backlog Register

| Backlog ID | Title | Source | Status | Priority | Owner | Notes |
|------------|-------|--------|--------|----------|-------|-------|
| EBG-0001 | ADR-0004 recovery or formal supersession | ESR-0001 deferred work | Completed | Medium | Programme Sponsor | ADR-0004 recovered during ESR-0003 EIP-R2 from approved repository evidence. |
| EBG-0002 | ADR-0005 recovery or formal supersession | ESR-0001 deferred work | Completed | Medium | Programme Sponsor | ADR-0005 recovered during ESR-0003 EIP-R2 from approved repository evidence. |
| EBG-0003 | Lifecycle review of COC-0001 | ESR-0001 deferred work | Approved Backlog | Medium | Programme Sponsor | Review lifecycle status of COC-0001 and determine whether promotion or continued draft status is appropriate. |
| EBG-0004 | Lifecycle review of PBK-0001 | ESR-0001 deferred work | Approved Backlog | Medium | Programme Sponsor | Review lifecycle status of PBK-0001 and determine whether promotion or continued draft status is appropriate. |
| EBG-0005 | REG-0001 metadata alignment following P2-004A | ESR-0001 deferred work | Approved Backlog | Medium | Programme Sponsor | Align REG-0001 metadata where required following P2-004A changes. |
| EBG-0006 | REV-0002 Repository Baseline Verification | ESR-0001 deferred work | Approved Backlog | Medium | Programme Sponsor | Create REV-0002 as a controlled Repository Baseline Verification artefact. |
| EBG-0007 | STD-0004 Validation and Quality Assurance Standard | ESR-0001 deferred work; GSF-011 | Completed | Medium | Programme Sponsor | STD-0004 created during ESR-0004 EIP-ESR0004-02. |
| EBG-0008 | Create Engineering Implementation Package Standard | ESR-0002 Candidate Backlog Review; GSF-028 | Approved Backlog | Medium | Programme Sponsor | Create a dedicated controlled standard defining Engineering Implementation Package format, lifecycle, mandatory sections, numbering and approval rules to reduce repeated instruction overhead. |
| EBG-0009 | Create Engineering Session Standard | ESR-0002 Candidate Backlog Review; GSF-028 | Approved Backlog | Medium | Programme Sponsor | Create a dedicated controlled standard for Engineering Session initiation, execution, closure, handover, continuity, single active session governance and Engineering Session Archive standardisation to reduce repeated session overhead. Include an Engineering Session Archive template / standard with consistent archive sections for engineering session overview, engineering timeline, approved EIPs, baseline acceptance history, repository verification log, engineering decisions and rationale, backlog changes, AIEMS improvements introduced, session metrics, lessons learned, final repository health review outcome and handover to the next Engineering Session. |
| EBG-0010 | Define repository metadata and cross-reference validation rules | ESR-0002 Candidate Backlog Review | Approved Backlog | Medium | Programme Sponsor | Define validation rules for repository metadata, identifier uniqueness, artefact cross-references, parent artefact consistency and controlled document traceability as the rule baseline for future automation. |
| EBG-0011 | Create AI Roles and Capability Matrix | ESR-0002 Candidate Backlog Review; GSF-012 | Approved Backlog | Medium | Programme Sponsor | Create a matrix defining AI collaborator roles, capabilities, permissions, limitations, decision boundaries and tool usage across ChatGPT, Codex, GitHub connector and future AI agents, including GitHub connector capability validation boundaries. |
| EBG-0012 | Establish AIEMS roadmap and release planning artefact | ESR-0002 Candidate Backlog Review | Approved Backlog | Medium | Programme Sponsor | Create a controlled roadmap or release planning artefact showing AIEMS phases, milestones, dependencies, sequencing and target outcomes. |
| EBG-0013 | Create Engineering Decision Index | ESR-0002 Candidate Backlog Review | Approved Backlog | Medium | Programme Sponsor | Create a searchable controlled index of ADRs, Engineering Decisions and significant governance changes to improve decision traceability. |
| EBG-0014 | Assess repository validation automation | ESR-0003 EIP-R4; GSF-020 | Approved Backlog | Medium | Programme Sponsor | Assess future automation for repository metadata and cross-reference validation after validation rules are defined; do not implement automation until separately approved. |
| EBG-0015 | Investigate JARVIS Human-AI Interaction Memory and Behavioural Intelligence Layer | ESR-0003 EIP-R4 | Approved Backlog | Medium | Programme Sponsor | Investigate future JARVIS memory and behavioural intelligence capability, including governance boundaries, risks and controls; no implementation is authorised by this backlog entry. |
| EBG-0016 | Consider renaming WP0 from "Engineering Synchronisation" to "Engineering & Repository Synchronisation" | ESR-0004 WP3 Governance Refinement | Deferred | Low | Programme Sponsor | Candidate terminology refinement for future consideration. Potentially clearer, but not required for the current implementation. |
| EBG-0017 | JARVIS Product Requirements and Capability Backlog | ESR-0004 EIP-EKR-0001 | Candidate Backlog | High | Programme Sponsor | Create or identify the authoritative product requirements backlog for recovered JARVIS capability intent, avoiding raw transcript import and duplicate product documentation. |
| EBG-0018 | JARVIS AI Provider Abstraction Architecture | ESR-0004 EIP-EKR-0001 | Candidate Backlog | High | Programme Sponsor | Define provider independence before any external AI provider integration. Preserve technology independence and avoid coupling JARVIS to one model or vendor. |
| EBG-0019 | JARVIS Memory and Data Storage Architecture | ESR-0004 EIP-EKR-0001 | Candidate Backlog | High | Programme Sponsor | Define memory, storage, privacy and consent boundaries before long-term memory or family knowledge is implemented. |
| EBG-0020 | JARVIS Guardian, Family Safety and Emergency Controls | ESR-0004 EIP-EKR-0001 | Candidate Backlog | High | Programme Sponsor | Define parental oversight, child safety, human approval and pre-approved emergency action boundaries before Guardian capability is implemented. |
| EBG-0021 | JARVIS Local Agent Permission Boundary | ESR-0004 EIP-EKR-0001 | Candidate Backlog | High | Programme Sponsor | Define local device control limits before local agent implementation; local agents must not receive unlimited control. |
| EBG-0022 | JARVIS AIEMS Knowledge Capability | ESR-0004 EIP-EKR-0001 | Candidate Backlog | Medium | Programme Sponsor | Investigate enabling JARVIS to understand and explain AIEMS using repository artefacts as governed knowledge. |
| EBG-0023 | JARVIS Backup, Recovery and Data Protection Guidance | ESR-0004 EIP-EKR-0001 | Candidate Backlog | Medium | Programme Sponsor | Define backup and recovery expectations before persistent memory, family data or local operational state becomes significant. |
| EBG-0024 | JARVIS Cost Strategy | ESR-0004 EIP-EKR-0001 | Candidate Backlog | Medium | Programme Sponsor | Define cost principles before paid providers, cloud services, voice, vision or storage decisions materially affect the programme. |
| EBG-0025 | JARVIS Home Assistant and Smart Home Integration Assessment | ESR-0004 EIP-EKR-0001 | Candidate Backlog | Medium | Programme Sponsor | Assess Home Assistant and smart-home integration options before any smart-home implementation package is approved. |
| EBG-0026 | Transcript Export Workflow Enhancement | ESR-0005 RBL-0006 observation | Candidate Backlog | Medium | Programme Sponsor | Improve transcript export with default save location, automatic naming convention, GUI acknowledgement and no popup save dialogue where practical. |
| EBG-0027 | JRM-0001 JARVIS Product Roadmap | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Create a controlled product roadmap for JARVIS capability sequencing without expanding implementation scope. |
| EBG-0028 | UXP Evolution Roadmap | ESR-0005 closure recommendation; ESR-0008 terminology alignment; [[ESR-0010_ENGINEERING_SESSION_REPORT|ESR-0010]] Section 15 phased achievability discussion | Candidate Backlog | Medium | Programme Sponsor | Define staged User Experience Platform maturity from First Light through operational workspace and future product surfaces. GUI is preserved as the historical alias for earlier presentation-layer work. Per the ESR-0010 Guardian Orb design conversation (`aiems/History/Full Chat/FCH-0010_ESR-0010_FULL_CHAT_HISTORY.md`, retroactively incorporated into [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Sections 8.1/8.2 at ESR-0017), a candidate phased sequencing for the knowledge-graph Orb specifically was discussed and should inform this roadmap's staging when actioned: Phase 1 - static live graph rendered from Obsidian/repository data; Phase 2 - cluster colours and chat UI around it; Phase 3 - agent activity/traversal animation; Phase 4 - connection to Guardian reasoning and future telemetry (e.g. GIA). No implementation is authorised by this backlog entry. |
| EBG-0029 | Product Growth Philosophy | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Record the principle that JARVIS grows by acquiring capabilities rather than accumulating features. |
| EBG-0030 | Sentinel Architecture Specification | ESR-0005 closure recommendation | Completed | High | Programme Sponsor | Define Sentinel responsibilities, boundaries and relationship to Guardian before Sentinel implementation. Satisfied by [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] and the Guardian/Sentinel boundary defined in ESR-0014 section 13. |
| EBG-0031 | Guardian Architecture Specification | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define Guardian safety, permission, approval and protection boundaries before Guardian implementation. |
| EBG-0032 | Historical Engineering Register | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Consider a controlled register for historically significant engineering baselines, tags and milestones. |
| EBG-0033 | AIEMS Improvement Register / AIEMS Improvement Review | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Define a controlled mechanism for recording AIEMS process improvements without disrupting active engineering flow. |
| EBG-0034 | Engineering Authority by Work Package | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define authority boundaries by work package type so implementation, assessment, correction and verification packages remain distinct. |
| EBG-0035 | Context Activation Guidance | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define how package context, repository baseline, role authority and relevant artefacts are activated before execution or verification. |
| EBG-0036 | WP6 Repository Content Verification Standard | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define repeatable WP6 repository content verification expectations, evidence requirements and reporting structure. |
| EBG-0037 | Engineering Package Classifications: EIP / EAP / ECP | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Define controlled package classifications for Engineering Implementation Packages, Engineering Assessment Packages and Engineering Corrective Packages. |
| EBG-0038 | Formal AIEMS Standards Review | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]]; ESR-0006 continuous improvement | Candidate Backlog | High | Programme Sponsor | Validate CI-0001 through CI-0007 and determine which ESR-0006 working practices require formal standardisation. Rationale: preserves AIEMS improvement discipline while avoiding premature standard creation. |
| EBG-0039 | JARVIS Runtime Chat Archive | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]]; ESR-0006 repository readiness classification | Completed | High | Programme Sponsor | Runtime chat exports moved from repository root to `logs/chats/`, including `Jarvis one.md` and `Jarvis two.md`. Rationale: separates product runtime artefacts from AIEMS controlled artefacts while preserving export evidence. |
| EBG-0040 | AIEMS Repository Integrity Troubleshooting Playbook | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]]; ESR-0006 repository readiness review | Candidate Backlog | Medium | Programme Sponsor | Create practical troubleshooting guidance for environmental Git status, line-ending normalization, ignored workspace state and baseline-readiness checks. Rationale: captures repeatable repository integrity learning from ESR-0006. |
| EBG-0041 | Guardian Identity Architecture Validation | [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Candidate Backlog | High | Programme Sponsor | Validate [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] and determine implementation sequencing for Guardian identity and faculties. |
| EBG-0042 | Agent Framework Architecture | [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]]; [[ADR-0011_AGENT_FRAMEWORK|ADR-0011]] | Candidate Backlog | High | Programme Sponsor | Define specialist agent contracts, including Engineering Agent, while preserving Guardian as the singular user-facing identity. |
| EBG-0043 | Engineering Ecosystem Synchronisation Workflow | [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Candidate Backlog | High | Programme Sponsor | Define repeatable WP0 workflow covering GitHub, AIEMS, OSE, Obsidian, registers, controlled artefacts, previous ESRs and summaries. |
| EBG-0044 | Obsidian / OSE Validation Workflow | [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Candidate Backlog | Medium | Programme Sponsor | Define how Obsidian as the human-facing Engineering Knowledge Workspace validates and navigates repository Markdown without replacing GitHub as source of truth. |
| EBG-0045 | Cost and Strategic Value Framework | [[ADR-0008_HYBRID_AI_RUNTIME_STRATEGY|ADR-0008]] | Candidate Backlog | High | Programme Sponsor | Define evaluation criteria for cloud providers, commercial options, cost, privacy, strategic value and product benefit. See also EBG-0049 (Cost-Aware Provider Routing and PEM-001 Revisit) - overlapping scope, consider together when either is actioned. |
| EBG-0046 | Device Independence and Restore Architecture | [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]] | Candidate Backlog | High | Programme Sponsor | Define bootstrap, progressive restore, portable memory, configuration and encrypted sync requirements. |
| EBG-0047 | Sentinel Gate of Durin Architecture Specification | [[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]] | Candidate Backlog | High | Programme Sponsor | Extend EBG-0030 with Sentinel trust gateway, trust tiers and platform-entry validation details. |
| EBG-0048 | Guardian HITL Governance Specification | [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]] | Candidate Backlog | High | Programme Sponsor | Extend EBG-0031 with consent, policy, privacy, approval, memory retention and trusted mobile approve/deny governance. |
| EBG-0049 | Cost-Aware Provider Routing and PEM-001 Revisit | [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]]; overlaps EBG-0045 | Candidate Backlog | High | Programme Sponsor | Define a cost/performance balance policy for Sentinel provider routing (leveraging ESR-0016's trust-tier classification as a candidate mechanism for cost-aware routing decisions), and revisit [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]]'s provider scoring to confirm cost is weighted as an explicit first-class criterion rather than incidental. Should account for institutional cloud/education resources potentially available to the Programme Sponsor as a cost-reduction lever. Overlapping scope with EBG-0045 (Cost and Strategic Value Framework, still Candidate Backlog, not yet actioned) - not a duplicate, but closely related and should be considered together when either is actioned. |
| EBG-0050 | UXP-Backend Bridge Implementation | [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]]; [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] WP1 | Candidate Backlog | High | Programme Sponsor | Implement the Tauri sidecar-managed Python process and duplex stdio JSON-RPC bridge decided in ADR-0019: new `python -m jarvis` headless IPC entry point, JSON-RPC message schema (including streaming notifications for Guardian/Sentinel state), `src-tauri/src/lib.rs` sidecar command and message forwarding, and replacing `src/platformStatus.js`'s hardcoded state with live data. Distinct from EBG-0028 (UXP Evolution Roadmap, which covers staged UXP maturity broadly, not this specific integration pattern). Per ChatGPT Engineering Reviewer's ESR-0017 WP1 recommendation, implementation must define explicit failure-mode behaviour: backend crash handling, restart policy, version negotiation, protocol compatibility and IPC timeout strategy - these belong at implementation time, not in ADR-0019 itself. Per ChatGPT Engineering Reviewer's ESR-0017 WP2 Observation 2, implementation should also consider whether `GuardianRuntime.converse()` (currently synchronous request/response) should eventually gain a streaming conversation interface once the JSON-RPC bridge's async-notification side exists, rather than assuming `converse()` stays synchronous forever. Per ChatGPT Engineering Reviewer's ESR-0017 WP9 implementation review Minor Finding 2: `StdioRpcServer.handle_line()` currently surfaces `f"{type(exc).__name__}: {exc}"` for handler exceptions - acceptable while every provider is local/deterministic (foundation scope), but once external/provider-backed paths are wired through this bridge, internal exception messages should not be surfaced verbatim to the client. No implementation is authorised by this backlog entry. |
| EBG-0051 | Gemini Provider Production Readiness | [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] WP3 | Candidate Backlog | Medium | Programme Sponsor | Per ChatGPT Engineering Reviewer's ESR-0017 WP3 observations, before `GeminiProvider` (`sentinel/gemini_provider.py`) is wired into any production `ProviderOrchestrator` route: (1) richer response parsing - current implementation assumes `candidates[0]` contains usable text; must handle safety-blocked responses, empty `parts`, tool responses and structured output; (2) consider exposing additional response metadata beyond `{"model": ...}` - finish reason, token usage, safety ratings (applies to future provider adapters generally, not Gemini alone); (3) **required before Gemini is enabled as a production provider**: a single live smoke test against the real Gemini API, equivalent to the live OpenAI validation performed during ESR-0015 WP5. No implementation is authorised by this backlog entry. |
| EBG-0052 | PBK-0001/EE-0001 "Execute After Approval" Principle | [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]]; [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 9 ESR-0017 entry | Candidate Backlog | Medium | Programme Sponsor | Improvement finding from the EE-0001 trial, originally reported by the Programme Sponsor and independently confirmed and refined by the Engineering Reviewer (ChatGPT) in its own ESR-0017 review: following explicit Programme Sponsor approval, the Reviewer continued conversational confirmation rather than transitioning immediately into execution, and engineering outputs were produced only after further Sponsor prompting - a process-efficiency issue, not an engineering-quality issue, per the Reviewer's own characterisation. Consider formalising a standing "execute after approval, don't just acknowledge" rule in PBK-0001 (parallel to the ESR-0016A WP4 "Operational Verification Before Reporting" precedent) and/or clarifying it within EE-0001 Section 3.2's Independent Reviewer role definition. No implementation is authorised by this backlog entry. |
| EBG-0053 | EE-0001 "Review Gate Compliance" Criterion | [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]]; [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 9 ESR-0017 entry | Candidate Backlog | Medium | Programme Sponsor | Jointly recommended by the Engineering Lead (Claude) and Engineering Reviewer (ChatGPT) during ESR-0017's scorecard reconciliation: EE-0001 currently has no criterion measuring whether agreed Lead/Reviewer checkpoints occurred before subsequent implementation proceeded (ESR-0017 was the first session to actually violate this, mid-session, and self-correct once caught by the Programme Sponsor). The Reviewer specifically recommended this stay distinct from Section 5.5 Lead Scope Discipline, since scope and execution-cadence discipline measure different things. Candidate wording: "Review Gate Compliance - measures whether agreed Lead/Reviewer checkpoints occurred before subsequent implementation proceeded." This is a proposed new EE-0001 Section 5.x criterion, not yet adopted - per EE-0001 Section 4, any change to the scoring instrument requires a dated, justified, Programme-Sponsor-decided log entry in Section 8, same as the ESR-0016 findings-definition precedent. No implementation is authorised by this backlog entry. |
| EBG-0054 | Dev-Environment Setup Automation Expansion | [[ESR-0017_ENGINEERING_SESSION_REPORT|ESR-0017]] Section 15.2 | Candidate Backlog | Low | Programme Sponsor | `setup.bat` / `scripts/setup-dev-environment.ps1` were added in ESR-0017 (prompted by the Programme Sponsor moving between machines, including a work laptop) to automate a fresh clone's environment: `npm install`, `cargo build`, Python venv + editable install, pre-commit hook activation, validator and test suite as a smoke test. Verified working end-to-end and idempotent. Candidate future expansion, not yet authorised: a cross-platform (bash/zsh) equivalent for non-Windows machines; reusing the same script in CI for environment parity with local dev; an "environment doctor" mode that only diagnoses/reports without changing anything; and prerequisite-version checks (e.g. minimum Node/Rust/Python versions) rather than only presence-on-PATH checks. No implementation is authorised by this backlog entry. |

---

# 6. Candidate Backlog Intake

Backlog items discovered from historical chat sessions must be marked **Candidate Backlog** until reviewed and accepted by the Programme Sponsor.

Candidate backlog items shall not be treated as approved engineering scope.

Candidate items may be reviewed and assigned one of the following outcomes:

- Accepted
- Merged
- Superseded
- Rejected
- Deferred

Accepted candidate items may be added to the approved Backlog Register with a unique backlog identifier.

Merged, superseded, rejected or deferred candidate items shall retain sufficient notes to preserve review traceability.

---

# 7. Prioritisation Rules

Backlog priority shall be assigned by the Programme Sponsor or through an approved engineering review.

Priority values are:

- Critical
- High
- Medium
- Low

Priority shall consider repository integrity, governance consistency, engineering risk, implementation dependency and programme value.

Priority does not authorise implementation.

---

# 8. Status Definitions

| Status | Definition |
|--------|------------|
| Candidate Backlog | Identified item awaiting Programme Sponsor review and acceptance. |
| Approved Backlog | Accepted backlog item that may be progressed through a future approved Engineering Implementation Package. |
| Planned | Approved backlog item selected for future planning but not yet authorised for implementation. |
| In Progress | Backlog item currently being implemented under an approved Engineering Implementation Package. |
| Completed | Backlog item implemented and accepted into the repository baseline. |
| Merged | Candidate or backlog item consolidated into another backlog item. |
| Superseded | Item replaced by a newer or more appropriate backlog item or artefact. |
| Rejected | Item reviewed and declined for inclusion or implementation. |
| Deferred | Item intentionally retained for later consideration without current implementation commitment. |

---

# 9. Relationship to AIEMS

EBR-0001 supports AIEMS by maintaining a controlled view of future engineering work without expanding current implementation scope.

It complements:

- Engineering Session Reports, which record completed sessions and deferred work.
- Programme Status, which records current programme state.
- Engineering Implementation Packages, which define approved implementation scope.
- Controlled Artefact Registers, which record governed artefacts.
- Engineering Reviews, which may identify backlog candidates or approve backlog progression.

Where conflict exists, approved Engineering Implementation Packages define current implementation scope.

---

# 10. OSE Relationships

| Artefact | OSE Relationship |
|----------|------------------|
| [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]] | Defines the retrospective relationship-only enrichment rule applied to this backlog register. |
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Establishes Engineering Ecosystem Synchronisation and the repository-compatible OSE context for backlog traceability. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Records authoritative artefact identity, ownership, status and current version for controlled backlog-related artefacts. |
| [[REG-0004_ACTION_REGISTER|REG-0004]] | Records governed actions that may become, complete or relate to backlog work. |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Provides product vision traceability context for backlog candidates and deferred work. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Records current programme status and backlog review context. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Current accepted repository baseline supporting this retrospective OSE pass. |

---
# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Source baseline for ESR-0006 repository readiness classification and new backlog intake. |
| [[RBL-0006_REPOSITORY_BASELINE|RBL-0006]] | Previous baseline that provided the starting point for ESR-0006. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Registers controlled artefacts whose changes may create backlog follow-up. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status context for session transition and future backlog review. |
| [[ESR-0005_ENGINEERING_SESSION_REPORT|ESR-0005]] | Source of the prototype JARVIS chat export artefacts classified during ESR-0006. |

---

# 12. Maintenance

The Engineering Backlog Register shall be reviewed:

- At engineering session transition.
- When deferred work is identified during session closure.
- When candidate backlog items are submitted for Programme Sponsor review.
- When backlog items are accepted, merged, superseded, rejected, deferred or completed.
- When the Programme Sponsor directs a backlog review.

Updates to this register shall preserve unique backlog identifiers and maintain traceability to source artefacts where known.

---

# 13. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.21 | 9 July 2026 | Claude Engineering Lead | Added ESR-0010's phased achievability roadmap (from FCH-0010's Guardian Orb design discussion, retroactively incorporated into UAM-0001 v1.2) to EBG-0028's note: Phase 1 static live graph, Phase 2 cluster colours/chat UI, Phase 3 agent traversal animation, Phase 4 Guardian reasoning/telemetry connection. |
| 1.20 | 9 July 2026 | Claude Engineering Lead | Added ChatGPT Engineering Reviewer's ESR-0017 WP9 implementation review Minor Finding 2 (handler exception messages should not surface verbatim once external/provider-backed paths exist) to EBG-0050's note. |
| 1.19 | 9 July 2026 | Claude Engineering Lead | Added EBG-0054 (Dev-Environment Setup Automation Expansion), recording ESR-0017's new setup.bat / scripts/setup-dev-environment.ps1 clone-bootstrap tooling and candidate future expansion (cross-platform equivalent, CI parity, environment-doctor mode, version-floor checks). |
| 1.18 | 9 July 2026 | Claude Engineering Lead | Refined EBG-0052 wording with ChatGPT Engineering Reviewer's own confirmation/clarification of the execute-after-approval finding; added EBG-0053 (EE-0001 Review Gate Compliance Criterion), jointly recommended by Lead and Reviewer during ESR-0017 scorecard reconciliation. |
| 1.17 | 9 July 2026 | Claude Engineering Lead | Added EBG-0052 (PBK-0001/EE-0001 Execute After Approval Principle) per Programme Sponsor-reported EE-0001 trial improvement finding for ESR-0017. |
| 1.16 | 9 July 2026 | Claude Engineering Lead | Added EBG-0051 (Gemini Provider Production Readiness) per ChatGPT Engineering Reviewer's ESR-0017 WP3 observations: richer response parsing, extended metadata, and a required live smoke test before Gemini is enabled as a production provider. |
| 1.15 | 9 July 2026 | Claude Engineering Lead | Added ChatGPT Engineering Reviewer's ESR-0017 WP2 Observation 2 (consider a streaming converse() interface at EBG-0050 implementation time) to EBG-0050's note. |
| 1.14 | 9 July 2026 | Claude Engineering Lead | Added explicit failure-mode implementation requirements (backend crash, restart policy, version negotiation, protocol compatibility, IPC timeout strategy) to EBG-0050, per ChatGPT Engineering Reviewer's ESR-0017 WP1 Recommendation 3. |
| 1.13 | 9 July 2026 | Claude Engineering Lead | Added EBG-0050 (UXP-Backend Bridge Implementation) per ADR-0019 / ESR-0017 WP1. |
| 1.12 | 9 July 2026 | Claude Engineering Reviewer | Added EBG-0049 (Cost-Aware Provider Routing and PEM-001 Revisit) per Programme Sponsor request following post-ESR-0016A discussion on balancing JARVIS running cost against performance. Cross-referenced with EBG-0045 (overlapping scope, not a duplicate) in both directions. |
| 1.11 | 8 July 2026 | Claude Engineering Implementer | Marked EBG-0030 Sentinel Architecture Specification Completed, satisfied by ADR-0018 and the Guardian/Sentinel boundary defined in ESR-0014. EBG-0047 left as Candidate Backlog - trust tiers and platform-entry validation are not confidently satisfied by the current Sentinel Core implementation. |
| 1.10 | 2 July 2026 | Codex Engineering Implementer | Added retrospective OSE relationships to improve semantic traceability without changing backlog governance. |
| 1.9 | 2 July 2026 | Codex Engineering Implementer | Completed EBG-0039 by moving prototype JARVIS chat exports into logs/chats/ runtime evidence archive. |
| 1.8 | 2 July 2026 | Codex Engineering Implementer | Added ESR-0008 closure candidate backlog items for UXP, Guardian identity, Agent Framework, Engineering Ecosystem Synchronisation, Obsidian/OSE, strategic value, device independence, Sentinel and Guardian governance. |
| 1.7 | 1 July 2026 | Programme Sponsor & Chief Engineering Advisor | Added ESR-0006 follow-up backlog items for AIEMS standards review, JARVIS runtime chat archive and repository integrity troubleshooting playbook. |
| 1.6 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added ESR-0005 closure backlog items for export workflow, product roadmaps, Sentinel and Guardian architecture, context activation and engineering package authority guidance. |
| 1.5 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added recovered knowledge promotion candidate backlog items from ESR-0004 EIP-EKR-0001. |
| 1.4 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Marked STD-0004 Validation and Quality Assurance Standard backlog item completed following ESR-0004 EIP-ESR0004-02. |
| 1.3 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added deferred candidate backlog item for future WP0 naming consideration following ESR-0004 WP3. |
| 1.2 | 28 June 2026 | Programme Sponsor & Chief Engineering Advisor | Consolidated future validation, capability, automation and EIP/session standardisation backlog themes from ESR-0003 EIP-R4. |
| 1.1 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Marked ADR-0004 and ADR-0005 recovery backlog items completed following ESR-0003 EIP-R2. |
| 1.0 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Engineering Backlog Register created with ESR-0001 deferred work items. |

---
