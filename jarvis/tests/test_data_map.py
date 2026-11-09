"""The data map lists every store and destination in the code (ESR-0062 WP5,
EIP-ESR0062-005 L2).

`docs/user/DATA_MAP.md` is the source for the user guide, the parents' guide
and the public "Children and privacy" page. This test fails when the code gains
a table, a column, a file or folder name, or an internet address that the map
does not mention, so a new store or destination cannot ship unlisted.

Not scanned, by design: writes through `open(`, `write_text` or
`sqlite3.connect` with a computed path (the real-run check, B1, lists every
file written); plain `http://` addresses, which in this code are the same
computer or the household's own network (Ollama, Home Assistant) and are
otherwise test fixtures; and `scripts/`, which the installed app does not run
apart from its own entry point. Matches are by name: a name in the map
counts, wherever it appears there.
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA_MAP = (REPO / "docs" / "user" / "DATA_MAP.md").read_text(encoding="utf-8")

TABLE = re.compile(r"CREATE TABLE (?:IF NOT EXISTS )?(\w+)\s*\(", re.IGNORECASE)
COLUMN = re.compile(r"ALTER TABLE \w+ ADD COLUMN (\w+)", re.IGNORECASE)
NAME_CONSTANT = re.compile(r"^[A-Z_]+_(?:FILENAME|DIRNAME)\s*=\s*\"([^\"]+)\"", re.MULTILINE)
HOME_PATH = re.compile(r"Path\.home\(\)((?:\s*/\s*\"[^\"]+\")+)")
HOST = re.compile(r"https://([A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,})")


def _sources(*roots, suffixes=(".py",)):
    for root in roots:
        for path in sorted((REPO / root).rglob("*")):
            if path.suffix in suffixes and "tests" not in path.relative_to(REPO).parts:
                yield path, path.read_text(encoding="utf-8")


def _found(pattern, *roots, suffixes=(".py",)):
    return {match for _, text in _sources(*roots, suffixes=suffixes) for match in pattern.findall(text)}


def _tables():
    return _found(TABLE, "jarvis", "sentinel")


def _columns():
    return _found(COLUMN, "jarvis", "sentinel")


def _names():
    names = _found(NAME_CONSTANT, "jarvis", "sentinel")
    for joined in _found(HOME_PATH, "jarvis", "sentinel"):
        names.update(part for part in re.findall(r"\"([^\"]+)\"", joined) if part != ".jarvis")
    return names


def _hosts():
    return (
        _found(HOST, "jarvis", "sentinel", suffixes=(".py",))
        | _found(HOST, "src-tauri/src", suffixes=(".rs",))
        | _found(HOST, "src", suffixes=(".js", ".jsx"))
    )


def test_the_scan_still_finds_what_is_known_to_be_there():
    # If the patterns stop matching, the checks below would pass vacuously.
    assert {"profiles", "personal_memory", "safety_events", "spend"} <= _tables()
    assert {"profile_id", "share_memory_with_cloud"} <= _columns()
    assert {"audit.jsonl", "personal.db", "profiles.db", "models"} <= _names()
    assert {"api.anthropic.com", "github.com", "huggingface.co"} <= _hosts()


def test_every_table_is_in_the_map():
    missing = sorted(name for name in _tables() if f"`{name}`" not in DATA_MAP)
    assert not missing, f"Tables not in docs/user/DATA_MAP.md: {missing}"


def test_every_added_column_is_in_the_map():
    missing = sorted(name for name in _columns() if f"`{name}`" not in DATA_MAP)
    assert not missing, f"Columns not in docs/user/DATA_MAP.md: {missing}"


def test_every_file_and_folder_name_is_in_the_map():
    missing = sorted(name for name in _names() if name not in DATA_MAP)
    assert not missing, f"File or folder names not in docs/user/DATA_MAP.md: {missing}"


def test_every_internet_address_is_in_the_map():
    missing = sorted(host for host in _hosts() if host not in DATA_MAP)
    assert not missing, f"Internet addresses not in docs/user/DATA_MAP.md: {missing}"
