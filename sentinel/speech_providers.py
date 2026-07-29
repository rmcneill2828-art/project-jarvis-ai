"""Sentinel speech-synthesis provider abstraction (Voice Faculty Phase 6,
Increment A - EIP-ESR0040-001).

Deliberately parallel to, and independent from, `sentinel/providers.py`'s
text-generation `ExecutionProvider`/`ProviderRequest`/`ProviderResponse`
contracts, rather than an extension of them: `ProviderResponse.content` is a
validated non-empty `str`, and every existing provider adapter, Sentinel
policy check and audit-trail code path assumes text content. Forcing
synthesised audio through that field would either violate the field's
existing contract or require changing a dataclass shared by every working
text-generation adapter - the same blast-radius-minimisation judgement
already made once for this reason in EIP-ESR0039-001 Section 8 item 2.
"""

from dataclasses import dataclass, field
from typing import Protocol

from sentinel.core import SentinelDecisionOutcome, SentinelResponse


@dataclass(frozen=True)
class SpeechSynthesisRequest:
    """Provider-neutral speech-synthesis request submitted after Sentinel approval."""

    text: str
    voice_id: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.text.strip():
            msg = "Speech synthesis request text must not be empty."
            raise ValueError(msg)


@dataclass(frozen=True)
class SpeechSynthesisResponse:
    """Provider-neutral speech-synthesis response returned by an execution provider."""

    provider_name: str
    audio_bytes: bytes
    mime_type: str
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.provider_name.strip():
            msg = "Speech synthesis response provider name must not be empty."
            raise ValueError(msg)
        if not self.audio_bytes:
            msg = "Speech synthesis response audio bytes must not be empty."
            raise ValueError(msg)
        if not self.mime_type.strip():
            msg = "Speech synthesis response mime type must not be empty."
            raise ValueError(msg)


class SpeechSynthesisProvider(Protocol):
    """Protocol implemented by Sentinel speech-synthesis providers."""

    @property
    def name(self) -> str:
        """Return provider name."""

    def synthesize(self, request: SpeechSynthesisRequest) -> SpeechSynthesisResponse:
        """Synthesize a speech request."""


def execute_speech_synthesis_with_sentinel_decision(
    sentinel_response: SentinelResponse,
    provider: SpeechSynthesisProvider,
    request: SpeechSynthesisRequest,
) -> SpeechSynthesisResponse:
    """Execute a speech synthesis request only when Sentinel allowed execution."""

    if sentinel_response.decision.outcome is not SentinelDecisionOutcome.ALLOW:
        msg = "Sentinel decision does not allow speech synthesis execution."
        raise PermissionError(msg)
    return provider.synthesize(request)
