# RBL-0008 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0008 |
| Title | ESR-0007 Repository Baseline |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] |
| Previous Baseline | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 1 July 2026 |

---

# 2. Purpose

RBL-0008 records the repository baseline prepared at the conclusion of ESR-0007.

It captures the accepted repository state after ESR-0007 introduced [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]], [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]], repository-first methodology outcomes and ESR-0008 candidate selection.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| HEAD at closure implementation start | `1a161466438fc65cdfd022e00ee3665413fa65cc` |
| Repository Readiness | Ready for ESR-0008 handover after closure validation |

---

# 4. Baseline Summary

RBL-0008 covers the ESR-0007 repository state following product capability assessment, product capability baseline acceptance and session closure.

Baseline outcomes:

- [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] created and accepted as repository product capability evidence.
- [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] created and accepted as the first JARVIS product capability baseline.
- [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] reviewed and preserved as the authoritative capability maturity model.
- [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] reviewed as the authoritative backlog source.
- Repository-First Engineering Protocol accepted as an ESR-0007 working practice.
- Repository-First Decision Protocol accepted as an ESR-0007 working practice.
- Continuous Repository Synchronisation accepted as an ESR-0007 working practice.
- EBG-0039 JARVIS Runtime Chat Archive selected as the next engineering candidate for ESR-0008 validation.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] | Completed repository product capability assessment. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline. |
| ESR-0007 closure report | Updated [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] to Version 1.0 / Closed. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Updated to ESR-0007 closure and ESR-0008 readiness. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Updated to register ESR-0007, RPCA-0001, PCB-0001 and RBL-0008. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] is the accepted operational product baseline for JARVIS at ESR-0007 closure.

The accepted baseline confirms the current First Light / Conversation Workspace foundation and its known constraints. Detailed product capability evidence remains in [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]]. Capability maturity remains in [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]].

---

# 7. Methodology Outcomes

ESR-0007 accepted the following methodology outcomes as working practices:

- ED-ESR0007-001 Repository-First Engineering Protocol (RFEP).
- ED-ESR0007-002 Repository-First Decision Protocol (RFDP).
- ED-ESR0007-003 Continuous Repository Synchronisation.

These are not formal AIEMS standards. Future promotion shall require separately approved standards review or controlled implementation work.

---

# 8. Knowledge Engineering Outcomes

ESR-0007 confirmed that GitHub is the authoritative engineering repository, OSE is the semantic relationship layer and Obsidian is the Engineering Knowledge Workspace.

The Obsidian graph demonstrates an emergent Engineering Knowledge Graph built from controlled repository artefacts. Future JARVIS knowledge capability should be explored from ESR-0008 onward, subject to approved scope.

Governed domain memory remains a future architectural consideration only and is not promoted to backlog or architecture by this baseline.

---

# 9. Independent Verification

Independent GitHub verification was completed for:

- [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]]
- [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]]

Repository-first closure validation remains required for the final ESR-0007 closure commit and post-push report.

---

# 10. Repository Readiness

The repository is ready for ESR-0008 handover when the ESR-0007 closure changes are committed, pushed and independently verified.

Scope boundaries for this baseline:

- no source code changes are included;
- no tests are changed;
- no product architecture changes are included;
- no Capability Readiness Matrix changes are included;
- no EBR-0001 status changes are included;
- no new ADRs or standards are created.

---

# 11. Handover to ESR-0008

ESR-0008 should begin with Repository-First Synchronisation.

Opening review should include:

1. [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]]
2. [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]]
3. [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]]
4. [[PST-0001_PROGRAMME_STATUS|PST-0001]]
5. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]
6. [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]]

ESR-0008 should then validate EBG-0039 JARVIS Runtime Chat Archive as the recommended next engineering candidate before any implementation authority is assumed.

---

# 12. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0007_ENGINEERING_SESSION_REPORT|ESR-0007]] | Engineering session closed by this repository baseline. |
| [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] | Previous accepted repository baseline and ESR-0007 starting point. |
| [[RPCA-0001_REPOSITORY_PRODUCT_CAPABILITY_ASSESSMENT|RPCA-0001]] | Product capability assessment completed during ESR-0007. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Product capability baseline accepted during ESR-0007. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status updated for ESR-0007 closure and ESR-0008 readiness. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Authoritative backlog source and EBG-0039 candidate source. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product architecture context for the accepted capability baseline. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Authoritative capability maturity assessment. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline and ESR-0007 closure artefacts. |

---

# 13. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 1 July 2026 | Codex Engineering Implementer | Initial ESR-0007 repository baseline recording RPCA-0001, PCB-0001, repository-first methodology outcomes and ESR-0008 handover readiness. |
