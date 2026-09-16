// Memory Management UXP panel (EIP-ESR0058-005, ESR-0058 WP6, EBG-0131).
// Surfaces BRD-0001's memory.backup/memory.restore RPC methods (delivered
// ESR-0057 WP2/ESR-0058 WP3) in the actual app for the first time - both
// were previously RPC-only, reachable only from a test or a manual RPC
// call, exactly the gap the gap analysis flagged. Mirrors
// AgentFrameworkPanel.jsx's dedicated-panel-file pattern and reuses the
// existing .metrics-list/.metric-row classes - no new metric-rendering CSS.
//
// Backup uses a native folder picker, not a save-file picker: the backend
// always names the backup file itself (a timestamped filename inside
// whatever directory it is given - PersonalMemoryService.export_backup()),
// so offering an exact filename choice the backend would then ignore would
// be misleading.
//
// Restore retains the backend's own "recovery never runs silently"
// guarantee (BRD-0001 Section 6) rather than working around it: the first
// restore attempt always passes confirmOverwrite: false; a non-empty store
// refuses with a distinctive error, which this panel recognises and turns
// into an explicit inline confirmation step before retrying with
// confirmOverwrite: true. An empty store restores immediately, with
// nothing to overwrite.

import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open } from "@tauri-apps/plugin-dialog";

const OVERWRITE_REFUSAL_MARKER = "confirm_overwrite=True";

export function MemoryManagementPanel({ recordCount, statusError, onStatusChange }) {
  const [backupBusy, setBackupBusy] = useState(false);
  const [backupResult, setBackupResult] = useState(null);
  const [backupError, setBackupError] = useState(null);

  const [restoreBusy, setRestoreBusy] = useState(false);
  const [restoreResult, setRestoreResult] = useState(null);
  const [restoreError, setRestoreError] = useState(null);
  const [pendingOverwritePath, setPendingOverwritePath] = useState(null);

  const handleBackup = async () => {
    setBackupError(null);
    setBackupResult(null);

    const chosenDir = await open({ directory: true, multiple: false, title: "Choose a backup folder" }).catch(
      () => null,
    );
    if (!chosenDir) return;

    setBackupBusy(true);
    invoke("backup_memory", { backupDir: chosenDir })
      .then((result) => {
        setBackupResult(result.path);
      })
      .catch((error) => {
        setBackupError(`Backup failed: ${error}`);
      })
      .finally(() => {
        setBackupBusy(false);
      });
  };

  const attemptRestore = (backupPath, confirmOverwrite) => {
    setRestoreBusy(true);
    setRestoreError(null);

    invoke("restore_memory", { backupPath, confirmOverwrite })
      .then((result) => {
        setRestoreResult(result.recordCount);
        setPendingOverwritePath(null);
        onStatusChange?.();
      })
      .catch((error) => {
        const message = String(error);
        if (!confirmOverwrite && message.includes(OVERWRITE_REFUSAL_MARKER)) {
          setPendingOverwritePath(backupPath);
          return;
        }
        setRestoreError(`Restore failed: ${message}`);
        setPendingOverwritePath(null);
      })
      .finally(() => {
        setRestoreBusy(false);
      });
  };

  const handleRestorePick = async () => {
    setRestoreError(null);
    setRestoreResult(null);
    setPendingOverwritePath(null);

    const chosenFile = await open({
      directory: false,
      multiple: false,
      title: "Choose a backup file to restore",
      filters: [{ name: "JARVIS Memory Backup", extensions: ["json"] }],
    }).catch(() => null);
    if (!chosenFile) return;

    attemptRestore(chosenFile, false);
  };

  const handleConfirmOverwrite = () => {
    if (pendingOverwritePath) attemptRestore(pendingOverwritePath, true);
  };

  return (
    <aside className="memory-management-panel" aria-labelledby="memory-management-panel-heading">
      <h2 id="memory-management-panel-heading">Memory Management</h2>
      {statusError ? (
        <p className="panel-status-message">Memory service is unavailable.</p>
      ) : (
        <dl className="metrics-list">
          <div className="metric-row">
            <dt>Stored memories</dt>
            <dd>{recordCount === null ? "Connecting..." : recordCount}</dd>
          </div>
        </dl>
      )}

      <div className="memory-action-row">
        <button type="button" className="outline-action" disabled={backupBusy} onClick={handleBackup}>
          {backupBusy ? "Backing up..." : "Back Up..."}
        </button>
        <button type="button" className="outline-action" disabled={restoreBusy} onClick={handleRestorePick}>
          {restoreBusy ? "Restoring..." : "Restore..."}
        </button>
      </div>

      {backupError && (
        <p className="conversation-error" role="alert">
          {backupError}
        </p>
      )}
      {backupResult && <p className="panel-status-message">Backed up to {backupResult}</p>}

      {pendingOverwritePath && (
        <div className="memory-overwrite-confirm" role="alertdialog" aria-label="Confirm overwrite">
          <p className="conversation-error">
            Restoring will permanently overwrite {recordCount === null ? "the" : recordCount} existing memor
            {recordCount === 1 ? "y" : "ies"}. This cannot be undone.
          </p>
          <div className="memory-action-row">
            <button type="button" className="outline-action" onClick={handleConfirmOverwrite} disabled={restoreBusy}>
              Overwrite and Restore
            </button>
            <button type="button" className="outline-action" onClick={() => setPendingOverwritePath(null)}>
              Cancel
            </button>
          </div>
        </div>
      )}
      {restoreError && (
        <p className="conversation-error" role="alert">
          {restoreError}
        </p>
      )}
      {restoreResult !== null && !pendingOverwritePath && (
        <p className="panel-status-message">Restored {restoreResult} record{restoreResult === 1 ? "" : "s"}.</p>
      )}
    </aside>
  );
}
