"""Tests for the Whisper (self-hosted local STT, via `faster-whisper`)
transcription provider adapter. Uses the injectable `transcriber` seam
throughout - never imports `faster_whisper` or loads a real model, matching
`PiperProvider`'s test-double pattern."""

import pytest

from sentinel.provider_config import ProviderConfiguration
from sentinel.transcription_providers import TranscriptionRequest
from sentinel.whisper_provider import WhisperProvider


def _configuration(**overrides) -> ProviderConfiguration:
    defaults = {
        "provider_name": "whisper",
        "endpoint": "base.en",
    }
    defaults.update(overrides)
    return ProviderConfiguration(**defaults)


def test_requires_endpoint_model_path():
    with pytest.raises(ValueError, match="requires a model size or path"):
        WhisperProvider(ProviderConfiguration(provider_name="whisper"), transcriber=lambda audio: "text")


def test_wraps_transcriber_load_failure(monkeypatch):
    def failing_load(model_size_or_path: str):
        raise FileNotFoundError(model_size_or_path)

    monkeypatch.setattr("sentinel.whisper_provider._load_model", failing_load)

    with pytest.raises(RuntimeError, match="could not be loaded"):
        WhisperProvider(_configuration())


def test_transcribe_returns_text_on_success():
    captured: dict[str, object] = {}

    def fake_transcriber(audio_bytes: bytes) -> str:
        captured["audio_bytes"] = audio_bytes
        return "hello world"

    provider = WhisperProvider(_configuration(), transcriber=fake_transcriber)
    response = provider.transcribe(TranscriptionRequest(audio_bytes=b"fake-audio", mime_type="audio/webm"))

    assert response.text == "hello world"
    assert response.provider_name == "whisper"
    assert response.metadata["model"] == _configuration().endpoint
    assert captured["audio_bytes"] == b"fake-audio"


def test_transcribe_wraps_transcriber_error_without_leaking_message():
    def failing_transcriber(audio_bytes: bytes) -> str:
        raise RuntimeError("internal ctranslate2 detail that should not leak")

    provider = WhisperProvider(_configuration(), transcriber=failing_transcriber)

    with pytest.raises(RuntimeError) as excinfo:
        provider.transcribe(TranscriptionRequest(audio_bytes=b"fake-audio", mime_type="audio/webm"))

    assert "internal ctranslate2 detail" not in str(excinfo.value)
    assert "RuntimeError" in str(excinfo.value)


def test_transcribe_raises_on_empty_text():
    provider = WhisperProvider(_configuration(), transcriber=lambda audio: "")

    with pytest.raises(RuntimeError, match="empty transcription text"):
        provider.transcribe(TranscriptionRequest(audio_bytes=b"fake-audio", mime_type="audio/webm"))


def test_name_reflects_configuration():
    provider = WhisperProvider(_configuration(), transcriber=lambda audio: "text")

    assert provider.name == "whisper"
