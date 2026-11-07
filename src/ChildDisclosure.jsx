// The Child's first-use explanation (ESR-0061 WP6d, EIP-ESR0061-006 D1, 6.7).
// Shown in place of the conversation the first time a Child profile is used,
// until the child says they understand; recorded by the backend. The
// permanent "You are talking to JARVIS, an AI" line stays regardless.
//
// A child reads this: wording approved by the Programme Sponsor, 7 November
// 2026 (EIP-ESR0061-006 Section 10F).

import { useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

const readable = (error) =>
  String(error).replace(/^(?:[A-Za-z]*Error:\s*)+/, "");

export const CHILD_DISCLOSURE_HEADING = "Before you start";

export const CHILD_DISCLOSURE = [
  "JARVIS is an AI, not a person, and it can make mistakes.",
  "It runs on this computer. What you say to it stays here, unless a grown-up has allowed you to ask " +
    "Claude and you choose to.",
  "JARVIS forgets your conversation when it is closed. It only keeps notes that a grown-up has agreed to " +
    "save for you, and a grown-up can get a copy of them.",
  "A safety check looks at what you say and at what JARVIS answers. If it stops something, a grown-up can " +
    "see that it happened, on which day, and what kind of thing it was, but not your words.",
  "The safety check is Llama Guard 3, made by Meta and built with Llama.",
  "If anything worries you, tell a grown-up.",
];

// Renders `children` (the conversation) unless this Child profile must first
// see the explanation. If the status cannot be read, the conversation is
// shown: this page discloses, it does not protect (moderation does).
export function ChildFirstUse({ profileId, children }) {
  const [status, setStatus] = useState(null);
  const [busy, setBusy] = useState(false);
  const [problem, setProblem] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setStatus(null);
    invoke("disclosure_status")
      .then((value) => {
        if (!cancelled) setStatus(value);
      })
      .catch(() => {
        if (!cancelled) setStatus({ required: false });
      });
    return () => {
      cancelled = true;
    };
  }, [profileId]);

  if (status === null) return null;
  if (!status.required) return children;

  const acknowledge = () => {
    setBusy(true);
    setProblem(null);
    invoke("acknowledge_disclosure")
      .then(setStatus)
      .catch((error) => setProblem(readable(error)))
      .finally(() => setBusy(false));
  };

  return (
    <section
      className="settings-card child-disclosure"
      aria-labelledby="child-disclosure-heading"
    >
      <h2 id="child-disclosure-heading">{CHILD_DISCLOSURE_HEADING}</h2>
      {CHILD_DISCLOSURE.map((line) => (
        <p key={line}>{line}</p>
      ))}
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
