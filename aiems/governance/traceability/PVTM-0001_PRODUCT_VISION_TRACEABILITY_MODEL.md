# PVTM-0001 - Product Vision Traceability Model

---

# Document Control

| Field | Value |
|-------|-------|
| Artefact ID | PVTM-0001 |
| Title | Product Vision Traceability Model |
| Version | 0.3 |
| Status | Draft |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Pending Programme Sponsor Review |
| Classification | Internal |
| Created During | ESR-0008 |
| Review Frequency | Triggered |

---

# Purpose

PVTM-0001 provides the traceability model showing how product vision flows through the AI Engineering Platform into implementation and verification.

It defines the blueprint for tracing Project JARVIS AI product vision through architecture, architectural domains, capabilities, engineering packages, repository artefacts, verification evidence and repository baselines.

PVTM-0001 owns relationships, not source content. It references authoritative artefacts rather than duplicating architecture, capability, backlog, baseline or session content.

---

# Scope

## In Scope

- Vision traceability.
- Architectural domain traceability.
- Capability traceability.
- Engineering package traceability.
- Repository artefact traceability.
- Verification traceability.
- Baseline traceability.
- OSE relationship support.

## Out of Scope

- Redefining architecture.
- Replacing [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]].
- Replacing [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]].
- Replacing [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]].
- Acting as a backlog.
- Acting as an implementation plan.

---

# Engineering Authority

PVTM-0001 applies the following authority hierarchy when interpreting engineering relationships:

1. GitHub repository.
2. Controlled artefacts.
3. OSE relationships.
4. Engineering Session Reports.
5. Engineering summaries.
6. Full historical chats.
7. Current engineering session.

Where conflict exists, repository evidence and controlled artefacts take precedence over recovered or conversational evidence.

---

# Evidence Sources

PVTM-0001 was prepared from repository-first validation of the following evidence:

- Git repository state on `main`.
- [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]].
- [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]].
- [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]].
- [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
- [[REG-0002_ADR_REGISTER|REG-0002]].
- [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]].
- [[PST-0001_PROGRAMME_STATUS|PST-0001]].
- [[ESR-0007A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0007A]].
- ESR-0008 WP1 engineering directive and closure evidence.

---

# Main Content

## Traceability Model

The approved traceability model is:

```text
Vision
  |
  v
Architectural Domain / Service
  |
  v
Capability
  |
  v
Engineering Package
  |
  v
Repository Artefact
  |
  v
Verification Evidence
  |
  v
Repository Baseline
```

This model shall be used to relate product intent to architecture, implementation and verification without duplicating the authoritative content held by the linked artefacts.

---

## Canonical Architectural Domains

The current repository-defined JARVIS architectural domains are recorded in [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]]:

- AI Core.
- Memory Services.
- Voice Services.
- Vision Services.
- Guardian Services.
- Automation Services.
- User Experience.
- Platform Services.
- External Integrations.

The following recovered candidate or alignment domains require future review:

- Sentinel.
- Engineering Assistant.
- Knowledge / OSE.
- Provider Architecture.

These recovered candidates are not approved MOD-0001 changes unless already represented in controlled artefacts. They shall be treated as alignment candidates for future architecture review.

---

## Relationship Rules

PVTM-0001 shall:

- reference authoritative artefacts rather than duplicate them;
- trace relationships between vision, architecture, implementation and verification;
- distinguish repository-approved architecture from recovered historical intent;
- record evidence status;
- support future engineering review.

---

## Evidence Status Model

PVTM-0001 uses the following evidence status values:

| Status | Meaning |
|--------|---------|
| Verified | Confirmed directly through repository evidence. |
| Approved | Approved through controlled governance or accepted baseline evidence. |
| Represented | Conceptually present in an existing controlled artefact or repository structure. |
| Recovered | Identified from historical engineering discussion or handover evidence. |
| Candidate | Proposed for future review and not yet approved. |
| Deferred | Recognised but intentionally held for later consideration. |
| Missing | Not currently represented by verified repository evidence. |

---

## OSE Integration

PVTM-0001 is an OSE navigation and traceability view over the existing Engineering Knowledge Graph.

It shall use WikiLinks to existing artefacts only. It shall not create speculative links or imply approval of recovered concepts that are not yet represented in controlled repository evidence.

PVTM-0001 supports OSE by showing how controlled artefacts, architecture, capability evidence, implementation records and baselines relate to each other.

## ESR-0008 Architecture Traceability

ESR-0008 extends PVTM traceability with the following architecture outcomes:

| Outcome | Traceability Position |
|---------|----------------------|
| Guardian Identity Architecture | Traced through [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] and [[ADR-0010_GUARDIAN_IDENTITY_AND_HITL_GOVERNANCE|ADR-0010]]. |
| UXP | Traced through [[ADR-0007_USER_EXPERIENCE_PLATFORM_SELECTION|ADR-0007]] and product architecture alignment. |
| Sentinel Gate of Durin | Traced through [[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]]. |
| Agent Framework | Traced through [[ADR-0011_AGENT_FRAMEWORK|ADR-0011]]. |
| Obsidian / OSE Engineering Ecosystem | Traced through [[ADR-0013_ENGINEERING_ECOSYSTEM_SYNCHRONISATION|ADR-0013]]. |
| Hybrid AI Runtime | Traced through [[ADR-0008_HYBRID_AI_RUNTIME_STRATEGY|ADR-0008]]. |
| Device Independence / Portable Restore | Traced through [[ADR-0012_DEVICE_INDEPENDENCE_AND_PORTABLE_RESTORE|ADR-0012]]. |

---

# OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[ERR-0001_ENGINEERING_RECOVERY_REPORT|ERR-0001]] | Records the WP1 recovery evidence and findings that informed this traceability model. |
| [[EIR-0001_ENGINEERING_IMPLEMENTATION_RECOMMENDATION|EIR-0001]] | Uses this traceability model to recommend ESR-0009 architecture validation and first implementation package selection. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Defines Guardian identity and cognitive architecture traced from ESR-0008 recovery. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | Records ESR-0008 closure outcomes that extend this traceability model. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Authoritative platform and JARVIS architectural domain source. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Authoritative JARVIS product vision and product architecture source. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Authoritative capability maturity and readiness view. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Registers controlled artefacts that participate in traceability. |
| [[REG-0002_ADR_REGISTER|REG-0002]] | Records architecture decisions that may affect traceability. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records governed future work without being replaced by PVTM-0001. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Provides current programme context and repository-first session guidance. |
| [[ESR-0007A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0007A]] | Provides strategic handover evidence into ESR-0008. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Platform architecture authority referenced by the traceability model. |
| [[JARVIS_PRODUCT_ARCHITECTURE|JARVIS Product Architecture]] | Product vision authority traced by PVTM-0001. |
| [[JARVIS_CAPABILITY_READINESS_MATRIX|JARVIS Capability Readiness Matrix]] | Capability readiness authority referenced by PVTM-0001. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Controlled artefact registration source. |
| [[REG-0002_ADR_REGISTER|REG-0002]] | Architecture decision register supporting traceability. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog authority kept separate from PVTM-0001. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme state and repository-first guidance source. |
| [[ESR-0007A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0007A]] | ESR-0008 strategic handover source. |
| [[ERR-0001_ENGINEERING_RECOVERY_REPORT|ERR-0001]] | WP1 recovery findings source. |
| [[EIR-0001_ENGINEERING_IMPLEMENTATION_RECOMMENDATION|EIR-0001]] | Recommended next activity based on WP1 recovery. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Guardian identity architecture traced by PVTM-0001. |
| [[ESR-0008_ENGINEERING_SESSION_REPORT|ESR-0008]] | ESR-0008 closure report recording architecture outcomes. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.3 | 2 July 2026 | Codex Engineering Implementer | Aligned OSE relationship wording with ESR-0008 closure and ESR-0009 validation readiness. |
| 0.2 | 2 July 2026 | Codex Engineering Implementer | Updated traceability for ESR-0008 Guardian identity, UXP, Sentinel, Agent Framework, Obsidian/OSE, hybrid runtime and portable restore outcomes. |
| 0.1 | 2 July 2026 | Codex Engineering Implementer | Initial draft created during ESR-0008 WP1 to define the product vision traceability model. |
