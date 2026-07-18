# EIP-ESR0028-001 - AIEMS Process Hygiene Batch

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0028-001 |
| Artefact ID | EIP-ESR0028-001 |
| Title | AIEMS Process Hygiene Batch |
| Version | 1.0 |
| Status | Approved-implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0058, EBG-0005, EBG-0068, EBG-0071) |
| Intended Session | ESR-0028 |
| Effective Date | 18 July 2026 |

---

# 2. Purpose

Implements ESR-0028 WP1: a Backlog Acceleration Opportunity bundling four small, unrelated-but-cheap governance-hygiene items into one Work Package, per JRM-0001 Track A Near-term guidance and PBK-0001's Backlog Acceleration Opportunities. Governance-only - no product code touched, paired this session with WP2-WP4's substantive work per PBK-0001's Feature-First Delivery Discipline.

---

# 3. Objective

Close four long-open, small backlog items with grounded, evidence-based resolutions rather than mechanical box-ticking - each was investigated against actual repository evidence before this package was drafted, per PBK-0001 Principle 1 (Engineering Before Implementation) and Principle 2 (Evidence Before Conclusion).

---

# 4. Repository Context and Investigation Findings

## 4.1 EBG-0005 - REG-0001 metadata alignment following P2-004A

P2-004A was ESR-0001's own "Engineering Session Lifecycle Alignment" work package (27 June 2026 - the project's first session). Recommended as ESR-0003's first EIP but apparently never actioned; the item has sat as "Approved Backlog" for 26+ sessions since.

**Finding**: REG-0001 has been continuously, actively maintained across every one of those 26+ sessions (currently v3.205, hundreds of version-history entries). No trace of an unresolved P2-004A-era metadata gap is identifiable in the current register - whatever specific field alignment was needed in ESR-0001/ESR-0002's context has almost certainly been absorbed through routine maintenance since. Re-deriving what "alignment" meant from `FCH-0001`'s raw transcript would cost more than the item is worth for a "Medium priority, low effort" item.

**Recommendation**: close as Resolved by Attrition, disclosed plainly rather than silently dropped.

## 4.2 EBG-0068 - EIB artefact type, adopt or drop

**Finding**: confirmed directly - no `EIB-*` file exists anywhere in the repository (`git ls-files` returns nothing), and no `EIB-*` row exists in REG-0001. The only mentions of EIB anywhere are EBR-0001's own backlog note and one historical chat reference (`FCH-0006`). The EIP convention has been used exclusively and consistently for 20+ sessions since.

**Recommendation**: close as Superseded by the EIP convention. No artefact cleanup needed - there was never a registered EIB artefact to retire.

## 4.3 REG-0001 HST/FCH registration gap (EBG-0071)

**Finding (corrected at v0.2)**: diffed every git-tracked `aiems/History/**/*.md` file against REG-0001's registered rows directly. v0.1 claimed the FCH side was fully registered (23/23) - **this was wrong**: `aiems/History/Full Chat/FCH-0020_GPT_FULL_CHAT_HISTORY.md` is tracked (24 FCH files exist, not 23) and has no REG-0001 row, a gap JRM-0001 Section 9 already names explicitly. Engineering Reviewer pre-implementation review (v0.1) caught this undercount. The complete gap is **10 tracked files with no REG-0001 row** - 9 HST plus 1 FCH:

| Missing | File |
|---|---|
| HST-0015 | `HST-0015_CLAUDE_CHAT_SUMMARY.md` |
| HST-0015_GPT | `HST-0015_GPT_CHAT_SUMMARY.md` |
| HST-0016 | `HST-0016_CLAUDE_CHAT_SUMMARY.md` |
| HST-0016_GPT | `HST-0016_GPT_CHAT_SUMMARY.md` |
| HST-0016a_GPT | `HST-0016a_GPT_CHAT_SUMMARY.md` (an incremental ESR-0016 conversation record, not a duplicate of HST-0016_GPT - title kept distinct per Engineering Reviewer advisory) |
| HST-0017 | `HST-0017_CLAUDE_CHAT_SUMMARY.md` |
| HST-0017a_GPT | `HST-0017a_GPT_CHAT_SUMMARY.md` |
| HST-0020 | `HST-0020_CLAUDE_CHAT_SUMMARY.md` |
| HST-0020_GPT | `HST-0020_GPT_CHAT_SUMMARY.md` |
| FCH-0020_GPT | `FCH-0020_GPT_FULL_CHAT_HISTORY.md` |

**Finding (Low, v0.1)**: this backlog item has no actual EBR-0001 row to mark `Complete` against - JRM-0001 Section 9 ("Unnumbered Items Requiring an EBG Identifier") is where this reservation is tracked; EBR-0001's own version history separately records that "EBG-0071 deliberately skipped here - reserved... for the still-open REG-0001 HST/FCH registration gap." The number was reserved but the row was never created. This package creates EBG-0071 now, against the number already reserved for it, and closes it in the same package rather than leaving the reservation dangling further or inventing a different number.

**Recommendation**: register all 10, matching the existing HST/FCH row format and `Archived` status exactly; create and close EBG-0071 in the same package.

## 4.4 EBG-0058 - PBK-0001 Clause Consolidation

Read PBK-0001 v1.27 in full. EBG-0058's own backlog note names three specific starting candidates to check, not a general open-ended search - v0.1 only fully addressed a fourth, independently-found cluster and gave the first named candidate partial treatment; it did not address the second or third named candidates at all. Corrected at v0.2: all three named candidates, plus the independently-found fourth, now each have an explicit disposition below, per Engineering Reviewer Finding 2 on v0.1.

**Named Candidate 1 - Approval Before Change / Working Report Lifecycle / Engineering Scope Control**: genuine overlap exists, but only at each section's edges, not throughout. Principle 3 states the rule itself. Working Report Lifecycle's closing sentence ("Controlled repository artefacts shall be created or modified only following explicit Programme Sponsor approval and an approved implementation instruction") restates it near-verbatim, but the section's actual content - the five-step Working Report -> Review -> Decision -> EIP -> Implementation lifecycle - is distinct, real procedural information, not a restatement. Engineering Scope Control's first bullet ("Implement only approved Engineering Implementation Packages") is the same idea again, but it sits inside an operational checklist whose other four bullets (avoid extending scope, report observations separately, distinguish defects from recommendations, pause if unsafe) are also distinct. **Disposition**: trim Working Report Lifecycle's closing sentence to a cross-reference (exact wording in Section 7); leave Engineering Scope Control's checklist bullet as-is - removing one bullet from a five-item operational checklist would hurt its scannability as a checklist more than the duplication currently costs, a judgement call disclosed here rather than silently made.

**Named Candidate 2 - Operational Verification Before Reporting vs Validation Before Completion**: on inspection, this is not an accidental duplication - Operational Verification's own text already states it "operationalises Principles 2 (Evidence Before Conclusion) and 4 (Validation Before Completion) specifically for repository and tool operations, where the abstract principle and the concrete checkable action can otherwise drift apart under time pressure." That is a deliberate, self-aware specialisation with its own stated rationale for existing separately (an abstract "validate before completion" principle is satisfiable by a self-assessment that feels like validation without literally invoking the operation; the concrete rule closes exactly that gap). **Disposition**: retain both sections unchanged - this is the kind of restatement EBG-0058 is not asking to be merged, since it is already correctly cross-referenced as a refinement, not redundant restatement.

**Named Candidate 3 - Feature-First Delivery Discipline's sub-clauses against each other**: the four sub-clauses (Minimise Controlled Artefact Creation; Product-Moving Engineering Work; Progress Toward the Live UXP; Incremental Visual Convergence) target four different, non-overlapping failure modes - document-count bloat, governance-only sessions, the UXP staying a permanent mock-up, and data-bearing UI elements implying capability that isn't real. "Progress Toward the Live UXP" reads adjacent to "Product-Moving Engineering Work" but is strictly narrower (a session can deliver real product-moving backend work with no UXP tie at all and satisfy the second sub-clause without touching the third - the sub-clause's own text requires backend work to demonstrably advance toward the UXP specifically, a stricter bar than "any real feature work"). "Incremental Visual Convergence" already explicitly states it is "additive... not a replacement for" the UXP-progress sub-clause. **Disposition**: no genuine redundancy found; retain all four sub-clauses unchanged.

**Independently-found Candidate 4 - repository-operations-authorisation**: "repository operations only when explicitly authorised by the Programme Sponsor or an approved Engineering Implementation Package" (or a near-verbatim paraphrase) appears three separate times with zero additional distinct content at each restatement, unlike Candidate 1's edges:
1. Engineering Implementer Session Initialisation, item 14.
2. Repository Lifecycle and Separation of Duties, opening sentence.
3. Git Operations, opening sentence.

**Disposition**: consolidate - this is the clearest, lowest-risk win in the whole review, and the only one where the restated sentence adds literally nothing its neighbours don't already say. Section 7 has the exact mechanism.

**Recommendation**: EBG-0058 is closeable as `Complete` once all four candidates have a recorded disposition (this section) - not because every candidate resulted in a merge, but because each was actually reviewed and disposed rather than left unexamined, satisfying the backlog item's own "identify... and merge... without losing the substance of any" framing (some substance is worth keeping exactly where it is).

Also bundled: the already-flagged PBK-0001 `RBL-0014` -> `RBL-0015` stale baseline reference (Related Artefacts, OSE Relationships) - unrelated to EBG-0058 itself but the same file, same Work Package, avoiding a second small PBK-0001 edit later.

---

# 5. Scope

This package authorises a future implementation to:

1. **EBG-0005**: mark `Resolved by Attrition` in EBR-0001, with the Section 4.1 rationale recorded in the item's note. No REG-0001/code change.
2. **EBG-0068**: mark `Superseded` in EBR-0001, with the Section 4.2 rationale recorded. No REG-0001/code change (nothing was ever registered).
3. **HST/FCH registration gap (EBG-0071)**: create a new EBG-0071 row in EBR-0001 (against the number JRM-0001 already reserved for this gap), and add 10 new rows to REG-0001 for the missing artefacts listed in Section 4.3 (9 HST + 1 FCH), matching the existing row format (`Historical Session Record`/`Full Chat Historical Evidence` type as appropriate, `Archived` status, `Programme Sponsor & Chief Engineering Advisor` owner, parent = the corresponding `ESR-00NN`, location `aiems/History/` or `aiems/History/Full Chat/`) exactly. Mark EBG-0071 `Complete` in EBR-0001 in the same package.
4. **EBG-0058**: in PBK-0001, (a) replace the Repository Lifecycle and Separation of Duties opening sentence and the Git Operations opening sentence with a cross-reference to Session Initialisation item 14, and (b) replace Working Report Lifecycle's closing restatement sentence with a cross-reference to Principle 3. Exact wording for all three in Section 7. Mark `Complete` in EBR-0001 with the Section 4.4 rationale, recording all four candidates' dispositions (two consolidated, two deliberately retained unchanged with reasons).
5. **PBK-0001 baseline reference fix**: correct `RBL-0014` to `RBL-0015` in PBK-0001's Related Artefacts and OSE Relationships sections (already-queued observation from ESR-0027 WP0A).

---

# 6. Authorised Files

1. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
2. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`
3. `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md`
4. `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md` (version alignment only, if touched)

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. PBK-0001's Session Initialisation item 14 remains the canonical statement, unchanged: *"Perform repository operations only when explicitly authorised by the Programme Sponsor or approved Engineering Implementation Package."*
2. Repository Lifecycle and Separation of Duties' opening sentence changes from restating the rule to: *"Repository execution is part of Engineering Implementer responsibility, subject to the authorisation rule already stated in Session Initialisation (item 14)."* - preserving the sentence's actual function (introducing the section) without re-stating the substantive rule a second time.
3. Git Operations' opening sentence changes similarly: *"Engineering Implementers shall perform repository staging, commit and push only as already scoped by Session Initialisation item 14 and the Repository Lifecycle above; the specific operations covered are:"* leading into its existing Stage/Commit/Push list, which is retained unchanged (it adds real information - which operations count - not just a restatement).
4. Working Report Lifecycle's closing sentence ("Controlled repository artefacts shall be created or modified only following explicit Programme Sponsor approval and an approved implementation instruction") changes to: *"This lifecycle operates within, and does not relax, Principle 3 (Approval Before Change)."* - the five-step lifecycle list immediately above is retained unchanged, since it is the section's actual distinct content.
5. No other PBK-0001 section is touched by EBG-0058 - Engineering Scope Control's checklist bullet (Named Candidate 1), Operational Verification Before Reporting (Named Candidate 2), and all four Feature-First Delivery Discipline sub-clauses (Named Candidate 3) are explicitly retained unchanged per Section 4.4's disclosed dispositions.
6. New REG-0001 rows use the exact same eight-column format as the existing HST-0001 through HST-0013 / FCH-0000 through FCH-0013 rows (Section 4.3's table gives the artefact ID and file; title follows the `ESR-00NN Chat Summary (Claude)` / `(GPT)` pattern already used for HST-0023/HST-0023_GPT, and the `ESR-0020 Full Chat History (GPT)` pattern already used for FCH-0020's own Claude-variant row).

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any change to Engineering Scope Control's checklist bullet, Operational Verification Before Reporting, or Feature-First Delivery Discipline's sub-clauses - each reviewed and deliberately excluded per Section 4.4's disclosed dispositions.
2. Any attempt to reconstruct or re-derive the original P2-004A metadata-alignment intent from `FCH-0001` - judged not worth the archival effort for a low-value historical item; closed by attrition instead.
3. Any product code, test, or backend/UXP change - this package is governance-artefact-only.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. Every EBR-0001 status change in this package shall carry a disclosed rationale in the item's own note - none shall be closed with a bare status flip and no explanation.

---

# 10. Validation

After implementation, run:

```powershell
python scripts/validate_repository.py
```

Validation should confirm:

1. `validate_repository.py` (full mode) passes with 0 errors - specifically confirming the 10 new HST/FCH rows don't break any WikiLink or register-consistency check, and PBK-0001's version-tracking row in REG-0001 stays aligned.
2. No unauthorised files changed.
3. `python -m pytest` unaffected (governance-only change, no code touched) - run anyway to confirm no incidental breakage.

---

# 11. Risks and Dependencies

## Dependencies

None - self-contained governance changes.

## Risks

1. **EBG-0005's "resolved by attrition" closure is a judgement call, not a verified fact** - it's possible some genuine P2-004A-era metadata gap still exists that this investigation didn't surface, since the original intent is 26 sessions old and only thinly documented even at the time. Disclosed as a judgement call for the Engineering Reviewer and Programme Sponsor to weigh, not presented as certain.
2. **PBK-0001 is actively referenced by every session's WP0A** - any error in the repository-operations-authorisation consolidation (Section 7) could create a genuine gap in that rule's coverage. Mitigated by keeping the canonical statement (item 14) completely unchanged and only touching the two restatements.

---

# 12. Approval Request

v0.1 reviewed by the Engineering Reviewer (Codex) via the AIEMS Exchange Bridge: "not ready for approval as drafted." Two Medium findings (HST/FCH inventory missed `FCH-0020_GPT`; EBG-0058 scoped too narrowly against its own named candidates) and one Low finding (EBG-0071 has no EBR-0001 row to close against) addressed at v0.2. **v0.2 confirmed by the Engineering Reviewer: "conditionally pass... no Medium or High findings remain."** One further Low/editorial finding on v0.2 (an incorrect JRM-0001 cross-reference number, should be Section 9) corrected at v0.3. Ready for Programme Sponsor approval.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0058, EBG-0005, EBG-0068 (this package's parents), plus EBG-0071 (created and closed by this package, against JRM-0001's reserved number). |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Subject of EBG-0058's consolidation (two clauses merged, two clusters reviewed and retained) and the RBL-0014 baseline-reference fix. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Receives the 10 new HST/FCH rows (9 HST + FCH-0020_GPT). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track A Near-term horizon source for these items' sequencing. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 18 July 2026 | Claude Engineering Implementer | Implemented following Programme Sponsor approval via the bridge (`sponsor-decision`, `repository_ref: 4428a711146f50fcd39a24a2eb8399cfc14eed71`, 18 July 2026 18:37:17Z). All six Section 7 implementation requirements applied: 10 HST/FCH rows registered in REG-0001, EBG-0071 created and closed, EBG-0005 closed Resolved by Attrition, EBG-0068 closed Superseded, EBG-0058 closed Complete with all four candidate dispositions recorded, PBK-0001's four sentences replaced with the exact Section 7 wording, RBL-0014 to RBL-0015 fixed. `validate_repository.py` (full mode): 0 errors. `pytest`: 286 passed. Status promoted Draft to Approved-implemented. |
| 0.3 | 18 July 2026 | Claude Engineering Implementer | Engineering Reviewer (Codex) confirmed v0.2 resolves all three v0.1 findings - "conditionally pass... no Medium or High findings remain." One further Low/editorial finding: Section 4.3 cited a nonexistent JRM-0001 sub-section number (already producing a validate_repository.py warning), corrected to Section 9 ("Unnumbered Items Requiring an EBG Identifier"), the section that actually tracks this reservation. Ready for Programme Sponsor approval. |
| 0.2 | 18 July 2026 | Claude Engineering Implementer | Addressed Engineering Reviewer (Codex) findings on v0.1, returned via the bridge. Finding 1 (Medium, incomplete inventory) - `FCH-0020_GPT` was tracked but uncounted; gap corrected from 9 to 10 rows. Finding 2 (Medium, EBG-0058 scoped too narrowly) - the two named candidates v0.1 never addressed (Operational Verification vs Validation Before Completion; Feature-First sub-clauses) now each have a recorded disposition (both retained unchanged, with reasons); Named Candidate 1 (Approval Before Change/Working Report Lifecycle/Engineering Scope Control) now also gets a partial consolidation (Working Report Lifecycle's restated closing sentence trimmed to a cross-reference) rather than being left entirely untouched. Finding 3 (Low, no EBR-0001 row for the HST/FCH gap) - creates and closes EBG-0071 in this same package, against JRM-0001's already-reserved number, rather than claiming a status flip against a nonexistent row. |
| 0.1 | 18 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0028 WP1, bundling EBG-0058/EBG-0005/EBG-0068/HST-registration-gap as a Backlog Acceleration Opportunity. Each item investigated against direct repository evidence before drafting: EBG-0005 recommended Resolved-by-Attrition (26-session-old P2-004A intent unrecoverable, REG-0001 continuously maintained since); EBG-0068 confirmed clean Superseded close (no EIB artefact ever existed); HST gap precisely identified as 9 specific missing rows via direct file/register diff; EBG-0058 scoped to one low-risk consolidation (repository-operations-authorisation, restated 3x) with a second overlap cluster explicitly considered and excluded. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
