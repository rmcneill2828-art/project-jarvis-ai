# EIP-ESR0021-002 - PBK-0001 Historical Archive Breadcrumb Alignment

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0021-002 |
| Artefact ID | EIP-ESR0021-002 |
| Title | PBK-0001 Historical Archive Breadcrumb Alignment |
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

The intent is to update the PBK-0001 OSE Relationships breadcrumb that still points to the ESR-0013 historical artefacts as the "latest" historical session record and full chat evidence record, even though the repository now contains the ESR-0020-era Claude artefacts.

This package preserves the historical archive model. It only aligns the breadcrumb references with the currently registered archive files.

---

# 3. Objective

Bring PBK-0001's historical-archive references into alignment with the current repository state without changing the underlying knowledge-tier model or archival policy.

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
| Current registered Claude historical artefacts | `HST-0020_CLAUDE_CHAT_SUMMARY.md` and `FCH-0020_CLAUDE_FULL_CHAT_HISTORY.md` |
| Current playbook version (pre-implementation) | 1.23 |

---

# 5. Scope

This package authorises a future implementation to update PBK-0001 so that:

1. The OSE Relationships entries for the historical archive point to the current Claude-side ESR-0020 artefacts rather than the ESR-0013 artefacts.
2. The descriptive text no longer labels the ESR-0013 artefacts as the "latest" historical session record or full chat historical evidence record.
3. The document-control version for PBK-0001 is incremented consistently with the resulting content change.
4. The corresponding PBK-0001 version entry in [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] is updated to match the new PBK-0001 version.
5. No other archival-policy text is changed.

Where historical lineage matters, the ESR-0013 artefacts may remain referenced elsewhere as historical records. They should no longer be described as the latest archive artefacts in PBK-0001.

---

# 6. Authorised Files

The implementation of this package is expected to modify only:

1. `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md`
2. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

The implementation shall:

1. Replace the PBK-0001 OSE Relationships breadcrumb text that currently treats `HST-0013` and `FCH-0013` as the latest historical artefacts.
2. Point the breadcrumb to the current Claude-side ESR-0020 history artefacts instead.
3. Preserve the knowledge-tier design established by [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]].
4. Keep the correction local to PBK-0001's archive-reference wording.
5. Update the PBK-0001 version metadata and register entry consistently.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Any change to [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]].
2. Any change to [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]].
3. Any change to [[PST-0001_PROGRAMME_STATUS|PST-0001]] beyond existing traceability already required by the PBK-0001 version bump.
4. Any change to the PBK-0001 session-initialisation or WP0A process text.
5. Any change to the historical archive policy itself.
6. Any attempt to rewrite or delete ESR-0013 archival records.

---

# 9. Constraints

1. Keep the implementation minimal and traceable.
2. Do not alter the meaning of the knowledge-tier model.
3. Do not widen scope to unrelated PBK-0001 clauses.
4. Preserve the existing document structure and style of PBK-0001.
5. Treat the breadcrumb update as the only substantive content change.

---

# 10. Validation

After implementation, run:

```powershell
python scripts/validate_repository.py --governance-only
git diff --check
git status --short
```

Validation should confirm:

1. PBK-0001 no longer presents the ESR-0013 archive artefacts as the latest historical session record.
2. PBK-0001 breadcrumb references now match the current archive state.
3. REG-0001 remains internally consistent with the PBK-0001 version bump.
4. No unauthorised files changed.

---

# 11. Risks And Dependencies

## Dependencies

1. [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] as the target artefact.
2. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] as the traceability register.
3. [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] for the current knowledge-tier model.
4. [[PST-0001_PROGRAMME_STATUS|PST-0001]] for current status context.

## Risks

1. The archive breadcrumb may have more than one occurrence, so the implementation must verify all stale references were corrected.
2. The correction should not accidentally rewrite legitimate historical lineage references.
3. Broader archive-policy cleanup would create unnecessary scope and should be avoided.

---

# 12. Approval Request

This package is ready for Programme Sponsor review.

If approved, the Engineering Implementer may apply the narrow PBK-0001 historical-archive breadcrumb correction and the corresponding REG-0001 traceability update in the next authorised implementation step.

**Approved by the Programme Sponsor, 15 July 2026.** Implemented as scoped: PBK-0001's OSE Relationships breadcrumb repointed - HST-0020/FCH-0020 (Claude) now carry the "latest" descriptor; HST-0013/FCH-0013 retained immediately below, reworded to note they are kept for lineage and are no longer the latest archive entry. PBK-0001 Document Control incremented 1.23 to 1.24, REG-0001 updated to match (artefact table row and Version History).

**Observation raised during implementation, not actioned by this package**: REG-0001's own controlled-artefact table has no entries at all for HST-0015 through HST-0020 or FCH-0020_GPT, despite these files existing under `aiems/History/` and `aiems/History/Full Chat/`. Per Programme Sponsor direction, this gap is not being raised as a new EBR-0001 backlog item now - it is deferred to a Work Package at ESR-0021 closure.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Target of the requested correction. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register expected to reflect the resulting PBK-0001 version change. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Provides current programme baseline context. |
| [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] | Defines the knowledge-tier model this correction preserves. |
| HST-0020_CLAUDE_CHAT_SUMMARY | Current Claude-side historical session record; new breadcrumb target. |
| FCH-0020_CLAUDE_FULL_CHAT_HISTORY | Current Claude-side full chat historical evidence record; new breadcrumb target. |
| HST-0013_ESR-0013_CHAT_HISTORY | Historical artefact retained for lineage, no longer the latest breadcrumb target. |
| FCH-0013_ESR-0013_FULL_CHAT_HISTORY | Historical artefact retained for lineage, no longer the latest breadcrumb target. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.2 | 15 July 2026 | Claude Engineering Implementer | Recorded Programme Sponsor approval (Section 12); implemented the approved package - PBK-0001 OSE Relationships breadcrumb repointed to HST-0020/FCH-0020 (Claude), HST-0013/FCH-0013 retained as lineage-only, Document Control 1.23 to 1.24, REG-0001 aligned. Raised the REG-0001 HST/FCH registration gap as an observation, deferred to ESR-0021 closure per Programme Sponsor direction. ESR-0021 WP3. |
| 0.1 | 15 July 2026 | ChatGPT Engineering Reviewer | Drafted EIP-ESR0021-002 to correct PBK-0001's stale historical-archive breadcrumb references from ESR-0013 artefacts to the current ESR-0020 Claude artefacts. |
