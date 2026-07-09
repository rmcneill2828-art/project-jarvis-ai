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


def latest_accepted_baseline(directory: Path) -> str | None:
    """Return the highest-numbered RBL file with Status: Accepted, or None.

    Unlike latest_numbered(), this only counts baselines that have actually
    been accepted. A Draft/recommended baseline file existing (e.g. one
    proposed at session closure but not yet accepted by the Programme
    Sponsor) does not make it the "current" baseline for this check -
    otherwise drafting a baseline recommendation would itself break the
    staleness check it's supposed to satisfy.
    """
    pattern = re.compile(r"^RBL-(\d{4})")
    status_pattern = re.compile(r"(?m)^\|\s*Status\s*\|\s*([^|\r\n]+?)\s*\|$")
    latest: tuple[int, str] | None = None
    for path in directory.glob("RBL-*.md"):
        match = pattern.match(path.name)
        if not match:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        status_match = status_pattern.search(text)
        if not status_match or status_match.group(1).strip() != "Accepted":
            continue
        number = int(match.group(1))
        artefact_id = f"RBL-{number:04d}"
        if latest is None or number > latest[0]:
            latest = (number, artefact_id)
    return latest[1] if latest else None


def latest_closed_numbered(prefix: str, directory: Path) -> str | None:
    """Return the highest-numbered artefact of this prefix with Status: Closed, or None.

    Mirrors latest_accepted_baseline()'s filtering approach. Unlike
    latest_numbered(), a file merely existing (e.g. a newly-opened session
    report, correctly Open rather than Closed) does not make it "latest" for
    staleness-checking purposes - otherwise PST-0001 would be required to
    reference a session before that session has actually closed, which
    directly contradicts PBK-0001 WP0B (PST-0001 must not reference an
    unclosed session). Found via ESR-0017: this check fired an ERROR the
    moment ESR-0017 opened, purely because it existed, despite the error
    message itself already claiming to check for "latest closed session".
    """
    pattern = re.compile(rf"^{re.escape(prefix)}-(\d{{4}})")
    status_pattern = re.compile(r"(?m)^\|\s*Status\s*\|\s*([^|\r\n]+?)\s*\|$")
    latest: tuple[int, str] | None = None
    for path in directory.glob(f"{prefix}-*.md"):
        match = pattern.match(path.name)
        if not match:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        status_match = status_pattern.search(text)
        if not status_match or status_match.group(1).strip() != "Closed":
            continue
        number = int(match.group(1))
        artefact_id = f"{prefix}-{number:04d}"
        if latest is None or number > latest[0]:
            latest = (number, artefact_id)
    return latest[1] if latest else None


def check_stale_status_references(result: ValidationResult) -> None:
    latest_rbl = latest_numbered("RBL", REPO_ROOT / "aiems/governance/baselines")
    latest_accepted_rbl = latest_accepted_baseline(REPO_ROOT / "aiems/governance/baselines")
    latest_esr = latest_closed_numbered("ESR", REPO_ROOT / "aiems/governance/sessions")
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
    if latest_accepted_rbl and current_baseline and current_baseline.group(1) != latest_accepted_rbl:
        result.error(
            f"PST-0001 current repository baseline is {current_baseline.group(1)}, "
            f"latest accepted is {latest_accepted_rbl}."
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


HEADING_NUMBER_PATTERN = re.compile(r"(?m)^#{1,6}\s+(\d+(?:\.\d+)*)\.?\s+\S")
SECTION_REF_PATTERN = re.compile(r"\bSections?\s+(\d+(?:\.\d+)*)\b")
WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
ARTEFACT_ID_PATTERN = re.compile(r"^([A-Z]{2,6}-\d{3,4}[A-Z]?)")
HISTORICAL_ARCHIVE_DIR = REPO_ROOT / "aiems" / "History"


def _is_historical_archive(path: Path) -> bool:
    """HST/FCH artefacts are frozen historical chat records (GDE-0001 tier),
    not actively-maintained structured documents - "Section 5" in a chat
    transcript doesn't mean a document heading, so they're excluded here
    rather than producing structural noise."""

    try:
        path.relative_to(HISTORICAL_ARCHIVE_DIR)
    except ValueError:
        return False
    return True


def extract_heading_numbers(text: str) -> set[str]:
    return set(HEADING_NUMBER_PATTERN.findall(text))


def _build_artefact_id_index(files: list[Path]) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in files:
        match = ARTEFACT_ID_PATTERN.match(path.stem)
        if match:
            index[match.group(1)] = path
    return index


def _referenced_artefact(preceding: str, file_by_basename: dict[str, Path], id_index: dict[str, Path]) -> Path | None:
    """Resolve what "Section N" actually refers to, from the text immediately
    before it - not anywhere earlier in the sentence.

    Real repository writing has two adjacent-reference patterns:
    "[[EE-0001|EE-0001]] Section 5.6" (WikiLink immediately before) and bare
    "EE-0001 Section 5.6" (no link at all). Both are checked only when the
    referent is the *immediately* preceding token, stripped of a trailing
    possessive - anything looser (a link or ID mentioned earlier in the same
    sentence but not immediately adjacent) produced false positives in
    practice and is deliberately not treated as a cross-reference signal.
    """

    trimmed = preceding.rstrip()
    if trimmed.endswith("'s"):
        trimmed = trimmed[: -len("'s")].rstrip()

    if trimmed.endswith("]]"):
        # The *last* link ending exactly here, not just any link somewhere
        # in a lookback window - a line can legitimately mention several
        # artefacts before the one actually adjacent to "Section N".
        link_matches = list(WIKILINK_PATTERN.finditer(trimmed))
        if link_matches and link_matches[-1].end() == len(trimmed):
            target = link_matches[-1].group(1)
            if target in file_by_basename:
                return file_by_basename[target]
            id_match = ARTEFACT_ID_PATTERN.match(target)
            if id_match and id_match.group(1) in id_index:
                return id_index[id_match.group(1)]
        return None

    bare_match = re.search(r"([A-Z]{2,6}-\d{3,4}[A-Z]?)$", trimmed)
    if bare_match and bare_match.group(1) in id_index:
        return id_index[bare_match.group(1)]

    return None


def check_section_references(result: ValidationResult) -> None:
    """Warn (not error - see WP3 EIP) when a "Section N" reference doesn't
    match any heading, in the current document or an immediately-adjacent
    cross-referenced one. See _referenced_artefact for the adjacency rule
    and why it's deliberately tight rather than scanning the whole sentence.
    """

    files = [p for p in iter_markdown_files() if not _is_historical_archive(p)]
    file_by_basename = {path.stem: path for path in files}
    id_index = _build_artefact_id_index(files)
    heading_cache: dict[Path, set[str]] = {}

    def headings_for(path: Path) -> set[str]:
        if path not in heading_cache:
            heading_cache[path] = extract_heading_numbers(
                path.read_text(encoding="utf-8", errors="replace")
            )
        return heading_cache[path]

    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        own_headings = headings_for(path)
        for line_num, line in enumerate(text.splitlines(), start=1):
            if re.match(r"^#{1,6}\s", line):
                continue
            for match in SECTION_REF_PATTERN.finditer(line):
                section_number = match.group(1)
                preceding = line[: match.start()]
                target_path = _referenced_artefact(preceding, file_by_basename, id_index)
                if target_path is not None and target_path != path:
                    target_headings = headings_for(target_path)
                    target_desc = target_path.stem
                else:
                    target_headings = own_headings
                    target_desc = "this document"
                if section_number not in target_headings:
                    rel = path.relative_to(REPO_ROOT)
                    result.warn(
                        f"{rel}:{line_num} references Section {section_number}, "
                        f"not found as a heading in {target_desc}."
                    )


def check_precommit_hook_installed(result: ValidationResult) -> None:
    """Warn if the tracked pre-commit hook isn't active on this clone.

    scripts/hooks/pre-commit runs this same validator and blocks a bad commit,
    but git only uses tracked hooks once core.hooksPath is configured per
    clone - there's no way to make that the default from inside the repo
    itself, so a missed opt-in is otherwise silent until CI runs.
    """

    completed = subprocess.run(
        ["git", "config", "core.hooksPath"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    configured = completed.stdout.strip()
    if configured != "scripts/hooks":
        result.warn(
            "Pre-commit governance hook is not active on this clone "
            "(run: git config core.hooksPath scripts/hooks) - "
            "commits will only be checked by CI, not before commit."
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
    check_precommit_hook_installed(result)
    check_section_references(result)
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
