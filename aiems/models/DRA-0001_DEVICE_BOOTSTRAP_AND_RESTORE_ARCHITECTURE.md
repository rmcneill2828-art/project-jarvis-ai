# DRA-0001 - Device Bootstrap and Restore Architecture

> *"A device earns the right to participate; it is never handed the right to see."*

**Version:** 1.0

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | DRA-0001 |
| Title | Device Bootstrap and Restore Architecture |
| Version | 1.0 |
| Status | Draft |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]] |
| Effective Date | - |
| Review Frequency | At architecture review or Device Independence implementation package selection |

---

# 2. Purpose

DRA-0001 defines the Platform Services mechanics [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]] requires and [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] Section 8 assumes but explicitly does not define: bootstrap, device registry, the sync protocol, and progressive restore - plus general (non-memory) configuration portability, which no existing artefact covers.

It resolves the remaining scope of [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0046 (Device Independence and Restore Architecture) once MDS-0001's own reservation is accounted for: MDS-0001 Section 8 already owns memory-record portability and encryption requirements; this artefact owns everything ADR-0012 requires beyond that - the device-level mechanics memory portability itself depends on.

This artefact provides architectural authority only. It does not implement bootstrap, registry, sync, or restore code, and does not select a specific sync transport, library or database technology.

---

# 3. Scope

DRA-0001 covers:

- a Device Registry model (Section 6) - identity binding, capability metadata, trust/authorisation state, revocation;
- bootstrap (Section 7) - the three cases a device becomes a working JARVIS instance, and the minimum bar for "bootstrapped";
- the sync protocol's required properties (Section 8) - trigger model, conflict handling, scope of what syncs, and the encryption/policy-control requirement extended to everything that leaves a device, not memory alone;
- progressive restore (Section 9) - staged pull-down order so a device becomes useful without blocking on full historical restore;
- configuration portability (Section 10) - what configuration is identity-scoped (syncs) versus device-scoped (does not);
- explicit non-goals for current and future implementation packages.

DRA-0001 does not cover:

- memory-record structure, the no-plaintext-memory-sync requirement, or personal/shared-family partitioning - governed by [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] Sections 6-8, referenced here, not restated;
- Guardian's consent gate or role-authority model - governed by [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]], depended upon, not altered;
- the identity model devices bind to - defined in [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]];
- backup, recovery, or data-protection operational policy - reserved for EBG-0023, gated on both MDS-0001 and this artefact existing;
- selecting or evaluating a specific sync transport, library, or database technology;
- any production source code.

---

# 4. Architectural Position

DRA-0001 sits alongside [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] as a Platform Services domain model, both governed by [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]]. MDS-0001 defines what memory needs from device portability; DRA-0001 defines the device-level mechanics that provide it - the registry, bootstrap, sync protocol and restore staging MDS-0001 Section 8 explicitly assumes rather than defines. Neither artefact redefines the other's boundary: MDS-0001 remains authoritative for memory-record payload rules; DRA-0001 is authoritative for device-level mechanics and for the general (non-memory) encryption/policy-control requirement ADR-0012 states.

---

# 5. Architectural Principles

- **Local-first remains authoritative.** Per ADR-0012, no device becomes a new system of record merely by receiving synced data - sync is a continuity/availability mechanism, not a redefinition of where truth lives.
- **No device is a consent-gate bypass.** Every device-registry, bootstrap or restore operation touching Personal or Shared Family Memory is subject to the same GAM-0001 consent boundaries as the originating device (MDS-0001 Section 8's own requirement, restated here only as a binding principle for this artefact's own design, not re-derived).
- **Progressive, not all-at-once.** A device becoming useful should not block on a complete restore - staged pull-down (Section 9) exists specifically to avoid a new/reconnecting device being unusable until every historical record has synced.
- **Identity-scoped vs device-scoped configuration.** Configuration that represents user/household identity or preference travels with sync; configuration that represents local hardware/environment does not, and is re-derived per device (Section 10).
- **Encryption and policy controls apply to everything that leaves a device, not only memory.** ADR-0012 states this requirement generally ("restore and sync require encryption and policy controls"). MDS-0001 Section 8 is authoritative for memory-record payload rules specifically; this artefact is authoritative that the same requirement extends to identity-scoped configuration and Device Registry/restore metadata (Section 8.4).

---

# 6. Device Registry

A first-class record of every device a user/household has authorised, held by Platform Services:

- **Identity binding**: each registered device is bound to the AAM-0001 identity it serves, established during bootstrap (Section 7) - a device is never itself the identity.
- **Capability metadata**: what a device can do locally (e.g. can it run local LLM/voice providers, is it headless, its storage capacity) - informs progressive restore's staging (Section 9) and future scheduling decisions, but does not gate consent.
- **Trust/authorisation state**: distinct from GAM-0001's per-content consent gate - this is device-level "is this device currently authorised to hold synced data at all," independent of which specific memory tier a piece of content belongs to. **Device-registry trust authorises a device to participate in sync; it never itself grants access to any specific memory tier or item** - every retained/surfaced memory item remains separately governed by GAM-0001's role authority, scoped consent and personal/shared-family partitioning (MDS-0001 Section 7.2/7.4), exactly as on the originating device. A trusted device is not, by that trust alone, entitled to see everything that happens to sync to it.
- **Revocation**: removing a lost/compromised device's registry entry must be possible without requiring that device's own cooperation, and must be disclosed to the user/household as a security-relevant event (exact notification mechanism is a future implementation decision, not specified here).

---

# 7. Bootstrap

The sequence a device follows to become a working JARVIS instance, in three distinct cases:

1. **First-ever device** (no existing household/user identity anywhere): establishes identity (AAM-0001) fresh; nothing to restore.
2. **New device joining an existing identity**: identity is verified against the existing registry (not re-created); device is added to the registry; progressive restore (Section 9) begins.
3. **Re-provisioning an existing, previously-registered device** (e.g. after a local wipe): identity is re-verified; existing registry entry is either reused or explicitly re-issued at the Programme Sponsor's/household's discretion - this artefact does not mandate which, only that it is a deliberate choice, not an automatic default.

Bootstrap's minimum bar: a device is considered "bootstrapped" once identity is established/verified and it is present in the Device Registry (Section 6) - it need not hold any synced content yet to be considered bootstrapped; content arrives via progressive restore.

---

# 8. Sync Protocol

Required properties, not a chosen transport or library - selecting one remains a future implementation decision.

## 8.1 Trigger Model

Sync may be event-driven (a change occurs, propagate it) or periodic/on-demand - this artefact does not mandate one, only that whichever is chosen must not violate Section 8.4's encryption/policy-control requirement.

## 8.2 Conflict Handling

A resolution strategy must exist and be explicit before implementation - this artefact does not select one (last-write-wins, per-field merge, or conflict surfaced to the user), but requires that the eventual implementation package state and justify its choice rather than leaving it undefined.

## 8.3 Scope of What Syncs

Memory records within MDS-0001's own boundaries (Sections 6-8), identity-scoped configuration (Section 10), and Device Registry/restore metadata (device capability records, revocation state, progressive-restore staging markers) - explicitly excludes session-scoped ephemeral state (MDS-0001 Section 6.1's Session Memory tier is, by its own definition, not intended to persist beyond a session, so it does not sync).

## 8.4 Encryption and Policy Controls Extend Beyond Memory

ADR-0012 states the encryption/policy-control requirement generally, not scoped to memory alone. MDS-0001 Section 8 remains authoritative for memory-record payload rules specifically; this artefact is authoritative that the same encryption-in-transit and policy-control requirement extends to identity-scoped configuration and Device Registry/restore metadata whenever either leaves a device via sync or restore. No synced or restored item of any kind - memory, configuration, or registry/restore metadata - travels in plaintext or unpoliced.

---

# 9. Progressive Restore

Staged pull-down order for a device that has just been bootstrapped onto an existing identity, so the device becomes minimally useful quickly rather than blocking on full historical restore:

1. Identity and identity-scoped configuration (persona, provider preference, Sentinel trust tier) - smallest payload, makes the device immediately recognisable as "this JARVIS."
2. Personal Memory (MDS-0001 Section 6.2) - subject to the same consent traceability as the originating device.
3. Shared Family Memory (MDS-0001 Section 6.3), once/if that tier is implemented - its own, potentially broader, consent gate applies per-item, not granted wholesale by the device restore itself.
4. Historical/bulk content (older records not needed for immediate usefulness) - lowest priority, may complete in the background or on demand.

A device's capability metadata (Section 6) may inform pacing (e.g. a storage-constrained device may defer stage 4 indefinitely) but never skips stage 1's consent-traceability requirement to go faster.

---

# 10. Configuration Portability

Distinguishes what travels with identity from what does not:

- **Identity-scoped (syncs)**: persona/characterisation settings, provider preference ordering, Sentinel trust-tier selection, any user-facing preference not tied to physical hardware.
- **Device-scoped (does not sync, re-derived locally)**: local file-system paths, detected local-provider availability (e.g. whether a local LLM is actually installed on this machine), device-specific capability flags already captured in the Device Registry (Section 6).
- Configuration that is ambiguous between the two (none identified during this drafting pass) would need an explicit per-item decision in a future revision, not silently defaulted either way.

---

# 11. Explicit Non-Goals

DRA-0001 does not:

- redefine memory-record structure, the no-plaintext-memory-sync requirement, or personal/shared-family partitioning - MDS-0001 Sections 6-8 own these; this artefact cross-references, does not restate or re-derive them;
- implement backup, recovery, or data-protection operational policy - reserved for EBG-0023, gated on both MDS-0001 and this artefact existing;
- select or evaluate a specific sync transport, library, or database technology;
- redefine GAM-0001's consent gate or AAM-0001's identity model - both are depended upon, neither is altered;
- write schema, migration, or runtime persistence code;
- create product source code.

---

# 12. Future Evolution

Anticipated follow-on work, to be sequenced in [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] once this artefact is accepted:

- an Engineering Implementation Package implementing the Device Registry and bootstrap flow (Sections 6-7);
- an Engineering Implementation Package implementing the sync protocol (Section 8), having chosen a concrete transport/conflict-resolution strategy against this artefact's required properties;
- EBG-0023 (Backup, Recovery and Data Protection), once actioned, gated on both MDS-0001 and this artefact;
- a future MOD-0001 refresh to reflect its "Platform Services" section against this artefact's and ADR-0012's actual requirements (disclosed gap, not this artefact's own scope).

Any such evolution shall require separately approved engineering packages.

---

# 13. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]] | Decision this artefact implements the device-mechanics half of; parent artefact. |
| [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] | Sibling Platform Services domain model - owns memory-record portability/encryption; this artefact owns the device-level mechanics MDS-0001 Section 8 assumes. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Consent gate this artefact's Device Registry trust model explicitly does not bypass. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Defines the identity every registered device binds to. |
| [[RBL-0035_REPOSITORY_BASELINE|RBL-0035]] | Current accepted repository baseline at this artefact's creation. |

---

# 14. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0046 (resolved by this artefact's creation, pending Sponsor acceptance), EBG-0023 (sequenced follow-on work referenced in Section 12). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Sequencing for EBG-0046 and its dependent follow-on items. |
| [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] | Section 8's forward reference to EBG-0046 now points to this artefact. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Registers DRA-0001 as a controlled architecture model. |

---

# 15. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 4 September 2026 | Claude Engineering Implementer | ESR-0056 WP3: initial Draft, resolving EBG-0046's remaining scope (bootstrap, device registry, sync protocol, progressive restore, configuration portability) once MDS-0001 Section 8's own reservation for it is accounted for. Codex design-reviewed (Conditional Pass, folded in v0.2 of EIP-ESR0056-003 before this artefact was written: encryption/policy-control coverage extended beyond memory to configuration and registry/restore metadata; device-registry trust explicitly does not grant memory-tier access). Programme Sponsor approved via direct chat instruction ("Approved"). Draft status - formal acceptance is a separate future Programme Sponsor decision, matching MDS-0001's own lifecycle. |
