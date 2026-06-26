# REG-0001 – Controlled Artefact Register

> *"You cannot govern what you cannot identify."*

**Version:** 1.3

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
    │
    ▼
In Review
    │
    ▼
Approved
    │
    ▼
Baselined
    │
    ▼
Superseded
    │
    ▼
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

Repository integrity shall be verified during Repository Hygiene activities and Engineering Assurance Reviews.

---

# Controlled Artefact Register

| Artefact ID | Artefact Type | Title | Version | Status | Owner | Parent | Repository Location |
|--------------|---------------|-------|---------|------------|----------------------|----------------|--------------------------------|
| CHR-0001 | Charter | Platform Charter | 2.1 | In Review | Programme Sponsor | - | `aiems/governance/charters/` |
| CHR-0002 | Charter | Engineering Constitution | 2.1 | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/charters/` |
| ADR-0001 | Architecture Decision Record | Documentation First | 2.0 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0002 | Architecture Decision Record | Git Repository Strategy | 2.0 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0003 | Architecture Decision Record | RTBO Engineering Decision Framework | 2.0 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0006 | Architecture Decision Record | Introduction of Playbooks as a Controlled Governance Artefact | 1.0 | Draft | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| REG-0001 | Register | Controlled Artefact Register | 1.3 | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| REG-0002 | Register | Architectural Decision Register | 2.3 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| REG-0003 | Register | Risk Register | 2.1 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| REG-0004 | Register | Action Register | 2.2 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| STD-0001 | Standard | Controlled Artefact Standard | 1.0 | In Review | Programme Sponsor | CHR-0002 | `aiems/standards/` |
| STD-0002 | Standard | Engineering Documentation Standard | 1.0 | In Review | Programme Sponsor | CHR-0002 | `aiems/standards/` |
| MOD-0001 | Model | Platform Architecture Model | 1.0 | Draft | Programme Sponsor | CHR-0002 | `aiems/models/` |
| REV-0001 | Review | Phase 0 Gate Review | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| SAR-0001 | Strategic Alignment Review | Phase 1 Strategic Alignment Review | 1.0 | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| AIE-0001 | Review | AI Engineering Workflow Evaluation | Unversioned Draft | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| FE-0001 | Engineering Feature | First Executable JARVIS Component | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| FE-0002 | Engineering Feature | Platform Lifecycle Foundation | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| FE-0003 | Engineering Feature | Introduction of Playbooks as a Controlled Governance Artefact | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| FE-0004 | Engineering Feature | Populate PBK-0001 AI Engineering Playbook (Part I) | 1.0 | Complete | Programme Sponsor | PBK-0001 | `aiems/governance/reviews/` |
| FE-0005 | Engineering Feature | Engineering Review of PBK-0001 AI Engineering Playbook (Part I) | 1.0 | Complete | Programme Sponsor | PBK-0001 | `aiems/governance/reviews/` |
| FE-0006 | Engineering Feature | Populate PBK-0001 AI Engineering Playbook (Part II - Operational Engineering Workflow) | 1.0 | Complete | Programme Sponsor | PBK-0001 | `aiems/governance/reviews/` |
| FE-0007 | Engineering Feature | Approved Implementation of PBK-0001 AI Engineering Playbook (Part II) | 1.0 | Complete | Programme Sponsor | PBK-0001 | `aiems/governance/reviews/` |
| PBK-0001 | Playbook | AI Engineering Playbook | 1.0 | Draft | Programme Sponsor | CHR-0002 | `aiems/governance/playbooks/` |
| COC-0001 | Conversation Operating Context | Human-AI Collaboration Context | 1.0 | Draft | Programme Sponsor | CHR-0002 | `aiems/governance/conversation/` |

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

# Engineering Assurance

Engineering Assurance Reviews (EAR) shall verify that:

- Every Controlled Artefact is present within this Register.
- Metadata accurately reflects the current repository baseline.
- Repository locations remain valid.
- Parent artefact relationships remain accurate.
- Governance status reflects the current approved state.

Any discrepancies identified during an Engineering Assurance Review shall be corrected before the Platform baseline is updated.

---

# Guiding Principle

The Controlled Artefact Register is the authoritative catalogue of the AI Engineering Platform.

If a Controlled Artefact is not recorded within this Register, it shall not be regarded as part of the approved Platform baseline.

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|-------------------------------|------------------------------------------------------------|
| 1.3 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Reconciled controlled artefact register with current repository baseline, registered FE and COC artefacts, and updated register version references. |
| 1.2 | 25 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered ADR-0006 and PBK-0001 for the introduction of Playbooks as a controlled governance artefact. |
| 1.1 | 25 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered AIE-0001 as a controlled governance review artefact. |
| 1.0 | 24 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Controlled Artefact Register established following the AI Engineering Platform repository refactor. |
