# EIP-ESR0059-002 - Restore the CI Python Gate

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-002 |
| Title | Engineering Implementation Package: WP2 Restore the CI Python Gate |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP2 |

---

# 2. Purpose

Implements ESR-0059 WP2, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0152: the CI `python` job has failed on every push to `main` since ESR-0040 WP1 (29 July 2026), because its first step, `ruff check .`, fails. `pytest`, `validate_repository.py`, `sync_product_version.py --check` and `pip-audit` have therefore not run in CI for two months. Selected by the Programme Sponsor as the first of four outstanding decisions ("start from 1. and work your way down").

---

# 3. Repository Context Investigated

* GitHub Actions history (`gh run list`/`gh run view`), independently confirmed by the Engineering Reviewer at WP1: last green `main` run 2026-07-29T11:35Z; every push since red; only the `python` job fails, at `ruff check .`.
* `ruff check .` on the clean ESR-0059 WP1 tree: 13 errors - 10 `RUF100` unused `noqa` directives (for rules the configuration does not enable: `SLF001`, `PLC0415`) and 1 `I001` across three test files, 1 `PLW1510` in `jarvis/gia/engineering_observability.py`, 1 `TRY004` in `jarvis/memory/store.py`.
* `pyproject.toml` `dev` extra: `ruff` unpinned, so CI installs whatever ruff is newest - a new release can add rules and turn the job red with no code change.
* **Second gate that would have failed next, found by running the job's later steps locally**: `pip-audit` reports PYSEC-2026-3721 against `pip` 26.1.2 itself (fixed in 26.2). EBG-0124 (ESR-0052) made `pip-audit` a hard gate while CI was already red at the ruff step, so that hard gate has never actually executed in CI. Whether the runner image's pip is affected depends on the image, so the fix makes the step independent of it.
* `ruff check --fix` was tried first and reverted: its `RUF100` fix deleted each rationale comment along with the unused `noqa` marker (for example "avoids a module-level import cycle"), discarding documentation. Replaced with a targeted edit that removes only the `noqa: RULE` marker and keeps the rationale as a plain comment.

---

# 4. Scope

## 4A. Lint fixes (no behaviour change)

* `jarvis/tests/test_activity_tracker.py`, `jarvis/tests/test_gia_engineering_observability.py`, `jarvis/tests/test_identity_store.py`: ten unused `noqa: SLF001`/`noqa: PLC0415` markers removed; every rationale kept as an ordinary comment. This also clears the `I001`.
* `jarvis/gia/engineering_observability.py`: `subprocess.run(..., check=False)` made explicit, with a comment - `validate_repository.py` exits non-zero exactly when it finds errors, which this observer reports rather than raises. Identical runtime behaviour (`check` already defaulted to `False`).
* `jarvis/memory/store.py`: the pre-existing `TRY004` suppressed with the same documented-`noqa` pattern WP1 used - `ValueError` is `import_snapshot()`'s public invalid-backup contract, asserted by its tests.

## 4B. Keep it green

* `pyproject.toml`: `ruff==0.16.0` pinned in the `dev` extra, with a comment. Dependabot (EBG-0123) proposes future bumps as reviewable changes.
* `.github/workflows/ci.yml` `python` job: `python -m pip install --upgrade pip` before the project install, so the hard `pip-audit` gate audits the project rather than the runner's own pip.

## 4C. Governance

* [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0152 closed Completed.
* [[ESR-0059_ENGINEERING_SESSION_REPORT|ESR-0059]] WP2 recorded.

## 4D. Explicitly out of scope

* **Branch protection** (a required `python` status check on `main`) - a GitHub repository-settings change, not a repository file, and outward-facing. Recommended to the Programme Sponsor as the step that stops a red gate going unnoticed again; not applied here.
* Any other workflow, job or dependency change.

---

# 5. Validation Requirements

* The whole CI `python` job reproduced locally, in order, in a **fresh** virtual environment (not the development `.venv`): pip upgrade, `pip install -e .[dev]`, `ruff check .`, `sync_product_version.py --check`, `pytest -q`, `validate_repository.py`, `pip-audit`.
* After commit and push: the real CI run on `main` is green for all four jobs.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* `ruff check .` reports no errors, with no rationale comment lost.
* Every step of the CI `python` job passes in a fresh environment.
* The first CI run on `main` after this package is green on all four jobs.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 28 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")**. Implemented exactly as design-reviewed at v0.2. Pending commit/push through `submit-response`. The Programme Sponsor also directed applying the branch-protection recommendation (Section 4D), done after this package's commit as a GitHub settings change, recorded in ESR-0059. |
| 0.2 | 28 September 2026 | Claude Engineering Implementer | Design-reviewed via a genuine scoped GitHub Copilot CLI invocation routed through the real bridge (`ESR-0059`/`WP2`, complete 11-file scope) - **Pass**, single `return-findings` entry. Confirmed ruff clean with the installed ruff matching the 0.16.0 pin; all 10 `noqa` removals kept their rationale with zero test-logic change; `check=False` behaviour-identical; the `TRY004` suppression justified by tests asserting `ValueError`; the CI diff touches only the `python` job; exactly 11 files changed. Re-ran pytest (616 passed/1 skipped), the validator (0 errors/333 warnings) and the version-sync check. One caveat, correctly scoped rather than a defect: `pip-audit` still flags pip 26.1.2 in the local development environment, because the fix upgrades pip only in CI - the fresh-environment reproduction already showed `pip-audit` passing once pip is upgraded. Not yet approved or committed. |
| 0.1 | 28 September 2026 | Claude Engineering Implementer | ESR-0059 WP2 draft. EBG-0152 fixed: 13 ruff errors cleared without losing any rationale comment (ruff's own autofix tried and reverted for deleting them), ruff pinned to 0.16.0, pip upgraded before the hard pip-audit gate (a second failure found by running the job's later steps locally). Full CI python job reproduced green in a fresh virtual environment: ruff clean, version sync agrees, pytest 616 passed/1 skipped, validator 0 errors/333 warnings, pip-audit no known vulnerabilities. Not yet reviewed, approved or committed. |
