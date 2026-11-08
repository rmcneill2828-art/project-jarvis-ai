"""The voice models JARVIS downloads (ESR-0062 WP3, EIP-ESR0062-003 V2).

A table, kept apart from the logic that reads it. **It is the allow-list for
voice downloads**: JARVIS fetches only these files, from these addresses, and
uses a file only once its size and SHA-256 match the entry here.

* Speaking: Kokoro v1.0, the full-precision model (Programme Sponsor decision
  D-1, the model `bm_george` was chosen on by ear, EIP-ESR0053-002), from the
  `kokoro-onnx` project's GitHub release `model-files-v1.0`.
* Listening: `faster-whisper` `base.en` (decision D-2), from Hugging Face,
  pinned to a commit so the files can never change under the same address.

Sizes and hashes were taken on 8 November 2026: the Kokoro files from the
copies already on the development PC (their sizes equal the release's
published sizes), the Whisper files from the pinned commit (`model.bin`'s hash
equals Hugging Face's own LFS record).
"""

from __future__ import annotations

from dataclasses import dataclass

KOKORO_RELEASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0"
WHISPER_COMMIT = "3d3d5dee26484f91867d81cb899cfcf72b96be6c"
WHISPER_REPOSITORY = f"https://huggingface.co/Systran/faster-whisper-base.en/resolve/{WHISPER_COMMIT}"


@dataclass(frozen=True)
class VoiceFile:
    name: str
    url: str
    size: int
    sha256: str


@dataclass(frozen=True)
class VoiceModel:
    key: str
    label: str
    purpose: str  # "speaking" or "listening"
    folder: tuple[str, ...]  # under the JARVIS models folder
    files: tuple[VoiceFile, ...]

    @property
    def total_bytes(self) -> int:
        return sum(item.size for item in self.files)


KOKORO_MODEL_FILE = "kokoro-v1.0.onnx"
KOKORO_VOICES_FILE = "voices-v1.0.bin"

KOKORO = VoiceModel(
    key="kokoro",
    label="Speaking (Kokoro, British English)",
    purpose="speaking",
    folder=("kokoro",),
    files=(
        VoiceFile(
            KOKORO_MODEL_FILE,
            f"{KOKORO_RELEASE}/{KOKORO_MODEL_FILE}",
            325_532_387,
            "7d5df8ecf7d4b1878015a32686053fd0eebe2bc377234608764cc0ef3636a6c5",
        ),
        VoiceFile(
            KOKORO_VOICES_FILE,
            f"{KOKORO_RELEASE}/{KOKORO_VOICES_FILE}",
            28_214_398,
            "bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d",
        ),
    ),
)

WHISPER_BASE_EN = VoiceModel(
    key="whisper-base.en",
    label="Listening (Whisper base.en)",
    purpose="listening",
    folder=("whisper", "base.en"),
    files=(
        VoiceFile(
            "config.json",
            f"{WHISPER_REPOSITORY}/config.json",
            2_227,
            "f3bc3821e9fc76a27bae538e11ae5b677dcdd352b4600429ce7951d398569aeb",
        ),
        VoiceFile(
            "model.bin",
            f"{WHISPER_REPOSITORY}/model.bin",
            145_216_508,
            "2a166925539a16005f14ff328359f9b9adb9dc4fb631bb3b227526862e93e2ef",
        ),
        VoiceFile(
            "tokenizer.json",
            f"{WHISPER_REPOSITORY}/tokenizer.json",
            2_128_466,
            "929c5252409436dce1b38a75d1abbcb5e132d170d8e324e4e04ed915fa2d22df",
        ),
        VoiceFile(
            "vocabulary.txt",
            f"{WHISPER_REPOSITORY}/vocabulary.txt",
            422_309,
            "ff77588746d3a2595d32ab5b69ffd7b95ce2441ac57533cb66fc3eb575a115cf",
        ),
    ),
)

VOICE_MODELS: tuple[VoiceModel, ...] = (KOKORO, WHISPER_BASE_EN)
