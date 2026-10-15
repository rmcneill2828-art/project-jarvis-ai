// What each household role may see and do in the app (ESR-0061 WP4c,
// EIP-ESR0061-004 item 6.5). The backend enforces these rules at the RPC
// boundary (jarvis/interfaces/stdio_rpc.py); this file only mirrors them so
// the screen never offers what would be refused. Profiles are not
// authenticated, so none of this is a security boundary.

export const ROLE = Object.freeze({
  ADMINISTRATOR: "Administrator",
  ADULT: "Adult",
  CHILD: "Child",
  GUEST: "Guest",
});

const ALL_VIEWS = ["guardian", "memory", "knowledge", "agents", "models", "settings", "system"];

const VIEWS_BY_ROLE = {
  [ROLE.ADMINISTRATOR]: ALL_VIEWS,
  [ROLE.ADULT]: ALL_VIEWS,
  [ROLE.CHILD]: ["guardian", "memory"],
  [ROLE.GUEST]: ["guardian"],
};

// No profile, or a role this app does not know, gets the conversation only:
// the backend refuses most of the rest without a profile, and showing less is
// the safe way to be wrong.
export function viewsForRole(role) {
  return VIEWS_BY_ROLE[role] ?? ["guardian"];
}

export const canAskClaude = (role) => role === ROLE.ADMINISTRATOR || role === ROLE.ADULT;

// Whole-store backup and restore are Administrator-only in the backend.
export const canBackupMemory = (role) => role === ROLE.ADMINISTRATOR;

// An Adult sees the backup controls, disabled, with the reason; a Child or
// Guest is not shown them at all.
export const seesBackupControls = (role) => role === ROLE.ADMINISTRATOR || role === ROLE.ADULT;

// A Child may read their own notes but not forget them.
export const canForgetMemory = (role) => role === ROLE.ADMINISTRATOR || role === ROLE.ADULT;

// Only an Administrator may set, remove or test the Claude key (the backend
// enforces it; an Adult sees the privacy notice in Settings and nothing else).
export const canChangeClaudeKey = (role) => role === ROLE.ADMINISTRATOR;

// Whether a profile of this role could ever have its notes sent to Claude: the
// backend allows it only for a profile that may ask Claude at all.
export const profileMayShareMemory = (profileRole) => profileRole === ROLE.ADMINISTRATOR || profileRole === ROLE.ADULT;

// Export: an Administrator for any profile, an Adult for their own only. A Child
// or Guest has no Settings view; an Administrator runs the export for them.
export const canExportProfile = (viewerRole, viewerId, profileId) =>
  viewerRole === ROLE.ADMINISTRATOR || (viewerRole === ROLE.ADULT && viewerId === profileId);

// Erasure is Administrator-only.
export const canErasePeople = (role) => role === ROLE.ADMINISTRATOR;

// Changing a profile's sharing, and the audit retention, are Administrator-only.
export const canChangeHouseholdSettings = (role) => role === ROLE.ADMINISTRATOR;

// Shared household notes (profileId null) can be deleted only by an Administrator.
export const canForgetHouseholdNote = (role) => role === ROLE.ADMINISTRATOR;
