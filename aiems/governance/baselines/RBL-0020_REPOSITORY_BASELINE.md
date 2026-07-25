# RBL-0020 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0020 |
| Title | ESR-0033 Repository Baseline (Documentation Debt, Theme 7 Cleanup, UXP Memory Row, Security Hygiene, and AIEMS Tooling Fixes) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | ESR-0033 (in progress - no session report artefact exists yet, per established practice) |
| Previous Baseline | [[RBL-0019_REPOSITORY_BASELINE|RBL-0019]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 25 July 2026 |
| HEAD at baseline creation | `700a670` |

---

# 2. Purpose

RBL-0020 records the repository baseline accepted by the Programme Sponsor at ESR-0033 WP9, superseding [[RBL-0019_REPOSITORY_BASELINE|RBL-0019]]. ESR-0033 ran seven Work Packages: WP1 (documentation debt - stale repository-baseline references across README.md/PBK-0001/COC-0001/REG-0001), WP2 (Theme 7 cleanup - Codex-led independent triage closing 16 of 23 dormant AIEMS governance/standards backlog items), WP3 (EBG-0100 - the UXP Memory row wired to live `platform.status` data), WP4 (Theme 5 Security Hygiene batch - `.aiems-exchange/` permission enforcement, GitHub Actions SHA pinning, `.env` gitignore entry, CSP `unsafe-inline` removal), WP5 (EBG-0107 - `session_launcher.py`'s missing Next Work Package Candidate / EBR-0001 Section 5A output fixed), WP6 (EBG-0098/0105 - version badge/table drift detection and transcript filename microsecond resolution), and WP7 (EBG-0101 - `bump_version.py`'s stale `--date` default fixed). Both independent WP8 views (Engineering Implementer and Engineering Reviewer) converged on this being baseline-worthy, citing WP3's live product-behaviour change and WP4's material security-posture improvement as the combined justification beyond pure governance churn.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0019_REPOSITORY_BASELINE|RBL-0019]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - not refreshed this session; WP3's Memory-row change makes an existing capability's status visible in the live UXP rather than adding a new product capability tier, so no PCB-0001 update was in scope |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for continued ESR-0033 work or a future session |

---

# 4. Baseline Recommendation Rationale

The [[ESR-0033_WP8_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP8 handover]] recorded two independently-reached views (Sections 9-10), both recommending a new baseline rather than retaining RBL-0019.

**Engineering Implementer's view**: while five of the seven Work Packages were governance/tooling work, WP3 delivered a genuine, live-verified product capability change - the UXP Memory row now reflects real backend state instead of a hardcoded placeholder, closing a real user-visible gap that had existed since Personal Memory was implemented at ESR-0027. WP4's security hardening (real CI-verified GitHub Actions SHA pinning, a genuinely narrower CSP with no `unsafe-inline`, real POSIX filesystem permission enforcement) is also a material, externally-motivated change to the product's actual security posture, not merely internal tooling. Combined with WP2's substantial backlog-register cleanup and the tooling fixes in WP5-WP7 that make the AIEMS process itself more trustworthy, this session's cumulative effect on both the product and the engineering process is substantive enough to warrant a new baseline.

**Engineering Reviewer's (Codex) independent view**: converged - citing WP3's live product-behaviour change, WP4's material security-posture improvement, and WP5-WP7's real process-tooling defect fixes as combined justification beyond pure governance churn. Codex independently confirmed the exact diff-stat figures (26 files, 752 insertions, 152 deletions), the file-list accuracy, that no `sentinel/` trust-boundary changed, and that `scripts/aiems_bridge.py`'s only change was the additive `_restrict_to_owner()` helper with no change to approval/decision-fetching logic, before reaching this view.

**The Programme Sponsor's determination**: **establish a new baseline**, agreeing with both independent views.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `README.md`, [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]], [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]], [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Stale RBL-0017/RBL-0018/RBL-0011/RBL-0010 repository-baseline references corrected to RBL-0019 (WP1), across three Codex review passes each catching a genuine additional miss. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | 16 of 23 Theme 7 dormant governance/standards items closed via Codex-led independent triage (WP2); EBG-0100/0086/0087/0088/0089/0107/0098/0105/0101 all closed across WP3-WP7; Section 5A regenerated five times as items closed (57 to 30 open items across the session). |
| `jarvis/interfaces/stdio_rpc.py`, `src/App.jsx`, `src/platformStatus.js` | `platform.status` gained a `memoryConnected` field; the live UXP Memory capability row now derives from it using the same pattern as Sentinel/Providers, closing EBG-0100 (WP3). |
| `scripts/aiems_bridge.py` | New `_restrict_to_owner()` helper (`os.chmod 0o700`) restricts `.aiems-exchange/` to owner-only access on POSIX at creation, closing EBG-0086 (WP4). |
| `.github/workflows/ci.yml`, `.github/workflows/release.yml` | All five third-party GitHub Actions pinned to independently-verified commit SHAs, closing EBG-0087 (WP4); live-verified via real green GitHub Actions runs at every subsequent push. |
| `.gitignore` | `.env`/`.env.*` entries added, closing EBG-0088 (WP4). |
| `src/KnowledgeGraphPanels.jsx`, `src-tauri/tauri.conf.json` | Repository's only inline style usage migrated to a CSSOM property-setter pattern; Tauri CSP narrowed to `style-src 'self'`, closing EBG-0089 (WP4). |
| `scripts/session_launcher.py` | `CurrentState` gained `next_wp_candidate`; new `read_active_backlog_snapshot()` reads EBR-0001 Section 5A directly; closes EBG-0107 (WP5), live-verified against the real repository. |
| `scripts/validate_repository.py` | New `check_version_badge_table_consistency()` closes EBG-0098 (WP6) - a live run immediately found and required fixing a genuine false positive against FCH-0000's raw pasted-transcript content. |
| `jarvis/gui/app.py` | New `_transcript_filename()` helper (microsecond resolution) closes EBG-0105 (WP6). |
| `scripts/bump_version.py` | `--date` now defaults to a computed today's date rather than a stale hardcoded placeholder, closing EBG-0101 (WP7) - self-demonstrated live by the commit that recorded its own closure. |
| Test suite | 374 tests plus 1 skip, up from RBL-0019's 359 - 15 net-new tests (1 win32-conditional skip on this Windows machine); no regressions. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] was not refreshed this session. WP3's Memory-row fix makes an already-implemented capability (Personal Memory, delivered at ESR-0027) visible correctly in the live UXP - it does not add a new product capability tier PCB-0001 needs to record, since Memory was already tracked there as Partial/implemented.

---

# 7. Architecture Outcomes

- The UXP Capability Sidebar's Memory row is now genuinely live-data-backed for the first time, closing a gap that had silently under-claimed a real, already-shipped capability since ESR-0027.
- The AIEMS Exchange Bridge's working directory now has a real, code-enforced permission restriction on POSIX systems, closing a documented-but-unenforced convention gap.
- This repository's CI/CD supply chain is now hardened against third-party Action tag mutation - all five Actions used across both workflows are pinned to commit SHAs, independently verified against each real upstream repository, with `dtolnay/rust-toolchain` specifically re-architected to preserve auto-tracking of current stable Rust while still gaining SHA-pin protection for the Action's own code.
- The Tauri application's Content-Security-Policy no longer requires `'unsafe-inline'` for styles - the repository's only inline style usage was migrated to a CSSOM property-setter pattern that achieves the same dynamic behaviour without weakening the policy.
- The AIEMS Session-Opening Launcher now genuinely serves its own stated purpose (informing WP0B objective selection) for the first time since its own gap was discovered post-ESR-0031 - live-verified against this repository's real current governance state, not just fixture tests.
- `validate_repository.py` gained a new class of check (version badge/table consistency) that found a real defect on its very first live run against the real repository.
- `bump_version.py` no longer silently mis-dates Version History rows when `--date` is omitted - a defect that had already caused real dating errors in a prior session's commits.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no new ESR-0034 artefact is created by this baseline - ESR-0033 remains open pending formal session closure;
- EBG-0085 (esbuild/vite dev-server vulnerability, a breaking Vite 8 upgrade) remains explicitly deferred to a future dedicated EIP, not addressed by this baseline;
- the 7 remaining Theme 7 items (EBG-0008/0011/0038/0040/0061/0066/0067) and all other open EBR-0001 backlog items remain out of scope, not addressed by this baseline;
- no new third-party product dependencies were introduced this session;
- `sentinel/` was not touched at all this session - no trust-boundary change of any kind.

---

# 9. Verification

Repository validation performed during ESR-0033 WP8/WP9:

- Git working tree was clean; the session's intended content range (`c62e361`..`07cac41`) pushed to `origin/main`.
- Repository branch was `main`, synchronised with `origin/main` at every commit in the session (confirmed via real GitHub Actions CI runs at WP4, WP5, WP6 and WP7's push points - all four jobs green each time, not assumed).
- 374/374 tests passing plus 1 correctly-skipped win32-conditional test, up from RBL-0019's 359 (15 net-new tests; no regressions).
- `python scripts/validate_repository.py` (full mode) passed with 0 errors, 152 warnings (three more than RBL-0019's 149, all confirmed to be the same pre-existing false-positive class introduced by this session's own new cross-document changelog prose, not a new class of problem).
- `ruff check .` clean.
- `npm run build` clean.
- `npx playwright test` - 2/2 passing.
- `git diff --stat c62e361..07cac41` independently re-run by the Engineering Reviewer, confirmed to match exactly (26 files, 752 insertions, 152 deletions).
- Real GitHub Actions CI green across all four jobs (`python`, `rust`, `playwright`, `frontend-build`) at every CI-relevant push this session (WP4, WP5, WP6, WP7).
- The Engineering Reviewer performed WP8 Independent Repository Verification: **Pass, no blocking findings** - independently confirmed the diff-stat figures, file-list accuracy, the `sentinel/` boundary, and that `scripts/aiems_bridge.py`'s scope was limited to the additive permission helper.
- The Programme Sponsor's own WP9 determination: establish a new baseline rather than retain RBL-0019 (Section 4).

---

# 10. Handover

**This baseline does not itself close ESR-0033** - the Engineering Session Report remains to be authored separately, following this baseline's acceptance, per established practice.

Future work against this baseline should include:

1. This document and [[RBL-0019_REPOSITORY_BASELINE|RBL-0019]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for this baseline's acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] - EBG-0100/0086/0087/0088/0089/0107/0098/0105/0101 all Complete, plus 16 Theme 7 items.
5. The [[ESR-0033_WP8_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|WP8 handover]] for full delivery detail.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[RBL-0019_REPOSITORY_BASELINE|RBL-0019]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0033_WP8_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0033 WP8 Handover]] | Independent verification record this baseline's acceptance is drawn from. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - not affected by this session's scope. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, to be updated for this baseline's acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register; 25 items closed this session across WP2-WP7. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 25 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0019, following the Engineering Reviewer's WP8 Pass and the Programme Sponsor's explicit WP9 decision to cut a new baseline rather than retain RBL-0019: WP3's live UXP Memory-row change, WP4's material security-posture improvement, and WP5-WP7's real process-tooling fixes together warrant a new baseline, agreeing with both independent WP8 baseline views. |
