# ADR-0004 - AI Repository Interaction Policy

---

## Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0004 |
| Title | AI Repository Interaction Policy |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 24 June 2026 |
| Review Trigger | Review if AI repository access, tooling, permissions or engineering workflow responsibilities change materially. |

---

# 1. Problem Statement

Project JARVIS AI uses AI collaborators to support repository engineering, governance maintenance and implementation activity.

Without an explicit repository interaction policy, AI-assisted repository work can exceed approved governance, weaken human accountability, or make repository changes without sufficient review and traceability.

---

# 2. Background

The repository contains historical approved references to ADR-0004 but the original ADR file was absent from `aiems/governance/decisions/` during ESR-0003 WS1 governance stabilisation.

Repository evidence records ADR-0004 as an approved governance decision dated 24 June 2026. [[REG-0002_ADR_REGISTER|REG-0002]] describes its intent as defining governance, approval model and responsibilities for AI-assisted repository interaction. [[REG-0004_ACTION_REGISTER|REG-0004]] records ACT-0004 as completed for creating the AI Repository Interaction Policy. [[REG-0003_RISK_REGISTER|REG-0003]] references ADR-0004 as mitigation for AI repository interaction exceeding approved governance.

This recovered ADR preserves that approved decision using repository evidence. The original detailed ADR text was not recoverable from the repository baseline.

---

# 3. Options Considered

## Option 1 - Allow AI repository interaction without a specific governance policy

This would reduce process overhead but would weaken approval discipline and make responsibility boundaries unclear.

## Option 2 - Prohibit AI repository interaction entirely

This would reduce governance risk but would prevent useful AI-assisted implementation, review and repository maintenance.

## Option 3 - Permit AI repository interaction only under approved governance and human accountability

This preserves AI-assisted engineering benefit while maintaining explicit approval, traceability and human ownership.

---

# 4. Decision

AI repository interaction is permitted only within the approved AIEMS governance model.

AI collaborators shall operate within assigned roles, approved scope and explicit human authority. Repository modification shall occur only when authorised by an approved engineering activity or direct Programme Sponsor instruction.

Human engineers remain accountable for repository direction, approval and final baseline acceptance. Operational repository execution responsibilities are governed by the current approved AIEMS workflow in [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]].

---

# 5. Rationale

AI-assisted engineering improves speed, consistency and review depth, but repository authority must remain governed.

This decision establishes that AI repository activity is a controlled engineering action, not an autonomous right. It preserves the repository as the authoritative engineering baseline while allowing AI collaborators to assist within clear boundaries.

---

# 6. Success Criteria

This decision is successful when:

- AI repository work is traceable to approved engineering authority.
- AI collaborators remain within approved scope.
- Human approval is required before controlled repository change.
- Repository execution responsibilities are assigned and controlled by the current approved AIEMS workflow in [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]].
- Repository verification and baseline acceptance remain explicit workflow steps.

---

# 7. Benefits

- Preserves human accountability for repository state.
- Reduces risk of unauthorised AI repository changes.
- Supports controlled AI-assisted engineering.
- Improves traceability between implementation work and approved scope.
- Provides governance basis for AI repository interaction controls.

---

# 8. Consequences

- AI collaborators must operate within approved engineering packages or direct Programme Sponsor instruction.
- Repository changes require explicit scope control and completion reporting.
- Some engineering work may proceed more slowly to preserve governance integrity.
- AI role boundaries must remain visible in operational artefacts such as [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] and [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]].

---

# 9. Evidence

Recovered from repository evidence during ESR-0003 EIP-R2.

Evidence includes:

- [[REG-0002_ADR_REGISTER|REG-0002]] row for ADR-0004: AI Repository Interaction Policy, Governance, Approved, 24 Jun 2026.
- [[REG-0003_RISK_REGISTER|REG-0003]] RSK-0008 mitigation referencing AI Repository Interaction Policy (ADR-0004).
- [[REG-0004_ACTION_REGISTER|REG-0004]] ACT-0004 recording creation of AI Repository Interaction Policy as completed on 24 Jun 2026.
- [[ESR-0001_ENGINEERING_SESSION_REPORT|ESR-0001]] and [[ESR-0002_ENGINEERING_SESSION_REPORT|ESR-0002]] references to ADR-0004 recovery or formal supersession.
- [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0001 approved backlog item for ADR-0004 recovery or formal supersession.

---

# 10. Review Trigger

Review this ADR if:

- AI collaborator roles or repository permissions materially change.
- GitHub, Codex or other AI tooling capabilities change materially.
- AIEMS introduces new repository automation.
- Repository governance, approval or verification workflow changes materially.

---

# 11. Related Decisions

- [[ADR-0001_DOCUMENTATION_FIRST|ADR-0001]] - Documentation First Development
- [[ADR-0002_GIT_REPOSITORY_STRATEGY|ADR-0002]] - Git Repository Strategy
- [[ADR-0003_RTBO_ENGINEERING_DECISION_FRAMEWORK|ADR-0003]] - RTBO Engineering Decision Framework
- [[ADR-0005_AIEMS_STRATEGIC_SCOPE|ADR-0005]] - AIEMS Strategic Scope

---

# 12. Status

**Approved - recovered from repository evidence**

---

# Related Artefacts

* [[REG-0002_ADR_REGISTER|REG-0002]] registers ADR-0004 as an Architecture Decision Record.
* [[REG-0003_RISK_REGISTER|REG-0003]] records AI repository interaction risk mitigation.
* [[REG-0004_ACTION_REGISTER|REG-0004]] records the completed action to create the AI Repository Interaction Policy.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] define operational AI collaboration responsibilities.
* [[RBL-0007_REPOSITORY_BASELINE|RBL-0007]] records the current accepted repository baseline.

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 24 June 2026 | Programme Sponsor & Chief Engineering Advisor | Recovered approved ADR from repository evidence during ESR-0003 EIP-R2. |
