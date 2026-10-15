import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

// ESR-0061 WP4d, EIP-ESR0061-004 item 6.10: axe checks every view and must
// report no serious or critical violation. The page is driven by the same
// in-page IPC mock as app.spec.js, reduced to what the views need to render.

const PROFILES = {
  Administrator: { id: "a1", displayName: "Robert", role: "Administrator", createdAt: "2026-01-01T00:00:00Z" },
  Child: { id: "c1", displayName: "Sam", role: "Child", createdAt: "2026-01-01T00:00:00Z" },
};

const PLATFORM = {
  state: "Running",
  runtimeHealth: "Healthy",
  providerConnected: "Online",
  memoryConnected: "Online",
  transcriptionAvailable: true,
  speechAvailable: true,
  providers: ["ollama"],
  policyEngine: "TrustTierPolicy",
};

const OLLAMA_STATUS = {
  installed: true,
  running: true,
  version: "0.35.0",
  endpoint: "http://localhost:11434",
  models: ["qwen3.5:4b"],
  activeModel: "qwen3.5:4b",
  activeModelInstalled: true,
  modelSource: "default",
  pull: { active: false, model: null, completed: 0, total: 0, status: "idle" },
};

const RECOMMENDATION = {
  hardware: { system: "Windows", ramGb: 32, gpuGb: 8, unifiedMemory: false, freeDiskGb: 25 },
  primary: { tag: "qwen3.5:4b", label: "Qwen3.5 4B (balanced)", downloadGb: 3.3, note: "Balanced.", installed: true },
  fallback: { tag: "qwen3.5:2b", label: "Qwen3.5 2B (light)", downloadGb: 2.7, note: "Light.", installed: false },
  reason: "Chosen for this computer's graphics card (8 GB).",
  belowMinimum: false,
  needsDiskGb: 4,
  diskOk: true,
  models: [],
};

async function installMock(page, profile) {
  await page.addInitScript(
    ({ profile, platform, ollama, recommendation }) => {
      window.__callbacks = {};
      window.__TAURI_EVENT_PLUGIN_INTERNALS__ = { unregisterListener: () => {} };
      window.__TAURI_INTERNALS__ = {
        transformCallback: (callback) => {
          const id = Math.floor(Math.random() * 1e9);
          window.__callbacks[id] = callback;
          return id;
        },
        invoke: (cmd) => {
          const answers = {
            platform_status: platform,
            knowledge_graph: {
              nodes: [
                { id: "n1", label: "Node 1" },
                { id: "n2", label: "Node 2" },
              ],
              edges: [{ source: "n1", target: "n2" }],
              active_clusters: [],
            },
            list_profiles: { profiles: [profile] },
            active_profile: { profile },
            list_agents: { agents: ["gia-observability"] },
            memory_status: { recordCount: 2 },
            list_memory: {
              records: [{ id: "m1", content: "Tea, no sugar.", createdAt: "2026-09-01T10:00:00+00:00", consentDecisionId: "d" }],
            },
            provider_status: {
              claude: {
                configured: true,
                model: "claude-sonnet-5-5",
                mayEscalate: ["Administrator", "Adult"].includes(profile.role),
                allowance: null,
              },
            },
            ollama_status: ollama,
            ollama_recommendation: recommendation,
            claude_key_status: { configured: false, source: "none", storeAvailable: true },
            get_settings: { auditRetentionDays: 90, allowedRetentionDays: [30, 90, 365], lastPrune: null },
          };
          if (cmd in answers) return Promise.resolve(structuredClone(answers[cmd]));
          if (cmd === "plugin:event|listen") return Promise.resolve(0);
          return Promise.reject(new Error(`not mocked: ${cmd}`));
        },
      };
    },
    { profile, platform: PLATFORM, ollama: OLLAMA_STATUS, recommendation: RECOMMENDATION },
  );
}

const openView = (page, name) =>
  page.getByRole("navigation", { name: "Views" }).getByRole("button", { name, exact: true }).click();

async function expectNoSeriousViolations(page, label) {
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]).analyze();
  const blocking = results.violations.filter((violation) => ["serious", "critical"].includes(violation.impact));
  const summary = blocking.map((violation) => ({
    id: violation.id,
    impact: violation.impact,
    nodes: violation.nodes.slice(0, 4).map((node) => node.target.join(" ")),
  }));
  expect(summary, `${label}: serious or critical accessibility violations`).toEqual([]);
}

const ADMIN_VIEWS = ["Guardian", "Memory", "Knowledge", "Agents", "AI models", "Settings", "System"];

for (const view of ADMIN_VIEWS) {
  test(`axe: the ${view} view has no serious or critical violation`, async ({ page }) => {
    await installMock(page, PROFILES.Administrator);
    await page.goto("/");
    await expect(page.getByRole("navigation", { name: "Views" })).toBeVisible();
    await openView(page, view);
    // Let the view read its data before it is judged.
    await page.waitForTimeout(400);
    await expectNoSeriousViolations(page, view);
  });
}

test("axe: a Child's Guardian and Memory views have no serious or critical violation", async ({ page }) => {
  await installMock(page, PROFILES.Child);
  await page.goto("/");
  await expect(page.getByRole("navigation", { name: "Views" })).toBeVisible();
  await expectNoSeriousViolations(page, "Child Guardian");
  await openView(page, "Memory");
  await page.waitForTimeout(300);
  await expectNoSeriousViolations(page, "Child Memory");
});

test("axe: every view at the smallest window has no serious or critical violation", async ({ page }) => {
  await page.setViewportSize({ width: 960, height: 640 });
  await installMock(page, PROFILES.Administrator);
  await page.goto("/");
  await expect(page.getByRole("navigation", { name: "Views" })).toBeVisible();
  for (const view of ADMIN_VIEWS) {
    await openView(page, view);
    await page.waitForTimeout(300);
    await expectNoSeriousViolations(page, `${view} at 960 x 640`);
  }
});

test("axe: the first-run steps have no serious or critical violation", async ({ page }) => {
  await page.addInitScript(() => {
    window.__TAURI_EVENT_PLUGIN_INTERNALS__ = { unregisterListener: () => {} };
    const state = { profile: null };
    window.__TAURI_INTERNALS__ = {
      transformCallback: () => 0,
      invoke: (cmd, args) => {
        if (cmd === "list_profiles") return Promise.resolve({ profiles: state.profile ? [state.profile] : [] });
        if (cmd === "active_profile") return Promise.resolve({ profile: state.profile });
        if (cmd === "create_profile") {
          state.profile = { id: "n1", displayName: args.displayName, role: args.role, createdAt: "2026-10-15T00:00:00Z" };
          return Promise.resolve(state.profile);
        }
        if (cmd === "select_profile") return Promise.resolve(state.profile);
        if (cmd === "ollama_status") {
          return Promise.resolve({
            installed: false,
            running: false,
            version: null,
            models: [],
            activeModelInstalled: false,
            install: { url: "https://ollama.com/download", installed: false, steps: ["Open the page."] },
          });
        }
        if (cmd === "ollama_recommendation") return Promise.reject(new Error("not running"));
        if (cmd === "claude_key_status") return Promise.resolve({ configured: false, source: "none", storeAvailable: true });
        if (cmd === "plugin:event|listen") return Promise.resolve(0);
        return Promise.reject(new Error("not mocked: " + cmd));
      },
    };
  });
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1, name: "Set up JARVIS" })).toBeVisible();
  await expectNoSeriousViolations(page, "first run, profile step");

  await page.getByPlaceholder("Your name").fill("Robert");
  await page.getByRole("button", { name: "Create profile" }).click();
  await expect(page.getByRole("list", { name: "Setup steps" }).locator('[aria-current="step"]')).toContainText("AI on this computer");
  await page.waitForTimeout(300);
  await expectNoSeriousViolations(page, "first run, AI step");

  await page.getByRole("button", { name: "Do this later" }).click();
  await page.waitForTimeout(300);
  await expectNoSeriousViolations(page, "first run, Claude step");

  await page.getByRole("button", { name: "Skip for now" }).click();
  await expect(page.getByRole("list", { name: "What is ready" })).toBeVisible();
  await expectNoSeriousViolations(page, "first run, ready step");
});
