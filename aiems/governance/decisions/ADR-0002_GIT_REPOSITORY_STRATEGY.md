# ADR-0002 - Git Repository Strategy

---

## Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0002 |
| Title | Git Repository Strategy |
| Version | 2.1 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 23 June 2026 |
| Review Trigger | See Section 10 |

---

# 1. Problem Statement

The AI Engineering Platform (AEP) is developed across multiple authorised development environments.

Without a consistent version control strategy there is a risk of conflicting changes, knowledge loss and an inconsistent engineering history.

---

# 2. Background

The Platform is developed across multiple authorised development environments, including a work laptop and a home PC.

The engineering workflow requires seamless transition between development environments while maintaining a complete, reliable and auditable engineering history.

Git was selected as the version control system, with GitHub providing the primary hosted repository.

---

# 3. Options Considered

## Option A - Manual File Synchronisation

### Advantages

- Simple to understand.
- No version control knowledge required.

### Disadvantages

- High risk of conflicting versions.
- No reliable history.
- Difficult collaboration.
- Increased possibility of data loss.

---

## Option B - Git with GitHub (Selected)

### Advantages

- Complete project history.
- Reliable version control.
- Multi-device development.
- Rollback capability.
- Supports future collaboration.
- Industry standard engineering practice.

### Disadvantages

- Initial learning curve.
- Requires disciplined commit practices.

---

# 4. Decision

The AI Engineering Platform adopts Git as its version control system.

GitHub shall remain the primary hosted repository.

The GitHub repository represents the authoritative source for synchronising approved engineering changes between authorised development environments.

---

# 5. Rationale

A professional version control strategy is essential for a long-term engineering platform.

Using Git enables traceability, controlled change, and confidence when evolving the platform.

---

# 6. Success Criteria

This decision is considered successful when:

- Development continues seamlessly across multiple devices.
- Every approved change is committed to Git.
- Repository history remains complete and understandable.
- GitHub accurately reflects the approved Platform baseline.

---

# 7. Benefits

- Reliable project history.
- Multi-device development.
- Easier recovery from errors.
- Supports future contributors.
- Enables structured engineering workflows.

---

# 8. Consequences

Developers must follow agreed Git workflows.

All significant work should be committed with meaningful commit messages.

---

# 9. Evidence

This decision is based upon:

- Project requirements.
- Multi-device development objectives.
- Long-term maintainability.
- Industry best practice.

---

# 10. Review Trigger

Review if:

- The project adopts a different repository platform.
- The development workflow changes significantly.
- New collaboration requirements emerge.

---

# 11. Related Decisions

- [[ADR-0001_DOCUMENTATION_FIRST|ADR-0001]] - Documentation First Development
- [[ADR-0003_RTBO_ENGINEERING_DECISION_FRAMEWORK|ADR-0003]] - RTBO Engineering Process
- ADR-0009 - Multi-Device Development Strategy

---

# 12. Status

**Approved**

---

> **Version control protects the project's history; disciplined commits protect its quality.**

---

# Subsequent OSE Relationships

The following relationships were added after original artefact creation to support repository navigation. They do not change the original decision, status or approval basis.

| Artefact | Relationship |
|----------|--------------|
| [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]] | Defines the retrospective OSE enrichment rule applied to this ADR. |
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Establishes Engineering Ecosystem Synchronisation and OSE as repository-compatible relationship support. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Controlled artefact register governed through repository-first source control. |
| [[REG-0002_ADR_REGISTER|REG-0002]] | ADR register preserving decision traceability in the Git repository. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status confirming repository-first engineering continuity. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Current accepted repository baseline and ESR-0009 handover point. |

---

## Related Artefacts

* [[REG-0002_ADR_REGISTER|REG-0002]] registers ADR-0002 as an Architecture Decision Record.
* [[REG-0004_ACTION_REGISTER|REG-0004]] records actions linked to repository and governance activity.
* [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] records the current accepted repository baseline and ESR-0009 handover point.
* [[PST-0001_PROGRAMME_STATUS|PST-0001]] records current programme status and governance position.

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.1 | 2 July 2026 | Codex Engineering Implementer | Added subsequent OSE relationships for retrospective repository navigation. |
| 2.0 | 23 June 2026 | Programme Sponsor & Chief Engineering Advisor | Existing approved ADR version recorded before retrospective OSE enrichment. |
