"""Tests for the Piper (self-hosted local TTS) speech-synthesis provider
adapter. Uses the injectable `synthesizer` seam throughout - never imports
`piper` or loads a real voice model, matching `OpenAIProvider`'s test-double
pattern and the Engineering Reviewer's import-isolation requirement."""

import pytest

from sentinel.piper_provider import MIME_TYPE, PiperProvider
from sentinel.provider_config import ProviderConfiguration
from sentinel.speech_providers import SpeechSynthesisRequest


def _configuration(**overrides) -> ProviderConfiguration:
    defaults = {
        "provider_name": "piper",
        "endpoint": r"C:\fake\voices\en_US-lessac-medium.onnx",
    }
    defaults.update(overrides)
    return ProviderConfiguration(**defaults)


def test_requires_endpoint_model_path():
    with pytest.raises(ValueError, match="requires a local voice model path"):
        PiperProvider(ProviderConfiguration(provider_name="piper"), synthesizer=lambda text: b"audio")


def test_wraps_synthesizer_load_failure(monkeypatch):
    def failing_load(model_path: str):
        raise FileNotFoundError(model_path)

    monkeypatch.setattr("sentinel.piper_provider._load_synthesizer", failing_load)

    with pytest.raises(RuntimeError, match="could not be loaded"):
        PiperProvider(_configuration())


def test_synthesize_returns_audio_on_success():
    captured: dict[str, object] = {}

    def fake_synthesizer(text: str) -> bytes:
        captured["text"] = text
        return b"fake-wav-bytes"

    provider = PiperProvider(_configuration(), synthesizer=fake_synthesizer)
    response = provider.synthesize(SpeechSynthesisRequest(text="hello"))

    assert response.audio_bytes == b"fake-wav-bytes"
    assert response.provider_name == "piper"
    assert response.mime_type == MIME_TYPE
    assert response.metadata["model_path"] == _configuration().endpoint
    assert captured["text"] == "hello"


def test_synthesize_wraps_synthesizer_error_without_leaking_message():
    def failing_synthesizer(text: str) -> bytes:
        raise RuntimeError("internal onnxruntime detail that should not leak")

    provider = PiperProvider(_configuration(), synthesizer=failing_synthesizer)

    with pytest.raises(RuntimeError) as excinfo:
        provider.synthesize(SpeechSynthesisRequest(text="hello"))

    assert "internal onnxruntime detail" not in str(excinfo.value)
    assert "RuntimeError" in str(excinfo.value)


def test_synthesize_raises_on_empty_audio_body():
    provider = PiperProvider(_configuration(), synthesizer=lambda text: b"")

    with pytest.raises(RuntimeError, match="empty audio body"):
        provider.synthesize(SpeechSynthesisRequest(text="hello"))


def test_name_reflects_configuration():
    provider = PiperProvider(_configuration(), synthesizer=lambda text: b"audio")

    assert provider.name == "piper"
