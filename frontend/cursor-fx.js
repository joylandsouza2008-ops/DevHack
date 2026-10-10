// Cursor and touch effects, in plain JavaScript with GSAP (no React).
//   Computer with a mouse:
//     - water ripples where the cursor moves over the page background
//     - a few cards tilt gently under the cursor
//       (Motion Primitives "Tilt", rewritten from scratch)
//     - buttons are slightly magnetic: they lean a few pixels toward the cursor
//   Phone (no cursor): a ripple where the finger taps, inside the button or
//   card that was tapped, or on the water background.
//
// Rules (we once crashed from animations piling up):
//   - Ripples come from FIXED pools of ring elements made once. A new ripple
//     reuses the oldest ring and kills that ring's last animation first, so
//     the number of rings and running ripple animations can never grow.
//   - Tap ink: at most ONE ink element per button or card, reused.
//   - Tilt and magnet use gsap.quickTo: one reusable tween per
//     property per element; each mouse move replaces the previous target.
//   - Background mouse moves are handled at most once per frame.
//   - "Reduce motion": no effects at all.
//   - Readings tiles and status banners are never tilted, and nothing here
//     ever changes the numbers themselves.
//
// Exposes window.CursorFX.stats() for the ?debug panel.

(function () {
  "use strict";

  const { gsap, reduce, lowPower, reduceQuery } = window.Motion;
  const mouseQuery = window.matchMedia("(hover: hover) and (pointer: fine)");
  const on = () => gsap && !reduce();

  // Cards that tilt. Only cards WITHOUT readings, scores or status, so no
  // number is ever shown at an angle.
  const TILT = ".pond-card, .alert-card, .history-card";
  const MAX_TILT = 3;                         // degrees: gentle
  const MAGNET = ".button-primary, .button-secondary";
  // Where the background is covered: no water ripple there.
  const SOLID = ".card, .reading, .status-banner, .scene, .top-bar, .bottom-toolbar, .controls, " +
                ".simulated-banner, .voice-row, .sensor-errors, button, a, input, select, label, .debug-panel";

  const pools = [];
  const inks = new Set();                     // tap-ink elements (one per button / card)
  const tilting = new Set(), pulled = new Set();
  let ready = false;

  // ---------------------------------------------------------------- ripple pool

  // `size` rings are created now and never more. spawn() reuses the oldest.
  function ripplePool(layer, size, className = "fx-ripple") {
    const rings = Array.from({ length: size }, () => {
      const ring = document.createElement("span");
      ring.className = className;
      ring.setAttribute("aria-hidden", "true");
      layer.append(ring);
      return ring;
    });
    let next = 0;
    const pool = {
      rings,
      spawn(x, y, scale = 1) {
        if (!on()) return;
        const ring = rings[next];
        next = (next + 1) % rings.length;
        gsap.killTweensOf(ring);              // stop this ring's previous ripple first
        gsap.fromTo(ring,
          { x, y, scaleX: 0.12 * scale, scaleY: 0.06 * scale, opacity: 0.6 },
          { scaleX: scale, scaleY: 0.5 * scale, opacity: 0, duration: 1.5, ease: "power2.out" });
      },
      destroy() {
        gsap && gsap.killTweensOf(rings);
        rings.forEach((r) => r.remove());
        const i = pools.indexOf(pool);
        if (i !== -1) pools.splice(i, 1);
      },
    };
    pools.push(pool);
    return pool;
  }

  // ---------------------------------------------------------------- background ripples (mouse)

  let water = null, bgPool = null;
  let pendingMove = null, frame = 0, lastX = -1e4, lastY = -1e4, lastAt = 0;

  function onBackground(target) {
    return !document.body.classList.contains("has-welcome") && !(target.closest && target.closest(SOLID));
  }

  function flushMove() {
    frame = 0;
    const e = pendingMove;
    if (!e || !onBackground(e.target)) return;
    const now = performance.now();
    if (now - lastAt < 110 || Math.hypot(e.clientX - lastX, e.clientY - lastY) < 56) return;
    lastAt = now; lastX = e.clientX; lastY = e.clientY;
    bgPool.spawn(e.clientX, e.clientY, 0.9 + Math.random() * 0.3);
  }

  function onPointerMove(e) {
    if (e.pointerType !== "mouse" || !on()) return;
    pendingMove = e;
    if (!frame) frame = requestAnimationFrame(flushMove);   // at most once per frame
  }

  // ---------------------------------------------------------------- tilt (mouse)

  function bindCard(card) {
    const rx = gsap.quickTo(card, "rotationX", { duration: 0.6, ease: "power3" });
    const ry = gsap.quickTo(card, "rotationY", { duration: 0.6, ease: "power3" });

    card.addEventListener("pointerenter", (e) => {
      if (e.pointerType !== "mouse" || !on() || !mouseQuery.matches) return;
      gsap.set(card, { transformPerspective: 1000 });
      tilting.add(card);
    });
    card.addEventListener("pointermove", (e) => {
      if (e.pointerType !== "mouse" || !on() || !mouseQuery.matches) return;
      const r = card.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
      rx((0.5 - py) * 2 * MAX_TILT); ry((px - 0.5) * 2 * MAX_TILT);
    });
    card.addEventListener("pointerleave", () => {
      if (!gsap) return;
      rx(0); ry(0); tilting.delete(card);
    });
  }

  // ---------------------------------------------------------------- magnetic buttons (mouse)

  function bindMagnet(button) {
    const qx = gsap.quickTo(button, "x", { duration: 0.45, ease: "power3" });
    const qy = gsap.quickTo(button, "y", { duration: 0.45, ease: "power3" });
    const clamp = (v, m) => Math.max(-m, Math.min(m, v));
    button.addEventListener("pointermove", (e) => {
      if (e.pointerType !== "mouse" || !on() || button.disabled) return;
      const r = button.getBoundingClientRect();
      qx(clamp((e.clientX - (r.left + r.width / 2)) * 0.18, 6));
      qy(clamp((e.clientY - (r.top + r.height / 2)) * 0.25, 4));
      pulled.add(button);
    });
    button.addEventListener("pointerleave", () => {
      if (!gsap) return;
      qx(0); qy(0);
      pulled.delete(button);
    });
  }

  // ---------------------------------------------------------------- tap ripples (phones)

  // One ink element per host, created on its first tap and reused after that.
  function tapInk(host, x, y) {
    let ink = host._fxInk;
    if (!ink) {
      ink = document.createElement("span");
      ink.className = "fx-ink";
      ink.setAttribute("aria-hidden", "true");
      host._fxInk = ink;
      inks.add(ink);
    }
    if (!ink.isConnected) host.append(ink);  // a label change (textContent) can remove it
    const r = host.getBoundingClientRect();
    const size = Math.max(r.width, r.height) * 2.2;
    gsap.killTweensOf(ink);                   // stop the previous tap's ripple first
    gsap.fromTo(ink,
      { x: x - r.left, y: y - r.top, width: size, height: size, xPercent: -50, yPercent: -50, scale: 0.05, opacity: 0.32 },
      { scale: 1, opacity: 0, duration: 0.7, ease: "power2.out" });
  }

  function onPointerDown(e) {
    if (e.pointerType === "mouse" || !on()) return;
    if (document.body.classList.contains("has-welcome")) return;   // welcome.js handles its own taps
    const t = e.target;
    const host = t.closest && t.closest("button:not(:disabled), .card");
    if (host) tapInk(host, e.clientX, e.clientY);
    else if (onBackground(t)) bgPool.spawn(e.clientX, e.clientY, 1.1);
  }

  // ---------------------------------------------------------------- setup

  function resetAll() {
    if (!gsap) return;
    gsap.set([...tilting, ...pulled], { x: 0, y: 0, rotationX: 0, rotationY: 0 });
    tilting.clear(); pulled.clear();
    gsap.killTweensOf([...inks]);
    gsap.set([...inks], { opacity: 0 });
    pools.forEach((p) => { gsap.killTweensOf(p.rings); gsap.set(p.rings, { opacity: 0 }); });
  }

  function init() {
    if (ready || !gsap) return;
    ready = true;
    water = document.createElement("div");
    water.className = "cursor-water";
    water.setAttribute("aria-hidden", "true");
    document.querySelector(".page-bg").after(water);
    bgPool = ripplePool(water, lowPower ? 5 : 8);

    document.querySelectorAll(`#dashboard :is(${TILT})`).forEach(bindCard);
    document.querySelectorAll(`#dashboard :is(${MAGNET})`).forEach(bindMagnet);
    document.addEventListener("pointermove", onPointerMove, { passive: true });
    document.addEventListener("pointerdown", onPointerDown, { passive: true });
    reduceQuery.addEventListener("change", resetAll);
  }

  function stats() {
    for (const set of [tilting, pulled]) set.forEach((el) => { if (!el.isConnected) set.delete(el); });   // e.g. the removed Start button
    const rings = pools.reduce((n, p) => n + p.rings.length, 0);
    const moving = gsap ? pools.reduce((n, p) => n + p.rings.filter((r) => gsap.isTweening(r)).length, 0) +
                          [...inks].filter((i) => gsap.isTweening(i)).length : 0;
    return { rings, inks: inks.size, moving, tilting: tilting.size, pulled: pulled.size };
  }

  window.CursorFX = { init, ripplePool, bindMagnet, stats, mouseQuery };
})();
