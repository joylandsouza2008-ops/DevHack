// Motion effects for the dashboard, in plain JavaScript with GSAP (no React).
// Inspired by Motion Primitives (Animated Number, Text Effect, In View,
// Border Trail, Animated Background), rewritten from scratch for this page.
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

  // ---------------------------------------------------------------- Text Effect
  // Headings appear word by word. Words, never letters: splitting Kannada into
  // letters would break its conjuncts (ಕ್ಷ, ತ್ತ) and vowel signs.
  function textEffect(el) {
    if (reduce()) return;
    gsap.killTweensOf(el.querySelectorAll(".te-word"));   // stop the last run before its words are thrown away
    const text = el.textContent;
    el.textContent = "";
    const words = text.split(/(\s+)/).map((part) => {
      if (/^\s+$/.test(part)) return document.createTextNode(part);
      const span = document.createElement("span");
      span.className = "te-word";
      span.textContent = part;
      return span;
    });
    el.append(...words);
    gsap.fromTo(el.querySelectorAll(".te-word"),
      { opacity: 0, y: 8 },
      { opacity: 1, y: 0, duration: 0.45, stagger: 0.06, ease: "power2.out" });
  }

  // ---------------------------------------------------------------- In View
  // Cards rise in gently the first time they scroll into view.
  function inView(elements, onEnter) {
    if (reduce() || !("IntersectionObserver" in window)) {
      elements.forEach((el) => onEnter && onEnter(el));
      return;
    }
    gsap.set(elements, { opacity: 0, y: 18 });
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        gsap.to(entry.target, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out", clearProps: "transform" });
        if (onEnter) onEnter(entry.target);
      });
    }, { threshold: 0.12 });
    elements.forEach((el) => io.observe(el));
  }

  // ---------------------------------------------------------------- Border Trail
  // A short line of light travels slowly around the active pond card, a quiet
  // "this pond is being watched live" signal. Reduce motion: a plain border.
  function borderTrail(host) {
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", "border-trail");
    svg.setAttribute("aria-hidden", "true");
    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("pathLength", "100");
    svg.append(rect);
    host.append(svg);

    let tween = null;
    function size() {
      const w = host.clientWidth, h = host.clientHeight;
      const radius = parseFloat(getComputedStyle(host).borderRadius) || 0;
      svg.setAttribute("viewBox", `0 0 ${w} ${h}`);
      rect.setAttribute("x", 1.5); rect.setAttribute("y", 1.5);
      rect.setAttribute("width", Math.max(0, w - 3)); rect.setAttribute("height", Math.max(0, h - 3));
      rect.setAttribute("rx", Math.max(0, Math.min(radius, h / 2) - 1.5));
    }
    function run() {
      if (tween) tween.kill();
      if (reduce()) {
        rect.setAttribute("stroke-dasharray", "none");
        return;
      }
      rect.setAttribute("stroke-dasharray", "16 84");
      tween = gsap.fromTo(rect, { attr: { "stroke-dashoffset": 0 } },
        { attr: { "stroke-dashoffset": -100 }, duration: 6, ease: "none", repeat: -1 });
    }
    new ResizeObserver(size).observe(host);
    size();
    run();
    reduceQuery.addEventListener("change", run);
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

  window.Motion = { gsap, reduce, reduceQuery, lowPower, animateNumber, textEffect, inView, borderTrail, animatedBackground };
})();
