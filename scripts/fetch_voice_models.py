"""Download JARVIS's voice models into a folder, for the release jobs' real
voice round trip (ESR-0062 WP3, EIP-ESR0062-003 V11).

    python scripts/fetch_voice_models.py <folder>

Uses the app's own `VoiceSetup`, so the files are fetched exactly as the app
fetches them - from the catalog, HTTPS only, size- and SHA-256-checked - and a
folder already holding good copies (a CI cache hit) downloads nothing.
Exits non-zero if any model is not ready.
"""

from __future__ import annotations

import sys
from pathlib import Path

from jarvis.config.voice_models import VOICE_MODELS
from jarvis.interfaces.voice_setup import ON, VoiceSetup


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 2
    root = Path(argv[0]).resolve()
    # Loading is only a marker here: the built executable loads the real models.
    setup = VoiceSetup(root, VOICE_MODELS, load=lambda model, location: object(), install=lambda model, provider: None)
    setup.load_now()
    for model in VOICE_MODELS:
        if setup.state(model.key) != ON:
            print(f"Downloading {model.label} ({model.total_bytes // 1024**2} MB)...", flush=True)
            setup.download(model.key)
            setup.wait()
    failed = [model.label for model in VOICE_MODELS if setup.state(model.key) != ON]
    for model in VOICE_MODELS:
        print(f"{model.label}: {setup.state(model.key)}")
    if failed:
        print(f"Not ready: {', '.join(failed)}. {setup.status()['download'].get('message') or ''}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
