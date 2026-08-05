# RBL-0030 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0030 |
| Title | ESR-0049 Repository Baseline (Agent Framework Phase 3: First Specialist Agent) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0049_ENGINEERING_SESSION_REPORT|ESR-0049]] |
| Previous Baseline | [[RBL-0029_REPOSITORY_BASELINE|RBL-0029]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 5 August 2026 |
| HEAD at baseline creation | `e9d2929` |

---

# 2. Purpose

RBL-0030 records the repository baseline accepted by the Programme Sponsor at ESR-0049 WP7, superseding [[RBL-0029_REPOSITORY_BASELINE|RBL-0029]]. ESR-0049 ran two Work Packages: WP1 (Documentation Debt Discipline - corrected COC-0001's stale RBL-0028 current-baseline references to RBL-0029) and WP2 (resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0119, Agent Framework Phase 3: First Specialist Agent Implementation - a genuine, live product-capability change). Guardian now has a real, working specialist-agent capability: GIA's existing read-only local resource observability is reachable as a Sentinel-gated specialist agent through the live JSON-RPC bridge, the first implementation built against the `SpecialistAgent` contract MOD-0001 scoped architecture-only at ESR-0048.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0029_REPOSITORY_BASELINE|RBL-0029]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not refreshed this session; the new Agent Framework Phase 3 capability is not yet reflected there, flagged as a documentation-staleness item for a future session's Documentation Debt sync. |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ESR-0049 remains open for further Work Packages at the Programme Sponsor's direction |

---

# 4. Baseline Recommendation Rationale

**Design review (Codex, direct `codex exec -s read-only` invocation)**: [[EIP-ESR0049-001_AGENT_FRAMEWORK_PHASE3_FIRST_SPECIALIST_AGENT|EIP-ESR0049-001]] v0.1 reviewed Pass with 2 non-blocking findings (`AgentOutcome`'s success status generalised rather than hardcoded to `"reported"`; `platform.status` summary narrowed to avoid implying local-action/automation/device-control capability) - both folded into v0.2 before implementation.

**Pre-implementation approval gate**: Programme Sponsor approval-to-implement obtained and verified via `submit-response` directly against the real Sponsor Approval Service (ESR-0049/WP2) - not merely asserted in chat - before any code was written. A first chat-only "approved" was correctly refused by the gate (no recorded decision existed yet); the second succeeded once a genuine decision was recorded.

**Post-commit review**: genuine independent Codex review of the real committed diff (`6b08690..e9d2929`) - Pass with 1 non-blocking finding (a limitation of Codex's own read-only sandbox, which could not invoke `pytest` directly and instead verified the test source directly - not a defect in the implementation).

**Session-wide WP6 Independent Repository Verification**: covering the full session range `7928626..e9d2929` (both WP1 and WP2). **Pass, no findings** - confirmed exactly the expected files changed, `GAM-0001` Section 8A and `sentinel/policy.py` untouched, the claimed 27 new tests genuinely present, and every governance-artefact claim consistent with the actual code diff. Codex's own advisory assessment: a genuine live product-capability change, recommending Establish.

**Push approval**: Programme Sponsor approval-to-push likewise obtained and verified via `submit-response` against the real Sponsor Approval Service before `git push` - the same two-step (chat-then-real-gate) pattern as the pre-implementation gate, with the same correct first-attempt refusal.

**The Programme Sponsor's determination**: **establish a new baseline**, since WP2 delivered a genuine, live product-capability change - Guardian's Agent Framework moved from architecture-only (ESR-0048) to a real, Sentinel-gated, JSON-RPC-reachable specialist-agent capability - matching the same threshold applied at RBL-0025/RBL-0027/RBL-0028/RBL-0029 rather than the Retain threshold applied at architecture/documentation-only sessions such as ESR-0048.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `jarvis/agents/contracts.py` (new) | `AgentRequest`/`AgentResult`/`SpecialistAgent` - the real contract MOD-0001 scoped architecture-only at ESR-0048, mirroring the existing Protocol-based provider contracts. |
| `jarvis/agents/gia_agent.py` (new) | `GiaObservabilityAgent`, wrapping GIA's existing read-only `LocalResourceObserver.snapshot()` as the first concrete specialist agent. |
| `jarvis/interfaces/sentinel_agent.py` (new) | `SentinelGatedAgentService`/`AgentOutcome`, mirroring `SentinelGatedConversationProvider`'s gateway-evaluate-then-proceed flow and `SpeechOutcome`/`TranscriptionOutcome`'s named-status envelope pattern. |
| `jarvis/guardian/runtime.py` | `GuardianRuntime.invoke_agent()`/`available_agents()`, mirroring `speak()`/`transcribe()`'s boundary-response discipline. |
| `jarvis/interfaces/stdio_rpc.py` | `build_default_runtime()` wires the agent service through the same shared Sentinel gateway every other capability already uses; two new RPC methods, `guardian.agent.list`/`guardian.agent.invoke`. |
| `jarvis/platform/shell.py` | "Agent Framework" capability entry corrected `PLACEHOLDER` to `AVAILABLE`, narrowly worded (one read-only agent, no local-action/automation/device-control implication). |
| `jarvis/tests/test_agents.py`, `test_sentinel_agent.py` (new), extended `test_guardian_runtime.py`/`test_stdio_rpc.py`/`test_guardian_shell.py` | 27 new tests, including a real-`TrustTierPolicy` regression confirming genuine `ROUTINE_INTERACTION` classification and a shared-gateway regression mirroring the existing speech/transcription tests. |
| [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] | WP1: stale RBL-0028 current-baseline references (Session Start Checklist, Related Artefacts, OSE Relationships) corrected to RBL-0029. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Agent Framework subsection's implementation status recorded (section text unchanged - it already described this contract correctly). |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0119 marked Completed. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not refreshed this session. The new Agent Framework Phase 3 capability is not yet reflected there - flagged as a documentation-staleness item, recommended for a future session's Documentation Debt sync alongside this baseline's own reference-pointer propagation.

---

# 7. Architecture Outcomes

- The Agent Framework moves from architecture-only (MOD-0001's subsection, ESR-0048) to a real, live capability: the first `SpecialistAgent` implementation, reachable through `GuardianRuntime` and the JSON-RPC bridge.
- The mandatory Sentinel gate MOD-0001 required is genuinely enforced in code, not merely documented - `SentinelGatedAgentService.invoke()` reuses the same shared gateway/`TrustTierPolicy` wiring every other capability (conversation, memory, speech, transcription) already relies on, confirmed by a dedicated regression test and independently re-confirmed at both Codex review passes.
- `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` boundary remains completely untouched - the one live agent classifies `ROUTINE_INTERACTION` only, and no code path in this delivery can reach the `LOCAL_AGENT_ACTION` classification.
- A second, pre-existing, ungated `gia.status` RPC method continues to expose the same underlying GIA snapshot directly (per GAM-0001 8A.1, observation was already exempt from Sentinel's request path) - this delivery adds an additional, Sentinel-gated path demonstrating the Agent Framework contract, not a replacement.
- No UXP surface exists yet for triggering an agent - the capability is real and live-reachable via RPC and honestly reflected in `platform.status`, but not yet exposed to a household member through the interface. Disclosed, not silently treated as complete.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- exactly one specialist agent (`gia-observability`), read-only, classified `ROUTINE_INTERACTION` - no other agent capability exists;
- no `LOCAL_AGENT_ACTION`-classified capability of any kind - `sentinel/policy.py` untouched, the hard `DENY` remains exactly as before;
- no UXP surface for invoking an agent - RPC/backend only;
- no change to the `SpecialistAgent` contract shape itself beyond implementing what MOD-0001 already scoped.

---

# 9. Verification

Repository validation performed across ESR-0049's Work Packages and at WP6/WP7:

- Git working tree was clean throughout; the session's content (`7928626..e9d2929`, 2 commits) pushed to `origin/main`.
- 512 Python tests passing plus 1 correctly-skipped test, up from 485/1 at RBL-0029 (27 new).
- `python scripts/validate_repository.py` (full mode): 0 errors throughout.
- Design review (Codex): v0.1 Pass with 2 non-blocking findings, folded into v0.2 before implementation.
- Post-commit review (Codex): Pass with 1 non-blocking finding (a Codex-side sandbox tooling limitation, not a defect).
- Session-wide WP6 (Codex): Pass, no findings, covering the full session diff against RBL-0029.
- Every commit gated through the real AIEMS Exchange Bridge / Sponsor Approval Service (`submit-to-review`/`return-findings`/`submit-response`) - both the pre-implementation and push approval gates correctly refused a first chat-only "approved" before a genuine recorded decision existed.
- The Programme Sponsor's own WP7 determination: establish a new baseline rather than retain RBL-0029 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0049** - the Programme Sponsor may add further Work Packages before the Engineering Session Report closure follows this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0029_REPOSITORY_BASELINE|RBL-0029]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] refresh - the new Agent Framework Phase 3 capability is not yet reflected there.
5. No UXP surface exists yet for the new agent-invocation capability - a future session could add one, or extend the Agent Framework with a second, real (non-illustrative) agent.
6. README.md's full "current session"/Capability Roadmap narrative sync is deferred to ESR-0049's eventual formal closure, matching established practice - this baseline's own reference-pointer propagation covers only the direct "current accepted repository baseline" citations, disclosed here rather than silently left inconsistent.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0029_REPOSITORY_BASELINE|RBL-0029]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0049_ENGINEERING_SESSION_REPORT|ESR-0049]] | Session this baseline is drawn from. |
| [[EIP-ESR0049-001_AGENT_FRAMEWORK_PHASE3_FIRST_SPECIALIST_AGENT|EIP-ESR0049-001]] | Approved Engineering Implementation Package this baseline's deliverables were built against. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Agent Framework subsection - the contract this baseline's deliverables implement as real code. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8A - the boundary this baseline's `ROUTINE_INTERACTION` classification stays inside, untouched. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0119 (closed this session). |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not refreshed this session, flagged for future sync. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 5 August 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0029, following Codex's design review (v0.1 Pass with 2 non-blocking findings, folded into v0.2), a verified pre-implementation approval gate, a post-commit Codex review (Pass with 1 non-blocking tooling-only finding), session-wide WP6 Independent Repository Verification (Pass, no findings), a verified push-approval gate, and the Programme Sponsor's explicit WP7 decision to cut a new baseline: WP2's real, live-verified Agent Framework Phase 3 (First Specialist Agent) delivery warrants a new baseline. |
