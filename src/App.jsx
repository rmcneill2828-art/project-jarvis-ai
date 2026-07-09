import { useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import {
  Activity,
  Bell,
  Box,
  ChevronDown,
  ChevronRight,
  CircleUserRound,
  Cloud,
  Code2,
  Database,
  FlaskConical,
  Grid3X3,
  Link2,
  Minus,
  Monitor,
  SendHorizontal,
  Server,
  Settings,
  Shield,
  Square,
  UsersRound,
  X,
  Zap,
} from "lucide-react";

import {
  capabilityStatuses as staticCapabilityStatuses,
  diagnostics,
  guardianStatus as staticGuardianStatus,
  platformSignals as staticPlatformSignals,
  STATUS,
} from "./platformStatus.js";

// Live overrides for platformStatus.js's static defaults, sourced from a real
// `platform.status` JSON-RPC call through the Tauri sidecar bridge
// (ADR-0019, ESR-0017 WP9). Per the WP9 design, a failed or not-yet-resolved
// call must show an honest connecting/offline state - never a silently
// retained mock "Operational" claim.
function derivePlatformIndicator(platformState, platformError) {
  if (platformError) return { label: "OFFLINE", status: STATUS.OFFLINE };
  if (!platformState) return { label: "CONNECTING", status: STATUS.CONNECTING };
  return platformState.state === "Running"
    ? { label: "JARVIS PLATFORM", status: STATUS.OPERATIONAL }
    : { label: platformState.state.toUpperCase(), status: STATUS.OFFLINE };
}

function deriveCapabilityStatuses(platformState, platformError) {
  const connected = platformState?.providerConnected === "Online";

  return staticCapabilityStatuses.map((capability) => {
    if (capability.id !== "sentinel" && capability.id !== "providers") return capability;

    if (platformError) {
      return { ...capability, state: STATUS.OFFLINE, detail: "JARVIS backend is unavailable" };
    }
    if (!platformState) {
      return { ...capability, state: STATUS.CONNECTING, detail: "Connecting to the JARVIS backend..." };
    }
    return {
      ...capability,
      state: connected ? STATUS.OPERATIONAL : STATUS.OFFLINE,
      detail: connected ? "Sentinel-gated provider connected" : "No provider adapters connected",
    };
  });
}

function derivePlatformSignals(platformState, platformError) {
  return staticPlatformSignals.map((signal) => {
    if (signal.id !== "providers") return signal;

    if (platformError) {
      return { ...signal, state: STATUS.OFFLINE, detail: "JARVIS backend is unavailable" };
    }
    if (!platformState) {
      return { ...signal, state: STATUS.CONNECTING, detail: "Connecting to the JARVIS backend..." };
    }
    const connected = platformState.providerConnected === "Online";
    return {
      ...signal,
      state: connected ? STATUS.OPERATIONAL : STATUS.OFFLINE,
      detail: connected ? "Sentinel-gated provider connected" : "No providers connected",
    };
  });
}

function deriveGuardianStatus(platformState, platformError) {
  if (platformError) {
    return {
      ...staticGuardianStatus,
      state: STATUS.OFFLINE,
      boundary: `JARVIS backend is unavailable: ${platformError}`,
    };
  }
  if (!platformState) return staticGuardianStatus;

  const connected = platformState.providerConnected === "Online";
  return {
    ...staticGuardianStatus,
    state: platformState.state === "Running" ? STATUS.OPERATIONAL : STATUS.OFFLINE,
    boundary: connected
      ? "Conversation runtime is connected."
      : "Conversation runtime is running without a connected provider.",
  };
}

const stateClass = (state) => state.toLowerCase().replaceAll(" ", "-");

const capabilityIcons = {
  sentinel: Shield,
  "platform-services": Grid3X3,
  memory: Database,
  providers: Link2,
  "agent-framework": UsersRound,
};

const signalIcons = {
  platform: Server,
  services: Box,
  providers: Cloud,
};

const diagnosticIcons = {
  boundary: Code2,
  shell: Monitor,
  guardian: Activity,
  sentinel: Shield,
  providers: Cloud,
  agents: UsersRound,
  "first-light": Zap,
};

function StatusBadge({ state }) {
  return <span className={`status-badge status-${stateClass(state)}`}>{state}</span>;
}

function StateDot({ state }) {
  return <span className={`state-dot dot-${stateClass(state)}`} aria-hidden="true" />;
}

function IconTile({ icon: Icon, className = "" }) {
  return (
    <span className={`icon-tile ${className}`} aria-hidden="true">
      <Icon size={24} strokeWidth={2.2} />
    </span>
  );
}

function AppHeader({ platformIndicator }) {
  return (
    <header className="app-header" aria-label="JARVIS desktop shell header">
      <div className="brand-lockup" aria-label="JARVIS">
        <span className="brand-mark" aria-hidden="true">
          <span />
        </span>
        <span className="brand-name">JARVIS</span>
      </div>
      <div className="platform-indicator" aria-label="JARVIS platform status">
        <StateDot state={platformIndicator.status} />
        <span>{platformIndicator.label}</span>
        <StatusBadge state={platformIndicator.status} />
      </div>
      <div className="window-actions" aria-label="Shell controls">
        <button type="button" aria-label="Notifications">
          <Bell size={20} />
        </button>
        <button type="button" aria-label="Settings">
          <Settings size={20} />
        </button>
        <button type="button" aria-label="Minimize">
          <Minus size={20} />
        </button>
        <button type="button" aria-label="Maximize">
          <Square size={16} />
        </button>
        <button type="button" aria-label="Close">
          <X size={20} />
        </button>
      </div>
    </header>
  );
}

function CapabilitySidebar({ capabilityStatuses }) {
  return (
    <aside className="sidebar" aria-labelledby="sidebar-heading">
      <section className="sidebar-panel">
        <h2 id="sidebar-heading">Platform Placeholders</h2>
        <div className="capability-stack">
          {capabilityStatuses.map((capability) => {
            const Icon = capabilityIcons[capability.id] ?? Shield;

            return (
              <article className="capability-row" key={capability.id}>
                <IconTile icon={Icon} />
                <div>
                  <h3>{capability.label}</h3>
                  <StatusBadge state={capability.state} />
                  <p>{capability.detail}</p>
                </div>
              </article>
            );
          })}
        </div>
        <button className="outline-action" type="button" aria-label="View all capabilities">
          <span>View all capabilities</span>
          <ChevronRight size={18} />
        </button>
      </section>
      <section className="profile-card" aria-label="Signed in profile">
        <span className="avatar" aria-hidden="true">
          <CircleUserRound size={34} />
        </span>
        <div>
          <strong>Richard</strong>
          <span>Signed in locally</span>
        </div>
        <ChevronDown size={18} aria-hidden="true" />
      </section>
    </aside>
  );
}

function StatusCards({ platformSignals }) {
  return (
    <section className="status-cards" aria-label="Platform service summary">
      {platformSignals.map((signal) => {
        const Icon = signalIcons[signal.id] ?? Activity;

        return (
          <article className="status-card" key={signal.id}>
            <IconTile icon={Icon} className="status-icon" />
            <div>
              <h2>{signal.label}</h2>
              <StatusBadge state={signal.state} />
              <p>{signal.detail}</p>
            </div>
          </article>
        );
      })}
    </section>
  );
}

function GuardianOrbit({ guardianStatus }) {
  return (
    <section className="guardian-stage" aria-labelledby="guardian-title">
      <div className="orbital-field" aria-hidden="true">
        {Array.from({ length: 9 }, (_, index) => (
          <span className={`orbit-line orbit-line-${index + 1}`} key={index} />
        ))}
        <span className="orbit-spark spark-one" />
        <span className="orbit-spark spark-two" />
        <span className="orbit-spark spark-three" />
      </div>
      <div className="guardian-orb" role="img" aria-label="Guardian visual presence">
        <span className="orb-glow" />
        <span className="orb-ring outer" />
        <span className="orb-ring inner" />
        <div className="orb-label">
          <h1 id="guardian-title">{guardianStatus.title}</h1>
          <p>AI Companion</p>
        </div>
      </div>
      <div className="guardian-copy">
        <h2>{guardianStatus.greeting}</h2>
        <p className="guardian-role">{guardianStatus.role}</p>
        <p>{guardianStatus.platform}</p>
        <p>{guardianStatus.assurance}</p>
      </div>
    </section>
  );
}

function DiagnosticsPanel() {
  return (
    <aside className="diagnostics-panel" aria-labelledby="diagnostics-heading">
      <h2 id="diagnostics-heading">Diagnostics</h2>
      <div className="diagnostics-list">
        {diagnostics.map((item) => {
          const Icon = diagnosticIcons[item.id] ?? Activity;

          return (
            <article className="diagnostic-item" key={item.id}>
              <IconTile icon={Icon} />
              <div>
                <h3>{item.label}</h3>
                <p>
                  <StateDot state={item.state} />
                  <span>{item.detail}</span>
                </p>
              </div>
            </article>
          );
        })}
      </div>
      <button className="outline-action" type="button" aria-label="View diagnostics">
        <span>View diagnostics</span>
        <ChevronRight size={18} />
      </button>
    </aside>
  );
}

function CommandPanel({ messages, inputValue, onInputChange, onSubmit, sending, sendError }) {
  return (
    <section className="command-panel" aria-labelledby="command-heading">
      <h2 id="command-heading">How can I help you today?</h2>
      {messages.length > 0 && (
        <div className="conversation-log" aria-live="polite" aria-label="Conversation with Guardian">
          {messages.map((entry) => (
            <p className={`conversation-message ${entry.role}`} key={entry.id}>
              {entry.text}
            </p>
          ))}
        </div>
      )}
      {sendError && (
        <p className="conversation-error" role="alert">
          {sendError}
        </p>
      )}
      <form
        className="input-shell"
        aria-label="Guardian conversation input"
        onSubmit={(event) => {
          event.preventDefault();
          onSubmit();
        }}
      >
        <input
          value={inputValue}
          onChange={(event) => onInputChange(event.target.value)}
          placeholder="Ask Guardian anything..."
          disabled={sending}
        />
        <button type="submit" disabled={sending || inputValue.trim().length === 0} aria-label="Send">
          <SendHorizontal size={24} />
        </button>
      </form>
      <div className="quick-actions" aria-label="Static Guardian shortcuts">
        <button type="button">
          <Activity size={18} />
          <span>Platform Status</span>
        </button>
        <button type="button">
          <Grid3X3 size={18} />
          <span>View Capabilities</span>
        </button>
        <button type="button">
          <Activity size={18} />
          <span>Run Diagnostics</span>
        </button>
        <button type="button">
          <FlaskConical size={18} />
          <span>Show Roadmap</span>
        </button>
      </div>
    </section>
  );
}

function AppFooter() {
  return (
    <footer className="shell-footer" aria-label="Shell edition and runtime boundary">
      <span>
        <Shield size={16} aria-hidden="true" />
        Guardian protecting your digital world
      </span>
      <span className="footer-separator" aria-hidden="true" />
      <span>All times are local</span>
      <span className="footer-version">v0.1.0</span>
      <span>
        <StateDot state={STATUS.OPERATIONAL} />
        Shell Edition
      </span>
    </footer>
  );
}

export function App() {
  const [platformState, setPlatformState] = useState(null);
  const [platformError, setPlatformError] = useState(null);

  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [sending, setSending] = useState(false);
  const [sendError, setSendError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    invoke("platform_status")
      .then((status) => {
        if (!cancelled) setPlatformState(status);
      })
      .catch((error) => {
        if (!cancelled) setPlatformError(String(error));
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const handleSubmit = () => {
    const message = inputValue.trim();
    if (!message || sending) return;

    setSending(true);
    setSendError(null);
    setMessages((current) => [...current, { id: `${Date.now()}-user`, role: "user", text: message }]);
    setInputValue("");

    invoke("send_message", { message })
      .then((response) => {
        setMessages((current) => [
          ...current,
          { id: `${Date.now()}-guardian`, role: "guardian", text: response.message },
        ]);
      })
      .catch((error) => {
        setSendError(`Guardian did not respond: ${error}`);
      })
      .finally(() => {
        setSending(false);
      });
  };

  return (
    <main className="jarvis-shell">
      <AppHeader platformIndicator={derivePlatformIndicator(platformState, platformError)} />
      <div className="shell-grid">
        <CapabilitySidebar capabilityStatuses={deriveCapabilityStatuses(platformState, platformError)} />
        <section className="workspace" aria-label="Guardian desktop experience">
          <StatusCards platformSignals={derivePlatformSignals(platformState, platformError)} />
          <div className="experience-grid">
            <div className="guardian-column">
              <GuardianOrbit guardianStatus={deriveGuardianStatus(platformState, platformError)} />
              <CommandPanel
                messages={messages}
                inputValue={inputValue}
                onInputChange={setInputValue}
                onSubmit={handleSubmit}
                sending={sending}
                sendError={sendError}
              />
            </div>
            <DiagnosticsPanel />
          </div>
          <AppFooter />
        </section>
      </div>
    </main>
  );
}