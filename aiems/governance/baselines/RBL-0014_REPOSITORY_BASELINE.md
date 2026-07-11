# RBL-0014 - Repository Baseline

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Artefact ID | RBL-0014 |
| Title | ESR-0019 Repository Baseline (Guardian Orb Knowledge Graph) |
| Version | 1.0 |
| Status | Accepted |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Engineering Session | [[ESR-0019_ENGINEERING_SESSION_REPORT|ESR-0019]] |
| Previous Baseline | [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] |
| Classification | Internal |
| Date | 11 July 2026 |
| HEAD at baseline creation | `2dbe1d1c1913ce8d350c8de9d3525513c0c66481` |

---

# 2. Purpose

RBL-0014 records the repository baseline accepted by the Programme Sponsor at the close of ESR-0019, superseding [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]]. Unlike WP1's small governance change (judged incremental, RBL-0013 retained per the ESR-0016 precedent), WP2 delivered a genuinely new backend capability - a repository knowledge-graph JSON-RPC endpoint - and a materially changed UXP hero element: the Guardian Orb, previously a decorative glow/ring/text-label animation, is now the live knowledge graph itself, per [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8.1's original design intent. Both the Engineering Implementer and the Engineering Reviewer's WP6 independently recommended a new baseline for this reason.

---

# 3. Repository State

| Item | Baseline State |
|------|----------------|
| Branch | main |
| Previous Baseline | [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] |
| Product Baseline | [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] - stale, unchanged by this baseline, tracked as EBG-0056 |
| Programme Status Reference | [[PST-0001_PROGRAMME_STATUS|PST-0001]] |
| Controlled Artefact Register Reference | [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] |
| Repository Readiness | Accepted; ready for ESR-0020 entry |

---

# 4. Baseline Recommendation Rationale

Recommended by the Engineering Implementer (Claude) at WP7 handover, following the Engineering Reviewer's (ChatGPT) WP6 Independent Repository Verification (Pass - see Section 9 and [[ESR-0019_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|the WP6 handover]]). Accepted by the Programme Sponsor on 11 July 2026.

WP1's role-binding update was judged incremental and did not itself warrant a baseline (RBL-0013 retained). WP2 is materially heavier: it adds a real backend capability (the `knowledge.graph` JSON-RPC method, backed by a tested repository-parsing module) and changes the Guardian Orb - the project's central visual identity element - from a static placeholder animation into a live, data-driven rendering, closing a gap first identified at ESR-0010 and formally recorded in UAM-0001 Section 8.1 since ESR-0017.

---

# 5. Engineering Deliverables

| Deliverable | Outcome |
|-------------|---------|
| `jarvis/interfaces/knowledge_graph.py` | New: parses git-tracked markdown WikiLinks into a node/edge graph. `git ls-files`-based enumeration anchored to `Path(__file__)` (not process cwd); explicit alias/duplicate/malformed/self-link/unresolved-link handling; repo-relative-path node ids (resolving a real ambiguity - three tracked files share the stem `README`). 11 tests. |
| `jarvis/interfaces/stdio_rpc.py` | New `knowledge.graph` JSON-RPC method registered alongside `guardian.converse`/`platform.status`. |
| `src-tauri/src/lib.rs` | New `knowledge_graph` Tauri command mirroring `platform_status`. |
| `src/GuardianOrbGraph.jsx` | New: the Guardian Orb's live visual presence. 2D force-directed layout confined to a circle (custom hard-boundary containment force), given a deterministic hemisphere depth projection (`z = sqrt(1 - r^2)`) for a parallax-sphere illusion - geometric and data-driven, not a physics engine, WebGL scene or decorative animation. Tuned and verified against the real 148-node/1220-edge graph for radial fill, angular symmetry (centroid within 5px of true centre) and zero node overlap. Supersedes the placeholder glow/ring/text-label animation and the initially-added, since-removed standalone panel (`src/KnowledgeGraph.jsx`). |
| `src/App.jsx`, `src/platformStatus.js`, `src/styles.css` | Wired the live graph into the hero orb; removed the "Guardian"/"AI Companion" text overlay (Programme Sponsor decision, cluster colour sufficient); corrected the hardcoded "Richard" placeholder name to Robert. |
| `vite.config.js` | Fixed a pre-existing scaffolding gap (missing `server.watch.ignored` for `src-tauri/target`) that crashed `npm run tauri dev` with `EBUSY` on Windows - found while attempting live verification, unrelated to WP2's design but blocking it. |
| [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] | v1.21. Two additions this session: role-binding to the permanent EE-0001 Section 7 appointment (WP1); "Incremental Visual Convergence Toward the Reference Mock-up" under Feature-First Delivery Discipline (Programme Sponsor direction at WP2 closure). |
| [[COC-0001_HUMAN_AI_COLLABORATION_CONTEXT|COC-0001]] | v1.12. Same role-binding addition as PBK-0001 (WP1). |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | v1.31. EBG-0055 marked Completed (Phase 1), recording the Guardian Orb delivery; true 3D rendering and live animation flagged as explicit deferred next candidates. |
| Test suite | Grew from 192 (RBL-0013) to 204 passing tests, zero regressions. |

---

# 6. Product Baseline

[[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] is unchanged by this baseline and remains materially stale, as already flagged at RBL-0013 and tracked as [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0056 (not actioned this session). What actually changed operationally: the repository's own knowledge graph is now a live, queryable capability (`knowledge.graph`), and the Guardian Orb - the UXP's central visual element - now reflects real repository state rather than a decorative placeholder. Neither is yet reflected in PCB-0001.

---

# 7. Architecture Outcomes

- First delivery under [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8.1's Guardian Orb knowledge-graph design direction, approved as far back as ESR-0010 and formally recovered into UAM-0001 at ESR-0017, but not implemented until this session.
- [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0055 Phase 1 delivered, per the phased roadmap recorded in EBG-0028's note (Phase 1 static graph, Phase 2 cluster illumination, Phase 3 agent-traversal animation, Phase 4 Guardian reasoning connection) - Phase 1 only, boundaries respected throughout.
- First standing PBK-0001 practice tying UXP evolution explicitly to a named visual reference (`aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg`), with an explicit safeguard preserving the no-mock-fallback rule for data-bearing UI elements.

---

# 8. Scope Boundaries

Scope boundaries for this baseline:

- no ESR-0020 artefact is created by this baseline - it hands over to ESR-0020, it does not open it;
- PCB-0001 is not refreshed - flagged stale at RBL-0013, tracked as EBG-0056, not actioned here;
- true 3D rendering (real depth/rotation) and live animation of the Guardian Orb are explicitly deferred, per Programme Sponsor decision recorded in [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] EBG-0055's note;
- Knowledge Graph Phases 2-4 (cluster-illumination semantics, agent-traversal animation, Guardian reasoning connection) remain not started;
- Gemini remains unvalidated against the real Gemini API (EBG-0051's live smoke test still outstanding, carried from RBL-0013).

---

# 9. Verification

Repository validation performed during ESR-0019's WP6/WP7 closure confirmed:

- Git working tree was clean at each commit; twelve commits (`abbae2e` through `2dbe1d1`) pushed to `origin/main` since RBL-0013's `1c1c7e9` (WP1's own WP7 acceptance point).
- Repository branch was `main`, synchronised with `origin/main` (`HEAD` confirmed at `2dbe1d1` by both the Engineering Implementer and independently by the Engineering Reviewer via GitHub).
- 204/204 tests passing, zero regressions since RBL-0013's 192.
- `python scripts/validate_repository.py` passed with 0 errors (85 warnings; the two beyond RBL-0013's 83 are the WP6 handover document's own cross-artefact section references, the same pre-existing warning class accepted at every prior baseline).
- `cargo check` (`src-tauri`) and `npm run build` both clean.
- ChatGPT Engineering Reviewer performed WP6 Independent Repository Verification: **Pass**, no blocking implementation defect found in `jarvis/interfaces/knowledge_graph.py`, `src/GuardianOrbGraph.jsx` or the `src-tauri/src/lib.rs` bridge wiring; two Low, non-blocking findings noted (the WP6 handover's own validation snapshot reads stale once the handover document itself joins the tracked corpus - an inherent, self-referential property of any handover document, not a defect).
- The Programme Sponsor accepted this baseline on 11 July 2026, superseding [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] as the current repository baseline.

---

# 10. Handover

**This baseline hands over to ESR-0020.** No next Engineering Session objective is created by this baseline - opening ESR-0020 is a separate, future action requiring its own Programme Sponsor approval.

ESR-0020 opening review should include:

1. This document and [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] for prior context.
2. [[PST-0001_PROGRAMME_STATUS|PST-0001]], updated for ESR-0019 closure immediately following this acceptance.
3. [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]].
4. [[ESR-0019_ENGINEERING_SESSION_REPORT|ESR-0019]] in full - Section 11's Extended Work log records the Guardian Orb integration's full iterative history, worth reading in full given how many follow-on fixes it involved.
5. [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]], specifically EBG-0055 (Completed, Phase 1 - true 3D/animation flagged as candidates for continuation), EBG-0056 (PCB-0001 refresh, still not actioned) and EBG-0057 (Claude&harr;Codex bridge, still not actioned).
6. [[PBK-0001_AI_ENGINEERING_PLAYBOOK|PBK-0001]] - the new Incremental Visual Convergence clause applies from ESR-0020 onward.
7. [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] Section 8.1 - now partially implemented (Phase 1); any future Guardian Orb work should be checked against Phases 2-4's remaining scope.

---

# 11. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ESR-0019_ENGINEERING_SESSION_REPORT|ESR-0019]] | Engineering session this baseline is drawn from; closes immediately following this baseline's acceptance. |
| [[RBL-0013_REPOSITORY_BASELINE|RBL-0013]] | Previous accepted repository baseline, superseded by this baseline's acceptance. |
| [[ESR-0019_WP6_INDEPENDENT_REPOSITORY_VERIFICATION_HANDOVER|ESR-0019 WP6 Handover]] | Independent verification record this baseline's acceptance is drawn from. |
| [[PCB-0001_PRODUCT_CAPABILITY_BASELINE|PCB-0001]] | Accepted operational product capability baseline - remains stale, tracked as EBG-0056, not refreshed by this baseline. |
| [[PST-0001_PROGRAMME_STATUS|PST-0001]] | Programme status, updated for ESR-0019 closure immediately following this acceptance. |
| [[REG-0001_CONTROLLED_ARTEFACT_REGISTER|REG-0001]] | Register updated to include this baseline. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Guardian Experience Architecture; this baseline's Phase 1 implementation milestone. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | Backlog register; EBG-0055 Phase 1 completed, EBG-0056/EBG-0057 remain candidates for a future session. |

---

# 12. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 11 July 2026 | Programme Sponsor | Accepted as the current repository baseline, superseding RBL-0013, following ChatGPT Engineering Reviewer's WP6 Pass and the Programme Sponsor's explicit WP7 decision to cut a new baseline rather than retain RBL-0013. |
