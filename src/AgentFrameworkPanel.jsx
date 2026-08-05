// Agent Framework panel (EIP-ESR0050-001, ESR-0050 WP2). Wires the ESR-0049
// Agent Framework backend (jarvis/agents/, guardian.agent.list/invoke) into
// the live UXP - lists registered specialist agents and lets a household
// member run one, rendering the real returned payload. Per the no-mock-
// fallback rule (ESR-0017 WP9), a not-yet-resolved or failed list_agents
// call shows an honest connecting/error message, never a fabricated agent
// name or result. Mirrors KnowledgeGraphPanels.jsx's dedicated-panel-file
// pattern and reuses the existing .metrics-list/.metric-row classes for the
// invocation result - no new metric-rendering CSS.

function PanelStatusMessage({ error }) {
  return (
    <p className="panel-status-message">
      {error ? "Agent Framework is unavailable." : "Connecting to the Agent Framework..."}
    </p>
  );
}

export function AgentFrameworkPanel({
  agents,
  agentsError,
  agentBusy,
  agentResult,
  agentInvokeError,
  onInvokeAgent,
}) {
  if (agentsError || !agents) {
    return (
      <aside className="agent-framework-panel" aria-labelledby="agent-framework-panel-heading">
        <h2 id="agent-framework-panel-heading">Agent Framework</h2>
        <PanelStatusMessage error={agentsError} />
      </aside>
    );
  }

  if (agents.length === 0) {
    return (
      <aside className="agent-framework-panel" aria-labelledby="agent-framework-panel-heading">
        <h2 id="agent-framework-panel-heading">Agent Framework</h2>
        <p className="panel-status-message">No specialist agents are registered.</p>
      </aside>
    );
  }

  return (
    <aside className="agent-framework-panel" aria-labelledby="agent-framework-panel-heading">
      <h2 id="agent-framework-panel-heading">Agent Framework</h2>
      <div className="agent-list">
        {agents.map((agentName) => (
          <div className="agent-row" key={agentName}>
            <span className="agent-name">{agentName}</span>
            <button
              type="button"
              className="outline-action agent-invoke-button"
              disabled={agentBusy}
              onClick={() => onInvokeAgent(agentName)}
              aria-label={`Run ${agentName}`}
            >
              Run
            </button>
          </div>
        ))}
      </div>
      {agentInvokeError && (
        <p className="conversation-error" role="alert">
          {agentInvokeError}
        </p>
      )}
      {agentResult && (
        <dl className="metrics-list agent-result-list">
          <div className="metric-row">
            <dt>Last run</dt>
            <dd>{agentResult.agent}</dd>
          </div>
          {Object.entries(agentResult.payload ?? {}).map(([key, value]) => (
            <div className="metric-row" key={key}>
              <dt>{key}</dt>
              <dd>{value}</dd>
            </div>
          ))}
        </dl>
      )}
    </aside>
  );
}
