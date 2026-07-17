# ADR-0020 - Sentinel Network Exposure Security Requirements

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0020 |
| Title | Sentinel Network Exposure Security Requirements |
| Version | 1.0 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 17 July 2026 |
| Review Trigger | Any future proposal to make Guardian/Sentinel reachable from outside the Tauri shell's own stdio pipe |

---

# Purpose

Record the decision that any future network-facing Guardian/Sentinel interface must satisfy defined authentication, rate-limiting and transport-encryption requirements before implementation is approved - closing the gap the Programme Sponsor's own ESR-0025 question surfaced ("how robust is Sentinel - can it be exposed to the internet, would it be safe?"), resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0076.

---

# Scope

This decision covers the security requirements a future network-facing interface proposal must satisfy before approval. It does not implement authentication, rate limiting or TLS. It does not build a network-facing interface - none exists today and none is authorised by this decision. It does not redefine [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]]'s authority or consent model.

---

# Engineering Authority

Backlogged as EBG-0076 (Approved Backlog, High priority) following the Programme Sponsor's direct question at ESR-0025 and explicit "sooner rather than later" direction. Actioned at ESR-0026 WP3.

---

# Evidence Sources

- `jarvis/interfaces/stdio_rpc.py` and `src-tauri/src/lib.rs` - confirmed directly at ESR-0025: the only UXP-backend bridge is a Tauri sidecar-managed Python process communicating over stdio, with no listening network socket. "Exposing Sentinel to the internet" is not currently possible without first building an entirely new network interface.
- [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] Section 6 (Consequences) - already anticipated this exact scenario: "if a concrete future need arises that stdio genuinely cannot serve well (for example, a requirement for the backend to be reachable from something other than the Tauri shell itself), it should be reconsidered explicitly against that need." This ADR is that explicit reconsideration, made proactively rather than deferred until a concrete proposal forces it.
- `sentinel/policy.py` (`TrustTierPolicy`) and [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] Section 6 - `TrustTierPolicy` classifies *what* a Guardian action may do once a request has already arrived. It has no concept of authentication, rate limiting or transport security - it is a behavioural authority boundary, not a network security boundary, and was never designed to be one.
- [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] - `guardian.converse` can route to billed cloud providers (OpenAI, Gemini). An unauthenticated network-facing path to it would let anyone reaching it consume the Programme Sponsor's paid API credit freely, not merely a data-exposure risk.

---

# Main Content

# 1. Problem Statement

No network-facing interface exists today, but if one is ever proposed (e.g. a remote or mobile companion access capability), there is currently no defined security requirement gating it. `TrustTierPolicy` governs Guardian's behavioural authority once a request arrives; nothing today would authenticate who is making that request, limit abuse, or encrypt it in transit if a network interface were built without first addressing this.

---

# 2. Background

At ESR-0025, the Programme Sponsor asked directly how robust Sentinel is and whether it could safely be exposed to the internet. Investigation confirmed: no network interface exists (the UXP-backend bridge is local stdio only, per ADR-0019), and `TrustTierPolicy`/GAM-0001 is a behavioural boundary, not a network security boundary. This was registered as EBG-0076 (Approved Backlog, High priority) with the Programme Sponsor's explicit direction to address it "sooner rather than later" - understood as defining the requirement now, as a prerequisite gate, not building a network interface now (EBG-0076 itself authorises no implementation).

---

# 3. Options Considered

| Option | Assessment |
|--------|------------|
| Wait until a concrete network-interface proposal is made, decide security requirements then | Risk of security being bolted on after a design is already chosen, rather than gating the design itself - the same reactive pattern ADR-0019 explicitly warned against. |
| Pre-emptively build authentication/rate-limiting/TLS infrastructure now, with no interface to attach it to | Risk of building infrastructure that doesn't fit whatever network interface is eventually proposed - guessing at a shape nothing currently requires. Raised and agreed against during this same ESR-0026 session's WP0 scope check. |
| Define binding security requirements now as a prerequisite gate any future network-facing proposal must satisfy before approval, without building anything | Matches GAM-0001 Section 7's "no silent capability expansion" principle - gates the decision point without guessing at implementation. |

---

# 4. Decision

Any future proposal to make a Guardian/Sentinel capability reachable from outside the Tauri shell's own stdio pipe (Section 1) **must explicitly address and satisfy all three of the following before implementation is approved**:

1. **Authentication** - every request must be attributable to an authenticated identity (device or user). No anonymous request path to any Guardian/Sentinel capability.
2. **Rate limiting** - protection against abuse and resource exhaustion, in particular because `guardian.converse` can route to billed cloud providers (PEM-001) - unrestricted access is a direct financial exposure, not only a data-exposure one.
3. **Transport encryption (TLS)** - no Guardian/Sentinel traffic may travel over plaintext network transport.

This decision does not implement any of the three. It is a gate a future implementation proposal must pass through, not a specification of the mechanism (e.g. which authentication scheme, which rate-limit thresholds, which TLS library) - selecting those remains separate, future-scoped work once a concrete network interface is actually proposed.

---

# 5. Rationale

This follows directly from evidence already confirmed in the repository, not a general security preference:

- ADR-0019 already named this exact scenario as the one condition under which its own stdio-only decision should be revisited - this ADR is that revisit, done before a concrete proposal forces it, consistent with GAM-0001's "no silent capability expansion" principle of deciding boundaries deliberately rather than by accretion.
- `TrustTierPolicy` was evaluated directly (`sentinel/policy.py`) and confirmed to carry no authentication, rate-limiting or transport-security concept - it was designed to answer "is this action authorised," not "who is asking and how much can they ask." Treating it as a network security boundary would be a category error, not an incremental gap.
- `guardian.converse`'s live routing to billed cloud providers (confirmed at ESR-0022's provider wiring, PEM-001) makes an unauthenticated network path a direct cost-exposure risk to the Programme Sponsor, not merely a confidentiality concern - this makes authentication and rate limiting non-negotiable, not best-practice hardening.

---

# 6. Consequences

- Any future backlog item proposing a network-facing Guardian/Sentinel interface must explicitly demonstrate how it satisfies all three Section 4 requirements before Programme Sponsor approval - this ADR is a required review gate for that future item, not a standing implementation.
- The current stdio-only architecture (ADR-0019) is unaffected - nothing changes about the existing UXP-backend bridge.
- No new code, dependency, or infrastructure is introduced by this decision.
- A future implementation package is required to select and build the specific authentication, rate-limiting and TLS mechanisms, once a concrete network-facing interface is actually proposed and scoped - not decided here.

---

# 7. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] | Confirmed the current stdio-only, no-network-socket architecture; explicitly anticipated this decision's trigger condition. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Behavioural authority boundary this decision distinguishes from network security; Section 7's "no silent capability expansion" principle this decision applies proactively. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Confirms `guardian.converse`'s billed cloud-provider routing, the cost-exposure risk motivating the rate-limiting requirement. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0076, resolved by this decision. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[REG-0002_ADR_REGISTER|REG-0002]] | Registers this decision. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Records this decision as resolving EBG-0076; any future network-facing interface proposal remains separate, not-yet-registered work. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 17 July 2026 | Claude Engineering Implementer | **Approved by the Programme Sponsor, 17 July 2026**, following Engineering Reviewer (Codex) confirmation via the AIEMS Exchange Bridge: scope is coherent with ADR-0019, GAM-0001, `sentinel/policy.py` and PEM-001; the three requirements (authentication, rate limiting, TLS) are appropriately framed as preconditions for a future proposal, not implementation; no repository-state mismatch or scope overreach found. Defines a binding three-part security gate any future network-facing Guardian/Sentinel interface proposal must satisfy before approval, resolving EBG-0076. Status Draft to Approved. ESR-0026 WP3. |
