import { colorForCluster, computeClusterOrder, computeDegree } from "./GuardianOrbGraph.jsx";

// Knowledge Metrics and Active Clusters panels (UAM-0001_GUARDIAN_ORB_MOCKUP.jpg
// reference layout; EBG-0055 continuation). Both derive entirely from the same
// `knowledge.graph` data the Orb already renders - no new backend call, no
// fabricated figures. Per the no-mock-fallback rule (ESR-0017 WP9), a
// not-yet-resolved or failed graph fetch shows an honest connecting/error
// message rather than a zeroed-out or placeholder metric set.

function formatPercent(value) {
  return `${value.toFixed(2)}%`;
}

function PanelStatusMessage({ error }) {
  return <p className="panel-status-message">{error ? "Knowledge graph is unavailable." : "Connecting to the knowledge graph..."}</p>;
}

export function KnowledgeMetricsPanel({ graph, error }) {
  if (!graph) {
    return (
      <aside className="knowledge-metrics-panel" aria-labelledby="knowledge-metrics-heading">
        <h2 id="knowledge-metrics-heading">Knowledge Metrics</h2>
        <PanelStatusMessage error={error} />
      </aside>
    );
  }

  const nodeCount = graph.nodes.length;
  const edgeCount = graph.edges.length;
  const clusterCount = computeClusterOrder(graph).length;
  const degree = computeDegree(graph.nodes, graph.edges);
  const orphanCount = graph.nodes.filter((node) => (degree.get(node.id) ?? 0) === 0).length;
  const maxPossibleEdges = nodeCount > 1 ? (nodeCount * (nodeCount - 1)) / 2 : 0;
  const density = maxPossibleEdges > 0 ? (edgeCount / maxPossibleEdges) * 100 : 0;

  const metrics = [
    { label: "Nodes", value: nodeCount.toLocaleString() },
    { label: "Connections", value: edgeCount.toLocaleString() },
    { label: "Clusters", value: clusterCount.toLocaleString() },
    { label: "Density", value: formatPercent(density) },
    { label: "Orphaned Nodes", value: orphanCount.toLocaleString() },
  ];

  return (
    <aside className="knowledge-metrics-panel" aria-labelledby="knowledge-metrics-heading">
      <h2 id="knowledge-metrics-heading">Knowledge Metrics</h2>
      <dl className="metrics-list">
        {metrics.map((metric) => (
          <div className="metric-row" key={metric.label}>
            <dt>{metric.label}</dt>
            <dd>{metric.value}</dd>
          </div>
        ))}
      </dl>
    </aside>
  );
}

export function ActiveClustersPanel({ graph, error }) {
  if (!graph) {
    return (
      <aside className="active-clusters-panel" aria-labelledby="active-clusters-heading">
        <h2 id="active-clusters-heading">Active Clusters</h2>
        <PanelStatusMessage error={error} />
      </aside>
    );
  }

  const clusterOrder = computeClusterOrder(graph);
  const counts = new Map(clusterOrder.map((cluster) => [cluster, 0]));
  for (const node of graph.nodes) {
    counts.set(node.cluster, (counts.get(node.cluster) ?? 0) + 1);
  }
  const clusters = clusterOrder
    .map((cluster) => ({ cluster, count: counts.get(cluster) ?? 0 }))
    .sort((a, b) => b.count - a.count);

  return (
    <aside className="active-clusters-panel" aria-labelledby="active-clusters-heading">
      <h2 id="active-clusters-heading">Active Clusters</h2>
      <ul className="cluster-list">
        {clusters.map(({ cluster, count }) => (
          <li className="cluster-row" key={cluster}>
            <span
              className="cluster-swatch"
              style={{ background: colorForCluster(cluster, clusterOrder) }}
              aria-hidden="true"
            />
            <span className="cluster-name">{cluster}</span>
            <span className="cluster-count">{count.toLocaleString()}</span>
          </li>
        ))}
      </ul>
    </aside>
  );
}
