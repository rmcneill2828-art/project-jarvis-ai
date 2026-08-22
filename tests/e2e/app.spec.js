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
      const state = { profiles: [...profiles], active: activeProfile };
      let nextId = state.profiles.length + 1;

      window.__TAURI_INTERNALS__ = {
        invoke: (cmd, args) => {
          if (cmd === "platform_status") return Promise.resolve({ ...platformStatus, transcriptionAvailable });
          if (cmd === "knowledge_graph") return Promise.resolve(knowledgeGraph);
          if (cmd === "send_message") {
            const message = args && args.message ? args.message : "";
            return Promise.resolve({ message: `local-echo: ${message}`, provider: "local-echo" });
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
