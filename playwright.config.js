import { defineConfig, devices } from "@playwright/test";

// Drives the Vite dev server directly (the same devUrl configured in
// src-tauri/tauri.conf.json), not a bundled Tauri binary - there is no
// display/webview stack in CI, and this repository has no committed
// native-webview E2E harness (EIP-ESR0032-002's own disclosed scope
// boundary). Tauri's IPC layer is mocked per-test via page.addInitScript,
// matching this project's own prior ad hoc verification approach
// (EBG-0072/EBG-0073).
export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:1420",
    trace: "retain-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: {
    command: "npm run dev",
    url: "http://127.0.0.1:1420",
    reuseExistingServer: !process.env.CI,
    timeout: 30_000,
  },
});
