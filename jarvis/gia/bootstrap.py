"""GIA bootstrap readiness primitives."""

import logging
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ReadinessState(Enum):
    """Supported readiness outcomes for GIA bootstrap evaluation."""

    READY = "Ready"
    NOT_READY = "Not ready"


@dataclass(frozen=True)
class EngineeringRequest:
    """Approved engineering request submitted for GIA bootstrap evaluation."""

    identifier: str
    objective: str
    scope: tuple[str, ...] = ()
    out_of_scope: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "scope", _normalise_items(self.scope))
        object.__setattr__(self, "out_of_scope", _normalise_items(self.out_of_scope))


@dataclass(frozen=True)
class EngineeringReadinessContext:
    """Readiness result for an approved engineering request."""

    request: EngineeringRequest
    state: ReadinessState
    findings: tuple[str, ...] = ()

    @property
    def ready(self) -> bool:
        """Return whether the request is ready for engineering execution."""

        return self.state is ReadinessState.READY


class GiaBootstrap:
    """Evaluate minimum GIA engineering readiness before execution."""

    def evaluate(self, request: EngineeringRequest) -> EngineeringReadinessContext:
        """Evaluate whether an engineering request has minimum readiness inputs."""

        findings = _readiness_findings(request)
        state = ReadinessState.NOT_READY if findings else ReadinessState.READY
        logger.info("GIA bootstrap readiness evaluated: %s", state.value)
        return EngineeringReadinessContext(
            request=request,
            state=state,
            findings=tuple(findings),
        )

    def boot(self, request: EngineeringRequest) -> EngineeringReadinessContext:
        """Run the GIA bootstrap readiness evaluation."""

        return self.evaluate(request)


def _readiness_findings(request: EngineeringRequest) -> list[str]:
    findings: list[str] = []

    if not request.identifier.strip():
        findings.append("Engineering request identifier is required.")
    if not request.objective.strip():
        findings.append("Engineering request objective is required.")
    if not request.scope:
        findings.append("Approved engineering scope is required.")

    return findings


def _normalise_items(items: Iterable[str]) -> tuple[str, ...]:
    return tuple(item.strip() for item in items if item.strip())
