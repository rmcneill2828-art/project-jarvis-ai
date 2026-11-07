// Settings, Administrator only: Children and safety (ESR-0061 WP6d,
// EIP-ESR0061-006 6.7). The safety checker's state and its "Built with Llama"
// attribution; Claude for each child (WP6c); and how many turns the safety
// check stopped, per Child and Guest profile, by day and kind. Never any of
// the words: none are kept.
//
// A parent reads these (the category names and explanations): wording
// approved by the Programme Sponsor, 7 November 2026 (EIP-ESR0061-006 10F).

import { useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { ChildClaudeSection } from "./ChildConsent.jsx";

// Plain names for the stored labels (jarvis/interfaces/moderation.py).
export const CATEGORY_NAMES = {
  violent_crimes: "Violence or violent crime",
  non_violent_crimes: "Other crime",
  sex_related_crimes: "Sex-related crime",
  child_sexual_exploitation: "Sexual exploitation of children",
  defamation: "Saying untrue, harmful things about a real person",
  specialized_advice: "Specialist advice (medical, legal or financial)",
  privacy: "Private information about someone",
  intellectual_property: "Copying someone else's work",
  indiscriminate_weapons: "Weapons that can harm many people",
  hate: "Hate",
  self_harm: "Self-harm or suicide",
  sexual_content: "Sexual content",
  elections: "Elections",
  code_interpreter_abuse: "Misuse of computer code",
  unspecified: "Unsafe (kind not given)",
  moderation_unavailable: "Not checked: the safety checker was not available",
};

export const DIRECTION_NAMES = {
  input: "their message",
  output: "JARVIS's reply",
};

export const SAFETY_EXPLANATION =
  "A Child's or Guest's conversation is checked by a safety checker on this computer: each message " +
  "before JARVIS sees it, and each reply before it is shown. If it finds something unsafe, or cannot " +
  "check, the conversation shows a fixed reply instead. Below is how often that happened, and what kind " +
  "of thing it was. The words themselves are never kept, so they cannot be shown.";

export const SAFETY_LIMITS =
  "The safety checker can miss things, and can stop things that were fine. It is a help, not a guarantee.";

export const LLAMA_ATTRIBUTION =
  "The safety checker is Llama Guard 3 by Meta, built with Llama. It is used under the Llama 3.2 " +
  "Community License (llama.com/llama3_2/license) and Meta's Acceptable Use Policy " +
  "(llama.com/llama3_2/use-policy).";

function checkerText(ollama) {
  if (!ollama) return "Checking the safety checker…";
  if (!ollama.running)
    return "The safety checker is not running, because Ollama is not running. Child and Guest conversations are refused until it is.";
  if (!ollama.classifier?.installed)
    return "The safety checker is not installed. Child and Guest conversations are refused until it is. Install it under Local AI.";
  return "The safety checker is installed and ready.";
}

function SafetyEvents({ entry }) {
  if (entry.events.length === 0)
    return <p className="local-ai-note">Nothing has been stopped.</p>;
  return (
    <table className="safety-events">
      <caption className="visually-hidden">
        What the safety check stopped for {entry.displayName}
      </caption>
      <thead>
        <tr>
          <th scope="col">Day</th>
          <th scope="col">Kind</th>
          <th scope="col">In</th>
          <th scope="col">Times</th>
        </tr>
      </thead>
      <tbody>
        {entry.events.map((event) => (
          <tr key={`${event.day}-${event.category}-${event.direction}`}>
            <td>{event.day}</td>
            <td>{CATEGORY_NAMES[event.category] ?? event.category}</td>
            <td>{DIRECTION_NAMES[event.direction] ?? event.direction}</td>
            <td>{event.count}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export function ChildrenAndSafety({ profiles = [] }) {
  const [ollama, setOllama] = useState(null);
  const [summary, setSummary] = useState(null);
  const [problem, setProblem] = useState(null);

  useEffect(() => {
    let cancelled = false;
    invoke("ollama_status")
      .then((value) => {
        if (!cancelled) setOllama(value);
      })
      .catch(() => {
        if (!cancelled) setOllama({ running: false });
      });
    invoke("safety_summary")
      .then((value) => {
        if (!cancelled) setSummary(value?.profiles ?? []);
      })
      .catch(() => {
        if (!cancelled)
          setProblem("What the safety check stopped could not be read.");
      });
    return () => {
      cancelled = true;
    };
  }, [profiles.length]);

  return (
    <section
      className="settings-card children-safety"
      aria-labelledby="children-safety-heading"
    >
      <h2 id="children-safety-heading">Children and safety</h2>
      <p>{SAFETY_EXPLANATION}</p>
      <p className="local-ai-note" data-testid="safety-checker-state">
        {checkerText(ollama)}
      </p>
      <p className="local-ai-note">{SAFETY_LIMITS}</p>
      <p className="local-ai-note" data-testid="llama-attribution">
        {LLAMA_ATTRIBUTION}
      </p>
      <ChildClaudeSection profiles={profiles} />
      <div className="safety-summary">
        <h3>What the safety check stopped</h3>
        {problem && (
          <p className="conversation-error" role="alert">
            {problem}
          </p>
        )}
        {summary !== null && summary.length === 0 && (
          <p className="local-ai-note">There are no Child or Guest profiles.</p>
        )}
        {summary?.map((entry) => (
          <div
            key={entry.profileId ?? "nobody"}
            className="safety-profile"
            data-testid={`safety-${entry.profileId ?? "nobody"}`}
          >
            <h4>
              {entry.profileId === null
                ? "Nobody signed in (treated as a Guest)"
                : `${entry.displayName} (${entry.role})`}
            </h4>
            <SafetyEvents entry={entry} />
          </div>
        ))}
      </div>
    </section>
  );
}
