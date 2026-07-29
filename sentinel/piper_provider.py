"""Piper (self-hosted local neural TTS) speech-synthesis provider adapter for
Sentinel.

Self-hosted per the Programme Sponsor's revision of EIP-ESR0040-001 v1.0
(originally ElevenLabs, a cloud HTTP API) to v1.1/v1.2: no API key, no
account, no recurring cost, consistent with the project's standing
no-discretionary-budget/self-hosted default. `import piper` (and its
`onnxruntime` dependency) is deliberately localised inside
`_load_synthesizer()`, never at module top level, so any code path that
never constructs a real `PiperProvider` - including every fake-seam unit
test - never pays that import cost (Engineering Reviewer finding).
"""

import io
import wave
from collections.abc import Callable

from sentinel.provider_config import ProviderConfiguration
from sentinel.speech_providers import SpeechSynthesisRequest, SpeechSynthesisResponse

VoiceSynthesizer = Callable[[str], bytes]

MIME_TYPE = "audio/wav"


def _load_synthesizer(model_path: str) -> VoiceSynthesizer:
    from piper import PiperVoice

    voice = PiperVoice.load(model_path)

    def synthesize(text: str) -> bytes:
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            voice.synthesize_wav(text, wav_file)
        return buffer.getvalue()

    return synthesize


class PiperProvider:
    """Sentinel speech-synthesis provider backed by the local Piper TTS engine.

    `ProviderConfiguration.endpoint` carries the local filesystem path to a
    Piper voice model (`.onnx`, with its companion `.onnx.json` config
    alongside it) - required for real construction, and interpreted only by
    this adapter as a local path, not a URL. The voice model is loaded once
    at construction (~3.5s measured) rather than per request (~0.25s
    measured once loaded): unlike a cloud credential, a local model path has
    no per-request freshness concern, making eager loading the right choice.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
        synthesizer: VoiceSynthesizer | None = None,
    ) -> None:
        if not configuration.endpoint:
            msg = "Piper provider configuration requires a local voice model path (endpoint)."
            raise ValueError(msg)
        self._configuration = configuration
        if synthesizer is not None:
            self._synthesizer = synthesizer
        else:
            try:
                self._synthesizer = _load_synthesizer(configuration.endpoint)
            except Exception as exc:
                msg = (
                    "Piper voice model could not be loaded from path: "
                    f"{configuration.endpoint} ({type(exc).__name__})."
                )
                raise RuntimeError(msg) from exc

    @property
    def name(self) -> str:
        return self._configuration.provider_name

    def synthesize(self, request: SpeechSynthesisRequest) -> SpeechSynthesisResponse:
        try:
            audio_bytes = self._synthesizer(request.text)
        except Exception as exc:
            msg = f"Piper synthesis failed: {type(exc).__name__}."
            raise RuntimeError(msg) from exc

        if not audio_bytes:
            msg = "Unexpected Piper response: empty audio body."
            raise RuntimeError(msg)

        return SpeechSynthesisResponse(
            provider_name=self.name,
            audio_bytes=audio_bytes,
            mime_type=MIME_TYPE,
            metadata={"model_path": self._configuration.endpoint},
        )
