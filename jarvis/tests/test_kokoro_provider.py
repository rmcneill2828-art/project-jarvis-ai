"""Tests for the Kokoro (self-hosted local TTS) speech-synthesis provider
adapter. Uses the injectable `synthesizer` seam throughout - never imports
`kokoro_onnx` or loads a real voice model, matching `PiperProvider`'s
test-double pattern and the Engineering Reviewer's import-isolation
requirement."""

import pytest

from sentinel.kokoro_provider import MIME_TYPE, KokoroProvider
from sentinel.provider_config import ProviderConfiguration
from sentinel.speech_providers import SpeechSynthesisRequest


def _configuration(**overrides) -> ProviderConfiguration:
    defaults = {
        "provider_name": "kokoro",
        "endpoint": r"C:\fake\voices\kokoro-v1.0.onnx",
        "metadata": {"voices_path": r"C:\fake\voices\voices-v1.0.bin"},
    }
    defaults.update(overrides)
    return ProviderConfiguration(**defaults)


def test_requires_endpoint_model_path():
    with pytest.raises(ValueError, match="requires a local voice model path"):
        KokoroProvider(
            ProviderConfiguration(
                provider_name="kokoro", metadata={"voices_path": r"C:\fake\voices.bin"}
            ),
            synthesizer=lambda text: b"audio",
        )


def test_requires_voices_path_metadata():
    with pytest.raises(ValueError, match="requires a local voices file path"):
        KokoroProvider(
            ProviderConfiguration(provider_name="kokoro", endpoint=r"C:\fake\model.onnx"),
            synthesizer=lambda text: b"audio",
        )


def test_wraps_synthesizer_load_failure(monkeypatch):
    def failing_load(model_path: str, voices_path: str, voice: str, lang: str):
        raise FileNotFoundError(model_path)

    monkeypatch.setattr("sentinel.kokoro_provider._load_synthesizer", failing_load)

    with pytest.raises(RuntimeError, match="could not be loaded"):
        KokoroProvider(_configuration())


def test_synthesize_returns_audio_on_success():
    captured: dict[str, object] = {}

    def fake_synthesizer(text: str) -> bytes:
        captured["text"] = text
        return b"fake-wav-bytes"

    provider = KokoroProvider(_configuration(), synthesizer=fake_synthesizer)
    response = provider.synthesize(SpeechSynthesisRequest(text="hello"))

    assert response.audio_bytes == b"fake-wav-bytes"
    assert response.provider_name == "kokoro"
    assert response.mime_type == MIME_TYPE
    assert response.metadata["model_path"] == _configuration().endpoint
    assert captured["text"] == "hello"


def test_synthesize_wraps_synthesizer_error_without_leaking_message():
    def failing_synthesizer(text: str) -> bytes:
        raise RuntimeError("internal onnxruntime detail that should not leak")

    provider = KokoroProvider(_configuration(), synthesizer=failing_synthesizer)

    with pytest.raises(RuntimeError) as excinfo:
        provider.synthesize(SpeechSynthesisRequest(text="hello"))

    assert "internal onnxruntime detail" not in str(excinfo.value)
    assert "RuntimeError" in str(excinfo.value)


def test_synthesize_raises_on_empty_audio_body():
    provider = KokoroProvider(_configuration(), synthesizer=lambda text: b"")

    with pytest.raises(RuntimeError, match="empty audio body"):
        provider.synthesize(SpeechSynthesisRequest(text="hello"))


def test_name_reflects_configuration():
    provider = KokoroProvider(_configuration(), synthesizer=lambda text: b"audio")

    assert provider.name == "kokoro"
