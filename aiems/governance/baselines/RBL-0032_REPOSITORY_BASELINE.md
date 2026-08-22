# RBL-0032 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0032 |
| Title | ESR-0051 Repository Baseline (Process/Tooling Backlog Cluster; Guardian Orb Phase 2 Cluster Illumination) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0051_ENGINEERING_SESSION_REPORT|ESR-0051]] |
| Previous Baseline | [[RBL-0031_REPOSITORY_BASELINE|RBL-0031]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 22 August 2026 |
| HEAD at baseline creation | `b5fa582` |

---

# 2. Purpose

RBL-0032 records the repository baseline accepted by the Programme Sponsor at ESR-0051 WP7, superseding [[RBL-0031_REPOSITORY_BASELINE|RBL-0031]]. ESR-0051 opened following a ~2-week gap since ESR-0050 closed, at the Programme Sponsor's direct request for a full project review on return. It ran two Work Packages: WP1 (cleared the EBG-0090 through EBG-0096 process/tooling backlog cluster - a real execpolicy bug fix achieving a genuinely unattended Claude↔Codex review round trip, a streamlined Sponsor approval command, an installer script, a status-check command, and Windows auto-start with an explicitly documented Credential Manager exception) and WP2 (resolved EBG-0121, Guardian Orb Phase 2: Cluster Illumination - a genuine, live product-capability change). Guardian's Orb and Active Clusters panel now illuminate in response to real, observed backend RPC activity, verified against the real running backend process, not mocked.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0031_REPOSITORY_BASELINE|RBL-0031]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not yet content-refreshed for this session's WP2 delivery (Guardian Orb Phase 2), flagged as a documentation-staleness item for a future session's Documentation Debt sync, matching the same disclosed gap RBL-0031 itself carried forward from ESR-0049. |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ESR-0051 closes following this baseline's acceptance |

---

# 4. Baseline Recommendation Rationale

**WP0 (pre-session)**: a full project health review ([[WR-ESR0051-001_FULL_PROJECT_HEALTH_REVIEW|WR-ESR0051-001]]) was produced and independently Codex cross-reviewed (Conditional Pass with corrections, both folded in) before the session formally opened. One real gap was found and fixed: ESR-0050's own closure commit (`e586eca`) had been committed locally but never pushed - pushed during WP0, restoring GitHub as the accurate authoritative baseline.

**WP1 design review (Codex, `codex exec -s workspace-write`)**: [[EIP-ESR0051-001_PROCESS_TOOLING_BACKLOG_CLUSTER|EIP-ESR0051-001]] v0.1 reviewed Pass with one non-blocking governance note (EBG-0095's Credential Manager framing) - folded into v0.2.

**WP2 design review**: [[EIP-ESR0051-002_GUARDIAN_ORB_PHASE2_CLUSTER_ILLUMINATION|EIP-ESR0051-002]] v0.1 reviewed Approve with one required correction (a method-count undercount risking `gia.status` going unmapped, plus locking guidance and required coverage tests) - folded into v0.2.

**Pre-implementation approval gates**: Programme Sponsor approval-to-implement obtained and verified via `submit-response` directly against the real Sponsor Approval Service for both WP1 and WP2, before any code was written.

**WP1 post-commit review**: genuine independent Codex review of the real committed diff (`e586eca..fde34dc`) - Pass, one non-blocking documentation finding (REG-0001's own version-history prose one version stale), corrected and pushed separately (`f90ba22`). A further real bug (an `Add-Type -MemberDefinition` C# wrapping defect) was found live by the Programme Sponsor's own first `-Setup` attempt, fixed, Codex-reviewed (Pass, no findings), and pushed (`fdbfe4d`); the Programme Sponsor's full live end-to-end verification of all three home-directory scripts was recorded in a final addendum (`c755272`).

**WP2 post-commit review**: genuine independent Codex review of the real committed diff (`c755272..b5fa582`) - **Approve, no findings**. Confirmed exactly the 13 expected files changed, the required method-count correction present and enforced by a coverage test, `ActivityTracker`'s lock never held across a blocking write, and zero touch on Sentinel or any production code outside `jarvis/interfaces/`.

**Session-wide WP6 Independent Repository Verification**: covering the full session range `e586eca..b5fa582` (WP1 and WP2 combined, 5 commits). **Pass, no blocking findings** - confirmed exactly the expected 18 changed paths, `GAM-0001`/`sentinel/policy.py` byte-identical/untouched across the whole session, every governance "Completed" claim backed by real evidence, and no leftover scratch artefacts. Codex's own advisory assessment: genuine and baseline-worthy, recommending Establish.

**Push approval**: Programme Sponsor approval-to-implement gates verified via `submit-response` against the real Sponsor Approval Service for both Work Packages before implementation began; commits and pushes proceeded under that same authorisation, per established practice.

**The Programme Sponsor's determination**: **establish a new baseline**, since WP2 delivered a genuine, live product-capability change - Guardian's Orb and Active Clusters panel now illuminate in response to real, observed backend activity, verified against the running backend process - matching the same threshold applied at RBL-0025/RBL-0027/RBL-0028/RBL-0029/RBL-0030/RBL-0031 rather than the Retain threshold applied at architecture/documentation-only sessions such as ESR-0048.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `~/approve` / `~/reject` (Sponsor's home directory) | Now infer the session from `~/.current_session`, taking only `<work_package> "note"`. |
| `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md` | New Scope-Creep and Cross-WP-Dependency Flagging Discipline section; new WP0B `~/.current_session` step (v1.38 to v1.39). |
| `scripts/install-sponsor-approval-service.ps1` (new) | Interactive one-time setup convenience for the Sponsor Approval Service, mirroring `start-jarvis.bat`'s precedent. |
| `~/bridge-status` (new, Sponsor's home directory) | Bare unauthenticated connectivity probe for the Sponsor Approval Service. |
| `scripts/start_sponsor_approval_service_autostart.ps1` (new) | Windows Credential Manager-backed unattended auto-start, an explicitly documented exception to the normal agent-boundary rule; a Windows Scheduled Task registered and live-verified by the Programme Sponsor. |
| `jarvis/interfaces/activity_tracker.py` (new) | `ActivityTracker`/`METHOD_CLUSTERS`, real RPC-dispatch-to-cluster mapping covering all 16 dispatched methods. |
| `jarvis/interfaces/stdio_rpc.py` | Records genuine successful dispatch; `knowledge.graph` gains a real `active_clusters` pull field; `serve_forever` emits a new `knowledge.cluster_activity` push notification mirroring the existing heartbeat pattern. |
| `src/App.jsx`, `src/GuardianOrbGraph.jsx`, `src/KnowledgeGraphPanels.jsx`, `src/styles.css` | Live cluster illumination rendering - a glow-alpha boost on active-cluster Orb nodes, an `is-active` pulse on the Active Clusters panel. |
| `tests/e2e/app.spec.js` | 2 new Playwright tests (pull-path seed illumination, no-activity idle state) - 15/15 passing. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0091 through EBG-0096 and EBG-0121 marked Completed; EBG-0090 marked Investigated (no implementation authorised by that item). |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not content-refreshed this session for either WP1's process-tooling delivery or WP2's Guardian Orb Phase 2 delivery - flagged as a documentation-staleness item, recommended for a future session's Documentation Debt sync, matching the same disclosed pattern RBL-0031 itself carried forward.

---

# 7. Architecture Outcomes

- Guardian's Orb and Active Clusters panel move from a static, real-but-unchanging cluster view (Phase 1) to genuine access-triggered illumination (Phase 2) - real observed RPC activity now visibly lights up the corresponding cluster, closing the gap `GuardianOrbGraph.jsx`'s own code comment had named since Phase 1.
- The Claude↔Codex automated review loop (EBG-0096) is now proven fully unattended, twice, end to end - `codex exec -s workspace-write` genuinely reads its own inbox, verifies real repository state, and calls `return-findings` itself, after a `~/.codex/rules/default.rules` execpolicy misconfiguration (forward-slash vs backslash path patterns) was root-caused and fixed.
- `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` boundary and `sentinel/policy.py` remain completely untouched throughout this session.
- No dependency was created on Guardian Orb Phase 3 (agent-traversal animation) or Phase 4 (Guardian reasoning connection) - both remain explicitly out of scope, confirmed by both Codex design and post-commit reviews.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- cluster illumination reflects genuine RPC-capability access, not proof that any downstream provider call within a handler itself succeeded;
- no change to which RPC methods exist or their params/return shape, beyond `knowledge.graph`'s additive `active_clusters` field;
- no per-request activity history/audit log - only "is this cluster active right now" is tracked;
- EBG-0095's Windows Credential Manager auto-start is an explicit, named, accepted exception to STD-0006/ADR-0022's original hard "must never be agent-reachable" boundary, not a resolved instance of it - protects against a different Windows user account or an off-machine copy, not against another process (including a future agent) under the same account;
- no change to `sponsor_client.py`'s or `sponsor_approval_service.py`'s security-relevant interfaces or token-gating logic;
- EBG-0090's investigation authorises no production wiring of any CLI-agent capability into Guardian's conversational path.

---

# 9. Verification

Repository validation performed across ESR-0051's Work Packages and at WP6/WP7:

- Git working tree was clean throughout; the session's content (`e586eca..b5fa582`, 5 commits) pushed to `origin/main`.
- 523 Python tests passing plus 1 correctly-skipped test - up from 512/1 at RBL-0031 (11 new tests: `ActivityTracker` unit tests plus `stdio_rpc.py` notification/pull-field tests).
- 15 Playwright tests passing (13 existing unchanged, 2 new) - up from 13 at RBL-0031.
- `npm run build` clean throughout.
- `python scripts/validate_repository.py` (full mode): 0 errors throughout (289 to 291 warnings, all pre-existing-pattern stray cross-references, non-blocking).
- WP1 design review (Codex): v0.1 Pass with one non-blocking governance note, folded into v0.2.
- WP2 design review (Codex): v0.1 Approve with one required correction, folded into v0.2.
- WP1 post-commit review (Codex): Pass with one non-blocking documentation finding, corrected; a live-caught real bug (Add-Type wrapping defect) separately fixed and Codex-reviewed Pass, no findings.
- WP2 post-commit review (Codex): Approve, no findings.
- Session-wide WP6 (Codex): Pass, no blocking findings, covering the full session diff against RBL-0031.
- Every commit gated through the real AIEMS Exchange Bridge / Sponsor Approval Service (`submit-to-review`/`return-findings`/`submit-response`) - approval-to-implement verified for real before implementation began on both Work Packages.
- Live smoke check against the real, unmocked `python -m jarvis --ipc-stdio` backend process: a real `platform.status` call produced a genuine `knowledge.cluster_activity` notification, and the subsequent `knowledge.graph` call correctly reported the resulting `active_clusters`.
- The Programme Sponsor's own live end-to-end verification of `~/approve`/`~/reject`/`~/bridge-status` and the Credential Manager `-Setup` flow.
- The Programme Sponsor's own WP7 determination: establish a new baseline rather than retain RBL-0031 (Section 4).

---

# 10. Handover

Future work against this baseline should include:

1. This document and [[RBL-0031_REPOSITORY_BASELINE|RBL-0031]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] refresh for this session's Guardian Orb Phase 2 delivery - not yet reflected there.
5. Guardian Orb Phase 3 (agent-traversal animation, blocked on deeper GIA telemetry) and Phase 4 (Guardian reasoning connection) remain the natural next increments of the Orb vision, when a future session takes them up.
6. The Local Agent/Action faculty remains the single largest remaining JARVIS capability gap, deliberately not selected this session - it crosses `GAM-0001` Section 8A's hard `DENY` boundary and warrants a dedicated scoping conversation.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0031_REPOSITORY_BASELINE|RBL-0031]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0051_ENGINEERING_SESSION_REPORT|ESR-0051]] | Session this baseline is drawn from. |
| [[WR-ESR0051-001_FULL_PROJECT_HEALTH_REVIEW|WR-ESR0051-001]] | Working Report produced ahead of this session's opening; source of this session's objective. |
| [[EIP-ESR0051-001_PROCESS_TOOLING_BACKLOG_CLUSTER|EIP-ESR0051-001]] | Approved Engineering Implementation Package WP1's deliverables were built against. |
| [[EIP-ESR0051-002_GUARDIAN_ORB_PHASE2_CLUSTER_ILLUMINATION|EIP-ESR0051-002]] | Approved Engineering Implementation Package WP2's deliverables were built against. |
| [[GAM-0001_GUARDIAN_AUTHORITY_AND_BOUNDARY_MODEL|GAM-0001]] | Section 8A - the boundary this baseline stays inside, untouched. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Section 8.1 - the Guardian Orb design direction WP2 implements Phase 2 of. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0090 through EBG-0096 and EBG-0121 (all closed or investigated this session). |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not content-refreshed this session, flagged for future sync. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 22 August 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0031, following Codex design reviews (WP1 v0.1 Pass with one non-blocking governance note; WP2 v0.1 Approve with one required correction, both folded in before implementation), verified pre-implementation approval gates, post-commit Codex reviews (WP1 Pass with one non-blocking finding plus a separately Codex-reviewed live-caught bug fix; WP2 Approve, no findings), session-wide WP6 Independent Repository Verification (Pass, no blocking findings), and the Programme Sponsor's explicit WP7 decision to cut a new baseline: WP2's real, live-verified Guardian Orb Phase 2 delivery warrants a new baseline. |
