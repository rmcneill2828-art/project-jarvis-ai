import { useEffect, useRef, useState } from "react";

import { subscribe } from "./animationScheduler.js";
import { minFrameIntervalMs } from "./orbState.js";

// The presence Orb (ESR-0061 WP4b, EIP-ESR0061-004 item 6.3): a 240-point
// sphere on Canvas 2D, time-based, driven by the shared animation clock. It
// reads nothing from the repository. The state arrives as a prop and is also
// written as text in a live region by the caller; this component only draws.

const POINTS = 240;
const TWO_PI = Math.PI * 2;

const PARAMS = {
  idle: { spin: 0.14, breathe: 0.025, hz: 0.28, wave: 0, rings: 0, ca: [65, 224, 240], cb: [143, 123, 255], glow: 0.55 },
  listening: { spin: 0.05, breathe: 0.02, hz: 0.6, wave: 0, rings: -1, ca: [83, 224, 160], cb: [65, 224, 240], glow: 0.7 },
  thinking: { spin: 0.95, breathe: 0.03, hz: 1.1, wave: 0.07, rings: 0, ca: [143, 123, 255], cb: [255, 120, 220], glow: 0.8 },
  speaking: { spin: 0.2, breathe: 0.07, hz: 3.1, wave: 0.03, rings: 1, ca: [255, 196, 107], cb: [65, 224, 240], glow: 0.85 },
  offline: { spin: 0, breathe: 0, hz: 0, wave: 0, rings: 0, ca: [120, 128, 150], cb: [255, 107, 122], glow: 0.22 },
};

// A sphere of points spread evenly (a Fibonacci spiral), each joined to its two
// nearest neighbours. Built once; it does not depend on any data.
function buildSphere() {
  const points = [];
  for (let i = 0; i < POINTS; i += 1) {
    const y = 1 - (i / (POINTS - 1)) * 2;
    const r = Math.sqrt(1 - y * y);
    const theta = i * 2.399963;
    points.push([Math.cos(theta) * r, y, Math.sin(theta) * r]);
  }
  const links = [];
  for (let i = 0; i < POINTS; i += 1) {
    const nearest = [];
    for (let j = 0; j < POINTS; j += 1) {
      if (i === j) continue;
      const dx = points[i][0] - points[j][0];
      const dy = points[i][1] - points[j][1];
      const dz = points[i][2] - points[j][2];
      nearest.push([dx * dx + dy * dy + dz * dz, j]);
    }
    nearest.sort((a, b) => a[0] - b[0]);
    for (let k = 0; k < 2; k += 1) if (i < nearest[k][1]) links.push([i, nearest[k][1]]);
  }
  return { points, links };
}

let sphere = null;
const spriteCache = new Map();

function lerp(a, b, k) {
  return a + (b - a) * k;
}

function mix(a, b, t) {
  return [Math.round(lerp(a[0], b[0], t)), Math.round(lerp(a[1], b[1], t)), Math.round(lerp(a[2], b[2], t))];
}

function sprite(color) {
  const key = color.join(",");
  if (spriteCache.has(key)) return spriteCache.get(key);
  const canvas = document.createElement("canvas");
  canvas.width = 32;
  canvas.height = 32;
  const g = canvas.getContext("2d");
  const gradient = g.createRadialGradient(16, 16, 0, 16, 16, 16);
  gradient.addColorStop(0, "rgba(255,255,255,1)");
  gradient.addColorStop(0.25, `rgba(${key},0.9)`);
  gradient.addColorStop(1, `rgba(${key},0)`);
  g.fillStyle = gradient;
  g.fillRect(0, 0, 32, 32);
  spriteCache.set(key, canvas);
  return canvas;
}

function prefersReducedMotion() {
  return typeof window !== "undefined" && window.matchMedia
    ? window.matchMedia("(prefers-reduced-motion: reduce)").matches
    : false;
}

function drawOrb(ctx, canvas, cur, state, angle, seconds, still, dpr) {
  const { points, links } = sphere;
  const W = canvas.width;
  const c = W / 2;
  const R = W * 0.36;
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, W, W);

  const speakingWobble = state === "speaking" ? cur.breathe * 0.6 * Math.sin(seconds * 7.3) * Math.sin(seconds * 2.1) : 0;
  const breathe = 1 + cur.breathe * Math.sin(seconds * cur.hz * TWO_PI) + speakingWobble;
  const core = ctx.createRadialGradient(c, c, 0, c, c, R * 1.35);
  const centre = mix(cur.ca, cur.cb, 0.5);
  core.addColorStop(0, `rgba(${centre.join(",")},${0.38 * cur.glow})`);
  core.addColorStop(0.5, `rgba(${cur.cb.map(Math.round).join(",")},${0.12 * cur.glow})`);
  core.addColorStop(1, "rgba(0,0,0,0)");
  ctx.fillStyle = core;
  ctx.fillRect(0, 0, W, W);

  const ca = cur.ca.map(Math.round);
  // Rings draw inwards while listening and outwards while speaking. A still
  // frame (reduced motion) marks an active state with one fixed ring instead.
  if (cur.rings !== 0 && !still) {
    for (let k = 0; k < 3; k += 1) {
      const phase = (seconds * 0.55 + k / 3) % 1;
      const radius = R * (cur.rings > 0 ? 0.9 + phase * 0.55 : 1.45 - phase * 0.55);
      ctx.strokeStyle = `rgba(${ca.join(",")},${0.4 * (1 - phase)})`;
      ctx.lineWidth = 1.5 * dpr;
      ctx.beginPath();
      ctx.arc(c, c, radius, 0, TWO_PI);
      ctx.stroke();
    }
  } else if (still && state !== "idle" && state !== "offline") {
    ctx.strokeStyle = `rgba(${ca.join(",")},0.55)`;
    ctx.lineWidth = 2 * dpr;
    ctx.beginPath();
    ctx.arc(c, c, R * 1.2, 0, TWO_PI);
    ctx.stroke();
  }

  const cosA = Math.cos(angle);
  const sinA = Math.sin(angle);
  const tilt = 0.35;
  const cosT = Math.cos(tilt);
  const sinT = Math.sin(tilt);
  const projected = new Array(POINTS);
  for (let i = 0; i < POINTS; i += 1) {
    const [x, y, z] = points[i];
    const displace = 1 + cur.wave * Math.sin(seconds * 5 + y * 6 + x * 3);
    const x1 = x * cosA + z * sinA;
    const z1 = -x * sinA + z * cosA;
    const y1 = y * cosT - z1 * sinT;
    const z2 = y * sinT + z1 * cosT;
    const scale = R * breathe * displace;
    projected[i] = [c + x1 * scale, c + y1 * scale, (z2 + 1) / 2];
  }

  ctx.lineWidth = dpr;
  for (let i = 0; i < links.length; i += 1) {
    const a = projected[links[i][0]];
    const b = projected[links[i][1]];
    const depth = (a[2] + b[2]) / 2;
    ctx.strokeStyle = `rgba(${mix(cur.ca, cur.cb, depth).join(",")},${0.05 + 0.2 * depth * cur.glow})`;
    ctx.beginPath();
    ctx.moveTo(a[0], a[1]);
    ctx.lineTo(b[0], b[1]);
    ctx.stroke();
  }
  for (let i = 0; i < POINTS; i += 1) {
    const q = projected[i];
    const size = (3 + q[2] * 7) * dpr * (W / 420 + 0.5);
    ctx.globalAlpha = (0.25 + 0.75 * q[2]) * Math.min(1, 0.15 + cur.glow * 1.1);
    ctx.drawImage(sprite(mix(cur.cb, cur.ca, q[2])), q[0] - size, q[1] - size, size * 2, size * 2);
  }
  ctx.globalAlpha = 1;

  const heart = ctx.createRadialGradient(c, c, 0, c, c, R * 0.22);
  heart.addColorStop(0, `rgba(255,255,255,${0.9 * cur.glow + 0.1})`);
  heart.addColorStop(1, `rgba(${centre.join(",")},0)`);
  ctx.fillStyle = heart;
  ctx.beginPath();
  ctx.arc(c, c, R * 0.22, 0, TWO_PI);
  ctx.fill();
}

export function PresenceOrb({ state }) {
  const canvasRef = useRef(null);
  const stateRef = useRef(state);
  const redrawRef = useRef(null);
  const [reduced, setReduced] = useState(prefersReducedMotion);

  stateRef.current = state;

  // The operating system's reduced-motion setting, followed live.
  useEffect(() => {
    if (!window.matchMedia) return undefined;
    const query = window.matchMedia("(prefers-reduced-motion: reduce)");
    const onChange = () => setReduced(query.matches);
    query.addEventListener?.("change", onChange);
    return () => query.removeEventListener?.("change", onChange);
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (!canvas || !ctx) return undefined;
    if (!sphere) sphere = buildSphere();

    let dpr = 1;
    let angle = 0.6;
    let lastFrame = 0;
    const cur = JSON.parse(JSON.stringify(PARAMS[stateRef.current]));

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      const size = Math.max(60, Math.round(rect.width));
      canvas.width = Math.round(size * dpr);
      canvas.height = Math.round(size * dpr);
    };
    resize();

    // One still frame for the current state: used for reduced motion, and to
    // redraw after a resize or a state change while nothing is animating.
    const drawStill = () => {
      const target = PARAMS[stateRef.current];
      Object.assign(cur, JSON.parse(JSON.stringify(target)));
      drawOrb(ctx, canvas, cur, stateRef.current, 0.6, 0, true, dpr);
    };
    redrawRef.current = drawStill;

    let observer = null;
    if (typeof ResizeObserver !== "undefined") {
      observer = new ResizeObserver(() => {
        resize();
        if (reduced) drawStill();
      });
      observer.observe(canvas);
    }

    if (reduced) {
      drawStill();
      return () => {
        observer?.disconnect();
        redrawRef.current = null;
      };
    }

    const onVisibility = () => {
      lastFrame = 0;
    };
    document.addEventListener("visibilitychange", onVisibility);

    const unsubscribe = subscribe((now) => {
      // Paused while hidden: nothing is drawn for a window nobody can see.
      if (document.hidden) return;
      const current = stateRef.current;
      let dt = (now - lastFrame) / 1000;
      if (lastFrame !== 0 && now - lastFrame < minFrameIntervalMs(current)) return;
      if (lastFrame === 0) dt = 0.016;
      lastFrame = now;
      dt = Math.min(dt, 0.1);
      const target = PARAMS[current];
      const k = 1 - Math.exp(-dt * 5);
      ["spin", "breathe", "hz", "wave", "glow"].forEach((name) => {
        cur[name] = lerp(cur[name], target[name], k);
      });
      cur.rings = target.rings;
      cur.ca = cur.ca.map((v, n) => lerp(v, target.ca[n], k));
      cur.cb = cur.cb.map((v, n) => lerp(v, target.cb[n], k));
      angle += cur.spin * dt;
      drawOrb(ctx, canvas, cur, current, angle, now / 1000, false, dpr);
    });

    return () => {
      unsubscribe();
      observer?.disconnect();
      document.removeEventListener("visibilitychange", onVisibility);
      redrawRef.current = null;
    };
  }, [reduced]);

  // With reduced motion nothing animates, so a change of state is drawn here.
  useEffect(() => {
    if (reduced && redrawRef.current) redrawRef.current();
  }, [state, reduced]);

  return (
    <div className="presence-orb" data-orb-state={state} data-reduced-motion={reduced ? "true" : "false"}>
      <canvas ref={canvasRef} aria-hidden="true" />
    </div>
  );
}
