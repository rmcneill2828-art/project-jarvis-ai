# ADR-0011 - Agent Framework

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0011 |
| Title | Agent Framework |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 2 July 2026 |
| Review Trigger | Significant agent architecture change |

---

# Purpose

Record the ESR-0008 decision that specialist agents are capabilities serving Guardian, not separate user-facing identities.

---

# Scope

This decision covers the Agent Framework concept and Engineering Agent correction. It does not implement agents or define detailed agent contracts.

---

# Engineering Authority

Approved by Programme Sponsor during ESR-0008 under repository-first AIEMS governance.

---

# Evidence Sources

- [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]].
- [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]].
- [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]].

---

# Main Content

# 1. Problem Statement

JARVIS requires specialist capabilities without fragmenting the user-facing AI identity.

---

# 2. Background

ESR-0008 corrected the Engineering Assistant concept into a specialist Engineering Agent within an Agent Framework serving Guardian.

---

# 3. Options Considered

| Option | Assessment |
|--------|------------|
| Separate AI identities per domain | Weakens Guardian coherence and user trust. |
| No specialist agents | Limits domain capability and future extensibility. |
| Specialist agents serving Guardian | Preserves Guardian identity while enabling domain expertise. |

---

# 4. Decision

Specialist agents are capabilities, not separate user-facing identities.

Engineering Assistant becomes Engineering Agent / specialist agent. Guardian orchestrates agents and asks agents how to accomplish specialist tasks.

---

# 5. Rationale

The Agent Framework supports extensibility while preserving Guardian as the trusted digital companion.

---

# 6. Consequences

- Agents do not bypass Guardian, Sentinel or policy governance.
- Agents shall operate through capability boundaries.
- Future agent implementation requires separate approved packages.

---

# 7. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Defines the relationship between Guardian and specialist agents. |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Traces Agent Framework into product vision recovery. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Session report recording the Agent Framework decision. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[REG-0002_ADR_REGISTER|REG-0002]] | Registers this decision. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records future Agent Framework work. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 2 July 2026 | Codex Engineering Implementer | Initial approved ADR created during ESR-0008 closure. |
