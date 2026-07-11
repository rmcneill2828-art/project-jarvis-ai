# ESR-0019 - Engineering Session Report

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | ESR-0019 |
| Title | Engineering Session Report |
| Version | 1.5 |
| Status | Closed |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Approved By | Programme Sponsor |
| Classification | Internal |
| Session | ESR-0019 |
| Date Opened | 11 July 2026 |
| Date Closed | 11 July 2026 |
| Closure Status | Closed |
| Final Validation | 204 / 204 tests passing, 0 validator errors |

---

# 2. Purpose

This report records the opening and execution of ESR-0019, the first Engineering Session run under the permanent Lead/Reviewer appointment established at [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7 and closed at [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]]: Claude as permanent Engineering Implementer (Lead Engineer), ChatGPT as permanent Engineering Reviewer (Lead Reviewer), Programme Sponsor gating every step.

---

# 3. Scope

ESR-0019's approved session objective (confirmed by the Programme Sponsor at WP0B):

1. **WP1** - Update [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] to reflect the permanent Lead/Reviewer appointment concluded at ESR-0018, binding Engineering Implementer to Claude and Engineering Reviewer to ChatGPT, while preserving the underlying role-definition-not-vendor principle as the documented default should the appointment ever change.
2. **WP2** (if time allows) - [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0055 (Knowledge Graph Phase 1 - Static Live Graph), per its candidate slot of ESR-0018 or ESR-0019.

No Work Package beyond these two is authorised at session opening. Each Work Package requires its own Engineering Implementation Package and Programme Sponsor approval before implementation begins.

---

# 4. Engineering Authority

ESR-0019 opening was authorised by Programme Sponsor instruction on 11 July 2026, following WP0A Repository Synchronisation confirming [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] was formally closed and [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] remains the accepted repository baseline.

GitHub and the repository remain the authoritative source of truth.

---

# 5. Session Objective

Execute WP1 (PBK-0001/COC-0001 role-binding update) as the session's first Programme Sponsor-approved Engineering Work Package, then WP2 (EBG-0055) if capacity and Sponsor approval allow.

---

# 6. Work Package Plan

| Work Package | Description | Status |
|---|---|---|
| WP0 | Repository synchronisation and session activation | Complete - see Section 8 |
| WP1 | PBK-0001/COC-0001 role-binding update | Complete - WP0-WP7 closed (commit `1c1c7e9`, RBL-0013 retained) |
| WP2 | EBG-0055 - Knowledge Graph Phase 1 (Static Live Graph), extended into the Guardian Orb integration | Complete, EBG-0055 marked Completed (Phase 1) - WP6/WP7 pending |

---

# 7. Architectural Milestones

- First Engineering Session opened under the permanent, non-alternating Lead/Reviewer appointment (no EE-0001 trial rotation to confirm).

---

# 8. WP0 Session Initialisation Record

**WP0A - Repository Synchronisation** (per [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] and [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] knowledge tiering):

- README.md reviewed for repository orientation and platform context.
- [[PST-0001_PROGRAMME_STATUS|PST-0001]] (v2.25) reviewed: Current State confirms ESR-0018 closed, RBL-0013 accepted, permanent Claude Lead Engineer / ChatGPT Lead Reviewer appointment made 10 July 2026.
- [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] (Current ESR tier) reviewed in full.
- [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] reviewed; Architecture tier referenced from PST-0001 not required in depth for WP1 (governance-only change).
- [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] (v1.19) and [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] (v1.11) reviewed; both confirmed to still describe Engineering Implementer/Reviewer generically, not bound to a specific AI - the gap this session's WP1 addresses.
- Repository state verified directly: `git status` clean, `main` up to date with `origin/main`, pre-commit hook active (`core.hooksPath = scripts/hooks`). HEAD (`f79a01f`) is 3 commits ahead of ESR-0018's closure commit (`12d1fa1`) - all three are governance-only `EBR-0001`/`REG-0001` updates recording post-closure EBG-0057 research; no session was opened for these and none is required retroactively.
- [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0055 entry reviewed for WP2 candidate scope.

**WP0B - Engineering Session Initialisation:**

- Next planned Engineering Session identifier: ESR-0019.
- Active Engineering Session: ESR-0019 (this report).
- Programme phase: Phase 2 - JARVIS Architecture Readiness (continuing).
- Repository baseline reference: [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]].
- Initial session objective: confirmed by Programme Sponsor - see Section 3.
- Planned engineering activities: WP1 (role-binding update), WP2 (EBG-0055) if time allows.
- Programme Sponsor approval of WP0B session opening: obtained 11 July 2026. Per-Work-Package approval remains separately required before each WP's implementation begins.

---

# 9. WP1 Completion Record

**Engineering Implementation Package:** EIP-ESR0019-001, approved by the Programme Sponsor 11 July 2026, following Engineering Reviewer (ChatGPT) pre-implementation review (scope confirmed appropriate; one non-blocking consistency-drift observation raised and accepted as a future follow-up, not part of this WP).

**Files modified:**
- `aiems/governance/conversation/COC-0001_HUMAN_AI_COLLABORATION_CONTEXT.md` (v1.11 to v1.12)
- `aiems/governance/playbooks/PBK-0001_AI_ENGINEERING_PLAYBOOK.md` (v1.19 to v1.20)
- `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md` (v3.113 to v3.115, synced via `scripts/bump_version.py`)

**Summary of content:** Both artefacts' Engineering Reviewer / Engineering Implementer role descriptions now state the current permanent holder (ChatGPT / Claude respectively) per the [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] Section 7 appointment (10 July 2026), while preserving the pre-existing "role definition, not the specific AI product, is authoritative" sentence as the standing default. No renaming of role terms; no change to GDE-0001.

**Validation performed:** `python scripts/validate_repository.py --governance-only` run before and after commit - 0 errors, 82 pre-existing warnings (unchanged set, unrelated to this change).

**Self-review findings:** Diff scoped to exactly the three authorised files; no unrelated files modified; ESR-0019 report itself correctly excluded from this commit (stays untracked until session closure, per the ESR-0018 precedent).

**Repository execution:**
- Commit SHA: `1c1c7e9`
- Commit message: "Bind Engineering Implementer/Reviewer roles to the permanent EE-0001 appointment (PBK-0001, COC-0001)"
- Repository status: pushed to `origin/main` (`f79a01f..1c1c7e9`); working tree clean aside from this untracked report.

**WP6 Independent Repository Verification:** Pass, performed by the Engineering Reviewer (ChatGPT), 11 July 2026 - confirmed commit `1c1c7e9` pushed, `main`/`origin/main` aligned, diff scoped to exactly the three expected files, both artefacts' role-binding text and generic-role caveat correctly present, REG-0001 change consistent with the `bump_version.py` sync workflow, ESR-0019 draft correctly excluded. No implementation error found.

**WP7 Repository Baseline Acceptance:** Granted by the Programme Sponsor, 11 July 2026. [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] is **retained** - WP1's change judged incremental, not warranting a new baseline, consistent with the ESR-0016/ESR-0018 precedent.

**Outstanding:** The consistency-drift observation (other artefacts' role-related references may still read generically) is logged as a candidate future item, not actioned by WP1. WP1 is fully closed (WP0-WP7 complete).

---

# 10. WP2 Completion Record

**Engineering Implementation Package:** EIP-ESR0019-002 (Revision 2 + the repo-root cwd-independence regression test recommendation), approved by the Programme Sponsor 11 July 2026, following two rounds of Engineering Reviewer (ChatGPT) pre-implementation review. Round 1 raised three findings (High: repo-root/cwd dependence; Medium: WikiLink parser parity/edge-case handling; Medium: node identity stability) - all addressed in Revision 2, which the Reviewer confirmed cleared with one non-blocking recommendation (a cwd-independence regression test), accepted into scope.

**Files created:**
- `jarvis/interfaces/knowledge_graph.py` - graph builder: `git ls-files`-based enumeration anchored to `Path(__file__)` (not process cwd), explicit alias/duplicate/malformed/self-link/unresolved-link handling, repo-relative-path node ids, first-H1-heading labels.
- `jarvis/tests/test_knowledge_graph.py` - 11 tests covering the full parity/edge-case matrix plus both repo-root/cwd regression tests.
- `src/KnowledgeGraph.jsx` - first-pass static SVG force-directed rendering (`d3-force`, bounded synchronous simulation, not an animated/running one).

**Files modified:**
- `jarvis/interfaces/stdio_rpc.py` / `jarvis/tests/test_stdio_rpc.py` - registered `knowledge.graph` JSON-RPC method, added dispatch test.
- `src-tauri/src/lib.rs` - added `knowledge_graph` Tauri command mirroring `platform_status`.
- `src/App.jsx` / `src/styles.css` - wired the live call and rendered panel into the UXP layout.
- `package.json` / `package-lock.json` - added `d3-force` (MIT, no recurring cost).

**Beyond the reviewed package, disclosed:** during implementation, discovered that three git-tracked files share the stem `README` (root, `scripts/`, `logs/chats/`) - a bare-stem node id would have silently collided three distinct artefacts into one node. Fixed by making node `id` the repo-relative path (always unique) and resolving ambiguous WikiLink targets to the shallowest matching file, which is what every one of the repository's dozens of existing `[[README|README]]` links already means. Added a dedicated regression test (`test_ambiguous_stem_resolves_to_shallowest_file`). This stayed within WP2's approved objective (accurate graph nodes/edges) rather than expanding scope.

**Validation performed:**
- `pytest` (full suite): 204/204 passing (192 baseline + 12 new: 11 in `test_knowledge_graph.py`, 1 dispatch test in `test_stdio_rpc.py`), 0 regressions.
- `python scripts/validate_repository.py`: 0 errors, 82 pre-existing warnings (unchanged set).
- `cargo check` (src-tauri): clean, 0 errors/warnings.
- `npm run build`: clean production build.
- Backend verified end-to-end through the real `python -m jarvis --ipc-stdio` entrypoint (the exact process the Tauri sidecar spawns), sending real JSON-RPC requests and confirming `knowledge.graph` returns real repository data (148 nodes, 1220 edges).
- **Verification gap, disclosed:** the rendered browser window itself was not screenshotted or interactively driven - no display/window-automation tool was available in this environment (unlike ESR-0017 WP9, verified through a real windowed Tauri session). A live windowed check by the Programme Sponsor (`npm run tauri dev`) remains outstanding before this can be considered fully verified to the ESR-0017 WP9 standard.

**Self-review findings:** diff scoped to exactly the files listed above (plus the disclosed README-collision fix); no unrelated files modified; `dist/` and `src-tauri/target/` build artifacts correctly gitignored, not staged.

**Repository execution:**
- Commit SHA: `3f68c86`
- Commit message: "Implement EBG-0055 Phase 1: repository knowledge-graph backend and first-pass UXP rendering"
- Repository status: pushed to `origin/main` (`1c1c7e9..3f68c86`); working tree clean aside from this untracked report.

**Outstanding:** WP6 Independent Repository Verification and WP7 Repository Baseline Acceptance (both pending). Phase 2 (cluster-illumination semantics), Phase 3 (agent-traversal animation) and Phase 4 (Guardian reasoning connection) remain future EBG-0055 work, not this WP's scope.

---

# 11. WP2 Extended Work - Guardian Orb Integration

Following commit `3f68c86`, the Programme Sponsor drove several rounds of live iteration on the delivered rendering, each confirmed before implementation. Recorded here as a single extended-work log rather than one subsection per commit, per Feature-First Delivery Discipline.

1. **Dev environment fix, unrelated to WP2 content** (`abbae2e`): the Programme Sponsor's first attempt to run `npm run tauri dev` failed with `EBUSY` - Vite's dev-server file watcher was also watching `src-tauri/target/`, and a Windows file lock on an in-progress `cargo build` `.dll` crashed it. Fixed by adding the standard Tauri v2 + Vite scaffolding exclusion (`server.watch.ignored: ["**/src-tauri/**"]`) that this repository's `vite.config.js` had been missing since it was first created.
2. **Invisible edges + node clustering fix** (`89125f3`): the Programme Sponsor's first screenshot showed ~15 of 148 nodes visible with no edges at all. Root-caused to two real bugs: (a) `graph.edges` (component state) was passed directly into `forceLink()`, which mutates link `source`/`target` from string ids to node object references in place, breaking the render function's later Map lookup by string id; (b) the simulation's natural equilibrium spread was far larger than the fixed viewBox, so most nodes landed outside it and were clipped. Fixed by copying edges before passing to `forceLink`, and rescaling converged positions into the viewBox afterward (independently per axis, verified against the real graph: 337 overlapping node pairs down to 20 out of 10,878 possible pairs).
3. **Hub sizing and labelling** (`f04b12c`): per the Programme Sponsor's screenshot of Obsidian's own graph view for this repository, added degree-based node sizing and text labels for the top 25 most-connected nodes.
4. **Outlier-drift fix** (`4f5ac99`): the sizing change revealed nodes crushed into a tiny central clump - `forceCenter` alone doesn't stop individual low-degree nodes drifting arbitrarily far under repulsion (confirmed: 16 of 148 nodes beyond 3x median distance from centroid, dominating the viewBox rescale). Fixed with a real per-node centering force (`forceX`/`forceY`), matching Obsidian's own "Centre force" setting, which the Programme Sponsor shared as a reference.
5. **Label removal** (`6e6dbe7`): the hub labels overlapped unreadably in the densely-interlinked centre. Programme Sponsor decision: remove labels entirely rather than tune further - cluster colour coding is sufficient, full labels remain on hover, Obsidian is available separately for detail.
6. **Guardian Orb integration** (`2bdf3c5`): Programme Sponsor decision, informed by `aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg` (the actual reference mock-up image), that the Orb's visual presence should be the live knowledge graph itself, not a separate panel - matching UAM-0001 Section 8.1's original design intent. New `src/GuardianOrbGraph.jsx`: the existing 2D force layout, confined to a circle via a custom hard-boundary containment force, given a deterministic hemisphere depth projection (`z = sqrt(1 - r^2)`, the orthographic silhouette of a sphere) for a parallax-sphere illusion - entirely geometric and data-driven, not a physics engine or WebGL scene, and not decorative animation. The standalone panel (`src/KnowledgeGraph.jsx`) was removed as superseded.
7. **Off-centre clump fix** (`4d71983`): the first orb screenshot showed the sphere lopsided in one quadrant. Confirmed against the real graph: the centering force strength carried over from the panel (0.1) left the centroid 44px off true centre out of a 140px radius - the tightly-interlinked hub cluster's mutual attraction is strong enough to settle as a rigid off-centre clump at that strength. Raised to 0.5: centroid offset 5.4px, balanced angular distribution across 8 sectors, 0 overlap.
8. **Orb label removal** (`f468418`): Programme Sponsor decision to remove the "Guardian" / "AI Companion" text overlay entirely, leaving only the live graph inside the orb. Removed the dead `orb-label` CSS and the now-unused `guardianStatus.title` data field; repointed the section's accessibility label from `aria-labelledby` (which pointed at the removed heading) to a direct `aria-label`.
9. **Name correction** (included in `2bdf3c5`): the hardcoded placeholder greeting name "Richard" (two locations: `platformStatus.js` greeting, `App.jsx` profile card) corrected to Robert, the actual Programme Sponsor.
10. **Backlog record** (`f0e47e5`): [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0055 marked Completed (Phase 1), recording the Guardian Orb delivery and explicitly flagging true 3D rendering and live animation as deferred next candidates - the Programme Sponsor's own framing being that this need not be perfect on the first pass.

Each step above was verified against the real repository data (148 nodes, 1220 edges) via disposable debug scripts before being applied to the production component, and each iteration ran the full validation suite (`pytest`, `validate_repository.py`, `npm run build`) before commit - consistent with Operational Verification Before Reporting.

11. **New standing practice adopted** (`b86f799`): Programme Sponsor proposed, and PBK-0001 was updated to record, "Incremental Visual Convergence Toward the Reference Mock-up" under Feature-First Delivery Discipline - future Engineering Sessions should include a small UXP change moving toward `aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg` where that session's work provides a natural opportunity, split into freely-adjustable cosmetic elements versus data-bearing elements that may only match the mock-up once backed by real observed data (preserving the ESR-0017 WP9 no-mock-fallback rule).

**Outstanding for a future session:** true 3D rendering (real depth/rotation) and live animation, explicitly deferred by Programme Sponsor decision.

---

# 12. WP2 WP6/WP7 Closure Record

**WP6 Independent Repository Verification:** Pass, performed by the Engineering Reviewer (ChatGPT), 11 July 2026, per [[ESR-0019_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|the WP6 handover]] (commit `2dbe1d1`). Verified `pytest` (204/204), `python scripts/validate_repository.py` (0 errors, 85 warnings) and `npm run build` (clean) independently; confirmed `HEAD` matched the handover's stated `b86f799` with the eleven commits since WP1's closure exactly as described; no blocking implementation defect found in `jarvis/interfaces/knowledge_graph.py`, `src/GuardianOrbGraph.jsx` or the `src-tauri/src/lib.rs` bridge wiring. Two Low, non-blocking findings: the handover's own validation snapshot (83 warnings, 148 nodes/1220 edges) reads stale once the handover document itself joins the tracked corpus (85 warnings, 149 nodes/1225 edges) - an inherent, self-referential property of any handover document, not a defect.

**WP7 Repository Baseline Acceptance:** Granted by the Programme Sponsor, 11 July 2026. **[[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] accepted**, superseding [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] - both the Engineering Implementer and the Engineering Reviewer's WP6 recommended a new baseline given the scale of delivered capability (a new backend endpoint and a materially changed UXP hero element), unlike WP1's incremental role-binding change. Full baseline record in [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]].

WP1 and WP2 are both now fully closed (WP0-WP7 complete for each). ESR-0019 itself is closed.

---

# 13. Closure Statement

ESR-0019 is closed. This was the first full Engineering Session run under the permanent Lead/Reviewer appointment concluded at ESR-0018 (Claude Engineering Implementer / Lead Engineer, ChatGPT Engineering Reviewer / Lead Reviewer). WP1 formally bound that appointment into PBK-0001 and COC-0001, closing a gap flagged as outstanding at ESR-0018 closure. WP2 delivered [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0055 Phase 1 - a repository knowledge-graph backend and JSON-RPC method - and grew, through direct Programme Sponsor iteration against a real running application, into the Guardian Orb's actual visual presence: the Orb now renders the live knowledge graph as a sphere, per [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8.1's original design intent, closing a gap first identified at ESR-0010 and formally recorded at ESR-0017. A new standing PBK-0001 practice - Incremental Visual Convergence Toward the Reference Mock-up - was adopted to keep this kind of convergence happening incrementally across future sessions.

Both Work Packages were independently verified (WP6 Pass for each) and accepted by the Programme Sponsor (WP7): WP1's incremental change retained [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]]; WP2's materially larger delivery is recorded in the new [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]], the current accepted repository baseline.

**Recommended focus for the next session**: candidates remain [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0056 (PCB-0001 refresh, now more materially stale given the Guardian Orb delivery), EBG-0057 (Claude&harr;Codex bridge), or continuing EBG-0055 into true 3D rendering/animation as explicitly deferred by the Programme Sponsor this session. All offered as candidates, not a mandate - engineering priorities remain a Programme Sponsor decision.

---

# 14. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0018_ENGINEERING_SESSION_REPORT|ESR-0018]] | Prior closed session; concluded the EE-0001 trial with the permanent appointment this session's WP1 formalises in PBK-0001/COC-0001. |
| [[EE-0001_INDEPENDENT_AI_PEER_REVIEW_TRIAL|EE-0001]] | Section 7 records the permanent appointment decision this session's WP1 implements. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | WP1 target artefact. |
| [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] | WP1 target artefact. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0055 is the WP2 backlog source; Phase 1 implemented this session. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Section 8.1 records the Guardian Orb knowledge-graph design direction WP2's Phase 1 backend/frontend serves. |
| `jarvis/interfaces/knowledge_graph.py` | WP2 backend deliverable. |
| `src/GuardianOrbGraph.jsx` | WP2 final frontend deliverable - supersedes the initially-added, since-removed `src/KnowledgeGraph.jsx` standalone panel. |
| [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] | Repository baseline at session opening; retained through WP1's closure. |
| [[RBL-0014_REPOSITORY_BASELINE|RBL-0014]] | Current accepted repository baseline, accepted at this session's closure, superseding RBL-0013. |
| [[ESR-0019_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0019 WP6 Handover]] | Independent verification record for WP2, underlying RBL-0014's acceptance. |
| [[GDE-0001_PROJECT_KNOWLEDGE_MAP|GDE-0001]] | Knowledge tiering followed during WP0A. |

---

# 15. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.5 | 11 July 2026 | Claude Engineering Implementer | ESR-0019 closed. Recorded WP2 WP6/WP7 (Section 12: ChatGPT WP6 Pass, Programme Sponsor WP7 accepted RBL-0014) and the Closure Statement (Section 13). PST-0001 refreshed and RBL-0014 registered in the same closure pass. |
| 1.4 | 11 July 2026 | Claude Engineering Implementer | Recorded WP2 Extended Work (Section 11): the Guardian Orb integration and ten follow-on Programme Sponsor-directed iterations following commit `3f68c86` (dev-environment fix, edge/overlap/outlier bug fixes, hub labelling added then removed, Guardian Orb integration per UAM-0001 8.1 and the mock-up reference, off-centre clump fix, orb-label removal, name correction, EBG-0055 backlog closure). |
| 1.3 | 11 July 2026 | Claude Engineering Implementer | WP2 (EBG-0055 Phase 1) implemented and pushed, commit `3f68c86`, following two rounds of Reviewer pre-implementation review. Recorded WP2 Completion Record (Section 10), including the self-identified README-basename-collision fix and the disclosed live-GUI verification gap. |
| 1.2 | 11 July 2026 | Claude Engineering Implementer | Recorded WP6 Independent Repository Verification (Pass, ChatGPT) and WP7 Repository Baseline Acceptance (RBL-0013 retained, Programme Sponsor). WP1 fully closed. |
| 1.1 | 11 July 2026 | Claude Engineering Implementer | WP1 (PBK-0001/COC-0001 role-binding update) delivered and pushed, commit `1c1c7e9`. Recorded WP1 Completion Record (Section 9). |
| 1.0 | 11 July 2026 | Claude Engineering Implementer | ESR-0019 opened: WP0A/WP0B session initialisation complete, session objective confirmed (WP1 PBK-0001/COC-0001 role-binding update; WP2 EBG-0055 if time allows). |
