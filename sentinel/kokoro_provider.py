"""Kokoro (self-hosted local neural TTS) speech-synthesis provider adapter for
Sentinel.

Adapter-only, per EBG-0115/EIP-ESR0052-002: constructible and testable
directly, but deliberately **not** registered in `sentinel/provider_config.py`'s
production provider-selection wiring and not reachable from any RPC or UXP
path. Whether Kokoro replaces or sits alongside Piper is a decision deferred
entirely to the Programme Sponsor's own live listening comparison - this
module makes no such decision.

Mirrors `sentinel/piper_provider.py`'s exact contract shape (constructor
validation, `name` property, lazy import-inside-function, injectable
synthesizer seam, `SpeechSynthesisResponse` construction and error handling) -
spelled out explicitly per the Engineering Reviewer's design-review
correction (EIP-ESR0052-002 v0.2), rather than left as an unverifiable
"mirrors Piper" claim. `import kokoro_onnx` is deliberately localised inside
`_load_synthesizer()`, never at module top level, so any code path that never
constructs a real `KokoroProvider` - including every fake-seam unit test -
never pays that import cost, matching the Engineering Reviewer finding
`piper_provider.py` was already built to satisfy.

One disclosed, justified deviation from Piper's shape: Kokoro requires two
local files (an `.onnx` model and a companion `voices` `.bin` file), not one.
`ProviderConfiguration.endpoint` continues to carry the model path exactly
like Piper; the voices file path is required via `configuration.metadata`
("voices_path"), the field `ProviderConfiguration` already provides for
provider-specific extension. Voice name and language are optional metadata
keys with sensible defaults - no new dependency added to `ProviderConfiguration`
itself.
"""

import io
import wave
from collections.abc import Callable

from sentinel.provider_config import ProviderConfiguration
from sentinel.speech_providers import SpeechSynthesisRequest, SpeechSynthesisResponse

VoiceSynthesizer = Callable[[str], bytes]

MIME_TYPE = "audio/wav"
DEFAULT_VOICE = "af_sarah"
DEFAULT_LANG = "en-us"
_SAMPLE_WIDTH_BYTES = 2  # 16-bit PCM


def _load_synthesizer(model_path: str, voices_path: str, voice: str, lang: str) -> VoiceSynthesizer:
    import espeakng_loader
    from kokoro_onnx import Kokoro
    from kokoro_onnx.config import EspeakConfig

    # kokoro_onnx phonemizes text via espeak-ng, but does not bundle or locate
    # it itself - without this, construction succeeds but synthesis fails the
    # first time phonemizer looks for a system espeak-ng install that does not
    # exist on a self-hosted-first machine. espeakng_loader ships the actual
    # espeak-ng binary/data (pulled in as part of the voice-eval dependency
    # group), so this is the one piece of wiring required to make the
    # dependency addition actually functional, not merely importable.
    espeakng_loader.make_library_available()
    espeak_config = EspeakConfig(
        lib_path=espeakng_loader.get_library_path(),
        data_path=espeakng_loader.get_data_path(),
    )
    engine = Kokoro(model_path, voices_path, espeak_config=espeak_config)

    def synthesize(text: str) -> bytes:
        samples, sample_rate = engine.create(text, voice=voice, speed=1.0, lang=lang)
        # kokoro_onnx returns float32 samples in [-1.0, 1.0] (no built-in WAV
        # encoder) - converted to 16-bit PCM and wrapped the same way Piper's
        # own `_load_synthesizer` wraps its already-integer PCM output, so
        # both adapters hand Sentinel an identical audio/wav container shape.
        import numpy as np

        pcm = np.clip(samples, -1.0, 1.0)
        pcm_int16 = (pcm * 32767.0).astype("<i2")

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(_SAMPLE_WIDTH_BYTES)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(pcm_int16.tobytes())
        return buffer.getvalue()

    return synthesize


class KokoroProvider:
    """Sentinel speech-synthesis provider backed by the local Kokoro TTS engine.

    `ProviderConfiguration.endpoint` carries the local filesystem path to a
    Kokoro `.onnx` model file, interpreted only by this adapter as a local
    path, not a URL - required for real construction, matching
    `PiperProvider`'s own `endpoint` contract exactly. `configuration.metadata`
    must additionally carry `voices_path` (the companion `voices` `.bin` file
    Kokoro also requires) - the one Kokoro-specific deviation from Piper's
    single-file shape, disclosed here rather than silently added. Optional
    metadata keys `voice` and `lang` default to `af_sarah`/`en-us`.
    """

    def __init__(
        self,
        configuration: ProviderConfiguration,
        synthesizer: VoiceSynthesizer | None = None,
    ) -> None:
        if not configuration.endpoint:
            msg = "Kokoro provider configuration requires a local voice model path (endpoint)."
            raise ValueError(msg)
        voices_path = configuration.metadata.get("voices_path")
        if not voices_path:
            msg = "Kokoro provider configuration requires a local voices file path (metadata['voices_path'])."
            raise ValueError(msg)
        self._configuration = configuration
        if synthesizer is not None:
            self._synthesizer = synthesizer
        else:
            try:
                self._synthesizer = _load_synthesizer(
                    configuration.endpoint,
                    voices_path,
                    configuration.metadata.get("voice", DEFAULT_VOICE),
                    configuration.metadata.get("lang", DEFAULT_LANG),
                )
            except Exception as exc:
                msg = (
                    "Kokoro voice model could not be loaded from path: "
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
            msg = f"Kokoro synthesis failed: {type(exc).__name__}."
            raise RuntimeError(msg) from exc

        if not audio_bytes:
            msg = "Unexpected Kokoro response: empty audio body."
            raise RuntimeError(msg)

        return SpeechSynthesisResponse(
            provider_name=self.name,
            audio_bytes=audio_bytes,
            mime_type=MIME_TYPE,
            metadata={"model_path": self._configuration.endpoint},
        )
