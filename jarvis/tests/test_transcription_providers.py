from dataclasses import dataclass

import pytest

from sentinel.core import SentinelDecisionOutcome, SentinelRequest, SentinelTrustGateway
from sentinel.transcription_providers import (
    TranscriptionRequest,
    TranscriptionResponse,
    execute_transcription_with_sentinel_decision,
)


@dataclass(frozen=True)
class StubTranscriptionProvider:
    name: str = "stub-transcription-provider"

    def transcribe(self, request: TranscriptionRequest) -> TranscriptionResponse:
        return TranscriptionResponse(
            provider_name=self.name,
            text=f"transcript:{len(request.audio_bytes)}",
            metadata={"source": "stub"},
        )


def test_transcription_request_rejects_empty_audio_bytes() -> None:
    with pytest.raises(ValueError, match="Transcription request audio bytes must not be empty."):
        TranscriptionRequest(audio_bytes=b"", mime_type="audio/wav")


def test_transcription_request_rejects_empty_mime_type() -> None:
    with pytest.raises(ValueError, match="Transcription request mime type must not be empty."):
        TranscriptionRequest(audio_bytes=b"audio", mime_type=" ")


def test_transcription_response_rejects_empty_provider_name() -> None:
    with pytest.raises(ValueError, match="Transcription response provider name must not be empty."):
        TranscriptionResponse(provider_name=" ", text="hello")


def test_transcription_response_rejects_empty_text() -> None:
    with pytest.raises(ValueError, match="Transcription response text must not be empty."):
        TranscriptionResponse(provider_name="stub", text=" ")


def test_sentinel_allow_decision_executes_transcription_provider() -> None:
    gateway = SentinelTrustGateway()
    provider = StubTranscriptionProvider()
    sentinel_response = gateway.evaluate(
        SentinelRequest(source="Guardian", intent="speech.transcribe")
    )

    response = execute_transcription_with_sentinel_decision(
        sentinel_response,
        provider,
        TranscriptionRequest(audio_bytes=b"fake-audio", mime_type="audio/wav"),
    )

    assert sentinel_response.decision.outcome == SentinelDecisionOutcome.ALLOW
    assert response.provider_name == "stub-transcription-provider"
    assert response.text == "transcript:10"


def test_sentinel_review_decision_blocks_transcription_provider_execution() -> None:
    gateway = SentinelTrustGateway()
    provider = StubTranscriptionProvider()
    sentinel_response = gateway.evaluate(
        SentinelRequest(
            source="Guardian",
            intent="execute.high_risk_action",
            requires_approval=True,
        )
    )

    with pytest.raises(
        PermissionError, match="Sentinel decision does not allow speech transcription execution."
    ):
        execute_transcription_with_sentinel_decision(
            sentinel_response,
            provider,
            TranscriptionRequest(audio_bytes=b"fake-audio", mime_type="audio/wav"),
        )
