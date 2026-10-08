"""Tests for local model setup: hardware, recommendation, status, the model
choice and downloads (ESR-0061 WP3c, EIP-ESR0061-003 6.9). No Ollama needed:
every outside effect is injected."""

import io
import json
import subprocess
import threading
import urllib.error
from pathlib import Path
from types import SimpleNamespace

import pytest

from jarvis.config.ollama_models import MODELS, CatalogModel
from jarvis.guardian.runtime import GuardianRuntime
from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces.ollama_setup import (
    DEFAULT_ENDPOINT,
    DOWNLOAD_PAGE_URL,
    GIB,
    HardwareInfo,
    ModelChoice,
    OllamaSetup,
    PullManager,
    install_locations,
    install_steps,
    memory_budget_gb,
    model_store_directory,
    read_hardware,
    recommend,
)
from jarvis.interfaces.stdio_rpc import StdioRpcServer
from sentinel.ollama_provider import OllamaProvider
from sentinel.provider_config import ProviderConfiguration
from sentinel.providers import ProviderRequest

TAGS = [model.tag for model in MODELS]


# --- the catalog ---------------------------------------------------------------------------------------------------


def test_the_catalog_is_ordered_largest_first_with_a_floor_that_fits_anything():
    sizes = [model.download_bytes for model in MODELS]
    budgets = [model.min_budget_gb for model in MODELS]

    assert sizes == sorted(sizes, reverse=True)
    assert budgets == sorted(budgets, reverse=True)
    assert MODELS[-1].min_budget_gb == 0


def test_catalog_tags_are_unique_licensed_and_sized():
    assert len(set(TAGS)) == len(TAGS)
    assert all(model.license == "Apache-2.0" and model.download_bytes > 0 and model.note for model in MODELS)
    assert all(model.tag.startswith("qwen3.5:") for model in MODELS)


# --- hardware ------------------------------------------------------------------------------------------------------


def _nvidia(stdout="8188\n", returncode=0):
    def run(command, **kwargs):
        assert command[0] == "/usr/bin/nvidia-smi"
        assert "--query-gpu=memory.total" in command
        return SimpleNamespace(returncode=returncode, stdout=stdout)

    return run


def _hardware(tmp_path, **overrides):
    defaults = {
        "environ": {"OLLAMA_MODELS": str(tmp_path / "models")},
        "system": "Windows",
        "machine": "AMD64",
        "ram_bytes": 32 * GIB,
        "run": _nvidia(),
        "which": lambda name: "/usr/bin/nvidia-smi",
        "disk_usage": lambda path: SimpleNamespace(free=20 * GIB),
    }
    return read_hardware(**{**defaults, **overrides})


def test_a_windows_pc_with_an_nvidia_card_reports_its_memory_and_free_disk(tmp_path):
    hardware = _hardware(tmp_path)

    assert hardware.gpu_bytes == 8188 * 1024 * 1024
    assert hardware.unified_memory is False
    assert hardware.ram_bytes == 32 * GIB
    assert hardware.free_disk_bytes == 20 * GIB


def test_the_largest_of_several_cards_counts(tmp_path):
    assert _hardware(tmp_path, run=_nvidia("6144\n12288\n")).gpu_bytes == 12288 * 1024 * 1024


@pytest.mark.parametrize(
    "run",
    [
        _nvidia(returncode=9),
        _nvidia("not a number\n"),
        _nvidia(""),
        lambda *a, **k: (_ for _ in ()).throw(OSError("gone")),
        lambda *a, **k: (_ for _ in ()).throw(subprocess.TimeoutExpired("nvidia-smi", 5)),
    ],
)
def test_an_unreadable_gpu_means_no_gpu_not_a_crash(tmp_path, run):
    assert _hardware(tmp_path, run=run).gpu_bytes is None


def test_no_nvidia_smi_means_no_gpu(tmp_path):
    assert _hardware(tmp_path, which=lambda name: None).gpu_bytes is None


def test_apple_silicon_is_unified_memory_and_never_asks_for_a_gpu(tmp_path):
    def forbidden(*args, **kwargs):
        raise AssertionError("nvidia-smi must not run on a Mac")

    hardware = _hardware(tmp_path, system="Darwin", machine="arm64", run=forbidden, ram_bytes=16 * GIB)

    assert hardware.unified_memory is True
    assert hardware.gpu_bytes is None


def test_an_intel_mac_is_not_unified_memory(tmp_path):
    assert _hardware(tmp_path, system="Darwin", machine="x86_64", which=lambda n: None).unified_memory is False


def test_free_disk_is_read_where_models_are_kept_walking_up_to_an_existing_folder(tmp_path):
    seen = []

    def disk_usage(path):
        seen.append(path)
        return SimpleNamespace(free=7 * GIB)

    hardware = _hardware(tmp_path, environ={"OLLAMA_MODELS": str(tmp_path / "not" / "yet" / "there")}, disk_usage=disk_usage)

    assert hardware.free_disk_bytes == 7 * GIB
    assert seen == [tmp_path]


def test_an_unreadable_disk_is_unknown_not_zero(tmp_path):
    def broken(path):
        raise OSError("no")

    assert _hardware(tmp_path, disk_usage=broken).free_disk_bytes is None


def test_the_model_store_is_where_ollama_models_says_else_the_home_folder():
    assert model_store_directory({"OLLAMA_MODELS": " /data/models "}) == Path("/data/models")
    assert model_store_directory({}) == Path.home() / ".ollama" / "models"
    assert model_store_directory({"OLLAMA_MODELS": "  "}) == Path.home() / ".ollama" / "models"


# --- the recommendation --------------------------------------------------------------------------------------------


def _machine(*, gpu_gb=None, ram_gb=32, unified=False, free_disk_gb=100):
    return HardwareInfo(
        system="Darwin" if unified else "Windows",
        ram_bytes=int(ram_gb * GIB),
        gpu_bytes=None if gpu_gb is None else int(gpu_gb * GIB),
        unified_memory=unified,
        free_disk_bytes=None if free_disk_gb is None else int(free_disk_gb * GIB),
    )


@pytest.mark.parametrize(
    ("machine", "primary", "fallback"),
    [
        # The household PC: RTX 4060 8 GB. The 9B runs fast alone but cannot sit beside the safety model.
        (_machine(gpu_gb=8), "qwen3.5:4b", "qwen3.5:2b"),
        (_machine(gpu_gb=12), "qwen3.5:9b", "qwen3.5:4b"),
        (_machine(gpu_gb=24), "qwen3.5:9b", "qwen3.5:4b"),
        (_machine(gpu_gb=4), "qwen3.5:2b", "qwen3.5:0.8b"),
        # The household Mac: Apple Silicon, 16 GB shared.
        (_machine(ram_gb=16, unified=True), "qwen3.5:4b", "qwen3.5:2b"),
        (_machine(ram_gb=24, unified=True), "qwen3.5:9b", "qwen3.5:4b"),
        (_machine(ram_gb=8, unified=True), "qwen3.5:2b", "qwen3.5:0.8b"),
        # No supported graphics card: the processor, so a small model whatever the memory.
        (_machine(ram_gb=32), "qwen3.5:2b", "qwen3.5:0.8b"),
        (_machine(ram_gb=64), "qwen3.5:4b", "qwen3.5:2b"),
        (_machine(ram_gb=4), "qwen3.5:0.8b", None),
    ],
)
def test_the_recommendation_follows_the_machine(machine, primary, fallback):
    advice = recommend(machine)

    assert advice.primary.tag == primary
    assert (advice.fallback.tag if advice.fallback else None) == fallback
    assert advice.below_minimum is False


def test_the_reason_names_what_the_choice_was_based_on():
    assert "graphics card (8 GB)" in recommend(_machine(gpu_gb=8)).reason
    assert "Mac's shared memory (16 GB" in recommend(_machine(ram_gb=16, unified=True)).reason
    assert "no supported graphics card" in recommend(_machine(ram_gb=16)).reason


def test_a_machine_below_every_minimum_gets_the_smallest_flagged():
    models = (CatalogModel("big", "Big", 10 * GIB, 8.0, "x", "n"), CatalogModel("small", "Small", GIB, 3.0, "x", "n"))

    advice = recommend(_machine(gpu_gb=1), models)

    assert advice.primary.tag == "small"
    assert advice.below_minimum is True
    assert advice.fallback is None


def test_disk_space_is_checked_against_the_download_plus_headroom():
    enough = recommend(_machine(gpu_gb=8, free_disk_gb=50))
    short = recommend(_machine(gpu_gb=8, free_disk_gb=3))
    unknown = recommend(_machine(gpu_gb=8, free_disk_gb=None))

    assert enough.disk_ok is True
    assert short.disk_ok is False
    assert unknown.disk_ok is None
    assert enough.needs_disk_bytes == int(3_320_000_000 * 1.2)


def test_the_memory_budget_for_each_kind_of_machine():
    assert memory_budget_gb(_machine(gpu_gb=8)) == pytest.approx(8.0)
    assert memory_budget_gb(_machine(ram_gb=16, unified=True)) == pytest.approx(8.0)
    assert memory_budget_gb(_machine(ram_gb=32)) == pytest.approx(4.0)
    assert memory_budget_gb(_machine(ram_gb=256)) == pytest.approx(6.0)  # capped


# --- status --------------------------------------------------------------------------------------------------------


class _Http:
    """Fakes Ollama's GET endpoints."""

    def __init__(self, version="0.35.0", models=("qwen3.5:2b",), up=True) -> None:
        self.version, self.models, self.up = version, models, up
        self.urls: list[str] = []

    def __call__(self, url, timeout):
        self.urls.append(url)
        assert timeout <= 5
        if not self.up:
            raise urllib.error.URLError("refused")
        if url.endswith("/api/version"):
            return json.dumps({"version": self.version}).encode()
        if url.endswith("/api/tags"):
            return json.dumps({"models": [{"name": name} for name in self.models]}).encode()
        raise AssertionError(url)


def _setup(tmp_path, *, http=None, which=lambda n: None, exists=lambda p: False, system="Windows", environment_model=None, opener=None, disk_free=lambda: None):
    choice = ModelChoice(tmp_path / "choice.json", "qwen3.5:2b", environment_model, TAGS)
    pulls = PullManager("http://localhost:11434", MODELS, opener=opener or (lambda *a, **k: None), disk_free=disk_free)
    return OllamaSetup(
        endpoint=None,
        choice=choice,
        pulls=pulls,
        environ={"LOCALAPPDATA": "C:/Users/x/AppData/Local"},
        system=system,
        http_get=http or _Http(),
        which=which,
        path_exists=exists,
        hardware_reader=lambda: _machine(gpu_gb=8),
    )


def test_a_running_ollama_reports_its_version_models_and_the_active_model(tmp_path):
    status = _setup(tmp_path, http=_Http(models=("qwen3.5:2b", "qwen3.5:4b"))).status()

    assert status["installed"] is True
    assert status["running"] is True
    assert status["version"] == "0.35.0"
    assert status["models"] == ["qwen3.5:2b", "qwen3.5:4b"]
    assert status["activeModel"] == "qwen3.5:2b"
    assert status["activeModelInstalled"] is True
    assert status["modelSource"] == "default"
    assert status["endpoint"] == DEFAULT_ENDPOINT
    assert "install" not in status


def test_an_active_model_ollama_lacks_is_reported_missing(tmp_path):
    assert _setup(tmp_path, http=_Http(models=("other:1b",))).status()["activeModelInstalled"] is False


def test_not_installed_gives_the_steps_and_the_download_page(tmp_path):
    status = _setup(tmp_path, http=_Http(up=False)).status()

    assert (status["installed"], status["running"]) == (False, False)
    assert status["install"]["url"] == DOWNLOAD_PAGE_URL == "https://ollama.com/download"
    assert status["install"]["installed"] is False
    assert len(status["install"]["steps"]) == 3
    assert status["models"] == []
    assert status["activeModelInstalled"] is False


def test_installed_but_not_running_is_told_apart_from_not_installed(tmp_path):
    on_path = _setup(tmp_path, http=_Http(up=False), which=lambda n: "/usr/local/bin/ollama").status()
    in_place = _setup(tmp_path, http=_Http(up=False), exists=lambda p: p.name == "ollama.exe").status()

    for status in (on_path, in_place):
        assert (status["installed"], status["running"]) == (True, False)
        assert status["install"]["installed"] is True


def test_a_running_ollama_counts_as_installed_wherever_it_lives(tmp_path):
    assert _setup(tmp_path, http=_Http()).status()["installed"] is True


@pytest.mark.parametrize("body", [b"not json", b"[]", b'"x"', b""])
def test_a_garbled_answer_means_not_running(tmp_path, body):
    status = _setup(tmp_path, http=lambda url, timeout: body).status()

    assert status["running"] is False


def test_status_never_starts_or_installs_anything(tmp_path):
    http = _Http()
    _setup(tmp_path, http=http).status()

    assert all(url.endswith(("/api/version", "/api/tags")) for url in http.urls)


def test_the_platform_decides_where_ollama_is_looked_for_and_what_to_do():
    assert install_locations({"LOCALAPPDATA": "C:/L"}, "Windows") == (Path("C:/L/Programs/Ollama/ollama.exe"),)
    assert install_locations({}, "Windows") == ()
    assert Path("/Applications/Ollama.app") in install_locations({}, "Darwin")
    assert Path("/usr/local/bin/ollama") in install_locations({}, "Linux")
    assert "macOS" in install_steps("Darwin")[0]
    assert "Windows" in install_steps("Windows")[0]
    assert "Linux" in install_steps("Linux")[0]


# --- the model choice ----------------------------------------------------------------------------------------------


def _choice(tmp_path, environment_model=None):
    return ModelChoice(tmp_path / "choice.json", "qwen3.5:2b", environment_model, TAGS)


def test_with_nothing_saved_the_default_model_is_used(tmp_path):
    choice = _choice(tmp_path)

    assert (choice.current(), choice.source) == ("qwen3.5:2b", "default")


def test_a_saved_choice_is_remembered_across_restarts(tmp_path):
    _choice(tmp_path).save("qwen3.5:4b")
    again = _choice(tmp_path)

    assert (again.current(), again.source) == ("qwen3.5:4b", "saved")


def test_the_environment_variable_still_overrides_a_saved_choice(tmp_path):
    _choice(tmp_path).save("qwen3.5:4b")
    overridden = _choice(tmp_path, environment_model="llama3.1:8b")

    assert (overridden.current(), overridden.source) == ("llama3.1:8b", "environment")


def test_only_a_catalog_tag_can_be_saved(tmp_path):
    choice = _choice(tmp_path)

    for tag in ["llama3.1:8b", "qwen3.5:9b ", "", "../x"]:
        with pytest.raises(ValueError, match="not one JARVIS offers"):
            choice.save(tag)
    assert not (tmp_path / "choice.json").exists()


@pytest.mark.parametrize("content", ["not json", "[]", '{"model": 5}', '{"model": "llama3.1:8b"}', ""])
def test_an_unreadable_or_unknown_saved_value_is_ignored(tmp_path, content):
    (tmp_path / "choice.json").write_text(content, encoding="utf-8")

    assert (_choice(tmp_path).current(), _choice(tmp_path).source) == ("qwen3.5:2b", "default")


def test_the_provider_asks_ollama_for_the_chosen_model_on_every_request(tmp_path):
    sent = []

    def transport(url, body, headers, timeout):
        sent.append(json.loads(body)["model"])
        return json.dumps({"response": "hi"}).encode()

    choice = _choice(tmp_path)
    provider = OllamaProvider(
        ProviderConfiguration(provider_name="ollama", default_model="qwen3.5:2b"),
        transport=transport,
        model_source=choice.current,
    )

    provider.execute(ProviderRequest(prompt="a"))
    choice.save("qwen3.5:4b")
    response = provider.execute(ProviderRequest(prompt="b"))

    assert sent == ["qwen3.5:2b", "qwen3.5:4b"]
    assert response.metadata["model"] == "qwen3.5:4b"


@pytest.mark.parametrize("source", [lambda: "", lambda: "   ", lambda: None])
def test_the_provider_falls_back_to_its_default_when_the_source_gives_nothing(source):
    provider = OllamaProvider(
        ProviderConfiguration(provider_name="ollama", default_model="qwen3.5:2b"),
        transport=lambda *a: b'{"response": "x"}',
        model_source=source,
    )

    assert provider.model == "qwen3.5:2b"


def test_using_a_model_needs_a_catalog_tag_that_ollama_already_holds(tmp_path):
    setup = _setup(tmp_path, http=_Http(models=("qwen3.5:2b", "qwen3.5:4b", "llama3.1:8b")))

    assert setup.use_model("qwen3.5:4b") == {"activeModel": "qwen3.5:4b", "modelSource": "saved"}
    with pytest.raises(ValueError, match="not one JARVIS offers"):
        setup.use_model("llama3.1:8b")  # installed, but not offered
    with pytest.raises(ValueError, match="not been downloaded"):
        setup.use_model("qwen3.5:9b")  # offered, but absent
    with pytest.raises(ValueError, match="not running"):
        _setup(tmp_path, http=_Http(up=False)).use_model("qwen3.5:4b")


def test_the_recommendation_marks_what_is_already_installed(tmp_path):
    result = _setup(tmp_path, http=_Http(models=("qwen3.5:4b",))).recommendation()

    assert result["primary"]["tag"] == "qwen3.5:4b"
    assert result["primary"]["installed"] is True
    assert result["fallback"]["installed"] is False
    assert result["hardware"]["gpuGb"] == 8.0
    assert result["diskOk"] is True
    assert [item["tag"] for item in result["models"]] == TAGS


# --- downloads -----------------------------------------------------------------------------------------------------


class _Stream:
    """A streamed /api/pull response."""

    def __init__(self, lines, hold=None) -> None:
        self._lines = lines
        self._hold = hold
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.closed = True
        return False

    def __iter__(self):
        for line in self._lines:
            if self._hold is not None:
                self._hold(line)
            yield (json.dumps(line) if isinstance(line, dict) else line).encode()


def _pull_lines(*layers):
    lines = [{"status": "pulling manifest"}]
    for step in range(1, 5):
        for digest, total in layers:
            lines.append({"status": f"pulling {digest[:6]}", "digest": digest, "total": total, "completed": total * step // 4})
    lines.append({"status": "verifying sha256 digest"})
    lines.append({"status": "success"})
    return lines


class _Clock:
    def __init__(self) -> None:
        self.now = 0.0

    def __call__(self) -> float:
        self.now += 1.0  # every line is a second apart, so none is throttled
        return self.now


def _manager(stream, **kwargs):
    requests = []
    notifications = []

    def opener(request, timeout):
        requests.append((request.full_url, json.loads(request.data), timeout))
        return stream

    manager = PullManager("http://localhost:11434/", MODELS, opener=opener, clock=_Clock(), **kwargs)
    manager.set_notifier(lambda method, params: notifications.append((method, params)))
    return manager, requests, notifications


def test_a_download_streams_through_ollama_and_reports_progress_across_all_layers():
    manager, requests, notifications = _manager(_Stream(_pull_lines(("sha256:aaaa1", 1000), ("sha256:bbbb2", 3000))))

    assert manager.start("qwen3.5:4b") == {"started": True, "model": "qwen3.5:4b"}
    manager.wait(5)

    url, body, _ = requests[0]
    assert url == "http://localhost:11434/api/pull"
    assert body == {"model": "qwen3.5:4b", "stream": True}
    progress = [params for method, params in notifications if method == "ollama.pullProgress"]
    assert all(p["completed"] <= p["total"] or p["total"] == 0 for p in progress)
    assert any(p["total"] == 4000 and p["completed"] == 2000 for p in progress)
    assert progress[-1]["status"] == "success"
    assert progress[-1]["completed"] == progress[-1]["total"] == 4000
    assert notifications[-1] == ("ollama.pullFinished", {"model": "qwen3.5:4b", "outcome": "completed"})
    assert manager.snapshot()["active"] is False
    assert manager.snapshot()["status"] == "completed"


def test_progress_notifications_are_throttled():
    clock = SimpleNamespace(now=0.0)
    notifications = []
    manager = PullManager(
        "http://localhost:11434",
        MODELS,
        opener=lambda request, timeout: _Stream(_pull_lines(("sha256:aaaa1", 1000))),
        clock=lambda: clock.now,  # time never moves: only the first line and the final one may be sent
    )
    manager.set_notifier(lambda method, params: notifications.append(method))

    manager.start("qwen3.5:0.8b")
    manager.wait(5)

    assert notifications.count("ollama.pullProgress") == 2  # the first, and the final success
    assert notifications[-1] == "ollama.pullFinished"


def test_on_success_the_total_is_complete_even_when_small_layers_never_report_completion():
    """Ollama's small manifest layers carry a total but no final completed count."""

    lines = [
        {"status": "pulling aaaa", "digest": "sha256:aaaa1", "total": 1000, "completed": 1000},
        {"status": "pulling bbbb", "digest": "sha256:bbbb2", "total": 321},
        {"status": "success"},
    ]
    manager, _, notifications = _manager(_Stream(lines))

    manager.start("qwen3.5:0.8b")
    manager.wait(5)

    last = [params for method, params in notifications if method == "ollama.pullProgress"][-1]
    assert (last["completed"], last["total"], last["status"]) == (1321, 1321, "success")


@pytest.mark.parametrize("tag", ["llama3.1:8b", "qwen3.5:9b ", "QWEN3.5:9B", "qwen3.5", "", "../../etc/passwd", "qwen3.5:9b;rm", "hf.co/x/y"])
def test_only_an_exact_catalog_tag_can_be_downloaded(tag):
    manager, requests, _ = _manager(_Stream([]))

    with pytest.raises(ValueError, match="not one JARVIS offers"):
        manager.start(tag)

    assert requests == []


def test_only_one_download_runs_at_a_time():
    manager, _, _ = _manager(_Stream([]))
    gate = threading.Event()
    manager._opener = lambda request, timeout: _Stream([{"status": "pulling manifest"}], hold=lambda line: gate.wait(5))

    manager.start("qwen3.5:2b")
    with pytest.raises(ValueError, match="already downloading"):
        manager.start("qwen3.5:4b")
    gate.set()
    manager.wait(5)

    assert manager.start("qwen3.5:4b")["started"] is True  # free again once it ended
    manager.wait(5)


def test_a_download_whose_thread_cannot_start_does_not_block_later_downloads(monkeypatch):
    """Engineering Reviewer finding (WP3c, Medium): `active` must not stay true
    when the worker thread never ran."""

    manager, _, _ = _manager(_Stream(_pull_lines(("sha256:aaaa1", 10))))
    real_start = threading.Thread.start

    def failing_start(self):
        if self.name == "jarvis-ollama-pull":
            raise RuntimeError("can't start new thread")
        real_start(self)

    monkeypatch.setattr(threading.Thread, "start", failing_start)
    with pytest.raises(RuntimeError, match="can't start new thread"):
        manager.start("qwen3.5:2b")

    assert manager.snapshot()["active"] is False
    monkeypatch.setattr(threading.Thread, "start", real_start)
    assert manager.start("qwen3.5:2b")["started"] is True
    manager.wait(5)
    assert manager.snapshot()["status"] == "completed"


def test_a_download_can_be_cancelled_and_says_so():
    gate = threading.Event()
    seen = []

    def hold(line):
        seen.append(line)
        if len(seen) == 2:
            gate.set()
            manager.cancel()

    lines = _pull_lines(("sha256:aaaa1", 1000))
    manager, _, notifications = _manager(_Stream(lines, hold=hold))

    manager.start("qwen3.5:2b")
    manager.wait(5)

    assert manager.snapshot()["status"] == "cancelled"
    assert notifications[-1] == ("ollama.pullFinished", {"model": "qwen3.5:2b", "outcome": "cancelled"})
    assert len(seen) < len(lines)


def test_cancelling_with_nothing_running_is_a_no_op():
    manager, _, _ = _manager(_Stream([]))

    assert manager.cancel() is False


def test_an_error_from_ollama_ends_the_download_without_passing_its_words_on(caplog):
    manager, _, notifications = _manager(_Stream([{"status": "pulling manifest"}, {"error": "secret path C:/Users/x"}]))

    manager.start("qwen3.5:2b")
    manager.wait(5)

    assert notifications[-1] == ("ollama.pullFinished", {"model": "qwen3.5:2b", "outcome": "failed"})
    assert "secret" not in repr(notifications)
    assert "secret" not in caplog.text


def test_a_connection_failure_ends_the_download_as_failed(caplog):
    notifications = []
    manager = PullManager(
        "http://localhost:11434", MODELS, opener=lambda request, timeout: (_ for _ in ()).throw(urllib.error.URLError("refused"))
    )
    manager.set_notifier(lambda method, params: notifications.append((method, params)))

    manager.start("qwen3.5:2b")
    manager.wait(5)

    assert notifications == [("ollama.pullFinished", {"model": "qwen3.5:2b", "outcome": "failed"})]
    assert manager.snapshot()["active"] is False
    assert "URLError" in caplog.text


def test_a_stream_that_ends_without_success_is_a_failure():
    manager, _, notifications = _manager(_Stream([{"status": "pulling manifest"}]))

    manager.start("qwen3.5:2b")
    manager.wait(5)

    assert notifications[-1][1]["outcome"] == "failed"


def test_not_enough_disk_refuses_before_downloading_anything():
    manager, requests, _ = _manager(_Stream([]), disk_free=lambda: 2 * GIB)

    with pytest.raises(ValueError, match="not enough free disk space"):
        manager.start("qwen3.5:9b")

    assert requests == []
    assert manager.snapshot()["active"] is False


def test_unknown_free_disk_does_not_block_a_download():
    manager, _, _ = _manager(_Stream(_pull_lines(("sha256:aaaa1", 10))), disk_free=lambda: None)

    manager.start("qwen3.5:0.8b")
    manager.wait(5)

    assert manager.snapshot()["status"] == "completed"


def test_a_notification_that_cannot_be_written_does_not_break_the_download():
    manager = PullManager(
        "http://localhost:11434", MODELS, opener=lambda r, timeout: _Stream(_pull_lines(("sha256:aaaa1", 10))), clock=_Clock()
    )
    sent = []
    manager.set_notifier(lambda method, params: sent.append(method))

    manager.start("qwen3.5:0.8b")
    manager.wait(5)

    assert sent[-1] == "ollama.pullFinished"


# --- the RPC methods and who may use them --------------------------------------------------------------------------


def _server(tmp_path, *, opener=None, http=None):
    setup = _setup(tmp_path, http=http or _Http(models=("qwen3.5:2b", "qwen3.5:4b")), opener=opener)
    runtime = GuardianRuntime(ollama_setup=setup)
    server = StdioRpcServer(runtime, identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")))
    return server, setup


def _call(server, method, **params):
    return server.handle_line(json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}))


def _as(server, role):
    created = _call(server, "profile.create", displayName="P", role=role)["result"]
    _call(server, "profile.select", profileId=created["id"])


def test_status_and_recommendation_are_readable_by_any_profile_including_a_child(tmp_path):
    server, _ = _server(tmp_path)
    _as(server, "Child")

    status = _call(server, "ollama.status")["result"]
    recommendation = _call(server, "ollama.recommendation")["result"]

    assert status["running"] is True
    assert status["pull"]["active"] is False
    assert recommendation["primary"]["tag"] == "qwen3.5:4b"


@pytest.mark.parametrize("role", ["Child", "Guest"])
@pytest.mark.parametrize(
    ("method", "params"),
    [("ollama.pull", {"model": "qwen3.5:4b"}), ("ollama.cancelPull", {}), ("ollama.useModel", {"model": "qwen3.5:4b"})],
)
def test_a_child_or_guest_cannot_download_cancel_or_change_the_model(tmp_path, role, method, params):
    opened = []
    server, setup = _server(tmp_path, opener=lambda *a, **k: opened.append(a))
    _as(server, role)

    response = _call(server, method, **params)

    assert "Only an Administrator or Adult" in response["error"]["message"]
    assert opened == []
    assert setup.choice.source == "default"


@pytest.mark.parametrize(
    ("method", "params"),
    [("ollama.pull", {"model": "qwen3.5:4b"}), ("ollama.cancelPull", {}), ("ollama.useModel", {"model": "qwen3.5:4b"})],
)
def test_with_no_profile_selected_nothing_can_be_changed(tmp_path, method, params):
    server, _ = _server(tmp_path)

    assert "Select a profile" in _call(server, method, **params)["error"]["message"]


@pytest.mark.parametrize("role", ["Administrator", "Adult"])
def test_an_administrator_or_adult_can_download_and_choose(tmp_path, role):
    server, setup = _server(tmp_path, opener=lambda request, timeout: _Stream(_pull_lines(("sha256:aaaa1", 10))))
    _as(server, role)

    started = _call(server, "ollama.pull", model="qwen3.5:4b")["result"]
    setup.pulls.wait(5)
    chosen = _call(server, "ollama.useModel", model="qwen3.5:4b")["result"]

    assert started == {"started": True, "model": "qwen3.5:4b"}
    assert chosen == {"activeModel": "qwen3.5:4b", "modelSource": "saved"}
    assert _call(server, "ollama.pullStatus")["result"]["status"] == "completed"
    assert _call(server, "ollama.cancelPull")["result"] == {"cancelled": False}


def test_a_model_outside_the_catalog_cannot_be_pulled_or_chosen_over_rpc(tmp_path):
    server, _ = _server(tmp_path)
    _as(server, "Administrator")

    for method in ("ollama.pull", "ollama.useModel"):
        assert "not one JARVIS offers" in _call(server, method, model="llama3.1:8b")["error"]["message"]
        assert "must be a string" in _call(server, method, model=5)["error"]["message"]


def test_download_progress_reaches_the_client_as_notifications(tmp_path):
    server, setup = _server(tmp_path, opener=lambda request, timeout: _Stream(_pull_lines(("sha256:aaaa1", 10))))
    server._notification_stream = io.StringIO()
    _as(server, "Administrator")

    _call(server, "ollama.pull", model="qwen3.5:0.8b")
    setup.pulls.wait(5)

    lines = [json.loads(line) for line in server._notification_stream.getvalue().splitlines()]
    assert all("id" not in line and line["jsonrpc"] == "2.0" for line in lines)
    assert lines[-1] == {"jsonrpc": "2.0", "method": "ollama.pullFinished", "params": {"model": "qwen3.5:0.8b", "outcome": "completed"}}


def test_without_a_running_server_loop_notifications_are_dropped_not_errors(tmp_path):
    server, setup = _server(tmp_path, opener=lambda request, timeout: _Stream(_pull_lines(("sha256:aaaa1", 10))))
    _as(server, "Administrator")

    _call(server, "ollama.pull", model="qwen3.5:0.8b")
    setup.pulls.wait(5)

    assert setup.pulls.snapshot()["status"] == "completed"


def test_a_runtime_built_without_setup_says_so(tmp_path):
    server = StdioRpcServer(GuardianRuntime(), identity_service=ProfileService(ProfileStore(tmp_path / "p.db")))

    assert "not available" in _call(server, "ollama.status")["error"]["message"]
