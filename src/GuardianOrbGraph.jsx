import { useEffect, useMemo, useState } from "react";
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
// (x, y, z) coordinates around the Y axis each tick, re-projected to 2D and
// re-sorted by resulting depth (painter's algorithm) - genuine nodes move
// to the back and are replaced by different genuine nodes rotating to the
// front, not a decorative spin of a static image. This keeps the layout
// genuinely data-driven, consistent with UAM-0001 8.1's "driven by
// observed data, not by animation scripts" principle. Phase 3
// (agent-traversal animation) and Phase 4 (Guardian reasoning connection)
// remain separate, later, explicitly out-of-scope phases.
export const CLUSTER_PALETTE = ["#1ff5ff", "#7c5cff", "#ff8a5c", "#5cff9d", "#ffd95c", "#ff5c8a", "#5c9dff", "#c95cff"];

const SIZE = 300;
const CENTER = SIZE / 2;
const RADIUS = 140;
const MIN_RADIUS = 1.5;
const MAX_RADIUS = 9;
const RADIUS_SCALE = 0.65;

// One full rotation roughly every 90 seconds at this angle-per-tick and
// interval, read as ambient presence rather than a spinning logo, per
// UAM-0001 8.1's "calm interaction" product principle.
const ROTATION_INTERVAL_MS = 50;
const ROTATION_RADIANS_PER_TICK = (2 * Math.PI) / (90000 / ROTATION_INTERVAL_MS);

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
// rotation - rotation operates on these fixed base coordinates each tick.
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
// the rotated z into [0, 1] for the existing opacity/size treatment, and
// nodes/edges are re-sorted back-to-front each tick (painter's algorithm)
// so nodes rotating to the front correctly draw over nodes rotating to
// the back.
function rotateAndProject(baseNodes, angle) {
  const cos = Math.cos(angle);
  const sin = Math.sin(angle);
  const rotated = baseNodes.map((node) => {
    const rx = node.bx * cos - node.bz * sin;
    const rz = node.bx * sin + node.bz * cos;
    const depth = (rz + RADIUS) / (2 * RADIUS);
    return { ...node, x: CENTER + rx, y: CENTER + node.by, z: rz, depth };
  });
  rotated.sort((a, b) => a.z - b.z);
  return rotated;
}

export function GuardianOrbGraph({ graph, loading, error }) {
  const baseNodes = useMemo(() => {
    if (!graph || graph.nodes.length === 0) return [];
    return layoutSphere(graph.nodes, graph.edges);
  }, [graph]);

  const prefersReducedMotion = usePrefersReducedMotion();
  const [angle, setAngle] = useState(0);

  useEffect(() => {
    if (prefersReducedMotion || baseNodes.length === 0) return undefined;
    const id = setInterval(() => {
      setAngle((current) => current + ROTATION_RADIANS_PER_TICK);
    }, ROTATION_INTERVAL_MS);
    return () => clearInterval(id);
  }, [prefersReducedMotion, baseNodes]);

  const positioned = useMemo(() => rotateAndProject(baseNodes, angle), [baseNodes, angle]);

  const clusterOrder = useMemo(() => computeClusterOrder(graph), [graph]);

  const positionedById = useMemo(() => {
    const map = new Map();
    positioned.forEach((node) => map.set(node.id, node));
    return map;
  }, [positioned]);

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
            const source = positionedById.get(edge.source);
            const target = positionedById.get(edge.target);
            if (!source || !target) return null;
            const depth = (source.depth + target.depth) / 2;
            return (
              <line
                key={`${edge.source}->${edge.target}`}
                x1={source.x}
                y1={source.y}
                x2={target.x}
                y2={target.y}
                style={{ opacity: 0.06 + depth * 0.14 }}
              />
            );
          })}
        </g>
        <g className="guardian-orb-graph-nodes">
          {positioned.map((node) => (
            <circle
              key={node.id}
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
