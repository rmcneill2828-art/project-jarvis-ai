# ESR-0019 WP6 - Independent Repository Verification Handover

**Status:** Working Report - not a controlled artefact (per PBK-0001 Working Report Lifecycle), not registered in REG-0001.

---

# 1. Purpose

Handover to the Engineering Reviewer (ChatGPT) for **WP6 Independent Repository Verification** of ESR-0019 WP2 and its follow-on work, per PBK-0001's Repository Lifecycle and TPL-0001 Section 22. WP1 (role-binding update, commit `1c1c7e9`) already went through its own WP6/WP7 earlier in this session - see the Version History table in [[ESR-0019_ENGINEERING_SESSION_REPORT|ESR-0019]] for that record. This handover covers everything after it.

This is not a re-review of the design decisions themselves (the WP2 EIP - EIP-ESR0019-002 Revision 2 - already went through your pre-implementation review earlier). WP6 is a check that what was pushed actually matches what was claimed, that the disclosed deviations below are accurately characterised, and that the repository is in a coherent, testable state.

---

# 2. Repository Access

| Field | Value |
|---|---|
| Repository | `https://github.com/rmcneill2828-art/project-jarvis-ai.git` |
| Branch | `main` |
| Expected `HEAD` | `b86f799f6083e943ab57ba8049e95ffd13ffc111` |
| Confirmed | Local `HEAD` and `origin/main` both resolve to this SHA (checked immediately before writing this handover) |
| Prior baseline | [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] at `1c1c7e9` (WP1's own WP7 acceptance point) |

**First action: confirm this SHA is what GitHub actually shows for `main`.**

---

# 3. The Commits (in push order, all after WP1's `1c1c7e9`)

| # | SHA | One-line summary |
|---|---|---|
| 1 | `abbae2e` | Exclude `src-tauri/target` from Vite's dev-server file watcher (unrelated dev-environment fix, found while attempting live verification) |
| 2 | `3f68c86` | EBG-0055 Phase 1: knowledge-graph backend (`jarvis/interfaces/knowledge_graph.py`), `knowledge.graph` JSON-RPC method, first-pass standalone panel rendering |
| 3 | `89125f3` | Fix: edges invisible (forceLink mutation bug) + most nodes clipped outside the viewBox (outlier normalization bug) |
| 4 | `f04b12c` | Add degree-based node sizing and hub text labels (Obsidian reference) |
| 5 | `4f5ac99` | Fix: outlier drift collapsing the graph into a central clump (needed a real per-node centering force, not just `forceCenter`) |
| 6 | `6e6dbe7` | Remove hub text labels (Programme Sponsor decision - cluster colour sufficient) |
| 7 | `2bdf3c5` | **Guardian Orb integration**: the standalone panel is replaced - the Orb itself becomes the live knowledge graph (`src/GuardianOrbGraph.jsx`), per UAM-0001 8.1 and the `aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg` reference. Also fixes the hardcoded "Richard" placeholder name to Robert. |
| 8 | `4d71983` | Fix: sphere rendered off-centre/lopsided (centering force strength insufficient at the orb's smaller scale) |
| 9 | `f468418` | Remove the "Guardian"/"AI Companion" text label from inside the orb (Programme Sponsor decision) |
| 10 | `f0e47e5` | Governance: mark [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0055 Completed (Phase 1), recording what was actually delivered |
| 11 | `b86f799` | Governance: new PBK-0001 clause, "Incremental Visual Convergence Toward the Reference Mock-up" (Programme Sponsor-directed standing practice) |

**Why so many commits for one Work Package:** this was live, iterative pair-engineering - each fix was found from the Programme Sponsor's own screenshot of the running app, root-caused against the real repository data (148 nodes, 1220 edges) via disposable debug scripts before being applied, and validated (`pytest`, `validate_repository.py`, `npm run build`) before every commit. Commits 3-9 are a connected chain of real, disclosed bugs and Sponsor-directed design changes on the same feature, not scope drift - full narrative is in [[ESR-0019_ENGINEERING_SESSION_REPORT|ESR-0019]] Section 11.

---

# 4. Disclosed Deviations From the Reviewed EIP

The approved package (EIP-ESR0019-002 Revision 2) covered commit `3f68c86` only. Everything from `89125f3` onward is **beyond that reviewed package**, each individually confirmed by the Programme Sponsor in conversation before implementation (screenshot -> diagnosis -> fix -> re-screenshot, repeated). Specifically flagged for your independent confirmation, not just acceptance:

1. **`3f68c86` itself** contains one self-identified fix beyond the reviewed design: three git-tracked files share the stem `README` (root, `scripts/`, `logs/chats/`); a bare-stem node id would have collided them into one node. Fixed by using repo-relative paths as node ids and resolving ambiguous WikiLink targets to the shallowest match - covered by `test_ambiguous_stem_resolves_to_shallowest_file`.
2. **`2bdf3c5`** is the largest undisclosed-at-review-time change: it removes `src/KnowledgeGraph.jsx` entirely and repurposes the Guardian Orb's own visual slot (previously a static glow/ring/text animation) to show the graph. This was a Programme Sponsor decision made live in conversation (not a pre-implementation-reviewed EIP), directly citing `aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg` and UAM-0001 Section 8.1's original design intent.
3. **Commits 3, 5, 8** (`89125f3`, `4f5ac99`, `4d71983`) are all layout-parameter bug fixes found and fixed reactively from screenshots, each with its own before/after verification against the real graph data recorded in the commit message - worth spot-checking that the stated numbers (e.g. "337 overlapping pairs down to 20", "centroid offset 44px to 5.4px") are plausible given the diffs, not just asserted.
4. **`f0e47e5`/`b86f799`** are governance-only and were not pre-reviewed by you before being written - they record decisions already made in conversation (EBG-0055 completion, the new PBK-0001 clause) rather than proposing new ones.

---

# 5. Validation Evidence (re-run immediately before this handover)

| Check | Result |
|---|---|
| `pytest` (full suite) | 204/204 passing (192 baseline + 12 new), 0 regressions |
| `python scripts/validate_repository.py` | 0 errors, 83 warnings (pre-existing set, +1 from ESR-0019's own draft report referencing a cross-artefact section - same class of warning as ~80 others already in the repository) |
| `cargo check` (`src-tauri`) | Clean, 0 errors/warnings |
| `npm run build` | Clean production build |
| Backend end-to-end | `knowledge.graph` verified via the real `python -m jarvis --ipc-stdio` entrypoint (the exact process the Tauri sidecar spawns), returning real repository data |

**Not independently verified by the Engineering Implementer in this environment:** the actual rendered browser window - no display/window-automation tooling is available in this environment. All visual verification in this session came from the Programme Sponsor's own screenshots of `npm run tauri dev` running on their machine, which is how commits 3, 5, 8 above were found and confirmed fixed.

---

# 6. Scope Check

- `dist/` and `src-tauri/target/` build artefacts: confirmed gitignored throughout, never staged.
- No changes to `scripts/validate_repository.py` itself.
- No Phase 2 (cluster-illumination semantics), Phase 3 (agent-traversal animation) or Phase 4 (Guardian reasoning connection) work - EBG-0055's own phase boundaries were respected throughout, including the explicit decision to defer true 3D/animation to a future session.

---

# 7. WP7 Baseline Recommendation

Unlike WP1 (small governance text change, RBL-0013 retained per the ESR-0016 precedent), this Work Package delivered a genuinely new product capability - a live backend graph endpoint and a materially changed UXP hero element - plus a new governance clause. **Recommend a new repository baseline (RBL-0014)** rather than retaining RBL-0013, but this remains the Programme Sponsor's WP7 decision, not a recommendation either of us can finalise.

---

# 8. What WP6 Should Produce

A recommendation to the Programme Sponsor: accept this repository state for WP7 baseline acceptance, or send something back for rework, plus any findings.

---

# 9. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0019_ENGINEERING_SESSION_REPORT|ESR-0019]] | This session's full report; Section 11 has the complete extended-work narrative. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0055 marked Completed (Phase 1) at `f0e47e5`. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | New clause added at `b86f799`. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Section 8.1 is the design authority the Guardian Orb integration implements. |
| [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] | Prior accepted baseline, WP1's acceptance point. |
