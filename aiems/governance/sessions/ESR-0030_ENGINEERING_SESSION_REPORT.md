# ESR-0030 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0030 |
| Title | Engineering Session Report |
| Version | 1.0 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Session | ESR-0030 |
| Date Opened | 19 July 2026 |
| Date Closed | 19 July 2026 |
| Closure Status | Closed - WP1-WP2 complete, session-wide WP3 Pass, WP4 Retain (RBL-0017 unchanged) |

---

# 2. Purpose

This report records the opening and execution of ESR-0030, run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7: Claude as Engineering Implementer, Codex (ChatGPT) as Engineering Reviewer, Programme Sponsor gating every step.

Continuing directly from ESR-0029, this session ran entirely through the AIEMS Exchange Bridge (`scripts/aiems_bridge.py`) with no manual relay anywhere - the fifth consecutive session run this way, and the first where the approval step itself moved off that bridge's own file-based mechanism onto a genuinely deployed, separately-hosted Sponsor Approval Service.

---

# 3. Scope

ESR-0030 opened with WP0A repository synchronisation, which found and fixed a deferred sync-staleness gap from ESR-0029's own closure (README.md and PBK-0001 still referencing ESR-0026/RBL-0015). The Programme Sponsor then selected the session objective: implement the Sponsor Approval Service ADR-0022 had decided at ESR-0029 but deliberately not built, closing EBG-0084.

WP1 delivered the implementation - a stdlib-only HTTP service, a host-side client, and the `aiems_bridge.py` diff deleting the old file-based approval command entirely - through three rounds of Codex review findings (an EIP-stage overclaim, two post-commit code defects). WP2 then confirmed genuine Sponsor-side deployment: the Programme Sponsor installed Tailscale on both the service host and a truly separate second device (Android, via Termux), held the sponsor token exclusively, and the whole approval chain was proven end to end with real, non-test decisions - closing EBG-0084 in full. Session-wide WP3 Independent Repository Verification and WP4 Repository Baseline Acceptance closed the session, both conducted via the bridge (WP3's own handover needing three rounds of fixes for a recurring self-inflicted WikiLink-syntax defect), converging on retaining the existing baseline.

---

# 4. Engineering Authority

ESR-0030 opening was authorised by Programme Sponsor instruction on 19 July 2026, following repository synchronisation confirming [[ESR-0029_ENGINEERING_SESSION_REPORT|ESR-0029]] was closed and [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] remained the accepted repository baseline at that time.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

One primary objective, selected by the Programme Sponsor at WP0B from a set of `AskUserQuestion` candidates:

- **WP1** - Sponsor Approval Service implementation (EBG-0084), replacing `scripts/aiems_bridge.py`'s file-based `sponsor-decision` command with a remote, genuinely separated approval mechanism, per [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]].
- **WP2** - Confirm real Sponsor-side deployment of that service (not initially part of the WP0B selection as a separate WP, but the natural, expected completion of WP1's own explicit Section 9 item 4 prerequisite).

Both were met by closure, with WP2 additionally proven via two genuine, non-test, cross-device approvals - not merely claimed.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation, deferred sync-staleness fix, session objective selection | Complete - Section 7 |
| WP1 | Sponsor Approval Service implementation (EBG-0084 code half) per EIP-ESR0030-001 | Complete - Section 8 |
| WP2 | Sponsor-side Tailscale deployment confirmation (EBG-0084 complete in full) | Complete - Section 9 |
| Session-wide WP3/WP4 | Independent Repository Verification; Repository Baseline Acceptance | Complete - Pass, RBL-0017 retained - Section 10 |

---

# 7. WP0 Session Initialisation Record

**WP0A - Repository Synchronisation:**

- Repository state verified directly: `main` at `31a2f1c`, confirmed matching `origin/main`.
- Confirmed [[ESR-0029_ENGINEERING_SESSION_REPORT|ESR-0029]] formally closed and [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] the accepted baseline.
- **Found and fixed a deferred sync-staleness gap**, without waiting to be asked twice: README.md and PBK-0001 still referenced ESR-0026/RBL-0015 (three and four sessions stale respectively). Fixed directly during WP0A per its own repository-synchronisation remit, then a further round of Codex-caught staleness (more ESR-0026/RBL-0015 references still present outside the top summary table, plus two separately-stale capability bullets) fixed immediately after. A missing REG-0001 traceability entry for an earlier PBK-0001 version bump was also caught and added.

**WP0B - Engineering Session Initialisation:**

- Active Engineering Session: ESR-0030 (this report, authored at closure per established practice).
- Repository baseline reference at opening: [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] (retained through this session's own WP4).
- Session objective selection presented via `AskUserQuestion`; the Programme Sponsor selected the Sponsor Approval Service implementation from a set of candidates that also included further GIA phases, the remaining Low-severity security hygiene items, and JRM-0001 catch-up (all left for a future session).

---

# 8. WP1 - Sponsor Approval Service Implementation (EBG-0084 Code Half)

Implements the architecture [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]] decided at ESR-0029 but deliberately did not build, per [[EIP-ESR0030-001_SPONSOR_APPROVAL_SERVICE_IMPLEMENTATION|EIP-ESR0030-001]].

**Design review found a genuine internal inconsistency before any code was written**: the initial package claimed full ADR-0022/EBG-0084 closure while simultaneously and correctly excluding actual Tailscale deployment as outside the Engineering Implementer's own authority - fixed by narrowing every closure claim to "code implementation Complete, deployment pending" and adding a checkable Sponsor-side acceptance prerequisite (Section 9 item 4), rather than either overclaiming or silently assuming an authority that does not exist.

**Delivered**: `scripts/sponsor_approval_service.py` (new) - a stdlib-only HTTP service (`http.server.ThreadingHTTPServer`, `sqlite3`, `hmac.compare_digest` token comparison, a structurally write-incapable GET route) exposing exactly two routes matching ADR-0022's Decision items; `scripts/sponsor_client.py` (new) - a host-side CLI auto-capturing `repository_ref` via `git rev-parse HEAD`, never accepting a token as a command-line argument; and the `scripts/aiems_bridge.py` diff deleting `cmd_sponsor_decision`/`find_latest_sponsor_decision` entirely and adding `fetch_latest_decision`, fail-closed on any unreachable/malformed-response case. Zero new third-party dependency - stdlib covers every capability needed, an improvement on ADR-0022's own anticipated `requests` dependency.

**Two rounds of genuine post-commit defects were found and fixed**: an unsafe `--host 0.0.0.0` bind was possible despite the module's own stated loopback-only boundary, fixed with an enforced `_is_safe_bind_host` check; and `fetch_latest_decision`'s malformed-response handling needed two successive fix rounds to fully close - first catching non-dict payloads, then a follow-up catching a dict with `decision: null` but inconsistent or incomplete companion fields, a real case of an initial fix not fully closing what it set out to close.

A genuine connection-draining bug was found and fixed during live verification, not hypothetical: `do_POST` returned auth-failure responses without first draining the client's already-sent request body, intermittently causing a client-side connection reset under the full test suite's load - fixed by reading the body unconditionally before any early return.

- Commit SHAs: `46995e6` (draft), `09a9524` (overclaim fix), `afdd673` (approved - last use of `sponsor-decision`), `fec589a` (implementation), `18e7b6d` (post-commit fix round 1), `3029d3d` (post-commit fix round 2)
- `python -m pytest`: 334 passed by WP1's close (was 295 at ESR-0029's closure). `python scripts/validate_repository.py`: 0 errors, 130 warnings.

---

# 9. WP2 - Sponsor-Side Deployment Confirmation (EBG-0084 Complete in Full)

Confirms ADR-0022 Decision item 6 and EIP-ESR0030-001 Section 9 item 4: the service actually running on the Programme Sponsor's own trusted host behind a private Tailscale address.

**Delivered**: the Programme Sponsor installed Tailscale on both the service host (this PC) and a genuinely separate second device (Android, via Termux), generated and held `AIEMS_SPONSOR_TOKEN` exclusively - never shared with or visible to the Engineering Implementer - started the service themselves from their own terminal session, and exposed it via `tailscale serve` at a real private tailnet address (`https://desktop-ogfkjds.tail266bfe.ts.net`). A downloadable field-reference guide (published as a Claude Artifact, not a controlled repository artefact) was produced covering the day-to-day approval workflow, one-time setup, and known issues.

**Live end-to-end proof, not simulated**: the Engineering Implementer's own agent-side `GET` succeeded against the real deployed instance using only `AIEMS_AGENT_TOKEN`. Separately, the Programme Sponsor recorded two genuine, non-test approval decisions from the separate Android device - first a direct test, then two real governance commits (this WP's own EBG-0084 closure commit, and its own post-commit fix) - each independently fetched via `fetch_latest_decision` and successfully passed through `submit-response`'s full gate (approval check, repository-ref drift check, live pytest/`validate_repository.py` evidence capture) with zero Engineering Implementer involvement in the approval action itself. A real operational issue was found and fixed along the way: a stale duplicate service process left both an old and new instance bound to the same port simultaneously, causing persistent 403s until both were killed and a single clean instance restarted.

**Post-commit review found two governance-consistency findings, both fixed**: PST-0001's Current Mode/Phase/Workflow/Objective rows still described ESR-0029 as the latest closed session with none open, directly contradicting the commit's own claims - fixed across two rounds (the first fix itself briefly violated `validate_repository.py`'s own WikiLink-first pattern for the Current Mode field, caught by validation before commit); and EIP-ESR0030-001's body text still read as deployment-pending despite its own version history saying otherwise, fixed with an explicit "Current Status" banner distinguishing historical WP1-era text from the current state.

- Commit SHAs: `c8a851d` (EBG-0084 closure), `0b4cfff` (post-commit fix)
- `python -m pytest`: 338 passed (unchanged this WP - governance-only). `python scripts/validate_repository.py`: 0 errors, 130 warnings.

---

# 10. Session-Wide WP3/WP4 - Independent Repository Verification and Baseline Acceptance

**Handover preparation**: an [[ESR-0030_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0030 WP3 Independent Repository Verification handover]] was prepared and submitted to Codex via the bridge, covering the full session diff (`31a2f1c`..`0b4cfff`) across WP0A/WP1/WP2 - 12 files changed, 1,539 insertions, 162 deletions.

**Session-wide WP3 (Independent Repository Verification)**: required three rounds before reaching Pass, all self-inflicted by the handover document itself rather than the underlying session content - a literal, unresolved WikiLink shorthand in the handover's own prose caused a genuine `validate_repository.py` failure while the handover simultaneously claimed clean validation (an Independent Repository Verification document itself failing the very check it was reporting clean), and the same defect recurred twice more as the fix's own changelog text quoted the broken syntax verbatim. Codex independently confirmed the committed range matched the submitted diff stat exactly, with no `jarvis/`, `src/`, or `sentinel/` files touched anywhere in the session. **Pass, no findings** (final round).

**Session-wide WP4 (Repository Baseline Acceptance): `RBL-0017` retained, no new baseline established.** Both independent views converged: this session delivered AIEMS process tooling and governance (the Sponsor Approval Service, replacing a file-based approval command), not a user-visible JARVIS/Guardian product-capability change - matching the pattern of ESR-0025/ESR-0026/ESR-0027's own retain-baseline sessions rather than ESR-0028/ESR-0029's product-change pattern. Programme Sponsor's own determination: **Retain RBL-0017.**

- Commit SHAs: `8579e13` (WP3 handover, Pass), `b67c6df` (WP4 closure, RBL-0017 retained)
- `python -m pytest`: 338 passed. `python scripts/validate_repository.py`: 0 errors, 130 warnings.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EIP-ESR0030-001_SPONSOR_APPROVAL_SERVICE_IMPLEMENTATION|EIP-ESR0030-001]] | Approved-implemented package for WP1/WP2, v1.5. |
| [[ADR-0022_SPONSOR_APPROVAL_SERVICE|ADR-0022]] | Approved decision this session implements in full - code and deployment. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0084 Complete in full this session. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Not touched this session - no `src/`/UXP change, disclosed as an intentional scope boundary (AIEMS tooling session). |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Permanent Lead/Reviewer appointment this session operates under. |
| [[ESR-0030_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0030 WP3 Handover]] | Session-wide Independent Repository Verification and Baseline Acceptance record, v0.5, Section 10. |
| [[ESR-0029_ENGINEERING_SESSION_REPORT|ESR-0029]] | Prior closed session this one continues from. |
| [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] | Repository baseline retained at Section 10 - no new baseline this session. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 19 July 2026 | Claude Engineering Implementer | Initial creation and closure, authored at session close per established practice. Records WP0 (deferred sync-staleness fix), WP1 (Sponsor Approval Service implementation with three Codex-caught fix rounds), WP2 (genuine Sponsor-side Tailscale deployment with real cross-device approvals, EBG-0084 complete in full), and the session-wide WP3 Independent Repository Verification (Pass after three self-inflicted fix rounds) and WP4 Repository Baseline Acceptance (Retain RBL-0017, no new baseline). Fifth session run entirely through the AIEMS Exchange Bridge with no manual relay, and the first where the approval step itself ran through a genuinely deployed, separately-hosted service rather than a local file or bootstrap instance. Status Open to Closed. |
