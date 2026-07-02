import {
  capabilityStatuses,
  diagnostics,
  guardianStatus,
  platformSignals,
  STATUS,
} from "./platformStatus.js";

const statusClass = (state) => state.toLowerCase().replaceAll(" ", "-");

function StatusPill({ state }) {
  return <span className={`status-pill status-${statusClass(state)}`}>{state}</span>;
}

function GuardianPanel() {
  return (
    <section className="guardian-panel" aria-labelledby="guardian-title">
      <div className="guardian-orbit" aria-hidden="true">
        <div className="guardian-core" />
      </div>
      <div className="guardian-copy">
        <p className="eyebrow">JARVIS Guardian Desktop Shell</p>
        <h1 id="guardian-title">Guardian is the trusted interface to JARVIS.</h1>
        <p className="guardian-message">{guardianStatus.message}</p>
        <p className="guardian-detail">{guardianStatus.detail}</p>
        <div className="guardian-actions" aria-label="Guardian shell state">
          <StatusPill state={guardianStatus.state} />
          <span>JARVIS Platform is preparing core services.</span>
        </div>
      </div>
    </section>
  );
}

function PlatformSignals() {
  return (
    <section className="signal-strip" aria-label="Platform status summary">
      {platformSignals.map((signal) => (
        <article className="signal-item" key={signal.label}>
          <div>
            <h2>{signal.label}</h2>
            <p>{signal.detail}</p>
          </div>
          <StatusPill state={signal.state} />
        </article>
      ))}
    </section>
  );
}

function CapabilityStatusGrid() {
  return (
    <section className="capability-section" aria-labelledby="capability-heading">
      <div className="section-heading">
        <p className="eyebrow">Capability posture</p>
        <h2 id="capability-heading">Platform placeholders are visible but inactive.</h2>
      </div>
      <div className="capability-grid">
        {capabilityStatuses.map((capability) => (
          <article className="capability-card" key={capability.id}>
            <header>
              <h3>{capability.label}</h3>
              <StatusPill state={capability.state} />
            </header>
            <p>{capability.detail}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function DiagnosticsPanel() {
  return (
    <section className="diagnostics-panel" aria-labelledby="diagnostics-heading">
      <div className="section-heading">
        <p className="eyebrow">Diagnostics</p>
        <h2 id="diagnostics-heading">Implementation boundary</h2>
      </div>
      <dl>
        {diagnostics.map(([label, value]) => (
          <div className="diagnostic-row" key={label}>
            <dt>{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}

export function App() {
  const unavailableCount = capabilityStatuses.filter(
    (capability) => capability.state === STATUS.NOT_IMPLEMENTED || capability.state === STATUS.OFFLINE,
  ).length;

  return (
    <main className="app-shell">
      <GuardianPanel />
      <PlatformSignals />
      <div className="content-grid">
        <CapabilityStatusGrid />
        <DiagnosticsPanel />
      </div>
      <footer className="shell-footer">
        <span>{unavailableCount} capabilities remain unavailable by design.</span>
        <span>No Guardian runtime, Sentinel enforcement, providers, memory or agents are implemented.</span>
      </footer>
    </main>
  );
}