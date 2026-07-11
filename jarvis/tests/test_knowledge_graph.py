"""Tests for the repository knowledge-graph builder (EBG-0055 Phase 1)."""

import subprocess
from pathlib import Path

from jarvis.interfaces import knowledge_graph


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _init_repo(repo: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)


def _commit_all(repo: Path) -> None:
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "test"], cwd=repo, check=True)


def test_build_graph_basic_nodes_and_edges(tmp_path):
    _init_repo(tmp_path)
    _write(tmp_path / "A.md", "# Artefact A\n\nSee [[B]] for detail.\n")
    _write(tmp_path / "B.md", "# Artefact B\n\nNo outgoing links.\n")
    _commit_all(tmp_path)

    graph = knowledge_graph.build_graph(repo_root=tmp_path)

    assert {node["id"] for node in graph["nodes"]} == {"A.md", "B.md"}
    assert {"source": "A.md", "target": "B.md"} in graph["edges"]


def test_alias_link_uses_target_not_alias_text(tmp_path):
    _init_repo(tmp_path)
    _write(tmp_path / "A.md", "# A\n\nSee [[B|a friendlier name]].\n")
    _write(tmp_path / "B.md", "# B\n")
    _commit_all(tmp_path)

    graph = knowledge_graph.build_graph(repo_root=tmp_path)

    assert {"source": "A.md", "target": "B.md"} in graph["edges"]


def test_duplicate_links_deduplicated_to_one_edge(tmp_path):
    _init_repo(tmp_path)
    _write(tmp_path / "A.md", "# A\n\n[[B]] and again [[B]] and once more [[B|B again]].\n")
    _write(tmp_path / "B.md", "# B\n")
    _commit_all(tmp_path)

    graph = knowledge_graph.build_graph(repo_root=tmp_path)

    matches = [edge for edge in graph["edges"] if edge == {"source": "A.md", "target": "B.md"}]
    assert len(matches) == 1


def test_malformed_links_are_skipped(tmp_path):
    _init_repo(tmp_path)
    _write(tmp_path / "A.md", "# A\n\n[[]] and [[|no target]] produce no edges.\n")
    _write(tmp_path / "B.md", "# B\n")
    _commit_all(tmp_path)

    graph = knowledge_graph.build_graph(repo_root=tmp_path)

    assert graph["edges"] == []


def test_self_link_produces_no_self_edge(tmp_path):
    _init_repo(tmp_path)
    _write(tmp_path / "A.md", "# A\n\nSelf reference [[A]].\n")
    _commit_all(tmp_path)

    graph = knowledge_graph.build_graph(repo_root=tmp_path)

    assert graph["edges"] == []


def test_unresolved_link_dropped_not_errored(tmp_path):
    _init_repo(tmp_path)
    _write(tmp_path / "A.md", "# A\n\nSee [[NOPE]] which does not exist.\n")
    _commit_all(tmp_path)

    graph = knowledge_graph.build_graph(repo_root=tmp_path)

    assert graph["edges"] == []
    assert len(graph["nodes"]) == 1


def test_label_falls_back_to_stem_when_no_heading(tmp_path):
    _init_repo(tmp_path)
    _write(tmp_path / "NOHEADING.md", "Just text, no heading.\n")
    _commit_all(tmp_path)

    graph = knowledge_graph.build_graph(repo_root=tmp_path)

    assert graph["nodes"] == [{"id": "NOHEADING.md", "label": "NOHEADING", "cluster": "root"}]


def test_cluster_derived_from_top_level_directory(tmp_path):
    _init_repo(tmp_path)
    _write(tmp_path / "docs" / "GUIDE.md", "# Guide\n")
    _write(tmp_path / "aiems" / "governance" / "X.md", "# X\n")
    _commit_all(tmp_path)

    graph = knowledge_graph.build_graph(repo_root=tmp_path)
    by_id = {node["id"]: node for node in graph["nodes"]}

    assert by_id["docs/GUIDE.md"]["cluster"] == "docs"
    assert by_id["aiems/governance/X.md"]["cluster"] == "aiems/governance"


def test_ambiguous_stem_resolves_to_shallowest_file(tmp_path):
    """Guards a real edge case found in this repository: three git-tracked
    README.md files (root, scripts/, logs/chats/) share the stem "README",
    and dozens of existing [[README|README]] links all clearly mean the
    root one - a bare-stem node id would collide all three into one node."""

    _init_repo(tmp_path)
    _write(tmp_path / "README.md", "# Root Readme\n")
    _write(tmp_path / "scripts" / "README.md", "# Scripts Readme\n")
    _write(tmp_path / "logs" / "chats" / "README.md", "# Chats Readme\n")
    _write(tmp_path / "CALLER.md", "# Caller\n\nSee [[README|README]].\n")
    _commit_all(tmp_path)

    graph = knowledge_graph.build_graph(repo_root=tmp_path)

    node_ids = {node["id"] for node in graph["nodes"]}
    assert node_ids == {"README.md", "scripts/README.md", "logs/chats/README.md", "CALLER.md"}
    assert {"source": "CALLER.md", "target": "README.md"} in graph["edges"]
    assert {"source": "CALLER.md", "target": "scripts/README.md"} not in graph["edges"]
    assert {"source": "CALLER.md", "target": "logs/chats/README.md"} not in graph["edges"]


def test_repo_root_resolution_is_independent_of_process_cwd(tmp_path, monkeypatch):
    """Guards the Engineering Reviewer's High finding: the Tauri sidecar
    spawns Python without setting a working directory (src-tauri/src/lib.rs),
    so REPO_ROOT must not depend on os.getcwd()."""

    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)

    assert (knowledge_graph.REPO_ROOT / "aiems").is_dir()
    assert (knowledge_graph.REPO_ROOT / "jarvis" / "interfaces" / "knowledge_graph.py").is_file()


def test_build_graph_uses_explicit_repo_root_not_process_cwd(tmp_path, monkeypatch):
    """Non-blocking recommendation from the Reviewer's re-review: confirms
    build_graph works from a non-root working directory."""

    repo = tmp_path / "repo"
    repo.mkdir()
    _init_repo(repo)
    _write(repo / "A.md", "# A\n")
    _commit_all(repo)

    somewhere_else = tmp_path / "somewhere_else"
    somewhere_else.mkdir()
    monkeypatch.chdir(somewhere_else)

    graph = knowledge_graph.build_graph(repo_root=repo)

    assert graph["nodes"] == [{"id": "A.md", "label": "A", "cluster": "root"}]
