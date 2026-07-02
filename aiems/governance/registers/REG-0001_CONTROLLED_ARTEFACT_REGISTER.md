# REG-0001 - Controlled Artefact Register

> *"You cannot govern what you cannot identify."*

**Version:** 3.3

---

# Purpose

The Controlled Artefact Register is the authoritative catalogue of all governed artefacts within the **AI Engineering Platform (AEP)**.

It provides the single source of truth for the identification, ownership, status and repository location of every **Controlled Artefact** managed through the **AI Engineering Management System (AIEMS)**.

The Register supports governance, engineering assurance, repository integrity and audit activities by maintaining an accurate record of the current approved Platform baseline.

---

# Scope

This Register records every Controlled Artefact that forms part of the AI Engineering Platform, including but not limited to:

- Charters
- Architecture Decision Records
- Registers
- Standards
- Policies
- Procedures
- Models
- Reviews
- Templates
- Guides
- Glossary
- Future Controlled Artefacts

Only artefacts recorded within this Register shall be considered part of the approved Platform baseline.

---

# Artefact Lifecycle

Every Controlled Artefact shall progress through the following lifecycle:

```text
Draft
    |
    v
In Review
    |
    v
Approved
    |
    v
Baselined
    |
    v
Superseded
    |
    v
Retired
```

The lifecycle ensures that every Controlled Artefact is governed, reviewed and traceable throughout its lifetime.

---

# Governance Rules

Every Controlled Artefact shall:

- Have a unique Artefact Identifier.
- Have a clearly defined Artefact Type.
- Have a single accountable Owner.
- Exist only once within the repository.
- Maintain version history.
- Record its governance status.
- Be referenced consistently throughout the Platform.
- Be recorded within this Register before becoming part of the approved Platform baseline.

---

# Repository Integrity

Repository integrity shall be verified by confirming that:

- The repository filename matches the Artefact Identifier.
- The internal document title matches the repository filename.
- The repository location is correct.
- The recorded version matches the approved version.
- Cross-references remain valid.
- The repository contains only one current version of each Controlled Artefact.

Repository integrity shall be verified during Repository Hygiene activities and Engineering Reviews.

---

# Controlled Artefact Register

| Artefact ID | Artefact Type | Title | Version | Status | Owner | Parent | Repository Location |
|--------------|---------------|-------|---------|------------|----------------------|----------------|--------------------------------|
| CHR-0001 | Charter | Platform Charter | 2.1 | In Review | Programme Sponsor | - | `aiems/governance/charters/` |
| CHR-0002 | Charter | Engineering Constitution | 2.1 | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/charters/` |
| ADR-0001 | Architecture Decision Record | Documentation First | 2.0 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0002 | Architecture Decision Record | Git Repository Strategy | 2.0 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0003 | Architecture Decision Record | RTBO Engineering Decision Framework | 2.0 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0004 | Architecture Decision Record | AI Repository Interaction Policy | 1.0 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0005 | Architecture Decision Record | AIEMS Strategic Scope | 1.0 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0006 | Architecture Decision Record | Introduction of Playbooks as a Controlled Governance Artefact | 1.0 | Draft | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| REG-0001 | Register | Controlled Artefact Register | 3.2 | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| REG-0002 | Register | Architectural Decision Register | 2.4 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| REG-0003 | Register | Risk Register | 2.1 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| REG-0004 | Register | Action Register | 2.3 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| EBR-0001 | Register | Engineering Backlog Register | 1.5 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| STD-0001 | Standard | Controlled Artefact Standard | 1.2 | Approved | Programme Sponsor | CHR-0002 | `aiems/standards/` |
| STD-0002 | Standard | Engineering Documentation Standard | 1.1 | Approved | Programme Sponsor | CHR-0002 | `aiems/standards/` |
| STD-0003 | Standard | Software / Python Engineering Standard | 1.0 | Approved | Programme Sponsor | CHR-0002 | `aiems/standards/` |
| STD-0004 | Standard | Validation and Quality Assurance Standard | 1.1 | Approved | Programme Sponsor | CHR-0002 | `aiems/standards/` |
| RBL-0004 | Repository Baseline | ESR-0004 Repository Baseline | 1.0 | Accepted | Programme Sponsor | CHR-0001 | `aiems/governance/baselines/` |
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Repository Baseline | ESR-0006 Repository Baseline | 1.0 | Accepted | Programme Sponsor | CHR-0001 | `aiems/governance/baselines/` |
| RBL-0008 | Repository Baseline | ESR-0007 Repository Baseline | 1.0 | Accepted | Programme Sponsor | CHR-0001 | `aiems/governance/baselines/` |
| PCB-0001 | Product Capability Baseline | Product Capability Baseline | 1.0 | Accepted | Programme Sponsor | JARVIS_PRODUCT_ARCHITECTURE | `aiems/governance/baselines/` |
| MOD-0001 | Model | Platform Architecture Model | 1.0 | In Review | Programme Sponsor | CHR-0002 | `aiems/models/` |
| PVTM-0001 | Traceability Model | Product Vision Traceability Model | 0.1 | Draft | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/traceability/` |
| REV-0001 | Review | Phase 0 Gate Review | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| ERR-0001 | Review | Engineering Recovery Report | 0.1 | Draft | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/reviews/` |
| EIR-0001 | Review | Engineering Implementation Recommendation | 0.1 | Draft | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/reviews/` |
| SAR-0001 | Strategic Alignment Review | Phase 1 Strategic Alignment Review | 1.0 | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| AIE-0001 | Review | AI Engineering Workflow Evaluation | Unversioned Draft | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| FE-0001 | Engineering Feature | First Executable JARVIS Component | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| FE-0002 | Engineering Feature | Platform Lifecycle Foundation | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| FE-0003 | Engineering Feature | Introduction of Playbooks as a Controlled Governance Artefact | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| FE-0004 | Engineering Feature | Populate PBK-0001 AI Engineering Playbook (Part I) | 1.0 | Complete | Programme Sponsor | PBK-0001 | `aiems/governance/reviews/` |
| FE-0005 | Engineering Feature | Engineering Review of PBK-0001 AI Engineering Playbook (Part I) | 1.0 | Complete | Programme Sponsor | PBK-0001 | `aiems/governance/reviews/` |
| FE-0006 | Engineering Feature | Populate PBK-0001 AI Engineering Playbook (Part II - Operational Engineering Workflow) | 1.0 | Complete | Programme Sponsor | PBK-0001 | `aiems/governance/reviews/` |
| FE-0007 | Engineering Feature | Approved Implementation of PBK-0001 AI Engineering Playbook (Part II) | 1.0 | Complete | Programme Sponsor | PBK-0001 | `aiems/governance/reviews/` |
| PBK-0001 | Playbook | AI Engineering Playbook | 1.7 | Draft | Programme Sponsor | CHR-0002 | `aiems/governance/playbooks/` |
| COC-0001 | Conversation Operating Context | Human-AI Collaboration Context | 1.6 | Draft | Programme Sponsor | CHR-0002 | `aiems/governance/conversation/` |
| RBA-0001 | Repository Baseline Assessment | ESR-0004 Repository Baseline Assessment | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| RPCA-0001 | Repository Product Capability Assessment | Repository Product Capability Assessment | 1.0 | Complete | Programme Sponsor | ESR-0007 | `aiems/governance/reviews/` |
| PST-0001 | Programme Status | Programme Status | 2.5 | Approved | Programme Sponsor | CHR-0001 | `aiems/governance/status/` |
| ESR-0001 | Engineering Session Report | Engineering Session Report | 1.1 | Completed | Programme Sponsor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0002 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0003 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0004 | Engineering Session Report | Engineering Session Report | 1.0 | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0007 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor | CHR-0001 | `aiems/governance/sessions/` |

---

# Register Maintenance

The Programme Sponsor is responsible for maintaining this Register.

The Register shall be reviewed whenever:

- A new Controlled Artefact is created.
- An existing Controlled Artefact changes version.
- A Controlled Artefact changes status.
- A Controlled Artefact is retired.
- Repository Hygiene activities are undertaken.

---

# Engineering Review

Engineering Reviews shall verify that:

- Every Controlled Artefact is present within this Register.
- Metadata accurately reflects the current repository baseline.
- Repository locations remain valid.
- Parent artefact relationships remain accurate.
- Governance status reflects the current approved state.

Any discrepancies identified during an Engineering Review shall be corrected before the Platform baseline is updated.

---

# Guiding Principle

The Controlled Artefact Register is the authoritative catalogue of the AI Engineering Platform.

If a Controlled Artefact is not recorded within this Register, it shall not be regarded as part of the approved Platform baseline.

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] | Current ESR-0007 repository baseline registered as a controlled artefact. |
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Previous ESR-0006 repository baseline. |
| [[RBL-0006_REPOSITORY_BASELINE|RBL-0006]] | Previous accepted repository baseline and source baseline for ESR-0006. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records follow-up engineering backlog items associated with ESR-0006 repository readiness and OSE outcomes. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status artefact that consumes the current controlled repository baseline context. |
| [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] | Repository product capability assessment registered during ESR-0007 closure. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Product capability baseline registered during ESR-0007 closure. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|-------------------------------|------------------------------------------------------------|
| 3.3 | 2 July 2026 | Codex Engineering Implementer | Registered ESR-0008 WP1 controlled artefacts PVTM-0001, ERR-0001 and EIR-0001. |
| 3.2 | 1 July 2026 | Codex Engineering Implementer | Registered ESR-0007, RPCA-0001, PCB-0001 and RBL-0008 for ESR-0007 closure. |
| 3.1 | 1 July 2026 | Programme Sponsor & Chief Engineering Advisor | Registered RBL-0007 as the accepted ESR-0006 repository baseline and added related artefact traceability. |
| 3.0 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Aligned PBK-0001, STD-0004 and PST-0001 metadata following engineering authority lifecycle clarification. |
| 2.9 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered RBL-0004 as the accepted ESR-0004 repository baseline for ESR-0005. |
| 2.8 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered RBA-0001 and ESR-0004 session report and aligned PST-0001 metadata for ESR-0005 handover. |
| 2.7 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Aligned EBR-0001 metadata following recovered knowledge promotion backlog consolidation. |
| 2.6 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered STD-0004 Validation and Quality Assurance Standard and aligned EBR-0001 and PST-0001 metadata. |
| 2.5 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Aligned PBK-0001, COC-0001, PST-0001 and EBR-0001 metadata following ESR-0004 WP3 README WP0 review update. |
| 2.4 | 28 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered ESR-0003 closure report and aligned PST-0001 metadata for repository baseline acceptance. |
| 2.3 | 28 June 2026 | Programme Sponsor & Chief Engineering Advisor | Aligned PST-0001 metadata and completed repository baseline final alignment following EBR-0002 final verification. |
| 2.2 | 28 June 2026 | Programme Sponsor & Chief Engineering Advisor | Aligned PBK-0001, COC-0001 and EBR-0001 metadata following EBR-0002 baseline review. |
| 2.1 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered recovered ADR-0004 and ADR-0005 artefacts and restored ADR traceability. |
| 2.0 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered EBR-0001 and aligned controlled artefact metadata with the current repository baseline. |
| 1.9 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered ESR-0002 Engineering Session Report artefact. |
| 1.8 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Reconciled PBK-0001 version and MOD-0001 status following repository consistency verification. |
| 1.7 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered STD-0003 Software / Python Engineering Standard. |
| 1.6 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered ESR-0001 Engineering Session Report artefact. |
| 1.5 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered PST-0001 Programme Status artefact. |
| 1.4 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered approved standards baseline and reconciled Action Register version reference. |
| 1.3 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Reconciled controlled artefact register with current repository baseline, registered FE and COC artefacts, and updated register version references. |
| 1.2 | 25 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered ADR-0006 and PBK-0001 for the introduction of Playbooks as a controlled governance artefact. |
| 1.1 | 25 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered AIE-0001 as a controlled governance review artefact. |
| 1.0 | 24 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Controlled Artefact Register established following the AI Engineering Platform repository refactor. |
