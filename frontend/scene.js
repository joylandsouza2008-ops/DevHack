// Day/night pond scene at the top of the dashboard, plus the small hand-drawn
// doodles (fish, reeds, ripples) on some cards.
//
// The sky follows the SIMULATED clock (the time of each reading), not the
// real one: sunrise, daylight, sunset, and a night sky with moon and stars,
// so the night oxygen crash happens under a night sky. The landscape is
// coastal Karnataka: Western Ghats hills, coconut palms, reeds and a small
// country boat on the water.
//
// Colours: the palette's indigo, blues, cyan, an orchid dusk and pale pearl only. Sunrise and sunset are
// shown by light and by the sun's position, never by orange, red or green,
// because those colours mean Warning / Danger / Safe in this app (DESIGN.md).
// tests/test_contrast.py checks the SKY colours below.
//
// Rules (we once crashed from animations piling up):
//   - Four sky layers cross-fade with opacity; sun and moon move by transform.
//   - Every update REPLACES the previous one (overwrite: true), so readings
//     arriving quickly never stack animations. Nothing is created per reading.
//   - Fixed number of stars, built once. The twinkle is 2 CSS animations in
//     total, off on low-power phones and with "reduce motion".
//   - The boat bobs only while the scene is on screen.
//
// Team Orbit touches (subtle; the pond stays the main picture):
//   - A richer starfield: three twinkle groups (3 CSS animations in total) and
//     a few bright stars with a soft halo.
//   - An occasional shooting star and a small satellite crossing slowly (our
//     weather forecast comes from satellites). Each is ONE element made once.
//     Each has ONE pending timer (gsap.delayedCall); a new run kills the old
//     one first. They only start at night, while the scene is on screen, and
//     never with "reduce motion". Low-power phones: fewer stars, rarer runs.
//   - "Reduce motion" or low-power phones: changes appear at once, no tweening.

(function () {
  "use strict";

  const { gsap, reduce, lowPower, reduceQuery } = window.Motion;
  const NS = "http://www.w3.org/2000/svg";

  // Weight of each phase through the day as [hour, weight] points. At every
  // hour the four weights add up to 1. Sunrise is about 06:15 on the
  // Karnataka coast in October, sunset about 18:10.
  const PHASES = {
    night: [[0, 1], [5.3, 1], [6.3, 0], [18.6, 0], [19.4, 1], [24, 1]],
    dawn:  [[5.3, 0], [6.3, 1], [7, 1], [8, 0]],
    day:   [[7, 0], [8, 1], [16.8, 1], [17.8, 0]],
    dusk:  [[16.8, 0], [17.8, 1], [18.6, 1], [19.4, 0]],
  };
  const ORDER = ["night", "dawn", "day", "dusk"];   // bottom layer first

  // Sky gradient per phase: top of the sky, middle, and the glow at the horizon.
  const SKY = {
    night: { top: "#03022e", mid: "#060351", horizon: "#1a1f7a" },
    dawn:  { top: "#1b1a78", mid: "#4f6fc0", horizon: "#cfe6f4" },
    day:   { top: "#1e78b8", mid: "#4fb0d8", horizon: "#b2e4f0" },
    dusk:  { top: "#120a5c", mid: "#4a2a8f", horizon: "#c48ccf" },
  };

  const SUN = [6.0, 18.4];          // hours the sun is above the horizon
  const PHASE_WORDS = {
    en: { night: "Night", dawn: "Sunrise", day: "Daytime", dusk: "Sunset" },
    kn: { night: "ರಾತ್ರಿ", dawn: "ಸೂರ್ಯೋದಯ", day: "ಹಗಲು", dusk: "ಸೂರ್ಯಾಸ್ತ" },
  };

  // viewBox of the landscape drawing and the horizon line inside it.
  const VB_W = 1000, VB_H = 260, HORIZON = 170;

  let art, layers = {}, stars, sun, moon, glint, boat, boatTween = null;
  let phaseEl, starCount = 0, visible = true;
  let nightFx, meteor, satellite, meteorRun = null, meteorCall = null, satTween = null, satCall = null;
  let current = null;               // last applied state, to skip repeat work

  // ---------------------------------------------------------------- maths

  function weight(points, hour) {
    if (hour < points[0][0] || hour > points[points.length - 1][0]) return 0;
    for (let i = 1; i < points.length; i++) {
      const [h1, w1] = points[i - 1], [h2, w2] = points[i];
      if (hour <= h2) return h2 === h1 ? w2 : w1 + (w2 - w1) * (hour - h1) / (h2 - h1);
    }
    return 0;
  }

  function weights(hour) {
    return Object.fromEntries(ORDER.map((p) => [p, weight(PHASES[p], hour)]));
  }

  // Opacity for each stacked layer so the visible mix matches the weights:
  // the top layer shows at its weight, each lower one fills what is left.
  function layerOpacity(w) {
    const out = {};
    let left = 1;
    for (let i = ORDER.length - 1; i > 0; i--) {
      const p = ORDER[i];
      out[p] = left > 0.001 ? Math.min(1, w[p] / left) : 0;
      left -= w[p];
    }
    out.night = 1;                  // the base layer is always fully there
    return out;
  }

  function mix(colours, w) {
    const rgb = [0, 0, 0];
    for (const p of ORDER) {
      const hex = colours[p];
      for (let i = 0; i < 3; i++) rgb[i] += parseInt(hex.slice(1 + i * 2, 3 + i * 2), 16) * w[p];
    }
    return "#" + rgb.map((c) => Math.round(c).toString(16).padStart(2, "0")).join("");
  }

  const hourOf = (iso) => {
    const m = /T(\d\d):(\d\d)/.exec(iso || "");
    return m ? Number(m[1]) + Number(m[2]) / 60 : null;
  };

  // A tiny fixed random generator, so the stars are in the same places on every visit.
  function seeded(seed) {
    return () => {
      seed = (seed + 0x6d2b79f5) | 0;
      let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // ---------------------------------------------------------------- build (once)

  const LAND = `
    <defs>
      <linearGradient id="scene-water" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#0c1060" stop-opacity="0.3"/>
        <stop offset="0.3" stop-color="#070642" stop-opacity="0.7"/>
        <stop offset="1" stop-color="#030226" stop-opacity="0.97"/>
      </linearGradient>
    </defs>
    <path class="sc-hills-far" d="M0 172 L0 126 C60 112 110 121 160 108 C220 93 262 113 320 104 C382 95 420 79 482 92 C540 104 582 87 640 96 C702 105 758 85 822 98 C880 110 942 99 1000 112 L1000 172 Z"/>
    <path class="sc-hills-near" d="M0 172 L0 147 C82 135 140 151 222 140 C300 130 362 147 440 142 C522 137 600 151 702 144 C800 137 882 151 1000 140 L1000 172 Z"/>
    <rect x="0" y="${HORIZON - 2}" width="${VB_W}" height="${VB_H - HORIZON + 2}" fill="url(#scene-water)"/>
    <g class="sc-shimmer">
      <path d="M120 192 c10 -3 22 3 34 0 s20 -3 28 0"/>
      <path d="M520 206 c12 -3 24 3 36 0 s22 -3 30 0"/>
      <path d="M210 228 c8 -2 18 2 26 0"/>
      <path d="M640 236 c14 -3 26 3 38 0 s20 -3 26 0"/>
      <path d="M860 214 c10 -3 20 3 30 0"/>
    </g>
    <g class="sc-ink">
      <path d="M598 177 C640 167 700 166 760 170 C822 174 882 167 1000 165 L1000 192 C902 187 802 191 700 187 C660 185 628 183 598 177 Z"/>
      <g class="sc-palm">
        <path class="sc-trunk" d="M702 171 C705 142 714 113 733 88"/>
        <path d="M733 88 C713 79 694 84 679 97 M733 88 C722 70 705 63 688 66 M733 88 C745 70 763 66 779 73 M733 88 C753 82 773 89 785 103 M733 88 C737 73 735 61 726 51 M733 88 C719 89 707 99 701 112"/>
      </g>
      <g class="sc-palm">
        <path class="sc-trunk" d="M803 173 C800 151 791 128 776 111"/>
        <path d="M776 111 C760 104 744 108 733 119 M776 111 C768 95 754 90 740 93 M776 111 C788 97 803 95 816 101 M776 111 C793 108 807 116 815 128 M776 111 C779 98 776 88 769 80"/>
      </g>
      <g class="sc-palm sc-palm-far">
        <path class="sc-trunk" d="M902 168 C904 152 909 137 919 124"/>
        <path d="M919 124 C908 119 897 122 890 130 M919 124 C914 113 904 109 895 111 M919 124 C927 114 938 113 947 118 M919 124 C931 122 940 128 945 137"/>
      </g>
      <g class="sc-boat" id="scene-boat">
        <path d="M388 197 C408 208 452 208 474 195 L469 192 C448 200 413 200 393 193 Z"/>
        <path class="sc-pole" d="M431 197 L437 166"/>
      </g>
      <g class="sc-reeds">
        <path d="M262 262 C264 232 259 206 250 183 M282 262 C281 236 286 214 295 194 M300 262 C303 240 300 222 292 204 M318 262 C316 244 322 226 332 212 M240 262 C243 244 238 228 229 214"/>
        <ellipse cx="249" cy="178" rx="3.4" ry="9" transform="rotate(-18 249 178)"/>
        <ellipse cx="296" cy="189" rx="3.2" ry="8.5" transform="rotate(20 296 189)"/>
        <ellipse cx="333" cy="207" rx="3" ry="8" transform="rotate(26 333 207)"/>
      </g>
    </g>
    <g class="sc-accent">
      <path d="M284 258 C283 238 287 218 294 200"/>
      <path d="M396 199 C418 206 446 206 466 197"/>
    </g>`;

  function svgEl(markup, cls, aspect) {
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("class", cls);
    svg.setAttribute("viewBox", `0 0 ${VB_W} ${VB_H}`);
    svg.setAttribute("preserveAspectRatio", aspect);
    svg.setAttribute("focusable", "false");
    svg.innerHTML = markup;
    return svg;
  }

  // Fixed number of stars, built once: small ones in three twinkle groups,
  // plus a few bright ones with a soft halo (no twinkle, no animation).
  function buildStars() {
    const rand = seeded(1802);
    const small = lowPower ? 30 : 64, bright = lowPower ? 4 : 7;
    starCount = small + bright;
    const groups = ["", "", ""];
    for (let i = 0; i < small; i++) {
      const x = (rand() * VB_W).toFixed(1);
      const y = (6 + rand() * (HORIZON - 64)).toFixed(1);
      const r = (0.5 + rand() * 1.2).toFixed(2);
      groups[i % 3] += `<circle cx="${x}" cy="${y}" r="${r}"/>`;
    }
    let shine = "";
    for (let i = 0; i < bright; i++) {
      const x = (40 + rand() * (VB_W - 80)).toFixed(1);
      const y = (10 + rand() * (HORIZON - 90)).toFixed(1);
      shine += `<circle class="sc-halo" cx="${x}" cy="${y}" r="5.5"/><circle cx="${x}" cy="${y}" r="${(1.6 + rand() * 0.8).toFixed(2)}"/>`;
    }
    return svgEl(`<g class="sc-stars-a">${groups[0]}</g><g class="sc-stars-b">${groups[1]}</g>` +
      `<g class="sc-stars-c">${groups[2]}</g><g class="sc-stars-bright">${shine}</g>`, "scene-stars", "xMidYMin slice");
  }

  // ---------------------------------------------------------------- shooting star + satellite

  const NIGHT_MIN = 0.6;            // only when the sky is mostly night
  const night = () => current && current.starAlpha >= NIGHT_MIN;
  const canRun = () => visible && night() && !reduce();
  const between = (a, b) => a + Math.random() * (b - a);

  function stopNightFx() {
    [meteorRun, meteorCall, satTween, satCall].forEach((t) => t && t.kill());
    meteorRun = meteorCall = satTween = satCall = null;
    if (gsap) gsap.set([meteor, satellite], { opacity: 0 });
  }

  // One shooting star: a short streak sliding down at an angle, fading in and out.
  function shootingStar() {
    meteorCall = null;
    if (canRun()) {
      if (meteorRun) meteorRun.kill();                    // never two at once
      const w = art.clientWidth, h = art.clientHeight;
      const x = between(0.15, 0.75) * w, y = between(0.06, 0.3) * h;
      const angle = between(18, 32), dist = between(140, 220);
      const rad = angle * Math.PI / 180;
      meteorRun = gsap.timeline({ onComplete: () => { meteorRun = null; } })
        .set(meteor, { x, y, rotation: angle, opacity: 0 })
        .to(meteor, { x: x + Math.cos(rad) * dist, y: y + Math.sin(rad) * dist, duration: 0.85, ease: "power1.in" }, 0)
        .to(meteor, { opacity: 1, duration: 0.12 }, 0)
        .to(meteor, { opacity: 0, duration: 0.4 }, 0.45);
    }
    scheduleMeteor();
  }

  function scheduleMeteor() {
    if (meteorCall) meteorCall.kill();
    meteorCall = reduce() ? null : gsap.delayedCall(lowPower ? between(16, 30) : between(7, 16), shootingStar);
  }

  // One satellite pass: a small dot with panels crossing the sky slowly, left to right.
  function satellitePass() {
    satCall = null;
    if (canRun()) {
      if (satTween) satTween.kill();
      const w = art.clientWidth, h = art.clientHeight;
      const y0 = between(0.12, 0.3) * h, y1 = y0 + between(-0.08, 0.1) * h;
      satTween = gsap.fromTo(satellite, { x: -20, y: y0, opacity: 0.9 },
        { x: w + 20, y: y1, duration: 42, ease: "none", onComplete: () => { satTween = null; scheduleSatellite(); } });
      return;                                              // the next pass is scheduled when this one ends
    }
    scheduleSatellite();
  }

  function scheduleSatellite() {
    if (satCall) satCall.kill();
    satCall = reduce() ? null : gsap.delayedCall(between(18, 36), satellitePass);
  }

  function startNightFx() {
    stopNightFx();
    if (reduce()) return;
    scheduleMeteor();
    satCall = gsap.delayedCall(4, satellitePass);         // first pass soon after the night begins
  }

  function build() {
    art = document.getElementById("scene-art");
    phaseEl = document.getElementById("scene-phase");
    if (!art) return false;
    for (const p of ORDER) {
      const layer = document.createElement("div");
      layer.className = "sky-layer";
      const c = SKY[p];
      layer.style.background = `linear-gradient(to bottom, ${c.top} 0%, ${c.mid} 40%, ${c.horizon} 66%, ${c.horizon} 100%)`;
      layer.style.opacity = p === "night" ? "1" : "0";
      art.append(layer);
      layers[p] = layer;
    }
    stars = buildStars();
    sun = document.createElement("div");
    sun.className = "scene-sun";
    moon = document.createElement("div");
    moon.className = "scene-moon";
    moon.innerHTML = `<svg viewBox="0 0 40 40" focusable="false"><path d="M25 5 A15.5 15.5 0 1 0 35.5 27.5 A12.5 12.5 0 1 1 25 5 Z"/></svg>`;
    glint = document.createElement("div");
    glint.className = "scene-glint";
    const land = svgEl(LAND, "scene-land", "xMidYMax slice");
    // Night-only extras: their layer fades with the stars, so they vanish by day.
    nightFx = document.createElement("div");
    nightFx.className = "scene-night-fx";
    meteor = document.createElement("div");
    meteor.className = "scene-meteor";
    satellite = document.createElement("div");
    satellite.className = "scene-satellite";
    satellite.innerHTML = `<svg viewBox="0 0 22 8" focusable="false"><rect x="0" y="2" width="7" height="4" rx="0.6"/><rect x="15" y="2" width="7" height="4" rx="0.6"/><rect x="8.5" y="1" width="5" height="6" rx="1.4"/></svg>`;
    nightFx.append(meteor, satellite);
    art.append(stars, nightFx, sun, moon, land, glint);
    boat = land.querySelector("#scene-boat");
    if (lowPower) art.classList.add("is-low-power");
    return true;
  }

  // ---------------------------------------------------------------- boat

  function setBoat() {
    if (boatTween) { boatTween.kill(); boatTween = null; }
    if (reduce() || lowPower) { gsap && gsap.set(boat, { y: 0, rotation: 0 }); return; }
    boatTween = gsap.to(boat, { y: 2.5, rotation: 1.6, svgOrigin: "431 197", duration: 2.6, ease: "sine.inOut", yoyo: true, repeat: -1 });
    if (!visible) boatTween.pause();
  }

  // ---------------------------------------------------------------- sky update

  // Where the sun or moon sits for progress p (0 = rising, 1 = setting).
  // `top` is the highest point of the arc: just under the clock chip when the
  // chip sits on the sky (computers), so the sun never hides behind it.
  function bodyPosition(p, w, h, top) {
    const scale = Math.max(w / VB_W, h / VB_H);
    const horizonPx = h - (VB_H - HORIZON) * scale;
    const peak = top < horizonPx - 50 ? top : 34;
    const x = w * (0.08 + 0.84 * p);
    const y = horizonPx + 10 - Math.sin(Math.PI * Math.min(1, Math.max(0, p))) * (horizonPx + 10 - peak);
    return { x, y, horizonPx };
  }

  function arcTop() {
    const chip = art.parentElement.querySelector(".scene-chip");
    if (!chip || getComputedStyle(chip).position !== "absolute") return 34;
    return chip.offsetTop + chip.offsetHeight + 26;
  }

  function apply(hour, lang) {
    const w = weights(hour);
    const op = layerOpacity(w);
    const width = art.clientWidth, height = art.clientHeight, peakY = arcTop();

    const sunUp = hour >= SUN[0] && hour <= SUN[1];
    const sunP = (hour - SUN[0]) / (SUN[1] - SUN[0]);
    const moonP = ((hour - SUN[1] + 24) % 24) / (24 - (SUN[1] - SUN[0]));
    const sunPos = bodyPosition(sunUp ? sunP : (hour < SUN[0] ? 0 : 1), width, height, peakY);
    const moonPos = bodyPosition(sunUp ? (hour < 12 ? 1 : 0) : moonP, width, height, peakY);
    // Fade the body out near the horizon so it never pops in or out.
    const edge = (p) => Math.min(1, Math.max(0, Math.min(p, 1 - p) * 12));
    const sunAlpha = sunUp ? edge(sunP) : 0;
    const moonAlpha = sunUp ? 0 : edge(moonP);
    const lit = sunUp ? sunPos : moonPos;

    const instant = reduce() || lowPower || !current;
    const set = (target, vars) => {
      if (instant) gsap.set(target, vars);
      else gsap.to(target, { ...vars, duration: 1.1, ease: "sine.inOut", overwrite: true });
    };

    // Sky layers: only touched when their opacity really changes.
    for (const p of ORDER) {
      op[p] = Math.round(op[p] * 100) / 100;
      if (!current || current.op[p] !== op[p]) set(layers[p], { opacity: op[p] });
    }

    const starAlpha = Math.round((w.night + 0.25 * (w.dawn + w.dusk)) * 100) / 100;
    if (!current || current.starAlpha !== starAlpha) set([stars, nightFx], { opacity: starAlpha });
    set(sun, { x: sunPos.x, y: sunPos.y, opacity: sunAlpha });
    set(moon, { x: moonPos.x, y: moonPos.y, opacity: moonAlpha });
    set(glint, { x: lit.x, y: lit.horizonPx, opacity: Math.max(sunAlpha * 0.55, moonAlpha * 0.7) });

    // Phase word next to the simulated clock.
    const phase = ORDER.reduce((best, p) => (w[p] > w[best] ? p : best), "night");
    phaseEl.textContent = PHASE_WORDS[lang][phase];
    art.dataset.phase = phase;

    // The little pond view shows the same sky above its water.
    const top = mix(Object.fromEntries(ORDER.map((p) => [p, SKY[p].mid])), w);
    const horizon = mix(Object.fromEntries(ORDER.map((p) => [p, SKY[p].horizon])), w);
    if (window.PondView && window.PondView.setSky && (!current || current.top !== top)) {
      window.PondView.setSky(top, horizon, w.night, instant);
    }
    current = { hour, op, starAlpha, top };
  }

  // ---------------------------------------------------------------- public

  let lastTime = null, lastLang = "kn";

  function init() {
    if (!build() || !gsap) return;
    setBoat();
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      if (boatTween) visible ? boatTween.resume() : boatTween.pause();
      if (satTween) visible ? satTween.resume() : satTween.pause();   // off screen: no work
    }).observe(art);
    startNightFx();
    reduceQuery.addEventListener("change", () => {
      setBoat();
      startNightFx();                          // stops everything; restarts only without "reduce motion"
      current = null;                          // re-apply at once with the new setting
      if (lastTime !== null) apply(lastTime, lastLang);
    });
    // Sun and moon positions depend on the scene's size.
    new ResizeObserver(() => { if (lastTime !== null) { current = null; apply(lastTime, lastLang); } }).observe(art);
    decorate();
  }

  // Called with every simulated reading (and on a language switch).
  function setTime(iso, lang) {
    const hour = hourOf(iso);
    if (hour === null || !art || !gsap) return;
    const sameHour = current && Math.abs(current.hour - hour) < 0.01;
    if (sameHour && lang === lastLang) return;
    lastTime = hour; lastLang = lang;
    apply(hour, lang);
  }

  function setLanguage(lang) {
    if (lastTime !== null && lang !== lastLang) { lastLang = lang; apply(lastTime, lang); }
  }

  function stats() {
    if (!art || !gsap) return { stars: 0, moving: 0, meteor: 0, satellite: 0, timers: 0 };
    const moving = [...ORDER.map((p) => layers[p]), stars, nightFx, sun, moon, glint].filter((t) => gsap.isTweening(t)).length;
    return {
      stars: starCount, moving,
      meteor: meteorRun && meteorRun.isActive() ? 1 : 0,
      satellite: satTween && satTween.isActive() ? 1 : 0,
      timers: (meteorCall ? 1 : 0) + (satCall ? 1 : 0),   // pending "next run" timers: at most 2
    };
  }

  // ---------------------------------------------------------------- hand-drawn doodles
  // Line drawings in the magenta accent, tucked into card corners behind the
  // content (decoration only, hidden from screen readers). Slightly uneven
  // curves on purpose, so they read as drawn by hand.

  const DOODLES = {
    fish: `<svg viewBox="0 0 130 64"><path d="M12 33 C28 13 62 9 90 27 C66 50 31 53 12 33 Z"/><path d="M90 27 C98 21 106 15 116 13 C111 23 111 34 117 46 C107 42 98 36 90 30"/><circle cx="31" cy="29" r="2.4"/><path d="M48 23 C52 29 52 36 47 42 M60 21 C65 28 65 37 59 44"/><path d="M6 14 c3 -3 7 -3 9 0 M2 24 c2 -2 4 -2 6 0"/></svg>`,
    reeds: `<svg viewBox="0 0 100 120"><path d="M30 120 C31 92 27 66 20 42 M48 120 C47 90 52 64 61 38 M64 120 C66 98 64 80 57 62 M80 120 C79 104 84 88 92 76"/><ellipse cx="19" cy="34" rx="4" ry="11" transform="rotate(-14 19 34)"/><ellipse cx="62" cy="30" rx="4" ry="10.5" transform="rotate(16 62 30)"/><path d="M6 118 c10 -4 22 3 34 0 s22 -4 34 0 s14 2 22 0"/></svg>`,
    ripples: `<svg viewBox="0 0 120 70"><ellipse cx="60" cy="35" rx="14" ry="6"/><path d="M28 36 C29 25 46 20 61 20 C79 20 93 26 93 36 C93 46 77 51 60 51 C44 51 30 46 28 38"/><path d="M8 37 C9 19 35 9 61 9 C88 9 113 20 112 36 C111 53 86 62 59 62 C36 62 14 55 9 42"/></svg>`,
    wave: `<svg viewBox="0 0 120 12" preserveAspectRatio="none"><path d="M2 7 C14 2 22 11 36 6 S58 2 70 7 S94 11 104 5 S114 4 118 6"/></svg>`,
  };

  function decorate() {
    document.querySelectorAll("[data-doodle]").forEach((host) => {
      if (host.querySelector(":scope > .doodle")) return;      // once only
      const kind = host.dataset.doodle;
      const box = document.createElement("span");
      box.className = `doodle doodle-${kind}`;
      box.setAttribute("aria-hidden", "true");
      box.innerHTML = DOODLES[kind] || "";
      host.append(box);
    });
  }

  window.Scene = { init, setTime, setLanguage, stats, hourOf, weights };
})();
