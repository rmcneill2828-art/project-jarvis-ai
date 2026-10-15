import { useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

import { LocalAiPanel } from "./LocalAiPanel.jsx";
import { ClaudeKeySection, PrivacyNotice } from "./SettingsView.jsx";

// First-run setup (ESR-0061 WP5d, EIP-ESR0061-005 6.7, decision F1).
//
// Four steps: (1) the first profile, which is an Administrator and says so;
// (2) the local AI model, using the existing panel; (3) Claude, optional, with
// the privacy notice; (4) what is ready and what is still missing.
//
// Nothing here is remembered as "done". Which steps are finished is read from
// the real state (a profile exists, a model is installed, a key is set), so the
// flow cannot be wrong after a restore, and it can be opened again from
// Settings. Every step but the first can be skipped, and the last never refuses
// to finish: a person can never be trapped by a missing Ollama or a failed
// download.

const STEPS = ["Your profile", "AI on this computer", "Claude", "Ready"];

function StepList({ current }) {
  return (
    <ol className="firstrun-steps" aria-label="Setup steps">
      {STEPS.map((label, index) => (
        <li
          key={label}
          aria-current={index === current ? "step" : undefined}
          className={index === current ? "current" : index < current ? "done" : ""}
        >
          <span className="firstrun-step-number" aria-hidden="true">
            {index + 1}
          </span>
          {label}
        </li>
      ))}
    </ol>
  );
}

function ProfileStep({ onCreateProfile, profileError }) {
  const [name, setName] = useState("");
  return (
    <section className="firstrun-card" aria-labelledby="firstrun-profile-heading">
      <h2 id="firstrun-profile-heading">Who is setting JARVIS up?</h2>
      <p>
        This first profile is an <strong>Administrator</strong>: the person who manages JARVIS for the household. They
        decide who else has a profile, whether Claude can be used, and what is kept. Other people get their own
        profiles later.
      </p>
      <form
        className="firstrun-form"
        onSubmit={(event) => {
          event.preventDefault();
          const trimmed = name.trim();
          if (trimmed) onCreateProfile(trimmed, "Administrator");
        }}
      >
        <label htmlFor="firstrun-name">Your name</label>
        <input
          id="firstrun-name"
          value={name}
          onChange={(event) => setName(event.target.value)}
          placeholder="Your name"
          autoComplete="off"
        />
        <div className="settings-actions">
          <button type="submit" disabled={name.trim().length === 0}>
            Create profile
          </button>
        </div>
      </form>
      {profileError && (
        <p className="profile-error" role="alert">
          {profileError}
        </p>
      )}
    </section>
  );
}

function ReadyStep({ onFinish }) {
  const [state, setState] = useState(null);

  useEffect(() => {
    let cancelled = false;
    Promise.allSettled([invoke("ollama_status"), invoke("claude_key_status")]).then(([ollama, claude]) => {
      if (cancelled) return;
      setState({
        model:
          ollama.status === "fulfilled"
            ? Boolean(ollama.value.running && ollama.value.activeModelInstalled)
            : null,
        modelName: ollama.status === "fulfilled" ? ollama.value.activeModel : null,
        claude: claude.status === "fulfilled" ? Boolean(claude.value.configured) : null,
      });
    });
    return () => {
      cancelled = true;
    };
  }, []);

  const line = (ready, readyText, missingText, unknownText) =>
    ready === null ? unknownText : ready ? readyText : missingText;

  return (
    <section className="firstrun-card" aria-labelledby="firstrun-ready-heading">
      <h2 id="firstrun-ready-heading">{state ? "Here is where things stand" : "Checking..."}</h2>
      {state && (
        <ul className="firstrun-summary" aria-label="What is ready">
          <li data-item="profile" data-ready="true">
            <strong>Your profile:</strong> ready.
          </li>
          <li data-item="model" data-ready={String(state.model === true)}>
            <strong>AI on this computer:</strong>{" "}
            {line(
              state.model,
              `ready (${state.modelName}).`,
              "not ready yet. JARVIS cannot answer until a model is installed. You can finish this any time under AI models.",
              "could not be checked. You can look under AI models.",
            )}
          </li>
          <li data-item="claude" data-ready={String(state.claude === true)}>
            <strong>Claude:</strong>{" "}
            {line(
              state.claude,
              "a key is saved. JARVIS will offer to ask Claude only when you confirm.",
              "not set up. JARVIS answers on this computer only. You can add a key any time under Settings.",
              "could not be checked. You can look under Settings.",
            )}
          </li>
        </ul>
      )}
      <div className="settings-actions">
        <button type="button" onClick={onFinish}>
          Start using JARVIS
        </button>
      </div>
    </section>
  );
}

export function FirstRun({
  activeProfile,
  profileError,
  onCreateProfile,
  onFinish,
  pullProgress,
  pullFinished,
  useWhenDoneRef,
  onPullFinishedHandled,
}) {
  // Starts at the profile step when there is none, else at the next step; moved
  // forward by the buttons and by the profile being created.
  const [step, setStep] = useState(activeProfile ? 1 : 0);

  useEffect(() => {
    if (activeProfile) setStep((current) => (current === 0 ? 1 : current));
  }, [activeProfile]);

  return (
    <section className="view firstrun" aria-label="Set up JARVIS">
      <div className="view-scroll" tabIndex={0}>
        <h1 className="view-heading">Set up JARVIS</h1>
        <StepList current={step} />

        {step === 0 && <ProfileStep onCreateProfile={onCreateProfile} profileError={profileError} />}

        {step === 1 && (
          <div>
            <p className="view-lede">
              JARVIS answers on this computer, with an AI model that runs here. Check it below and install one if you
              can. You can do this later.
            </p>
            <LocalAiPanel
              activeProfile={activeProfile}
              pullProgress={pullProgress}
              pullFinished={pullFinished}
              useWhenDoneRef={useWhenDoneRef}
              onPullFinishedHandled={onPullFinishedHandled}
            />
            <div className="settings-actions">
              <button type="button" onClick={() => setStep(2)}>
                Continue
              </button>
              <button type="button" onClick={() => setStep(2)}>
                Do this later
              </button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div>
            <p className="view-lede">
              Claude is optional. Without it JARVIS still works, on this computer. Read what is shared before you
              decide.
            </p>
            <PrivacyNotice />
            <ClaudeKeySection />
            <div className="settings-actions">
              <button type="button" onClick={() => setStep(3)}>
                Continue
              </button>
              <button type="button" onClick={() => setStep(3)}>
                Skip for now
              </button>
            </div>
          </div>
        )}

        {step === 3 && <ReadyStep onFinish={onFinish} />}
      </div>
    </section>
  );
}
