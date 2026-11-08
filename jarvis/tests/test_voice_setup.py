"""Tests for ESR-0062 WP3 (EIP-ESR0062-003): voice provisioning - the catalog,
trust before loading, background loading, downloads, the RPCs, and EBG-0179
(a voice that fails to load never stops the backend starting).

No test downloads anything or loads a real model: the network, the hash, the
clock and the model loader are injected, with a small made-up catalog."""

from __future__ import annotations

import hashlib
import io
import json
import logging
import os
import re
import socket
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

import jarvis.interfaces.voice_setup as voice_setup_module
from jarvis.config.voice_models import (
    KOKORO,
    VOICE_MODELS,
    WHISPER_BASE_EN,
    WHISPER_COMMIT,
    VoiceFile,
    VoiceModel,
)
from jarvis.guardian.runtime import GuardianRuntime
from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.stdio_rpc import StdioRpcServer, build_default_runtime
from jarvis.interfaces.voice_setup import (
    DAMAGED,
    DAMAGED_MESSAGE,
    DISK_MESSAGE,
    FAILED,
    LOADING,
    MISSING,
    ON,
    PART_SUFFIX,
    UNFINISHED_MESSAGE,
    VERIFIED_FILENAME,
    HttpsOnlyRedirects,
    Location,
    VoiceSetup,
)
from jarvis.shared.errors import ClientFacingValueError
from jarvis.tests.household import join_household

# -- a small made-up catalog ----------------------------------------------------------------------------------------

SPEAK_A = b"speaking model bytes " * 10
SPEAK_B = b"voices"
LISTEN_A = b"listening model"


def _file(name: str, content: bytes) -> VoiceFile:
    return VoiceFile(name, f"https://example.test/{name}", len(content), hashlib.sha256(content).hexdigest())


SPEAKING = VoiceModel("speak", "Speaking", "speaking", ("speak",), (_file("a.onnx", SPEAK_A), _file("b.bin", SPEAK_B)))
LISTENING = VoiceModel("listen", "Listening", "listening", ("listen", "en"), (_file("model.bin", LISTEN_A),))
CONTENT = {"a.onnx": SPEAK_A, "b.bin": SPEAK_B, "model.bin": LISTEN_A}


class _Response:
    def __init__(self, body: bytes, *, fail_after: int | None = None, gate: threading.Event | None = None) -> None:
        self._stream = io.BytesIO(body)
        self._fail_after = fail_after
        self._gate = gate
        self._sent = 0

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self, size: int) -> bytes:
        if self._gate is not None:
            self._gate.wait(5)
        if self._fail_after is not None and self._sent >= self._fail_after:
            raise TimeoutError("stalled")
        chunk = self._stream.read(min(size, 4))
        self._sent += len(chunk)
        return chunk


class _Opener:
    """Serves each catalog file by its name; `bodies` overrides what is sent."""

    def __init__(self, bodies: dict[str, bytes] | None = None, **response_options) -> None:
        self.bodies = bodies or {}
        self.options = response_options
        self.requested: list[str] = []

    def __call__(self, request: urllib.request.Request, timeout: float):
        name = request.full_url.rsplit("/", 1)[1]
        self.requested.append(name)
        return _Response(self.bodies.get(name, CONTENT[name]), **self.options)


class _Loads:
    def __init__(self, fail: set[str] | None = None) -> None:
        self.fail = fail or set()
        self.loaded: list[tuple[str, Location]] = []
        self.installed: dict[str, object] = {}

    def load(self, model, location):
        if model.key in self.fail:
            msg = f"could not open {location.files}"  # a path a log must never repeat
            raise RuntimeError(msg)
        self.loaded.append((model.key, location))
        return f"provider:{model.key}"

    def install(self, model, provider):
        self.installed[model.key] = provider


def _setup(tmp_path, loads=None, *, opener=None, hasher=None, overrides=None, disk_free=None, notes=None, models=None):
    loads = loads or _Loads()
    setup = VoiceSetup(
        tmp_path / "models",
        models or (SPEAKING, LISTENING),
        load=loads.load,
        install=loads.install,
        overrides=overrides,
        opener=opener or _Opener(),
        sleep=lambda seconds: None,
        disk_free=disk_free or (lambda path: 10**12),
        **({"hasher": hasher} if hasher else {}),
    )
    if notes is not None:
        setup.set_notifier(lambda method, params: notes.append((method, params)))
    return setup, loads


def _place(tmp_path, model: VoiceModel, contents: dict[str, bytes] | None = None) -> Path:
    folder = (tmp_path / "models").joinpath(*model.folder)
    folder.mkdir(parents=True, exist_ok=True)
    for item in model.files:
        (folder / item.name).write_bytes((contents or {}).get(item.name, CONTENT[item.name]))
    return folder


class _CountingHasher:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, path: Path) -> str:
        self.calls += 1
        return hashlib.sha256(path.read_bytes()).hexdigest()


# -- the real catalog (V2) ------------------------------------------------------------------------------------------


@pytest.mark.parametrize("model", VOICE_MODELS, ids=lambda m: m.key)
def test_every_catalog_file_is_https_with_a_size_and_a_sha256(model):
    for item in model.files:
        assert item.url.startswith("https://")
        assert item.url.endswith("/" + item.name)
        assert item.size > 0
        assert re.fullmatch(r"[0-9a-f]{64}", item.sha256)
        assert "/" not in item.name and "\\" not in item.name and ".." not in item.name


def test_whisper_is_pinned_to_a_commit_never_a_branch():
    for item in WHISPER_BASE_EN.files:
        assert f"/resolve/{WHISPER_COMMIT}/" in item.url
    assert re.fullmatch(r"[0-9a-f]{40}", WHISPER_COMMIT)


def test_the_decided_models_are_offered():
    """D-1 the full Kokoro model (325 MB); D-2 Whisper base.en (145 MB)."""

    assert {item.name: item.size for item in KOKORO.files}["kokoro-v1.0.onnx"] == 325_532_387
    assert {item.name: item.size for item in WHISPER_BASE_EN.files}["model.bin"] == 145_216_508


# -- trust before loading (V1) and background loading (V5, V6) ------------------------------------------------------


def test_no_files_means_missing_and_nothing_is_loaded(tmp_path):
    setup, loads = _setup(tmp_path)
    setup.load_now()

    assert setup.state("speak") == MISSING
    assert loads.loaded == []


def test_files_jarvis_did_not_download_are_hash_checked_before_the_first_load(tmp_path):
    _place(tmp_path, SPEAKING)
    hasher = _CountingHasher()
    setup, loads = _setup(tmp_path, hasher=hasher)

    setup.load_now()

    assert hasher.calls == 2
    assert setup.state("speak") == ON
    assert loads.installed == {"speak": "provider:speak"}
    assert (tmp_path / "models" / "speak" / VERIFIED_FILENAME).exists()


def test_a_later_start_trusts_the_record_without_hashing_again(tmp_path):
    _place(tmp_path, SPEAKING)
    _setup(tmp_path)[0].load_now()
    hasher = _CountingHasher()
    setup, _ = _setup(tmp_path, hasher=hasher)

    setup.load_now()

    assert hasher.calls == 0
    assert setup.state("speak") == ON


def test_a_changed_file_is_hash_checked_again(tmp_path):
    folder = _place(tmp_path, SPEAKING)
    _setup(tmp_path)[0].load_now()
    stat = (folder / "a.onnx").stat()
    os.utime(folder / "a.onnx", ns=(stat.st_atime_ns, stat.st_mtime_ns + 5_000_000_000))
    hasher = _CountingHasher()
    setup, _ = _setup(tmp_path, hasher=hasher)

    setup.load_now()

    assert hasher.calls == 2
    assert setup.state("speak") == ON


def test_a_damaged_file_of_the_right_size_is_never_loaded(tmp_path):
    tampered = bytes(len(SPEAK_A))
    _place(tmp_path, SPEAKING, {"a.onnx": tampered})
    setup, loads = _setup(tmp_path)

    setup.load_now()

    assert setup.state("speak") == DAMAGED
    assert loads.loaded == []


def test_a_record_cannot_vouch_for_a_file_swapped_after_it(tmp_path):
    folder = _place(tmp_path, SPEAKING)
    _setup(tmp_path)[0].load_now()
    (folder / "a.onnx").write_bytes(bytes(len(SPEAK_A)))  # same size, new time
    setup, loads = _setup(tmp_path)

    setup.load_now()

    assert setup.state("speak") == DAMAGED
    assert loads.loaded == []


def test_incomplete_files_are_damaged(tmp_path):
    folder = _place(tmp_path, SPEAKING)
    (folder / "b.bin").unlink()
    setup, loads = _setup(tmp_path)

    setup.load_now()

    assert setup.state("speak") == DAMAGED
    assert loads.loaded == []


def test_a_model_that_fails_to_load_is_left_off_and_logged_by_type_only(tmp_path, caplog):
    _place(tmp_path, SPEAKING)
    _place(tmp_path, LISTENING)
    setup, _ = _setup(tmp_path, _Loads(fail={"speak"}))

    with caplog.at_level(logging.WARNING):
        setup.load_now()

    assert setup.state("speak") == FAILED
    assert setup.state("listen") == ON  # one failing never holds up the other
    assert "RuntimeError" in caplog.text
    assert str(tmp_path) not in caplog.text


def test_start_returns_at_once_while_a_model_loads(tmp_path):
    _place(tmp_path, SPEAKING)
    release = threading.Event()
    loads = _Loads()

    def slow_load(model, location):
        release.wait(5)
        return "provider"

    setup = VoiceSetup(
        tmp_path / "models", (SPEAKING,), load=slow_load, install=loads.install, sleep=lambda s: None
    )
    setup.start()
    deadline = threading.Event()
    for _ in range(100):
        if setup.state("speak") == LOADING:
            break
        deadline.wait(0.01)

    assert setup.state("speak") == LOADING
    release.set()
    setup.wait()
    assert setup.state("speak") == ON


def test_leftover_partial_downloads_are_removed_at_start(tmp_path):
    folder = (tmp_path / "models" / "speak")
    folder.mkdir(parents=True)
    (folder / ("a.onnx" + PART_SUFFIX)).write_bytes(b"half")
    setup, _ = _setup(tmp_path)

    setup.load_now()

    assert not (folder / ("a.onnx" + PART_SUFFIX)).exists()


def _make_link(link: Path, target: Path) -> None:
    if sys.platform == "win32":
        import _winapi

        _winapi.CreateJunction(str(target), str(link))
    else:
        link.symlink_to(target, target_is_directory=True)


def test_a_linked_model_folder_is_not_used(tmp_path):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    for item in SPEAKING.files:
        (elsewhere / item.name).write_bytes(CONTENT[item.name])
    (tmp_path / "models").mkdir()
    try:
        _make_link(tmp_path / "models" / "speak", elsewhere)
    except OSError:
        pytest.skip("this computer cannot make a link here")
    setup, loads = _setup(tmp_path)

    setup.load_now()

    assert setup.state("speak") == FAILED
    assert loads.loaded == []

    setup.download("speak")
    setup.wait()

    assert setup.status()["download"]["outcome"] == "failed"
    assert "link" in setup.status()["download"]["message"]
    assert loads.loaded == []


# -- developer settings (V1) ----------------------------------------------------------------------------------------


def test_a_developer_setting_at_catalog_sizes_is_hash_checked(tmp_path):
    elsewhere = tmp_path / "dev"
    elsewhere.mkdir()
    (elsewhere / "a.onnx").write_bytes(bytes(len(SPEAK_A)))  # right size, wrong content
    (elsewhere / "b.bin").write_bytes(SPEAK_B)
    override = Location(files={"a.onnx": elsewhere / "a.onnx", "b.bin": elsewhere / "b.bin"}, from_environment=True)
    setup, loads = _setup(tmp_path, overrides={"speak": override})

    setup.load_now()

    assert setup.state("speak") == DAMAGED
    assert loads.loaded == []


def test_a_developers_own_model_is_loaded_as_given(tmp_path):
    override = Location(files={}, name="base.en", from_environment=True)
    setup, loads = _setup(tmp_path, overrides={"listen": override})

    setup.load_now()

    assert setup.state("listen") == ON
    assert loads.loaded == [("listen", override)]


def test_a_voice_set_by_a_developer_setting_is_not_downloaded(tmp_path):
    override = Location(files={}, name="base.en", from_environment=True)
    setup, _ = _setup(tmp_path, overrides={"listen": override})

    with pytest.raises(ClientFacingValueError, match="developer setting"):
        setup.download("listen")


# -- downloads (V3) -------------------------------------------------------------------------------------------------


def test_a_download_puts_checked_files_in_place_and_turns_the_voice_on(tmp_path):
    notes = []
    setup, loads = _setup(tmp_path, notes=notes)
    setup.start()
    setup.wait()

    assert setup.download("speak") == {"started": True, "model": "speak"}
    setup.wait()

    folder = tmp_path / "models" / "speak"
    assert (folder / "a.onnx").read_bytes() == SPEAK_A
    assert (folder / VERIFIED_FILENAME).exists()
    assert not list(folder.glob("*" + PART_SUFFIX))
    assert setup.state("speak") == ON
    assert loads.installed["speak"] == "provider:speak"
    finished = [p for m, p in notes if m == "voice.downloadProgress" and p["state"] == "completed"]
    assert finished and finished[0]["receivedBytes"] == SPEAKING.total_bytes
    assert ("voice.changed", {"model": "speak", "state": ON}) in notes


@pytest.mark.parametrize(
    ("body", "message"),
    [
        (bytes(len(SPEAK_A)), DAMAGED_MESSAGE),  # wrong hash
        (SPEAK_A + b"extra", DAMAGED_MESSAGE),  # too many bytes
        (SPEAK_A[:-3], DAMAGED_MESSAGE),  # cut short
    ],
    ids=["wrong-hash", "too-many-bytes", "cut-short"],
)
def test_a_bad_download_leaves_nothing_in_place(tmp_path, body, message):
    setup, loads = _setup(tmp_path, opener=_Opener({"a.onnx": body}))

    setup.download("speak")
    setup.wait()

    folder = tmp_path / "models" / "speak"
    assert not (folder / "a.onnx").exists()
    assert not list(folder.glob("*" + PART_SUFFIX))
    assert setup.status()["download"] == {
        "active": False,
        "model": "speak",
        "receivedBytes": setup.status()["download"]["receivedBytes"],
        "totalBytes": SPEAKING.total_bytes,
        "outcome": "failed",
        "message": message,
    }
    assert loads.loaded == []


def test_a_stalled_download_ends_and_is_cleaned_up(tmp_path):
    setup, _ = _setup(tmp_path, opener=_Opener(fail_after=8))

    setup.download("speak")
    setup.wait()

    assert setup.status()["download"]["outcome"] == "failed"
    assert setup.status()["download"]["message"] == UNFINISHED_MESSAGE
    assert not list((tmp_path / "models" / "speak").glob("*" + PART_SUFFIX))
    assert setup.state("speak") == MISSING


def test_a_redirect_to_an_address_that_is_not_https_is_refused():
    handler = HttpsOnlyRedirects()
    request = urllib.request.Request("https://example.test/a")

    with pytest.raises(urllib.error.URLError):
        handler.redirect_request(request, None, 302, "Found", {}, "http://example.test/a")
    assert handler.redirect_request(request, None, 302, "Found", {}, "https://cdn.example.test/a") is not None
    assert HttpsOnlyRedirects.max_redirections == 5


def test_a_catalog_address_that_is_not_https_is_never_fetched(tmp_path):
    plain = VoiceModel("plain", "Plain", "speaking", ("plain",), (VoiceFile("a.onnx", "http://example.test/a.onnx", 1, "0" * 64),))
    opener = _Opener()
    setup, _ = _setup(tmp_path, opener=opener, models=(plain,))

    setup.download("plain")
    setup.wait()

    assert opener.requested == []
    assert setup.status()["download"]["outcome"] == "failed"


def test_a_cancelled_download_leaves_nothing_behind(tmp_path):
    gate = threading.Event()
    setup, _ = _setup(tmp_path, opener=_Opener(gate=gate))

    setup.download("speak")
    assert setup.cancel() is True
    gate.set()
    setup.wait()

    assert setup.status()["download"]["outcome"] == "cancelled"
    assert not list((tmp_path / "models" / "speak").glob("*" + PART_SUFFIX))
    assert not (tmp_path / "models" / "speak" / "a.onnx").exists()
    assert setup.state("speak") == MISSING


def test_cancel_after_the_files_are_in_place_undoes_nothing(tmp_path):
    setup, _ = _setup(tmp_path)

    setup.download("speak")
    setup.wait()

    assert setup.cancel() is False
    assert setup.state("speak") == ON


def test_not_enough_disk_space_is_refused_before_anything_is_fetched(tmp_path):
    opener = _Opener()
    setup, _ = _setup(tmp_path, opener=opener, disk_free=lambda path: 10)

    with pytest.raises(ClientFacingValueError, match="not enough free disk space"):
        setup.download("speak")
    assert opener.requested == []


def test_a_disk_that_fills_during_the_download_is_reported(tmp_path, monkeypatch):
    real_open = Path.open

    class _Full:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def write(self, data):
            raise OSError(28, "No space left on device")

    def fake_open(self, mode="r", *args, **kwargs):
        if mode in {"wb", "xb"} and self.name.endswith(PART_SUFFIX):
            return _Full()
        return real_open(self, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", fake_open)
    setup, _ = _setup(tmp_path)

    setup.download("speak")
    setup.wait()

    assert setup.status()["download"]["message"] == DISK_MESSAGE
    assert setup.state("speak") == MISSING


def test_only_one_download_at_a_time(tmp_path):
    gate = threading.Event()
    setup, _ = _setup(tmp_path, opener=_Opener(gate=gate))

    setup.download("speak")
    try:
        with pytest.raises(ClientFacingValueError, match="already downloading"):
            setup.download("listen")
    finally:
        gate.set()
        setup.wait()


def test_two_requests_at_the_same_moment_start_one_download(tmp_path):
    gate = threading.Event()
    setup, _ = _setup(tmp_path, opener=_Opener(gate=gate))
    results = []
    barrier = threading.Barrier(8)

    def ask():
        barrier.wait()
        try:
            results.append(setup.download("speak"))
        except ClientFacingValueError:
            results.append(None)

    threads = [threading.Thread(target=ask) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    gate.set()
    setup.wait()

    assert sum(result is not None for result in results) == 1


def test_downloading_over_a_voice_that_is_on_is_refused(tmp_path):
    _place(tmp_path, SPEAKING)
    setup, _ = _setup(tmp_path)
    setup.load_now()

    with pytest.raises(ClientFacingValueError, match="already on"):
        setup.download("speak")


def test_a_damaged_voice_can_be_downloaded_again(tmp_path):
    _place(tmp_path, SPEAKING, {"a.onnx": bytes(len(SPEAK_A))})
    setup, _ = _setup(tmp_path)
    setup.load_now()
    assert setup.state("speak") == DAMAGED

    setup.download("speak")
    setup.wait()

    assert setup.state("speak") == ON
    assert (tmp_path / "models" / "speak" / "a.onnx").read_bytes() == SPEAK_A


def test_moving_the_file_into_place_is_retried_when_windows_holds_it(tmp_path, monkeypatch):
    real_replace = os.replace
    attempts = []

    def flaky_replace(source, target):
        attempts.append(target)
        if len(attempts) < 3:
            raise PermissionError("held by a scanner")
        return real_replace(source, target)

    monkeypatch.setattr(voice_setup_module.os, "replace", flaky_replace)
    setup, _ = _setup(tmp_path, models=(LISTENING,))

    setup.download("listen")
    setup.wait()

    assert len(attempts) == 3
    assert setup.state("listen") == ON


def test_an_unknown_voice_is_refused(tmp_path):
    setup, _ = _setup(tmp_path)

    with pytest.raises(ClientFacingValueError, match="not one JARVIS offers"):
        setup.download("anything-else")


# -- the runtime swap (V5) ------------------------------------------------------------------------------------------


class _BlockingSpeech:
    def __init__(self, name: str, release: threading.Event | None = None) -> None:
        self.name = name
        self.release = release
        self.started = threading.Event()

    def synthesize(self, text):
        self.started.set()
        if self.release is not None:
            self.release.wait(5)
        return self.name  # the runtime passes the provider's answer straight through


def test_a_provider_installed_while_speaking_never_splits_the_call():
    release = threading.Event()
    first = _BlockingSpeech("first", release)
    runtime = GuardianRuntime(speech_provider=first)
    runtime.start()
    outcome = {}
    worker = threading.Thread(target=lambda: outcome.update(result=runtime.speak("hello")))
    worker.start()
    first.started.wait(5)

    runtime.set_speech_provider(_BlockingSpeech("second"))
    release.set()
    worker.join(5)

    assert outcome["result"] == "first"
    assert runtime.speak("hello") == "second"


# -- the RPCs and roles (V4, V7) ------------------------------------------------------------------------------------


def _server(tmp_path) -> StdioRpcServer:
    return StdioRpcServer(
        build_default_runtime(
            environ={"JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1", "JARVIS_MEMORY_DB_PATH": str(tmp_path / "memory" / "personal.db")}
        ),
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )


def _call(server, method, **params):
    return server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}))


def test_the_voice_folders_are_in_the_jarvis_data_folder(tmp_path):
    server = _server(tmp_path)

    setup = server._runtime.voice_setup
    assert setup.folder(KOKORO) == tmp_path / "models" / "kokoro"
    assert setup.folder(WHISPER_BASE_EN) == tmp_path / "models" / "whisper" / "base.en"


@pytest.mark.parametrize("role", ["Child", "Guest"])
def test_a_child_or_guest_cannot_download_a_voice(tmp_path, role, monkeypatch):
    server = _server(tmp_path)
    join_household(server, "Someone", role)
    started = []
    monkeypatch.setattr(server._runtime.voice_setup, "download", lambda key: started.append(key))

    reply = _call(server, "voice.download", model="kokoro")
    cancel = _call(server, "voice.cancelDownload")

    assert "Only an Administrator or Adult profile can download a voice" in reply["error"]["message"]
    assert "Only an Administrator or Adult profile" in cancel["error"]["message"]
    assert started == []
    assert _call(server, "voice.status")["result"]["mayDownload"] is False


def test_with_no_profile_selected_a_voice_cannot_be_downloaded(tmp_path):
    reply = _call(_server(tmp_path), "voice.download", model="kokoro")

    assert "error" in reply


@pytest.mark.parametrize("role", ["Adult", "Administrator"])
def test_an_adult_or_administrator_can_download_a_voice(tmp_path, role, monkeypatch):
    server = _server(tmp_path)
    join_household(server, "Someone", role)
    monkeypatch.setattr(server._runtime.voice_setup, "download", lambda key: {"started": True, "model": key})

    reply = _call(server, "voice.download", model="kokoro")

    assert reply["result"] == {"started": True, "model": "kokoro"}
    status = _call(server, "voice.status")["result"]
    assert status["mayDownload"] is True
    assert {model["key"]: model["state"] for model in status["models"]} == {"kokoro": "missing", "whisper-base.en": "missing"}


# -- EBG-0179: start-up never fails because of voice (V6) -----------------------------------------------------------


def test_a_voice_that_cannot_load_never_stops_the_backend_starting(tmp_path):
    """The defect found on the packaged backend: the real KokoroProvider given
    files it cannot load used to raise out of build_default_runtime."""

    runtime = build_default_runtime(
        environ={
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "memory" / "personal.db"),
            "JARVIS_KOKORO_MODEL_PATH": str(tmp_path / "missing.onnx"),
            "JARVIS_KOKORO_VOICES_PATH": str(tmp_path / "missing.bin"),
        }
    )
    runtime.voice_setup.load_now()

    assert runtime.speech_available is False
    assert runtime.voice_setup.state("kokoro") == FAILED
    assert runtime.speak("hello").status == "not_connected"


def test_building_the_runtime_loads_no_voice(tmp_path, monkeypatch):
    """Loading waits for the server to start (V5): build_default_runtime
    itself never touches a voice model."""

    calls = []
    monkeypatch.setattr("jarvis.interfaces.stdio_rpc.KokoroProvider", lambda *a, **k: calls.append(a))
    build_default_runtime(
        environ={
            "JARVIS_MEMORY_DB_PATH": str(tmp_path / "memory" / "personal.db"),
            "JARVIS_KOKORO_MODEL_PATH": "kokoro.onnx",
            "JARVIS_KOKORO_VOICES_PATH": "voices.bin",
        }
    )

    assert calls == []


# -- the Mac's recording format (Section 7 item 7) ------------------------------------------------------------------


def test_an_aac_in_mp4_recording_decodes_for_listening():
    av = pytest.importorskip("av")
    np = pytest.importorskip("numpy")
    decode_audio = pytest.importorskip("faster_whisper.audio").decode_audio
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

    assert 15_000 < len(samples) < 17_500  # about one second at 16 kHz


# -- the packaged voice self-check (V10) ----------------------------------------------------------------------------


def test_the_voice_self_check_passes_from_source():
    result = subprocess.run(
        [sys.executable, "scripts/jarvis_backend_entry.py", "--voice-self-check"],
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
        cwd=Path(__file__).resolve().parents[2],
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "voice self-check passed" in result.stdout


def test_socket_timeout_is_a_timeout_error():
    """The stall test relies on urllib's read timeout being a TimeoutError."""

    assert issubclass(socket.timeout, TimeoutError)


# -- implementation review L2, L3 -----------------------------------------------------------------------------------


def test_a_link_planted_at_the_partial_name_is_removed_not_followed(tmp_path):
    folder = tmp_path / "models" / "listen" / "en"
    folder.mkdir(parents=True)
    victim = tmp_path / "victim.txt"
    victim.write_text("keep me", encoding="utf-8")
    try:
        (folder / ("model.bin" + PART_SUFFIX)).symlink_to(victim)
    except OSError:
        pytest.skip("this computer cannot make a file link here")
    setup, _ = _setup(tmp_path, models=(LISTENING,))

    setup.download("listen")
    setup.wait()

    assert victim.read_text(encoding="utf-8") == "keep me"
    assert (folder / "model.bin").read_bytes() == LISTEN_A
    assert setup.state("listen") == ON


def test_a_download_cannot_start_while_the_start_up_check_runs(tmp_path):
    release = threading.Event()
    loads = _Loads()

    def slow_hash(path):
        release.wait(5)
        return hashlib.sha256(path.read_bytes()).hexdigest()

    _place(tmp_path, LISTENING, {"model.bin": LISTEN_A})
    setup = VoiceSetup(
        tmp_path / "models",
        (LISTENING,),
        load=loads.load,
        install=loads.install,
        opener=_Opener(),
        sleep=lambda seconds: None,
        hasher=slow_hash,
    )
    setup.start()
    try:
        with pytest.raises(ClientFacingValueError, match="starting"):
            setup.download("listen")
    finally:
        release.set()
        setup.wait()
    assert setup.state("listen") == ON
