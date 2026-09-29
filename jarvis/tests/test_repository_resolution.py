"""Tests for EBG-0148 (ESR-0059 WP11): repository-reading capabilities in an
installation with no source repository - the packaged sidecar."""

import json
from pathlib import Path

import pytest

from jarvis import repository
from jarvis.gia.engineering_observability import EngineeringStateObserver
from jarvis.identity.service import ProfileService
from jarvis.identity.store import ProfileStore
from jarvis.interfaces import knowledge_graph
from jarvis.interfaces.stdio_rpc import StdioRpcServer, build_default_runtime
from jarvis.repository import (
    UNAVAILABLE_MESSAGE,
    RepositoryUnavailableError,
    resolve_repository_root,
)

REAL_CHECKOUT = Path(__file__).resolve().parents[2]


@pytest.fixture
def packaged_install(tmp_path, monkeypatch):
    """Simulate the PyInstaller sidecar: the code's own directory is not a
    checkout, and no JARVIS_REPOSITORY_ROOT is set."""

    extracted = tmp_path / "_MEI12345"
    extracted.mkdir()
    monkeypatch.setattr(repository, "_PACKAGE_CHECKOUT", extracted)
    monkeypatch.delenv("JARVIS_REPOSITORY_ROOT", raising=False)
    return extracted


def test_resolves_this_packages_own_checkout_by_default(monkeypatch):
    monkeypatch.delenv("JARVIS_REPOSITORY_ROOT", raising=False)

    assert resolve_repository_root() == REAL_CHECKOUT


def test_environment_variable_points_at_a_checkout(packaged_install):
    assert resolve_repository_root({"JARVIS_REPOSITORY_ROOT": str(REAL_CHECKOUT)}) == REAL_CHECKOUT


def test_no_checkout_raises_a_path_free_error(packaged_install):
    with pytest.raises(RepositoryUnavailableError) as raised:
        resolve_repository_root()

    assert str(raised.value) == UNAVAILABLE_MESSAGE
    assert str(packaged_install) not in str(raised.value)
    assert "JARVIS_REPOSITORY_ROOT" in str(raised.value)


def test_environment_variable_pointing_at_a_non_checkout_is_unavailable(tmp_path):
    with pytest.raises(RepositoryUnavailableError):
        resolve_repository_root({"JARVIS_REPOSITORY_ROOT": str(tmp_path)})


def test_knowledge_graph_is_unavailable_not_a_raw_git_error(packaged_install):
    with pytest.raises(RepositoryUnavailableError, match="No JARVIS source repository"):
        knowledge_graph.build_graph()


def test_engineering_status_is_unavailable_not_a_raw_git_error(packaged_install):
    with pytest.raises(RepositoryUnavailableError, match="No JARVIS source repository"):
        EngineeringStateObserver().snapshot()


def test_git_failure_inside_a_checkout_is_reported_without_paths(tmp_path, monkeypatch):
    import subprocess

    fake_checkout = tmp_path / "checkout"
    (fake_checkout / ".git").mkdir(parents=True)

    def failing_run(*args, **kwargs):
        raise subprocess.CalledProcessError(128, ["git", "ls-files", str(fake_checkout)])

    monkeypatch.setattr(knowledge_graph.subprocess, "run", failing_run)

    with pytest.raises(RepositoryUnavailableError) as raised:
        knowledge_graph.build_graph(fake_checkout)

    assert str(fake_checkout) not in str(raised.value)


def test_rpc_methods_report_unavailability_cleanly_in_a_packaged_install(packaged_install, tmp_path):
    server = StdioRpcServer(
        build_default_runtime(
            environ={"JARVIS_OLLAMA_ENDPOINT": "http://127.0.0.1:1", "JARVIS_MEMORY_DB_PATH": str(tmp_path / "personal.db")}
        ),
        identity_service=ProfileService(ProfileStore(tmp_path / "profiles.db")),
    )

    for request_id, method in enumerate(("knowledge.graph", "gia.engineeringStatus"), start=1):
        response = server.handle_line(json.dumps({"jsonrpc": "2.0", "id": request_id, "method": method, "params": {}}))
        message = response["error"]["message"]
        assert message == f"RepositoryUnavailableError: {UNAVAILABLE_MESSAGE}"
        assert "_MEI" not in message
        assert "CalledProcessError" not in message


def test_setting_the_environment_variable_restores_both_capabilities(packaged_install, monkeypatch):
    monkeypatch.setenv("JARVIS_REPOSITORY_ROOT", str(REAL_CHECKOUT))

    graph = knowledge_graph.build_graph()
    snapshot = EngineeringStateObserver().snapshot()

    assert len(graph["nodes"]) > 0
    assert snapshot.git_branch


# The packaged-build interpreter and stdin findings (ESR-0059 WP11).


def test_from_source_scripts_run_with_the_current_interpreter(monkeypatch):
    import sys

    from jarvis.gia import engineering_observability

    monkeypatch.delattr(sys, "frozen", raising=False)

    assert engineering_observability._script_interpreter() == sys.executable


def test_packaged_build_never_runs_scripts_with_its_own_executable(monkeypatch):
    """In a PyInstaller build sys.executable is the backend itself - using it
    started a second backend that could read the RPC stream."""

    import sys

    from jarvis.gia import engineering_observability

    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(engineering_observability.shutil, "which", lambda name: f"C:/Python/{name}.exe")

    assert engineering_observability._script_interpreter() == "C:/Python/python.exe"
    assert engineering_observability._script_interpreter() != sys.executable


def test_packaged_build_without_python_reports_it(monkeypatch):
    import sys

    from jarvis.gia import engineering_observability

    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(engineering_observability.shutil, "which", lambda name: None)

    with pytest.raises(RepositoryUnavailableError, match="needs a Python interpreter"):
        engineering_observability._script_interpreter()


def test_no_child_process_can_read_the_rpc_request_stream(monkeypatch):
    """Every subprocess the backend starts must have stdin closed: the
    backend's own stdin is the JSON-RPC request stream."""

    import subprocess

    from jarvis.gia import engineering_observability

    calls: list[dict] = []

    def recording_run(args, **kwargs):
        calls.append(kwargs)
        if args[0] == "git" and "ls-files" in args:
            return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
        if args[0] == "git":
            return subprocess.CompletedProcess(args, 0, stdout="main\n", stderr="")
        return subprocess.CompletedProcess(args, 0, stdout="Repository validation passed: 0 errors, 1 warning(s).", stderr="")

    monkeypatch.setattr(subprocess, "run", recording_run)
    reader = engineering_observability.RealEngineeringStateReader()
    reader.branch()
    reader.repository_validation()
    knowledge_graph.build_graph(REAL_CHECKOUT)

    assert len(calls) == 3
    assert all(call.get("stdin") is subprocess.DEVNULL for call in calls)


def test_validation_timeout_is_a_clear_error(monkeypatch):
    import subprocess

    from jarvis.gia import engineering_observability

    def slow_run(args, **kwargs):
        raise subprocess.TimeoutExpired(args, kwargs.get("timeout"))

    monkeypatch.setattr(subprocess, "run", slow_run)
    reader = engineering_observability.RealEngineeringStateReader()

    with pytest.raises(RuntimeError, match="did not finish within 120s"):
        reader.repository_validation()
