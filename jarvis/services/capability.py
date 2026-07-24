"""Capability registry primitives for the JARVIS platform foundation."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class CapabilityDescriptor:
    """Describe a capability known to the platform without executing it."""

    name: str
    summary: str
    status: str = "Placeholder"

    def __post_init__(self) -> None:
        if not self.name.strip():
            msg = "Capability name must not be empty."
            raise ValueError(msg)
        if not self.summary.strip():
            msg = "Capability summary must not be empty."
            raise ValueError(msg)
        if not self.status.strip():
            msg = "Capability status must not be empty."
            raise ValueError(msg)


class CapabilityRegistry:
    """Register and list capability descriptors without executing capabilities."""

    def __init__(self) -> None:
        self._capabilities: dict[str, CapabilityDescriptor] = {}

    def register(self, descriptor: CapabilityDescriptor) -> CapabilityDescriptor:
        """Register or replace a capability descriptor."""

        self._capabilities[descriptor.name] = descriptor
        return descriptor

    def list_capabilities(self) -> tuple[CapabilityDescriptor, ...]:
        """Return registered capability descriptors in name order."""

        return tuple(self._capabilities[name] for name in sorted(self._capabilities))

    def capabilities(self) -> Mapping[str, CapabilityDescriptor]:
        """Return registered capability descriptors keyed by name."""

        return MappingProxyType(dict(self._capabilities))