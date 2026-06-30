# EBR-0001 - Engineering Backlog Register

> *"Deferred work remains governed work."*

**Version:** 1.6

---

# 1. Document Control

| Field | Value |
|------|-------|
| Artefact ID | EBR-0001 |
| Title | Engineering Backlog Register |
| Version | 1.6 |
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
| EBG-0028 | GUI Evolution Roadmap | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Define staged GUI maturity from First Light through operational workspace and future product surfaces. |
| EBG-0029 | Product Growth Philosophy | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Record the principle that JARVIS grows by acquiring capabilities rather than accumulating features. |
| EBG-0030 | Sentinel Architecture Specification | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define Sentinel responsibilities, boundaries and relationship to Guardian before Sentinel implementation. |
| EBG-0031 | Guardian Architecture Specification | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define Guardian safety, permission, approval and protection boundaries before Guardian implementation. |
| EBG-0032 | Historical Engineering Register | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Consider a controlled register for historically significant engineering baselines, tags and milestones. |
| EBG-0033 | AIEMS Improvement Register / AIEMS Improvement Review | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Define a controlled mechanism for recording AIEMS process improvements without disrupting active engineering flow. |
| EBG-0034 | Engineering Authority by Work Package | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define authority boundaries by work package type so implementation, assessment, correction and verification packages remain distinct. |
| EBG-0035 | Context Activation Guidance | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define how package context, repository baseline, role authority and relevant artefacts are activated before execution or verification. |
| EBG-0036 | WP6 Repository Content Verification Standard | ESR-0005 closure recommendation | Candidate Backlog | High | Programme Sponsor | Define repeatable WP6 repository content verification expectations, evidence requirements and reporting structure. |
| EBG-0037 | Engineering Package Classifications: EIP / EAP / ECP | ESR-0005 closure recommendation | Candidate Backlog | Medium | Programme Sponsor | Define controlled package classifications for Engineering Implementation Packages, Engineering Assessment Packages and Engineering Corrective Packages. |

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

# 10. Maintenance

The Engineering Backlog Register shall be reviewed:

- At engineering session transition.
- When deferred work is identified during session closure.
- When candidate backlog items are submitted for Programme Sponsor review.
- When backlog items are accepted, merged, superseded, rejected, deferred or completed.
- When the Programme Sponsor directs a backlog review.

Updates to this register shall preserve unique backlog identifiers and maintain traceability to source artefacts where known.

---

# 11. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.6 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added ESR-0005 closure backlog items for export workflow, product roadmaps, Sentinel and Guardian architecture, context activation and engineering package authority guidance. |
| 1.5 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added recovered knowledge promotion candidate backlog items from ESR-0004 EIP-EKR-0001. |
| 1.4 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Marked STD-0004 Validation and Quality Assurance Standard backlog item completed following ESR-0004 EIP-ESR0004-02. |
| 1.3 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added deferred candidate backlog item for future WP0 naming consideration following ESR-0004 WP3. |
| 1.2 | 28 June 2026 | Programme Sponsor & Chief Engineering Advisor | Consolidated future validation, capability, automation and EIP/session standardisation backlog themes from ESR-0003 EIP-R4. |
| 1.1 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Marked ADR-0004 and ADR-0005 recovery backlog items completed following ESR-0003 EIP-R2. |
| 1.0 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Engineering Backlog Register created with ESR-0001 deferred work items. |

---
