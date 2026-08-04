"""Whisper (self-hosted local speech-to-text, via `faster-whisper`)
transcription provider adapter for Sentinel.

Self-hosted per EIP-ESR0047-001 Section 5.1: no API key, no account, no
recurring cost, consistent with the project's standing
no-discretionary-budget/self-hosted default already applied to
`sentinel/piper_provider.py`. `import faster_whisper` is deliberately
localised inside `_load_model()`, never at module top level, so any code
path that never constructs a real `WhisperProvider` - including every
fake-seam unit test - never pays that import cost, matching
`PiperProvider`'s established pattern.
"""

import io
from collections.abc import Callable

from sentinel.provider_config import ProviderConfiguration
from sentinel.transcription_providers import TranscriptionRequest, TranscriptionResponse

AudioTranscriber = Callable[[bytes], str]


def _load_model(model_size_or_path: str) -> AudioTranscriber:
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size_or_path, device="cpu", compute_type="int8")

    def transcribe(audio_bytes: bytes) -> str:
        segments, _info = model.transcribe(io.BytesIO(audio_bytes))
        return " ".join(segment.text.strip() for segment in segments).strip()

    return transcribe


class WhisperProvider:
    """Sentinel transcription provider backed by the local `faster-whisper` engine.

    `ProviderConfiguration.endpoint` carries the Whisper model size or local
    model path (for example `"base.en"`) - required for real construction,
    interpreted only by this adapter, matching `PiperProvider`'s existing
    `endpoint`-as-local-identifier pattern. The model is loaded once at
    construction rather than per request, the same eager-load judgement
    already made for Piper's voice model.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
        transcriber: AudioTranscriber | None = None,
    ) -> None:
        if not configuration.endpoint:
            msg = "Whisper provider configuration requires a model size or path (endpoint)."
            raise ValueError(msg)
        self._configuration = configuration
        if transcriber is not None:
            self._transcriber = transcriber
        else:
            try:
                self._transcriber = _load_model(configuration.endpoint)
            except Exception as exc:
                msg = (
                    "Whisper model could not be loaded from: "
                    f"{configuration.endpoint} ({type(exc).__name__})."
                )
                raise RuntimeError(msg) from exc

    @property
    def name(self) -> str:
        return self._configuration.provider_name

    def transcribe(self, request: TranscriptionRequest) -> TranscriptionResponse:
        try:
            text = self._transcriber(request.audio_bytes)
        except Exception as exc:
            msg = f"Whisper transcription failed: {type(exc).__name__}."
            raise RuntimeError(msg) from exc

        if not text:
            msg = "Unexpected Whisper response: empty transcription text."
            raise RuntimeError(msg)

        return TranscriptionResponse(
            provider_name=self.name,
            text=text,
            metadata={"model": self._configuration.endpoint},
        )
