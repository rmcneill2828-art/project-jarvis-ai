import { Activity, Cpu, Database, MessageSquare, Share2, UsersRound } from "lucide-react";

// The app shell (ESR-0061 WP4a, EIP-ESR0061-004 item 6.1): a top bar, a left
// rail of views and a main area. Which views a household role may see is added
// in WP4c; until then every view is listed.

export const VIEWS = [
  { id: "guardian", label: "Guardian", icon: MessageSquare },
  { id: "memory", label: "Memory", icon: Database },
  { id: "knowledge", label: "Knowledge", icon: Share2 },
  { id: "agents", label: "Agents", icon: UsersRound },
  { id: "models", label: "AI models", icon: Cpu },
  { id: "system", label: "System", icon: Activity },
];

export function TopBar({ platformChip, profileSlot }) {
  return (
    <header className="topbar" aria-label="JARVIS">
      <div className="brand">
        <span className="brand-mark" aria-hidden="true" />
        <span className="brand-text">JARVIS</span>
      </div>
      <div className="platform-chip" role="status" aria-label="JARVIS platform status">
        {platformChip}
      </div>
      <span className="topbar-spacer" />
      <div className="profile-slot">{profileSlot}</div>
    </header>
  );
}

export function NavRail({ views = VIEWS, current, onSelect }) {
  return (
    <nav className="rail" aria-label="Views">
      {views.map(({ id, label, icon: Icon }) => (
        <button
          key={id}
          type="button"
          className="nav-item"
          aria-label={label}
          aria-current={current === id ? "page" : undefined}
          onClick={() => onSelect(id)}
        >
          <Icon size={18} aria-hidden="true" />
          <span>{label}</span>
        </button>
      ))}
      <p className="rail-note">Everything stays on this computer unless you ask Claude.</p>
    </nav>
  );
}
