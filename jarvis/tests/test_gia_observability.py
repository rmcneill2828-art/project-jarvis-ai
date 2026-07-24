import time
from datetime import UTC, datetime

import pytest

from jarvis import GiaSnapshot, LocalResourceObserver


class _FakeVirtualMemory:
    def __init__(self, percent: float, used: int, total: int) -> None:
        self.percent = percent
        self.used = used
        self.total = total


class _FakeDiskUsage:
    def __init__(self, percent: float, used: int, total: int) -> None:
        self.percent = percent
        self.used = used
        self.total = total


class _FakeProcessHealth:
    def __init__(self, status: str, create_time: float, cpu_percent: float, memory_rss: int) -> None:
        self.status = status
        self.create_time = create_time
        self.cpu_percent = cpu_percent
        self.memory_rss = memory_rss


class _FakeResourceReader:
    def __init__(
        self,
        cpu_percent: float,
        memory: _FakeVirtualMemory,
        disk: _FakeDiskUsage,
        process: _FakeProcessHealth,
        running_names: frozenset[str] = frozenset(),
    ) -> None:
        self._cpu_percent = cpu_percent
        self._memory = memory
        self._disk = disk
        self._process = process
        self._running_names = running_names
        self.cpu_percent_calls: list[float] = []
        self.disk_usage_calls: list[str] = []
        self.process_health_calls: list[float] = []
        self.running_process_names_calls = 0

    def cpu_percent(self, interval: float) -> float:
        self.cpu_percent_calls.append(interval)
        return self._cpu_percent

    def virtual_memory(self) -> _FakeVirtualMemory:
        return self._memory

    def disk_usage(self, path: str) -> _FakeDiskUsage:
        self.disk_usage_calls.append(path)
        return self._disk

    def process_health(self, interval: float) -> _FakeProcessHealth:
        self.process_health_calls.append(interval)
        return self._process

    def running_process_names(self) -> frozenset[str]:
        self.running_process_names_calls += 1
        return self._running_names


class _FailingResourceReader:
    def cpu_percent(self, interval: float) -> float:
        msg = "simulated resource read failure"
        raise OSError(msg)

    def virtual_memory(self) -> _FakeVirtualMemory:
        raise AssertionError("should not be called after cpu_percent fails")

    def disk_usage(self, path: str) -> _FakeDiskUsage:
        raise AssertionError("should not be called after cpu_percent fails")

    def process_health(self, interval: float) -> _FakeProcessHealth:
        raise AssertionError("should not be called after cpu_percent fails")

    def running_process_names(self) -> frozenset[str]:
        raise AssertionError("should not be called after cpu_percent fails")


def test_local_resource_observer_returns_real_snapshot_from_injected_reader() -> None:
    memory = _FakeVirtualMemory(percent=42.5, used=4 * 1024 * 1024 * 1024, total=8 * 1024 * 1024 * 1024)
    disk = _FakeDiskUsage(percent=28.7, used=430 * 1024 * 1024 * 1024, total=1500 * 1024 * 1024 * 1024)
    process = _FakeProcessHealth(
        status="running",
        create_time=time.time() - 120.0,
        cpu_percent=3.2,
        memory_rss=64 * 1024 * 1024,
    )
    reader = _FakeResourceReader(
        cpu_percent=17.3,
        memory=memory,
        disk=disk,
        process=process,
        running_names=frozenset({"Code.exe", "ChatGPT Classic.exe"}),
    )
    observer = LocalResourceObserver(reader=reader)

    snapshot = observer.snapshot()

    assert isinstance(snapshot, GiaSnapshot)
    assert snapshot.cpu_percent == 17.3
    assert snapshot.memory_percent == 42.5
    assert snapshot.memory_used_mb == pytest.approx(4096.0)
    assert snapshot.memory_total_mb == pytest.approx(8192.0)
    assert snapshot.disk_percent == 28.7
    assert snapshot.disk_used_gb == pytest.approx(430.0)
    assert snapshot.disk_total_gb == pytest.approx(1500.0)
    assert snapshot.process_status == "running"
    assert snapshot.process_uptime_seconds == pytest.approx(120.0, abs=1.0)
    assert snapshot.process_cpu_percent == 3.2
    assert snapshot.process_memory_mb == pytest.approx(64.0)
    assert snapshot.engineering_tools_running == {
        "vscode": True,
        "obsidian": False,
        "githubDesktop": False,
        "chatgpt": True,
    }
    assert snapshot.captured_at.tzinfo is not None
    assert snapshot.captured_at <= datetime.now(UTC)


def test_local_resource_observer_matches_chatgpt_desktop_under_either_candidate_name() -> None:
    """ChatGPT Desktop's real process name (`ChatGPT Classic.exe`) differs
    from the obvious guess (`ChatGPT.exe`) - confirmed directly via
    `tasklist` against the Programme Sponsor's real machine. Both are
    configured as candidates; this proves either alone is sufficient."""

    memory = _FakeVirtualMemory(percent=1.0, used=1, total=2)
    disk = _FakeDiskUsage(percent=1.0, used=1, total=2)
    process = _FakeProcessHealth(status="running", create_time=time.time(), cpu_percent=0.0, memory_rss=1)
    reader = _FakeResourceReader(
        cpu_percent=0.0, memory=memory, disk=disk, process=process, running_names=frozenset({"ChatGPT.exe"})
    )
    observer = LocalResourceObserver(reader=reader)

    snapshot = observer.snapshot()

    assert snapshot.engineering_tools_running["chatgpt"] is True


def test_local_resource_observer_reads_disk_usage_for_the_storage_path() -> None:
    from jarvis.gia.observability import STORAGE_PATH

    memory = _FakeVirtualMemory(percent=1.0, used=1, total=2)
    disk = _FakeDiskUsage(percent=1.0, used=1, total=2)
    process = _FakeProcessHealth(status="running", create_time=time.time(), cpu_percent=0.0, memory_rss=1)
    reader = _FakeResourceReader(cpu_percent=0.0, memory=memory, disk=disk, process=process)
    observer = LocalResourceObserver(reader=reader)

    observer.snapshot()

    assert reader.disk_usage_calls == [STORAGE_PATH]


def test_local_resource_observer_samples_cpu_with_a_real_interval_not_zero() -> None:
    memory = _FakeVirtualMemory(percent=1.0, used=1, total=2)
    disk = _FakeDiskUsage(percent=1.0, used=1, total=2)
    process = _FakeProcessHealth(status="running", create_time=time.time(), cpu_percent=0.0, memory_rss=1)
    reader = _FakeResourceReader(cpu_percent=0.0, memory=memory, disk=disk, process=process)
    observer = LocalResourceObserver(reader=reader)

    observer.snapshot()

    assert reader.cpu_percent_calls == [pytest.approx(0.2)]
    assert reader.process_health_calls == [pytest.approx(0.2)]


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
    assert 0.0 <= snapshot.disk_percent <= 100.0
    assert snapshot.disk_used_gb > 0
    assert snapshot.disk_total_gb >= snapshot.disk_used_gb
    assert snapshot.process_status
    assert snapshot.process_uptime_seconds >= 0
    assert snapshot.process_cpu_percent >= 0.0
    assert snapshot.process_memory_mb > 0
    assert set(snapshot.engineering_tools_running) == {"vscode", "obsidian", "githubDesktop", "chatgpt"}
    assert all(isinstance(value, bool) for value in snapshot.engineering_tools_running.values())
