# Repository Scripts

This directory contains lightweight repository maintenance utilities.

## Setting Up a New Clone

Run `setup.bat` (repo root, double-click or from a terminal) or `scripts/setup-dev-environment.ps1` directly. It first checks prerequisites (see [PREREQUISITES.md](PREREQUISITES.md)), then installs npm dependencies, builds the Rust/Tauri backend, creates/updates the Python virtual environment (`.venv`, via `pip install -e ".[dev]"`), activates the tracked pre-commit hook (see below), and runs the validator and test suite as a smoke test. Safe to re-run at any time - useful after pulling changes that touch dependencies.

On a brand new machine, see [PREREQUISITES.md](PREREQUISITES.md) for the baseline software needed and for running just the prerequisite check (`scripts/check-prerequisites.ps1`) on its own.

`node_modules/`, `src-tauri/target/`, and `.venv/` are all gitignored - they are rebuilt locally from `package-lock.json`, `Cargo.lock`, and `pyproject.toml` respectively, not carried between machines.

## Repository Validation

Run:

```text
python scripts/validate_repository.py
```

For documentation/governance-only packages, run:

```text
python scripts/validate_repository.py --governance-only
```

The validation script checks:

- repository WikiLinks resolve to Markdown artefacts;
- REG-0001 registered artefacts exist and versions match where parseable;
- programme status references the latest repository baseline and engineering session;
- governance-only changes do not include Python source or test files;
- the pre-commit hook below is actually active on this clone (warning only, since it can't be enforced from inside the repository itself).

## Pre-commit Hook

A tracked pre-commit hook (`scripts/hooks/pre-commit`) runs the validator above and blocks the commit if it fails, so a version/status mismatch is caught before it's committed rather than only in CI afterward.

Git does not use tracked hooks by default - each clone needs to opt in once:

```text
git config core.hooksPath scripts/hooks
```
