# OSE-0001 - Organic Semantic Enhancement Update Rule

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | OSE-0001 |
| Title | Organic Semantic Enhancement Update Rule |
| Version | 0.1 |
| Status | Draft |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Pending Programme Sponsor Review |
| Classification | Internal |
| Parent | [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] |
| Created During | ESR-0009 readiness |
| Review Frequency | Triggered by OSE workflow change |

---

# 2. Purpose

OSE-0001 defines the rule for applying Organic Semantic Enhancement to existing Project JARVIS AI controlled artefacts.

It exists to support retrospective OSE enrichment without changing the approved meaning, authority, status or evidential character of existing artefacts.

This artefact supports future work associated with [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], including EBG-0043 Engineering Ecosystem Synchronisation Workflow and EBG-0044 Obsidian / OSE Validation Workflow.

---

# 3. Scope

## In Scope

- OSE relationship sections.
- Verified WikiLinks.
- Related artefact relationship cleanup.
- Retrospective relationship wording.
- Artefact class guidance for future OSE enrichment.
- Validation expectations for OSE documentation changes.

## Out of Scope

- Changing historical decisions.
- Reopening accepted baselines.
- Reinterpreting approved artefact intent.
- Creating runtime JARVIS functionality.
- Making Obsidian or any external tool the source of truth.
- Replacing [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]].

---

# 4. Authority

OSE updates shall follow the current AIEMS authority order:

1. Git repository evidence.
2. Controlled artefacts.
3. OSE relationships.
4. Engineering Session Reports.
5. Engineering summaries.
6. Historical conversations.
7. Current engineering discussion.

Where conflict exists, repository evidence and controlled artefacts take precedence over OSE relationship convenience.

[[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] remains the architecture decision authority for Engineering Ecosystem Synchronisation. [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] remains the traceability model authority for product vision relationships.

---

# 5. OSE Update Principles

| Principle | Rule |
|-----------|------|
| Repository Authority | GitHub and the Git repository remain the source of truth. |
| Navigation Only | OSE improves semantic navigation and traceability; it does not approve implementation. |
| Verified Links | OSE links shall point to existing repository Markdown artefacts only. |
| Historical Integrity | Historical artefacts shall not be rewritten to imply that OSE existed at the time of original approval. |
| Minimal Meaning Change | OSE updates shall avoid changing requirements, decisions, statuses, baselines or ownership. |
| Register Alignment | Controlled artefact version changes shall be reflected in [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]]. |
| Validation Required | OSE updates shall pass repository validation before commit. |

---

# 6. Artefact Class Rules

| Artefact Class | OSE Treatment | Rationale |
|----------------|---------------|-----------|
| Current operating artefacts | Full OSE relationship section allowed where useful. | These guide active engineering work. |
| Architecture and traceability artefacts | Full OSE relationship section encouraged where relationships are verified. | These are natural relationship hubs. |
| ADRs created before OSE | Use retrospective wording such as Subsequent OSE Relationships. | Preserves original decision history. |
| Standards and charters | Treat as governance-impacting; use related links first unless approved. | Normative text can create unintended obligations. |
| Registers | Use OSE sparingly; registers already provide structured relationships. | Avoid duplicating register function. |
| Reviews and feature records | Apply OSE only where navigation value is clear. | Avoid low-value historical churn. |
| Accepted baselines | Avoid direct enrichment unless explicitly approved. Prefer external traceability. | Baselines are evidence snapshots. |
| Session reports | Preserve closure evidence; add only subsequent navigation if approved. | Sessions record historical state. |
| Runtime logs and chat archives | Do not treat as controlled OSE artefacts unless promoted. | Runtime evidence is not governance authority by default. |

---

# 7. Standard Wording Patterns

For current artefacts:

```text
# OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| Target artefact WikiLink | Verified relationship description. |
```

For retrospective artefacts:

```text
# Subsequent OSE Relationships

The following relationships were added after original artefact creation to support repository navigation. They do not change the original decision, status or approval basis.
```

For accepted baselines or archival session records:

```text
# Subsequent OSE Navigation

This section provides later navigation context only. It does not modify the accepted baseline or historical session evidence.
```

---

# 8. Validation Expectations

Every OSE enrichment package shall verify:

- all WikiLinks resolve;
- controlled artefact versions match [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]];
- historical wording is preserved where required;
- accepted baselines are not reinterpreted;
- no source or test files are changed unless explicitly approved;
- `python scripts/validate_repository.py` passes;
- `git diff --check` passes.

For governance-only OSE packages, `python scripts/validate_repository.py --governance-only` should also pass.

---

# 9. Phase 2 Readiness Criteria

Phase 2 OSE enrichment may proceed when:

1. OSE-0001 has been created and registered.
2. The working tree is clean or contains only approved Phase 1 changes.
3. Repository validation passes.
4. The first target artefact class is selected.
5. The intended OSE treatment for that artefact class is stated before editing.

Recommended first target class: current operating artefacts, including [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]], [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]].

---

# 10. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Architecture decision establishing Engineering Ecosystem Synchronisation and OSE context. |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Traceability model that uses OSE as a navigation and relationship view. |
| [[ERR-0001_ENGINEERING_RECOVERY_REPORT|ERR-0001]] | Recovery report that identifies OSE as emerging repository relationship infrastructure. |
| [[EIR-0001_ENGINEERING_IMPLEMENTATION_RECOMMENDATION|EIR-0001]] | Recommendation artefact that carries ESR-0009 validation context. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme status and ESR-0009 readiness context. |
| [[RBL-0009_REPOSITORY_BASELINE|RBL-0009]] | Current accepted repository baseline and ESR-0009 handover point. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog source containing EBG-0043 and EBG-0044 OSE workflow items. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Controlled artefact register that records OSE-0001. |

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]] | Parent decision authority. |
| [[PVTM-0001_PRODUCT_VISION_TRACEABILITY_MODEL|PVTM-0001]] | Product vision traceability authority. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Current programme state. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Registration and version alignment authority. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog authority for future OSE workflow work. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.1 | 2 July 2026 | Codex Engineering Implementer | Initial OSE update rule created for Phase 1 of retrospective OSE enrichment. |