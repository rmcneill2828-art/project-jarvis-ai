from dataclasses import dataclass

import pytest

from sentinel.core import SentinelDecisionOutcome, SentinelRequest, SentinelTrustGateway
from sentinel.speech_providers import (
    SpeechSynthesisRequest,
    SpeechSynthesisResponse,
    execute_speech_synthesis_with_sentinel_decision,
)


@dataclass(frozen=True)
class StubSpeechProvider:
    name: str = "stub-speech-provider"

    def synthesize(self, request: SpeechSynthesisRequest) -> SpeechSynthesisResponse:
        return SpeechSynthesisResponse(
            provider_name=self.name,
            audio_bytes=f"audio:{request.text}".encode(),
            mime_type="audio/mpeg",
            metadata={"source": "stub"},
        )


def test_speech_synthesis_request_rejects_empty_text() -> None:
    with pytest.raises(ValueError, match="Speech synthesis request text must not be empty."):
        SpeechSynthesisRequest(text=" ")


def test_speech_synthesis_response_rejects_empty_audio_bytes() -> None:
    with pytest.raises(ValueError, match="Speech synthesis response audio bytes must not be empty."):
        SpeechSynthesisResponse(provider_name="stub", audio_bytes=b"", mime_type="audio/mpeg")


def test_speech_synthesis_response_rejects_empty_provider_name() -> None:
    with pytest.raises(ValueError, match="Speech synthesis response provider name must not be empty."):
        SpeechSynthesisResponse(provider_name=" ", audio_bytes=b"audio", mime_type="audio/mpeg")


def test_speech_synthesis_response_rejects_empty_mime_type() -> None:
    with pytest.raises(ValueError, match="Speech synthesis response mime type must not be empty."):
        SpeechSynthesisResponse(provider_name="stub", audio_bytes=b"audio", mime_type=" ")


def test_sentinel_allow_decision_executes_speech_provider() -> None:
    gateway = SentinelTrustGateway()
    provider = StubSpeechProvider()
    sentinel_response = gateway.evaluate(
        SentinelRequest(source="Guardian", intent="speech.synthesize")
    )

    response = execute_speech_synthesis_with_sentinel_decision(
        sentinel_response,
        provider,
        SpeechSynthesisRequest(text="hello"),
    )

    assert sentinel_response.decision.outcome == SentinelDecisionOutcome.ALLOW
    assert response.provider_name == "stub-speech-provider"
    assert response.audio_bytes == b"audio:hello"


def test_sentinel_review_decision_blocks_speech_provider_execution() -> None:
    gateway = SentinelTrustGateway()
    provider = StubSpeechProvider()
    sentinel_response = gateway.evaluate(
        SentinelRequest(
            source="Guardian",
            intent="execute.high_risk_action",
            requires_approval=True,
        )
    )

    with pytest.raises(PermissionError, match="Sentinel decision does not allow speech synthesis execution."):
        execute_speech_synthesis_with_sentinel_decision(
            sentinel_response,
            provider,
            SpeechSynthesisRequest(text="open the pod bay doors"),
        )
