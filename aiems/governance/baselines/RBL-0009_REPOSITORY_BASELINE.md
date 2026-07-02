# RBL-0009 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0009 |
| Title | ESR-0008 Repository Baseline |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] |
| Previous Baseline | [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 2 July 2026 |

---

# 2. Purpose

RBL-0009 records the repository baseline accepted at the conclusion of ESR-0008.

It captures the accepted repository state after ESR-0008 Product Vision Recovery, architecture evaluation, Guardian identity discovery, JARVIS Platform alignment, Engineering Ecosystem Synchronisation and ESR-0009 readiness update.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| HEAD at baseline creation | `7dc48cc` |
| Repository Readiness | Ready for ESR-0009 Engineering Ecosystem Synchronisation |

---

# 4. Baseline Summary

RBL-0009 covers the ESR-0008 repository state following documentation-only architecture evaluation and closure.

Baseline outcomes:

- [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] created and updated for ESR-0008 traceability.
- [[ERR-0001_ENGINEERING_RECOVERY_REPORT|ERR-0001]] created and updated for ESR-0008 recovery findings.
- [[EIR-0001_ENGINEERING_IMPLEMENTATION_RECOMMENDATION|EIR-0001]] created and updated for ESR-0009 validation recommendation.
- [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] created to record Guardian identity and cognitive architecture.
- ADR-0007 through ADR-0013 created to record ESR-0008 architecture decisions.
- [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] created and closed.
- [[PST-0001_PROGRAMME_STATUS|PST-0001]] updated for ESR-0009 readiness.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Product vision traceability model created and extended. |
| [[ERR-0001_ENGINEERING_RECOVERY_REPORT|ERR-0001]] | Engineering recovery findings recorded. |
| [[EIR-0001_ENGINEERING_IMPLEMENTATION_RECOMMENDATION|EIR-0001]] | ESR-0009 validation recommendation recorded. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity and cognitive architecture recorded. |
| ADR-0007 through ADR-0013 | ESR-0008 architecture decisions recorded. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | ESR-0008 closure report created and closed. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Updated for ESR-0009 readiness. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Updated to register RBL-0009 and align ESR-0008 closure status. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] remains the accepted operational product baseline for JARVIS.

ESR-0008 did not change runtime implementation. External AI providers, persistent memory, voice, vision, Guardian runtime behaviour, local agent and internet-backed assistance remain outside the accepted operational product baseline until separately implemented and accepted.

---

# 7. Architecture Outcomes

ESR-0008 accepted the following architecture outcomes for future validation and implementation planning:

- JARVIS Platform as the runtime operating platform.
- Guardian as the trusted digital companion / AI entity.
- Sentinel as the trust gateway before Platform Services.
- User Experience Platform (UXP) as the presentation-layer architecture term.
- Tauri + React as the selected UXP direction.
- Hybrid AI Runtime Strategy.
- Device independence and portable restore.
- Provider Architecture based on capability requests rather than vendor coupling.
- Agent Framework with specialist agents serving Guardian.
- Obsidian as the human-facing Engineering Knowledge Workspace for OSE.
- Engineering Ecosystem Synchronisation as the next synchronisation practice.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no product source code changes are included;
- no tests are changed;
- no runtime implementation is introduced;
- no ESR-0009 artefacts are created;
- no new product capability baseline is created;
- ESR-0008 architecture outcomes require ESR-0009 validation before implementation package selection.

---

# 9. Verification

Repository validation performed before baseline creation confirmed:

- Git working tree was clean.
- Repository branch was `main`.
- ESR-0008 closure commits were present.
- Repository-wide WikiLinks resolved during the preceding health check.
- Automated tests passed during the preceding health check: 19 tests passed.

---

# 10. Handover to ESR-0009

ESR-0009 should begin with Engineering Ecosystem Synchronisation.

Opening review should include:

1. [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]]
2. [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]]
3. [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]]
4. [[PST-0001_PROGRAMME_STATUS|PST-0001]]
5. [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]]
6. [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]]
7. [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]]
8. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]
9. [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]]
10. [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]]

ESR-0009 should validate ESR-0008 architecture before selecting or authorising the first implementation package.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Engineering session closed by this repository baseline. |
| [[RBL-0008_REPOSITORY_BASELINE|RBL-0008]] | Previous accepted repository baseline and ESR-0008 starting point. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Current accepted operational product capability baseline. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status updated for ESR-0009 readiness and RBL-0009 acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian architecture outcome accepted into this repository baseline. |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Traceability model accepted into this repository baseline. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog source for ESR-0009 candidate selection. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 2 July 2026 | Codex Engineering Implementer | Initial ESR-0008 repository baseline recording accepted architecture evaluation, Guardian identity, Engineering Ecosystem Synchronisation and ESR-0009 readiness. |
