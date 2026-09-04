# EIP-ESR0056-004 - JRM-0001 REG-0001 HST/FCH Gap Staleness Fix

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0056-004 |
| Title | Engineering Implementation Package: WP4 JRM-0001 REG-0001 HST/FCH Gap Staleness Fix |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0056 |
| Work Package | WP4 |

---

# 2. Purpose

Implements ESR-0056 WP4. At WP0B, cross-checking every HST/FCH file on disk (`aiems/History/`, `aiems/History/Full Chat/`) against [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]]'s artefact table found all 24 HST and 24 FCH files already registered - the "REG-0001 HST/FCH registration gap" [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] lists as live near-term work (Section 6.1, Section 9) is stale.

Root cause confirmed: [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]]'s EBG-0071 row shows the gap was formally created and closed **Complete at ESR-0028 WP1** - 10 tracked artefacts (HST-0015 Claude/GPT, HST-0016 Claude/GPT/incremental, HST-0017 Claude/incremental, HST-0020 Claude/GPT, FCH-0020_GPT) diffed against REG-0001 and registered, Codex-confirmed complete. JRM-0001's two references to this gap (Section 6.1 near-term list; Section 9 numbered item) were never updated to reflect EBG-0071's resolution.

---

# 3. Repository Context Investigated

* `aiems/History/` and `aiems/History/Full Chat/`: 24 HST files, 24 FCH files on disk (WP0B's own direct listing).
* [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]]: all 48 corresponding rows present, cross-checked file-by-file at WP0B.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0071 row: "Complete... Diffed every git-tracked `aiems/History/**/*.md` file against REG-0001's registered rows directly at ESR-0028 WP1 and found 10 tracked artefacts with no REG-0001 row... All 10 registered... Engineering Reviewer (Codex) confirmed the inventory complete."
* [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] Section 6.1 (line 76): "REG-0001 HST/FCH registration gap (unnumbered - see Section 9)... Deferred to an ESR-0021 WP... small, mechanical, should not linger" - stale, no longer unnumbered (EBG-0071 exists) and no longer open.
* JRM-0001 Section 9 (line 210): "**REG-0001 HST/FCH registration gap**... Surfaced at ESR-0021 WP4... Recommend EBG-0071 if not resolved before session close" - stale in the same way; EBG-0071 was in fact created and closed.

---

# 4. Scope

## 4A. Fix JRM-0001 Section 6.1 (line 76)

Update the row to reflect Complete status, matching the pattern already used elsewhere in the same table (EBG-0065, EBG-0057, EBG-0018) - retain for lineage, prepend a **Resolved at ESR-0028 WP1 (EBG-0071)** note rather than deleting the row.

## 4B. Fix JRM-0001 Section 9 (line 210)

Update the numbered item to note EBG-0071 was in fact created and closed Complete at ESR-0028 WP1, rather than leaving it phrased as a still-open recommendation.

## 4C. Explicitly out of scope

* No REG-0001 or EBR-0001 edit - both are already accurate; only JRM-0001 is stale.
* No further HST/FCH file audit - WP0B's cross-check already confirmed completeness; not repeated here.

---

# 5. Validation Requirements

* `python scripts/validate_repository.py` - 0 errors, warning count disclosed.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* JRM-0001 no longer lists the REG-0001 HST/FCH registration gap as open, unnumbered, or a live recommendation anywhere.
* `validate_repository.py` remains clean.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 4 September 2026 | Claude Engineering Implementer | Codex Engineering Reviewer design review via the AIEMS Exchange Bridge - **Pass, no corrections needed**: independently confirmed EBG-0071's Complete status and resolution detail, independently searched JRM-0001 and confirmed lines 76/210 are the only two active stale references. Programme Sponsor approved via direct chat instruction ("Approved"), implemented exactly as scoped: JRM-0001 Section 6.1 and Section 9 both corrected. `validate_repository.py` clean. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 0.1 | 4 September 2026 | Claude Engineering Implementer | ESR-0056 WP4 draft - JRM-0001 staleness fix, confirming EBG-0071 (already Complete since ESR-0028 WP1) as the resolution. Not yet reviewed, approved or implemented. |
