"""Applying the audit retention setting (ESR-0061 WP5b, EIP-ESR0061-005 6.4).

Runs once at start and once a day while the backend runs, and immediately when
an Administrator changes the setting. Counts only; never any content.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable

from jarvis.shared.settings import SettingsStore
from sentinel.audit import JsonAuditRecorder, PruneResult

logger = logging.getLogger(__name__)

PRUNE_INTERVAL_SECONDS = 24 * 60 * 60


class RetentionService:
    def __init__(self, recorder: JsonAuditRecorder, settings: SettingsStore) -> None:
        self._recorder = recorder
        self._settings = settings
        self._last: PruneResult | None = None
        self._lock = threading.Lock()
        # Other records kept for the same number of days (ESR-0061 WP6b: the
        # safety events in the identity database). Each takes the days.
        self._extra_pruners: list[Callable[[int], object]] = []

    def add_pruner(self, prune: Callable[[int], object]) -> None:
        """Prune another record by the same retention setting."""

        self._extra_pruners.append(prune)

    @property
    def settings(self) -> SettingsStore:
        return self._settings

    def run_once(self) -> PruneResult | None:
        """Prune now. A failure is logged by type and does not stop the backend."""

        try:
            result = self._recorder.prune_older_than(self._settings.retention_days())
        except Exception as exc:  # noqa: BLE001 - retention must never take the backend down
            logger.warning("Audit retention could not run (%s).", type(exc).__name__)
            return None
        for prune in list(self._extra_pruners):
            try:
                prune(self._settings.retention_days())
            except Exception as exc:  # noqa: BLE001 - retention must never take the backend down
                logger.warning("A retention pruner could not run (%s).", type(exc).__name__)
        with self._lock:
            self._last = result
        return result

    def last_result(self) -> PruneResult | None:
        with self._lock:
            return self._last

    def run_forever(self, stop_event: threading.Event, interval_seconds: float = PRUNE_INTERVAL_SECONDS) -> None:
        """Prune at start, then every `interval_seconds`, until `stop_event` is set."""

        self.run_once()
        while not stop_event.wait(interval_seconds):
            self.run_once()


__all__ = ["PRUNE_INTERVAL_SECONDS", "RetentionService"]
