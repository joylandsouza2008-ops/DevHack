// Live dissolved-oxygen chart (Chart.js, bundled locally in vendor/chartjs).
// Safe / Warning / Danger bands are shaded behind the line and labelled with
// their words, so the bands never rely on colour alone. The thresholds come
// from the API's classifier result (3 and 5 mg/L, config/thresholds.toml).
// New points are added without animation: the line doesn't wobble each second.

(function () {
  "use strict";

  const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  const MAX_POINTS = 36;          // 36 readings x 20 minutes = the last 12 hours
  const DANGER_BELOW = 3, SAFE_FROM = 5;

  let chart = null;
  let words = { safe: "Safe", warning: "Warning", danger: "Danger" };

  // Redrawing the chart is the most expensive thing on the page (~40 ms on a
  // slow phone). Redraws wait for an idle moment, so they don't land in the
  // middle of an animation frame; on phones and low-power devices at most one
  // redraw every 3 seconds (several readings are drawn together). Real sensors
  // send a reading every 20 minutes; only the fast demo needs this.
  const lowPower = window.Motion ? window.Motion.lowPower : false;
  const MIN_GAP_MS = lowPower || window.matchMedia("(max-width: 767px)").matches ? 3000 : 0;
  let pending = false, lastDraw = 0;
  const idle = window.requestIdleCallback || ((fn) => setTimeout(fn, 1));

  function scheduleUpdate() {
    if (pending || !chart) return;
    pending = true;
    const wait = Math.max(0, lastDraw + MIN_GAP_MS - performance.now());
    setTimeout(() => idle(() => {
      pending = false;
      lastDraw = performance.now();
      chart.update("none");
    }, { timeout: 1000 }), wait);
  }

  function hexToRgba(hex, alpha) {
    const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }

  // Draws the shaded bands and their words behind the data.
  const bands = {
    id: "riskBands",
    beforeDatasetsDraw(c) {
      const { ctx, chartArea: area, scales: { y } } = c;
      const top = y.max;
      const zones = [
        { level: "safe", from: SAFE_FROM, to: top, colour: css("--safe") },
        { level: "warning", from: DANGER_BELOW, to: SAFE_FROM, colour: css("--warning") },
        { level: "danger", from: 0, to: DANGER_BELOW, colour: css("--danger") },
      ];
      ctx.save();
      zones.forEach((z) => {
        const yTop = y.getPixelForValue(z.to), yBottom = y.getPixelForValue(z.from);
        ctx.fillStyle = hexToRgba(z.colour, 0.14);
        ctx.fillRect(area.left, yTop, area.right - area.left, yBottom - yTop);
        // Threshold line at the top of Warning and Danger.
        if (z.level !== "safe") {
          ctx.strokeStyle = hexToRgba(z.colour, 0.7);
          ctx.setLineDash([5, 5]);
          ctx.lineWidth = 1.5;
          ctx.beginPath(); ctx.moveTo(area.left, yTop); ctx.lineTo(area.right, yTop); ctx.stroke();
        }
        // Band word, inside the band at the LEFT edge: the newest reading is on the right.
        ctx.setLineDash([]);
        ctx.fillStyle = css("--text-secondary");
        ctx.font = `600 15px ${css("--font")}`;
        ctx.textAlign = "left";
        ctx.textBaseline = "middle";
        const mid = Math.max(yTop + 12, Math.min(yBottom - 12, (yTop + yBottom) / 2));
        ctx.fillText(words[z.level], area.left + 8, z.level === "safe" ? yBottom - 14 : mid);
      });
      ctx.restore();
    },
    // Dot on the latest reading.
    afterDatasetsDraw(c) {
      const meta = c.getDatasetMeta(0);
      const last = meta.data[meta.data.length - 1];
      if (!last) return;
      const { ctx } = c;
      ctx.save();
      ctx.fillStyle = css("--primary");
      ctx.beginPath(); ctx.arc(last.x, last.y, 4.5, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    },
  };

  // Colours come from the current theme's CSS variables. The bands and the
  // latest-reading dot read them on every draw; these are set at init and
  // again by restyle() when the theme changes.
  function applyTheme() {
    const o = chart.options.scales;
    chart.data.datasets[0].borderColor = css("--primary");
    o.y.grid.color = css("--hairline");
    o.y.ticks.color = o.x.ticks.color = o.y.title.color = css("--text-secondary");
  }

  function restyle() {
    if (!chart) return;
    applyTheme();
    chart.update("none");
  }

  function init(canvas) {
    const Chart = window.Chart;
    if (!Chart) return;
    Chart.defaults.font.family = css("--font");
    Chart.defaults.font.size = 15;
    Chart.defaults.color = css("--text-secondary");

    chart = new Chart(canvas, {
      type: "line",
      data: { labels: [], datasets: [{
        data: [],
        borderColor: css("--primary"),
        borderWidth: 2.5,
        pointRadius: 0,            // the latest reading is marked by the riskBands plugin (cheaper)
        pointHoverRadius: 4,
        tension: 0.3,
        fill: false,
      }] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,
        interaction: { mode: "index", intersect: false },
        scales: {
          y: { min: 0, max: 16, ticks: { stepSize: 2 }, grid: { color: css("--hairline") },
               title: { display: true, text: "mg/L" } },
          // A label every 6 readings (2 hours). Fixed spacing: Chart.js doesn't have to
          // measure every label each update (much faster on cheap phones).
          x: { ticks: { autoSkip: false, maxRotation: 0,
                        callback(value, index) { return index % 6 === 0 ? this.getLabelForValue(value) : null; } },
               grid: { display: false } },
        },
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: (item) => `${item.parsed.y.toFixed(1)} mg/L` } },
        },
      },
      plugins: [bands],
    });
    applyTheme();
  }

  function reset() {
    if (!chart) return;
    chart.data.labels = [];
    chart.data.datasets[0].data = [];
    chart.update("none");
  }

  function add(label, value) {
    if (!chart || value === null || value === undefined) return;
    const { labels, datasets: [set] } = chart.data;
    labels.push(label); set.data.push(value);
    while (labels.length > MAX_POINTS) { labels.shift(); set.data.shift(); }   // hard cap: memory stays flat
    chart.options.scales.y.max = Math.max(16, Math.ceil(Math.max(...set.data) + 1));
    scheduleUpdate();
  }

  function setWords(next) {
    words = next;
    scheduleUpdate();
  }

  function values() {
    return chart ? chart.data.datasets[0].data.slice() : [];
  }

  window.DOChart = { init, reset, add, setWords, values, restyle };
})();
