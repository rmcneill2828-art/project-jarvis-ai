# EIP-ESR0030-001 - Sponsor Approval Service Implementation

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0030-001 |
| Artefact ID | EIP-ESR0030-001 |
| Title | Sponsor Approval Service Implementation |
| Version | 1.5 |
| Status | Approved-implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0084) |
| Intended Session | ESR-0030 |
| Effective Date | 19 July 2026 |

---

# Current Status (as of v1.4, ESR-0030 WP2)

**Section 9 item 4's Sponsor-side deployment acceptance is now satisfied.** Sections 2, 3, 4.7, 5 item 7, and 9 item 4 below were written at WP1 (v0.1-v1.1), when only the code and local (`127.0.0.1`) verification existed - they correctly describe *that* state and are left unedited as the historical record of what WP1 actually delivered, per this project's practice of not silently rewriting past sections. Since then, the Programme Sponsor has deployed the service behind a real Tailscale address, holds `AIEMS_SPONSOR_TOKEN` exclusively on a genuinely separate second device (Android/Termux), and a real cross-device approval has been independently fetched and accepted by `submit-response` with zero Engineering Implementer involvement in the approval action. **EBG-0084 is Complete in full** (`EBR-0001` v1.104) - not merely code-complete. See Version History entry 1.4 for the full evidence. Wherever the sections below say deployment "remains pending" or "future", read that as accurate for WP1's own scope, superseded by this note.

---

# 2. Purpose

Implement the code the architecture [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]] decided but deliberately did not build: a remote Sponsor Approval Service replacing `scripts/aiems_bridge.py`'s file-based `sponsor-decision` command, closing the self-approval gap confirmed at ESR-0029 WP5 - no code path in any agent-accessible environment may set `programme_sponsor_authorisation: true`. **This package delivers the code and its local verification only.** ADR-0022 Decision item 6 additionally requires the service actually run on the Programme Sponsor's own trusted host behind a private Tailscale address - that is a Sponsor-owned deployment step this package cannot perform (Section 4.7) and does not claim to. EBG-0084's implementation half is therefore only fully Complete once both this package's code is implemented *and* the Sponsor-side deployment acceptance in Section 9 item 4 is confirmed - this package moves EBG-0084 from Approved Backlog to a new, narrower "Code Complete, deployment pending Programme Sponsor acceptance" state, not to Complete outright.

---

# 3. Related Backlog Item

`EBG-0084` (`EBR-0001`), decision half Complete via ADR-0022, implementation half Approved Backlog. This package delivers the code half of that implementation - the service, `sponsor_client.py`, the `aiems_bridge.py` diff, and local (`127.0.0.1`) end-to-end verification - per ADR-0022 Section 6 (Consequences), items covering the service/client/bridge diff. It does **not** deliver ADR-0022 Decision item 6 (actual Tailscale/trusted-host deployment), which remains a separate, Sponsor-owned follow-up step, checkable per Section 9 item 4, before EBG-0084 can be marked Complete in full.

---

# 4. Repository Context and Investigation Findings

## 4.1 Current implementation, read directly

`cmd_sponsor_decision` (`scripts/aiems_bridge.py:375-401`) is a plain function with an `argparse` subparser (`sponsor-decision`), gated by nothing beyond convention - any process with repository access can invoke it. It writes only to the Work Package's local transcript file via `append_transcript`, no inbox/outbox routing. `cmd_submit_response` (`:404-468`) already correctly implements the two properties ADR-0022 requires be preserved: reads the transcript's most recent `sponsor-decision` via `find_latest_sponsor_decision`, refuses unless it approves, and refuses unless `capture_repository_ref(repo_root) == decision.repository_ref` - both checks run inside `work_package_lock`, closing the TOCTOU window an earlier Engineering Reviewer finding identified (EIP-ESR0025-001).

## 4.2 What must change, precisely

Per ADR-0022 Decision items 1-3 and 8: `cmd_sponsor_decision` and its subparser are deleted entirely; `cmd_submit_response`'s approval/drift checks move from reading the local transcript to fetching from the new service, with the checks' own logic (approve-only, exact-ref-match) unchanged; `submit-to-review`/`return-findings` and the transcript file itself are untouched - only the `sponsor-decision` handover type disappears from local files. Concretely, `find_latest_sponsor_decision` and the `Handover.type == "sponsor-decision"` filtering become dead code once no caller ever writes that type locally again, and should be deleted rather than left unreachable.

## 4.3 Dependency choice: stdlib only, not `requests`

ADR-0022 Section 6 disclosed `requests` as an anticipated new dependency for the client side. Investigation found this is not necessary: Python's stdlib `urllib.request` (client-side HTTP) and `http.server.ThreadingHTTPServer` plus `sqlite3` (server-side) cover every capability this package needs - a two-route JSON-over-HTTPS-or-plain-HTTP service with token auth and durable append-only persistence. This package proposes stdlib-only, adding **zero new dependencies**, an improvement on the ADR's own anticipated consequence, not a deviation from any binding requirement (the ADR names `requests` only as a disclosed possibility in Consequences, not a Decision item).

## 4.4 Token comparison

`hmac.compare_digest` is used for every token comparison (both routes) to avoid a timing side-channel on the equality check - a cheap, standard hardening not explicitly required by ADR-0022 but consistent with this project's existing security-conscious precedent (`sentinel/`'s policy checks, the bridge's own path-traversal closure) and directly relevant given this service's entire purpose is an auth boundary.

## 4.5 Persistence

A local SQLite database (stdlib `sqlite3`), append-only (no `UPDATE`/`DELETE` code path in the service), one row per decision, matching the durability property of today's transcript file (Decision item 5). Default path `.aiems-exchange/sponsor_decisions.db` (already-gitignored directory), overridable via `AIEMS_SPONSOR_DB_PATH` so the database can live on genuinely separate storage if the service is later moved to different hardware than the agent's own machine.

## 4.6 Environment variables

`AIEMS_AGENT_TOKEN` (agent-side, read-only capability), `AIEMS_SPONSOR_TOKEN` (host-side only, write capability, must never exist in any agent-reachable environment), `AIEMS_SPONSOR_URL` (both sides, the service's address - a private Tailscale address once deployed, `http://127.0.0.1:<port>` for local development/testing). Prefixed with `AIEMS_` rather than the ADR's own shorthand (`AGENT_TOKEN`/`SPONSOR_TOKEN`/`SPONSOR_URL`) to avoid collision with unrelated environment variables of the same generic name on the Sponsor's machine - a naming refinement, not a scope change.

## 4.7 Deployment is explicitly out of this package's authority

ADR-0022 Decision item 6 requires the service run on "the Programme Sponsor's own trusted host, reachable only via a private Tailscale address." The Engineering Implementer has no access to the Programme Sponsor's Tailscale network or any host the Sponsor designates as trusted - this package builds and tests the code, and documents how to start it and put it behind Tailscale (`tailscale serve`), but actually running it long-term, keeping it available, and rotating tokens is a Programme Sponsor operational responsibility, not something this package can complete on the Sponsor's behalf. Live end-to-end verification (Section 9) is therefore performed against `127.0.0.1` as a stand-in for the eventual Tailscale address, not against a real tailnet.

## 4.8 Bootstrapping this package's own approval

The service does not exist until this package is implemented, so this package's own Programme Sponsor approval (WP1 of ESR-0030) must still use the existing `sponsor-decision` command - the last time it is ever used. From the commit that implements this package onward, `submit-response` against the new service becomes the real gate for every subsequent Work Package this session and beyond, per ADR-0022 Decision item 7.

---

# 5. Scope

This package authorises:

1. `scripts/sponsor_approval_service.py` (new): an HTTP service (stdlib `http.server.ThreadingHTTPServer`) exposing exactly two routes:
   - `GET /decisions/latest?session=...&work_package=...` - requires `Authorization: Bearer <token>` matching `AIEMS_AGENT_TOKEN` (via `hmac.compare_digest`); returns the latest decision record for that Work Package as JSON, or a null-decision response if none exists. Structurally incapable of writing - no code path in the GET handler touches the database beyond a `SELECT`.
   - `POST /decisions` - requires `Authorization: Bearer <token>` matching `AIEMS_SPONSOR_TOKEN`; body `{"session", "work_package", "decision" ("approve"|"reject"), "repository_ref", "note"}`; inserts one durable row. The only route that can create a decision record - `AIEMS_AGENT_TOKEN` is never accepted here even if presented.
   - Any other/missing/malformed token on either route: `401`/`403` as appropriate, no partial information leaked.
2. SQLite-backed durable persistence (`.aiems-exchange/sponsor_decisions.db` default, `AIEMS_SPONSOR_DB_PATH` overridable), append-only.
3. `scripts/sponsor_client.py` (new): a host-side CLI the Programme Sponsor runs manually (`python scripts/sponsor_client.py <session> <work_package> --decision approve|reject --note "..."`), reading `AIEMS_SPONSOR_TOKEN`/`AIEMS_SPONSOR_URL` from environment, auto-capturing `repository_ref` via local `git rev-parse HEAD` (matching `cmd_sponsor_decision`'s existing behaviour), POSTing to the service.
4. `scripts/aiems_bridge.py` diff:
   - Delete `cmd_sponsor_decision`, its `argparse` subparser, `find_latest_sponsor_decision`, and the now-dead `Handover.type == "sponsor-decision"` handling.
   - Add `fetch_latest_decision(session, work_package) -> DecisionRecord | None`, using `urllib.request` against `AIEMS_SPONSOR_URL`/`AIEMS_AGENT_TOKEN`, with a bounded timeout; raises `BridgeError` on any failure (connection refused, timeout, non-2xx status, malformed JSON) - fail-closed, never a silent fallback (Decision item 4).
   - Modify `cmd_submit_response` to call `fetch_latest_decision` in place of `find_latest_sponsor_decision(read_transcript(...))`, preserving the approve-only check and the exact-repository-ref-match drift check unchanged in substance, still inside `work_package_lock`.
5. Test coverage: `scripts/tests/test_sponsor_approval_service.py` (new, real socket-based tests against the service on an ephemeral localhost port), `scripts/tests/test_sponsor_client.py` (new, mocked HTTP call), and `scripts/tests/test_aiems_bridge.py` rewritten where it currently exercises `cmd_sponsor_decision`/transcript-based approval to instead inject a fake `fetch_latest_decision`, preserving every existing behavioural case (refused without decision, refused after rejection, succeeds after approval with matching ref, refused on drift, succeeds after fresh decision clears drift, refused when validation failed, TOCTOU-lock coverage) plus a new fail-closed-when-unreachable case.
6. A short operator note (in this EIP's own Constraints/Consequences, not a new controlled artefact) on starting the service and exposing it via `tailscale serve`.
7. Record delivery against `EBG-0084` in `EBR-0001` as **code implementation Complete, Tailscale deployment pending Programme Sponsor acceptance** - not Complete in full, per Section 9 item 4.

---

# 6. Authorised Files

1. `scripts/sponsor_approval_service.py` (new)
2. `scripts/sponsor_client.py` (new)
3. `scripts/aiems_bridge.py`
4. `scripts/tests/test_sponsor_approval_service.py` (new)
5. `scripts/tests/test_sponsor_client.py` (new)
6. `scripts/tests/test_aiems_bridge.py`
7. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
8. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`
9. `.gitignore` (adding the SQLite database path if not already covered by the existing `.aiems-exchange/` exclusion)

No `jarvis/` or `src/` files - this package is AIEMS tooling, not product code. No new third-party dependency (Section 4.3).

---

# 7. Implementation Requirements

1. Every token comparison uses `hmac.compare_digest`, never `==`, on both routes.
2. `AIEMS_SPONSOR_TOKEN` must never be read, logged, or written by any code path other than the service's own POST-route auth check and `sponsor_client.py`'s own request construction - it must not appear in `aiems_bridge.py` or any agent-facing code at all.
3. The GET route's handler must have no code path that can reach the database's write logic, even if `AIEMS_SPONSOR_TOKEN` is presented to it - structural incapability, not a conditional check, mirroring `return-findings`' existing "no file-path argument" property.
4. `fetch_latest_decision` must raise `BridgeError` (not return `None`, not retry silently) on: connection refused, timeout, any non-2xx HTTP status, or a response body that fails to parse as the expected JSON shape.
5. `cmd_submit_response`'s refusal messages must remain at least as specific as today's (distinguish "no approving decision", "repository drifted", "validation failed") plus a new distinct message for "service unreachable."
6. The SQLite schema must have no `UPDATE`/`DELETE` statement anywhere in the service - append-only, matching the transcript file's own durability property.
7. `sponsor_client.py` must refuse to run (clear error, not a stack trace) if `AIEMS_SPONSOR_TOKEN` or `AIEMS_SPONSOR_URL` is unset, rather than sending a request with a missing/blank token.
8. No behavioural change to `submit-to-review`, `return-findings`, `init`, the transcript file format, or the repository-ref drift check's underlying comparison logic.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Actually deploying the service behind a real Tailscale address, keeping it running, or any Programme Sponsor-side infrastructure/credential provisioning - the Programme Sponsor's own operational responsibility (Section 4.7).
2. TLS/HTTPS termination for the service itself - it is designed to sit behind Tailscale's own private network boundary (per ADR-0022 Decision item 6), not to be its own hardened internet-facing endpoint. If the Programme Sponsor later exposes it more broadly (e.g. `tailscale funnel`), that is a separate, future decision requiring its own review.
3. Any change to `cmd_init`, `cmd_submit_to_review`, `cmd_return_findings`, the transcript file format, or the Work Package locking mechanism.
4. Multi-Sponsor or multi-token support (a single `AIEMS_SPONSOR_TOKEN`/`AIEMS_AGENT_TOKEN` pair is in scope; per-user tokens are a future extension if ever needed).
5. A UI, dashboard, or any way to view decision history other than direct SQLite inspection or the existing transcript (`submit-response` still appends its own record to the transcript once validated, per ADR-0022 Decision item 8 - unchanged).

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status, via the existing `sponsor-decision` command (the last use of it, per Section 4.8).
2. Live end-to-end verification, against `127.0.0.1` (Section 4.7), must cover: agent-side `GET` succeeding with a valid `AIEMS_AGENT_TOKEN`; `GET` failing with a missing/wrong token; `POST` succeeding with a valid `AIEMS_SPONSOR_TOKEN` via `sponsor_client.py`; `POST` failing (403) if presented `AIEMS_AGENT_TOKEN` instead; `submit-response` correctly refusing when no decision exists, when the decision rejects, when the repository has drifted, and when the service is stopped (fail-closed); `submit-response` succeeding once a matching approval exists.
3. From this package's own implementing commit onward, the Engineering Implementer commits to using `submit-response` against a real running instance of the service (initially local, per item 4) as the actual gate before every subsequent commit this session (ADR-0022 Decision item 7) - not reverting to reading the transcript directly.
4. **Sponsor-Side Deployment Acceptance (prerequisite to marking EBG-0084 Complete in full, distinct from this package's own code-complete state)**: this package's own commit records EBG-0084 as code-implementation Complete only. Full closure additionally requires the Programme Sponsor to confirm, in a future session or a direct instruction: (a) the service is genuinely running behind a private Tailscale address, not merely `127.0.0.1`; (b) `AIEMS_SPONSOR_TOKEN`/`AIEMS_AGENT_TOKEN` have been set to real, non-development values, with the sponsor token held only on the Sponsor's own host; (c) a real agent-side `GET` against the Tailscale address succeeds from the actual environment agents run in. Until that confirmation, `AIEMS_SPONSOR_URL` in any environment agents use should continue pointing at a local development instance (per item 3) - this package does not require or assume Tailscale deployment has happened by the time it is implemented.

---

# 10. Validation

```powershell
python -m pytest
python scripts/validate_repository.py
```

1. All existing and new tests pass.
2. Live verification per Section 9 item 2.
3. `validate_repository.py` 0 errors.
4. `npm run build` not required - no frontend files touched.

---

# 11. Risks and Dependencies

No new third-party dependency (Section 4.3). Risks:

1. **A locally-run service is not yet the real Tailscale deployment** - the code and its auth/persistence properties are fully verifiable locally, but genuine network-boundary security (private-address-only reachability) depends on the Programme Sponsor's own Tailscale setup, which this package cannot verify. Disclosed, not hidden, per Section 4.7 and Explicit Exclusion 1.
2. **A single shared token pair is a simpler trust model than per-agent tokens** - acceptable at current scale (one Programme Sponsor, one Engineering Implementer, one Engineering Reviewer, none of whom currently need distinct revocable credentials), but would need revisiting if the project ever has multiple distinct agent identities needing independently revocable access.
3. **Operational discipline risk carried over from ADR-0022 Decision item 7 itself**: the service closes the *code-level* self-approval gap, but only if `submit-response` is actually, consistently used going forward - a repeat of ESR-0029's own finding (a correct gate existing but not being the practiced path) remains possible if this requirement is not honoured in future sessions. Mitigated by Section 9 item 3's explicit commitment, checkable in future session review.

---

# 12. Approval Request

Requesting Engineering Reviewer (Codex) pre-implementation design review via the AIEMS Exchange Bridge, then Programme Sponsor approval via the existing `sponsor-decision` command (the last invocation of it).

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]] | Approved decision this package implements in full - code (WP1) and Decision item 6's Tailscale deployment, confirmed by the Programme Sponsor at WP2 (Section 9 item 4, satisfied - see Current Status above). |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0084 Complete in full as of ESR-0030 WP2 - code and Sponsor-side deployment acceptance both delivered. |
| [[EIP-ESR0025-001_AIEMS_EXCHANGE_BRIDGE_MVP|EIP-ESR0025-001]] | Original bridge implementation this package amends; its three post-implementation findings are the precedent for this bridge's security properties needing adversarial review. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.5 | 19 July 2026 | Claude Engineering Implementer | Addressed an Engineering Reviewer Low finding on v1.4: the version history recorded Section 9 item 4's satisfaction, but the document body still repeatedly read as if deployment were future/pending (Sections 2, 3, 4.7, 5 item 7, 9 item 4, Related Artefacts), with nothing distinguishing WP1-era text from the now-superseded state. Added a "Current Status" note directly after Document Control, pointing at the v1.4 history entry and explicitly stating the WP1-era sections below are left unedited as historical record, not current claims. Updated the two Related Artefacts rows (a live reference table, not historical narrative) to reflect current state directly. |
| 1.4 | 19 July 2026 | Claude Engineering Implementer | Section 9 item 4's Sponsor-side deployment acceptance confirmed at ESR-0030 WP2: the Programme Sponsor installed Tailscale on the service host and a genuinely separate second device (Android/Termux), generated and held `AIEMS_SPONSOR_TOKEN` exclusively, started the service themselves with real tokens, and exposed it via `tailscale serve` at a real tailnet address. Live end-to-end confirmed with genuine separation: a real Sponsor-originated approval from the separate device was independently fetched and accepted by `submit-response` with zero Engineering Implementer involvement in the approval action - exceeding this section's own bar (which only required the Engineering Implementer's `GET` to succeed). EBG-0084 marked Complete in full in EBR-0001 (1.103 to 1.104). |
| 1.3 | 19 July 2026 | Claude Engineering Implementer | Addressed an Engineering Reviewer follow-up Low finding on v1.2's fix: `fetch_latest_decision` correctly rejected non-dict payloads but still accepted any dict with `decision: null` regardless of the other three fields - a dict with `repository_ref` unexpectedly non-null, or with only `decision: null` and the other keys missing entirely, was still treated as a genuine absence of approval. Fixed to require all three other fields (`repository_ref`, `timestamp`, `note`) both present in the payload and explicitly null, matching `sponsor_approval_service.py`'s actual emitted shape exactly - a field missing via `.get()`'s default is no longer indistinguishable from one explicitly set to null. 4 new tests; 338 tests total (was 334). |
| 1.2 | 19 July 2026 | Claude Engineering Implementer | Addressed two Engineering Reviewer post-commit findings on the implemented code. Medium: `--host` accepted any value including `0.0.0.0`, letting the service bind to every interface despite the module's own stated loopback-only boundary - fixed with a new `_is_safe_bind_host` check (using `ipaddress.ip_address(...).is_loopback`, plus the `localhost` literal) enforced inside `build_server` itself, refusing any non-loopback bind before the socket is ever opened. Low: `fetch_latest_decision` treated any non-dict JSON payload the same as a genuine `{"decision": null, ...}` response, losing the distinct malformed-response signal the EIP required - fixed by raising `BridgeError` for any non-dict payload before checking `decision`, so only a real dict-shaped null-decision reply is treated as "no decision yet." 19 new tests added (host-safety validation, and fetch_latest_decision's own JSON-handling exercised directly via a mocked `urlopen` rather than only through the monkeypatched-away fixture used elsewhere in the bridge test file); 334 tests total (was 315). |
| 1.1 | 19 July 2026 | Claude Engineering Implementer | Implemented exactly as scoped: `scripts/sponsor_approval_service.py` (new, stdlib-only), `scripts/sponsor_client.py` (new), and the `scripts/aiems_bridge.py` diff (`cmd_sponsor_decision`/`find_latest_sponsor_decision` deleted, `cmd_submit_response` now calls `fetch_latest_decision`, fail-closed). 21 new tests (13 service, 8 client) plus the bridge test file rewritten to inject a fake decision; 315 tests total (was 295). Live end-to-end verified against a real running instance on `127.0.0.1` per Section 9 item 2, all six cases. A real connection-draining bug was found and fixed during this verification: `do_POST` returned an auth-failure response without first reading the client's already-sent request body, leaving unread socket bytes that intermittently caused a client-side connection reset under the full test suite - fixed by draining the body unconditionally before any early return, regardless of auth outcome. EBG-0084 recorded as code-complete, Tailscale deployment pending Programme Sponsor acceptance (Section 9 item 4) - not Complete in full. Status Approved to Approved-implemented. |
| 1.0 | 19 July 2026 | Claude Engineering Implementer | Approved by the Programme Sponsor via the bridge (`sponsor-decision`, `repository_ref: 09a95243c4bd5e3bd78d9c354ecaba10dcebca8c`, 19 July 2026 19:00:47Z), following Engineering Reviewer (Codex) confirmation: Pass, no findings on v0.2 - the overclaim finding resolved, technical design sound. Status promoted Draft to Approved. This is the last use of `sponsor-decision`; the service this package builds replaces it. |
| 0.2 | 19 July 2026 | Claude Engineering Implementer | Addressed an Engineering Reviewer Medium finding: v0.1 overclaimed full ADR-0022/EBG-0084 closure (Sections 2, 3, 5 item 7, 13) while explicitly excluding actual Tailscale deployment (Decision item 6) as outside the Engineering Implementer's authority (Section 4.7) - an internal inconsistency. Narrowed every closure claim throughout to "code implementation Complete, Tailscale deployment pending Programme Sponsor acceptance," and added Section 9 item 4 defining a checkable Sponsor-side deployment-acceptance step as the actual prerequisite to marking EBG-0084 Complete in full. No scope, file list, or technical design change - wording/claim-accuracy only. |
| 0.1 | 19 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0030 WP1, implementing ADR-0022 in full: stdlib-only (no new dependency) HTTP service with SQLite persistence, `sponsor_client.py`, and the `aiems_bridge.py` diff replacing transcript-based sponsor-decision with a fetch from the new service. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
