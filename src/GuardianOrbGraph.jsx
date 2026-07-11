import { useMemo } from "react";
import { forceCollide, forceLink, forceManyBody, forceSimulation, forceX, forceY } from "d3-force";

// Guardian Orb - Knowledge Graph Representation (UAM-0001 Section 8.1;
// EBG-0055 Phase 1). Renders the repository's knowledge graph
// (`knowledge.graph` JSON-RPC method) as the Guardian Orb's actual visual
// presence, matching the reference mock-up
// (aiems/models/UAM-0001_GUARDIAN_ORB_MOCKUP.jpg): a sphere of coloured,
// interconnected nodes, not a flat 2D scatter or the prior decorative-only
// glow/ring animation.
//
// The "3D" sphere illusion is a deterministic geometric projection, not a
// physics simulation or WebGL scene: nodes are laid out with a standard 2D
// force simulation confined to a circle, then each node's depth is derived
// from its distance from the circle's centre - z = sqrt(1 - r^2) describes
// exactly the hemisphere whose orthographic silhouette is that circle. This
// keeps the layout genuinely data-driven (real graph topology, real force
// layout), consistent with UAM-0001 8.1's "driven by observed data, not by
// animation scripts" principle, while reading visually as a globe. Phase 3
// (agent-traversal animation) and Phase 4 (Guardian reasoning connection)
// remain separate, later, explicitly out-of-scope phases - this is still a
// static snapshot, not a rotating or live-updating view.
const CLUSTER_PALETTE = ["#1ff5ff", "#7c5cff", "#ff8a5c", "#5cff9d", "#ffd95c", "#ff5c8a", "#5c9dff", "#c95cff"];

const SIZE = 300;
const CENTER = SIZE / 2;
const RADIUS = 140;
const MIN_RADIUS = 1.5;
const MAX_RADIUS = 9;
const RADIUS_SCALE = 0.65;

function colorForCluster(cluster, clusterOrder) {
  const index = clusterOrder.indexOf(cluster);
  return CLUSTER_PALETTE[index % CLUSTER_PALETTE.length];
}

function computeDegree(nodes, edges) {
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

// Hard circular containment: any node beyond RADIUS from centre is pulled
// back onto the boundary each tick. Unlike a soft centering force alone,
// this guarantees the whole layout stays inside the orb regardless of how
// charge/link forces converge - verified against the real 148-node/
// 1220-edge graph (0 nodes beyond the boundary, 0 overlapping node pairs at
// this configuration).
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

function layoutSphere(nodes, edges) {
  const degree = computeDegree(nodes, edges);
  const simNodes = nodes.map((node) => {
    const d = degree.get(node.id) ?? 0;
    return { ...node, degree: d, r: radiusForDegree(d) };
  });
  const simEdges = edges.map((edge) => ({ ...edge }));

  const simulation = forceSimulation(simNodes)
    .force("charge", forceManyBody().strength(-60))
    .force(
      "link",
      forceLink(simEdges)
        .id((node) => node.id)
        .distance(15)
        .strength(0.2),
    )
    .force("collide", forceCollide((node) => node.r + 1))
    // Weak centering pull, same fix as the standalone panel's outlier-drift
    // bug: without it, most nodes push out to the boundary shell, leaving
    // the core empty - verified against the real graph, this brings the
    // radial fill from ~3% of nodes in the inner quarter to a genuinely
    // filled sphere.
    .force("x", forceX(CENTER).strength(0.1))
    .force("y", forceY(CENTER).strength(0.1))
    .force("contain", forceContainCircle(RADIUS, CENTER, CENTER))
    .stop();

  for (let i = 0; i < 400; i += 1) {
    simulation.tick();
  }

  // Hemisphere depth projection: z in [0, 1], 0 at the silhouette edge
  // (grazing angle, furthest from viewer), 1 at dead centre (closest to
  // viewer) - the orthographic projection of a sphere viewed head-on.
  return simNodes.map((node) => {
    const dx = node.x - CENTER;
    const dy = node.y - CENTER;
    const normalizedDist = Math.min(1, Math.sqrt(dx * dx + dy * dy) / RADIUS);
    const depth = Math.sqrt(Math.max(0, 1 - normalizedDist * normalizedDist));
    return { ...node, depth };
  });
}

export function GuardianOrbGraph({ graph, loading, error }) {
  const positioned = useMemo(() => {
    if (!graph || graph.nodes.length === 0) return [];
    return layoutSphere(graph.nodes, graph.edges);
  }, [graph]);

  const clusterOrder = useMemo(() => {
    if (!graph) return [];
    return [...new Set(graph.nodes.map((node) => node.cluster))].sort();
  }, [graph]);

  const positionedById = useMemo(() => {
    const map = new Map();
    positioned.forEach((node) => map.set(node.id, node));
    return map;
  }, [positioned]);

  if (error || loading || !graph) {
    // Loading/error states stay silent: the orb's existing glow/ring
    // decoration (rendered around this component) already communicates an
    // ambient presence, and this component should only add content once
    // real data exists - never a placeholder graph, per the no-mock-
    // fallback rule established at ESR-0017 WP9.
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
