# ESR-0024 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0024 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0024 |
| Date Opened | 17 July 2026 |
| Date Closed | 17 July 2026 |
| Closure Status | Closed - WP1-WP2 complete, session-wide WP6 Pass, WP7 RBL-0015 retained |

---

# 2. Purpose

This report records the opening and execution of ESR-0024, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex (ChatGPT) as Engineering Reviewer, Programme Sponsor gating every step.

---

# 3. Scope

ESR-0024 opened with "please read PBK-0001," mirroring ESR-0023's own opening. WP0A/WP0B confirmed repository synchronisation (ESR-0023 closed, RBL-0015 accepted baseline) and, at the Programme Sponsor's direction, selected [[JRM-0001_PROJECT_ROADMAP|JRM-0001]]'s leading Near-term candidate as the session objective. WP1 wired `TrustTierPolicy` into the production runtime, closing EBG-0074. WP2, prompted directly by the Programme Sponsor citing PBK-0001's Feature-First Delivery Discipline, delivered a small Incremental Visual Convergence increment - the System Health panel's Sentinel row now names the live-connected policy engine. Both Work Packages followed the same Working Report Lifecycle: Engineering Implementer drafts an Engineering Implementation Package, Engineering Reviewer reviews it, Programme Sponsor approves, Engineering Implementer implements exactly as scoped. Closed with session-wide WP6 Independent Repository Verification (Pass) and WP7 Repository Baseline Acceptance (RBL-0015 retained).

---

# 4. Engineering Authority

ESR-0024 opening was authorised by Programme Sponsor instruction on 17 July 2026, following repository synchronisation confirming [[ESR-0023_ENGINEERING_SESSION_REPORT|ESR-0023]] was formally closed and [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] remained the accepted repository baseline.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

No single objective was set at opening. Following WP0A/WP0B repository synchronisation, the Programme Sponsor was offered a choice of Near-term candidates from JRM-0001 and selected **EBG-0074** (wiring `TrustTierPolicy` as `SentinelCore`'s production default) - JRM-0001's top-ranked candidate, Engineering Reviewer-endorsed as urgent at ESR-0023 WP5. WP2's objective - a small Incremental Visual Convergence increment - was added mid-session at the Programme Sponsor's direct prompt, citing PBK-0001's Feature-First Delivery Discipline. Both objectives were met by closure.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation and session activation; PBK-0001 review | Complete - see Section 7 |
| WP1 | Wired `TrustTierPolicy` into `build_default_runtime()`, closing EBG-0074 | Complete - Section 8 |
| WP2 | System Health Sentinel row names the live policy engine, satisfying Incremental Visual Convergence | Complete - Section 9 |
| Session-wide WP6/WP7 | Independent Repository Verification; Repository Baseline Acceptance | Complete - Pass, RBL-0015 retained - Section 10 |

---

# 7. WP0 Session Initialisation Record

**WP0A - Repository Synchronisation:**

- [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (v1.26) reviewed in full at session open.
- [[PST-0001_PROGRAMME_STATUS|PST-0001]] (v2.35) reviewed: confirmed ESR-0023 closed, [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] accepted baseline, permanent Claude Implementer / Codex (ChatGPT) Reviewer appointment in force.
- Repository state verified directly: `git status` clean, `main` at `317dd69`, `core.hooksPath` confirmed set to `scripts/hooks`.

**WP0B - Engineering Session Initialisation:**

- Active Engineering Session: ESR-0024 (this report, authored at closure per the practice established at ESR-0022/ESR-0023).
- Repository baseline reference at opening: [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] (unchanged this session).
- Session objective: EBG-0074, selected by the Programme Sponsor from JRM-0001's Near-term candidates after WP0A/WP0B synchronisation - see Section 5.
- Programme Sponsor approval of WP0B session opening: given directly via the session-opening instruction and the subsequent objective selection.

---

# 8. WP1 - TrustTierPolicy Production Wiring (EBG-0074)

Resolves EBG-0074 (Wire TrustTierPolicy as SentinelCore's Production Default, discovered at ESR-0023 WP5). A Working Report / Engineering Implementation Package ([[EIP-ESR0024-001_TRUSTTIERPOLICY_PRODUCTION_WIRING|EIP-ESR0024-001]]) was drafted, reviewed by Codex (Engineering Reviewer), and revised once before approval.

**v0.1 to v0.2 (Engineering Reviewer findings, both addressed):** (1) the drafted `gateway`/`sentinel_gateway()` accessors returned only the gateway object, not the policy engine, leaving no way to confirm the wired type without reaching into the private `_policy_engine` field or inferring from behaviour (identical under either policy for the fixed conversation request shape) - added a `policy_engine` property to `SentinelTrustGateway`; (2) a proposed five-case category-classification test matrix would have duplicated existing `TrustTierPolicy` coverage (`jarvis/tests/test_sentinel_policy.py`) without exercising the production path - trimmed to one wiring assertion plus one unchanged-`guardian.converse` regression test.

**Implementation.** `jarvis/interfaces/stdio_rpc.py`'s `build_default_runtime()` now constructs `SentinelTrustGateway(policy_engine=TrustTierPolicy())`, replacing the class default `SimpleApprovalPolicy()` for the one runtime object the live UXP actually runs. `SentinelTrustGateway`'s own class-level default (`sentinel/core.py`) is deliberately left unchanged, confining the change's blast radius away from the many existing tests/scripts that construct a bare gateway elsewhere. New `policy_engine` (`SentinelTrustGateway`), `gateway` (`SentinelGatedConversationProvider`) and `sentinel_gateway()` (`GuardianRuntime`) accessors let a new test assert `isinstance(runtime.sentinel_gateway().policy_engine, TrustTierPolicy)` directly against the production construction path. A second test evaluates the real conversation request shape through the wired gateway and confirms `ALLOW`/`ROUTINE`/`ROUTINE_INTERACTION`, distinct from the plain RPC-response duplicate the EIP's literal text described - a disclosed, self-reviewed refinement recorded in the EIP's own v1.0 approval section, since a byte-for-byte duplicate of the existing `test_guardian_converse_returns_real_response_through_sentinel` would have added no incremental protection.

No production call site yet varies request shape per Guardian action (Action faculty remains Not Started, gated behind EBG-0021), so this wiring closes the "operationally inert" gap in the classification-wiring sense without yet producing an observable behaviour change in the live conversation path.

**Review**: Engineering Reviewer (Codex) approved v0.2 with no further findings. Programme Sponsor approved implementation. EBG-0074 closed Complete in EBR-0001. [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] synced to match.

- Commit SHA: `82ea244`
- `python -m pytest`: 211 passed (was 209). `python scripts/validate_repository.py`: 0 errors, 102 pre-existing warnings (corrected from a stale "85" figure carried in PST-0001 since ESR-0022; confirmed via `git stash` comparison against clean `main` to be pre-existing and unrelated to this session's changes).

---

# 9. WP2 - System Health Policy Engine Detail (Incremental Visual Convergence)

Following WP1's closure, the Programme Sponsor prompted a check against PBK-0001's Feature-First Delivery Discipline, noting the session had so far delivered backend-only work. Reviewing `aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg` (the reference mock-up) and the live UXP together surfaced a natural, small increment directly tied to WP1's own delivered capability: the System Health panel's Sentinel row could now honestly name which policy engine actually governs the connected gateway, a fact that did not exist before this session.

A Working Report / Engineering Implementation Package ([[EIP-ESR0024-002_SYSTEM_HEALTH_POLICY_ENGINE_DETAIL|EIP-ESR0024-002]]) was drafted, reviewed by Codex, and approved with no blocking findings.

**Implementation.** `jarvis/interfaces/stdio_rpc.py`'s `_platform_status` adds a `policyEngine` field (`type(gateway.policy_engine).__name__` via the WP1-added `sentinel_gateway()` accessor, `None` if no gateway is connected). `src/App.jsx`'s `deriveSystemHealth()` Sentinel row now reads e.g. "Trust gateway active (TrustTierPolicy)" when running, falling back to the prior unqualified text if the field is ever absent. No other row or panel changed; no mock-up fields (`MODE`/`CONFIDENCE`/`AUTONOMY`/`PERMISSION`) were invented, since Guardian does not compute any of those concepts today and doing so would have violated the no-mock-fallback rule.

**Verification, not just build-checked**: `npm run build` clean; a Playwright-driven check against the real Vite dev server (mocking `window.__TAURI_INTERNALS__.invoke`, no live backend) confirmed the Sentinel row's connecting ("Connecting to the JARVIS backend..."), offline ("JARVIS backend is unavailable") and running ("Trust gateway active (TrustTierPolicy)") states all render honestly, zero console errors in every state. Playwright itself was found missing from `node_modules` despite being declared in `package.json` and had to be installed (`npm install`) before this check could run.

**Review**: Engineering Reviewer (Codex) reviewed the design with no blocking findings, noting one residual risk - verification depends on a manual Playwright check rather than automated UI test infrastructure, which does not exist anywhere in this repository (confirmed at ESR-0023 WP6) - accepted as pre-existing and out of this package's scope, flagged as a possible future backlog candidate at the Programme Sponsor's discretion. Codex separately reviewed the implemented diff post-hoc with no blocking findings, recording one further residual risk: `policyEngine` is now part of the `platform.status` RPC contract, so a future `TrustTierPolicy` rename would be a user-visible change, not merely internal - accepted, not actioned. Programme Sponsor approved implementation. [[PST-0001_PROGRAMME_STATUS|PST-0001]] and [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] synced to match.

- Commit SHA: `8e45ff8`
- `python -m pytest`: 212 passed. `python scripts/validate_repository.py`: 0 errors, 102 pre-existing warnings. `npm run build`: clean.

## 9.1 Process Note - Overly Broad Process Termination

While stopping the Vite dev server used for WP2's Playwright verification, the Engineering Implementer ran `taskkill /IM node.exe /T`, which terminates every `node.exe` process on the host machine, not only the one dev server started for this check. This was broader than intended - the correct action would have been to target the specific PID. Self-disclosed to the Programme Sponsor immediately; no adverse effect was reported. Recorded here as a process note for future sessions: prefer PID-targeted process termination over blanket `/IM` kills on a shared development machine.

---

# 10. Session-Wide WP6/WP7 - Independent Repository Verification and Baseline Acceptance

**Handover preparation**: an [[ESR-0024_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0024 WP6 Independent Repository Verification handover]] was prepared covering both session commits, validation evidence and scope boundaries, deliberately leaving the retain-vs-new-baseline question open. The Engineering Implementer's own review of the drafted handover found one defect before it was passed to the Reviewer: the handover's `Parent` field wikilinked to `ESR-0024_ENGINEERING_SESSION_REPORT`, which did not yet exist at that point (this report is authored at closure, per established practice) - corrected to plain text, `validate_repository.py` confirmed clean afterward.

**Session-wide WP6 (Independent Repository Verification)**: the Engineering Reviewer confirmed repository state on `main` (`8e45ff8`) matches both commits' claims, confirmed scope boundaries as accurately characterised (WP1 changed runtime wiring, WP2 displayed the live policy engine honestly, neither altered the trust-tier logic itself), and confirmed validation evidence is coherent (212 passed, 0 errors, 102 warnings, `8e45ff8` on both `HEAD` and `origin/main`, clean build). **Pass.**

**Session-wide WP7 (Repository Baseline Acceptance): [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained, no new baseline.** Engineering Reviewer's independent view: retain - WP2 is presentation-only, and WP1, while operationally important, stays scoped to the existing runtime path rather than broadening the baseline the way ESR-0022's provider wiring did. Engineering Implementer's own view, offered independently before the Programme Sponsor's determination, agreed on the same grounds. Programme Sponsor's own determination: accept, retaining RBL-0015, agreeing with both independent views - WP1's `TrustTierPolicy` wiring stays within the existing runtime path (no new production call site, no observable behaviour change for the live conversation flow) and WP2 is a pure presentation update, materially different in kind from ESR-0022's default-provider-wiring milestone that warranted RBL-0015 itself.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Governs Engineering Implementer behaviour; Feature-First Delivery Discipline and Incremental Visual Convergence practice satisfied at WP2. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0074 closed this session. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | EBG-0074 annotated resolved; EBG-0019's rationale updated to reflect it as landed. |
| [[EIP-ESR0024-001_TRUSTTIERPOLICY_PRODUCTION_WIRING|EIP-ESR0024-001]] | Approved implementation package for WP1. |
| [[EIP-ESR0024-002_SYSTEM_HEALTH_POLICY_ENGINE_DETAIL|EIP-ESR0024-002]] | Approved implementation package for WP2. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Permanent Lead/Reviewer appointment this session operates under. |
| [[ESR-0024_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0024-WP6]] | Session-wide Independent Repository Verification handover, Section 10. |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] | Retained as the current accepted repository baseline at Section 10. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 17 July 2026 | Claude Engineering Implementer | Initial creation and closure, authored at session close per the practice established at ESR-0022/ESR-0023. Records WP0-WP2, the session-wide WP6 Independent Repository Verification (Pass) and WP7 Repository Baseline Acceptance (RBL-0015 retained). Status Open to Closed. |
