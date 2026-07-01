# ADR-0005 - AIEMS Strategic Scope

---

## Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0005 |
| Title | AIEMS Strategic Scope |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 24 June 2026 |
| Review Trigger | Review if the strategic relationship between AIEMS, Project JARVIS AI or future AI-enabled products changes materially. |

---

# 1. Problem Statement

Project JARVIS AI requires a clear distinction between the AI Engineering Management System and the JARVIS product implementation.

Without an explicit strategic scope decision, AIEMS could become tightly coupled to JARVIS or JARVIS engineering could begin before the governance system is mature enough to support it.

---

# 2. Background

The repository contains historical approved references to ADR-0005 but the original ADR file was absent from `aiems/governance/decisions/` during ESR-0003 WS1 governance stabilisation.

Repository evidence records ADR-0005 as an approved strategy decision dated 24 June 2026. [[REG-0002_ADR_REGISTER|REG-0002]] describes its intent as recognising AIEMS as an independent strategic deliverable and JARVIS as its flagship implementation. [[CHR-0001_PLATFORM_CHARTER|CHR-0001]] version history records expansion of the Charter to recognise AIEMS as a strategic deliverable and define the long-term vision for AIEMS and JARVIS.

This recovered ADR preserves that approved decision using repository evidence. The original detailed ADR text was not recoverable from the repository baseline.

---

# 3. Options Considered

## Option 1 - Treat AIEMS as internal documentation for JARVIS only

This would make governance subordinate to the first product implementation and reduce reusability.

## Option 2 - Treat JARVIS and AIEMS as unrelated initiatives

This would preserve separation but weaken practical validation of AIEMS through implementation.

## Option 3 - Treat AIEMS as an independent strategic deliverable with JARVIS as the flagship implementation

This preserves AIEMS as reusable engineering governance while allowing JARVIS to validate and demonstrate it.

---

# 4. Decision

AIEMS is recognised as an independent strategic deliverable within Project JARVIS AI.

JARVIS is the flagship product implementation that will be engineered using AIEMS, but AIEMS is not limited to JARVIS and shall remain reusable for future AI-enabled engineering work.

---

# 5. Rationale

Separating AIEMS from JARVIS improves governance maturity, reuse and engineering discipline.

AIEMS defines how trustworthy AI-assisted engineering is governed. JARVIS demonstrates what can be built using that governance. This separation allows governance to mature before substantive product implementation while preserving a clear path to delivery.

---

# 6. Success Criteria

This decision is successful when:

- AIEMS remains visible as a strategic deliverable.
- JARVIS development follows AIEMS rather than redefining it ad hoc.
- Governance artefacts distinguish framework responsibilities from product implementation responsibilities.
- AIEMS can be reused beyond JARVIS where appropriate.
- JARVIS readiness is assessed against governance maturity, standards and repository verification capability.

---

# 7. Benefits

- Prevents AIEMS from becoming product-specific documentation only.
- Enables reusable governance and engineering practices.
- Supports staged maturity before full JARVIS development.
- Clarifies the relationship between governance, architecture and product implementation.
- Improves strategic traceability across programme artefacts.

---

# 8. Consequences

- AIEMS may require dedicated engineering work before JARVIS implementation accelerates.
- Programme planning must distinguish governance maturity from product capability maturity.
- Repository artefacts must preserve separate AIEMS and JARVIS responsibilities.
- JARVIS development readiness should be reviewed using evidence from AIEMS maturity.

---

# 9. Evidence

Recovered from repository evidence during ESR-0003 EIP-R2.

Evidence includes:

- [[REG-0002_ADR_REGISTER|REG-0002]] row for ADR-0005: AIEMS Strategic Scope, Strategy, Approved, 24 Jun 2026.
- [[REG-0004_ACTION_REGISTER|REG-0004]] ACT-0001, ACT-0002, ACT-0003, ACT-0006, ACT-0007 and ACT-0009 references to ADR-0005.
- [[CHR-0001_PLATFORM_CHARTER|CHR-0001]] version history entry 2.0 recognising AIEMS as a strategic deliverable and defining the long-term vision for AIEMS and JARVIS.
- [[ESR-0001_ENGINEERING_SESSION_REPORT|ESR-0001]] and [[ESR-0002_ENGINEERING_SESSION_REPORT|ESR-0002]] references to ADR-0005 recovery or formal supersession.
- [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0002 approved backlog item for ADR-0005 recovery or formal supersession.

---

# 10. Review Trigger

Review this ADR if:

- AIEMS strategic scope changes.
- JARVIS product scope changes materially.
- AIEMS is adopted for another implementation.
- Programme governance changes the relationship between AIEMS and JARVIS.

---

# 11. Related Decisions

- [[ADR-0001_DOCUMENTATION_FIRST|ADR-0001]] - Documentation First Development
- [[ADR-0002_GIT_REPOSITORY_STRATEGY|ADR-0002]] - Git Repository Strategy
- [[ADR-0003_RTBO_ENGINEERING_DECISION_FRAMEWORK|ADR-0003]] - RTBO Engineering Decision Framework
- [[ADR-0004_AI_REPOSITORY_INTERACTION_POLICY|ADR-0004]] - AI Repository Interaction Policy

---

# 12. Status

**Approved - recovered from repository evidence**

---

# Related Artefacts

* [[REG-0002_ADR_REGISTER|REG-0002]] registers ADR-0005 as an Architecture Decision Record.
* [[REG-0004_ACTION_REGISTER|REG-0004]] records actions linked to ADR-0005.
* [[CHR-0001_PLATFORM_CHARTER|CHR-0001]] records the strategic AIEMS and JARVIS relationship.
* [[PST-0001_PROGRAMME_STATUS|PST-0001]] records current programme status and governance position.
* [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] records the current accepted repository baseline.

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 24 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recovered approved ADR from repository evidence during ESR-0003 EIP-R2. |
