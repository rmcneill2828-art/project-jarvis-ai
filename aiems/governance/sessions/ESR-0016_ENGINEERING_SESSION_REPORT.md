# ESR-0016 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0016 |
| Title | Engineering Session Report |
| Version | 0.2 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Session | ESR-0016 |
| Date Opened | 8 July 2026 |
| Date Closed | - |
| Closure Status | Open |
| Final Validation | 144 / 144 tests passing (as of WP1) |

---

# 2. Purpose

This report records the opening and execution of ESR-0016 as it happens.

ESR-0016 is the second Engineering Session run under the [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Lead/Reviewer trial: ChatGPT as Engineering Lead, Claude as Independent Reviewer, Programme Sponsor gating every step.

**Authorship note:** unlike prior session reports (authored by whichever AI held the Engineering Implementer/Lead role that session), this report is maintained by the Engineering Reviewer (Claude), not the Engineering Lead (ChatGPT). This is an explicit Programme Sponsor decision recorded on 9 July 2026, made because ChatGPT operates through ChatGPT Desktop with metered, slow GitHub connector access, making incremental repository documentation costly for it, whereas Claude has direct, low-cost repository access and is already independently verifying each work package as part of Reviewer duties. WP0 and WP1 below are backfilled from ChatGPT's session transcript, with every factual claim (commit SHAs, test results, code behaviour) independently re-verified against the repository rather than taken from the transcript at face value.

---

# 3. Scope

ESR-0016 designs and implements a richer Sentinel trust-tier policy model, informed by real ESR-0015 audit evidence, cross-referencing `EBG-0020` (Guardian, Family Safety and Emergency Controls), `EBG-0021` (Local Agent Permission Boundary) and `EBG-0047` (Sentinel trust gateway, trust tiers and platform-entry validation).

---

# 4. Engineering Authority

ESR-0016 opening was authorised by Programme Sponsor approval of WP0B on 8 July 2026, following WP0A Repository Synchronisation confirming [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] was formally closed and [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] accepted.

WP1 (Sentinel trust-tier policy model) was authorised by Programme Sponsor approval of the Engineering Lead's revised Engineering Implementation Package, following Engineering Reviewer (Claude) review and requested refinements.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Design and implement the richer Sentinel trust-tier policy model, using the existing `PolicyEngine` seam, while preserving current `SentinelTrustGateway` behaviour and avoiding Guardian Memory, automation, local-agent execution or UI scope.

**Outcome (in progress):** WP1 achieved and independently verified. WP2 (SAM-0001 architecture alignment) not yet started.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation and session activation | Complete |
| WP1 | Sentinel trust-tier policy model (`TrustTier`, `TrustCategory`, `TrustTierPolicy`), additive to `PolicyEngine`, `SimpleApprovalPolicy` retained as production default | Complete (commits `598c13a`, `50029d1`, `d08f9b4`, `a5b6406`, `b4ba22d`) |
| WP2 | Update [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] to describe the implemented trust-tier model | Not started - agreed as a same-session follow-up after WP1 code review, per Engineering Lead/Reviewer sequencing agreement |

The Engineering Lead originally proposed bundling a SAM-0001 update into WP1 itself. The Engineering Reviewer recommended sequencing it as a separate WP2 after WP1's implementation stabilised, on the basis that architecture documentation should describe implemented and validated behaviour rather than a design that might still shift during implementation (consistent with how [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] and [[ADR-0018_SENTINEL_AI_EXECUTION_SECURITY_PLATFORM|ADR-0018]] were updated after ESR-0014/0015's real decisions existed, not ahead of them). The Engineering Lead agreed; this sequencing was formally adopted.

---

# 7. Architectural Milestones

- First trust-tier classification model for Sentinel policy decisions (`TrustTier`: routine/sensitive/restricted).
- First additive `PolicyEngine` implementation alongside `SimpleApprovalPolicy` - proves the seam introduced in ESR-0015 WP2 supports extension without replacing existing behaviour.
- First explicit precedence ordering for policy outcomes (deny-worthy categories checked before `requires_approval`, established only after a review-caught defect - see Section 9).

---

# 8. Executive Summary

WP1 extended `sentinel/policy.py` with a `TrustTierPolicy` that classifies Sentinel requests into forward-compatible trust categories (routine interaction, human-approval-required, emergency control, local-agent action, unsupported high risk) and maps them to ALLOW/REVIEW/DENY outcomes, without changing `SentinelTrustGateway`'s default (`SimpleApprovalPolicy` remains the production policy; the new engine is additive and unwired).

The work was proposed as an EIP, refined once during Engineering Reviewer pre-implementation review (EBG-0020/0021 grounding honesty, SAM-0001 sequencing, explicit Success Criteria, a hard constraint that the production default must not change), then implemented on a feature branch (`esr-0016-wp1-trust-tier-policy`) rather than directly on `main`, on Engineering Reviewer recommendation, so validation could happen before merge.

Two full review cycles followed:

- **Review 1** found one confirmed correctness defect (`classify()` let `requires_approval=True` downgrade a deny-worthy category to REVIEW instead of DENY - a real security-relevant bug, since it meant a caller could soften a hard boundary just by also flagging approval) and two scope gaps (missing package exports, no tests at all despite the EIP requiring them).
- **Review 2**, after the defect fix and initial test commit, found the test commit had a **pytest collection error** (`request` collides with pytest's reserved fixture name), which is a blocking severity, not cosmetic - it meant the entire suite (all 136 previously-passing tests) failed to execute at all, not just the new tests.

Both were fixed on the same feature branch and re-reviewed clean. The branch was then fast-forward merged to `main` (no merge commit) once the Engineering Reviewer confirmed no outstanding findings.

---

# 9. Engineering Outcomes

1. Added `TrustTier` (routine/sensitive/restricted) and `TrustCategory` (routine_interaction/human_approval_required/emergency_control/local_agent_action/unsupported_high_risk) to `sentinel/policy.py`.
2. Added `TrustTierPolicy`, implementing `PolicyEngine`, classifying `SentinelRequest`s using existing fields only (`source`, `intent`, `payload_type`, `requires_approval`, `metadata`) - no new request fields required.
3. Confirmed `SentinelTrustGateway.__init__`'s default (`self._policy_engine = policy_engine or SimpleApprovalPolicy()`) is the only production construction site for a `PolicyEngine`; `TrustTierPolicy` is not wired there, so existing callers are provably unaffected.
4. Found and fixed a classification-precedence defect: `classify()` originally checked `requires_approval` before deny-worthy categories, allowing a caller to downgrade `UNSUPPORTED_HIGH_RISK`/`EMERGENCY_CONTROL`/`LOCAL_AGENT_ACTION` requests from DENY to REVIEW simply by also setting `requires_approval=True`. Corrected precedence order: unsupported-high-risk, then emergency-control, then local-agent, then requires-approval, then routine allow - documented inline in `classify()`.
5. Exported `TrustTier`, `TrustCategory`, `TrustTierPolicy` from `sentinel/__init__.py`, matching the established pattern that every public Sentinel policy type is re-exported at package level.
6. Added trust-tier test coverage: one ALLOW case, one REVIEW case, one DENY case per restricted category, and a dedicated precedence-regression test proving `requires_approval=True` combined with each deny-worthy category still produces DENY - the permanent guard against the defect in outcome 4.
7. Found and fixed a pytest collection error in the first test commit (`request` parametrize argument name collided with pytest's reserved `request` fixture, aborting collection of the entire suite) by renaming to `sentinel_request` throughout - a test-only change, no production code touched.
8. Preserved `SimpleApprovalPolicy` as `SentinelTrustGateway`'s production default throughout; zero regressions to any pre-existing Sentinel test.

---

# 10. Validation Summary

| Checkpoint | Commit | Tests Collected | Result |
|---|---|---:|---|
| RBL-0011 baseline (ESR-0015 close) | `c51f95e` | 136 | 136 passing |
| WP1: policy model implemented | `598c13a` | 136 | unchanged (no tests yet) |
| WP1: precedence defect fixed | `50029d1` | 136 | unchanged (no tests yet) |
| WP1: package exports added | `d08f9b4` | 136 | unchanged (no tests yet) |
| WP1: tests added (first attempt) | `a5b6406` | 130 collected, 1 collection error | **Blocking - full suite failed to execute** (`Interrupted: 1 error during collection`) |
| WP1: parametrize rename fix | `b4ba22d` (current `main`) | 144 | **144 / 144 passing** |

All checkpoint counts independently re-run against the actual repository (`git checkout <commit>`, `pytest`/`pytest --collect-only`), not taken from the Engineering Lead's or Engineering Reviewer's self-reported figures. The `a5b6406` collection-error row is verified to be a full-suite abort, not a partial failure: running plain `pytest` (not `--collect-only`) at that commit produces zero executed tests and `Interrupted: 1 error during collection`.

`python scripts/validate_repository.py` and the pre-existing, unrelated `ruff` finding in `sentinel/orchestrator.py` were reported clean/unchanged throughout WP1 per the Engineering Lead and Engineering Reviewer; not independently re-run at every checkpoint for this backfill entry.

---

# 11. WP0 Session Initialisation Record

WP0A Repository Synchronisation (Engineering Lead) confirmed via GitHub connector: repository `rmcneill2828-art/project-jarvis-ai`, default branch `main`, [[PST-0001_PROGRAMME_STATUS|PST-0001]] state (ESR-0015 closed, [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] accepted, no active session), [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] tiers, [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]], [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]].

WP0B confirmed: session identifier ESR-0016, Engineering Lead ChatGPT, Independent Reviewer Claude, baseline RBL-0011, objective as Section 5, Programme Sponsor approval obtained 8 July 2026.

---

# 12. Repository Deliverables

## Code

- `sentinel/policy.py` (amended: `TrustTier`, `TrustCategory`, `TrustTierPolicy` added; `SimpleApprovalPolicy` unchanged)
- `sentinel/__init__.py` (amended: exports)

## Tests

- `jarvis/tests/test_sentinel_policy.py` (amended: trust-tier ALLOW/REVIEW/DENY cases and precedence-regression test added)

## Governance

- [[ESR-0016_ENGINEERING_SESSION_REPORT|ESR-0016]] (this report)

---

# 13. Outstanding Work

- WP2 - [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] architecture alignment: document the implemented trust-tier model (tier names, classification approach, outcome semantics, precedence rule, extension points), cross-referencing `EBG-0047` and forward-looking references to `EBG-0020`/`EBG-0021`. Not started.
- README.md is stale relative to current programme state (still describes ESR-0013/RBL-0010) - flagged during ESR-0016 pre-session review as an observation, not yet actioned. Out of ESR-0016's approved scope unless the Programme Sponsor directs otherwise.
- This report itself is not yet registered in [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] - deferred until session closure, consistent with when prior ESR reports were typically registered.

---

# 14. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Lead/Reviewer trial this session operates under. |
| [[ESR-0015_ENGINEERING_SESSION_REPORT|ESR-0015]] | Prior closed session; ESR-0016 continues its ESR-0016 Entry Recommendation (Section 17). |
| [[RBL-0011_REPOSITORY_BASELINE|RBL-0011]] | Current accepted repository baseline this session builds on. |
| [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] | Knowledge tiering followed during this session's WP0A. |
| [[SAM-0001_SENTINEL_TRUST_ARCHITECTURE|SAM-0001]] | Target of WP2, not yet updated. |
| [[PEM-001_AI_PROVIDER_EVALUATION_MATRIX|PEM-001]] | Precedent for documenting implemented (not prospective) architecture, referenced in WP2 sequencing rationale. |

---

# 15. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.1 | 8 July 2026 | ChatGPT Engineering Lead | ESR-0016 opened following WP0A/WP0B and Programme Sponsor approval. (Recorded retrospectively - see 0.2.) |
| 0.2 | 9 July 2026 | Claude Engineering Reviewer | Backfilled WP0 and WP1 from the Engineering Lead's session transcript, with every factual claim independently re-verified against the repository (commit contents, checkpoint-by-checkpoint test counts, the `a5b6406` collection-failure behaviour). Report authorship taken on by the Engineering Reviewer for this session per explicit Programme Sponsor decision, due to the Engineering Lead's metered/slow GitHub connector access. Not yet registered in REG-0001; not yet committed to the repository pending Programme Sponsor confirmation. |
