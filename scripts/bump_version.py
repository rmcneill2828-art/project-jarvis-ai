"""Bump a controlled artefact's version and keep REG-0001 in sync.

Replaces the three-touch manual pattern (artefact's own version fields,
REG-0001's row for that artefact, REG-0001's own self-row and version,
since editing REG-0001 is itself a REG-0001 change) with one command.

Usage:
    python scripts/bump_version.py <ARTEFACT_ID> <NEW_VERSION> --summary "..."
        [--author "Claude Engineering Reviewer"] [--date "9 July 2026"]

This is mechanical only. It does not decide what changed - the --summary
text is required and inserted verbatim into both Version History tables.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_repository import (  # noqa: E402
    REPO_ROOT,
    extract_document_version,
    find_registered_file,
    parse_register_rows,
)

REGISTER_PATH = REPO_ROOT / "aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md"
DEFAULT_AUTHOR = "Claude Engineering Reviewer"


class BumpVersionError(Exception):
    """Raised when the requested bump cannot be applied safely."""


@dataclass
class PlannedEdit:
    path: Path
    text: str


def _bump_version_fields(text: str, old_version: str, new_version: str, path: Path) -> str:
    badge_pattern = re.compile(
        rf"(?m)^(\*\*Version:\*\*\s*){re.escape(old_version)}[ \t]*$"
    )
    table_pattern = re.compile(
        rf"(?m)^(\|\s*Version\s*\|\s*){re.escape(old_version)}(\s*\|)[ \t]*$"
    )

    updated, badge_count = badge_pattern.subn(rf"\g<1>{new_version}", text)
    updated, table_count = table_pattern.subn(rf"\g<1>{new_version}\g<2>", updated)

    if badge_count == 0 and table_count == 0:
        rel = path.relative_to(REPO_ROOT)
        raise BumpVersionError(
            f"No '**Version:**' badge or Document Control 'Version' row reading "
            f"'{old_version}' found in {rel} - refusing to guess."
        )
    return updated


def _insert_version_history_row(text: str, row: str, path: Path) -> str:
    heading_pattern = re.compile(r"(?m)^#{1,2}\s+(?:\d+\.\s*)?Version History\s*$")
    heading_match = heading_pattern.search(text)
    if not heading_match:
        rel = path.relative_to(REPO_ROOT)
        raise BumpVersionError(f"No 'Version History' section found in {rel}.")

    separator_pattern = re.compile(r"\n(\|-{2,}[-|]*\|)\n")
    separator_match = separator_pattern.search(text, heading_match.end())
    if not separator_match:
        rel = path.relative_to(REPO_ROOT)
        raise BumpVersionError(f"No Version History table separator found in {rel}.")

    insert_at = separator_match.end()
    return text[:insert_at] + row + "\n" + text[insert_at:]


def _next_register_version(current: str) -> str:
    match = re.match(r"^(\d+)\.(\d+)$", current.strip())
    if not match:
        raise BumpVersionError(f"REG-0001's own version '{current}' is not in X.Y form - refusing to guess.")
    major, minor = match.groups()
    return f"{major}.{int(minor) + 1}"


def _update_register_row(text: str, artefact_id: str, new_version: str) -> str:
    row_pattern = re.compile(
        rf"(?m)^(\|\s*(?:\[\[{re.escape(artefact_id)}[^\]]*\|)?{re.escape(artefact_id)}\]?\]?\s*\|(?:[^|]*\|){{2}}\s*)([^|]+?)(\s*\|)"
    )
    updated, count = row_pattern.subn(rf"\g<1>{new_version}\g<3>", text, count=1)
    if count != 1:
        raise BumpVersionError(f"Could not find exactly one REG-0001 row for {artefact_id} to update version.")
    return updated


def plan_bump(artefact_id: str, new_version: str, summary: str, author: str, date: str) -> list[PlannedEdit]:
    if not REGISTER_PATH.exists():
        raise BumpVersionError("REG-0001 controlled artefact register is missing.")

    register_text = REGISTER_PATH.read_text(encoding="utf-8", errors="replace")
    rows = {row["id"]: row for row in parse_register_rows(REGISTER_PATH)}
    if artefact_id not in rows:
        raise BumpVersionError(f"{artefact_id} is not registered in REG-0001.")

    row = rows[artefact_id]
    artefact_path = find_registered_file(artefact_id, row["location"])
    if artefact_path is None:
        raise BumpVersionError(f"{artefact_id} is registered but no file was found under {row['location']}.")

    old_version = extract_document_version(artefact_path)
    if old_version is None:
        raise BumpVersionError(f"Could not parse {artefact_id}'s current version.")
    if old_version == new_version:
        raise BumpVersionError(f"{artefact_id} is already at version {new_version}.")

    artefact_text = artefact_path.read_text(encoding="utf-8", errors="replace")
    artefact_text = _bump_version_fields(artefact_text, old_version, new_version, artefact_path)
    artefact_row = f"| {new_version} | {date} | {author} | {summary} |"
    artefact_text = _insert_version_history_row(artefact_text, artefact_row, artefact_path)

    reg_text = _update_register_row(register_text, artefact_id, new_version)

    reg_row = {r["id"]: r for r in parse_register_rows(REGISTER_PATH)}["REG-0001"]
    reg_old_version = reg_row["version"]
    reg_new_version = _next_register_version(reg_old_version)
    reg_summary = f"Aligned {artefact_id} version ({old_version} to {new_version}) following: {summary}"
    reg_text = _update_register_row(reg_text, "REG-0001", reg_new_version)
    reg_text = _bump_version_fields(reg_text, reg_old_version, reg_new_version, REGISTER_PATH)
    reg_row_entry = f"| {reg_new_version} | {date} | {author} | {reg_summary} |"
    reg_text = _insert_version_history_row(reg_text, reg_row_entry, REGISTER_PATH)

    return [
        PlannedEdit(path=artefact_path, text=artefact_text),
        PlannedEdit(path=REGISTER_PATH, text=reg_text),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artefact_id", help="Registered artefact ID, e.g. SAM-0001")
    parser.add_argument("new_version", help="New version string, e.g. 0.4")
    parser.add_argument("--summary", required=True, help="What changed - inserted verbatim into Version History")
    parser.add_argument("--author", default=DEFAULT_AUTHOR)
    parser.add_argument("--date", default="9 July 2026")
    args = parser.parse_args()

    try:
        edits = plan_bump(args.artefact_id, args.new_version, args.summary, args.author, args.date)
    except BumpVersionError as exc:
        print(f"ERROR: {exc}")
        print("No files were changed.")
        return 1

    for edit in edits:
        edit.path.write_text(edit.text, encoding="utf-8")
        print(f"Updated {edit.path.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
