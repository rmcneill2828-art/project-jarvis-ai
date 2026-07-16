# ESR-0023 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0023 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0023 |
| Date Opened | 16 July 2026 |
| Date Closed | 17 July 2026 |
| Closure Status | Closed - WP1-WP6 complete, session-wide WP6 Pass, WP7 RBL-0015 retained |

---

# 2. Purpose

This report records the opening and execution of ESR-0023, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex (ChatGPT) as Engineering Reviewer, Programme Sponsor gating every step.

---

# 3. Scope

ESR-0023 opened with "please read PBK-0001." WP0A/WP0B confirmed repository synchronisation (ESR-0022 closed, RBL-0015 accepted baseline). The session then addressed a Programme Sponsor-directed sweep of outstanding architecture design work: a set of quick backlog judgement calls (WP1); the entire Guardian authority/boundary cluster in JRM-0001's own horizon order - EBG-0031 (WP2), EBG-0020 (WP3), EBG-0048 (WP4); AAM-0001 identity validation, which surfaced a significant operational gap and new backlog item EBG-0074 (WP5); and a UXP diagnostics deduplication satisfying Feature-First Delivery Discipline (WP6). A repository write boundary deviation occurred during WP2's review step, a second attempt was caught and stopped during WP3, and its root cause was found and fixed the same session. Closed with session-wide WP6 Independent Repository Verification (Pass) and WP7 Repository Baseline Acceptance (RBL-0015 retained).

---

# 4. Engineering Authority

ESR-0023 opening was authorised by Programme Sponsor instruction on 16 July 2026, following repository synchronisation confirming [[ESR-0022_ENGINEERING_SESSION_REPORT|ESR-0022]] was formally closed and [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] remained the accepted repository baseline.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

No single objective was set at opening. Following a Programme Sponsor request to survey outstanding Guardian and wider architecture design work, the session's objective became: close as many quick, well-evidenced architecture backlog judgement calls as fit safely in one session (WP1), then work through the entire Guardian authority/boundary cluster in JRM-0001's own horizon order - EBG-0031 (WP2), EBG-0020 (WP3), EBG-0048 (WP4) - followed by identity validation (WP5) and, at the Programme Sponsor's request, a UXP improvement to close the session with (WP6). All objectives were met by closure.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation and session activation; PBK-0001 review | Complete - see Section 7 |
| WP1 | Architecture backlog judgement calls: EBG-0018 closed, EBG-0067 split-disposed | Complete - Section 8 |
| WP2 | MOD-0001 status currency housekeeping; GAM-0001 (Guardian Authority and Boundary Model) created and approved, resolving EBG-0031 | Complete, with a process deviation - Section 9 |
| WP3 | GAM-0001 v1.1 Section 8 (Family Safety and Emergency Controls) added, resolving EBG-0020 | Complete, with a second (prevented) deviation attempt and its root-cause fix - Section 10 |
| WP4 | GAM-0001 v1.2 Section 9 extended (consent, memory-retention consent boundary, trusted mobile approve/deny), resolving EBG-0048 | Complete - Section 11 |
| WP5 | AAM-0001 identity architecture validation and Draft to Approved promotion, resolving EBG-0041; new EBG-0074 surfaced | Complete - Section 12 |
| WP6 | UXP Diagnostics/System Health duplication removed, resolving EBG-0073 | Complete - Section 13 |
| Session-wide WP6/WP7 | Independent Repository Verification; Repository Baseline Acceptance | Complete - Pass, RBL-0015 retained - Section 14 |

---

# 7. WP0 Session Initialisation Record

**WP0A - Repository Synchronisation:**

- [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (v1.25) reviewed in full at session open.
- [[PST-0001_PROGRAMME_STATUS|PST-0001]] (v2.34) reviewed: confirmed ESR-0022 closed, [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] accepted baseline, permanent Claude Implementer / Codex (ChatGPT) Reviewer appointment in force.
- Repository state verified directly: `git status` clean, `main` up to date with `origin/main` at `9466a0f`.

**WP0B - Engineering Session Initialisation:**

- Active Engineering Session: ESR-0023 (this report, created retrospectively during WP2 at Programme Sponsor direction to record the Section 9 deviation - see Section 9).
- Repository baseline reference at opening: [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] (unchanged this session to date).
- Session objective: none set at opening - see Section 5.
- Programme Sponsor approval of WP0B session opening: given directly via the session-opening instruction.

---

# 8. WP1 - Architecture Backlog Judgement Calls

Three candidate judgement calls were identified during a Programme Sponsor-requested survey of outstanding architecture work. A Working Report was drafted, reviewed by Codex (Engineering Reviewer), and adjusted per Programme Sponsor direction before implementation - Finding 3 (MOD-0001 status currency) was withdrawn as a new backlog item and folded into WP2 instead, per Programme Sponsor judgement that it was housekeeping rather than a capability gap.

**EBG-0018 (JARVIS AI Provider Abstraction Architecture) - closed Completed.** Judged substantially satisfied by the existing Sentinel provider abstraction (`CURRENT_ARCHITECTURE.md`, ADR-0018) - execution provider abstraction, provider registry, credential reference abstraction, three provider categories with failover, backed by the live `sentinel/` implementation. Engineering Reviewer confirmed.

**EBG-0067 (Dropped ADR-0007 Topics) - promoted Candidate to Approved Backlog, split disposition.** JARVIS UI Architecture Strategy sub-topic judged Superseded (resolved by the real ADR-0007/ADR-0019). AIEMS Knowledge Architecture / relationship-vocabulary sub-topic confirmed a genuine live gap - checked directly against GDE-0001, which does not define the `implements/supports/depends_on/verifies/records/supersedes/references/relates_to/derived_from/governed_by` vocabulary approved at ESR-0006. Retained as the item's remaining scope. Engineering Reviewer confirmed.

[[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] synced to match.

- Commit SHA: `8ce4dbe`
- `python scripts/validate_repository.py`: 0 errors, 85 pre-existing warnings.

**Process note (self-caught before push):** between WP0A synchronisation and this commit, `HEAD` was found switched to a pre-existing branch (`agent/readme-baseline-update`) carrying an unrelated pushed commit from outside this session. The WP1 commit was initially made on that branch by mistake. Caught via `git log`/`git status` before pushing: cherry-picked onto `main` (final SHA `8ce4dbe`), the other branch restored to its original tip untouched, then pushed cleanly.

---

# 9. WP2 - MOD-0001 Housekeeping and GAM-0001 (Guardian Authority and Boundary Model)

**MOD-0001 (Platform Architecture Model) housekeeping, 1.4 to 1.5.** Full document read end-to-end; content confirmed still architecturally accurate against everything implemented since. `Status` corrected In Review to Approved, reflecting ESR-0011's implementation-readiness validation that was never written back into the document. Two stale `RBL-0009` "current accepted repository baseline" references corrected to `RBL-0015` (Related Artefacts, OSE Relationships), with `RBL-0009`/`RBL-0008` retained as historical lineage rows. No content rewrite. Engineering Reviewer confirmed.

**GAM-0001 (Guardian Authority and Boundary Model) - new controlled artefact, Approved v1.0.** Resolves EBG-0031 (Guardian Architecture Specification, open since ESR-0005). Evidence-gathered against AAM-0001 (identity/cognitive, explicitly conceptual), ADR-0010 (Guardian is the HITL point in principle, explicitly does not implement runtime behaviour), `CURRENT_ARCHITECTURE.md` (Sentinel's trust-tier policy model already implemented with `ROUTINE_INTERACTION`/`HUMAN_APPROVAL_REQUIRED`/`UNSUPPORTED_HIGH_RISK`/`EMERGENCY_CONTROL`/`LOCAL_AGENT_ACTION` classification categories, explicitly left as extension points for this work), and the live `jarvis/guardian/runtime.py` (confirmed minimal, no safety/permission logic implemented today).

Defines three Guardian authority levels (Autonomous / Approval-Required / Out of Scope, mapped directly onto Sentinel's existing trust-tier categories) and general protection principles, with family-safety content (EBG-0020) and HITL/consent mechanics (EBG-0048) explicitly deferred rather than restated. Structure follows the SAM-0001 house style. Engineering Reviewer confirmed the authority-level split and protection principles, and that the EBG-0020/EBG-0048/EBG-0021 deferrals do not pre-empt those items' own future scope. Programme Sponsor approved; EBG-0031 closed Completed in EBR-0001. [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] synced to match.

## 9.1 Process Deviation - Repository Write Boundary Breach

**What happened.** The WP2 change set (MOD-0001, GAM-0001, EBR-0001, JRM-0001, REG-0001) was correct in content and scope - independently verified as identical to the reviewed and approved intent. However, the resulting commit (`46aa027`, "Close WP2 architecture boundary work") was published through the Engineering Reviewer's review path rather than the Engineering Implementer's repository-execution path, landing on a new branch `agent/wp2-architecture-boundary` (pushed to its own remote) rather than `main`.

**Why this matters.** PBK-0001's Repository Lifecycle and Separation of Duties states the Engineering Reviewer "shall not perform repository implementation." This is a control-boundary failure, not a content or architecture defect - the deviation is operational and procedural.

**Correction performed.** Content verified identical to the reviewed/approved scope. The commit was cherry-picked onto `main` (final SHA `76212dc`) under the Engineering Implementer role and pushed. `validate_repository.py`: 0 errors, 85 pre-existing warnings.

**Disposition (Programme Sponsor-confirmed):**

- WP2 repository state accepted as content-correct.
- The pushed branch `agent/wp2-architecture-boundary` is retained for traceability, not deleted.
- [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0057 (Claude<->Codex Engineering Bridge) is noted as supporting evidence for this exact class of role-locked access-control failure - EBG-0057's architecture (role-locked permissions, Sponsor-stamped authorisation required before any write) is designed to prevent this by construction.
- A COC-0001/EE-0001 operating-context note on this boundary is optional, at Programme Sponsor discretion, not yet actioned. **Actioned post-WP3**: see Section 10.1 and [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7.4 - COC-0001's existing role text already states the rule unambiguously, so the addition was an EE-0001 evidentiary record, not a COC-0001 rewording.
- WP3 is held pending Programme Sponsor direction.

- Commit SHA: `76212dc` (main; supersedes the stray `46aa027` on `agent/wp2-architecture-boundary`, which remains pushed and retained per the disposition above)
- `python scripts/validate_repository.py`: 0 errors, 85 pre-existing warnings.

---

# 10. WP3 - GAM-0001 v1.1 Family Safety and Emergency Controls

**GAM-0001 (Guardian Authority and Boundary Model) v1.0 to v1.1** - new Section 8, resolving EBG-0020 (Guardian, Family Safety and Emergency Controls, open since ESR-0004's EKR-0001 vision recovery). Evidence gathered from the original ESR-0004 EKR-0001 vision-recovery findings (`aiems/History/Full Chat/FCH-0004_ESR-0004_FULL_CHAT_HISTORY.md`), confirmed absent from both AAM-0001 and PVTM-0001 before this addition - checked directly, not assumed.

Content added: a household role model (Administrator/Adult/Child/Guest, governing who may direct or approve a Guardian action, not Guardian's own classification); a child-safe assistance boundary (Child role cannot satisfy a `REVIEW` escalation); an emergency assistance scope (cameras, security monitoring, incident logging, emergency policies) bounded by the original vision's own non-destructive-without-approval principle; and a narrow pre-approved-emergency-action mechanism (explicit, named, Administrator-authored policy only) that does not soften Sentinel's `EMERGENCY_CONTROL` deny-by-default for anything not covered by such a policy. An explicit boundary against EBG-0021 (local-agent action) was also recorded.

**Review**: Engineering Reviewer (Codex) found no blocking issues - confirmed the pre-approval mechanism does not create a backdoor around Sentinel's deny-by-default, and that the Child-role restrictions are adequately conservative. One non-blocking note incorporated: the artefact now states the emergency policy record itself is subject to PBK-0001's Approval Before Change discipline, not a bypass of it. Programme Sponsor approved; EBG-0020 closed Completed in EBR-0001. [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] synced to match.

- Commit SHA: `0453623`
- `python scripts/validate_repository.py`: 0 errors, 85 pre-existing warnings.

## 10.1 Process Note - Second Write Boundary Attempt (Prevented)

Before this WP's commit, the Engineering Reviewer attempted to perform the repository write directly a second time - the same class of deviation recorded in Section 9.1. The Programme Sponsor caught and stopped it before any commit or push occurred this time; Codex acknowledged directly that it should remain in review-only mode and that the Engineering Implementer performs all repository writes.

**Significance.** A second occurrence changes this from an isolated incident to a recurring failure mode in whatever review environment or tooling access Codex is operating with. This strengthens, rather than merely offsets, the case recorded in Section 9.1 for treating [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0057 (Claude<->Codex Engineering Bridge) as more than optional supporting evidence.

**Actioned.** [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7.4 now records both incidents as post-appointment corroborating evidence, following that document's own established 7.3 precedent for logging events after the trial's formal scoring closed. COC-0001 was checked and found to already state the boundary unambiguously ("Engineering Reviewer... Does not modify the repository directly") - a third restatement there would only add accretion (the exact risk EBR-0001 EBG-0058 already flags in this project) without changing enforcement, so no COC-0001 edit was made.

No repository content was affected by this second attempt; nothing to correct beyond the record itself.

## 10.2 Root Cause Identified and Fixed - Significant Change

**GitHub branch protection ruled out.** The repository has exactly one collaborator (`rmcneill2828-art`, the Programme Sponsor's own account, confirmed via the GitHub API) - Codex has no separate GitHub identity; the stray WP2 commit (Section 9.1) was authored and committed as "Robert McNeill." A branch-protection rule restricting pushes "to the Engineering Implementer's credentials" therefore cannot technically distinguish the Programme Sponsor's own direct pushes from Codex acting through the same local credentials - this option was correctly ruled out rather than applied.

**Actual root cause found, local to the Programme Sponsor's machine, not GitHub.** Codex runs as the OpenAI Codex VS Code extension (`openai.chatgpt`), reading configuration from `C:\Users\rober\.codex\config.toml`. `codex doctor` confirmed the tool's general default is `approval policy: OnRequest` (asks before running shell commands) - but the config file carried a project-specific override:

```toml
[projects.'i:\project ai']
trust_level = "trusted"
```

This marked the current repository specifically as a trusted workspace, which is the direct mechanism that let Codex run `git add`/`git commit`/`git push` without an approval prompt on both occasions - not a comprehension gap, a permission-mode setting.

**Fix applied, with the Programme Sponsor's explicit confirmation.** The `[projects.'i:\project ai']` trust override was removed from `config.toml`. Verified via `codex doctor` that the config still parses cleanly (`config.toml parse: ok`) after the edit. This repository now falls back to Codex's general `OnRequest` approval policy - Codex must ask before running write-capable shell commands here specifically; no other project the Programme Sponsor uses Codex on is affected.

**Caveats flagged to the Programme Sponsor:** an already-running Codex session may not pick up the change until restarted; Codex will likely re-prompt to trust the folder the next time it opens this workspace, and re-approving full trust would silently undo this fix.

**Significance.** This is a genuine technical control, not a documentation restatement - it directly closes the mechanism behind both Section 9.1 and Section 10.1, superseding the "not actioned by this report" note EE-0001 Section 7.4 originally recorded for the GitHub-branch-protection option. `gh` CLI was installed (`winget install GitHub.cli`) and authenticated during this investigation, which is what made the GitHub-side collaborator check possible in the first place.

---

# 11. WP4 - GAM-0001 v1.2 Consent, Approval Mechanics and Trusted Mobile Governance

**GAM-0001 v1.1 to v1.2** - Section 9 (Approval and Escalation Path) extended with four subsections, resolving EBG-0048 (Guardian HITL Governance Specification, open since ESR-0004), per ADR-0010. Evidence checked directly: `sentinel/policy.py`'s `REVIEW` outcome is a static-message enum value only, no approval workflow implemented, confirming this remained genuinely architecture-only work.

- **9.1 Consent mechanics** - scoped to the specific action, not a standing grant; mirrors Section 7's "no silent capability expansion" principle.
- **9.2 Memory-retention consent boundary** - the section given the hardest review scrutiny: an explicit scope line against EBG-0019 (Memory and Data Storage Architecture, still open) - GAM-0001 governs whether/who-consented to retention, not storage technology, encryption, or technical retention duration.
- **9.3 Trusted mobile approve/deny** - architecture only, confirmed by ADR-0010 as a future capability; a trusted endpoint can only exercise the authority Section 8.1's household role model already grants, never more; endpoint trust itself stays Sentinel's concern.
- **9.4 Privacy boundary reinforcement** - makes Section 8.2's personal/shared-family memory distinction an explicit `HUMAN_APPROVAL_REQUIRED` gate rather than an assumed default.

**Review**: Engineering Reviewer (Codex) found no blocking issues - confirmed the Section 9.2 EBG-0019 boundary is drawn in the right place (policy/consent layer only, no pre-emption, no gap) and that Section 9.3's endpoint-trust framing is consistent with SAM-0001 and ADR-0010. Programme Sponsor approved; EBG-0048 closed Completed in EBR-0001. [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] synced to match.

- Commit SHA: `36da22d`
- `python scripts/validate_repository.py`: 0 errors, 85 pre-existing warnings.

This closed the entire Guardian authority/boundary cluster GAM-0001 was created for: EBG-0031, EBG-0020 and EBG-0048 all resolved.

---

# 12. WP5 - AAM-0001 Identity Architecture Validation

Resolves EBG-0041 (Guardian Identity Architecture Validation, open since ESR-0008). AAM-0001 re-checked in full against everything implemented since - no contradictions found, no rewrite needed.

**AAM-0001 v0.2 to v0.3** - added a second Subsequent Architectural Update note (matching the existing Sentinel/ADR-0018 pattern) pointing to GAM-0001, which operationalises AAM-0001's Judgement faculty and Guardian Relationship section. Status promoted Draft to Approved, mirroring MOD-0001's WP2 fix.

**Significant finding, not previously tracked.** Checked `sentinel/core.py` directly: `SentinelCore` defaults to `SimpleApprovalPolicy()`, not `TrustTierPolicy` - the mechanism carrying the classification categories GAM-0001's Sections 5-9 are built on. GAM-0001's policy content is architecturally complete but not operationally connected to the live Guardian runtime. Recorded as new **EBG-0074** (Wire TrustTierPolicy as SentinelCore's Production Default), Approved Backlog, High priority.

**Implementation-sequencing judgement for the seven Guardian faculties**, cross-checked against `JARVIS_CAPABILITY_READINESS_MATRIX`:

| Faculty | State |
|---|---|
| Trust | Implemented, not wired as default |
| Judgement | Architecturally defined (GAM-0001), not operationally connected |
| Reasoning | Basic/live (EBG-0070) |
| Action | Not implemented |
| Memory | Not Started |
| Voice | Not Started |
| Vision | Not Started |

Recommended order: EBG-0074 (wiring) first, then Memory (EBG-0019), then Voice/Vision, then Action (gated behind EBG-0021).

**Review**: Engineering Reviewer (Codex) confirmed Finding 2 (the wiring gap) as the most important, elevated it to High/Near-term, and adjusted the sequencing to place it explicitly ahead of Memory/Voice/Vision/Action. Programme Sponsor approved; EBG-0041 closed Completed in EBR-0001. [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] synced to match, including EBG-0074's Near-term placement.

- Commit SHA: `9e14a87`
- `python scripts/validate_repository.py`: 0 errors, 85 pre-existing warnings.

---

# 13. WP6 - UXP Diagnostics/System Health Duplication Removed

Resolves EBG-0073 (UXP Duplicate Monitoring Elements Tidy-up, flagged at ESR-0022 WP1). Also the session's only product-code change, satisfying PBK-0001's Feature-First Delivery Discipline for a session otherwise entirely governance/architecture work.

**Implementation** (option (a) of EBG-0073's three listed options): `src/platformStatus.js`'s static `diagnostics` export had its `guardian`/`sentinel`/`providers` entries removed; `src/App.jsx`'s `deriveDiagnostics()` (which existed only to re-inject live data into those rows) removed entirely; `diagnosticIcons` trimmed to match; the call site simplified to pass the static `diagnostics` list directly. `SystemHealthPanel` is now the sole owner of live Guardian/Sentinel/Providers status; `DiagnosticsPanel` shows only its four permanently-static placeholder rows (boundary, shell, agents, first-light).

**Verification, not just build-checked**: `npm run build` clean; live check via a Playwright-driven headless Chromium screenshot against the real Vite dev server confirmed `DiagnosticsPanel` renders exactly 4 rows and `SystemHealthPanel` is unaffected, zero console errors. Independently confirmed by the Programme Sponsor viewing the running dev server directly ("look much cleaner excellent"). No frontend test/snapshot files exist in this repository to check for row-count regressions (confirmed directly).

**Review**: Engineering Reviewer (Codex) found no blocking findings on the final diff. Programme Sponsor visually confirmed. EBG-0073 closed Completed in EBR-0001. [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] and [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] synced to match.

- Commit SHA: `656a573`
- `python -m pytest`: 209 passed. `python scripts/validate_repository.py`: 0 errors, 85 pre-existing warnings.

---

# 14. Session-Wide WP6/WP7 - Independent Repository Verification and Baseline Acceptance

**Handover preparation**: the Engineering Implementer prepared an [[ESR-0023_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0023 WP6 Independent Repository Verification handover]], covering all nine session commits, both write-boundary deviations and the root-cause fix, and all seven backlog closures plus EBG-0074 - deliberately leaving the retain-vs-new-baseline question open rather than presuming an answer.

**Session-wide WP6 (Independent Repository Verification)**: the Engineering Reviewer confirmed repository state on `main` (`656a573`) matches all nine commits' claims, confirmed both write-boundary disclosures (Sections 9.1, 10.1) are accurately characterised and cross-corroborated against EE-0001 Section 7.4, and confirmed validation evidence is coherent (209 passed, 0 errors, 85 warnings). **Pass.**

**Session-wide WP7 (Repository Baseline Acceptance): [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained, no new baseline.** Engineering Reviewer's independent view: no repository-baseline justification for a new baseline - WP6's diagnostics deduplication removes duplication rather than changing runtime behaviour, and EBG-0074 remains backlog-only (`SimpleApprovalPolicy` confirmed still the production default). Programme Sponsor's own determination: accept, agreeing with the Reviewer - this session's changes are governance/architecture-maturity work (the Guardian authority/boundary cluster closed, AAM-0001/MOD-0001 promoted) plus one non-behavioural UXP deduplication, materially different in kind from ESR-0022's default-provider-wiring milestone that warranted RBL-0015 itself.

---

# 15. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Governs Engineering Implementer behaviour and the Separation of Duties breached (Section 9.1) and attempted again (Section 10.1) this session; Feature-First Delivery Discipline satisfied at WP6. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0018, EBG-0031, EBG-0067, EBG-0020, EBG-0048, EBG-0041, EBG-0073 closed this session; EBG-0074 added; EBG-0057 noted as supporting evidence for Sections 9.1 and 10.1. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Synced to match EBR-0001 disposition throughout WP1-WP6. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Created at WP2 (v1.0), extended at WP3 (v1.1) and WP4 (v1.2). |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Validated and promoted to Approved (v0.3) at WP5. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Status currency housekeeping performed at WP2. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Permanent Lead/Reviewer appointment this session operates under; Section 7.4 records both write-boundary incidents and the root-cause fix. |
| [[ESR-0023_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0023-WP6]] | Session-wide Independent Repository Verification handover, Section 14. |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] | Retained as the current accepted repository baseline at Section 14. |

---

# 16. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 17 July 2026 | Claude Engineering Implementer | **Session closed.** Added WP4 (Section 11), WP5 (Section 12), WP6 (Section 13) and Session-Wide WP6/WP7 (Section 14), which had only been recorded in commit messages until now. Session-wide WP6 Independent Repository Verification: Pass (Engineering Reviewer, no blocking findings). Session-wide WP7 Repository Baseline Acceptance: [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] retained, no new baseline (Programme Sponsor accepted the Engineering Reviewer's independent recommendation). Scope and Session Objective sections updated to reflect the full session. Status Open to Closed. |
| 0.4 | 16 July 2026 | Claude Engineering Implementer | Added Section 10.2, a significant change: identified and fixed the actual root cause of both write-boundary incidents - a `trust_level = "trusted"` override for this project in Codex's local `config.toml`, which bypassed the tool's own general OnRequest approval policy. GitHub branch protection was investigated and ruled out first (single-collaborator repository, cannot distinguish identities). `gh` CLI installed and authenticated to perform the GitHub-side check. Fix applied with Programme Sponsor confirmation. EE-0001 Section 7.4 updated to match. |
| 0.3 | 16 July 2026 | Claude Engineering Implementer | Actioned Section 10.1's open question: added EE-0001 Section 7.4 (post-appointment evidentiary record of both write-boundary incidents, following the document's own 7.3 precedent). COC-0001 checked and found to already state the rule unambiguously - no edit made there. Branch protection on `main` identified as the actual technical control, flagged as a Programme Sponsor decision outside repository content. |
| 0.2 | 16 July 2026 | Claude Engineering Implementer | Added WP3 (GAM-0001 v1.1, EBG-0020 closed) and Section 10.1 (second write-boundary attempt, caught and stopped before any repository action, per Programme Sponsor direction). Session remains Open. |
| 0.1 | 16 July 2026 | Claude Engineering Implementer | Initial creation, recording WP0-WP2 and the Section 9.1 process deviation, per Programme Sponsor direction during WP2. Session remains Open; WP3 held. |
