"""Prove the packaged backend carries every part voice needs, with no model
download (ESR-0062 WP3, EIP-ESR0062-003 V10).

Run as `jarvis-backend --voice-self-check` against the built executable in CI,
on Windows and macOS. Each library the voice uses reads data files that sit
beside its own code (`kokoro_onnx`'s `config.json`, espeak-ng's library and
data, Whisper's voice-activity model, PyAV's codecs); a one-file build leaves
them out unless asked, and the voice then fails only on the household's
computer. Each check prints one line; the exit status is non-zero if any fails.
"""

from __future__ import annotations

import ctypes
import io
from collections.abc import Callable
from pathlib import Path
from typing import TextIO


def _imports() -> str:
    import av  # noqa: F401
    import ctranslate2  # noqa: F401
    import faster_whisper  # noqa: F401
    import kokoro_onnx  # noqa: F401
    import onnxruntime  # noqa: F401
    import tokenizers  # noqa: F401

    return "kokoro_onnx, faster_whisper, ctranslate2, onnxruntime, tokenizers and av import"


def _kokoro_config() -> str:
    from kokoro_onnx.config import get_vocab

    vocab = get_vocab()
    if not vocab:
        msg = "kokoro_onnx's vocabulary is empty"
        raise RuntimeError(msg)
    return f"kokoro_onnx config.json read ({len(vocab)} symbols)"


def _espeak_phonemizes() -> str:
    import espeakng_loader
    from kokoro_onnx.config import EspeakConfig
    from kokoro_onnx.tokenizer import Tokenizer

    library = Path(espeakng_loader.get_library_path())
    data = Path(espeakng_loader.get_data_path())
    if not library.is_file() or not data.is_dir():
        msg = "the bundled espeak-ng library or its data is missing"
        raise RuntimeError(msg)
    # The bundled library itself, not a system one kokoro_onnx would fall back to.
    ctypes.cdll.LoadLibrary(str(library))
    espeakng_loader.make_library_available()
    tokenizer = Tokenizer(EspeakConfig(lib_path=str(library), data_path=str(data)))
    phonemes = tokenizer.phonemize("Good evening.", lang="en-gb")
    if not phonemes.strip():
        msg = "espeak-ng returned no phonemes"
        raise RuntimeError(msg)
    return "espeak-ng loaded from the build and phonemized a sentence"


def _onnx_session() -> str:
    import onnxruntime
    from faster_whisper.utils import get_assets_path

    model = Path(get_assets_path()) / "silero_vad_v6.onnx"
    onnxruntime.InferenceSession(str(model), providers=["CPUExecutionProvider"])
    return "ONNX Runtime opened Whisper's voice-activity model"


def _decodes_mp4() -> str:
    import av
    import numpy as np
    from faster_whisper.audio import decode_audio

    buffer = io.BytesIO()
    container = av.open(buffer, "w", format="mp4")
    stream = container.add_stream("aac", rate=48000)
    stream.layout = "mono"
    tone = np.sin(2 * np.pi * 440 * np.arange(48000) / 48000).astype("float32").reshape(1, -1)
    frame = av.AudioFrame.from_ndarray(tone, format="fltp", layout="mono")
    frame.sample_rate = 48000
    for packet in stream.encode(frame):
        container.mux(packet)
    for packet in stream.encode():
        container.mux(packet)
    container.close()
    samples = decode_audio(io.BytesIO(buffer.getvalue()))
    if not 15_000 < len(samples) < 17_500:
        msg = f"decoded {len(samples)} samples, expected about 16000"
        raise RuntimeError(msg)
    return "PyAV decoded an AAC-in-MP4 recording (the Mac's format)"


CHECKS: tuple[Callable[[], str], ...] = (_imports, _kokoro_config, _espeak_phonemizes, _onnx_session, _decodes_mp4)


def run(out: TextIO) -> int:
    failures = 0
    for check in CHECKS:
        try:
            out.write(f"ok   {check()}\n")
        except Exception as exc:  # noqa: BLE001 - report every part, whatever failed
            failures += 1
            out.write(f"FAIL {check.__name__.strip('_')}: {type(exc).__name__}: {exc}\n")
    out.write("voice self-check passed\n" if failures == 0 else f"voice self-check FAILED ({failures})\n")
    out.flush()
    return 0 if failures == 0 else 1


# -- the release jobs' real round trip (V11) ------------------------------------------------------------------------

ROUND_TRIP_SENTENCE = "Good evening. This is a voice test."
ROUND_TRIP_WORDS = ("evening", "voice", "test")


def round_trip(root: Path, out: TextIO) -> int:
    """With the real models under `root` (as `scripts/fetch_voice_models.py`
    leaves them), speak a sentence with Kokoro and hear it back with Whisper.
    Run against the built executable in the two release jobs."""

    from jarvis.config.voice_models import (
        KOKORO,
        KOKORO_MODEL_FILE,
        KOKORO_VOICES_FILE,
        WHISPER_BASE_EN,
    )
    from sentinel.kokoro_provider import KokoroProvider
    from sentinel.provider_config import ProviderConfiguration
    from sentinel.speech_providers import SpeechSynthesisRequest
    from sentinel.transcription_providers import TranscriptionRequest
    from sentinel.whisper_provider import WhisperProvider

    try:
        kokoro_folder = root.joinpath(*KOKORO.folder)
        speech = KokoroProvider(
            ProviderConfiguration(
                provider_name="kokoro",
                endpoint=str(kokoro_folder / KOKORO_MODEL_FILE),
                metadata={"voices_path": str(kokoro_folder / KOKORO_VOICES_FILE), "voice": "bm_george", "lang": "en-gb"},
            )
        ).synthesize(SpeechSynthesisRequest(text=ROUND_TRIP_SENTENCE))
        out.write(f"ok   Kokoro spoke {len(speech.audio_bytes)} bytes of audio\n")
        heard = (
            WhisperProvider(
                ProviderConfiguration(provider_name="whisper", endpoint=str(root.joinpath(*WHISPER_BASE_EN.folder)))
            )
            .transcribe(TranscriptionRequest(audio_bytes=speech.audio_bytes, mime_type=speech.mime_type))
            .text
        )
        out.write(f"ok   Whisper heard: {heard}\n")
        missing = [word for word in ROUND_TRIP_WORDS if word not in heard.lower()]
        if missing:
            out.write(f"voice round trip FAILED: did not hear {', '.join(missing)}\n")
            return 1
    except Exception as exc:  # noqa: BLE001 - report whatever failed
        out.write(f"voice round trip FAILED: {type(exc).__name__}: {exc}\n")
        return 1
    out.write("voice round trip passed\n")
    out.flush()
    return 0
