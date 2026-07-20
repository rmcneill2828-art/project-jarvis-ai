# MDS-0001 - Memory and Data Storage Architecture

> *"Guardian remembers what it has been trusted to keep, structured so that trust can be revoked as cleanly as it was given."*

**Version:** 1.2

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | MDS-0001 |
| Title | Memory and Data Storage Architecture |
| Version | 1.2 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] |
| Effective Date | 17 July 2026 |
| Review Frequency | At architecture review or Memory implementation package selection |

---

# 2. Purpose

MDS-0001 defines the storage architecture behind Guardian's Memory faculty: how session, personal and shared-family knowledge is structured, persisted, made portable across devices, and technically deleted when consent is revoked.

It resolves [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0019 (JARVIS Memory and Data Storage Architecture, open since ESR-0004's EIP-EKR-0001 vision recovery), and implements the exact scope [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 9.2 already reserved for it: *"the underlying storage technology, encryption, technical retention duration, or data architecture"* sitting behind GAM-0001's consent gate. GAM-0001 governs *whether* Guardian may retain something and *who consented*; MDS-0001 governs *how* that retained thing is actually stored, structured, and made portable once consent exists.

This artefact provides architectural authority only. It does not implement a storage engine, schema, or runtime persistence code.

---

# 3. Scope

MDS-0001 covers:

- a taxonomy of what Guardian stores (Section 6), grounded in [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]]'s Memory faculty and `jarvis/architecture/JARVIS_PRODUCT_ARCHITECTURE.md` Section 7's existing Session/Personal/Shared-Family split;
- storage architecture principles (Section 7) - local-first persistence, the data-layer boundary between personal and shared-family memory, and technical retention/deletion mechanics;
- how memory participates in device portability and encrypted sync (Section 8), as a consumer of [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]]'s existing decision, not a redefinition of it;
- the extension point [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0023 (Backup, Recovery and Data Protection) needs once actioned;
- explicit non-goals for current and future implementation packages.

MDS-0001 does not cover:

- whether Guardian may retain something, or who must consent - governed by [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Sections 9.1/9.2, referenced here, not restated;
- Guardian's cognitive Memory faculty definition itself (what memory *is* to Guardian's identity) - defined in [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]];
- device bootstrap, progressive restore, device registry, or the general sync/restore protocol - defined in [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]] and reserved for EBG-0046 (Device Independence and Restore Architecture); MDS-0001 specifies what memory needs *from* that protocol, not the protocol itself;
- backup, recovery, or data-protection mechanics - reserved for EBG-0023, which JRM-0001 explicitly gates on MDS-0001 existing first;
- the AIEMS Knowledge Capability (repository-backed engineering knowledge graph) - already implemented separately under EBG-0055 (Guardian Orb knowledge-graph phases); a distinct system from Guardian's personal/session/family memory, sharing no schema or consent model with it;
- any specific database product's operational configuration (backup schedules, replication, hosting) beyond naming an initial embedded engine (Section 7.3) - a full technology evaluation is not in scope, matching how PEM-001 evaluated AI providers but no equivalent evaluation exists yet for storage engines;
- React components, Tauri behaviour, Python implementation details, or executable schema/migration code.

---

# 4. Architectural Position

MDS-0001 sits beneath [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]]'s consent gate - it implements the storage architecture that gate protects, not the gate itself. A memory-write request is classified and consented under GAM-0001 first; only once approved does it reach the data layer MDS-0001 defines.

```text
MOD-0001
  |
  v
SAM-0001  (Sentinel: can this be trusted?)
  |
  v
AAM-0001  (Guardian: who is acting?)
  |
  v
GAM-0001  (Guardian: is this action authorised, and who consented?)
  |
  v
MDS-0001  (how is retained knowledge structured, stored and made portable?)
  |
  v
UAM-0001  (how is this experienced by the user?)
  |
  v
Engineering Implementation Packages
```

MDS-0001 does not redefine Guardian's authority or consent model. It defines the data architecture that model's already-consented decisions are recorded into.

---

# 5. Relationship to GAM-0001's Consent Gate and Current Implementation State

| GAM-0001 Element | Already Defined |
|---|---|
| Consent scoping | Section 9.1 - consent is scoped to the specific action, never a standing grant |
| Memory-retention consent boundary | Section 9.2 - a retention request is itself a classified, consented Guardian action |
| Personal/shared-family distinction | Section 8.2 - the boundary exists; mechanics deferred to this artefact |
| Privacy boundary reinforcement | Section 9.4 - crossing personal/shared-family is itself `HUMAN_APPROVAL_REQUIRED`, never inferred |

MDS-0001 does not alter any of the above. It defines the storage-layer mechanism that records a consent decision once GAM-0001 has produced one, and enforces the personal/shared-family boundary Section 9.4 requires at the data layer, not only in application logic.

**Evidence check (updated post-ESR-0027)**: Personal Memory (Section 6.2) is now implemented - `jarvis/memory/store.py` (`PersonalMemoryStore`) and `jarvis/memory/service.py` (`PersonalMemoryService`) provide a working, consent-gated, unit-tested implementation delivered at ESR-0027 WP1 (EBG-0080), wired into `GuardianRuntime`. Session Memory (Section 6.1) and Shared Family Memory (Section 6.3) remain unimplemented. `jarvis/architecture/JARVIS_CAPABILITY_READINESS_MATRIX.md` (v2.1, refreshed ESR-0028 WP2) correctly reflects this as "Partial" maturity. This artefact continues to define the architecture that Session and Shared Family Memory would build against; only the Personal tier exists in code today.

---

# 6. Memory Taxonomy

Grounded in `jarvis/architecture/JARVIS_PRODUCT_ARCHITECTURE.md` Section 7's existing product-level description ("provide personal, family and session memory in a way that supports useful assistance while preserving privacy boundaries") and [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]]'s Memory faculty definition ("preserves personal, family, session and governed knowledge within consent and retention boundaries").

## 6.1 Session Memory

Conversation-scoped context for the duration of an active interaction. Not retained beyond the session by default - session memory becoming persistent (e.g. summarised into personal memory) is itself a retention event subject to GAM-0001 Section 9.2's consent gate, not an automatic promotion.

## 6.2 Personal Memory

Private to the individual household member who is its subject. Per GAM-0001 Section 8.2, personal memory must never be surfaced in a shared-family context without the Section 9.4 approval gate. At the storage layer (Section 7.2), this requires partitioning that makes crossing this boundary a deliberate, checked operation - not merely an application-logic convention that a future code change could silently bypass.

## 6.3 Shared Family Memory

Household-scoped knowledge belonging to the family context rather than any one individual, per GAM-0001 Section 8.1's household role model. Guest-role users have no access to shared family memory (GAM-0001 Section 8.1); Child-role users' access is bounded by GAM-0001 Section 8.2's child-safe assistance boundary.

## 6.4 Out of Scope: AIEMS Knowledge Capability

The repository-backed engineering knowledge graph (EBG-0055, already implemented in phases) is a distinct system - it stores project/engineering artefacts and their relationships, not personal or family knowledge, and carries no consent-retention model since it is not personal data. MDS-0001 does not cover it and the two systems shall not share a schema, store, or access-control model.

---

# 7. Storage Architecture Principles

## 7.1 Local-First Persistence

Per [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]]'s existing decision ("local-first hybrid runtime cache"), each device holds a local, functional copy of the memory a user needs on that device. Per ADR-0012 Section 6's consequence, "local runtime caches are not authoritative memory by themselves" - a device's local store is a cache of a portable, synchronised memory model (Section 8), not an independent system of record.

## 7.2 Data-Layer Partitioning of the Personal/Shared-Family Boundary

Session, Personal and Shared Family memory (Section 6) shall be structurally separated at the storage layer - distinct stores, or clearly partitioned tables/collections with access paths that require an explicit, checked crossing to move data between them. This operationalises GAM-0001 Section 9.4's requirement that crossing the boundary is a deliberate `HUMAN_APPROVAL_REQUIRED` action, not an inference: a schema that mixed personal and shared-family records in one undifferentiated table would make an accidental crossing a query bug rather than a governed action, which this architecture must not permit.

## 7.3 Initial Storage Engine

Recommended: an embedded, file-based engine (e.g. SQLite, via Python's standard library) as the initial local store - zero-install, dependency-light, and consistent with the Programme Sponsor's no-discretionary-budget constraint (no hosted database service, no new recurring cost). This is a starting-point recommendation, not a full technology evaluation comparable to PEM-001's AI-provider matrix; revisiting the engine choice remains open if a future implementation package finds a concrete reason to.

## 7.4 Technical Retention and Deletion

GAM-0001 Section 9.2 explicitly reserves "technical retention duration" as this artefact's scope. When consent for a retained item is revoked (per GAM-0001 Section 9.1's per-action consent scoping), the storage architecture shall support deleting that specific item without requiring a broader destructive operation - consent revocation for one personal-memory record must not require, for example, clearing an entire user's memory store to honour it. Each retained item shall be traceable to the consent decision that authorised it, so a revocation can be resolved to the exact records it covers.

---

# 8. Device Portability and Encrypted Sync

Per [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]]'s decision that "devices host JARVIS but do not define JARVIS" and require "portable memory... restore and sync require encryption and policy controls":

- Memory records (Section 6) shall be structured so they can be synchronised across a household member's devices - the sync *protocol*, bootstrap and device-registry mechanics belong to Platform Services per ADR-0012 and remain EBG-0046's scope, not redefined here;
- any memory record leaving a single device (for sync, backup, or restore) shall be encrypted, per ADR-0012 Section 6's consequence that "restore and sync require encryption and policy controls" - this artefact does not specify the encryption mechanism itself, which is a Platform Services concern, but requires that no memory record is ever synchronised or backed up in plaintext;
- a new device's progressive restore (ADR-0012) of memory data is itself subject to the same personal/shared-family partitioning (Section 7.2) and consent traceability (Section 7.4) as the originating device - portability does not create a second path around GAM-0001's consent gate.

---

# 9. Relationship to EBG-0023 (Backup, Recovery and Data Protection)

[[JRM-0001_PROJECT_ROADMAP|JRM-0001]] explicitly gates EBG-0023 on this artefact existing first. MDS-0001 does not define backup schedules, recovery procedures, or data-protection operational policy - it defines the data architecture (Sections 6-8) that a future EBG-0023 implementation package would need to back up and recover correctly, in particular the personal/shared-family partitioning (Section 7.2) and per-item consent traceability (Section 7.4) that any backup/recovery mechanism must preserve, not flatten.

---

# 10. Explicit Non-Goals

MDS-0001 does not:

- implement Guardian's consent gate or retention-authorisation decision - defined in GAM-0001 Sections 9.1/9.2;
- implement Guardian's cognitive Memory faculty itself - defined in AAM-0001;
- implement device bootstrap, the sync protocol, or device registry - reserved for EBG-0046 under ADR-0012;
- implement backup, recovery, or data-protection operational policy - reserved for EBG-0023;
- select or evaluate a production-grade hosted database - Section 7.3 names an initial embedded-engine recommendation only, not a final technology decision;
- implement the AIEMS Knowledge Capability's storage (already implemented separately under EBG-0055);
- write schema, migration, or runtime persistence code;
- create product source code.

---

# 11. Future Evolution

Future implementation packages may use MDS-0001 to guide Memory development. Anticipated follow-on work, already sequenced in [[JRM-0001_PROJECT_ROADMAP|JRM-0001]]:

- an Engineering Implementation Package implementing Session Memory (Section 6.1) and Shared Family Memory (Section 6.3) against Sections 6-7, extending the Personal Memory (Section 6.2) foundation already delivered at ESR-0027 WP1;
- EBG-0046 - Device Independence and Restore Architecture (implements the sync/restore protocol Section 8 assumes);
- EBG-0023 - Backup, Recovery and Data Protection (implements the backup/recovery mechanics Section 9 requires be preserved, once actioned).

Any such evolution shall require separately approved engineering packages.

---

# 12. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Consent gate this model sits beneath; parent artefact - MDS-0001 implements the storage architecture GAM-0001 Section 9.2 reserved for it. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Defines the Memory faculty this model's taxonomy (Section 6) implements. |
| [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]] | Decision this model's portability content (Section 8) is bound by, not a redefinition of. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Records Memory's current baseline state (Personal tier implemented, Session and Shared Family tiers not yet implemented), confirmed by this artefact's evidence check. |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] | Current accepted repository baseline. |

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0019 (resolved by this artefact), EBG-0046 and EBG-0023 (sequenced follow-on work referenced in Section 11), EBG-0015 (overlapping/adjacent investigative scope, distinct from this artefact's architecture-definition scope). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track B sequencing for EBG-0019 and its dependent follow-on items (EBG-0023 explicitly gated on this artefact). |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 9.2's pre-drawn boundary this artefact fills. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Registers MDS-0001 as a controlled architecture model. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.2 | 20 July 2026 | Claude Engineering Implementer | ESR-0031 WP0 fix round (Codex Medium finding on v1.1/commit 7393a03): Section 11's Future Evolution bullet still said a future package would implement `jarvis/memory/` "currently an empty stub" - reworded to reflect that Personal Memory is already delivered and only Session/Shared-Family remain. Section 12's OSE Relationships row for PCB-0001 still said it "records Memory's current not implemented baseline state" - corrected to describe the Personal/Session/Shared-Family split. |
| 1.1 | 20 July 2026 | Claude Engineering Implementer | ESR-0031 WP0 repository synchronisation: corrected Section 5's "Evidence check" paragraph, which still said no persistence implementation existed and `jarvis/memory/` was an empty stub - stale since ESR-0027 WP1 delivered Personal Memory (EBG-0080, `PersonalMemoryStore`/`PersonalMemoryService`). Now correctly states Personal Memory is implemented while Session and Shared Family Memory remain unbuilt. |
| 1.0 | 17 July 2026 | Claude Engineering Implementer | **Approved by the Programme Sponsor, 17 July 2026**, following Engineering Reviewer (Codex) confirmation via the AIEMS Exchange Bridge: the boundary against GAM-0001 is coherent (stays at the storage-architecture layer, does not reopen the consent gate), the Session/Personal/Shared-Family taxonomy matches AAM-0001 and the current product architecture, and the SQLite recommendation is clearly framed as an initial recommendation, not a final technology decision - no blocking findings. Status Draft to Approved, version 0.1 to 1.0, resolving EBG-0019 in EBR-0001. ESR-0026 WP2. |
| 0.1 | 17 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0026 WP2, resolving EBG-0019. Defines a Session/Personal/Shared-Family memory taxonomy grounded in existing product architecture and AAM-0001's Memory faculty; storage architecture principles (local-first persistence, data-layer partitioning of the personal/shared-family boundary, an initial embedded-engine recommendation, technical retention/deletion mechanics); device portability and encrypted sync bound by ADR-0012's existing decision; and the extension point EBG-0023 needs once actioned. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
