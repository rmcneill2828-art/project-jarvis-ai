import { test, expect } from "@playwright/test";

// Mocks Tauri's IPC layer directly (window.__TAURI_INTERNALS__.invoke),
// matching this repository's own prior ad hoc verification approach
// (EBG-0072/EBG-0073) and the mechanism `@tauri-apps/api/core`'s invoke()
// actually calls under the hood (confirmed by direct source read,
// EIP-ESR0032-002). There is no live backend and no bundled Tauri binary
// in this test - it drives the Vite dev server's React app directly.
async function mockTauriIpc(page, { speakResult, profiles = [], activeProfile = null } = {}) {
  await page.addInitScript(
    ({ platformStatus, knowledgeGraph, speakResult, profiles, activeProfile }) => {
      // Stateful, in-page mock (EIP-ESR0046-001): list_profiles/active_profile
      // read this state, create_profile/select_profile mutate it - a real
      // Tauri backend behaves the same way, just persisted to SQLite instead
      // of an in-memory closure.
      const state = { profiles: [...profiles], active: activeProfile };
      let nextId = state.profiles.length + 1;

      window.__TAURI_INTERNALS__ = {
        invoke: (cmd, args) => {
          if (cmd === "platform_status") return Promise.resolve(platformStatus);
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
      },
      speakResult,
      profiles,
      activeProfile,
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
