# EIP-ESR0020-001 - PBK-0001 Playbook Alignment and Baseline Reference Correction

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0020-001 |
| Artefact ID | EIP-ESR0020-001 |
| Title | PBK-0001 Playbook Alignment and Baseline Reference Correction |
| Version | 0.2 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | PBK-0001 |
| Intended Session | ESR-0020 or the next approved engineering session |
| Effective Date | 13 July 2026 |

---

# 2. Purpose

This Engineering Implementation Package prepares a small governance correction to [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]].

The intent is to remove two stale references identified during review:

1. PBK-0001 still presents [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] as the current accepted repository baseline in places where the live programme baseline is now [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]].
2. PBK-0001 still uses the retired or undefined term `Engineering Architect` in the session-closure check sentence.

The package preserves the underlying governance model and limits the work to these targeted corrections.

---

# 3. Objective

Bring PBK-0001 back into alignment with the live repository baseline and the current role terminology without broadening scope into unrelated governance refresh work.

---

# 4. Repository Context

| Item | Current State |
|------|---------------|
| Repository | `project-jarvis-ai` |
| Branch | `main` |
| Current accepted repository baseline | [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] |
| Previous baseline | [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] |
| Current programme status | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Current session record | [[ESR-0019_ENGINEERING_SESSION_REPORT|ESR-0019]] |
| Current playbook under correction | [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] |

---

# 5. Scope

This package authorises a future implementation to update PBK-0001 so that:

1. The `RBL-0009` references that currently claim or imply "current accepted repository baseline" are rewritten to reflect the actual current accepted baseline, `RBL-0014`.
2. The closure-check sentence currently referring to `Engineering Architect` is rewritten to use the correct current role term.
3. The playbook's document-control version and version history are incremented consistently with the resulting content change.
4. Any direct register traceability that must reflect the PBK-0001 version bump is updated in `REG-0001` as part of the same controlled change.

Where historical context is needed, `RBL-0009` may remain as a historical baseline reference, but it must not be presented as the current accepted baseline.

---

# 6. Authorised Files

The implementation of this package is expected to modify only:

1. `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md`
2. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other files are authorised unless required by repository validation and explicitly reported.

---

# 7. Implementation Requirements

The implementation shall:

1. Replace the stale `RBL-0009` "current accepted repository baseline" wording in PBK-0001 with `RBL-0014`.
2. Preserve `RBL-0009` only as a historical reference where the document needs to describe earlier baseline lineage.
3. Replace the closure-check reference to `Engineering Architect` with the correct current role term used elsewhere in PBK-0001.
4. Keep the correction narrow and editorial. Do not rework unrelated governance language, workflow policy, or backlog references.
5. Keep PBK-0001's role-definition-not-vendor principle intact.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Changes to `PST-0001`.
2. Changes to `COC-0001`.
3. Changes to `ESR-0019`.
4. Changes to `RBL-0014`.
5. Any global terminology cleanup outside PBK-0001.
6. Any repository baseline change.
7. Any new policy or workflow redesign.

---

# 9. Constraints

1. Keep the implementation minimal and traceable.
2. Do not widen the change to other governance artefacts unless a real dependency is discovered during execution.
3. Ensure the resulting text reflects the current repository state, not historical state.
4. Preserve the existing document structure and style of PBK-0001.

---

# 10. Validation

After implementation, run:

```powershell
python scripts/validate_repository.py --governance-only
git diff --check
git status --short
```

Validation should confirm:

1. PBK-0001 no longer claims `RBL-0009` is the current accepted repository baseline.
2. The `Engineering Architect` term is removed from the targeted closure-check sentence.
3. `REG-0001` remains internally consistent with the PBK-0001 version bump.
4. No unauthorised files changed.

---

# 11. Risks And Dependencies

## Dependencies

1. [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] as the current accepted repository baseline.
2. [[ESR-0019_ENGINEERING_SESSION_REPORT|ESR-0019]] and [[PST-0001_PROGRAMME_STATUS|PST-0001]] as the current session and status context.

## Risks

1. The targeted text may have more than one occurrence, so the implementation must verify all stale baseline references were corrected.
2. The correction should not accidentally rewrite legitimate historical baseline lineage.
3. Broad terminology cleanup would create unnecessary scope and should be avoided.

---

# 12. Approval Request

This package is ready for Programme Sponsor review.

If approved, the Engineering Implementer may apply the narrow PBK-0001 correction and the corresponding REG-0001 traceability update in the next authorised implementation step.

**Approved by the Programme Sponsor, 13 July 2026**, with an explicit scope extension directed at approval time: the Engineering Implementer's ESR-0020 WP1 review (Section 9) additionally raised Finding 1 (PBK-0001/COC-0001 Draft status - EBG-0004) and Finding 3 (PBK-0001 Version History v1.7/v1.8 ordering). The Programme Sponsor directed both be corrected in this same implementation pass, resolving Finding 1 by promoting both PBK-0001 and COC-0001 from Draft to Approved. This supersedes Section 8 Explicit Exclusion item 2 for the specific, narrow purpose of COC-0001's Document Control Status/Version fields only - no other COC-0001 content was authorised or changed. WP1 Finding 4 (Health Review Guidance duplication) was explicitly left unactioned per Programme Sponsor decision - no change made.

The Version History author attribution on v0.1 below was corrected from "Claude Engineering Reviewer" to "ChatGPT Engineering Reviewer": Claude holds the permanent Engineering Implementer role per the EE-0001 Section 7 appointment, not Reviewer, and did not draft this package.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Target of the requested correction. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register expected to reflect the resulting PBK-0001 version change. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Provides current programme baseline context. |
| [[ESR-0019_ENGINEERING_SESSION_REPORT|ESR-0019]] | Latest closed session and immediate context for the correction. |
| [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] | Current accepted repository baseline. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Historical baseline reference that must no longer be treated as current. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 13 July 2026 | Claude Engineering Implementer | Recorded Programme Sponsor approval and directed scope extension (Section 12); implemented the approved package - RBL-0009 to RBL-0014 corrections, `Engineering Architect` to Programme Sponsor, plus Finding 1 (PBK-0001/COC-0001 Draft to Approved) and Finding 3 (Version History ordering). ESR-0020 WP2. |
| 0.1 | 13 July 2026 | ChatGPT Engineering Reviewer | Drafted EIP-ESR0020-001 to correct PBK-0001 stale baseline references and the remaining `Engineering Architect` terminology drift. Author attribution corrected from "Claude Engineering Reviewer" at ESR-0020 WP2 (Claude holds the permanent Engineering Implementer role, not Reviewer). |
