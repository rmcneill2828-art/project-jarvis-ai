export const STATUS = Object.freeze({
  AVAILABLE: "Available",
  PLACEHOLDER: "Placeholder",
  NOT_IMPLEMENTED: "Not Implemented",
  OFFLINE: "Offline",
  UNKNOWN: "Unknown",
});

export const guardianStatus = Object.freeze({
  title: "Guardian Interface",
  state: STATUS.AVAILABLE,
  message: "Good evening. Guardian interface is online.",
  detail:
    "Guardian is the trusted companion at the centre of this desktop experience. Runtime intelligence is not implemented in this shell.",
});

export const platformSignals = Object.freeze([
  {
    label: "Platform Status",
    state: STATUS.PLACEHOLDER,
    detail: "Desktop shell available; platform services are preparing.",
  },
  {
    label: "Core Services",
    state: STATUS.AVAILABLE,
    detail: "Python platform foundation exists for bootstrap and status reporting.",
  },
  {
    label: "External Providers",
    state: STATUS.OFFLINE,
    detail: "No AI provider integration is connected in this shell.",
  },
]);

export const capabilityStatuses = Object.freeze([
  {
    id: "guardian-interface",
    label: "Guardian Interface",
    state: STATUS.AVAILABLE,
    detail: "Primary trusted user-facing companion shell.",
  },
  {
    id: "sentinel",
    label: "Sentinel Trust Posture",
    state: STATUS.PLACEHOLDER,
    detail: "Trust posture is visible only; no enforcement engine is active.",
  },
  {
    id: "memory",
    label: "Memory",
    state: STATUS.NOT_IMPLEMENTED,
    detail: "Persistent memory is outside this implementation package.",
  },
  {
    id: "providers",
    label: "Providers",
    state: STATUS.OFFLINE,
    detail: "Provider adapters are not connected and no external calls are made.",
  },
  {
    id: "agent-framework",
    label: "Agent Framework",
    state: STATUS.PLACEHOLDER,
    detail: "Future specialist capabilities extend Guardian; no agent execution exists.",
  },
  {
    id: "skills",
    label: "Skills",
    state: STATUS.NOT_IMPLEMENTED,
    detail: "Skill execution is not implemented in this desktop shell.",
  },
  {
    id: "settings",
    label: "Settings",
    state: STATUS.PLACEHOLDER,
    detail: "Settings navigation placeholder; no routed feature is active.",
  },
]);

export const conversationMessages = Object.freeze([
  {
    speaker: "Guardian",
    state: STATUS.AVAILABLE,
    text: "Good evening. Guardian interface is online.",
  },
  {
    speaker: "Platform",
    state: STATUS.PLACEHOLDER,
    text: "Core services are preparing.",
  },
  {
    speaker: "Boundary",
    state: STATUS.NOT_IMPLEMENTED,
    text: "Conversation runtime is not yet implemented.",
  },
]);

export const diagnostics = Object.freeze([
  ["Build mode", "Vite + Tauri React shell"],
  ["Shell status", "Available"],
  ["Sentinel posture", "Trust posture placeholder only"],
  ["Capability count", "7 visible capabilities"],
  ["Placeholder boundary", "Runtime, memory, providers and agents inactive"],
  ["Validation status", "External command evidence only"],
]);
