# ESR-0059 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0059 |
| Title | Engineering Session Report |
| Version | 0.3 |
| Status | Open |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0059 |
| Date Opened | 28 September 2026 |
| Date Closed | - |
| Closure Status | Open |

---

# 2. Purpose

This report records the opening of ESR-0059, at the Programme Sponsor's direct request: implement the action plan from the Claude Engineering Implementer's production code review of the JARVIS codebase (28 September 2026, delivered in chat), stopping only where Programme Sponsor input or a decision on a change is needed.

The review rated production readiness 5/10 for a single-user desktop release and grouped its action plan into Critical, High and Nice-to-Have tiers. Its findings are registered in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] as EBG-0135 to EBG-0151 by WP1, so that none of them lives only in chat.

WP0A/WP0B session initialisation followed PBK-0001 and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]].

---

# 3. Scope

**WP0A - Repository Synchronisation (Complete):** Working tree clean at session open. HEAD `85068ed` (ESR-0058 WP8). Repository baseline confirmed as [[RBL-0038_REPOSITORY_BASELINE|RBL-0038]] (accepted ESR-0058 WP8). Pre-commit governance hook confirmed active (`core.hooksPath` = `scripts/hooks`). Full Python suite confirmed green at open: 587 passed, 1 skipped. README.md, PST-0001, PBK-0001 (WP0A/WP0B checklist) and ESR-0058 reviewed.

**WP0B - Engineering Session Initialisation (Complete):** ESR-0058 confirmed formally Closed. ESR-0059 opened as the next session identifier. `~/.current_session` updated to `ESR-0059`. Objective set by direct Programme Sponsor instruction: "proceed with the action plan, only stop when you need my input or decisions on changes."

Backlog validation against [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] before registering the review's findings (PBK-0001 Repository Engineering Health Review Guidance): profile-scoped memory is already EBG-0132; the verbatim handler-exception-message concern is already EBG-0050's residual scope; wiring Gemini into a production route is EBG-0051's own named "separate, not-yet-authorised decision"; the local-echo final fallback is EBG-0070's deliberate design; the memory-content-to-external-providers policy gap is EBG-0110. EBG-0109 (Complete) closed its Finding 2(b) GUI hang as most likely a diagnostic confound; the review's main-thread finding (EBG-0135) is a plausible mechanism for the freeze part of that symptom, recorded as such rather than as a reproduction.

**WP1 - Critical Runtime Safety Fixes (Drafted):** [[EIP-ESR0059-001_CRITICAL_RUNTIME_SAFETY_FIXES|EIP-ESR0059-001]] drafted (v0.1) and implemented against the working tree - the four Critical-tier items that need no product decision:

* **EBG-0135**: all fourteen Tauri commands converted to `async fn`, running the unchanged blocking backend call on Tauri's blocking pool rather than the main thread.
* **EBG-0136**: backend teardown now terminates the process it tears down, and only ever tears down its own process (a per-spawn generation identifier), closing both the orphaned-process leak and a stale-reader race against a newer backend.
* **EBG-0137**: `import_snapshot()` refuses content backed by a denied consent decision, and refuses non-text fields and unparseable timestamps, all before any write.
* **EBG-0138**: Home Assistant entity ids validated against `domain.object_id` in both the agent and the client, before any request path is built.

EBG-0139 to EBG-0151 registered as Candidate Backlog (the review's High and Nice-to-Have findings).

**Real finding made during WP1's own validation, not by the review**: `ruff check .` reported 13 errors on the clean ESR-0058 tree. Checked against the real GitHub Actions history: the CI `python` job has failed on every push to `main` since ESR-0040 WP1 (29 July 2026) - 161 of the last 200 runs - and because ruff is its first step, `pytest`, `validate_repository.py` and `pip-audit` have not run in CI since. The other three jobs stayed green. Registered as EBG-0152 (High) and flagged to the Programme Sponsor as a scope decision rather than folded silently into WP1.

**Disclosed process note** (same pattern as every Work Package at ESR-0058): drafted and implemented directly against the working tree before Programme Sponsor review of this specific content.

**Live smoke check**: the real dev shell (`npm run tauri dev`) built, launched and spawned the backend through the new async commands; the Guardian runtime started with no errors. Disclosed observation from the same check: the dev backend appeared as two processes (a `python` launcher and the real interpreter), so terminating the direct child may not reach the interpreter - recorded in EIP-ESR0059-001 Section 4G as open follow-up for EBG-0136, not fixed here. All smoke-check processes were stopped and port 1420 confirmed free afterwards.

**Design review**: routed through the real bridge (`init`/`submit-to-review` for `ESR-0059`/`WP1`, complete 9-file `files_in_scope`) and reviewed by GitHub Copilot CLI with scoped, write-denied tools. **Verdict: Pass**, single `return-findings` entry, independently verified against the transcript (`sender: reviewer`). The reviewer counted all 14 async commands and all 7 generation-guarded teardown sites itself, confirmed no lock is held across the cleanup branches, confirmed all restore validation precedes the transaction, confirmed entity-id validation in both agent and client, read all 18 new backlog rows against the items they cross-reference, and independently confirmed EBG-0152 from GitHub Actions history. Re-ran pytest (616 passed/1 skipped), `validate_repository.py` (0 errors/333 warnings), ruff (13 pre-existing only), cargo test (8 passed) and clippy (clean). One documentation nit, fixed: the EIP undercounted the documented `TRY004` suppressions (three, not two). Awaiting Programme Sponsor approval.

**Programme Sponsor approved via direct chat instruction ("Approved")** after reviewing the change summary directly. [[EIP-ESR0059-001_CRITICAL_RUNTIME_SAFETY_FIXES|EIP-ESR0059-001]] synced to v1.0 (Approved - implemented). The Programme Sponsor's decisions on EBG-0152 scope, the local-echo fallback, Gemini routing and code signing remain outstanding.

---

# 4. Engineering Authority

ESR-0059 opening was authorised by direct Programme Sponsor instruction on 28 September 2026, following ESR-0058's formal closure.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Implement the production code review's action plan, one Work Package at a time through the standing design-review, Programme Sponsor approval, `submit-response` and post-commit-review template. Items needing a Programme Sponsor product decision are held for that decision rather than implemented on assumption.

---

# 6. Work Package Plan

| WP | Description | Status |
|----|-------------|--------|
| WP0A | Repository Synchronisation | Complete |
| WP0B | Engineering Session Initialisation | Complete |
| WP1 | Critical Runtime Safety Fixes (EBG-0135 to EBG-0138) plus review-finding registration | Approved (EIP-ESR0059-001 v1.0) - pending commit/push |
| Proposed | Restore the CI `python` gate (EBG-0152) | Not started - recommended next, pending Programme Sponsor scope decision |
| Planned | Backend request concurrency and per-turn deadline (EBG-0139) | Not started |
| Planned | Provider resilience: retry, backoff, circuit breaking (EBG-0140) | Not started - Gemini routing needs a Programme Sponsor decision |
| Planned | Non-model replies never presented or recorded as model replies (EBG-0141) | Not started - needs a Programme Sponsor decision on the local-echo fallback |
| Planned | Prompt structure and token budgets (EBG-0142, EBG-0143) | Not started |
| Planned | Production observability (EBG-0144) and memory revocation (EBG-0145) | Not started |

---

# 7. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 0.3 | 28 September 2026 | Claude Engineering Implementer | WP1 approved via Programme Sponsor direct chat instruction ("Approved"). EIP-ESR0059-001 synced to v1.0. Pending commit/push through submit-response. |
| 0.2 | 28 September 2026 | Claude Engineering Implementer | WP1 live smoke check and design review recorded - Pass via genuine GitHub Copilot CLI invocation routed through the real bridge. Awaiting Programme Sponsor approval. |
| 0.1 | 28 September 2026 | Claude Engineering Implementer | ESR-0059 opened. WP0A/WP0B complete. Objective set by direct Programme Sponsor instruction: implement the production code review's action plan. WP1 drafted per EIP-ESR0059-001 v0.1 - four Critical-tier fixes (EBG-0135 to EBG-0138) implemented and tested, EBG-0139 to EBG-0151 registered; EBG-0152 (CI `python` job red since 29 July 2026) found during WP1 validation and registered. Not yet reviewed, approved or committed. |
