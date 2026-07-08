# Repository Scripts

This directory contains lightweight repository maintenance utilities.

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
- governance-only changes do not include Python source or test files.

## Pre-commit Hook

A tracked pre-commit hook (`scripts/hooks/pre-commit`) runs the validator above and blocks the commit if it fails, so a version/status mismatch is caught before it's committed rather than only in CI afterward.

Git does not use tracked hooks by default - each clone needs to opt in once:

```text
git config core.hooksPath scripts/hooks
```
