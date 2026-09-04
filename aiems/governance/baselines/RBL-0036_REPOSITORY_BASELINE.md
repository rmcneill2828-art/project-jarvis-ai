# RBL-0036 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0036 |
| Title | ESR-0056 Repository Baseline (esbuild/vite Security Upgrade; DRA-0001 Device Bootstrap and Restore Architecture) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0056_ENGINEERING_SESSION_REPORT|ESR-0056]] |
| Previous Baseline | [[RBL-0035_REPOSITORY_BASELINE|RBL-0035]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 4 September 2026 |
| HEAD at baseline creation | `9b96dcc` |

---

# 2. Purpose

RBL-0036 records the repository baseline accepted by the Programme Sponsor at ESR-0056 WP7, superseding [[RBL-0035_REPOSITORY_BASELINE|RBL-0035]]. ESR-0056 opened at the Programme Sponsor's direct request following an instruction to read PBK-0001, then set a four-Work-Package objective through iterative scoping: EBG-0058 (PBK-0001 Clause Consolidation) and the JRM-0001 REG-0001 HST/FCH gap were both found already resolved at WP0A/WP0B, requiring a Feature-First Delivery Discipline flag and the addition of a genuine product-moving Work Package (EBG-0085) ahead of the originally-planned order. The session ultimately delivered a real dependency security remediation (WP1), two documentation-currency corrections evidencing and closing stale backlog/roadmap claims (WP2, WP4), and a genuine new architecture artefact defining Platform Services mechanics no prior artefact covered (WP3).

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0035_REPOSITORY_BASELINE|RBL-0035]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not content-refreshed this session; the Vite/esbuild dependency upgrade and DRA-0001's creation are not yet reflected there, flagged as a documentation-staleness item for a future session's Documentation Debt sync. |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ESR-0056 closes following this baseline's acceptance |

---

# 4. Baseline Recommendation Rationale

**WP0A/WP0B**: Repository Synchronisation and Session Initialisation. The Programme Sponsor's initial four-item selection (EBG-0058, EBG-0046, REG-0001 HST/FCH gap) was found to include two already-resolved items - EBG-0058 (Complete since ESR-0028) and the REG-0001 HST/FCH gap (Complete since ESR-0028 via EBG-0071) - both flagged before proceeding rather than silently re-executed. A Feature-First Delivery Discipline flag led to EBG-0085 (esbuild/vite dev-server vulnerability) being added as a genuine product-moving Work Package, sequenced first.

**WP1 (EBG-0085)**: [[EIP-ESR0056-001_ESBUILD_VITE_DEV_SERVER_VULNERABILITY_UPGRADE|EIP-ESR0056-001]] - `vite` `^5.4.11`→`^8.2.2`, `@vitejs/plugin-react` `^4.3.4`→`^6.1.1`. Codex design review: Conditional Pass, two corrections folded in (CI Node-version check extended to both `frontend-build` and `playwright` jobs; `npm ci` added as an explicit validation step). Implementation found a genuine side-effect defect (a new transitive dependency's README tripped `validate_repository.py`'s WikiLink scan) - fixed within the same WP as a disclosed, Sponsor-approved scope extension (`node_modules` added to `IGNORED_DIRS`). Post-commit review round 1: **Fail** (a real documentation-consistency defect - this session's own report still read as pre-commit within the pushed commit); fixed. Round 2: **Pass**.

**WP2 (EBG-0058)**: retargeted at WP0B once found already Complete - a fresh accretion re-check of PBK-0001's growth from v1.28 through v1.43 (the two new clauses added since the original consolidation, Documentation Debt Discipline and Scope-Creep and Cross-WP-Dependency Flagging Discipline, both compared against existing content and confirmed non-duplicative). Codex Pass, no corrections. No PBK-0001 text changed - the genuine finding.

**WP3 (EBG-0046)**: scope narrowed once MDS-0001 Section 8 was found to already own the portable-memory/encryption requirements EBG-0046's own description named, reserving bootstrap/device-registry/sync-protocol specifically for EBG-0046. [[DRA-0001_DEVICE_BOOTSTRAP_AND_RESTORE_ARCHITECTURE|DRA-0001]] created (Draft) - a new domain-specific architecture model covering that genuine remaining gap plus general configuration portability. Codex design review: Conditional Pass, one required fix folded in (the encryption/policy-control requirement, originally scoped to memory records only, extended to identity-scoped configuration and Device Registry/restore metadata per ADR-0012's general requirement) plus one non-blocking tightening (device-registry trust never grants memory-tier access on its own). Post-commit review: Pass.

**WP4**: JRM-0001's two stale references to the REG-0001 HST/FCH gap (Sections 6.1 and 9) corrected - EBR-0001's EBG-0071 row showed the gap was formally created and closed Complete at ESR-0028 WP1. Codex Pass, no corrections.

**Approval Service integrity note**: getting genuine Sponsor approvals recorded this session surfaced and fixed a real defect in the Programme Sponsor's own `~/approve`/`~/reject` host-side shortcut scripts (outside this repository) - calling them with `sponsor_client.py`-style flags silently mis-mapped arguments into wrongly-addressed database rows, diagnosed by reading `.aiems-exchange/sponsor_decisions.db` directly (read-only; `AIEMS_SPONSOR_TOKEN` never used or possessed by the Engineering Implementer). Both scripts hardened to reject malformed invocations with a clear usage message, applied directly (host-side tooling, outside AIEMS's controlled-artefact governance).

**Session-wide WP6 Independent Repository Verification**: covering the full session range `f39ff37..HEAD` (ESR-0055's own closure commit; nine ESR-0056 commits). **Pass, no blocking findings** - confirmed the expected changed-file set with no `src/`/`src-tauri/`/`sentinel/policy.py`/`GAM-0001` path touched; independently re-ran `pytest` (553 passed/1 skipped) and `validate_repository.py` (0 errors/312 warnings), both matching; confirmed EBR-0001/REG-0001/JRM-0001/MDS-0001/DRA-0001 internally consistent with each other and the real repository state. One non-blocking observation: MDS-0001 Section 3's scope overview still carries older wording naming EBG-0046 as broadly "reserved," while the operative sections already point to DRA-0001 - disclosed as minor future documentation-debt, not a contradiction. Node-side commands (`npm ci`/`build`/`playwright`/`audit`) remained blocked by Codex's own exec-sandbox network policy throughout the session, a disclosed environment limitation, not a repository defect.

**The Programme Sponsor's determination**: **establish a new baseline**, agreeing with Codex's advisory - the session delivered a genuine dependency security remediation (EBG-0085) and a genuine new backend/architecture artefact (DRA-0001), matching the Establish threshold applied at ESR-0049 through ESR-0055.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `package.json` / `package-lock.json` | `vite` `^5.4.11`→`^8.2.2`, `@vitejs/plugin-react` `^4.3.4`→`^6.1.1` - the `esbuild <=0.24.2` dev-server CSRF finding confirmed gone via both `npm audit --omit=dev` and full `npm audit` (0 vulnerabilities). |
| `scripts/validate_repository.py` | `node_modules` added to `IGNORED_DIRS`, closing a pre-existing gap newly tripped by a transitive dependency's README. |
| `aiems/models/DRA-0001_DEVICE_BOOTSTRAP_AND_RESTORE_ARCHITECTURE.md` | New architecture model (Draft) - Device Registry, Bootstrap, Sync Protocol, Progressive Restore, Configuration Portability, cross-referencing MDS-0001's owned areas rather than restating them. |
| [[MDS-0001_MEMORY_AND_DATA_STORAGE_ARCHITECTURE|MDS-0001]] | Sections 8/10/11 forward references repointed from bare "EBG-0046" text to the real DRA-0001 artefact; no requirement/boundary text changed. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0085 closed Complete; EBG-0058 re-verified (status unchanged, Complete); EBG-0046 updated to Drafted. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Sections 6.1/6.3/9 corrected - EBG-0058 and the REG-0001 HST/FCH gap both reflected as resolved; EBG-0052's stale "resolve together" framing removed. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not content-refreshed this session - the Vite/esbuild dependency upgrade (a security/tooling change, not a user-facing capability) and DRA-0001 (a Draft architecture document, not yet an implemented capability) do not immediately warrant a PCB-0001 entry, but the gap is flagged for a future Documentation Debt sync's own judgement.

---

# 7. Architecture Outcomes

- Frontend build tooling (`vite`/`@vitejs/plugin-react`) upgraded to a major version carrying no known dev-server CSRF advisory - a real security posture improvement, verified via a full Playwright E2E pass and both `npm audit` variants against the real upgraded dependency tree.
- A new Platform Services architecture domain (device bootstrap, device registry, sync protocol, progressive restore, configuration portability) is now defined for the first time, completing the decomposition ADR-0012 anticipated and MDS-0001 Section 8 explicitly deferred - no implementation yet exists against it.
- `sentinel/policy.py` and `GAM-0001` Section 8A's `LOCAL_AGENT_ACTION` boundary remain completely untouched.
- No change to `src/`/`src-tauri/` product UXP code - this session's product-moving work (WP1) was a dependency/tooling upgrade, not a UXP feature, per PBK-0001's Feature-First Delivery Discipline's allowance for backend/infrastructure delivery.
- **Disclosed limitation**: DRA-0001 is Draft, not yet formally Accepted - a separate future Programme Sponsor decision, matching MDS-0001's own precedent lifecycle.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no sync transport, database, or conflict-resolution strategy selected for DRA-0001's sync protocol - required properties only, implementation deferred;
- no code implementing bootstrap, device registry, sync, or restore - architecture definition only;
- no PBK-0001 content changed (WP2's own genuine finding - no new duplication to merge);
- no UXP/frontend behavioural change beyond the underlying build-tool version.

---

# 9. Verification

Repository validation performed across ESR-0056's Work Packages and at WP6/WP7:

- Git working tree was clean throughout; the session's content (`f39ff37..HEAD`, 9 commits) pushed to `origin/main`.
- 553 Python tests passing plus 1 correctly-skipped test throughout (unaffected by this session's frontend/documentation-only changes).
- `python scripts/validate_repository.py` (full mode): 0 errors throughout; warning count moved 298→312 across the session (net +14: -1 from the `node_modules` exclusion fix, remainder from new cross-referencing governance prose - all confirmed benign, matching the established pre-existing false-positive pattern).
- `npm ci`/`npm run build`: clean under Vite 8.2.2. `npx playwright test`: 18/18 passed across three confirmatory runs (one initial flaky run, disclosed as a probable environmental one-off, not a Vite 8 regression). `npm audit --omit=dev` and full `npm audit`: both 0 vulnerabilities.
- WP1/WP2/WP3/WP4 design reviews (Codex): Conditional Pass (WP1, WP3, corrections folded in) or Pass (WP2, WP4).
- WP1/WP2/WP3/WP4 post-commit reviews (Codex): Pass (WP1 required one fix round first; WP2/WP3/WP4 Pass on first review).
- Session-wide WP6 (Codex): Pass, no blocking findings, covering the full session diff against RBL-0035.
- Every commit gated through the real AIEMS Exchange Bridge / Sponsor Approval Service (`submit-to-review`/`return-findings`/`submit-response`), including two genuine drift-refusal-and-retry episodes and the diagnosis/fix of a real `~/approve` argument-mapping defect that had been silently mis-filing decisions.
- The Programme Sponsor's own WP7 determination: establish a new baseline rather than retain RBL-0035 (Section 4).

---

# 10. Handover

Future work against this baseline should include:

1. This document and [[RBL-0035_REPOSITORY_BASELINE|RBL-0035]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. DRA-0001's formal acceptance - a separate future Programme Sponsor decision, matching MDS-0001's own precedent.
5. An Engineering Implementation Package implementing DRA-0001's Device Registry and bootstrap flow, once accepted.
6. An Engineering Implementation Package implementing DRA-0001's sync protocol (having chosen a concrete transport/conflict-resolution strategy), once accepted.
7. MOD-0001's "Platform Services" section refresh against ADR-0012's and DRA-0001's actual requirements - disclosed gap, not yet scoped.
8. MDS-0001 Section 3's minor wording debt (still broadly names EBG-0046 as "reserved" despite operative sections pointing to DRA-0001) - non-blocking, flagged at WP6.
9. PCB-0001 refresh for this session's Vite/esbuild upgrade and DRA-0001's creation - not yet reflected there.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0035_REPOSITORY_BASELINE|RBL-0035]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0056_ENGINEERING_SESSION_REPORT|ESR-0056]] | Session this baseline is drawn from. |
| [[EIP-ESR0056-001_ESBUILD_VITE_DEV_SERVER_VULNERABILITY_UPGRADE|EIP-ESR0056-001]] | Approved Engineering Implementation Package WP1's deliverables were built against. |
| [[EIP-ESR0056-002_PBK-0001_ACCRETION_RECHECK_AND_JRM-0001_STALENESS_FIX|EIP-ESR0056-002]] | Approved Engineering Implementation Package WP2 was built against. |
| [[EIP-ESR0056-003_DEVICE_BOOTSTRAP_AND_RESTORE_ARCHITECTURE|EIP-ESR0056-003]] | Approved Engineering Implementation Package WP3's deliverables were built against. |
| [[EIP-ESR0056-004_JRM-0001_REG-0001_HST-FCH_GAP_STALENESS_FIX|EIP-ESR0056-004]] | Approved Engineering Implementation Package WP4 was built against. |
| [[DRA-0001_DEVICE_BOOTSTRAP_AND_RESTORE_ARCHITECTURE|DRA-0001]] | New architecture model created this session, Draft status. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0085 closed Complete; EBG-0058 re-verified; EBG-0046 updated to Drafted. |
| [[JRM-0001_PROJECT_ROADMAP|JRM-0001]] | Two stale reference clusters corrected. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not content-refreshed this session, flagged for future sync. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 4 September 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0035, following Codex design reviews across all four Work Packages (WP1/WP3 Conditional Pass with corrections folded in, WP2/WP4 Pass), verified pre-implementation approvals via the real Sponsor Approval Service, post-commit Codex reviews (WP1 required one fix round, WP2/WP3/WP4 Pass on first review), session-wide WP6 Independent Repository Verification (Pass, no blocking findings), and the Programme Sponsor's explicit WP7 decision to cut a new baseline, agreeing with Codex's own advisory: a genuine dependency security remediation (EBG-0085) and a genuine new architecture artefact (DRA-0001) together warrant a new baseline. |
