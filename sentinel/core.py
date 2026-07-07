"""Sentinel Core trust boundary primitives.

Sentinel is intentionally independent of the JARVIS package so it can become a
shared trust gateway for Guardian and future AI systems.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from types import MappingProxyType
from typing import Mapping


class SentinelDecisionOutcome(Enum):
    """Supported Sentinel trust decision outcomes."""

    ALLOW = "Allow"
    DENY = "Deny"
    REVIEW = "Review"


@dataclass(frozen=True)
class SentinelRequest:
    """Request presented to Sentinel before platform execution."""

    source: str
    intent: str
    payload_type: str = "generic"
    requires_approval: bool = False
    metadata: Mapping[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.source.strip():
            msg = "Sentinel request source must not be empty."
            raise ValueError(msg)
        if not self.intent.strip():
            msg = "Sentinel request intent must not be empty."
            raise ValueError(msg)
        if not self.payload_type.strip():
            msg = "Sentinel request payload type must not be empty."
            raise ValueError(msg)
        if self.created_at.tzinfo is None:
            msg = "Sentinel request timestamp must be timezone-aware."
            raise ValueError(msg)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True)
class SentinelDecision:
    """Sentinel trust decision for a submitted request."""

    outcome: SentinelDecisionOutcome
    reason: str
    trust_boundary: str = "Sentinel Core"
    requires_human_approval: bool = False
    decided_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.reason.strip():
            msg = "Sentinel decision reason must not be empty."
            raise ValueError(msg)
        if not self.trust_boundary.strip():
            msg = "Sentinel trust boundary must not be empty."
            raise ValueError(msg)
        if self.decided_at.tzinfo is None:
            msg = "Sentinel decision timestamp must be timezone-aware."
            raise ValueError(msg)


@dataclass(frozen=True)
class SentinelResponse:
    """Sentinel response returned to a requesting client."""

    request: SentinelRequest
    decision: SentinelDecision
    message: str

    def __post_init__(self) -> None:
        if not self.message.strip():
            msg = "Sentinel response message must not be empty."
            raise ValueError(msg)


class SentinelTrustGateway:
    """Minimum Sentinel trust gateway.

    The gateway establishes the execution boundary without implementing a policy
    engine, provider routing or Guardian cognition.
    """

    def __init__(self) -> None:
        self._decisions: list[SentinelResponse] = []

    def evaluate(self, request: SentinelRequest) -> SentinelResponse:
        """Evaluate a request at the Sentinel trust boundary."""

        if request.requires_approval:
            decision = SentinelDecision(
                outcome=SentinelDecisionOutcome.REVIEW,
                reason="Request requires human approval before execution.",
                requires_human_approval=True,
            )
            response = SentinelResponse(
                request=request,
                decision=decision,
                message="Sentinel routed the request for review.",
            )
        else:
            decision = SentinelDecision(
                outcome=SentinelDecisionOutcome.ALLOW,
                reason="Request accepted by Sentinel Core boundary.",
            )
            response = SentinelResponse(
                request=request,
                decision=decision,
                message="Sentinel allowed the request to proceed.",
            )

        self._decisions.append(response)
        return response

    def decisions(self) -> tuple[SentinelResponse, ...]:
        """Return immutable Sentinel decision history."""

        return tuple(self._decisions)
