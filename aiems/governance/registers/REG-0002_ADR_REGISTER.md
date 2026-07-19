# REG-0002 - Architectural Decision Register

> *"Good architecture is not defined by the decisions it makes, but by the reasoning it preserves."*

**Version:** 2.13

---

# Purpose

The Architectural Decision Register (ADR Register) is the authoritative record of all significant architectural and engineering decisions made within Project JARVIS AI and AIEMS.

Each Architecture Decision Record (ADR) captures the context, rationale, decision and consequences of a significant engineering choice.

The register provides traceability, supports future decision making and preserves organisational knowledge.

---

# Scope

This register includes Architecture Decision Records relating to:

- Project Governance
- Engineering Practices
- Architecture
- Development Standards
- AI Collaboration
- Repository Management
- Strategic Direction

---

# Architecture Decision Register

| ADR | Title | Domain | Status | Date Approved | Supersedes | Summary |
|------|-------------------------------|--------------|-----------|---------------|------------|---------------------------------------------------------------|
| [[ADR-0001_DOCUMENTATION_FIRST]] | Documentation First | Engineering | Approved | 22 Jun 2026 | - | Established documentation as the foundation for engineering activities. |
| [[ADR-0002_GIT_REPOSITORY_STRATEGY]] | Git Repository Strategy | Engineering | Approved | 22 Jun 2026 | - | Defined GitHub as the authoritative source for project artefacts and version control. |
| [[ADR-0003_RTBO_ENGINEERING_DECISION_FRAMEWORK]] | RTBO Engineering Decision Framework | Engineering | Approved | 23 Jun 2026 | - | Adopted the Review Twice. Build Once. Improve for Everyone decision-making framework. |
| [[ADR-0004_AI_REPOSITORY_INTERACTION_POLICY]] | AI Repository Interaction Policy | Governance | Approved | 24 Jun 2026 | - | Defined governance, approval model and responsibilities for AI-assisted repository interaction. |
| [[ADR-0005_AIEMS_STRATEGIC_SCOPE]] | AIEMS Strategic Scope | Strategy | Approved | 24 Jun 2026 | - | Recognised AIEMS as an independent strategic deliverable and JARVIS as its flagship implementation. |
| [[ADR-0006_INTRODUCTION_OF_PLAYBOOKS_AS_A_CONTROLLED_GOVERNANCE_ARTEFACT]] | Introduction of Playbooks as a Controlled Governance Artefact | Governance | Draft | 25 Jun 2026 | - | Established Playbooks as a new controlled governance artefact category within AIEMS. |
| [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION]] | User Experience Platform Selection | Architecture | Approved | 2 Jul 2026 | - | Selected Tauri + React as the UXP direction and clarified that UXP visualises state only. |
| [[ADR-0008_HYBRID_AI_RUNTIME_STRATEGY]] | Hybrid AI Runtime Strategy | Architecture | Approved | 2 Jul 2026 | - | Approved local-first hybrid runtime with provider abstraction and cloud use where strategic value justifies cost. |
| [[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN]] | Sentinel Gate of Durin Pattern | Architecture | Approved | 2 Jul 2026 | - | Established Sentinel as the trust gateway before Platform Services. |
| [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE]] | Guardian Identity and HITL Governance | Architecture | Approved | 2 Jul 2026 | - | Established Guardian as the singular trusted digital companion and HITL governance entity. |
| [[ADR-0011_AGENT_FRAMEWORK]] | Agent Framework | Architecture | Approved | 2 Jul 2026 | - | Established specialist agents as capabilities serving Guardian, not separate identities. |
| [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE]] | Device Independence and Portable Restore | Architecture | Approved | 2 Jul 2026 | - | Established devices as execution environments with portable memory, configuration and restore requirements. |
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION]] | Engineering Ecosystem Synchronisation | Governance | Approved | 2 Jul 2026 | - | Established WP0 Engineering Ecosystem Synchronisation including GitHub, AIEMS, OSE, Obsidian and session evidence. |
| [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM]] | Sentinel AI Execution and Security Platform | Architecture | Approved | 8 Jul 2026 | - | Positioned Sentinel as the AI Execution and Security Platform for AIEMS, expanding the earlier trust-gateway interpretation while preserving the Guardian/Sentinel separation. |
| [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE]] | UXP-Backend Integration Architecture | Architecture | Approved | 9 Jul 2026 | - | Selected a Tauri sidecar-managed Python process communicating over duplex stdio JSON-RPC as the UXP-to-backend integration pattern, over local HTTP/WebSocket, PyO3 embedding and a Rust/Node rewrite. |
| [[ADR-0020_SENTINEL_NETWORK_EXPOSURE_SECURITY_REQUIREMENTS]] | Sentinel Network Exposure Security Requirements | Architecture | Approved | 17 Jul 2026 | - | Defines a binding three-part security gate (authentication, rate limiting, TLS) any future network-facing Guardian/Sentinel interface proposal must satisfy before approval - no network interface exists today, this is a prerequisite gate, not implementation. |
| [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE]] | Guardian Orb Rendering Engine | Architecture | Approved-implemented | 18 Jul 2026 | - | Recommends migrating GuardianOrbGraph.jsx from SVG DOM rendering to Canvas 2D, grounded in ESR-0028 WP4's seven-round animation-performance optimisation evidence; rejects WebGL/a 3D library as disproportionate to current/anticipated scale. Implemented at ESR-0029 WP2 per EIP-ESR0029-001. |

---

# Repository Integrity Notes

[[ADR-0004_AI_REPOSITORY_INTERACTION_POLICY|ADR-0004]] and [[ADR-0005_AIEMS_STRATEGIC_SCOPE|ADR-0005]] were recovered during [[ESR-0003_ENGINEERING_SESSION_REPORT|ESR-0003]] EIP-R2 from approved repository evidence.

The recovered ADR files preserve historical approved decisions and restore decision traceability for existing register, risk, action and session references.

---

# ADR Lifecycle

Every Architecture Decision Record progresses through the following lifecycle.

Proposed

v

Review

v

Approved

v

Active

v

Superseded (if applicable)

v

Archived

---

# Approval Process

Every ADR shall:

- Describe the problem.
- Explain the available options.
- Record the selected decision.
- Explain the rationale.
- Describe the consequences.
- Receive explicit approval from the Programme Sponsor.
- Be entered into this register.

---

# Governance Principles

Architecture decisions should:

- Be evidence based.
- Be proportionate.
- Be traceable.
- Be reviewable.
- Be understandable.
- Be reusable where practical.

---

# Review Policy

Architecture Decision Records shall be reviewed:

- During every Strategic Alignment Review.
- Following significant technology changes.
- Following major architectural changes.
- When superseded by a newer ADR.

Historical ADRs shall never be deleted.

They remain part of the permanent engineering history of AIEMS.

---

# Relationship to AIEMS

Architecture Decision Records form one of the core knowledge management mechanisms within AIEMS.

They ensure that engineering reasoning is preserved alongside engineering implementation, allowing future contributors to understand not only what decisions were made, but why they were made.

---

# OSE Relationships

* [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]] defines the retrospective relationship-only enrichment rule applied to this register.
* [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] establishes Engineering Ecosystem Synchronisation and the repository-compatible OSE context for decision traceability.
* [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] records authoritative ADR artefact identity, ownership, status and current version.
* [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] provides product vision traceability context for architectural decisions.
* [[PST-0001_PROGRAMME_STATUS|PST-0001]] records current programme status and governance position.
* [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] is the current accepted repository baseline supporting this retrospective OSE pass.

---
# Related Artefacts

* [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] records controlled artefact registration for AIEMS governance artefacts.
* [[REG-0003_RISK_REGISTER|REG-0003]] records risks that may reference architectural decisions.
* [[REG-0004_ACTION_REGISTER|REG-0004]] records actions arising from decisions and risks.
* [[PST-0001_PROGRAMME_STATUS|PST-0001]] records current programme status and governance position.
* [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] records the current accepted repository baseline.

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|----------------------------|-------------------------------------------------------------|
| 2.13 | 19 July 2026 | Claude Engineering Implementer | ADR-0021 implementation recorded (1.3 to 1.4, Approved to Approved-implemented) - GuardianOrbGraph.jsx migrated to Canvas 2D at ESR-0029 WP2 per EIP-ESR0029-001. |
| 2.12 | 18 July 2026 | Claude Engineering Implementer | ADR-0021 approved by the Programme Sponsor via the bridge (1.2 to 1.3, Draft to Approved) - Canvas 2D selected over continued SVG or WebGL/a 3D library for GuardianOrbGraph.jsx's rendering, decision only. |
| 2.11 | 18 July 2026 | Claude Engineering Implementer | ADR-0021 revised (1.0 to 1.1) per Engineering Reviewer finding - corrected this register's own v2.10 entry, which overstated a still-Draft ADR's effect on EBG-0081. |
| 2.10 | 18 July 2026 | Claude Engineering Implementer | Registered ADR-0021 Guardian Orb Rendering Engine (Draft), per ESR-0028 WP5, drafted to resolve the rendering-engine question EBG-0081 raises, pending Programme Sponsor approval - EBG-0081 itself remains Candidate Backlog, not yet updated. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
| 2.9 | 17 July 2026 | Claude Engineering Implementer | Registered ADR-0020 Sentinel Network Exposure Security Requirements, per ESR-0026 WP3 (resolving EBG-0076). Engineering Reviewer (Codex) reviewed via the AIEMS Exchange Bridge, no blocking findings, Programme Sponsor approved. |
| 2.8 | 9 July 2026 | Claude Engineering Lead | Registered ADR-0019 UXP-Backend Integration Architecture, per ESR-0017 WP1. |
| 2.7 | 8 July 2026 | Claude Engineering Implementer | Registered ADR-0018 Sentinel AI Execution and Security Platform, closing a gap where it was present in REG-0001 but missing from this ADR-specific register. |
| 2.6 | 2 July 2026 | Codex Engineering Implementer | Added retrospective OSE relationships to improve semantic traceability without changing ADR governance. |
| 2.5 | 2 July 2026 | Codex Engineering Implementer | Registered ESR-0008 architectural decisions ADR-0007 through ADR-0013. |
| 1.0 | 23 June 2026 | Project Sponsor | Initial ADR Register established. |
| 2.0 | 24 June 2026 | Project Sponsor & Chief Architect | Expanded to include AIEMS governance, ADR lifecycle, approval process, review policy and new strategic decisions ADR-0004 and ADR-0005. |
| 2.1 | 24 June 2026 | Programme Sponsor & Chief Engineering Advisor | Repository architecture alignment. Updated artefact identifiers, Platform terminology and repository references. |
| 2.2 | 25 June 2026 | Programme Sponsor & Chief Engineering Advisor | Registered ADR-0006 for the introduction of Playbooks as a controlled governance artefact while preserving existing ADR-0004 and ADR-0005 register history. |
| 2.3 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Added repository integrity note identifying missing ADR-0004 and ADR-0005 artefact files while preserving historical register references. |
| 2.4 | 27 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recorded recovery of ADR-0004 and ADR-0005 from approved repository evidence. |
