"""Synchronise the product release version across all build-tool manifests
(EBG-0104, EIP-ESR0032-003).

`VERSION` (repo root, plain text, single `X.Y.Z` line) is the single
authoritative source - deliberately not one of `pyproject.toml`,
`package.json`, `src-tauri/Cargo.toml` or `src-tauri/tauri.conf.json`
themselves, since each is a tool-specific manifest (Python packaging, npm,
Cargo, Tauri app config) with its own unrelated fields; picking one as
"primary" would arbitrarily couple the other three ecosystems to that
tool's file format.

Usage:
    python scripts/sync_product_version.py <NEW_VERSION>
        Updates VERSION and propagates it into all four build files.

    python scripts/sync_product_version.py --check
        Verifies VERSION and all four build files already agree; writes
        nothing. Used as a CI gate (EIP-ESR0032-003 Section 5 item 3).

This is mechanical only, matching `scripts/bump_version.py`'s own
established convention in this repository: refuse to guess or silently
skip a file whose version field cannot be found or parsed.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = REPO_ROOT / "VERSION"

VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")

# (path relative to REPO_ROOT, pattern with the version value in group 2)
TARGETS: list[tuple[str, re.Pattern[str]]] = [
    ("pyproject.toml", re.compile(r'(?m)^(version = ")([^"]+)(")$')),
    ("package.json", re.compile(r'(?m)^(  "version": ")([^"]+)(",)$')),
    ("src-tauri/Cargo.toml", re.compile(r'(?m)^(version = ")([^"]+)(")$')),
    ("src-tauri/tauri.conf.json", re.compile(r'(?m)^(  "version": ")([^"]+)(",)$')),
]


class VersionSyncError(Exception):
    """Raised when the version cannot be synced or checked safely."""


@dataclass
class PlannedEdit:
    path: Path
    text: str


def _current_version() -> str | None:
    if not VERSION_FILE.exists():
        return None
    text = VERSION_FILE.read_text(encoding="utf-8").strip()
    return text or None


def _find_version(relative: str, pattern: re.Pattern[str]) -> str:
    path = REPO_ROOT / relative
    if not path.exists():
        raise VersionSyncError(f"{relative} does not exist.")
    text = path.read_text(encoding="utf-8")
    match = pattern.search(text)
    if match is None:
        raise VersionSyncError(f"Could not find a version field in {relative} - refusing to guess.")
    return match.group(2)


def plan_sync(new_version: str) -> list[PlannedEdit]:
    if not VERSION_PATTERN.match(new_version):
        raise VersionSyncError(f"'{new_version}' is not a plain X.Y.Z version - refusing to guess.")

    if _current_version() == new_version:
        raise VersionSyncError(f"Already at version {new_version}.")

    edits = [PlannedEdit(path=VERSION_FILE, text=new_version + "\n")]

    for relative, pattern in TARGETS:
        _find_version(relative, pattern)  # raises if missing/unparseable
        path = REPO_ROOT / relative
        text = path.read_text(encoding="utf-8")
        updated, count = pattern.subn(rf"\g<1>{new_version}\g<3>", text, count=1)
        if count != 1:
            raise VersionSyncError(f"Could not update version field in {relative}.")
        edits.append(PlannedEdit(path=path, text=updated))

    return edits


def check_synced() -> list[str]:
    """Return a list of human-readable mismatch descriptions - empty if all
    four build files agree with VERSION."""

    current = _current_version()
    if current is None:
        return ["VERSION file is missing or empty."]

    mismatches = []
    for relative, pattern in TARGETS:
        try:
            found = _find_version(relative, pattern)
        except VersionSyncError as exc:
            mismatches.append(str(exc))
            continue
        if found != current:
            mismatches.append(f"{relative} is at {found}, VERSION is {current}.")

    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("new_version", nargs="?", help="New version string, e.g. 0.2.0")
    parser.add_argument(
        "--check", action="store_true", help="Verify all files agree with VERSION; write nothing."
    )
    args = parser.parse_args()

    if args.check:
        mismatches = check_synced()
        if mismatches:
            print("ERROR: version drift detected:")
            for mismatch in mismatches:
                print(f"  - {mismatch}")
            return 1
        print(f"All build files agree with VERSION ({_current_version()}).")
        return 0

    if not args.new_version:
        parser.error("new_version is required unless --check is given.")

    try:
        edits = plan_sync(args.new_version)
    except VersionSyncError as exc:
        print(f"ERROR: {exc}")
        print("No files were changed.")
        return 1

    for edit in edits:
        edit.path.write_text(edit.text, encoding="utf-8")
        print(f"Updated {edit.path.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
