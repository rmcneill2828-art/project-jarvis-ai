import { useMemo } from "react";
import { forceCenter, forceCollide, forceLink, forceManyBody, forceSimulation, forceX, forceY } from "d3-force";

// EBG-0055 Phase 1 (ESR-0019 WP2): first-pass rendering of the repository
// knowledge graph returned by the `knowledge.graph` JSON-RPC method
// (jarvis/interfaces/knowledge_graph.py, ADR-0019 bridge).
//
// A small, deterministic palette keyed by cluster name - purely cosmetic
// grouping to keep ~150 nodes legible. This is not the cluster-illumination
// system described in UAM-0001 Section 8.1/8.2; that is Phase 2, not built
// here.
const CLUSTER_PALETTE = ["#1ff5ff", "#7c5cff", "#ff8a5c", "#5cff9d", "#ffd95c", "#ff5c8a", "#5c9dff", "#c95cff"];

const WIDTH = 900;
const HEIGHT = 600;
const PADDING = 16;

// Node sizing and hub labelling, added per the Programme Sponsor's Obsidian
// graph-view reference: well-connected artefacts should read as visually
// larger, and only the most-connected "hub" nodes carry a visible label -
// labelling all 148 would just reproduce Obsidian's own cluttered result,
// not improve on it. Everything else remains reachable via the existing
// hover tooltip.
const HUB_LABEL_COUNT = 25;
const MIN_RADIUS = 3;
const MAX_RADIUS = 18;
const RADIUS_SCALE = 1.3;

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

function topHubIds(nodes, edges, count) {
  const degree = computeDegree(nodes, edges);
  return new Set(
    [...degree.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, count)
      .map(([id]) => id),
  );
}

// Rescales converged simulation coordinates into the SVG viewBox. The
// simulation is run in its own natural (unbounded) coordinate space - its
// equilibrium spread is typically far larger than any fixed viewBox, so
// nodes must be rescaled afterward rather than relying on the simulation to
// land within [0, WIDTH] x [0, HEIGHT] on its own. Scaled independently per
// axis (not preserving aspect ratio): the simulation's natural spread is
// roughly square regardless of the target viewBox's aspect ratio, so a
// uniform scale is bottlenecked by whichever axis is more constrained,
// compressing the other axis and creating avoidable overlap.
function normalizeToViewBox(nodes, width, height, padding) {
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;
  for (const node of nodes) {
    minX = Math.min(minX, node.x);
    maxX = Math.max(maxX, node.x);
    minY = Math.min(minY, node.y);
    maxY = Math.max(maxY, node.y);
  }
  const spanX = Math.max(maxX - minX, 1);
  const spanY = Math.max(maxY - minY, 1);
  const scaleX = (width - 2 * padding) / spanX;
  const scaleY = (height - 2 * padding) / spanY;

  return nodes.map((node) => ({
    ...node,
    x: padding + (node.x - minX) * scaleX,
    y: padding + (node.y - minY) * scaleY,
  }));
}

// Runs a bounded, synchronous force simulation and returns positioned nodes,
// rescaled to fit the viewBox. Deliberately not an animated/running
// simulation - EBG-0055 Phase 1 is a static graph snapshot, not a live
// physics view. Phase 3 (agent-traversal animation) is a separate, later,
// explicitly out-of-scope phase.
function layoutGraph(nodes, edges) {
  const degree = computeDegree(nodes, edges);
  const simNodes = nodes.map((node) => ({ ...node, degree: degree.get(node.id) ?? 0 }));
  // forceLink mutates each link's source/target from a string id into a
  // node object reference as part of its own internal bookkeeping - copying
  // here keeps that mutation off the `edges` array from component state
  // (graph.edges), which the render below still looks up by string id.
  const simEdges = edges.map((edge) => ({ ...edge }));

  const simulation = forceSimulation(simNodes)
    .force("charge", forceManyBody().strength(-500))
    .force(
      "link",
      forceLink(simEdges)
        .id((node) => node.id)
        .distance(70)
        .strength(0.05),
    )
    .force("center", forceCenter(WIDTH / 2, HEIGHT / 2))
    // Per-node collide radius (not a flat value): a well-connected node
    // renders larger (radiusForDegree), so its collision boundary must scale
    // the same way or big circles would overlap their smaller neighbours.
    .force("collide", forceCollide((node) => radiusForDegree(node.degree) + 2))
    // forceCenter alone only recentres the barycenter - it does not stop
    // individual low-degree/loosely-connected nodes drifting arbitrarily far
    // under repulsion. Confirmed against the real graph: without this, 16 of
    // 148 nodes end up beyond 3x the median distance from the centroid,
    // which then dominates normalizeToViewBox's scale and crushes the real
    // cluster into a tiny fraction of the canvas. A weak per-node restoring
    // pull (matching Obsidian's own "Centre force" graph-view setting)
    // removes that: 0 outliers beyond 3x median at this strength.
    .force("x", forceX(WIDTH / 2).strength(0.1))
    .force("y", forceY(HEIGHT / 2).strength(0.1))
    .stop();

  for (let i = 0; i < 600; i += 1) {
    simulation.tick();
  }

  return normalizeToViewBox(simNodes, WIDTH, HEIGHT, PADDING);
}

export function KnowledgeGraph({ graph, loading, error }) {
  const positioned = useMemo(() => {
    if (!graph || graph.nodes.length === 0) return [];
    return layoutGraph(graph.nodes, graph.edges);
  }, [graph]);

  const clusterOrder = useMemo(() => {
    if (!graph) return [];
    return [...new Set(graph.nodes.map((node) => node.cluster))].sort();
  }, [graph]);

  const hubIds = useMemo(() => {
    if (!graph) return new Set();
    return topHubIds(graph.nodes, graph.edges, HUB_LABEL_COUNT);
  }, [graph]);

  const positionedById = useMemo(() => {
    const map = new Map();
    positioned.forEach((node) => map.set(node.id, node));
    return map;
  }, [positioned]);

  if (error) {
    return (
      <section className="knowledge-graph-panel" aria-labelledby="knowledge-graph-heading">
        <h2 id="knowledge-graph-heading">Knowledge Graph</h2>
        <p className="knowledge-graph-error" role="alert">
          Knowledge graph is unavailable: {error}
        </p>
      </section>
    );
  }

  if (loading || !graph) {
    return (
      <section className="knowledge-graph-panel" aria-labelledby="knowledge-graph-heading">
        <h2 id="knowledge-graph-heading">Knowledge Graph</h2>
        <p className="knowledge-graph-status">Loading repository knowledge graph...</p>
      </section>
    );
  }

  return (
    <section className="knowledge-graph-panel" aria-labelledby="knowledge-graph-heading">
      <h2 id="knowledge-graph-heading">Knowledge Graph</h2>
      <p className="knowledge-graph-status">
        {graph.nodes.length} artefacts, {graph.edges.length} relationships - EBG-0055 Phase 1 static snapshot
      </p>
      <svg
        viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
        className="knowledge-graph-svg"
        role="img"
        aria-label={`Repository knowledge graph with ${graph.nodes.length} artefacts and ${graph.edges.length} relationships`}
      >
        <g className="knowledge-graph-edges">
          {graph.edges.map((edge) => {
            const source = positionedById.get(edge.source);
            const target = positionedById.get(edge.target);
            if (!source || !target) return null;
            return <line key={`${edge.source}->${edge.target}`} x1={source.x} y1={source.y} x2={target.x} y2={target.y} />;
          })}
        </g>
        <g className="knowledge-graph-nodes">
          {positioned.map((node) => (
            <circle
              key={node.id}
              cx={node.x}
              cy={node.y}
              r={radiusForDegree(node.degree)}
              fill={colorForCluster(node.cluster, clusterOrder)}
            >
              <title>{node.label}</title>
            </circle>
          ))}
        </g>
        <g className="knowledge-graph-labels">
          {positioned
            .filter((node) => hubIds.has(node.id))
            .map((node) => (
              <text key={node.id} x={node.x + radiusForDegree(node.degree) + 4} y={node.y + 4}>
                {node.label}
              </text>
            ))}
        </g>
      </svg>
    </section>
  );
}
