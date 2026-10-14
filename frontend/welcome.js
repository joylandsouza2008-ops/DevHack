// Welcome screen: a calm animated pond (light shimmer, slow fish) and the
// Start button that hands over to the dashboard.
//
// Wide screens: a 3D pond (pond-3d.js: water, bubbles, moon) fills the empty
// right half. Not on phones (no empty half), low-power devices or with
// "reduce motion": those keep the 2D pond only. With a mouse, the example
// warning card tilts gently toward the cursor (6 degrees at most), and if the
// screen is short enough to scroll, the ponds move a little slower than the
// text (soft parallax).
//
// Performance (cheap Android phones):
//   - Only transform and opacity are animated, so the GPU moves ready-made
//     layers instead of the browser repainting the page every frame.
//   - Low-power devices get fewer fish, no tail wag and 30 frames per second.
//   - On Start, every animation is stopped and the scene is removed.
// Accessibility:
//   - "Reduce motion" setting: a still pond, no entrance or exit animation.
//   - The scene is decoration (aria-hidden); the dashboard is `inert` until Start.

(function () {
  "use strict";

  const welcome = document.getElementById("welcome");
  if (!welcome) return;

  const dashboard = document.getElementById("dashboard");
  const content = document.getElementById("welcome-content");
  const startButton = document.getElementById("welcome-start");
  const fishLayer = document.getElementById("pond-fish");

  const gsap = window.gsap;                     // bundled locally: /vendor/gsap/gsap.min.js
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const lowPower = (navigator.hardwareConcurrency || 8) <= 4 || (navigator.deviceMemory || 8) <= 2;
  const smallScreen = window.matchMedia("(max-width: 640px)").matches;

  const FISH_COUNT = lowPower || smallScreen ? 3 : 5;

  let running = false;   // true while the pond is animating
  let entered = false;   // true once Start was pressed

  // ---------------------------------------------------------------- fish

  // A fish seen from above, facing right: body, two side fins, and a tail that can wag.
  function fishSvg(width) {
    const height = Math.round(width * 0.42);
    return (
      `<svg width="${width}" height="${height}" viewBox="0 0 100 42" aria-hidden="true" focusable="false">` +
      `<g fill="#030226">` +
      `<path class="fish-tail" d="M25 21 L7 9 C10.5 16.5 10.5 25.5 7 33 Z"/>` +
      `<path d="M62 12.5 L55 3 L50 13 Z M62 29.5 L55 39 L50 29 Z"/>` +
      `<path d="M90 21 C86 12 72 9 56 10 C42 11 31 15 22 21 C31 27 42 31 56 32 C72 33 86 30 90 21 Z"/>` +
      `</g></svg>`
    );
  }

  function makeFish(i) {
    const depth = i / Math.max(1, FISH_COUNT - 1);         // 0 = near the surface, 1 = deep
    const width = Math.round((smallScreen ? 70 : 96) * (1 - depth * 0.35));
    // fish (swims across, faces left/right) > body (drifts)
    const fish = document.createElement("div");
    fish.className = "fish";
    fish.innerHTML = `<div class="fish-body">${fishSvg(width)}</div>`;
    fish.style.opacity = String(0.62 - depth * 0.28);       // deeper fish are fainter
    fishLayer.append(fish);
    return { el: fish, body: fish.firstElementChild, tail: fish.querySelector(".fish-tail"), width, depth };
  }

  const fishes = Array.from({ length: FISH_COUNT }, (_, i) => makeFish(i));

  function placeFishStill() {
    // Calm, fixed positions used when motion is reduced (or GSAP failed to load).
    const spots = [[0.62, 0.22, 1], [0.78, 0.46, -1], [0.38, 0.36, 1], [0.86, 0.18, -1], [0.55, 0.6, 1]];
    fishes.forEach((f, i) => {
      const [x, y, dir] = spots[i % spots.length];
      f.el.style.transform =
        `translate(${x * window.innerWidth}px, ${y * window.innerHeight}px) scaleX(${dir}) rotate(${dir * 4}deg)`;
    });
  }

  function swim(fish, firstLap) {
    if (!running) return;
    const w = window.innerWidth;
    const h = window.innerHeight;
    const goingRight = Math.random() < 0.5;
    const from = goingRight ? -fish.width - 20 : w + 20;
    const to = goingRight ? w + 20 : -fish.width - 20;
    const y = h * (0.1 + Math.random() * 0.62);
    const speed = (26 + Math.random() * 18) * (1 - fish.depth * 0.3);   // px per second: slow
    const duration = (w + fish.width + 40) / speed;

    const lap = gsap.fromTo(fish.el,
      { x: from, y, scaleX: goingRight ? 1 : -1 },
      { x: to, duration, ease: "none", onComplete: () => swim(fish, false) });
    // Start already part-way across the screen, so the pond isn't empty at first.
    if (firstLap) lap.progress(0.15 + Math.random() * 0.6);
  }

  function startFish() {
    fishes.forEach((fish) => {
      swim(fish, true);
      // Gentle drift up and down with a slight turn, like a fish steering.
      // Handles are kept: stopScene() kills these endless tweens by name
      // (killTweensOf alone left the repeatRefresh drift running after Start).
      fish.drift = gsap.to(fish.body, {
        y: "random(-18, 18)", rotation: "random(-5, 5)",
        duration: "random(3, 5)", ease: "sine.inOut", yoyo: true, repeat: -1, repeatRefresh: true,
      });
      if (!lowPower) {
        fish.wag = gsap.fromTo(fish.tail, { rotation: -9 },
          { rotation: 9, svgOrigin: "25 21", duration: 0.9 + fish.depth * 0.4, ease: "sine.inOut", yoyo: true, repeat: -1 });
      }
    });
  }

  // ---------------------------------------------------------------- 3D pond, right half (wide screens)

  const pond3dHost = document.getElementById("welcome-3d");
  const wide = window.matchMedia("(min-width: 900px)");
  let pond3d = null;

  function start3D() {
    if (pond3d || entered || !pond3dHost || !wide.matches || reduceMotion.matches || lowPower) return;
    const go = () => {
      if (pond3d || entered || !window.Pond3D.supported()) return;
      pond3d = window.Pond3D.create(pond3dHost, {
        transparent: true, level: "safe", oxygen: 7.5, night: 1,
        onFail: () => { pond3d = null; welcome.classList.remove("has-3d"); },   // the 2D pond is still there
      });
      if (!pond3d) return;
      pond3d.setSky("#060351", "#1a1f7a", 1);              // night: moon and stars
      welcome.classList.add("has-3d");
    };
    if (window.Pond3D) go();
    else window.addEventListener("pond3d-ready", go, { once: true });
  }

  function stop3D() {
    if (pond3d) pond3d.destroy();
    pond3d = null;
    welcome.classList.remove("has-3d");
  }

  wide.addEventListener("change", () => (wide.matches ? start3D() : stop3D()));

  // ---------------------------------------------------------------- tilt (mouse) and parallax (scroll)

  const card = welcome.querySelector(".welcome-example");
  const mouse = window.matchMedia("(hover: hover) and (pointer: fine)");
  const MAX_TILT = 6;                          // degrees
  let tiltFx = null, parallaxFrame = 0;

  function startTilt() {
    if (!gsap || !card || tiltFx || !mouse.matches || reduceMotion.matches) return;
    tiltFx = new AbortController();
    gsap.set(card, { transformPerspective: 900 });
    const rx = gsap.quickTo(card, "rotationX", { duration: 0.6, ease: "power3" });
    const ry = gsap.quickTo(card, "rotationY", { duration: 0.6, ease: "power3" });
    const clamp = (v) => Math.max(-1, Math.min(1, v));
    welcome.addEventListener("pointermove", (e) => {
      if (e.pointerType !== "mouse") return;
      const r = card.getBoundingClientRect();
      const px = clamp((e.clientX - (r.left + r.width / 2)) / (window.innerWidth / 2));
      const py = clamp((e.clientY - (r.top + r.height / 2)) / (window.innerHeight / 2));
      ry(px * MAX_TILT);
      rx(-py * MAX_TILT);
    }, { passive: true, signal: tiltFx.signal });
    welcome.addEventListener("pointerleave", () => { rx(0); ry(0); }, { signal: tiltFx.signal });
  }

  function stopTilt() {
    if (tiltFx) tiltFx.abort();
    tiltFx = null;
    if (gsap && card) { gsap.killTweensOf(card); gsap.set(card, { rotationX: 0, rotationY: 0 }); }
  }

  function onScroll() {
    if (parallaxFrame || !gsap || reduceMotion.matches) return;
    parallaxFrame = requestAnimationFrame(() => {
      parallaxFrame = 0;
      const y = welcome.scrollTop;
      gsap.set(".pond", { y: y * 0.25 });
      if (pond3dHost) gsap.set(pond3dHost, { y: y * 0.4 });
    });
  }
  welcome.addEventListener("scroll", onScroll, { passive: true });

  // ---------------------------------------------------------------- light

  function startLight() {
    gsap.to(".pond-caustics-a", { x: 70, y: 40, duration: 19, ease: "sine.inOut", yoyo: true, repeat: -1 });
    gsap.to(".pond-caustics-b", { x: -60, y: 35, duration: 24, ease: "sine.inOut", yoyo: true, repeat: -1 });
    gsap.to(".pond-light", { opacity: 0.55, duration: 5, ease: "sine.inOut", yoyo: true, repeat: -1 });
  }

  // ---------------------------------------------------------------- scene on / off

  function startScene() {
    if (!gsap || reduceMotion.matches) {
      placeFishStill();
      return;
    }
    running = true;
    if (lowPower) gsap.ticker.fps(30);
    startLight();
    startFish();
    start3D();
    startTilt();
  }

  function stopScene() {
    running = false;
    stop3D();
    stopTilt();
    if (!gsap) return;
    const lights = [...welcome.querySelectorAll(".pond-caustics, .pond-light")];
    fishes.forEach((f) => { if (f.drift) f.drift.kill(); if (f.wag) f.wag.kill(); f.drift = f.wag = null; });
    gsap.killTweensOf([...lights, ...fishes.flatMap((f) => [f.el, f.body, f.tail])]);
    // Leave the frame rate as is: low-power phones keep 30 fps for the dashboard too (motion.js).
  }

  // Follow the setting if it changes while the welcome screen is open.
  reduceMotion.addEventListener("change", () => {
    stopScene();
    if (!entered) startScene();
  });

  // ---------------------------------------------------------------- Start -> dashboard

  function finishEnter() {
    stopScene();
    welcome.remove();                          // free the scene's memory and layers
    document.body.classList.remove("has-welcome");
    // Focus the pond status, or the heading of the page the address asked for (#/alerts ...).
    const status = document.getElementById("status");
    if (status.getClientRects().length) status.focus({ preventScroll: true });
    else if (window.Router) window.Router.focusPage();
  }

  function enter() {
    if (entered) return;
    entered = true;
    window.MeenuRaksha.start();                // connect to the data stream right away
    dashboard.removeAttribute("inert");

    if (!gsap || reduceMotion.matches) {
      finishEnter();
      return;
    }
    gsap.timeline({ onComplete: finishEnter })
      .to(content.children, { y: -24, opacity: 0, duration: 0.35, stagger: 0.05, ease: "power2.in" })
      .to(".pond", { scale: 1.08, duration: 0.9, ease: "power2.inOut" }, 0.1)
      .to(welcome, { opacity: 0, duration: 0.55, ease: "power2.out" }, 0.4)
      // clearProps: a transform left on .dashboard would pin the phone tab bar
      // (position: fixed) to the page instead of the screen.
      .from(dashboard, { y: 18, duration: 0.6, ease: "power2.out", clearProps: "transform" }, 0.45);
  }

  startButton.addEventListener("click", enter);

  // ---------------------------------------------------------------- go

  startScene();
  if (gsap && !reduceMotion.matches) {
    // Name, tagline, then the button: draws the eye down to the one action.
    gsap.from(content.children, { y: 20, opacity: 0, duration: 0.8, stagger: 0.12, ease: "power3.out", delay: 0.15 });
  }
})();
