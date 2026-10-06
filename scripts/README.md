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
- REG-0001 registered artefacts exist, and their versions and statuses match the documents' Document Control (every row shape, including `EIP-ESR####-###` and `JARVIS_*` IDs);
- the five live artefacts (README, COC-0001, PBK-0001, PCB-0001, the Capability Readiness Matrix) do not name a current baseline - PST-0001 is its single source (an error there, a warning elsewhere);
- "Section N" references resolve to a heading in this document or the artefact referred to (warnings);
- programme status references the latest repository baseline and engineering session;
- governance-only changes do not include Python source or test files;
- the pre-commit hook below is actually active on this clone (warning only, since it can't be enforced from inside the repository itself).

## Review Tooling (ESR-0061 WP1c)

- `python scripts/run_reviewer.py --tool antigravity|copilot --session ESR-#### --wp WPn --prompt-file FILE` runs an independent reviewer read-only through the AIEMS Exchange Bridge. The full prompt goes to a git-ignored file under `.aiems-exchange/reviews/`; the CLI receives only a shell-safe instruction to read it. It reports Copilot's quota failure (exit 3), an Antigravity refused-tool abort with the refused command (exit 4; continue with `--resume "message"`) and a run that recorded no verdict (exit 5). Antigravity always runs with a Gemini model.
- `python scripts/run_reviewer.py --check-settings` / `--install-settings` compares or merges `scripts/reviewer/antigravity_allowlist.json` into `~/.gemini/antigravity-cli/settings.json` (allow rules only; never deny rules). Change the allow-list only to add a genuinely read-only command, with a test in `scripts/tests/test_run_reviewer.py`.
- `python scripts/post_commit_precheck.py <commit> --session ESR-#### --wp WPn [--eip PATH --contents-heading "..."]` is the deterministic pre-check handed to the post-commit reviewer: clean tree, commit on `origin/main`, files equal to the EIP's Commit Contents, the approval gate against the parent, and pytest/ruff/validator clean. Count differences against the commit message are advisory only.
- `python scripts/local_prescreen.py [--base B --head H]` asks a local model (gpt-oss-20b via LM Studio) to pre-screen a diff. **Advisory only, never independent review**; it skips with exit 0 if LM Studio is not running.
- `python scripts/bump_version.py <ID> <VERSION> --summary "..." --author "Claude Engineering Implementer"` - `--author` is required.

## Pre-commit Hook

A tracked pre-commit hook (`scripts/hooks/pre-commit`) runs the validator above and blocks the commit if it fails, so a version/status mismatch is caught before it's committed rather than only in CI afterward.

Git does not use tracked hooks by default - each clone needs to opt in once:

```text
git config core.hooksPath scripts/hooks
```
