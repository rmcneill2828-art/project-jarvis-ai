# RBL-0039 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0039 |
| Title | ESR-0059 Repository Baseline (Production Code Review Action Plan; CI Gate Restored; Profile-Scoped Memory) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0059_ENGINEERING_SESSION_REPORT|ESR-0059]] |
| Previous Baseline | [[RBL-0038_REPOSITORY_BASELINE|RBL-0038]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 29 September 2026 |
| HEAD at baseline creation | `61f1712` |

---

# 2. Purpose

RBL-0039 records the repository baseline accepted by the Programme Sponsor at ESR-0059 WP16, superseding [[RBL-0038_REPOSITORY_BASELINE|RBL-0038]]. ESR-0059 opened at the Programme Sponsor's direct request to implement the action plan from the Claude Engineering Implementer's production code review of the JARVIS codebase (28 September 2026), which rated production readiness 5/10 for a single-user desktop release. Fourteen Work Packages delivered every Critical, High and Medium item on that plan, then continued into the backlog under the Programme Sponsor's standing instruction.

The session had a second defining feature: GitHub Copilot CLI, the Engineering Reviewer, reached its monthly quota during WP4. WP1 to WP3 and WP4's design review were genuinely reviewed; everything after was self-verified with full disclosure, on the Programme Sponsor's decision, with a retrospective review owed (EBG-0153).

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0038_REPOSITORY_BASELINE|RBL-0038]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] v2.18 - content refreshed across the session for the provider route, the removed echo fallback and profile-scoped memory with role enforcement. |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ESR-0059 closes following this baseline's acceptance |

---

# 4. Baseline Recommendation Rationale

**WP0A/WP0B**: Repository Synchronisation and Session Initialisation. Objective set by direct Programme Sponsor instruction: implement the production code review's action plan, stopping only for input or decisions.

**WP1 - Critical Runtime Safety Fixes** ([[EIP-ESR0059-001_CRITICAL_RUNTIME_SAFETY_FIXES|EIP-ESR0059-001]]): Tauri commands off the main thread (EBG-0135); backend teardown kills its own process only (EBG-0136); memory restore requires approved consent and valid fields (EBG-0137); Home Assistant entity-id validation (EBG-0138). Seventeen review findings registered.

**WP2 - CI Gate Restored** ([[EIP-ESR0059-002_RESTORE_CI_PYTHON_GATE|EIP-ESR0059-002]]): the CI `python` job had been red on `main` since 29 July 2026, so pytest, the validator and pip-audit had not run in CI for two months (EBG-0152). Fixed, ruff pinned, pip upgraded before pip-audit; branch protection applied at the Programme Sponsor's direction.

**WP3 - Honest Provider-Failure Replies** ([[EIP-ESR0059-003_HONEST_PROVIDER_FAILURE_REPLIES|EIP-ESR0059-003]]): a typed model-reply flag replaced string-matched history recording; the local-echo fallback left the production route (EBG-0141), on the Programme Sponsor's decision.

**WP4 - Gemini Secondary Provider** ([[EIP-ESR0059-004_GEMINI_SECONDARY_PROVIDER|EIP-ESR0059-004]]): credentialed secondary cloud provider (EBG-0051's decision), whitespace keys treated as absent. Copilot's quota ran out during its re-review.

**WP5 - Turn Deadline and Slow-Request Lane** ([[EIP-ESR0059-005_TURN_DEADLINE_AND_SLOW_LANE|EIP-ESR0059-005]], EBG-0139): a 100s per-turn deadline under the 120s Tauri timeout, and a single-worker lane so status and memory calls no longer queue behind slow turns. Live-verified.

**WP6 - Provider Retry and Circuit Breaker** ([[EIP-ESR0059-006_PROVIDER_RETRY_AND_CIRCUIT_BREAKER|EIP-ESR0059-006]], EBG-0140): transient/permanent error classification, deadline-aware retry, a 30s circuit breaker, an up-front deny check.

**WP7 - Prompt Structure** ([[EIP-ESR0059-007_PROMPT_STRUCTURE|EIP-ESR0059-007]], EBG-0142): the system prompt is the approved persona only; history in its own roles and memory as delimited notes, closing the review's prompt-injection finding.

**WP8 - Input Limits and Prompt Budgets** ([[EIP-ESR0059-008_INPUT_LIMITS_AND_PROMPT_BUDGETS|EIP-ESR0059-008]], EBG-0143), **WP9 - Durable Audit Trail and Backend Logging** ([[EIP-ESR0059-009_DURABLE_AUDIT_AND_LOGGING|EIP-ESR0059-009]], EBG-0144), **WP10 - Per-Item Memory Revocation** ([[EIP-ESR0059-010_MEMORY_REVOCATION|EIP-ESR0059-010]], EBG-0145).

**WP11 - Repository Capabilities in Packaged Builds** ([[EIP-ESR0059-011_REPOSITORY_CAPABILITIES_IN_PACKAGED_BUILDS|EIP-ESR0059-011]], EBG-0148): verified on a real packaged build first. While verifying, found the packaged backend re-launching itself as "Python" with the JSON-RPC stream as the child's stdin - fixed.

**WP12 - SQLite Schema Versioning** ([[EIP-ESR0059-012_SCHEMA_VERSIONING|EIP-ESR0059-012]], EBG-0147): atomic, append-only migrations. Its own live check found five test call sites writing into the Programme Sponsor's real home-directory stores - fixed, with a conftest guard.

**WP13 - Profile-Scoped Memory** ([[EIP-ESR0059-013_PROFILE_SCOPED_MEMORY|EIP-ESR0059-013]]) and **WP14 - Household Role Enforcement for Memory** ([[EIP-ESR0059-014_HOUSEHOLD_ROLE_ENFORCEMENT|EIP-ESR0059-014]]): EBG-0132, on three Programme Sponsor decisions asked before building.

**WP15 - Session-wide verification**: disclosed self-verification (Copilot quota exhausted) across `85068ed..61f1712` - Pass, one register inconsistency (EBG-0146's status) corrected.

**The Programme Sponsor's determination** (WP16): **establish a new baseline**, accepting the Engineering Implementer's advisory.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `src-tauri/src/lib.rs` | Async commands; generation-guarded teardown; `list_memory`/`delete_memory` commands. |
| `sentinel/` | Deadline-aware providers, `ProviderError`, retry and circuit breaker, deny check, durable rotating audit, bounded histories, `ConversationTurn`/framed prompts, output caps. |
| `jarvis/interfaces/stdio_rpc.py` | Echo out of the route, Gemini secondary, deadline, slow lane, input limits, audit and log files, memory delete, profile and role resolution. |
| `jarvis/guardian/`, `jarvis/memory/`, `jarvis/identity/` | Typed model replies, per-profile Cognitive Cores, prompt budgets, schema migrations, profile-scoped memory, restore validation and reassignment. |
| `jarvis/repository.py`, `jarvis/shared/schema_migrations.py` (new) | Repository resolution for packaged builds; SQLite migration helper. |
| `src/` | Chat input limit; memory list with confirmed delete and household labels. |
| `.github/workflows/ci.yml`, `pyproject.toml` | CI python gate restored; ruff pinned. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0135 to EBG-0153 registered; fifteen closed Completed, EBG-0146 Deferred. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was content-refreshed during the session (2.14 to 2.18): the provider route with a credentialed secondary, the removal of the local echo fallback, and profile-scoped memory with household role enforcement.

---

# 7. Architecture Outcomes

- The backend is no longer strictly sequential: slow methods run on one dedicated worker, with every other method answered inline. Safety relies on CPython's GIL (disclosed).
- Provider resilience is real: retry, backoff, circuit breaking and a per-turn deadline, replacing a `RetryPolicy` nothing read and a health state nothing acted on.
- No user-authored text reaches the system prompt.
- Personal Memory is private to each profile, with household notes, schema versioning, and role enforcement for approval, Guest access and backup/restore.
- CI is a working gate again, and branch protection makes a red check visible.

---

# 8. Scope Boundaries

- no `LOCAL_AGENT_ACTION` boundary change - `sentinel/policy.py` untouched all session;
- no credentialed authentication - profiles remain unauthenticated;
- no default output-token cap - available but off, pending a live test with the Programme Sponsor's keys;
- no code signing (EBG-0146, Deferred on cost);
- no knowledge-graph snapshot in the installer - a Programme Sponsor product decision not yet taken;
- process-tree termination for the packaged backend and the `python` launcher not yet verified (EIP-ESR0059-001 Section 4G).

---

# 9. Verification

- 27 session commits, every one gated through the real Sponsor Approval Service via `submit-response`, several after genuine drift refusals requiring a fresh decision.
- CI on `main`: 26 of 28 session runs green; the two red runs predate WP2's repair of the gate.
- pytest 751 passed/1 skipped (587 at RBL-0038); Playwright 26/26 (23 at RBL-0038); cargo build/test/clippy/fmt clean; validator 0 errors/333 warnings, unchanged; pip-audit clean in a fresh environment; the suite creates no files in a fake home directory.
- Engineering Reviewer coverage: genuine GitHub Copilot CLI review for WP1 to WP3 and WP4's design review; disclosed self-verification thereafter, on the Programme Sponsor's decision, with a retrospective review owed (EBG-0153).
- Live checks against the real backend process, a recording provider stand-in and a real packaged build throughout; three real defects found by those checks rather than by review.

---

# 10. Handover

Future work against this baseline should include:

1. This document and [[RBL-0038_REPOSITORY_BASELINE|RBL-0038]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. **EBG-0153** - the retrospective GitHub Copilot CLI review of WP4 to WP14, first once the quota resets; WP5's reliance on the GIL is the point most worth an independent look.
5. EBG-0149, EBG-0150, EBG-0151 - the remaining Low-priority review items.
6. Process-tree termination for the packaged backend (EIP-ESR0059-001 Section 4G).
7. EBG-0130 (v1.0 release-gate contradiction), EBG-0110, EBG-0050's residual, and EBG-0128 carried forward unchanged.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0038_REPOSITORY_BASELINE|RBL-0038]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0059_ENGINEERING_SESSION_REPORT|ESR-0059]] | Session this baseline is drawn from. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0135 to EBG-0153 registered; the session's closures and deferral recorded. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline, content-refreshed this session. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 September 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0038, on the Programme Sponsor's WP16 approval of the Engineering Implementer's advisory to establish: fourteen Work Packages delivering every Critical, High and Medium item of the production code review, a two-month CI outage ended, and three real defects found by the session's own live checks. |
