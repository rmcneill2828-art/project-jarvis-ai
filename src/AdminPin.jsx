// The household's Administrator PIN on screen (ESR-0061 WP6a, EIP-ESR0061-006
// Section 6.3). The backend decides everything: whether a switch needs the PIN,
// whether a PIN is right, and the lock-out. These components only ask, show the
// answer, and never keep a PIN beyond the form it was typed into.

import { useEffect, useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

// The backend's reply reads "PermissionError: ..."; an Error wrapping it adds
// another "Error: " in front. Neither prefix is for the person.
const readable = (error) => String(error).replace(/^(?:[A-Za-z]*Error:\s*)+/, "");
const PIN_SHAPE = /^[0-9]{6,12}$/;
const FOCUSABLE =
  "button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex='-1'])";

export const NO_PIN_WARNING =
  "No Administrator PIN is set, so safety features are not enforced: anyone can switch to any profile, including the Administrator.";

function PinInput({ id, label, value, onChange, disabled, inputRef, autoComplete = "off" }) {
  return (
    <>
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        ref={inputRef}
        type="password"
        inputMode="numeric"
        pattern="[0-9]*"
        maxLength={12}
        autoComplete={autoComplete}
        spellCheck={false}
        value={value}
        onChange={(event) => onChange(event.target.value.replace(/[^0-9]/g, ""))}
        disabled={disabled}
      />
    </>
  );
}

// Counts a lock-out down to zero, so the screen says how long is left.
function useCountdown(seconds) {
  const [left, setLeft] = useState(seconds);
  useEffect(() => {
    setLeft(seconds);
    if (!seconds) return undefined;
    const started = Date.now();
    const timer = setInterval(() => {
      const remaining = Math.max(0, seconds - Math.floor((Date.now() - started) / 1000));
      setLeft(remaining);
      if (remaining === 0) clearInterval(timer);
    }, 1000);
    return () => clearInterval(timer);
  }, [seconds]);
  return left;
}

// Asked when switching to a profile the elevation rule guards. A modal dialog
// like the Claude one (WP4d): focus moves in, Tab stays inside, Escape cancels,
// and focus returns to what opened it.
export function PinDialog({ target, lockedForSeconds = 0, returnFocusRef, onSignedIn, onCancel }) {
  const [pin, setPin] = useState("");
  const [busy, setBusy] = useState(false);
  const [problem, setProblem] = useState(null);
  const [lock, setLock] = useState(lockedForSeconds);
  const left = useCountdown(lock);
  const dialogRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    const previous = document.activeElement;
    inputRef.current?.focus();
    return () => {
      const opener = returnFocusRef?.current;
      const destination = opener && opener.isConnected ? opener : previous;
      if (destination && destination.isConnected && typeof destination.focus === "function") destination.focus();
    };
  }, []);

  useEffect(() => {
    if (left === 0 && lock) setProblem(null);
  }, [left, lock]);

  const submit = () => {
    const typed = pin;
    setPin("");
    setBusy(true);
    setProblem(null);
    invoke("select_profile", { profileId: target.id, pin: typed })
      .then((selected) => onSignedIn(selected))
      .catch((error) => {
        const text = readable(error);
        setProblem(text);
        const wait = /try again in (\d+) seconds/i.exec(text);
        if (wait) setLock(Number(wait[1]));
        setBusy(false);
        inputRef.current?.focus();
      });
  };

  const handleKeyDown = (event) => {
    if (event.key === "Escape") {
      if (!busy) {
        event.stopPropagation();
        onCancel();
      }
      return;
    }
    if (event.key !== "Tab") return;
    const items = [...(dialogRef.current?.querySelectorAll(FOCUSABLE) ?? [])];
    event.preventDefault();
    if (items.length === 0) {
      dialogRef.current?.focus();
      return;
    }
    const at = items.indexOf(document.activeElement);
    const step = event.shiftKey ? -1 : 1;
    const next = at === -1 ? (event.shiftKey ? items.length - 1 : 0) : (at + step + items.length) % items.length;
    items[next].focus();
  };

  const locked = left > 0;
  return (
    <div className="escalation-backdrop" onKeyDown={handleKeyDown}>
      <div
        ref={dialogRef}
        tabIndex={-1}
        className="escalation-dialog pin-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="pin-dialog-title"
        aria-describedby="pin-dialog-details"
      >
        <h2 id="pin-dialog-title">Administrator PIN needed</h2>
        <p id="pin-dialog-details">
          Switching to <strong>{target.displayName}</strong> ({target.role}) needs the household&rsquo;s Administrator
          PIN.
        </p>
        <form
          className="pin-form"
          onSubmit={(event) => {
            event.preventDefault();
            if (!busy && !locked && PIN_SHAPE.test(pin)) submit();
          }}
        >
          <PinInput id="pin-dialog-input" label="PIN" value={pin} onChange={setPin} disabled={busy} inputRef={inputRef} />
          {locked && (
            <p className="conversation-error" role="alert" data-testid="pin-locked">
              Too many wrong tries. Try again in {left} seconds.
            </p>
          )}
          {problem && !locked && (
            <p className="conversation-error" role="alert">
              {problem}
            </p>
          )}
          <div className="escalation-actions">
            <button type="button" onClick={onCancel} disabled={busy}>
              Cancel
            </button>
            <button type="submit" className="escalation-confirm" disabled={busy || locked || !PIN_SHAPE.test(pin)}>
              {busy ? "Checking…" : "Switch"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function when(at) {
  if (!at) return "an unknown time";
  const date = new Date(at);
  return Number.isNaN(date.getTime()) ? "an unknown time" : date.toLocaleString();
}

export function noticeText(notice) {
  switch (notice.kind) {
    case "pinSet":
      return `An Administrator PIN was set on ${when(notice.at)} from the ${notice.byProfile ?? "unknown"} profile.`;
    case "pinReset":
      return `The Administrator PIN was reset from the command line on ${when(notice.at)}. Set a new PIN under Settings.`;
    case "wrongTries":
      return `${notice.count} wrong PIN ${notice.count === 1 ? "try" : "tries"} since an Administrator last signed in, the last at ${when(notice.at)}.`;
    default:
      return null;
  }
}

// Shown once to the Administrator who has just signed in (P1, P3, P5): the
// backend hands these over once and then forgets them.
export function PinNotices({ notices, onDismiss }) {
  if (!notices || notices.length === 0) return null;
  const lines = notices.map(noticeText).filter(Boolean);
  if (lines.length === 0) return null;
  return (
    <section className="settings-card pin-notices" aria-labelledby="pin-notices-heading" role="region">
      <h2 id="pin-notices-heading">Since an Administrator last signed in</h2>
      <ul>
        {lines.map((line) => (
          <li key={line}>{line}</li>
        ))}
      </ul>
      <div className="settings-actions">
        <button type="button" onClick={onDismiss}>
          Dismiss
        </button>
      </div>
    </section>
  );
}

// Choosing a PIN: typed twice, 6 to 12 digits.
export function SetPinForm({ onSaved, submitLabel = "Set PIN" }) {
  const [pin, setPin] = useState("");
  const [again, setAgain] = useState("");
  const [busy, setBusy] = useState(false);
  const [problem, setProblem] = useState(null);

  const mismatch = again.length > 0 && pin !== again;
  const ready = PIN_SHAPE.test(pin) && pin === again;

  return (
    <form
      className="pin-form"
      aria-label="Set the Administrator PIN"
      onSubmit={(event) => {
        event.preventDefault();
        if (!ready || busy) return;
        const typed = pin;
        setPin("");
        setAgain("");
        setBusy(true);
        setProblem(null);
        invoke("set_pin", { pin: typed })
          .then((status) => onSaved?.(status))
          .catch((error) => setProblem(readable(error)))
          .finally(() => setBusy(false));
      }}
    >
      <PinInput id="pin-new" label="New PIN (6 to 12 digits)" value={pin} onChange={setPin} disabled={busy} autoComplete="new-password" />
      <PinInput id="pin-new-again" label="The same PIN again" value={again} onChange={setAgain} disabled={busy} autoComplete="new-password" />
      {mismatch && <p className="local-ai-note">The two PINs are not the same.</p>}
      {problem && (
        <p className="conversation-error" role="alert">
          {problem}
        </p>
      )}
      <div className="settings-actions">
        <button type="submit" disabled={busy || !ready}>
          {submitLabel}
        </button>
      </div>
    </form>
  );
}

function ChangePinForm({ onChanged }) {
  const [current, setCurrent] = useState("");
  const [pin, setPin] = useState("");
  const [again, setAgain] = useState("");
  const [busy, setBusy] = useState(false);
  const [problem, setProblem] = useState(null);

  const ready = PIN_SHAPE.test(current) && PIN_SHAPE.test(pin) && pin === again;

  return (
    <form
      className="pin-form"
      aria-label="Change the Administrator PIN"
      onSubmit={(event) => {
        event.preventDefault();
        if (!ready || busy) return;
        const typed = { currentPin: current, newPin: pin };
        setCurrent("");
        setPin("");
        setAgain("");
        setBusy(true);
        setProblem(null);
        invoke("change_pin", typed)
          .then((status) => onChanged?.(status))
          .catch((error) => setProblem(readable(error)))
          .finally(() => setBusy(false));
      }}
    >
      <PinInput id="pin-current" label="Current PIN" value={current} onChange={setCurrent} disabled={busy} />
      <PinInput id="pin-change-new" label="New PIN (6 to 12 digits)" value={pin} onChange={setPin} disabled={busy} autoComplete="new-password" />
      <PinInput id="pin-change-again" label="The same new PIN again" value={again} onChange={setAgain} disabled={busy} autoComplete="new-password" />
      {again.length > 0 && pin !== again && <p className="local-ai-note">The two new PINs are not the same.</p>}
      {problem && (
        <p className="conversation-error" role="alert">
          {problem}
        </p>
      )}
      <div className="settings-actions">
        <button type="submit" disabled={busy || !ready}>
          Change PIN
        </button>
      </div>
    </form>
  );
}

// What the PIN is for and what it is not, in the same words wherever it is set.
export function PinExplanation() {
  return (
    <p>
      Switching to an Administrator profile needs the PIN, and so does leaving a Child or Guest profile for an Adult
      one. Only an Administrator can add profiles, once a PIN is set. It is a lock inside JARVIS, not on the
      computer: someone who can open this computer&rsquo;s files can still reach JARVIS&rsquo;s data. If it is
      forgotten, it can be reset from the command line on this computer, and the next Administrator to sign in is told.
    </p>
  );
}

// Settings (Administrator only): set a first PIN, or change it.
export function PinSection({ onStatusChanged }) {
  const [status, setStatus] = useState(null);
  const [problem, setProblem] = useState(null);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    let cancelled = false;
    invoke("pin_status")
      .then((result) => {
        if (!cancelled) setStatus(result);
      })
      .catch((error) => {
        if (!cancelled) setProblem(readable(error));
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const updated = (result, text) => {
    setStatus(result);
    setMessage(text);
    onStatusChanged?.(result);
  };

  return (
    <section className="settings-card admin-pin" aria-labelledby="admin-pin-heading">
      <h2 id="admin-pin-heading">Administrator PIN</h2>
      <PinExplanation />
      {problem && (
        <p className="conversation-error" role="alert">
          The PIN&rsquo;s status could not be read: {problem}
        </p>
      )}
      {status && !status.set && (
        <>
          <p className="escalation-warning" role="alert" data-testid="no-pin-warning">
            {NO_PIN_WARNING}
          </p>
          <SetPinForm onSaved={(result) => updated(result, "The PIN is set.")} />
        </>
      )}
      {status?.set && (
        <>
          <p role="status" className="claude-key-status">
            A PIN is set.
            {status.locked ? ` It is locked for ${status.lockedForSeconds} seconds after too many wrong tries.` : ""}
          </p>
          <ChangePinForm onChanged={(result) => updated(result, "The PIN was changed.")} />
        </>
      )}
      {message && (
        <p role="status" className="panel-status-message">
          {message}
        </p>
      )}
    </section>
  );
}
