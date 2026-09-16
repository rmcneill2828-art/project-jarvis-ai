import { defineConfig, devices } from "@playwright/test";

// Drives the Vite dev server (the same devUrl port configured in
// src-tauri/tauri.conf.json), not a bundled Tauri binary - there is no
// display/webview stack in CI, and this repository has no committed
// native-webview E2E harness (EIP-ESR0032-002's own disclosed scope
// boundary). Tauri's IPC layer is mocked per-test via page.addInitScript,
// matching this project's own prior ad hoc verification approach
// (EBG-0072/EBG-0073).
//
// EBG-0129 (ESR-0058 WP5): the dev server's on-demand per-request module
// transform, combined with Playwright's default parallel workers, produced
// a genuine cold-start race (a real, reproduced failure pattern: 12
// failed/6 passed at default parallelism, 17 passed/1 failed sequentially,
// the one failure an initial page.goto() timeout, not an assertion
// failure). A build+preview production server was tried first and
// reverted: it serves only bundled output, but
// tests/e2e/animationScheduler.spec.js intentionally dynamic-imports the
// raw `/src/animationScheduler.js` source path to exercise that module in
// isolation (EBG-0081 Question 1), which a production build does not
// serve - that approach traded the original failure for a different,
// equally real one (3 new failures). The actual fix keeps the dev server
// and instead warms it with one sequential real-browser navigation before
// any parallel worker starts (see tests/e2e/global-setup.js), so Vite's
// module transforms are already cached when concurrent workers begin.
export default defineConfig({
  testDir: "./tests/e2e",
  globalSetup: "./tests/e2e/global-setup.js",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:1420",
    trace: "retain-on-failure",
    actionTimeout: 15_000,
    navigationTimeout: 15_000,
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
