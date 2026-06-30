# STD-0004 - Validation and Quality Assurance Standard

> *"A deliverable is complete when evidence shows it is correct, reviewed and ready for the repository baseline."*

**Version:** 1.1

---

# 1. Document Control

| Field | Value |
|------|------|
| Artefact ID | STD-0004 |
| Title | Validation and Quality Assurance Standard |
| Version | 1.1 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Review Frequency | Triggered or Periodic |
| Effective Date | 29 June 2026 |
| Next Review | As Required |

---

# 2. Purpose

STD-0004 defines the validation and quality assurance standard for Project JARVIS AI engineering deliverables.

It answers the primary validation question:

> How do we know that an engineering deliverable is complete, correct and ready to become part of the accepted Project JARVIS AI repository baseline?

This standard defines how engineering deliverables are validated, independently verified and accepted into the repository baseline.

---

# 3. Scope

This standard applies to validation of:

- documentation;
- standards;
- governance artefacts;
- software;
- engineering sessions;
- repository updates.

It applies to deliverables created or changed through approved Project JARVIS AI and AIEMS engineering activity.

This standard does not define project roadmap content, estimation methods, AI role matrices, HABEI research promotion, WP0 naming, unrelated governance workflows or JARVIS OS implementation requirements.

---

# 4. Relationship to AIEMS

STD-0004 forms part of the AI Engineering Management System.

AIEMS defines the governance framework for Project JARVIS AI. This standard defines the validation and quality assurance expectations used to confirm that approved engineering work is complete, correct and ready for baseline acceptance.

Where conflict exists, approved AIEMS governance artefacts and Programme Sponsor decisions take precedence.

---

# 5. Validation Principles

Validation shall follow these principles:

- Evidence before opinion.
- Independent verification.
- Repository-first validation.
- Proportional validation.
- Review Twice. Build Once. Improve for Everyone.
- Governance exists to enable delivery, not replace it.

Validation effort shall be appropriate to the risk, complexity and permanence of the deliverable.

---

# 6. Authority and Assurance Definitions

AIEMS distinguishes the following assurance and authority terms:

| Term | Meaning |
|------|---------|
| Engineering Approval | Programme Sponsor authorisation for a defined engineering activity, scope or repository operation to proceed. |
| Validation | Evidence-gathering that confirms the completed work satisfies the approved scope, constraints and checks. |
| Verification | Independent confirmation that implementation evidence is present in the repository and matches the reported outcome. |
| Acceptance | Programme Sponsor decision that establishes the accepted engineering or repository baseline. |

Validation provides evidence.

Verification confirms implementation.

Acceptance establishes engineering authority.

Engineering Approval is distinct from Acceptance. Approval authorises work to begin or proceed. Acceptance confirms the resulting baseline after implementation, validation and verification.

Only the Programme Sponsor may accept a Repository Baseline.

---

# 7. Definition of Done

An engineering deliverable is done when the approved scope has been implemented, reviewed, verified and accepted or explicitly deferred by the appropriate authority.

| Deliverable Type | Completion Expectation |
|------------------|------------------------|
| Documentation | Required content is present, accurate, traceable and consistent with authoritative artefacts. |
| Standards | Mandatory sections are present, requirements are clear, scope is bounded and version history is recorded. |
| Governance artefacts | Metadata, status, ownership, references and register entries are consistent. |
| Software | Approved behaviour is implemented, relevant tests or justified deferrals exist, and agreed checks are reported. |
| Engineering sessions | Session objectives, completed work, validation evidence, findings and handover state are recorded. |
| Repository updates | Intended files are changed, unrelated files are excluded, changes are committed, pushed and verified where available. |

---

# 8. Validation Gates

Engineering deliverables shall progress through the following validation gates where applicable:

```text
Engineering Planning
    |
    v
Programme Sponsor Approval
    |
    v
Implementation
    |
    v
Programme Sponsor Validation
    |
    v
Commit & Push
    |
    v
Independent Repository Verification
    |
    v
Programme Sponsor Baseline Acceptance
    |
    v
Repository Baseline Accepted
```

Validation gates may be scaled for small or low-risk changes, but any skipped or unavailable gate shall be reported.

---

# 9. Verification Types

| Verification Type | Definition |
|-------------------|------------|
| Self Validation | The implementer confirms that the completed work matches the approved scope and reports checks performed. |
| Programme Sponsor Validation | The Programme Sponsor validates that the completed work satisfies the approved intent before repository baseline progression. |
| Independent Engineering Review | A reviewer evaluates the deliverable against the approved scope, repository evidence and applicable standards. |
| Human Verified | Confirmation supplied by the Programme Sponsor or Engineering Implementer. |
| AI Verified | Independent verification using GitHub connector, repository evidence or equivalent available verification capability. |
| Repository Accepted | The Programme Sponsor accepts the repository baseline after verification. |

Verification evidence shall identify what was checked, the result and any findings or limitations.

---

# 10. Repository Baseline Acceptance

Repository Baseline Acceptance requires the following minimum conditions:

- approved scope implemented;
- repository committed;
- repository pushed;
- GitHub verification completed where available;
- engineering review completed;
- findings recorded;
- Programme Sponsor approval obtained.

If any condition cannot be completed, the limitation shall be recorded before acceptance is recommended.

Independent verification may recommend acceptance. It does not establish acceptance.

Repository Baseline Acceptance is established only when the Programme Sponsor accepts the verified repository baseline.

---

# 11. Validation Checklist

Future Engineering Implementation Packages may use the following checklist:

| Check | Result |
|-------|--------|
| Approved scope implemented. | Pass / Fail / N/A |
| Required files created or modified. | Pass / Fail / N/A |
| Required sections or behaviours present. | Pass / Fail / N/A |
| Registers and status artefacts updated where required. | Pass / Fail / N/A |
| No unrelated files modified. | Pass / Fail / N/A |
| Relevant checks or reviews completed. | Pass / Fail / N/A |
| Findings recorded with severity and outcome. | Pass / Fail / N/A |
| Commit and push completed where authorised. | Pass / Fail / N/A |
| Repository verification completed where available. | Pass / Fail / N/A |
| Baseline acceptance decision recorded. | Pass / Fail / N/A |

---

# 12. Quality Review Findings

Quality review findings shall use the following severity levels:

| Severity | Meaning |
|----------|---------|
| Critical | Blocks acceptance or creates material governance, repository, security or correctness risk. |
| High | Materially affects future engineering, validation confidence or maintainability. |
| Medium | Should be corrected to improve consistency, readiness or maintainability. |
| Low | Useful refinement that does not materially affect acceptance. |
| Observation | Not a defect; recorded context, limitation or future consideration. |

Quality review outcomes shall be:

| Outcome | Meaning |
|---------|---------|
| Accept | Deliverable is ready for acceptance. |
| Accept with Observation | Deliverable is acceptable; observations are recorded for awareness or future work. |
| Remediate | Correction is required before acceptance. |
| Defer | Finding is intentionally deferred for future approved work. |
| Reject | Deliverable is not acceptable in its current form. |

---

# 13. Maintenance Requirements

STD-0004 shall remain concise and delivery-focused.

It shall not become a general governance manual.

This standard shall be reviewed when validation practice changes materially, recurring quality findings emerge, or AIEMS governance requires updated acceptance rules.

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 June 2026 | Programme Sponsor & Chief Engineering Advisor | Initial Validation and Quality Assurance Standard created for Project JARVIS AI. |
| 1.1 | 30 June 2026 | Programme Sponsor & Chief Engineering Advisor | Clarified engineering approval, validation, independent verification and Programme Sponsor baseline acceptance lifecycle. |
