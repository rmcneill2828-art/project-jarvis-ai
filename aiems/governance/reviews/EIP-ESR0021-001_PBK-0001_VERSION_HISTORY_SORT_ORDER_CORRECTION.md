# EIP-ESR0021-001 - PBK-0001 Version History Sort Order Correction

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0021-001 |
| Artefact ID | EIP-ESR0021-001 |
| Title | PBK-0001 Version History Sort Order Correction |
| Version | 0.2 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | PBK-0001 |
| Intended Session | ESR-0021 or the next approved engineering session |
| Effective Date | 15 July 2026 |

---

# 2. Purpose

This Engineering Implementation Package prepares a narrow editorial correction to [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]].

The intent is to resolve the mixed sort order in the PBK-0001 Version History table. The table is descending for most of its entries, but the older `v1.0` through `v1.8` block remained arranged in ascending order, which created an internal formatting inconsistency.

This package does not authorise any substantive governance change. It only normalises the ordering of the existing version-history rows.

---

# 3. Objective

Bring the PBK-0001 Version History table into a single consistent descending order without changing any row text, meaning, or governance content.

---

# 4. Repository Context

| Item | Current State |
|------|---------------|
| Repository | `project-jarvis-ai` |
| Branch | `main` |
| Current accepted repository baseline | [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] |
| Current programme status | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Current closed session record | [[ESR-0020_ENGINEERING_SESSION_REPORT|ESR-0020]] |
| Current playbook under correction | [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] |
| Current playbook version (pre-implementation) | 1.22 |

---

# 5. Scope

This package authorises a future implementation to update PBK-0001 so that:

1. The Version History table is reordered into descending version order throughout, including the existing `v1.0` through `v1.8` block.
2. The Document Control version for PBK-0001 is incremented consistently with the resulting content change.
3. The corresponding PBK-0001 version entry in [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] is updated to match the new PBK-0001 version.
4. No wording within the version-history summaries is altered except where required for traceability metadata such as the version number itself.

The ordering correction should be minimal: move the existing rows into descending order, do not rewrite the historical summaries.

---

# 6. Authorised Files

The implementation of this package is expected to modify only:

1. `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md`
2. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

The implementation shall:

1. Reorder the PBK-0001 Version History table so it is consistently descending from newest to oldest.
2. Preserve each version-history row verbatim apart from any version-control metadata that must change because of the PBK-0001 version bump.
3. Update PBK-0001 Document Control to the next version number.
4. Update REG-0001 so the PBK-0001 row reflects the new approved version.
5. Keep the change editorial and local to the version-history ordering issue.
6. Avoid any unrelated governance cleanup.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any change to [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]].
2. Any change to [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]].
3. Any change to [[PST-0001_PROGRAMME_STATUS|PST-0001]] beyond existing traceability already required by the PBK-0001 version bump.
4. Any change to the substantive PBK-0001 governance clauses outside the Version History / Document Control metadata.
5. Any implementation of ESR-0020 Finding 4 regarding PBK-0001/COC-0001 Health Review Guidance duplication.
6. Any attempt to fold Health Review Guidance duplication into this package.

Finding 4 should remain a separate governance discussion and, if actioned later, be folded into EBG-0058 rather than tracked as a separate one-off fix.

---

# 9. Constraints

1. Keep the implementation minimal and traceable.
2. Do not alter the meaning of the version-history entries.
3. Do not widen scope to other documents or backlog items.
4. Preserve PBK-0001's existing structure and tone.
5. Treat the version-history reordering as the only substantive content change.

---

# 10. Validation

After implementation, run:

```powershell
python scripts/validate_repository.py --governance-only
git diff --check
git status --short
```

---

# 11. Risks And Dependencies

## Dependencies

1. [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] as the target artefact.
2. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] as the traceability register.
3. [[PST-0001_PROGRAMME_STATUS|PST-0001]] for current status context.

## Risks

1. Reordering rows could accidentally change row content if done too broadly.
2. A version bump must remain consistent between PBK-0001 and REG-0001.
3. The open ESR-0020 Finding 4 should not be pulled into this change by accident.

---

# 12. Approval Request

This package is ready for Programme Sponsor review.

If approved, the Engineering Implementer may apply the narrow PBK-0001 version-history ordering correction and the corresponding REG-0001 traceability update in the next authorised implementation step.

The separate ESR-0020 Finding 4 regarding PBK-0001/COC-0001 Health Review Guidance duplication is intentionally not included here and is recommended for later consolidation under EBG-0058.

**Approved by the Programme Sponsor, 15 July 2026.** Implemented as scoped: PBK-0001's Version History table reordered (v1.0-v1.8 block reversed to descending order, no row text altered beyond the new v1.23 entry recording this change itself), PBK-0001 Document Control incremented 1.22 to 1.23, and REG-0001 updated to match (artefact table row and Version History). Finding 4 remains excluded from this package, per Section 8, and remains a candidate for EBG-0058 consolidation.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Target of the requested correction. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register expected to reflect the resulting PBK-0001 version change. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Provides current programme baseline context. |
| [[ESR-0020_ENGINEERING_SESSION_REPORT|ESR-0020]] | Prior session that raised the underlying finding. |
| EBG-0058 | Recommended home for the separately-excluded Finding 4. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 15 July 2026 | Claude Engineering Implementer | Recorded Programme Sponsor approval (Section 12); implemented the approved package - PBK-0001 Version History v1.0-v1.8 block reordered to descending, Document Control 1.22 to 1.23, REG-0001 aligned. ESR-0021 WP2. |
| 0.1 | 15 July 2026 | ChatGPT Engineering Reviewer | Drafted EIP-ESR0021-001 to correct the PBK-0001 Version History mixed sort order and the corresponding version-traceability metadata. Explicitly excluded ESR-0020 Finding 4, recommending it later be folded into EBG-0058 rather than tracked separately. |
