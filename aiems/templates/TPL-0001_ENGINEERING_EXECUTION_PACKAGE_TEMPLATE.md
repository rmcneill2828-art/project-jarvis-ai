# TPL-0001 - Engineering Implementation Package Standard and Template

> *"A repeatable execution package turns approved intent into governed delivery."*

**Version:** 1.0

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | TPL-0001 |
| Title | Engineering Implementation Package Standard and Template |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[CHR-0002_ENGINEERING_CONSTITUTION|CHR-0002]] |
| Effective Date | 6 October 2026 |
| Review Frequency | At Engineering Execution Package review or template change |

---

# 2. Purpose

Defines the format, lifecycle, numbering and approval rules for an Engineering Implementation Package (EIP), and gives its template. Replaces the ESR-0009-era Engineering Execution Package template (TPL-0001 0.2), which no Work Package has used since EIPs superseded it. EBG-0008, ESR-0061 WP1b.

# 3. Numbering and Location

`EIP-ESR<session>-<nnn>_<TITLE>.md` in `aiems/governance/reviews/`, numbered in creation order within the session, registered in REG-0001 when created.

# 4. Lifecycle and Approval

| Step | Code WP (rule A6) | Documentation-only WP (rule A5) |
|---|---|---|
| 1 | EIP drafted with its evidence pack (Section 6) and commit contents | EIP drafted with the exact text and the full commit contents (Section 5, item 4A) |
| 2 | Independent design review (both reviewers if high-risk) | Independent review |
| 3 | Programme Sponsor design approval (chat; no commit) | - |
| 4 | Implement; independent review of the built result | Apply the exact text |
| 5 | Sponsor Approval Service approval; `submit-response`; commit | Sponsor Approval Service approval; `submit-response`; commit |
| 6 | CI on every platform; post-commit pre-check and independent review | Same |

Version 0.x while in draft; 1.0 when approved and implemented. Every review verdict and every change made after a review is recorded in the EIP itself.

# 5. Mandatory Sections

1. **Document Control** - ID, title, version, status, session, Work Package, risk class (standard or high-risk).
2. **Purpose** - what is delivered and which backlog items it closes.
3. **Repository Context Investigated** - what the Engineering Implementer read and verified, with file references.
4. **Scope** - for code, the design; for documentation, the exact text.
4A. **Commit Contents** - every file the commit will add or change, including session records (the ESR, register rows, Working Reports, the EIP itself). An A5 approval covers exactly these files and this text; nothing else may enter that commit.
5. **Evidence Pack** - Section 6 below (code WPs).
6. **Explicitly Out of Scope** - including disclosed residuals.
7. **Validation Requirements** - tests, validator, CI jobs, live checks.
8. **Questions for the Engineering Reviewer.**
9. **Review Record** - each verdict, its findings and their dispositions.
10. **Version History.**

# 6. Evidence Pack (R3)

Built from ESR-0060 WP2, where three design rounds missed facts a source check would have caught. Required for every code WP before design review:

| Item | Content |
|---|---|
| API facts | Every library, OS or framework behaviour the design relies on, checked against source or documentation, with the reference |
| Platform coverage | Windows and macOS behaviour, stated separately; any platform-specific code path named |
| CI | Which CI jobs will exercise the change, on which platforms; any CI change needed |
| Tests | The test list, and which tests are shown failing on the old code |
| New dependencies and features | Every new package, crate, crate feature, OS permission or capability - listed so the design approval covers them (rule A4) |

# 7. ESR Work Package Entry (R11)

An Engineering Session Report records each Work Package as one table row; detail stays in the EIP and the bridge transcript.

| WP | EIP | Commit | CI run | Design review | Post-commit review | Decisions | Deviations |
|---|---|---|---|---|---|---|---|
| WPn | EIP-ESRxxxx-nnn vX | `abc1234` | run id, result | reviewer, verdict, findings | reviewer, verdict | approvals with timestamps | anything not as designed |

# 8. Template

```text
# EIP-ESRxxxx-nnn - <Title>
# 1. Document Control   (table: ID, Title, Version, Status, Session, Work Package, Risk class)
# 2. Purpose
# 3. Repository Context Investigated
# 4. Scope
# 4A. Commit Contents
# 5. Evidence Pack
# 6. Explicitly Out of Scope
# 7. Validation Requirements
# 8. Questions for the Engineering Reviewer
# 9. Review Record
# 10. Version History
```

# 9. Related Artefacts

[[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (Approval Economy, Delivery Cadence and Independent Review), [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]], [[CHR-0002_ENGINEERING_CONSTITUTION|CHR-0002]].

# 10. Version History

| Version | Date | Author | Summary |
|---|---|---|---|
| 1.0 | 6 October 2026 | Claude Engineering Implementer | ESR-0061 WP1b per EIP-ESR0061-001 (EBG-0008, R3, R11): rewritten as the EIP standard and template - numbering, lifecycle and approval (A5/A6), mandatory sections including the full commit contents, evidence pack, tabular ESR entry. Replaces the unused 0.2 Engineering Execution Package template. |
| 0.2 | 8 July 2026 | Claude Engineering Implementer | Replaced ChatGPT/Codex role naming with Engineering Reviewer/Engineering Implementer throughout, decoupling this template from named AI products. |
| 0.1 | 2 July 2026 | Codex Engineering Implementer | Initial Engineering Execution Package Template created under EIP-ESR0009-002. |
