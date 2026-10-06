"""Advisory local pre-screen of a diff by a local model (gpt-oss-20b via
LM Studio), before the independent review (ESR-0061 WP1c; Programme Sponsor
decision D29, 2 October 2026).

    python scripts/local_prescreen.py [--base HEAD] [--head WORKTREE] [--model ID]

ADVISORY ONLY. Its output is never independent review, is never written to
the bridge transcript, and every finding must be verified by the Engineering
Implementer before it is acted on (scorecard, 2 October 2026: it caught 2 of
4 known defects, under-rated both, and raised one false High - but also found
a genuine new defect). If LM Studio's server is not running it prints a skip
message and exits 0, so it can never block anything. Standard library only;
nothing leaves the machine.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / ".aiems-exchange" / "prescreen"
BASE_URL = "http://localhost:1234/v1"
MODEL_HINT = "gpt-oss-20b"
MAX_DIFF_CHARS = 60_000
REQUEST_TIMEOUT_SECONDS = 20 * 60
HEADER = "ADVISORY - NOT INDEPENDENT REVIEW"

PROMPT = """You are pre-screening a code change before an independent human-gated review.
List concrete defects only: bugs, unsafe input handling, broken error paths, platform problems.
For each: severity (High/Medium/Low), file and line, the failing input or scenario, and why.
Do not comment on style. If you find nothing concrete, say so.

DIFF:
"""


def get_diff(base: str, head: str | None) -> str:
    args = ["git", "diff", base] + ([head] if head else [])
    completed = subprocess.run(args, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    return completed.stdout


def truncate(diff: str, limit: int = MAX_DIFF_CHARS) -> tuple[str, bool]:
    if len(diff) <= limit:
        return diff, False
    return diff[:limit] + f"\n\n[... diff truncated at {limit} characters ...]\n", True


def _get_json(url: str, timeout: float) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.load(response)


def find_model(explicit: str | None, timeout: float = 5) -> str | None:
    """The served model id containing MODEL_HINT, or None if the server is
    not reachable or does not serve it."""

    try:
        models = _get_json(f"{BASE_URL}/models", timeout)
    except (urllib.error.URLError, OSError, ValueError):
        return None
    ids = [entry.get("id", "") for entry in models.get("data", [])]
    if explicit:
        return explicit if explicit in ids else None
    return next((model_id for model_id in ids if MODEL_HINT in model_id), None)


def ask(model: str, diff: str) -> str:
    body = json.dumps(
        {"model": model, "messages": [{"role": "user", "content": PROMPT + diff}], "temperature": 0.2, "max_tokens": 2000}
    ).encode()
    request = urllib.request.Request(f"{BASE_URL}/chat/completions", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        return json.load(response)["choices"][0]["message"]["content"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", default="HEAD", help="Diff base (default: HEAD, i.e. uncommitted changes)")
    parser.add_argument("--head", help="Diff head commit (default: the working tree)")
    parser.add_argument("--model", help="Exact LM Studio model id (default: the one containing gpt-oss-20b)")
    args = parser.parse_args(argv)

    model = find_model(args.model)
    if model is None:
        print(f"{HEADER}: skipped - LM Studio is not running at {BASE_URL} or does not serve {args.model or MODEL_HINT}.")
        return 0

    diff, truncated = truncate(get_diff(args.base, args.head))
    if not diff.strip():
        print(f"{HEADER}: skipped - empty diff.")
        return 0
    try:
        answer = ask(model, diff)
    except (urllib.error.URLError, OSError, KeyError, ValueError) as exc:
        print(f"{HEADER}: skipped - the local model did not answer ({type(exc).__name__}).")
        return 0

    report = f"# {HEADER}\n\nModel: {model}. Diff: {args.base}..{args.head or 'working tree'}"
    report += " (truncated)" if truncated else ""
    report += ".\nVerify every finding before acting on it. Never counted as independent review (D29).\n\n" + answer
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / f"prescreen-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}.md"
    out.write_text(report, encoding="utf-8")
    print(report)
    print(f"\nSaved to {out.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
