"""Service status definitions for JARVIS OS."""

from enum import Enum


class ServiceStatus(Enum):
    """Supported service status values."""

    ONLINE = "Online"
    OFFLINE = "Offline"
    UNAVAILABLE = "Unavailable"
    STARTING = "Starting"
