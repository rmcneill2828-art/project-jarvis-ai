"""Repository validation checks for Project JARVIS AI.

This script performs lightweight repository-first checks that are useful before
baseline acceptance or governance-only commits.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", ".obsidian", ".pytest_cache", ".ruff_cache", "__pycache__", ".venv", "venv"}


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def iter_markdown_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO_ROOT.rglob("*.md"):
        if any(part in IGNORED_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def markdown_basenames(files: list[Path]) -> set[str]:
    return {path.stem for path in files}


def check_wikilinks(result: ValidationResult) -> None:
    files = iter_markdown_files()
    basenames = markdown_basenames(files)
    link_pattern = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in link_pattern.finditer(text):
            target = match.group(1)
            if target not in basenames:
                rel = path.relative_to(REPO_ROOT)
                result.error(f"Unresolved WikiLink in {rel}: [[{target}]]")


def parse_register_rows(register_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in register_path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("| "):
            continue
        if "Artefact ID" in line or line.startswith("|-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        artefact_id = cells[0]
        wikilink_id = re.match(r"\[\[[^\]|]+(?:\|([^\]]+))?\]\]", artefact_id)
        if wikilink_id:
            artefact_id = wikilink_id.group(1) or artefact_id
        if not re.match(r"^[A-Z]+-\d{4}$", artefact_id):
            continue
        rows.append(
            {
                "id": artefact_id,
                "type": cells[1],
                "title": cells[2],
                "version": cells[3],
                "status": cells[4],
                "location": cells[7].strip("`"),
            }
        )
    return rows


def extract_document_version(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    table_match = re.search(r"(?m)^\|\s*Version\s*\|\s*([^|\r\n]+?)\s*\|$", text)
    if table_match:
        return table_match.group(1).strip()
    bold_match = re.search(r"(?m)^\*\*Version:\*\*\s*([^\r\n]+)", text)
    if bold_match:
        return bold_match.group(1).strip()
    return None


def find_registered_file(artefact_id: str, location: str) -> Path | None:
    if not location or location == "-":
        return None
    base = REPO_ROOT / location
    if not base.exists():
        return None
    matches = sorted(base.glob(f"{artefact_id}*.md"))
    return matches[0] if matches else None


def check_controlled_register(result: ValidationResult) -> None:
    register_path = REPO_ROOT / "aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md"
    if not register_path.exists():
        result.error("REG-0001 controlled artefact register is missing.")
        return

    for row in parse_register_rows(register_path):
        path = find_registered_file(row["id"], row["location"])
        if path is None:
            result.error(f"{row['id']} is registered but no matching file was found under {row['location']}.")
            continue
        document_version = extract_document_version(path)
        if document_version is None:
            result.warn(f"{row['id']} has no parseable document version in {path.relative_to(REPO_ROOT)}.")
            continue
        if document_version != row["version"]:
            rel = path.relative_to(REPO_ROOT)
            result.error(
                f"{row['id']} version mismatch: REG-0001={row['version']} file={document_version} path={rel}"
            )


def latest_numbered(prefix: str, directory: Path) -> str | None:
    pattern = re.compile(rf"^{re.escape(prefix)}-(\d{{4}})")
    latest: tuple[int, str] | None = None
    for path in directory.glob(f"{prefix}-*.md"):
        match = pattern.match(path.name)
        if not match:
            continue
        number = int(match.group(1))
        artefact_id = f"{prefix}-{number:04d}"
        if latest is None or number > latest[0]:
            latest = (number, artefact_id)
    return latest[1] if latest else None


def extract_current_esr_reference(text: str) -> str | None:
    match = re.search(r"\| Current Mode \| \[\[(ESR-\d{4})[A-Z]?_", text)
    return match.group(1) if match else None


def check_stale_status_references(result: ValidationResult) -> None:
    latest_rbl = latest_numbered("RBL", REPO_ROOT / "aiems/governance/baselines")
    latest_esr = latest_numbered("ESR", REPO_ROOT / "aiems/governance/sessions")
    status_path = REPO_ROOT / "aiems/governance/status/PST-0001_PROGRAMME_STATUS.md"
    if not status_path.exists():
        result.error("PST-0001 programme status artefact is missing.")
        return

    text = status_path.read_text(encoding="utf-8", errors="replace")
    if latest_rbl and latest_rbl not in text:
        result.warn(f"PST-0001 does not reference latest repository baseline {latest_rbl}.")

    current_esr = extract_current_esr_reference(text)
    if latest_esr and current_esr != latest_esr:
        result.error(
            f"PST-0001 Current Mode references {current_esr or 'no ESR'}, "
            f"latest closed session is {latest_esr}."
        )

    current_baseline = re.search(r"\| Current Repository Baseline \| \[\[(RBL-\d{4})_", text)
    if latest_rbl and current_baseline and current_baseline.group(1) != latest_rbl:
        result.error(
            f"PST-0001 current repository baseline is {current_baseline.group(1)}, latest is {latest_rbl}."
        )

    for path in [REPO_ROOT / "README.md", status_path]:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"current accepted repository baseline[^\n]*\[\[(RBL-\d{4})_", content, re.I):
            if latest_rbl and match.group(1) != latest_rbl:
                result.warn(
                    f"{path.relative_to(REPO_ROOT)} may contain stale current-baseline wording: {match.group(1)}"
                )


def git_changed_files(staged: bool) -> list[str]:
    args = ["git", "diff", "--name-only"]
    if staged:
        args.insert(2, "--cached")
    completed = subprocess.run(args, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        return []
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def check_governance_only_scope(result: ValidationResult) -> None:
    changed = set(git_changed_files(staged=False)) | set(git_changed_files(staged=True))
    for path in sorted(changed):
        normalized = path.replace("\\", "/")
        product_source = normalized.startswith("jarvis/") and normalized.endswith(".py")
        tests = "/tests/" in normalized or normalized.startswith("tests/")
        if product_source or tests:
            result.error(f"Governance-only scope violation: {path}")


def run_validation(governance_only: bool) -> ValidationResult:
    result = ValidationResult(errors=[], warnings=[])
    check_wikilinks(result)
    check_controlled_register(result)
    check_stale_status_references(result)
    if governance_only:
        check_governance_only_scope(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Project JARVIS AI repository governance health.")
    parser.add_argument(
        "--governance-only",
        action="store_true",
        help="Fail if staged or unstaged changes include Python source or test files.",
    )
    args = parser.parse_args()

    result = run_validation(governance_only=args.governance_only)

    for warning in result.warnings:
        print(f"WARNING: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")

    if result.errors:
        print(f"Repository validation failed: {len(result.errors)} error(s), {len(result.warnings)} warning(s).")
        return 1

    print(f"Repository validation passed: 0 errors, {len(result.warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
