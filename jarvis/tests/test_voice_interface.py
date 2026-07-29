"""Tests for the Sentinel-gated speech-output interface (Voice Faculty Phase
6, Increment A - EIP-ESR0040-001)."""

import pytest

from jarvis.interfaces.voice import (
    STATUS_DENIED,
    STATUS_SYNTHESIZED,
    STATUS_UNAVAILABLE,
    SentinelGatedSpeechProvider,
    SpeechOutcome,
)
from sentinel.core import SentinelDecisionOutcome, SentinelRequest, SentinelTrustGateway
from sentinel.policy import PolicyDecision, TrustCategory
from sentinel.speech_providers import SpeechSynthesisRequest, SpeechSynthesisResponse


class _StubSpeechProvider:
    name = "stub-speech-provider"

    def __init__(self, response: SpeechSynthesisResponse | None = None, error: Exception | None = None) -> None:
        self._response = response
        self._error = error
        self.received: list[SpeechSynthesisRequest] = []

    def synthesize(self, request: SpeechSynthesisRequest) -> SpeechSynthesisResponse:
        self.received.append(request)
        if self._error is not None:
            raise self._error
        assert self._response is not None
        return self._response


class _DenyAllPolicy:
    def evaluate(self, request: SentinelRequest) -> PolicyDecision:
        return PolicyDecision(
            outcome=SentinelDecisionOutcome.DENY,
            reason="Denied for test.",
            category=TrustCategory.UNSUPPORTED_HIGH_RISK,
        )


def test_speech_outcome_rejects_empty_status() -> None:
    with pytest.raises(ValueError, match="Speech outcome status must not be empty."):
        SpeechOutcome(status=" ")


def test_speech_outcome_requires_audio_when_synthesized() -> None:
    with pytest.raises(ValueError, match="A synthesized speech outcome must include audio."):
        SpeechOutcome(status=STATUS_SYNTHESIZED)


def test_speech_outcome_rejects_audio_when_not_synthesized() -> None:
    audio = SpeechSynthesisResponse(provider_name="stub", audio_bytes=b"audio", mime_type="audio/mpeg")
    with pytest.raises(ValueError, match="A non-synthesized speech outcome must not include audio."):
        SpeechOutcome(status=STATUS_UNAVAILABLE, audio=audio)


def test_sentinel_gated_speech_provider_returns_audio_on_allow() -> None:
    gateway = SentinelTrustGateway()
    audio = SpeechSynthesisResponse(provider_name="stub", audio_bytes=b"audio-bytes", mime_type="audio/mpeg")
    provider = _StubSpeechProvider(response=audio)
    gated = SentinelGatedSpeechProvider(gateway, provider)

    outcome = gated.synthesize("Guardian's response text.")

    assert outcome.status == STATUS_SYNTHESIZED
    assert outcome.audio is audio
    assert provider.received[0].text == "Guardian's response text."


def test_sentinel_gated_speech_provider_returns_denied_on_deny() -> None:
    gateway = SentinelTrustGateway(policy_engine=_DenyAllPolicy())
    provider = _StubSpeechProvider(response=SpeechSynthesisResponse(
        provider_name="stub", audio_bytes=b"audio", mime_type="audio/mpeg"
    ))
    gated = SentinelGatedSpeechProvider(gateway, provider)

    outcome = gated.synthesize("some text")

    assert outcome.status == STATUS_DENIED
    assert outcome.audio is None
    assert provider.received == []


def test_sentinel_gated_speech_provider_returns_unavailable_on_provider_failure() -> None:
    gateway = SentinelTrustGateway()
    provider = _StubSpeechProvider(error=RuntimeError("ElevenLabs request failed: HTTPError."))
    gated = SentinelGatedSpeechProvider(gateway, provider)

    outcome = gated.synthesize("some text")

    assert outcome.status == STATUS_UNAVAILABLE
    assert outcome.audio is None
