"""Local model setup: is Ollama there, which model suits this machine, and
fetching one (ESR-0061 WP3c, EIP-ESR0061-003 6.9; ADR-0023).

JARVIS answers on this computer first, so a fresh install has to be able to
get a working local model without the person knowing what Ollama is. This
module reports, recommends and - only when asked - downloads. It never installs
Ollama, never starts it and never runs anything it downloaded:

* `OllamaSetup.status()` - is Ollama installed, running, which models it holds.
  "Installed" means the executable is on the PATH or in a standard place;
  "running" means a short `GET /api/version` answered. Neither starts anything.
* `recommend()` - from the machine's memory, a model and a smaller fallback
  from `jarvis/config/ollama_models.py`, with the download size and whether
  there is room on disk for it.
* `PullManager` - downloads a catalog model through Ollama's own `/api/pull`,
  in the background, with progress notifications and a cancel. A tag that is
  not in the catalog is refused: the catalog is the allow-list.
* `ModelChoice` - which model conversation uses, remembered in a small file.
  The `JARVIS_OLLAMA_MODEL` environment variable still overrides it.

Every outside effect (the HTTP calls, the executable lookup, the hardware
readers, the clock) is injectable, so the whole module is tested without Ollama.
"""

from __future__ import annotations

import json
import logging
import os
import platform
import shutil
import subprocess
import threading
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psutil

from jarvis.config.ollama_models import BUDGET_RULES, MODELS, BudgetRules, CatalogModel
from jarvis.shared.errors import ClientFacingValueError

logger = logging.getLogger(__name__)

GIB = 1024**3
DEFAULT_ENDPOINT = "http://localhost:11434"
DOWNLOAD_PAGE_URL = "https://ollama.com/download"
STATUS_TIMEOUT_SECONDS = 2.0
# How long a download may sit silent before it is treated as stalled. Ollama
# streams progress lines every fraction of a second while data is moving.
PULL_READ_TIMEOUT_SECONDS = 60.0
# At most one progress notification per this interval, plus the last one.
PROGRESS_INTERVAL_SECONDS = 0.5

HttpGet = Callable[[str, float], bytes]
Notifier = Callable[[str, dict[str, Any]], None]


# --- hardware and recommendation -----------------------------------------------------------------------------------


@dataclass(frozen=True)
class HardwareInfo:
    """What the machine can give a model. Memory in bytes; None means unknown."""

    system: str
    ram_bytes: int
    gpu_bytes: int | None
    unified_memory: bool
    free_disk_bytes: int | None


def _nvidia_memory_bytes(run: Callable[..., Any], which: Callable[[str], str | None]) -> int | None:
    """The largest NVIDIA graphics card's memory, from `nvidia-smi`, or None."""

    executable = which("nvidia-smi")
    if executable is None:
        return None
    try:
        completed = run(
            [executable, "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    sizes: list[int] = []
    for line in completed.stdout.splitlines():
        try:
            sizes.append(int(float(line.strip())) * 1024 * 1024)  # nvidia-smi reports MiB
        except ValueError:
            continue
    return max(sizes) if sizes else None


def model_store_directory(environ: Mapping[str, str]) -> Path:
    """Where Ollama keeps its models: `OLLAMA_MODELS`, else `~/.ollama/models`."""

    explicit = (environ.get("OLLAMA_MODELS") or "").strip()
    return Path(explicit) if explicit else Path.home() / ".ollama" / "models"


def _free_disk_bytes(directory: Path, disk_usage: Callable[[Path], Any]) -> int | None:
    """Free space on the volume `directory` is (or would be) on."""

    candidate = directory
    while not candidate.exists() and candidate.parent != candidate:
        candidate = candidate.parent
    try:
        return int(disk_usage(candidate).free)
    except OSError:
        return None


def read_hardware(
    environ: Mapping[str, str] | None = None,
    *,
    system: str | None = None,
    machine: str | None = None,
    ram_bytes: int | None = None,
    run: Callable[..., Any] = subprocess.run,
    which: Callable[[str], str | None] = shutil.which,
    disk_usage: Callable[[Path], Any] = shutil.disk_usage,
) -> HardwareInfo:
    """Read this machine's memory and the free space where models are kept."""

    environ = os.environ if environ is None else environ
    system = system or platform.system()
    machine = machine or platform.machine()
    unified = system == "Darwin" and machine.lower() in {"arm64", "aarch64"}
    return HardwareInfo(
        system=system,
        ram_bytes=ram_bytes if ram_bytes is not None else psutil.virtual_memory().total,
        gpu_bytes=None if unified else _nvidia_memory_bytes(run, which),
        unified_memory=unified,
        free_disk_bytes=_free_disk_bytes(model_store_directory(environ), disk_usage),
    )


def memory_budget_gb(hardware: HardwareInfo, rules: BudgetRules = BUDGET_RULES) -> float:
    """The memory, in GiB, that counts towards running a model on this machine."""

    if hardware.unified_memory:
        return hardware.ram_bytes / GIB * rules.unified_memory_fraction
    if hardware.gpu_bytes is not None:
        return hardware.gpu_bytes / GIB * rules.gpu_fraction
    return min(hardware.ram_bytes / GIB * rules.cpu_fraction, rules.cpu_cap_gb)


@dataclass(frozen=True)
class Recommendation:
    primary: CatalogModel
    fallback: CatalogModel | None
    budget_gb: float
    reason: str
    below_minimum: bool
    needs_disk_bytes: int
    disk_ok: bool | None


def recommend(
    hardware: HardwareInfo,
    models: tuple[CatalogModel, ...] = MODELS,
    rules: BudgetRules = BUDGET_RULES,
) -> Recommendation:
    """The best catalog model this machine can run, and the next one down.

    `models` is ordered largest first. A machine below every model's minimum is
    given the smallest, flagged `below_minimum`, rather than nothing.
    """

    budget = memory_budget_gb(hardware, rules)
    index = next((i for i, model in enumerate(models) if budget >= model.min_budget_gb), len(models) - 1)
    primary = models[index]
    fallback = models[index + 1] if index + 1 < len(models) else None
    below = budget < primary.min_budget_gb
    if hardware.unified_memory:
        source = f"this Mac's shared memory ({hardware.ram_bytes / GIB:.0f} GB, about {budget:.1f} GB usable for a model)"
    elif hardware.gpu_bytes is not None:
        source = f"this computer's graphics card ({hardware.gpu_bytes / GIB:.0f} GB)"
    else:
        source = f"this computer's processor and memory ({hardware.ram_bytes / GIB:.0f} GB, no supported graphics card found)"
    reason = f"Chosen for {source}."
    needs = int(primary.download_bytes * (1 + rules.disk_headroom_fraction))
    disk_ok = None if hardware.free_disk_bytes is None else hardware.free_disk_bytes >= needs
    return Recommendation(primary, fallback, budget, reason, below, needs, disk_ok)


# --- is Ollama here, and is it running -------------------------------------------------------------------------------


def install_locations(environ: Mapping[str, str], system: str) -> tuple[Path, ...]:
    """Where Ollama puts its executable when installed the normal way."""

    if system == "Windows":
        local = (environ.get("LOCALAPPDATA") or "").strip()
        return (Path(local) / "Programs" / "Ollama" / "ollama.exe",) if local else ()
    if system == "Darwin":
        return (
            Path("/Applications/Ollama.app"),
            Path("/usr/local/bin/ollama"),
            Path("/opt/homebrew/bin/ollama"),
        )
    return (Path("/usr/local/bin/ollama"), Path("/usr/bin/ollama"))


def install_steps(system: str) -> tuple[str, ...]:
    """Plain steps for getting Ollama, for this platform. JARVIS runs none of them."""

    if system == "Windows":
        return (
            "Open the Ollama download page and choose the Windows download.",
            "Run the installer you downloaded and follow its steps.",
            "Ollama then runs in the background; come back here and press Check again.",
        )
    if system == "Darwin":
        return (
            "Open the Ollama download page and choose the macOS download.",
            "Open the downloaded file and drag Ollama into Applications.",
            "Open Ollama once from Applications, then come back here and press Check again.",
        )
    return (
        "Open the Ollama download page and follow the instructions for Linux.",
        "Start the Ollama service as those instructions describe.",
        "Come back here and press Check again.",
    )


def _default_http_get(url: str, timeout_seconds: float) -> bytes:
    with urllib.request.urlopen(url, timeout=timeout_seconds) as response:
        return response.read()


def _parse_object(raw: bytes) -> dict[str, Any] | None:
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


# --- which model conversation uses -------------------------------------------------------------------------------------


class ModelChoice:
    """The local model conversation uses.

    Order of authority: the `JARVIS_OLLAMA_MODEL` environment variable (a
    deliberate override, left alone), then the choice saved here, then the
    built-in default. The saved choice is a catalog tag in a small JSON file;
    a missing, unreadable or unknown value is ignored.
    """

    def __init__(
        self,
        path: Path,
        default_model: str,
        environment_model: str | None,
        catalog_tags: Iterable[str],
    ) -> None:
        self._path = path
        self._default_model = default_model
        self._environment_model = environment_model
        self._catalog_tags = frozenset(catalog_tags)
        self._lock = threading.Lock()

    @property
    def source(self) -> str:
        """`environment`, `saved` or `default` - where the active model came from."""

        if self._environment_model:
            return "environment"
        return "saved" if self._saved() is not None else "default"

    def _saved(self) -> str | None:
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        model = data.get("model") if isinstance(data, dict) else None
        return model if isinstance(model, str) and model in self._catalog_tags else None

    def current(self) -> str:
        """The model conversation should use right now."""

        with self._lock:
            return self._environment_model or self._saved() or self._default_model

    def save(self, tag: str) -> None:
        """Remember `tag`. Only a catalog tag is accepted."""

        if tag not in self._catalog_tags:
            msg = "That model is not one JARVIS offers."
            raise ClientFacingValueError(msg)
        with self._lock:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self._path.with_suffix(".tmp")
            temporary.write_text(json.dumps({"model": tag}), encoding="utf-8")
            temporary.replace(self._path)


# --- downloading ----------------------------------------------------------------------------------------------------------


class PullManager:
    """Downloads one catalog model at a time, in the background.

    A download takes minutes, so it runs on its own thread and reports through
    notifications (`ollama.pullProgress`, then `ollama.pullFinished`) rather
    than holding up the slow lane that answers conversation. Cancelling closes
    the connection; Ollama keeps the layers already fetched, so a later pull
    resumes. Nothing downloaded is ever run by JARVIS.
    """

    def __init__(
        self,
        endpoint: str,
        models: tuple[CatalogModel, ...],
        *,
        opener: Callable[..., Any] = urllib.request.urlopen,
        clock: Callable[[], float] = time.monotonic,
        disk_free: Callable[[], int | None] = lambda: None,
        rules: BudgetRules = BUDGET_RULES,
    ) -> None:
        self._endpoint = endpoint.rstrip("/")
        self._models = {model.tag: model for model in models}
        self._opener = opener
        self._clock = clock
        self._disk_free = disk_free
        self._rules = rules
        self._notify: Notifier = lambda method, params: None
        self._lock = threading.Lock()
        self._thread: threading.Thread | None = None
        self._cancel = threading.Event()
        self._state: dict[str, Any] = {"active": False, "model": None, "completed": 0, "total": 0, "status": "idle"}

    def set_notifier(self, notify: Notifier) -> None:
        self._notify = notify

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return dict(self._state)

    def start(self, tag: str) -> dict[str, Any]:
        """Begin downloading `tag`. Raises for anything but a catalog tag."""

        model = self._models.get(tag)
        if model is None:
            msg = "That model is not one JARVIS offers."
            raise ClientFacingValueError(msg)
        free = self._disk_free()
        needed = int(model.download_bytes * (1 + self._rules.disk_headroom_fraction))
        if free is not None and free < needed:
            msg = (
                f"There is not enough free disk space for {model.label}: it needs about "
                f"{needed / GIB:.1f} GB and {free / GIB:.1f} GB is free."
            )
            raise ClientFacingValueError(msg)
        with self._lock:
            if self._state["active"]:
                msg = "A model is already downloading."
                raise ClientFacingValueError(msg)
            self._cancel.clear()
            self._state = {"active": True, "model": tag, "completed": 0, "total": 0, "status": "starting"}
            self._thread = threading.Thread(target=self._run, args=(tag,), daemon=True, name="jarvis-ollama-pull")
            thread = self._thread
        try:
            thread.start()
        except BaseException:
            # The worker never ran (for example the system could not make
            # another thread): without this, `active` would stay true and block
            # every later download (Engineering Reviewer finding, WP3c).
            with self._lock:
                self._state = {"active": False, "model": None, "completed": 0, "total": 0, "status": "failed"}
            raise
        return {"started": True, "model": tag}

    def cancel(self) -> bool:
        """Ask the running download to stop. False if none is running."""

        with self._lock:
            if not self._state["active"]:
                return False
        self._cancel.set()
        return True

    def wait(self, timeout: float | None = None) -> None:
        """Block until the running download ends (used by tests)."""

        thread = self._thread
        if thread is not None:
            thread.join(timeout)

    def _progress(self, layers: dict[str, tuple[int, int]], status: str, tag: str) -> None:
        total = sum(t for t, _ in layers.values())
        completed = sum(c for _, c in layers.values())
        if status == "success":
            # Ollama's small manifest layers carry a total but never a final
            # completed count; at success everything is, by definition, done.
            completed = total
        with self._lock:
            self._state.update(completed=completed, total=total, status=status)
        self._notify(
            "ollama.pullProgress",
            {"model": tag, "status": status, "completed": completed, "total": total},
        )

    def _run(self, tag: str) -> None:
        outcome = "failed"
        layers: dict[str, tuple[int, int]] = {}
        last_sent = float("-inf")
        status = "starting"
        try:
            request = urllib.request.Request(
                f"{self._endpoint}/api/pull",
                data=json.dumps({"model": tag, "stream": True}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self._opener(request, timeout=PULL_READ_TIMEOUT_SECONDS) as response:
                for raw_line in response:
                    if self._cancel.is_set():
                        outcome = "cancelled"
                        break
                    event = _parse_object(raw_line)
                    if event is None:
                        continue
                    if event.get("error"):
                        # Ollama's own wording can name paths or hosts; keep it in the log's type only.
                        logger.warning("Ollama reported a download error.")
                        break
                    status = str(event.get("status") or status)
                    digest = event.get("digest")
                    if isinstance(digest, str) and isinstance(event.get("total"), int):
                        layers[digest] = (event["total"], int(event.get("completed") or 0))
                    if status == "success":
                        outcome = "completed"
                        break
                    now = self._clock()
                    if now - last_sent >= PROGRESS_INTERVAL_SECONDS:
                        last_sent = now
                        self._progress(layers, status, tag)
                else:
                    outcome = "completed" if status == "success" else "failed"
        except Exception as exc:  # noqa: BLE001 - a download failure must end the download cleanly, whatever raised
            logger.warning("Model download failed: %s", type(exc).__name__)
            outcome = "cancelled" if self._cancel.is_set() else "failed"
        finally:
            if outcome == "completed":
                self._progress(layers, "success", tag)
            with self._lock:
                self._state.update(active=False, status=outcome)
            self._notify("ollama.pullFinished", {"model": tag, "outcome": outcome})


# --- the whole picture -------------------------------------------------------------------------------------------------


class OllamaSetup:
    """What the UI needs to set up local conversation: status, a recommendation,
    downloads and the choice of model."""

    def __init__(
        self,
        *,
        endpoint: str | None,
        choice: ModelChoice,
        pulls: PullManager,
        environ: Mapping[str, str] | None = None,
        system: str | None = None,
        http_get: HttpGet = _default_http_get,
        which: Callable[[str], str | None] = shutil.which,
        path_exists: Callable[[Path], bool] = Path.exists,
        hardware_reader: Callable[[], HardwareInfo] | None = None,
        models: tuple[CatalogModel, ...] = MODELS,
    ) -> None:
        self._endpoint = (endpoint or DEFAULT_ENDPOINT).rstrip("/")
        self._choice = choice
        self._pulls = pulls
        self._environ = os.environ if environ is None else environ
        self._system = system or platform.system()
        self._http_get = http_get
        self._which = which
        self._path_exists = path_exists
        self._models = models
        self._hardware_reader = hardware_reader or (lambda: read_hardware(self._environ))

    @property
    def pulls(self) -> PullManager:
        return self._pulls

    @property
    def choice(self) -> ModelChoice:
        return self._choice

    def _installed_path(self) -> str | None:
        on_path = self._which("ollama")
        if on_path:
            return on_path
        for location in install_locations(self._environ, self._system):
            if self._path_exists(location):
                return str(location)
        return None

    def _get_json(self, path: str) -> dict[str, Any] | None:
        try:
            return _parse_object(self._http_get(f"{self._endpoint}{path}", STATUS_TIMEOUT_SECONDS))
        except (OSError, ValueError):
            return None

    def installed_models(self) -> tuple[str, ...] | None:
        """Tags Ollama holds, or None when it cannot be reached."""

        data = self._get_json("/api/tags")
        if data is None or not isinstance(data.get("models"), list):
            return None
        return tuple(str(item["name"]) for item in data["models"] if isinstance(item, dict) and "name" in item)

    def status(self) -> dict[str, Any]:
        version_data = self._get_json("/api/version")
        running = version_data is not None
        installed_path = self._installed_path()
        # A running Ollama is installed by definition, wherever it lives.
        installed = running or installed_path is not None
        tags = self.installed_models() if running else None
        active = self._choice.current()
        result: dict[str, Any] = {
            "installed": installed,
            "running": running,
            "version": version_data.get("version") if version_data and isinstance(version_data.get("version"), str) else None,
            "endpoint": self._endpoint,
            "models": list(tags) if tags is not None else [],
            "activeModel": active,
            "activeModelInstalled": tags is not None and active in tags,
            "modelSource": self._choice.source,
        }
        if not running:
            result["install"] = {"url": DOWNLOAD_PAGE_URL, "steps": list(install_steps(self._system)), "installed": installed}
        return result

    def recommendation(self) -> dict[str, Any]:
        hardware = self._hardware_reader()
        advice = recommend(hardware, self._models)
        tags = self.installed_models() or ()

        def describe(model: CatalogModel | None) -> dict[str, Any] | None:
            if model is None:
                return None
            return {
                "tag": model.tag,
                "label": model.label,
                "downloadGb": round(model.download_bytes / GIB, 1),
                "note": model.note,
                "installed": model.tag in tags,
            }

        return {
            "hardware": {
                "system": hardware.system,
                "ramGb": round(hardware.ram_bytes / GIB, 1),
                "gpuGb": None if hardware.gpu_bytes is None else round(hardware.gpu_bytes / GIB, 1),
                "unifiedMemory": hardware.unified_memory,
                "freeDiskGb": None if hardware.free_disk_bytes is None else round(hardware.free_disk_bytes / GIB, 1),
            },
            "primary": describe(advice.primary),
            "fallback": describe(advice.fallback),
            "reason": advice.reason,
            "belowMinimum": advice.below_minimum,
            "needsDiskGb": round(advice.needs_disk_bytes / GIB, 1),
            "diskOk": advice.disk_ok,
            "models": [describe(model) for model in self._models],
        }

    def use_model(self, tag: str) -> dict[str, Any]:
        """Make `tag` the conversation model. It must be a catalog model Ollama
        already holds - choosing one it lacks would break conversation."""

        if tag not in {model.tag for model in self._models}:
            msg = "That model is not one JARVIS offers."
            raise ClientFacingValueError(msg)
        tags = self.installed_models()
        if tags is None:
            msg = "Ollama is not running, so JARVIS cannot check that model is installed."
            raise ClientFacingValueError(msg)
        if tag not in tags:
            msg = "That model has not been downloaded yet."
            raise ClientFacingValueError(msg)
        self._choice.save(tag)
        return {"activeModel": self._choice.current(), "modelSource": self._choice.source}
