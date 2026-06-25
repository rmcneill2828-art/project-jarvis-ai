"""
JARVIS Root Object.

The Jarvis class represents the root orchestrator for the JARVIS platform.
"""

from enum import Enum


class JarvisState(Enum):
    """Supported lifecycle states for the JARVIS platform."""

    STOPPED = "STOPPED"
    RUNNING = "RUNNING"


class Jarvis:
    """Root orchestrator for the JARVIS platform."""

    def __init__(self) -> None:
        self._state = JarvisState.STOPPED

    def start(self) -> JarvisState:
        """Start the platform."""

        self._state = JarvisState.RUNNING
        return self._state

    def stop(self) -> JarvisState:
        """Stop the platform."""

        self._state = JarvisState.STOPPED
        return self._state

    def status(self) -> JarvisState:
        """Return the current platform state."""

        return self._state