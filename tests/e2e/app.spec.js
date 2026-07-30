import { test, expect } from "@playwright/test";

// Mocks Tauri's IPC layer directly (window.__TAURI_INTERNALS__.invoke),
// matching this repository's own prior ad hoc verification approach
// (EBG-0072/EBG-0073) and the mechanism `@tauri-apps/api/core`'s invoke()
// actually calls under the hood (confirmed by direct source read,
// EIP-ESR0032-002). There is no live backend and no bundled Tauri binary
// in this test - it drives the Vite dev server's React app directly.
async function mockTauriIpc(page, { speakResult } = {}) {
  await page.addInitScript(
    ({ platformStatus, knowledgeGraph, speakResult }) => {
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
