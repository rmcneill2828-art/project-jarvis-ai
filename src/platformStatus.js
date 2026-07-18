export const STATUS = Object.freeze({
  OPERATIONAL: "Operational",
  AVAILABLE: "Available",
  PLACEHOLDER: "Placeholder",
  NOT_IMPLEMENTED: "Not Implemented",
  OFFLINE: "Offline",
  UNKNOWN: "Unknown",
  CONNECTING: "Connecting",
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

// Guardian/Sentinel/Providers were removed from this list at ESR-0023 WP6
// (EBG-0073): SystemHealthPanel is now their sole owner, sourced from live
// platform.status data. The rows below remain permanently-static placeholders.
// first-light removed at ESR-0027 WP2 (EBG-0077): it reported on the legacy
// Tkinter First Light app rather than this shell's own implementation
// boundary, so it didn't fit this panel's UAM-0001 Section 11 purpose.
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
    id: "agents",
    label: "Agents",
    state: STATUS.OFFLINE,
    detail: "No execution",
  },
]);