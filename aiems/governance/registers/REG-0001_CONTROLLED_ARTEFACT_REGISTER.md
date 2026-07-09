# REG-0001 - Controlled Artefact Register

> *"You cannot govern what you cannot identify."*

**Version:** 3.93

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
| ADR-0019 | Architecture Decision Record | UXP-Backend Integration Architecture | 1.1 | Approved | Programme Sponsor & Chief Engineering Advisor | ESR-0017 | `aiems/governance/decisions/` |
| REG-0001 | Register | Controlled Artefact Register | 3.93 | In Review | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| REG-0002 | Register | Architectural Decision Register | 2.8 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| REG-0003 | Register | Risk Register | 2.2 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| REG-0004 | Register | Action Register | 2.4 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
| EBR-0001 | Register | Engineering Backlog Register | 1.21 | Draft | Programme Sponsor | CHR-0001 | `aiems/governance/registers/` |
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
| RBL-0011 | Repository Baseline | ESR-0015 Repository Baseline | 1.0 | Accepted | Programme Sponsor & Chief Engineering Advisor | ESR-0015 | `aiems/governance/baselines/` |
| RBL-0012 | Repository Baseline | ESR-0017 Repository Baseline | 1.0 | Accepted | Programme Sponsor & Chief Engineering Advisor | ESR-0017 | `aiems/governance/baselines/` |
| PCB-0001 | Product Capability Baseline | Product Capability Baseline | 1.0 | Accepted | Programme Sponsor | JARVIS_PRODUCT_ARCHITECTURE | `aiems/governance/baselines/` |
| MOD-0001 | Model | Platform Architecture Model | 1.4 | In Review | Programme Sponsor | CHR-0002 | `aiems/models/` |
| SAM-0001 | Model | Sentinel Trust Architecture | 0.3 | Draft | Programme Sponsor & Chief Engineering Advisor | MOD-0001 | `aiems/models/` |
| AAM-0001 | Model | Guardian Identity and Cognitive Architecture | 0.2 | Draft | Programme Sponsor & Chief Engineering Advisor | ESR-0008 | `aiems/models/` |
| UAM-0001 | Model | Guardian Experience Architecture v1.0 | 1.4 | Approved Baseline | Programme Sponsor & Chief Engineering Advisor | AAM-0001 | `aiems/models/` |
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
| PBK-0001 | Playbook | AI Engineering Playbook | 1.19 | Draft | Programme Sponsor | CHR-0002 | `aiems/governance/playbooks/` |
| COC-0001 | Conversation Operating Context | Human-AI Collaboration Context | 1.11 | Draft | Programme Sponsor | CHR-0002 | `aiems/governance/conversation/` |
| GDE-0001 | Guide | Project Knowledge Map | 1.2 | Approved | Programme Sponsor | ESR-0014 | `aiems/guides/` |
| RBA-0001 | Repository Baseline Assessment | ESR-0004 Repository Baseline Assessment | 1.0 | Complete | Programme Sponsor | CHR-0001 | `aiems/governance/reviews/` |
| RPCA-0001 | Repository Product Capability Assessment | Repository Product Capability Assessment | 1.0 | Complete | Programme Sponsor | ESR-0007 | `aiems/governance/reviews/` |
| PST-0001 | Programme Status | Programme Status | 2.23 | Approved | Programme Sponsor | CHR-0001 | `aiems/governance/status/` |
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
| ESR-0016 | Engineering Session Report | Engineering Session Report | 1.0 | Closed | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/sessions/` |
| ESR-0016A | Engineering Session Report | Post-Closure Engineering Addendum - Governance and Tooling Improvements | 1.0 | Accepted Addendum | Programme Sponsor & Chief Engineering Advisor | ESR-0016 | `aiems/governance/sessions/` |
| ESR-0017 | Engineering Session Report | Engineering Session Report | 0.16 | Open | Programme Sponsor & Chief Engineering Advisor | CHR-0001 | `aiems/governance/sessions/` |
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
| FCH-0015 | Full Chat Historical Evidence | ESR-0015 Full Chat History (Claude) | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0015 | `aiems/History/Full Chat/` |
| FCH-0016 | Full Chat Historical Evidence | ESR-0016 Full Chat History (Claude) | 1.0 | Archived | Programme Sponsor & Chief Engineering Advisor | ESR-0016 | `aiems/History/Full Chat/` |

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
| 3.93 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.15 to 0.16) following: Updated Section 15.5: Programme Sponsor saved the mock-up image directly into the repository (aiems/models/, renamed to UAM-0001_GUARDIAN_ORB_MOCKUP.jpg for convention). UAM-0001 (now v1.4) updated to reference the real file instead of describing it as outstanding. |
| 3.92 | 9 July 2026 | Claude Engineering Lead | Aligned UAM-0001 version (1.3 to 1.4) following: Referenced the now-persisted mock-up image at aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg from Section 7.1, replacing the earlier description-only reference. |
| 3.91 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.14 to 0.15) following: Recorded Section 15.5: Programme Sponsor located and provided the actual FCH-0010/FCH-0011 mock-up image, confirming it is materially richer than the text description already incorporated. Added UAM-0001 Sections 7.1 (Reference Dashboard Composition - System Health, Knowledge Metrics, Active Clusters, Real-Time Activity, AIEMS Principles panel, persistent conversation bar) and 8.3 (Orb Status Panel - Mode/Confidence/Autonomy/Permission, tied to ADR-0010 HITL governance), both explicit design-direction-only (UAM-0001 v1.3). Noted the image file itself cannot be persisted to the repository from this environment - no mechanism exists to extract pasted image bytes to disk - and remains outstanding pending the Programme Sponsor saving it directly. |
| 3.90 | 9 July 2026 | Claude Engineering Lead | Aligned UAM-0001 version (1.2 to 1.3) following: Incorporated the actual Guardian Orb mock-up image provided by the Programme Sponsor at ESR-0017 (richer than the FCH-0010 text description already in 8.1/8.2): new Section 7.1 Reference Dashboard Composition (System Health, Knowledge Metrics, Active Clusters, Real-Time Activity, AIEMS Principles panel, persistent conversation bar with voice affordance) and Section 8.3 Orb Status Panel (Mode/Confidence/Autonomy/Permission textual readout, distinct from 8.2's ambient animation semantics, tied explicitly to ADR-0010 HITL governance). Both explicitly illustrative/design-direction only, not implementation, per Section 18. |
| 3.89 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.13 to 0.14) following: Recorded Section 15.4: Programme Sponsor located FCH-0010's Guardian Orb design conversation, believing it was already merged into governed architecture. Traced the chain - ESR-0010 Section 15 did approve and record a design direction correctly, but UAM-0001 (created earlier, under ESR-0009) was never updated afterward to reference it. Fixed per Programme Sponsor's full-incorporation decision: UAM-0001 v1.2 (Sections 8.1 Knowledge Graph Representation, 8.2 Orb Status Semantics, both explicit design-direction-only) and EBR-0001 v1.21 (EBG-0028 phased achievability roadmap). Noted the original mock-up image is not recoverable from the repository. |
| 3.88 | 9 July 2026 | Claude Engineering Lead | Aligned EBR-0001 version (1.20 to 1.21) following: Added ESR-0010's phased achievability roadmap (from FCH-0010's Guardian Orb design discussion, retroactively incorporated into UAM-0001 v1.2) to EBG-0028's note: Phase 1 static live graph, Phase 2 cluster colours/chat UI, Phase 3 agent traversal animation, Phase 4 Guardian reasoning/telemetry connection. |
| 3.87 | 9 July 2026 | Claude Engineering Lead | Aligned UAM-0001 version (1.1 to 1.2) following: Retroactively incorporated ESR-0010 Section 15's approved Guardian Orb design direction (originally discussed in FCH-0010, never merged into this artefact at the time): new Section 8.1 Knowledge Graph Representation (Orb as live rendering of the repository's engineering knowledge graph - nodes/connections/cluster illumination/agent-as-nodes) and Section 8.2 Orb Status Semantics (idle/learning/reasoning/awaiting-approval/approved colour states, distinct from Section 14's general capability colour language). Both remain design direction only, not implementation, per Section 18. Added ESR-0010 to OSE Relationships/Related Artefacts. Gap identified when the Programme Sponsor asked whether a final UXP look had already been discussed with ChatGPT. |
| 3.86 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.12 to 0.13) following: Recorded Section 15.3: consulted UAM-0001 (Approved Guardian Experience Architecture baseline, previously not checked before WP9's frontend work) and its FCH-0009/FCH-0011 origin (a ChatGPT-generated mock-up, not preserved in-repo). Confirmed Obsidian-as-product-feature was already explicitly decided against (FCH-0008), consistent with current architecture. Compliance check against UAM-0001 Sections 5-19 found and fixed one real defect: DiagnosticsPanel's guardian/sentinel/providers rows were static and could contradict the live sidebar/status-card state from the same platform.status call; now derived consistently via a new deriveDiagnostics() in App.jsx. Verified by npm run build (clean) and live via Vite HMR against the running dev session. Noted JARVIS_CAPABILITY_READINESS_MATRIX.md is stale (pre-dates WP2/WP9) but did not action it - out of this check's scope. |
| 3.85 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.11 to 0.12) following: Recorded ChatGPT Engineering Reviewer's WP9 implementation review outcome (Section 15.1.1): Approved with 4 Minor findings. Fixed 2 (jsonrpc version validation in stdio_rpc.py with 2 new regression tests, 184/184 passing; Rust state cleared on malformed response too, cargo build clean); deliberately deferred 2 (handler exception detail leakage - noted on EBR-0001 EBG-0050 v1.20; compile-only verification boundary - already honestly disclosed, Reviewer confirmed acceptable for foundation scope). WP9 marked Complete and Reviewed per Reviewer recommendation. Corrected a stale Section 13 WP8 row that still read 'awaiting review' after WP8 was already completed. |
| 3.84 | 9 July 2026 | Claude Engineering Lead | Aligned EBR-0001 version (1.19 to 1.20) following: Added ChatGPT Engineering Reviewer's ESR-0017 WP9 implementation review Minor Finding 2 (handler exception messages should not surface verbatim once external/provider-backed paths exist) to EBG-0050's note. |
| 3.83 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.10 to 0.11) following: Recorded WP9-adjacent Dev-Environment Setup Automation (Section 15.2): setup.bat / scripts/setup-dev-environment.ps1, prompted by the Programme Sponsor's work-laptop move. Verified by direct execution (idempotent re-run, 182/182 tests). Added EBR-0001 EBG-0054 as the forward-looking backlog item for future expansion (cross-platform equivalent, CI parity, environment-doctor mode, version-floor checks). Committed and pushed as b3806d5. |
| 3.82 | 9 July 2026 | Claude Engineering Lead | Aligned EBR-0001 version (1.18 to 1.19) following: Added EBG-0054 (Dev-Environment Setup Automation Expansion), recording ESR-0017's new setup.bat / scripts/setup-dev-environment.ps1 clone-bootstrap tooling and candidate future expansion (cross-platform equivalent, CI parity, environment-doctor mode, version-floor checks). |
| 3.81 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.9 to 0.10) following: Recorded WP9 Implementation Record (Section 15.1): all three parts (Python backend, Tauri Rust bridge, React frontend) implemented and self-reviewed against the approved design. Backend verified end-to-end by direct execution and 12 passing tests; Rust and React verified by clean build/compile only - verification boundary disclosed honestly (no windowed-app or click-through testing possible in this environment). Status: awaiting Engineering Reviewer verification before WP9 is marked complete. |
| 3.80 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.8 to 0.9) following: Recorded ChatGPT Engineering Reviewer's WP9 design review outcome: approve with five refinements, all incorporated (JSON-RPC 2.0 envelope, LocalEchoProvider default confirmed, minimal child-process lifecycle handling with explicit no-mock-fallback rule, method set confirmed sufficient, explicit dev-mode-only Rust process note). Implementation now proceeding. |
| 3.79 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.7 to 0.8) following: Recorded WP9 (First Interactive UXP - Bring JARVIS, Guardian and Sentinel to life) design plan: three-part foundation-scope implementation of ADR-0019's bridge (Python stdio JSON-RPC entry point, Tauri Rust sidecar process management, React live-data wiring), environment confirmed by direct execution, explicit scope exclusions stated. Design only, not yet implemented - awaiting Engineering Reviewer input per Programme Sponsor direction before coding begins. |
| 3.78 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.6 to 0.7) following: Recorded ChatGPT Engineering Reviewer's WP8 review outcome: Accept with one minor refinement, one non-blocking observation (0 Blocking, 0 Major). Both incorporated into PBK-0001 v1.19. WP8 complete and reviewed; WP9 may now begin. |
| 3.77 | 9 July 2026 | Claude Engineering Lead | Aligned PBK-0001 version (1.18 to 1.19) following: Incorporated ChatGPT Engineering Reviewer's WP8 refinements: Minimise Controlled Artefact Creation's threshold reworded to the objectively-testable 'repository or governance record no longer accurately reflects the implemented engineering state' (was 'drift'); UXP rule reworded to 'demonstrable progress toward the live UXP, achieved through direct UXP implementation or through delivery of backend capability required by that UXP' - explicitly permits backend-only sessions and rules out cosmetic compliance edits. Both accepted on their own merits, not deferred to Reviewer authority. |
| 3.76 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.5 to 0.6) following: Recorded WP8 (Feature-First Delivery Discipline, added to PBK-0001 v1.18) directly in this session report per the new artefact-minimisation rule it introduces - no new file created. Drafted, awaiting Engineering Reviewer review before WP9 begins. |
| 3.75 | 9 July 2026 | Claude Engineering Lead | Aligned PBK-0001 version (1.17 to 1.18) following: Added Feature-First Delivery Discipline: minimise controlled artefact creation (update existing artefacts unless not doing so would cause repo/governance drift), every Engineering Session must deliver product-moving engineering work (not governance-only), every Engineering Session must improve the UXP until the mock-up becomes a live system. Directed by the Programme Sponsor, ESR-0017 WP8. |
| 3.74 | 9 July 2026 | Claude Engineering Lead | Aligned PST-0001 version (2.22 to 2.23) following: Recorded RBL-0012 acceptance (superseding RBL-0011) and ESR-0017 in-progress state: WP1-WP4 complete and reviewed, WP6/WP7 complete, WP8/WP9 pending Programme Sponsor scope definition. Current Mode correctly retained as ESR-0016 (latest closed session) per WP0B, with ESR-0017 progress described separately in the same field. Updated Sections 3, 4A, 5 (Sentinel/UXP/JARVIS Development rows), 8 and 9. |
| 3.73 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.4 to 0.5) following: Recorded WP7 Repository Baseline Acceptance (RBL-0012) and WP6/WP8/WP9 rows in Work Package Plan. Programme Sponsor indicated two further Work Packages (WP8, WP9) before session closure - scope not yet defined. Session remains Open. |
| 3.72 | 9 July 2026 | Claude Engineering Lead | Registered RBL-0012 (ESR-0017 Repository Baseline), accepted by the Programme Sponsor 9 July 2026, superseding RBL-0011. Correction: this entry originally read "(3.71 to 3.62)", a `bump_version.py` self-referential-target bug (see `scripts/bump_version.py` fix, same date) - the tool ignored the literal target version and computed 3.72 correctly, but generated an inaccurate log sentence naming the wrong target. Text corrected; the version number itself (3.72) was always correct. |
| 3.71 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.3 to 0.4) following: Recorded WP6 Independent Repository Verification result: ChatGPT Engineering Reviewer PASS (repository state, content, OSE and scope compliance all Pass; one disclosed non-blocking commit-message deviation; recommends baseline acceptance). WP7 Repository Baseline Acceptance now outstanding, Programme Sponsor decision. |
| 3.70 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.2 to 0.3) following: Recorded EE-0001 scorecard reconciliation: Engineering Reviewer (ChatGPT) reviewed the Lead's ESR-0017 draft self-assessment, substantially agreed, and provided four refinements (signal-to-noise recorded as instrument gap, evidence responsiveness marked not meaningfully exercised, Reviewer behavioural finding reworded in its own words, new EBG-0053 Review Gate Compliance criterion jointly recommended). Not yet accepted by the Programme Sponsor. |
| 3.69 | 9 July 2026 | Claude Engineering Lead | Aligned EBR-0001 version (1.17 to 1.18) following: Refined EBG-0052 wording with ChatGPT Engineering Reviewer's own confirmation/clarification of the execute-after-approval finding; added EBG-0053 (EE-0001 Review Gate Compliance Criterion), jointly recommended by Lead and Reviewer during ESR-0017 scorecard reconciliation. |
| 3.68 | 9 July 2026 | Claude Engineering Lead | Aligned ESR-0017 version (0.1 to 0.2) following: Added consolidated Engineering Completion Report (Architectural Milestones, Executive Summary, Engineering Outcomes, Validation Summary, Repository Deliverables, EE-0001 Trial Observations, Outstanding Work) following WP1-WP4 completion and Reviewer disposition. Session remains Open pending Programme Sponsor authorisation for repository operations. |
| 3.67 | 9 July 2026 | Claude Engineering Lead | Aligned EBR-0001 version (1.16 to 1.17) following: Added EBG-0052 (PBK-0001/EE-0001 Execute After Approval Principle) per Programme Sponsor-reported EE-0001 trial improvement finding for ESR-0017. |
| 3.66 | 9 July 2026 | Claude Engineering Lead | Aligned EBR-0001 version (1.15 to 1.16) following: Added EBG-0051 (Gemini Provider Production Readiness) per ChatGPT Engineering Reviewer's ESR-0017 WP3 observations: richer response parsing, extended metadata, and a required live smoke test before Gemini is enabled as a production provider. |
| 3.65 | 9 July 2026 | Claude Engineering Lead | Aligned EBR-0001 version (1.14 to 1.15) following: Added ChatGPT Engineering Reviewer's ESR-0017 WP2 Observation 2 (consider a streaming converse() interface at EBG-0050 implementation time) to EBG-0050's note. |
| 3.64 | 9 July 2026 | Claude Engineering Lead | Aligned EBR-0001 version (1.13 to 1.14) following: Added explicit failure-mode implementation requirements (backend crash, restart policy, version negotiation, protocol compatibility, IPC timeout strategy) to EBG-0050, per ChatGPT Engineering Reviewer's ESR-0017 WP1 Recommendation 3. |
| 3.63 | 9 July 2026 | Claude Engineering Lead | Aligned ADR-0019 version (1.0 to 1.1) following: Softened HTTP/WebSocket wording per ChatGPT Engineering Reviewer WP1 finding - reframed from implying loopback HTTP is inherently insecure to the actual reason (avoidable complexity for no current requirement). |
| 3.62 | 9 July 2026 | Claude Engineering Lead | Aligned EBR-0001 version (1.12 to 1.13) following: Added EBG-0050 (UXP-Backend Bridge Implementation) per ADR-0019 / ESR-0017 WP1. |
| 3.61 | 9 July 2026 | Claude Engineering Lead | Aligned REG-0001 version (3.60 to 3.61) following: Registered ADR-0019 (UXP-Backend Integration Architecture) directly in REG-0001's own artefact table, per ESR-0017 WP1. |
| 3.60 | 9 July 2026 | Claude Engineering Lead | Aligned REG-0002 version (2.7 to 2.8) following: Registered ADR-0019 UXP-Backend Integration Architecture, per ESR-0017 WP1. |
| 3.59 | 9 July 2026 | Claude Engineering Lead | Aligned REG-0001 version (3.58 to 3.59) following: Registered ESR-0017 (Open) - Cold Start Validation Session, third EE-0001 trial session. |
| 3.58 | 9 July 2026 | Claude Engineering Reviewer | Aligned EBR-0001 version (1.11 to 1.12) following: Added EBG-0049 (Cost-Aware Provider Routing and PEM-001 Revisit) per Programme Sponsor request following post-ESR-0016A discussion on balancing JARVIS running cost against performance. Cross-referenced with EBG-0045 (overlapping scope, not a duplicate) in both directions. |
| 3.57 | 9 July 2026 | Claude Engineering Reviewer | Registered FCH-0016 (Claude Full Chat History), generated from the live Claude Code session transcript per the FCH-0015 methodology. HST-0016 (Claude Chat Summary) created alongside it but not registered, consistent with HST-0014/HST-0015 - the simpler chat-summary format has no parseable version field for this register to track. Aligned self version row accordingly. |
| 3.56 | 9 July 2026 | Claude Engineering Reviewer | Registered ESR-0016A Post-Closure Engineering Addendum following completion of all five approved work packages. Aligned self version row accordingly. |
| 3.55 | 9 July 2026 | Claude Engineering Reviewer | Aligned COC-0001 version (1.10 to 1.11) following: Added Operating Rule 51 and a note under Engineering Reviewer: the Programme Sponsor may direct the Engineering Reviewer to maintain the Engineering Session Report when the Implementer's environment cannot support incremental documentation - a per-session Sponsor decision, documentation only, not a change to accountability. Per ESR-0016A WP5. |
| 3.54 | 9 July 2026 | Claude Engineering Reviewer | Aligned PBK-0001 version (1.16 to 1.17) following: Added Operational Verification Before Reporting: an AI collaborator shall not report a repository/tool operation's outcome without having actually invoked it and observed the result. Operationalises Principles 2 and 4 for tool operations specifically, per ESR-0016A WP4. |
| 3.53 | 9 July 2026 | Claude Engineering Reviewer | Aligned PBK-0001 version (1.15 to 1.16) following the ESR-0016A WP1 pre-commit hook visibility fix - caught immediately by the newly-activated local hook itself. Aligned self version row accordingly. |
| 3.52 | 9 July 2026 | Claude Engineering Reviewer | Aligned PST-0001 version (2.21 to 2.22) following ESR-0016 closure update. Aligned self version row accordingly. |
| 3.51 | 9 July 2026 | Claude Engineering Reviewer | Registered ESR-0016 Engineering Session Report following ESR-0016 closure. Aligned self version row accordingly. |
| 3.50 | 9 July 2026 | Claude Engineering Reviewer | Aligned SAM-0001 version (0.2 to 0.3) following ESR-0016 WP2B's trust-tier policy model reference, fixed on explicit Programme Sponsor instruction after `scripts/validate_repository.py` flagged the mismatch this introduced. Aligned self version row accordingly. |
| 3.49 | 8 July 2026 | Claude Engineering Reviewer | Aligned COC-0001 version (1.9 to 1.10) following a Programme Sponsor-directed housekeeping fix ahead of ESR-0016: corrected the stale RBL-0009 baseline reference to RBL-0011. Aligned self version row accordingly. |
| 3.48 | 8 July 2026 | Claude Engineering Implementer | Registered FCH-0015 (ESR-0015 Full Chat History, Claude side), generated directly from the live session transcript at Programme Sponsor request. Aligned self version row accordingly. |
| 3.47 | 8 July 2026 | Claude Engineering Implementer | GDE-0001 updated to 1.2 (added Section 7, Role Terminology mapping). Aligned GDE-0001 and self version rows accordingly. |
| 3.46 | 8 July 2026 | Claude Engineering Implementer | RBL-0011 accepted by the Programme Sponsor (Draft/0.1 to Accepted/1.0), superseding RBL-0010 as the current repository baseline. Aligned PST-0001 version following the acceptance update. |
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
