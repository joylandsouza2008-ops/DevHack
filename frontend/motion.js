// Motion for the dashboard, in plain JavaScript with GSAP (no React). Only
// movement with a job is kept: a reading counting to its new value, and the
// pond picker's highlight sliding to the chosen pond.
//
// Rules every effect follows:
//   - "Reduce motion" setting: no movement, the final state appears at once.
//   - Only transform and opacity animate (plus a few small SVG strokes), so
//     cheap phones don't repaint the page every frame.
//   - Low-power phones run GSAP at 30 frames per second.

(function () {
  "use strict";

  const gsap = window.gsap;
  const reduceQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  const lowPower = (navigator.hardwareConcurrency || 8) <= 4 || (navigator.deviceMemory || 8) <= 2;
  const reduce = () => reduceQuery.matches || !gsap;

  if (gsap && lowPower) gsap.ticker.fps(30);

  // ---------------------------------------------------------------- Animated Number
  // Counts smoothly from the number shown now to the new one, so a farmer sees
  // which way a reading moved. `format(value)` turns the number into text.
  const shown = new WeakMap();

  function animateNumber(el, value, format, duration = 0.7) {
    if (value === null || value === undefined || Number.isNaN(value)) {
      gsap && gsap.killTweensOf(shown.get(el) || {});
      shown.delete(el);
      el.textContent = "-";
      return;
    }
    const current = shown.get(el);
    // Low-power phones: no counting, the new value just appears (it's the
    // costliest effect: every text change makes the browser lay out again).
    if (reduce() || lowPower || !current) {
      if (current) gsap && gsap.killTweensOf(current);
      shown.set(el, { v: value, wrote: 0 });
      el.textContent = format(value);
      return;
    }
    gsap.killTweensOf(current);
    gsap.to(current, {
      v: value, duration, ease: "power2.out",
      onUpdate: () => {
        // Write at most 20 times a second, and only when the visible text changes.
        const now = performance.now();
        if (now - current.wrote < 50) return;
        const text = format(current.v);
        if (text !== el.textContent) { el.textContent = text; current.wrote = now; }
      },
      onComplete: () => { el.textContent = format(value); },
    });
  }

  // ---------------------------------------------------------------- Animated Background
  // One highlight slides behind the selected option, so the eye follows the change.
  function animatedBackground(highlight, active, instant = false) {
    const box = { x: active.offsetLeft, y: active.offsetTop, width: active.offsetWidth, height: active.offsetHeight };
    if (reduce() || instant) {
      gsap ? gsap.set(highlight, box) : Object.assign(highlight.style, {
        transform: `translate(${box.x}px, ${box.y}px)`, width: `${box.width}px`, height: `${box.height}px` });
      return;
    }
    gsap.to(highlight, { ...box, duration: 0.45, ease: "power3.out" });
  }

  window.Motion = { gsap, reduce, reduceQuery, lowPower, animateNumber, animatedBackground };
})();
