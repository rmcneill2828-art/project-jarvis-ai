# REG-0001 - Controlled Artefact Register

> *"You cannot govern what you cannot identify."*

**Version:** 3.45

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
| CHR-0001 | Charter | Platform Charter | 2.2 | In Review | Programme Sponsor | - | `aiems/governance/charters/` |
| CHR-0002 | Charter | Engineering Constitution | 2.2 | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/charters/` |
| ADR-0001 | Architecture Decision Record | Documentation First | 2.1 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0002 | Architecture Decision Record | Git Repository Strategy | 2.1 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0003 | Architecture Decision Record | RTBO Engineering Decision Framework | 2.1 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0004 | Architecture Decision Record | AI Repository Interaction Policy | 1.1 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0005 | Architecture Decision Record | AIEMS Strategic Scope | 1.1 | Approved | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0006 | Architecture Decision Record | Introduction of Playbooks as a Controlled Governance Artefact | 1.1 | Draft | Programme Sponsor | CHR-0002 | `aiems/governance/decisions/` |
| ADR-0007 | Architecture Decision Record | User Experience Platform Selection | 1.0 | Approved | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/decisions/` |
| ADR-0008 | Architecture Decision Record | Hybrid AI Runtime Strategy | 1.0 | Approved | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/decisions/` |
| ADR-0009 | Architecture Decision Record | Sentinel Gate of Durin Pattern | 1.0 | Approved | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/decisions/` |
| ADR-0010 | Architecture Decision Record | Guardian Identity and HITL Governance | 1.0 | Approved | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/decisions/` |
| ADR-0011 | Architecture Decision Record | Agent Framework | 1.0 | Approved | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/decisions/` |
| ADR-0012 | Architecture Decision Record | Device Independence and Portable Restore | 1.0 | Approved | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/decisions/` |
| ADR-0013 | Architecture Decision Record | Engineering Ecosystem Synchronisation | 1.0 | Approved | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/decisions/` |
| REG-0001 | Register | Controlled Artefact Register | 3.45 | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| REG-0002 | Register | Architectural Decision Register | 2.7 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| REG-0003 | Register | Risk Register | 2.2 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| REG-0004 | Register | Action Register | 2.4 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| EBR-0001 | Register | Engineering Backlog Register | 1.11 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| STD-0001 | Standard | Controlled Artefact Standard | 1.3 | Approved | Programme Sponsor | CHR-0002 | `aiems/standards/` |
| STD-0002 | Standard | Engineering Documentation Standard | 1.2 | Approved | Programme Sponsor | CHR-0002 | `aiems/standards/` |
| STD-0003 | Standard | Software / Python Engineering Standard | 1.1 | Approved | Programme Sponsor | CHR-0002 | `aiems/standards/` |
| STD-0004 | Standard | Validation and Quality Assurance Standard | 1.2 | Approved | Programme Sponsor | CHR-0002 | `aiems/standards/` |
| TPL-0001 | Template | Engineering Execution Package Template | 0.2 | Draft | Programme Sponsor & Chief Engineering Advisor | CHR-0002 | `aiems/templates/` |
| RBL-0004 | Repository Baseline | ESR-0004 Repository Baseline | 1.0 | Accepted | Programme Sponsor | CHR-0001 | `aiems/governance/baselines/` |
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Repository Baseline | ESR-0006 Repository Baseline | 1.0 | Accepted | Programme Sponsor | CHR-0001 | `aiems/governance/baselines/` |
| RBL-0008 | Repository Baseline | ESR-0007 Repository Baseline | 1.0 | Accepted | Programme Sponsor | CHR-0001 | `aiems/governance/baselines/` |
| RBL-0009 | Repository Baseline | ESR-0008 Repository Baseline | 1.0 | Accepted | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/baselines/` |
| RBL-0010 | Repository Baseline | ESR-0009 Repository Baseline | 1.0 | Accepted | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/baselines/` |
| RBL-0011 | Repository Baseline | ESR-0015 Repository Baseline | 0.1 | Draft | Programme Sponsor & Chief Engineering Advisor | ESR-0015 | `aiems/governance/baselines/` |
| PCB-0001 | Product Capability Baseline | Product Capability Baseline | 1.0 | Accepted | Programme Sponsor | JARVIS_PRODUCT_ARCHITECTURE | `aiems/governance/baselines/` |
| MOD-0001 | Model | Platform Architecture Model | 1.4 | In Review | Programme Sponsor | CHR-0002 | `aiems/models/` |
| SAM-0001 | Model | Sentinel Trust Architecture | 0.2 | Draft | Programme Sponsor & Chief Engineering Advisor | MOD-0001 | `aiems/models/` |
| AAM-0001 | Model | Guardian Identity and Cognitive Architecture | 0.2 | Draft | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/models/` |
| UAM-0001 | Model | Guardian Experience Architecture v1.0 | 1.1 | Approved Baseline | Programme Sponsor & Chief Engineering Advisor | AAM-0001 | `aiems/models/` |
| PVTM-0001 | Traceability Model | Product Vision Traceability Model | 0.3 | Draft | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/traceability/` |
| REV-0001 | Review | Phase 0 Gate Review | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| ERR-0001 | Review | Engineering Recovery Report | 0.3 | Draft | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/reviews/` |
| EIR-0001 | Review | Engineering Implementation Recommendation | 0.3 | Draft | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/governance/reviews/` |
| OSE-0001 | Engineering Assessment | Organic Semantic Enhancement Update Rule | 0.1 | Draft | Programme Sponsor & Chief Engineering Advisor | ADR-0013 | `aiems/governance/reviews/` |
| SAR-0001 | Strategic Alignment Review | Phase 1 Strategic Alignment Review | 1.0 | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| AIE-0001 | Review | AI Engineering Workflow Evaluation | Unversioned Draft | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| FE-0001 | Engineering Feature | First Executable JARVIS Component | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| FE-0002 | Engineering Feature | Platform Lifecycle Foundation | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| FE-0003 | Engineering Feature | Introduction of Playbooks as a Controlled Governance Artefact | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| FE-0004 | Engineering Feature | Populate PBK-0001 AI Engineering Playbook (Part I) | 1.0 | Complete | Programme Sponsor | PBK-0001 | `aiems/governance/reviews/` |
| FE-0005 | Engineering Feature | Engineering Review of PBK-0001 AI Engineering Playbook (Part I) | 1.0 | Complete | Programme Sponsor | PBK-0001 | `aiems/governance/reviews/` |
| FE-0006 | Engineering Feature | Populate PBK-0001 AI Engineering Playbook (Part II - Operational Engineering Workflow) | 1.0 | Complete | Programme Sponsor | PBK-0001 | `aiems/governance/reviews/` |
| FE-0007 | Engineering Feature | Approved Implementation of PBK-0001 AI Engineering Playbook (Part II) | 1.0 | Complete | Programme Sponsor | PBK-0001 | `aiems/governance/reviews/` |
| PBK-0001 | Playbook | AI Engineering Playbook | 1.15 | Draft | Programme Sponsor | CHR-0002 | `aiems/governance/playbooks/` |
| COC-0001 | Conversation Operating Context | Human-AI Collaboration Context | 1.9 | Draft | Programme Sponsor | CHR-0002 | `aiems/governance/conversation/` |
| GDE-0001 | Guide | Project Knowledge Map | 1.1 | Approved | Programme Sponsor | ESR-0014 | `aiems/guides/` |
| RBA-0001 | Repository Baseline Assessment | ESR-0004 Repository Baseline Assessment | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| RPCA-0001 | Repository Product Capability Assessment | Repository Product Capability Assessment | 1.0 | Complete | Programme Sponsor | ESR-0007 | `aiems/governance/reviews/` |
| PST-0001 | Programme Status | Programme Status | 2.20 | Approved | Programme Sponsor | CHR-0001 | `aiems/governance/status/` |
| PEM-001 | Evaluation Matrix | AI Provider Evaluation Matrix | 1.0 | Approved | Programme Sponsor & Chief Engineering Advisor | ESR-0014 | `aiems/evaluations/` |
| ESR-0001 | Engineering Session Report | Engineering Session Report | 1.1 | Completed | Programme Sponsor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0002 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0003 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0004 | Engineering Session Report | Engineering Session Report | 1.1 | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0005 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0005-RELOAD | Session Reload Snapshot | Engineering Session Reload | 1.0 | Superseded | Programme Sponsor & Chief Engineering Advisor | ESR-0005 | `aiems/governance/status/` |
| ESR-0006 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0007 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0008 | Engineering Session Report | Engineering Session Report | 1.1 | Closed | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0009 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0010 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0011 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0012 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0013 | Engineering Session Report | Engineering Session Report | 0.1 | Closure Review | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0014 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0014A | Engineering Session Report | Post-Closure Engineering Addendum - Knowledge Tiering | 1.0 | Accepted Addendum | Programme Sponsor & Chief Engineering Advisor | ESR-0014 | `aiems/governance/sessions/` |
| ESR-0015 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/sessions/` |
| HST-0001 | Historical Session Record | ESR-0001 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0001 | `aiems/History/` |
| HST-0002 | Historical Session Record | ESR-0002 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0002 | `aiems/History/` |
| HST-0003 | Historical Session Record | ESR-0003 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0003 | `aiems/History/` |
| HST-0004 | Historical Session Record | ESR-0004 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0004 | `aiems/History/` |
| HST-0005 | Historical Session Record | ESR-0005 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0005 | `aiems/History/` |
| HST-0006 | Historical Session Record | ESR-0006 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0006 | `aiems/History/` |
| HST-0007 | Historical Session Record | ESR-0007 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0007 | `aiems/History/` |
| HST-0008 | Historical Session Record | ESR-0008 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/History/` |
| HST-0009 | Historical Session Record | ESR-0009 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0009 | `aiems/History/` |
| HST-0010 | Historical Session Record | ESR-0010 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0010 | `aiems/History/` |
| HST-0011 | Historical Session Record | ESR-0011 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0011 | `aiems/History/` |
| HST-0012 | Historical Session Record | ESR-0012 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0012 | `aiems/History/` |
| HST-0013 | Historical Session Record | ESR-0013 Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0013 | `aiems/History/` |
| FCH-0000 | Full Chat Historical Evidence | Initial Project Full Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | Initial Project Session | `aiems/History/Full Chat/` |
| FCH-0001 | Full Chat Historical Evidence | ESR-0001 Full Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0001 | `aiems/History/Full Chat/` |
| FCH-0002 | Full Chat Historical Evidence | ESR-0002 Full Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0002 | `aiems/History/Full Chat/` |
| FCH-0003 | Full Chat Historical Evidence | ESR-0003 Full Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0003 | `aiems/History/Full Chat/` |
| FCH-0004 | Full Chat Historical Evidence | ESR-0004 Full Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0004 | `aiems/History/Full Chat/` |
| FCH-0005 | Full Chat Historical Evidence | ESR-0005 Full Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0005 | `aiems/History/Full Chat/` |
| FCH-0006 | Full Chat Historical Evidence | ESR-0006 Full Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0006 | `aiems/History/Full Chat/` |
| FCH-0007 | Full Chat Historical Evidence | ESR-0007 Full Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0007 | `aiems/History/Full Chat/` |
| FCH-0008 | Full Chat Historical Evidence | ESR-0008 Full Chat Review History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/History/Full Chat/` |
| FCH-0009 | Full Chat Historical Evidence | ESR-0009 Full Chat Review Issue History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0009 | `aiems/History/Full Chat/` |
| FCH-0010 | Full Chat Historical Evidence | ESR-0010 Full Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0010 | `aiems/History/Full Chat/` |
| FCH-0011 | Full Chat Historical Evidence | ESR-0011 Full Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0011 | `aiems/History/Full Chat/` |
| FCH-0012 | Full Chat Historical Evidence | ESR-0012 Full Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0012 | `aiems/History/Full Chat/` |
| FCH-0013 | Full Chat Historical Evidence | ESR-0013 Full Chat History | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0013 | `aiems/History/Full Chat/` |

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
| [[HST-0013_ESR-0013_CHAT_HISTORY|HST-0013]] | Historical session record preserving the ESR-0013 chat summary. |
| [[FCH-0013_ESR-0013_FULL_CHAT_HISTORY|FCH-0013]] | Full chat historical evidence record preserving the ESR-0013 Engineering Agent transcript and independent review findings transcript. |
| [[ESR-0013_ENGINEERING_SESSION_REPORT|ESR-0013]] | Engineering session report prepared for ESR-0013 closure review. |
| [[HST-0012_ESR-0012_CHAT_HISTORY|HST-0012]] | Historical session record preserving the ESR-0012 chat summary. |
| [[FCH-0012_ESR-0012_FULL_CHAT_HISTORY|FCH-0012]] | Full chat historical evidence record preserving the ESR-0012 full chat transcript. |
| [[ESR-0012_ENGINEERING_SESSION_REPORT|ESR-0012]] | Engineering session report recording ESR-0012 closure, GIA-BOOT Proof of Concept completion and AIEMS Engineering Agent validation. |
| [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] | Current accepted ESR-0009 repository baseline and ESR-0010 handover point. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Previous accepted ESR-0008 repository baseline and ESR-0009 starting point. |
| [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] | Previous ESR-0007 repository baseline registered as a controlled artefact. |
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Previous ESR-0006 repository baseline. |
| [[RBL-0006_REPOSITORY_BASELINE|RBL-0006]] | Previous accepted repository baseline and source baseline for ESR-0006. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records follow-up engineering backlog items associated with ESR-0006 repository readiness and OSE outcomes. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status artefact that consumes the current controlled repository baseline context. |
| [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]] | Defines the retrospective OSE enrichment rule for future controlled artefact updates. |
| [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] | Repository product capability assessment registered during ESR-0007 closure. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Product capability baseline registered during ESR-0007 closure. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|-------------------------------|------------------------------------------------------------|
| 3.45 | 8 July 2026 | Claude Engineering Implementer | ESR-0015 closed (status Open to Closed, version 1.0). Registered RBL-0011 (Draft, recommended pending Programme Sponsor acceptance). Aligned PST-0001 version following ESR-0015 closure update. |
| 3.44 | 8 July 2026 | Claude Engineering Implementer | Aligned ESR-0015 version following WP5 completion record and evidence table. |
| 3.43 | 8 July 2026 | Claude Engineering Implementer | Aligned ESR-0015 version following WP4 completion record. |
| 3.42 | 8 July 2026 | Claude Engineering Implementer | Registered PEM-001 as Approved (1.0) following ESR-0015 WP3a decision outcome; aligned ESR-0015 version following WP3a/WP3b completion record. |
| 3.41 | 8 July 2026 | Claude Engineering Implementer | Aligned ESR-0015 version following WP2 completion record. |
| 3.40 | 8 July 2026 | Claude Engineering Implementer | Aligned ESR-0015 version following WP1 completion record. |
| 3.39 | 8 July 2026 | Claude Engineering Implementer | Aligned PST-0001 version following ESR-0015 opening update. |
| 3.38 | 8 July 2026 | Claude Engineering Implementer | Registered ESR-0015, opened following WP0A/WP0B completion under the EE-0001 Lead/Reviewer trial. |
| 3.37 | 8 July 2026 | Claude Engineering Implementer | Registered ESR-0005-RELOAD (aiems/governance/status/ESR-0005_ENGINEERING_SESSION_RELOAD.md), a previously unregistered historical session-reload snapshot superseded by PST-0001. Note: its compound ID falls outside check_controlled_register's strict PREFIX-NNNN pattern, so it is not mechanically re-verified by that check - same characteristic as the pre-existing RBR-ESR0009-001 entry. |
| 3.36 | 8 July 2026 | Claude Engineering Implementer | Aligned AAM-0001 and UAM-0001 versions following addition of Subsequent Architectural Update notes pointing to ADR-0018 and CURRENT_ARCHITECTURE.md. |
| 3.35 | 8 July 2026 | Claude Engineering Implementer | Aligned SAM-0001 and MOD-0001 versions following addition of Subsequent Architectural Update notes pointing to ADR-0018 and CURRENT_ARCHITECTURE.md. |
| 3.34 | 8 July 2026 | Claude Engineering Implementer | Aligned REG-0002, EBR-0001 and GDE-0001 versions following ADR-0018 registration in REG-0002, EBG-0030 reclassification in EBR-0001 and GDE-0001 Draft/1.0 versioning correction. |
| 3.33 | 8 July 2026 | Claude Engineering Implementer | Registered PEM-001 AI Provider Evaluation Matrix, brought into STD-0001 structural compliance; aligned PST-0001 version following residual product-naming and Session Start Guidance completeness fixes. |
| 3.32 | 8 July 2026 | Claude Engineering Implementer | Aligned COC-0001, PBK-0001 and TPL-0001 versions following role-definition generalisation (ChatGPT/Codex to Engineering Reviewer/Engineering Implementer). |
| 3.31 | 8 July 2026 | Claude Engineering Implementer | Aligned PST-0001 version following ESR-0014/ESR-0014A closure content update and validate_repository.py staleness-check correction. |
| 3.30 | 8 July 2026 | Claude Engineering Implementer | Registered ESR-0014, ESR-0014A post-closure addendum and GDE-0001 Project Knowledge Map; aligned PBK-0001 and COC-0001 versions following knowledge tiering introduction. |
| 3.29 | 7 July 2026 | Engineering Agent | Registered HST-0013 and FCH-0013 ESR-0013 history artefacts and aligned PBK-0001 / README WP0 session start guidance. |
| 3.28 | 7 July 2026 | Engineering Agent | Registered ESR-0013 closure review report and aligned PST-0001 metadata for ESR-0013 closure preparation. |
| 3.27 | 6 July 2026 | Codex Engineering Implementer | Registered HST-0012 and FCH-0012 ESR-0012 history artefacts and aligned PBK-0001 / README WP0 session start guidance. |
| 3.26 | 6 July 2026 | Codex Engineering Implementer | Registered ESR-0012 Engineering Session Report and aligned PST-0001 metadata for ESR-0012 closure. |
| 3.25 | 5 July 2026 | Codex Engineering Implementer | Registered HST-0011 and FCH-0011 ESR-0011 history artefacts and aligned PBK-0001 / README WP0 session start guidance. |
| 3.24 | 5 July 2026 | Codex Engineering Implementer | Registered ESR-0011 Engineering Session Report and aligned programme status for ESR-0011 closure and ESR-0012 implementation handover. |
| 3.23 | 4 July 2026 | Codex Engineering Implementer | Registered FCH-0000 through FCH-0010 Full Chat historical evidence artefacts and aligned PBK-0001 WP0 session start guidance. |
| 3.22 | 4 July 2026 | Codex Engineering Implementer | Registered HST-0001 through HST-0010 AIEMS History artefacts and aligned PBK-0001 WP0 session start guidance. |
| 3.21 | 4 July 2026 | Codex Engineering Implementer | Registered ESR-0010 Engineering Session Report and aligned programme status for ESR-0010 closure. |
| 3.20 | 4 July 2026 | Codex Engineering Implementer | Registered ESR-0005 and ESR-0006 and corrected repository status alignment for ESR-0010 closure. |
| 3.19 | 3 July 2026 | Codex Engineering Implementer | Registered RBL-0010 as the accepted ESR-0009 repository baseline and aligned PST-0001 version. |
| 3.18 | 3 July 2026 | Codex Engineering Implementer | Registered ESR-0009 Engineering Session Report following ESR-0009 closure. |
| 3.17 | 2 July 2026 | Codex Engineering Implementer | Registered SAM-0001 Sentinel Trust Architecture and UAM-0001 Guardian Experience Architecture v1.0. |
| 3.16 | 2 July 2026 | Codex Engineering Implementer | Registered TPL-0001 Engineering Execution Package Template created under EIP-ESR0009-002. |
| 3.15 | 2 July 2026 | Codex Engineering Implementer | Aligned Phase 5 decision, backlog and status artefact versions following retrospective OSE enrichment. |
| 3.14 | 2 July 2026 | Codex Engineering Implementer | Aligned Phase 4 governance backbone artefact versions following retrospective OSE enrichment. |
| 3.13 | 2 July 2026 | Codex Engineering Implementer | Aligned ADR-0001 through ADR-0006 versions following Phase 3 retrospective OSE enrichment. |
| 3.12 | 2 July 2026 | Codex Engineering Implementer | Aligned MOD-0001, PBK-0001 and COC-0001 versions following Phase 2 OSE enrichment. |
| 3.11 | 2 July 2026 | Codex Engineering Implementer | Registered OSE-0001 Organic Semantic Enhancement Update Rule for Phase 1 retrospective OSE enrichment. |
| 3.10 | 2 July 2026 | Codex Engineering Implementer | Aligned controlled artefact versions and OSE relationship wording following ESR-0009 readiness pass. |
| 3.9 | 2 July 2026 | Codex Engineering Implementer | Corrected ESR-0004 registered version after repository validation script detected metadata drift. |
| 3.8 | 2 July 2026 | Codex Engineering Implementer | Aligned EBR-0001 and PST-0001 metadata after completing EBG-0039 JARVIS Runtime Chat Archive. |
| 3.7 | 2 July 2026 | Codex Engineering Implementer | Aligned MOD-0001 metadata after Guardian, Sentinel and Platform Services architectural reconciliation. |
| 3.6 | 2 July 2026 | Codex Engineering Implementer | Registered RBL-0009, closed ESR-0008 metadata and aligned PST-0001 following ESR-0008 baseline acceptance. |
| 3.5 | 2 July 2026 | Codex Engineering Implementer | Aligned PST-0001 metadata following ESR-0008 closure and ESR-0009 readiness update. |
| 3.4 | 2 July 2026 | Codex Engineering Implementer | Registered ESR-0008 closure artefacts including AAM-0001, ADR-0007 through ADR-0013 and ESR-0008, and aligned updated artefact versions. |
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
