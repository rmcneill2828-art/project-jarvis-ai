import {
  capabilityStatuses,
  conversationMessages,
  diagnostics,
  guardianStatus,
  platformSignals,
  STATUS,
} from "./platformStatus.js";

const statusClass = (state) => state.toLowerCase().replaceAll(" ", "-");

function StatusPill({ state, compact = false }) {
  return (
    <span className={`status-pill status-${statusClass(state)}${compact ? " status-pill-compact" : ""}`}>
      {state}
    </span>
  );
}

function TopStatusStrip() {
  return (
    <section className="status-strip" aria-label="Platform and provider status">
      {platformSignals.map((signal) => (
        <article className="status-summary" key={signal.label}>
          <div>
            <p className="panel-kicker">{signal.label}</p>
            <p>{signal.detail}</p>
          </div>
          <StatusPill state={signal.state} compact />
        </article>
      ))}
    </section>
  );
}

function CapabilityPanel() {
  return (
    <aside className="capability-panel" aria-labelledby="capability-heading">
      <div className="panel-heading">
        <p className="panel-kicker">Capabilities</p>
        <h2 id="capability-heading">Navigation awareness</h2>
      </div>
      <nav aria-label="Guardian capability awareness">
        <ul className="capability-list">
          {capabilityStatuses.map((capability) => (
            <li className="capability-item" key={capability.id}>
              <div>
                <span className="capability-label">{capability.label}</span>
                <span className="capability-detail">{capability.detail}</span>
              </div>
              <StatusPill state={capability.state} compact />
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}

function GuardianOrb() {
  return (
    <div className="guardian-orb" role="img" aria-label="Guardian visual presence">
      <span className="orb-ring orb-ring-outer" />
      <span className="orb-ring orb-ring-middle" />
      <span className="orb-core" />
      <span className="orb-glint" />
    </div>
  );
}

function GuardianPresence() {
  return (
    <section className="guardian-presence" aria-labelledby="guardian-title">
      <div className="guardian-presence-copy">
        <p className="panel-kicker">{guardianStatus.title}</p>
        <h1 id="guardian-title">Guardian</h1>
        <p className="guardian-message">{guardianStatus.message}</p>
        <p className="guardian-detail">{guardianStatus.detail}</p>
        <div className="guardian-state" aria-label="Guardian shell state">
          <StatusPill state={guardianStatus.state} />
          <span>Desktop interface shell only</span>
        </div>
      </div>
      <GuardianOrb />
    </section>
  );
}

function ConversationArea() {
  return (
    <section className="conversation-area" aria-labelledby="conversation-heading">
      <div className="panel-heading conversation-heading-row">
        <div>
          <p className="panel-kicker">Conversation</p>
          <h2 id="conversation-heading">Primary interaction surface</h2>
        </div>
        <StatusPill state={STATUS.NOT_IMPLEMENTED} compact />
      </div>
      <div className="conversation-thread" aria-label="Static conversation placeholders">
        {conversationMessages.map((message) => (
          <article className="conversation-message" key={`${message.speaker}-${message.text}`}>
            <header>
              <span>{message.speaker}</span>
              <StatusPill state={message.state} compact />
            </header>
            <p>{message.text}</p>
          </article>
        ))}
      </div>
      <div className="conversation-boundary" aria-label="Conversation runtime boundary">
        <span>Input unavailable</span>
        <strong>Conversation runtime is not yet implemented.</strong>
      </div>
    </section>
  );
}

function DiagnosticsPanel({ capabilityCount, unavailableCount }) {
  const valueFor = ([label, value]) => {
    if (label === "Capability count") {
      return `${capabilityCount} visible capabilities`;
    }

    if (label === "Placeholder boundary") {
      return `${unavailableCount} capabilities unavailable or inactive by design`;
    }

    return value;
  };

  return (
    <aside className="diagnostics-panel" aria-labelledby="diagnostics-heading">
      <div className="panel-heading">
        <p className="panel-kicker">Diagnostics</p>
        <h2 id="diagnostics-heading">Runtime boundary</h2>
      </div>
      <dl>
        {diagnostics.map((diagnostic) => (
          <div className="diagnostic-row" key={diagnostic[0]}>
            <dt>{diagnostic[0]}</dt>
            <dd>{valueFor(diagnostic)}</dd>
          </div>
        ))}
      </dl>
    </aside>
  );
}

export function App() {
  const unavailableCount = capabilityStatuses.filter(
    (capability) => capability.state !== STATUS.AVAILABLE,
  ).length;

  return (
    <main className="app-shell">
      <TopStatusStrip />
      <div className="guardian-layout" aria-label="Guardian desktop experience layout">
        <CapabilityPanel />
        <div className="guardian-main-column">
          <GuardianPresence />
          <ConversationArea />
        </div>
        <DiagnosticsPanel capabilityCount={capabilityStatuses.length} unavailableCount={unavailableCount} />
      </div>
      <footer className="shell-footer">
        <span>{unavailableCount} capabilities remain unavailable or inactive by design.</span>
        <span>No AI runtime, provider calls, Sentinel enforcement, memory, agents, voice or vision are implemented.</span>
      </footer>
    </main>
  );
}
