// Pond health score ring: a big 0-100 circle that fills to the score from the
// server (backend/health_score.py). The ring takes the status colour, and the
// status icon + word sit under it (in index.html), so the score never stands
// alone as colour. Safe always scores 75-100, Warning 40-74, Danger 0-39.
//
// Team Orbit touch: a small glowing dot circles the ring (decoration, never a
// status colour, never over the number). ONE endless tween, made once; it
// pauses when the ring is off screen and is removed with "reduce motion".

(function () {
  "use strict";

  const { gsap, reduce, reduceQuery, animateNumber } = window.Motion;
  const NS = "http://www.w3.org/2000/svg";
  const R = 52;
  const C = 2 * Math.PI * R;          // length of the circle's outline

  let arc, number, orbit, orbitTween = null, onScreen = true, current = { offset: C };

  function setOrbit() {
    if (orbitTween) { orbitTween.kill(); orbitTween = null; }
    if (!gsap || reduce()) { orbit.setAttribute("visibility", "hidden"); return; }
    orbit.setAttribute("visibility", "visible");
    orbitTween = gsap.to(orbit, { rotation: 360, svgOrigin: "60 60", duration: 11, ease: "none", repeat: -1 });
    if (!onScreen) orbitTween.pause();
  }

  function init(container) {
    const svg = document.createElementNS(NS, "svg");
    svg.setAttribute("viewBox", "0 0 120 120");
    svg.setAttribute("class", "health-svg");
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("focusable", "false");
    svg.innerHTML =
      `<circle class="health-track" cx="60" cy="60" r="${R}"/>` +
      `<circle class="health-arc" cx="60" cy="60" r="${R}" stroke-dasharray="${C.toFixed(2)}" stroke-dashoffset="${C.toFixed(2)}" transform="rotate(-90 60 60)"/>` +
      `<g class="health-orbit"><circle class="health-orbit-halo" cx="60" cy="${60 - R}" r="5.5"/><circle class="health-orbit-dot" cx="60" cy="${60 - R}" r="2.6"/></g>`;
    arc = svg.querySelector(".health-arc");
    orbit = svg.querySelector(".health-orbit");
    number = document.createElement("span");
    number.className = "health-number";
    number.textContent = "-";
    container.append(svg, number);
    setOrbit();
    new IntersectionObserver(([entry]) => {
      onScreen = entry.isIntersecting;
      if (orbitTween) onScreen ? orbitTween.resume() : orbitTween.pause();
    }).observe(container);
    reduceQuery.addEventListener("change", setOrbit);
  }

  // For the ?debug panel: 1 while the dot is circling, else 0.
  const stats = () => ({ orbiting: orbitTween && orbitTween.isActive() ? 1 : 0 });

  // score: 0-100, or null when the status is unknown (empty ring, "-").
  function set(score, level) {
    if (!arc) return;
    arc.setAttribute("class", `health-arc health-arc-${level}`);
    const offset = score == null ? C : C * (1 - score / 100);
    animateNumber(number, score == null ? null : score, (v) => String(Math.round(v)));
    if (gsap) gsap.killTweensOf(current);
    if (reduce() || !gsap) {
      current.offset = offset;
      arc.setAttribute("stroke-dashoffset", offset.toFixed(2));
      return;
    }
    gsap.to(current, {
      offset, duration: 0.9, ease: "power2.out",
      onUpdate: () => arc.setAttribute("stroke-dashoffset", current.offset.toFixed(2)),
    });
  }

  window.HealthRing = { init, set, stats };
})();
