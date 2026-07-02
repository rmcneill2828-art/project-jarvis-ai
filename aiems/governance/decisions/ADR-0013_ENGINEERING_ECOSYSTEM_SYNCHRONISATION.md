# ADR-0013 - Engineering Ecosystem Synchronisation

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0013 |
| Title | Engineering Ecosystem Synchronisation |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 2 July 2026 |
| Review Trigger | Significant engineering workflow or knowledge ecosystem change |

---

# Purpose

Record the ESR-0008 decision that WP0 evolves to Engineering Ecosystem Synchronisation.

---

# Scope

This decision covers synchronisation across GitHub, AIEMS, OSE, Obsidian, registers, controlled artefacts, previous ESRs and summaries. It does not replace GitHub as source of truth.

---

# Engineering Authority

Approved by Programme Sponsor during ESR-0008 under repository-first AIEMS governance.

---

# Evidence Sources

- [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]].
- [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
- [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]].

---

# Main Content

# 1. Problem Statement

Repository-first engineering must account for the full Engineering Ecosystem, including passive knowledge workspaces that are easy to overlook during synchronisation.

---

# 2. Background

ESR-0008 identified Obsidian as a first-class Engineering Ecosystem component and clarified OSE as the semantic relationship layer connecting engineering knowledge.

---

# 3. Options Considered

| Option | Assessment |
|--------|------------|
| Repository-only synchronisation | Strong source-of-truth discipline but may miss passive knowledge workspace context. |
| Conversation-led synchronisation | Too weak for governed engineering. |
| Engineering Ecosystem Synchronisation | Preserves GitHub authority while accounting for AIEMS, OSE, Obsidian and session evidence. |

---

# 4. Decision

WP0 evolves to Engineering Ecosystem Synchronisation.

GitHub, AIEMS, OSE, Obsidian, registers, controlled artefacts, previous ESRs and summaries must be considered. Obsidian must not be forgotten because it is passive / background.

---

# 5. Rationale

GitHub remains the source of truth. Obsidian is the human-facing Engineering Knowledge Workspace that visualises and navigates repository Markdown and OSE relationships. Treating both correctly improves engineering continuity without weakening repository authority.

---

# 6. Consequences

- Future synchronisation should explicitly account for Obsidian/OSE context where relevant.
- Obsidian remains outside the JARVIS runtime platform.
- OSE links shall remain verified and repository-compatible.

---

# 7. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Traceability model consuming OSE and Engineering Ecosystem context. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Session report recording Engineering Ecosystem Synchronisation. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Controlled artefact register participating in synchronisation. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[REG-0002_ADR_REGISTER|REG-0002]] | Registers this decision. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records future Obsidian/OSE workflow work. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 2 July 2026 | Codex Engineering Implementer | Initial approved ADR created during ESR-0008 closure. |
