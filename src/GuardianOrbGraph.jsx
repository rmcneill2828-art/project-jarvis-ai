import { useEffect, useMemo, useRef, useState } from "react";
import { forceCollide, forceLink, forceManyBody, forceSimulation, forceX, forceY } from "d3-force";

// Guardian Orb - Knowledge Graph Representation (UAM-0001 Section 8.1;
// EBG-0055 Phase 1, Phase 1.5; rendering migrated to Canvas 2D at
// ESR-0029 WP2 per ADR-0021). Renders the repository's knowledge graph
// (`knowledge.graph` JSON-RPC method) as the Guardian Orb's actual visual
// presence, matching the reference mock-up
// (aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg): a sphere of coloured,
// interconnected, glowing nodes, not a flat 2D scatter or a decorative-only
// glow/ring animation.
//
// The "3D" sphere is a deterministic geometric model, not a physics engine
// or WebGL scene: nodes are laid out with a standard 2D force simulation
// confined to a circle (this determines real graph topology - which nodes
// cluster near which), then each node is assigned a stable front/back
// hemisphere sign via a hash of its id, giving every node a real (x, y, z)
// position on the sphere's surface. Rotation is a real rotation of those
// (x, y, z) coordinates around the Y axis every animation frame, re-
// projected to 2D - genuine nodes move to the back and are replaced by
// different genuine nodes rotating to the front, not a decorative spin of
// a static image. This keeps the layout genuinely data-driven, consistent
// with UAM-0001 8.1's "driven by observed data, not by animation scripts"
// principle. Phase 3 (agent-traversal animation) and Phase 4 (Guardian
// reasoning connection) remain separate, later, out-of-scope phases - as
// does UAM-0001 8.1's access-triggered cluster illumination, which needs
// real backend activity signal this component does not have.
//
// Rendering is a single <canvas> surface, fully cleared and redrawn each
// animation tick (ADR-0021, EIP-ESR0029-001), replacing an earlier SVG
// implementation where every node/edge was a real DOM element mutated in
// place. That SVG architecture required seven rounds of fixes (ESR-0028
// WP4) to bring a single ambient rotation's cost down and still did not
// clear Windows' "Very high" power-usage classification even after every
// fix - direct evidence the per-element DOM cost, not any single
// implementation detail, was the limiting factor at ~1,880 elements (195
// nodes + 1,687 edges on the real graph). Canvas draws the same element
// count into one bitmap per frame instead of managing ~1,880 individually
// laid-out/painted/composited DOM nodes.
export const CLUSTER_PALETTE = ["#1ff5ff", "#7c5cff", "#ff8a5c", "#5cff9d", "#ffd95c", "#ff5c8a", "#5c9dff", "#c95cff"];

const SIZE = 300;
const CENTER = SIZE / 2;
const RADIUS = 140;
const MIN_RADIUS = 1.5;
const MAX_RADIUS = 9;
const RADIUS_SCALE = 0.65;

// One full rotation roughly every 90 seconds, read as ambient presence
// rather than a spinning logo, per UAM-0001 8.1's "calm interaction"
// product principle. Angle is derived from elapsed wall-clock time, not a
// fixed tick count, so the rotation speed is identical regardless of the
// device's actual achieved frame rate.
const ROTATION_MS_PER_TURN = 90000;
const ANGLE_PER_MS = (2 * Math.PI) / ROTATION_MS_PER_TURN;

// requestAnimationFrame fires at the display's refresh rate (60Hz+, higher
// on gaming monitors); the rotation is far too slow for 60fps to matter
// visually, so the actual redraw work is capped to this interval
// regardless of how often rAF itself fires - still timestamp-driven
// (smooth, frame-rate-independent), just not doing real work on every
// single callback. Carried over unchanged from the SVG-era tuning
// (ESR-0028 WP4); Canvas's different cost profile did not warrant a
// different value on live verification.
const MIN_FRAME_INTERVAL_MS = 1000 / 12;

// Edges (1,687 on the real graph, ~8.6x the 195 nodes) are by far the
// larger share of drawn elements per update. Nodes are the visually
// salient part of the sphere - their motion is what reads as "rotating" -
// while the thin, low-opacity connector lines are background context
// whose position lagging slightly behind the nodes is not perceptible.
// Under Canvas's full-redraw model this can no longer mean "skip drawing
// edges" (they would flicker out of existence for that frame, since
// nothing persists between frames the way DOM elements did) - it means
// recompute edge endpoint positions only every Nth work-frame, but redraw
// the (possibly slightly stale) cached positions on every frame. See
// `edgeCacheRef` in the draw loop.
//
// A first live-verified attempt drew each of the 1,745 real edges with its
// own beginPath/moveTo/lineTo/stroke call every redrawn frame - individually
// depth-varied but, measured via Chrome DevTools Protocol TaskDuration
// against the same real graph, materially *more* expensive than the SVG
// baseline this migration was meant to improve on (~27-29% vs ~9% of one
// core), the opposite of ADR-0021's premise. Root cause: Canvas's full-
// redraw model means those ~1,745 individual draw-call sequences repeat
// every single frame regardless of the recompute-decoupling above, unlike
// SVG's persistent elements, which cost nothing between attribute updates.
// Fixed by bucketing edges into a small number of depth bands and building
// one batched Path2D per band during the (already throttled) recompute
// step - each redrawn frame then issues one stroke() per band (a handful),
// not one per edge, while still preserving the depth-based opacity fade
// (banded, not perfectly continuous, but the original per-edge alpha range
// - 0.55 * (0.06 to 0.20) - is already narrow enough that banding is not
// visually distinguishable from continuous variation).
const EDGE_UPDATE_EVERY_N_FRAMES = 3;
const EDGE_DEPTH_BANDS = 8;

// Page Visibility API: no reason to keep redrawing the sphere 12 times a
// second for a window the user isn't even looking at (minimised, on
// another virtual desktop, or behind other windows).
function isPageVisible() {
  return typeof document === "undefined" || document.visibilityState !== "hidden";
}

// Sustained continuous animation prevents the GPU from reaching its
// deepest idle/power-saving states regardless of how cheap each individual
// update is - confirmed directly against real hardware during the SVG-era
// investigation (ESR-0028 WP4). Pausing after a period of no interaction -
// not just when hidden - keeps this ambient feature from costing power
// indefinitely for as long as the app happens to be open.
const IDLE_TIMEOUT_MS = 45000;
const ACTIVITY_EVENTS = ["mousemove", "mousedown", "keydown", "wheel", "touchstart"];

// Returns a ref (not React state) - the only consumer is the imperative
// rAF loop below, which reads it fresh every frame and has no need to
// trigger a React re-render (or restart its own effect) on every idle/
// active transition.
function useIsIdleRef(timeoutMs) {
  const lastActivityRef = useRef(typeof performance !== "undefined" ? performance.now() : 0);
  const idleRef = useRef(false);

  useEffect(() => {
    if (typeof window === "undefined") return undefined;

    const markActive = () => {
      lastActivityRef.current = performance.now();
      idleRef.current = false;
    };
    ACTIVITY_EVENTS.forEach((event) => window.addEventListener(event, markActive, { passive: true }));

    const checkId = setInterval(() => {
      if (performance.now() - lastActivityRef.current >= timeoutMs) idleRef.current = true;
    }, 5000);

    return () => {
      ACTIVITY_EVENTS.forEach((event) => window.removeEventListener(event, markActive));
      clearInterval(checkId);
    };
  }, [timeoutMs]);

  return idleRef;
}

// Depth-sort (painter's algorithm draw order) is decoupled from the
// per-frame position update: occlusion between two specific nodes only
// visibly changes when their depth order crosses, a slow, infrequent event
// at this rotation speed, so recomputing draw order every 300ms (instead
// of every frame) is visually indistinguishable while avoiding an O(n log
// n) sort of ~195 nodes every animation frame. Under Canvas, nodes are
// still drawn fresh at their current (non-cached) position every frame -
// only the *order* they are drawn in is cached, per `sortOrderRef` below.
const RESORT_INTERVAL_MS = 300;

// Glow-sprite treatment (ESR-0029 WP2, per UAM-0001_GUARDIAN_ORB_MOCKUP.jpg's
// look and layout): one radial-gradient sprite per cluster colour, rendered
// once onto an offscreen canvas and reused via drawImage every frame,
// deliberately avoiding per-node ctx.shadowBlur (a real blur convolution
// per shape, every frame, for up to 195 nodes) or per-node gradient
// object creation. Edges intentionally receive no glow treatment - 1,687
// edges is a materially larger performance surface than 195 nodes.
const GLOW_SPRITE_PX = 128;
const GLOW_RADIUS_MULTIPLIER = 2.6;
const GLOW_CENTER_ALPHA = 0.6;

function buildGlowSprite(color) {
  const canvas = document.createElement("canvas");
  canvas.width = GLOW_SPRITE_PX;
  canvas.height = GLOW_SPRITE_PX;
  const ctx = canvas.getContext("2d");
  const center = GLOW_SPRITE_PX / 2;
  const gradient = ctx.createRadialGradient(center, center, 0, center, center, center);
  gradient.addColorStop(0, `${color}${Math.round(GLOW_CENTER_ALPHA * 255).toString(16).padStart(2, "0")}`);
  gradient.addColorStop(1, `${color}00`);
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, GLOW_SPRITE_PX, GLOW_SPRITE_PX);
  return canvas;
}

function buildGlowSprites() {
  const sprites = new Map();
  for (const color of CLUSTER_PALETTE) {
    sprites.set(color, buildGlowSprite(color));
  }
  return sprites;
}

// Shared with KnowledgeGraphPanels.jsx so the Knowledge Metrics/Active
// Clusters panels use the identical cluster order and colour assignment as
// the Orb itself, rather than a second implementation that could drift.
export function computeClusterOrder(graph) {
  if (!graph) return [];
  return [...new Set(graph.nodes.map((node) => node.cluster))].sort();
}

export function colorForCluster(cluster, clusterOrder) {
  const index = clusterOrder.indexOf(cluster);
  return CLUSTER_PALETTE[index % CLUSTER_PALETTE.length];
}

export function computeDegree(nodes, edges) {
  const degree = new Map(nodes.map((node) => [node.id, 0]));
  for (const edge of edges) {
    degree.set(edge.source, (degree.get(edge.source) ?? 0) + 1);
    degree.set(edge.target, (degree.get(edge.target) ?? 0) + 1);
  }
  return degree;
}

function radiusForDegree(degree) {
  return Math.min(MAX_RADIUS, MIN_RADIUS + Math.sqrt(degree) * RADIUS_SCALE);
}

// Deterministic front/back hemisphere assignment: a stable hash of the
// node's own id, not Math.random() - identical across every re-render and
// re-mount, so the sphere's composition never shuffles on its own.
function hemisphereSign(id) {
  let hash = 0;
  for (let i = 0; i < id.length; i += 1) {
    hash = (hash * 31 + id.charCodeAt(i)) | 0;
  }
  return hash % 2 === 0 ? 1 : -1;
}

// Hard circular containment: any node beyond RADIUS from centre is pulled
// back onto the boundary each tick. Unlike a soft centering force alone,
// this guarantees the whole layout stays inside the orb regardless of how
// charge/link forces converge - re-verified against the real 195-node/
// 1687-edge graph after the Phase 1.5 retuning below (0 nodes beyond the
// boundary, 0 overlapping node pairs, centroid 4.88px off-centre, matching
// the original tuning's own 4.62px baseline).
function forceContainCircle(radius, cx, cy) {
  let nodes;
  function force() {
    for (const node of nodes) {
      const dx = node.x - cx;
      const dy = node.y - cy;
      const dist = Math.sqrt(dx * dx + dy * dy);
      const maxDist = radius - (node.r ?? 0);
      if (dist > maxDist && dist > 0) {
        const k = maxDist / dist;
        node.x = cx + dx * k;
        node.y = cy + dy * k;
      }
    }
  }
  force.initialize = (_nodes) => {
    nodes = _nodes;
  };
  return force;
}

// Base sphere-surface layout: 2D force-simulated (x, y) topology (unchanged
// in spirit from Phase 1) plus a real z coordinate from the deterministic
// hemisphere sign. This is computed once per graph and never mutated by
// rotation - rotation operates on these fixed base coordinates each frame.
//
// Phase 1.5 force retuning: charge -60 to -100 and link strength 0.2 to
// 0.05, informed by the Programme Sponsor's own tuned Obsidian graph-view
// measurements (Repel Force at that control's maximum, Link force at its
// minimum) read as directional signal, not literal values - this system's
// hard containment force means Obsidian's literal numbers don't port (see
// EIP-ESR0028-004 Section 4.4). Central force strength moved from 0.5 to
// 0.53, the one dimension where the Sponsor's own number ports directly,
// since it was already almost identical to this component's prior value.
// Re-verified against the real graph: 0 overlaps, 0 nodes beyond boundary,
// centroid 4.88px off-centre (original: 4.62px) - both well within the
// original tuning's own precedent.
function layoutSphere(nodes, edges) {
  const degree = computeDegree(nodes, edges);
  const simNodes = nodes.map((node) => {
    const d = degree.get(node.id) ?? 0;
    return { ...node, degree: d, r: radiusForDegree(d) };
  });
  const simEdges = edges.map((edge) => ({ ...edge }));

  const simulation = forceSimulation(simNodes)
    .force("charge", forceManyBody().strength(-100))
    .force(
      "link",
      forceLink(simEdges)
        .id((node) => node.id)
        .distance(15)
        .strength(0.05),
    )
    .force("collide", forceCollide((node) => node.r + 1))
    .force("x", forceX(CENTER).strength(0.53))
    .force("y", forceY(CENTER).strength(0.53))
    .force("contain", forceContainCircle(RADIUS, CENTER, CENTER))
    .stop();

  for (let i = 0; i < 400; i += 1) {
    simulation.tick();
  }

  return simNodes.map((node) => {
    const dx = node.x - CENTER;
    const dy = node.y - CENTER;
    const normalizedDist = Math.min(1, Math.sqrt(dx * dx + dy * dy) / RADIUS);
    const zMagnitude = RADIUS * Math.sqrt(Math.max(0, 1 - normalizedDist * normalizedDist));
    return { ...node, bx: dx, by: dy, bz: hemisphereSign(node.id) * zMagnitude };
  });
}

function usePrefersReducedMotion() {
  const [reduced, setReduced] = useState(
    () => typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches,
  );

  useEffect(() => {
    if (typeof window === "undefined") return undefined;
    const query = window.matchMedia("(prefers-reduced-motion: reduce)");
    const handleChange = (event) => setReduced(event.matches);
    query.addEventListener("change", handleChange);
    return () => query.removeEventListener("change", handleChange);
  }, []);

  return reduced;
}

// Real Y-axis rotation of the base sphere coordinates: bx/bz rotate,
// by is unchanged (rotation axis is vertical). Depth is renormalised from
// the rotated z into [0, 1] for the existing opacity/size treatment.
function rotateNode(node, cos, sin) {
  const rx = node.bx * cos - node.bz * sin;
  const rz = node.bx * sin + node.bz * cos;
  const depth = (rz + RADIUS) / (2 * RADIUS);
  return { x: CENTER + rx, y: CENTER + node.by, z: rz, depth };
}

export function GuardianOrbGraph({ graph, loading, error }) {
  const baseNodes = useMemo(() => {
    if (!graph || graph.nodes.length === 0) return [];
    return layoutSphere(graph.nodes, graph.edges);
  }, [graph]);

  const prefersReducedMotion = usePrefersReducedMotion();
  const isIdleRef = useIsIdleRef(IDLE_TIMEOUT_MS);
  const clusterOrder = useMemo(() => computeClusterOrder(graph), [graph]);
  const glowSprites = useMemo(() => buildGlowSprites(), []);

  const canvasRef = useRef(null);
  // Latest drawn node screen positions + hit radius, kept for manual
  // hit-testing (Canvas has no free per-shape hit-testing the way SVG did).
  const hitTestRef = useRef([]);

  const labelById = useMemo(() => {
    const map = new Map();
    if (graph) graph.nodes.forEach((node) => map.set(node.id, node.label));
    return map;
  }, [graph]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || baseNodes.length === 0) return undefined;

    const ctx = canvas.getContext("2d");
    const nodeById = new Map(baseNodes.map((node) => [node.id, node]));
    const edgeCacheRef = { current: null };
    const sortOrderRef = { current: null };

    const startTime = performance.now();
    let lastResort = startTime;
    let currentAngle = 0;
    let frameCount = 0;
    let now = startTime;
    let frameId;

    const drawFrame = (angle, forceFullRecompute) => {
      const cos = Math.cos(angle);
      const sin = Math.sin(angle);
      const currentById = new Map();

      for (const node of baseNodes) {
        const projected = rotateNode(node, cos, sin);
        currentById.set(node.id, projected);
      }

      if (forceFullRecompute || frameCount % EDGE_UPDATE_EVERY_N_FRAMES === 0 || edgeCacheRef.current === null) {
        const bandPaths = Array.from({ length: EDGE_DEPTH_BANDS }, () => new Path2D());
        const bandDepthSum = new Array(EDGE_DEPTH_BANDS).fill(0);
        const bandCount = new Array(EDGE_DEPTH_BANDS).fill(0);
        for (const edge of graph.edges) {
          const source = currentById.get(edge.source);
          const target = currentById.get(edge.target);
          if (!source || !target) continue;
          const depth = (source.depth + target.depth) / 2;
          const band = Math.min(EDGE_DEPTH_BANDS - 1, Math.floor(depth * EDGE_DEPTH_BANDS));
          bandPaths[band].moveTo(source.x, source.y);
          bandPaths[band].lineTo(target.x, target.y);
          bandDepthSum[band] += depth;
          bandCount[band] += 1;
        }
        edgeCacheRef.current = bandPaths
          .map((path, band) => ({
            path,
            opacity: bandCount[band] > 0 ? 0.06 + (bandDepthSum[band] / bandCount[band]) * 0.14 : 0,
          }))
          .filter((band) => band.opacity > 0);
      }

      if (forceFullRecompute || now - lastResort >= RESORT_INTERVAL_MS || sortOrderRef.current === null) {
        sortOrderRef.current = [...currentById.entries()].sort((a, b) => a[1].z - b[1].z).map(([id]) => id);
        lastResort = now;
      }

      // Hit-testing must search in the same back-to-front order nodes are
      // actually painted in (sortOrderRef.current), not baseNodes' arbitrary
      // iteration order - otherwise, for overlapping nodes, handlePointerMove
      // could report a node the pointer isn't actually looking at instead of
      // the frontmost visible one (Engineering Reviewer finding, ESR-0029
      // WP2 post-implementation review). Built fresh from currentById every
      // frame regardless of the resort-interval cache above, since hit
      // targets must track each node's current rotated position, not a
      // stale cached one.
      const hitEntries = [];
      for (const id of sortOrderRef.current) {
        const projected = currentById.get(id);
        const node = nodeById.get(id);
        if (!projected || !node) continue;
        hitEntries.push({ id, x: projected.x, y: projected.y, r: node.r * (0.6 + projected.depth * 0.4) });
      }
      hitTestRef.current = hitEntries;

      ctx.clearRect(0, 0, SIZE, SIZE);

      // Edges never need the circular clip below: forceContainCircle keeps
      // every node within RADIUS of centre, rotation preserves each node's
      // distance from centre (it moves points on a fixed sphere), and a
      // disk is convex - a line between two points inside it never leaves
      // it. Only node glow sprites (Section 4.3) can extend past RADIUS for
      // nodes sitting right at the boundary, so only the node-drawing pass
      // is clipped. This matters a great deal in practice, not just in
      // principle: live-verified via Chrome DevTools Protocol TaskDuration
      // against the real graph, clipping the edge-stroke calls too cost
      // ~20 percentage points of one core on its own (clip-vs-complex-path
      // intersection appears to be the expensive combination, not either
      // alone) - confining the clip to the ~200 node draws instead of all
      // ~1,745 edges was the single largest factor in this migration
      // actually reducing cost versus the SVG baseline it replaces.
      ctx.lineWidth = 0.4;
      ctx.strokeStyle = "rgb(0, 239, 255)";
      for (const band of edgeCacheRef.current) {
        ctx.globalAlpha = 0.55 * band.opacity;
        ctx.stroke(band.path);
      }

      ctx.save();
      ctx.beginPath();
      ctx.arc(CENTER, CENTER, RADIUS, 0, 2 * Math.PI);
      ctx.clip();

      for (const id of sortOrderRef.current) {
        const projected = currentById.get(id);
        const node = nodeById.get(id);
        if (!projected || !node) continue;
        const coreRadius = node.r * (0.6 + projected.depth * 0.4);
        const depthAlpha = 0.45 + projected.depth * 0.55;
        const color = colorForCluster(node.cluster, clusterOrder);
        const sprite = glowSprites.get(color);

        ctx.globalAlpha = depthAlpha;
        if (sprite) {
          const glowRadius = coreRadius * GLOW_RADIUS_MULTIPLIER;
          ctx.drawImage(sprite, projected.x - glowRadius, projected.y - glowRadius, glowRadius * 2, glowRadius * 2);
        }

        ctx.beginPath();
        ctx.arc(projected.x, projected.y, coreRadius, 0, 2 * Math.PI);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.lineWidth = 0.3;
        ctx.strokeStyle = "rgb(2, 7, 9)";
        ctx.stroke();
      }

      ctx.restore();
      ctx.globalAlpha = 1;
    };

    // Canvas has no viewBox equivalent: SVG scaled the same 0-SIZE
    // coordinate space to any rendered container size for free. Here the
    // backing store is sized explicitly to the container's actual
    // rendered CSS size x devicePixelRatio, then the context is scaled so
    // drawFrame above can keep using the existing 0-SIZE coordinate math
    // unchanged, regardless of the container's real pixel size.
    const applySize = (renderedWidth, renderedHeight) => {
      const dpr = typeof window !== "undefined" ? window.devicePixelRatio || 1 : 1;
      const width = Math.max(1, Math.round(renderedWidth * dpr));
      const height = Math.max(1, Math.round(renderedHeight * dpr));
      canvas.width = width;
      canvas.height = height;
      const scale = Math.min(width, height) / SIZE;
      ctx.setTransform(scale, 0, 0, scale, 0, 0);
      drawFrame(currentAngle, true);
    };

    const resizeObserver = new ResizeObserver((entries) => {
      const entry = entries[0];
      if (!entry) return;
      const { width, height } = entry.contentRect;
      if (width > 0 && height > 0) applySize(width, height);
    });
    resizeObserver.observe(canvas);

    // Initial size + first paint, before any rAF loop starts - Canvas has
    // no declarative initial render the way JSX-rendered SVG elements did,
    // so an explicit first draw is required regardless of animation state.
    const rect = canvas.getBoundingClientRect();
    applySize(rect.width || SIZE, rect.height || SIZE);

    if (prefersReducedMotion) {
      return () => resizeObserver.disconnect();
    }

    let lastFrame = startTime;

    const handleVisibilityChange = () => {
      if (isPageVisible()) lastFrame = performance.now();
    };
    document.addEventListener("visibilitychange", handleVisibilityChange);

    const tick = (frameNow) => {
      frameId = requestAnimationFrame(tick);
      now = frameNow;

      if (!isPageVisible() || isIdleRef.current) {
        lastFrame = frameNow;
        return;
      }

      if (frameNow - lastFrame < MIN_FRAME_INTERVAL_MS) return;
      currentAngle += ANGLE_PER_MS * (frameNow - lastFrame);
      lastFrame = frameNow;
      frameCount += 1;

      drawFrame(currentAngle, false);
    };

    frameId = requestAnimationFrame(tick);
    return () => {
      cancelAnimationFrame(frameId);
      resizeObserver.disconnect();
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, [prefersReducedMotion, baseNodes, clusterOrder, glowSprites, graph]);

  const handlePointerMove = (event) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const localX = ((event.clientX - rect.left) / rect.width) * SIZE;
    const localY = ((event.clientY - rect.top) / rect.height) * SIZE;

    const hits = hitTestRef.current;
    let found = null;
    for (let i = hits.length - 1; i >= 0; i -= 1) {
      const candidate = hits[i];
      const dx = localX - candidate.x;
      const dy = localY - candidate.y;
      if (dx * dx + dy * dy <= candidate.r * candidate.r) {
        found = candidate;
        break;
      }
    }
    canvas.title = found ? labelById.get(found.id) ?? "" : "";
  };

  const handlePointerLeave = () => {
    const canvas = canvasRef.current;
    if (canvas) canvas.title = "";
  };

  if (error || loading || !graph) {
    // Loading/error states stay silent: this component should only add
    // content once real data exists - never a placeholder graph, per the
    // no-mock-fallback rule established at ESR-0017 WP9.
    return null;
  }

  return (
    <canvas
      ref={canvasRef}
      width={SIZE}
      height={SIZE}
      className="guardian-orb-graph"
      role="img"
      aria-label={`Guardian Orb: repository knowledge graph with ${graph.nodes.length} artefacts and ${graph.edges.length} relationships`}
      onPointerMove={handlePointerMove}
      onPointerLeave={handlePointerLeave}
    />
  );
}
