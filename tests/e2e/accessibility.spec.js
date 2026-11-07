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

async function installMock(page, profile, { others = [], consent = null, disclosure = null, safety = null } = {}) {
  await page.addInitScript(
    ({ profile, others, consent, disclosure, safety, platform, ollama, recommendation }) => {
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
            list_profiles: { profiles: [profile, ...others] },
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
            // No PIN yet, so Settings shows the warning and the form to set one (WP6a).
            pin_status: { set: false, locked: false, lockedForSeconds: 0 },
            // Claude for a Child (WP6c): allowed by a grown-up, not yet acknowledged.
            consent_status: consent || { profileId: "c", recorded: false, acknowledged: false, allowed: false },
            // The Child's first-use explanation and the safety summary (WP6d).
            disclosure_status: disclosure || { required: false, acknowledged: true, acknowledgedAt: null },
            safety_summary: safety || { profiles: [] },
          };
          if (cmd in answers) return Promise.resolve(structuredClone(answers[cmd]));
          if (cmd === "plugin:event|listen") return Promise.resolve(0);
          return Promise.reject(new Error(`not mocked: ${cmd}`));
        },
      };
    },
    { profile, others, consent, disclosure, safety, platform: PLATFORM, ollama: OLLAMA_STATUS, recommendation: RECOMMENDATION },
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
        if (cmd === "select_profile") return Promise.resolve({ ...state.profile, pinNotices: [] });
        if (cmd === "pin_status") return Promise.resolve({ set: Boolean(state.pinSet), locked: false, lockedForSeconds: 0 });
        if (cmd === "set_pin") {
          state.pinSet = true;
          return Promise.resolve({ set: true, locked: false, lockedForSeconds: 0 });
        }
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
  const current = page.getByRole("list", { name: "Setup steps" }).locator('[aria-current="step"]');
  await expect(current).toContainText("Administrator PIN");
  await page.waitForTimeout(300);
  await expectNoSeriousViolations(page, "first run, PIN step");

  await page.getByLabel("New PIN (6 to 12 digits)").fill("246810");
  await page.getByLabel("The same PIN again").fill("246810");
  await page.getByRole("button", { name: "Set PIN and continue" }).click();
  await expect(current).toContainText("AI on this computer");
  await page.waitForTimeout(300);
  await expectNoSeriousViolations(page, "first run, AI step");

  await page.getByRole("button", { name: "Do this later" }).click();
  await page.waitForTimeout(300);
  await expectNoSeriousViolations(page, "first run, Claude step");

  await page.getByRole("button", { name: "Skip for now" }).click();
  await expect(page.getByRole("list", { name: "What is ready" })).toBeVisible();
  await expectNoSeriousViolations(page, "first run, ready step");
});

test("axe: the Administrator PIN prompt has no serious or critical violation", async ({ page }) => {
  await page.addInitScript(() => {
    window.__TAURI_EVENT_PLUGIN_INTERNALS__ = { unregisterListener: () => {} };
    const child = { id: "c1", displayName: "Sam", role: "Child", createdAt: "2026-10-01T00:00:00Z" };
    const admin = { id: "a1", displayName: "Robert", role: "Administrator", createdAt: "2026-10-01T00:00:00Z" };
    window.__TAURI_INTERNALS__ = {
      transformCallback: () => 0,
      invoke: (cmd) => {
        if (cmd === "list_profiles") return Promise.resolve({ profiles: [admin, child] });
        if (cmd === "active_profile") return Promise.resolve({ profile: child });
        if (cmd === "profile_switch_requirements") {
          return Promise.resolve({ pinRequired: true, set: true, locked: false, lockedForSeconds: 0 });
        }
        if (cmd === "select_profile") return Promise.reject(new Error("PermissionError: That PIN is not right. Try again."));
        if (cmd === "plugin:event|listen") return Promise.resolve(0);
        return Promise.reject(new Error("not mocked: " + cmd));
      },
    };
  });
  await page.goto("/");
  await page.getByRole("button", { name: "Switch Guardian profile" }).click();
  await page.getByRole("list", { name: "Other profiles" }).getByRole("button", { name: /Robert/ }).click();
  const dialog = page.getByRole("dialog", { name: "Administrator PIN needed" });
  await expect(dialog).toBeVisible();
  await expectNoSeriousViolations(page, "PIN prompt");

  await dialog.getByLabel("PIN").fill("123456");
  await dialog.getByRole("button", { name: "Switch" }).click();
  await expect(dialog.getByRole("alert")).toBeVisible();
  await expectNoSeriousViolations(page, "PIN prompt with a refusal");
});

// --- ESR-0061 WP6c: Claude for a Child -------------------------------------------------------------------------------

const WAITING_CONSENT = {
  profileId: "c",
  recorded: true,
  recordedBy: "Robert",
  recordedAt: "2026-11-07T15:00:00+00:00",
  acknowledged: false,
  acknowledgedAt: null,
  allowed: false,
};

test("axe: the child's 'You can ask Claude' card has no serious or critical violation", async ({ page }) => {
  await installMock(page, PROFILES.Child, { consent: WAITING_CONSENT });
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "You can ask Claude" })).toBeVisible();
  await expectNoSeriousViolations(page, "Child acknowledgement card");
});

test("axe: Settings with a child to allow has no serious or critical violation", async ({ page }) => {
  await installMock(page, PROFILES.Administrator, { others: [PROFILES.Child], consent: WAITING_CONSENT });
  await page.goto("/");
  await openView(page, "Settings");
  await expect(page.getByRole("heading", { name: "Claude for a child" })).toBeVisible();
  await page.waitForTimeout(300);
  await expectNoSeriousViolations(page, "Settings, Claude for a child");
});

// --- ESR-0061 WP6d: the Child's first-use explanation and Children and safety ------------------------------------

test("axe: the child's first-use explanation has no serious or critical violation", async ({ page }) => {
  await installMock(page, PROFILES.Child, { disclosure: { required: true, acknowledged: false, acknowledgedAt: null } });
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Before you start" })).toBeVisible();
  await expectNoSeriousViolations(page, "Child first-use explanation");
});

test("axe: Children and safety with stopped turns has no serious or critical violation", async ({ page }) => {
  await installMock(page, PROFILES.Administrator, {
    others: [PROFILES.Child],
    safety: {
      profiles: [
        {
          profileId: PROFILES.Child.id,
          displayName: PROFILES.Child.displayName,
          role: "Child",
          events: [{ day: "2026-11-07", category: "violent_crimes", direction: "input", count: 2 }],
        },
      ],
    },
  });
  await page.goto("/");
  await openView(page, "Settings");
  await expect(page.getByRole("heading", { name: "Children and safety" })).toBeVisible();
  await expect(page.getByRole("table")).toBeVisible();
  await page.waitForTimeout(300);
  await expectNoSeriousViolations(page, "Settings, Children and safety");
});
