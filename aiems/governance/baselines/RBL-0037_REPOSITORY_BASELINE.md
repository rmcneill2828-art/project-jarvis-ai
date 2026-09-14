# RBL-0037 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0037 |
| Title | ESR-0057 Repository Baseline (JRM-0001 Staleness Sweep; BRD-0001 Personal Memory Backup; Home Assistant Assessment) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0057_ENGINEERING_SESSION_REPORT|ESR-0057]] |
| Previous Baseline | [[RBL-0036_REPOSITORY_BASELINE|RBL-0036]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 14 September 2026 |
| HEAD at baseline creation | `fb2381d` |

---

# 2. Purpose

RBL-0037 records the repository baseline accepted by the Programme Sponsor at ESR-0057 WP7, superseding [[RBL-0036_REPOSITORY_BASELINE|RBL-0036]]. ESR-0057 opened at the Programme Sponsor's direct request following an instruction to read PBK-0001, without an initial Work Package selection - WP0A surfaced a documentation-staleness finding that became WP1, and WP2/WP3 were selected from Sponsor-presented options as the session progressed. The session also absorbed a real, disclosed crisis mid-way through: Codex (the permanent Engineering Reviewer, EE-0001 Section 7) was found retired on cost grounds, not merely temporarily unavailable, and a same-session Antigravity CLI substitute was blocked twice by Claude Code's own harness - every Work Package from that point was closed via Programme Sponsor direct review plus Engineering Implementer self-verification rather than genuine independent AI review, disclosed throughout rather than silently substituted.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0036_REPOSITORY_BASELINE|RBL-0036]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not content-refreshed this session; the Personal Memory export/backup capability is not yet reflected there, flagged as a documentation-staleness item for a future session's Documentation Debt sync. |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ESR-0057 closes following this baseline's acceptance |

---

# 4. Baseline Recommendation Rationale

**WP0A/WP0B**: Repository Synchronisation and Session Initialisation. No initial Work Package selection was given; WP0A's own review of JRM-0001 surfaced two stale rows (EBG-0005, EBG-0068), which the Programme Sponsor directed as WP1.

**WP1 (JRM-0001 Whole-Document Staleness Sweep)**: [[EIP-ESR0057-001_JRM-0001_WHOLE_DOCUMENT_STALENESS_SWEEP|EIP-ESR0057-001]] - applying PBK-0001's Documentation Debt Discipline whole-document sweep to the two originally-spotted rows found 19 stale `EBG-####` references across four sections, most closed at ESR-0033 WP2's Codex-led Theme 7 triage and never reflected back into the roadmap. Two rows (EBG-0042, EBG-0047) were significantly stale, describing real delivered architecture work as still-open Candidate Backlog. Codex design review was attempted and found genuinely unobtainable - two `codex exec` invocations both failed with `HTTP 402 Payment Required`/`deactivated_workspace` - disclosed rather than assumed Pass; Programme Sponsor reviewed the diff directly and approved. Post-commit review was attempted a third time with the same result; Programme Sponsor directed Engineering Implementer self-verification in its place. **This is where the Codex-retirement finding surfaced**: the Programme Sponsor confirmed live in chat that the account issue was not temporary but a deliberate cost-driven retirement, with Gemini/Antigravity as the intended replacement - EBG-0126 registered to track the required governance re-appointment and bridge engineering work, not actioned this session.

**WP2 (EBG-0023, BRD-0001 Guidance and Personal Memory Export)**: [[EIP-ESR0057-002_BRD-0001_GUIDANCE_AND_MEMORY_EXPORT|EIP-ESR0057-002]] - EBG-0023 as registered authorised guidance/architecture-definition only; flagged to the Programme Sponsor that a second documentation-only Work Package this session would leave the session without the product-moving work PBK-0001's Feature-First Delivery Discipline requires. Programme Sponsor directed a disclosed scope extension: [[BRD-0001_BACKUP_RECOVERY_AND_DATA_PROTECTION_GUIDANCE|BRD-0001]] created (Draft) alongside a real first implementation slice - `PersonalMemoryStore.export_snapshot()`, `PersonalMemoryService.export_backup()`, `GuardianRuntime.backup_memory()` and a new `memory.backup` RPC method, preserving MDS-0001 Section 7.4's consent traceability by exporting both `personal_memory` and `consent_decisions` tables together. A real defect (a missing `activity_tracker.py` cluster-mapping entry) was caught by running the full test suite rather than only the new tests. No independent AI review available; Programme Sponsor reviewed and approved directly; Engineering Implementer self-verified the pushed commit.

**WP3 (EBG-0025, Home Assistant and Smart Home Integration Assessment)**: [[WR-ESR0057-001_HOME_ASSISTANT_SMART_HOME_INTEGRATION_ASSESSMENT|WR-ESR0057-001]] (Working Report) - assessed Home Assistant as the right platform on architectural fit alone (the only major self-hosted, no-cloud-dependent ecosystem matching this project's own defaults), but identified the substantive gate as GAM-0001's `LOCAL_AGENT_ACTION` boundary (confirmed still `DENY` for every request), independent of platform choice, and unblocked only by JRM-0001 Track B Phase 3 - which had no backlog item authorising its build at all. Programme Sponsor directed closing EBG-0025 and registering both a narrower read-only candidate (EBG-0127, mirroring GIA's `ROUTINE_INTERACTION` precedent) and Phase 3 itself (EBG-0128, closing JRM-0001's own flagged gap) - neither authorising implementation. No code touched, matching EBG-0025's own assessment-only registered scope.

**Session-wide WP6 Independent Repository Verification**: covering the full session range `c30b703..HEAD` (ESR-0056's own closure commit; six ESR-0057 commits). **No independent AI review was available** - Codex retired, Antigravity blocked by Claude Code's own harness twice. Self-verified by the Engineering Implementer instead, disclosed as a materially weaker substitute for the standing template: confirmed exactly six commits and 18 changed files, no `src/`/`src-tauri/`/`sentinel/policy.py`/`GAM-0001` path touched; independently re-ran `pytest` (561 passed/1 skipped) and `validate_repository.py` (0 errors/329 warnings); cross-checked that both this session's scope extensions (WP2's implementation slice, WP3's EBG-0127/0128 registrations) were disclosed and Programme Sponsor-approved before proceeding, not silently absorbed. **Verdict: Pass**, self-assessed only.

**The Programme Sponsor's determination**: **establish a new baseline**, agreeing with the Engineering Implementer's own advisory - WP2 delivered a genuine new backend capability (Personal Memory export/backup), matching the Establish threshold applied at ESR-0049 through ESR-0055.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | 19 stale `EBG-####` references corrected across Sections 6.1/6.2/6.3/7.5 (WP1); Section 7.1/7.3 Phase 3, Phase 8 and Section 7.5 updated for EBG-0127/EBG-0128 (WP3). |
| `jarvis/memory/store.py`, `jarvis/memory/service.py`, `jarvis/guardian/runtime.py`, `jarvis/interfaces/stdio_rpc.py` | New Personal Memory export/backup capability - `export_snapshot()`, `export_backup()`, `backup_memory()`, new `memory.backup` RPC method (WP2). |
| `jarvis/interfaces/activity_tracker.py` | `memory.backup` added to `METHOD_CLUSTERS` (WP2, a real gap the full test suite caught). |
| [[BRD-0001_BACKUP_RECOVERY_AND_DATA_PROTECTION_GUIDANCE|BRD-0001]] | New architecture model (Draft) - backup/recovery/data-protection guidance, resolving EBG-0023 (WP2). |
| [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] | Sections 9/10/11 forward references repointed from bare "EBG-0023" text to BRD-0001; a stale RBL-0015 baseline reference (since ESR-0028) also corrected to RBL-0036 (WP2). |
| [[WR-ESR0057-001_HOME_ASSISTANT_SMART_HOME_INTEGRATION_ASSESSMENT|WR-ESR0057-001]] | Working Report (uncontrolled) - Home Assistant/smart-home assessment, resolving EBG-0025 (WP3). |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0023, EBG-0025 closed Complete; EBG-0126, EBG-0127, EBG-0128 registered (Candidate Backlog, no implementation authorised). |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not content-refreshed this session - the Personal Memory export/backup capability (a real, tested, live-wired new RPC method) is not yet reflected there, flagged for a future Documentation Debt sync's own judgement, matching the precedent set at RBL-0036's own equivalent gap.

---

# 7. Architecture Outcomes

- Personal Memory now has a real, tested export/backup capability (`memory.backup`), the first concrete delivery against MDS-0001's Section 9 gate - a genuine new backend capability, not merely an architecture document.
- A new architecture domain (Backup, Recovery and Data Protection) is defined for the first time via BRD-0001, explicitly scoping what this session delivered (export only) against what remains future work (recovery/restore, encryption at rest, retention scheduling).
- JRM-0001 Track B Phase 3 (Local Agent Action Faculty) now has a registered backlog item (EBG-0128) for the first time since the roadmap's own Phase 3 definition - closing a gap the roadmap itself had repeatedly flagged as open, though no implementation or `LOCAL_AGENT_ACTION` policy change is authorised by that registration.
- `sentinel/policy.py` and `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` boundary remain completely untouched - confirmed `DENY` for every request, read directly rather than assumed.
- No change to `src/`/`src-tauri/` product UXP code this session - WP2's product-moving work was backend-only (RPC method), matching PBK-0001's Feature-First Delivery Discipline's allowance for backend/infrastructure delivery.
- **Disclosed limitation, session-wide**: the Engineering Reviewer role (Codex, EE-0001 Section 7) is unavailable for the remainder of this project's near-term future absent a resolution recorded against EBG-0126. Every Work Package from WP1 onward was closed via Programme Sponsor direct review plus Engineering Implementer self-verification, not genuine independent AI review - a real, material reduction in this baseline's own verification rigour relative to every prior accepted baseline back to EE-0001's original appointment.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no recovery/restore/import capability for Personal Memory backups - export only;
- no encryption at rest for backup files - disclosed open gap in BRD-0001;
- no Session or Shared-Family Memory tier coverage - neither tier is implemented yet;
- no UXP/frontend surface for the backup capability - RPC-only this session;
- no implementation, policy change, or specific action-capability selection authorised by EBG-0128's registration;
- no Codex/Antigravity reviewer-role resolution - EBG-0126 remains open, scoping deferred to a future session.

---

# 9. Verification

Repository validation performed across ESR-0057's Work Packages and at WP6/WP7:

- Git working tree was clean throughout; the session's content (`c30b703..HEAD`, 6 commits) pushed to `origin/main`.
- 561 Python tests passing plus 1 correctly-skipped test by session close (up from 553 at RBL-0036's acceptance - 8 new tests, all from WP2's Personal Memory export/backup coverage).
- `python scripts/validate_repository.py` (full mode): 0 errors throughout; warning count moved 323→329 across the session (net +6, from new cross-referencing governance prose in the new/modified artefacts - consistent with the established pre-existing false-positive pattern, not a new class of issue).
- **No Codex/Antigravity design or post-commit review was obtained for any Work Package this session** - every review step from WP1 onward is Programme Sponsor direct review plus Engineering Implementer self-verification, disclosed throughout rather than silently substituted. This is the first ESR since EE-0001's Section 7 appointment (10 July 2026) with zero genuine independent-AI-review coverage.
- Every commit gated through the real AIEMS Exchange Bridge / Sponsor Approval Service (`submit-to-review`/`submit-response`), including three genuine drift-refusal-and-retry episodes (each Work Package's closure-record commit required a fresh Sponsor decision at the moved HEAD).
- Session-wide WP6 (Engineering Implementer self-verification): Pass, no blocking findings, covering the full session diff against RBL-0036 - self-assessed only, no independent cross-check.
- The Programme Sponsor's own WP7 determination: establish a new baseline rather than retain RBL-0036 (Section 4).

---

# 10. Handover

Future work against this baseline should include:

1. This document and [[RBL-0036_REPOSITORY_BASELINE|RBL-0036]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. **EBG-0126 (retire Codex, adopt Gemini/Antigravity as permanent Engineering Reviewer)** - the highest-priority open item this baseline carries forward: the standing dual-AI review workflow this project's whole governance model assumes is currently non-functional, and every session until this is resolved will face the same choice ESR-0057 made repeatedly.
5. BRD-0001's recovery/restore capability - explicitly deferred, minimum requirements already stated in BRD-0001 Section 6.
6. EBG-0127 (read-only Home Assistant state-query agent) and EBG-0128 (Action faculty implementation) - both Candidate Backlog, neither authorising implementation yet.
7. PCB-0001 refresh for this session's Personal Memory export/backup capability - not yet reflected there.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0036_REPOSITORY_BASELINE|RBL-0036]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0057_ENGINEERING_SESSION_REPORT|ESR-0057]] | Session this baseline is drawn from. |
| [[EIP-ESR0057-001_JRM-0001_WHOLE_DOCUMENT_STALENESS_SWEEP|EIP-ESR0057-001]] | Approved Engineering Implementation Package WP1's deliverables were built against. |
| [[EIP-ESR0057-002_BRD-0001_GUIDANCE_AND_MEMORY_EXPORT|EIP-ESR0057-002]] | Approved Engineering Implementation Package WP2's deliverables were built against. |
| [[WR-ESR0057-001_HOME_ASSISTANT_SMART_HOME_INTEGRATION_ASSESSMENT|WR-ESR0057-001]] | Working Report WP3 was built from. |
| [[BRD-0001_BACKUP_RECOVERY_AND_DATA_PROTECTION_GUIDANCE|BRD-0001]] | New architecture model created this session, Draft status. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0023, EBG-0025 closed Complete; EBG-0126, EBG-0127, EBG-0128 registered. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | 19-row staleness sweep plus Phase 3/8/7.5 updates. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not content-refreshed this session, flagged for future sync. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 14 September 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0036, in the absence of any independent AI review this session (Codex retired on cost grounds; a genuine Antigravity CLI substitute blocked twice by Claude Code's own harness). Every Work Package closed via Programme Sponsor direct review plus Engineering Implementer self-verification instead, disclosed throughout. The Programme Sponsor's explicit WP7 decision to cut a new baseline agrees with the Engineering Implementer's own advisory: WP2's genuine new backend capability (Personal Memory export/backup) warrants a new baseline, matching the Establish threshold applied at ESR-0049 through ESR-0055. |
