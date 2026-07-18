import { useEffect, useMemo, useRef, useState } from "react";
import { forceCollide, forceLink, forceManyBody, forceSimulation, forceX, forceY } from "d3-force";

// Guardian Orb - Knowledge Graph Representation (UAM-0001 Section 8.1;
// EBG-0055 Phase 1, Phase 1.5). Renders the repository's knowledge graph
// (`knowledge.graph` JSON-RPC method) as the Guardian Orb's actual visual
// presence, matching the reference mock-up
// (aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg): a sphere of coloured,
// interconnected nodes, not a flat 2D scatter or a decorative-only
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
// reasoning connection) remain separate, later, out-of-scope phases.
//
// Rotation is driven by direct DOM attribute updates inside a
// requestAnimationFrame loop, not React state/re-render, per node/edge
// element. An earlier version drove rotation through React state (a full
// re-render of ~1,880 SVG elements - 195 nodes + 1,687 edges on the real
// graph - every tick), which measured as sustained "Very high" power
// usage on real hardware even after throttling the tick rate, and
// throttling alone made the motion visibly choppy. Bypassing React's
// reconciliation for the animation hot path fixes both: smooth,
// frame-rate-independent motion at a fraction of the CPU/GPU cost, since
// attribute mutation on existing DOM nodes is far cheaper than React
// re-rendering and diffing the same element count every frame.
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
// on gaming monitors) - measured directly against real hardware, an
// uncapped rAF loop mutating ~1,880 SVG element attributes (195 nodes +
// 1,687 edges on the real graph) every single frame still sustained
// "Very high" Windows power usage even after moving the mutation itself
// off React's render cycle (confirmed via an isolated Task Manager
// comparison: rotation on vs off, with no other confounding process
// running). The rotation is far too slow for 60fps to matter visually, so
// the actual DOM-mutation work is capped to this interval regardless of
// how often rAF itself fires - still timestamp-driven (smooth, frame-rate-
// independent), just not doing real work on every single callback.
const MIN_FRAME_INTERVAL_MS = 1000 / 12;

// Edges (1,687 on the real graph, ~8.6x the 195 nodes) are by far the
// larger share of the ~1,880 mutated elements per update. Nodes are the
// visually salient part of the sphere - their motion is what reads as
// "rotating" - while the thin, low-opacity connector lines are background
// context whose position lagging slightly behind the nodes is not
// perceptible. Updating them at a third of the node rate cuts the
// dominant share of the remaining per-update DOM-write cost with no
// visible effect on the rotation itself.
const EDGE_UPDATE_EVERY_N_FRAMES = 3;

// Page Visibility API: no reason to keep mutating ~1,880 SVG elements 12
// times a second for a window the user isn't even looking at (minimised,
// on another virtual desktop, or behind other windows).
function isPageVisible() {
  return typeof document === "undefined" || document.visibilityState !== "hidden";
}

// Node DOM re-sort (painter's algorithm draw order) is decoupled from the
// per-frame position update: occlusion between two specific nodes only
// visibly changes when their depth order crosses, a slow, infrequent event
// at this rotation speed, so re-sorting the DOM every 300ms (instead of
// every frame) is visually indistinguishable while avoiding a full
// insertBefore/appendChild pass on every animation frame.
const RESORT_INTERVAL_MS = 300;

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

  const clusterOrder = useMemo(() => computeClusterOrder(graph), [graph]);

  // Initial (angle = 0) positions for first paint - React renders this once;
  // the rAF loop below then mutates these same DOM nodes directly.
  const initialPositioned = useMemo(() => {
    return baseNodes.map((node) => ({ ...node, ...rotateNode(node, 1, 0) }));
  }, [baseNodes]);

  const initialPositionedById = useMemo(() => {
    const map = new Map();
    initialPositioned.forEach((node) => map.set(node.id, node));
    return map;
  }, [initialPositioned]);

  const nodeGroupRef = useRef(null);
  const nodeElementsRef = useRef(new Map());
  const edgeElementsRef = useRef(new Map());

  useEffect(() => {
    if (prefersReducedMotion || baseNodes.length === 0) return undefined;

    const nodeGroup = nodeGroupRef.current;
    const nodeElements = nodeElementsRef.current;
    const edgeElements = edgeElementsRef.current;
    const startTime = performance.now();
    let lastResort = startTime;
    let lastFrame = startTime;
    let frameCount = 0;
    let frameId;

    const tick = (now) => {
      frameId = requestAnimationFrame(tick);
      if (!isPageVisible()) return;
      if (now - lastFrame < MIN_FRAME_INTERVAL_MS) return;
      lastFrame = now;
      frameCount += 1;

      const angle = ANGLE_PER_MS * (now - startTime);
      const cos = Math.cos(angle);
      const sin = Math.sin(angle);
      const currentById = new Map();

      for (const node of baseNodes) {
        const projected = rotateNode(node, cos, sin);
        currentById.set(node.id, projected);
        const circle = nodeElements.get(node.id);
        if (circle) {
          circle.setAttribute("cx", projected.x);
          circle.setAttribute("cy", projected.y);
          circle.setAttribute("r", node.r * (0.6 + projected.depth * 0.4));
          circle.style.opacity = 0.45 + projected.depth * 0.55;
        }
      }

      if (frameCount % EDGE_UPDATE_EVERY_N_FRAMES === 0) {
        for (const [key, line] of edgeElements) {
          const [sourceId, targetId] = key.split("->");
          const source = currentById.get(sourceId);
          const target = currentById.get(targetId);
          if (!source || !target) continue;
          const depth = (source.depth + target.depth) / 2;
          line.setAttribute("x1", source.x);
          line.setAttribute("y1", source.y);
          line.setAttribute("x2", target.x);
          line.setAttribute("y2", target.y);
          line.style.opacity = 0.06 + depth * 0.14;
        }
      }

      // Periodic DOM re-sort for correct front/back occlusion
      // (painter's algorithm) - appendChild on an already-attached node
      // moves it to the end, so appending back-to-front reorders cheaply.
      if (nodeGroup && now - lastResort >= RESORT_INTERVAL_MS) {
        lastResort = now;
        const order = [...currentById.entries()].sort((a, b) => a[1].z - b[1].z);
        for (const [id] of order) {
          const circle = nodeElements.get(id);
          if (circle) nodeGroup.appendChild(circle);
        }
      }
    };

    frameId = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frameId);
  }, [prefersReducedMotion, baseNodes]);

  if (error || loading || !graph) {
    // Loading/error states stay silent: this component should only add
    // content once real data exists - never a placeholder graph, per the
    // no-mock-fallback rule established at ESR-0017 WP9.
    return null;
  }

  return (
    <svg
      viewBox={`0 0 ${SIZE} ${SIZE}`}
      className="guardian-orb-graph"
      role="img"
      aria-label={`Guardian Orb: repository knowledge graph with ${graph.nodes.length} artefacts and ${graph.edges.length} relationships`}
    >
      <defs>
        <clipPath id="guardian-orb-clip">
          <circle cx={CENTER} cy={CENTER} r={RADIUS} />
        </clipPath>
      </defs>
      <g clipPath="url(#guardian-orb-clip)">
        <g className="guardian-orb-graph-edges">
          {graph.edges.map((edge) => {
            const source = initialPositionedById.get(edge.source);
            const target = initialPositionedById.get(edge.target);
            if (!source || !target) return null;
            const depth = (source.depth + target.depth) / 2;
            const key = `${edge.source}->${edge.target}`;
            return (
              <line
                key={key}
                ref={(el) => {
                  if (el) edgeElementsRef.current.set(key, el);
                  else edgeElementsRef.current.delete(key);
                }}
                x1={source.x}
                y1={source.y}
                x2={target.x}
                y2={target.y}
                style={{ opacity: 0.06 + depth * 0.14 }}
              />
            );
          })}
        </g>
        <g className="guardian-orb-graph-nodes" ref={nodeGroupRef}>
          {initialPositioned.map((node) => (
            <circle
              key={node.id}
              ref={(el) => {
                if (el) nodeElementsRef.current.set(node.id, el);
                else nodeElementsRef.current.delete(node.id);
              }}
              cx={node.x}
              cy={node.y}
              r={node.r * (0.6 + node.depth * 0.4)}
              fill={colorForCluster(node.cluster, clusterOrder)}
              style={{ opacity: 0.45 + node.depth * 0.55 }}
            >
              <title>{node.label}</title>
            </circle>
          ))}
        </g>
      </g>
    </svg>
  );
}
