import { CheckCircle2, CircleHelp, CloudOff, Loader, MinusCircle } from "lucide-react";

import { CAP, NOT_BUILT_YET } from "./capabilities.js";

// One icon and one word per state, so colour is never the only signal.
const STATE_ICON = {
  [CAP.READY]: CheckCircle2,
  [CAP.PREPARING]: Loader,
  [CAP.NOT_AVAILABLE]: MinusCircle,
  [CAP.OFFLINE]: CloudOff,
  [CAP.UNKNOWN]: CircleHelp,
};

const stateSlug = (state) => state.toLowerCase().replaceAll(" ", "-");

export function CapabilityState({ state }) {
  const Icon = STATE_ICON[state] ?? CircleHelp;
  return (
    <span className={`cap-state cap-${stateSlug(state)}`}>
      <Icon size={14} aria-hidden="true" />
      <span>{state}</span>
    </span>
  );
}

// The System view's full list, with what is not built yet kept apart from it.
export function CapabilityPanel({ rows }) {
  return (
    <section className="capabilities-panel" aria-labelledby="capabilities-heading">
      <h2 id="capabilities-heading">What JARVIS can do</h2>
      <ul className="capability-list">
        {rows.map((entry) => (
          <li
            className="capability-item"
            key={entry.id}
            data-capability={entry.id}
            data-capability-state={stateSlug(entry.state)}
          >
            <div>
              <h3>{entry.label}</h3>
              <p>{entry.detail}</p>
            </div>
            <CapabilityState state={entry.state} />
          </li>
        ))}
      </ul>
      <h3 className="capability-subheading">Not available yet</h3>
      <ul className="not-built-list">
        {NOT_BUILT_YET.map((name) => (
          <li key={name}>{name}</li>
        ))}
      </ul>
    </section>
  );
}

// The slim "What is available" column beside the conversation.
export function AvailableColumn({ rows }) {
  return (
    <aside className="available-column" aria-labelledby="available-heading">
      <h2 id="available-heading">What is available</h2>
      <ul className="capability-list compact">
        {rows.map((entry) => (
          <li
            className="capability-item"
            key={entry.id}
            data-capability={entry.id}
            data-capability-state={stateSlug(entry.state)}
          >
            <span className="capability-name">{entry.label}</span>
            <CapabilityState state={entry.state} />
          </li>
        ))}
      </ul>
    </aside>
  );
}
