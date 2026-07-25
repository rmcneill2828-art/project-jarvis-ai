// Shared UXP animation clock (EBG-0081 Question 1). Any continuously-
// animated element registers a callback here instead of running its own
// independent requestAnimationFrame loop, so the whole UXP drives its
// animations from a single rAF call regardless of how many elements are
// animating. The loop itself only runs while at least one subscriber is
// registered - it starts on the first subscribe and stops on the last
// unsubscribe, rather than idling forever in the background.

const subscribers = new Set();
let frameId = null;

function frame(now) {
  frameId = requestAnimationFrame(frame);
  for (const callback of subscribers) {
    try {
      callback(now);
    } catch (error) {
      // A subscriber's own bug must not silently stop every other
      // subscriber's animation - this shared loop is more fragile than
      // each element running its own private rAF, so failures here are
      // isolated and surfaced rather than left to propagate.
      console.error("animationScheduler: subscriber callback threw", error);
    }
  }
}

export function subscribe(callback) {
  subscribers.add(callback);
  if (frameId === null) {
    frameId = requestAnimationFrame(frame);
  }
  return () => {
    subscribers.delete(callback);
    if (subscribers.size === 0 && frameId !== null) {
      cancelAnimationFrame(frameId);
      frameId = null;
    }
  };
}
