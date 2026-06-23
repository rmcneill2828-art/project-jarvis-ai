# ADR-0003 — RTBO Engineering Decision Framework

---

## Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0003 |
| Title | RTBO Engineering Decision Framework |
| Version | 1.0 |
| Status | Approved |
| Owner | Project Sponsor & Chief Architect |
| Date Approved | 23 June 2026 |
| Review Trigger | See Section 10 |

---

# 1. Problem Statement

Engineering teams regularly make technical and architectural decisions under time pressure.

Without a consistent decision-making framework, important considerations can be overlooked, leading to unnecessary risk, technical debt and inconsistent outcomes.

---

# 2. Background

During Phase 0, Project JARVIS AI adopted a simple decision framework known as RTBO:

**Review Twice. Build Once. Improve for Everyone.**

The framework was developed to encourage evidence-based decision making while maintaining delivery momentum.

---

# 3. Options Considered

## Option A — Ad-hoc Decision Making

### Advantages

- Fast.
- Minimal process.

### Disadvantages

- Inconsistent quality.
- Greater reliance on assumptions.
- Higher risk of avoidable mistakes.

---

## Option B — RTBO Engineering Decision Framework (Selected)

### Advantages

- Encourages evidence-based decisions.
- Challenges assumptions before implementation.
- Improves engineering consistency.
- Reduces unnecessary rework.
- Supports continuous improvement.

### Disadvantages

- Requires discipline.
- May slightly increase decision time for significant changes.

---

# 4. Decision

Project JARVIS AI adopts RTBO as its primary engineering decision framework.

RTBO shall be applied to significant architectural, technical, security and governance decisions throughout the project.

---

# 5. Framework

## Review

Gather evidence.

Understand the problem.

Identify constraints.

---

## Review Again

Challenge assumptions.

Consider alternatives.

Verify available evidence.

Seek additional information where appropriate.

---

## Build

Implement the agreed solution.

Follow approved engineering standards.

Document significant changes.

---

## Improve

Review outcomes.

Capture lessons learned.

Update documentation where appropriate.

Continuously improve the engineering process.

---

# 6. Success Criteria

RTBO is considered successful when:

- Decisions are based upon evidence rather than assumptions.
- Technical debt is reduced.
- Rework decreases over time.
- Lessons learned are captured.
- Engineering quality improves continuously.

---

# 7. Benefits

- Better engineering decisions.
- Improved consistency.
- Reduced implementation risk.
- Encourages collaboration.
- Supports long-term maintainability.

---

# 8. Consequences

Important decisions require deliberate review before implementation.

Minor routine tasks should continue to use professional judgement without unnecessary process.

RTBO is intended to improve engineering—not slow it down.

---

# 9. Evidence

This framework was developed through the collaborative planning of Project JARVIS AI.

It reflects practical engineering experience, governance principles and continuous improvement practices.

---

# 10. Review Trigger

Review if:

- RTBO becomes unnecessarily bureaucratic.
- The framework no longer supports effective delivery.
- Significant improvements are identified through project experience.

---

# 11. Related Decisions

- ADR-0001 — Documentation First Development
- ADR-0002 — Git Repository Strategy
- ADR-0004 — Verify Before Deciding

---

# 12. Status

**Approved**

---

> **"Review Twice. Build Once. Improve for Everyone."**