"""SQLite concurrency settings for the local stores (ESR-0061 WP2a,
EBG-0157 item 1): WAL journal mode and an explicit busy timeout, so a
conversation turn on the slow lane and a memory write on the main thread can
use the same database at once."""

from __future__ import annotations

import threading

from jarvis.identity.store import ProfileStore
from jarvis.memory.store import PersonalMemoryStore
from jarvis.shared.schema_migrations import BUSY_TIMEOUT_MS, connect


def _journal_mode(db_path) -> str:
    connection = connect(db_path)
    try:
        return connection.execute("PRAGMA journal_mode").fetchone()[0]
    finally:
        connection.close()


def test_memory_store_uses_wal(tmp_path):
    db_path = tmp_path / "memory.db"
    PersonalMemoryStore(db_path)
    assert _journal_mode(db_path) == "wal"


def test_profile_store_uses_wal(tmp_path):
    db_path = tmp_path / "profiles.db"
    ProfileStore(db_path)
    assert _journal_mode(db_path) == "wal"


def test_connections_set_an_explicit_busy_timeout(tmp_path):
    db_path = tmp_path / "memory.db"
    PersonalMemoryStore(db_path)
    connection = connect(db_path)
    try:
        assert connection.execute("PRAGMA busy_timeout").fetchone()[0] == BUSY_TIMEOUT_MS
    finally:
        connection.close()


def test_a_reader_is_not_blocked_by_an_open_write_transaction(tmp_path):
    """Under WAL a reader sees the last committed state while a writer holds
    its transaction open; under the old rollback journal this reader would
    wait on the writer's lock."""

    db_path = tmp_path / "memory.db"
    PersonalMemoryStore(db_path)
    writer = connect(db_path)
    writer.isolation_level = None
    writer.execute("BEGIN IMMEDIATE")
    writer.execute("CREATE TABLE IF NOT EXISTS probe (n INTEGER)")
    writer.execute("INSERT INTO probe VALUES (1)")
    try:
        reader = connect(db_path)
        reader.execute("PRAGMA busy_timeout = 0")  # fail at once rather than wait
        try:
            # The schema and data the writer added are not committed yet,
            # so the reader sees the committed state without blocking.
            tables = {row[0] for row in reader.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            assert "probe" not in tables
        finally:
            reader.close()
    finally:
        writer.execute("ROLLBACK")
        writer.close()


def test_concurrent_threads_read_and_write_without_lock_errors(tmp_path):
    db_path = tmp_path / "memory.db"
    PersonalMemoryStore(db_path)
    setup = connect(db_path)
    setup.execute("CREATE TABLE counter (n INTEGER)")
    setup.commit()
    setup.close()
    errors: list[BaseException] = []

    def write() -> None:
        try:
            for i in range(200):
                connection = connect(db_path)
                with connection:
                    connection.execute("INSERT INTO counter VALUES (?)", (i,))
                connection.close()
        except BaseException as exc:  # noqa: BLE001 - surfaced by the assert below
            errors.append(exc)

    def read() -> None:
        try:
            for _ in range(200):
                connection = connect(db_path)
                connection.execute("SELECT COUNT(*) FROM counter").fetchone()
                connection.close()
        except BaseException as exc:  # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=write), threading.Thread(target=read), threading.Thread(target=read)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert errors == []
    final = connect(db_path)
    assert final.execute("SELECT COUNT(*) FROM counter").fetchone()[0] == 200
    final.close()
