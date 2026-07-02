"""Service primitives for JARVIS OS."""

from jarvis.services.capability import CapabilityDescriptor, CapabilityRegistry
from jarvis.services.model import JarvisService
from jarvis.services.status import ServiceHealth, ServiceStatus

__all__ = [
    "CapabilityDescriptor",
    "CapabilityRegistry",
    "JarvisService",
    "ServiceHealth",
    "ServiceStatus",
]