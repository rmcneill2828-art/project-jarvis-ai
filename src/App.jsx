import { useEffect, useMemo, useRef, useState } from "react";
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
  Mic,
  Minus,
  Monitor,
  SendHorizontal,
  Server,
  Settings,
  Shield,
  Square,
  UsersRound,
  Volume2,
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
import { AgentFrameworkPanel } from "./AgentFrameworkPanel.jsx";

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

function deriveCapabilityStatuses(platformState, platformError, agents, agentsError) {
  const connected = platformState?.providerConnected === "Online";
  const memoryConnected = platformState?.memoryConnected === "Online";

  return staticCapabilityStatuses.map((capability) => {
    if (capability.id === "memory") {
      if (platformError) {
        return { ...capability, state: STATUS.OFFLINE, detail: "JARVIS backend is unavailable" };
      }
      if (!platformState) {
        return { ...capability, state: STATUS.CONNECTING, detail: "Connecting to the JARVIS backend..." };
      }
      return {
        ...capability,
        state: memoryConnected ? STATUS.OPERATIONAL : STATUS.OFFLINE,
        detail: memoryConnected ? "Personal Memory service connected" : "No memory service connected",
      };
    }

    // Agent Framework (EIP-ESR0050-001): derived from a real guardian.agent.list
    // call, not platform.status - a separate live channel, matching the
    // memory/sentinel/providers connecting/offline/live pattern above.
    if (capability.id === "agent-framework") {
      if (agentsError) {
        return { ...capability, state: STATUS.OFFLINE, detail: "Agent Framework is unavailable" };
      }
      if (!agents) {
        return { ...capability, state: STATUS.CONNECTING, detail: "Connecting to the Agent Framework..." };
      }
      if (agents.length === 0) return capability;
      return {
        ...capability,
        state: STATUS.AVAILABLE,
        detail: `${agents.length} specialist agent${agents.length === 1 ? "" : "s"} available (${agents.join(", ")})`,
      };
    }

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

function CapabilitySidebar({ capabilityStatuses, profiles, activeProfile, profileError, onCreateProfile, onSelectProfile }) {
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
      <ProfileCard
        profiles={profiles}
        activeProfile={activeProfile}
        profileError={profileError}
        onCreateProfile={onCreateProfile}
        onSelectProfile={onSelectProfile}
      />
    </aside>
  );
}

// GAM-0001 Section 8.1's Household Role Model - the only roles a profile may
// be created with (EIP-ESR0046-001).
const HOUSEHOLD_ROLES = ["Administrator", "Adult", "Child", "Guest"];

function ProfileCard({ profiles, activeProfile, profileError, onCreateProfile, onSelectProfile }) {
  const [pickerOpen, setPickerOpen] = useState(false);
  const [newDisplayName, setNewDisplayName] = useState("");
  const [newRole, setNewRole] = useState(HOUSEHOLD_ROLES[0]);

  if (!activeProfile) {
    return (
      <section className="profile-card profile-card-create" aria-label="Create a Guardian profile">
        <form
          className="profile-create-form"
          onSubmit={(event) => {
            event.preventDefault();
            const trimmed = newDisplayName.trim();
            if (!trimmed) return;
            onCreateProfile(trimmed, newRole);
            setNewDisplayName("");
          }}
        >
          <span className="avatar" aria-hidden="true">
            <CircleUserRound size={34} />
          </span>
          <div className="profile-create-fields">
            <input
              value={newDisplayName}
              onChange={(event) => setNewDisplayName(event.target.value)}
              placeholder="Your name"
              aria-label="New profile display name"
            />
            <select
              value={newRole}
              onChange={(event) => setNewRole(event.target.value)}
              aria-label="New profile household role"
            >
              {HOUSEHOLD_ROLES.map((role) => (
                <option key={role} value={role}>
                  {role}
                </option>
              ))}
            </select>
            <button type="submit" disabled={newDisplayName.trim().length === 0}>
              Create profile
            </button>
          </div>
        </form>
        {profileError && (
          <p className="profile-error" role="alert">
            {profileError}
          </p>
        )}
      </section>
    );
  }

  const otherProfiles = (profiles ?? []).filter((profile) => profile.id !== activeProfile.id);

  return (
    <section className="profile-card" aria-label="Signed in profile">
      <button
        type="button"
        className="profile-summary"
        onClick={() => setPickerOpen((open) => !open)}
        aria-expanded={pickerOpen}
        aria-label="Switch Guardian profile"
      >
        <span className="avatar" aria-hidden="true">
          <CircleUserRound size={34} />
        </span>
        <div>
          <strong>{activeProfile.displayName}</strong>
          <span>{activeProfile.role}</span>
        </div>
        <ChevronDown size={18} aria-hidden="true" />
      </button>
      {pickerOpen && otherProfiles.length > 0 && (
        <ul className="profile-picker" aria-label="Other profiles">
          {otherProfiles.map((profile) => (
            <li key={profile.id}>
              <button
                type="button"
                onClick={() => {
                  onSelectProfile(profile.id);
                  setPickerOpen(false);
                }}
              >
                <strong>{profile.displayName}</strong>
                <span>{profile.role}</span>
              </button>
            </li>
          ))}
        </ul>
      )}
      {profileError && (
        <p className="profile-error" role="alert">
          {profileError}
        </p>
      )}
    </section>
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

// Guardian Orb Phase 2 (EBG-0121): a cluster counts as "active" for this
// long after its most recent recorded RPC activity before illumination
// fades. Deliberately short - this reflects genuinely current access, not a
// lingering decorative state. Pruned on a plain interval, checked this often.
const CLUSTER_ACTIVE_WINDOW_MS = 10000;
const CLUSTER_PRUNE_INTERVAL_MS = 2000;

function GuardianOrbit({ knowledgeGraph, knowledgeGraphError, activeClusters }) {
  return (
    <section className="guardian-stage" aria-label="Guardian">
      <div className="guardian-orb" role="img" aria-label="Guardian visual presence: live repository knowledge graph">
        <GuardianOrbGraph
          graph={knowledgeGraph}
          loading={!knowledgeGraph && !knowledgeGraphError}
          error={knowledgeGraphError}
          activeClusters={activeClusters}
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

function CommandPanel({
  messages,
  inputValue,
  onInputChange,
  onSubmit,
  sending,
  sendError,
  onSpeak,
  speakError,
  isRecording,
  onToggleRecording,
  transcribeError,
  transcriptionAvailable,
}) {
  return (
    <section className="command-panel" aria-labelledby="command-heading">
      <h2 id="command-heading">How can I help you today?</h2>
      {messages.length > 0 && (
        <div className="conversation-log" aria-live="polite" aria-label="Conversation with Guardian">
          {messages.map((entry) => (
            <p className={`conversation-message ${entry.role}`} key={entry.id}>
              <span>{entry.text}</span>
              {entry.role === "guardian" && (
                <button
                  type="button"
                  className="speak-button"
                  aria-label="Speak this response"
                  onClick={() => onSpeak(entry.text)}
                >
                  <Volume2 size={16} />
                </button>
              )}
            </p>
          ))}
        </div>
      )}
      {sendError && (
        <p className="conversation-error" role="alert">
          {sendError}
        </p>
      )}
      {speakError && (
        <p className="conversation-error" role="alert">
          {speakError}
        </p>
      )}
      {transcribeError && (
        <p className="conversation-error" role="alert">
          {transcribeError}
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
        {transcriptionAvailable && (
          <button
            type="button"
            className={`mic-button${isRecording ? " recording" : ""}`}
            aria-label={isRecording ? "Stop recording and transcribe" : "Speak a message"}
            aria-pressed={isRecording}
            disabled={sending}
            onClick={onToggleRecording}
          >
            <Mic size={20} />
          </button>
        )}
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

  // Guardian Orb Phase 2 (EBG-0121, UAM-0001 Section 8.1): cluster
  // illumination. Map<cluster, lastActiveAtMs> - a cluster is "active" if it
  // has a recent enough entry (see CLUSTER_ACTIVE_WINDOW_MS below), never a
  // decorative default. Seeded from knowledge_graph's own active_clusters
  // pull field (real prior activity) once it loads, then kept live by
  // knowledge.cluster_activity notifications.
  const [activeClusterTimestamps, setActiveClusterTimestamps] = useState(() => new Map());

  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [sending, setSending] = useState(false);
  const [sendError, setSendError] = useState(null);
  const [speakError, setSpeakError] = useState(null);

  // Voice Faculty Increment B (EIP-ESR0047-001): push-to-talk speech input.
  // isRecording drives the mic button's visual state only - the actual
  // MediaRecorder instance and its bounded 30s auto-stop timer live in refs,
  // not state, since neither needs to trigger a re-render.
  const [isRecording, setIsRecording] = useState(false);
  const [transcribeError, setTranscribeError] = useState(null);
  const mediaRecorderRef = useRef(null);
  const recordedChunksRef = useRef([]);
  const recordingTimeoutRef = useRef(null);

  const [profiles, setProfiles] = useState([]);
  const [activeProfile, setActiveProfile] = useState(null);
  const [profileError, setProfileError] = useState(null);

  // Agent Framework (EIP-ESR0050-001): agents null = connecting, [] = empty,
  // otherwise the real registered agent name list from guardian.agent.list.
  const [agents, setAgents] = useState(null);
  const [agentsError, setAgentsError] = useState(null);
  const [agentBusy, setAgentBusy] = useState(false);
  const [agentResult, setAgentResult] = useState(null);
  const [agentInvokeError, setAgentInvokeError] = useState(null);

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
        if (!cancelled) {
          setKnowledgeGraph(graph);
          // Seed from real prior activity (EBG-0121) so a cluster active in
          // the moments just before the UXP mounted is not shown as falsely
          // idle - the same "now" all subsequent notification timestamps use.
          const activeAtMount = graph.active_clusters ?? [];
          if (activeAtMount.length > 0) {
            const now = Date.now();
            setActiveClusterTimestamps((current) => {
              const next = new Map(current);
              activeAtMount.forEach((cluster) => next.set(cluster, now));
              return next;
            });
          }
        }
      })
      .catch((error) => {
        if (!cancelled) setKnowledgeGraphError(String(error));
      });

    invoke("list_profiles")
      .then((result) => {
        if (!cancelled) setProfiles(result.profiles ?? []);
      })
      .catch((error) => {
        if (!cancelled) setProfileError(String(error));
      });

    invoke("active_profile")
      .then((result) => {
        if (!cancelled) setActiveProfile(result.profile ?? null);
      })
      .catch((error) => {
        if (!cancelled) setProfileError(String(error));
      });

    invoke("list_agents")
      .then((result) => {
        if (!cancelled) setAgents(result.agents ?? []);
      })
      .catch((error) => {
        if (!cancelled) setAgentsError(String(error));
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
      if (event.payload?.method === "knowledge.cluster_activity") {
        const cluster = event.payload?.params?.cluster;
        if (cluster) {
          setActiveClusterTimestamps((current) => {
            const next = new Map(current);
            next.set(cluster, Date.now());
            return next;
          });
        }
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

  // Illumination fades rather than sticking on forever - a plain interval,
  // not the shared animation clock (GuardianOrbGraph's own concern), since
  // this only needs to run a few times a second, not every frame.
  useEffect(() => {
    const pruneInterval = setInterval(() => {
      const cutoff = Date.now() - CLUSTER_ACTIVE_WINDOW_MS;
      setActiveClusterTimestamps((current) => {
        let changed = false;
        const next = new Map();
        current.forEach((timestamp, cluster) => {
          if (timestamp >= cutoff) {
            next.set(cluster, timestamp);
          } else {
            changed = true;
          }
        });
        return changed ? next : current;
      });
    }, CLUSTER_PRUNE_INTERVAL_MS);
    return () => clearInterval(pruneInterval);
  }, []);

  const activeClusters = useMemo(
    () => [...activeClusterTimestamps.keys()],
    [activeClusterTimestamps],
  );

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

  const handleSpeak = (text) => {
    setSpeakError(null);

    invoke("speak_message", { text })
      .then((result) => {
        if (result.status !== "synthesized") {
          setSpeakError(result.message || "Guardian could not speak this response.");
          return;
        }
        try {
          const audio = new Audio(`data:${result.mimeType};base64,${result.audio}`);
          audio.play().catch((error) => {
            setSpeakError(`Guardian's voice could not play: ${error}`);
          });
        } catch (error) {
          setSpeakError(`Guardian's voice could not play: ${error}`);
        }
      })
      .catch((error) => {
        setSpeakError(`Guardian could not speak this response: ${error}`);
      });
  };

  // Maximum push-to-talk recording length (EIP-ESR0047-001 Section 5.5 item
  // 9 / Implementation Requirement 4): a hard client-side cap, not merely a
  // UI suggestion - recording is force-stopped at this limit.
  const MAX_RECORDING_MS = 30000;

  const blobToBase64 = (blob) =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        const dataUrl = reader.result;
        resolve(dataUrl.slice(dataUrl.indexOf(",") + 1));
      };
      reader.onerror = () => reject(reader.error);
      reader.readAsDataURL(blob);
    });

  const handleStopRecording = () => {
    if (recordingTimeoutRef.current) {
      clearTimeout(recordingTimeoutRef.current);
      recordingTimeoutRef.current = null;
    }
    const recorder = mediaRecorderRef.current;
    if (recorder && recorder.state !== "inactive") {
      recorder.stop();
    }
    setIsRecording(false);
  };

  const handleStartRecording = async () => {
    setTranscribeError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      recordedChunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) recordedChunksRef.current.push(event.data);
      };

      recorder.onstop = () => {
        stream.getTracks().forEach((track) => track.stop());
        const mimeType = recorder.mimeType || "audio/webm";
        const blob = new Blob(recordedChunksRef.current, { type: mimeType });
        recordedChunksRef.current = [];

        blobToBase64(blob)
          .then((audioBase64) => invoke("transcribe_audio", { audioBase64, mimeType }))
          .then((result) => {
            if (result.status !== "transcribed") {
              setTranscribeError(result.message || "Guardian could not transcribe that.");
              return;
            }
            // Populated for the household member to review and send
            // themselves - never auto-submitted (EIP-ESR0047-001 Section
            // 5.5 item 10 / Section 8 exclusion 4).
            applyTranscript(result.text);
          })
          .catch((error) => {
            setTranscribeError(`Guardian could not transcribe that: ${error}`);
          });
      };

      mediaRecorderRef.current = recorder;
      recorder.start();
      setIsRecording(true);
      recordingTimeoutRef.current = setTimeout(handleStopRecording, MAX_RECORDING_MS);
    } catch (error) {
      setTranscribeError(`Microphone unavailable: ${error}`);
    }
  };

  const applyTranscript = (text) => {
    setInputValue((current) => (current.trim().length > 0 ? `${current.trim()} ${text}` : text));
  };

  const handleToggleRecording = () => {
    if (isRecording) {
      handleStopRecording();
    } else {
      handleStartRecording();
    }
  };

  const handleCreateProfile = (displayName, role) => {
    setProfileError(null);

    invoke("create_profile", { displayName, role })
      .then((created) => {
        setProfiles((current) => [...current, created]);
        return invoke("select_profile", { profileId: created.id });
      })
      .then((selected) => {
        setActiveProfile(selected);
      })
      .catch((error) => {
        setProfileError(`Could not create profile: ${error}`);
      });
  };

  const handleSelectProfile = (profileId) => {
    setProfileError(null);

    invoke("select_profile", { profileId })
      .then((selected) => {
        setActiveProfile(selected);
      })
      .catch((error) => {
        setProfileError(`Could not switch profile: ${error}`);
      });
  };

  // Agent Framework (EIP-ESR0050-001): task is a fixed, non-empty string -
  // GiaObservabilityAgent (the only registered agent) ignores it and always
  // returns the same real snapshot; no UI for arbitrary task/parameter input
  // is in this package's scope. A denied/unknown-agent/other non-success
  // status is a valid, honestly-reported AgentOutcome (not a transport
  // failure) and is shown via its own message, mirroring handleSpeak's
  // result.status !== "synthesized" check exactly.
  const handleInvokeAgent = (agentName) => {
    setAgentBusy(true);
    setAgentInvokeError(null);

    invoke("invoke_agent", { agent: agentName, task: "status" })
      .then((result) => {
        if (result.status === "denied" || result.status === "unknown_agent") {
          setAgentInvokeError(result.message || `Guardian could not run ${agentName}.`);
          setAgentResult(null);
          return;
        }
        setAgentResult({ agent: agentName, status: result.status, payload: result.payload ?? {} });
      })
      .catch((error) => {
        setAgentInvokeError(`Could not run ${agentName}: ${error}`);
      })
      .finally(() => {
        setAgentBusy(false);
      });
  };

  return (
    <main className="jarvis-shell">
      <AppHeader platformIndicator={derivePlatformIndicator(platformState, platformError)} />
      <div className="shell-grid">
        <CapabilitySidebar
          capabilityStatuses={deriveCapabilityStatuses(platformState, platformError, agents, agentsError)}
          profiles={profiles}
          activeProfile={activeProfile}
          profileError={profileError}
          onCreateProfile={handleCreateProfile}
          onSelectProfile={handleSelectProfile}
        />
        <section className="workspace" aria-label="Guardian desktop experience">
          <StatusCards platformSignals={derivePlatformSignals(platformState, platformError)} />
          <div className="experience-grid">
            <div className="guardian-column">
              <GuardianOrbit
                knowledgeGraph={knowledgeGraph}
                knowledgeGraphError={knowledgeGraphError}
                activeClusters={activeClusters}
              />
              <CommandPanel
                messages={messages}
                inputValue={inputValue}
                onInputChange={setInputValue}
                onSubmit={handleSubmit}
                sending={sending}
                sendError={sendError}
                onSpeak={handleSpeak}
                speakError={speakError}
                isRecording={isRecording}
                onToggleRecording={handleToggleRecording}
                transcribeError={transcribeError}
                transcriptionAvailable={Boolean(platformState?.transcriptionAvailable)}
              />
            </div>
            <div className="side-column">
              <SystemHealthPanel
                platformState={platformState}
                platformError={platformError}
                lastHeartbeatAt={lastHeartbeatAt}
              />
              <KnowledgeMetricsPanel graph={knowledgeGraph} error={knowledgeGraphError} />
              <ActiveClustersPanel graph={knowledgeGraph} error={knowledgeGraphError} activeClusters={activeClusters} />
              <AgentFrameworkPanel
                agents={agents}
                agentsError={agentsError}
                agentBusy={agentBusy}
                agentResult={agentResult}
                agentInvokeError={agentInvokeError}
                onInvokeAgent={handleInvokeAgent}
              />
              <DiagnosticsPanel diagnostics={diagnostics} />
            </div>
          </div>
          <AppFooter />
        </section>
      </div>
    </main>
  );
}