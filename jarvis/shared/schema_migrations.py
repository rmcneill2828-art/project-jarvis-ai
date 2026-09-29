"""SQLite schema versioning for JARVIS's local stores (EBG-0147, ESR-0059 WP12).

The Personal Memory and profile stores used to create their tables with
`CREATE TABLE IF NOT EXISTS` and record no schema version, so there was no
safe way to change a table on an existing installation - the prerequisite
EBG-0132 (profile-scoped memory) needs, since it adds a column.

Each store now declares an ordered list of migrations. A migration is a
tuple of SQL statements; migration N brings the schema to version N, and the
database's `PRAGMA user_version` records the version it has reached.
`apply_migrations()` runs every pending migration in one `BEGIN IMMEDIATE`
transaction - taken explicitly, because Python's `sqlite3` module does not
open a transaction before DDL or PRAGMA statements on its own - so a
failure leaves the database exactly as it was.

Migration 1 of each store is its original schema, written with `IF NOT
EXISTS`, so it is safe on the existing installations that already have those
tables at `user_version` 0. A database from a newer JARVIS - a version this
code does not know - is refused rather than opened, so an older app can
never write to a schema it does not understand.
"""

from __future__ import annotations

import sqlite3
from collections.abc import Sequence
from pathlib import Path

Migration = Sequence[str]


class SchemaVersionError(RuntimeError):
    """The database was created by a newer JARVIS than this one."""


def schema_version(db_path: Path) -> int:
    """Return the database's recorded schema version (0 if never versioned)."""

    connection = sqlite3.connect(db_path)
    try:
        return int(connection.execute("PRAGMA user_version").fetchone()[0])
    finally:
        connection.close()


def apply_migrations(db_path: Path, migrations: Sequence[Migration], store_name: str) -> int:
    """Bring the database at `db_path` up to `len(migrations)`; return the
    resulting version.

    Raises `SchemaVersionError` if the database is already at a higher
    version than this code knows about. All pending migrations apply in a
    single transaction, or none do.
    """

    latest = len(migrations)
    connection = sqlite3.connect(db_path, isolation_level=None)
    try:
        # IMMEDIATE takes the write lock up front, so two processes opening
        # the same store cannot both decide to run the same migration.
        connection.execute("BEGIN IMMEDIATE")
        try:
            current = int(connection.execute("PRAGMA user_version").fetchone()[0])
            if current > latest:
                msg = (
                    f"The {store_name} database is at schema version {current}, newer than this "
                    f"version of JARVIS supports ({latest}). Update JARVIS before opening it."
                )
                raise SchemaVersionError(msg)
            for version in range(current + 1, latest + 1):
                for statement in migrations[version - 1]:
                    connection.execute(statement)
            if current != latest:
                # PRAGMA does not accept bound parameters; `latest` is an int
                # computed here, never user input.
                connection.execute(f"PRAGMA user_version = {latest:d}")
            connection.execute("COMMIT")
        except BaseException:
            connection.execute("ROLLBACK")
            raise
        return latest
    finally:
        connection.close()
