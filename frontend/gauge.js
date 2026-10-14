// Risk scale: a slim bar under the health score, from 0 (left) to 100 (right),
// split into the Danger (0-39), Warning (40-74) and Safe (75-100) zones of
// the health score (backend/health_score.py). A marker sits at the score.
// The zone that holds the score is drawn at full strength, the others dimmed.
// The words are in the legend under it (healthScale) and in the status block,
// so the level is never shown by colour alone. Part of the "Pond health" panel.

(function () {
  "use strict";

  // Zone widths follow the score ranges: 40 + 35 + 26 points = 0..100 (+1 for the 100 itself).
  const ZONES = [
    { level: "danger", width: 40 },
    { level: "warning", width: 35 },
    { level: "safe", width: 26 },
  ];

  let marker, zones = {};

  function init(container) {
    const track = document.createElement("div");
    track.className = "risk-track";
    ZONES.forEach((z) => {
      const zone = document.createElement("span");
      zone.className = `risk-zone risk-zone-${z.level}`;
      zone.style.flexGrow = String(z.width);
      track.append(zone);
      zones[z.level] = zone;
    });
    marker = document.createElement("span");
    marker.className = "risk-marker";
    marker.hidden = true;
    track.append(marker);
    container.append(track);
  }

  // score: 0-100, or null while waiting (no marker). level: safe | warning | danger | unknown.
  function set(score, level) {
    if (!marker) return;
    ZONES.forEach((z) => zones[z.level].classList.toggle("is-active", z.level === level));
    marker.hidden = score == null;
    if (score != null) marker.style.left = `${Math.min(100, Math.max(0, score))}%`;   // CSS glides it (not with reduce motion)
  }

  window.RiskGauge = { init, set };
})();
