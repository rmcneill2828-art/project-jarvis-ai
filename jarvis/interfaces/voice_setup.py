"""Voice setup: finding, checking, downloading and loading the voice models
(ESR-0062 WP3, EIP-ESR0062-003; EBG-0167, EBG-0179).

Speaking (Kokoro) and listening (`faster-whisper`) each need model files. An
installed JARVIS fetches them itself, from the catalog in
`jarvis/config/voice_models.py`, which is the allow-list:

* **Trust before loading (V1).** A model is loaded only once every file's size
  and SHA-256 match the catalog - checked by the download itself, or, for
  files JARVIS did not download (copies made by hand, say), in the background
  before the first load. A small `verified.json` (each file's size and
  modification time) lets later starts skip the hash while nothing has
  changed. A damaged file is never handed to ONNX Runtime or CTranslate2, so
  it cannot crash the backend in native code.
* **Background loading (V5, V6).** `start()` returns at once; each model is
  checked and loaded on its own thread, so the backend answers immediately,
  and one model failing never holds up the other. A load that raises leaves
  that voice off and is logged by exception type only.
* **Downloads (V3).** One at a time; HTTPS at every hop; file names only from
  the catalog; written to `<name>.part`, size-capped, hash-checked, then moved
  into place with `os.replace`. Nothing downloaded is ever run.

Every outside effect (the network, the disk, the clock, the hash, loading a
model) is injectable, so the whole module is tested without a download or a
model.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import shutil
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jarvis.config.voice_models import VoiceFile, VoiceModel
from jarvis.shared.errors import ClientFacingValueError

logger = logging.getLogger(__name__)

READ_TIMEOUT_SECONDS = 60.0
CHUNK_BYTES = 1024 * 1024
PROGRESS_INTERVAL_SECONDS = 0.5
DISK_HEADROOM_FRACTION = 0.10
MAX_REDIRECTS = 5
REPLACE_ATTEMPTS = 5
REPLACE_RETRY_SECONDS = 0.2
VERIFIED_FILENAME = "verified.json"
PART_SUFFIX = ".part"

# A model's state, as `voice.status` reports it.
MISSING = "missing"
CHECKING = "checking"
LOADING = "loading"
ON = "on"
DAMAGED = "damaged"
FAILED = "failed"
DOWNLOADING = "downloading"

DAMAGED_MESSAGE = "The download was damaged. Try again."
DISK_MESSAGE = "JARVIS could not save the download. The disk may be full."
UNFINISHED_MESSAGE = "The download did not finish. Try again."

Notifier = Callable[[str, dict[str, Any]], None]
Opener = Callable[[urllib.request.Request, float], Any]


@dataclass(frozen=True)
class Location:
    """Where one model's files are. `files` maps each catalog file name to a
    path. A developer may instead name a model (`name`, for example Whisper's
    "base.en"), with no files: that is loaded as given, as before WP3."""

    files: Mapping[str, Path]
    folder: Path | None = None
    name: str | None = None
    from_environment: bool = False


Loader = Callable[[VoiceModel, Location], Any]
Installer = Callable[[VoiceModel, Any], None]


class _Cancelled(Exception):
    pass


class _DownloadError(Exception):
    """A download failure whose message may be shown to the person."""


class HttpsOnlyRedirects(urllib.request.HTTPRedirectHandler):
    """Follow a redirect only to another https:// address, at most five times.

    GitHub and Hugging Face both redirect to signed content-delivery hosts, so
    the host is not pinned: the catalog's SHA-256 is what is trusted."""

    max_redirections = MAX_REDIRECTS

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urllib.parse.urlparse(newurl).scheme.lower() != "https":
            reason = "A download was redirected to an address that is not https."
            raise urllib.error.URLError(reason)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def https_opener() -> Opener:
    opener = urllib.request.build_opener(HttpsOnlyRedirects())

    def open_url(request: urllib.request.Request, timeout: float) -> Any:
        return opener.open(request, timeout=timeout)

    return open_url


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK_BYTES), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _default_disk_free(path: Path) -> int | None:
    probe = path
    while not probe.exists():
        if probe.parent == probe:
            return None
        probe = probe.parent
    try:
        return shutil.disk_usage(probe).free
    except OSError:
        return None


def _is_link(path: Path) -> bool:
    return os.path.islink(path) or os.path.isjunction(path)


class VoiceSetup:
    """The voice models' state, their background loading and their download."""

    def __init__(
        self,
        root: Path,
        models: Iterable[VoiceModel],
        *,
        load: Loader,
        install: Installer,
        overrides: Mapping[str, Location] | None = None,
        opener: Opener | None = None,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
        disk_free: Callable[[Path], int | None] = _default_disk_free,
        hasher: Callable[[Path], str] = sha256_of,
    ) -> None:
        self._root = root
        self._models = {model.key: model for model in models}
        self._load = load
        self._install = install
        self._overrides = dict(overrides or {})
        self._opener = opener if opener is not None else https_opener()
        self._clock = clock
        self._sleep = sleep
        self._disk_free = disk_free
        self._hasher = hasher
        self._notify: Notifier = lambda method, params: None
        self._lock = threading.Lock()
        self._states = dict.fromkeys(self._models, MISSING)
        self._download: dict[str, Any] = self._idle_download()
        self._cancel = threading.Event()
        self._threads: list[threading.Thread] = []
        self._started = False
        # Each model's start-up check, so a download cannot begin while it runs
        # (implementation review L3).
        self._checks: dict[str, threading.Thread] = {}
        self._last_progress = float("-inf")

    @staticmethod
    def _idle_download() -> dict[str, Any]:
        return {"active": False, "model": None, "receivedBytes": 0, "totalBytes": 0, "outcome": None, "message": None}

    # -- public ------------------------------------------------------------------------------------------------------

    def set_notifier(self, notify: Notifier) -> None:
        self._notify = notify

    def folder(self, model: VoiceModel) -> Path:
        return self._root.joinpath(*model.folder)

    def location(self, model: VoiceModel) -> Location:
        override = self._overrides.get(model.key)
        if override is not None:
            return override
        folder = self.folder(model)
        return Location(files={item.name: folder / item.name for item in model.files}, folder=folder)

    def state(self, key: str) -> str:
        with self._lock:
            return self._states[key]

    def status(self) -> dict[str, Any]:
        with self._lock:
            states = dict(self._states)
            download = dict(self._download)
        return {
            "models": [
                {
                    "key": model.key,
                    "label": model.label,
                    "purpose": model.purpose,
                    "state": states[model.key],
                    "totalBytes": model.total_bytes,
                    "fromEnvironment": model.key in self._overrides,
                }
                for model in self._models.values()
            ],
            "download": download,
            "freeBytes": self._disk_free(self._root),
        }

    def start(self) -> None:
        """Remove leftover partial downloads, then check and load each model on
        its own background thread. Returns at once and never raises."""

        with self._lock:
            if self._started:
                return
            self._started = True
        for model in self._models.values():
            self._remove_parts(model)
            self._spawn(self._bring_up, model, f"jarvis-voice-{model.key}", check=True)

    def wait(self, timeout: float | None = None) -> None:
        """Block until every background check, load and download has ended (tests)."""

        while True:
            with self._lock:
                running = [thread for thread in self._threads if thread.is_alive()]
            if not running:
                return
            for thread in running:
                thread.join(timeout)
            if timeout is not None:
                return

    def load_now(self) -> None:
        """`start()` and wait: for tests and tools that need voice ready on return."""

        self.start()
        self.wait()

    def download(self, key: str) -> dict[str, Any]:
        """Begin downloading catalog model `key`. Raises for anything not allowed."""

        model = self._models.get(key)
        if model is None:
            msg = "That voice is not one JARVIS offers."
            raise ClientFacingValueError(msg)
        if key in self._overrides:
            msg = "This voice is set by a developer setting, so it is not downloaded here."
            raise ClientFacingValueError(msg)
        folder = self.folder(model)
        needed = self._bytes_needed(model)
        free = self._disk_free(folder)
        if free is not None and free < int(needed * (1 + DISK_HEADROOM_FRACTION)):
            msg = (
                f"There is not enough free disk space for this voice: it needs about "
                f"{needed / 1024**2:.0f} MB and {free / 1024**2:.0f} MB is free."
            )
            raise ClientFacingValueError(msg)
        with self._lock:
            if self._download["active"]:
                msg = "A voice is already downloading."
                raise ClientFacingValueError(msg)
            state = self._states[key]
            if state == ON:
                msg = "Voice is already on."
                raise ClientFacingValueError(msg)
            check = self._checks.get(key)
            if state in {CHECKING, LOADING} or (check is not None and check.is_alive()):
                msg = "This voice is starting. Try again in a moment."
                raise ClientFacingValueError(msg)
            self._cancel.clear()
            self._last_progress = float("-inf")
            self._download = {**self._idle_download(), "active": True, "model": key, "totalBytes": needed}
            self._states[key] = DOWNLOADING
            thread = threading.Thread(
                target=self._run_download, args=(model,), daemon=True, name=f"jarvis-voice-download-{key}"
            )
            self._threads.append(thread)
        try:
            thread.start()
        except BaseException:
            # The worker never ran: without this the download would stay "active"
            # and block every later one (the WP3c lesson from PullManager).
            with self._lock:
                self._download = {**self._idle_download(), "outcome": "failed"}
                self._states[key] = self._resting_state(model)
            raise
        self._changed(model, DOWNLOADING)
        return {"started": True, "model": key}

    def cancel(self) -> bool:
        """Ask the running download to stop. False if none is running."""

        with self._lock:
            if not self._download["active"]:
                return False
        self._cancel.set()
        return True

    # -- checking and loading ----------------------------------------------------------------------------------------

    def _spawn(self, target: Callable[[VoiceModel], None], model: VoiceModel, name: str, *, check: bool = False) -> None:
        thread = threading.Thread(target=target, args=(model,), daemon=True, name=name)
        with self._lock:
            self._threads.append(thread)
            if check:
                self._checks[model.key] = thread
        try:
            thread.start()
        except Exception as exc:  # noqa: BLE001 - a voice must never stop the backend starting (EBG-0179)
            logger.warning("%s is off: it could not be started (%s).", model.label, type(exc).__name__)
            self._set(model, FAILED)

    def _bring_up(self, model: VoiceModel) -> None:
        """Check `model` and, if it can be trusted, load and install it."""

        try:
            location = self.location(model)
            if not self._trusted(model, location):
                return
            self._set(model, LOADING)
            provider = self._load(model, location)
            self._install(model, provider)
            self._set(model, ON)
        except Exception as exc:  # noqa: BLE001 - a voice problem must cost only the voice (EBG-0179)
            logger.warning("%s is off: the voice model could not be loaded (%s).", model.label, type(exc).__name__)
            self._set(model, FAILED)

    def _trusted(self, model: VoiceModel, location: Location) -> bool:
        """True if `model` may be loaded from `location`. Sets the state and
        returns False if it is missing or damaged."""

        if location.from_environment:
            paths = [location.files.get(item.name) for item in model.files]
            if not location.files or not all(
                path is not None and path.is_file() and path.stat().st_size == item.size
                for path, item in zip(paths, model.files, strict=True)
            ):
                # A developer's own model, named or at other sizes: loaded as
                # given, exactly as before WP3.
                return True
            self._set(model, CHECKING)
            if self._hashes_match(model, location):
                return True
            logger.warning("%s is off: its files do not match the catalog.", model.label)
            self._set(model, DAMAGED)
            return False

        folder = self.folder(model)
        if self._has_link(folder):
            logger.warning("%s is off: its folder is a link, which JARVIS does not use.", model.label)
            self._set(model, FAILED)
            return False
        paths = [location.files[item.name] for item in model.files]
        if not any(path.exists() for path in paths):
            logger.info("%s is not configured.", model.label)
            self._set(model, MISSING)
            return False
        if not all(
            path.is_file() and path.stat().st_size == item.size for path, item in zip(paths, model.files, strict=True)
        ):
            logger.warning("%s is off: its files are incomplete.", model.label)
            self._set(model, DAMAGED)
            return False
        if self._marker_matches(model):
            return True
        self._set(model, CHECKING)
        if not self._hashes_match(model, location):
            logger.warning("%s is off: its files do not match the catalog.", model.label)
            self._set(model, DAMAGED)
            return False
        self._write_marker(model)
        return True

    def _hashes_match(self, model: VoiceModel, location: Location) -> bool:
        return all(self._hasher(location.files[item.name]) == item.sha256 for item in model.files)

    def _marker_matches(self, model: VoiceModel) -> bool:
        folder = self.folder(model)
        try:
            recorded = json.loads((folder / VERIFIED_FILENAME).read_text(encoding="utf-8"))["files"]
            for item in model.files:
                entry = recorded[item.name]
                stat = (folder / item.name).stat()
                if (
                    entry["sha256"] != item.sha256
                    or entry["size"] != item.size
                    or stat.st_size != item.size
                    or entry["mtimeNs"] != stat.st_mtime_ns
                ):
                    return False
        except (OSError, ValueError, KeyError, TypeError):
            return False
        return True

    def _write_marker(self, model: VoiceModel) -> None:
        folder = self.folder(model)
        try:
            files = {
                item.name: {"size": item.size, "sha256": item.sha256, "mtimeNs": (folder / item.name).stat().st_mtime_ns}
                for item in model.files
            }
            (folder / VERIFIED_FILENAME).write_text(json.dumps({"files": files}, indent=2), encoding="utf-8")
        except OSError as exc:
            # Only costs a hash check at the next start.
            logger.warning("Could not record that %s was checked (%s).", model.label, type(exc).__name__)

    def _has_link(self, folder: Path) -> bool:
        """Whether the model folder, or any folder between it and the models
        folder, is a link or junction."""

        probe = folder
        while True:
            if _is_link(probe):
                return True
            if probe == self._root or probe.parent == probe:
                return False
            probe = probe.parent

    def _remove_parts(self, model: VoiceModel) -> None:
        folder = self.folder(model)
        for item in model.files:
            try:
                (folder / (item.name + PART_SUFFIX)).unlink(missing_ok=True)
            except OSError:
                logger.warning("Could not remove a partial %s download.", model.label)

    def _resting_state(self, model: VoiceModel) -> str:
        """MISSING if none of the model's files is there, otherwise DAMAGED."""

        folder = self.folder(model)
        return DAMAGED if any((folder / item.name).exists() for item in model.files) else MISSING

    def _bytes_needed(self, model: VoiceModel) -> int:
        folder = self.folder(model)
        needed = 0
        for item in model.files:
            path = folder / item.name
            try:
                present = path.is_file() and path.stat().st_size == item.size
            except OSError:
                present = False
            if not present:
                needed += item.size
        return needed

    def _set(self, model: VoiceModel, state: str) -> None:
        """Record a state; tell the screen only when it changed."""

        with self._lock:
            changed = self._states[model.key] != state
            self._states[model.key] = state
        if changed:
            self._changed(model, state)

    def _changed(self, model: VoiceModel, state: str) -> None:
        self._notify("voice.changed", {"model": model.key, "state": state})

    # -- downloading -------------------------------------------------------------------------------------------------

    def _run_download(self, model: VoiceModel) -> None:
        outcome = "failed"
        message: str | None = UNFINISHED_MESSAGE
        try:
            folder = self.folder(model)
            folder.mkdir(parents=True, exist_ok=True)
            if self._has_link(folder):
                raise _DownloadError("The voice folder is a link, which JARVIS does not use.")
            for item in model.files:
                target = folder / item.name
                if target.is_file() and target.stat().st_size == item.size and self._hasher(target) == item.sha256:
                    continue
                self._fetch(model, item, folder)
            # Every file is verified and in place: a cancel no longer undoes it.
            self._write_marker(model)
            outcome, message = "completed", None
        except _Cancelled:
            outcome, message = "cancelled", None
        except _DownloadError as exc:
            outcome, message = "failed", str(exc)
        except Exception as exc:  # noqa: BLE001 - a download failure must end the download cleanly, whatever raised
            logger.warning("A voice download failed: %s", type(exc).__name__)
        finally:
            with self._lock:
                self._download.update(active=False, outcome=outcome, message=message)
                download = dict(self._download)
                if outcome != "completed":
                    self._states[model.key] = self._resting_state(model)
                state = self._states[model.key]
            self._notify(
                "voice.downloadProgress",
                {
                    "model": model.key,
                    "state": outcome,
                    "receivedBytes": download["receivedBytes"],
                    "totalBytes": download["totalBytes"],
                    "message": message,
                },
            )
            if outcome != "completed":
                self._changed(model, state)
        if outcome == "completed":
            self._bring_up(model)

    def _fetch(self, model: VoiceModel, item: VoiceFile, folder: Path) -> None:
        if urllib.parse.urlparse(item.url).scheme.lower() != "https":
            raise _DownloadError(DAMAGED_MESSAGE)
        part = folder / (item.name + PART_SUFFIX)
        request = urllib.request.Request(item.url, headers={"User-Agent": "JARVIS-voice-setup"})
        digest = hashlib.sha256()
        received = 0
        try:
            # Whatever is at the partial name - a leftover, or a link planted there -
            # is removed (a link itself, never its target), and the file is created
            # afresh, refusing anything that appears meanwhile (review L2).
            part.unlink(missing_ok=True)
            with self._opener(request, READ_TIMEOUT_SECONDS) as response, part.open("xb") as out:
                while True:
                    if self._cancel.is_set():
                        raise _Cancelled
                    chunk = response.read(CHUNK_BYTES)
                    if not chunk:
                        break
                    received += len(chunk)
                    if received > item.size:
                        # Content-Length is not trusted: stop at the catalog size.
                        raise _DownloadError(DAMAGED_MESSAGE)
                    try:
                        out.write(chunk)
                    except OSError as exc:
                        raise _DownloadError(DISK_MESSAGE) from exc
                    digest.update(chunk)
                    self._progress(model, len(chunk))
            if received != item.size or digest.hexdigest() != item.sha256:
                raise _DownloadError(DAMAGED_MESSAGE)
            self._replace(part, folder / item.name)
        except BaseException:
            try:
                part.unlink(missing_ok=True)
            except OSError:
                logger.warning("Could not remove a partial %s download.", model.label)
            raise

    def _replace(self, part: Path, target: Path) -> None:
        """`os.replace`, retried briefly: on Windows an antivirus scanner can
        hold a newly written file for a moment."""

        for attempt in range(REPLACE_ATTEMPTS):
            try:
                os.replace(part, target)
                return
            except PermissionError:
                if attempt == REPLACE_ATTEMPTS - 1:
                    raise
                self._sleep(REPLACE_RETRY_SECONDS)

    def _progress(self, model: VoiceModel, added: int) -> None:
        now = self._clock()
        with self._lock:
            self._download["receivedBytes"] += added
            if now - self._last_progress < PROGRESS_INTERVAL_SECONDS:
                return
            self._last_progress = now
            params = {
                "model": model.key,
                "state": "downloading",
                "receivedBytes": self._download["receivedBytes"],
                "totalBytes": self._download["totalBytes"],
            }
        self._notify("voice.downloadProgress", params)
