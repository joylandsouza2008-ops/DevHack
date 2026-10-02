// Pond view: a small water scene that shows the pond's condition.
//   Safe    clear water, fish swim normally at different depths
//   Warning murkier water, fish slow down and drift upwards
//   Danger  dark murky water, fish hang at the surface, nose up, gasping (bubbles)
// The water tones are murky blues and greys, never the Safe/Warning/Danger
// colours; the caption under the scene always shows the status icon + word.
// Reduce motion: the same scene, still. Off screen: animation pauses.
// Above the water is a thin strip of sky that follows the simulated time of
// day (scene.js calls setSky), with the moon at night.

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

  const MAX_BUBBLES = 12;           // never more bubbles than this on screen

  let root, stopTop, stopBottom, skyTop, skyBottom, moon, bubbleLayer, fishes = [], level = null;
  let visible = true, tweens = [], bubbleTimer = null;

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
    const sky = el("linearGradient", { id: "pv-sky", x1: 0, y1: 0, x2: 0, y2: 1 });
    skyTop = el("stop", { offset: "0", "stop-color": "#08223f" });
    skyBottom = el("stop", { offset: "1", "stop-color": "#12406f" });
    sky.append(skyTop, skyBottom);
    defs.append(grad, sky);
    moon = el("path", { d: "M283 5 A6 6 0 1 0 287 14 A4.8 4.8 0 1 1 283 5 Z", class: "pv-moon", opacity: 0 });
    svg.append(defs, el("rect", { width: W, height: H, fill: "url(#pv-water)" }),
      el("rect", { width: W, height: SURFACE, fill: "url(#pv-sky)" }), moon);

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
      dropSway(fish);                          // never two sway animations on one fish
      fish.swim.pause();
      const spot = W * (0.22 + 0.56 * (fishes.length === 1 ? 0.5 : i / (fishes.length - 1)));
      fish.sway = gsap.timeline()
        .to(fish.lane, { x: spot, duration: 2.5, ease: "power2.inOut" })
        .to(fish.lane, { x: spot + 6 * fish.dir, duration: 2.2, ease: "sine.inOut", yoyo: true, repeat: -1 });
      tweens.push(fish.sway);
    });
  }

  function dropSway(fish) {
    if (!fish.sway) return;
    fish.sway.kill();
    const i = tweens.indexOf(fish.sway);
    if (i !== -1) tweens.splice(i, 1);
    fish.sway = null;
  }

  function swimOn() {
    fishes.forEach((fish) => {
      if (!fish.sway) return;
      dropSway(fish);
      fish.swim.kill();
      lap(fish, gsap.getProperty(fish.lane, "x"));
    });
  }

  // Bubbles rise from the fish mouths to the surface while fish gasp (Danger).
  // Only ONE bubble loop runs at a time (bubbleTimer), and it stops when Danger ends.
  function stopBubbles() {
    if (bubbleTimer) bubbleTimer.kill();
    bubbleTimer = null;
  }

  function bubble() {
    bubbleTimer = null;
    if (level !== "danger" || reduce()) return;
    if (visible && bubbleLayer.childElementCount < MAX_BUBBLES) {
      const fish = fishes[Math.floor(Math.random() * fishes.length)];
      const x = gsap.getProperty(fish.lane, "x") + 18 * fish.dir * fish.scale;
      const y = gsap.getProperty(fish.depth, "y") - 6;
      const b = el("circle", { cx: x, cy: y, r: 1.6 + Math.random() * 1.4, class: "pv-bubble" });
      bubbleLayer.append(b);
      gsap.to(b, { attr: { cy: SURFACE }, opacity: 0, duration: 0.9 + Math.random() * 0.6, ease: "power1.out", onComplete: () => b.remove() });
    }
    bubbleTimer = gsap.delayedCall(lowPower ? 0.9 : 0.5, bubble);
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

    // overwrite: "auto" stops the previous level's change on the same property,
    // so quick level changes never stack up running animations.
    const ease = "power2.inOut", overwrite = "auto";
    const duration = first ? 0 : 1.5;              // calm change, never a jump
    gsap.to(stopTop, { attr: { "stop-color": water.top }, duration, ease, overwrite });
    gsap.to(stopBottom, { attr: { "stop-color": water.bottom }, duration, ease, overwrite });
    if (level === "danger") gatherAtSurface(); else swimOn();
    fishes.forEach((fish) => {
      fish.speed = b.speed;                        // later laps use the new speed too
      if (level !== "danger") gsap.to(fish.swim, { timeScale: b.speed, duration: duration || 0.01, ease, overwrite });
      gsap.to(fish.tailTween, { timeScale: b.tail / 0.45, duration: duration || 0.01, overwrite });
      gsap.to(fish.depth, { y: depthFor(fish, level), duration: first ? 0 : 2, ease, overwrite });
      gsap.to(fish.body, { rotation: b.tilt, svgOrigin: "0 0", duration: first ? 0 : 1.2, ease, overwrite });
    });
    stopBubbles();
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

  // Sky colours from scene.js. overwrite: the newest sky always replaces the last change.
  function setSky(top, horizon, night, instant) {
    if (!root) return;
    if (instant || reduce()) {
      skyTop.setAttribute("stop-color", top);
      skyBottom.setAttribute("stop-color", horizon);
      moon.setAttribute("opacity", night.toFixed(2));
      return;
    }
    const vars = { duration: 1.1, ease: "sine.inOut", overwrite: true };
    gsap.to(skyTop, { attr: { "stop-color": top }, ...vars });
    gsap.to(skyBottom, { attr: { "stop-color": horizon }, ...vars });
    gsap.to(moon, { attr: { opacity: night }, ...vars });
  }

  window.PondView = { init, setLevel, setSky };
})();
