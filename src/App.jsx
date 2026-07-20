import { useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
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
} from "lucide-react";

import {
  capabilityStatuses as staticCapabilityStatuses,
  diagnostics,
  platformSignals as staticPlatformSignals,
  STATUS,
} from "./platformStatus.js";
import { GuardianOrbGraph } from "./GuardianOrbGraph.jsx";
import { ActiveClustersPanel, KnowledgeMetricsPanel } from "./KnowledgeGraphPanels.jsx";

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

// System Health panel rows (JRM-0001 Track C Near-term): Guardian, Sentinel
// and Providers, sourced only from real `platform.status` fields. As of
// ESR-0023 WP6 (EBG-0073), SystemHealthPanel is these rows' sole owner -
// DiagnosticsPanel below no longer duplicates them; its remaining rows
// (boundary, shell, agents) are permanently-static placeholders.
const SYSTEM_HEALTH_LABELS = { guardian: "Guardian", sentinel: "Sentinel", providers: "Providers" };

function deriveSystemHealth(platformState, platformError) {
  if (platformError) {
    return ["guardian", "sentinel", "providers"].map((id) => ({
      id,
      label: SYSTEM_HEALTH_LABELS[id],
      state: STATUS.OFFLINE,
      detail: "JARVIS backend is unavailable",
    }));
  }
  if (!platformState) {
    return ["guardian", "sentinel", "providers"].map((id) => ({
      id,
      label: SYSTEM_HEALTH_LABELS[id],
      state: STATUS.CONNECTING,
      detail: "Connecting to the JARVIS backend...",
    }));
  }

  const running = platformState.state === "Running";
  const providers = Array.isArray(platformState.providers) ? platformState.providers : [];

  return [
    {
      id: "guardian",
      label: SYSTEM_HEALTH_LABELS.guardian,
      state: running ? STATUS.OPERATIONAL : STATUS.OFFLINE,
      detail: `Runtime: ${platformState.state}`,
    },
    {
      id: "sentinel",
      label: SYSTEM_HEALTH_LABELS.sentinel,
      state: running ? STATUS.OPERATIONAL : STATUS.OFFLINE,
      detail: running
        ? platformState.policyEngine
          ? `Trust gateway active (${platformState.policyEngine})`
          : "Trust gateway active"
        : "Not running",
    },
    {
      id: "providers",
      label: SYSTEM_HEALTH_LABELS.providers,
      state: providers.length > 0 ? STATUS.OPERATIONAL : STATUS.OFFLINE,
      detail: providers.length > 0 ? providers.join(" -> ") : "No providers connected",
    },
  ];
}

function SystemHealthPanel({ platformState, platformError, lastHeartbeatAt }) {
  const rows = deriveSystemHealth(platformState, platformError);

  return (
    <aside className="system-health-panel" aria-labelledby="system-health-heading">
      <h2 id="system-health-heading">System Health</h2>
      <div className="system-health-list">
        {rows.map((row) => (
          <article className="system-health-row" key={row.id}>
            <span className="system-health-label">{row.label}</span>
            <span className="system-health-value">
              <StateDot state={row.state} />
              <span>{row.detail}</span>
            </span>
          </article>
        ))}
      </div>
      {/* EIP-ESR0031-002: proves the streaming-notification plumbing works end
          to end with real, live data - not a decorative placeholder. Absent
          until the first heartbeat actually arrives, never a fabricated
          initial value. */}
      <p className="system-health-heartbeat">
        {lastHeartbeatAt
          ? `Backend heartbeat: ${lastHeartbeatAt.toLocaleTimeString()}`
          : "Backend heartbeat: waiting for first signal…"}
      </p>
    </aside>
  );
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
  agents: UsersRound,
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
          <strong>Robert</strong>
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

function GuardianOrbit({ knowledgeGraph, knowledgeGraphError }) {
  return (
    <section className="guardian-stage" aria-label="Guardian">
      <div className="guardian-orb" role="img" aria-label="Guardian visual presence: live repository knowledge graph">
        <GuardianOrbGraph
          graph={knowledgeGraph}
          loading={!knowledgeGraph && !knowledgeGraphError}
          error={knowledgeGraphError}
        />
      </div>
    </section>
  );
}

function DiagnosticsPanel({ diagnostics }) {
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

  const [knowledgeGraph, setKnowledgeGraph] = useState(null);
  const [knowledgeGraphError, setKnowledgeGraphError] = useState(null);

  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [sending, setSending] = useState(false);
  const [sendError, setSendError] = useState(null);

  // EIP-ESR0031-002 (Streaming Notifications MVP): the UXP's first live-push
  // channel. platform_status/knowledge_graph above remain one-time mount
  // fetches, unchanged - this is a second, independent channel proving the
  // Python-to-Rust-to-React notification plumbing works, not a replacement.
  const [lastHeartbeatAt, setLastHeartbeatAt] = useState(null);

  useEffect(() => {
    let cancelled = false;

    invoke("platform_status")
      .then((status) => {
        if (!cancelled) setPlatformState(status);
      })
      .catch((error) => {
        if (!cancelled) setPlatformError(String(error));
      });

    invoke("knowledge_graph")
      .then((graph) => {
        if (!cancelled) setKnowledgeGraph(graph);
      })
      .catch((error) => {
        if (!cancelled) setKnowledgeGraphError(String(error));
      });

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let unlisten;
    let cancelled = false;

    listen("jarvis://notification", (event) => {
      if (event.payload?.method === "system.heartbeat") {
        setLastHeartbeatAt(new Date());
      }
    }).then((fn) => {
      if (cancelled) {
        fn();
      } else {
        unlisten = fn;
      }
    });

    return () => {
      cancelled = true;
      if (unlisten) unlisten();
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
              <GuardianOrbit
                knowledgeGraph={knowledgeGraph}
                knowledgeGraphError={knowledgeGraphError}
              />
              <CommandPanel
                messages={messages}
                inputValue={inputValue}
                onInputChange={setInputValue}
                onSubmit={handleSubmit}
                sending={sending}
                sendError={sendError}
              />
            </div>
            <div className="side-column">
              <SystemHealthPanel
                platformState={platformState}
                platformError={platformError}
                lastHeartbeatAt={lastHeartbeatAt}
              />
              <KnowledgeMetricsPanel graph={knowledgeGraph} error={knowledgeGraphError} />
              <ActiveClustersPanel graph={knowledgeGraph} error={knowledgeGraphError} />
              <DiagnosticsPanel diagnostics={diagnostics} />
            </div>
          </div>
          <AppFooter />
        </section>
      </div>
    </main>
  );
}