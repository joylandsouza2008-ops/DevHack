// Risk gauge: a half-circle meter with Safe, Warning and Danger zones (each
// labelled with its word) and a needle that glides to the current level.
// The current zone is drawn at full strength, the others dimmed. The icon +
// word for the level is shown under the gauge (gauge-label in index.html).

(function () {
  "use strict";

  const { gsap, reduce } = window.Motion;
  const NS = "http://www.w3.org/2000/svg";
  const CX = 110, CY = 108, R = 82;
  // Zones from left (calm) to right (urgent), as angles in degrees (180 = left, 0 = right).
  const ZONES = [
    { level: "safe", from: 180, to: 122 },
    { level: "warning", from: 118, to: 62 },
    { level: "danger", from: 58, to: 0 },
  ];
  const NEEDLE = { safe: -60, warning: 0, danger: 60, unknown: -90 };   // rotation from straight up

  let needle, arcs = {}, labels = {}, current = null;

  const el = (name, attrs) => {
    const node = document.createElementNS(NS, name);
    for (const [k, v] of Object.entries(attrs || {})) node.setAttribute(k, v);
    return node;
  };
  const point = (deg, r) => [CX + r * Math.cos((deg * Math.PI) / 180), CY - r * Math.sin((deg * Math.PI) / 180)];

  function arcPath(from, to) {
    const [x1, y1] = point(from, R), [x2, y2] = point(to, R);
    return `M${x1.toFixed(1)} ${y1.toFixed(1)} A${R} ${R} 0 0 1 ${x2.toFixed(1)} ${y2.toFixed(1)}`;
  }

  function init(container) {
    const svg = el("svg", { viewBox: "0 0 220 130", class: "gauge-svg", "aria-hidden": "true", focusable: "false" });
    ZONES.forEach((z) => {
      arcs[z.level] = el("path", { d: arcPath(z.from, z.to), class: `gauge-arc gauge-arc-${z.level}` });
      svg.append(arcs[z.level]);
    });
    needle = el("g", { class: "gauge-needle" });
    needle.append(
      el("path", { d: `M${CX - 4} ${CY} L${CX} ${CY - R + 16} L${CX + 4} ${CY} Z` }),
      el("circle", { cx: CX, cy: CY, r: 7 }),
    );
    svg.append(needle);
    container.append(svg);

    // Zone words around the arc (HTML, so Kannada renders with the page fonts).
    ZONES.forEach((z) => {
      const label = document.createElement("span");
      label.className = `gauge-word gauge-word-${z.level}`;
      container.append(label);
      labels[z.level] = label;
    });
    if (reduce()) needle.setAttribute("transform", `rotate(${NEEDLE.unknown} ${CX} ${CY})`);
    else gsap.set(needle, { rotation: NEEDLE.unknown, svgOrigin: `${CX} ${CY}` });   // GSAP must own the rotation
  }

  function setWords(words) {
    ZONES.forEach((z) => { labels[z.level].textContent = words[z.level]; });
  }

  function setLevel(level) {
    if (level === current) return;
    current = level;
    ZONES.forEach((z) => {
      arcs[z.level].classList.toggle("is-active", z.level === level);
      labels[z.level].classList.toggle("is-active", z.level === level);
    });
    const rotation = NEEDLE[level] ?? NEEDLE.unknown;
    if (reduce()) {
      needle.setAttribute("transform", `rotate(${rotation} ${CX} ${CY})`);
      return;
    }
    gsap.to(needle, { rotation, svgOrigin: `${CX} ${CY}`, duration: 1.2, ease: "power3.inOut", overwrite: "auto" });
  }

  window.RiskGauge = { init, setLevel, setWords };
})();
