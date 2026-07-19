"""Sponsor Approval Service client (ADR-0022, EIP-ESR0030-001).

Run manually, by the Programme Sponsor, from a host-side terminal only -
never from any environment an agent (Claude Code or Codex CLI) can reach.
Reads AIEMS_SPONSOR_TOKEN/AIEMS_SPONSOR_URL from the environment; never
accepts a token as a command-line argument, so it cannot end up in shell
history or a process list visible to another user on a shared machine.

Usage:
    python scripts/sponsor_client.py <session> <work_package> --decision approve|reject [--note "..."]

repository_ref is captured automatically from the local `git rev-parse
HEAD`, matching the prior file-based sponsor-decision command's behaviour -
not accepted as an argument, since the whole point is recording what the
Sponsor approved at the repository state they can see on their own host.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class ClientError(RuntimeError):
    """Raised for expected client failures (missing config, request failure)."""


def capture_repository_ref(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def submit_decision(
    sponsor_url: str,
    sponsor_token: str,
    session: str,
    work_package: str,
    decision: str,
    repository_ref: str,
    note: str,
) -> dict:
    """POST a decision to the Sponsor Approval Service.

    Raises ClientError on any failure - connection refused, timeout,
    non-2xx status, or a malformed response - never silently succeeds.
    """

    body = json.dumps(
        {
            "session": session,
            "work_package": work_package,
            "decision": decision,
            "repository_ref": repository_ref,
            "note": note,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        sponsor_url.rstrip("/") + "/decisions",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {sponsor_token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        msg = f"Sponsor Approval Service refused the decision (HTTP {exc.code}): {detail}"
        raise ClientError(msg) from exc
    except urllib.error.URLError as exc:
        msg = f"Could not reach Sponsor Approval Service at {sponsor_url}: {exc.reason}"
        raise ClientError(msg) from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sponsor_client", description=__doc__)
    parser.add_argument("session")
    parser.add_argument("work_package")
    parser.add_argument("--decision", required=True, choices=("approve", "reject"))
    parser.add_argument("--note", default="")
    args = parser.parse_args(argv)

    sponsor_token = os.environ.get("AIEMS_SPONSOR_TOKEN")
    sponsor_url = os.environ.get("AIEMS_SPONSOR_URL")
    if not sponsor_token:
        print("ERROR: AIEMS_SPONSOR_TOKEN is not set.", file=sys.stderr)
        return 1
    if not sponsor_url:
        print("ERROR: AIEMS_SPONSOR_URL is not set.", file=sys.stderr)
        return 1

    try:
        repository_ref = capture_repository_ref(REPO_ROOT)
        result = submit_decision(
            sponsor_url,
            sponsor_token,
            args.session,
            args.work_package,
            args.decision,
            repository_ref,
            args.note,
        )
    except ClientError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        f"Recorded {result['decision']} for {args.session}/{args.work_package} "
        f"at {result['timestamp']} (repository_ref={result['repository_ref']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
