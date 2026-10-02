// Debug panel, only with ?debug in the address (http://127.0.0.1:8000/?debug).
// Shows live counts so you can watch whether anything keeps growing during a
// long demo: chart points, history entries, page elements, running
// animations, timers, cursor/tap effects and the sky scene, and (in Edge /
// Chrome) JavaScript memory.
// Each line shows "now (at start) peak". Without ?debug this file does nothing.
//
// Loaded BEFORE the other scripts, so it can count every timer they start.

(function () {
  "use strict";

  if (!new URLSearchParams(location.search).has("debug")) return;

  // ---- count timers: wrap setTimeout / setInterval and their clear functions
  const timeouts = new Set(), intervals = new Set();
  const realSetTimeout = window.setTimeout, realClearTimeout = window.clearTimeout;
  const realSetInterval = window.setInterval, realClearInterval = window.clearInterval;
  window.setTimeout = function (fn, ms, ...args) {
    const id = realSetTimeout(function () {
      timeouts.delete(id);
      return typeof fn === "function" ? fn.apply(this, args) : undefined;
    }, ms);
    timeouts.add(id);
    return id;
  };
  window.clearTimeout = (id) => { timeouts.delete(id); realClearTimeout(id); };
  window.setInterval = function (fn, ms, ...args) {
    const id = realSetInterval(fn, ms, ...args);
    intervals.add(id);
    return id;
  };
  window.clearInterval = (id) => { intervals.delete(id); realClearInterval(id); };

  // ---- what to measure
  const mb = (bytes) => Math.round(bytes / 1048576);
  const METRICS = [
    ["Chart points", () => (window.DOChart ? window.DOChart.values().length : 0)],
    ["History entries", () => (window.MeenuRaksha && window.MeenuRaksha.historyCount ? window.MeenuRaksha.historyCount() : 0)],
    ["History items on page", () => document.querySelectorAll(".history-item").length],
    ["Page elements", () => document.getElementsByTagName("*").length],
    ["Pond bubbles", () => document.querySelectorAll(".pv-bubble").length],
    ["GSAP animations (active)", () => (window.gsap ? window.gsap.globalTimeline.getChildren(true, true, false).filter((t) => t.isActive()).length : 0)],
    ["GSAP animations (all)", () => (window.gsap ? window.gsap.globalTimeline.getChildren(true, true, false).length : 0)],
    ["CSS animations", () => (document.getAnimations ? document.getAnimations().length : 0)],
    ["Timers: timeouts", () => timeouts.size],
    ["Timers: intervals", () => intervals.size],
    // Cursor / tap effects and the sky scene: all from fixed pools, so these must stay flat.
    ["Ripple rings (fixed pools)", () => (window.CursorFX ? window.CursorFX.stats().rings : 0)],
    ["Tap ink elements", () => (window.CursorFX ? window.CursorFX.stats().inks : 0)],
    ["Ripples moving", () => (window.CursorFX ? window.CursorFX.stats().moving : 0)],
    ["Spotlights", () => (window.CursorFX ? window.CursorFX.stats().spotlights : 0)],
    ["Cards tilting", () => (window.CursorFX ? window.CursorFX.stats().tilting : 0)],
    ["Buttons pulled (magnet)", () => (window.CursorFX ? window.CursorFX.stats().pulled : 0)],
    ["Welcome fish fleeing", () => (window.WelcomeFX ? window.WelcomeFX.stats().fleeing : 0)],
    ["Sky stars", () => (window.Scene ? window.Scene.stats().stars : 0)],
    ["Sky changes running", () => (window.Scene ? window.Scene.stats().moving : 0)],
    ["Saved keys (localStorage)", () => { try { return localStorage.length; } catch { return 0; } }],
  ];
  if (performance.memory) METRICS.push(["JS memory (MB)", () => mb(performance.memory.usedJSHeapSize)]);

  const first = {}, peak = {};
  const started = performance.now();
  let panel, rows;

  function build() {
    panel = document.createElement("aside");
    panel.className = "debug-panel";
    panel.setAttribute("aria-label", "Debug counts");
    panel.innerHTML = `<p class="debug-title">Debug <span id="debug-uptime"></span></p><table><thead><tr><th></th><th>now</th><th>start</th><th>peak</th></tr></thead><tbody></tbody></table>`;
    rows = METRICS.map(([name]) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<th scope="row"></th><td></td><td></td><td></td>`;
      tr.firstChild.textContent = name;
      panel.querySelector("tbody").append(tr);
      return tr.querySelectorAll("td");
    });
    document.body.append(panel);
  }

  function sample() {
    const minutes = (performance.now() - started) / 60000;
    METRICS.forEach(([name, read], i) => {
      let value;
      try { value = read(); } catch { value = NaN; }
      // "start" = first reading after the demo has run 10 seconds (page settled).
      if (!(name in first) && minutes >= 1 / 6) first[name] = value;
      peak[name] = Math.max(peak[name] ?? value, value);
      const [now, start, top] = rows[i];
      now.textContent = value;
      start.textContent = first[name] ?? "-";
      top.textContent = peak[name];
      // Highlight lines that have grown a lot since the start.
      now.parentElement.classList.toggle("debug-grew", name in first && value > first[name] * 1.5 + 5);
    });
    document.getElementById("debug-uptime").textContent = `${Math.floor(minutes)} min`;
  }

  function start() {
    build();
    sample();
    realSetInterval(sample, 1000);          // the panel's own timer is not counted
    // One line per minute in the console too, so the numbers survive a crash
    // if DevTools is open ("Preserve log").
    realSetInterval(() => {
      const line = Object.fromEntries(METRICS.map(([name], i) => [name, rows[i][0].textContent]));
      console.info("[MeenuRaksha debug]", Math.floor((performance.now() - started) / 60000), "min", line);
    }, 60000);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
