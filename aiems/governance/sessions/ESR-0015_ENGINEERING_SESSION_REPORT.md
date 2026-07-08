# ESR-0015 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0015 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Session | ESR-0015 |
| Date Opened | 8 July 2026 |
| Date Closed | 8 July 2026 |
| Closure Status | Closed |
| Final Validation | 133 / 133 tests passing |

---

# 2. Purpose

This report records the opening, execution and closure of ESR-0015.

ESR-0015 is the first Engineering Session run under the [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Lead/Reviewer trial: Claude as Engineering Implementer (Lead), ChatGPT as Engineering Reviewer, Programme Sponsor gating every step.

---

# 3. Scope

ESR-0015 establishes the Sentinel execution pipeline so that Guardian interactions are auditable, policy-controlled and provider-independent, culminating in the first policy-gated Guardian conversation.

---

# 4. Engineering Authority

ESR-0015 opening was authorised by Programme Sponsor approval of WP0B on 8 July 2026, following WP0A Repository Synchronisation confirming [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] and [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] were both formally closed.

ESR-0015 closure is authorised by Programme Sponsor approval following Engineering Reviewer (ChatGPT) closure review.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Establish the Sentinel execution pipeline so that Guardian interactions are auditable, policy-controlled and provider-independent, culminating in the first policy-gated Guardian conversation.

**Outcome: achieved.** See Section 12, WP5 Evidence Table.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP1 | `AuditRecorder` infrastructure (`MemoryAuditRecorder` + `JsonAuditRecorder`) | Complete (commit `5733e45`) |
| WP2 | `PolicyEngine` abstraction and `SimpleApprovalPolicy` | Complete (commit `cdf283e`) |
| WP3a | Complete PEM-001 scoring against current provider information; Programme Sponsor approves primary provider, secondary provider, and first adapter to implement | Complete. Primary: OpenAI. Secondary: Google Gemini. Reasoning/coding comparison: Anthropic (retained). Gateway: OpenRouter (experimentation only). Local fallback: Ollama. First adapter: OpenAI direct. Scored independently by Claude and ChatGPT against PEM-001's 8 weighted criteria; both evaluators ranked OpenAI first despite each having a structural bias toward their own maker's provider. |
| WP3b | Implement the approved provider adapter | Complete (commit `a9d89fa`) |
| WP4 | Guardian to Sentinel integration | Complete (commit `e70c420`) |
| WP5 | End-to-end validation and first audited/policy-gated conversation | Complete (commits `057f40b`, `fcdec8a`) - see Section 12 Evidence Table |
| WP6 | Session closure and engineering handover | Complete (this report) |

This plan was reviewed and refined by the Engineering Reviewer (ChatGPT) during WP0B, which split the originally-proposed WP3 into WP3a/WP3b after identifying that provider selection is an unmet decision gate under [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]]'s own "Decision Required" section, not an implementation detail that should be decided unilaterally by the Implementer.

---

# 7. Architectural Milestones

ESR-0015 marks the point at which Project JARVIS AI's Sentinel architecture moved from designed to operationally proven. Prior sessions established architecture; ESR-0015 demonstrated it working end to end against a real external system. Enduring milestones, per Engineering Reviewer recognition:

- First end-to-end Sentinel execution pipeline.
- First `PolicyEngine` abstraction.
- First `AuditRecorder` infrastructure.
- First external provider adapter.
- First live provider execution.
- First audited, policy-gated Guardian conversation.
- Provider-independent execution path established (`ProviderConfiguration`/`ProviderRegistry` support registering further providers without touching `SentinelTrustGateway` or `ProviderOrchestrator`).

---

# 8. Executive Summary

ESR-0015 built and validated the Sentinel execution pipeline: audit recording, policy evaluation, provider orchestration and a real external provider adapter, connected through to Guardian's conversation layer, and demonstrated end to end with a live, billed OpenAI API call that was allowed by policy, executed successfully, and fully recorded in an audit trail.

The session ran under the [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] trial: every work package was drafted as an Engineering Implementation Package, reviewed by the Engineering Reviewer (ChatGPT) before implementation, and gated by explicit Programme Sponsor approval. Ten Engineering Reviewer findings were raised across the session; all ten were accepted and implemented, including one classic Python mutable-default-argument bug (WP1), a circular-import risk self-caught by the Lead (WP2), three required adjustments to the first external adapter (WP3b), two refinements preventing internal policy/error detail from reaching end users (WP4), and four safety adjustments to the live-call demonstration script (WP5) plus a follow-up fix motivated directly by a real diagnostic gap encountered during that live run.

Test coverage grew from 105 to 133 passing tests with zero regressions at any point. Repository validation (`scripts/validate_repository.py`) remained clean throughout.

---

# 9. Engineering Outcomes

1. Established `sentinel/audit.py`: `AuditEvent`, `AuditRecorder` protocol, `MemoryAuditRecorder`, `JsonAuditRecorder`.
2. Wired audit recording into `SentinelTrustGateway` and `ProviderOrchestrator`, covering both the decision and execution stages, not decision alone.
3. Established `sentinel/policy.py`: `PolicyDecision`, `PolicyEngine` protocol, `SimpleApprovalPolicy` - extracted from existing inline approval logic with zero behaviour change, verified by regression test.
4. Resolved a circular import between `core.py` and `policy.py`, unanticipated by the approved EIP, via deferred import - verified empirically by importing all affected modules standalone and together.
5. Completed [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] provider scoring against current (2026) evidence, independently by both Lead and Reviewer against the same 8 weighted criteria. Approved: Primary OpenAI, Secondary Gemini, reasoning/coding comparison Anthropic, Gateway OpenRouter (experimentation only), local fallback Ollama.
6. Implemented `sentinel/openai_provider.py`: `OpenAIProvider`, the first external provider adapter - stdlib `urllib` only (no new dependency), injectable transport for testability, controlled error handling that never surfaces raw exception messages or credentials.
7. Implemented `jarvis/interfaces/sentinel_conversation.py`: `SentinelGatedConversationProvider`, connecting Guardian's conversation layer through Sentinel's trust/policy/audit/execution pipeline, without changing First Light's deterministic-by-default GUI behaviour.
8. Demonstrated the first live, policy-gated, audited Guardian conversation against a real external AI provider (`scripts/wp5_first_conversation_demo.py`), executed by the Programme Sponsor directly (not by an AI tool call, by design).
9. Diagnosed and fixed a real gap found through that live run: HTTP status codes were not surfaced in adapter error messages, making a billing failure indistinguishable from an auth or model-identifier failure without manual investigation. Fixed to surface status codes (safe, non-sensitive) while continuing to suppress raw exception messages.
10. Brought [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] to Approved status, recording the decision outcome in place of the prior open "Decision Required" section.

---

# 10. Validation Summary

| Stage | Tests Passing |
|---|---:|
| Start of ESR-0015 (post ESR-0014A) | 105 |
| WP1 complete | 114 |
| WP2 complete | 120 |
| WP3b complete | 127 |
| WP4 complete | 132 |
| WP5 / status-code fix complete | 133 |

Final result:

```text
133 passed, 0 failed, 0 regressions
```

`python scripts/validate_repository.py` reported 0 errors, 0 warnings at every commit across the session. `ruff check .` remained clean throughout except for one pre-existing, unrelated finding in `sentinel/orchestrator.py` that predates ESR-0015 and was not introduced by it.

---

# 11. WP0 Session Initialisation Record

WP0A Repository Synchronisation confirmed: README.md, [[PST-0001_PROGRAMME_STATUS|PST-0001]] (v2.18), [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]]/[[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] closed, [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] tiers (Current State, Architecture, Active Standards), [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]], [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]], repository baseline [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]], clean working tree, 105/105 tests passing, 0 validation errors/warnings.

WP0B confirmed: session identifier ESR-0015, Programme Phase 2 (JARVIS Architecture Readiness), baseline RBL-0010, objective and work package plan as above, Programme Sponsor approval obtained 8 July 2026.

---

# 12. WP5 Evidence Table

First live, Sentinel-mediated Guardian conversation. Recorded per Engineering Reviewer (ChatGPT) recommendation, run via `scripts/wp5_first_conversation_demo.py` (not part of the automated test suite - requires a real API key and makes a real, billed call).

| Stage | Result |
|---|---|
| Policy | ALLOW |
| Audit | 4 events across 2 runs (decision+failed, then decision+succeeded) |
| Provider | OpenAI |
| Model | gpt-5.5 |
| Conversation | Successful on second attempt; first attempt failed on exhausted API credit (HTTP 429) |
| Response content | Received, but hallucinated - the model has no real knowledge of this private, unpublished project and produced a plausible but factually incorrect description |
| Tests | 133/133 pass, unaffected (demo intentionally outside the automated suite) |
| Repository validation | Pass |

The first run's `HTTPError` gave no way to distinguish a billing issue from an auth issue or a bad model identifier without manually querying the OpenAI models endpoint. Commit `fcdec8a` (same session) fixed this: `sentinel/openai_provider.py` now surfaces the HTTP status code specifically (safe, non-sensitive protocol-level information) rather than only the exception type name.

Audit log (`~/.jarvis/logs/wp5_demo.jsonl`, outside the repository per `logs/` not being gitignored) is not committed; its content is captured here as the durable record instead, consistent with the repository being the authoritative source of truth.

---

# 13. Repository Deliverables

## Code

- `sentinel/audit.py` (new)
- `sentinel/core.py` (amended: audit and policy wiring)
- `sentinel/orchestrator.py` (amended: audit wiring)
- `sentinel/policy.py` (new)
- `sentinel/openai_provider.py` (new)
- `sentinel/__init__.py` (amended: exports)
- `jarvis/interfaces/sentinel_conversation.py` (new)
- `jarvis/interfaces/__init__.py` (amended: exports)

## Tests

- `jarvis/tests/test_sentinel_audit.py` (new)
- `jarvis/tests/test_sentinel_policy.py` (new)
- `jarvis/tests/test_openai_provider.py` (new)
- `jarvis/tests/test_sentinel_conversation.py` (new)

## Scripts

- `scripts/wp5_first_conversation_demo.py` (new)

## Governance

- [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] (brought to Approved status, decision outcome recorded)
- [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] (this report)
- [[PST-0001_PROGRAMME_STATUS|PST-0001]] (updated throughout, opening and closure)
- [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] (updated throughout)
- [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] (drafted, recommended - Programme Sponsor acceptance pending, see Section 16)

---

# 14. Outstanding Work

Deferred intentionally, not blocking ESR-0015 closure:

- Gemini, Anthropic, OpenRouter and Ollama provider adapters - approved in principle under [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] WP3a but not yet implemented.
- Richer trust-tier policy engine (per `EBG-0047`) - deferred to ESR-0016, to be informed by real ESR-0015 audit evidence rather than designed speculatively.
- `RetryPolicy` exists on `ProviderConfiguration` but is not yet consumed by any adapter or by `ProviderOrchestrator`.
- Streaming responses.
- First Light GUI default wiring to Sentinel - deliberately deferred; First Light remains deterministic-by-default per [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]].
- Voice (ElevenLabs/Deepgram) - credentials available per Programme Sponsor note, but no approved work package exists.
- `GuardianRuntime`/`ConversationService` architectural merge - not attempted; remain separate objects as before ESR-0015.

---

# 15. Risks / Technical Debt

- `SimpleApprovalPolicy` performs no real trust-tier discrimination - all requests not explicitly flagged `requires_approval` are `ALLOW`ed uniformly. Adequate for current scope; should not be mistaken for a real security policy ahead of the ESR-0016 policy design work.
- No default persistent audit path is wired into the running JARVIS application - only `scripts/wp5_first_conversation_demo.py` wires `JsonAuditRecorder` to a real file. A production Guardian session today would only get in-memory (`MemoryAuditRecorder`) audit by default.
- `OpenAIProvider` has no retry/backoff on transient failures (e.g. rate limits) - a single failed attempt fails the whole request. `ProviderOrchestrator`-level failover exists across *different* registered providers, but there is currently only one.
- Only one external provider is implemented. [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]]'s stated goal of provider independence is architecturally supported (`ProviderConfiguration`/`ProviderRegistry`) but not yet demonstrated in practice with a second provider.

---

# 16. Repository Baseline Recommendation

Engineering Reviewer (ChatGPT) recommendation, concurred by Engineering Implementer (Claude): create [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]].

Rationale: [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] (ESR-0009) has remained the accepted baseline across five subsequent sessions (ESR-0010 through ESR-0014), including ESR-0014 itself, which delivered the Sentinel package this session builds on and explicitly declined a new baseline. ESR-0015 is judged qualitatively different: prior sessions established architecture, ESR-0015 is the first to demonstrate that architecture working end to end against a real external system, evidenced by Section 12's WP5 Evidence Table.

Countervailing context recorded for completeness, not as an objection: [[PST-0001_PROGRAMME_STATUS|PST-0001]] already tracks current repository state on an ongoing, accurately-maintained basis, so the incremental informational value of a new formal snapshot is more about marking a milestone than filling a gap `PST-0001` doesn't already cover.

[[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] has been drafted for review (Section 13). Per [[STD-0004_VALIDATION_QUALITY_ASSURANCE_STANDARD|STD-0004]], only the Programme Sponsor may accept a repository baseline; this recommendation does not itself constitute acceptance.

---

# 17. ESR-0016 Entry Recommendation

Per [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]]'s Lead/Reviewer rotation, ESR-0016: **ChatGPT leads, Claude reviews.**

Recommended opening focus, per the Sentinel architecture convergence discussion that preceded ESR-0015's formal opening: design the richer trust-tier policy model informed by real ESR-0015 audit evidence rather than speculative design, cross-referencing `EBG-0020` (Guardian, Family Safety and Emergency Controls) and `EBG-0021` (Local Agent Permission Boundary) for the actual consequential-action categories needed, since the trust tiers should be derived from those specs rather than invented independently.

ESR-0017 (not ESR-0016) is the designated Cold Start Validation Session per [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 3.4 - no cold-start requirement applies to ESR-0016's opening.

---

# 18. EE-0001 Trial Scorecard - ESR-0015 (Engineering Implementer Draft)

Drafted by Claude (Engineering Implementer) as a self-assessment only. Per Engineering Reviewer position, the authoritative score is completed independently by ChatGPT (Engineering Reviewer) and accepted by the Programme Sponsor - this table is an input to that process, not the final record.

| Criterion | Self-Assessment |
|---|---|
| Findings raised / accepted / rejected / false positive | 10 / 10 / 0 / 0 |
| Average defect discovery weight | 3.0 (12 defects: 1 Lead self-caught [WP2 circular import], 10 Reviewer-caught [WP1, WP3b x3, WP4 x2, WP5 script x4], 1 Sponsor-caught [WP5 live-run HTTPError ambiguity]) |
| Repeat issue prevention | Yes - WP1's mutable-default lesson was correctly applied from the start in WP2's `PolicyEngine` constructor; WP3b's "never surface raw exception detail" lesson was proactively applied in WP4 before being extended to `decision.reason` |
| Documentation-only handoff successful | Not applicable this session - Cold Start Validation is designated for ESR-0017 |
| Lead scope discipline | Met - deviations (WP2 circular import, WP5 non-execution by Claude) were reported explicitly, not absorbed silently |
| Reviewer role discipline | Met - Reviewer refined and required adjustments but did not draft alternative implementations |
| Evidence responsiveness | Met - both sides revised positions on evidence during the session (e.g. Anthropic scoring discussion, WP4/WP3 sequencing correction pre-session, model identifier uncertainty in WP5) |
| Signal-to-noise (Observations excluded) | High - all 10 Reviewer findings were substantive and accepted, none were editorial/Observation-level |
| Better converged solution achieved | Yes - WP3a's independent dual-scoring converging on OpenAI despite differing structural biases is the clearest example |
| Repository impact (multi-tag) | C (code), A (architecture), G (governance), D (documentation) |
| Sponsor arbitration required | Low - a small number of direct scope decisions (WP3a/WP3b split, WP5 execution-by-Sponsor), no extended mediation on any single point |

---

# 19. Closure Statement

ESR-0015 is closed. The session delivered the Sentinel execution pipeline in full - audit, policy, provider abstraction, a working external provider adapter, and Guardian integration - and proved it end to end with a real, live, audited, policy-gated conversation against OpenAI. Ten Engineering Reviewer findings were raised and all ten accepted, including one real defect (audit event double-counting) and one real diagnostic gap (HTTP status codes) discovered directly through live execution rather than static review alone.

[[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] is retained pending Programme Sponsor decision on [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] (Section 16). ESR-0015 closure does not itself accept a new repository baseline or create ESR-0016.

---

# 20. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0014_ENGINEERING_SESSION_REPORT|ESR-0014]] | Prior closed session; ESR-0015 continues its entry recommendation, refined through subsequent Sentinel architecture discussion. |
| [[ESR-0014A_POST_CLOSURE_ENGINEERING_ADDENDUM|ESR-0014A]] | Prior closed addendum. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Provider evaluation matrix; WP3a completed its scoring decision gate. |
| [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] | Knowledge tiering followed during this session's WP0A. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial this session operated under; scorecard drafted in Section 18. |
| [[RBL-0010_REPOSITORY_BASELINE|RBL-0010]] | Current accepted repository baseline, retained pending RBL-0011 decision. |
| [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] | Recommended repository baseline, drafted for Programme Sponsor review. |

---

# 21. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 8 July 2026 | Claude Engineering Implementer | ESR-0015 closed. Added Architectural Milestones, Executive Summary, Engineering Outcomes, Validation Summary, Repository Deliverables, Outstanding Work, Risks/Technical Debt, Repository Baseline Recommendation (RBL-0011), ESR-0016 Entry Recommendation, EE-0001 Trial Scorecard draft, and Closure Statement. 133/133 tests passing. |
| 0.6 | 8 July 2026 | Claude Engineering Implementer | WP5 complete: first live Sentinel-mediated Guardian conversation via scripts/wp5_first_conversation_demo.py, run by Programme Sponsor (not Claude - real billed external call). First attempt failed on exhausted API credit (HTTP 429); second succeeded. Evidence table recorded. Fixed sentinel/openai_provider.py to surface HTTP status codes (commit fcdec8a), motivated directly by this run's undiagnosable bare "HTTPError". 133/133 tests passing. Commits 057f40b, fcdec8a. |
| 0.5 | 8 July 2026 | Claude Engineering Implementer | WP4 complete: jarvis/interfaces/sentinel_conversation.py SentinelGatedConversationProvider routes conversation through SentinelTrustGateway and ProviderOrchestrator. Two Engineering Reviewer-required refinements applied (capability-only metadata, decision.reason never surfaced to user). First Light GUI wiring unchanged - deterministic-by-default preserved per PCB-0001. 132/132 tests passing. Commit e70c420. |
| 0.4 | 8 July 2026 | Claude Engineering Implementer | WP3a complete: PEM-001 provider scoring approved (Primary: OpenAI, Secondary: Gemini, first adapter: OpenAI direct). WP3b complete: sentinel/openai_provider.py OpenAIProvider adapter, three Engineering Reviewer-required adjustments applied (configured timeout, required default_model, controlled error wrapping). PEM-001 updated to Approved status recording the decision outcome. 127/127 tests passing. Commit a9d89fa. |
| 0.3 | 8 July 2026 | Claude Engineering Implementer | WP2 complete: sentinel/policy.py (PolicyDecision, PolicyEngine, SimpleApprovalPolicy) wired into SentinelTrustGateway, reproducing prior inline approval logic with zero behaviour change. Resolved an EIP-unanticipated circular import between core.py and policy.py via deferred import, verified empirically. 120/120 tests passing. Commit cdf283e. |
| 0.2 | 8 July 2026 | Claude Engineering Implementer | WP1 complete: sentinel/audit.py (AuditEvent, AuditRecorder, MemoryAuditRecorder, JsonAuditRecorder) wired into SentinelTrustGateway and ProviderOrchestrator. Constructor pattern corrected during Engineering Reviewer EIP review (audit_recorder: AuditRecorder \| None = None) to avoid a shared mutable default recorder. 114/114 tests passing. Commit 5733e45. |
| 0.1 | 8 July 2026 | Claude Engineering Implementer | ESR-0015 opened following WP0A/WP0B completion and Programme Sponsor approval. |
