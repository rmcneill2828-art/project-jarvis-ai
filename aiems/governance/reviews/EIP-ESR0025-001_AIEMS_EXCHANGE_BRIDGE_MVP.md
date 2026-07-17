# EIP-ESR0025-001 - AIEMS Exchange Bridge MVP

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0025-001 |
| Artefact ID | EIP-ESR0025-001 |
| Title | AIEMS Exchange Bridge MVP |
| Version | 1.2 |
| Status | Approved - implemented, post-implementation findings addressed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0057) |
| Intended Session | ESR-0025 |
| Effective Date | 17 July 2026 |

---

# 2. Purpose

Implements **EBG-0057** (Claude<->Codex Engineering Bridge), Approved Backlog, elevated to JRM-0001 Track A Near-term post-ESR-0024 closure. This is an AIEMS engineering-tooling workstream, run separately from JRM-0001's JARVIS/Guardian product tracks - it governs how the Engineering Implementer (Claude) and Engineering Reviewer (Codex) exchange Work Packages, not any Guardian/Sentinel/UXP capability.

EBG-0057's architecture (directory layout, role-locking principle, command set, evidence capture, no CLI session-resume dependency) is already decided and recorded in EBR-0001, following an independent Lead Reviewer code review of an earlier prototype. This package translates that architecture into a concrete, implementable specification - file formats, exact CLI shape, and the precise mechanism by which "role-locked" is actually enforced in code rather than only described in prose - and requests review and approval before any of it is built.

---

# 3. Objective

Let the Programme Sponsor stop manually relaying Work Packages between two windows, while preserving - by construction, not by convention alone - the two properties ESR-0023's write-boundary incidents proved matter most: Codex can never write to the repository directly, and Claude can never act on a handover the Programme Sponsor has not explicitly authorised.

---

# 4. Repository Context

| Item | Current State |
|------|---------------|
| `.aiems-exchange/` | Does not exist. Not present in `.gitignore`. |
| `scripts/` conventions | Existing scripts (`validate_repository.py`, `bump_version.py`) are single-file Python CLIs with tests under `scripts/tests/test_<name>.py` (`test_validate_repository.py`, `test_bump_version.py` precedent). This package follows that convention rather than introducing a new package layout. |
| Current handover mechanism | The Programme Sponsor manually relays Work Packages, findings and approvals between separate Claude and Codex sessions/windows - functioning, but entirely manual. |
| PBK-0001 Separation of Duties | "The Engineering Reviewer shall not perform repository implementation" - the exact rule ESR-0023 Sections 9.1/10.1 record being breached twice, root-caused to a Codex tool-configuration setting, not a comprehension gap. |
| EBG-0060 disposition | DCE (single-AI direct execution) Superseded by this architecture; REA (execution-automation agent) folded into this item's own future-phase scope, not this MVP's. |

---

# 5. Scope

This package authorises a future implementation to:

1. Create `scripts/aiems_bridge.py`, a single-file Python CLI (argparse subcommands), and `scripts/tests/test_aiems_bridge.py`.
2. Add `.aiems-exchange/` to `.gitignore`.
3. Implement the directory layout, handover file format, five commands, preflight checks, HEAD-drift detection and evidence capture exactly as specified in Sections 6-9 below.
4. Mark EBG-0057 `Complete` in EBR-0001 only once actually implemented, validated and committed - with corresponding updates to JRM-0001, PST-0001 and REG-0001.

No other files are authorised to change. No product code (`jarvis/`, `sentinel/`, `src/`) is touched by this package - this is engineering tooling only.

---

# 6. Directory Layout and File Formats

```
.aiems-exchange/                    (gitignored, restrictive permissions - PBK-0001/EE-0001 Section 7.4 lesson: must not be left writable/readable in the repo root as the superseded prototype was)
  claude/inbox/                     handover files addressed to Claude (submit-to-review's own copy lives here for symmetry, though Claude is its sender; return-findings' target)
  claude/outbox/                    handover files Claude has sent (submit-to-review, submit-response)
  codex/inbox/                      handover files addressed to Codex (submit-to-review's target)
  codex/outbox/                     handover files Codex has sent (return-findings)
  transcript/<session>-<wp>.md      append-only log of every handover for one Work Package, in order - the ONLY location for sponsor-decision handovers (Section 7 item 4; Engineering Reviewer finding, addressed)
  .locks/<session>-<wp>.lock        held for the duration of a single command's execution, preventing two invocations from racing on the same Work Package's transcript
```

**`sponsor-decision` is transcript-only, by design, not inbox-routed.** It is not a point-to-point handover between two AI roles - it is a gate-setting record the whole Work Package depends on, and `submit-response` already reads the transcript (not any inbox) to check authorisation (Section 9). Giving it a third inbox location would create two sources of truth for the same fact; the transcript is the single canonical location. **(Engineering Reviewer finding, addressed: the original draft never stated where `sponsor-decision` records lived or how they were routed, since the inbox/outbox model only covers Claude/Codex - resolved by making the transcript the sole location for this handover type, rather than inventing a third inbox.)**

**Handover file** (plain header block, not YAML, per the architecture's own stated reason - no new parser dependency):

```
session: ESR-0025
work_package: WP1
type: submit-to-review | return-findings | sponsor-decision | submit-response
sender: claude | codex | programme_sponsor
recipient: claude | codex | n/a (sponsor-decision only - transcript-only, no inbox routing)
repository_ref: <git rev-parse HEAD at time of writing>
files_in_scope: path/one.py, path/two.py
programme_sponsor_authorisation: true | false | (field absent - only ever present on sponsor-decision)
timestamp: <ISO 8601 UTC>
---
<free-text message body>
---evidence---
<raw pytest / validate_repository.py output, verbatim, not interpreted - present only on submit-to-review and submit-response>
```

Every handover is appended, verbatim, to the Work Package's transcript file - the transcript is the authoritative continuity record (Section 8 explains why this replaces CLI session-resume flags) and, for `sponsor-decision` specifically, the only record at all.

---

# 7. Commands

1. **`bridge init <session> <wp>`** - creates the directory layout if absent, creates an empty transcript file for `<session>-<wp>` if one does not already exist (refuses to overwrite an existing one).
2. **`bridge submit-to-review <session> <wp> --files <comma-separated> --message <text>`** - Claude only, by protocol (Section 9). Captures `repository_ref` (current `HEAD`), runs `pytest` and `validate_repository.py`, attaches their raw output as evidence, writes the handover to `codex/inbox/` and appends to the transcript.
3. **`bridge return-findings <session> <wp> --message <text>`** - Codex only, by protocol. Writes only to `.aiems-exchange/` (`claude/inbox/` and the transcript) - never touches any file outside that directory. No evidence re-run (Codex is reviewing, not re-validating).
4. **`bridge sponsor-decision <session> <wp> --decision approve|reject --note <text>`** - the Programme Sponsor's own command, run directly in their own terminal, never invoked by either AI. The **only** code path that may write `programme_sponsor_authorisation: true` to a handover. Writes a new, timestamped, structured handover recording the decision, appended to the transcript only (Section 6) - not a flag silently mutating a prior file, so the record is append-only like everything else. **Captures `repository_ref` (current `HEAD`) at decision time** - this is the exact repository state the Programme Sponsor is approving, and the baseline `submit-response` checks itself against (item 5, Engineering Reviewer finding, addressed).
5. **`bridge submit-response <session> <wp> --message <text>`** - Claude only, by protocol, and the only command that represents "the approved implementation may now proceed." **Hard-refuses to run** (non-zero exit, no side effects) unless the transcript for `<session>-<wp>` contains a `sponsor-decision` handover with `programme_sponsor_authorisation: true` and no later `sponsor-decision` reversing it. **Also hard-refuses if the current `repository_ref` does not match the `repository_ref` recorded on that approving `sponsor-decision` handover** - drift since approval is not a warning-level condition for a tool whose entire purpose is preserving approval boundaries (Section 8; Engineering Reviewer finding, addressed). On a clean match, re-runs `pytest`/`validate_repository.py`, attaches evidence, writes to `claude/outbox/` and the transcript.

No sixth command performs an autonomous multi-turn loop or a default-continue prompt, matching the architecture's explicit exclusion.

---

# 8. Preflight, HEAD-Drift and Continuity

1. **Preflight** (every command): confirm `claude` and `codex` executables are resolvable (`shutil.which`), capture both tools' `--version` output, and run `codex login-status` (or the closest available equivalent to confirming Codex authentication) - attach all three to the command's log output. A failed preflight aborts before any file is written.
2. **HEAD-drift detection**: `repository_ref` is captured at `submit-to-review` (submission), again at `sponsor-decision` (the state actually being approved), and again at `submit-response` (implementation). The authorisation-relevant comparison is `submit-response`'s current `repository_ref` against the approving `sponsor-decision`'s recorded value (Section 7 item 5) - on a mismatch, `submit-response` **hard-refuses**, the same as missing authorisation, rather than merely warning. Drift can be legitimate (an unrelated commit may have landed in between) but the tool's purpose is preserving approval boundaries, so re-establishing them - a fresh `sponsor-decision` against the new `HEAD`, or a fresh review cycle if the drift is substantive - is the correct response, not a logged warning that lets an unreviewed repository state proceed anyway. **(Engineering Reviewer finding, addressed: the original draft treated drift as warn-only, which would have let a response apply against a different repository state than the one actually reviewed and approved.)** The `submit-to-review`-to-`sponsor-decision` gap remains informational only (recorded in both handovers, not gated) since the Programme Sponsor's own review of the submission already accounts for any drift up to their decision.
3. **Continuity**: no command reads or writes `claude -r` / `codex exec resume --last` state. The transcript and handover files are the sole continuity source, because each handover is self-contained (carries its own `repository_ref`, files-in-scope and message) and `--last`-style flags risk silently resuming an unrelated session, per the architecture's own stated reasoning.

---

# 9. How Role-Locking Is Actually Enforced

This section is deliberately explicit, since "role-locked" is a claim that must be checkable, not just asserted:

1. **Codex can never write to the repository.** The tool provides Codex with exactly one command, `return-findings`, whose implementation only ever opens files under `.aiems-exchange/`. There is no code path in `return-findings` that touches any path outside that directory - not a permission check, a structural one (the function has no parameter or branch that could resolve to a repository source path). **This claim had a real gap at v1.0, closed post-implementation (Engineering Reviewer High finding):** `session`/`work_package` fed unsanitised into `_wp_key()`, which every path-building function (`transcript_path`, `_lock_path`) goes through - a value such as `work_package="../../escape"` could resolve outside `.aiems-exchange/` despite `return-findings` itself taking no file-path argument. Fixed by validating both identifiers (`^[A-Za-z0-9_-]+$`) inside `_wp_key()` itself, so every path-building call site is covered structurally, not per call site. Verified live via the real CLI, not only unit tests.
2. **Claude can never act on an unauthorised, or since-drifted, handover.** `submit-response` is the only command that represents "proceed with the approved change," and its very first action (inside the Work Package lock - see item 5) is to scan the transcript for the most recent `sponsor-decision` handover. If none exists, the most recent one is `reject`, or the current `repository_ref` no longer matches the state that `sponsor-decision` actually approved (Section 8), the command exits non-zero before performing any other action. This is a real code gate, not a documentation convention - `programme_sponsor_authorisation: true` can only ever be written by `sponsor-decision`, and `sponsor-decision` is a command the Programme Sponsor runs themselves, never invoked by either AI within this tool's own command set.
3. **Claude cannot record a successful response against a failing validation run.** Added post-implementation (Engineering Reviewer Medium finding): `submit-response` also refuses if `pytest`/`validate_repository.py` did not both pass cleanly, exiting before any file write, the same way it refuses on missing authorisation or drift. `submit-to-review` deliberately stays non-blocking on validation - submitting known-broken work-in-progress for review is legitimate - but its evidence text now opens with an unmissable `VALIDATION: PASSED`/`VALIDATION: FAILED` marker, so a failing run can no longer be mistaken for a passing one at a glance.
4. **The authorisation check itself cannot be raced.** Added post-implementation (Engineering Reviewer Medium finding, TOCTOU): at v1.1, `submit-response` read the transcript, checked drift, ran preflight and captured evidence (the slowest step - a full `pytest` run) all *before* acquiring the Work Package lock, only locking for the final write. A concurrent `sponsor-decision` (e.g. a reject) could land in that window, and `submit-response` would still proceed on the stale approval it had already read - the lock protected the write, not the decision it was based on. Fixed by moving the entire read-check-evidence-write sequence inside the lock. Every other command that can append to the same Work Package's transcript (`sponsor-decision`, `return-findings`, `submit-to-review`, a second `submit-response`) already acquires this same lock before writing, so holding it for `submit-response`'s full duration means a concurrent same-WP action now fails fast against the lock instead of racing in - proven directly by a test that injects a concurrent `sponsor-decision` attempt during evidence capture and asserts it is blocked, not merely by inspection.
5. **What this does *not* claim to do.** The tool cannot cryptographically verify *which* human or AI process is invoking a given command - `bridge return-findings` run by a differently-configured Codex session (or, in principle, by anyone with shell access) would still only be able to write into `.aiems-exchange/`, and `bridge submit-response` run without a prior `sponsor-decision: approve` would still refuse - so the enforcement holds regardless of caller identity for these properties specifically. What it relies on outside the tool is the same thing ESR-0023's root-cause fix already addressed: the calling AI's own approval-policy configuration (e.g. Codex's `~/.codex/config.toml` `trust_level`) determines whether it can invoke shell commands at all without a human prompt - this tool does not change or substitute for that control, it adds a second, code-level gate behind it.

---

# 10. Authorised Files

1. `scripts/aiems_bridge.py`
2. `scripts/tests/test_aiems_bridge.py`
3. `.gitignore`
4. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
5. `aiems/governance/roadmap/JRM-0001_PROJECT_ROADMAP.md`
6. `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`
7. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 11. Explicit Exclusions

This package does not authorise:

1. **REA** (Repository Execution Agent - a future agent automating the mechanical commit/diff/reporting execution step). Folded into this item's future-phase scope per the EBG-0060 disposition, not part of this MVP.
2. **DCE** in any form - no command in this tool ever permits Codex, or any AI other than Claude acting under an approved `sponsor-decision`, to write outside `.aiems-exchange/`.
3. Any change to `claude`'s or `codex`'s own tool configuration (e.g. `~/.codex/config.toml`) - this package adds a second gate behind that configuration, it does not manage it.
4. Any venue change (browser automation of either AI's consumer web UI remains explicitly rejected, per the architecture's own ESR-0018 post-closure discussion - ToS risk to the Programme Sponsor's actual accounts).
5. A new personal ChatGPT Plus subscription or any other recurring cost - the existing cost decision (Business workspace sufficient, per ESR-0019's empirical finding) is unchanged by this package.
6. Live invocation of real `claude`/`codex` CLI processes from the automated test suite - tests must mock subprocess calls, matching this codebase's existing no-real-network-call convention for provider tests.

---

# 12. Constraints

1. `return-findings`'s implementation must have no code path capable of writing outside `.aiems-exchange/` - this is a testable property (Section 14) and a blocking requirement, not a preference.
2. `submit-response` must refuse to proceed - before any evidence capture, before any file write - when no approving `sponsor-decision` handover exists for the Work Package, when the most recent `sponsor-decision` is `reject`, **or when the current `repository_ref` does not match the approving `sponsor-decision`'s recorded `repository_ref`** (Section 8; Engineering Reviewer finding, addressed).
3. `programme_sponsor_authorisation: true` must never be settable by any command other than `sponsor-decision`, and `sponsor-decision` handovers must never be routed to any inbox/outbox - transcript only (Section 6; Engineering Reviewer finding, addressed).
4. `.aiems-exchange/` must be `.gitignore`d before any command that creates it is exercised, including in tests (tests must operate against a temporary directory, never the real repository-root `.aiems-exchange/`).
5. No implementation shall begin until this package reaches Approved status.

---

# 13. Validation

After implementation, run:

```powershell
python -m pytest
python scripts/validate_repository.py
```

Validation should confirm:

1. Full pytest suite passes, including new tests for `aiems_bridge.py`.
2. A test proves `return-findings` cannot write outside a temporary `.aiems-exchange/` (Constraint 1) - e.g. asserting the function's file-write calls are confined to that directory across representative inputs.
3. A test proves `submit-response` exits non-zero and performs no file writes when no `sponsor-decision: approve` handover exists for the target Work Package (Constraint 2).
4. A test proves `submit-response` still exits non-zero after a `sponsor-decision: reject` even if an earlier `approve` exists, and succeeds after an `approve` with no later `reject`, matching `repository_ref`.
5. A test proves `submit-response` exits non-zero, performing no file writes, when the current `repository_ref` no longer matches the approving `sponsor-decision`'s recorded value - and succeeds once a fresh matching `sponsor-decision` is recorded (Constraint 2, Section 8).
6. A test proves `sponsor-decision` handovers are written only to the transcript, never to any inbox/outbox (Constraint 3, Section 6).
7. `validate_repository.py` (full mode, since this touches source) passes with the same pre-existing warning count, 0 errors.
8. A manual dry run (not part of the automated suite) exercising one real `submit-to-review` -> `return-findings` -> `sponsor-decision` -> `submit-response` cycle against a throwaway Work Package, confirming the transcript reads correctly end to end - including one deliberate re-run of the cycle where an intervening commit forces the Section 8 drift-refusal path, then a fresh `sponsor-decision` clears it.

---

# 14. Risks and Dependencies

## Dependencies

1. `git`, `claude` and `codex` CLIs available on the Programme Sponsor's machine (already confirmed - this session's own tooling).
2. EBG-0060's disposition (Section 4), already resolved and committed (`fdb82f7`).

## Risks

1. **Enforcement is code-level for the two properties that matter most (Codex write-scope, Claude authorisation-gating), not a full sandbox.** Section 9 states this explicitly rather than overclaiming. Residual risk: a differently-configured AI tool could still invoke arbitrary shell commands *outside* this tool entirely, exactly as the ESR-0023 incidents did - this package adds a second gate, it does not replace the first (tool-configuration) one.
2. **This is a materially larger build than either ESR-0024 EIP** - five commands, a file format, and three structural safety properties needing their own tests, not a two-line wiring change. Sized at roughly one full session for this MVP scope, per the workload estimate discussed before this package was drafted.
3. Manual dry-run validation (Section 13 item 7) depends on both CLIs behaving as expected in a live session - cannot be fully proven by the automated suite alone, similar in kind to the residual risk already accepted for UXP Playwright verification (EIP-ESR0024-002).

---

# 15. Approval Request

**v0.1 reviewed by Engineering Reviewer (Codex): one High, one Medium finding, both addressed in v0.2** (Sections 6, 7, 8, 9, 12, 13). **v0.2 approved by Codex.** **Approved by the Programme Sponsor, 17 July 2026.** Implemented exactly as scoped: `scripts/aiems_bridge.py` (five commands), `scripts/tests/test_aiems_bridge.py` (15 new tests, 227 total), `.gitignore` entry. All Section 13 validation items confirmed except item 8's full live cycle (see below). `validate_repository.py`: 0 errors. A live dry run against a throwaway Work Package confirmed, for real (not mocked): the authorisation-refusal path (`submit-response` before any `sponsor-decision`), the approval-success path (past both the authorisation and drift gates once approved), and the preflight-refusal path (neither `claude` nor `codex` is on the Engineering Implementer's own sandboxed shell `PATH`, so `submit-to-review`/`submit-response` correctly refused with no side effects). The full successful cycle with real `claude`/`codex` CLI presence was not verified live, since that requires an environment where both are actually installed - disclosed as an honest residual gap (EIP Section 14 item 3), not asserted as tested; the Programme Sponsor's own terminal is best placed to exercise it when convenient.

**Post-implementation review of the actual diff by Engineering Reviewer (Codex): one High, one Medium finding, both addressed in v1.1.** High: `session`/`work_package` fed unsanitised into path construction could escape `.aiems-exchange/` via `..`/path-separator injection, undermining the Section 9 item 1 containment claim - fixed by validating both identifiers inside `_wp_key()`, verified live via the real CLI in addition to 6 new parametrised unit tests. Medium: `capture_evidence()` never checked `pytest`/`validate_repository.py` return codes, so `submit-to-review` and `submit-response` could emit handovers that looked successful even when validation had failed - resolved asymmetrically: `submit-response` now hard-refuses on validation failure (Section 9 item 3, 3 new tests), `submit-to-review` stays non-blocking but its evidence now opens with an unmissable `VALIDATION: PASSED`/`FAILED` marker. 236 tests pass (was 227). `validate_repository.py`: 0 errors, 104 warnings, unchanged.

**A second post-implementation review found one further Medium finding, addressed in v1.2 (TOCTOU).** `submit-response` read the transcript, checked drift, ran preflight and captured evidence - all before acquiring the Work Package lock, only locking for the final write - so a concurrent `sponsor-decision` could land in that window and the response would still proceed on the stale approval already read. Fixed by moving the entire read-check-evidence-write sequence inside the lock (Section 9 item 4), matching every other command's existing lock-before-write discipline. Proven by a new test that injects a concurrent `sponsor-decision` attempt during evidence capture (the slowest step) via a monkeypatched `capture_evidence`, and asserts the concurrent call is genuinely blocked by the lock, not merely that the code compiles. 237 tests pass (was 236). Live smoke-checked via the real CLI. `validate_repository.py`: 0 errors, 104 warnings, unchanged.

---

# 16. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0057 (this package's parent) and EBG-0060 (resolved dependency, `fdb82f7`). |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Track A 6.1, EBG-0057's current Near-term placement. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Section 7.4, the write-boundary incidents this package's role-locking is designed against. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | Separation of Duties, Working Report Lifecycle and Approval Before Change principles this package follows. |
| [[ESR-0023_ENGINEERING_SESSION_REPORT|ESR-0023]] | Sections 9.1/10.1/10.2, the direct empirical evidence motivating Section 9's design. |

---

# 17. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.2 | 17 July 2026 | Claude Engineering Implementer | Addressed a further Engineering Reviewer (Codex) Medium finding (TOCTOU) on the v1.1 diff: `submit-response` read the transcript, checked drift, ran preflight and captured evidence - all before acquiring `work_package_lock()`, only locking for the final write - so a concurrent `sponsor-decision` could land in that window and the response would still proceed on the stale approval already read. Fixed by moving the entire read-check-evidence-write sequence inside the lock, matching every other command's existing lock-before-write discipline (Section 9 item 4 added). Proven by a new test injecting a concurrent `sponsor-decision` attempt during evidence capture and asserting it is genuinely blocked. 237 tests pass (was 236). Live smoke-checked via the real CLI. |
| 1.1 | 17 July 2026 | Claude Engineering Implementer | Addressed two Engineering Reviewer (Codex) findings on the implemented v1.0 diff: (1) **High** - `session`/`work_package` fed unsanitised into `_wp_key()`-derived paths (`transcript_path`, `_lock_path`) could escape `.aiems-exchange/` via `..`/path-separator injection, undermining the Section 9 item 1 containment claim - fixed by validating both identifiers inside `_wp_key()` itself (`_validate_identifier`, `^[A-Za-z0-9_-]+$`), so every path-building call site is covered structurally; verified live via the real CLI plus 6 new parametrised tests; (2) **Medium** - `capture_evidence()` never checked `pytest`/`validate_repository.py` return codes, so `submit-to-review`/`submit-response` could emit handovers that looked successful even when validation had failed - `capture_evidence` now returns an `EvidenceResult(passed, text)`; `submit-response` hard-refuses on `not passed`, matching the missing-authorisation/drift refusal pattern (3 new tests); `submit-to-review` stays non-blocking but its evidence text now opens with an unmissable `VALIDATION: PASSED`/`FAILED` marker. 236 tests pass (was 227). Section 9 rewritten to document both fixes; Sections 1, module docstring updated. |
| 1.0 | 17 July 2026 | Claude Engineering Implementer | Programme Sponsor approved implementation following Codex's v0.2 approval. Implemented exactly as scoped: `scripts/aiems_bridge.py`, `scripts/tests/test_aiems_bridge.py` (15 new tests, 227 total), `.gitignore`. EBR-0001 (1.53 to 1.54), JRM-0001 (1.12 to 1.13) aligned - EBG-0057 marked Complete. `validate_repository.py` 0 errors. Live dry run confirmed the authorisation, drift-gate-ordering and preflight-refusal paths for real; the full successful cycle needs the Programme Sponsor's own environment (neither `claude` nor `codex` is on the Engineering Implementer's sandboxed shell `PATH`) - disclosed, not asserted as tested. Status Draft to Approved, version 0.2 to 1.0. |
| 0.2 | 17 July 2026 | Claude Engineering Implementer | Addressed two Engineering Reviewer (Codex) findings on v0.1: (1) **High** - `sponsor-decision` had no canonical storage location, since the inbox/outbox model only covers Claude/Codex and the schema only allowed `recipient: claude | codex` - resolved by making `sponsor-decision` transcript-only, no inbox routing (Sections 6, 7, 12); (2) **Medium** - `submit-response` only warned on HEAD drift rather than blocking, letting a response apply against a repository state different from what was actually sponsor-approved - resolved by having `sponsor-decision` itself capture `repository_ref` at decision time and having `submit-response` hard-refuse on any mismatch against that value, requiring a fresh `sponsor-decision` (Sections 7, 8, 9, 12, 13). |
| 0.1 | 17 July 2026 | Claude Engineering Implementer | Initial draft translating EBG-0057's already-decided architecture into a concrete, implementable specification: file formats, exact CLI shape, and an explicit statement (Section 9) of how role-locking is actually enforced in code versus what it does not claim to guarantee. Reviewed by Engineering Reviewer (Codex): one High, one Medium finding, superseded by v0.2. |
