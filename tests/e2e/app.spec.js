import { test, expect } from "@playwright/test";

// Mocks Tauri's IPC layer directly (window.__TAURI_INTERNALS__.invoke),
// matching this repository's own prior ad hoc verification approach
// (EBG-0072/EBG-0073) and the mechanism `@tauri-apps/api/core`'s invoke()
// actually calls under the hood (confirmed by direct source read,
// EIP-ESR0032-002). There is no live backend and no bundled Tauri binary
// in this test - it drives the Vite dev server's React app directly.
async function mockTauriIpc(page, { onSendMessage } = {}) {
  await page.addInitScript(
    ({ platformStatus, knowledgeGraph }) => {
      window.__TAURI_INTERNALS__ = {
        invoke: (cmd, args) => {
          if (cmd === "platform_status") return Promise.resolve(platformStatus);
          if (cmd === "knowledge_graph") return Promise.resolve(knowledgeGraph);
          if (cmd === "send_message") {
            const message = args && args.message ? args.message : "";
            return Promise.resolve({ message: `local-echo: ${message}`, provider: "local-echo" });
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
