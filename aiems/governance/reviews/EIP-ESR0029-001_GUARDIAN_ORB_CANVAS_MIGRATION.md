# EIP-ESR0029-001 - Guardian Orb Canvas 2D Rendering Migration

---

# 1. Document Control

| Field | Value |
|-------|-------|
| Package ID | EIP-ESR0029-001 |
| Artefact ID | EIP-ESR0029-001 |
| Title | Guardian Orb Canvas 2D Rendering Migration |
| Version | 1.2 |
| Status | Approved-implemented |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Classification | Internal |
| Parent | EBR-0001 (EBG-0081) |
| Intended Session | ESR-0029 |
| Effective Date | 19 July 2026 |

---

# 2. Purpose

Implement the Canvas 2D migration decided by [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]] (Approved, 18 July 2026): replace `GuardianOrbGraph.jsx`'s per-element SVG DOM rendering (195 nodes + 1,687 edges as real DOM nodes on the real repository graph) with a single Canvas 2D surface drawn imperatively, retaining the existing `d3-force` layout and every performance safeguard proven in ESR-0028 WP4 (frame-rate cap, edge-update decoupling, page-visibility pause, idle-timeout pause, `prefers-reduced-motion`).

Also delivers a static visual refinement toward `UAM-0001_GUARDIAN_ORB_MOCKUP.jpg` (UAM-0001's reference mock-up)'s look and layout - soft glow/gradient node treatment in place of today's flat filled circles - per the Programme Sponsor's direction that Canvas makes this affordable to do now rather than as a later second pass. This is explicitly **not** an implementation of UAM-0001 Section 8.1's access-triggered cluster illumination or Section 8.2's Guardian-activity-state semantics (calm pulse / colour flow / traversal paths / gold highlight) - both require real backend activity signal that does not yet exist and remain separately scoped, later work, consistent with `EBG-0055`'s own Phase 3/4 boundary.

---

# 3. Related Backlog Item and Decision

`EBG-0081` (`EBR-0001`) Question (2), resolved as a decision by `ADR-0021`: "the implementation half remains not authorised... a future EIP must separately scope the actual Canvas migration." This package is that EIP.

---

# 4. Repository Context and Investigation Findings

## 4.1 Current implementation (`src/GuardianOrbGraph.jsx`, as delivered through ESR-0028 WP4)

Every node and edge is a real SVG DOM element (`<circle>`/`<line>`). A `requestAnimationFrame` loop mutates existing elements' attributes directly (bypassing React), capped to `MIN_FRAME_INTERVAL_MS` (~12 updates/second), with edges updated only every `EDGE_UPDATE_EVERY_N_FRAMES` (3rd) node-update and a periodic `appendChild`-based DOM re-sort every `RESORT_INTERVAL_MS` (300ms) for correct front/back occlusion (painter's algorithm). This architecture, evolved over seven fix rounds, is the direct evidence base for `ADR-0021`'s decision.

## 4.2 Why Canvas's full-redraw model changes two of those safeguards' mechanics, not their intent

Canvas has no persistent, individually-mutable elements - each drawn frame clears the surface and redraws everything visible in it. Two of the existing throttling techniques relied specifically on SVG's persistent-DOM model and do not port unchanged:

- **Edge-update decoupling**: on SVG, skipping an edge's position update for 2 out of 3 frames left it drawn at a slightly stale position - still visible, just not perfectly current. On Canvas, if edges are not drawn at all in a frame, they disappear from that frame entirely (visible flicker), since the whole surface is redrawn from scratch. The port must **recompute** edge endpoint positions only every `EDGE_UPDATE_EVERY_N_FRAMES`, but **redraw** edges (using the last-computed, possibly-stale positions) on every actual draw call, so they never disappear.
- **Painter's-algorithm re-sort**: on SVG, this reordered persistent DOM children every 300ms specifically to avoid the cost of reordering on every frame. On Canvas there is no persistent child order to reorder - draw order is simply the iteration order of an array immediately before that frame's draw calls. The real cost being avoided (an O(n log n) sort of ~195 nodes) is still real on Canvas; the port must keep a cached sort order, recomputed only every `RESORT_INTERVAL_MS`, and draw nodes in that cached order using each node's freshly-computed position every frame - not resorted every frame.

Getting this distinction right matters: a naive "redraw only what changed this frame" port would either flicker (if genuinely skipping draws) or silently discard the performance win (if resorting/redrawing everything every frame regardless).

## 4.3 Glow/gradient node treatment - performance-aware approach

`UAM-0001_GUARDIAN_ORB_MOCKUP.jpg`'s nodes read as soft radial glows, not flat filled circles. Two implementation approaches were considered:

- **Per-node `ctx.shadowBlur`/`ctx.shadowColor`**: simplest to write, but forces the browser to perform a real blur convolution for every shape drawn with an active shadow, every frame, for up to 195 nodes - a real, currently-unmeasured cost.
- **Pre-baked glow sprites** (recommended): render one small offscreen-canvas radial-gradient sprite per distinct cluster colour (up to 8, from `CLUSTER_PALETTE`) **once**, outside the animation loop, then per-frame per-node simply `drawImage()` the appropriate pre-baked sprite at the node's current position and depth-scaled alpha, followed by a small solid core circle on top (matching today's crisp node body, sized as today via `radiusForDegree`). This is the standard cheap technique for many-particle glow effects precisely because the expensive gradient computation happens once, not per node per frame.

The sprite approach is specified as the implementation target; `shadowBlur` is recorded as a disclosed fallback if the sprite approach proves visually insufficient during live verification. Edges are **not** given glow treatment (1,687 edges is a materially larger performance surface than 195 nodes) - they remain simple stroked lines as today, with at most a tuned opacity/width to read slightly more luminous, verified not to regress the edge-decoupling cost saving.

## 4.4 Loss of SVG's free per-element behaviour

- **Hit-testing/tooltips**: SVG's per-`<circle>` `<title>` gave a free native hover tooltip per node. Canvas has no per-shape hit-testing. Replacement: track each node's current on-screen position (already computed every draw tick) in a ref, and on `pointermove` over the canvas, find the frontmost node whose current radius contains the pointer position, then set the `<canvas>` element's own `title` attribute to that node's label (cleared on `pointerleave` or when no node is under the pointer) - the same browser-native tooltip affordance as before, computed manually instead of coming free from individual DOM elements.
- **Accessible description**: the outer element's `role="img"`/`aria-label` (a single summary description: "Guardian Orb: repository knowledge graph with N artefacts and M relationships") is retained unchanged - `<canvas>` supports the same ARIA attributes as `<svg>` at this level. Per-node `<title>` elements inside SVG had inconsistent assistive-technology support in the first place (title text on non-focusable shape children is not reliably announced); the canvas port preserves the same **summary-level** accessible description that existed before, not a regression, but does not add new per-node screen-reader granularity that did not meaningfully exist before either. A fully accessible per-node data view remains a possible future enhancement, out of scope here.

## 4.5 Device pixel ratio and responsive sizing

SVG's `viewBox` scaling means the existing markup renders crisply at any container size (300px desktop, `min(280px, 78vw)` on the documented mobile breakpoint in `src/styles.css:846-848`) with zero extra code. Canvas has no equivalent - a canvas element has a separate backing-store resolution (`canvas.width`/`canvas.height`, in device pixels) from its CSS display size, and a naive fixed backing-store size would render blurry on high-DPI displays or when the container is resized to the mobile breakpoint. The port must read the container's actual rendered CSS size (via `ResizeObserver`, since `.guardian-orb` is itself responsive) and `window.devicePixelRatio`, size the backing store to `renderedSize * devicePixelRatio`, scale the drawing context accordingly (`ctx.scale(dpr, dpr)`), and redraw on resize - otherwise this migration would introduce a visible regression (blurriness) that does not exist today.

## 4.6 No test infrastructure precedent

Consistent with `EIP-ESR0028-004` and this component's entire delivery history: no committed automated test suite exists for `GuardianOrbGraph.jsx`. Verification is ad hoc Playwright live-verification against the real graph plus a direct Windows Task Manager comparison, following the same rigour ESR-0028 WP4 established, not a new regression suite.

---

# 5. Scope

This package authorises a future implementation to:

1. Replace the `<svg>` element and its per-node/per-edge DOM children in `GuardianOrbGraph.jsx` with a single `<canvas>` element, sized and DPI-scaled per Section 4.5, clipped to the same circular boundary (`ctx.arc` + `ctx.clip()` in place of the existing SVG `<clipPath>`).
2. Reimplement the animation tick as a full clear-and-redraw each draw call: recompute node positions via the existing, unchanged `rotateNode()`/rotation-angle logic; draw edges first (stroked lines, cached-position recompute-decoupling per Section 4.2), then nodes in cached depth-sorted order (per Section 4.2) with the glow-sprite-plus-core-circle treatment from Section 4.3.
3. Retain unchanged: `layoutSphere()`, `hemisphereSign()`, `rotateNode()`, the rotation-angle/timestamp math, `MIN_FRAME_INTERVAL_MS` frame cap, page-visibility pause, idle-timeout pause (`useIsIdleRef`), `visibilitychange` handling, and `prefers-reduced-motion` support (rendering a single static frame at angle 0 when reduced motion is set, matching today's behaviour) - only the drawing mechanism changes, not the simulation, timing or accessibility-preference logic.
4. Implement manual hit-testing and a `title`-attribute tooltip swap per Section 4.4, and retain the outer element's `role="img"`/`aria-label` summary description.
5. Re-tune `MIN_FRAME_INTERVAL_MS`/`EDGE_UPDATE_EVERY_N_FRAMES`/`RESORT_INTERVAL_MS` empirically if live verification shows Canvas's different cost profile warrants different values - disclosed as measured tuning, not asserted unchanged from the SVG-era constants.
6. Update `src/styles.css`: remove the now-dead `.guardian-orb-graph-edges line`/`.guardian-orb-graph-nodes circle` SVG-specific selectors; the existing `.guardian-orb-graph` sizing rule (`position: absolute; inset: 0; width: 100%; height: 100%`) is reused as-is for the canvas element.
7. Live-verify against the real backend (`npm run tauri dev` or Playwright against the real `knowledge.graph` data) in two isolated steps: (a) confirm a plain Canvas port (before adding glow) measurably reduces CPU/GPU cost versus the SVG baseline via Task Manager comparison, isolating the rendering-engine change's own effect; (b) confirm adding the glow/gradient treatment does not materially erode that win. Both figures disclosed, not just a single combined before/after.
8. Record delivery against `EBG-0081` in `EBR-0001` (Canvas migration implemented; the still-open shared-animation-scheduler question, Question (1), remains untouched by this package) and add a short delivery cross-reference to `ADR-0021` noting the decision is now implemented.

---

# 6. Authorised Files

1. `src/GuardianOrbGraph.jsx`
2. `src/styles.css`
3. `aiems/governance/registers/EBR-0001_ENGINEERING_BACKLOG_REGISTER.md`
4. `aiems/governance/registers/REG-0001_CONTROLLED_ARTEFACT_REGISTER.md`
5. `aiems/governance/decisions/ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE.md` (a short delivery annotation only - the Decision, Rationale and Consequences sections themselves are not reopened)

`src/KnowledgeGraphPanels.jsx` is explicitly **not** authorised - it imports `computeClusterOrder`/`colorForCluster`/`computeDegree`, whose signatures and behaviour this package must not change. No other files are authorised unless a dependency is discovered during validation and explicitly reported.

---

# 7. Implementation Requirements

1. `computeClusterOrder`/`colorForCluster`/`computeDegree` remain unchanged, same exports, same signatures.
2. `d3-force` remains the layout engine; `layoutSphere()`'s force configuration is not altered by this package.
3. Rotation-angle computation (elapsed-wall-clock-time-driven, not fixed tick count) is unchanged - only how each frame's computed positions get drawn changes.
4. The `visibilitychange`-driven `lastFrame` pinning fix from ESR-0028 WP4 (preventing a jump-forward after a hidden window resumes) must be retained exactly - this is animation-timing logic, independent of rendering surface.
5. Canvas backing-store sizing must use `ResizeObserver` and `window.devicePixelRatio`, redrawing (not just rescaling) on resize, per Section 4.5.
6. Glow sprites (Section 4.3) must be created once (e.g. via `useMemo` with no dependency, or on first draw) and reused every frame - never recreated per node per frame.
7. No new npm dependency is introduced - Canvas 2D is a native browser API.
8. Manual hit-testing (Section 4.4) must use each frame's actual current node positions (not the initial/unrotated positions) so the hover target tracks the rotating sphere correctly.
9. `EBR-0001`'s `EBG-0081` entry gets a new delivery paragraph (not a rewrite of the existing decision-recording paragraph) disclosing what this package delivers.

---

# 8. Explicit Exclusions

This package does not authorise:

1. UAM-0001 Section 8.1's access-triggered cluster illumination or Section 8.2's Guardian-activity-state animation semantics (calm pulse / colour flow / traversal paths / gold highlight / green pulse) - both require real backend activity signal that does not exist yet and remain separate, later, out-of-scope work (`EBG-0055` Phase 3/Phase 4 territory).
2. Labelled callouts pointing at specific named clusters/nodes, as shown in `UAM-0001_GUARDIAN_ORB_MOCKUP.jpg` - a distinct informational-overlay feature, not part of this rendering migration.
3. Glow/gradient treatment on edges - explicitly excluded per Section 4.3's performance-risk reasoning (1,687 edges is a materially larger surface than 195 nodes).
4. `EBG-0081` Question (1) (the separate shared-animation-scheduler question) - remains open Candidate Backlog, untouched by this package.
5. Any change to `src/KnowledgeGraphPanels.jsx` or the shared helper function signatures it depends on.
6. Any backend/`jarvis/interfaces/knowledge_graph.py` change - the graph data itself is unchanged, only its rendering.
7. Reopening `ADR-0021`'s Decision, Rationale or Consequences sections beyond a brief delivery cross-reference.

---

# 9. Constraints

1. No implementation shall begin until this package reaches Approved status.
2. Live verification (Section 5 item 7) must occur before the package is reported complete, using the same two-isolated-steps approach specified there - not asserted without evidence, and not combined into a single conflated before/after figure.

---

# 10. Validation

After implementation, run:

```powershell
npm run build
python scripts/validate_repository.py
```

Validation should confirm:

1. `npm run build` passes clean.
2. Live verification against the real backend or a Playwright-mocked real graph: rotation in motion, `prefers-reduced-motion` correctly disabling it, hover tooltip working, correct depth-based occlusion (front nodes drawn over back nodes), no blurriness at both the desktop and mobile-breakpoint container sizes.
3. Isolated Task Manager comparison, two steps: plain Canvas port vs. the ESR-0028 WP4 SVG baseline; then Canvas-with-glow vs. plain Canvas port. Both figures disclosed.
4. `validate_repository.py` (full mode) passes with 0 errors for the governance-artefact files.
5. `python -m pytest` unaffected (no Python code touched) - run anyway to confirm no incidental breakage.

---

# 11. Risks and Dependencies

## Dependencies

None - self-contained frontend change plus governance closure.

## Risks

1. **Glow sprite rendering cost is currently unmeasured.** Section 4.3's sprite-based approach is chosen specifically to bound this risk versus per-node `shadowBlur`, but the two-step verification in Section 5 item 7 is what actually confirms it, not assumed.
2. **The edge-decoupling and re-sort adaptations in Section 4.2 are a new design, with no direct SVG-era precedent to check against.** Mitigated by keeping the underlying throttling *intent* (and constants as starting values) identical, changing only how each is expressed under Canvas's full-redraw model.
3. **Canvas hit-testing (Section 4.4) is a new manual implementation replacing SVG's free per-element behaviour.** If pointer-tracking overhead itself proves non-trivial, throttling `pointermove` handling (not every event) is a disclosed, available fallback not pre-emptively applied here.
4. **DPI/resize handling (Section 4.5) is genuinely new code with no prior version in this component to compare against**, since SVG never needed it. Mitigated by explicit live verification at both documented container sizes (Section 10 item 2).

---

# 12. Approval Request

Requesting Engineering Reviewer (Codex) pre-implementation design review via the AIEMS Exchange Bridge, then Programme Sponsor approval.

---

# 13. Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[ADR-0021_GUARDIAN_ORB_RENDERING_ENGINE|ADR-0021]] | The Approved decision this package implements. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0081 (this package's parent backlog item), Question (2)'s implementation delivered by this package. |
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Defines the Guardian Orb's knowledge-graph visual presence; `UAM-0001_GUARDIAN_ORB_MOCKUP.jpg` is this package's visual reference for the static glow/gradient treatment only, not its data-driven semantics. |
| [[EIP-ESR0028-004_GUARDIAN_ORB_3D_ROTATION|EIP-ESR0028-004]] | The SVG-era rotation/performance implementation this package migrates away from, while retaining its layout, timing and accessibility-preference logic unchanged. |
| `src/GuardianOrbGraph.jsx` | Component revised by this package. |
| `src/KnowledgeGraphPanels.jsx` | Depends on shared helpers this package must not break; explicitly not itself edited. |

---

# 14. Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.2 | 19 July 2026 | Claude Engineering Implementer | Addressed two Engineering Reviewer (Codex) findings on the v1.1 implementation review. Medium 1: `hitTestRef.current` was built from `baseNodes`' arbitrary iteration order, not the actual `sortOrderRef.current` depth-sorted paint order `handlePointerMove` assumed when searching in reverse - for overlapping nodes, the tooltip could report a node other than the frontmost one actually under the pointer. Fixed by building hit entries from `sortOrderRef.current` (the same order nodes are painted in) after it is established each frame, so the existing reverse-search correctly finds the frontmost match. Re-verified live via Playwright (sampled several points across the orb, confirmed a real node label returned correctly) and via Chrome DevTools Protocol TaskDuration (~6.00% of one core, unchanged within measurement noise from v1.1's ~6.26%, confirming the fix - now running every frame rather than only when the resort cache refreshed - added no meaningful cost). Medium 2: REG-0001's EBR-0001 and EIP-ESR0029-001 rows were stale relative to the v1.1 update at the moment of review (a timing artefact of submitting a second update while the first was still being reviewed, not a content error in the final file state) - reconfirmed both rows match their respective documents' current versions before this resubmission. |
| 1.1 | 19 July 2026 | Claude Engineering Implementer | Real hardware confirmation added, closing the gap the CDP-based measurement alone could not: the Programme Sponsor ran the live Tauri app (`npm run tauri dev`) and observed Windows Task Manager directly - JARVIS Guardian Shell process group at 1.4% CPU, 1.0% GPU, Power Usage "Low" (Power Usage Trend "Very low"), a categorical change from the SVG-era baseline's sustained "Very high" classification that persisted through all seven ESR-0028 WP4 fix rounds. This is the actual symptom this migration exists to resolve - the CDP TaskDuration comparison in v1.0 measured a consistent, real, but different thing (headless Chromium JS main-thread script time), and did not by itself confirm the Windows-reported GPU/power-state improvement; this entry supplies that confirmation. |
| 1.0 | 19 July 2026 | Claude Engineering Implementer | Implemented following Programme Sponsor approval via the bridge (`sponsor-decision`, `repository_ref: 541e6c1d6a61394c36b162f515e0c5d502b909bf`, 19 July 2026 08:20:01Z). `GuardianOrbGraph.jsx` migrated to a single Canvas 2D surface; `src/styles.css`'s now-dead SVG-element selectors removed. Node depth-sorting, idle/visibility pausing, `prefers-reduced-motion`, rotation timing and `d3-force` layout all retained unchanged. Manual hit-testing (canvas `title` swap on `pointermove`) and `ResizeObserver`+`devicePixelRatio` backing-store sizing implemented per Section 4.4/4.5. Static glow/gradient node treatment delivered via pre-baked per-cluster-colour sprites (Section 4.3). **A genuine performance defect was found and fixed during this package's own live verification, disclosed rather than hidden**: an initial implementation stroked each of the 1,745 real edges individually every redrawn frame, measured via Chrome DevTools Protocol TaskDuration against the real graph at ~27-29% of one core - *more* expensive than the ~9.05% SVG baseline this migration was meant to improve on, the opposite of ADR-0021's premise. A CDP-based ablation study isolated the cause to Canvas's circular clip combined with per-edge stroke calls (not edge count or the clip alone). Fixed in two steps: (1) batching edges into `EDGE_DEPTH_BANDS` (8) depth-banded `Path2D` objects built during the already-throttled recompute step; (2) recognising edges are mathematically guaranteed to stay within the circular boundary (`forceContainCircle` bounds every node, rotation preserves distance from centre, a disk is convex) and scoping the clip to only the node/glow-drawing pass, which is the only part that can overflow it. Final measured result: plain Canvas ~4.46%, Canvas with glow ~6.26%, both below the ~9.05% SVG baseline (same real 200-node/1,745-edge graph, same CDP TaskDuration methodology for both, isolating the rendering-engine change from the glow-styling cost per Section 5 item 7/Section 10 item 3's two-step requirement). Functional live verification (Playwright, mocking the real backend bridge): rotation confirmed via canvas pixel-sampling, `prefers-reduced-motion` confirmed static, hover tooltip confirmed against real node labels, correct DPR/responsive sizing confirmed at both the desktop (312px) and mobile (`min(280px, 78vw)`) breakpoints, zero console errors across all scenarios. `npm run build` clean, `python -m pytest` 286/286 passing (no Python touched), `validate_repository.py` 0 errors. |
| 0.1 | 19 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0029 WP2, following Programme Sponsor approval of ADR-0021's Canvas 2D decision and agreement to include a static glow/gradient visual refinement toward UAM-0001's reference mock-up (look and layout only, not its data-driven activity semantics). Investigated how SVG's edge-update-decoupling and painter's-algorithm re-sort throttling techniques must be re-expressed under Canvas's full-redraw model, a performance-aware glow-sprite approach, manual hit-testing/tooltip replacement, and DPI/responsive-sizing requirements Canvas needs that SVG did not. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
