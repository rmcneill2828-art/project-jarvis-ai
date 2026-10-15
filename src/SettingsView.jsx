import { useCallback, useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

import { canChangeClaudeKey } from "./roles.js";

// The Settings view (ESR-0061 WP5a, EIP-ESR0061-005 6.3 and 6.9). It holds what
// a household's Administrator decides: the Claude key, and the privacy notice
// everyone who can open the view may read. The backend enforces who may do
// what; this mirrors it.

// An error from the backend arrives as "ValueError: message"; the person sees
// the message.
const readable = (error) => String(error).replace(/^[A-Za-z]*Error:\s*/, "");

export function PrivacyNotice() {
  return (
    <section className="settings-card privacy-notice" aria-labelledby="privacy-heading">
      <h2 id="privacy-heading">Your privacy</h2>
      <h3>What stays on this computer</h3>
      <ul>
        <li>
          JARVIS answers on this computer first, with the AI model you chose here. What you say to it is not sent
          anywhere to be answered.
        </li>
        <li>
          Things JARVIS remembers are saved on this computer, and only after you approve each one. You can see them and
          remove them in Memory.
        </li>
        <li>
          The recent conversation is kept in memory only, one per profile, and is gone when JARVIS closes. The activity
          log records what happened, such as a question being sent to Claude, but never what was said.
        </li>
      </ul>
      <h3>What can leave it, and only when you say so</h3>
      <ul>
        <li>
          Claude is a service run by Anthropic over the internet. JARVIS asks it only when you confirm, one question at
          a time. Nothing is sent to Claude otherwise.
        </li>
        <li>
          When you confirm, Claude receives your question and your recent conversation with JARVIS. It also receives
          the notes JARVIS has saved for that profile only if sharing is turned on for that profile. It is off unless
          an Administrator turns it on.
        </li>
        <li>
          Asking Claude costs money. A monthly allowance is set, and what is left is shown before you confirm.
          Anthropic&rsquo;s own terms say how long it keeps what it receives; read them before you use Claude for
          anything private.
        </li>
        <li>Only an Administrator or an Adult profile can ask Claude. A Child or Guest profile cannot.</li>
      </ul>
      <h3>Downloads</h3>
      <ul>
        <li>
          Downloading an AI model fetches the model file from its library. It is a download; JARVIS does not send your
          conversations or notes with it.
        </li>
      </ul>
    </section>
  );
}

function ClaudeKeySection() {
  const [status, setStatus] = useState(null);
  const [statusError, setStatusError] = useState(null);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState(null);
  const [problem, setProblem] = useState(null);
  const [confirmingTest, setConfirmingTest] = useState(false);

  const refresh = useCallback(() => {
    return invoke("claude_key_status")
      .then((result) => {
        setStatus(result);
        setStatusError(null);
      })
      .catch((error) => {
        setStatus(null);
        setStatusError(readable(error));
      });
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const run = (action, onDone) => {
    setBusy(true);
    setProblem(null);
    setMessage(null);
    return action()
      .then((result) => onDone?.(result))
      .catch((error) => setProblem(readable(error)))
      .finally(() => setBusy(false));
  };

  const save = () =>
    run(
      () => invoke("set_claude_key", { key: draft.trim() }),
      (result) => {
        setDraft("");
        setStatus(result);
        setMessage("The key is saved on this computer.");
      },
    );

  const remove = () =>
    run(
      () => invoke("remove_claude_key"),
      (result) => {
        setStatus(result);
        setMessage(
          result.configured
            ? "The saved key was removed. The key from the ANTHROPIC_API_KEY setting is still in use."
            : "The key was removed. JARVIS will not ask Claude until another is saved.",
        );
      },
    );

  const test = () => {
    setConfirmingTest(false);
    return run(
      () => invoke("test_claude_key"),
      (result) => {
        if (result.ok) setMessage("Claude accepted the key.");
        else if (result.failure === "no_key") setProblem("There is no key to test.");
        else setProblem("Claude did not accept a test request. Check the key, then try again.");
      },
    );
  };

  const fromEnvironment = status?.source === "environment";
  const storeMissing = status && !status.storeAvailable;

  return (
    <section className="settings-card claude-key" aria-labelledby="claude-key-heading">
      <h2 id="claude-key-heading">Claude</h2>
      <p>
        With a Claude key, JARVIS can offer to ask Claude when the model on this computer cannot answer, or when you
        ask it to. Each question is confirmed by the person asking.
      </p>
      {statusError && (
        <p className="conversation-error" role="alert">
          The key&rsquo;s status could not be read: {statusError}
        </p>
      )}
      {status && (
        <p role="status" className="claude-key-status" data-key-source={status.source}>
          {status.configured
            ? fromEnvironment
              ? "A key is set by the ANTHROPIC_API_KEY setting, which overrides this screen."
              : "A key is saved on this computer."
            : "No key is set. JARVIS answers on this computer only."}
        </p>
      )}
      {storeMissing && (
        <p className="local-ai-note">
          This computer has no secure place to keep a key. Set the ANTHROPIC_API_KEY setting instead, then restart
          JARVIS.
        </p>
      )}
      {status && status.storeAvailable && !fromEnvironment && (
        <form
          className="claude-key-form"
          onSubmit={(event) => {
            event.preventDefault();
            if (draft.trim()) save();
          }}
        >
          <label htmlFor="claude-key-input">Claude API key</label>
          <input
            id="claude-key-input"
            type="password"
            autoComplete="off"
            spellCheck={false}
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            placeholder="sk-ant-..."
            disabled={busy}
          />
          <p className="local-ai-note">
            The key is kept in this computer&rsquo;s credential store. It is never shown again, and JARVIS cannot
            read it back to you.
          </p>
          <div className="settings-actions">
            <button type="submit" disabled={busy || draft.trim().length === 0}>
              Save key
            </button>
          </div>
        </form>
      )}
      {status?.configured && (
        <div className="settings-actions">
          {status.source === "store" && (
            <button type="button" onClick={remove} disabled={busy}>
              Remove key
            </button>
          )}
          {!confirmingTest ? (
            <button type="button" onClick={() => setConfirmingTest(true)} disabled={busy}>
              Test this key
            </button>
          ) : (
            <span className="settings-confirm" role="group" aria-label="Confirm key test">
              <span>This sends one tiny question to Claude and costs a fraction of a cent.</span>
              <button type="button" onClick={test} disabled={busy}>
                Send the test
              </button>
              <button type="button" onClick={() => setConfirmingTest(false)}>
                Cancel
              </button>
            </span>
          )}
        </div>
      )}
      {message && (
        <p role="status" className="panel-status-message">
          {message}
        </p>
      )}
      {problem && (
        <p className="conversation-error" role="alert">
          {problem}
        </p>
      )}
    </section>
  );
}

export function SettingsView({ role }) {
  return (
    <div className="settings-view">
      {canChangeClaudeKey(role) && <ClaudeKeySection />}
      <PrivacyNotice />
    </div>
  );
}
