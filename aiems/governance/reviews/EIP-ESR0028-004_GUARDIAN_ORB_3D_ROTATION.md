# EIP-ESR0028-004 - Guardian Orb 3D Rotation (EBG-0055 Phase 1.5)

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0028-004 |
| Artefact ID | EIP-ESR0028-004 |
| Title | Guardian Orb 3D Rotation (EBG-0055 Phase 1.5) |
| Version | 1.0 |
| Status | Approved-implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0055) |
| Intended Session | ESR-0028 |
| Effective Date | 18 July 2026 |

---

# 2. Purpose

Deliver EBG-0055's two explicitly-deferred continuation items - "true 3D rendering (real depth/rotation)" and "live animation/rotation of the sphere" - as a single coherent Phase 1.5 increment, per the Programme Sponsor's own framing at ESR-0019 ("doesn't have to be perfect first time... layered on incrementally"). Also applies the Programme Sponsor's own Obsidian graph-view force measurements as a disclosed, directionally-informed force retuning.

---

# 3. Related Backlog Item

EBG-0055 (`EBR-0001:124-128`, Completed Phase 1 at ESR-0019, Phase 2 panels at ESR-0021 WP4). The explicitly not-yet-delivered continuation (`EBR-0001:128`): "true 3D rendering (real depth/rotation, e.g. via WebGL or a 3D scene library, rather than the current geometric 2D-to-hemisphere projection) and live animation/rotation of the sphere... a future EIP should clarify whether this becomes explicit Phase 1.5 scope."

---

# 4. Repository Context and Investigation Findings

## 4.1 Current implementation (`src/GuardianOrbGraph.jsx`)

A static SVG rendering: `layoutSphere()` runs a bounded 2D `d3-force` simulation (charge -60, link distance 15/strength 0.2, x/y centering 0.5, hard circular containment at `RADIUS` 140) for 400 fixed ticks, then reconstructs a depth value per node as `z = sqrt(1 - normalizedDist^2)` - the orthographic-projection identity for a hemisphere viewed head-on. This models only the **front hemisphere**: every node's depth is a positive magnitude, there is no "back" of the sphere in the data model, and positions are computed once via `useMemo` and never change after mount. This is why rotation cannot be added as a simple CSS transform: rotating a one-sided hemisphere around Y would immediately need to reveal nodes that do not exist in the current data model on the far side.

## 4.2 Why not WebGL / a 3D scene library

The backlog item names WebGL/a 3D scene library as one option, not a requirement ("via WebGL or a 3D scene library, rather than..."). Introducing one (e.g. Three.js) would add a new rendering pipeline and dependency to a codebase that has deliberately stayed SVG-based (per the component's own header comment: "not a physics simulation or WebGL scene... consistent with UAM-0001 8.1's 'driven by observed data, not by animation scripts' principle"). A genuine, real 3D rotation is achievable without one - Section 4.3.

## 4.3 Design: full-sphere coordinates + real Y-axis rotation

Extend `layoutSphere()`'s existing 2D force-simulated positions (unchanged - the topology/clustering layout is already well-verified) with a **stable, deterministic front/back hemisphere assignment per node** (a hash of `node.id`, not random - identical across re-renders and re-mounts), giving every node real `(x, y, z)` sphere-surface coordinates instead of only a front-hemisphere depth magnitude. Each animation tick rotates all node coordinates around the Y axis by a slowly-advancing angle, re-projects to 2D screen space (standard orthographic rotation: `x' = x*cosθ - z*sinθ`, `z' = x*sinθ + z*cosθ`, `y` unchanged), and re-sorts the node/edge render lists by resulting `z'` (painter's algorithm) so nodes rotating to the front correctly draw over nodes rotating to the back. This is a genuine, data-driven 3D rotation - real nodes move to the back and are actually replaced by different real nodes rotating to the front - not a decorative spin of a static image.

## 4.4 Programme Sponsor's Obsidian graph-view measurements

Supplied ahead of this WP (Obsidian Filters - Display and Forces): Central force 0.53, Repel Force 20.00, Link force 0.00, Link Distance 500, Node Size 1.58, Line Thickness 0.94 (plus display toggles - Tags/Attachments/Existing Files only/Orphans/Arrows all Off, Text Fade Threshold -2.30 - not applicable, this Orb never renders text labels or arrows, per the ESR-0019 decision to remove labels in favour of cluster colour alone).

**These values do not port literally.** Obsidian's force engine operates on an unbounded, freely-panned canvas; `GuardianOrbGraph`'s simulation is hard-bounded to a fixed circle (`forceContainCircle`, verified against the real graph: 0 nodes beyond boundary, 0 overlapping pairs). Increasing repulsion/link-distance by Obsidian's literal numbers in a bounded system would mostly just push more nodes into the containment clamp, producing a denser boundary ring rather than Obsidian's "spread across free space" look - a different, worse outcome, not an equivalent one.

**What does translate is the directional signal**, reading each value against Obsidian's own slider ranges: Repel Force 20.00 is that slider's maximum (strongest possible repulsion); Link force 0.00 is that slider's minimum (links exert no pulling force); Link Distance 500 is that slider's maximum (longest possible links). Central force 0.53 is close to `GuardianOrbGraph`'s own existing `forceX`/`forceY` strength of 0.5 - a validating coincidence, not something needing change. The clear intent: strong mutual repulsion, near-zero link-pull, held together mainly by central cohesion rather than link tension. This is portable as a *direction* (increase charge repulsion moderately, reduce link strength toward near-zero) without porting the literal numbers, and must be re-verified geometrically against the real graph exactly as the original tuning was (centroid distance from true centre, overlapping-pair count), since this system's containment force means "how strong is too strong" is empirically bounded, not something Obsidian's numbers can answer for us.

## 4.5 Accessibility

`prefers-reduced-motion` is a real, standard consideration for any newly-introduced animation and costs little to respect - not previously relevant to this component since it had no animation before.

## 4.6 No test infrastructure precedent

Per EBG-0055's own delivery history (ESR-0019 WP2, ESR-0021 WP4), this component has no committed automated test suite - verification has consistently been ad hoc Playwright live-verification against a synthetic or real graph, run once at implementation time, not a regression suite. This package follows the same precedent rather than introducing one, consistent with "no committed frontend test infrastructure exists" for this codebase.

---

# 5. Scope

This package authorises a future implementation to:

1. Extend `layoutSphere()` in `src/GuardianOrbGraph.jsx` to compute full-sphere `(x, y, z)` coordinates per node via a stable, deterministic front/back hemisphere hash - the existing 2D force-simulated `(x, y)` topology is unchanged.
2. Add a slow, continuous idle rotation around the Y axis, driven by component-local state on a throttled interval (not full 60fps - an ambient background rotation, not a fast animation), re-projecting all node/edge positions and re-sorting by depth each tick for correct front-over-back rendering.
3. Respect `prefers-reduced-motion`: when set, render the sphere at a fixed angle (no rotation), matching the pre-existing static behaviour.
4. Modestly retune `layoutSphere()`'s charge and link force strengths, informed by the directional signal in Section 4.4 (moderately stronger repulsion, link strength reduced toward near-zero), leaving `forceX`/`forceY` centering, containment radius and link *distance* unchanged (Section 4.4 explains why literal distance/repulsion numbers don't port). Re-verify geometric properties (centroid offset, overlapping-pair count) against the real repository knowledge graph and disclose before/after numbers, matching the rigour of the original tuning documented in the component's own comments.
5. Live-verify the rotating, retuned Orb against the real backend (`npm run tauri dev` or Playwright with the real `knowledge.graph` data) before reporting complete.
6. Record this delivery against EBG-0055 in EBR-0001, disclosing what remains not delivered (a true depth-buffered/WebGL 3D scene, real perspective, lighting) versus what this package delivers (a genuine, data-driven orthographic 3D rotation).

---

# 6. Authorised Files

1. `src/GuardianOrbGraph.jsx`
2. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
3. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`

`src/KnowledgeGraphPanels.jsx` is explicitly **not** authorised for changes - it imports `computeClusterOrder`/`colorForCluster`/`computeDegree` from `GuardianOrbGraph.jsx`, whose signatures and behaviour this package must not change, only the internal `layoutSphere`/rendering logic. No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. Front/back hemisphere assignment must be a pure, deterministic function of `node.id` (e.g. a simple string hash mod 2) - never `Math.random()` - so the sphere's composition is stable across re-renders, re-mounts and identical across a session, consistent with the "data-driven, not animation-scripted" principle already stated in the component's header comment.
2. Rotation state must live inside `GuardianOrbGraph` itself (not lifted to `App.jsx`), started in a `useEffect` on mount and cleaned up on unmount, matching React's standard interval/timer lifecycle discipline.
3. Rotation speed should be slow enough to read as ambient presence, not a spinning logo - a full rotation on the order of a minute or more, consistent with UAM-0001 8.1's "calm interaction" product principle already governing this component's design.
4. `prefers-reduced-motion: reduce` must be checked via `window.matchMedia` and disable the rotation interval entirely (not merely slow it), rendering the same fixed-angle sphere as before this change.
5. Force retuning (charge, link strength) must be verified against the real `knowledge.graph` data (not a synthetic graph) with before/after centroid-offset and overlapping-pair-count figures recorded in the implementation's evidence, matching the standard already set by the original tuning.
6. No new npm dependency is introduced - implementation stays within the existing `d3-force` + SVG architecture.
7. EBR-0001's EBG-0055 entry gets a new delivery paragraph (not a rewrite of prior paragraphs) disclosing rotation + full-sphere delivered, retuning applied with verification figures, and WebGL/true-3D-scene/lighting explicitly still not delivered.

---

# 8. Explicit Exclusions

This package does not authorise:

1. Introducing WebGL, Three.js, or any new 3D rendering dependency - Section 4.2 found a genuine 3D rotation is achievable within the existing SVG/d3-force architecture.
2. Porting Obsidian's literal force values numerically - Section 4.4 found this would produce a worse outcome in this bounded system; only the directional signal is applied, re-verified empirically.
3. Phase 3 (agent-traversal animation, blocked on GIA telemetry) or Phase 4 (Guardian reasoning connection) - both remain explicitly separate, later phases per EBG-0055's own scope boundary.
4. Any change to `src/KnowledgeGraphPanels.jsx` or the shared helper function signatures it depends on.
5. Any backend/`jarvis/interfaces/knowledge_graph.py` change - the graph data itself is unchanged, only its rendering.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. Live verification (Section 7 item 5) must occur before the package is reported complete, per this session's standing UI-change verification practice - not asserted without evidence.

---

# 10. Validation

After implementation, run:

```powershell
npm run build
python scripts/validate_repository.py
```

Validation should confirm:

1. `npm run build` passes clean.
2. Live verification against the real backend or a Playwright-mocked real graph, screenshotted or otherwise evidenced, showing rotation in motion and `prefers-reduced-motion` correctly disabling it.
3. `validate_repository.py` (full mode) passes with 0 errors for the governance-artefact files.
4. `python -m pytest` unaffected (no Python code touched) - run anyway to confirm no incidental breakage.

---

# 11. Risks and Dependencies

## Dependencies

None - self-contained frontend change plus governance closure.

## Risks

1. **Rotation performance at the real graph's node count (~150 nodes) is assumed acceptable, not yet measured.** If the throttled-interval re-render approach proves too costly in practice, a ref-based imperative DOM update (bypassing React's render cycle) is a known, disclosed fallback for a future iteration - not attempted here to keep this package's scope proportionate.
2. **The force-retuning direction (Section 4.4) is an interpretive judgement about what Obsidian's slider positions signal, not a mechanical translation.** Disclosed as a judgement call for the Engineering Reviewer and Programme Sponsor to weigh, verified empirically rather than asserted.
3. **Deterministic front/back hemisphere assignment is a new design choice with no real-graph precedent to check against.** Mitigated by keeping the existing 2D topology layout (already verified) completely unchanged - only the depth-sign assignment and rotation are new.

---

# 12. Approval Request

Requesting Engineering Reviewer (Codex) pre-implementation design review via the AIEMS Exchange Bridge, then Programme Sponsor approval.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0055 (this package's parent), Phase 1.5 delivered by this package. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Defines the Guardian Orb's knowledge-graph visual presence (the same sub-section EBG-0055's own EBR-0001 entry cites); this package continues its Phase 1 delivery. |
| `src/GuardianOrbGraph.jsx` | Component revised by this package. |
| `src/KnowledgeGraphPanels.jsx` | Depends on shared helpers this package must not break; explicitly not itself edited. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0 | 18 July 2026 | Claude Engineering Implementer | Implemented following Programme Sponsor approval via the bridge (`sponsor-decision`, `repository_ref: 070eb2a10d43bebea4bdc82bc70629f486c7d663`, 18 July 2026 20:56:53Z). All items applied: full-sphere coordinates with deterministic hemisphere assignment, real Y-axis rotation with depth re-sorting, `prefers-reduced-motion` support, force retuning verified against the real graph (centroid 4.88px vs original 4.62px, 0 overlaps, 0 boundary breaches). Live-verified via Playwright against the real backend data - rotation confirmed moving under normal motion, confirmed static under reduced motion. `npm run build`: clean. Status promoted Draft to Approved-implemented. |
| 0.1 | 18 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0028 WP4. Investigated the current front-hemisphere-only static rendering and designed a full-sphere coordinate model with deterministic front/back assignment and real Y-axis rotation, staying within the existing SVG/d3-force architecture rather than introducing WebGL. Investigated the Programme Sponsor's Obsidian graph-view force measurements and found literal value-porting inappropriate for this bounded-containment system; scoped instead to a directionally-informed, empirically-reverified retuning. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
