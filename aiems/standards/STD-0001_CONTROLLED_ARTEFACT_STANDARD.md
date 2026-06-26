# STD-0001 – Controlled Artefact Standard

> *"A controlled artefact is more than a document—it is governed engineering evidence. Consistent artefacts enable consistent engineering."*

**Version:** 1.2

---

# Document Control

| Field | Value |
|------|------|
| Artefact ID | STD-0001 |
| Title | Controlled Artefact Standard |
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

This standard defines the minimum requirements for all Controlled Artefacts created, maintained and governed within the **AI Engineering Management System (AIEMS)**.

The objectives of this standard are to:

- establish a consistent structure for Controlled Artefacts;
- ensure engineering traceability;
- support governance and quality assurance;
- simplify maintenance and review;
- improve readability and reuse across the AI Engineering Platform.

All Controlled Artefacts shall comply with this standard unless an approved Architecture Decision Record explicitly states otherwise.

---

# 2. Scope

This standard applies to all Controlled Artefacts managed within AIEMS.

It applies regardless of whether the artefact is created by:

- a human contributor;
- an AI-assisted engineering process; or
- a collaborative engineering activity.

This standard applies throughout the complete lifecycle of each Controlled Artefact.

---

# 3. Controlled Artefact Categories

AIEMS recognises the following categories of Controlled Artefacts.

| Prefix | Artefact Type |
|---------|---------------|
| CHR | Charter |
| ADR | Architecture Decision Record |
| STD | Standard |
| POL | Policy |
| PRO | Procedure |
| MOD | Model |
| REG | Register |
| REV | Review |
| SAR | Strategic Alignment Review |
| GDE | Guide |
| TMP | Template |

Additional categories may be introduced through an approved Architecture Decision Record.

---

# 4. Standard Objectives

Controlled Artefacts shall provide:

- consistency;
- traceability;
- accountability;
- maintainability;
- repeatability; and
- governance evidence.

Every Controlled Artefact shall contribute to the engineering integrity of the AI Engineering Platform.

---

# 5. Controlled Artefact Principles

Every Controlled Artefact shall support the following engineering principles.

## Single Source of Truth

Each engineering concept should have one authoritative Controlled Artefact.

Duplicate or conflicting information should be avoided.

---

## Evidence Before Opinion

Controlled Artefacts shall record approved engineering knowledge supported by evidence, review or formal decision making.

---

## Traceability

Engineering decisions, changes and relationships shall remain traceable throughout the artefact lifecycle.

---

## Minimal Duplication

Controlled Artefacts should reference authoritative artefacts rather than reproduce their content.

---

## Continual Improvement

Controlled Artefacts shall evolve through controlled engineering change and continual learning while preserving governance and traceability.

---

# 6. Applicability

Unless specifically exempted, every Controlled Artefact shall comply with the requirements defined within this standard.

Where another AIEMS standard defines additional requirements, those requirements shall supplement rather than replace this standard.

If conflicting requirements are identified, this standard shall take precedence unless superseded by an approved Architecture Decision Record.

---

# 7. Controlled Artefact Definition

A Controlled Artefact is an engineering artefact that is subject to formal governance under AIEMS.

A Controlled Artefact shall:

- have a unique Artefact Identifier;
- be maintained under version control;
- have an identified Owner;
- be subject to review and approval;
- maintain a version history;
- be recorded within the Controlled Artefact Register where applicable.

Artefacts that do not meet these criteria shall not be regarded as Controlled Artefacts.

---

# 8. Mandatory Artefact Structure

Unless specifically exempted, every Controlled Artefact shall contain the following sections.

## Mandatory Sections

- Title
- Document Control
- Purpose
- Main Content
- Version History

The following sections are recommended where applicable:

- Scope
- Definitions
- References
- Appendices

The use of optional sections shall be determined by the purpose of the artefact.

---

# 9. Document Control Requirements

Every Controlled Artefact shall include a Document Control section.

The minimum required fields are:

| Field | Requirement |
|------|-------------|
| Artefact ID | Mandatory |
| Title | Mandatory |
| Version | Mandatory |
| Status | Mandatory |
| Owner | Mandatory |
| Approved By | Mandatory |
| Classification | Mandatory |
| Review Frequency | Triggered or Periodic (as defined by the artefact) |


Additional fields may be added where required by the specific artefact type.

---

# 10. Artefact Lifecycle

Every Controlled Artefact shall exist within one of the following lifecycle states.

| Status | Meaning |
|---------|---------|
| Draft | Initial development. Content may change significantly. |
| In Review | Under formal engineering review. |
| Approved | Current controlled version. |
| Superseded | Replaced by a newer approved version. |
| Archived | Retained for historical reference. No further maintenance is expected. |

Only artefacts with a status of **Approved** shall be regarded as part of the current engineering baseline.

---

# 11. Review Requirements

Controlled Artefacts shall be reviewed:

- before initial approval;
- following significant engineering change;
- when triggered by an Architecture Decision Record;
- when required by a Strategic Alignment Review;
- at other intervals defined by the owning artefact.

Engineering Reviews should be used to verify compliance with this standard.

---

# 12. Ownership and Accountability

Every Controlled Artefact shall have a designated Owner.

The Owner is responsible for:

- maintaining the artefact;
- ensuring technical accuracy;
- coordinating reviews;
- ensuring version history is maintained;
- recommending approval where appropriate.

Approval authority shall be defined by the governance applicable to the artefact type.

---

# 13. Versioning Requirements

Controlled Artefacts shall follow a consistent versioning approach.

| Version | Description |
|---------|-------------|
| 0.x | Draft development versions. Not approved for operational use. |
| 1.0 | Initial approved baseline. |
| 1.x | Minor approved revisions that do not fundamentally alter the artefact's purpose or intent. |
| 2.0+ | Major revisions introducing significant structural or functional changes. |

Version numbers shall increase sequentially and shall be recorded within the Version History.

---

# 14. Naming and Identification

Every Controlled Artefact shall possess a unique Artefact Identifier.

Identifiers shall use the approved AIEMS naming convention.

```
<PREFIX>-<NUMBER>_<DESCRIPTIVE_NAME>.md
```

Examples include:

```
CHR-0001_PLATFORM_CHARTER.md
ADR-0003_RTBO_ENGINEERING_DECISION_FRAMEWORK.md
STD-0001_CONTROLLED_ARTEFACT_STANDARD.md
PRO-0001_CHANGE_MANAGEMENT_PROCEDURE.md
```

Identifiers shall not be reused.

Superseded artefacts shall retain their original identifiers.

---

# 15. Cross-Referencing

Where relationships exist between Controlled Artefacts, those relationships should be explicitly referenced.

Cross-references shall:

- identify the related artefact by its identifier;
- remain current and accurate;
- avoid unnecessary duplication of content.

Controlled Artefacts should reference authoritative sources rather than reproduce them.

---

# 16. Compliance

Compliance with this standard shall be verified through Engineering Reviews or other approved governance activities.

A Controlled Artefact is considered compliant when it:

- follows the mandatory structure defined by this standard;
- contains the required Document Control information;
- maintains an appropriate Version History;
- has an assigned Owner;
- has an approved lifecycle status;
- complies with applicable AIEMS governance.

Non-conformities shall be recorded and corrected through the AIEMS change process.

---

# 17. Exceptions

Exceptions to this standard shall only be permitted where:

- there is a justified engineering reason;
- the exception has been reviewed;
- the exception is approved through an Architecture Decision Record or equivalent governance mechanism.

Approved exceptions shall be documented and remain traceable.

---

# 18. Maintenance of this Standard

This standard shall be reviewed when:

- new Controlled Artefact categories are introduced;
- governance processes change significantly;
- improvements are identified through Engineering Reviews;
- Strategic Alignment Reviews recommend revision.

The Programme Sponsor is responsible for ensuring that this standard remains current and effective.

---

# Guiding Principle

> *"Consistent engineering begins with consistent evidence. Every Controlled Artefact contributes to the integrity, traceability and continual improvement of the AI Engineering Platform."*

---

# Version History

| Version | Date | Author | Summary |
|---------|------------|-------------------------------------------|--------------------------------------------------------------|
| 1.0 | 24 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Controlled Artefact Standard establishing the mandatory requirements for all AIEMS Controlled Artefacts. |
| 1.1 | 24 June 2026 | Programme Sponsor & Chief Engineering Advisor | Perfective improvements introducing Controlled Artefact Principles, Review Frequency and clarification of mandatory artefact structure. |
| 1.2 | 26 June 2026 | Programme Sponsor & Chief Engineering Advisor | Approved and baselined following engineering review and metadata remediation. |
