import { useCallback, useEffect, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

// Voice setup (ESR-0062 WP3, EIP-ESR0062-003 V8): speaking (Kokoro) and
// listening (Whisper) are downloaded here, once, by an Adult or Administrator.
// The backend checks every file against its catalog before using it, loads the
// voice in the background, and enforces who may download; this panel only
// shows that and asks. When a voice comes on, the app re-reads the platform
// status, so the speak and microphone buttons appear without a restart.

const STATE_TEXT = {
  missing: "Not downloaded",
  checking: "Checking the files…",
  loading: "Starting…",
  on: "On",
  damaged: "The files are damaged. Download again to fix this.",
  failed: "Could not start. Download again to try to fix this.",
  downloading: "Downloading…",
};

const PURPOSE_TEXT = {
  speaking: "Speaking: JARVIS reads its replies aloud.",
  listening: "Listening: you can speak a question instead of typing it.",
};

function megabytes(bytes) {
  return Math.round((bytes ?? 0) / 1024 ** 2);
}

function percent(received, total) {
  if (!total) return 0;
  return Math.min(100, Math.floor((received / total) * 100));
}

export function VoicePanel({ activeProfile, voiceEvent }) {
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(null);

  const refresh = useCallback(() => {
    return invoke("voice_status")
      .then((next) => {
        setStatus(next);
        setError(null);
      })
      .catch((failure) => {
        setStatus(null);
        setError(`Could not read the voice status: ${failure}`);
      });
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh, activeProfile?.id]);

  // Progress, the end of a download, and a voice coming on or off.
  useEffect(() => {
    if (!voiceEvent) return;
    const { method, params } = voiceEvent;
    if (method === "voice.downloadProgress") {
      if (params?.state === "downloading") {
        setProgress(params);
        return;
      }
      setProgress(null);
      refresh().then(() => {
        if (params?.state === "failed") setError(params.message || "The download did not finish. Try again.");
      });
      return;
    }
    if (method === "voice.changed") refresh();
  }, [voiceEvent, refresh]);

  const mayDownload = Boolean(status?.mayDownload);
  const download = status?.download;
  const downloading = Boolean(download?.active);

  const startDownload = (model) => {
    setBusy(true);
    setError(null);
    invoke("voice_download", { model })
      .then(() => refresh())
      .catch((failure) => setError(`Could not start the download: ${failure}`))
      .finally(() => setBusy(false));
  };

  const cancelDownload = () => {
    invoke("voice_cancel_download")
      .then(() => refresh())
      .catch((failure) => setError(`Could not cancel: ${failure}`));
  };

  const live = downloading && progress?.model === download?.model ? progress : download;

  return (
    <section className="voice-panel" aria-labelledby="voice-heading" data-testid="voice-panel">
      <h2 id="voice-heading">Voice</h2>
      {!status && !error && <p>Checking voice&hellip;</p>}
      {error && (
        <p className="conversation-error" role="alert">
          {error}
        </p>
      )}
      {status?.models?.map((model) => {
        const canDownload =
          mayDownload && !model.fromEnvironment && ["missing", "damaged", "failed"].includes(model.state);
        return (
          <div className="local-ai-model" key={model.key} data-testid={`voice-${model.key}`}>
            <p>
              <strong>{model.label}</strong>
            </p>
            <p className="local-ai-note">{PURPOSE_TEXT[model.purpose]}</p>
            <p role="status">{STATE_TEXT[model.state] ?? model.state}</p>
            {model.fromEnvironment && (
              <p className="local-ai-note">Set by a developer setting, which overrides this screen.</p>
            )}
            {canDownload && (
              <button type="button" onClick={() => startDownload(model.key)} disabled={busy || downloading}>
                {model.state === "missing" ? "Download" : "Download again"} ({megabytes(model.totalBytes)} MB)
              </button>
            )}
          </div>
        );
      })}
      {status && !mayDownload && (
        <p className="local-ai-note">Only an Administrator or Adult profile can turn voice on. Ask an adult to do it.</p>
      )}
      {downloading && live && (
        <div className="local-ai-progress">
          <p>Downloading voice&hellip;</p>
          <div
            className="local-ai-bar"
            role="progressbar"
            aria-label="Voice download progress"
            aria-valuemin={0}
            aria-valuemax={100}
            aria-valuenow={percent(live.receivedBytes, live.totalBytes)}
          >
            <div
              className="local-ai-bar-fill"
              style={{ width: `${percent(live.receivedBytes, live.totalBytes)}%` }}
            />
          </div>
          <p>{percent(live.receivedBytes, live.totalBytes)}%</p>
          {mayDownload && (
            <button type="button" onClick={cancelDownload}>
              Cancel download
            </button>
          )}
        </div>
      )}
    </section>
  );
}
