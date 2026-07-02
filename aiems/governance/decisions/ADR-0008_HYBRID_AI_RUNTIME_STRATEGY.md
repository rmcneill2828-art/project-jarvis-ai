# ADR-0008 - Hybrid AI Runtime Strategy

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0008 |
| Title | Hybrid AI Runtime Strategy |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 2 July 2026 |
| Review Trigger | Significant AI runtime or provider architecture change |

---

# Purpose

Record the ESR-0008 decision to use a hybrid AI runtime strategy with provider independence.

---

# Scope

This decision covers runtime strategy, local-first preference, cloud use boundary and provider abstraction. It does not select or integrate a runtime provider.

---

# Engineering Authority

Approved by Programme Sponsor during ESR-0008 under repository-first AIEMS governance.

---

# Evidence Sources

- [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]].
- [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]].
- [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]].

---

# Main Content

# 1. Problem Statement

JARVIS needs AI runtime capability without becoming hard-coupled to one local runtime, cloud provider or commercial model.

---

# 2. Background

ESR-0008 approved a local-first but not local-only runtime strategy. Cloud providers may be used where strategic value justifies cost, risk and integration complexity.

---

# 3. Options Considered

| Option | Assessment |
|--------|------------|
| Local-only runtime | Strong privacy and cost control but may limit capability. |
| Cloud-only runtime | Strong capability access but creates cost, privacy and dependency risk. |
| Hybrid runtime | Balances privacy, capability, cost and strategic value. |

---

# 4. Decision

JARVIS shall use a Hybrid AI Runtime Strategy:

- local-first where appropriate;
- cloud providers allowed where strategic value justifies cost;
- provider abstraction required;
- Ollama may be an early local runtime candidate, but JARVIS shall not be hard-coupled to Ollama.

---

# 5. Rationale

Hybrid runtime preserves product value and technology independence. Provider selection shall consider trust, policy, privacy, cost, value and context.

---

# 6. Consequences

- JARVIS requests capabilities, not vendors.
- Provider Architecture shall mediate provider choice.
- Capability contracts shall preserve future provider replacement.

---

# 7. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product architecture source for provider independence. |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Traceability model for runtime decisions. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Session report recording the hybrid runtime outcome. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[REG-0002_ADR_REGISTER|REG-0002]] | Registers this decision. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records future provider and cost framework work. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 2 July 2026 | Codex Engineering Implementer | Initial approved ADR created during ESR-0008 closure. |
