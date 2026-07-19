"""GIA Phase 1a/1b/1c/1d: local resource observability (EBG-0083,
EIP-ESR0029-002/003/004/005).

Distinct from `jarvis.gia.bootstrap` (GIA-BOOT, ESR-0012 WP3), which
evaluates engineering-request readiness and has no connection to platform
telemetry. This module is GIA's first real observability slice.
"""

import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

import psutil

logger = logging.getLogger(__name__)

# A bare psutil.cpu_percent() call returns a meaningless 0.0 on first
# invocation - it measures usage between two calls, not an instant value.
# A short blocking sample gives a real, honest reading at the cost of this
# one RPC call taking slightly longer, an accepted tradeoff for a status
# check rather than a hot path.
CPU_SAMPLE_INTERVAL_SECONDS = 0.2

_BYTES_PER_MEGABYTE = 1024 * 1024
_BYTES_PER_GIGABYTE = 1024 * 1024 * 1024

# Cross-platform-safe storage path: os.sep resolves to a real, meaningful
# root on POSIX ("/") and to the current working directory's drive root on
# Windows (e.g. "C:\\") - never a hardcoded drive letter guess.
STORAGE_PATH = os.path.abspath(os.sep)

# Local engineering-environment state (EBG-0083 Phase 1d): a small, fixed,
# disclosed list of named tools, per ESR-0011's own FCH-0011 discussion.
# Real process names, not guessed - confirmed directly via `tasklist`
# against the Programme Sponsor's actual running machine. ChatGPT
# Desktop's real name ("ChatGPT Classic.exe") differs from the obvious
# guess ("ChatGPT.exe"), which is exactly why this was verified rather
# than assumed - both are listed as candidates in case a future install
# uses the other name.
ENGINEERING_TOOLS: dict[str, tuple[str, ...]] = {
    "vscode": ("Code.exe",),
    "obsidian": ("Obsidian.exe",),
    "githubDesktop": ("GitHubDesktop.exe",),
    "chatgpt": ("ChatGPT.exe", "ChatGPT Classic.exe"),
}


@dataclass(frozen=True)
class GiaSnapshot:
    """A single real, current local resource observation."""

    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_total_mb: float
    disk_percent: float
    disk_used_gb: float
    disk_total_gb: float
    process_status: str
    process_uptime_seconds: float
    process_cpu_percent: float
    process_memory_mb: float
    engineering_tools_running: dict[str, bool]
    captured_at: datetime


class ResourceReader(Protocol):
    """Reads real host CPU/memory/disk/process state - implemented by
    `psutil` in production, substitutable with a fake in tests so unit
    tests never depend on the actual host machine's live resource state."""

    def cpu_percent(self, interval: float) -> float: ...

    def virtual_memory(self) -> "VirtualMemory": ...

    def disk_usage(self, path: str) -> "DiskUsage": ...

    def process_health(self, interval: float) -> "ProcessHealth": ...

    def running_process_names(self) -> frozenset[str]: ...


class VirtualMemory(Protocol):
    """Shape this module needs from `psutil.virtual_memory()`'s return value."""

    percent: float
    used: int
    total: int


class DiskUsage(Protocol):
    """Shape this module needs from `psutil.disk_usage()`'s return value."""

    percent: float
    used: int
    total: int


class ProcessHealth(Protocol):
    """Shape this module needs describing the JARVIS backend's own process -
    self-observation only (`psutil.Process(os.getpid())`), never an
    externally-specified PID."""

    status: str
    create_time: float
    cpu_percent: float
    memory_rss: int


@dataclass(frozen=True)
class _ProcessHealthSnapshot:
    status: str
    create_time: float
    cpu_percent: float
    memory_rss: int


class PsutilResourceReader:
    """Default production reader, backed by the real `psutil` library."""

    def cpu_percent(self, interval: float) -> float:
        return psutil.cpu_percent(interval=interval)

    def virtual_memory(self) -> "VirtualMemory":
        return psutil.virtual_memory()

    def disk_usage(self, path: str) -> "DiskUsage":
        return psutil.disk_usage(path)

    def process_health(self, interval: float) -> "ProcessHealth":
        process = psutil.Process(os.getpid())
        return _ProcessHealthSnapshot(
            status=process.status(),
            create_time=process.create_time(),
            cpu_percent=process.cpu_percent(interval=interval),
            memory_rss=process.memory_info().rss,
        )

    def running_process_names(self) -> frozenset[str]:
        return frozenset(
            proc.info["name"] for proc in psutil.process_iter(["name"]) if proc.info["name"]
        )


class LocalResourceObserver:
    """GIA Phase 1a/1b/1c: observes and publishes real local CPU/memory/disk/
    process state.

    Per ESR-0011 Section 10, GIA "shall observe and publish state. It
    shall not become a policy engine, decision-maker or owner of platform
    state" - this class contains no thresholds, alerts or branching on the
    values it reads; it is a pure read-and-report boundary.
    """

    def __init__(self, reader: ResourceReader | None = None) -> None:
        self._reader = reader or PsutilResourceReader()

    def snapshot(self) -> GiaSnapshot:
        """Return a real, current local resource snapshot.

        Propagates whatever the underlying reader raises on failure -
        never fabricates a value, per the project's no-mock-fallback rule.
        """

        cpu_percent = self._reader.cpu_percent(interval=CPU_SAMPLE_INTERVAL_SECONDS)
        memory = self._reader.virtual_memory()
        disk = self._reader.disk_usage(STORAGE_PATH)
        process = self._reader.process_health(interval=CPU_SAMPLE_INTERVAL_SECONDS)
        running_names = self._reader.running_process_names()
        engineering_tools_running = {
            tool: any(name in running_names for name in candidates)
            for tool, candidates in ENGINEERING_TOOLS.items()
        }
        snapshot = GiaSnapshot(
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / _BYTES_PER_MEGABYTE,
            memory_total_mb=memory.total / _BYTES_PER_MEGABYTE,
            disk_percent=disk.percent,
            disk_used_gb=disk.used / _BYTES_PER_GIGABYTE,
            disk_total_gb=disk.total / _BYTES_PER_GIGABYTE,
            process_status=process.status,
            process_uptime_seconds=time.time() - process.create_time,
            process_cpu_percent=process.cpu_percent,
            process_memory_mb=process.memory_rss / _BYTES_PER_MEGABYTE,
            engineering_tools_running=engineering_tools_running,
            captured_at=datetime.now(timezone.utc),
        )
        logger.info(
            "GIA local resource snapshot captured: cpu=%.1f%% memory=%.1f%% disk=%.1f%%",
            snapshot.cpu_percent,
            snapshot.memory_percent,
            snapshot.disk_percent,
        )
        return snapshot
