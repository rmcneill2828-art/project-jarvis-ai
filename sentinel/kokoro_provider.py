"""Kokoro (self-hosted local neural TTS) speech-synthesis provider adapter for
Sentinel.

Wired into Guardian's production speech-output path as of EBG-0125
(EIP-ESR0053-002), replacing Piper outright per the Programme Sponsor's
explicit decision following a real live listening comparison among Kokoro's
four confirmed UK English voices. `jarvis/interfaces/stdio_rpc.py`'s
`_build_speech_provider()` is this adapter's production caller.

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

Dual-voice automatic fallback (EIP-ESR0053-002, Codex design-reviewed): a
second, disclosed deviation from Piper's single-voice shape. An optional
`fallback_voice` metadata key lets `synthesize()` retry once with a second
voice if the primary voice's synthesis fails at runtime - Guardian's own
production choice is `bm_george` primary, `bf_isabella` fallback, wired by
`stdio_rpc.py`, not hardcoded here. This required changing `VoiceSynthesizer`
from a single voice bound at construction time (`Callable[[str], bytes]`) to
a voice-parameterised callable (`Callable[[str, str], bytes]`, `(text, voice)`)
so one loaded Kokoro engine - the expensive ~90 MB ONNX session load - can
serve both voices without loading the model twice. This is a disclosed
breaking change to the adapter's internal test seam only, not to any public
RPC contract: no caller outside this module and its own tests constructs a
`VoiceSynthesizer` directly.
"""

import io
import wave
from collections.abc import Callable

from sentinel.provider_config import ProviderConfiguration
from sentinel.speech_providers import SpeechSynthesisRequest, SpeechSynthesisResponse

VoiceSynthesizer = Callable[[str, str], bytes]

MIME_TYPE = "audio/wav"
DEFAULT_VOICE = "af_sarah"
DEFAULT_LANG = "en-us"
_SAMPLE_WIDTH_BYTES = 2  # 16-bit PCM


def _load_synthesizer(model_path: str, voices_path: str, lang: str) -> VoiceSynthesizer:
    import espeakng_loader
    from kokoro_onnx import Kokoro
    from kokoro_onnx.config import EspeakConfig

    # kokoro_onnx phonemizes text via espeak-ng, but does not bundle or locate
    # it itself - without this, construction succeeds but synthesis fails the
    # first time phonemizer looks for a system espeak-ng install that does not
    # exist on a self-hosted-first machine. espeakng_loader ships the actual
    # espeak-ng binary/data (a real runtime dependency as of EIP-ESR0053-002),
    # so this is the one piece of wiring required to make the dependency
    # addition actually functional, not merely importable.
    espeakng_loader.make_library_available()
    espeak_config = EspeakConfig(
        lib_path=espeakng_loader.get_library_path(),
        data_path=espeakng_loader.get_data_path(),
    )
    # Loaded once, shared by every synthesize() call this closure serves -
    # letting a primary and fallback voice share the same engine instance
    # rather than each paying their own ~90 MB ONNX session load.
    engine = Kokoro(model_path, voices_path, espeak_config=espeak_config)

    def synthesize(text: str, voice: str) -> bytes:
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
    Kokoro also requires) - one Kokoro-specific deviation from Piper's
    single-file shape, disclosed here rather than silently added. Optional
    metadata keys `voice` and `lang` default to `af_sarah`/`en-us`. A further
    optional `fallback_voice` metadata key, unset by default, enables the
    automatic-retry behaviour described in this module's own docstring.
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
        self._voice = configuration.metadata.get("voice", DEFAULT_VOICE)
        self._fallback_voice = configuration.metadata.get("fallback_voice")
        if synthesizer is not None:
            self._synthesizer = synthesizer
        else:
            try:
                self._synthesizer = _load_synthesizer(
                    configuration.endpoint,
                    voices_path,
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
        voice_used = self._voice
        try:
            audio_bytes = self._synthesizer(request.text, self._voice)
        except Exception as primary_exc:
            if self._fallback_voice is None:
                msg = f"Kokoro synthesis failed: {type(primary_exc).__name__}."
                raise RuntimeError(msg) from primary_exc
            try:
                voice_used = self._fallback_voice
                audio_bytes = self._synthesizer(request.text, self._fallback_voice)
            except Exception as fallback_exc:
                msg = f"Kokoro synthesis failed for primary and fallback voice: {type(fallback_exc).__name__}."
                raise RuntimeError(msg) from fallback_exc

        if not audio_bytes:
            msg = "Unexpected Kokoro response: empty audio body."
            raise RuntimeError(msg)

        return SpeechSynthesisResponse(
            provider_name=self.name,
            audio_bytes=audio_bytes,
            mime_type=MIME_TYPE,
            metadata={"model_path": self._configuration.endpoint, "voice_used": voice_used},
        )
