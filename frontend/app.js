// MeenuRaksha dashboard: shows the simulator stream (current risk, pond view,
// risk gauge, time until danger, oxygen chart, latest readings) in Kannada or
// English. Alert text (reasons, time until danger) comes from the API in both
// languages; only the page labels are translated here.
//
// Motion (motion.js, pond-view.js, gauge.js, do-chart.js) helps farmers notice
// changes; every status is still shown as colour + icon + word.

"use strict";

const TEXT = {
  en: {
    appName: "MeenuRaksha",
    tagline: "Pond water early warning",
    welcomeTagline: "Pond water warnings before your fish are in danger.",
    start: "Start",
    simulatedNote: "Not a real pond. For demonstration only.",
    pond: "Pond", pond1: "Pond 1", pond2: "Pond 2", pond3: "Pond 3",
    scenario: "Scenario", scenarioNormal: "Normal day", scenarioCrash: "Night oxygen crash",
    restart: "Restart", pause: "Pause", resume: "Resume",
    simTime: "Simulated time",
    connecting: "Connecting…",
    ended: "Demo finished. Press Restart to play again.",
    connectionLost: "Connection lost. Press Restart.",
    pondViewTitle: "Pond view",
    gaugeTitle: "Risk level",
    ttdTitle: "Time until danger",
    countdownLabel: "Danger expected in",
    chartTitle: "Dissolved oxygen, last 12 hours",
    readingsTitle: "Latest readings",
    infoOnly: "For information",
    pondCaption: {
      safe: "Fish are swimming normally.",
      warning: "Fish are slowing down.",
      danger: "Fish are gasping for air at the surface.",
      unknown: "Waiting for readings.",
    },
    duration: (h, m) => (h ? `${h} h ${String(m).padStart(2, "0")} min` : `${m} min`),
    around: (clock) => `around ${clock}`,
    chartSummary: (now, min) => `Now ${now} mg/L. Lowest in this period: ${min} mg/L.`,
    weatherTitle: "Tonight's weather",
    weatherLoading: "Checking the forecast…",
    weatherUnavailable: "No internet and no saved forecast. Tonight's weather is not known.",
    crashRisk: (level) => `Oxygen crash risk: ${level}`,
    weatherDetails: (c, w, t) => `Day cloud ${c}% · Night wind ${w} km/h · Night ${t} °C · Forecast: Open-Meteo`,
    weatherOffline: (when) => (when ? `Offline: showing the forecast saved on ${when}.` : "Offline."),
  },
  kn: {
    appName: "ಮೀನುರಕ್ಷಾ",
    tagline: "ಕೊಳದ ನೀರಿನ ಮುನ್ನೆಚ್ಚರಿಕೆ",
    welcomeTagline: "ಮೀನುಗಳಿಗೆ ಅಪಾಯ ಬರುವ ಮೊದಲೇ ಕೊಳದ ನೀರಿನ ಎಚ್ಚರಿಕೆ.",
    start: "ಪ್ರಾರಂಭಿಸಿ",
    simulatedNote: "ನಿಜವಾದ ಕೊಳವಲ್ಲ. ಪ್ರದರ್ಶನಕ್ಕಾಗಿ ಮಾತ್ರ.",
    pond: "ಕೊಳ", pond1: "ಕೊಳ 1", pond2: "ಕೊಳ 2", pond3: "ಕೊಳ 3",
    scenario: "ಸನ್ನಿವೇಶ", scenarioNormal: "ಸಾಮಾನ್ಯ ದಿನ", scenarioCrash: "ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕುಸಿತ",
    restart: "ಮರುಪ್ರಾರಂಭಿಸಿ", pause: "ವಿರಾಮ", resume: "ಮುಂದುವರಿಸಿ",
    simTime: "ಅನುಕರಿಸಿದ ಸಮಯ",
    connecting: "ಸಂಪರ್ಕಿಸಲಾಗುತ್ತಿದೆ…",
    ended: "ಪ್ರದರ್ಶನ ಮುಗಿದಿದೆ. ಮತ್ತೆ ನೋಡಲು ಮರುಪ್ರಾರಂಭಿಸಿ ಒತ್ತಿ.",
    connectionLost: "ಸಂಪರ್ಕ ಕಡಿದುಹೋಗಿದೆ. ಮರುಪ್ರಾರಂಭಿಸಿ ಒತ್ತಿ.",
    pondViewTitle: "ಕೊಳದ ನೋಟ",
    gaugeTitle: "ಅಪಾಯದ ಮಟ್ಟ",
    ttdTitle: "ಅಪಾಯದವರೆಗಿನ ಸಮಯ",
    countdownLabel: "ಅಪಾಯಕ್ಕೆ ಉಳಿದ ಸಮಯ",
    chartTitle: "ಕರಗಿದ ಆಮ್ಲಜನಕ, ಕಳೆದ 12 ಗಂಟೆಗಳು",
    readingsTitle: "ಇತ್ತೀಚಿನ ಅಳತೆಗಳು",
    infoOnly: "ಮಾಹಿತಿಗಾಗಿ",
    pondCaption: {
      safe: "ಮೀನುಗಳು ಸಾಮಾನ್ಯವಾಗಿ ಈಜುತ್ತಿವೆ.",
      warning: "ಮೀನುಗಳು ನಿಧಾನವಾಗಿ ಈಜುತ್ತಿವೆ.",
      danger: "ಮೀನುಗಳು ಮೇಲ್ಮೈಗೆ ಬಂದು ಗಾಳಿಗಾಗಿ ಒದ್ದಾಡುತ್ತಿವೆ.",
      unknown: "ಅಳತೆಗಳಿಗಾಗಿ ಕಾಯಲಾಗುತ್ತಿದೆ.",
    },
    duration: (h, m) => (h ? `${h} ಗಂಟೆ ${String(m).padStart(2, "0")} ನಿಮಿಷ` : `${m} ನಿಮಿಷ`),
    around: (clock) => `ಸುಮಾರು ${clock} ಹೊತ್ತಿಗೆ`,
    chartSummary: (now, min) => `ಈಗ ${now} mg/L. ಈ ಅವಧಿಯ ಕನಿಷ್ಠ: ${min} mg/L.`,
    weatherTitle: "ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ",
    weatherLoading: "ಮುನ್ಸೂಚನೆ ನೋಡಲಾಗುತ್ತಿದೆ…",
    weatherUnavailable: "ಇಂಟರ್ನೆಟ್ ಇಲ್ಲ, ಉಳಿಸಿದ ಮುನ್ಸೂಚನೆಯೂ ಇಲ್ಲ. ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ ತಿಳಿದಿಲ್ಲ.",
    crashRisk: (level) => `ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯ: ${level}`,
    weatherDetails: (c, w, t) => `ಹಗಲಿನ ಮೋಡ ${c}% · ರಾತ್ರಿ ಗಾಳಿ ${w} km/h · ರಾತ್ರಿ ${t} °C · ಮುನ್ಸೂಚನೆ: Open-Meteo`,
    weatherOffline: (when) => (when ? `ಆಫ್‌ಲೈನ್: ${when} ರಂದು ಉಳಿಸಿದ ಮುನ್ಸೂಚನೆ ತೋರಿಸಲಾಗುತ್ತಿದೆ.` : "ಆಫ್‌ಲೈನ್."),
  },
};

// Order, units and number format of the reading cards.
const PARAMETERS = [
  ["dissolved_oxygen", "mg/L", 1],
  ["ph", "", 2],
  ["temperature", "°C", 1],
  ["ammonia", "mg/L", 3],
  ["nitrate", "mg/L", 1],
  ["turbidity", "NTU", 1],
];

const ICONS = {
  safe: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm-1.5 14.5-4-4 1.4-1.4 2.6 2.6 5.6-5.6 1.4 1.4-7 7Z"/></svg>',
  warning: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M1 21h22L12 2 1 21Zm12-3h-2v-2h2v2Zm0-4h-2v-4h2v4Z"/></svg>',
  danger: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M15.7 3H8.3L3 8.3v7.4L8.3 21h7.4l5.3-5.3V8.3L15.7 3ZM13 17h-2v-2h2v2Zm0-4h-2V7h2v6Z"/></svg>',
  unknown: "",
};

const LEVEL_WORDS = {
  safe: { en: "Safe", kn: "ಸುರಕ್ಷಿತ" },
  warning: { en: "Warning", kn: "ಎಚ್ಚರಿಕೆ" },
  danger: { en: "Danger", kn: "ಅಪಾಯ" },
  unknown: { en: "Unknown", kn: "ತಿಳಿದಿಲ್ಲ" },
};

const state = {
  lang: "kn", source: null, paused: false, last: null,
  station: "station1", level: null, chartTime: null, effectsReady: false,
  weather: null,
};

const $ = (id) => document.getElementById(id);
const M = window.Motion;

// ---------------------------------------------------------------- language

function loadLanguage() {
  try { return localStorage.getItem("meenuraksha-lang") || "kn"; } catch { return "kn"; }
}

function levelWords(lang) {
  return { safe: LEVEL_WORDS.safe[lang], warning: LEVEL_WORDS.warning[lang], danger: LEVEL_WORDS.danger[lang] };
}

function setLanguage(lang) {
  state.lang = lang;
  try { localStorage.setItem("meenuraksha-lang", lang); } catch { /* storage blocked: ignore */ }
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = TEXT[lang][el.dataset.i18n];
  });
  document.querySelectorAll(".language-toggle button").forEach((b) => {
    b.setAttribute("aria-pressed", String(b.dataset.lang === lang));
  });
  $("pause").textContent = TEXT[lang][state.paused ? "resume" : "pause"];
  if (state.effectsReady) {
    window.RiskGauge.setWords(levelWords(lang));
    window.DOChart.setWords(levelWords(lang));
    // Headings re-appear word by word in the new language (feedback for the switch).
    document.querySelectorAll("#dashboard .text-effect").forEach((h) => M.textEffect(h));
    moveHighlight(true);                       // option widths change with the language
  }
  if (state.last) render(state.last);
  renderWeather();
}

// ---------------------------------------------------------------- helpers

function formatTime(iso) {
  const d = new Date(iso);
  const date = d.toLocaleDateString(state.lang === "kn" ? "kn-IN" : "en-IN", { day: "numeric", month: "short" });
  return `${date}, ${clock(d)}`;
}

function clock(d) {
  return d.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
}

function badgeHTML(level, lang) {
  return `${ICONS[level] || ""}${LEVEL_WORDS[level][lang]}`;
}

// Rebuild a badge only when its level or language changes, not on every reading
// (less work per second on cheap phones).
function setBadge(el, level, lang, className) {
  const key = `${level}|${lang}`;
  if (el.dataset.key === key) return;
  el.dataset.key = key;
  el.className = className;
  if (level === "info") el.textContent = TEXT[lang].infoOnly;
  else el.innerHTML = level === "unknown" ? "" : badgeHTML(level, lang);
}

// ---------------------------------------------------------------- reading cards (built once, updated in place)

const cards = {};

function buildReadingCards() {
  const box = $("readings");
  for (const [parameter, unit] of PARAMETERS) {
    const card = document.createElement("article");
    card.className = "reading in-view";
    card.hidden = true;
    card.innerHTML =
      `<span class="reading-name"></span>` +
      `<span class="reading-value"><span class="reading-number">-</span><span class="reading-unit">${unit}</span></span>` +
      `<span class="badge"></span>`;
    box.append(card);
    cards[parameter] = {
      card,
      name: card.querySelector(".reading-name"),
      number: card.querySelector(".reading-number"),
      badge: card.querySelector(".badge"),
    };
  }
}

function renderReadings(data, lang) {
  const risk = data.risk;
  const graded = Object.fromEntries(risk.parameters.map((p) => [p.parameter, p]));
  const info = Object.fromEntries(risk.info.map((p) => [p.parameter, p]));
  for (const [parameter, , decimals] of PARAMETERS) {
    const c = cards[parameter];
    const result = graded[parameter] || info[parameter];
    c.card.hidden = !result;
    if (!result) continue;
    const level = graded[parameter] ? result.level : "info";
    if (!c.card.classList.contains(`level-${level}`)) c.card.className = `reading in-view level-${level}`;
    c.name.textContent = result.name[lang];
    // Animated Number: the value counts to the new reading.
    M.animateNumber(c.number, data.reading[parameter], (v) => v.toFixed(decimals));
    setBadge(c.badge, level, lang, `badge badge-${level}`);
  }
}

// ---------------------------------------------------------------- status, pond view, gauge, countdown, chart

function renderStatus(risk, lang) {
  const banner = $("status");
  const changed = state.level !== null && state.level !== risk.level;
  banner.className = `status-banner status-${risk.level}`;
  banner.setAttribute("role", risk.level === "danger" ? "alert" : "status");
  $("status-icon").innerHTML = ICONS[risk.level] || "";
  $("status-level").textContent = risk.level_name[lang];
  $("status-summary").textContent = risk.summary[lang];
  // Smooth change of level: colours cross-fade (CSS), the words settle in.
  if (changed && !M.reduce()) {
    M.gsap.fromTo(["#status-icon", "#status-text"], { opacity: 0, y: 6 },
      { opacity: 1, y: 0, duration: 0.5, ease: "power2.out", stagger: 0.05 });
  }
  state.level = risk.level;
}

function renderPondAndGauge(level, lang) {
  window.PondView.setLevel(level);
  window.RiskGauge.setLevel(level);
  const badge = $("pond-view-badge");
  setBadge(badge, level, lang, `badge badge-${level}`);
  badge.hidden = level === "unknown";
  $("pond-view-text").textContent = TEXT[lang].pondCaption[level] || TEXT[lang].pondCaption.unknown;
  setBadge($("gauge-label"), level, lang, `gauge-label gauge-label-${level}`);
}

function renderCountdown(ttd, level, lang) {
  const box = $("countdown");
  const expected = ttd.status === "danger_expected";
  box.hidden = !expected;
  box.classList.toggle("countdown-urgent", expected && level === "warning");
  if (!expected) return;
  // Same rounding as the message: to the nearest 10 minutes.
  const minutes = Math.max(10, Math.round((ttd.hours_to_danger * 60) / 10) * 10);
  M.animateNumber($("countdown-value"), minutes, (v) => {
    const m = Math.round(v / 10) * 10;
    return TEXT[state.lang].duration(Math.floor(m / 60), m % 60);
  }, 0.8);
  const at = new Date(ttd.danger_at);
  at.setMinutes(Math.round(at.getMinutes() / 10) * 10, 0, 0);
  $("countdown-at").textContent = TEXT[lang].around(clock(at));
}

function renderChart(data, lang) {
  if (state.chartTime !== data.time) {          // one point per reading, not per re-render
    state.chartTime = data.time;
    window.DOChart.add(clock(new Date(data.time)), data.reading.dissolved_oxygen);
  }
  const values = (window.DOChart.values && window.DOChart.values()) || [];
  const now = data.reading.dissolved_oxygen;
  const min = values.length ? Math.min(...values) : now;
  $("chart-summary").textContent = now == null ? "" : TEXT[lang].chartSummary(now.toFixed(1), min.toFixed(1));
}

function render(data) {
  const lang = state.lang;
  const risk = data.risk;
  $("simulated-label").textContent = data.label[lang];
  $("sim-time").textContent = formatTime(data.time);

  renderStatus(risk, lang);
  renderPondAndGauge(risk.level, lang);

  const ttd = data.time_to_danger;
  renderCountdown(ttd, risk.level, lang);
  const ttdEl = $("ttd-message");
  ttdEl.textContent = ttd.message[lang];
  ttdEl.classList.toggle("ttd-alert", ttd.status === "danger_expected" || ttd.status === "already_danger");

  renderChart(data, lang);
  renderReadings(data, lang);

  const errors = risk.sensor_errors.map((e) => e.message[lang]);
  $("sensor-errors").hidden = errors.length === 0;
  $("sensor-errors").textContent = errors.join(" ");
}

function showMessage(key) {
  $("status").className = "status-banner status-unknown";
  $("status-icon").innerHTML = "";
  $("status-level").textContent = TEXT[state.lang][key];
  $("status-summary").textContent = "";
}

// ---------------------------------------------------------------- tonight's weather (bottom toolbar)
// Real forecast, not simulated. The server falls back to its saved forecast when
// there is no internet; if even the server can't be reached, the copy saved in
// this browser is shown. Either way the note says "offline".

const WEATHER_KEY = "meenuraksha-weather";
const CRASH_BADGE = { low: "safe", medium: "warning", high: "danger" };   // same colour + icon pairs as the status

async function loadWeather() {
  try {
    const response = await fetch("/api/weather/tonight");
    if (!response.ok) throw new Error(response.statusText);
    state.weather = await response.json();
    if (state.weather.status === "ok") {
      try { localStorage.setItem(WEATHER_KEY, JSON.stringify(state.weather)); } catch { /* storage blocked */ }
    }
  } catch {
    let saved = null;
    try { saved = JSON.parse(localStorage.getItem(WEATHER_KEY)); } catch { /* nothing saved */ }
    state.weather = saved ? { ...saved, offline: true }
      : { status: "unavailable", offline: true, saved_at: null,
          message: { en: TEXT.en.weatherUnavailable, kn: TEXT.kn.weatherUnavailable } };
  }
  renderWeather();
}

function renderWeather() {
  const w = state.weather;
  if (!w) return;
  const lang = state.lang;
  const ok = w.status === "ok";
  const badge = $("weather-badge");
  badge.hidden = !ok;
  if (ok) {
    const level = CRASH_BADGE[w.level];
    badge.className = `badge weather-badge badge-${level}`;
    badge.innerHTML = `${ICONS[level]}${TEXT[lang].crashRisk(w.level_name[lang])}`;
  }
  $("weather-place").textContent = w.location ? ` · ${w.location[lang]}` : "";
  const message = $("weather-message");
  message.removeAttribute("data-i18n");
  message.textContent = w.message[lang];
  $("weather-details").textContent = ok
    ? TEXT[lang].weatherDetails(w.day_cloud_cover_pct, w.night_wind_speed_kmh, w.night_temperature_c) : "";
  const offline = $("weather-offline");
  offline.hidden = !w.offline;
  offline.textContent = TEXT[lang].weatherOffline(w.saved_at ? formatTime(w.saved_at) : null);
}

// ---------------------------------------------------------------- pond picker

function activePondButton() {
  return document.querySelector(`.pond-option[data-station="${state.station}"]`);
}

function moveHighlight(instant = false) {
  M.animatedBackground($("pond-highlight"), activePondButton(), instant);
}

function choosePond(station) {
  if (station === state.station) return;
  state.station = station;
  document.querySelectorAll(".pond-option").forEach((b) => {
    b.setAttribute("aria-pressed", String(b.dataset.station === station));
  });
  moveHighlight();                              // Animated Background slides to the new pond
  start();
}

// ---------------------------------------------------------------- effects (once, when the dashboard first shows)

function initEffects() {
  if (state.effectsReady) return;
  state.effectsReady = true;
  window.PondView.init($("pond-view"));
  window.RiskGauge.init($("gauge"));
  window.RiskGauge.setWords(levelWords(state.lang));
  window.DOChart.init($("do-chart"));
  window.DOChart.setWords(levelWords(state.lang));
  moveHighlight(true);
  M.borderTrail($("pond-highlight"));           // Border Trail on the active pond card
  window.addEventListener("resize", () => moveHighlight(true));
  // In View: cards rise in as they scroll into view; their headings get the Text Effect.
  M.inView([...document.querySelectorAll("#dashboard .in-view")], (card) => {
    const heading = card.querySelector(".text-effect");
    if (heading) M.textEffect(heading);
  });
  renderPondAndGauge("unknown", state.lang);
  loadWeather();
  setInterval(loadWeather, 30 * 60 * 1000);     // the server re-downloads at most every 30 minutes
}

// ---------------------------------------------------------------- stream

// Connect to the simulator stream. To resume a paused demo, pass the demo's
// original first reading time and how many readings were already shown:
// the scenario (e.g. when the night crash happens) is tied to that start time.
function connect(resume) {
  if (state.source) state.source.close();
  const params = new URLSearchParams({ station: state.station, scenario: $("scenario").value });
  if (resume) { params.set("start", resume.start); params.set("skip", String(resume.skip)); }
  const source = new EventSource(`/api/simulator/stream?${params}`);
  source.addEventListener("reading", (event) => {
    state.last = JSON.parse(event.data);
    if (!state.firstTime) state.firstTime = state.last.time;
    state.shown += 1;
    render(state.last);
  });
  source.addEventListener("end", () => { source.close(); showMessage("ended"); });
  source.onerror = () => { if (source.readyState === EventSource.CLOSED) showMessage("connectionLost"); };
  state.source = source;
}

// Restart the demo from the beginning (new pond, new scenario, Restart button).
function start() {
  initEffects();
  state.paused = false;
  state.last = null;
  state.level = null;
  state.chartTime = null;
  state.firstTime = null;
  state.shown = 0;
  window.DOChart.reset();
  $("pause").textContent = TEXT[state.lang].pause;
  showMessage("connecting");
  connect(null);
}

// Pause really stops the stream; Resume continues with the very next reading,
// so no readings are skipped while paused.
function togglePause() {
  state.paused = !state.paused;
  $("pause").textContent = TEXT[state.lang][state.paused ? "resume" : "pause"];
  if (state.paused) {
    if (state.source) state.source.close();
    state.source = null;
    return;
  }
  if (!state.firstTime) { start(); return; }
  connect({ start: state.firstTime, skip: state.shown });
}

// ---------------------------------------------------------------- wiring

buildReadingCards();
document.querySelectorAll(".language-toggle button").forEach((b) => {
  b.addEventListener("click", () => setLanguage(b.dataset.lang));
});
document.querySelectorAll(".pond-option").forEach((b) => {
  b.addEventListener("click", () => choosePond(b.dataset.station));
});
$("restart").addEventListener("click", start);
$("scenario").addEventListener("change", start);
$("pause").addEventListener("click", togglePause);

setLanguage(loadLanguage());

// The welcome screen (welcome.js) calls start() when the farmer presses Start.
// Without a welcome screen, start straight away.
window.MeenuRaksha = { start, setLanguage };
if (!document.getElementById("welcome")) start();
