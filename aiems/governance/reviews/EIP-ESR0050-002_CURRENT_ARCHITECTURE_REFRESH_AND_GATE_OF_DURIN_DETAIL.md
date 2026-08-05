# EIP-ESR0050-002 - CURRENT_ARCHITECTURE.md Refresh and Sentinel Gate of Durin Detail

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0050-002 |
| Title | CURRENT_ARCHITECTURE.md Refresh and Sentinel Gate of Durin Detail |
| Version | 1.0 |
| Status | Approved - implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0050 WP3 |

---

# 2. Purpose

This package resolves [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0047 (Sentinel Gate of Durin Architecture Specification: "Extend EBG-0030 with Sentinel trust gateway, trust tiers and platform-entry validation details") by refreshing `aiems/architecture/CURRENT_ARCHITECTURE.md` in full and adding the trust-gateway/platform-entry-validation detail EBG-0047 specifically asks for.

---

# 3. Objective

Bring `CURRENT_ARCHITECTURE.md` current against real repository evidence (34 sessions stale, last substantively edited at ESR-0016 WP2A despite its own "Status" line claiming ESR-0014), correct one factually wrong claim, register it as a controlled artefact for the first time, and add a dedicated Sentinel Gate of Durin subsection documenting the real, already-implemented trust-gateway/platform-entry-validation pattern.

---

# 4. Repository Context

**Investigation that led to this scope** (per the Programme Sponsor's explicit two-part decision at WP3 selection): EBG-0047 asks to extend EBG-0030 (satisfied by [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]]) with trust-gateway/trust-tier/platform-entry-validation detail, citing [[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]]. Two existing artefacts were investigated as candidate targets before drafting scope:

- [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] - Draft, v0.3, last touched 9 July 2026 (version-metadata only), written before nearly all real Sentinel implementation. Its own Scope section explicitly disclaims "does not define... executable policy logic" - the wrong home for implementation-grounded trust-tier/gateway detail.
- `CURRENT_ARCHITECTURE.md` - self-designated "the authoritative architecture snapshot" for the next engineering session, and the actual target of ESR-0016 WP2A's own trust-tier-model update (commit `d6eb854`). Its existing Sentinel section explicitly states "The trust-tier model provides extension points for EBG-0047" - this document already names itself as EBG-0047's intended home. Four other controlled artefacts (AAM-0001, MOD-0001, SAM-0001, UAM-0001) each carry a "Subsequent Architectural Update" note explicitly pointing to `CURRENT_ARCHITECTURE.md` as "the current authoritative architecture snapshot for Sentinel's scope"; a fifth (GAM-0001) references it as authoritative through its own Related Artefacts table rather than a matching pointer-note heading (Codex design-review finding, corrected from an earlier overstatement that all five carried the same note). It is heavily load-bearing despite never itself being registered as a controlled artefact (no REG-0001 entry, no Document Control block, no version field).

**Confirmed factual error, not merely staleness**: `CURRENT_ARCHITECTURE.md` line 92 states "`SimpleApprovalPolicy` remains the production default for `SentinelTrustGateway`." Direct read of `jarvis/interfaces/stdio_rpc.py`'s `build_default_runtime()` (line 255): `gateway = SentinelTrustGateway(policy_engine=TrustTierPolicy())` - `TrustTierPolicy` has been the actual production default since ESR-0024 WP1 (EBG-0074, Complete). This claim has been actively wrong for approximately 26 sessions.

**Confirmed the document's "Status" line is itself wrong**: it claims "close of Engineering Session ESR-0014," but `git log`/ESR-0016's own Section 13.10 confirm the last substantive edit was ESR-0016 WP2A (commit `d6eb854`), not ESR-0014.

**Real current Sentinel/Guardian evidence gathered directly from code before drafting scope**: `sentinel/core.py` (`SentinelTrustGateway.evaluate()`'s real request-decision-response-audit flow), `sentinel/policy.py` (`TrustTier`/`TrustCategory`/`TrustTierPolicy.classify()`'s real precedence rules, unchanged since ESR-0016), `sentinel/audit.py` (`AuditEvent`/`AuditRecorder`/`MemoryAuditRecorder`/`JsonAuditRecorder`, not mentioned in the current document at all), `sentinel/orchestrator.py` (`ProviderOrchestrator`, `ProviderRoute`, `ProviderHealth` - broadly matches the existing Resilience Model diagram), and `jarvis/interfaces/stdio_rpc.py`'s `build_default_runtime()` in full (the real, single shared `gateway` instance every capability - conversation, memory, speech, transcription, and now the Agent Framework - is evaluated through, "one trust boundary, not two" per its own `EIP-ESR0027-001` Section 4 comment - this is the concrete platform-entry-validation evidence EBG-0047 asks to have documented).

---

# 5. Scope

## 5.1 Register `CURRENT_ARCHITECTURE.md` as a controlled artefact for the first time

Add a Document Control block (Artefact ID `CURRENT_ARCHITECTURE`, Version 1.0, Status Approved, Owner Programme Sponsor & Chief Engineering Advisor) and a Version History section - mirroring the precedent set for `JARVIS_CAPABILITY_READINESS_MATRIX` (registered for the first time at ESR-0028 WP2, per `EIP-ESR0028-002`). Register in [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] for the first time.

## 5.2 Correct the Status section

Replace the incorrect "close of Engineering Session ESR-0014" claim with an accurate statement of this refresh's basis (ESR-0050 WP3, superseding the ESR-0016 WP2A snapshot).

## 5.3 Refresh Guardian section

Update "Future Guardian Orb interaction" (now real, ESR-0019) and note the real Guardian faculties delivered since ESR-0014: Guardian Cognitive Core Phase 1 (ESR-0039), Personal Memory (ESR-0027 WP1), Identity (ESR-0046), Voice both directions (ESR-0040/ESR-0044/ESR-0047), Agent Framework (ESR-0049/ESR-0050). Responsibilities/Non-Responsibilities lists remain conceptually accurate and are not rewritten wholesale - only the stale forward-looking item is corrected.

## 5.4 Refresh Sentinel's "Current Implemented Capabilities"

Correct the wrong `SimpleApprovalPolicy`-is-default claim to state `TrustTierPolicy` is the real production default (EBG-0074, ESR-0024 WP1), with `SimpleApprovalPolicy` remaining the bare-construction default when no policy engine is explicitly injected. Add the capabilities implemented since ESR-0016 that the current document omits entirely: audit logging (`sentinel/audit.py`), self-hosted speech synthesis/transcription providers (Piper/Whisper, Sentinel-gated), the Agent Framework's `SentinelGatedAgentService`, and the real external-provider wiring (OpenAI/Gemini live-validated, Ollama local fallback, `LocalEchoProvider` final failover).

## 5.5 New subsection: Sentinel Gate of Durin - Trust Gateway and Platform-Entry Validation

Directly resolves EBG-0047. Documents, grounded in real code: the Gate of Durin metaphor ([[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]], "Speak, friend, and enter" as trusted-entry metaphor, not literal authentication); `SentinelTrustGateway.evaluate()`'s real request-decision-response-audit flow; `TrustTierPolicy.classify()`'s real precedence rules and tier/category/outcome mapping (unchanged since ESR-0016, still accurate); and the concrete evidence that platform-entry validation is real and shared, not per-capability: every one of `build_default_runtime()`'s capabilities (conversation, memory, speech, transcription, Agent Framework) is evaluated through the exact same shared `gateway` instance before executing.

## 5.6 Refresh Provider Ecosystem Architecture

Distinguish implemented from still-planned within each category: Direct Providers (OpenAI, Gemini - implemented, live-validated; Anthropic - approved in principle per PEM-001, not implemented); Local Providers (Ollama - implemented, EBG-0075; llama.cpp/LM Studio/vLLM - still illustrative examples, not implemented). Gateway Providers section unchanged (still illustrative only, no gateway provider implemented).

## 5.7 Replace "ESR-0015 Starting Architecture" section

This section's seven forward-looking items (PEM-001 scoring, provider ecosystem approval, first external adapter, secondary execution path, live failover validation, Guardian-through-Sentinel connection, first interactive conversation) are all long completed (by approximately ESR-0017). Replace with a brief historical note recording this, and redirect forward-looking guidance to [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - the artefacts already responsible for that role - rather than leaving a second, competing, now-inert forward-look inline.

## 5.8 Minor sections left unchanged

Platform Overview diagram, Core Architectural Principle, Runtime Architecture diagram, Resilience Model, Security Positioning, and Key Architecture Decisions Reflected remain conceptually accurate against current evidence and are not rewritten - only cross-checked.

---

# 6. Authorised Files

- `aiems/architecture/CURRENT_ARCHITECTURE.md`
- `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`
- `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md` (closing EBG-0047)
- `aiems/governance/sessions/ESR-0050_ENGINEERING_SESSION_REPORT.md`
- This package, `EIP-ESR0050-002_CURRENT_ARCHITECTURE_REFRESH_AND_GATE_OF_DURIN_DETAIL.md`

---

# 7. Implementation Requirements

1. Every new or corrected claim must be independently verifiable against real code (`sentinel/`, `jarvis/interfaces/stdio_rpc.py`) or real governance evidence (EBR-0001, PST-0001) - no aspirational or planned content presented as implemented.
2. The `SimpleApprovalPolicy`-is-production-default correction must be unambiguous - the document must not leave both the old and new claims present in a way that contradicts itself.
3. No other controlled artefact's content is modified by this package beyond REG-0001/EBR-0001 registration/closure bookkeeping and the ESR-0050 report - `SAM-0001`, `MOD-0001`, `GAM-0001`, `AAM-0001` and `UAM-0001`'s existing "Subsequent Architectural Update" pointer notes remain valid and are not touched.

---

# 8. Explicit Exclusions

This package does not:

- Implement, wire, or modify any Sentinel/Guardian code - documentation only.
- Rewrite `SAM-0001` - it remains Draft/architecture-position-only, per its own explicit scope; a future package may separately decide whether to promote or retire it now that `CURRENT_ARCHITECTURE.md` carries the implementation-grounded detail.
- Perform a full accuracy audit of every other artefact that cross-references `CURRENT_ARCHITECTURE.md` (AAM-0001, MOD-0001, GAM-0001, UAM-0001) - their existing pointer notes are read and confirmed still valid, not re-authored.
- Address any Theme 7/8 backlog item other than EBG-0047.

---

# 9. Validation

- `python scripts/validate_repository.py` (full mode) - 0 errors expected.
- Every new/corrected factual claim manually cross-checked against the real cited source file during drafting (recorded in Section 4 above).

---

# 10. Risks and Dependencies

## Dependencies

None - this package only reads already-implemented, already-tested code and already-approved governance artefacts.

## Risks

- **Low**: registering `CURRENT_ARCHITECTURE.md` for the first time changes its governance status (informal snapshot to controlled artefact) - mitigated by following the exact precedent already set for `JARVIS_CAPABILITY_READINESS_MATRIX`'s own first registration.

---

# 11. Approval Request

Requesting Codex design review of this draft, followed by Programme Sponsor approval-to-implement (verified via the real Sponsor Approval Service) before content is written.

---

# 12. Related Artefacts

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0047, this package's resolved backlog item.
* [[ADR-0009_SENTINEL_GATE_OF_DURIN_PATTERN|ADR-0009]] - the architecture decision this package documents the real implementation of.
* [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] - investigated as an alternative target, not selected (architecture-position-only by its own scope).
* [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] - the decision that broadened Sentinel's role beyond trust-gateway-only, already reflected in `CURRENT_ARCHITECTURE.md`'s existing pointer notes from other artefacts.
* [[ESR-0050_ENGINEERING_SESSION_REPORT|ESR-0050]] - this session, WP3.

---

# 13. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 5 August 2026 | Claude Engineering Implementer | **Implemented exactly as scoped in v0.2.** Programme Sponsor approval-to-implement verified via `submit-response` against the real Sponsor Approval Service. `CURRENT_ARCHITECTURE.md` registered as a controlled artefact for the first time (Document Control block, Version 1.0), Status corrected, wrong production-default claim corrected, Guardian's post-ESR-0014 faculties and Sentinel's post-ESR-0016 capabilities documented, new Sentinel Gate of Durin subsection added (resolving EBG-0047), Provider Ecosystem's implemented-versus-planned distinction clarified, obsolete "ESR-0015 Starting Architecture" section replaced with a historical note, Related Artefacts and Version History sections added. EBR-0001 EBG-0047 marked Completed. Validation: `python scripts/validate_repository.py` (full mode) - 0 errors. |
| 0.2 | 5 August 2026 | Claude Engineering Implementer | Codex design review: Pass with 1 non-blocking finding, folded in - the "each carry a Subsequent Architectural Update note" claim narrowed to four of the five cross-referencing artefacts (GAM-0001 references CURRENT_ARCHITECTURE.md differently, via its own Related Artefacts table). |
| 0.1 | 5 August 2026 | Claude Engineering Implementer | Initial draft. Scopes registering `CURRENT_ARCHITECTURE.md` as a controlled artefact for the first time, correcting its wrong production-policy-default claim and stale ESR-0014 status line, adding a Sentinel Gate of Durin subsection resolving EBG-0047, and replacing its long-completed "ESR-0015 Starting Architecture" section. Submitted for Codex design review. |
