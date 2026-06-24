"""
JARVIS Root Object

The Jarvis class represents the root orchestrator for the JARVIS platform.

Future services such as Memory, Guardian and Automation will be attached
to this object through composition rather than direct implementation.
"""


class Jarvis:
    """Root orchestrator for the JARVIS platform."""

    def start(self) -> str:
        """Start the platform."""

        return "JARVIS initialised"
