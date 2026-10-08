// Smallest honest UI for asking Claude (ESR-0061 WP3b, EIP-ESR0061-003 6.7).
// Functional and tested, not designed: WP4 restyles it. Nothing here sends
// anything - the dialog states what would be sent, and only its confirm button
// does, using the one-time token the backend issued for this exact message.

const OFFER_TEXT = {
  local_unavailable: "The model on this computer could not answer.",
  research_cue: "Claude may give a more thorough answer to this.",
  requested: "You asked to send this to Claude.",
};

export function ClaudeBadge() {
  return (
    <span className="claude-badge" title="This answer came from Claude, over the internet">
      Claude
    </span>
  );
}

export function EscalationBar({ claudeStatus, offer, canAsk, busy, onAskClaude, onReviewOffer }) {
  if (!claudeStatus?.configured || !claudeStatus?.mayEscalate) return null;
  return (
    <div className="escalation-bar">
      {offer && (
        <p className="escalation-offer" role="status">
          <span>{OFFER_TEXT[offer.reason] ?? "Claude is available for this question."}</span>
          <button type="button" onClick={onReviewOffer} disabled={busy}>
            Review and ask Claude
          </button>
        </p>
      )}
      <button
        type="button"
        className="ask-claude-button"
        onClick={onAskClaude}
        disabled={!canAsk || busy}
        aria-label="Ask Claude about my last message"
      >
        Ask Claude
      </button>
    </div>
  );
}

function money(usd, gbp) {
  return `about £${gbp.toFixed(2)} (US$${usd.toFixed(2)})`;
}

export function ClaudeConfirmDialog({ offer, busy, onConfirm, onCancel }) {
  const allowance = offer.allowance;
  return (
    <div className="escalation-backdrop">
      <div
        className="escalation-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="escalation-title"
        aria-describedby="escalation-details"
      >
        <h2 id="escalation-title">Send this question to Claude?</h2>
        <div id="escalation-details">
          <p>
            Your question, and your recent conversation with JARVIS, will be sent over the internet to Claude, a service
            run by Anthropic. JARVIS does this only because you confirm.
          </p>
          <p>
            {offer.sendsMemory
              ? "Your saved memory notes will also be sent."
              : "Your saved memory notes will not be sent."}
          </p>
          <blockquote className="escalation-message">{offer.message}</blockquote>
          <p>
            This costs money. A question costs a few cents at most. Allowance left this month:{" "}
            {money(allowance.remainingUsd, allowance.remainingGbp)}.
          </p>
          {allowance.warning && (
            <p className="escalation-warning" role="alert">
              More than 80% of this month&rsquo;s allowance has been used.
            </p>
          )}
        </div>
        <div className="escalation-actions">
          <button type="button" onClick={onCancel} disabled={busy}>
            Cancel
          </button>
          <button type="button" className="escalation-confirm" onClick={onConfirm} disabled={busy}>
            {busy ? "Asking Claude…" : "Send to Claude"}
          </button>
        </div>
      </div>
    </div>
  );
}
