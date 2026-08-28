import subprocess
import sys
from datetime import UTC, datetime

import pytest

from jarvis import EngineeringSnapshot, EngineeringStateObserver
from jarvis.gia.engineering_observability import RealEngineeringStateReader


class _FakeEngineeringStateReader:
    def __init__(
        self,
        branch: str = "main",
        uncommitted_file_count: int = 0,
        last_commit: tuple[str, str] = ("abc123", "example commit"),
        repository_validation: tuple[int, int] = (0, 298),
        register_state: tuple[str, str, str] = ("RBL-0034", "ESR-0054", "Closed"),
    ) -> None:
        self._branch = branch
        self._uncommitted_file_count = uncommitted_file_count
        self._last_commit = last_commit
        self._repository_validation = repository_validation
        self._register_state = register_state
        self.branch_calls = 0
        self.uncommitted_file_count_calls = 0
        self.last_commit_calls = 0
        self.repository_validation_calls = 0
        self.register_state_calls = 0

    def branch(self) -> str:
        self.branch_calls += 1
        return self._branch

    def uncommitted_file_count(self) -> int:
        self.uncommitted_file_count_calls += 1
        return self._uncommitted_file_count

    def last_commit(self) -> tuple[str, str]:
        self.last_commit_calls += 1
        return self._last_commit

    def repository_validation(self) -> tuple[int, int]:
        self.repository_validation_calls += 1
        return self._repository_validation

    def register_state(self) -> tuple[str, str, str]:
        self.register_state_calls += 1
        return self._register_state


class _FailingEngineeringStateReader:
    def branch(self) -> str:
        msg = "simulated git failure"
        raise subprocess.CalledProcessError(returncode=128, cmd=["git", "rev-parse"], stderr=msg)

    def uncommitted_file_count(self) -> int:
        raise AssertionError("should not be called after branch() fails")

    def last_commit(self) -> tuple[str, str]:
        raise AssertionError("should not be called after branch() fails")

    def repository_validation(self) -> tuple[int, int]:
        raise AssertionError("should not be called after branch() fails")

    def register_state(self) -> tuple[str, str, str]:
        raise AssertionError("should not be called after branch() fails")


def test_engineering_state_observer_returns_real_snapshot_from_injected_reader() -> None:
    reader = _FakeEngineeringStateReader(
        branch="feature/gia-phase3a",
        uncommitted_file_count=2,
        last_commit=("deadbeefcafe", "GIA Phase 3a"),
        repository_validation=(0, 298),
        register_state=("RBL-0034", "ESR-0055", "Open"),
    )
    observer = EngineeringStateObserver(reader=reader)

    snapshot = observer.snapshot()

    assert isinstance(snapshot, EngineeringSnapshot)
    assert snapshot.git_branch == "feature/gia-phase3a"
    assert snapshot.git_uncommitted_files == 2
    assert snapshot.git_last_commit_sha == "deadbeefcafe"
    assert snapshot.git_last_commit_message == "GIA Phase 3a"
    assert snapshot.repository_validation_errors == 0
    assert snapshot.repository_validation_warnings == 298
    assert snapshot.current_repository_baseline == "RBL-0034"
    assert snapshot.latest_registered_session == "ESR-0055"
    assert snapshot.latest_registered_session_status == "Open"
    assert snapshot.captured_at.tzinfo is not None
    assert snapshot.captured_at <= datetime.now(UTC)
    assert reader.branch_calls == 1
    assert reader.uncommitted_file_count_calls == 1
    assert reader.last_commit_calls == 1
    assert reader.repository_validation_calls == 1
    assert reader.register_state_calls == 1


def test_engineering_state_observer_propagates_reader_failure_without_fabricating_a_snapshot() -> None:
    observer = EngineeringStateObserver(reader=_FailingEngineeringStateReader())

    with pytest.raises(subprocess.CalledProcessError):
        observer.snapshot()


def test_register_state_is_unfiltered_by_status() -> None:
    """Codex design-review correction on EIP-ESR0055-001 v0.1 -> v0.2,
    Programme Sponsor-selected: `register_state()` must report the
    highest-numbered ESR-* row's own literal status verbatim, including
    `Open` for a currently in-progress session - never silently falling
    back to a previous `Closed` row. This is a deliberate, different
    concept from `scripts/validate_repository.latest_closed_numbered()`."""

    reader = _FakeEngineeringStateReader(register_state=("RBL-0034", "ESR-0055", "Open"))
    observer = EngineeringStateObserver(reader=reader)

    snapshot = observer.snapshot()

    assert snapshot.latest_registered_session == "ESR-0055"
    assert snapshot.latest_registered_session_status == "Open"


def test_real_engineering_state_reader_construction_is_side_effect_free() -> None:
    """Codex design-review correction on EIP-ESR0054-002 v0.1: repository
    root resolution must be lazy, on first any-method invocation, not at
    construction - a missing `git` executable or transient failure must
    not be able to break unrelated object construction. Asserted here by
    confirming no `_repo_root` is resolved until a real method is called."""

    reader = RealEngineeringStateReader()

    assert reader._repo_root is None  # noqa: SLF001 - the exact behaviour under test


def test_real_engineering_state_reader_caches_the_resolved_repo_root_after_first_use() -> None:
    reader = RealEngineeringStateReader()

    reader.branch()

    assert reader._repo_root is not None  # noqa: SLF001 - the exact behaviour under test
    resolved_once = reader._repo_root  # noqa: SLF001

    reader.uncommitted_file_count()

    assert reader._repo_root == resolved_once  # noqa: SLF001 - not re-resolved on a second call


def test_real_engineering_state_reader_shares_one_resolved_repo_root_across_all_methods() -> None:
    """EIP-ESR0055-001 Section 5: `repository_validation()` and
    `register_state()` must reuse the same lazy-cached resolution
    `branch()`/`uncommitted_file_count()`/`last_commit()` already
    established, not each re-resolve it independently."""

    reader = RealEngineeringStateReader()

    reader.branch()
    resolved_once = reader._repo_root  # noqa: SLF001

    reader.repository_validation()
    reader.register_state()

    assert reader._repo_root == resolved_once  # noqa: SLF001


def test_engineering_state_observer_defaults_to_the_real_backed_reader() -> None:
    observer = EngineeringStateObserver()

    snapshot = observer.snapshot()

    assert snapshot.git_branch
    assert snapshot.git_uncommitted_files >= 0
    assert len(snapshot.git_last_commit_sha) == 40
    assert snapshot.git_last_commit_message
    assert snapshot.repository_validation_errors >= 0
    assert snapshot.repository_validation_warnings >= 0
    assert snapshot.current_repository_baseline.startswith("RBL-")
    assert snapshot.latest_registered_session.startswith("ESR-")
    assert snapshot.latest_registered_session_status


def test_real_engineering_state_reader_repository_validation_matches_a_direct_run() -> None:
    """Live verification (EIP-ESR0055-001 Section 5): the reader's parsed
    counts must match an independently-run `validate_repository.py`
    invocation on this actual repository, not fake-reader coverage alone."""

    reader = RealEngineeringStateReader()

    errors, warnings = reader.repository_validation()

    repo_root = reader._resolve_repo_root()  # noqa: SLF001 - reusing the already-resolved root directly
    result = subprocess.run(
        [sys.executable, "scripts/validate_repository.py"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    # "N error" is a substring of both this tool's own summary phrasings
    # ("N errors, ..." on pass; "N error(s), ..." on fail).
    assert f"{errors} error" in result.stdout
    assert f"{warnings} warning" in result.stdout


def test_real_engineering_state_reader_register_state_matches_a_direct_read() -> None:
    reader = RealEngineeringStateReader()

    baseline, session, status = reader.register_state()

    assert baseline.startswith("RBL-")
    assert session.startswith("ESR-")
    assert status
