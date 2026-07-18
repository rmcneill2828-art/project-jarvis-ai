# ADR-0021 - Guardian Orb Rendering Engine

---

# Document Control

| Field | Value |
|------|------|
| ADR ID | ADR-0021 |
| Title | Guardian Orb Rendering Engine |
| Version | 1.3 |
| Status | Approved |
| Owner | Programme Sponsor & Chief Engineering Advisor |
| Date Approved | 18 July 2026 |
| Review Trigger | GuardianOrbGraph.jsx node/edge count grows by an order of magnitude, or the knowledge graph gains further animated capability (Phase 3 agent-traversal, Phase 4 Guardian reasoning connection) |

---

# Purpose

Record a decision on whether `GuardianOrbGraph.jsx` should continue rendering the Guardian Orb's knowledge graph as SVG DOM elements, or migrate to Canvas 2D (or another approach), following the Programme Sponsor's direct concern raised during ESR-0028 WP4: a single, deliberately-optimised ambient rotation required seven rounds of fixes to bring its GPU/CPU cost down, and more animated UXP capability is anticipated before the project ends. This decision is made now, while the component is still small and the migration cost is comparatively low, rather than deferred until switching becomes more expensive.

---

# Scope

This ADR decides the rendering approach only. It does not implement any migration, does not change the knowledge-graph data model (`jarvis/interfaces/knowledge_graph.py`), does not alter the force-simulation topology (`d3-force` remains the layout engine regardless of rendering choice), and does not decide the separate EBG-0081 shared-animation-scheduler question, which remains open Candidate Backlog. If this ADR recommends migration, implementing it is future, separately-scoped and separately-approved work.

---

# Engineering Authority

Raised directly by the Programme Sponsor during ESR-0028 WP4's post-implementation fix cycle, following seven live-verified fix rounds to GuardianOrbGraph.jsx's rotation performance. Investigated and drafted by the Engineering Implementer against direct evidence from that same investigation, per Principle 1/2 (Engineering Before Implementation, Evidence Before Conclusion).

---

# Evidence Sources

- `src/GuardianOrbGraph.jsx` (as delivered through ESR-0028 WP4, commit `003d8c9`) - the current implementation: every node and edge is a real SVG DOM element (`<circle>`/`<line>`), 195 nodes and 1,687 edges against the real repository graph (`~1,880` elements total).
- ESR-0028 WP4's seven-round fix history (`EBR-0001` EBG-0055 entry) - direct, measured evidence that DOM-based SVG rendering imposed real, attributable cost for a single animated feature: React-state re-rendering all ~1,880 elements per tick measured "Very high" sustained power usage; moving to direct ref-based DOM mutation (bypassing React) reduced but did not eliminate it; capping update frequency, decoupling edge updates from node updates (edges are ~8.6x the node count), and pausing when hidden/idle each measurably reduced real CPU/GPU percentages (roughly 20.9%/15.5% down to ~13-15%/9-11% across the rounds) without ever fully clearing Windows' qualitative "Very high" classification.
- `EBG-0055`'s own original Phase 1 scope note (`EBR-0001:124`): "At ~135 nodes, rendering performance is not a significant constraint for any standard graph library... should re-assess rendering approach if/when the real node count grows by an order of magnitude" - the real node count has since grown to 195 (repository growth, not a magnitude-order change), and this ADR treats the *animation* cost (not raw node count) as the concrete trigger for reassessment, since that is what the WP4 investigation actually measured.
- `EBG-0081` (`EBR-0001`, Candidate Backlog) - the Programme Sponsor's own forward-looking framing: "if we add more animation to the UXP it cause more CPU spikes," raised specifically because a single optimised animation already required this much effort.
- `package.json` - confirms no Canvas/WebGL rendering library is currently a dependency; `d3-force` (the layout engine, independent of rendering choice) is already present and would be retained under any option below.

---

# Main Content

## 1. Problem Statement

`GuardianOrbGraph.jsx` renders the Guardian Orb's knowledge graph as SVG, with one real DOM element per node and edge. ESR-0028 WP4 needed seven rounds of increasingly specific optimisation to bring a single ambient rotation's GPU/CPU cost down to an acceptable level, and even the final, well-optimised state did not clear Windows' "Very high" power-usage classification. This is evidence that SVG's per-element DOM cost is already close to its practical limit for animated rendering at the current ~1,880-element scale - a concern worth resolving before more animated UXP capability (Phase 3 agent-traversal, Phase 4 Guardian reasoning connection, or any other future animated feature) is built on the same pattern.

## 2. Background

SVG was the original, deliberate choice for the Guardian Orb (ESR-0019 WP2), explicitly to avoid "a physics simulation or WebGL scene," keeping the component's 3D illusion a "deterministic geometric projection" consistent with UAM-0001 8.1's "driven by observed data, not by animation scripts" principle. That reasoning was sound for a *static* rendering (Phase 1) and remains sound as an argument against jumping straight to a full 3D engine - it does not, on its own, argue for or against SVG specifically versus a different 2D rendering surface like Canvas, which can express the identical deterministic, data-driven projection.

## 3. Options Considered

| Option | Assessment |
|--------|------------|
| **Stay with SVG, optimise further** | ESR-0028 WP4 already applied the standard SVG-performance playbook: bypass React reconciliation (ref-based direct DOM mutation), cap update frequency, decouple update rates by element importance, pause when hidden/idle. Each measurably helped; none fully resolved the qualitative cost. Further gains from here would mean either reducing visual quality (slower rotation, fewer visible edges) or reducing element count (rendering fewer nodes/edges than the real graph has) - both cut against the "driven by observed data" principle rather than serving it. Diminishing returns for continued investment in the same architecture. |
| **Canvas 2D** | Native browser API, no new dependency. All shapes drawn into a single bitmap via one context; the browser composites one layer regardless of shape count, instead of managing ~1,880 individual DOM nodes each with their own layout/paint/composite accounting. The standard, well-established right-sized tool for exactly this problem shape: hundreds-to-thousands of simple shapes (circles, lines) redrawn frequently. Loses SVG's free per-element hit-testing, `<title>` tooltips and DOM-based accessibility tree integration - manual mouse-position hit-testing and a synthetic accessible description (e.g. an offscreen list or `aria-live` summary) would be needed to preserve the current per-node label tooltip and the SVG's existing `role="img"`/`aria-label` treatment. Real, disclosed cost, not free - but a bounded, well-understood one. |
| **WebGL / a 3D scene library (Three.js, PixiJS, etc.)** | Justified when a scene needs thousands-to-millions of GPU-instanced elements, custom shaders, or genuine 3D perspective/lighting. None of those apply here: `EBG-0055`'s own scope note ties reassessment to an order-of-magnitude node-count increase, not currently anticipated; the "3D" illusion is and is intended to remain a deterministic geometric projection, not real perspective/depth-of-field. Adopting WebGL now would add a new rendering paradigm, a new dependency (for any of the common libraries; hand-rolled WebGL is a materially larger undertaking than either SVG or Canvas), and solve a scale problem the project does not have. Rejected as disproportionate to the actual, evidenced need. |
| **Do nothing now, revisit only if the problem recurs** | Rejected as the Programme Sponsor's own framing for raising this ADR: the cost of switching rendering approach is lower now, with one moderately-sized component and no other animated UXP features yet built on the same pattern, than it would be after more features are built the same way. Waiting converts a currently-bounded, single-component migration into a larger one. |

## 4. Decision

`GuardianOrbGraph.jsx` **shall migrate to Canvas 2D rendering**, replacing per-element SVG DOM nodes with a single canvas surface drawn imperatively each frame (or on each capped update, per the existing throttling/decoupling/pause logic already proven in ESR-0028 WP4, which is retained rather than discarded).

WebGL/a 3D scene library is explicitly **not** selected - the current and anticipated scale does not justify it, per Section 3.

This ADR authorises the decision only. Implementation is separate, future, scoped work (see Consequences).

## 5. Rationale

- Seven rounds of real, measured optimisation on the current SVG architecture reduced but did not eliminate the cost - direct evidence that the architecture itself, not any single implementation detail within it, is the limiting factor.
- Canvas 2D is proportionate to the actual problem (hundreds of simple shapes, frequent redraws) without over-committing to WebGL's complexity for a scale the project does not have and does not currently plan to have.
- No new dependency is required for Canvas (native browser API), consistent with this session's WP4 decision to avoid adding a rendering dependency, and with the project's general no-discretionary-spend/minimise-dependency posture.
- Timing: the Programme Sponsor's own stated concern - resolving this "before we are too near the end of the project" - is best served by migrating one bounded, already-well-understood component now, rather than after further animated features exist on the same SVG pattern.

## 6. Consequences

- **Not implemented by this ADR.** A future EIP must scope: the Canvas drawing implementation itself; a manual hit-testing/tooltip replacement for the current per-node `<title>` labels; an accessible-description strategy replacing SVG's DOM-based `role="img"`/`aria-label` treatment (still achievable on a `<canvas>` element, but requires deliberate implementation rather than coming for free from individual DOM nodes); and live before/after performance verification against the real graph, following the same rigour (Playwright live-verification, Task Manager comparison) established in ESR-0028 WP4.
- `computeClusterOrder`/`colorForCluster`/`computeDegree` (exported for `KnowledgeGraphPanels.jsx`) are pure data functions independent of rendering surface and are not expected to change.
- `d3-force` remains the layout engine regardless of rendering surface - this decision does not touch graph topology or force parameters.
- EBG-0081's shared-animation-scheduler question remains separately open; a Canvas-based Guardian Orb would still benefit from participating in a shared scheduler if/when one exists, rather than running its own independent draw loop indefinitely.
- Until implemented, `GuardianOrbGraph.jsx` continues to run as delivered at ESR-0028 WP4 (SVG, seven-round-optimised) - this ADR does not require or imply any immediate change to the running component.

---

# 7. OSE Relationships

| Artefact | Relationship |
|----------|--------------|
| [[UAM-0001_GUARDIAN_EXPERIENCE_ARCHITECTURE_V1|UAM-0001]] | Defines the Guardian Orb's knowledge-graph visual presence (the same sub-section EBG-0055's own EBR-0001 entry cites); this ADR decides its rendering surface, not its visual design intent. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0055 (rendering history) and EBG-0081 (the backlog item whose rendering-engine question this ADR resolves, now Approved - see EBG-0081's own updated entry for the Complete/Candidate split between the decision recorded here and the Canvas-migration implementation still not yet authorised). |
| [[EIP-ESR0028-004_GUARDIAN_ORB_3D_ROTATION|EIP-ESR0028-004]] | ESR-0028 WP4's seven-round optimisation history is this ADR's primary evidence source. |

---

# Related Artefacts

| Artefact | Relationship |
|----------|--------------|
| [[REG-0002_ADR_REGISTER|REG-0002]] | Registers this decision. |
| [[EBR-0001_ENGINEERING_BACKLOG_REGISTER|EBR-0001]] | EBG-0081's rendering-engine question is resolved by this now-Approved ADR - its own entry is updated in the same package to reflect the decision. The separate shared-animation-scheduler half of EBG-0081 remains open Candidate Backlog. Any future Canvas-migration implementation remains separately scoped and separately authorised - not authorised by this ADR itself. |

---

# Version History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.3 | 18 July 2026 | Claude Engineering Implementer | Approved by the Programme Sponsor via the bridge (`sponsor-decision`, `repository_ref: 003d8c9edec3b43ab3ec2a00d41816cef329413a`, 18 July 2026 22:57:04Z). Status promoted Draft to Approved. Updated the two remaining "pending approval" wording instances (Related Artefacts, OSE Relationships) to reflect the decision is now made, while continuing to clarify that no implementation is authorised by this ADR itself. |
| 1.2 | 18 July 2026 | Claude Engineering Implementer | Addressed a residual instance of the v1.0 finding: the OSE Relationships table still described EBG-0081 as something this ADR already "resolves," missed in the v1.1 fix which only corrected the separate Related Artefacts table. Reworded to conditional/draft language matching the rest of the document. |
| 1.1 | 18 July 2026 | Claude Engineering Implementer | Addressed an Engineering Reviewer (Codex) finding on v1.0: the package overstated a still-Draft, not-yet-approved ADR's effect - reworded Related Artefacts to state EBG-0081 remains Candidate Backlog with no implementation authorised until this ADR reaches Approved status, and that any resulting backlog recording is separate future work. REG-0002's changelog entry corrected to match. |
| 1.0 | 18 July 2026 | Claude Engineering Implementer | Initial draft created for ESR-0028 WP5, following the Programme Sponsor's direct request to review (not implement) the rendering-engine question raised during WP4. Recommends Canvas 2D over continued SVG or WebGL/a 3D library, grounded directly in WP4's seven-round optimisation evidence. Not yet Engineering Reviewer or Programme Sponsor reviewed. |
