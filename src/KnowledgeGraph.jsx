import { useMemo } from "react";
import { forceCenter, forceCollide, forceLink, forceManyBody, forceSimulation } from "d3-force";

// EBG-0055 Phase 1 (ESR-0019 WP2): first-pass rendering of the repository
// knowledge graph returned by the `knowledge.graph` JSON-RPC method
// (jarvis/interfaces/knowledge_graph.py, ADR-0019 bridge).
//
// A small, deterministic palette keyed by cluster name - purely cosmetic
// grouping to keep ~150 nodes legible. This is not the cluster-illumination
// system described in UAM-0001 Section 8.1/8.2; that is Phase 2, not built
// here.
const CLUSTER_PALETTE = ["#1ff5ff", "#7c5cff", "#ff8a5c", "#5cff9d", "#ffd95c", "#ff5c8a", "#5c9dff", "#c95cff"];

const WIDTH = 640;
const HEIGHT = 420;

function colorForCluster(cluster, clusterOrder) {
  const index = clusterOrder.indexOf(cluster);
  return CLUSTER_PALETTE[index % CLUSTER_PALETTE.length];
}

// Runs a bounded, synchronous force simulation and returns positioned nodes.
// Deliberately not an animated/running simulation - EBG-0055 Phase 1 is a
// static graph snapshot, not a live physics view. Phase 3 (agent-traversal
// animation) is a separate, later, explicitly out-of-scope phase.
function layoutGraph(nodes, edges) {
  const simNodes = nodes.map((node) => ({ ...node }));
  const simulation = forceSimulation(simNodes)
    .force("charge", forceManyBody().strength(-40))
    .force(
      "link",
      forceLink(edges)
        .id((node) => node.id)
        .distance(28)
        .strength(0.15),
    )
    .force("center", forceCenter(WIDTH / 2, HEIGHT / 2))
    .force("collide", forceCollide(5))
    .stop();

  for (let i = 0; i < 300; i += 1) {
    simulation.tick();
  }

  return simNodes;
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
            <circle key={node.id} cx={node.x} cy={node.y} r={4} fill={colorForCluster(node.cluster, clusterOrder)}>
              <title>{node.label}</title>
            </circle>
          ))}
        </g>
      </svg>
    </section>
  );
}
