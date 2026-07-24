"""AIEMS Exchange Bridge - file-based, command-driven handover tool between
the Engineering Implementer (Claude) and Engineering Reviewer (Codex) roles.

Implements EBG-0057 per EIP-ESR0025-001. Three properties are enforced in
code, not only by convention (Section 9 of the EIP; the third added after an
Engineering Reviewer post-implementation finding):

1. `return-findings` (Codex's only command) has no code path capable of
   writing outside `.aiems-exchange/` - it takes no file-path argument at
   all, only session/work-package identifiers and a message. Those
   identifiers are themselves validated (`_validate_identifier`) before any
   path is built from them, closing a path-traversal gap a raw
   `session`/`work_package` value could otherwise open.
2. `submit-response` (the only command that represents "proceed with the
   approved change") refuses to run - before any file write - unless the
   Sponsor Approval Service's latest decision for this Work Package approves,
   and the current repository state matches the state that decision actually
   approved. Per ADR-0022/EIP-ESR0030-001, approval no longer lives in a
   locally-writable transcript file: `programme_sponsor_authorisation` can no
   longer be set by any code path in this module at all - see
   `scripts/sponsor_approval_service.py` and `scripts/sponsor_client.py`.
3. `submit-response` additionally refuses if validation (`pytest` and
   `validate_repository.py`) did not pass cleanly - a failing run must not
   produce a handover indistinguishable from a successful one.
   `submit-to-review` stays non-blocking on validation (submitting known-
   broken work-in-progress for review is legitimate) but its evidence
   carries an unmissable `VALIDATION: PASSED/FAILED` marker.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXCHANGE_DIRNAME = ".aiems-exchange"

# session/work_package feed directly into transcript and lock file paths
# (_wp_key below). Restricting them to this shape closes path-traversal at
# the source - every path-building function goes through _wp_key, so no
# call site can forget the check (Engineering Reviewer finding, addressed).
_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
TRANSCRIPT_SEPARATOR = "\n===\n"


class BridgeError(RuntimeError):
    """Raised for expected bridge failures: preflight, authorisation, drift."""


@dataclass(frozen=True)
class Handover:
    session: str
    work_package: str
    type: str
    sender: str
    recipient: str
    repository_ref: str
    files_in_scope: tuple[str, ...]
    programme_sponsor_authorisation: bool | None
    timestamp: str
    message: str
    evidence: str | None = None

    def render(self) -> str:
        auth = (
            "true"
            if self.programme_sponsor_authorisation is True
            else "false"
            if self.programme_sponsor_authorisation is False
            else ""
        )
        header = (
            f"session: {self.session}\n"
            f"work_package: {self.work_package}\n"
            f"type: {self.type}\n"
            f"sender: {self.sender}\n"
            f"recipient: {self.recipient}\n"
            f"repository_ref: {self.repository_ref}\n"
            f"files_in_scope: {', '.join(self.files_in_scope)}\n"
            f"programme_sponsor_authorisation: {auth}\n"
            f"timestamp: {self.timestamp}\n"
        )
        body = f"---\n{self.message}\n"
        if self.evidence is not None:
            body += f"---evidence---\n{self.evidence}\n"
        return header + body


def parse_handover(text: str) -> Handover:
    header_part, _, rest = text.partition("---\n")
    fields: dict[str, str] = {}
    for line in header_part.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()

    if "---evidence---\n" in rest:
        message, _, evidence = rest.partition("---evidence---\n")
    else:
        message, evidence = rest, None

    auth_raw = fields.get("programme_sponsor_authorisation", "")
    if auth_raw == "true":
        auth: bool | None = True
    elif auth_raw == "false":
        auth = False
    else:
        auth = None

    files_raw = fields.get("files_in_scope", "")
    files = tuple(item.strip() for item in files_raw.split(",") if item.strip())

    return Handover(
        session=fields["session"],
        work_package=fields["work_package"],
        type=fields["type"],
        sender=fields["sender"],
        recipient=fields["recipient"],
        repository_ref=fields["repository_ref"],
        files_in_scope=files,
        programme_sponsor_authorisation=auth,
        timestamp=fields["timestamp"],
        message=message.strip("\n"),
        evidence=evidence.strip("\n") if evidence is not None else None,
    )


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _validate_identifier(value: str, label: str) -> None:
    if not _IDENTIFIER_PATTERN.fullmatch(value):
        msg = (
            f"Invalid {label} {value!r}: must contain only letters, digits, "
            "'_' and '-' (no path separators or '..' segments)."
        )
        raise BridgeError(msg)


def _wp_key(session: str, work_package: str) -> str:
    _validate_identifier(session, "session")
    _validate_identifier(work_package, "work_package")
    return f"{session}-{work_package}"


def exchange_root(repo_root: Path) -> Path:
    return repo_root / EXCHANGE_DIRNAME


def transcript_path(repo_root: Path, session: str, work_package: str) -> Path:
    return exchange_root(repo_root) / "transcript" / f"{_wp_key(session, work_package)}.md"


def _lock_path(repo_root: Path, session: str, work_package: str) -> Path:
    return exchange_root(repo_root) / ".locks" / f"{_wp_key(session, work_package)}.lock"


def ensure_layout(repo_root: Path) -> None:
    root = exchange_root(repo_root)
    for sub in ("claude/inbox", "claude/outbox", "codex/inbox", "codex/outbox", "transcript", ".locks"):
        (root / sub).mkdir(parents=True, exist_ok=True)


@contextlib.contextmanager
def work_package_lock(repo_root: Path, session: str, work_package: str):
    path = _lock_path(repo_root, session, work_package)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        msg = f"Work Package {_wp_key(session, work_package)} is locked by another bridge invocation."
        raise BridgeError(msg) from exc
    try:
        os.close(fd)
        yield
    finally:
        path.unlink(missing_ok=True)


def read_transcript(repo_root: Path, session: str, work_package: str) -> list[Handover]:
    path = transcript_path(repo_root, session, work_package)
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return []
    return [parse_handover(chunk) for chunk in text.split(TRANSCRIPT_SEPARATOR) if chunk.strip()]


def append_transcript(repo_root: Path, handover: Handover) -> None:
    path = transcript_path(repo_root, handover.session, handover.work_package)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    separator = TRANSCRIPT_SEPARATOR if existing.strip() else ""
    with path.open("a", encoding="utf-8") as fh:
        fh.write(separator + handover.render())


def _write_handover_file(directory: Path, handover: Handover) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    stamp = handover.timestamp.replace(":", "").replace("-", "")
    path = directory / f"{stamp}-{handover.type}.md"
    path.write_text(handover.render(), encoding="utf-8")
    return path


@dataclass(frozen=True)
class RemoteDecision:
    """A decision fetched from the Sponsor Approval Service (ADR-0022)."""

    decision: str
    repository_ref: str
    timestamp: str
    note: str


def fetch_latest_decision(session: str, work_package: str) -> RemoteDecision | None:
    """Fetch the latest Sponsor Approval Service decision for a Work
    Package, or None if none has been recorded yet.

    Fails closed (raises BridgeError) on any unreachable-service or
    malformed-response case - never a silent fallback to a local file
    (ADR-0022 Decision item 4). Reads AIEMS_AGENT_TOKEN/AIEMS_SPONSOR_URL
    from the environment; this is the only code path in this module that
    contacts the service, and it never reads AIEMS_SPONSOR_TOKEN (that
    token must never exist in any agent-reachable environment at all).
    """

    agent_token = os.environ.get("AIEMS_AGENT_TOKEN")
    sponsor_url = os.environ.get("AIEMS_SPONSOR_URL")
    if not agent_token or not sponsor_url:
        msg = "AIEMS_AGENT_TOKEN and AIEMS_SPONSOR_URL must both be set to contact the Sponsor Approval Service."
        raise BridgeError(msg)

    query = urllib.parse.urlencode({"session": session, "work_package": work_package})
    request = urllib.request.Request(
        f"{sponsor_url.rstrip('/')}/decisions/latest?{query}",
        headers={"Authorization": f"Bearer {agent_token}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        # HTTPError is a URLError subclass, so a non-2xx status (e.g. a
        # misconfigured token) is caught here too, not just connection
        # failures - either way, fail closed rather than assume approval.
        msg = f"Sponsor Approval Service unreachable at {sponsor_url}: {exc}"
        raise BridgeError(msg) from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        msg = "Sponsor Approval Service returned a malformed response."
        raise BridgeError(msg) from exc

    if not isinstance(payload, dict):
        # A valid "no decision recorded yet" response is always a dict with
        # decision: null (Section below) - anything else (a list, a bare
        # string/number, etc.) is a malformed response, not an absence of
        # decision, and must not be silently treated as "no approval" via
        # the same code path as a genuine null-decision reply (Engineering
        # Reviewer finding, addressed).
        msg = "Sponsor Approval Service returned a malformed response."
        raise BridgeError(msg)
    if payload.get("decision") is None:
        # sponsor_approval_service.py's do_GET emits exactly
        # {"decision": None, "repository_ref": None, "timestamp": None,
        # "note": None} when no decision exists yet (Section 5 item 1) -
        # every other field must be both PRESENT and null to match that
        # shape. A field missing entirely (e.g. {"decision": None} alone)
        # is indistinguishable from one explicitly set to null via a bare
        # `.get()` default, so presence is checked separately from value
        # (Engineering Reviewer follow-up finding, addressed: the first fix
        # only caught non-dict payloads, not a dict with an inconsistent or
        # incomplete null shape).
        other_fields = ("repository_ref", "timestamp", "note")
        if not all(key in payload for key in other_fields) or any(
            payload[key] is not None for key in other_fields
        ):
            msg = "Sponsor Approval Service returned a malformed response."
            raise BridgeError(msg)
        return None
    try:
        return RemoteDecision(
            decision=payload["decision"],
            repository_ref=payload["repository_ref"],
            timestamp=payload["timestamp"],
            note=payload.get("note", ""),
        )
    except KeyError as exc:
        msg = "Sponsor Approval Service returned a malformed response."
        raise BridgeError(msg) from exc


def capture_repository_ref(repo_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


@dataclass(frozen=True)
class EvidenceResult:
    passed: bool
    text: str


def capture_evidence(repo_root: Path) -> EvidenceResult:
    """Run pytest and validate_repository.py and attach their raw output,
    verbatim, not interpreted beyond a pass/fail exit-code summary - the
    evidence itself is for a human (or Codex) to read, per the architecture's
    own design, not for this function to judge line-by-line. The leading
    VALIDATION: PASSED/FAILED marker exists so a failing run cannot be
    mistaken for a passing one at a glance (Engineering Reviewer finding,
    addressed) - callers decide what to do with `passed`; submit-to-review
    treats it as informational, submit-response treats it as a hard gate."""

    pytest_result = subprocess.run(
        [sys.executable, "-m", "pytest"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    validate_result = subprocess.run(
        [sys.executable, "scripts/validate_repository.py"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    passed = pytest_result.returncode == 0 and validate_result.returncode == 0
    text = (
        f"VALIDATION: {'PASSED' if passed else 'FAILED'}\n"
        f"$ python -m pytest (exit {pytest_result.returncode})\n"
        f"{pytest_result.stdout}{pytest_result.stderr}\n"
        f"$ python scripts/validate_repository.py (exit {validate_result.returncode})\n"
        f"{validate_result.stdout}{validate_result.stderr}"
    )
    return EvidenceResult(passed=passed, text=text)


@dataclass(frozen=True)
class PreflightResult:
    ok: bool
    details: str


def run_preflight() -> PreflightResult:
    # On Windows, npm installs global CLI tools (claude, codex) as .CMD shim
    # files, which subprocess can only launch via the shell - without
    # shell=True here, subprocess.run raises FileNotFoundError (WinError 2)
    # even when the tool is genuinely present and shutil.which finds it.
    use_shell = sys.platform == "win32"
    lines: list[str] = []
    ok = True
    for tool in ("claude", "codex"):
        path = shutil.which(tool)
        if path is None:
            ok = False
            lines.append(f"{tool}: NOT FOUND on PATH")
            continue
        version = subprocess.run(
            [tool, "--version"], capture_output=True, text=True, shell=use_shell, check=False
        )
        lines.append(f"{tool}: {path} ({(version.stdout or version.stderr).strip()})")

    if shutil.which("codex") is not None:
        status = subprocess.run(
            ["codex", "login", "status"], capture_output=True, text=True, shell=use_shell, check=False
        )
        lines.append(f"codex login status: {(status.stdout or status.stderr).strip()}")

    return PreflightResult(ok=ok, details="\n".join(lines))


def cmd_init(repo_root: Path, session: str, work_package: str) -> Path:
    ensure_layout(repo_root)
    path = transcript_path(repo_root, session, work_package)
    if path.exists():
        msg = f"Work Package {_wp_key(session, work_package)} is already initialised."
        raise BridgeError(msg)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    return path


def cmd_submit_to_review(
    repo_root: Path, session: str, work_package: str, files: list[str], message: str
) -> Handover:
    preflight = run_preflight()
    if not preflight.ok:
        raise BridgeError(f"Preflight failed:\n{preflight.details}")

    # Not gated on evidence.passed: submitting known-broken work-in-progress
    # for review is legitimate. The VALIDATION: PASSED/FAILED marker inside
    # the evidence text (capture_evidence) makes a failing run unmissable to
    # Codex and the transcript reader, rather than silently blocking review.
    evidence = capture_evidence(repo_root)

    with work_package_lock(repo_root, session, work_package):
        handover = Handover(
            session=session,
            work_package=work_package,
            type="submit-to-review",
            sender="claude",
            recipient="codex",
            repository_ref=capture_repository_ref(repo_root),
            files_in_scope=tuple(files),
            programme_sponsor_authorisation=None,
            timestamp=_now(),
            message=message,
            evidence=evidence.text,
        )
        ensure_layout(repo_root)
        _write_handover_file(exchange_root(repo_root) / "codex" / "inbox", handover)
        _write_handover_file(exchange_root(repo_root) / "claude" / "outbox", handover)
        append_transcript(repo_root, handover)
    return handover


def cmd_return_findings(repo_root: Path, session: str, work_package: str, message: str) -> Handover:
    """Codex's only command. Takes no file-path argument - structurally
    incapable of writing anything outside .aiems-exchange/."""

    preflight = run_preflight()
    if not preflight.ok:
        raise BridgeError(f"Preflight failed:\n{preflight.details}")

    with work_package_lock(repo_root, session, work_package):
        handover = Handover(
            session=session,
            work_package=work_package,
            type="return-findings",
            sender="codex",
            recipient="claude",
            repository_ref=capture_repository_ref(repo_root),
            files_in_scope=(),
            programme_sponsor_authorisation=None,
            timestamp=_now(),
            message=message,
        )
        ensure_layout(repo_root)
        _write_handover_file(exchange_root(repo_root) / "claude" / "inbox", handover)
        _write_handover_file(exchange_root(repo_root) / "codex" / "outbox", handover)
        append_transcript(repo_root, handover)
    return handover


def cmd_submit_response(repo_root: Path, session: str, work_package: str, message: str) -> Handover:
    """The only command representing 'proceed with the approved change'.
    Refuses before any file write unless the Sponsor Approval Service's
    latest decision for this Work Package approves, the current repository
    state matches the state that decision actually approved, and validation
    is clean (Engineering Reviewer finding, addressed: a failing pytest/
    validate_repository.py run must not produce a handover that looks like
    a successful response)."""

    # The entire fetch-check-evidence-write sequence runs inside the lock,
    # not just the final write (Engineering Reviewer finding, addressed,
    # originally against the file-based sponsor-decision command this
    # replaced): every other command that can append to this Work Package's
    # transcript (return-findings, submit-to-review, a concurrent
    # submit-response) also acquires this same lock before writing, so
    # holding it here for the full duration - including the slow evidence
    # capture step - closes the TOCTOU window rather than only narrowing it.
    with work_package_lock(repo_root, session, work_package):
        decision = fetch_latest_decision(session, work_package)
        if decision is None or decision.decision != "approve":
            msg = "submit-response refused: no approving decision found for this Work Package."
            raise BridgeError(msg)

        current_ref = capture_repository_ref(repo_root)
        if current_ref != decision.repository_ref:
            msg = (
                "submit-response refused: repository has drifted since the approved decision "
                f"(approved {decision.repository_ref}, current {current_ref}). "
                "A fresh decision is required before this response can proceed."
            )
            raise BridgeError(msg)

        preflight = run_preflight()
        if not preflight.ok:
            raise BridgeError(f"Preflight failed:\n{preflight.details}")

        evidence = capture_evidence(repo_root)
        if not evidence.passed:
            msg = (
                "submit-response refused: validation failed (pytest and/or "
                "validate_repository.py returned non-zero). The approved response "
                "must pass clean validation before it can be recorded as complete."
            )
            raise BridgeError(msg)

        handover = Handover(
            session=session,
            work_package=work_package,
            type="submit-response",
            sender="claude",
            recipient="n/a",
            repository_ref=current_ref,
            files_in_scope=(),
            programme_sponsor_authorisation=None,
            timestamp=_now(),
            message=message,
            evidence=evidence.text,
        )
        ensure_layout(repo_root)
        _write_handover_file(exchange_root(repo_root) / "claude" / "outbox", handover)
        append_transcript(repo_root, handover)
    return handover


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aiems_bridge", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialise a Work Package's exchange layout and transcript.")
    p_init.add_argument("session")
    p_init.add_argument("work_package")

    p_submit = sub.add_parser("submit-to-review", help="Claude submits a Work Package to Codex for review.")
    p_submit.add_argument("session")
    p_submit.add_argument("work_package")
    p_submit.add_argument("--files", default="", help="Comma-separated files in scope.")
    p_submit.add_argument("--message", required=True)

    p_findings = sub.add_parser("return-findings", help="Codex returns findings. Never writes outside .aiems-exchange/.")
    p_findings.add_argument("session")
    p_findings.add_argument("work_package")
    p_findings.add_argument("--message", required=True)

    p_response = sub.add_parser("submit-response", help="Claude implements the approved change. Gated on the Sponsor Approval Service.")
    p_response.add_argument("session")
    p_response.add_argument("work_package")
    p_response.add_argument("--message", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "init":
            path = cmd_init(REPO_ROOT, args.session, args.work_package)
            print(f"Initialised {path}")
        elif args.command == "submit-to-review":
            files = [f.strip() for f in args.files.split(",") if f.strip()]
            handover = cmd_submit_to_review(REPO_ROOT, args.session, args.work_package, files, args.message)
            print(f"Submitted to review at {handover.timestamp}")
        elif args.command == "return-findings":
            handover = cmd_return_findings(REPO_ROOT, args.session, args.work_package, args.message)
            print(f"Findings returned at {handover.timestamp}")
        elif args.command == "submit-response":
            handover = cmd_submit_response(REPO_ROOT, args.session, args.work_package, args.message)
            print(f"Response submitted at {handover.timestamp}")
    except BridgeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
