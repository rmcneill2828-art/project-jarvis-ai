# EIP-ESR0056-003 - Device Bootstrap and Restore Architecture (EBG-0046)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0056-003 |
| Title | Engineering Implementation Package: WP3 Device Bootstrap and Restore Architecture |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0056 |
| Work Package | WP3 |

---

# 2. Purpose

Implements ESR-0056 WP3: [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0046 (Device Independence and Restore Architecture) - "define bootstrap, progressive restore, portable memory, configuration and encrypted sync requirements," per [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]]'s decision that "devices host JARVIS but do not define JARVIS."

**Scope correction found and flagged before drafting:** EBG-0046's own description is broader than what is genuinely still undefined. [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] (accepted ESR-0026 WP2, after EBG-0046 was written but before its ESR-0034 WP1 promotion to Approved Backlog) Section 8 already defines the portable-memory and encrypted-sync requirements for memory records specifically, and Section 10 explicitly reserves "device bootstrap, the sync protocol, or device registry" for EBG-0046, naming EBG-0046 as the item that "implements the sync/restore protocol Section 8 assumes." Programme Sponsor directed scoping this Work Package to the genuine remaining gap: **bootstrap, device registry, the sync protocol, and progressive-restore mechanics**, plus **general (non-memory) configuration portability** - cross-referencing MDS-0001's memory-specific requirements rather than re-deriving them.

No implementation is authorised by EBG-0046 - this Work Package's deliverable is a requirements/architecture document, matching MDS-0001/GAM-0001/AAM-0001's own precedent as domain-specific models split out from [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]]'s high-level "Platform Services" summary once a domain needs real depth.

---

# 3. Repository Context Investigated

* [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]]: the governing decision - "devices host JARVIS but do not define JARVIS"; requires bootstrap, progressive restore, minimal data pull-down for new hardware, portable memory, portable configuration; Consequences name Platform Services as needing "bootstrap, configuration, device registry, progressive restore, health, capability registry and backup/sync coordination."
* [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] Section 8 (Device Portability and Encrypted Sync): memory records "shall be structured so they can be synchronised... the sync *protocol*, bootstrap and device-registry mechanics belong to Platform Services per ADR-0012 and remain EBG-0046's scope"; any memory record leaving a device "shall be encrypted"; progressive restore of memory data "is itself subject to the same personal/shared-family partitioning... and consent traceability... as the originating device." Section 10 (Explicit Non-Goals) confirms MDS-0001 does not "implement device bootstrap, the sync protocol, or device registry - reserved for EBG-0046." This Work Package treats MDS-0001 Section 8 as authoritative for memory-record portability and does not restate it.
* [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]]: the consent-gate/authority model MDS-0001 Section 8 requires be preserved across devices - this Work Package's device-registry and progressive-restore design must not create a second path around it.
* [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]]: defines the identity that ADR-0012's OSE Relationships note "must survive device changes" - bootstrap's identity-establishment step depends on this without redefining it.
* [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]]'s current "Platform Services" section (five generic bullets: configuration management, logging, monitoring, diagnostics, service discovery) does not yet reflect ADR-0012's specific requirement that Platform Services include bootstrap/device-registry/progressive-restore/backup-sync-coordination - a pre-existing gap, not something this Work Package is scoped to fix, but the new model's Related Artefacts will note it.
* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0023 (Backup, Recovery and Data Protection): explicitly gated on MDS-0001 existing first (already does); this Work Package's device-registry/sync-protocol design is a further prerequisite EBG-0023 will need once actioned, disclosed but not itself scoped here.
* Existing model-artefact naming/structure precedent: `aiems/models/` holds one file per domain (AAM-0001, GAM-0001, MDS-0001, SAM-0001, UAM-0001), each following a similar Document Control / Purpose / Scope / Architectural Position / domain sections / Explicit Non-Goals / Future Evolution / OSE Relationships / Related Artefacts / Version History shape.

---

# 4. Scope

## 4A. New controlled artefact: `DRA-0001 - Device Bootstrap and Restore Architecture`

Created at `aiems/models/DRA-0001_DEVICE_BOOTSTRAP_AND_RESTORE_ARCHITECTURE.md`, Draft status pending Sponsor acceptance (matching MDS-0001's own lifecycle - created Draft, later formally Accepted). Full planned content, for Codex design review before being written into the real file:

### Purpose and Scope
Defines the Platform Services mechanics ADR-0012 requires and MDS-0001 Section 8 assumes but explicitly does not define: bootstrap, device registry, the sync protocol, and progressive restore - plus general (non-memory) configuration portability, which no existing artefact covers. Does not redefine memory-record structure, encryption requirement, or personal/shared-family partitioning (MDS-0001 owns these, cross-referenced not restated). Does not implement code, select a specific sync transport/library, or define backup/recovery operational policy (EBG-0023).

### Architectural Principles
* **Local-first remains authoritative.** Per ADR-0012, no device becomes a new system of record merely by receiving synced data - sync is a continuity/availability mechanism, not a redefinition of where truth lives.
* **No device is a consent-gate bypass.** Every device-registry, bootstrap or restore operation touching Personal or Shared Family Memory is subject to the same GAM-0001 consent boundaries as the originating device (MDS-0001 Section 8's own requirement, restated here only as a binding principle for this document's own design, not re-derived).
* **Progressive, not all-at-once.** A device becoming useful should not block on a complete restore - staged pull-down (Section below) exists specifically to avoid a new/reconnecting device being unusable until every historical record has synced.
* **Identity-scoped vs device-scoped configuration.** Configuration that represents user/household identity or preference (persona settings, provider preference, Sentinel trust-tier selection) travels with sync; configuration that represents local hardware/environment (file system paths, detected local-provider availability, device-specific capability flags) does not and is re-derived per device.

### Device Registry
A first-class record of every device a user/household has authorised, held by Platform Services:
* **Identity binding**: each registered device is bound to the AAM-0001 identity it serves, established during bootstrap (below) - a device is never itself the identity.
* **Capability metadata**: what a device can do locally (e.g. can it run local LLM/voice providers, is it headless, its storage capacity) - informs progressive restore's staging (below) and future scheduling decisions, but does not gate consent.
* **Trust/authorisation state**: distinct from GAM-0001's per-content consent gate - this is device-level "is this device currently authorised to hold synced data at all," independent of which specific memory tier a piece of content belongs to. **Device-registry trust authorises a device to participate in sync; it never itself grants access to any specific memory tier or item** (Codex design-review tightening) - every retained/surfaced memory item remains separately governed by GAM-0001's role authority, scoped consent and personal/shared-family partitioning (MDS-0001 Section 7.2/7.4), exactly as on the originating device. A trusted device is not, by that trust alone, entitled to see everything that happens to sync to it.
* **Revocation**: removing a lost/compromised device's registry entry must be possible without requiring that device's own cooperation, and must be disclosed to the user/household as a security-relevant event (exact notification mechanism is a future implementation decision, not specified here).

### Bootstrap
The sequence a device follows to become a working JARVIS instance, in three distinct cases:
1. **First-ever device** (no existing household/user identity anywhere): establishes identity (AAM-0001) fresh; nothing to restore.
2. **New device joining an existing identity**: identity is verified against the existing registry (not re-created); device is added to the registry; progressive restore (below) begins.
3. **Re-provisioning an existing, previously-registered device** (e.g. after a local wipe): identity is re-verified; existing registry entry is either reused or explicitly re-issued at the Programme Sponsor's/household's discretion - this document does not mandate which, only that it is a deliberate choice, not an automatic default.

Bootstrap's minimum bar: a device is considered "bootstrapped" once identity is established/verified and it is present in the device registry - it need not hold any synced content yet to be considered bootstrapped; content arrives via progressive restore.

### Sync Protocol (shape, not implementation)
This document specifies the protocol's required properties, not a chosen transport or library - that remains a future implementation decision:
* **Trigger model**: sync may be event-driven (a change occurs, propagate it) or periodic/on-demand - this document does not mandate one, only that whichever is chosen must not violate the encryption-in-transit requirement MDS-0001 Section 8 already states.
* **Conflict handling**: a resolution strategy must exist and be explicit before implementation - this document does not select one (last-write-wins, per-field merge, or conflict surfaced to the user), but requires that the eventual implementation package state and justify its choice rather than leaving it undefined.
* **Scope of what syncs**: memory records within MDS-0001's own boundaries (Sections 6-8), identity-scoped configuration (this document's own Configuration Portability section, below), and Device Registry/restore metadata (device capability records, revocation state, progressive-restore staging markers) - explicitly excludes session-scoped ephemeral state (MDS-0001 Section 6.1's Session Memory tier is, by its own definition, not intended to persist beyond a session, so it does not sync).
* **Encryption and policy controls apply to everything that leaves a device, not only memory** (Codex design-review correction): ADR-0012 states this requirement generally ("restore and sync require encryption and policy controls"), not scoped to memory alone. MDS-0001 Section 8 remains authoritative for memory-record payload rules specifically; this document is authoritative that the same encryption-in-transit and policy-control requirement extends to identity-scoped configuration and Device Registry/restore metadata whenever either leaves a device via sync or restore. No synced or restored item of any kind - memory, configuration, or registry/restore metadata - travels in plaintext or unpoliced.

### Progressive Restore
Staged pull-down order for a device that has just been bootstrapped onto an existing identity, so the device becomes minimally useful quickly rather than blocking on full historical restore:
1. Identity and identity-scoped configuration (persona, provider preference, Sentinel trust tier) - smallest payload, makes the device immediately recognisable as "this JARVIS."
2. Personal Memory (MDS-0001 Section 6.2) - subject to the same consent traceability as the originating device.
3. Shared Family Memory (MDS-0001 Section 6.3), once/if that tier is implemented - its own, potentially broader, consent gate applies per-item, not granted wholesale by the device restore itself.
4. Historical/bulk content (older records not needed for immediate usefulness) - lowest priority, may complete in the background or on demand.

A device's capability metadata (Device Registry, above) may inform pacing (e.g. a storage-constrained device may defer stage 4 indefinitely) but never skips stage 1's consent-traceability requirement to go faster.

### Configuration Portability
Distinguishes what travels with identity from what does not:
* **Identity-scoped (syncs)**: persona/characterisation settings, provider preference ordering, Sentinel trust-tier selection, any user-facing preference not tied to physical hardware.
* **Device-scoped (does not sync, re-derived locally)**: local file-system paths, detected local-provider availability (e.g. whether a local LLM is actually installed on this machine), device-specific capability flags already captured in the Device Registry.
* Configuration that is ambiguous between the two (none identified during this drafting pass) would need an explicit per-item decision in a future revision, not silently defaulted either way.

### Explicit Non-Goals
* Memory-record structure, encryption requirement, or personal/shared-family partitioning - MDS-0001 Sections 6-8 own these; this document cross-references, does not restate or re-derive them.
* Backup, recovery, or data-protection operational policy - reserved for EBG-0023, gated on this document existing (alongside MDS-0001).
* Selecting or evaluating a specific sync transport, library, or database technology.
* Any production source code.
* Redefining GAM-0001's consent gate or AAM-0001's identity model - both are depended upon, neither is altered.

### Future Evolution
Anticipated follow-on work, to be sequenced in [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] once this document is accepted:
* An Engineering Implementation Package implementing the Device Registry and bootstrap flow.
* An Engineering Implementation Package implementing the sync protocol (having chosen a concrete transport/conflict-resolution strategy against this document's required properties).
* EBG-0023 (Backup, Recovery and Data Protection), once actioned, gated on both MDS-0001 and this document.
* A future MOD-0001 refresh to reflect its "Platform Services" section against this document's and ADR-0012's actual requirements (disclosed gap, not this Work Package's scope).

## 4B. Update EBG-0046's EBR-0001 entry

Record this document's creation and scope-narrowing rationale in the existing row (no new backlog number).

## 4C. Update MDS-0001's Future Evolution / Section 8 cross-references

Section 8's existing prose already anticipates EBG-0046 as future work by name - update its phrasing once DRA-0001 exists to point to the real artefact ID rather than only the backlog item number, preserving the existing non-restatement boundary.

## 4D. Explicitly out of scope

* Any implementation of bootstrap, device registry, sync protocol, or progressive restore code.
* Selecting a specific sync transport/library.
* MOD-0001's own Platform Services section refresh (disclosed as a related future gap, not actioned here).
* EBG-0023 itself.

---

# 5. Validation Requirements

* `python scripts/validate_repository.py` - 0 errors, warning count disclosed.
* Manual cross-check: every cross-reference this document makes to MDS-0001/GAM-0001/AAM-0001/ADR-0012 matches those artefacts' actual current text (not an assumed or outdated reading).
* Manual re-read confirming this document does not restate any requirement MDS-0001 Section 8 already states as authoritative.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* `DRA-0001` created, Draft status, covering bootstrap/device-registry/sync-protocol/progressive-restore/configuration-portability requirements without redefining what MDS-0001 already owns.
* EBG-0046's EBR-0001 row updated to reflect the document's creation and scope-narrowing rationale (not closed - Draft artefacts require separate Sponsor acceptance, matching MDS-0001's own precedent).
* MDS-0001 Section 8's forward-reference updated to name the real artefact.
* No implementation code of any kind introduced.
* `validate_repository.py` remains clean.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 4 September 2026 | Claude Engineering Implementer | Programme Sponsor approved via direct chat instruction ("Approved"), implemented exactly as scoped in v0.2: `DRA-0001` created at `aiems/models/DRA-0001_DEVICE_BOOTSTRAP_AND_RESTORE_ARCHITECTURE.md`, Draft status, 15 sections following the MDS-0001 structural precedent. EBR-0001's EBG-0046 row updated to Drafted with the scope-narrowing rationale (not Complete - formal DRA-0001 acceptance is a separate future decision). MDS-0001 Sections 8/10/11 forward references repointed from the bare EBG-0046 name to the real DRA-0001 artefact, no boundary text changed. `validate_repository.py` clean. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 0.2 | 4 September 2026 | Claude Engineering Implementer | Codex Engineering Reviewer design review via the AIEMS Exchange Bridge - **Conditional Pass**, one required fix folded in: the Sync Protocol section's encryption/policy-control requirement was scoped to memory records only (via MDS-0001 Section 8), but ADR-0012 states the requirement generally; Configuration Portability introduces non-memory data (identity-scoped configuration, Device Registry/restore metadata) leaving a device with no equivalent stated requirement. Fixed - Sync Protocol now states the requirement extends to everything that leaves a device, with MDS-0001 remaining authoritative only for memory-record payload rules specifically. One non-blocking tightening also folded in: Device Registry's trust/authorisation-state bullet now explicitly states device-registry trust authorises participation only, never memory-tier access - every item remains separately governed by GAM-0001/MDS-0001's existing consent and partitioning rules. Codex confirmed no Fail-level issue with the new-artefact scoping decision, the MDS-0001 boundary elsewhere, or the EBR-0001/MDS-0001 cross-reference update plan. Not yet approved or implemented. |
| 0.1 | 4 September 2026 | Claude Engineering Implementer | ESR-0056 WP3 draft - EBG-0046 (Device Independence and Restore Architecture), scope narrowed to bootstrap/device-registry/sync-protocol/progressive-restore/configuration-portability (the genuine remaining gap once MDS-0001 Section 8's own reservation is accounted for) per Programme Sponsor direction. Not yet reviewed, approved or implemented. |
