# GDE-0001 - Project Knowledge Map

> *"Bounded onboarding scales. Exhaustive onboarding does not."*

**Version:** 1.1

---

# 1. Document Control

| Field | Value |
|------|------|
| Artefact ID | GDE-0001 |
| Title | Project Knowledge Map |
| Version | 1.1 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Parent | [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] |
| Review Frequency | Triggered by session initialisation workflow change |

---

# 2. Purpose

GDE-0001 defines the tiered knowledge structure AI collaborators use for Engineering Session initialisation.

It replaces exhaustive mandatory reading of the full AIEMS History and Full Chat archive with a bounded current-state reading set, plus search-on-demand access to historical evidence.

This artefact exists because mandatory session-start reading grows without bound as Engineering Sessions accumulate. [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] previously required every session to review all AIEMS History ([[HST-0001_ESR-0001_CHAT_HISTORY|HST]]) and Full Chat ([[FCH-0000_INITIAL_PROJECT_SESSION_FULL_CHAT_HISTORY|FCH]]) artefacts in full. That approach does not scale: it was already fourteen files deep at ESR-0014 and grows by two files every session indefinitely.

GDE-0001 does not retire, delete or devalue AIEMS History or Full Chat artefacts. They remain the authoritative historical record. GDE-0001 changes only when they are read: on demand, by search, rather than exhaustively, by default.

---

# 3. Scope

## In Scope

- Defining the knowledge tier structure.
- Defining the mandatory session initialisation set.
- Defining the Historical Archive access rule.
- Amending [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] session initialisation and WP0A guidance to reference this tiering.

## Out of Scope

- Retiring, deleting or archiving any HST or FCH artefact.
- Changing [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]]'s Authority Order, which this Guide operationalises rather than replaces.
- Correcting unrelated [[PST-0001_PROGRAMME_STATUS|PST-0001]] or repository validation staleness, which is tracked as separate engineering work.

---

# 4. Knowledge Tier Structure

```text
Project Knowledge
├── Current State        -> PST-0001
├── Architecture           -> MOD-0001, SAM-0001, AAM-0001, UAM-0001,
│                             JARVIS Product Architecture, CURRENT_ARCHITECTURE.md
├── Active Standards        -> STD-0001, STD-0002, STD-0003, STD-0004
├── Current ESR              -> the latest Engineering Session Report only
└── Historical Archive        -> HST-*, FCH-*, superseded and closed ESRs
                                 (searched on demand, not mandatory reading)
```

---

# 5. Mandatory Session Initialisation Set

Every Engineering Session shall begin by reviewing only:

1. README.md.
2. Current State ([[PST-0001_PROGRAMME_STATUS|PST-0001]]).
3. Architecture tier, as referenced by the Current State artefact.
4. Active Standards, where the session's work touches artefact creation or modification.
5. Current ESR only - the latest Engineering Session Report, not prior closed sessions.
6. [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]].
7. [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]].
8. The approved Engineering Implementation Package for the session, where one exists.

This set is bounded: its size does not grow as further Engineering Sessions close.

---

# 6. Historical Archive Access Rule

AIEMS History ([[HST-0001_ESR-0001_CHAT_HISTORY|HST]]) and Full Chat ([[FCH-0000_INITIAL_PROJECT_SESSION_FULL_CHAT_HISTORY|FCH]]) artefacts, and closed Engineering Session Reports prior to the current one, are reference material. They are searched on demand rather than read exhaustively at every session start.

Search shall be performed when:

- the Current State or Architecture tier explicitly points to a specific historical record for decision rationale; or
- an AI collaborator or the Programme Sponsor determines that a decision's reasoning is not captured in current controlled artefacts and historical evidence is required.

Current State and Architecture artefacts should carry breadcrumbs to specific HST/FCH entries where only the archive holds the rationale for a decision (for example, "see HST-0009 for the Sentinel/Guardian boundary discussion"). This keeps the archive reachable without requiring exhaustive reads.

---

# 7. Authority

This Guide operationalises the authority ordering already established in [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]] Section 4, which ranks historical conversations below controlled artefacts and Engineering Session Reports. It does not change that ordering, and it does not reduce the evidential status of HST or FCH artefacts - it changes only when they are read.

Where this Guide conflicts with [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] or [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]], those artefacts take precedence, consistent with [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] Section 6.

---

# 8. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Session initialisation and WP0A guidance amended to reference this tiering. |
| [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] | Collaboration context that defers to PBK-0001 for session initialisation detail. |
| [[OSE-0001_ORGANIC_SEMANTIC_ENHANCEMENT_UPDATE_RULE|OSE-0001]] | Defines the authority ordering this Guide operationalises. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current State tier source artefact. |
| [[STD-0001_CONTROLLED_ARTEFACT_STANDARD|STD-0001]] | Defines the Guide (GDE) artefact category used by this artefact. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Registers this artefact as a controlled AIEMS Guide. |
| [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] | Parent engineering session; this artefact was created as ESR-0014 post-closure work. |

---

# 9. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1 | 8 July 2026 | Claude Engineering Implementer | Corrected Status from Draft to Approved to comply with STD-0001 section 13 versioning (Version 1.0 requires Approved status, not Draft). This artefact is already operationally binding - referenced and followed by PBK-0001, COC-0001 and PST-0001. |
| 1.0 | 8 July 2026 | Claude Engineering Implementer | Initial Project Knowledge Map created as ESR-0014 post-closure work, bounding mandatory session initialisation reading and moving AIEMS History and Full Chat artefacts to search-on-demand access. |
