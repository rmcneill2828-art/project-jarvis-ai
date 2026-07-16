# ESR-0023 WP6 - Independent Repository Verification Handover

---

## 1. Document Control

| Field | Value |
|------|------|
| Artefact ID | ESR-0023-WP6 |
| Title | Independent Repository Verification Handover |
| Version | 0.3 |
| Status | Working Report - not a controlled artefact |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | [[ESR-0023_ENGINEERING_SESSION_REPORT|ESR-0023]] |
| Effective Date | 17 July 2026 |

---

## 2. Purpose

This handover prepares ESR-0023's full session-wide record (WP1-WP6, plus the Section 9.1/10.1 process deviation and its Section 10.2 root-cause fix) for WP6 Independent Repository Verification. WP6 should confirm that the repository state on `main` matches the claims made across all nine session commits, that the disclosed process deviation and its correction are accurately characterised, and that no unauthorised scope drift occurred.

---

## 3. Repository Access

| Field | Value |
|---|---|
| Repository | `https://github.com/rmcneill2828-art/project-jarvis-ai.git` |
| Branch | `main` |
| Expected `HEAD` | `656a573` |
| Confirmed | Local `HEAD` and `origin/main` both resolve to `656a573` (`git rev-parse --short HEAD` / `origin/main` after `git fetch origin main`) |
| Prior accepted baseline | `RBL-0015` |

---

## 4. Commits

Nine commits since the prior accepted baseline, in order:

| # | SHA | One-line summary |
|---|---|---|
| 1 | `8ce4dbe` | ESR-0023 WP1: close EBG-0018, split-disposition EBG-0067. |
| 2 | `76212dc` | Close WP2 architecture boundary work (GAM-0001 created v1.0, EBG-0031 closed, MOD-0001 housekeeping). |
| 3 | `d8acb3b` | ESR-0023: create session report, record WP2 write boundary deviation (Section 9.1). |
| 4 | `0453623` | ESR-0023 WP3: close EBG-0020, GAM-0001 v1.1 family safety section. |
| 5 | `d2357a5` | ESR-0023: record WP3 and second write-boundary attempt (Section 10.1). |
| 6 | `2b48697` | ESR-0023: root-cause fix for the repository write-boundary incidents (Section 10.2). |
| 7 | `36da22d` | ESR-0023 WP4: close EBG-0048, GAM-0001 v1.2 consent/approval section. |
| 8 | `9e14a87` | ESR-0023 WP5: close EBG-0041, AAM-0001 approved, new EBG-0074. |
| 9 | `656a573` | ESR-0023 WP6: close EBG-0073, remove UXP monitoring duplication. |

---

## 5. Session Observations

1. **Two repository write boundary deviations, both self-caught, one self-caught before push and one caught before it happened at all.** During WP1, `HEAD` was found switched to a pre-existing, unrelated branch (`agent/readme-baseline-update`) between session synchronisation and commit - not an action taken within this session. The WP1 commit was corrected onto `main` before pushing (Section 8 of this session's report). During WP2, a reviewed and content-correct change set was committed and pushed directly by the Engineering Reviewer (Codex), landing on a stray branch (`agent/wp2-architecture-boundary`) rather than going through the Engineering Implementer's repository-execution path - a genuine violation of PBK-0001's Separation of Duties, corrected by cherry-picking the verified-identical content onto `main` (Section 9.1). During WP3, the Engineering Reviewer attempted the identical action a second time; the Programme Sponsor caught and stopped it before any commit or push occurred (Section 10.1).
2. **Root cause found and fixed, not just documented.** GitHub branch protection was investigated and ruled out (the repository has exactly one collaborator - the Programme Sponsor's own account - so a push-restriction rule cannot distinguish the Sponsor's own pushes from Codex acting through the same local credentials). The actual root cause was a `trust_level = "trusted"` project-specific override in Codex's local `~/.codex/config.toml`, bypassing the tool's own general `OnRequest` approval policy. Removed with the Programme Sponsor's explicit confirmation and verified via `codex doctor` (Section 10.2). Both incidents are also recorded as post-appointment evidence in [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7.4.
3. **New controlled artefact created and twice extended.** [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] (Guardian Authority and Boundary Model) was created at WP2 (v1.0, resolving EBG-0031), extended at WP3 (v1.1, Section 8, resolving EBG-0020) and WP4 (v1.2, Section 9 extended, resolving EBG-0048). Each version was reviewed by the Engineering Reviewer and approved by the Programme Sponsor before the next extension began.
4. **AAM-0001 and MOD-0001 promoted Draft/In Review to Approved**, both after content re-validation against current implementation found no contradictions requiring rewrite (WP2 for MOD-0001, WP5 for AAM-0001).
5. **A significant operational gap surfaced by WP5's validation, not implemented, tracked as new backlog.** Checking `sentinel/core.py` directly confirmed `SimpleApprovalPolicy` remains `SentinelCore`'s production default; `TrustTierPolicy` (the mechanism GAM-0001's Sections 5-9 classification model depends on) remains additive/opt-in only. GAM-0001's policy content is architecturally complete but not yet operationally connected to the live Guardian runtime. Recorded as EBG-0074 (Approved Backlog, High priority), Engineering Reviewer-endorsed as urgent and sequenced ahead of Memory/Voice/Vision/Action work in JRM-0001 Track B.
6. **One product-code change, the session's only source-code commit.** WP6 removed `DiagnosticsPanel`'s duplicate Guardian/Sentinel/Providers rows (`src/App.jsx`, `src/platformStatus.js`), resolving EBG-0073. Verified via a live Playwright-driven headless Chromium check against the real Vite dev server (confirmed exactly 4 diagnostic rows, zero console errors) and independently confirmed by the Programme Sponsor viewing the running dev server directly. This satisfies PBK-0001's Feature-First Delivery Discipline for a session that was otherwise entirely governance/architecture work.
7. **Seven backlog items closed, one new item opened.** EBG-0018, EBG-0067, EBG-0031, EBG-0020, EBG-0048, EBG-0041 and EBG-0073 all marked Completed in EBR-0001; EBG-0074 added as new Approved Backlog.

---

## 6. Validation Evidence

Validation re-run immediately before this handover:

| Check | Result |
|---|---|
| `python -m pytest` | 209 passed |
| `python scripts/validate_repository.py` (full mode, not `--governance-only` - this session's changes include source code) | Passed, 0 errors, 85 warnings |
| `npm run build` | Clean (performed at WP6) |
| `git rev-parse --short HEAD` | `656a573` |
| `git rev-parse --short origin/main` | `656a573` |
| `git status --short` | Clean (captured before this handover file itself was added to the workspace) |

The 85 warnings are the same pre-existing, non-blocking set present at every prior session's closure (unchanged count throughout this session).

---

## 7. Scope Check

- No changes to `scripts/validate_repository.py`.
- No changes to Sentinel enforcement code, the trust-tier classifier, or `SentinelCore`'s default policy - EBG-0074 (the wiring gap WP5 surfaced) is recorded as backlog only, not implemented.
- No family-safety, HITL or consent *mechanics* were implemented in code - GAM-0001's Sections 8-9 remain architecture-only, as each version's own Explicit Non-Goals states.
- The only source-code change this session is WP6's `src/App.jsx` / `src/platformStatus.js` diagnostics-deduplication, matching EBG-0073's approved scope exactly (option (a) of three listed options; options (b)/(c) explicitly not actioned).
- The stray branches `agent/readme-baseline-update` and `agent/wp2-architecture-boundary` were not deleted or force-updated - both retained for traceability per their respective dispositions (Section 8 and Section 9.1 of the session report).

---

## 8. WP7 Baseline Recommendation

Flagged for the Engineering Reviewer's and Programme Sponsor's own judgement, not pre-decided here, following the ESR-0022 precedent of leaving this question genuinely open:

**Case for retaining RBL-0015:** no Sentinel enforcement, runtime behaviour, or production code path changed - `TrustTierPolicy` remains unwired, exactly as it was at RBL-0015's acceptance. The one UXP change (WP6) is a pure removal of duplicate presentation, not new capability. GAM-0001/AAM-0001 are new/promoted *governance* artefacts (policy-only, explicitly not implementing enforcement), closer in kind to ESR-0020/ESR-0021's incremental sessions than to ESR-0022's default-provider-wiring milestone.

**Case for a new baseline:** this session closed seven backlog items including the entire Guardian authority/boundary architecture cluster (EBG-0031/0020/0048/0041) that has been open since ESR-0005/ESR-0008 - a substantial governance-maturity milestone even without a runtime behaviour change. It also surfaced and fixed a genuine security-relevant gap (the write-boundary root cause) affecting how future sessions are safely conducted.

No recommendation is asserted either way in this handover; Section 9 below asks the Engineering Reviewer to form an independent view.

**Engineering Reviewer WP6 verification: Pass.** No blocking findings - repository state on `main` confirmed consistent with all nine commits (Section 4), both write-boundary disclosures confirmed accurate and cross-corroborated against EE-0001 Section 7.4, validation evidence confirmed coherent (209 passed, 0 errors, 85 warnings, `656a573` on both `HEAD` and `origin/main`).

**Engineering Reviewer's independent baseline view: retain RBL-0015.** No repository-baseline justification for a new baseline - WP6's diagnostics deduplication removes duplication rather than changing runtime behaviour, and EBG-0074 is backlog-only (`SimpleApprovalPolicy` remains the confirmed production default; the operational gap is real but not yet baseline-changing).

**Resolved.** Programme Sponsor's own WP7 determination: accept, retaining RBL-0015 - no new baseline. Agrees with the Engineering Reviewer's independent view: this session's changes are governance/architecture-maturity work (Guardian authority/boundary cluster closed, AAM-0001/MOD-0001 promoted) plus one non-behavioural UXP deduplication, not a runtime capability change - a materially different kind of session from ESR-0022's default-provider-wiring milestone. RBL-0015 remains the current accepted repository baseline.

---

## 9. What WP6 Should Produce

WP6 should produce:

1. Confirmation that the repository state on `main` matches the claims made across all nine commits listed in Section 4.
2. Confirmation that both process-deviation disclosures (Section 5, items 1-2) are accurately characterised - in particular, that the stray branches contain no content divergence from what was actually reviewed and approved, and that the root-cause fix (Section 10.2 of the session report) is correctly described.
3. An independent view on Section 8's open question: retain `RBL-0015` or recommend a new baseline.
4. A recommendation to the Programme Sponsor on WP7 closure.

---

## 10. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | New controlled artefact created and twice extended this session. |
| [[AAM-0001_GUARDIAN_IDENTITY_AND_COGNITIVE_ARCHITECTURE|AAM-0001]] | Promoted Draft to Approved at WP5. |
| [[MOD-0001_PLATFORM_ARCHITECTURE_MODEL|MOD-0001]] | Promoted In Review to Approved at WP2. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Section 7.4 records both write-boundary incidents and the root-cause fix. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Roadmap sequencing used throughout; updated to reflect all closures and EBG-0074. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Seven items closed, one new item (EBG-0074) added. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Traceability register updated for every session change. |
| [[RBL-0015_REPOSITORY_BASELINE|RBL-0015]] | Prior accepted baseline. |

---

## 11. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.3 | 17 July 2026 | Claude Engineering Implementer | Recorded Programme Sponsor's WP7 determination: accept, retaining RBL-0015 - no new baseline. |
| 0.2 | 17 July 2026 | Claude Engineering Implementer | Recorded Engineering Reviewer (Codex) WP6 verification: Pass, no blocking findings. Recorded independent baseline recommendation: retain RBL-0015. Applied minor precision note on `git status --short` evidence timing. Pending Programme Sponsor's own WP7 determination. |
| 0.1 | 17 July 2026 | Claude Engineering Implementer | Drafted WP6 Independent Repository Verification handover for ESR-0023: records all nine session commits, validation evidence, both disclosed process deviations and the root-cause fix, seven backlog closures plus one new item, and an open (not pre-decided) WP7 baseline question for the Engineering Reviewer. |
