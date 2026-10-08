import { useCallback, useEffect, useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

// Local AI setup (ESR-0061 WP3c, EIP-ESR0061-003 6.9): is Ollama there, which
// model suits this computer, and fetching it. Functional and tested, not
// designed: WP4/WP5 restyle it and add first-run flow. JARVIS never installs
// Ollama; it only opens the download page and says what to do. Downloads are
// limited by the backend to a short list of models.

const MANAGER_ROLES = ["Administrator", "Adult"];

function percent(pull) {
  if (!pull || !pull.total) return 0;
  return Math.min(100, Math.floor((pull.completed / pull.total) * 100));
}

export function LocalAiPanel({ activeProfile, pullProgress, pullFinished }) {
  const [status, setStatus] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);
  const useWhenDone = useRef(null);
  const canManage = MANAGER_ROLES.includes(activeProfile?.role);

  const refresh = useCallback(() => {
    setError(null);
    return Promise.all([invoke("ollama_status"), invoke("ollama_recommendation")])
      .then(([nextStatus, nextRecommendation]) => {
        setStatus(nextStatus);
        setRecommendation(nextRecommendation);
      })
      .catch((failure) => {
        setStatus(null);
        setRecommendation(null);
        setError(`Could not read the local AI status: ${failure}`);
      });
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh, activeProfile?.id]);

  // A finished download: if the person asked to use it, switch to it; then re-read.
  useEffect(() => {
    if (!pullFinished) return;
    const tag = pullFinished.model;
    const wanted = useWhenDone.current === tag;
    useWhenDone.current = null;
    const done =
      pullFinished.outcome === "completed" && wanted
        ? invoke("ollama_use_model", { model: tag }).catch((failure) => setError(`Could not switch model: ${failure}`))
        : Promise.resolve();
    if (pullFinished.outcome === "failed") setError("The download did not finish. You can try again.");
    done.then(refresh);
  }, [pullFinished, refresh]);

  const pull = status?.pull;
  const downloading = Boolean(pull?.active);
  const live = downloading && pullProgress?.model === pull?.model ? { ...pull, ...pullProgress } : pull;

  const startDownload = (model, andUse) => {
    setBusy(true);
    setError(null);
    useWhenDone.current = andUse ? model : null;
    invoke("ollama_pull", { model })
      .then(() => refresh())
      .catch((failure) => {
        useWhenDone.current = null;
        setError(`Could not start the download: ${failure}`);
      })
      .finally(() => setBusy(false));
  };

  const cancelDownload = () => {
    useWhenDone.current = null;
    invoke("ollama_cancel_pull")
      .then(() => refresh())
      .catch((failure) => setError(`Could not cancel: ${failure}`));
  };

  const useModel = (model) => {
    setBusy(true);
    setError(null);
    invoke("ollama_use_model", { model })
      .then(() => refresh())
      .catch((failure) => setError(`Could not switch model: ${failure}`))
      .finally(() => setBusy(false));
  };

  const openDownloadPage = () => {
    invoke("open_ollama_download_page").catch((failure) => setError(String(failure)));
  };

  const primary = recommendation?.primary;
  const fallback = recommendation?.fallback;
  const active = status?.activeModel;

  const modelAction = (model, isFallback) => {
    if (!model) return null;
    const isActive = model.tag === active;
    return (
      <div className="local-ai-model" key={model.tag}>
        <p>
          <strong>{isFallback ? "Smaller option" : "Recommended"}:</strong> {model.label}, {model.downloadGb} GB to
          download.
        </p>
        <p className="local-ai-note">{model.note}</p>
        {isActive ? (
          <p role="status">In use</p>
        ) : model.installed ? (
          <button type="button" onClick={() => useModel(model.tag)} disabled={!canManage || busy || downloading}>
            Use this model
          </button>
        ) : (
          <button
            type="button"
            onClick={() => startDownload(model.tag, true)}
            disabled={!canManage || busy || downloading || (!isFallback && recommendation?.diskOk === false)}
          >
            Download and use
          </button>
        )}
      </div>
    );
  };

  return (
    <section className="local-ai-panel" aria-labelledby="local-ai-heading">
      <h2 id="local-ai-heading">Local AI</h2>
      {!status && !error && <p>Checking this computer&hellip;</p>}
      {error && (
        <p className="conversation-error" role="alert">
          {error}
        </p>
      )}
      {status && !status.running && (
        <div className="local-ai-install">
          <p role="status">
            {status.installed
              ? "Ollama is installed but not running. Open Ollama, then check again."
              : "Ollama is not installed. JARVIS uses it to answer on this computer."}
          </p>
          {!status.installed && (
            <ol>
              {status.install.steps.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ol>
          )}
          <div className="local-ai-actions">
            {!status.installed && (
              <button type="button" onClick={openDownloadPage}>
                Open download page
              </button>
            )}
            <button type="button" onClick={refresh}>
              Check again
            </button>
          </div>
        </div>
      )}
      {status?.running && (
        <div>
          <p role="status">
            Ollama {status.version} is running. Active model: {active}
            {status.activeModelInstalled ? "" : " (not downloaded yet)"}.
          </p>
          {status.modelSource === "environment" && (
            <p className="local-ai-note">The model is set by the JARVIS_OLLAMA_MODEL setting, which overrides this screen.</p>
          )}
          {recommendation && (
            <>
              <p className="local-ai-note">{recommendation.reason}</p>
              {recommendation.belowMinimum && (
                <p className="conversation-error" role="alert">
                  This computer is below the usual minimum, so answers may be slow.
                </p>
              )}
              {recommendation.diskOk === false && (
                <p className="conversation-error" role="alert">
                  Not enough free disk space for the recommended model: it needs about {recommendation.needsDiskGb} GB and{" "}
                  {recommendation.hardware.freeDiskGb} GB is free.
                </p>
              )}
              {modelAction(primary, false)}
              {fallback && modelAction(fallback, true)}
            </>
          )}
          {!canManage && <p className="local-ai-note">Only an Administrator or Adult profile can download or change models.</p>}
        </div>
      )}
      {downloading && (
        <div className="local-ai-progress">
          <p>Downloading {live.model}&hellip;</p>
          <div
            className="local-ai-bar"
            role="progressbar"
            aria-label="Model download progress"
            aria-valuemin={0}
            aria-valuemax={100}
            aria-valuenow={percent(live)}
          >
            <div className="local-ai-bar-fill" style={{ width: `${percent(live)}%` }} />
          </div>
          <p>{percent(live)}%</p>
          {canManage && (
            <button type="button" onClick={cancelDownload}>
              Cancel download
            </button>
          )}
        </div>
      )}
    </section>
  );
}
