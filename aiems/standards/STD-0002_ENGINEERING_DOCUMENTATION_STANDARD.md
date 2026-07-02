# STD-0002 - Engineering Documentation Standard

> *"Engineering documentation exists to improve engineering decisions. Its value is measured not by its volume, but by the clarity, accuracy and traceability it provides."*

**Version:** 1.2

---

# Document Control

| Field | Value |
|------|------|
| Artefact ID | STD-0002 |
| Title | Engineering Documentation Standard |
| Version | 1.2 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Review Frequency | Triggered or Periodic (as defined by the artefact) |
| Effective Date | 26 June 2026 |
| Next Review | As Required |

---

# 1. Purpose

This standard defines the principles, language and quality requirements for engineering documentation produced within the AI Engineering Management System (AIEMS).

Its objectives are to:

- improve engineering communication;
- promote consistent documentation practices;
- reduce ambiguity;
- support engineering governance;
- provide traceable engineering evidence;
- enable long-term maintainability of engineering knowledge.

This standard complements [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] by defining how engineering documentation shall be written rather than how Controlled Artefacts shall be governed.

---

# 2. Scope

This standard applies to all engineering documentation governed by AIEMS, including Controlled Artefacts and any supporting engineering documentation intended to influence engineering decisions.

It applies equally to documentation produced by:

- human contributors;
- AI-assisted engineering processes; and
- collaborative engineering activities.

---

# 3. Engineering Documentation Definition

Engineering documentation is information created to communicate engineering intent, decisions, architecture, requirements, standards, procedures or evidence.

Engineering documentation shall:

- support engineering activities;
- communicate approved knowledge clearly;
- remain technically accurate;
- be maintainable throughout its lifecycle.

Documentation that does not contribute to engineering understanding or decision making should not be retained as controlled engineering documentation.

---

# 4. Documentation Philosophy

Engineering documentation exists to enable better engineering.

Documentation shall support engineering activities rather than become an objective in itself.

Documentation should reduce uncertainty, preserve organisational knowledge and improve future engineering decisions.

The value of documentation is determined by its usefulness, accuracy and maintainability—not by its length.

---

# 5. Engineering Documentation Principles

Engineering documentation within AIEMS shall be guided by the following principles.

## Documentation Supports Engineering

Documentation exists to improve engineering outcomes.

---

## Write for the Next Engineer

Documentation shall assume no prior knowledge beyond the information referenced within the engineering baseline.

---

## Record Decisions, Not Conversations

Controlled documentation shall record approved decisions, rationale and evidence rather than historical discussion.

---

## Evidence Before Opinion

Engineering conclusions shall be supported by evidence, analysis or approved decisions wherever practicable.

---

## One Source of Truth

Engineering information should exist in one authoritative location.

Duplication should be avoided.

---

## Minimise Cognitive Load

Documentation should communicate information using the simplest language capable of conveying the required engineering meaning.

Complexity shall only be introduced where technically necessary.

---

# 6. Writing Standards

Engineering documentation shall communicate information clearly, accurately and consistently.

Documentation should:

- use plain English;
- use active voice where practical;
- keep sentences concise;
- express one primary idea per paragraph;
- avoid unnecessary technical jargon;
- avoid marketing or promotional language;
- avoid ambiguous terminology.

Documentation shall prioritise clarity over complexity.

---

# 7. Normative Language

Where requirements are stated, the following terminology shall be used consistently.

| Term | Meaning |
|------|---------|
| **Shall** | Mandatory requirement |
| **Should** | Strong recommendation |
| **May** | Optional permission |
| **Will** | Future intention or expected outcome |
| **Can** | Capability or possibility |

These terms shall be used consistently throughout AIEMS Controlled Artefacts.

---

# 8. Documentation Structure

The structural requirements of Controlled Artefacts are defined by [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]].

Engineering documentation should:

- use meaningful headings;
- present information in a logical order;
- separate concepts into clearly defined sections;
- avoid unnecessary repetition.

Documentation should guide the reader naturally through the engineering subject.

---

# 9. Engineering Evidence

Engineering documentation shall distinguish between:

- verified facts;
- approved decisions;
- recommendations;
- assumptions;
- future proposals.

Where engineering conclusions are presented, the supporting rationale should also be documented.

Evidence should be referenced rather than duplicated wherever practical.

---

# 10. Documentation Quality Characteristics

Engineering documentation should demonstrate the following quality characteristics.

| Characteristic | Description |
|----------------|-------------|
| Accuracy | Technically correct and factually accurate |
| Clarity | Easily understood by the intended engineering audience |
| Consistency | Uses approved terminology, structure and style |
| Traceability | References related artefacts and supporting evidence |
| Maintainability | Straightforward to review and update |
| Relevance | Contains only information that supports engineering objectives |
| Verifiability | Statements can be confirmed through evidence or approved governance |

These characteristics shall form the basis of documentation reviews and Engineering Reviews.

---

# 11. Tables, Lists and Diagrams

Tables should be used where they improve comparison or readability.

Bullet lists should be used where the order of items is not significant.

Numbered lists should be used where sequence or procedural order is important.

Diagrams should:

- communicate engineering concepts clearly;
- remain consistent with approved architecture;
- avoid unnecessary detail;
- be maintained alongside the associated documentation.

Visual representations shall support engineering understanding rather than replace documented requirements.

---

# 12. Cross-Referencing

Engineering documentation should reference authoritative AIEMS artefacts instead of reproducing their content.

Cross-references shall:

- identify artefacts using their unique Artefact Identifier;
- remain accurate and current;
- support engineering traceability.

Where conflicts arise, the authoritative Controlled Artefact shall take precedence.

---

# 13. Documentation Reviews

Engineering documentation shall be reviewed:

- before initial approval;
- following significant engineering change;
- when affected by an approved [[REG-0002_ADR_REGISTER|Architecture Decision Record]];
- when required by a [[SAR-0001_PHASE_1_STRATEGIC_ALIGNMENT_REVIEW|Strategic Alignment Review]];
- when improvements are identified through Engineering Reviews.

Reviews shall verify both technical accuracy and compliance with this standard.

---

# 14. Engineering Documentation as a Deliverable

Engineering documentation is a deliverable of the engineering process.

Documentation shall be planned, reviewed, approved and maintained with the same level of discipline applied to software, architecture and governance artefacts.

Engineering activities shall not be considered complete until the associated documentation accurately reflects the approved engineering baseline.

---

# 15. Compliance

Compliance with this standard shall be demonstrated through Engineering Reviews or other approved governance activities.

Documentation is considered compliant when it:

- communicates engineering intent clearly;
- follows the writing principles defined by this standard;
- uses normative language consistently where applicable;
- references authoritative artefacts appropriately;
- demonstrates the required documentation quality characteristics;
- remains current and technically accurate.

Non-conformities shall be recorded and corrected through the AIEMS governance process.

---

# 16. Exceptions

Exceptions to this standard shall only be permitted where:

- there is a justified engineering reason;
- the exception has been formally reviewed;
- the exception has been approved through an Architecture Decision Record or equivalent governance mechanism.

Approved exceptions shall remain documented and traceable.

---

# 17. Maintenance of this Standard

This standard shall be reviewed when:

- improvements are identified through Engineering Reviews;
- documentation practices evolve significantly;
- AIEMS governance changes;
- new documentation categories are introduced;
- Strategic Alignment Reviews recommend revision.

The Programme Sponsor is responsible for ensuring that this standard remains current and effective.

---

# Guiding Principle

> *"Good engineering documentation does not describe engineering after the fact; it enables better engineering before, during and after implementation."*

---

## OSE Relationships

| Artefact | OSE Relationship |
|----------|------------------|
| [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]] | Defines the retrospective relationship-only enrichment rule applied to documentation artefacts. |
| [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] | Defines controlled artefact structure that this standard complements. |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Provides vision-to-documentation traceability context. |
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Establishes Engineering Ecosystem Synchronisation and the repository-compatible OSE context. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Records authoritative artefact identity, ownership, status and current version. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Records current programme readiness and approved standards position. |

---
## Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] | Defines controlled artefact structure that this standard complements. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Records controlled artefacts subject to documentation quality requirements. |
| [[REG-0002_ADR_REGISTER|REG-0002]] | Records decisions that may affect documentation requirements or exceptions. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status and approved standards position. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|-------------------------------------------|--------------------------------------------------------------|
| 1.0 | 24 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Engineering Documentation Standard establishing the principles, language and quality requirements for engineering documentation within AIEMS. |
| 1.1 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Approved and baselined following engineering review and section numbering remediation. |
| 1.2 | 2 July 2026 | Codex Engineering Implementer | Added retrospective OSE relationships to improve semantic traceability without changing documentation requirements. |
