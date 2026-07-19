from datetime import datetime, timezone

import pytest

from jarvis import GiaSnapshot, LocalResourceObserver


class _FakeVirtualMemory:
    def __init__(self, percent: float, used: int, total: int) -> None:
        self.percent = percent
        self.used = used
        self.total = total


class _FakeResourceReader:
    def __init__(self, cpu_percent: float, memory: _FakeVirtualMemory) -> None:
        self._cpu_percent = cpu_percent
        self._memory = memory
        self.cpu_percent_calls: list[float] = []

    def cpu_percent(self, interval: float) -> float:
        self.cpu_percent_calls.append(interval)
        return self._cpu_percent

    def virtual_memory(self) -> _FakeVirtualMemory:
        return self._memory


class _FailingResourceReader:
    def cpu_percent(self, interval: float) -> float:  # noqa: ARG002
        msg = "simulated resource read failure"
        raise OSError(msg)

    def virtual_memory(self) -> _FakeVirtualMemory:
        raise AssertionError("should not be called after cpu_percent fails")


def test_local_resource_observer_returns_real_snapshot_from_injected_reader() -> None:
    memory = _FakeVirtualMemory(percent=42.5, used=4 * 1024 * 1024 * 1024, total=8 * 1024 * 1024 * 1024)
    reader = _FakeResourceReader(cpu_percent=17.3, memory=memory)
    observer = LocalResourceObserver(reader=reader)

    snapshot = observer.snapshot()

    assert isinstance(snapshot, GiaSnapshot)
    assert snapshot.cpu_percent == 17.3
    assert snapshot.memory_percent == 42.5
    assert snapshot.memory_used_mb == pytest.approx(4096.0)
    assert snapshot.memory_total_mb == pytest.approx(8192.0)
    assert snapshot.captured_at.tzinfo is not None
    assert snapshot.captured_at <= datetime.now(timezone.utc)


def test_local_resource_observer_samples_cpu_with_a_real_interval_not_zero() -> None:
    memory = _FakeVirtualMemory(percent=1.0, used=1, total=2)
    reader = _FakeResourceReader(cpu_percent=0.0, memory=memory)
    observer = LocalResourceObserver(reader=reader)

    observer.snapshot()

    assert reader.cpu_percent_calls == [pytest.approx(0.2)]


def test_local_resource_observer_propagates_reader_failure_without_fabricating_a_snapshot() -> None:
    observer = LocalResourceObserver(reader=_FailingResourceReader())

    with pytest.raises(OSError, match="simulated resource read failure"):
        observer.snapshot()


def test_local_resource_observer_defaults_to_the_real_psutil_reader() -> None:
    observer = LocalResourceObserver()

    snapshot = observer.snapshot()

    assert 0.0 <= snapshot.cpu_percent <= 100.0
    assert 0.0 <= snapshot.memory_percent <= 100.0
    assert snapshot.memory_used_mb > 0
    assert snapshot.memory_total_mb >= snapshot.memory_used_mb
