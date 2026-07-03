# RBL-0010 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0010 |
| Title | ESR-0009 Repository Baseline |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]] |
| Previous Baseline | [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 3 July 2026 |

---

# 2. Purpose

RBL-0010 records the repository baseline accepted at the conclusion of ESR-0009.

It captures the accepted repository state after ESR-0009 governed implementation, Guardian Desktop Platform Shell establishment, Guardian Experience v1.0 implementation, architecture model creation, programme status update and repository baseline readiness review.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Baseline Review | [[RBR-ESR0009-001_REPOSITORY_BASELINE_REVIEW|RBR-ESR0009-001]] |
| HEAD at baseline creation | `4715e3ed99699a7918ae035351f5b3b1a1637131` |
| Repository Readiness | Ready for ESR-0010 Engineering Ecosystem Modernisation |

---

# 4. Baseline Summary

RBL-0010 covers the ESR-0009 repository state following governed product implementation, architecture documentation and session closure.

Baseline outcomes:

- [[TPL-0001_ENGINEERING_EXECUTION_PACKAGE_TEMPLATE|TPL-0001]] Engineering Execution Package Template created.
- Guardian Desktop Platform Shell established.
- Tauri + React adopted as UXP implementation baseline.
- [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] Sentinel Trust Architecture established.
- [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Guardian Experience Architecture v1.0 established.
- Guardian Experience v1.0 implemented.
- [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]] created and closed.
- [[PST-0001_PROGRAMME_STATUS|PST-0001]] updated for ESR-0009 closure and ESR-0010 approval.
- [[RBR-ESR0009-001_REPOSITORY_BASELINE_REVIEW|RBR-ESR0009-001]] completed and recommended RBL-0010 creation.
- Repository validation passed at closure.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| [[TPL-0001_ENGINEERING_EXECUTION_PACKAGE_TEMPLATE|TPL-0001]] | Engineering Execution Package Template created for governed Codex delivery. |
| Guardian Desktop Platform Shell | Desktop presentation foundation established. |
| Tauri + React UXP implementation baseline | UXP implementation baseline adopted following [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]]. |
| [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] | Sentinel Trust Architecture established. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Guardian Experience Architecture v1.0 established. |
| Guardian Experience v1.0 | Guardian-centred experience layout implemented. |
| [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]] | ESR-0009 closure report created and closed. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Updated for ESR-0009 closure, RBL-0010 acceptance and ESR-0010 approval. |
| [[RBR-ESR0009-001_REPOSITORY_BASELINE_REVIEW|RBR-ESR0009-001]] | Baseline readiness review completed and RBL-0010 creation recommended. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Updated to register RBL-0010 and align current baseline metadata. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] remains the accepted operational product capability baseline unless separately updated.

ESR-0009 adds the Guardian Desktop Platform Shell and Guardian Experience v1.0 implementation foundation.

Provider execution, persistent memory, Sentinel enforcement, agent runtime, voice, vision, internet-backed assistance and automation remain outside the accepted operational product baseline until separately implemented and accepted.

---

# 7. Architecture Outcomes

ESR-0009 accepted the following architecture and implementation-aligned outcomes:

- Tauri + React adopted as the User Experience Platform implementation baseline, following [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]].
- Guardian Desktop Platform Shell established as the immediate desktop implementation surface.
- Sentinel Trust Architecture established in [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]].
- Guardian Experience Architecture v1.0 established in [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]].
- Guardian identity and cognitive architecture remains governed by [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]].
- Platform architecture remains governed by [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]].
- Engineering Ecosystem Synchronisation remains governed by [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]].

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no ESR-0010 artefact is created;
- no new product capability baseline is created;
- no product source code changes are introduced by this baseline package;
- no tests are changed by this baseline package;
- no architecture artefacts or ADRs are modified by this baseline package;
- provider execution, persistent memory, Sentinel enforcement, agent runtime, voice, vision, internet-backed assistance and automation remain outside the accepted operational product baseline.

---

# 9. Verification

Repository validation performed before baseline creation confirmed:

- Git working tree was clean.
- Repository branch was `main`.
- Repository was synchronised with `origin/main`.
- [[RBR-ESR0009-001_REPOSITORY_BASELINE_REVIEW|RBR-ESR0009-001]] existed and recommended RBL-0010 creation.
- [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]] was closed.
- [[PST-0001_PROGRAMME_STATUS|PST-0001]] recorded ESR-0009 closure and ESR-0010 approval.
- [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] remained the current accepted baseline before this package.
- `python scripts/validate_repository.py` passed.
- `git diff --check` passed.

---

# 10. Handover to ESR-0010

ESR-0010 is approved as AIEMS Engineering Ecosystem Modernisation.

Opening review should include:

1. [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]]
2. [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]]
3. [[PST-0001_PROGRAMME_STATUS|PST-0001]]
4. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]]
5. [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]]
6. [[RBR-ESR0009-001_REPOSITORY_BASELINE_REVIEW|RBR-ESR0009-001]]
7. [[TPL-0001_ENGINEERING_EXECUTION_PACKAGE_TEMPLATE|TPL-0001]]
8. [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]]
9. [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]]
10. [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]]

ESR-0010 should treat RBL-0010 as the accepted ESR-0009 repository baseline.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBR-ESR0009-001_REPOSITORY_BASELINE_REVIEW|RBR-ESR0009-001]] | Repository baseline review recommending RBL-0010 creation. |
| [[ESR-0009_ENGINEERING_SESSION_REPORT|ESR-0009]] | Engineering session closed by this repository baseline. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Previous accepted repository baseline and ESR-0009 starting baseline. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status updated for RBL-0010 acceptance and ESR-0010 handover. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[TPL-0001_ENGINEERING_EXECUTION_PACKAGE_TEMPLATE|TPL-0001]] | Execution package template created during ESR-0009. |
| [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] | Sentinel Trust Architecture accepted into this repository baseline. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Guardian Experience Architecture v1.0 accepted into this repository baseline. |
| [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]] | Decision authority for Tauri + React UXP direction. |
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Decision authority for Engineering Ecosystem Synchronisation. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 3 July 2026 | Codex Engineering Implementer | Initial ESR-0009 repository baseline recording Guardian Desktop Platform Shell, Guardian Experience v1.0, TPL-0001, SAM-0001, UAM-0001, ESR-0009 closure, PST-0001 update and RBR-ESR0009-001 recommendation. |
