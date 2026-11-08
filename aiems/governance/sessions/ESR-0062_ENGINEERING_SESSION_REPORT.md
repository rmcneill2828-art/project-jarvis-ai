# ESR-0062 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0062 |
| Title | Engineering Session Report |
| Version | 0.3 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0062 |
| Date Opened | 8 November 2026 |
| Date Closed | - |
| Closure Status | Open - Session B of the go-live plan |

---

# 2. Purpose

This report records the opening of ESR-0062, at the Programme Sponsor's direct request ("Please start next session"), following ESR-0061's formal closure and the establishment of [[RBL-0041_REPOSITORY_BASELINE|RBL-0041]].

ESR-0062 is **Session B** of the go-live plan in [[WR-ESR0061-001_GO_LIVE_READINESS_REVIEW_AND_WORK_PACKAGE_PLAN|WR-ESR0061-001]]. It takes up the items [[ESR-0061_ENGINEERING_SESSION_REPORT|ESR-0061]] Section 6A carried forward, ordered around Mac visit 1 (the new Mac, about 21 November 2026): work that must be checked on a real Mac is built before the visit.

WP0A/WP0B session initialisation followed PBK-0001 and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]].

---

# 3. Scope

| WP | Record |
|----|--------|
| **WP0A - Repository Synchronisation (Complete)** | Working tree clean at open. HEAD `8a40497` (ESR-0061 WP8, RBL-0041), **one commit ahead of `origin/main`** (`80b462f`, whose CI run 42411987427 is green): the closure commit is not yet pushed; pushing is the Programme Sponsor's. Repository baseline confirmed as [[RBL-0041_REPOSITORY_BASELINE|RBL-0041]]. Pre-commit governance hook active (`core.hooksPath` = `scripts/hooks`). `.venv` runs Python 3.12.10. pytest 1461 passed, 4 skipped (the same count as ESR-0061 closed with); validator 0 errors, 311 warnings. `scripts/session_launcher.py` run: it reports ESR-0061 as the latest closed session, no session open, and the go-live Session B items as the Next Work Package Candidate. |
| **Reviewer availability** | GitHub Copilot CLI (Engineering Reviewer): available - `copilot -p "Reply with the single word OK." -s --deny-tool='write'` returned "OK" (quota reset 1 November). Antigravity CLI (D19 second reviewer): 1.5.3 installed. Codex CLI: last recorded `402 deactivated_workspace`; not re-probed, not relied on. |
| **Open pull requests** | 21 open. **#40** (the Programme Sponsor's own, 29 October 2026): CI moves from Node 20 to Node 24 for CVE-2026-111497 (Node 20 is end of life). 20 Dependabot pull requests, carried by ESR-0061 Section 6A for triage at this opening: WP1. |
| **WP0B - Engineering Session Initialisation (Complete)** | ESR-0061 confirmed formally Closed. ESR-0062 opened as the next session identifier. `~/.current_session` updated to `ESR-0062`. Objective and Work Package order proposed and **approved by the Programme Sponsor** (direct chat, 8 November 2026, "1. Approved"). Each WP's design approval is still required (rule A6). |
| **Programme Sponsor decisions at opening** | (1) The session objective and WP order in Section 6: **approved**. (2) **Camera on request (EBG-0176): after go-live**; its design may be drafted in this session if there is time (D22), and built straight after go-live - not added to the go-live scope. (3) **EBG-0171: option A** - household notes are hidden from a Child's conversation (rather than an Administrator marking notes child-visible, or checking the notes a Child's turn carries). Built in WP2. |

---

# 4. Engineering Authority

ESR-0062 opening was authorised by direct Programme Sponsor instruction on 8 November 2026, following ESR-0061's formal closure, under the go-live plan's approved sequence (rule A7), with the objective and Work Package order approved in the same conversation.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Session B of the go-live plan: settle the repository's open pull requests; close the household-safety follow-ups ESR-0061 carried (EBG-0171, the idle lock, EBG-0172); deliver voice provisioning on Windows and macOS (EBG-0167, go-live WP7) before Mac visit 1; run Mac visit 1 (EBG-0162 checks and the carried measurements); then the guides and the public "Children and privacy" page (EBG-0168, go-live WP8), which Claude for a Child waits on. Every WP goes through EIP, independent design review, Programme Sponsor approval, `submit-response`, CI and post-commit review.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP0A | Repository Synchronisation | Complete |
| WP0B | Engineering Session Initialisation | Complete |
| WP1 | Repository hygiene ([[EIP-ESR0062-001_REPOSITORY_HYGIENE_DEPENDENCIES_AND_CI|EIP-ESR0062-001]]): #40 (Node 24, CVE-2026-111497) and the 20 Dependabot pull requests applied locally through the gate or closed; the action-gh-release pin (a tag object, not a commit) fixed; the moderation sentence set, **found lost**, to be rewritten (decision D-3) | **Complete.** EIP v0.2: design review (Copilot) Conditional Pass, two Mediums and four Lows addressed. **Design approved** by the Programme Sponsor (8 November 2026; D-1 yes, D-2 agreed, D-3 a private location). Built (recorded in EIP v0.3): one deviation needing explicit approval (#28 `windows-sys` 0.61, after Tauri's crates moved to it); replacement sentence set written and measured (18 of 20 unsafe stopped, 19 of 20 safe allowed). Implementation reviews: Copilot Pass (two Lows: check a file dialog by hand, carried to WP4; release.yml untested until a tag), Antigravity Pass. Built result **approved** through the Sponsor Approval Service, including deviation 1. **Committed `a21984e`**; CI run 42489517516 success on Node 24 (the allowed-to-fail WebKit job fails on the same 5 microphone tests as before). All 21 pull requests settled. Post-commit review: Copilot Pass, Antigravity Pass. Nine new Dependabot pull requests (#41 to #49) opened after the push; placement put to the Programme Sponsor |
| WP2 | Household safety follow-ups: EBG-0171 (option A, household notes hidden from a Child); the idle lock (EIP-ESR0061-006 P4); EBG-0172 backend hardening (export and backup paths, endpoint schemes, speech text), brought forward from go-live WP9; EBG-0178 (Copilot reviewer command form), folded in with the Programme Sponsor's agreement | [[EIP-ESR0062-002_HOUSEHOLD_SAFETY_FOLLOW_UPS|EIP-ESR0062-002]] v0.2: design review (Copilot) Conditional Pass - one High (household notes reached the no-profile state a lock leaves) and six Mediums, all accepted. **Design approved** by the Programme Sponsor (8 November 2026; D-1 15 minutes fixed, D-2 backend validation, D-3 every role). Built (recorded in EIP v0.3): six deviations and clarifications disclosed; Implementation reviews: Copilot Pass (four Lows and an Info fixed, two Lows accepted), Antigravity Pass. Windows pytest 1549 passed, Linux 1548 passed, Playwright 197 passed. Awaiting the Programme Sponsor's approval of the built result |
| WP3 | Voice provisioning on Windows and macOS (EBG-0167, go-live WP7), built before Mac visit 1 so it can be checked there | Not started |
| WP4 | Mac visit 1 (about 21 November 2026): the EBG-0162 real-Mac checks and the measurements carried from EIP-ESR0061-003 and -006 | Not started |
| WP5 | User guide, parents' guide and the public "Children and privacy" page (EBG-0168, go-live WP8) | Not started |
| Session-wide | Independent repository verification, then the Programme Sponsor's baseline determination | Not started |

---

# 7. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.3 | 8 November 2026 | Claude Engineering Implementer | WP1 complete: approved, committed a21984e, CI green, post-commit review Pass from both reviewers; nine new Dependabot pull requests put to the Programme Sponsor. |
| 0.2 | 8 November 2026 | Claude Engineering Implementer | WP1 designed (EIP-ESR0062-001 v0.2) and design-reviewed (Copilot Conditional Pass, findings addressed). Found: the release workflow pins a tag object, not a commit; the moderation sentence set from ESR-0061 WP6d is lost. PR count corrected to 21. |
| 0.1 | 8 November 2026 | Claude Engineering Implementer | ESR-0062 opened as go-live Session B under rule A7. WP0A/WP0B complete: tree clean at 8a40497 (one commit ahead of origin, not pushed), pytest 1461 passed/4 skipped, validator 0 errors; Copilot and Antigravity available. Programme Sponsor approved the objective and WP order; camera on request (EBG-0176) after go-live; EBG-0171 option A. No code changed. |
