import { useCallback, useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open } from "@tauri-apps/plugin-dialog";

import {
  canChangeClaudeKey,
  canChangeHouseholdSettings,
  canErasePeople,
  canExportProfile,
  profileMayShareMemory,
} from "./roles.js";

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
      <h3>Your rights over what is kept</h3>
      <ul>
        <li>
          Under Your data, a profile&rsquo;s saved notes can be exported to a readable file and a portable file. An
          Adult can export their own; an Administrator can export any profile.
        </li>
        <li>
          An Administrator can erase a profile and every note saved for it. Erasing does not change notes shared by the
          household, the record that each note was agreed (which holds no names), or backup files already made. Anything
          already sent to Claude is subject to Anthropic&rsquo;s own terms.
        </li>
        <li>The activity log is deleted after the number of days an Administrator chooses; there is no setting to keep it for ever.</li>
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

export function ClaudeKeySection() {
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

// Which profiles' saved notes may go to Claude with a question (EBG-0110, the
// screen half). An Administrator sets it for any profile that can ask Claude at
// all; an Adult sees their own, switched off or on, with the reason it is not
// theirs to change; a Child or Guest never sees this section.
function MemorySharingSection({ role, profiles, activeProfile, onProfileUpdated }) {
  const [busyId, setBusyId] = useState(null);
  const [problem, setProblem] = useState(null);
  const mayChange = canChangeHouseholdSettings(role);
  const rows = mayChange ? profiles : profiles.filter((profile) => profile.id === activeProfile?.id);

  const change = (profile, enabled) => {
    setBusyId(profile.id);
    setProblem(null);
    invoke("set_profile_cloud_memory", { profileId: profile.id, enabled })
      .then((updated) => onProfileUpdated?.(updated))
      .catch((error) => setProblem(readable(error)))
      .finally(() => setBusyId(null));
  };

  return (
    <section className="settings-card memory-sharing" aria-labelledby="memory-sharing-heading">
      <h2 id="memory-sharing-heading">Notes and Claude</h2>
      <p>
        When this is on for a profile, that profile&rsquo;s saved notes go to Claude together with a question it asks,
        after the usual confirmation, which says so. When it is off, Claude never receives them. It is off unless an
        Administrator turns it on.
      </p>
      {!mayChange && (
        <p className="local-ai-note">Only an Administrator can change this, so it is shown here for you to read.</p>
      )}
      <ul className="sharing-list" aria-label="Profiles and note sharing">
        {rows.map((profile) => {
          const eligible = profileMayShareMemory(profile.role);
          const inputId = `share-${profile.id}`;
          return (
            <li key={profile.id} className="sharing-row" data-profile-id={profile.id}>
              <div>
                <label htmlFor={inputId}>
                  {profile.displayName} <span className="sharing-role">({profile.role})</span>
                </label>
                {!eligible && (
                  <p className="local-ai-note">This profile cannot ask Claude, so none of its notes are ever sent.</p>
                )}
              </div>
              <input
                id={inputId}
                type="checkbox"
                role="switch"
                checked={eligible && Boolean(profile.shareMemoryWithCloud)}
                disabled={!mayChange || !eligible || busyId === profile.id}
                onChange={(event) => change(profile, event.target.checked)}
              />
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

// How long the activity log is kept (R1). Never "for ever": there is always a
// limit, and a shorter one takes effect at once.
function RetentionSection() {
  const [settings, setSettings] = useState(null);
  const [statusError, setStatusError] = useState(null);
  const [problem, setProblem] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let cancelled = false;
    invoke("get_settings")
      .then((result) => {
        if (!cancelled) setSettings(result);
      })
      .catch((error) => {
        if (!cancelled) setStatusError(readable(error));
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const choose = (days) => {
    setBusy(true);
    setProblem(null);
    invoke("set_retention_days", { days })
      .then((result) => setSettings(result))
      .catch((error) => setProblem(readable(error)))
      .finally(() => setBusy(false));
  };

  const labels = { 30: "30 days", 90: "90 days", 365: "One year" };

  return (
    <section className="settings-card retention" aria-labelledby="retention-heading">
      <h2 id="retention-heading">Activity log</h2>
      <p>
        JARVIS keeps a log of what it did, such as a question being sent to Claude or a request being refused. It never
        holds what was said. Entries older than the limit you choose are deleted.
      </p>
      {statusError && (
        <p className="conversation-error" role="alert">
          The setting could not be read: {statusError}
        </p>
      )}
      {settings && (
        <fieldset className="retention-choices" disabled={busy}>
          <legend>Keep the activity log for</legend>
          {settings.allowedRetentionDays.map((days) => (
            <label key={days} className="retention-choice">
              <input
                type="radio"
                name="audit-retention"
                value={days}
                checked={settings.auditRetentionDays === days}
                onChange={() => choose(days)}
              />
              {labels[days] ?? `${days} days`}
            </label>
          ))}
        </fieldset>
      )}
      {settings?.lastPrune && (
        <p className="local-ai-note" role="status">
          Last tidy-up: {settings.lastPrune.removed} old entr{settings.lastPrune.removed === 1 ? "y" : "ies"} deleted.
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

// A profile's own data: a readable and a portable export, and erasure (WP5c).
// Erasure needs the profile's name typed; it is refused for the profile in use
// and for the last Administrator, and it says plainly what it does not touch.
function YourDataSection({ role, profiles, activeProfile, onProfileErased }) {
  const [busyId, setBusyId] = useState(null);
  const [message, setMessage] = useState(null);
  const [problem, setProblem] = useState(null);
  const [erasing, setErasing] = useState(null);
  const [typed, setTyped] = useState("");

  const mayErase = canErasePeople(role);
  const rows = profiles.filter((profile) => canExportProfile(role, activeProfile?.id, profile.id));
  const administrators = profiles.filter((profile) => profile.role === "Administrator").length;

  const exportData = async (profile) => {
    setProblem(null);
    setMessage(null);
    const folder = await open({ directory: true, multiple: false, title: "Choose a folder for the export" }).catch(
      () => null,
    );
    if (!folder) return;
    setBusyId(profile.id);
    invoke("export_profile", { profileId: profile.id, directory: folder })
      .then((result) => {
        setMessage(
          `Exported ${result.noteCount} saved note${result.noteCount === 1 ? "" : "s"} for ${profile.displayName} to ` +
            `${result.markdownPath} and ${result.jsonPath}.`,
        );
      })
      .catch((error) => setProblem(readable(error)))
      .finally(() => setBusyId(null));
  };

  const erase = (profile) => {
    setBusyId(profile.id);
    setProblem(null);
    setMessage(null);
    invoke("erase_profile", { profileId: profile.id, confirmName: typed })
      .then((result) => {
        setErasing(null);
        setTyped("");
        onProfileErased?.(profile.id);
        setMessage(
          `${profile.displayName} was erased. ${result.notesRemoved} saved note${result.notesRemoved === 1 ? "" : "s"} removed.`,
        );
      })
      .catch((error) => setProblem(readable(error)))
      .finally(() => setBusyId(null));
  };

  const whyNotErasable = (profile) => {
    if (profile.id === activeProfile?.id) return "You are using this profile. Switch to another first.";
    if (profile.role === "Administrator" && administrators <= 1) return "This is the last Administrator profile.";
    return null;
  };

  return (
    <section className="settings-card your-data" aria-labelledby="your-data-heading">
      <h2 id="your-data-heading">Your data</h2>
      <p>
        Export gives you a readable file and a portable file of what JARVIS keeps for a profile: its own saved notes and
        when each was agreed. It leaves out other profiles, notes shared by the household, and any key.
      </p>
      <ul className="data-list" aria-label="Profiles and their data">
        {rows.map((profile) => {
          const reason = mayErase ? whyNotErasable(profile) : null;
          const isErasing = erasing === profile.id;
          return (
            <li key={profile.id} className="data-row" data-profile-id={profile.id}>
              <div className="data-row-head">
                <span>
                  {profile.displayName} <span className="sharing-role">({profile.role})</span>
                </span>
                <span className="settings-actions">
                  <button
                    type="button"
                    onClick={() => exportData(profile)}
                    disabled={busyId === profile.id}
                    aria-label={`Export data for ${profile.displayName}`}
                  >
                    Export
                  </button>
                  {mayErase && (
                    <button
                      type="button"
                      onClick={() => {
                        setErasing(profile.id);
                        setTyped("");
                        setProblem(null);
                        setMessage(null);
                      }}
                      disabled={Boolean(reason) || busyId === profile.id}
                      aria-label={`Erase ${profile.displayName}`}
                    >
                      Erase...
                    </button>
                  )}
                </span>
              </div>
              {mayErase && reason && <p className="local-ai-note">{reason}</p>}
              {isErasing && (
                <form
                  className="erase-confirm"
                  aria-label={`Confirm erasing ${profile.displayName}`}
                  onSubmit={(event) => {
                    event.preventDefault();
                    if (typed.trim()) erase(profile);
                  }}
                >
                  <p>
                    This deletes the profile and every note saved for it. It cannot be undone. It does not change
                    notes shared by the household, the record that you agreed to each note (which holds no names), or
                    any backup file made earlier. Anything already sent to Claude is subject to Anthropic&rsquo;s own
                    terms.
                  </p>
                  <label htmlFor={`erase-${profile.id}`}>Type {profile.displayName} to confirm</label>
                  <input
                    id={`erase-${profile.id}`}
                    value={typed}
                    onChange={(event) => setTyped(event.target.value)}
                    autoComplete="off"
                    spellCheck={false}
                  />
                  <div className="settings-actions">
                    <button type="submit" disabled={busyId === profile.id || typed.trim() !== profile.displayName}>
                      Erase this profile and its notes
                    </button>
                    <button type="button" onClick={() => setErasing(null)}>
                      Cancel
                    </button>
                  </div>
                </form>
              )}
            </li>
          );
        })}
      </ul>
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

export function SettingsView({
  role,
  profiles = [],
  activeProfile = null,
  onProfileUpdated,
  onProfileErased,
  onRunSetup,
}) {
  return (
    <div className="settings-view">
      {canChangeClaudeKey(role) && <ClaudeKeySection />}
      <MemorySharingSection
        role={role}
        profiles={profiles}
        activeProfile={activeProfile}
        onProfileUpdated={onProfileUpdated}
      />
      {canChangeHouseholdSettings(role) && <RetentionSection />}
      <YourDataSection
        role={role}
        profiles={profiles}
        activeProfile={activeProfile}
        onProfileErased={onProfileErased}
      />
      {canChangeHouseholdSettings(role) && onRunSetup && (
        <section className="settings-card" aria-labelledby="run-setup-heading">
          <h2 id="run-setup-heading">Setup</h2>
          <p>Go through the first-run steps again: the AI model on this computer, and Claude.</p>
          <div className="settings-actions">
            <button type="button" onClick={onRunSetup}>
              Run setup again
            </button>
          </div>
        </section>
      )}
      <PrivacyNotice />
    </div>
  );
}
