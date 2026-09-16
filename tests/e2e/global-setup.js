import { chromium } from "@playwright/test";

// EBG-0129 (ESR-0058 WP5): the reproduced race (12 failed/6 passed at
// default parallelism, 17 passed/1 failed sequentially, the one failure an
// initial page.goto() timeout) is a cold-start problem, not a real product
// defect - Vite's dev server transforms each module the first time it is
// requested. When Playwright's parallel workers all issue their first
// page.goto() at once, right after the dev server reports itself ready,
// several of them race to trigger the same first-ever transform of the
// app's module graph (main.jsx -> App.jsx -> GuardianOrbGraph.jsx ->
// animationScheduler.js, etc), and the slowest one can miss the
// navigation timeout.
//
// A genuine production build+preview was tried first (serves pre-built
// static output, no per-request transform work at all) but was reverted:
// tests/e2e/animationScheduler.spec.js deliberately dynamic-imports the
// raw `/src/animationScheduler.js` source path to exercise that module in
// isolation (EBG-0081 Question 1) - a real, intentional test design this
// project already had, and a production build does not serve raw
// `/src/*` paths, so that approach traded one real failure mode for
// another instead of fixing it.
//
// This performs one sequential real-browser navigation to the app root
// before any parallel worker starts, so Vite pre-transforms and caches
// the whole module graph the tests actually exercise. Concurrent workers
// then hit an already-warm dev server instead of a cold one.
export default async function globalSetup(config) {
  const { baseURL } = config.projects[0].use;
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    await page.goto(baseURL, { waitUntil: "networkidle" });
  } finally {
    await browser.close();
  }
}
