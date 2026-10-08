"""Deterministic post-commit pre-check, run before the independent
post-commit review and handed to it (ESR-0061 WP1c, R8; EIP-ESR0061-001
Section 7.2).

    python scripts/post_commit_precheck.py <commit> --session ESR-0061 --wp WP1c \
        [--eip PATH --contents-heading "7.4 Commit Contents"]

Hard checks (exit 1 on failure):
  * the working tree is clean and the commit is on origin/main;
  * with --eip, the files the commit changed equal the EIP's Commit Contents
    list (backticked paths under the named heading or bold label);
  * the latest submit-response transcript entry for the session/WP recorded
    the commit's parent as repository_ref (the approval gate);
  * pytest has no failures or errors, ruff is clean, the validator reports
    0 errors.

Advisory checks (reported, never failing): "N passed", "N skipped" or
"N warning(s)" figures in the commit message against the actual results -
those counts legitimately move, so a difference is shown, not enforced.

This replaces nothing: the independent post-commit review still runs.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPT_DIR = REPO_ROOT / ".aiems-exchange" / "transcript"
_PATH_TOKEN = re.compile(r"`([^`\s]+\.(?:md|py|json|jsx|js|rs|toml|yml|yaml|txt|lock|sh|ps1|bat|html|css|plist|ini|cfg|xml))`")


@dataclass
class Report:
    hard: list[tuple[str, bool, str]] = field(default_factory=list)
    advisory: list[str] = field(default_factory=list)

    def check(self, name: str, ok: bool, detail: str = "") -> None:
        self.hard.append((name, ok, detail))

    @property
    def passed(self) -> bool:
        return all(ok for _, ok, _ in self.hard)

    def render(self) -> str:
        lines = ["# Post-commit pre-check", ""]
        for name, ok, detail in self.hard:
            lines.append(f"- [{'PASS' if ok else 'FAIL'}] {name}" + (f" - {detail}" if detail else ""))
        lines += ["", "## Advisory (never failing)", ""]
        lines += [f"- {note}" for note in self.advisory] or ["- none"]
        lines += ["", f"**Result: {'PASS' if self.passed else 'FAIL'}**"]
        return "\n".join(lines)


def git(*args: str) -> str:
    completed = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    return completed.stdout.strip()


def eip_commit_contents(eip_text: str, heading: str) -> set[str]:
    """Backticked paths in the block that starts at `heading` (a Markdown
    heading or a bold label) and runs to the next heading."""

    start = eip_text.find(heading)
    if start == -1:
        raise ValueError(f"heading not found in EIP: {heading}")
    rest = eip_text[start + len(heading):]
    # A bold label (`**12.4 Commit contents`) also ends at the next line that
    # starts with another bold label - later bold paragraphs in the same
    # section are not part of the list (ESR-0061 WP2b, from the WP2a-fix review).
    stop = r"(?m)^(?:#{1,6}\s|\*\*)" if heading.startswith("**") else r"(?m)^#{1,6}\s"
    end = re.search(stop, rest)
    block = rest[: end.start()] if end else rest
    # A "Not changed" or "Differences" note names paths the build left alone: stop there, but only
    # once a listed path has been seen, so a leading note cannot empty the list.
    first_path = _PATH_TOKEN.search(block)
    if first_path:
        note = re.search(r"(?m)^(?:Not changed|Differences)", block[first_path.end():])
        if note:
            block = block[: first_path.end() + note.start()]
    return set(_PATH_TOKEN.findall(block))


def latest_submit_response_ref(session: str, wp: str) -> str | None:
    path = TRANSCRIPT_DIR / f"{session}-{wp}.md"
    if not path.exists():
        return None
    ref = None
    for block in path.read_text(encoding="utf-8", errors="replace").split("\n===\n"):
        if re.search(r"^type: submit-response$", block, re.MULTILINE):
            found = re.search(r"^repository_ref: (\S+)$", block, re.MULTILINE)
            ref = found.group(1) if found else ref
    return ref


def parse_pytest(output: str) -> dict[str, int]:
    counts = {key: 0 for key in ("passed", "failed", "errors", "skipped")}
    for number, word in re.findall(r"(\d+) (passed|failed|errors?|skipped)", output):
        counts["errors" if word.startswith("error") else word] = int(number)
    return counts


def parse_validator(output: str) -> tuple[int, int] | None:
    # Passing runs say "0 errors"; failing runs say "2 error(s)".
    found = re.search(r"(\d+) errors?(?:\(s\))?, (\d+) warning", output)
    return (int(found.group(1)), int(found.group(2))) if found else None


def run(command: list[str]) -> tuple[int, str]:
    completed = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    return completed.returncode, (completed.stdout or "") + (completed.stderr or "")


def advisory_figures(message: str, pytest_counts: dict[str, int], validator: tuple[int, int] | None) -> list[str]:
    notes = []
    # Only a figure that follows the word "pytest" in the same clause is compared;
    # cargo's and the Linux run's counts are different suites.
    for number, word in re.findall(r"pytest[^;,.\n]{0,30}?(\d+) (passed|skipped)", message):
        actual = pytest_counts[word]
        if int(number) != actual:
            notes.append(f"commit message says {number} {word}; actual {actual}")
    claimed_warnings = re.search(r"(\d+) warnings?", message)
    if claimed_warnings and validator and int(claimed_warnings.group(1)) != validator[1]:
        notes.append(f"commit message says {claimed_warnings.group(1)} warnings; validator reports {validator[1]}")
    return notes


def precheck(commit: str, session: str, wp: str, eip: Path | None, heading: str | None, run_suites: bool = True) -> Report:
    report = Report()
    full = git("rev-parse", commit)
    parent = git("rev-parse", f"{commit}^")

    status = git("status", "--porcelain")
    report.check("working tree clean", status == "", status.replace("\n", "; ")[:200])
    on_main = "origin/main" in git("branch", "-r", "--contains", full).split()
    report.check("commit is on origin/main", on_main)

    if eip is not None:
        if heading is None:
            raise ValueError("--contents-heading is required with --eip")
        expected = eip_commit_contents(eip.read_text(encoding="utf-8"), heading)
        changed = set(git("diff-tree", "--no-commit-id", "--name-only", "-r", full).splitlines())
        extra, missing = sorted(changed - expected), sorted(expected - changed)
        detail = "; ".join(filter(None, [f"not listed: {extra}" if extra else "", f"listed but unchanged: {missing}" if missing else ""]))
        report.check("changed files equal the EIP's Commit Contents", not extra and not missing, detail)

    gated_ref = latest_submit_response_ref(session, wp)
    report.check(
        "submit-response gated against the commit's parent",
        gated_ref == parent,
        f"transcript ref {gated_ref}, parent {parent}" if gated_ref != parent else "",
    )

    pytest_counts = {key: 0 for key in ("passed", "failed", "errors", "skipped")}
    validator = None
    if run_suites:
        _, pytest_out = run([sys.executable, "-m", "pytest", "-q"])
        pytest_counts = parse_pytest(pytest_out)
        report.check(
            "pytest: no failures or errors",
            pytest_counts["failed"] == 0 and pytest_counts["errors"] == 0 and pytest_counts["passed"] > 0,
            f"{pytest_counts}",
        )
        ruff_code, ruff_out = run([sys.executable, "-m", "ruff", "check", "."])
        report.check("ruff clean", ruff_code == 0, ruff_out.strip().splitlines()[-1] if ruff_code else "")
        _, validator_out = run([sys.executable, "scripts/validate_repository.py"])
        validator = parse_validator(validator_out)
        report.check("validator: 0 errors", validator is not None and validator[0] == 0, f"{validator}")

    report.advisory = advisory_figures(git("log", "-1", "--format=%B", full), pytest_counts, validator)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("commit")
    parser.add_argument("--session", required=True)
    parser.add_argument("--wp", required=True)
    parser.add_argument("--eip", type=Path)
    parser.add_argument("--contents-heading")
    args = parser.parse_args(argv)
    report = precheck(args.commit, args.session, args.wp, args.eip, args.contents_heading)
    print(report.render())
    return 0 if report.passed else 1


if __name__ == "__main__":
    sys.exit(main())
