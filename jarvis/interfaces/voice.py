"""Voice interface that routes speech requests through Sentinel.

Voice Faculty Phase 6: Increment A (EIP-ESR0040-001) delivered speech output
only. Increment B (EIP-ESR0047-001) adds speech input (transcription) -
push-to-talk only, no wake word/continuous listening, no speaker
identification. No Vision - see each approved package for its own excluded
scope and GAM-0001 Section 8.1 reasoning.
"""

import logging
from dataclasses import dataclass
from typing import Protocol

from sentinel.core import SentinelDecisionOutcome, SentinelRequest, SentinelTrustGateway
from sentinel.speech_providers import (
    SpeechSynthesisProvider,
    SpeechSynthesisRequest,
    SpeechSynthesisResponse,
    execute_speech_synthesis_with_sentinel_decision,
)
from sentinel.transcription_providers import (
    TranscriptionProvider,
    TranscriptionRequest,
    execute_transcription_with_sentinel_decision,
)

logger = logging.getLogger(__name__)

STATUS_SYNTHESIZED = "synthesized"
STATUS_NOT_CONNECTED = "not_connected"
STATUS_NOT_RUNNING = "not_running"
STATUS_DENIED = "denied"
STATUS_UNAVAILABLE = "unavailable"
STATUS_TRANSCRIBED = "transcribed"

NOT_CONNECTED_MESSAGE = "Guardian has no speech synthesis provider connected."
NOT_RUNNING_MESSAGE = "Guardian runtime is not running."
DENIED_MESSAGE = "Sentinel did not allow this speech request to proceed."
UNAVAILABLE_MESSAGE = "JARVIS could not reach a speech provider right now. Please try again."
TRANSCRIPTION_NOT_CONNECTED_MESSAGE = "Guardian has no speech transcription provider connected."


@dataclass(frozen=True)
class SpeechOutcome:
    """Boundary-safe outcome for a Guardian speech-output request.

    A dedicated, named-status envelope rather than `None` or a raised
    exception (Engineering Reviewer design-review finding on
    EIP-ESR0040-001 v0.1, folded into v0.2) - every outcome, success or
    boundary failure, is a distinct, separately assertable `status` value.
    """

    status: str
    audio: SpeechSynthesisResponse | None = None
    message: str | None = None

    def __post_init__(self) -> None:
        if not self.status.strip():
            msg = "Speech outcome status must not be empty."
            raise ValueError(msg)
        if self.status == STATUS_SYNTHESIZED and self.audio is None:
            msg = "A synthesized speech outcome must include audio."
            raise ValueError(msg)
        if self.status != STATUS_SYNTHESIZED and self.audio is not None:
            msg = "A non-synthesized speech outcome must not include audio."
            raise ValueError(msg)


@dataclass(frozen=True)
class TranscriptionOutcome:
    """Boundary-safe outcome for a Guardian speech-input (transcription) request.

    Mirrors `SpeechOutcome`'s named-status envelope shape for the opposite
    data direction: every outcome, success or boundary failure, is a
    distinct, separately assertable `status` value rather than `None` or a
    raised exception.
    """

    status: str
    text: str | None = None
    message: str | None = None

    def __post_init__(self) -> None:
        if not self.status.strip():
            msg = "Transcription outcome status must not be empty."
            raise ValueError(msg)
        if self.status == STATUS_TRANSCRIBED and not self.text:
            msg = "A transcribed outcome must include text."
            raise ValueError(msg)
        if self.status != STATUS_TRANSCRIBED and self.text is not None:
            msg = "A non-transcribed outcome must not include text."
            raise ValueError(msg)


class GuardianSpeechProvider(Protocol):
    """Provider interface Guardian's runtime speaks through."""

    def synthesize(self, text: str) -> SpeechOutcome:
        """Synthesize `text` into a `SpeechOutcome`."""


class GuardianTranscriptionProvider(Protocol):
    """Provider interface Guardian's runtime transcribes speech input through."""

    def transcribe(self, audio_bytes: bytes, mime_type: str) -> TranscriptionOutcome:
        """Transcribe `audio_bytes` into a `TranscriptionOutcome`."""


class SentinelGatedSpeechProvider:
    """Speech-synthesis provider that routes requests through Sentinel for
    trust evaluation before executing the connected synthesis provider."""

    name = "sentinel-gated-speech"

    def __init__(
        self,
        gateway: SentinelTrustGateway,
        provider: SpeechSynthesisProvider,
        source: str = "jarvis.guardian.voice",
    ) -> None:
        self._gateway = gateway
        self._provider = provider
        self._source = source

    @property
    def gateway(self) -> SentinelTrustGateway:
        """Return the connected Sentinel trust gateway, for test/diagnostic introspection."""

        return self._gateway

    def synthesize(self, text: str) -> SpeechOutcome:
        """Synthesize `text` into speech by routing the request through Sentinel."""

        sentinel_request = SentinelRequest(
            source=self._source,
            intent="speech.synthesize",
            metadata={"capability": "speech-synthesis"},
        )
        sentinel_response = self._gateway.evaluate(sentinel_request)

        if sentinel_response.decision.outcome is not SentinelDecisionOutcome.ALLOW:
            # decision.reason is not surfaced here, matching
            # SentinelGatedConversationProvider's established pattern - the
            # full reason is already captured in Sentinel's audit trail.
            return SpeechOutcome(status=STATUS_DENIED, message=DENIED_MESSAGE)

        try:
            audio = execute_speech_synthesis_with_sentinel_decision(
                sentinel_response,
                self._provider,
                SpeechSynthesisRequest(text=text),
            )
        except RuntimeError as exc:
            logger.warning("Speech provider execution failed: %s", type(exc).__name__)
            return SpeechOutcome(status=STATUS_UNAVAILABLE, message=UNAVAILABLE_MESSAGE)

        return SpeechOutcome(status=STATUS_SYNTHESIZED, audio=audio)


class SentinelGatedTranscriptionProvider:
    """Speech-transcription provider that routes requests through Sentinel for
    trust evaluation before executing the connected transcription provider."""

    name = "sentinel-gated-transcription"

    def __init__(
        self,
        gateway: SentinelTrustGateway,
        provider: TranscriptionProvider,
        source: str = "jarvis.guardian.voice",
    ) -> None:
        self._gateway = gateway
        self._provider = provider
        self._source = source

    @property
    def gateway(self) -> SentinelTrustGateway:
        """Return the connected Sentinel trust gateway, for test/diagnostic introspection."""

        return self._gateway

    def transcribe(self, audio_bytes: bytes, mime_type: str) -> TranscriptionOutcome:
        """Transcribe `audio_bytes` into text by routing the request through Sentinel.

        Per EIP-ESR0047-001 Section 5.2, capability enablement (whether this
        provider was constructed at all) is this feature's approval gate -
        this per-request Sentinel call classifies as routine, audited
        interaction, not a live approval decision.
        """

        sentinel_request = SentinelRequest(
            source=self._source,
            intent="speech.transcribe",
            metadata={"capability": "speech-transcription"},
        )
        sentinel_response = self._gateway.evaluate(sentinel_request)

        if sentinel_response.decision.outcome is not SentinelDecisionOutcome.ALLOW:
            # decision.reason is not surfaced here, matching
            # SentinelGatedSpeechProvider's established pattern - the full
            # reason is already captured in Sentinel's audit trail.
            return TranscriptionOutcome(status=STATUS_DENIED, message=DENIED_MESSAGE)

        try:
            response = execute_transcription_with_sentinel_decision(
                sentinel_response,
                self._provider,
                TranscriptionRequest(audio_bytes=audio_bytes, mime_type=mime_type),
            )
        except RuntimeError as exc:
            logger.warning("Transcription provider execution failed: %s", type(exc).__name__)
            return TranscriptionOutcome(status=STATUS_UNAVAILABLE, message=UNAVAILABLE_MESSAGE)

        return TranscriptionOutcome(status=STATUS_TRANSCRIBED, text=response.text)
