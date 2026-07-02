export const STATUS = Object.freeze({
  OPERATIONAL: "Operational",
  AVAILABLE: "Available",
  PLACEHOLDER: "Placeholder",
  NOT_IMPLEMENTED: "Not Implemented",
  OFFLINE: "Offline",
  UNKNOWN: "Unknown",
});

export const guardianStatus = Object.freeze({
  title: "Guardian",
  state: STATUS.AVAILABLE,
  greeting: "Good evening, Richard.",
  role: "I am Guardian, your trusted AI companion.",
  platform: "The JARVIS Platform is operational.",
  assurance: "I am here to help, support and protect your world.",
  boundary: "Conversation runtime is not yet implemented.",
});

export const platformSignals = Object.freeze([
  {
    id: "platform",
    label: "JARVIS Platform",
    state: STATUS.OPERATIONAL,
    detail: "Core platform online",
  },
  {
    id: "services",
    label: "Core Services",
    state: STATUS.OPERATIONAL,
    detail: "All core services healthy",
  },
  {
    id: "providers",
    label: "External Providers",
    state: STATUS.OFFLINE,
    detail: "No providers connected",
  },
]);

export const capabilityStatuses = Object.freeze([
  {
    id: "sentinel",
    label: "Sentinel Gateway",
    state: STATUS.PLACEHOLDER,
    detail: "Trust gateway before Platform Services",
  },
  {
    id: "platform-services",
    label: "Platform Services",
    state: STATUS.PLACEHOLDER,
    detail: "Reserved service boundary for future capabilities",
  },
  {
    id: "memory",
    label: "Memory",
    state: STATUS.NOT_IMPLEMENTED,
    detail: "Persistent memory is outside this implementation",
  },
  {
    id: "providers",
    label: "Providers",
    state: STATUS.OFFLINE,
    detail: "No provider adapters connected",
  },
  {
    id: "agent-framework",
    label: "Agent Framework",
    state: STATUS.PLACEHOLDER,
    detail: "Specialist capabilities will extend Guardian",
  },
]);

export const diagnostics = Object.freeze([
  {
    id: "boundary",
    label: "Implementation Boundary",
    state: STATUS.UNKNOWN,
    detail: "Tauri + React UXP shell",
  },
  {
    id: "shell",
    label: "Shell Status",
    state: STATUS.UNKNOWN,
    detail: "Interface shell only",
  },
  {
    id: "guardian",
    label: "Guardian",
    state: STATUS.OPERATIONAL,
    detail: "Interface active",
  },
  {
    id: "sentinel",
    label: "Sentinel",
    state: STATUS.PLACEHOLDER,
    detail: "Trust gateway placeholder",
  },
  {
    id: "providers",
    label: "Providers",
    state: STATUS.OFFLINE,
    detail: "Not connected",
  },
  {
    id: "agents",
    label: "Agents",
    state: STATUS.OFFLINE,
    detail: "No execution",
  },
  {
    id: "first-light",
    label: "First Light",
    state: STATUS.OPERATIONAL,
    detail: "Python reference preserved",
  },
]);