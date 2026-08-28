import subprocess
from datetime import UTC, datetime

import pytest

from jarvis import EngineeringSnapshot, EngineeringStateObserver
from jarvis.gia.engineering_observability import RealGitStateReader


class _FakeGitStateReader:
    def __init__(
        self,
        branch: str = "main",
        uncommitted_file_count: int = 0,
        last_commit: tuple[str, str] = ("abc123", "example commit"),
    ) -> None:
        self._branch = branch
        self._uncommitted_file_count = uncommitted_file_count
        self._last_commit = last_commit
        self.branch_calls = 0
        self.uncommitted_file_count_calls = 0
        self.last_commit_calls = 0

    def branch(self) -> str:
        self.branch_calls += 1
        return self._branch

    def uncommitted_file_count(self) -> int:
        self.uncommitted_file_count_calls += 1
        return self._uncommitted_file_count

    def last_commit(self) -> tuple[str, str]:
        self.last_commit_calls += 1
        return self._last_commit


class _FailingGitStateReader:
    def branch(self) -> str:
        msg = "simulated git failure"
        raise subprocess.CalledProcessError(returncode=128, cmd=["git", "rev-parse"], stderr=msg)

    def uncommitted_file_count(self) -> int:
        raise AssertionError("should not be called after branch() fails")

    def last_commit(self) -> tuple[str, str]:
        raise AssertionError("should not be called after branch() fails")


def test_engineering_state_observer_returns_real_snapshot_from_injected_reader() -> None:
    reader = _FakeGitStateReader(
        branch="feature/gia-phase3a",
        uncommitted_file_count=2,
        last_commit=("deadbeefcafe", "GIA Phase 3a"),
    )
    observer = EngineeringStateObserver(reader=reader)

    snapshot = observer.snapshot()

    assert isinstance(snapshot, EngineeringSnapshot)
    assert snapshot.git_branch == "feature/gia-phase3a"
    assert snapshot.git_uncommitted_files == 2
    assert snapshot.git_last_commit_sha == "deadbeefcafe"
    assert snapshot.git_last_commit_message == "GIA Phase 3a"
    assert snapshot.captured_at.tzinfo is not None
    assert snapshot.captured_at <= datetime.now(UTC)
    assert reader.branch_calls == 1
    assert reader.uncommitted_file_count_calls == 1
    assert reader.last_commit_calls == 1


def test_engineering_state_observer_propagates_reader_failure_without_fabricating_a_snapshot() -> None:
    observer = EngineeringStateObserver(reader=_FailingGitStateReader())

    with pytest.raises(subprocess.CalledProcessError):
        observer.snapshot()


def test_real_git_state_reader_construction_is_side_effect_free() -> None:
    """Codex design-review correction on EIP-ESR0054-002 v0.1: repository
    root resolution must be lazy, on first git-command invocation, not at
    construction - a missing `git` executable or transient failure must
    not be able to break unrelated object construction. Asserted here by
    confirming no `_repo_root` is resolved until a real method is called."""

    reader = RealGitStateReader()

    assert reader._repo_root is None  # noqa: SLF001 - the exact behaviour under test


def test_real_git_state_reader_caches_the_resolved_repo_root_after_first_use() -> None:
    reader = RealGitStateReader()

    reader.branch()

    assert reader._repo_root is not None  # noqa: SLF001 - the exact behaviour under test
    resolved_once = reader._repo_root  # noqa: SLF001

    reader.uncommitted_file_count()

    assert reader._repo_root == resolved_once  # noqa: SLF001 - not re-resolved on a second call


def test_engineering_state_observer_defaults_to_the_real_git_backed_reader() -> None:
    observer = EngineeringStateObserver()

    snapshot = observer.snapshot()

    assert snapshot.git_branch
    assert snapshot.git_uncommitted_files >= 0
    assert len(snapshot.git_last_commit_sha) == 40
    assert snapshot.git_last_commit_message
