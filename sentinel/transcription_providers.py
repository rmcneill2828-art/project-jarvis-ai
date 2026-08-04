"""Sentinel speech-transcription provider abstraction (Voice Faculty Phase 6,
Increment B - EIP-ESR0047-001).

Deliberately parallel to, and independent from, `sentinel/speech_providers.py`'s
`SpeechSynthesisRequest`/`SpeechSynthesisResponse` contracts, for the opposite
data direction: a transcription request carries audio bytes in and text out,
where a synthesis request carries text in and audio bytes out. Kept as a
distinct module rather than a single bidirectional contract, matching the
blast-radius-minimisation judgement already applied when
`speech_providers.py` was kept separate from `sentinel/providers.py`'s
text-generation contracts (EIP-ESR0039-001 Section 8 item 2).
"""

from dataclasses import dataclass, field
from typing import Protocol

from sentinel.core import SentinelDecisionOutcome, SentinelResponse


@dataclass(frozen=True)
class TranscriptionRequest:
    """Provider-neutral transcription request submitted after Sentinel approval."""

    audio_bytes: bytes
    mime_type: str
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.audio_bytes:
            msg = "Transcription request audio bytes must not be empty."
            raise ValueError(msg)
        if not self.mime_type.strip():
            msg = "Transcription request mime type must not be empty."
            raise ValueError(msg)


@dataclass(frozen=True)
class TranscriptionResponse:
    """Provider-neutral transcription response returned by an execution provider."""

    provider_name: str
    text: str
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.provider_name.strip():
            msg = "Transcription response provider name must not be empty."
            raise ValueError(msg)
        if not self.text.strip():
            msg = "Transcription response text must not be empty."
            raise ValueError(msg)


class TranscriptionProvider(Protocol):
    """Protocol implemented by Sentinel speech-transcription providers."""

    @property
    def name(self) -> str:
        """Return provider name."""

    def transcribe(self, request: TranscriptionRequest) -> TranscriptionResponse:
        """Transcribe a speech-transcription request."""


def execute_transcription_with_sentinel_decision(
    sentinel_response: SentinelResponse,
    provider: TranscriptionProvider,
    request: TranscriptionRequest,
) -> TranscriptionResponse:
    """Execute a transcription request only when Sentinel allowed execution."""

    if sentinel_response.decision.outcome is not SentinelDecisionOutcome.ALLOW:
        msg = "Sentinel decision does not allow speech transcription execution."
        raise PermissionError(msg)
    return provider.transcribe(request)
