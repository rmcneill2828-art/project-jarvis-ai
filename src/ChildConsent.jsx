// Claude for a Child (ESR-0061 WP6c, EIP-ESR0061-006 C1, C2, 6.6). Off by
// default. An Administrator allows it per child in Settings; the child then
// says they understand, once, before it works. The backend checks both on every
// offer and every send; these screens only ask and explain.
//
// A child and a parent read these texts: wording approved by the Programme
// Sponsor, 7 November 2026 (EIP-ESR0061-006 Section 10E).

import { useCallback, useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

const readable = (error) =>
  String(error).replace(/^(?:[A-Za-z]*Error:\s*)+/, "");

export const PARENT_EXPLANATION =
  "This is off unless you turn it on, for each child separately. When it is on, the child can choose to " +
  "send a question to Claude, a service run by Anthropic, and confirms each time. Their question and " +
  "their recent conversation with JARVIS (the last few messages, up to six) are sent, and that " +
  "conversation might include their name. Their saved notes are not sent themselves, but something " +
  "JARVIS said using them may be part of that conversation. Anthropic handles what is sent under its " +
  "own privacy terms. The safety checker checks each question before it goes and each answer before it " +
  "is shown. It only starts working once the child has said they understand, and you can turn it off at " +
  "any time: it stops at once.";

export const CHILD_ACKNOWLEDGEMENT =
  "A grown-up has said you can ask Claude. Claude is an AI made by a company called Anthropic. It is " +
  "not a person, and it can make mistakes. When you choose to ask Claude, your question and your last " +
  "few messages with JARVIS are sent to Anthropic over the internet. They might include your name, or " +
  "something JARVIS said using your notes. Your notes themselves are never sent. If anything Claude " +
  "says worries you, tell a grown-up.";

function statusText(status, name) {
  if (!status?.recorded) return "Off.";
  if (!status.acknowledged)
    return `Allowed by ${status.recordedBy ?? "an Administrator"}. Waiting for ${name} to say they understand.`;
  if (!status.allowed)
    return "Off: the Administrator who allowed it is no longer an Administrator here.";
  return `On. Allowed by ${status.recordedBy ?? "an Administrator"}; ${name} has said they understand.`;
}

// Settings, Administrator only: one row per Child profile.
export function ChildClaudeSection({ profiles = [] }) {
  const children = profiles.filter((profile) => profile.role === "Child");
  const [statuses, setStatuses] = useState({});
  const [busyId, setBusyId] = useState(null);
  const [problem, setProblem] = useState(null);
  const childIds = children.map((child) => child.id).join(",");

  useEffect(() => {
    let cancelled = false;
    for (const id of childIds ? childIds.split(",") : []) {
      invoke("consent_status", { profileId: id })
        .then((status) => {
          if (!cancelled)
            setStatuses((current) => ({ ...current, [id]: status }));
        })
        .catch(() => {});
    }
    return () => {
      cancelled = true;
    };
  }, [childIds]);

  if (children.length === 0) return null;

  const change = (child, allow) => {
    setBusyId(child.id);
    setProblem(null);
    invoke(allow ? "record_consent" : "revoke_consent", { profileId: child.id })
      .then((status) =>
        setStatuses((current) => ({ ...current, [child.id]: status })),
      )
      .catch((error) => setProblem(readable(error)))
      .finally(() => setBusyId(null));
  };

  return (
    <section
      className="settings-card child-claude"
      aria-labelledby="child-claude-heading"
    >
      <h2 id="child-claude-heading">Claude for a child</h2>
      <p>{PARENT_EXPLANATION}</p>
      <ul
        className="sharing-list consent-list"
        aria-label="Children and Claude"
      >
        {children.map((child) => {
          const status = statuses[child.id];
          const on = Boolean(status?.recorded);
          return (
            <li
              key={child.id}
              className="consent-row"
              data-profile-id={child.id}
            >
              <div>
                <strong>{child.displayName}</strong>
                <p
                  className="local-ai-note"
                  data-testid={`consent-status-${child.id}`}
                >
                  {status ? statusText(status, child.displayName) : "Checking…"}
                </p>
              </div>
              <button
                type="button"
                onClick={() => change(child, !on)}
                disabled={!status || busyId === child.id}
              >
                {on
                  ? `Turn off for ${child.displayName}`
                  : `Allow ${child.displayName} to ask Claude`}
              </button>
            </li>
          );
        })}
      </ul>
      {problem && (
        <p className="conversation-error" role="alert">
          {problem}
        </p>
      )}
    </section>
  );
}

// The conversation screen, a Child profile only: shown once a grown-up has
// allowed Claude and until the child says they understand.
export function ChildAcknowledgementCard({ profileId, onAcknowledged }) {
  const [status, setStatus] = useState(null);
  const [busy, setBusy] = useState(false);
  const [problem, setProblem] = useState(null);

  const load = useCallback(() => {
    invoke("consent_status")
      .then(setStatus)
      .catch(() => setStatus(null));
  }, []);

  useEffect(() => {
    setStatus(null);
    load();
  }, [profileId, load]);

  if (!status?.recorded || status.acknowledged) return null;

  const acknowledge = () => {
    setBusy(true);
    setProblem(null);
    invoke("acknowledge_consent")
      .then((updated) => {
        setStatus(updated);
        onAcknowledged?.();
      })
      .catch((error) => setProblem(readable(error)))
      .finally(() => setBusy(false));
  };

  return (
    <section
      className="settings-card child-acknowledgement"
      aria-labelledby="child-ack-heading"
    >
      <h2 id="child-ack-heading">You can ask Claude</h2>
      <p>{CHILD_ACKNOWLEDGEMENT}</p>
      <div className="settings-actions">
        <button type="button" onClick={acknowledge} disabled={busy}>
          I understand
        </button>
      </div>
      {problem && (
        <p className="conversation-error" role="alert">
          {problem}
        </p>
      )}
    </section>
  );
}
