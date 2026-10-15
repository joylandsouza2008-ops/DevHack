// Pond view: a small, flat picture of the pond. A rounded rectangle of water
// (one flat colour), three flat fish swimming slowly, and small bubbles rising.
//   - Bubbles follow the dissolved oxygen: more oxygen, more bubbles (2 to 16).
//   - Fish slow down in Warning and slow down more in Danger.
// Colours come from the theme (styles.css: --pond-water, --pond-fish,
// --pond-bubble): soft teal water in the light theme, dark grey water with
// light grey fish in the dark theme. Never the Safe / Warning / Danger colours;
// the caption under the picture says what the fish are doing, in words.
//
// Speed rules (cheap phones): a fixed number of shapes made once, at most 30
// frames per second, nothing drawn while the picture is off screen or the
// tab is hidden. "Reduce motion": the same picture, still.

(function () {
  "use strict";

  const { reduce } = window.Motion;
  const NS = "http://www.w3.org/2000/svg";
  const W = 320, H = 180;
  const FRAME_MS = 1000 / 30;
  const MAX_BUBBLES = 16;
  const SWIM = 16;                                     // viewBox units per second at full speed: slow
  const SPEED = { safe: 1, warning: 0.5, danger: 0.25, unknown: 0.7 };
  // A fish seen from the side, facing right, about 30 units long. The eye is a hole of water colour.
  const FISH_PATH = "M15 0 C11 -6.5 2 -7.5 -6 -5 L-15 -10.5 L-12.5 0 L-15 10.5 L-6 5 C2 7.5 11 6.5 15 0 Z";
  const LANES = [{ y: 58, dir: 1, size: 1 }, { y: 98, dir: -1, size: 0.85 }, { y: 136, dir: 1, size: 0.75 }];

  let svg = null, fishes = [], bubbles = [], level = "unknown", speed = SPEED.unknown, wanted = 6;
  let raf = 0, last = 0, onScreen = true, running = false;

  const el = (name, attrs) => {
    const node = document.createElementNS(NS, name);
    for (const [k, v] of Object.entries(attrs || {})) node.setAttribute(k, v);
    return node;
  };

  // Bubbles for a dissolved-oxygen reading (mg/L): 2 at 0 mg/L, up to 16 at 12 mg/L.
  function bubblesFor(oxygen) {
    if (oxygen == null || Number.isNaN(oxygen)) return 6;
    return Math.round(2 + (Math.min(12, Math.max(0, oxygen)) / 12) * (MAX_BUBBLES - 2));
  }

  function build(container) {
    svg = el("svg", { viewBox: `0 0 ${W} ${H}`, class: "pv-svg", "aria-hidden": "true", focusable: "false",
                      preserveAspectRatio: "xMidYMid slice" });
    svg.append(el("rect", { width: W, height: H, class: "pv-water" }));
    const bubbleLayer = el("g");
    const fishLayer = el("g");
    bubbles = Array.from({ length: MAX_BUBBLES }, (_, i) => {
      const node = el("circle", { r: 2 + (i % 3) * 0.7, class: "pv-bubble" });
      bubbleLayer.append(node);
      return { node, x: 20 + ((i * 53) % 280), y: H - 6 - ((i * 37) % (H - 20)), speed: 9 + (i % 4) * 2.5, phase: i * 1.3 };
    });
    fishes = LANES.map((lane, i) => {
      const g = el("g", { class: "pv-fish" });
      g.append(el("path", { d: FISH_PATH }), el("circle", { cx: 8.5, cy: -1.5, r: 1.6, class: "pv-eye" }));
      fishLayer.append(g);
      return { g, ...lane, x: 40 + i * 105 };
    });
    svg.append(bubbleLayer, fishLayer);
    container.append(svg);
    draw(0);
  }

  // Move everything by dt seconds and write the new positions.
  function draw(dt) {
    speed += ((SPEED[level] ?? SPEED.unknown) - speed) * Math.min(1, dt * 1.5);   // speed changes gently
    fishes.forEach((f) => {
      f.x += f.dir * SWIM * f.size * speed * dt;
      if (f.dir > 0 && f.x > W + 20) f.x = -20;
      if (f.dir < 0 && f.x < -20) f.x = W + 20;
      f.g.setAttribute("transform", `translate(${f.x.toFixed(1)} ${f.y}) scale(${f.dir * f.size} ${f.size})`);
    });
    bubbles.forEach((b, i) => {
      const shown = i < wanted;
      b.node.style.display = shown ? "" : "none";
      if (!shown) return;
      b.y -= b.speed * dt;
      if (b.y < 6) b.y = H - 6;
      b.phase += dt;
      b.node.setAttribute("cx", (b.x + Math.sin(b.phase * 1.6) * 2).toFixed(1));
      b.node.setAttribute("cy", b.y.toFixed(1));
    });
  }

  // ---- loop: 30 fps, only while visible
  function frame(now) {
    raf = requestAnimationFrame(frame);
    if (now - last < FRAME_MS - 1) return;
    const dt = Math.min(0.1, (now - last) / 1000);
    last = now;
    draw(dt);
  }
  function start() {
    if (running || !svg || reduce() || !onScreen || document.hidden) return;
    running = true;
    last = performance.now();
    raf = requestAnimationFrame(frame);
  }
  function stop() {
    running = false;
    cancelAnimationFrame(raf);
  }

  function init(container) {
    build(container);
    new IntersectionObserver(([entry]) => { onScreen = entry.isIntersecting; onScreen ? start() : stop(); }).observe(container);
    document.addEventListener("visibilitychange", () => (document.hidden ? stop() : start()));
    window.Motion.reduceQuery.addEventListener("change", () => { stop(); draw(0); start(); });
    start();
  }

  function setLevel(next) {
    level = next in SPEED ? next : "unknown";
    if (!running) draw(0);
  }

  // Dissolved oxygen (mg/L): more oxygen, more bubbles.
  function setOxygen(oxygen) {
    wanted = bubblesFor(oxygen);
    if (!running) draw(0);
  }

  // For the ?debug panel and the speed check.
  const stats = () => ({ running, bubbles: wanted, speed: Math.round(speed * 100) / 100 });

  window.PondView = { init, setLevel, setOxygen, stats, bubblesFor };
})();
