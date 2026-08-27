"""Tests for the Kokoro (self-hosted local TTS) speech-synthesis provider
adapter. Uses the injectable `synthesizer` seam throughout - never imports
`kokoro_onnx` or loads a real voice model, matching `PiperProvider`'s
test-double pattern and the Engineering Reviewer's import-isolation
requirement.

The `synthesizer` seam is `(text, voice) -> bytes` (EIP-ESR0053-002), not the
single-voice `(text) -> bytes` shape used before dual-voice fallback support -
a disclosed, intentional breaking change to this module's own test contract."""

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
            synthesizer=lambda text, voice: b"audio",
        )


def test_requires_voices_path_metadata():
    with pytest.raises(ValueError, match="requires a local voices file path"):
        KokoroProvider(
            ProviderConfiguration(provider_name="kokoro", endpoint=r"C:\fake\model.onnx"),
            synthesizer=lambda text, voice: b"audio",
        )


def test_wraps_synthesizer_load_failure(monkeypatch):
    def failing_load(model_path: str, voices_path: str, lang: str):
        raise FileNotFoundError(model_path)

    monkeypatch.setattr("sentinel.kokoro_provider._load_synthesizer", failing_load)

    with pytest.raises(RuntimeError, match="could not be loaded"):
        KokoroProvider(_configuration())


def test_synthesize_returns_audio_on_success():
    captured: dict[str, object] = {}

    def fake_synthesizer(text: str, voice: str) -> bytes:
        captured["text"] = text
        captured["voice"] = voice
        return b"fake-wav-bytes"

    provider = KokoroProvider(_configuration(metadata={"voices_path": r"C:\fake\voices.bin", "voice": "bm_george"}), synthesizer=fake_synthesizer)
    response = provider.synthesize(SpeechSynthesisRequest(text="hello"))

    assert response.audio_bytes == b"fake-wav-bytes"
    assert response.provider_name == "kokoro"
    assert response.mime_type == MIME_TYPE
    assert response.metadata["model_path"] == _configuration().endpoint
    assert response.metadata["voice_used"] == "bm_george"
    assert captured["text"] == "hello"
    assert captured["voice"] == "bm_george"


def test_synthesize_wraps_synthesizer_error_without_leaking_message():
    def failing_synthesizer(text: str, voice: str) -> bytes:
        raise RuntimeError("internal onnxruntime detail that should not leak")

    provider = KokoroProvider(_configuration(), synthesizer=failing_synthesizer)

    with pytest.raises(RuntimeError) as excinfo:
        provider.synthesize(SpeechSynthesisRequest(text="hello"))

    assert "internal onnxruntime detail" not in str(excinfo.value)
    assert "RuntimeError" in str(excinfo.value)


def test_synthesize_raises_on_empty_audio_body():
    provider = KokoroProvider(_configuration(), synthesizer=lambda text, voice: b"")

    with pytest.raises(RuntimeError, match="empty audio body"):
        provider.synthesize(SpeechSynthesisRequest(text="hello"))


def test_name_reflects_configuration():
    provider = KokoroProvider(_configuration(), synthesizer=lambda text, voice: b"audio")

    assert provider.name == "kokoro"


def test_synthesize_never_calls_fallback_when_primary_succeeds():
    """EIP-ESR0053-002: a healthy primary voice must not pay the cost of, or
    risk, a fallback call it never needed."""

    calls: list[str] = []

    def synthesizer(text: str, voice: str) -> bytes:
        calls.append(voice)
        return b"primary-audio"

    provider = KokoroProvider(
        _configuration(metadata={"voices_path": r"C:\fake\voices.bin", "voice": "bm_george", "fallback_voice": "bf_isabella"}),
        synthesizer=synthesizer,
    )
    response = provider.synthesize(SpeechSynthesisRequest(text="hello"))

    assert calls == ["bm_george"]
    assert response.audio_bytes == b"primary-audio"
    assert response.metadata["voice_used"] == "bm_george"


def test_synthesize_falls_back_to_second_voice_on_primary_failure():
    """EIP-ESR0053-002 (Programme Sponsor decision): bm_george primary,
    bf_isabella automatic fallback if primary synthesis fails at runtime."""

    def synthesizer(text: str, voice: str) -> bytes:
        if voice == "bm_george":
            raise RuntimeError("primary voice synthesis failed")
        return b"fallback-audio"

    provider = KokoroProvider(
        _configuration(metadata={"voices_path": r"C:\fake\voices.bin", "voice": "bm_george", "fallback_voice": "bf_isabella"}),
        synthesizer=synthesizer,
    )
    response = provider.synthesize(SpeechSynthesisRequest(text="hello"))

    assert response.audio_bytes == b"fallback-audio"
    assert response.metadata["voice_used"] == "bf_isabella"


def test_synthesize_raises_without_fallback_configured_matching_prior_behaviour():
    """No fallback_voice metadata means synthesize() must still raise on a
    primary-voice failure exactly as it always has - no behaviour change for
    a caller that never opts into fallback."""

    def failing_synthesizer(text: str, voice: str) -> bytes:
        raise RuntimeError("primary voice synthesis failed")

    provider = KokoroProvider(_configuration(), synthesizer=failing_synthesizer)

    with pytest.raises(RuntimeError, match="Kokoro synthesis failed"):
        provider.synthesize(SpeechSynthesisRequest(text="hello"))


def test_synthesize_raises_when_both_primary_and_fallback_fail():
    def always_failing_synthesizer(text: str, voice: str) -> bytes:
        raise RuntimeError(f"{voice} synthesis failed, internal detail")

    provider = KokoroProvider(
        _configuration(metadata={"voices_path": r"C:\fake\voices.bin", "voice": "bm_george", "fallback_voice": "bf_isabella"}),
        synthesizer=always_failing_synthesizer,
    )

    with pytest.raises(RuntimeError) as excinfo:
        provider.synthesize(SpeechSynthesisRequest(text="hello"))

    assert "primary and fallback voice" in str(excinfo.value)
    assert "internal detail" not in str(excinfo.value)
