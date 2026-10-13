// The honest capability list (ESR-0061 WP4c, EIP-ESR0061-004 item 6.7).
// Every row is built from a real status call; a status that could not be read
// is Unknown, never Ready. A capability that is not built is not a row here:
// it is named in NOT_BUILT_YET and shown only as "Not available yet".

export const CAP = Object.freeze({
  READY: "Ready",
  PREPARING: "Preparing",
  NOT_AVAILABLE: "Not available",
  OFFLINE: "Offline",
  UNKNOWN: "Unknown",
});

export const NOT_BUILT_YET = Object.freeze([
  "Seeing images or the camera",
  "Searching the internet",
  "Controlling smart-home devices",
]);

const row = (id, label, state, detail) => ({ id, label, state, detail });

const LOCAL_MODEL = "AI model on this computer";
const CLAUDE = "Claude (over the internet)";

// Inputs are exactly what the app has read; null means "not read yet" and the
// matching *Error means the read failed.
export function deriveCapabilityList({
  platformState,
  platformError,
  ollama,
  ollamaError,
  claude,
  agents,
  agentsError,
  memoryStatusError,
}) {
  const down = Boolean(platformError);
  const waiting = !down && !platformState;
  const running = platformState?.state === "Running";

  const fromPlatform = (id, label, whenKnown) => {
    if (down) return row(id, label, CAP.OFFLINE, "JARVIS backend is unavailable");
    if (waiting) return row(id, label, CAP.PREPARING, "Connecting to JARVIS...");
    return whenKnown();
  };

  const guardian = fromPlatform("guardian", "Conversation", () =>
    running
      ? row("guardian", "Conversation", CAP.READY, "JARVIS is running")
      : row("guardian", "Conversation", CAP.OFFLINE, `Runtime: ${platformState.state}`),
  );

  const sentinel = fromPlatform("sentinel", "Safety gateway", () =>
    running
      ? row("sentinel", "Safety gateway", CAP.READY, "Every request passes the trust gateway")
      : row("sentinel", "Safety gateway", CAP.OFFLINE, "Not running"),
  );

  let localModel;
  if (ollamaError) {
    localModel = row("local-model", LOCAL_MODEL, CAP.UNKNOWN, "Its status could not be read");
  } else if (!ollama) {
    localModel = row("local-model", LOCAL_MODEL, CAP.PREPARING, "Checking...");
  } else if (!ollama.installed) {
    localModel = row("local-model", LOCAL_MODEL, CAP.NOT_AVAILABLE, "Ollama is not installed");
  } else if (!ollama.running) {
    localModel = row("local-model", LOCAL_MODEL, CAP.OFFLINE, "Ollama is installed but not running");
  } else if (ollama.pull?.active && !ollama.activeModelInstalled) {
    localModel = row("local-model", LOCAL_MODEL, CAP.PREPARING, `Downloading ${ollama.pull.model ?? "a model"}`);
  } else if (!ollama.activeModelInstalled) {
    localModel = row(
      "local-model",
      LOCAL_MODEL,
      CAP.NOT_AVAILABLE,
      ollama.activeModel ? `${ollama.activeModel} is not downloaded yet` : "No model is chosen yet",
    );
  } else {
    localModel = row("local-model", LOCAL_MODEL, CAP.READY, ollama.activeModel);
  }

  let claudeRow;
  if (!claude) {
    claudeRow = row("claude", CLAUDE, CAP.UNKNOWN, "Its status could not be read");
  } else if (!claude.configured) {
    claudeRow = row("claude", CLAUDE, CAP.NOT_AVAILABLE, "No Claude key is set up");
  } else if (!claude.mayEscalate) {
    claudeRow = row("claude", CLAUDE, CAP.NOT_AVAILABLE, "This profile cannot ask Claude");
  } else {
    claudeRow = row("claude", CLAUDE, CAP.READY, "Used only when you ask");
  }

  const memory = fromPlatform("memory", "Memory", () => {
    if (memoryStatusError) return row("memory", "Memory", CAP.UNKNOWN, "Its status could not be read");
    if (platformState.memoryConnected === "Online") {
      return row("memory", "Memory", CAP.READY, "Notes are kept on this computer");
    }
    if (platformState.memoryConnected === "Unknown") {
      return row("memory", "Memory", CAP.UNKNOWN, "Its status could not be read");
    }
    return row("memory", "Memory", CAP.NOT_AVAILABLE, "No memory service is connected");
  });

  let agentsRow;
  if (agentsError) {
    agentsRow = row("agents", "Agents", CAP.UNKNOWN, "Their status could not be read");
  } else if (!agents) {
    agentsRow = row("agents", "Agents", CAP.PREPARING, "Checking...");
  } else if (agents.length === 0) {
    agentsRow = row("agents", "Agents", CAP.NOT_AVAILABLE, "No agents are registered");
  } else {
    agentsRow = row("agents", "Agents", CAP.READY, `${agents.length} available (${agents.join(", ")})`);
  }

  const flag = (id, label, key, onText, offText) =>
    fromPlatform(id, label, () => {
      const value = platformState[key];
      if (value === true) return row(id, label, CAP.READY, onText);
      if (value === false) return row(id, label, CAP.NOT_AVAILABLE, offText);
      return row(id, label, CAP.UNKNOWN, "Its status could not be read");
    });

  const voiceIn = flag(
    "voice-in",
    "Speaking to JARVIS",
    "transcriptionAvailable",
    "Speech is turned into text on this computer",
    "No speech-to-text is set up",
  );
  const voiceOut = flag(
    "voice-out",
    "JARVIS speaking aloud",
    "speechAvailable",
    "Replies can be read aloud",
    "No voice is set up",
  );

  return [guardian, localModel, claudeRow, memory, voiceIn, voiceOut, agentsRow, sentinel];
}

// The short list beside the conversation: what a person can use now, for the
// role they have. Claude is not mentioned to a role that cannot ask it.
export function visibleToGuardianColumn(rows, { mayAskClaude, seesMemory }) {
  const wanted = new Set(["local-model", "voice-in", "voice-out"]);
  if (mayAskClaude) wanted.add("claude");
  if (seesMemory) wanted.add("memory");
  return rows.filter((entry) => wanted.has(entry.id));
}
