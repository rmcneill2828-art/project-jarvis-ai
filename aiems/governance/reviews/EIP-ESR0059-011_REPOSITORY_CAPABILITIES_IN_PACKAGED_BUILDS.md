# EIP-ESR0059-011 - Repository-Reading Capabilities in Packaged Builds

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-011 |
| Title | Engineering Implementation Package: WP11 Repository-Reading Capabilities in Packaged Builds |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP11 |

---

# 2. Purpose

Implements ESR-0059 WP11, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0148, under the Programme Sponsor's standing instruction to proceed with the review's action plan and backlog.

EBG-0148 was registered as "most likely errors in a packaged install - verify first". **Verified first, against a real packaged build** (`scripts/build_backend_sidecar.py`, run from a directory outside the repository, as an installed app is): `platform.status`, `gia.status` and `guardian.converse` worked; `knowledge.graph` and `gia.engineeringStatus` both failed with a raw `CalledProcessError` whose message exposed the PyInstaller temporary extraction path (`_MEI...`) - the EBG-0050 residual concern, in practice.

---

# 3. Repository Context Investigated

* `jarvis/interfaces/knowledge_graph.py` - `REPO_ROOT` derived from `__file__`, then `git ls-files` with `check=True`.
* `jarvis/gia/engineering_observability.py` - `git -C <module dir> rev-parse --show-toplevel`, then git commands and `scripts/validate_repository.py`.
* In the packaged build, `__file__` is inside the temporary extraction directory, which is not a checkout.
* The Guardian Orb and Knowledge panels already have an error state; engineering status is reached through the agent panel.

**A second, more serious defect found while verifying the fix, not by review**: with a repository configured, the packaged backend's engineering status hung. `repository_validation()` ran the validator with `sys.executable` - which in a PyInstaller build is the backend executable itself, not Python. It started a second backend, and because the child inherited the backend's stdin - the JSON-RPC request stream - that second backend could read requests meant for the first.

---

# 4. Scope

## 4A. Repository resolution (`jarvis/repository.py`, new)

* `resolve_repository_root()`: `JARVIS_REPOSITORY_ROOT` when set, otherwise the checkout this package sits in, recognised by its `.git` entry (directory or worktree file) without running git.
* `RepositoryUnavailableError` - path-free: "No JARVIS source repository is available to this installation. Set JARVIS_REPOSITORY_ROOT to a git checkout of the project to enable this."
* Used by `knowledge_graph.build_graph()` and `RealEngineeringStateReader`. A git failure inside a checkout (git missing, not a repository) becomes a path-free `RepositoryUnavailableError`, never `str()` of the underlying error.

## 4B. Child processes in the stdio backend

* Every child process the backend starts - both git calls and the validator - now runs with `stdin=subprocess.DEVNULL`. A test enforces it across all three call sites, which are the only `subprocess` uses in `jarvis/` and `sentinel/`.
* `_script_interpreter()`: from source, the running interpreter; in a packaged build, a Python found on `PATH` - never the backend executable - with a clear error if there is none.
* The validator run has a 120s timeout, and its failure messages no longer include a local path.

## 4C. Tests

New `jarvis/tests/test_repository_resolution.py` (14): default and configured resolution; path-free unavailability; a configured non-checkout is unavailable; knowledge graph and engineering status both unavailable in a simulated packaged install; a git failure reported without paths; both RPC methods return the exact clean message with no `_MEI` path or `CalledProcessError`; setting the variable restores both; interpreter choice from source, packaged with Python, packaged without; stdin closed for every child process; validator timeout.

## 4D. Explicitly out of scope

* Bundling a knowledge-graph snapshot into the installer so the Orb renders without a repository - a product decision for the Programme Sponsor.
* Sanitising exception text in `handle_line()` generally (EBG-0050's residual). This package removes the one instance found leaking in practice.

## 4E. Review

**Review - disclosed self-review** (GitHub Copilot CLI quota re-probed, still exhausted; EBG-0153 applies). Checked: every `subprocess` call in `jarvis/` and `sentinel/` enumerated - exactly three, all now with closed stdin, enforced by a test; resolution by `.git` presence cannot fail merely because git is absent, and git's own failures are converted without echoing their command line; `_script_interpreter()` can never return the frozen executable; the cached `_repo_root` behaviour the existing observer tests depend on is unchanged; the live re-verification covered both configurations on a freshly rebuilt package, and left no stray processes. No further change needed.

---

# 5. Validation Requirements

* `python -m pytest -q`, `ruff check .`, `python scripts/validate_repository.py`.

## 5A. Live check - performed against a real packaged build

The sidecar was rebuilt with `scripts/build_backend_sidecar.py` and run from a directory outside the repository:

| Configuration | `knowledge.graph` | `gia.engineeringStatus` | `platform.status` after |
|---|---|---|---|
| No repository (before fix) | raw `CalledProcessError` with `_MEI...` path | same | - |
| No repository (after fix) | clean unavailable message | clean unavailable message | Running |
| `JARVIS_REPOSITORY_ROOT` set (before stdin/interpreter fix) | 325 nodes | hung; run timed out | - |
| `JARVIS_REPOSITORY_ROOT` set (after fix) | 325 nodes | 2.9s: branch `main`, 0 validation errors, RBL-0038 | Running |

No stray backend processes remained afterwards.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* In a packaged install, repository-reading methods report their unavailability plainly, with no internal paths.
* With `JARVIS_REPOSITORY_ROOT` set, both work in a packaged install.
* No child process can read the backend's JSON-RPC request stream.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** on the disclosed self-review. Implemented exactly as at v0.2. Pending commit/push through `submit-response`. |
| 0.2 | 29 September 2026 | Claude Engineering Implementer | Disclosed self-review recorded in Section 4E (Copilot CLI quota still exhausted). Retrospective Copilot review owed (EBG-0153). Not yet approved or committed. |
| 0.1 | 29 September 2026 | Claude Engineering Implementer | ESR-0059 WP11 draft. EBG-0148 verified against a real packaged build, then fixed: shared repository resolver with `JARVIS_REPOSITORY_ROOT` and a path-free unavailable error. A second defect found while verifying - the packaged backend re-launching itself as "Python" with the RPC stream as the child's stdin - fixed. pytest 721 passed/1 skipped, ruff clean. Re-verified on a rebuilt packaged build in both configurations. Not yet reviewed, approved or committed. |
