# ADR-0002 — Git Repository Strategy

---

## Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0002 |
| Title | Git Repository Strategy |
| Version | 1.0 |
| Status | Approved |
| Owner | Project Sponsor & Chief Architect |
| Date Approved | 23 June 2026 |
| Review Trigger | See Section 10 |

---

# 1. Problem Statement

Project JARVIS AI is developed across multiple devices.

Without a consistent version control strategy there is a risk of conflicting changes, knowledge loss and inconsistent project history.

---

# 2. Background

The project is developed using a work laptop and a home PC.

The engineering workflow requires seamless transition between development environments while maintaining a complete and reliable history of the project.

Git was selected as the version control system, with GitHub providing the primary hosted repository.

---

# 3. Options Considered

## Option A — Manual File Synchronisation

### Advantages

- Simple to understand.
- No version control knowledge required.

### Disadvantages

- High risk of conflicting versions.
- No reliable history.
- Difficult collaboration.
- Increased possibility of data loss.

---

## Option B — Git with GitHub (Selected)

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

Project JARVIS AI shall use Git as its version control system.

GitHub shall be used as the primary hosted repository.

The GitHub repository becomes the central location for synchronising approved project changes between authorised development devices.

---

# 5. Rationale

A professional version control strategy is essential for a long-term engineering programme.

Using Git enables traceability, controlled change, and confidence when evolving the platform.

---

# 6. Success Criteria

This decision is considered successful when:

- Development continues seamlessly across multiple devices.
- Every approved change is committed to Git.
- Repository history remains complete and understandable.
- GitHub accurately reflects the approved project baseline.

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

- ADR-0001 — Documentation First Development
- ADR-0003 — RTBO Engineering Process
- ADR-0009 — Multi-Device Development Strategy

---

# 12. Status

**Approved**

---

> **Version control protects the project's history; disciplined commits protect its quality.**