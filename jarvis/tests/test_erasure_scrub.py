"""Erased and deleted data leaves no readable copy in the database files
(ESR-0062 WP5, EIP-ESR0062-005 B2).

Before this, SQLite marked a deleted row's space as free without overwriting
it: after a profile erasure the note text and the profile's name were still
in the raw bytes of `personal.db` and `profiles.db`, with no row holding them.
"""

import sqlite3

from jarvis.shared.schema_migrations import connect, scrub
from jarvis.tests.test_profile_data_rights import World

NOTE = "Quillon keeps a spare key under the blue flowerpot."
NAME = "Quillonette"


def _raw(path):
    """Every byte of the database and any write-ahead log beside it."""

    data = b""
    for candidate in (path, path.with_name(path.name + "-wal")):
        if candidate.exists():
            data += candidate.read_bytes()
    return data


def _household(tmp_path):
    w = World(tmp_path)
    w.make("Robert", "Administrator")
    w.make(NAME, "Adult")
    w.use(NAME)
    w.save_note(NOTE)
    w.use("Robert")
    return w


def test_every_connection_overwrites_deleted_data(tmp_path):
    connection = connect(tmp_path / "x.db")
    try:
        assert connection.execute("PRAGMA secure_delete").fetchone()[0] == 1
    finally:
        connection.close()


def test_after_erasure_neither_file_holds_the_note_or_the_name(tmp_path):
    w = _household(tmp_path)
    assert NOTE.encode() in _raw(tmp_path / "personal.db")

    w.result("profile.erase", profileId=w.ids[NAME], confirmName=NAME)

    assert NOTE.encode() not in _raw(tmp_path / "personal.db")
    assert NAME.encode() not in _raw(tmp_path / "profiles.db")


def test_after_deleting_a_note_the_file_does_not_hold_it(tmp_path):
    w = _household(tmp_path)
    w.use(NAME)
    record = next(r for r in w.result("memory.list")["records"] if r["content"] == NOTE)

    w.result("memory.delete", recordId=record["id"])

    assert NOTE.encode() not in _raw(tmp_path / "personal.db")


def test_scrub_also_clears_what_was_deleted_before_overwriting_was_on(tmp_path):
    # An installation from before this change: rows deleted without secure_delete.
    path = tmp_path / "old.db"
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA secure_delete = OFF")
    connection.execute("CREATE TABLE t (v TEXT)")
    connection.executemany("INSERT INTO t VALUES (?)", [(f"keep {i}",) for i in range(50)] + [(NOTE,)])
    connection.commit()
    connection.execute("DELETE FROM t WHERE v = ?", (NOTE,))
    connection.commit()
    connection.close()
    assert NOTE.encode() in _raw(path)

    assert scrub(path) is True

    assert NOTE.encode() not in _raw(path)
    connection = sqlite3.connect(path)
    try:
        assert connection.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 50
    finally:
        connection.close()
