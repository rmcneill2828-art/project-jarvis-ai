"""Run an independent Engineering Reviewer CLI (GitHub Copilot or Antigravity)
on a bridge Work Package, read-only, and report what happened.

ESR-0061 WP1c (R8), per EIP-ESR0061-001 Section 7.2. Usage:

    python scripts/run_reviewer.py --tool antigravity --session ESR-0061 \
        --wp WP1c --prompt-file review.txt [--resume "text"]
    python scripts/run_reviewer.py --check-settings
    python scripts/run_reviewer.py --install-settings

The reviewer records its own verdict with `aiems_bridge.py return-findings`;
this script never writes findings. It:

* appends the standard TOOL RULES block for the tool to the prompt, writes
  the full prompt to `.aiems-exchange/reviews/` (git-ignored), and passes the
  CLI only a fixed instruction to read that file - so no prompt text ever
  reaches a Windows `cmd.exe` command line (Copilot is a `.cmd` shim there);
* runs Copilot with narrowly scoped read-only `--allow-tool` rules (ESR-0060's
  `shell(git:*)`/`shell(python:*)` also allowed `git push` and `python -c`),
  and Antigravity headless with a Gemini model - never a Claude model, so the
  review stays independent of the Engineering Implementer;
* detects Copilot's monthly-quota failure and Antigravity's refused-tool
  abort, naming the refused command so a `--resume` is one step;
* confirms a new `sender: reviewer` transcript entry appeared, and says so
  plainly if not.

Exit codes: 0 verdict recorded; 2 usage or settings problem; 3 quota
exhausted; 4 tool refused (run aborted); 5 finished without a verdict.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST_PATH = REPO_ROOT / "scripts" / "reviewer" / "antigravity_allowlist.json"
ANTIGRAVITY_SETTINGS = Path.home() / ".gemini" / "antigravity-cli" / "settings.json"
ANTIGRAVITY_BRAIN = Path.home() / ".gemini" / "antigravity-cli" / "brain"
REVIEWS_DIR = REPO_ROOT / ".aiems-exchange" / "reviews"
TRANSCRIPT_DIR = REPO_ROOT / ".aiems-exchange" / "transcript"

ANTIGRAVITY_MODEL = "gemini-3.1-pro-high"
RUN_TIMEOUT_SECONDS = 45 * 60

EXIT_OK, EXIT_USAGE, EXIT_QUOTA, EXIT_REFUSED, EXIT_NO_VERDICT = 0, 2, 3, 4, 5

COPILOT_ALLOWED_TOOLS = (
    "shell(git log:*)",
    "shell(git show:*)",
    "shell(git diff:*)",
    "shell(git status:*)",
    "shell(git grep:*)",
    "shell(git ls-files:*)",
    "shell(git rev-parse:*)",
    "shell(git cat-file:*)",
    "shell(python -m pytest:*)",
    "shell(python -m ruff check:*)",
    "shell(python scripts/validate_repository.py)",
    "shell(python scripts/aiems_bridge.py return-findings:*)",
)

QUOTA_MARKER = "exceeded your monthly quota"
REFUSED_MARKER = "auto-denied"

TOOL_RULES = {
    "antigravity": """
TOOL RULES (any other tool use is refused and aborts your whole run, losing your work):
- Read files with your file-viewing tool (preferred), or cat FILE.
- Allowed shell commands: git log|show|diff|status|rev-parse|ls-files|grep|cat-file with arguments
  (no = signs, no option starting --ou, no -O); cat FILE; grep with options and a single-word or
  double-quoted pattern on files; ls; head -n N FILE; tail -n N FILE; wc FILE. Any git, cat or grep
  command may be followed by up to two read-only filters: grep, head -n N, tail -n N, wc.
  Plus python -m pytest -q (paths only), python scripts/validate_repository.py,
  python -m ruff check (paths only), and the return-findings command below.
- Never: python -c, other pipes, redirects (>), ;, &, $ or backticks. Do not create, edit or delete any file.
""",
    "copilot": """
TOOL RULES: you may read files and run only read-only git (log, show, diff, status, grep, ls-files,
rev-parse, cat-file), python -m pytest, python -m ruff check, python scripts/validate_repository.py
and the return-findings command below. Do not create, edit or delete any file.
""",
}

VERDICT_RULES = """
- Record your verdict exactly once with:
  python scripts/aiems_bridge.py return-findings {session} {wp} --message "<full verdict and findings>"
  The message must be wrapped in double quotes and must NOT contain any of these characters:
  double quote, backtick, dollar, semicolon, ampersand, pipe, less-than, greater-than.
- Do not post any test or placeholder entry. Then print the same verdict as your final answer.
"""


def compose_prompt(tool: str, session: str, wp: str, prompt: str) -> str:
    return prompt.rstrip() + "\n" + TOOL_RULES[tool] + VERDICT_RULES.format(session=session, wp=wp)


def launcher_instruction(prompt_path: Path) -> str:
    """A fixed, shell-safe instruction: letters, digits, spaces, slashes,
    dots, hyphens and underscores only."""

    rel = prompt_path.relative_to(REPO_ROOT).as_posix()
    if not re.fullmatch(r"[A-Za-z0-9_./ -]+", rel):
        raise ValueError(f"unsafe prompt path: {rel}")
    return f"Read the file {rel} in full and follow its instructions exactly"


def build_command(tool: str, instruction: str, resume: str | None) -> list[str]:
    if tool == "copilot":
        command = ["copilot", "-p", instruction, "-s"]
        for rule in COPILOT_ALLOWED_TOOLS:
            command += ["--allow-tool", rule]
        return command + ["--deny-tool", "write"]
    command = ["agy"]
    if resume is not None:
        command.append("-c")
    return command + ["-p", instruction, "--model", ANTIGRAVITY_MODEL, "--effort", "high", "--print-timeout", "40m"]


def load_allowlist(repo_root: Path = REPO_ROOT) -> list[str]:
    data = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
    root = repo_root.as_posix()
    return [rule.replace("{repo_root}", root) for rule in data["permissions"]["allow"]]


def command_allowed(rules: list[str], command: str) -> bool:
    """Approximate Antigravity's matcher for `command(regex:...)` rules, for
    tests. The live matcher may use a different regex engine, so the rules
    avoid look-around and back-references."""

    for rule in rules:
        match = re.fullmatch(r"command\(regex:(.*)\)", rule)
        if match and re.fullmatch(match.group(1), command):
            return True
    return False


def check_settings() -> list[str]:
    """Return the allow-list rules missing from the live settings file."""

    if not ANTIGRAVITY_SETTINGS.exists():
        return load_allowlist()
    live = json.loads(ANTIGRAVITY_SETTINGS.read_text(encoding="utf-8"))
    current = set(live.get("permissions", {}).get("allow", []))
    return [rule for rule in load_allowlist() if rule not in current]


def install_settings() -> int:
    """Merge the allow-list into the live settings. Never adds deny rules, so
    the Programme Sponsor's interactive use is unaffected."""

    live = json.loads(ANTIGRAVITY_SETTINGS.read_text(encoding="utf-8")) if ANTIGRAVITY_SETTINGS.exists() else {}
    allow = live.setdefault("permissions", {}).setdefault("allow", [])
    added = [rule for rule in load_allowlist() if rule not in allow]
    allow.extend(added)
    ANTIGRAVITY_SETTINGS.parent.mkdir(parents=True, exist_ok=True)
    ANTIGRAVITY_SETTINGS.write_text(json.dumps(live, indent=2) + "\n", encoding="utf-8")
    return len(added)


def reviewer_entries_since(session: str, wp: str, since: datetime) -> list[str]:
    path = TRANSCRIPT_DIR / f"{session}-{wp}.md"
    if not path.exists():
        return []
    entries = []
    for block in path.read_text(encoding="utf-8", errors="replace").split("\n===\n"):
        if "sender: reviewer" not in block:
            continue
        stamp = re.search(r"^timestamp: (\S+)$", block, re.MULTILINE)
        if stamp and datetime.fromisoformat(stamp.group(1)) >= since:
            entries.append(block.split("\n---\n", 1)[-1].strip())
    return entries


def last_refused_command(brain: Path | None = None) -> str | None:
    """Best effort: the command Antigravity's latest conversation refused."""

    brain = brain or ANTIGRAVITY_BRAIN
    if not brain.exists():
        return None
    conversations = sorted((p for p in brain.iterdir() if p.is_dir()), key=lambda p: p.stat().st_mtime)
    if not conversations:
        return None
    log = conversations[-1] / ".system_generated" / "logs" / "transcript.jsonl"
    if not log.exists():
        return None
    refused = None
    for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            step = json.loads(line)
        except json.JSONDecodeError:
            continue
        error = str(step.get("error") or "")
        found = re.search(r'permission check failed for command "(.*?)": ', error, re.DOTALL)
        if found:
            refused = found.group(1)
    return refused


def run_review(tool: str, session: str, wp: str, prompt: str, resume: str | None) -> int:
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    # Transcript timestamps have whole seconds; a verdict recorded in the same
    # second the run started must still count.
    started = datetime.now(UTC).replace(microsecond=0)
    stamp = started.strftime("%Y%m%dT%H%M%SZ")
    prompt_path = REVIEWS_DIR / f"{session}-{wp}-{stamp}-prompt.md"
    output_path = REVIEWS_DIR / f"{session}-{wp}-{stamp}-output.txt"
    body = resume if resume is not None else compose_prompt(tool, session, wp, prompt)
    prompt_path.write_text(body, encoding="utf-8")

    command = build_command(tool, launcher_instruction(prompt_path), resume)
    executable = shutil.which(command[0])
    if executable is None:
        print(f"{command[0]}: not found on PATH")
        return EXIT_USAGE
    completed = subprocess.run(
        [executable, *command[1:]],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
        timeout=RUN_TIMEOUT_SECONDS,
        check=False,
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    output_path.write_text(output, encoding="utf-8")
    print(f"Output saved to {output_path.relative_to(REPO_ROOT)}")

    if QUOTA_MARKER in output:
        print("Reviewer quota exhausted - no review ran.")
        return EXIT_QUOTA
    if REFUSED_MARKER in output:
        refused = last_refused_command() if tool == "antigravity" else None
        print("Reviewer run aborted on a refused tool" + (f": {refused}" if refused else "."))
        print("If the command is read-only and safe, extend the allow-list deliberately, then --resume.")
        return EXIT_REFUSED
    entries = reviewer_entries_since(session, wp, started)
    if not entries:
        print("The reviewer finished without recording a verdict in the transcript.")
        return EXIT_NO_VERDICT
    print("Verdict recorded:\n" + entries[-1][:2000])
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tool", choices=("copilot", "antigravity"))
    parser.add_argument("--session")
    parser.add_argument("--wp")
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument("--resume", help="Continue the last Antigravity conversation with this message")
    parser.add_argument("--check-settings", action="store_true")
    parser.add_argument("--install-settings", action="store_true")
    args = parser.parse_args(argv)

    if args.check_settings:
        missing = check_settings()
        for rule in missing:
            print(f"missing: {rule}")
        print("Antigravity settings match the allow-list." if not missing else f"{len(missing)} rule(s) missing.")
        return EXIT_OK if not missing else EXIT_USAGE
    if args.install_settings:
        print(f"Added {install_settings()} rule(s) to {ANTIGRAVITY_SETTINGS}.")
        return EXIT_OK

    if not (args.tool and args.session and args.wp):
        parser.error("--tool, --session and --wp are required for a review run")
    if args.resume is not None and args.tool != "antigravity":
        parser.error("--resume is only supported for Antigravity")
    if args.resume is None and args.prompt_file is None:
        parser.error("--prompt-file is required unless --resume is given")
    prompt = args.prompt_file.read_text(encoding="utf-8") if args.prompt_file else ""
    return run_review(args.tool, args.session, args.wp, prompt, args.resume)


if __name__ == "__main__":
    sys.exit(main())
