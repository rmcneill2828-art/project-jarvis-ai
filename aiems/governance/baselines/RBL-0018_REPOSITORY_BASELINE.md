# RBL-0018 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0018 |
| Title | ESR-0031 Repository Baseline (Streaming Notifications MVP + AIEMS Session-Opening Launcher) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | ESR-0031 (in progress - no session report artefact exists yet, per established practice) |
| Previous Baseline | [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 20 July 2026 |
| HEAD at baseline creation | `4c5e4dd` |

---

# 2. Purpose

RBL-0018 records the repository baseline accepted by the Programme Sponsor at ESR-0031 WP4, superseding [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]]. ESR-0031 delivered the UXP-backend bridge's first-ever live-push mechanism (WP2, Streaming Notifications MVP, EBG-0099) - a real Rust I/O restructuring and a genuinely new, live-verified user-observable capability, not process tooling alone. Both independent WP3 views (Engineering Implementer and Engineering Reviewer) converged on this being baseline-worthy, matching the pattern of RBL-0016/RBL-0017's own product-capability-change triggers rather than RBL-0015's AIEMS-tooling-only precedent.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - refreshed this session (WP0) to reflect ESR-0027's Personal Memory delivery; the streaming-notifications capability itself is not yet reflected, tracked as a future refresh |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for continued ESR-0031 work or a future session |

---

# 4. Baseline Recommendation Rationale

The [[ESR-0031_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP3 handover]] recorded two independently-reached views (Section 9), both recommending a new baseline rather than retaining RBL-0017.

**Engineering Implementer's view**: unlike ESR-0030 (pure AIEMS process tooling), this session delivered a genuine, live-verified, user-observable UXP capability - the streaming-notifications heartbeat display, proven via a real running application session (two screenshots ~35 seconds apart showing the timestamp genuinely advance) rather than unit tests alone.

**Engineering Reviewer's (Codex) independent view**: converged - "the intended ESR-0031 range contains a real user-observable product increment: backend-originated streaming notifications carried through Python stdio JSON-RPC, Rust/Tauri event forwarding, and React display. It is deliberately small, but it changes the UXP's runtime capability rather than only updating governance or process tooling. That is baseline-worthy."

**The Programme Sponsor's determination**: **establish a new baseline**, agreeing with both independent views.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `jarvis/interfaces/stdio_rpc.py` | `StdioRpcServer` gained a background heartbeat thread emitting a `system.heartbeat` JSON-RPC notification (no `id` key) every `JARVIS_HEARTBEAT_INTERVAL_SECONDS` (default 30s), guarded by a shared write lock so it can never interleave with response writes. 4 new in-process unit tests. |
| `src-tauri/src/lib.rs` | Restructured from a single synchronous write-then-read per call into a background reader thread plus a pending-call dispatch map: a line with an `id` key routes to the matching in-flight call, a line with no `id` key is forwarded via `app_handle.emit("jarvis://notification", ...)`. An unparsable line fails every currently-pending call and resets connection state - the multi-call generalisation of the pre-existing single-call teardown behaviour, fixed during pre-implementation review. |
| `src/App.jsx`, `src/styles.css` | A second, independent `useEffect` listens for `jarvis://notification`, displaying the live heartbeat timestamp next to the System Health panel. The existing one-time `platform_status`/`knowledge_graph` mount fetch is unchanged. |
| `scripts/session_launcher.py` (new), `scripts/tests/test_session_launcher.py` (new) | AIEMS Session-Opening Launcher (EBG-0097) - a read-only reporting script gathering PST-0001 current state, EBR-0001 high-priority backlog, and JRM-0001 near-term roadmap into one report for WP0B objective discussion. Two genuine defects (a WikiLink-pipe table-parsing bug, a header-row false-positive) found and fixed during its own required live smoke check. |
| `aiems/governance/status/PST-0001_PROGRAMME_STATUS.md`, `aiems/models/MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE.md`, `aiems/governance/baselines/PCB-0001_PRODUCT_CAPABILITY_BASELINE.md`, `jarvis/platform/shell.py` | WP0 repository synchronisation - corrected stale "`jarvis/memory/` empty stub" claims predating ESR-0027 WP1's real Personal Memory delivery, across three fix rounds; a genuine version-badge-vs-Document-Control-table drift bug found and fixed along the way. |
| [[EIP-ESR0031-001_SESSION_OPENING_LAUNCHER|EIP-ESR0031-001]] | v1.1, Approved-implemented. Closes EBG-0097. |
| [[EIP-ESR0031-002_STREAMING_NOTIFICATIONS_MVP|EIP-ESR0031-002]] | v1.0, Approved-implemented. Closes EBG-0099 (EBG-0050's remaining "streaming notifications" scope). |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0097 (Session-Opening Launcher) and EBG-0099 (Streaming Notifications MVP) Complete; EBG-0098 (version-drift detection) and EBG-0100 (hardcoded UXP Memory sidebar row) registered, Candidate Backlog, not actioned. |
| Test suite | 351 tests, up from RBL-0017's 338 - 9 new from the launcher, 4 new from the heartbeat mechanism; no regressions. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was refreshed this session (WP0) to correct a stale Memory-capability claim, unrelated to WP2's streaming-notifications delivery. The streaming-notifications capability itself is not yet reflected in PCB-0001 or the JARVIS Capability Readiness Matrix - tracked as a future refresh, not actioned by this baseline.

---

# 7. Architecture Outcomes

- First live-push mechanism the UXP-backend bridge has ever had. ADR-0019's JSON-RPC 2.0 envelope was adopted at ESR-0017 specifically so this could be added without a breaking change (EBG-0050's own long-open remaining scope) - this baseline is the first time that provision was actually exercised.
- First genuine architectural restructuring of the Tauri sidecar's I/O model since its original foundation-scope implementation: synchronous per-call `read_line()` replaced by a background reader thread and pending-call dispatch map, proven not to silently break existing request/response calls via a real running-application live smoke check, not unit tests alone.
- A genuine internal contradiction in the implementation package's own requirements was found and fixed before any code was written - an unparsable stream line's handling could not be resolved as originally specified, since the reader thread has no way to distinguish a broken notification from a broken response.
- A previously-selected Work Package objective (Shared Family Memory) was abandoned before drafting began, once GAM-0001 Section 10's explicit non-goal (household role authentication/enforcement not implemented) was checked directly - a disclosed, deliberate re-scoping rather than a silently-dropped one.
- A recurring project-wide staleness pattern (governance documents describing repository state that has since changed) was found to run deeper than initially scoped at WP0, requiring three fix rounds; a genuine, previously-undetected version-badge-vs-Document-Control-table drift bug was found and fixed along the way, and a new backlog item (EBG-0098) registered to prevent recurrence.
- A refined AI-to-AI review-automation pattern (`codex exec -s read-only`, Claude relaying findings under explicit per-instance Sponsor approval) was proven across every Work Package this session, replacing an earlier approach that depended on a fragile Windows sandbox permission grant.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no new ESR-0032 artefact is created by this baseline - ESR-0031 closes with this baseline's acceptance;
- PCB-0001's streaming-notifications capability is not reflected - a future refresh remains open work;
- EBG-0098 (version badge/table drift detection in `validate_repository.py`) is registered but not implemented by this baseline;
- EBG-0100 (the UXP capability sidebar's hardcoded Memory row) is registered but not implemented by this baseline - found as a byproduct of WP2's own live smoke check, out of that Work Package's scope;
- Shared Family Memory (MDS-0001 Section 6.3) remains unimplemented - explicitly deferred, not silently dropped, pending a future household identity/authentication system GAM-0001 Section 10 excludes from its own scope;
- real business-logic-driven notifications (beyond the proof-of-concept heartbeat) remain unbuilt - explicitly excluded from EIP-ESR0031-002's own scope, a future package's work.

---

# 9. Verification

Repository validation performed during ESR-0031 WP3/WP4:

- Git working tree was clean; the session's intended content range (`82050c9`..`d611c67`) pushed to `origin/main`.
- Repository branch was `main`, synchronised with `origin/main`.
- 351/351 tests passing, up from RBL-0017's 338 (13 net-new tests; no regressions).
- `python scripts/validate_repository.py` (full mode) passed with 0 errors, 140 warnings (130 pre-existing plus 10 new, disclosed, accepted cross-document false positives).
- `cargo build --manifest-path src-tauri/Cargo.toml` clean, no warnings.
- `npm run build` clean.
- `git diff --stat 82050c9..d611c67` independently re-run by the Engineering Reviewer, confirmed to match exactly (16 files, 1,353 insertions, 116 deletions).
- Live verification throughout: a real subprocess invocation of `python -m jarvis --ipc-stdio` confirming genuine heartbeat emission at the configured interval (manual, not part of the committed test suite); a real `npm run tauri dev` session, two screenshots ~35 seconds apart showing the heartbeat timestamp genuinely advance while `platform_status`/`knowledge_graph` continued to populate real data correctly in the same session.
- The Engineering Reviewer performed WP3 Independent Repository Verification: **Pass, no blocking findings** after one fix round on the handover document itself (a self-referential HEAD-staleness clarification, not a repository-content defect).
- The Programme Sponsor's own WP4 determination: establish a new baseline rather than retain RBL-0017 (Section 4).

---

# 10. Handover

**This baseline closes ESR-0031**, per the Programme Sponsor's WP4 acceptance. The ESR-0031 Engineering Session Report is authored separately, following this baseline's acceptance.

Future work against this baseline should include:

1. This document and [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - specifically EBG-0098 (version-drift detection) and EBG-0100 (hardcoded UXP Memory sidebar row), both Candidate Backlog.
5. [[EIP-ESR0031-001_SESSION_OPENING_LAUNCHER|EIP-ESR0031-001]], [[EIP-ESR0031-002_STREAMING_NOTIFICATIONS_MVP|EIP-ESR0031-002]], and the [[ESR-0031_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP3 handover]] for full delivery detail.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0017_REPOSITORY_BASELINE|RBL-0017]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0031_WP3_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0031 WP3 Handover]] | Independent verification record this baseline's acceptance is drawn from. |
| [[EIP-ESR0031-001_SESSION_OPENING_LAUNCHER|EIP-ESR0031-001]] | Approved-implemented package for the AIEMS Session-Opening Launcher. |
| [[EIP-ESR0031-002_STREAMING_NOTIFICATIONS_MVP|EIP-ESR0031-002]] | Approved-implemented package this baseline's streaming-notifications deliverable was implemented against. |
| [[ADR-0019_UXP_BACKEND_INTEGRATION_ARCHITECTURE|ADR-0019]] | Decision this baseline's WP2 extends - the JSON-RPC 2.0 envelope was adopted specifically to allow streaming notifications without a breaking change. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 10's explicit non-goal (household role authentication/enforcement) that ruled out Shared Family Memory as this session's WP2. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - refreshed this session for Memory-status accuracy; streaming-notifications not yet reflected. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register; EBG-0097/EBG-0099 Complete, EBG-0098/EBG-0100 Candidate Backlog. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 20 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0017, following the Engineering Reviewer's WP3 Pass and the Programme Sponsor's explicit WP4 decision to cut a new baseline rather than retain RBL-0017: the Streaming Notifications MVP materially changes the running UXP's runtime capability, agreeing with both independent WP3 baseline views. |
