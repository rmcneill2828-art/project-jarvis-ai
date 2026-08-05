"""Specialist agent contract: `AgentRequest`, `AgentResult`, `SpecialistAgent`.

Implements the contract shape scoped at ESR-0048
(`aiems/models/MOD-0001_PLATFORM_ARCHITECTURE_MODEL.md`, "Agent Framework"
subsection) - a `SpecialistAgent` Protocol mirroring the existing
Protocol-based provider contracts (`sentinel/providers.py`'s
`ExecutionProvider`, `sentinel/speech_providers.py`'s
`SpeechSynthesisProvider`, `sentinel/transcription_providers.py`'s
`TranscriptionProvider`), not a new interface shape.

`AgentRequest`/`AgentResult` field validation mirrors
`sentinel.core.SentinelRequest`'s own `__post_init__` pattern exactly:
non-empty required strings, a `Mapping` field normalised to
`MappingProxyType` so callers cannot mutate it after construction.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Protocol


@dataclass(frozen=True)
class AgentRequest:
    """A task presented to a specialist agent."""

    task: str
    parameters: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.task.strip():
            msg = "Agent request task must not be empty."
            raise ValueError(msg)
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))


@dataclass(frozen=True)
class AgentResult:
    """A specialist agent's structured response to an `AgentRequest`.

    `status` is the agent's own success-status vocabulary - it is not a
    fixed contract value shared across all agents. `GiaObservabilityAgent`
    (`jarvis/agents/gia_agent.py`) reports `"reported"`; a future agent may
    define a different status string appropriate to its own capability
    (Engineering Reviewer design-review finding on EIP-ESR0049-001,
    folded in).
    """

    status: str
    payload: Mapping[str, str] = field(default_factory=dict)
    message: str | None = None

    def __post_init__(self) -> None:
        if not self.status.strip():
            msg = "Agent result status must not be empty."
            raise ValueError(msg)
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))


class SpecialistAgent(Protocol):
    """A bounded, named provider of one specific domain capability.

    Invoked only through `SentinelGatedAgentService`
    (`jarvis/interfaces/sentinel_agent.py`) - never directly by a caller,
    matching MOD-0001's mandatory-Sentinel-gate requirement. An agent is
    not itself user-facing; it performs or reports on a named task and
    returns a structured `AgentResult`, which alone Guardian may compose
    into any response to the household.
    """

    @property
    def name(self) -> str:
        """Return this agent's stable, registry-unique name."""
        ...

    def execute(self, request: AgentRequest) -> AgentResult:
        """Execute `request` and return a structured result.

        Propagates whatever the underlying capability raises on failure -
        never fabricates a value, per the project's no-mock-fallback rule.
        """
        ...
