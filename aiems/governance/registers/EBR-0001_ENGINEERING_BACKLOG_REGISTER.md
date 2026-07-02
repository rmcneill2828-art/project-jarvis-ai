# EBR-0001 - Engineering Backlog Register

> *"Deferred work remains governed work."*

**Version:** 1.8

---

# 1. Document Control

| Field | Value |
|------|-------|
| Artefact ID | EBR-0001 |
| Title | Engineering Backlog Register |
| Version | 1.8 |
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
| EBG-0028 | UXP Evolution Roadmap | ESR-0005 closure recommendation; ESR-0008 terminology alignment | Candidate Backlog | Medium | Programme Sponsor | Define staged User Experience Platform maturity from First Light through operational workspace and future product surfaces. GUI is preserved as the historical alias for earlier presentation-layer work. |
| EBG-0029 | Product Growth Philosophy | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Record the principle that JARVIS grows by acquiring capabilities rather than accumulating features. |
| EBG-0030 | Sentinel Architecture Specification | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define Sentinel responsibilities, boundaries and relationship to Guardian before Sentinel implementation. |
| EBG-0031 | Guardian Architecture Specification | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define Guardian safety, permission, approval and protection boundaries before Guardian implementation. |
| EBG-0032 | Historical Engineering Register | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Consider a controlled register for historically significant engineering baselines, tags and milestones. |
| EBG-0033 | AIEMS Improvement Register / AIEMS Improvement Review | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Define a controlled mechanism for recording AIEMS process improvements without disrupting active engineering flow. |
| EBG-0034 | Engineering Authority by Work Package | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define authority boundaries by work package type so implementation, assessment, correction and verification packages remain distinct. |
| EBG-0035 | Context Activation Guidance | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define how package context, repository baseline, role authority and relevant artefacts are activated before execution or verification. |
| EBG-0036 | WP6 Repository Content Verification Standard | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define repeatable WP6 repository content verification expectations, evidence requirements and reporting structure. |
| EBG-0037 | Engineering Package Classifications: EIP / EAP / ECP | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Define controlled package classifications for Engineering Implementation Packages, Engineering Assessment Packages and Engineering Corrective Packages. |
| EBG-0038 | Formal AIEMS Standards Review | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]]; ESR-0006 continuous improvement | Candidate Backlog | High | Programme Sponsor | Validate CI-0001 through CI-0007 and determine which ESR-0006 working practices require formal standardisation. Rationale: preserves AIEMS improvement discipline while avoiding premature standard creation. |
| EBG-0039 | JARVIS Runtime Chat Archive | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]]; ESR-0006 repository readiness classification | Candidate Backlog | High | Programme Sponsor | Define and implement the approved future runtime archive location for JARVIS chat exports under `JARVIS/Logs/Chats/`, including handling of `Jarvis one.md` and `Jarvis two.md`. Rationale: separates product runtime artefacts from AIEMS controlled artefacts while preserving export evidence. |
| EBG-0040 | AIEMS Repository Integrity Troubleshooting Playbook | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]]; ESR-0006 repository readiness review | Candidate Backlog | Medium | Programme Sponsor | Create practical troubleshooting guidance for environmental Git status, line-ending normalization, ignored workspace state and baseline-readiness checks. Rationale: captures repeatable repository integrity learning from ESR-0006. |
| EBG-0041 | Guardian Identity Architecture Validation | [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Candidate Backlog | High | Programme Sponsor | Validate [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] and determine implementation sequencing for Guardian identity and faculties. |
| EBG-0042 | Agent Framework Architecture | [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]]; [[ADR-0011_AGENT_FRAMEWORK|ADR-0011]] | Candidate Backlog | High | Programme Sponsor | Define specialist agent contracts, including Engineering Agent, while preserving Guardian as the singular user-facing identity. |
| EBG-0043 | Engineering Ecosystem Synchronisation Workflow | [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Candidate Backlog | High | Programme Sponsor | Define repeatable WP0 workflow covering GitHub, AIEMS, OSE, Obsidian, registers, controlled artefacts, previous ESRs and summaries. |
| EBG-0044 | Obsidian / OSE Validation Workflow | [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Candidate Backlog | Medium | Programme Sponsor | Define how Obsidian as the human-facing Engineering Knowledge Workspace validates and navigates repository Markdown without replacing GitHub as source of truth. |
| EBG-0045 | Cost and Strategic Value Framework | [[ADR-0008_HYBRID_AI_RUNTIME_STRATEGY|ADR-0008]] | Candidate Backlog | High | Programme Sponsor | Define evaluation criteria for cloud providers, commercial options, cost, privacy, strategic value and product benefit. |
| EBG-0046 | Device Independence and Restore Architecture | [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]] | Candidate Backlog | High | Programme Sponsor | Define bootstrap, progressive restore, portable memory, configuration and encrypted sync requirements. |
| EBG-0047 | Sentinel Gate of Durin Architecture Specification | [[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]] | Candidate Backlog | High | Programme Sponsor | Extend EBG-0030 with Sentinel trust gateway, trust tiers and platform-entry validation details. |
| EBG-0048 | Guardian HITL Governance Specification | [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]] | Candidate Backlog | High | Programme Sponsor | Extend EBG-0031 with consent, policy, privacy, approval, memory retention and trusted mobile approve/deny governance. |

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

# 10. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Source baseline for ESR-0006 repository readiness classification and new backlog intake. |
| [[RBL-0006_REPOSITORY_BASELINE|RBL-0006]] | Previous baseline that provided the starting point for ESR-0006. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Registers controlled artefacts whose changes may create backlog follow-up. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status context for session transition and future backlog review. |
| [[ESR-0005_ENGINEERING_SESSION_REPORT|ESR-0005]] | Source of the prototype JARVIS chat export artefacts classified during ESR-0006. |

---

# 11. Maintenance

The Engineering Backlog Register shall be reviewed:

- At engineering session transition.
- When deferred work is identified during session closure.
- When candidate backlog items are submitted for Programme Sponsor review.
- When backlog items are accepted, merged, superseded, rejected, deferred or completed.
- When the Programme Sponsor directs a backlog review.

Updates to this register shall preserve unique backlog identifiers and maintain traceability to source artefacts where known.

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
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
