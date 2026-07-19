"""GIA Phase 1a: local resource observability (EBG-0083, EIP-ESR0029-002).

Distinct from `jarvis.gia.bootstrap` (GIA-BOOT, ESR-0012 WP3), which
evaluates engineering-request readiness and has no connection to platform
telemetry. This module is GIA's first real observability slice.
"""

import logging
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


@dataclass(frozen=True)
class GiaSnapshot:
    """A single real, current local resource observation."""

    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_total_mb: float
    captured_at: datetime


class ResourceReader(Protocol):
    """Reads real host CPU/memory state - implemented by `psutil` in
    production, substitutable with a fake in tests so unit tests never
    depend on the actual host machine's live resource state."""

    def cpu_percent(self, interval: float) -> float: ...

    def virtual_memory(self) -> "VirtualMemory": ...


class VirtualMemory(Protocol):
    """Shape this module needs from `psutil.virtual_memory()`'s return value."""

    percent: float
    used: int
    total: int


class PsutilResourceReader:
    """Default production reader, backed by the real `psutil` library."""

    def cpu_percent(self, interval: float) -> float:
        return psutil.cpu_percent(interval=interval)

    def virtual_memory(self) -> "VirtualMemory":
        return psutil.virtual_memory()


class LocalResourceObserver:
    """GIA Phase 1a: observes and publishes real local CPU/memory state.

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
        snapshot = GiaSnapshot(
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / _BYTES_PER_MEGABYTE,
            memory_total_mb=memory.total / _BYTES_PER_MEGABYTE,
            captured_at=datetime.now(timezone.utc),
        )
        logger.info(
            "GIA local resource snapshot captured: cpu=%.1f%% memory=%.1f%%",
            snapshot.cpu_percent,
            snapshot.memory_percent,
        )
        return snapshot
