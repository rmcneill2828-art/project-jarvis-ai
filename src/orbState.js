// The presence Orb's state, from real events only (ESR-0061 WP4b,
// EIP-ESR0061-004 item 6.3). Nothing here runs on a timer or a script.
//
// Priority when several apply: speaking, thinking, offline, listening, idle.
// Offline outranks Listening so the Orb never looks ready to hear a question
// the system cannot answer.

export function deriveOrbState({ speaking, thinking, offline, listening }) {
  if (speaking) return "speaking";
  if (thinking) return "thinking";
  if (offline) return "offline";
  if (listening) return "listening";
  return "idle";
}

// Offline is: the backend cannot be reached or is not running, no provider is
// online, or the last turn failed because no AI model answered (cleared by the
// next success). Before the first platform status arrives nothing is known, so
// that is "connecting", not offline.
export function isOffline({ platformState, platformError, lastTurnFailed }) {
  if (platformError) return true;
  if (lastTurnFailed) return true;
  if (!platformState) return false;
  return platformState.state !== "Running" || platformState.providerConnected !== "Online";
}

export function isConnecting({ platformState, platformError }) {
  return !platformState && !platformError;
}

// The words for each state. The state is always written as text, so colour and
// motion are never the only signal.
export function orbReadout(state, { recording, connecting, model }) {
  if (connecting && state === "idle") {
    return { label: "Connecting", detail: "Connecting to JARVIS on this computer." };
  }
  switch (state) {
    case "listening":
      return { label: "Listening", detail: "Speak now. Press the microphone again when you finish." };
    case "thinking":
      return { label: "Thinking", detail: "Working on your question." };
    case "speaking":
      return { label: "Speaking", detail: "Reading the reply aloud." };
    case "offline":
      return {
        label: "Offline",
        detail: recording
          ? "Offline: the microphone is on, but JARVIS cannot answer until an AI model is reachable."
          : "Offline: JARVIS cannot reach an AI model on this computer.",
      };
    default:
      return {
        label: "Ready",
        detail: model ? `Answering on this computer with ${model}.` : "Answering on this computer.",
      };
  }
}

// The most frames a state may draw per second (EIP item 6.3): a 120 Hz display
// is not driven twice as hard as a 60 Hz one, a slow drift needs no more than
// 30, and nothing moves while offline.
export const FRAME_BUDGET_FPS = { speaking: 60, thinking: 60, listening: 60, idle: 30, offline: 10 };

export function minFrameIntervalMs(state) {
  return 1000 / (FRAME_BUDGET_FPS[state] ?? 30) - 2;
}
