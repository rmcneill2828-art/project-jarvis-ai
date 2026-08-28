# EIP-ESR0054-002 - GIA Phase 3a: Git State Observability (EBG-0083)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0054-002 |
| Title | Engineering Implementation Package: WP2 GIA Phase 3a Git State Observability |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0054 |
| Work Package | WP2 |

---

# 2. Purpose

Implements ESR-0054 WP2: the first slice of [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0083 Phase 3 ("engineering instrumentation - repository health, session/baseline state, git state"), the next undelivered GIA phase per ESR-0011's original four-phase plan (Phase 1 complete in full since ESR-0029; Phases 2-4 remain open).

Selected following the Programme Sponsor's direct question about getting JARVIS/Guardian/Sentinel to a position where it can become aware of its own code and eventually assist with engineering work. This WP delivers the first concrete step of a staged path discussed and agreed in chat: GIA read-only awareness of the repository's own engineering state, with no policy/decision authority (matching GIA's existing constraint) and no governance change required (`ROUTINE_INTERACTION`, the same trust tier `gia-observability` already runs under).

Phase 3's full scope (repository health via `validate_repository.py`, session/baseline state via REG-0001) is intentionally **not** attempted in this WP - split into a first slice (git state) matching the same staged-increment discipline EBG-0083's own text already established for Phase 1 (1a/1b/1c/1d, each its own WP).

---

# 3. Repository Context Investigated

* `jarvis/gia/observability.py`: existing `GiaSnapshot`/`LocalResourceObserver`/`ResourceReader` pattern (Phase 1a-1d) - a frozen dataclass snapshot, an injectable reader Protocol with a real `psutil`-backed implementation and a test-only fake, a pure observer class with no thresholds/branching. Git state is a different data domain (subprocess/git, not `psutil`), so this WP adds a new, parallel module rather than extending `GiaSnapshot` itself.
* `jarvis/agents/gia_agent.py` / `jarvis/agents/contracts.py`: existing `GiaObservabilityAgent` pattern - a `SpecialistAgent` wrapping an injected observer, classified `ROUTINE_INTERACTION`, registered by name in `build_default_runtime()`'s `agents` dict. This WP follows the identical shape for a second agent.
* `jarvis/interfaces/stdio_rpc.py`: `gia.status`'s existing wiring (`_gia_observer` constructor-injectable, defaulting to the real observer; dispatch table entry; exact camelCase serialization). This WP mirrors it for a new `gia.engineeringStatus` method.
* `aiems/models/GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL.md` Section 8A.1: "observation is not control" - git state reads (branch, uncommitted count, last commit) are read-only `git` invocations, no write/mutating git operation, staying clearly on the observation side of the boundary.
* `git status`: clean; branch `main`; up to date with `origin/main` as of WP1's commit `187fd0a`.

---

# 4. Scope

## 4A. New module: `jarvis/gia/engineering_observability.py`

* `EngineeringSnapshot` (frozen dataclass): `git_branch: str`, `git_uncommitted_files: int`, `git_last_commit_sha: str`, `git_last_commit_message: str`, `captured_at: datetime`.
* `GitStateReader` (Protocol): `branch() -> str`, `uncommitted_file_count() -> int`, `last_commit() -> tuple[str, str]` (sha, message) - mirrors `ResourceReader`'s injectable-Protocol pattern so unit tests never depend on the actual repository's live git state.
* `RealGitStateReader`: subprocess-backed against the real `git` CLI (`git rev-parse --abbrev-ref HEAD`; `git status --porcelain`, counting lines; `git log -1 --format=%H%x1f%s`). **Corrected per Codex design review**: the repository root (`git rev-parse --show-toplevel`) is resolved **lazily**, on first use inside the reader's git-command path - never at construction - and cached after that first successful resolution. Construction itself performs no external operation and cannot fail; a missing `git` executable, non-worktree `cwd`, or transient git failure only surfaces when `gia.engineeringStatus`/the agent is actually invoked, not at unrelated runtime/RPC startup. No new dependency (no GitPython) - matches the project's existing preference for the `git` CLI directly (already used throughout `scripts/`). Detached `HEAD` state reports the literal string `"HEAD"` via `rev-parse --abbrev-ref HEAD` - documented as the literal git observation, not a defect (Codex non-blocking note).
* `EngineeringStateObserver`: constructor-injected reader (defaults to `RealGitStateReader`), a pure `snapshot()` method with no thresholds, alerts or branching on the values it reads - same "observe and publish only" constraint GIA already operates under (ESR-0011 Section 10).
* Propagates whatever the underlying `git` invocation raises (e.g. `subprocess.CalledProcessError`) - never fabricates a value, per the project's no-mock-fallback rule.

## 4B. New RPC method: `gia.engineeringStatus`

`jarvis/interfaces/stdio_rpc.py` gains a second, independently-injectable observer (`_gia_engineering_observer`, defaulting to the real one) and a `gia.engineeringStatus` dispatch entry, returning `EngineeringSnapshot` serialized to exact camelCase (`gitBranch`, `gitUncommittedFiles`, `gitLastCommitSha`, `gitLastCommitMessage`, `capturedAt`) - matching `gia.status`'s existing serialization convention exactly. Ungated, like `gia.status` - GIA observation does not go through Sentinel's request path at all, per GAM-0001 8A.1 (unchanged existing precedent, not a new decision this WP makes).

## 4C. New specialist agent: `jarvis/agents/gia_engineering_agent.py`

`GiaEngineeringAgent` (`name = "gia-engineering"`), constructor-injected `EngineeringStateObserver`, wraps the same snapshot as a Sentinel-gated `SpecialistAgent` path (mirroring `GiaObservabilityAgent`'s own docstring explanation of why both an ungated RPC method and a gated agent path coexist). Classified `ROUTINE_INTERACTION` - read-only, no local device/system state touched, never approaches `LOCAL_AGENT_ACTION`. Registered in `build_default_runtime()`'s `agents` dict alongside `gia-observability`.

## 4D. Explicitly out of scope

* Repository health (`validate_repository.py` invocation/parsing) and session/baseline state (REG-0001 parsing) - deferred to future Phase 3 slices (3b, 3c), not attempted here.
* Any UXP/frontend surface for this data - backend-only capability delivery, per PBK-0001's Feature-First Delivery Discipline allowance (matching EBG-0083 Phase 1's own precedent).
* Any connection into Guardian's Cognitive Core or a recommendation-producing capability (Layer 2 of the staged path discussed in chat) - this WP delivers awareness data only, not reasoning over it.
* Any write/mutating git operation - read-only observation only.

## 4E. Update EBG-0083's EBR-0001 entry

Record Phase 3a's delivery in EBG-0083's existing Section 5 row (no new backlog number - matching how Phase 1a-1d were all recorded within the same row).

---

# 5. Validation Requirements

* New unit tests for `EngineeringStateObserver`/`RealGitStateReader` using a fake `GitStateReader` (success path, subprocess-failure propagation).
* New RPC-layer tests: exact camelCase serialization from a fixed fake `EngineeringSnapshot`; Guardian-independence (bare `StdioRpcServer` construction still resolves `gia.engineeringStatus`); default-wiring sanity (confirms the real `RealGitStateReader` is used when no observer is injected).
* **New per Codex design review**: a construction-is-side-effect-free test - constructing `RealGitStateReader`/`EngineeringStateObserver`/`GiaEngineeringAgent`/`StdioRpcServer` performs no subprocess call; the `git rev-parse --show-toplevel` resolution only happens on the first actual `snapshot()`/RPC/agent invocation.
* New agent-layer test mirroring `GiaObservabilityAgent`'s own test shape.
* Full suite: `pytest jarvis/tests sentinel scripts/tests` - must remain green, count disclosed.
* `python scripts/validate_repository.py` - 0 errors, warning count disclosed (unchanged expected).
* **Live verification against the real repository** (matching every prior GIA phase's own precedent): a real `gia.engineeringStatus` call compared directly against independently-run `git rev-parse --abbrev-ref HEAD` / `git status --porcelain` / `git log -1` on this actual repository - not fake-reader coverage alone.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* `gia.engineeringStatus` returns real, live-verified git state matching independently-confirmed ground truth.
* `gia-engineering` specialist agent invokable through the existing Agent Framework path, Sentinel-gated, classified `ROUTINE_INTERACTION`.
* No change to `gia.status`, `GiaObservabilityAgent`, `LocalResourceObserver`, or any existing GIA Phase 1 behaviour.
* No Sentinel policy, GAM-0001, or UXP change of any kind.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 28 August 2026 | Claude Engineering Implementer | Programme Sponsor approved via direct chat instruction ("Approved"), implemented exactly as scoped in v0.2: `jarvis/gia/engineering_observability.py` (new), `jarvis/agents/gia_engineering_agent.py` (new), `gia.engineeringStatus` RPC method, `gia-engineering` specialist agent registered in `build_default_runtime()`. 11 new tests, full suite 549 passed/1 skipped (was 538/1), `validate_repository.py` 0 errors/298 warnings (unchanged). Live-verified against this repository's real git state via both the RPC method and the Agent Framework path - matched independently-run `git` commands exactly. Pending commit/push through `submit-response` and the real Sponsor Approval Service. |
| 0.2 | 28 August 2026 | Claude Engineering Implementer | Codex Engineering Reviewer design review via the AIEMS Exchange Bridge - Conditional Pass with correction, folded in: repository-root resolution changed from eager (at `RealGitStateReader` construction) to lazy (on first git-command invocation, cached after success), so a missing `git` executable or transient failure cannot break unrelated runtime/RPC construction. Added a construction-is-side-effect-free test requirement. Documented the detached-`HEAD` literal-observation behaviour (non-blocking note). Not yet approved or implemented. |
| 0.1 | 28 August 2026 | Claude Engineering Implementer | ESR-0054 WP2 draft - GIA Phase 3a (Git State Observability), the first slice of EBG-0083 Phase 3. Not yet reviewed, approved or implemented. |
