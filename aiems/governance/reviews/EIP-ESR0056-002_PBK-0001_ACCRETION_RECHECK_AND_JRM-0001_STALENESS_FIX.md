# EIP-ESR0056-002 - PBK-0001 Accretion Re-check and JRM-0001 Staleness Fix (EBG-0058)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0056-002 |
| Title | Engineering Implementation Package: WP2 PBK-0001 Accretion Re-check and JRM-0001 Staleness Fix |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0056 |
| Work Package | WP2 |

---

# 2. Purpose

Implements ESR-0056 WP2. Originally scoped from [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0058 (PBK-0001 Clause Consolidation) per the WP0A candidate list, which described it as the "highest process-hygiene value of anything currently open" - a framing sourced from [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Section 6.1.

**WP0A/WP2 scope correction, flagged before proceeding rather than silently absorbed:** EBG-0058 is already **Complete**, closed at ESR-0028 WP1 per [[EIP-ESR0028-001_AIEMS_PROCESS_HYGIENE_BATCH|EIP-ESR0028-001]] Section 4.4 - the repository-operations-authorisation restatement (three near-verbatim copies, zero added content each) was consolidated into PBK-0001 v1.27→1.28; three other named candidate clusters were reviewed and deliberately retained unmerged, each found to carry genuine distinct content. JRM-0001's Section 6.1 near-term roadmap entry was never updated to reflect this - the same category of staleness ESR-0056 WP4 is separately correcting for the REG-0001 HST/FCH line.

Programme Sponsor directed retargeting WP2 to: (1) a fresh accretion re-check of PBK-0001 - has any new overlapping-restatement duplication crept in during the 15 versions (v1.28→v1.43) since the original consolidation pass - and (2) fixing JRM-0001's stale EBG-0058 references either way.

---

# 3. Repository Context Investigated

* [[EIP-ESR0028-001_AIEMS_PROCESS_HYGIENE_BATCH|EIP-ESR0028-001]] Section 4.4 and PBK-0001's own v1.28 changelog entry: the original consolidation's methodology and bar for merging - "near-verbatim... with zero added content" - applied to four named candidates, only one (repository-operations-authorisation) actually merged; the other three (Engineering Scope Control checklist / Approval Before Change / Working Report Lifecycle overlap; Operational Verification Before Reporting vs Validation Before Completion; Feature-First Delivery Discipline's four sub-clauses) deliberately retained unchanged as genuinely distinct.
* [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] Version History, v1.29 through v1.43 (16 entries): only two carry new substantive prose - v1.30 (Documentation Debt Discipline) and v1.39 (Scope-Creep and Cross-WP-Dependency Flagging Discipline). Every other entry in that range is a mechanical RBL baseline-pointer correction (Related Artefacts/OSE Relationships), carrying no new principle-restating text.
* Full current text of both new sections compared against the closest existing PBK-0001 content using the same bar the v1.28 review applied:
  * **Documentation Debt Discipline** (Whole-Document Staleness Sweep on Edit; Documentation-Debt Priority Until Backlog Cleared) vs. **Engineering Self-Review**'s checklist (scope completed, formatting, repository consistency, no unrelated files, constraints respected, deviations reported): different concern - Self-Review validates the specific approved scope was completed correctly; Documentation Debt Discipline is a proactive sweep for *unrelated* staleness discovered incidentally while a document is already open, plus a session-priority-ordering rule. No overlapping sentence, no restated principle.
  * **Documentation-Debt Priority Until Backlog Cleared** vs. **Repository Engineering Health Review Guidance**'s Backlog Progression Analysis: different mechanism - Backlog Progression Analysis is Health-Review-specific advisory output requiring a future session's own Programme Sponsor approval before any Work Package is created from it; Documentation-Debt Priority is a standing, self-executing WP0/WP1 selection rule that applies automatically without a Health Review as trigger. Thematically adjacent (both concern prioritisation) but not the same rule from two angles.
  * **Scope-Creep and Cross-WP-Dependency Flagging Discipline** vs. **Engineering Scope Control**'s "Avoid extending approved scope" checklist bullet: the closest genuine overlap found - both address not silently expanding scope. Judged non-duplicative under the v1.28 bar for the same reason Engineering Scope Control was already retained unmerged at v1.28 itself (it was the "other half" of that review's own Named Candidate 1): the Scope-Creep Discipline adds real content the bare checklist bullet does not carry - the cross-WP-dependency concern (entirely absent from Engineering Scope Control), the explicit Principle-5 override mechanism, and the "flag plainly and by name before proceeding" behavioural instruction. Not a near-verbatim, zero-added-content restatement; trimming the checklist bullet to a cross-reference would also cost the list's scannability for a thin edge saving, the same trade-off v1.28 itself already declined to make for this exact bullet.
* [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Section 6.1 (line 75): lists EBG-0058 as "Already Approved Backlog... highest process-hygiene value of anything currently open" - stale. Section 6.3 (line 107): EBG-0052's rationale reads "overlaps conceptually with material EBG-0058 will already touch (Approval Before Change restatements) - resolve together" - also stale, since EBG-0058 closed without ever touching EBG-0052 (a distinct, still-open backlog item about an "Execute After Approval" principle, unrelated in substance to Approval Before Change restatement).

---

# 4. Scope

## 4A. Record the fresh accretion-check finding in EBR-0001

Append a re-verification note to EBG-0058's existing (already-Complete) row - do not reopen its status - documenting that ESR-0056 WP2 re-checked PBK-0001's growth since the original v1.28 consolidation and found no new duplication warranting a merge, per Section 3's comparison above.

## 4B. Fix JRM-0001 Section 6.1 (line 75)

Update the EBG-0058 row to reflect Complete status, matching the pattern already used elsewhere in this same table for other resolved items (EBG-0065, EBG-0057, EBG-0018) - retain the row for lineage, prepend a **Resolved at ESR-0028 WP1** note rather than deleting it.

## 4C. Fix JRM-0001 Section 6.3 (line 107)

Correct EBG-0052's rationale to remove the stale "resolve together" framing - EBG-0052 remains its own independent open Candidate/Approved Backlog item, no longer tied to EBG-0058.

## 4D. Explicitly out of scope

* No PBK-0001 text edit - the fresh re-check's own finding is that none is warranted. A null result is treated as a legitimate, disclosed outcome (matching v1.28's own EBG-0058 closure note: "closed as Complete because each... candidate was actually reviewed and disposed, not because every candidate resulted in a merge").
* EBG-0052 itself is not actioned, closed, or otherwise touched beyond correcting the stale cross-reference - it remains open, unrelated backlog.
* WP4's own JRM-0001 REG-0001 HST/FCH line (Section 6.1, the row immediately below EBG-0058's) - separate Work Package, not touched here even though it sits in the same table.

---

# 5. Validation Requirements

* `python scripts/validate_repository.py` - 0 errors, warning count disclosed (unchanged expected).
* Manual re-read of the edited EBR-0001/JRM-0001 sections to confirm no other reference to EBG-0058 or EBG-0052 was left inconsistent.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* EBR-0001's EBG-0058 row carries a disclosed re-verification note; status remains Complete (not reopened).
* JRM-0001 no longer lists EBG-0058 as open/highest-value anywhere.
* JRM-0001's EBG-0052 rationale no longer implies it is blocked on or bundled with EBG-0058.
* No PBK-0001 content changed (the genuine finding of this Work Package).
* `validate_repository.py` remains clean.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 4 September 2026 | Claude Engineering Implementer | Programme Sponsor approved via direct chat instruction ("Approved"), implemented exactly as scoped in v0.2: EBR-0001's EBG-0058 row gained a re-verification note (status unchanged, Complete); JRM-0001 Section 6.1's EBG-0058 line and Section 6.3's EBG-0052 line both corrected to drop the staleness. No PBK-0001 content changed - the genuine finding of this Work Package. `validate_repository.py` 0 errors. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 0.2 | 4 September 2026 | Claude Engineering Implementer | Codex Engineering Reviewer design review via the AIEMS Exchange Bridge - **Pass, no corrections needed**. Codex independently re-read the real Engineering Scope Control / Scope-Creep Discipline / Documentation Debt Discipline / Backlog Progression Analysis text, independently re-verified PBK-0001's v1.29-v1.43 Version History (confirming only v1.30/v1.39 carry new substantive prose), independently confirmed JRM-0001's line 75/107 text matches what this EIP quotes, and confirmed the "no PBK-0001 edit" outcome is a legitimate null result, not avoided work. Not yet approved or implemented. |
| 0.1 | 4 September 2026 | Claude Engineering Implementer | ESR-0056 WP2 draft - retargeted from PBK-0001 clause consolidation (already Complete since ESR-0028) to a fresh accretion re-check plus JRM-0001 staleness fix, per Programme Sponsor direction after the EBG-0058 status discrepancy was flagged. Not yet reviewed, approved or implemented. |
