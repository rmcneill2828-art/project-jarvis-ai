import { test, expect } from "@playwright/test";

// Exercises src/animationScheduler.js's own contract in isolation (EBG-0081
// Question 1), separately from the app-level tests in app.spec.js that
// mount GuardianOrbGraph indirectly. requestAnimationFrame only exists in a
// real browser (not plain Node), so this runs in Playwright's browser
// context rather than a Node-only unit test.

test("animationScheduler drives multiple subscribers from a single requestAnimationFrame loop", async ({ page }) => {
  await page.goto("/");

  // Real browser rAF timing is too jittery (headless throttling, background
  // tabs) for a wall-clock-based frame count to be a reliable assertion, so
  // this replaces window.requestAnimationFrame with a fully deterministic
  // fake that only ever fires when this test explicitly steps it - proving
  // the scheduler's actual contract (one underlying raf call per step,
  // shared across however many subscribers are registered) without any
  // dependency on real timing.
  const result = await page.evaluate(async () => {
    const runWithFakeRaf = async (subscriberCount) => {
      const originalRaf = window.requestAnimationFrame;
      const originalCancel = window.cancelAnimationFrame;
      let nextId = 1;
      let pending = null;
      let rafCallCount = 0;
      window.requestAnimationFrame = (cb) => {
        rafCallCount += 1;
        pending = cb;
        return nextId++;
      };
      window.cancelAnimationFrame = () => {
        pending = null;
      };

      // A fresh module instance per run, so each run starts with zero
      // subscribers/no leftover scheduler state from the previous run -
      // cache-busted via a dummy query param.
      const { subscribe } = await import(`/src/animationScheduler.js?run=${subscriberCount}`);

      let totalCalls = 0;
      const unsubscribes = Array.from({ length: subscriberCount }, () =>
        subscribe(() => {
          totalCalls += 1;
        }),
      );

      const STEPS = 5;
      for (let i = 0; i < STEPS; i += 1) {
        const callback = pending;
        pending = null;
        if (callback) callback(performance.now());
      }

      unsubscribes.forEach((unsubscribe) => unsubscribe());
      window.requestAnimationFrame = originalRaf;
      window.cancelAnimationFrame = originalCancel;

      return { rafCallCount, totalCalls };
    };

    const oneSubscriber = await runWithFakeRaf(1);
    const twoSubscribers = await runWithFakeRaf(2);

    return { oneSubscriber, twoSubscribers };
  });

  // Both subscribers in the two-subscriber run actually received every
  // stepped frame...
  expect(result.oneSubscriber.totalCalls).toBe(5);
  expect(result.twoSubscribers.totalCalls).toBe(10);
  // ...while the scheduler's own requestAnimationFrame call count is
  // identical regardless of subscriber count - one shared loop, not one per
  // subscriber.
  expect(result.twoSubscribers.rafCallCount).toBe(result.oneSubscriber.rafCallCount);
});

test("animationScheduler isolates a throwing subscriber from other subscribers", async ({ page }) => {
  await page.goto("/");

  const result = await page.evaluate(async () => {
    const { subscribe } = await import("/src/animationScheduler.js");

    let goodCalls = 0;
    const unsubscribeBad = subscribe(() => {
      throw new Error("boom");
    });
    const unsubscribeGood = subscribe(() => {
      goodCalls += 1;
    });

    await new Promise((resolve) => setTimeout(resolve, 100));

    unsubscribeBad();
    unsubscribeGood();

    return { goodCalls };
  });

  expect(result.goodCalls).toBeGreaterThan(0);
});

test("animationScheduler stops its internal loop once the last subscriber unsubscribes", async ({ page }) => {
  await page.goto("/");

  const result = await page.evaluate(async () => {
    const { subscribe } = await import("/src/animationScheduler.js");

    const unsubscribe = subscribe(() => {});
    await new Promise((resolve) => setTimeout(resolve, 50));
    unsubscribe();

    let rafCallCountAfterStop = 0;
    const originalRaf = window.requestAnimationFrame.bind(window);
    window.requestAnimationFrame = (cb) => {
      rafCallCountAfterStop += 1;
      return originalRaf(cb);
    };

    await new Promise((resolve) => setTimeout(resolve, 100));

    window.requestAnimationFrame = originalRaf;

    return { rafCallCountAfterStop };
  });

  // With zero subscribers, the scheduler's own loop must not still be
  // calling requestAnimationFrame - the monkey-patched call count set up
  // strictly after the last unsubscribe must stay at zero.
  expect(result.rafCallCountAfterStop).toBe(0);
});
