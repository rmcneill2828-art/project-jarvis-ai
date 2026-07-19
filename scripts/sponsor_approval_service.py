"""Sponsor Approval Service (ADR-0022, EIP-ESR0030-001).

A minimal HTTP service replacing scripts/aiems_bridge.py's file-based
sponsor-decision command. Exposes exactly two routes:

- GET /decisions/latest?session=...&work_package=... - AIEMS_AGENT_TOKEN
  gated, read-only, returns the latest decision for a Work Package or a
  null decision if none exists. The handler has no code path that reaches
  the store's write method, regardless of what token is presented -
  structural incapability, not a conditional check, mirroring
  aiems_bridge.py's return-findings own "no file-path argument to exploit"
  property.
- POST /decisions - AIEMS_SPONSOR_TOKEN gated, the only route that can
  create a decision record.

Runs on the Programme Sponsor's own trusted host, bound to 127.0.0.1 by
default - never 0.0.0.0 - and reachable to agents only via a private
Tailscale address (`tailscale serve`), never the open internet (ADR-0022
Decision item 6). Deploying it behind Tailscale and keeping it running is
a Programme Sponsor operational responsibility, not something this module
performs for itself (EIP-ESR0030-001 Section 4.7 / Section 9 item 4).
"""

from __future__ import annotations

import argparse
import contextlib
import hmac
import ipaddress
import json
import os
import re
import sqlite3
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterator
from urllib.parse import parse_qs, urlsplit

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = REPO_ROOT / ".aiems-exchange" / "sponsor_decisions.db"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765

# Mirrors aiems_bridge.py's own _IDENTIFIER_PATTERN - session/work_package
# feed directly into a SQL WHERE clause (parameterised, so not an injection
# risk by itself) and are validated here anyway for the same shape
# discipline as the bridge's own path-building functions.
_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")
_VALID_DECISIONS = ("approve", "reject")


class ServiceError(RuntimeError):
    """Raised for expected service failures (missing configuration)."""


@dataclass(frozen=True)
class DecisionRecord:
    session: str
    work_package: str
    decision: str
    repository_ref: str
    note: str
    timestamp: str


class DecisionStore:
    """SQLite-backed, append-only store for Sponsor Approval decisions.

    No UPDATE/DELETE statement exists anywhere in this class - append-only,
    matching the transcript file's own durability property (ADR-0022
    Decision item 5). Mirrors jarvis/memory/store.py's connection-per-
    transaction pattern: sqlite3.Connection's own context manager only
    commits/rolls back, it never closes the connection, so every
    transaction opens and explicitly closes its own connection rather than
    leaking a file handle (the exact bug found and fixed in that module).
    """

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._transaction() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session TEXT NOT NULL,
                    work_package TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    repository_ref TEXT NOT NULL,
                    note TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    @contextlib.contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self._connect()
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def record(self, decision: DecisionRecord) -> DecisionRecord:
        with self._transaction() as connection:
            connection.execute(
                """
                INSERT INTO decisions
                    (session, work_package, decision, repository_ref, note, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    decision.session,
                    decision.work_package,
                    decision.decision,
                    decision.repository_ref,
                    decision.note,
                    decision.timestamp,
                ),
            )
        return decision

    def latest(self, session: str, work_package: str) -> DecisionRecord | None:
        """Return the most recent decision for a Work Package, or None."""

        with self._transaction() as connection:
            row = connection.execute(
                """
                SELECT session, work_package, decision, repository_ref, note, timestamp
                FROM decisions
                WHERE session = ? AND work_package = ?
                ORDER BY id DESC LIMIT 1
                """,
                (session, work_package),
            ).fetchone()
        if row is None:
            return None
        return DecisionRecord(
            session=row[0],
            work_package=row[1],
            decision=row[2],
            repository_ref=row[3],
            note=row[4],
            timestamp=row[5],
        )


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _valid_identifier(value: object) -> bool:
    return isinstance(value, str) and bool(_IDENTIFIER_PATTERN.fullmatch(value))


def _extract_bearer_token(handler: BaseHTTPRequestHandler) -> str | None:
    header = handler.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    token = header[len("Bearer ") :].strip()
    return token or None


def build_handler_class(
    store: DecisionStore, agent_token: str, sponsor_token: str
) -> type[BaseHTTPRequestHandler]:
    """Build a request handler bound to this store and these tokens.

    do_GET never calls store.record - only store.latest - so the read
    route is structurally incapable of writing regardless of which token
    is presented (Implementation Requirement 3).
    """

    class Handler(BaseHTTPRequestHandler):
        server_version = "SponsorApprovalService/1.0"

        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            pass  # not a diagnostics endpoint; silence default stderr access log

        def _send_json(self, status: int, payload: dict) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            parts = urlsplit(self.path)
            if parts.path != "/decisions/latest":
                self._send_json(404, {"error": "not found"})
                return

            token = _extract_bearer_token(self)
            if token is None:
                self._send_json(401, {"error": "missing bearer token"})
                return
            if not hmac.compare_digest(token, agent_token):
                self._send_json(403, {"error": "forbidden"})
                return

            query = parse_qs(parts.query)
            session = (query.get("session") or [""])[0]
            work_package = (query.get("work_package") or [""])[0]
            if not _valid_identifier(session) or not _valid_identifier(work_package):
                self._send_json(400, {"error": "invalid session/work_package"})
                return

            decision = store.latest(session, work_package)
            if decision is None:
                self._send_json(
                    200,
                    {"decision": None, "repository_ref": None, "timestamp": None, "note": None},
                )
                return
            self._send_json(
                200,
                {
                    "decision": decision.decision,
                    "repository_ref": decision.repository_ref,
                    "timestamp": decision.timestamp,
                    "note": decision.note,
                },
            )

        def do_POST(self) -> None:  # noqa: N802
            # The request body is drained unconditionally, before any check
            # that might return early - leaving Content-Length bytes unread
            # on the socket when responding early (e.g. an auth failure)
            # left the connection in an inconsistent state, causing an
            # intermittent client-side connection reset under load (found
            # via this package's own test suite, not a hypothetical).
            length = int(self.headers.get("Content-Length", "0") or "0")
            raw_body = self.rfile.read(length) if length else b""

            parts = urlsplit(self.path)
            if parts.path != "/decisions":
                self._send_json(404, {"error": "not found"})
                return

            token = _extract_bearer_token(self)
            if token is None:
                self._send_json(401, {"error": "missing bearer token"})
                return
            if not hmac.compare_digest(token, sponsor_token):
                self._send_json(403, {"error": "forbidden"})
                return

            try:
                payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
            except (json.JSONDecodeError, UnicodeDecodeError):
                self._send_json(400, {"error": "malformed JSON body"})
                return
            if not isinstance(payload, dict):
                self._send_json(400, {"error": "malformed JSON body"})
                return

            session = payload.get("session", "")
            work_package = payload.get("work_package", "")
            decision_value = payload.get("decision", "")
            repository_ref = payload.get("repository_ref", "")
            note = payload.get("note", "")

            if not _valid_identifier(session) or not _valid_identifier(work_package):
                self._send_json(400, {"error": "invalid session/work_package"})
                return
            if decision_value not in _VALID_DECISIONS:
                self._send_json(400, {"error": "decision must be 'approve' or 'reject'"})
                return
            if not isinstance(repository_ref, str) or not repository_ref.strip():
                self._send_json(400, {"error": "repository_ref must be a non-empty string"})
                return
            if not isinstance(note, str):
                self._send_json(400, {"error": "note must be a string"})
                return

            record = DecisionRecord(
                session=session,
                work_package=work_package,
                decision=decision_value,
                repository_ref=repository_ref,
                note=note,
                timestamp=_now(),
            )
            store.record(record)
            self._send_json(
                201,
                {
                    "session": record.session,
                    "work_package": record.work_package,
                    "decision": record.decision,
                    "repository_ref": record.repository_ref,
                    "timestamp": record.timestamp,
                    "note": record.note,
                },
            )

    return Handler


def _is_safe_bind_host(host: str) -> bool:
    """Reject any bind address that isn't loopback-only.

    This service's entire security model assumes it is reachable only via
    127.0.0.1 directly, or a private Tailscale address forwarded to a
    loopback port by `tailscale serve` - never by binding to a
    publicly/LAN-reachable interface itself (ADR-0022 Decision item 6).
    `--host 0.0.0.0` (or any other non-loopback address) would silently
    expose both routes on every interface, bypassing that boundary
    entirely - an Engineering Reviewer post-commit finding, addressed by
    enforcing this in code rather than only stating it in the docstring.
    """

    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def build_server(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    db_path: Path = DEFAULT_DB_PATH,
    agent_token: str | None = None,
    sponsor_token: str | None = None,
) -> ThreadingHTTPServer:
    """Build and return a bound, not-yet-serving ThreadingHTTPServer.

    Caller is responsible for calling serve_forever()/shutdown() - split
    this way so tests can bind on an ephemeral port, hand the server to a
    background thread, and shut it down deterministically.
    """

    if not _is_safe_bind_host(host):
        msg = (
            f"Refusing to bind to {host!r}: only loopback addresses (127.0.0.1, ::1, "
            "localhost) are permitted. Reach this service from other machines via a "
            "private Tailscale address forwarded with `tailscale serve`, never by "
            "binding directly to a non-loopback interface (ADR-0022 Decision item 6)."
        )
        raise ServiceError(msg)

    resolved_agent_token = agent_token if agent_token is not None else os.environ.get("AIEMS_AGENT_TOKEN")
    resolved_sponsor_token = (
        sponsor_token if sponsor_token is not None else os.environ.get("AIEMS_SPONSOR_TOKEN")
    )
    if not resolved_agent_token or not resolved_sponsor_token:
        msg = "AIEMS_AGENT_TOKEN and AIEMS_SPONSOR_TOKEN must both be set (non-blank)."
        raise ServiceError(msg)

    store = DecisionStore(db_path)
    handler_class = build_handler_class(store, resolved_agent_token, resolved_sponsor_token)
    return ThreadingHTTPServer((host, port), handler_class)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="sponsor_approval_service", description=__doc__)
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument(
        "--db-path",
        type=Path,
        default=Path(os.environ.get("AIEMS_SPONSOR_DB_PATH", str(DEFAULT_DB_PATH))),
    )
    args = parser.parse_args(argv)

    try:
        server = build_server(host=args.host, port=args.port, db_path=args.db_path)
    except ServiceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Sponsor Approval Service listening on {args.host}:{args.port} (db: {args.db_path})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
