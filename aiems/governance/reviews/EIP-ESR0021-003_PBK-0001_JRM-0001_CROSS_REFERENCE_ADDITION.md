# EIP-ESR0021-003 - PBK-0001 JRM-0001 Cross-Reference Addition

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0021-003 |
| Artefact ID | EIP-ESR0021-003 |
| Title | PBK-0001 JRM-0001 Cross-Reference Addition |
| Version | 0.2 |
| Status | Draft |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | PBK-0001 |
| Intended Session | ESR-0021 or the next approved engineering session |
| Effective Date | 15 July 2026 |

---

# 2. Purpose

This Engineering Implementation Package prepares a narrow addition to [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]].

[[JRM-0001_PROJECT_ROADMAP|JRM-0001]] (Project Roadmap) was created and Programme Sponsor-approved at ESR-0021 WP5, closing EBG-0012, EBG-0027 and EBG-0028. It is the first forward-looking sequencing artefact this programme has had - but PBK-0001's Backlog Progression Analysis guidance, and its Related Artefacts / OSE Relationships sections, were all last touched before JRM-0001 existed and make no reference to it. Without a pointer, a future session doing backlog sequencing work has no reason to consult it, and JRM-0001's own Section 4 Principle 5 already anticipates exactly this risk - a roadmap nobody actually checks.

This package is mostly a cross-reference: two of its three additions (Related Artefacts, OSE Relationships) are pure discoverability, adding a link and nothing else. The third addition (the Backlog Progression Analysis sentence) is honestly a small behavioural addition, not merely a link - it changes what Backlog Progression Analysis considers, by directing that an item's existing JRM-0001 horizon placement inform the recommendation rather than being re-derived from nothing. **Revised per Engineering Reviewer finding**: the original draft understated this by calling the whole package "a cross-reference only," which was not accurate for this one sentence. The behavioural addition is kept in this same package rather than split into a separate EIP - it is one sentence, proportionate to review alongside the cross-references rather than as its own cycle - but it is named honestly here as guidance, not merely a pointer. None of the three additions restates anything JRM-0001 or EBR-0001 already say, and none introduces a new mandatory rule with its own compliance criteria - both PBK-0001 itself (Repository Documentation Principle) and the still-open EBG-0058 (PBK-0001 Clause Consolidation) caution against that kind of accretion.

---

# 3. Objective

Make JRM-0001 discoverable from PBK-0001's existing backlog-sequencing guidance and artefact-reference sections, without introducing new obligations, workflow steps, or restated content.

---

# 4. Repository Context

| Item | Current State |
|------|---------------|
| Repository | `project-jarvis-ai` |
| Branch | `main` |
| Current accepted repository baseline | [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] |
| Current programme status | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Current session record | ESR-0021 (open) |
| Current playbook under correction | [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] |
| Current playbook version (pre-implementation) | 1.24 |
| New artefact this package cross-references | [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] v1.0, Approved, registered in REG-0001 at ESR-0021 WP5 |

---

# 5. Scope

This package authorises a future implementation to update PBK-0001 so that:

1. The Backlog Progression Analysis guidance (Repository Engineering Health Review Guidance section) gains one sentence directing that, where a backlog item already has a horizon placement in JRM-0001, that placement should inform the recommendation rather than being re-derived independently from nothing.
2. JRM-0001 is added as a bullet in the Related Artefacts section.
3. JRM-0001 is added as a row in the OSE Relationships table.
4. The playbook's Document Control version and Version History are incremented consistently with the resulting content change.
5. The corresponding PBK-0001 version entry in [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] is updated to match.

No other PBK-0001 content is authorised to change.

---

# 6. Authorised Files

The implementation of this package is expected to modify only:

1. `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md`
2. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

The implementation shall:

1. Insert one sentence immediately after the existing line "Backlog Progression Analysis shall examine EBR-0001 and recommend activities that best progress Project JARVIS AI during the next Engineering Session" - to the effect that where JRM-0001 already places the item in a horizon, that placement shall inform the recommendation rather than being independently re-derived. The sentence shall not enumerate JRM-0001's specific horizon names (Near-term, Mid-term, Longer-term, Not Yet Justified) - referring generically to "horizon placement" avoids the wording going stale if JRM-0001's own horizon labels change, and avoids silently excluding whichever horizon isn't named (caught by Engineering Reviewer finding: the original draft named only three of JRM-0001's four horizons, which would have left "Not Yet Justified" items outside this guidance).
2. Add a single new bullet to Related Artefacts: JRM-0001 as the forward-looking sequencing artefact referenced by Backlog Progression Analysis.
3. Add a single new row to the OSE Relationships table for JRM-0001, matching the existing table's style.
4. Increment PBK-0001 Document Control version and add one Version History row describing this change.
5. Update REG-0001's PBK-0001 row and Version History to match.
6. Make no other wording change anywhere else in PBK-0001.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any new procedural rule, obligation, or workflow step beyond the one cross-reference sentence in Section 7, item 1.
2. Any change to [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] or [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]].
3. Any change to [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] or [[PST-0001_PROGRAMME_STATUS|PST-0001]].
4. Any action on EBG-0058 (PBK-0001 Clause Consolidation) - that remains its own separate, larger piece of work.
5. Adding JRM-0001 to the mandatory WP0/WP0A session-start review list - that is a heavier obligation than a cross-reference and, if wanted, should be its own considered decision, not bundled in here.

---

# 9. Constraints

1. Keep the implementation to exactly the additions listed in Section 7 - no more.
2. The new Backlog Progression Analysis sentence is guidance shaping how an existing analysis step is performed, not a new mandatory rule with its own compliance criteria (no new pass/fail check, no new reporting obligation) - consistent in weight with the other bullet points Backlog Progression Analysis already directs Health Reviews to consider (dependencies, sequencing, risk, benefit, effort, and so on).
3. Preserve PBK-0001's existing structure, tone and section ordering.
4. Do not touch any other Repository Engineering Health Review Guidance content.

---

# 10. Validation

After implementation, run:

```powershell
python scripts/validate_repository.py --governance-only
git diff --check
git status --short
```

Validation should confirm:

1. PBK-0001 references JRM-0001 in Related Artefacts, OSE Relationships and Backlog Progression Analysis.
2. No other PBK-0001 wording changed.
3. REG-0001 remains internally consistent with the PBK-0001 version bump.
4. No unauthorised files changed.

---

# 11. Risks and Dependencies

## Dependencies

1. [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] as the target of the new cross-references, already Approved and registered.
2. [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] as the artefact under correction.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] as the traceability register.

## Risks

1. Scope creep into a full JRM-0001/PBK-0001 integration pass (e.g. adding it to WP0A) rather than the narrow cross-reference approved here.
2. The new sentence being worded strongly enough that it reads as a new rule rather than a pointer - the Engineering Reviewer should specifically check this during review.
3. Overlap with EBG-0058's eventual clause-consolidation work - this package should not pre-empt or complicate that separate effort.

---

# 12. Approval Request

**Engineering Reviewer review completed.** Two findings raised, both accepted and addressed in this revision (0.2):

1. **Medium** - the horizon-placement sentence originally enumerated only three of JRM-0001's four horizons (Near-term/Mid-term/Longer-term), omitting Not Yet Justified, which would have silently excluded items in that bucket from the new guidance. Fixed: Section 7 item 1 no longer enumerates specific horizon names, referring generically to "horizon placement" instead.
2. **Low** - the package's original framing ("a cross-reference only... does not add a new procedural rule") understated the Backlog Progression Analysis sentence, which is a small behavioural addition, not merely a link. Per Programme Sponsor decision, resolved by keeping the addition in this one package rather than splitting it into two, but reframing Section 2 and Section 9 to describe it honestly as guidance shaping an existing analysis step, rather than claiming it is purely a documentation pointer.

This package is now ready for Programme Sponsor decision.

If approved, the Engineering Implementer may apply the narrow PBK-0001 cross-reference and guidance addition, and the corresponding REG-0001 traceability update, in the next authorised implementation step.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Target of the requested addition. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | New artefact being cross-referenced. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register expected to reflect the resulting PBK-0001 version change. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Existing backlog source Backlog Progression Analysis already references; this package adds JRM-0001 alongside it, not in place of it. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 15 July 2026 | Claude Engineering Implementer | Revised following Engineering Reviewer findings (both accepted): fixed the horizon-placement sentence to stop enumerating three of JRM-0001's four horizons (Medium); reframed Section 2/Section 9 to honestly describe the Backlog Progression Analysis addition as a small behavioural change, not merely a cross-reference (Low), per Programme Sponsor decision to keep it in one package with corrected framing rather than splitting into two. Ready for Programme Sponsor decision. |
| 0.1 | 15 July 2026 | Claude Engineering Implementer | Drafted EIP-ESR0021-003 at the Programme Sponsor's direct request, for Engineering Reviewer review: adds a narrow JRM-0001 cross-reference to PBK-0001's Backlog Progression Analysis guidance, Related Artefacts and OSE Relationships - no new procedural rule, no other content change. |
