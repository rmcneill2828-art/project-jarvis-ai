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
  message: "Guardian interface initialised.",
  detail:
    "This shell is the first desktop expression of the JARVIS Platform. Guardian is the trusted companion at the centre of the experience.",
});

export const platformSignals = Object.freeze([
  {
    label: "JARVIS Platform",
    state: STATUS.PLACEHOLDER,
    detail: "Preparing the desktop shell and future service boundary.",
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
    id: "sentinel",
    label: "Sentinel Gateway",
    state: STATUS.PLACEHOLDER,
    detail: "Positioned as the future trust gateway before Platform Services.",
  },
  {
    id: "platform-services",
    label: "Platform Services",
    state: STATUS.PLACEHOLDER,
    detail: "Reserved service boundary for future approved capabilities.",
  },
  {
    id: "memory",
    label: "Memory",
    state: STATUS.NOT_IMPLEMENTED,
    detail: "Persistent memory is explicitly outside this implementation package.",
  },
  {
    id: "providers",
    label: "Providers",
    state: STATUS.OFFLINE,
    detail: "Provider adapters are not connected and no external calls are made.",
  },
  {
    id: "agents",
    label: "Agent Framework",
    state: STATUS.PLACEHOLDER,
    detail: "Future specialist capabilities extend Guardian; no agent execution exists.",
  },
  {
    id: "diagnostics",
    label: "Diagnostics",
    state: STATUS.AVAILABLE,
    detail: "Static shell diagnostics are visible for implementation review.",
  },
]);

export const diagnostics = Object.freeze([
  ["Shell", "Tauri + React UXP scaffold"],
  ["Guardian", "Interface shell only"],
  ["Sentinel", "Trust gateway placeholder"],
  ["Providers", "Not connected"],
  ["Agents", "No execution"],
  ["First Light", "Python reference implementation preserved"],
]);