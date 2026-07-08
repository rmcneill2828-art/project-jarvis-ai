# RBL-0011 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0011 |
| Title | ESR-0015 Repository Baseline |
| Version | 0.1 |
| Status | Draft |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] |
| Previous Baseline | [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 8 July 2026 |

---

# 2. Purpose

RBL-0011 is drafted and recommended, recording the repository baseline proposed at the conclusion of ESR-0015. It has **not** been accepted. Per [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]], only the Programme Sponsor may accept a Repository Baseline - this document records a recommendation and its supporting evidence, not an acceptance decision.

It would capture the accepted repository state after ESR-0015's Sentinel execution pipeline delivery: audit infrastructure, policy abstraction, first external provider adapter, Guardian integration, and a live, audited, policy-gated conversation demonstrated end to end against a real external AI provider.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Ready for ESR-0016, pending Programme Sponsor baseline acceptance decision |

---

# 4. Baseline Recommendation Rationale

Recommended by Engineering Reviewer (ChatGPT), concurred by Engineering Implementer (Claude), during ESR-0015 WP6 closure.

[[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] (ESR-0009) has remained the accepted baseline across five subsequent sessions (ESR-0010 through ESR-0014), including ESR-0014 itself, which delivered the Sentinel package this session builds on and explicitly declined a new baseline. ESR-0015 is judged qualitatively different: prior sessions established architecture; ESR-0015 is the first to demonstrate that architecture working end to end against a real external system.

Countervailing context recorded for completeness: [[PST-0001_PROGRAMME_STATUS|PST-0001]] already tracks current repository state on an ongoing, accurately-maintained basis, so the incremental informational value of a new formal snapshot is more about marking a milestone than filling a gap PST-0001 doesn't already cover. This does not change the recommendation, but is offered so the Programme Sponsor's acceptance decision is made with the full picture.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `sentinel/audit.py` | AuditRecorder infrastructure: AuditEvent, AuditRecorder protocol, MemoryAuditRecorder, JsonAuditRecorder. |
| `sentinel/policy.py` | PolicyEngine abstraction: PolicyDecision, PolicyEngine protocol, SimpleApprovalPolicy. |
| `sentinel/openai_provider.py` | First external provider adapter, using stdlib urllib, injectable transport, controlled error handling. |
| `jarvis/interfaces/sentinel_conversation.py` | Guardian/Sentinel integration: SentinelGatedConversationProvider. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Brought to Approved status; decision outcome recorded (Primary OpenAI, Secondary Gemini). |
| `scripts/wp5_first_conversation_demo.py` | First live, audited, policy-gated Guardian conversation, demonstrated against OpenAI. |
| [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] | ESR-0015 closure report created and closed. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Updated for ESR-0015 closure and ESR-0016 entry recommendation. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Updated throughout ESR-0015; RBL-0011 registered. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] remains the accepted operational product capability baseline unless separately updated. First Light's deterministic-by-default GUI behaviour is unchanged - ESR-0015 built the Sentinel-gated conversation capability without wiring it as the running application's default.

Provider execution beyond OpenAI (Gemini, Anthropic, OpenRouter, Ollama), persistent memory, richer trust-tier policy, agent runtime, voice, vision, internet-backed assistance and automation remain outside the accepted operational product baseline until separately implemented and accepted.

---

# 7. Architecture Outcomes

ESR-0015 proved, rather than newly decided, the following architecture:

- Sentinel as the AI Execution and Security Platform ([[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]]) - demonstrated operationally, not just designed.
- Guardian expresses intent; Sentinel governs execution - demonstrated via `SentinelGatedConversationProvider`.
- Provider independence - architecturally supported (`ProviderConfiguration`/`ProviderRegistry`), with one provider (OpenAI) now implemented and proven; further providers remain future work.

---

# 8. Scope Boundaries

Scope boundaries for this baseline recommendation:

- no ESR-0016 artefact is created;
- no new product capability baseline is created;
- First Light GUI default wiring is unchanged - remains deterministic-by-default;
- Gemini, Anthropic, OpenRouter and Ollama provider adapters are not implemented by this baseline;
- richer trust-tier policy engine is not implemented by this baseline - deferred to ESR-0016.

---

# 9. Verification

Repository validation performed during ESR-0015 WP6 closure confirmed:

- Git working tree was clean at each commit.
- Repository branch was `main`.
- Repository was synchronised with `origin/main` at each commit.
- 133/133 tests passing, zero regressions across the session.
- `python scripts/validate_repository.py` passed with 0 errors, 0 warnings.
- [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] was closed.
- [[PST-0001_PROGRAMME_STATUS|PST-0001]] recorded ESR-0015 closure.
- [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] remains the current accepted baseline pending this recommendation's acceptance.

---

# 10. Handover to ESR-0016

ESR-0016 entry is recommended, not created, by this baseline. Per [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]]'s Lead/Reviewer rotation: **ChatGPT leads, Claude reviews.**

Opening review should include:

1. [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] and this document, RBL-0011 (accepted or not)
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]]
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]]
4. [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]]
5. [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]]
6. [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]]
7. `EBG-0047`, `EBG-0020`, `EBG-0021` (trust-tier design inputs)

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] | Engineering session this baseline recommendation is drawn from. |
| [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] | Previous accepted repository baseline, retained pending this recommendation's acceptance. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline, unchanged by this recommendation. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status updated for ESR-0015 closure. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline recommendation. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Provider evaluation matrix; decision outcome recorded during ESR-0015. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial ESR-0015 operated under. |
| [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] | Decision authority for Sentinel's positioning, proven operationally by ESR-0015. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.1 | 8 July 2026 | Claude Engineering Implementer | Initial ESR-0015 repository baseline drafted and recommended by Engineering Reviewer (ChatGPT), concurred by Engineering Implementer (Claude). Not yet accepted - Programme Sponsor acceptance decision pending per STD-0004. |
