"""GIA Phase 3: engineering state observability (EBG-0083, EIP-ESR0054-002
Phase 3a git state; EIP-ESR0055-001 Phase 3b/3c repository health and
register state).

Phase 3 in full: "engineering instrumentation - repository health,
session/baseline state, git state" (ESR-0011's original four-phase plan).
Phase 3a (git state) was delivered first as the cheapest, fastest-to-verify
slice; this module now also covers Phase 3b (repository health, via
`scripts/validate_repository.py`) and Phase 3c (session/baseline state, via
REG-0001), matching the staged, small, evidence-led delivery discipline
Phase 1's own four increments (1a/1b/1c/1d) already established - just
delivered together in one Work Package (ESR-0055 WP1) rather than as
further separate slices.

Kept as a separate module rather than extending `jarvis.gia.observability`
directly: this is a distinct subprocess/file-backed data domain, not a
`psutil` reading, so it needs its own reader abstraction rather than
overloading `ResourceReader`.

Per ESR-0011 Section 10, GIA "shall observe and publish state. It shall
not become a policy engine, decision-maker or owner of platform state" -
`EngineeringStateObserver` contains no thresholds, alerts or branching on
the values it reads, matching `LocalResourceObserver`'s own constraint.
`register_state()` in particular reports REG-0001's highest-numbered
`RBL-*`/`ESR-*` rows and their own literal Status column value, unfiltered
by status (Codex design-review correction on EIP-ESR0055-001 v0.1 -> v0.2,
Programme Sponsor-selected): while a session is open, this genuinely
returns that open session and its `Open` status, not a fallback to the
previous closed one - a deliberate observe-only choice, not the same
concept as `scripts/validate_repository.py`'s own `latest_closed_numbered()`,
which filters to `Closed` rows for a different purpose (avoiding false
staleness warnings against an in-progress session).

Both `repository_validation()` and `register_state()` depend on files that
exist only in a source/repository checkout (`scripts/validate_repository.py`,
`aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`) -
neither is bundled into the Guardian Desktop distributable's PyInstaller
sidecar freeze (`scripts/build_backend_sidecar.py` only freezes
`jarvis/`'s own import graph). In that packaged context these two methods
fail identically to how the git-backed methods already silently fail
there today (no `.git` directory either) - propagated as a genuine error,
never a fabricated value, per the no-mock-fallback rule. This is not a new
gap introduced by this module; it is GIA's engineering-instrumentation
scope working exactly as intended (observability for the Engineering
Implementer's own repository checkout, not end-user product telemetry).
"""

import logging
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Protocol

logger = logging.getLogger(__name__)

# Field separator for `git log`'s combined --format output - unlikely to
# appear in a commit subject line, avoiding ambiguity a plain space or colon
# split could introduce.
_GIT_LOG_FIELD_SEPARATOR = "\x1f"

# This file's own location is used only to resolve which repository `git`
# should operate against (via `git -C <dir> rev-parse --show-toplevel`) -
# robust regardless of the calling process's own working directory, unlike
# depending on `Path.cwd()`.
_MODULE_DIR = Path(__file__).resolve().parent

# Tolerant of both of scripts/validate_repository.py's own summary
# phrasings ("0 errors, N warning(s)." on pass; "N error(s), M warning(s)."
# on fail) without depending on which one was printed.
_VALIDATION_SUMMARY_PATTERN = re.compile(r"(\d+)\s*errors?(?:\(s\))?,\s*(\d+)\s*warnings?(?:\(s\))?")

_REGISTER_RELATIVE_PATH = Path("aiems") / "governance" / "registers" / "REG-0001_CONTROLLED_ARTEFACT_REGISTER.md"
_ARTEFACT_ID_PATTERN = re.compile(r"^[A-Z]+-\d{4}$")


@dataclass(frozen=True)
class EngineeringSnapshot:
    """A single real, current engineering-instrumentation observation."""

    git_branch: str
    git_uncommitted_files: int
    git_last_commit_sha: str
    git_last_commit_message: str
    repository_validation_errors: int
    repository_validation_warnings: int
    current_repository_baseline: str
    latest_registered_session: str
    latest_registered_session_status: str
    captured_at: datetime


class EngineeringStateReader(Protocol):
    """Reads real repository engineering state - implemented by the real
    `git` CLI, `scripts/validate_repository.py` and REG-0001 in production,
    substitutable with a fake in tests so unit tests never depend on this
    repository's own live state.

    Renamed from `GitStateReader` (EIP-ESR0055-001, Codex design-review
    agreed): the Protocol is no longer git-specific once
    `repository_validation()`/`register_state()` are added - keeping the
    old name would misdescribe it. Internal only, never exposed via any
    RPC field name or external contract.
    """

    def branch(self) -> str: ...

    def uncommitted_file_count(self) -> int: ...

    def last_commit(self) -> tuple[str, str]:
        """Return (sha, subject) of the most recent commit."""
        ...

    def repository_validation(self) -> tuple[int, int]:
        """Return (error_count, warning_count) from a fresh
        `scripts/validate_repository.py` run."""
        ...

    def register_state(self) -> tuple[str, str, str]:
        """Return (current_repository_baseline, latest_registered_session,
        latest_registered_session_status) read directly from REG-0001."""
        ...


class RealEngineeringStateReader:
    """Default production reader.

    The repository root is resolved lazily, on first use inside any of
    this reader's own operations - never at construction - and cached
    after that first successful resolution (Codex design-review
    correction on EIP-ESR0054-002 v0.1: eager resolution at construction
    risked breaking unrelated runtime/RPC startup on a missing `git`
    executable or transient failure, before this capability is ever
    actually invoked). Construction itself therefore performs no external
    operation and cannot fail. `repository_validation()` and
    `register_state()` (EIP-ESR0055-001) share this same cached
    resolution rather than each re-resolving it independently.
    """

    def __init__(self) -> None:
        self._repo_root: str | None = None

    def _resolve_repo_root(self) -> str:
        if self._repo_root is None:
            result = subprocess.run(
                ["git", "-C", str(_MODULE_DIR), "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True,
            )
            self._repo_root = result.stdout.strip()
        return self._repo_root

    def _run_git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self._resolve_repo_root(),
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout

    def branch(self) -> str:
        # Detached HEAD reports the literal string "HEAD" via this command -
        # an honest, literal git observation, not a defect (Codex
        # design-review non-blocking note on EIP-ESR0054-002 v0.1).
        return self._run_git("rev-parse", "--abbrev-ref", "HEAD").strip()

    def uncommitted_file_count(self) -> int:
        output = self._run_git("status", "--porcelain")
        return len([line for line in output.splitlines() if line.strip()])

    def last_commit(self) -> tuple[str, str]:
        output = self._run_git("log", "-1", f"--format=%H{_GIT_LOG_FIELD_SEPARATOR}%s")
        sha, _, message = output.strip().partition(_GIT_LOG_FIELD_SEPARATOR)
        return sha, message

    def repository_validation(self) -> tuple[int, int]:
        """Run `scripts/validate_repository.py` as a subprocess (not an
        in-process import) and parse its printed summary line.

        Deliberately shells out rather than importing
        `scripts.validate_repository` - `scripts/` is repository tooling,
        not part of `jarvis/`'s own PyInstaller sidecar import graph
        (`scripts/build_backend_sidecar.py`), and importing it here would
        blur that packaging boundary. This mirrors the exact CLI contract
        README.md already documents (`python scripts/validate_repository.py`)
        - what GIA reports matches 1:1 what a human running the same
        command sees. Never fabricates a count: an unparseable summary
        line (missing script, unexpected output format) raises rather
        than returning a guessed value.
        """

        script_path = Path(self._resolve_repo_root()) / "scripts" / "validate_repository.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
        )
        match = _VALIDATION_SUMMARY_PATTERN.search(result.stdout)
        if not match:
            msg = (
                f"Could not parse a repository validation summary line from '{script_path}' "
                f"output (exit code {result.returncode})."
            )
            raise RuntimeError(msg)
        return int(match.group(1)), int(match.group(2))

    def register_state(self) -> tuple[str, str, str]:
        """Read REG-0001 directly (no subprocess) and return the
        highest-numbered `RBL-*` row's ID, and the highest-numbered
        `ESR-*` row's ID and its own literal Status column value.

        Unfiltered by status - see this module's own docstring. Row
        parsing mirrors `scripts/validate_repository.parse_register_rows()`'s
        shape without importing it, for the same packaging-boundary
        reason as `repository_validation()`.
        """

        register_path = Path(self._resolve_repo_root()) / _REGISTER_RELATIVE_PATH
        text = register_path.read_text(encoding="utf-8", errors="replace")

        rows: list[tuple[str, str]] = []
        for line in text.splitlines():
            if not line.startswith("| "):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) < 5:
                continue
            artefact_id = cells[0]
            if not _ARTEFACT_ID_PATTERN.match(artefact_id):
                continue
            rows.append((artefact_id, cells[4]))

        def _highest(prefix: str) -> tuple[str, str] | None:
            candidates = [
                (int(artefact_id.split("-")[1]), artefact_id, status)
                for artefact_id, status in rows
                if artefact_id.startswith(f"{prefix}-")
            ]
            if not candidates:
                return None
            _, artefact_id, status = max(candidates, key=lambda item: item[0])
            return artefact_id, status

        baseline = _highest("RBL")
        session = _highest("ESR")
        if baseline is None or session is None:
            msg = f"REG-0001 register at '{register_path}' has no RBL-*/ESR-* rows to report."
            raise RuntimeError(msg)

        current_repository_baseline, _ = baseline
        latest_registered_session, latest_registered_session_status = session
        return current_repository_baseline, latest_registered_session, latest_registered_session_status


class EngineeringStateObserver:
    """GIA Phase 3: observes and publishes real repository engineering state.

    Contains no thresholds, alerts or branching on the values it reads -
    a pure read-and-report boundary, matching `LocalResourceObserver`'s
    own constraint (ESR-0011 Section 10).
    """

    def __init__(self, reader: EngineeringStateReader | None = None) -> None:
        self._reader = reader or RealEngineeringStateReader()

    def snapshot(self) -> EngineeringSnapshot:
        """Return a real, current engineering state snapshot.

        Propagates whatever the underlying reader raises on failure -
        never fabricates a value, per the project's no-mock-fallback rule.
        Every call re-reads fresh (no caching of validation/register
        results across snapshots) - a real, disclosed latency cost for
        `repository_validation()` in particular, since it runs a full
        markdown-scanning subprocess rather than a near-instant git/file
        read.
        """

        branch = self._reader.branch()
        uncommitted_files = self._reader.uncommitted_file_count()
        sha, message = self._reader.last_commit()
        validation_errors, validation_warnings = self._reader.repository_validation()
        baseline, session, session_status = self._reader.register_state()
        snapshot = EngineeringSnapshot(
            git_branch=branch,
            git_uncommitted_files=uncommitted_files,
            git_last_commit_sha=sha,
            git_last_commit_message=message,
            repository_validation_errors=validation_errors,
            repository_validation_warnings=validation_warnings,
            current_repository_baseline=baseline,
            latest_registered_session=session,
            latest_registered_session_status=session_status,
            captured_at=datetime.now(UTC),
        )
        logger.info(
            "GIA engineering snapshot captured: branch=%s uncommitted=%d commit=%s "
            "validation_errors=%d validation_warnings=%d baseline=%s session=%s/%s",
            snapshot.git_branch,
            snapshot.git_uncommitted_files,
            snapshot.git_last_commit_sha[:8],
            snapshot.repository_validation_errors,
            snapshot.repository_validation_warnings,
            snapshot.current_repository_baseline,
            snapshot.latest_registered_session,
            snapshot.latest_registered_session_status,
        )
        return snapshot
