"""Guardian runtime state definitions."""

from enum import Enum


class GuardianRuntimeState(Enum):
    """Supported Guardian runtime lifecycle states."""

    STOPPED = "Stopped"
    STARTING = "Starting"
    RUNNING = "Running"
    DEGRADED = "Degraded"
