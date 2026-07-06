"""Guardian runtime configuration boundary."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GuardianRuntimeConfig:
    """Configuration for the minimum Guardian runtime foundation."""

    runtime_name: str = "Guardian"
    persistence_enabled: bool = False
    diagnostics_enabled: bool = True

    def __post_init__(self) -> None:
        if not self.runtime_name.strip():
            msg = "Guardian runtime name must not be empty."
            raise ValueError(msg)
