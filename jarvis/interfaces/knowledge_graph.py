"""Repository knowledge-graph builder (EBG-0055 Phase 1 - static live graph).

Parses the repository's git-tracked markdown artefacts and their explicit
`[[Target]]` / `[[Target|Alias]]` WikiLinks into a node/edge graph structure
for the Guardian Orb knowledge-graph rendering direction
([[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8.1),
exposed via the `knowledge.graph` JSON-RPC method (ADR-0019 bridge).

Phase 1 only. Cluster colour semantics (Phase 2), agent-traversal animation
(Phase 3, blocked on GIA telemetry) and the Guardian reasoning connection
(Phase 4) are out of scope - see EBG-0055. The bare trailing-artefact-ID
heuristic used elsewhere for Related-Artefacts-table OSE enrichment
(`scripts/validate_repository.py`) is also out of scope: only bracketed
WikiLinks produce edges here.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

# Anchored to this module's own file location, not the process's working
# directory. The Tauri sidecar spawns Python via `Command::new("python")`
# with no `.current_dir(...)` set (src-tauri/src/lib.rs), so relying on
# `os.getcwd()` or a bare `git rev-parse` from an unknown cwd would be
# brittle depending on how/where the bridge happens to be launched from.
REPO_ROOT = Path(__file__).resolve().parents[2]

WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
HEADING_PATTERN = re.compile(r"(?m)^#\s+(.+)$")


def _tracked_markdown_files(repo_root: Path) -> list[Path]:
    """Enumerate git-tracked markdown files via `git ls-files`, explicitly
    scoped to repo_root regardless of the calling process's cwd. Deliberately
    not a filesystem rglob: this repository's `node_modules/` alone contains
    dozens of untracked README.md files that would otherwise dwarf the
    repository's own ~135-150 real engineering artefacts."""

    result = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=repo_root,
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    return [repo_root / line for line in result.stdout.splitlines() if line]


def _node_id(path: Path, repo_root: Path) -> str:
    """Repo-root-relative posix path. Unique even where basenames collide -
    this repository has three git-tracked README.md files (root, scripts/,
    logs/chats/) - and invariant to heading/prose edits, unlike a label."""

    return path.relative_to(repo_root).as_posix()


def _cluster_for(path: Path, repo_root: Path) -> str:
    """Coarse cluster derived from the file's top-level repository directory -
    a free byproduct of parsing for Phase 1. Phase 2 owns the real
    cluster-illumination semantics (UAM-0001 Section 8.1/8.2)."""

    parts = path.relative_to(repo_root).parts
    if len(parts) == 1:
        return "root"
    if parts[0] == "aiems" and len(parts) > 2:
        return f"aiems/{parts[1]}"
    return parts[0]


def _label_for(text: str, stem: str) -> str:
    """First H1 heading as a cosmetic display label, falling back to the
    file's stem if none is found. Purely cosmetic: edges reference nodes by
    id (_node_id), never by label, so a heading rewrite cannot churn edges."""

    heading = HEADING_PATTERN.search(text)
    return heading.group(1).strip() if heading else stem


def _resolve_stem(stem: str, candidates_by_stem: dict[str, list[Path]], repo_root: Path) -> Path | None:
    """Resolve a bare WikiLink target (e.g. "README") to one tracked file.

    Where more than one tracked file shares a stem, the shallowest path wins
    (fewest path parts, then alphabetical for determinism). This repository
    has dozens of existing `[[README|README]]` links, all of which clearly
    mean the root README.md, not scripts/README.md or logs/chats/README.md.
    `scripts/validate_repository.py`'s own WikiLink check does not
    disambiguate this case either (it only checks stem membership) - this is
    a real pre-existing ambiguity in the repository's WikiLink convention,
    not something introduced by this parser. Returns None if the stem
    matches no tracked file (an unresolved link, dropped by the caller).
    """

    candidates = candidates_by_stem.get(stem)
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    return min(candidates, key=lambda p: (len(p.relative_to(repo_root).parts), p.as_posix()))


def build_graph(repo_root: Path | None = None) -> dict[str, list[dict[str, str]]]:
    """Build the Phase 1 knowledge graph: one node per git-tracked markdown
    artefact, one edge per resolved WikiLink between them.

    Malformed links (`[[]]`, `[[|Alias]]`) never match WIKILINK_PATTERN and
    are silently skipped. Self-links and duplicate links (including the same
    target linked once plainly and once with an alias) are collapsed:
    self-links are dropped, duplicates de-duplicated via the `edges` set.
    Unresolved and ambiguous-but-undecidable targets are dropped rather than
    raised as errors - this function is a best-effort renderer, not a second
    governance gate; `scripts/validate_repository.py` already owns erroring
    on unresolved WikiLinks.
    """

    root = repo_root if repo_root is not None else REPO_ROOT
    files = _tracked_markdown_files(root)

    candidates_by_stem: dict[str, list[Path]] = {}
    for path in files:
        candidates_by_stem.setdefault(path.stem, []).append(path)

    nodes: list[dict[str, str]] = []
    edges: set[tuple[str, str]] = set()

    for path in files:
        source_id = _node_id(path, root)
        text = path.read_text(encoding="utf-8", errors="replace")
        nodes.append(
            {
                "id": source_id,
                "label": _label_for(text, path.stem),
                "cluster": _cluster_for(path, root),
            }
        )

        for match in WIKILINK_PATTERN.finditer(text):
            target_path = _resolve_stem(match.group(1), candidates_by_stem, root)
            if target_path is None:
                continue
            target_id = _node_id(target_path, root)
            if target_id == source_id:
                continue
            edges.add((source_id, target_id))

    return {
        "nodes": nodes,
        "edges": [{"source": source, "target": target} for source, target in sorted(edges)],
    }
