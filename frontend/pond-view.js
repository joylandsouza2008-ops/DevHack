// Pond view: a small water scene that shows the pond's condition.
//   Safe    clear water, fish swim normally at different depths
//   Warning murkier water, fish slow down and drift upwards
//   Danger  dark murky water, fish hang at the surface, nose up, gasping (bubbles)
// The water tones are murky blues and greys, never the Safe/Warning/Danger
// colours; the caption under the scene always shows the status icon + word.
// Reduce motion: the same scene, still. Off screen: animation pauses.

(function () {
  "use strict";

  const { gsap, reduce, lowPower } = window.Motion;
  const NS = "http://www.w3.org/2000/svg";
  const W = 320, H = 180, SURFACE = 22;

  const WATER = {
    safe:    { top: "#2f7f96", bottom: "#0e3a4a" },
    warning: { top: "#3c6467", bottom: "#132b2d" },
    danger:  { top: "#454d57", bottom: "#161b21" },
    unknown: { top: "#2f5c6c", bottom: "#0e2630" },
  };
  // Per level: swim speed, depth band (y), body tilt (negative = nose up), tail speed.
  const BEHAVIOUR = {
    safe:    { speed: 1,    depth: [70, 140], tilt: 0,   tail: 0.45 },
    warning: { speed: 0.4,  depth: [44, 90],  tilt: -6,  tail: 0.9 },
    danger:  { speed: 0.12, depth: [26, 34],  tilt: -24, tail: 1.6 },
    unknown: { speed: 0.6,  depth: [60, 130], tilt: 0,   tail: 0.7 },
  };

  let root, stopTop, stopBottom, bubbleLayer, fishes = [], level = null;
  let visible = true, tweens = [];

  const el = (name, attrs) => {
    const node = document.createElementNS(NS, name);
    for (const [k, v] of Object.entries(attrs || {})) node.setAttribute(k, v);
    return node;
  };

  function fishShape() {
    // Seen from the side, facing right (same family as the welcome screen fish).
    const g = el("g");
    const tail = el("path", { d: "M-14 0 L-24 -7 C-22 -2 -22 2 -24 7 Z", class: "pv-tail" });
    g.append(
      tail,
      el("path", { d: "M18 0 C14 -7 4 -9 -6 -8 C-12 -7 -15 -3 -15 0 C-15 3 -12 7 -6 8 C4 9 14 7 18 0 Z" }),
      el("path", { d: "M2 -8 L-4 -13 L-6 -7 Z" }),
      el("circle", { cx: 11, cy: -2, r: 1.4, class: "pv-eye" }),
    );
    return { g, tail };
  }

  function build(container) {
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, class: "pv-svg", "aria-hidden": "true", focusable: "false" });
    const defs = el("defs");
    const grad = el("linearGradient", { id: "pv-water", x1: 0, y1: 0, x2: 0, y2: 1 });
    stopTop = el("stop", { offset: "0", "stop-color": WATER.unknown.top });
    stopBottom = el("stop", { offset: "1", "stop-color": WATER.unknown.bottom });
    grad.append(stopTop, stopBottom);
    defs.append(grad);
    svg.append(defs, el("rect", { width: W, height: H, fill: "url(#pv-water)" }));

    // Surface: a gentle wave line that slides sideways (drawn twice as wide).
    const surface = el("g", { class: "pv-surface" });
    let d = `M0 ${SURFACE}`;
    for (let x = 0; x <= W * 2; x += 40) d += ` q10 -4 20 0 t20 0`;
    surface.append(el("path", { d, class: "pv-surface-line" }));
    svg.append(surface);

    // Pond floor.
    svg.append(el("path", { d: `M0 ${H - 14} C80 ${H - 22} 160 ${H - 8} 240 ${H - 16} S${W} ${H - 12} ${W} ${H - 12} L${W} ${H} L0 ${H} Z`, class: "pv-floor" }));

    bubbleLayer = el("g", { class: "pv-bubbles" });
    const fishLayer = el("g");
    const count = lowPower ? 2 : 3;
    for (let i = 0; i < count; i++) {
      const lane = el("g");                    // swims across (x) and faces left or right
      const depth = el("g");                   // moves between depth bands (y)
      const body = el("g");                    // tilt + wobble
      const { g, tail } = fishShape();
      body.append(g); depth.append(body); lane.append(depth); fishLayer.append(lane);
      const dir = i % 2 === 0 ? 1 : -1;
      const scale = 1 - i * 0.12;
      fishes.push({ lane, depth, body, tail, dir, scale, slot: i / Math.max(1, count - 1), swim: null, tailTween: null });
    }
    svg.append(fishLayer, bubbleLayer);
    container.append(svg);
    root = svg;

    // Surface drift.
    if (!reduce()) tweens.push(gsap.to(surface, { x: -40, duration: 4, ease: "none", repeat: -1 }));
  }

  function depthFor(fish, lvl) {
    const [top, bottom] = BEHAVIOUR[lvl].depth;
    return top + (bottom - top) * fish.slot;
  }

  // One lap across the pond from `fromX`, then the next lap from the edge.
  // Each lap is a new tween at the fish's current speed (timeScale).
  function lap(fish, fromX) {
    const start = fish.dir > 0 ? -30 : W + 30;
    const end = fish.dir > 0 ? W + 30 : -30;
    const x = fromX ?? start;
    const duration = fish.lapTime * Math.abs(end - x) / (W + 60);
    fish.swim = gsap.fromTo(fish.lane, { x }, { x: end, duration, ease: "none", onComplete: () => lap(fish) });
    fish.swim.timeScale(fish.speed);
    if (!visible) fish.swim.pause();
  }

  function startSwimming() {
    fishes.forEach((fish, i) => {
      fish.lapTime = 14 + i * 3;
      fish.speed = 1;
      gsap.set(fish.lane, { scaleX: fish.dir * fish.scale, scaleY: fish.scale });
      const start = fish.dir > 0 ? -30 : W + 30;
      lap(fish, start + fish.dir * (W + 60) * (0.2 + i * 0.27));   // start part-way across
      fish.tailTween = gsap.fromTo(fish.tail, { rotation: -14 }, { rotation: 14, svgOrigin: "-14 0", duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: -1 });
      tweens.push(fish.tailTween,
        gsap.to(fish.body, { y: "+=3", duration: 1.6 + i * 0.3, ease: "sine.inOut", yoyo: true, repeat: -1 }));
    });
  }

  // Danger: every fish glides to its own visible spot at the surface and hangs
  // there gasping, instead of drifting off the edge. Leaving Danger: swim on.
  function gatherAtSurface() {
    fishes.forEach((fish, i) => {
      fish.swim.pause();
      const spot = W * (0.22 + 0.56 * (fishes.length === 1 ? 0.5 : i / (fishes.length - 1)));
      fish.sway = gsap.timeline()
        .to(fish.lane, { x: spot, duration: 2.5, ease: "power2.inOut" })
        .to(fish.lane, { x: spot + 6 * fish.dir, duration: 2.2, ease: "sine.inOut", yoyo: true, repeat: -1 });
      tweens.push(fish.sway);
    });
  }

  function swimOn() {
    fishes.forEach((fish) => {
      if (!fish.sway) return;
      fish.sway.kill();
      tweens.splice(tweens.indexOf(fish.sway), 1);
      fish.sway = null;
      fish.swim.kill();
      lap(fish, gsap.getProperty(fish.lane, "x"));
    });
  }

  // Bubbles rise from the fish mouths to the surface while fish gasp (Danger).
  function bubble() {
    if (level !== "danger" || reduce()) return;
    if (visible) {
      const fish = fishes[Math.floor(Math.random() * fishes.length)];
      const x = gsap.getProperty(fish.lane, "x") + 18 * fish.dir * fish.scale;
      const y = gsap.getProperty(fish.depth, "y") - 6;
      const b = el("circle", { cx: x, cy: y, r: 1.6 + Math.random() * 1.4, class: "pv-bubble" });
      bubbleLayer.append(b);
      gsap.to(b, { attr: { cy: SURFACE }, opacity: 0, duration: 0.9 + Math.random() * 0.6, ease: "power1.out", onComplete: () => b.remove() });
    }
    gsap.delayedCall(lowPower ? 0.9 : 0.5, bubble);
  }

  function setLevel(next) {
    if (!root || next === level) return;
    const first = level === null;
    level = next in BEHAVIOUR ? next : "unknown";
    const b = BEHAVIOUR[level];
    const water = WATER[level];

    if (reduce()) {
      stopTop.setAttribute("stop-color", water.top);
      stopBottom.setAttribute("stop-color", water.bottom);
      fishes.forEach((fish, i) => {
        const x = fish.dir > 0 ? 70 + i * 90 : 250 - i * 80;
        fish.lane.setAttribute("transform", `translate(${x} 0) scale(${fish.dir * fish.scale} ${fish.scale})`);
        fish.depth.setAttribute("transform", `translate(0 ${depthFor(fish, level)})`);
        fish.body.setAttribute("transform", `rotate(${b.tilt})`);
      });
      return;
    }

    const ease = "power2.inOut";
    const duration = first ? 0 : 1.5;              // calm change, never a jump
    gsap.to(stopTop, { attr: { "stop-color": water.top }, duration, ease });
    gsap.to(stopBottom, { attr: { "stop-color": water.bottom }, duration, ease });
    if (level === "danger") gatherAtSurface(); else swimOn();
    fishes.forEach((fish) => {
      fish.speed = b.speed;                        // later laps use the new speed too
      if (level !== "danger") gsap.to(fish.swim, { timeScale: b.speed, duration: duration || 0.01, ease });
      gsap.to(fish.tailTween, { timeScale: b.tail / 0.45, duration: duration || 0.01 });
      gsap.to(fish.depth, { y: depthFor(fish, level), duration: first ? 0 : 2, ease });
      gsap.to(fish.body, { rotation: b.tilt, svgOrigin: "0 0", duration: first ? 0 : 1.2, ease });
    });
    if (level === "danger") bubble();
  }

  function init(container) {
    build(container);
    if (!reduce()) {
      startSwimming();
      // Pause when scrolled out of view (phones): no work for an unseen scene.
      new IntersectionObserver(([entry]) => {
        visible = entry.isIntersecting;
        tweens.forEach((t) => (visible ? t.resume() : t.pause()));
        fishes.forEach((f) => {
          if (!f.swim) return;
          if (!visible) f.swim.pause();
          else if (!f.sway) f.swim.resume();       // in Danger the lap stays paused
        });
      }).observe(container);
    }
  }

  window.PondView = { init, setLevel };
})();
