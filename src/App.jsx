import { useEffect, useMemo, useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import {
  Activity,
  Box,
  ChevronDown,
  CircleUserRound,
  Cloud,
  Code2,
  Database,
  Grid3X3,
  Link2,
  Mic,
  Monitor,
  SendHorizontal,
  Server,
  Shield,
  UsersRound,
  Volume2,
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
import { MemoryManagementPanel } from "./MemoryManagementPanel.jsx";
import { ClaudeBadge, ClaudeConfirmDialog, EscalationBar } from "./ClaudeEscalation.jsx";
import { LocalAiPanel } from "./LocalAiPanel.jsx";
import { PresenceOrb } from "./PresenceOrb.jsx";
import { deriveOrbState, isConnecting, isOffline, orbReadout } from "./orbState.js";
import { NavRail, TopBar } from "./Shell.jsx";

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
// Must match MAX_MESSAGE_CHARS in jarvis/interfaces/stdio_rpc.py (EBG-0143,
// ESR-0059 WP8): the backend refuses longer messages, so the input stops
// accepting typing at the same limit instead of failing after send.
const MAX_MESSAGE_CHARS = 4000;

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

// The capability rows that used to fill the sidebar ("Platform Placeholders"),
// now a panel in the System view (ESR-0061 WP4a). WP4c replaces them with a
// list built only from real status.
function CapabilitiesPanel({ capabilityStatuses }) {
  return (
    <section className="capabilities-panel" aria-labelledby="capabilities-heading">
      <h2 id="capabilities-heading">Capabilities</h2>
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
    </section>
  );
}

// GAM-0001 Section 8.1's Household Role Model - the only roles a profile may
// be created with (EIP-ESR0046-001).
const HOUSEHOLD_ROLES = ["Administrator", "Adult", "Child", "Guest"];

function ProfileCard({ profiles, activeProfile, profileError, onCreateProfile, onSelectProfile, inTopBar = false }) {
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
    <section className={`profile-card${inTopBar ? " in-topbar" : ""}`} aria-label="Signed in profile">
      <button
        type="button"
        className="profile-summary"
        onClick={() => setPickerOpen((open) => !open)}
        aria-expanded={pickerOpen}
        aria-label="Switch Guardian profile"
      >
        <span className="avatar" aria-hidden="true">
          {activeProfile.displayName.trim().charAt(0).toUpperCase() || "?"}
        </span>
        <div>
          <strong>{activeProfile.displayName}</strong>
          <span>{activeProfile.role}</span>
        </div>
        <ChevronDown size={16} aria-hidden="true" />
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
      <div className="guardian-orb" role="img" aria-label="Repository knowledge graph">
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
    </aside>
  );
}

// Where a reply came from (WP4b, EIP item 6.6). Every reply from the platform
// carries one: the model on this computer, Claude, or "no model", for the
// platform's own messages. Claude is named only on a reply Claude gave, so a
// profile that cannot ask Claude never sees the word.
function ReplySource({ entry }) {
  if (entry.source === "claude") {
    return (
      <span className="reply-source">
        <ClaudeBadge /> answered over the internet
      </span>
    );
  }
  if (entry.source === "local") {
    return (
      <span className="reply-source">
        On this computer{entry.model ? ` · ${entry.model}` : ""}
      </span>
    );
  }
  if (entry.source === "none") return <span className="reply-source">No AI model answered</span>;
  return null;
}

// The permanent line above the composer: the person is told they are talking
// to an AI, and where the replies in this conversation come from.
function disclosureText(messages) {
  const lastLocal = [...messages].reverse().find((entry) => entry.source === "local" && entry.model);
  const fromClaude = messages.some((entry) => entry.source === "claude");
  const base = lastLocal
    ? `You are talking to JARVIS, an AI. Replies come from the AI model on this computer (${lastLocal.model}).`
    : "You are talking to JARVIS, an AI. Replies come from the AI model on this computer.";
  return fromClaude ? `${base} Some replies in this conversation came from Claude, over the internet.` : base;
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
  claudeStatus,
  offer,
  escalating,
  onAskClaude,
  onReviewOffer,
}) {
  const lastUserMessage = [...messages].reverse().find((entry) => entry.role === "user");
  return (
    <section className="command-panel" aria-labelledby="command-heading">
      <div className="conversation-area">
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
              {entry.role === "guardian" && <ReplySource entry={entry} />}
            </p>
          ))}
          </div>
        )}
      </div>
      <div className="composer-area">
      <EscalationBar
        claudeStatus={claudeStatus}
        offer={offer}
        canAsk={Boolean(lastUserMessage) && !sending}
        busy={escalating}
        onAskClaude={onAskClaude}
        onReviewOffer={onReviewOffer}
      />
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
      <p className="ai-disclosure" id="ai-disclosure">
        {disclosureText(messages)}
      </p>
      <form
        className="input-shell"
        aria-describedby="ai-disclosure"
        aria-label="Guardian conversation input"
        onSubmit={(event) => {
          event.preventDefault();
          onSubmit();
        }}
      >
        <input
          value={inputValue}
          onChange={(event) => onInputChange(event.target.value)}
          maxLength={MAX_MESSAGE_CHARS}
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
      </div>
    </section>
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

  // Which view of the app shell is showing (ESR-0061 WP4a).
  const [view, setView] = useState("guardian");

  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [sending, setSending] = useState(false);
  const [sendError, setSendError] = useState(null);
  const [speakError, setSpeakError] = useState(null);

  // Asking Claude (ESR-0061 WP3b, EIP-ESR0061-003 6.5-6.7). `claudeStatus` is
  // what the backend says about Claude for the active profile (configured,
  // whether this role may ask, the month's allowance); `offer` is the latest
  // offer, with the message it is for; nothing is sent until the dialog's
  // confirm button spends the offer's one-time token.
  const [claudeStatus, setClaudeStatus] = useState(null);
  const [offer, setOffer] = useState(null);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [escalating, setEscalating] = useState(false);
  const [escalationError, setEscalationError] = useState(null);

  // Model download progress and completion, pushed by the backend as
  // notifications (ESR-0061 WP3c); the Local AI panel acts on them.
  const [pullProgress, setPullProgress] = useState(null);
  const [pullFinished, setPullFinished] = useState(null);
  // Which model the person asked to switch to once its download ends. Held here,
  // and acted on here when the download ends, so it works whichever view is
  // showing while a download that takes minutes runs (WP4a implementation
  // review, Low; post-commit review, High).
  const useWhenDoneRef = useRef(null);

  // Voice Faculty Increment B (EIP-ESR0047-001): push-to-talk speech input.
  // isRecording drives the mic button's visual state only - the actual
  // MediaRecorder instance and its bounded 30s auto-stop timer live in refs,
  // not state, since neither needs to trigger a re-render.
  const [isRecording, setIsRecording] = useState(false);
  const [transcribing, setTranscribing] = useState(false);
  // The Orb's other real events (WP4b): reply audio playing, and whether the
  // last turn failed because no AI model answered.
  const [speaking, setSpeaking] = useState(false);
  const [lastTurnFailed, setLastTurnFailed] = useState(false);
  const audioRef = useRef(null);
  // A conversation belongs to the profile that had it. Every request notes the
  // epoch it started in, and its answer is dropped if the profile has changed.
  const conversationEpochRef = useRef(0);
  const previousProfileIdRef = useRef(null);
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

  // Memory Management (EBG-0131, ESR-0058 WP6): recordCount null =
  // connecting, otherwise the real memory.status count.
  const [memoryRecordCount, setMemoryRecordCount] = useState(null);
  const [memoryStatusError, setMemoryStatusError] = useState(null);

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

    invoke("memory_status")
      .then((result) => {
        if (!cancelled) setMemoryRecordCount(result.recordCount ?? 0);
      })
      .catch((error) => {
        if (!cancelled) setMemoryStatusError(String(error));
      });

    return () => {
      cancelled = true;
    };
  }, []);

  // Who may ask Claude depends on the active profile's role, so this is read
  // again whenever the profile changes. A failed read hides the controls
  // rather than guessing.
  useEffect(() => {
    let cancelled = false;
    setOffer(null);
    setConfirmOpen(false);
    invoke("provider_status")
      .then((result) => {
        if (!cancelled) setClaudeStatus(result.claude ?? null);
      })
      .catch(() => {
        if (!cancelled) setClaudeStatus(null);
      });
    return () => {
      cancelled = true;
    };
  }, [activeProfile?.id]);

  // Switching profile clears the on-screen conversation, any open offer or
  // dialog, and anything in flight (WP4b, EIP item 6.2): the backend keeps each
  // profile's history separate, so the screen must not show the previous
  // profile's messages - or its Claude labels - to the next person.
  useEffect(() => {
    const previous = previousProfileIdRef.current;
    previousProfileIdRef.current = activeProfile?.id ?? null;
    if (previous === null || previous === (activeProfile?.id ?? null)) return;
    conversationEpochRef.current += 1;
    setMessages([]);
    setInputValue("");
    setSending(false);
    setSendError(null);
    setSpeakError(null);
    setTranscribeError(null);
    setEscalating(false);
    setEscalationError(null);
    setLastTurnFailed(false);
    setOffer(null);
    setConfirmOpen(false);
    if (audioRef.current) {
      audioRef.current.pause?.();
      audioRef.current = null;
    }
    setSpeaking(false);
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      // Recording belongs to the previous person too: stop it; its onstop
      // releases the microphone and drops the audio.
      mediaRecorderRef.current.stop();
    }
    if (recordingTimeoutRef.current) {
      clearTimeout(recordingTimeoutRef.current);
      recordingTimeoutRef.current = null;
    }
    setIsRecording(false);
    setTranscribing(false);
  }, [activeProfile?.id]);

  // Re-reads the real count after a restore, rather than trusting the
  // restore response's own recordCount as a proxy for the store's new
  // total - restoring into a non-empty store (once ever allowed) would
  // make those two numbers genuinely different.
  const refreshMemoryStatus = () => {
    invoke("memory_status")
      .then((result) => setMemoryRecordCount(result.recordCount ?? 0))
      .catch((error) => setMemoryStatusError(String(error)));
  };

  useEffect(() => {
    let unlisten;
    let cancelled = false;

    listen("jarvis://notification", (event) => {
      if (event.payload?.method === "system.heartbeat") {
        setLastHeartbeatAt(new Date());
      }
      if (event.payload?.method === "ollama.pullProgress") {
        setPullProgress(event.payload.params ?? null);
      }
      if (event.payload?.method === "ollama.pullFinished") {
        const finished = event.payload.params ?? {};
        // Switching to the model the person asked to use happens here, in the
        // app, so it does not depend on which view is showing when the download
        // ends (WP4a post-commit review). The panel is told afterwards, so its
        // refresh sees the switch.
        const wanted = finished.outcome === "completed" && useWhenDoneRef.current === finished.model;
        if (finished.model && useWhenDoneRef.current === finished.model) useWhenDoneRef.current = null;
        const announce = (switchFailed) => setPullFinished({ ...finished, switchFailed, at: Date.now() });
        if (wanted) {
          invoke("ollama_use_model", { model: finished.model })
            .then(() => announce(false))
            .catch(() => announce(true));
        } else {
          announce(false);
        }
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
    setOffer(null);
    setEscalationError(null);

    const epoch = conversationEpochRef.current;
    invoke("send_message", { message })
      .then((response) => {
        if (epoch !== conversationEpochRef.current) return;
        // `answered` is false for the platform's own messages (no provider, not
        // running): no model produced those, and the Orb goes Offline until a
        // turn succeeds. A backend that does not say is not assumed to have failed.
        const answered = response.answered !== false;
        setLastTurnFailed(!answered);
        setMessages((current) => [
          ...current,
          {
            id: `${Date.now()}-guardian`,
            role: "guardian",
            text: response.message,
            source: answered ? "local" : "none",
            model: response.model ?? null,
          },
        ]);
        if (response.escalation?.offered) setOffer({ ...response.escalation, message });
      })
      .catch((error) => {
        if (epoch !== conversationEpochRef.current) return;
        setSendError(`Guardian did not respond: ${error}`);
        setLastTurnFailed(true);
      })
      .finally(() => {
        if (epoch === conversationEpochRef.current) setSending(false);
      });
  };

  // "Ask Claude": an offer for the last thing the person said, whatever the
  // local model answered. Opens the confirmation; sends nothing.
  const handleAskClaude = () => {
    const last = [...messages].reverse().find((entry) => entry.role === "user");
    if (!last) return;
    setEscalationError(null);
    const epoch = conversationEpochRef.current;
    invoke("offer_escalation", { message: last.text })
      .then((requested) => {
        if (epoch !== conversationEpochRef.current) return;
        setOffer({ ...requested, message: last.text });
        setConfirmOpen(true);
      })
      .catch((error) => {
        if (epoch !== conversationEpochRef.current) return;
        setEscalationError(`Could not ask Claude: ${error}`);
      });
  };

  const handleConfirmEscalation = () => {
    if (!offer || escalating) return;
    setEscalating(true);
    setEscalationError(null);

    const epoch = conversationEpochRef.current;
    invoke("escalate_message", { token: offer.token })
      .then((result) => {
        if (epoch !== conversationEpochRef.current) return;
        setMessages((current) => [
          ...current,
          {
            id: `${Date.now()}-claude`,
            role: "guardian",
            text: result.message,
            answeredBy: result.answeredBy ?? null,
            source: result.answeredBy === "claude" ? "claude" : "none",
          },
        ]);
        setClaudeStatus((current) => (current ? { ...current, allowance: result.allowance ?? current.allowance } : current));
      })
      .catch((error) => {
        if (epoch !== conversationEpochRef.current) return;
        setEscalationError(`Claude did not respond: ${error}`);
      })
      .finally(() => {
        if (epoch !== conversationEpochRef.current) return;
        // The token is spent either way, so the offer is over.
        setOffer(null);
        setConfirmOpen(false);
        setEscalating(false);
      });
  };

  const handleSpeak = (text) => {
    setSpeakError(null);

    const epoch = conversationEpochRef.current;
    invoke("speak_message", { text })
      .then((result) => {
        // Audio synthesised for the previous profile is never played to the next.
        if (epoch !== conversationEpochRef.current) return;
        if (result.status !== "synthesized") {
          setSpeakError(result.message || "Guardian could not speak this response.");
          return;
        }
        try {
          // The Orb speaks while this audio plays: the app records play, end
          // and error of the audio it plays (WP4b). A newer reply replaces an
          // older one still playing.
          audioRef.current?.pause?.();
          const audio = new Audio(`data:${result.mimeType};base64,${result.audio}`);
          audioRef.current = audio;
          const stop = () => {
            if (audioRef.current === audio) {
              audioRef.current = null;
              setSpeaking(false);
            }
          };
          audio.onended = stop;
          audio.onerror = () => {
            if (audioRef.current === audio) setSpeakError("Guardian's voice could not play.");
            stop();
          };
          audio
            .play()
            .then(() => {
              if (audioRef.current === audio) setSpeaking(true);
            })
            .catch((error) => {
              if (audioRef.current === audio) setSpeakError(`Guardian's voice could not play: ${error}`);
              stop();
            });
        } catch (error) {
          setSpeakError(`Guardian's voice could not play: ${error}`);
          setSpeaking(false);
        }
      })
      .catch((error) => {
        if (epoch !== conversationEpochRef.current) return;
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

      // A recording belongs to the profile that started it (WP4b): if the
      // profile changes before it ends, the microphone is still released but
      // the audio is dropped, never transcribed into the next person's screen.
      const epoch = conversationEpochRef.current;
      recorder.onstop = () => {
        stream.getTracks().forEach((track) => track.stop());
        const mimeType = recorder.mimeType || "audio/webm";
        const blob = new Blob(recordedChunksRef.current, { type: mimeType });
        recordedChunksRef.current = [];
        if (epoch !== conversationEpochRef.current) return;

        setTranscribing(true);
        blobToBase64(blob)
          .then((audioBase64) => invoke("transcribe_audio", { audioBase64, mimeType }))
          .then((result) => {
            if (epoch !== conversationEpochRef.current) return;
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
            if (epoch !== conversationEpochRef.current) return;
            setTranscribeError(`Guardian could not transcribe that: ${error}`);
          })
          .finally(() => {
            setTranscribing(false);
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

  // The presence Orb's state, from real events only (WP4b, src/orbState.js).
  const orbState = deriveOrbState({
    speaking,
    thinking: sending || escalating || transcribing,
    offline: isOffline({ platformState, platformError, lastTurnFailed }),
    listening: isRecording,
  });
  const lastLocalModel = [...messages].reverse().find((entry) => entry.source === "local" && entry.model)?.model ?? null;
  const orbText = orbReadout(orbState, {
    recording: isRecording,
    connecting: isConnecting({ platformState, platformError }),
    model: lastLocalModel,
  });

  const platformIndicator = derivePlatformIndicator(platformState, platformError);
  const capabilityStatusRows = deriveCapabilityStatuses(platformState, platformError, agents, agentsError);

  return (
    <div className="app-shell">
      <TopBar
        platformChip={
          <>
            <StateDot state={platformIndicator.status} />
            <span>{platformIndicator.label}</span>
            <StatusBadge state={platformIndicator.status} />
          </>
        }
        profileSlot={
          activeProfile ? (
            <ProfileCard
              inTopBar
              profiles={profiles}
              activeProfile={activeProfile}
              profileError={profileError}
              onCreateProfile={handleCreateProfile}
              onSelectProfile={handleSelectProfile}
            />
          ) : (
            <span className="local-ai-note">No profile selected</span>
          )
        }
      />
      <NavRail current={view} onSelect={setView} />
      <main className="app-main" aria-label="Guardian desktop experience">
        {!activeProfile && (
          <div className="profile-banner">
            <ProfileCard
              profiles={profiles}
              activeProfile={activeProfile}
              profileError={profileError}
              onCreateProfile={handleCreateProfile}
              onSelectProfile={handleSelectProfile}
            />
          </div>
        )}

        {view === "guardian" && (
          <section className="view guardian-view" aria-label="Guardian">
            <div className="guardian-presence">
              <PresenceOrb state={orbState} />
              <div className="orb-readout" role="status" aria-live="polite" data-orb-readout={orbState}>
                <span className="orb-state-label">{orbText.label}</span>
                <span className="orb-state-detail">{orbText.detail}</span>
              </div>
              <h1 id="command-heading" className="guardian-title">
                How can I help you today?
              </h1>
            </div>
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
              claudeStatus={claudeStatus}
              offer={offer}
              escalating={escalating}
              onAskClaude={handleAskClaude}
              onReviewOffer={() => setConfirmOpen(true)}
            />
            {escalationError && (
              <p className="conversation-error" role="alert">
                {escalationError}
              </p>
            )}
          </section>
        )}

        {view === "memory" && (
          <section className="view" aria-label="Memory">
            <div className="view-scroll">
              <h1 className="view-heading">Memory</h1>
              <p className="view-lede">Notes JARVIS keeps on this computer, only after you approve them.</p>
              <MemoryManagementPanel
                recordCount={memoryRecordCount}
                statusError={memoryStatusError}
                onStatusChange={refreshMemoryStatus}
              />
            </div>
          </section>
        )}

        {view === "knowledge" && (
          <section className="view" aria-label="Knowledge">
            <div className="view-scroll">
              <h1 className="view-heading">Knowledge</h1>
              <p className="view-lede">The project&rsquo;s engineering knowledge graph, drawn from the repository on this computer.</p>
              <div className="knowledge-stage">
                <GuardianOrbit
                  knowledgeGraph={knowledgeGraph}
                  knowledgeGraphError={knowledgeGraphError}
                  activeClusters={activeClusters}
                />
              </div>
              <div className="view-grid">
                <KnowledgeMetricsPanel graph={knowledgeGraph} error={knowledgeGraphError} />
                <ActiveClustersPanel graph={knowledgeGraph} error={knowledgeGraphError} activeClusters={activeClusters} />
              </div>
            </div>
          </section>
        )}

        {view === "agents" && (
          <section className="view" aria-label="Agents">
            <div className="view-scroll">
              <h1 className="view-heading">Agents</h1>
              <p className="view-lede">Helpers that do one job and report back. Each runs only when you ask.</p>
              <AgentFrameworkPanel
                agents={agents}
                agentsError={agentsError}
                agentBusy={agentBusy}
                agentResult={agentResult}
                agentInvokeError={agentInvokeError}
                onInvokeAgent={handleInvokeAgent}
              />
            </div>
          </section>
        )}

        {view === "models" && (
          <section className="view" aria-label="AI models">
            <div className="view-scroll">
              <h1 className="view-heading">AI models</h1>
              <p className="view-lede">JARVIS answers on this computer first. Claude is used only when you ask.</p>
              <LocalAiPanel
                activeProfile={activeProfile}
                pullProgress={pullProgress}
                pullFinished={pullFinished}
                useWhenDoneRef={useWhenDoneRef}
                onPullFinishedHandled={() => setPullFinished(null)}
              />
            </div>
          </section>
        )}

        {view === "system" && (
          <section className="view" aria-label="System">
            <div className="view-scroll">
              <h1 className="view-heading">System</h1>
              <p className="view-lede">What is running. JARVIS v0.1.0, shell edition.</p>
              <StatusCards platformSignals={derivePlatformSignals(platformState, platformError)} />
              <div className="view-grid">
                <SystemHealthPanel
                  platformState={platformState}
                  platformError={platformError}
                  lastHeartbeatAt={lastHeartbeatAt}
                />
                <CapabilitiesPanel capabilityStatuses={capabilityStatusRows} />
                <DiagnosticsPanel diagnostics={diagnostics} />
              </div>
            </div>
          </section>
        )}
      </main>
      {confirmOpen && offer && (
        <ClaudeConfirmDialog
          offer={offer}
          busy={escalating}
          onConfirm={handleConfirmEscalation}
          onCancel={() => setConfirmOpen(false)}
        />
      )}
    </div>
  );
}
