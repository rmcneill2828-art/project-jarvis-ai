"""Household settings kept beside the databases (ESR-0061 WP5b).

One small JSON file. Today it holds one value, how long the audit log is kept
(EIP-ESR0061-005 R1). A missing, unreadable or out-of-range file means the
default, never an error and never "keep for ever": there is always a limit.
Writes are atomic (a temporary file, then a replace) and serialised.
"""

from __future__ import annotations

import json
import logging
import os
import threading
from pathlib import Path

logger = logging.getLogger(__name__)

ALLOWED_RETENTION_DAYS = (30, 90, 365)
DEFAULT_RETENTION_DAYS = 90
SETTINGS_FILENAME = "settings.json"


class SettingsStore:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._lock = threading.Lock()

    def _read(self) -> dict[str, object]:
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
        return data if isinstance(data, dict) else {}

    def retention_days(self) -> int:
        with self._lock:
            value = self._read().get("auditRetentionDays")
        if isinstance(value, int) and not isinstance(value, bool) and value in ALLOWED_RETENTION_DAYS:
            return value
        return DEFAULT_RETENTION_DAYS

    def set_retention_days(self, days: int) -> int:
        if not isinstance(days, int) or isinstance(days, bool) or days not in ALLOWED_RETENTION_DAYS:
            msg = "Audit retention must be one of: " + ", ".join(str(item) for item in ALLOWED_RETENTION_DAYS) + " days."
            raise ValueError(msg)
        with self._lock:
            data = self._read()
            data["auditRetentionDays"] = days
            self._path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self._path.with_name(f"{self._path.name}.tmp")
            temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            os.replace(temporary, self._path)
        return days


__all__ = ["ALLOWED_RETENTION_DAYS", "DEFAULT_RETENTION_DAYS", "SETTINGS_FILENAME", "SettingsStore"]
