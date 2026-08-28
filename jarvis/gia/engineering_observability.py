"""GIA Phase 3a: engineering (git) state observability (EBG-0083,
EIP-ESR0054-002).

The first slice of EBG-0083 Phase 3 ("engineering instrumentation -
repository health, session/baseline state, git state"). Deliberately
scoped to git state only - repository health (`validate_repository.py`)
and session/baseline state (REG-0001) are separate, not-yet-delivered
future slices (Phase 3b/3c), matching the staged, small, evidence-led
delivery discipline Phase 1's own four increments (1a/1b/1c/1d) already
established.

Kept as a separate module rather than extending `jarvis.gia.observability`
directly: git state is a distinct subprocess-backed data domain, not a
`psutil` reading, so it needs its own reader abstraction rather than
overloading `ResourceReader`.

Per ESR-0011 Section 10, GIA "shall observe and publish state. It shall
not become a policy engine, decision-maker or owner of platform state" -
`EngineeringStateObserver` contains no thresholds, alerts or branching on
the values it reads, matching `LocalResourceObserver`'s own constraint.
"""

import logging
import subprocess
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


@dataclass(frozen=True)
class EngineeringSnapshot:
    """A single real, current engineering (git) state observation."""

    git_branch: str
    git_uncommitted_files: int
    git_last_commit_sha: str
    git_last_commit_message: str
    captured_at: datetime


class GitStateReader(Protocol):
    """Reads real repository git state - implemented by the real `git` CLI
    in production, substitutable with a fake in tests so unit tests never
    depend on this repository's own live git state."""

    def branch(self) -> str: ...

    def uncommitted_file_count(self) -> int: ...

    def last_commit(self) -> tuple[str, str]:
        """Return (sha, subject) of the most recent commit."""
        ...


class RealGitStateReader:
    """Default production reader, backed by the real `git` CLI.

    The repository root is resolved lazily, on first use inside a git
    command's own invocation - never at construction - and cached after
    that first successful resolution (Codex design-review correction on
    EIP-ESR0054-002 v0.1: eager resolution at construction risked breaking
    unrelated runtime/RPC startup on a missing `git` executable or
    transient failure, before this capability is ever actually invoked).
    Construction itself therefore performs no external operation and
    cannot fail.
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


class EngineeringStateObserver:
    """GIA Phase 3a: observes and publishes real repository git state.

    Contains no thresholds, alerts or branching on the values it reads -
    a pure read-and-report boundary, matching `LocalResourceObserver`'s
    own constraint (ESR-0011 Section 10).
    """

    def __init__(self, reader: GitStateReader | None = None) -> None:
        self._reader = reader or RealGitStateReader()

    def snapshot(self) -> EngineeringSnapshot:
        """Return a real, current engineering (git) state snapshot.

        Propagates whatever the underlying reader raises on failure -
        never fabricates a value, per the project's no-mock-fallback rule.
        """

        branch = self._reader.branch()
        uncommitted_files = self._reader.uncommitted_file_count()
        sha, message = self._reader.last_commit()
        snapshot = EngineeringSnapshot(
            git_branch=branch,
            git_uncommitted_files=uncommitted_files,
            git_last_commit_sha=sha,
            git_last_commit_message=message,
            captured_at=datetime.now(UTC),
        )
        logger.info(
            "GIA engineering snapshot captured: branch=%s uncommitted=%d commit=%s",
            snapshot.git_branch,
            snapshot.git_uncommitted_files,
            snapshot.git_last_commit_sha[:8],
        )
        return snapshot
