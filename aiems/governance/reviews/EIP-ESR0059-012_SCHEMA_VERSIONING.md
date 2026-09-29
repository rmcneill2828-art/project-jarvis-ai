# EIP-ESR0059-012 - SQLite Schema Versioning

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | EIP-ESR0059-012 |
| Title | Engineering Implementation Package: WP12 SQLite Schema Versioning |
| Version | 1.0 |
| Status | Approved - implemented |
| Session | ESR-0059 |
| Work Package | WP12 |

---

# 2. Purpose

Implements ESR-0059 WP12, resolving [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0147, under the Programme Sponsor's standing instruction to continue with the backlog.

`PersonalMemoryStore` and `ProfileStore` created their tables with `CREATE TABLE IF NOT EXISTS` and recorded no schema version, so there was no safe way to change a table on an existing installation. EBG-0132 (profile-scoped memory) needs exactly that - a new column on `personal_memory` - so this is its prerequisite.

---

# 3. Repository Context Investigated

* Both stores' `__init__` - two `CREATE TABLE IF NOT EXISTS` statements each, via `_transaction()`.
* Python's `sqlite3` module (default `isolation_level`) opens a transaction implicitly only before `INSERT`/`UPDATE`/`DELETE`/`REPLACE` - not before DDL or `PRAGMA` - so a multi-statement schema change is not atomic unless a transaction is opened explicitly.
* The development machine's real stores (`~/.jarvis/memory/personal.db`, `~/.jarvis/identity/profiles.db`) exist and are empty.

---

# 4. Scope

## 4A. Migration helper (`jarvis/shared/schema_migrations.py`, new)

* A store declares an ordered, append-only tuple of migrations; migration N brings the schema to version N, recorded in `PRAGMA user_version`.
* `apply_migrations()` runs every pending migration in one explicit `BEGIN IMMEDIATE` transaction (write lock taken up front, so two processes cannot both migrate), rolling back entirely on any failure - DDL included.
* A database already at a higher version than the code knows is refused with `SchemaVersionError` ("... newer than this version of JARVIS supports ... Update JARVIS before opening it.") and left untouched, so an older app can never write to a schema it does not understand.

## 4B. Both stores

* `PERSONAL_MEMORY_MIGRATIONS` and `PROFILE_MIGRATIONS`: migration 1 is each store's original schema, SQL text unchanged, `IF NOT EXISTS` - so existing installations (tables present, `user_version` 0) are upgraded to version 1 with no data change.

## 4C. Test isolation - a real defect found during this package's live check

The live check upgrades *copies* of the real stores. It found the real `~/.jarvis/memory/personal.db` and `~/.jarvis/identity/profiles.db` already modified minutes earlier and already at version 1. Running the full suite against a fake home directory, then each test individually, identified five test call sites that opened the real home-directory stores by omission:

* `test_stdio_rpc.py` - two GIA serialisation tests calling `build_default_runtime()` with no environment (since ESR-0029), and the Home Assistant RPC test (since ESR-0058 WP4) constructing `StdioRpcServer` without an isolated profile store;
* `test_activity_tracker.py` (since ESR-0051);
* `test_audit_and_logging.py` - this session's own WP9 test.

Before WP12, opening a store on an existing database was a read-only no-op, so the leak did no harm. After WP12, opening records the schema version - a write - so it is fixed in this package rather than deferred:

* All five call sites now pass explicit temporary paths.
* New `jarvis/tests/conftest.py`: an autouse fixture points every home-directory default the backend uses (`DEFAULT_MEMORY_DB_PATH`, `DEFAULT_MEMORY_BACKUP_DIR`, `DEFAULT_IDENTITY_DB_PATH`) at the test's temporary directory and clears the related environment variables, so no future test can touch real data by omission.
* Verified: the full suite run against a fake home directory now creates **zero** files there (previously both databases).
* **Disclosed effect on the real data**: both real stores had already been stamped `user_version = 1` by leaking test runs during this session. That is the correct version for their unchanged schema, both are empty, and no data was changed or lost.

## 4D. Tests

New `jarvis/tests/test_schema_migrations.py` (8): new stores created at the latest version; an unversioned pre-WP12 database with data upgraded without loss; reopening changes nothing; a newer-version database refused and left untouched; pending migrations applied in order; a failing migration rolls back everything including DDL; released migrations pinned.

## 4E. Explicitly out of scope

* Any schema change itself - EBG-0132 will be the first real migration 2.
* Down-migrations.
* Other SQLite files (none in the product today).

## 4F. Review

**Review - disclosed self-review** (GitHub Copilot CLI quota re-probed, still exhausted; EBG-0153 applies). Checked: migration 1's SQL is character-for-character the original schema, so existing databases see no change beyond the version stamp; the only f-string SQL is the `PRAGMA user_version` value, an integer computed from the migration count, never user input; `BEGIN IMMEDIATE` plus rollback on `BaseException` covers interrupted startups; the conftest guard patches module defaults rather than `Path.home()`, which the defaults are computed from at import time; every test still passes with it in place. No further change needed.

---

# 5. Validation Requirements

* `python -m pytest -q`, `ruff check .`, `python scripts/validate_repository.py`.
* The full suite against a fake home directory: no files created there.
* **Live check**: copies of the real memory and profile databases opened with the new stores - row counts identical before and after, version 1; originals not written by the check itself.

---

# 6. Completion Report Requirements

Standard PBK-0001 completion report: summary, files modified, validation performed, self-review findings, observations, outstanding issues, commit SHA/message/repository status once authorised.

---

# 7. Success Criteria

* Both stores record and advance a schema version, atomically.
* Existing installations upgrade with no data change.
* A newer database is refused, never altered.
* No test can touch the real home-directory stores.
* All validation in Section 5 passes.

---

# 8. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 29 September 2026 | Claude Engineering Implementer | **Programme Sponsor approved via direct chat instruction ("Approved")** on the disclosed self-review. Implemented exactly as at v0.2. Pending commit/push through `submit-response`. |
| 0.2 | 29 September 2026 | Claude Engineering Implementer | Disclosed self-review recorded in Section 4F (Copilot CLI quota still exhausted). Retrospective Copilot review owed (EBG-0153). Not yet approved or committed. |
| 0.1 | 29 September 2026 | Claude Engineering Implementer | ESR-0059 WP12 draft. Append-only, atomic `user_version` migrations for both stores, refusing newer databases. Real test-isolation defect found by the live check - five call sites touching the real home-directory stores, one from this session's WP9 - fixed, plus an autouse conftest guard; suite now creates zero files in a fake home. pytest 729 passed/1 skipped, ruff clean. Not yet reviewed, approved or committed. |
