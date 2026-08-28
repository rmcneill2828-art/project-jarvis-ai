# EIP-ESR0055-001 - GIA Phase 3b/3c: Repository Health and Register State Observability (EBG-0083)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0055-001 |
| Title | Engineering Implementation Package: WP1 GIA Phase 3b/3c Repository Health and Register State Observability |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0055 |
| Work Package | WP1 |

---

# 2. Purpose

Implements ESR-0055 WP1: the remainder of [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0083 Phase 3 ("engineering instrumentation - repository health, session/baseline state, git state"), following on directly from ESR-0054 WP2 (Phase 3a, git state - [[EIP-ESR0054-002_GIA_PHASE3A_GIT_STATE_OBSERVABILITY|EIP-ESR0054-002]]).

Selected at the Programme Sponsor's direct request to continue where ESR-0054 left off. Two continuations were possible: the remainder of Phase 3 at the same additive-snapshot layer as Phase 3a, or Layer 2 of the broader self-awareness path (feeding GIA's observations into Guardian's Cognitive Core to produce recommendations). The Programme Sponsor selected the former, and specifically **Phase 3b (repository health) and Phase 3c (session/baseline state) together in one Work Package** - completing EBG-0083 Phase 3 in full this session, rather than one more single-slice increment.

No policy, decision-making or platform-state ownership authority is introduced - GIA continues to observe and publish only, per its own defining constraint (ESR-0011 Section 10). No connection to Guardian's Cognitive Core, no recommendation-producing capability, and no GAM-0001/Sentinel policy change - all remain explicitly out of scope (Layer 2/3 of the broader staged path).

---

# 3. Repository Context Investigated

* [[EIP-ESR0054-002_GIA_PHASE3A_GIT_STATE_OBSERVABILITY|EIP-ESR0054-002]] / `jarvis/gia/engineering_observability.py` (as delivered at ESR-0054 WP2): `EngineeringSnapshot` (frozen dataclass), `GitStateReader` (Protocol), `RealGitStateReader` (subprocess-backed `git` CLI, lazy cached repo-root resolution - Codex's own Phase 3a correction), `EngineeringStateObserver` (pure `snapshot()`, no thresholds/decisions). This WP extends this module additively, matching the same precedent Phase 1's 1a-1d increments established for `GiaSnapshot`/`LocalResourceObserver`.
* `scripts/validate_repository.py`: `run_validation(governance_only: bool) -> ValidationResult` and `main()`'s own printed summary line (`"Repository validation passed: 0 errors, N warning(s)."` / `"Repository validation failed: N error(s), M warning(s)."`) - the same command every session already runs manually and the same public CLI contract README documents. `scripts/` has no `__init__.py`; `scripts/tests/` imports it as `scripts.validate_repository` only because `pyproject.toml`'s `pythonpath = ["."]` makes it resolvable as a Python 3 implicit namespace package under pytest - this is a test-time convenience, not something the packaged product can rely on (see Section 4E).
* `scripts/build_backend_sidecar.py`: confirms the Guardian Desktop distributable's PyInstaller sidecar freezes only `scripts/jarvis_backend_entry.py`'s own import graph (`jarvis/`'s product code) - `scripts/validate_repository.py`, the `.git` directory and `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md` are none of them bundled into that distributable. This is a real, disclosed constraint on this WP's scope (Section 4E), not new to this WP - it already silently applied to Phase 3a's `RealGitStateReader` (a packaged install has no `.git` either), just not previously written down.
* `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`: markdown table, one row per controlled artefact - `| ID | Type | Title | Version | Status | Owner | Parent | Location |`. Confirmed every `RBL-*` row present carries Status `Accepted` (superseded baselines are not marked differently in this register - the highest-numbered `RBL-*` row is unambiguously the current one) and `ESR-*` rows carry Status `Closed` once registered at closure, per direct inspection of the current file.
* `scripts/validate_repository.py`'s own `parse_register_rows()`, `latest_accepted_baseline()` and `latest_closed_numbered()`: existing, already-tested functions that address a related but **not identical** problem - **not imported** by this WP (see Section 4E's packaging-boundary reasoning), and only the row-parsing shape is mirrored, not the filtering behaviour (see Section 4A's Codex-corrected field semantics below): `latest_accepted_baseline()`/`latest_closed_numbered()` deliberately filter to `Accepted`/`Closed` rows only, answering "what is the current accepted state" for staleness-checking purposes. This WP's `register_state()` answers a different, simpler question - "what does REG-0001's own table currently say" - with no such filter.
* `aiems/models/GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL.md` Section 8A.1 ("observation is not control"): both new reads (invoking a read-only validation script; reading a markdown file) stay clearly on the observation side of the boundary - no write/mutating operation of any kind.
* `git status`: clean; branch `main`; up to date with `origin/main` as of ESR-0054's closure commit `2d74cc0`.

---

# 4. Scope

## 4A. Extend `jarvis/gia/engineering_observability.py`

* **Rename** `GitStateReader` → `EngineeringStateReader` and `RealGitStateReader` → `RealEngineeringStateReader`. Disclosed as a deliberate internal rename, not a new abstraction: the Protocol was accurately named for Phase 3a alone, but this WP adds two methods that are not git-specific, so keeping the git-scoped name would misdescribe it going forward - matching how `EngineeringSnapshot`/`EngineeringStateObserver` were already named generically from the start. Internal only (never exposed via any RPC field name or external contract); no behavioural change to the existing git-related methods.
* `EngineeringStateReader` gains two methods:
  * `repository_validation() -> tuple[int, int]` - `(error_count, warning_count)`.
  * `register_state() -> tuple[str, str, str]` - `(current_repository_baseline, latest_registered_session, latest_registered_session_status)`.
* `RealEngineeringStateReader.repository_validation()`: runs `[sys.executable, str(repo_root / "scripts" / "validate_repository.py")]` via `subprocess.run` (no shell), captures stdout, and parses the final summary line with a regex tolerant of both the tool's existing "passed"/"failed" phrasings (`(\d+) errors?(?:\(s\))?,\s*(\d+) warning\(s\)`). Propagates on any failure to locate/parse a count (missing `scripts/validate_repository.py`, unexpected output, non-zero exit combined with unparseable stdout) - never fabricates a value, matching the no-mock-fallback rule already applied to `RealGitStateReader`.
* `RealEngineeringStateReader.register_state()`: reads `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md` directly (`Path.read_text`, no subprocess), parses markdown table rows with a self-contained regex mirroring `validate_repository.parse_register_rows()`'s row shape (not imported - see Section 4E), and returns the highest-numbered `RBL-*` row's ID as `current_repository_baseline`, and the highest-numbered `ESR-*` row's ID and its own literal Status column value as `latest_registered_session`/`latest_registered_session_status` - **unfiltered by status** (Codex design-review correction, folded in at v0.2): while a session is open, this genuinely returns e.g. `ESR-0055`/`Open`, not the previous closed session. This is a deliberate choice, not an oversight - `register_state()` reports exactly what REG-0001's table currently contains for its highest-numbered row of each prefix, with no judgement about whether that state is itself "current" in any other sense (that remains a human/Documentation-Debt-Discipline concern, unchanged by this WP), matching GIA's pure observe-and-publish constraint more directly than a filtered read would. This is deliberately **not** the same concept as `validate_repository.latest_closed_numbered()`, which exists to answer a different question (avoiding false staleness warnings against an in-progress session) - `register_state()` is not a staleness check and does not need that filter.
* Both new methods reuse the **same lazy-cached repository-root resolution** Codex's Phase 3a review already established (`git rev-parse --show-toplevel`, resolved on first actual use, cached after success) - factored out of `RealGitStateReader`'s git-command path into one small private helper all three concerns (git, `validate_repository.py` invocation, REG-0001 path) now share, rather than duplicating the resolve-and-cache logic three times. Construction of `RealEngineeringStateReader` remains side-effect-free, matching the existing construction-is-side-effect-free test requirement.
* `EngineeringSnapshot` gains five new fields: `repository_validation_errors: int`, `repository_validation_warnings: int`, `current_repository_baseline: str`, `latest_registered_session: str`, `latest_registered_session_status: str`.
* `EngineeringStateObserver.snapshot()` calls the two new reader methods alongside the three existing ones, same pure/no-branching shape.

## 4B. `gia.engineeringStatus` RPC method (no new endpoint)

Same method as Phase 3a - additive fields only, matching how Phase 1b/1c/1d each extended `gia.status` without adding new RPC methods. Response gains: `repositoryValidationErrors`, `repositoryValidationWarnings`, `currentRepositoryBaseline`, `latestRegisteredSession`, `latestRegisteredSessionStatus` (exact camelCase, matching the existing serialization convention). No change to `gia.status`, `GiaObservabilityAgent`, or any Phase 1 behaviour.

## 4C. `gia-engineering` specialist agent

No code change beyond the observer it already wraps gaining fields - same agent, same `ROUTINE_INTERACTION` classification, same registration.

## 4D. Explicitly out of scope

* Layer 2 (feeding this into Guardian's Cognitive Core to produce recommendations) and Layer 3 (GAM-0001-gated action) - distinct, larger, not-yet-authorised future work, per ESR-0054's own framing.
* Any UXP/frontend surface for this data - backend-only, per PBK-0001's Feature-First Delivery Discipline allowance (matching EBG-0083 Phase 1 and Phase 3a's own precedent).
* Any write/mutating operation - `validate_repository.py` is invoked in its default read-only mode (no `--governance-only`, which only changes which checks run, not whether anything is written); REG-0001 is only ever read.
* Caching the repository-validation result across calls - every `gia.engineeringStatus`/`gia-engineering` invocation re-runs it fresh, matching GIA's existing no-caching precedent (e.g. `cpu_percent`'s live 0.2s sample). This is a real, disclosed latency cost (Section 5) - introducing caching would be its own design decision (invalidation, staleness) and is not attempted here.
* Correcting any staleness `register_state()` happens to observe in REG-0001 itself - this WP reports what the register says, it does not fix the register.

## 4E. Disclosed limitation: source/repository-checkout context only

`repository_validation()` and `register_state()` both depend on files that exist only in a source checkout (`scripts/validate_repository.py`, `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`) - neither is bundled into the Guardian Desktop distributable's PyInstaller sidecar freeze (Section 3). In that packaged context, both new fields will fail identically to how `RealGitStateReader`'s git fields already silently fail there today (no `.git` directory either) - propagated as a genuine error, never a fabricated value, consistent with the no-mock-fallback rule. This is not a new gap introduced by this WP; it is GIA's engineering-instrumentation scope working exactly as intended (observability for the Engineering Implementer's own repository checkout, not end-user product telemetry) - simply not written down explicitly until now. No mitigation is scoped here; disclosed for the Programme Sponsor/Engineering Reviewer's own judgement on whether it warrants a future backlog item (e.g. an explicit "unavailable outside a repository checkout" response shape) rather than a bare propagated exception.

## 4F. Update EBG-0083's EBR-0001 entry

Record Phase 3b/3c's delivery in the existing row (no new backlog number, matching how every prior GIA phase was recorded). Status label extended to reflect Phase 3 complete in full - Phase 2 (platform service instrumentation) and Phase 4 (external instrumentation) remain the only undelivered phases, Phase 2 having been deliberately skipped ahead of Phase 3 by the Programme Sponsor's own explicit ESR-0054 selection, not overlooked.

---

# 5. Validation Requirements

* New unit tests for `RealEngineeringStateReader.repository_validation()`/`register_state()` using fakes for the subprocess call and a fixed REG-0001-shaped fixture text (both success and failure/malformed-output paths).
* **New per Codex design review**: a dedicated `register_state()` test asserting the unfiltered-by-status behaviour explicitly - a fixture REG-0001 table whose highest-numbered `ESR-*` row is `Open` must return that row's ID and `"Open"` verbatim, not silently fall back to a lower-numbered `Closed` row.
* New unit test confirming the shared lazy-cached repo-root helper is actually shared (constructing `RealEngineeringStateReader` and calling all three read methods in sequence resolves the root subprocess call exactly once, not three times).
* Extended RPC-layer tests: exact camelCase serialization of the five new fields from a fixed fake `EngineeringSnapshot`.
* Extended agent-layer test mirroring the existing `gia-engineering` test shape with the new fields present.
* Rename regression check: existing `GitStateReader`/`RealGitStateReader` tests updated to the new names, behaviour otherwise unchanged and still passing.
* Full suite: `pytest jarvis/tests sentinel scripts/tests` - must remain green, count disclosed.
* `python scripts/validate_repository.py` - 0 errors, warning count disclosed (unchanged expected, since this WP does not touch governance content beyond EBR-0001/REG-0001/this EIP/the session report).
* **Live verification against the real repository** (matching every prior GIA phase's own precedent): a real `gia.engineeringStatus` call compared directly against an independently-run `python scripts/validate_repository.py` (error/warning counts) and a direct read of REG-0001 (current highest `RBL-*`/`ESR-*` rows) - not fake-reader coverage alone.
* **Latency disclosure**: report the actual measured wall-clock time `repository_validation()` adds to a `gia.engineeringStatus` call on this repository, since it invokes a full markdown-scanning subprocess rather than the near-instant git/process reads Phase 1/3a used.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* `gia.engineeringStatus` returns real, live-verified repository-health and register-state data matching independently-confirmed ground truth (a direct `validate_repository.py` run; a direct REG-0001 read).
* `gia-engineering` specialist agent continues to work unchanged in shape, now returning the extended snapshot.
* No change to `gia.status`, `GiaObservabilityAgent`, `LocalResourceObserver`, or any existing GIA Phase 1 behaviour.
* No change to Phase 3a's own git-state behaviour beyond the disclosed internal rename.
* No Sentinel policy, GAM-0001, or UXP change of any kind.
* EBG-0083 Phase 3 closed in full (3a/3b/3c all delivered).

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 28 August 2026 | Claude Engineering Implementer | Programme Sponsor approved via direct chat instruction ("Approved"), implemented exactly as scoped in v0.2: `jarvis/gia/engineering_observability.py` extended (`GitStateReader`/`RealGitStateReader` renamed to `EngineeringStateReader`/`RealEngineeringStateReader`; `EngineeringSnapshot` gained 5 fields; `repository_validation()`/`register_state()` added, sharing the existing lazy-cached repo-root resolution), `gia.engineeringStatus` RPC response and `gia-engineering` agent payload both extended additively. 9 new tests, full suite 553 passed/1 skipped (was 549/1), `validate_repository.py` 0 errors/298 warnings (unchanged). Live-verified against this repository's real git/validation/register state - a real `gia.engineeringStatus` call matched independently-run `git`, `validate_repository.py` and a direct REG-0001 read exactly. Measured latency ~2.5s per call, disclosed. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 0.2 | 28 August 2026 | Claude Engineering Implementer | Codex Engineering Reviewer design review via the AIEMS Exchange Bridge - **Conditional Pass with correction**, folded in: Section 4A was internally inconsistent about `latestRegisteredSession`/`latestRegisteredSessionStatus` semantics (named as "latest registered session" while citing `validate_repository.latest_closed_numbered()`, a filtered-to-Closed concept, as a model - the two disagree once a session is genuinely open, as ESR-0055 itself now is). Programme Sponsor selected the unfiltered reading: the fields report the highest-numbered `ESR-*` row in REG-0001 and its literal Status column, whatever that currently is - matching GIA's pure observe-and-publish constraint, deliberately distinct from `latest_closed_numbered()`'s staleness-avoidance filtering. Section 3/4A reworded accordingly; a dedicated unfiltered-status test added to Section 5. Codex separately confirmed agreement with the subprocess/import packaging-boundary tradeoff, the `GitStateReader`->`EngineeringStateReader` rename, and no harder gate needed for Section 4E's dev-checkout-only limitation this WP. No Fail-level issues found once this correction is applied. Not yet approved or implemented. |
| 0.1 | 28 August 2026 | Claude Engineering Implementer | ESR-0055 WP1 draft - GIA Phase 3b/3c (repository health and register-state observability), completing EBG-0083 Phase 3 in full per the Programme Sponsor's direction to continue where ESR-0054 left off. Not yet reviewed, approved or implemented. |
