import { test, expect } from "@playwright/test";

// Mocks Tauri's IPC layer directly (window.__TAURI_INTERNALS__.invoke),
// matching this repository's own prior ad hoc verification approach
// (EBG-0072/EBG-0073) and the mechanism `@tauri-apps/api/core`'s invoke()
// actually calls under the hood (confirmed by direct source read,
// EIP-ESR0032-002). There is no live backend and no bundled Tauri binary
// in this test - it drives the Vite dev server's React app directly.
async function mockTauriIpc(
  page,
  {
    speakResult,
    transcribeResult,
    transcriptionAvailable = false,
    profiles = [],
    activeProfile = null,
    agents = [],
    invokeAgentResult,
    knowledgeGraphOverrides = {},
    memoryRecordCount = 0,
    dialogOpenResult = null,
    backupMemoryResult,
    restoreMemoryResult,
    memories = [],
    claude = null,
    ollama = {},
  } = {},
) {
  await page.addInitScript(
    ({
      platformStatus,
      knowledgeGraph,
      speakResult,
      transcribeResult,
      transcriptionAvailable,
      profiles,
      activeProfile,
      agents,
      invokeAgentResult,
      memoryRecordCount,
      dialogOpenResult,
      backupMemoryResult,
      restoreMemoryResult,
      memories,
      claude,
      ollama,
    }) => {
      // Voice Faculty Increment B (EIP-ESR0047-001): navigator.mediaDevices
      // and MediaRecorder are real browser APIs the app calls directly,
      // before ever reaching the mocked Tauri invoke() below - stubbed here
      // so the mic button's full click-to-populated-composer path can be
      // exercised without real microphone hardware, matching Increment A's
      // own disclosed real-audio-hardware e2e limitation.
      class FakeMediaRecorder {
        constructor() {
          this.state = "inactive";
          this.mimeType = "audio/webm";
          this.ondataavailable = null;
          this.onstop = null;
        }

        start() {
          this.state = "recording";
        }

        stop() {
          this.state = "inactive";
          if (this.ondataavailable) {
            this.ondataavailable({ data: new Blob(["fake-audio-bytes"], { type: this.mimeType }) });
          }
          if (this.onstop) this.onstop();
        }
      }

      window.MediaRecorder = FakeMediaRecorder;
      if (!window.navigator.mediaDevices) window.navigator.mediaDevices = {};
      window.navigator.mediaDevices.getUserMedia = () =>
        Promise.resolve({ getTracks: () => [{ stop: () => {} }] });
      // Stateful, in-page mock (EIP-ESR0046-001): list_profiles/active_profile
      // read this state, create_profile/select_profile mutate it - a real
      // Tauri backend behaves the same way, just persisted to SQLite instead
      // of an in-memory closure.
      const state = {
        profiles: [...profiles],
        active: activeProfile,
        memoryRecordCount: memories.length || memoryRecordCount,
        memories: [...memories],
      };
      let nextId = state.profiles.length + 1;

      window.__TAURI_INTERNALS__ = {
        invoke: (cmd, args) => {
          if (cmd === "platform_status") return Promise.resolve({ ...platformStatus, transcriptionAvailable });
          if (cmd === "knowledge_graph") return Promise.resolve(knowledgeGraph);
          // Asking Claude (ESR-0061 WP3b): `claude` is null for a machine with no
          // key (provider_status fails, so the controls stay hidden). Otherwise
          // it describes what the backend would report; every escalate call is
          // recorded so a test can prove nothing was sent without a confirm.
          window.__escalateCalls = window.__escalateCalls || [];
          const claudeAllowance = {
            month: "2026-10",
            capUsd: 37.5,
            spentUsd: 1.25,
            remainingUsd: 36.25,
            capGbp: 30,
            remainingGbp: 29,
            requests: 3,
            warning: Boolean(claude && claude.warning),
            capReached: false,
          };
          const claudeOffer = (reason, message) => ({
            offered: true,
            reason,
            token: `token-${window.__escalateCalls.length + 1}`,
            expiresInSeconds: 600,
            model: "claude-sonnet-5-5",
            sendsMemory: Boolean(claude && claude.sendsMemory),
            allowance: claudeAllowance,
            message,
          });
          // Local AI setup (ESR-0061 WP3c). The default is a healthy machine with
          // the recommended model in use, so other tests see a quiet panel.
          window.__ollamaCalls = window.__ollamaCalls || [];
          const model = (tag, label, installed, downloadGb = 3.3) => ({
            tag,
            label,
            downloadGb,
            note: `${label} note.`,
            installed,
          });
          const ollamaState = (window.__ollamaState = window.__ollamaState || {
            status: {
              installed: true,
              running: true,
              version: "0.35.0",
              endpoint: "http://localhost:11434",
              models: ["qwen3.5:4b"],
              activeModel: "qwen3.5:4b",
              activeModelInstalled: true,
              modelSource: "default",
              pull: { active: false, model: null, completed: 0, total: 0, status: "idle" },
              ...(ollama.status || {}),
            },
            recommendation: {
              hardware: { system: "Windows", ramGb: 31.9, gpuGb: 8, unifiedMemory: false, freeDiskGb: 25 },
              primary: model("qwen3.5:4b", "Qwen3.5 4B (balanced)", true),
              fallback: model("qwen3.5:2b", "Qwen3.5 2B (light)", false, 2.7),
              reason: "Chosen for this computer's graphics card (8 GB).",
              belowMinimum: false,
              needsDiskGb: 4,
              diskOk: true,
              models: [],
              ...(ollama.recommendation || {}),
            },
          });
          // Copies, as a real IPC reply would be: React ignores a state update that is the same object.
          if (cmd === "ollama_status") return Promise.resolve(structuredClone(ollamaState.status));
          if (cmd === "ollama_recommendation") return Promise.resolve(structuredClone(ollamaState.recommendation));
          if (cmd === "ollama_pull") {
            window.__ollamaCalls.push(["pull", args.model]);
            ollamaState.status.pull = { active: true, model: args.model, completed: 0, total: 100, status: "starting" };
            return Promise.resolve({ started: true, model: args.model });
          }
          if (cmd === "ollama_cancel_pull") {
            window.__ollamaCalls.push(["cancel"]);
            ollamaState.status.pull = { active: false, model: null, completed: 0, total: 0, status: "cancelled" };
            return Promise.resolve({ cancelled: true });
          }
          if (cmd === "ollama_use_model") {
            window.__ollamaCalls.push(["use", args.model]);
            ollamaState.status.activeModel = args.model;
            return Promise.resolve({ activeModel: args.model, modelSource: "saved" });
          }
          if (cmd === "open_ollama_download_page") {
            window.__ollamaCalls.push(["open-download-page"]);
            return Promise.resolve(null);
          }
          if (cmd === "provider_status") {
            if (!claude) return Promise.reject(new Error("provider.status unavailable"));
            return Promise.resolve({
              claude: {
                configured: true,
                model: "claude-sonnet-5-5",
                mayEscalate: claude.mayEscalate !== false,
                allowance: claudeAllowance,
              },
            });
          }
          if (cmd === "offer_escalation") return Promise.resolve(claudeOffer("requested", args.message));
          if (cmd === "escalate_message") {
            window.__escalateCalls.push(args.token);
            if (claude && claude.escalateError) return Promise.reject(new Error(claude.escalateError));
            return Promise.resolve({
              message: "Claude says: a considered answer.",
              provider: "anthropic",
              answeredBy: "claude",
              failure: null,
              allowance: { ...claudeAllowance, spentUsd: 1.254, remainingUsd: 36.246, requests: 4 },
            });
          }
          if (cmd === "send_message") {
            const message = args && args.message ? args.message : "";
            const escalation =
              claude && claude.offerReason
                ? claudeOffer(claude.offerReason, message)
                : { offered: false, reason: null, token: null };
            return Promise.resolve({ message: `local-echo: ${message}`, provider: "local-echo", escalation });
          }
          if (cmd === "speak_message") {
            return Promise.resolve(
              speakResult || { status: "not_connected", message: "Guardian has no speech synthesis provider connected." },
            );
          }
          if (cmd === "transcribe_audio") {
            return Promise.resolve(
              transcribeResult || {
                status: "not_connected",
                text: null,
                message: "Guardian has no speech transcription provider connected.",
              },
            );
          }
          if (cmd === "list_profiles") return Promise.resolve({ profiles: state.profiles });
          if (cmd === "active_profile") return Promise.resolve({ profile: state.active });
          if (cmd === "create_profile") {
            const created = {
              id: `profile-${nextId++}`,
              displayName: args.displayName,
              role: args.role,
              createdAt: new Date().toISOString(),
            };
            state.profiles.push(created);
            return Promise.resolve(created);
          }
          if (cmd === "select_profile") {
            const selected = state.profiles.find((profile) => profile.id === args.profileId);
            if (!selected) return Promise.reject(new Error(`No such profile: ${args.profileId}`));
            state.active = selected;
            return Promise.resolve(selected);
          }
          if (cmd === "list_agents") return Promise.resolve({ agents });
          if (cmd === "invoke_agent") {
            return Promise.resolve(
              invokeAgentResult || {
                status: "reported",
                message: null,
                payload: { cpuPercent: "12.5", memoryPercent: "40.0" },
              },
            );
          }
          if (cmd === "memory_status") return Promise.resolve({ recordCount: state.memoryRecordCount });
          // EBG-0145 (ESR-0059 WP10): list and revoke, mirroring the real
          // backend - an unknown id is an error, not a silent success.
          if (cmd === "list_memory") return Promise.resolve({ records: state.memories });
          if (cmd === "delete_memory") {
            const before = state.memories.length;
            state.memories = state.memories.filter((record) => record.id !== args.recordId);
            if (state.memories.length === before) {
              return Promise.reject(new Error(`KeyError: No stored memory found for id: '${args.recordId}'.`));
            }
            state.memoryRecordCount = state.memories.length;
            return Promise.resolve({ recordId: args.recordId, deleted: true });
          }
          if (cmd === "plugin:dialog|open") return Promise.resolve(dialogOpenResult);
          if (cmd === "backup_memory") {
            if (backupMemoryResult && backupMemoryResult.error) {
              return Promise.reject(new Error(backupMemoryResult.error));
            }
            return Promise.resolve(backupMemoryResult || { path: "C:\\fake\\personal_memory_backup_test.json" });
          }
          if (cmd === "restore_memory") {
            if (restoreMemoryResult && restoreMemoryResult.error) {
              return Promise.reject(new Error(restoreMemoryResult.error));
            }
            // A real backend refuses a non-empty store without
            // confirmOverwrite - mirrored here so the panel's own
            // detect-refusal-then-confirm flow has something genuine to
            // react to, not just a canned success.
            if (state.memoryRecordCount > 0 && !args.confirmOverwrite) {
              return Promise.reject(
                new Error(
                  "Store is not empty: restoring would overwrite existing data. " +
                    "Pass confirm_overwrite=True to proceed - recovery never runs silently.",
                ),
              );
            }
            const restoredCount = restoreMemoryResult?.recordCount ?? 1;
            state.memoryRecordCount = restoredCount;
            return Promise.resolve({ recordCount: restoredCount });
          }
          return Promise.reject(new Error(`Unmocked Tauri command: ${cmd}`));
        },
      };
    },
    {
      platformStatus: {
        state: "Running",
        runtimeHealth: "Healthy",
        providerConnected: "Online",
        memoryConnected: "Online",
        providers: ["local-echo"],
        policyEngine: "TrustTierPolicy",
      },
      knowledgeGraph: {
        nodes: [
          { id: "n1", label: "Test Node 1" },
          { id: "n2", label: "Test Node 2" },
        ],
        edges: [{ source: "n1", target: "n2" }],
        active_clusters: [],
        ...knowledgeGraphOverrides,
      },
      speakResult,
      transcribeResult,
      transcriptionAvailable,
      profiles,
      activeProfile,
      agents,
      invokeAgentResult,
      memoryRecordCount,
      dialogOpenResult,
      backupMemoryResult,
      restoreMemoryResult,
      memories,
      claude,
      ollama,
    },
  );
}

test("app launches and shows JARVIS branding with live system health", async ({ page }) => {
  await mockTauriIpc(page);
  await page.goto("/");

  await expect(page.getByText("JARVIS", { exact: true })).toBeVisible();
  await expect(page.locator(".system-health-panel")).toContainText("Runtime: Running");
});

test("sending a message renders the mocked response in the conversation log", async ({ page }) => {
  await mockTauriIpc(page);
  await page.goto("/");

  await page.getByPlaceholder("Ask Guardian anything...").fill("Hello Guardian");
  await page.getByRole("button", { name: "Send" }).click();

  await expect(page.locator(".conversation-message.guardian")).toContainText(
    "local-echo: Hello Guardian",
  );
});

// EIP-ESR0044-001 (EBG-0114): the speak button is a new, additive affordance
// on an already-rendered Guardian message - these two tests cover the honest
// not_connected/error path (the real default on most machines, since
// JARVIS_PIPER_VOICE_PATH is unconfigured) and the synthesized/audio-playing
// path, matching guardian.speak's own two observable outcome shapes.
test("speak button shows an inline note when Guardian has no speech provider connected", async ({
  page,
}) => {
  await mockTauriIpc(page, {
    speakResult: { status: "not_connected", message: "Guardian has no speech synthesis provider connected." },
  });
  await page.goto("/");

  await page.getByPlaceholder("Ask Guardian anything...").fill("Hello Guardian");
  await page.getByRole("button", { name: "Send" }).click();
  await expect(page.locator(".conversation-message.guardian")).toBeVisible();

  await page.getByRole("button", { name: "Speak this response" }).click();

  await expect(page.locator(".conversation-error")).toContainText(
    "Guardian has no speech synthesis provider connected.",
  );
});

test("speak button plays synthesized audio without showing an error note", async ({ page }) => {
  // A minimal, valid, silent WAV fixture (44-byte header, 0 data bytes) - real
  // enough for the browser's Audio element to decode without error, no real
  // Piper synthesis or audio hardware required for this wiring-level test.
  const silentWavBase64 = "UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=";

  await mockTauriIpc(page, {
    speakResult: { status: "synthesized", message: null, audio: silentWavBase64, mimeType: "audio/wav" },
  });
  await page.goto("/");

  await page.getByPlaceholder("Ask Guardian anything...").fill("Hello Guardian");
  await page.getByRole("button", { name: "Send" }).click();
  await expect(page.locator(".conversation-message.guardian")).toBeVisible();

  await page.getByRole("button", { name: "Speak this response" }).click();

  await expect(page.locator(".conversation-error")).toHaveCount(0);
});

// EIP-ESR0047-001 (EBG-0117): the mic button is a new, additive affordance
// on the message composer - these tests cover guardian.transcribe's two
// observable outcome shapes, mirroring the speak button's own pattern, plus
// the capability-gating fix from session-wide WP6 (Engineering Reviewer
// finding): the button must not render - never mind activate a real
// microphone permission prompt - unless platform.status reports
// transcriptionAvailable. getUserMedia/MediaRecorder are stubbed in
// mockTauriIpc (no real microphone hardware, matching Increment A's own
// disclosed limitation).
test("mic button does not render when transcription is not available", async ({ page }) => {
  await mockTauriIpc(page);
  await page.goto("/");

  await expect(page.getByPlaceholder("Ask Guardian anything...")).toBeVisible();
  await expect(page.getByRole("button", { name: "Speak a message" })).toHaveCount(0);
});

test("mic button shows an inline note when Guardian has no transcription provider connected", async ({
  page,
}) => {
  await mockTauriIpc(page, {
    transcriptionAvailable: true,
    transcribeResult: {
      status: "not_connected",
      text: null,
      message: "Guardian has no speech transcription provider connected.",
    },
  });
  await page.goto("/");

  await page.getByRole("button", { name: "Speak a message" }).click();
  await page.getByRole("button", { name: "Stop recording and transcribe" }).click();

  await expect(page.locator(".conversation-error")).toContainText(
    "Guardian has no speech transcription provider connected.",
  );
});

test("mic button populates the composer with the transcript without auto-sending", async ({
  page,
}) => {
  await mockTauriIpc(page, {
    transcriptionAvailable: true,
    transcribeResult: { status: "transcribed", text: "hello Guardian", message: null },
  });
  await page.goto("/");

  await page.getByRole("button", { name: "Speak a message" }).click();
  await page.getByRole("button", { name: "Stop recording and transcribe" }).click();

  await expect(page.getByPlaceholder("Ask Guardian anything...")).toHaveValue("hello Guardian");
  await expect(page.locator(".conversation-message.guardian")).toHaveCount(0);
  await expect(page.locator(".conversation-error")).toHaveCount(0);
});

// EIP-ESR0046-001 (EBG-0116): the profile card is a new, real affordance
// replacing the previously static "Robert / Signed in locally" placeholder -
// these two tests cover the two observable states guardian.speak's own tests
// already established the pattern for: no profile yet selected (create form),
// and an existing profile that can be switched away from (picker).
test("profile create form appears when no profile is active, and creating one shows it as active", async ({
  page,
}) => {
  await mockTauriIpc(page);
  await page.goto("/");

  await expect(page.getByPlaceholder("Your name")).toBeVisible();

  await page.getByPlaceholder("Your name").fill("Robert");
  await page.getByLabel("New profile household role").selectOption("Administrator");
  await page.getByRole("button", { name: "Create profile" }).click();

  await expect(page.getByRole("button", { name: "Switch Guardian profile" })).toContainText("Robert");
  await expect(page.getByRole("button", { name: "Switch Guardian profile" })).toContainText("Administrator");
  await expect(page.getByPlaceholder("Your name")).toHaveCount(0);
});

test("selecting a profile from the picker switches the active profile", async ({ page }) => {
  await mockTauriIpc(page, {
    profiles: [
      { id: "profile-1", displayName: "Robert", role: "Administrator", createdAt: "2026-07-31T00:00:00Z" },
      { id: "profile-2", displayName: "Alex", role: "Child", createdAt: "2026-07-31T00:00:00Z" },
    ],
    activeProfile: { id: "profile-1", displayName: "Robert", role: "Administrator", createdAt: "2026-07-31T00:00:00Z" },
  });
  await page.goto("/");

  const summary = page.getByRole("button", { name: "Switch Guardian profile" });
  await expect(summary).toContainText("Robert");

  await summary.click();
  await page.getByRole("button", { name: "Alex" }).click();

  await expect(summary).toContainText("Alex");
  await expect(summary).toContainText("Child");
});

// EIP-ESR0050-001 (EBG-0120): wires the ESR-0049 Agent Framework backend
// into the live UXP. These tests cover the four observable states -
// registered agent shown live in both the sidebar row and the panel,
// clicking "Run" rendering the real returned payload, and a denied/error
// outcome rendering inline rather than silently failing - mirroring the
// speak/transcribe buttons' own established outcome-status test pattern.
test("agent framework sidebar row and panel show no agents when none are registered", async ({
  page,
}) => {
  await mockTauriIpc(page);
  await page.goto("/");

  await expect(page.locator(".agent-framework-panel")).toContainText(
    "No specialist agents are registered.",
  );
});

test("agent framework sidebar row and panel reflect a real registered agent", async ({ page }) => {
  await mockTauriIpc(page, { agents: ["gia-observability"] });
  await page.goto("/");

  await expect(page.locator(".capability-row", { hasText: "Agent Framework" })).toContainText(
    "gia-observability",
  );
  await expect(page.locator(".agent-framework-panel")).toContainText("gia-observability");
});

test("running an agent renders its real returned payload", async ({ page }) => {
  await mockTauriIpc(page, {
    agents: ["gia-observability"],
    invokeAgentResult: {
      status: "reported",
      message: null,
      payload: { cpuPercent: "12.5", memoryPercent: "40.0" },
    },
  });
  await page.goto("/");

  await page.getByRole("button", { name: "Run gia-observability" }).click();

  await expect(page.locator(".agent-result-list")).toContainText("cpuPercent");
  await expect(page.locator(".agent-result-list")).toContainText("12.5");
});

test("a denied agent outcome renders inline rather than silently failing", async ({ page }) => {
  await mockTauriIpc(page, {
    agents: ["gia-observability"],
    invokeAgentResult: { status: "denied", message: "Guardian declined this request." },
  });
  await page.goto("/");

  await page.getByRole("button", { name: "Run gia-observability" }).click();

  await expect(page.locator(".agent-framework-panel .conversation-error")).toContainText(
    "Guardian declined this request.",
  );
});

test("a cluster reported active by knowledge.graph's pull field renders as illuminated", async ({ page }) => {
  // EBG-0121 (Guardian Orb Phase 2): exercises the pull-interface seed path
  // (App.jsx's knowledge_graph mount-fetch handling) - the live
  // knowledge.cluster_activity push-notification path is not covered here,
  // since this suite has no existing mock for @tauri-apps/api/event's
  // listen() (system.heartbeat is likewise untested at this layer) -
  // disclosed rather than silently assumed covered.
  await mockTauriIpc(page, {
    knowledgeGraphOverrides: {
      nodes: [
        { id: "n1", label: "Test Node 1", cluster: "jarvis" },
        { id: "n2", label: "Test Node 2", cluster: "sentinel" },
      ],
      edges: [{ source: "n1", target: "n2" }],
      active_clusters: ["jarvis"],
    },
  });
  await page.goto("/");

  const activeRow = page.locator(".cluster-row", { hasText: "jarvis" });
  const idleRow = page.locator(".cluster-row", { hasText: "sentinel" });

  await expect(activeRow).toHaveClass(/is-active/);
  await expect(idleRow).not.toHaveClass(/is-active/);
});

test("a cluster with no reported activity renders without the illumination class", async ({ page }) => {
  await mockTauriIpc(page, {
    knowledgeGraphOverrides: {
      nodes: [{ id: "n1", label: "Test Node 1", cluster: "jarvis" }],
      edges: [],
      active_clusters: [],
    },
  });
  await page.goto("/");

  await expect(page.locator(".cluster-row", { hasText: "jarvis" })).not.toHaveClass(/is-active/);
});

// Memory Management UXP surface (EBG-0131, ESR-0058 WP6): the first frontend
// coverage of memory.backup/memory.restore, previously RPC-only.
test("memory management panel shows the real stored record count", async ({ page }) => {
  await mockTauriIpc(page, { memoryRecordCount: 3 });
  await page.goto("/");

  await expect(page.locator(".memory-management-panel")).toContainText("Stored memories");
  await expect(page.locator(".memory-management-panel .metric-row")).toContainText("3");
});

test("backing up memory shows the real returned backup path", async ({ page }) => {
  await mockTauriIpc(page, {
    memoryRecordCount: 2,
    dialogOpenResult: "C:\\Users\\test\\Backups",
    backupMemoryResult: { path: "C:\\Users\\test\\Backups\\personal_memory_backup_20260916T120000000000Z.json" },
  });
  await page.goto("/");

  await page.locator(".memory-management-panel").getByRole("button", { name: "Back Up..." }).click();

  await expect(page.locator(".memory-management-panel")).toContainText(
    "personal_memory_backup_20260916T120000000000Z.json",
  );
});

test("restoring into an empty store succeeds immediately without an overwrite prompt", async ({ page }) => {
  await mockTauriIpc(page, {
    memoryRecordCount: 0,
    dialogOpenResult: "C:\\Users\\test\\backup.json",
    restoreMemoryResult: { recordCount: 5 },
  });
  await page.goto("/");

  await page.locator(".memory-management-panel").getByRole("button", { name: "Restore..." }).click();

  await expect(page.locator(".memory-management-panel")).toContainText("Restored 5 records.");
  await expect(page.locator(".memory-overwrite-confirm")).toHaveCount(0);
});

test("restoring into a non-empty store requires an explicit overwrite confirmation", async ({ page }) => {
  await mockTauriIpc(page, {
    memoryRecordCount: 4,
    dialogOpenResult: "C:\\Users\\test\\backup.json",
  });
  await page.goto("/");

  await page.locator(".memory-management-panel").getByRole("button", { name: "Restore..." }).click();

  await expect(page.locator(".memory-overwrite-confirm")).toContainText("permanently overwrite 4 existing memories");

  await page.getByRole("button", { name: "Overwrite and Restore" }).click();

  await expect(page.locator(".memory-management-panel")).toContainText("Restored 1 record.");
  await expect(page.locator(".memory-overwrite-confirm")).toHaveCount(0);
});

test("cancelling the overwrite confirmation leaves stored memory untouched", async ({ page }) => {
  await mockTauriIpc(page, {
    memoryRecordCount: 4,
    dialogOpenResult: "C:\\Users\\test\\backup.json",
  });
  await page.goto("/");

  await page.locator(".memory-management-panel").getByRole("button", { name: "Restore..." }).click();
  await expect(page.locator(".memory-overwrite-confirm")).toBeVisible();

  await page.getByRole("button", { name: "Cancel" }).click();

  await expect(page.locator(".memory-overwrite-confirm")).toHaveCount(0);
  await expect(page.locator(".memory-management-panel .metric-row")).toContainText("4");
});


const SAMPLE_MEMORIES = [
  { id: "m-1", content: "Robert prefers dark mode.", createdAt: "2026-09-01T10:00:00+00:00", consentDecisionId: "d-1" },
  { id: "m-2", content: "Tea, no sugar.", createdAt: "2026-09-02T10:00:00+00:00", consentDecisionId: "d-2" },
];

test("stored memory text is hidden until the list is explicitly opened", async ({ page }) => {
  await mockTauriIpc(page, { memories: SAMPLE_MEMORIES });
  await page.goto("/");

  const panel = page.locator(".memory-management-panel");
  await expect(panel).toContainText("Stored memories");
  await expect(panel).not.toContainText("Robert prefers dark mode.");

  await panel.getByRole("button", { name: "Show memories" }).click();

  await expect(panel.getByRole("list", { name: "Stored memories" })).toContainText("Robert prefers dark mode.");
  await expect(panel.getByRole("list", { name: "Stored memories" })).toContainText("Tea, no sugar.");
});

test("deleting a memory needs confirmation, then removes it and updates the count", async ({ page }) => {
  await mockTauriIpc(page, { memories: SAMPLE_MEMORIES });
  await page.goto("/");

  const panel = page.locator(".memory-management-panel");
  await panel.getByRole("button", { name: "Show memories" }).click();
  await panel.getByRole("button", { name: "Delete memory: Tea, no sugar." }).click();

  await expect(panel.locator(".memory-delete-confirm")).toContainText("This cannot be undone.");
  await panel.locator(".memory-delete-confirm").getByRole("button", { name: "Delete" }).click();

  const list = panel.getByRole("list", { name: "Stored memories" });
  await expect(list).not.toContainText("Tea, no sugar.");
  await expect(list).toContainText("Robert prefers dark mode.");
  await expect(panel.locator(".metric-row")).toContainText("1");
});

test("cancelling a delete leaves the memory in place", async ({ page }) => {
  await mockTauriIpc(page, { memories: SAMPLE_MEMORIES });
  await page.goto("/");

  const panel = page.locator(".memory-management-panel");
  await panel.getByRole("button", { name: "Show memories" }).click();
  await panel.getByRole("button", { name: "Delete memory: Tea, no sugar." }).click();
  await panel.locator(".memory-delete-confirm").getByRole("button", { name: "Cancel" }).click();

  await expect(panel.locator(".memory-delete-confirm")).toHaveCount(0);
  await expect(panel.getByRole("list", { name: "Stored memories" })).toContainText("Tea, no sugar.");
  await expect(panel.locator(".metric-row")).toContainText("2");
});

// --- ESR-0061 WP3b (EIP-ESR0061-003 6.7): asking Claude -------------------------------------------------------------

async function sendMessage(page, text) {
  await page.getByPlaceholder("Ask Guardian anything...").fill(text);
  await page.getByRole("button", { name: "Send" }).click();
  await expect(page.locator(".conversation-message.guardian")).toHaveCount(1);
}

test("with no Claude key the Ask Claude controls are not shown at all", async ({ page }) => {
  await mockTauriIpc(page);
  await page.goto("/");
  await sendMessage(page, "hello");

  await expect(page.getByRole("button", { name: "Ask Claude about my last message" })).toHaveCount(0);
  await expect(page.locator(".escalation-bar")).toHaveCount(0);
});

test("a profile that may not ask Claude (a Child or Guest) sees no Claude controls", async ({ page }) => {
  await mockTauriIpc(page, { claude: { mayEscalate: false, offerReason: "local_unavailable" } });
  await page.goto("/");
  await sendMessage(page, "hello");

  await expect(page.locator(".escalation-bar")).toHaveCount(0);
  await expect(page.getByRole("dialog")).toHaveCount(0);
});

test("Ask Claude is disabled until there is a message to ask about", async ({ page }) => {
  await mockTauriIpc(page, { claude: {} });
  await page.goto("/");

  await expect(page.getByRole("button", { name: "Ask Claude about my last message" })).toBeDisabled();
  await sendMessage(page, "hello");
  await expect(page.getByRole("button", { name: "Ask Claude about my last message" })).toBeEnabled();
});

test("an offer is shown after a local failure and sends nothing until it is confirmed", async ({ page }) => {
  await mockTauriIpc(page, { claude: { offerReason: "local_unavailable" } });
  await page.goto("/");
  await sendMessage(page, "what is the capital of Peru");

  await expect(page.locator(".escalation-offer")).toContainText("could not answer");
  await page.getByRole("button", { name: "Review and ask Claude" }).click();

  const dialog = page.getByRole("dialog");
  await expect(dialog).toContainText("Send this question to Claude?");
  await expect(dialog).toContainText("over the internet");
  await expect(dialog).toContainText("what is the capital of Peru");
  await expect(dialog).toContainText("This costs money");
  await expect(dialog).toContainText("£29.00");
  await expect(dialog).toContainText("Your saved memory notes will not be sent.");
  expect(await page.evaluate(() => window.__escalateCalls.length)).toBe(0);

  await dialog.getByRole("button", { name: "Cancel" }).click();

  await expect(page.getByRole("dialog")).toHaveCount(0);
  expect(await page.evaluate(() => window.__escalateCalls.length)).toBe(0);
  await expect(page.locator(".claude-badge")).toHaveCount(0);
});

test("confirming sends the offer's token once and labels the answer as Claude's", async ({ page }) => {
  await mockTauriIpc(page, { claude: { offerReason: "research_cue" } });
  await page.goto("/");
  await sendMessage(page, "research solar panels");

  await expect(page.locator(".escalation-offer")).toContainText("more thorough");
  await page.getByRole("button", { name: "Review and ask Claude" }).click();
  await page.getByRole("button", { name: "Send to Claude" }).click();

  const answer = page.locator(".conversation-message.guardian").last();
  await expect(answer).toContainText("Claude says: a considered answer.");
  await expect(answer.locator(".claude-badge")).toHaveText("Claude");
  await expect(page.locator(".claude-badge")).toHaveCount(1);
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(page.locator(".escalation-offer")).toHaveCount(0);
  expect(await page.evaluate(() => window.__escalateCalls)).toEqual(["token-1"]);
});

test("the dialog says when saved memory notes will be sent and warns near the cap", async ({ page }) => {
  await mockTauriIpc(page, { claude: { offerReason: "local_unavailable", sendsMemory: true, warning: true } });
  await page.goto("/");
  await sendMessage(page, "hello");

  await page.getByRole("button", { name: "Review and ask Claude" }).click();

  await expect(page.getByRole("dialog")).toContainText("Your saved memory notes will also be sent.");
  await expect(page.getByRole("dialog").getByRole("alert")).toContainText("80%");
});

test("Ask Claude opens the confirmation for the last message even after a good local answer", async ({ page }) => {
  await mockTauriIpc(page, { claude: {} });
  await page.goto("/");
  await sendMessage(page, "what is two plus two");
  await expect(page.locator(".escalation-offer")).toHaveCount(0);

  await page.getByRole("button", { name: "Ask Claude about my last message" }).click();

  await expect(page.getByRole("dialog")).toContainText("what is two plus two");
  expect(await page.evaluate(() => window.__escalateCalls.length)).toBe(0);
  await page.getByRole("button", { name: "Send to Claude" }).click();
  await expect(page.locator(".claude-badge")).toHaveCount(1);
  expect(await page.evaluate(() => window.__escalateCalls)).toEqual(["token-1"]);
});

test("a failed escalation is shown as an error and ends the offer", async ({ page }) => {
  await mockTauriIpc(page, {
    claude: { offerReason: "local_unavailable", escalateError: "ValueError: This offer has expired or was already used." },
  });
  await page.goto("/");
  await sendMessage(page, "hello");
  await page.getByRole("button", { name: "Review and ask Claude" }).click();

  await page.getByRole("button", { name: "Send to Claude" }).click();

  await expect(page.locator(".conversation-error")).toContainText("Claude did not respond");
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(page.locator(".escalation-offer")).toHaveCount(0);
  await expect(page.locator(".claude-badge")).toHaveCount(0);
});

// --- ESR-0061 WP3c (EIP-ESR0061-003 6.9): local AI setup ------------------------------------------------------------

const notInstalled = {
  status: {
    installed: false,
    running: false,
    version: null,
    models: [],
    activeModelInstalled: false,
    install: {
      url: "https://ollama.com/download",
      installed: false,
      steps: ["Open the Ollama download page.", "Run the installer.", "Come back and press Check again."],
    },
  },
};

test("a healthy machine shows the running version, the active model and the recommendation in use", async ({ page }) => {
  await mockTauriIpc(page);
  await page.goto("/");

  const panel = page.locator(".local-ai-panel");
  await expect(panel).toContainText("Ollama 0.35.0 is running");
  await expect(panel).toContainText("Active model: qwen3.5:4b");
  await expect(panel).toContainText("Chosen for this computer's graphics card (8 GB).");
  await expect(panel.getByRole("status").filter({ hasText: "In use" })).toBeVisible();
  await expect(panel.getByRole("alert")).toHaveCount(0);
});

test("with Ollama not installed the steps are shown and nothing is installed by JARVIS", async ({ page }) => {
  await mockTauriIpc(page, { ollama: notInstalled });
  await page.goto("/");

  const panel = page.locator(".local-ai-panel");
  await expect(panel).toContainText("Ollama is not installed");
  await expect(panel.getByRole("listitem")).toHaveCount(3);
  await panel.getByRole("button", { name: "Open download page" }).click();
  expect(await page.evaluate(() => window.__ollamaCalls)).toEqual([["open-download-page"]]);
  await expect(panel.getByRole("button", { name: /Download and use/ })).toHaveCount(0);
});

test("installed but not running is told apart from not installed", async ({ page }) => {
  await mockTauriIpc(page, {
    ollama: { status: { ...notInstalled.status, installed: true, install: { ...notInstalled.status.install, installed: true } } },
  });
  await page.goto("/");

  const panel = page.locator(".local-ai-panel");
  await expect(panel).toContainText("installed but not running");
  await expect(panel.getByRole("button", { name: "Open download page" })).toHaveCount(0);
  await expect(panel.getByRole("button", { name: "Check again" })).toBeVisible();
});

test("downloading the recommended model asks for exactly that model and shows progress and a cancel", async ({ page }) => {
  await mockTauriIpc(page, {
    profiles: [{ id: "a1", displayName: "Robert", role: "Administrator", createdAt: "2026-01-01T00:00:00Z" }],
    activeProfile: { id: "a1", displayName: "Robert", role: "Administrator", createdAt: "2026-01-01T00:00:00Z" },
    ollama: {
      status: { models: [], activeModel: "qwen3.5:2b", activeModelInstalled: false },
      recommendation: {
        primary: { tag: "qwen3.5:4b", label: "Qwen3.5 4B (balanced)", downloadGb: 3.3, note: "n", installed: false },
      },
    },
  });
  await page.goto("/");
  const panel = page.locator(".local-ai-panel");

  await panel.getByRole("button", { name: "Download and use" }).first().click();

  await expect(panel.getByRole("progressbar", { name: "Model download progress" })).toBeVisible();
  expect(await page.evaluate(() => window.__ollamaCalls)).toEqual([["pull", "qwen3.5:4b"]]);
  await panel.getByRole("button", { name: "Cancel download" }).click();
  await expect(panel.getByRole("progressbar")).toHaveCount(0);
  expect(await page.evaluate(() => window.__ollamaCalls)).toEqual([["pull", "qwen3.5:4b"], ["cancel"]]);
});

test("a download in progress is shown with its percentage", async ({ page }) => {
  await mockTauriIpc(page, {
    ollama: { status: { pull: { active: true, model: "qwen3.5:4b", completed: 50, total: 100, status: "pulling" } } },
  });
  await page.goto("/");

  const bar = page.locator(".local-ai-panel").getByRole("progressbar");
  await expect(bar).toHaveAttribute("aria-valuenow", "50");
  await expect(page.locator(".local-ai-panel")).toContainText("50%");
});

test("a model already downloaded can be switched to", async ({ page }) => {
  await mockTauriIpc(page, {
    profiles: [{ id: "a1", displayName: "Robert", role: "Administrator", createdAt: "2026-01-01T00:00:00Z" }],
    activeProfile: { id: "a1", displayName: "Robert", role: "Administrator", createdAt: "2026-01-01T00:00:00Z" },
    ollama: {
      status: { models: ["qwen3.5:2b", "qwen3.5:4b"], activeModel: "qwen3.5:2b" },
      recommendation: {
        primary: { tag: "qwen3.5:4b", label: "Qwen3.5 4B (balanced)", downloadGb: 3.3, note: "n", installed: true },
      },
    },
  });
  await page.goto("/");
  const panel = page.locator(".local-ai-panel");

  await panel.getByRole("button", { name: "Use this model" }).first().click();

  expect(await page.evaluate(() => window.__ollamaCalls)).toEqual([["use", "qwen3.5:4b"]]);
  await expect(panel).toContainText("Active model: qwen3.5:4b");
});

test("not enough disk space is shown and blocks downloading the recommended model", async ({ page }) => {
  await mockTauriIpc(page, {
    ollama: {
      recommendation: {
        primary: { tag: "qwen3.5:4b", label: "Qwen3.5 4B (balanced)", downloadGb: 3.3, note: "n", installed: false },
        diskOk: false,
        needsDiskGb: 4,
        hardware: { system: "Windows", ramGb: 32, gpuGb: 8, unifiedMemory: false, freeDiskGb: 1.5 },
      },
    },
  });
  await page.goto("/");
  const panel = page.locator(".local-ai-panel");

  await expect(panel.getByRole("alert")).toContainText("Not enough free disk space");
  await expect(panel.getByRole("button", { name: "Download and use" }).first()).toBeDisabled();
});

test("a Child profile sees the setup but cannot download or change the model", async ({ page }) => {
  await mockTauriIpc(page, {
    profiles: [{ id: "p1", displayName: "Young", role: "Child", createdAt: "2026-01-01T00:00:00Z" }],
    activeProfile: { id: "p1", displayName: "Young", role: "Child", createdAt: "2026-01-01T00:00:00Z" },
    ollama: {
      status: { models: [], activeModel: "qwen3.5:2b", activeModelInstalled: false },
      recommendation: {
        primary: { tag: "qwen3.5:4b", label: "Qwen3.5 4B (balanced)", downloadGb: 3.3, note: "n", installed: false },
      },
    },
  });
  await page.goto("/");
  const panel = page.locator(".local-ai-panel");

  await expect(panel).toContainText("Only an Administrator or Adult profile can download or change models.");
  await expect(panel.getByRole("button", { name: "Download and use" }).first()).toBeDisabled();
});

test("a model set by the environment variable says that it overrides the screen", async ({ page }) => {
  await mockTauriIpc(page, { ollama: { status: { modelSource: "environment" } } });
  await page.goto("/");

  await expect(page.locator(".local-ai-panel")).toContainText("JARVIS_OLLAMA_MODEL");
});

test("a failed status read is shown honestly rather than as a healthy panel", async ({ page }) => {
  await mockTauriIpc(page);
  await page.addInitScript(() => {
    const original = window.__TAURI_INTERNALS__.invoke;
    window.__TAURI_INTERNALS__.invoke = (cmd, args) =>
      cmd === "ollama_status" ? Promise.reject(new Error("backend unavailable")) : original(cmd, args);
  });
  await page.goto("/");

  await expect(page.locator(".local-ai-panel").getByRole("alert")).toContainText("Could not read the local AI status");
});
