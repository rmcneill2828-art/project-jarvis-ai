# ADR-0003 - RTBO Engineering Decision Framework

---

## Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0003 |
| Title | RTBO Engineering Decision Framework |
| Version | 2.1 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 23 June 2026 |
| Review Trigger | See Section 10 |

---

# 1. Problem Statement

Engineering teams regularly make technical and architectural decisions under time pressure.

Without a consistent decision-making framework, important considerations can be overlooked, leading to unnecessary risk, technical debt and inconsistent outcomes.

---

# 2. Background

During Phase 0, the AI Engineering Platform (AEP) adopted a simple engineering decision framework known as RTBO:

**Review Twice. Build Once. Improve for Everyone.**

The framework was developed to encourage evidence-based decision making while maintaining disciplined engineering and delivery momentum.

---

# 3. Options Considered

## Option A - Ad-hoc Decision Making

### Advantages

- Fast.
- Minimal process.

### Disadvantages

- Inconsistent quality.
- Greater reliance on assumptions.
- Higher risk of avoidable mistakes.

---

## Option B - RTBO Engineering Decision Framework (Selected)

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

The AI Engineering Platform adopts RTBO as its primary engineering decision framework.

RTBO shall be applied to significant architectural, technical, security and governance decisions throughout the Platform.

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

RTBO is intended to improve engineering - not slow it down.

---

# 9. Evidence

This framework was developed through the collaborative engineering of the AI Engineering Platform.

It reflects practical engineering experience, governance principles and continuous improvement practices.

---

# 10. Review Trigger

Review if:

- RTBO becomes unnecessarily bureaucratic.
- The framework no longer supports effective delivery.
- Significant improvements are identified through Platform engineering experience.

---

# 11. Related Decisions

- [[ADR-0001_DOCUMENTATION_FIRST|ADR-0001]] - Documentation First Development
- [[ADR-0002_GIT_REPOSITORY_STRATEGY|ADR-0002]] - Git Repository Strategy
- [[ADR-0004_AI_REPOSITORY_INTERACTION_POLICY|ADR-0004]] - AI Repository Interaction Policy

---

# 12. Status

**Approved**

---

> **"Review Twice. Build Once. Improve for Everyone."**

---

# Subsequent OSE Relationships

The following relationships were added after original artefact creation to support repository navigation. They do not change the original decision, status or approval basis.

| Artefact | Relationship |
|----------|--------------|
| [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]] | Defines the retrospective OSE enrichment rule applied to this ADR. |
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Establishes Engineering Ecosystem Synchronisation and OSE as repository-compatible relationship support. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Playbook translating RTBO principles into Engineering Implementer behaviour. |
| [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] | Collaboration context applying RTBO-aligned human and AI engineering roles. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status for evidence-led engineering decisions. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Current accepted repository baseline and ESR-0009 handover point. |

---

## Related Artefacts

* [[REG-0002_ADR_REGISTER|REG-0002]] registers ADR-0003 as an Architecture Decision Record.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] defines engineering implementer behaviour aligned with RTBO principles.
* [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] defines collaboration context for human and AI engineering work.
* [[PST-0001_PROGRAMME_STATUS|PST-0001]] records current programme status and governance position.

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.1 | 2 July 2026 | Codex Engineering Implementer | Added subsequent OSE relationships for retrospective repository navigation. |
| 2.0 | 23 June 2026 | Programme Sponsor & Chief Engineering Advisor | Existing approved ADR version recorded before retrospective OSE enrichment. |
