// MeenuRaksha basic page: shows the simulator stream (current risk, time
// until danger, latest readings) in Kannada or English.
// Alert text (reasons, time until danger) comes from the API in both
// languages; only the page labels are translated here.

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
    ttdTitle: "Time until danger",
    readingsTitle: "Latest readings",
    infoOnly: "For information",
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
    ttdTitle: "ಅಪಾಯದವರೆಗಿನ ಸಮಯ",
    readingsTitle: "ಇತ್ತೀಚಿನ ಅಳತೆಗಳು",
    infoOnly: "ಮಾಹಿತಿಗಾಗಿ",
  },
};

// Order and units of the reading cards. Units are the same in both languages.
const PARAMETERS = [
  ["dissolved_oxygen", "mg/L"],
  ["ph", ""],
  ["temperature", "°C"],
  ["ammonia", "mg/L"],
  ["nitrate", "mg/L"],
  ["turbidity", "NTU"],
];

const ICONS = {
  safe: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm-1.5 14.5-4-4 1.4-1.4 2.6 2.6 5.6-5.6 1.4 1.4-7 7Z"/></svg>',
  warning: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M1 21h22L12 2 1 21Zm12-3h-2v-2h2v2Zm0-4h-2v-4h2v4Z"/></svg>',
  danger: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M15.7 3H8.3L3 8.3v7.4L8.3 21h7.4l5.3-5.3V8.3L15.7 3ZM13 17h-2v-2h2v2Zm0-4h-2V7h2v6Z"/></svg>',
  unknown: "",
};

const state = { lang: "kn", source: null, paused: false, last: null };

const $ = (id) => document.getElementById(id);

// ---------------------------------------------------------------- language

function loadLanguage() {
  try { return localStorage.getItem("meenuraksha-lang") || "kn"; } catch { return "kn"; }
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
  if (state.last) render(state.last);
}

// ---------------------------------------------------------------- rendering

function formatValue(parameter, value) {
  if (value === null || value === undefined) return "-";
  if (parameter === "ammonia") return value.toFixed(3);
  if (parameter === "ph") return value.toFixed(2);
  return value.toFixed(1);
}

function formatTime(iso) {
  const d = new Date(iso);
  const date = d.toLocaleDateString(state.lang === "kn" ? "kn-IN" : "en-IN", { day: "numeric", month: "short" });
  const time = d.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
  return `${date}, ${time}`;
}

function render(data) {
  const lang = state.lang;
  const risk = data.risk;

  $("simulated-label").textContent = data.label[lang];
  $("sim-time").textContent = formatTime(data.time);

  // Status banner: icon + level word + reason.
  const banner = $("status");
  banner.className = `status-banner status-${risk.level}`;
  banner.setAttribute("role", risk.level === "danger" ? "alert" : "status");
  $("status-icon").innerHTML = ICONS[risk.level] || "";
  $("status-level").textContent = risk.level_name[lang];
  $("status-summary").textContent = risk.summary[lang];

  // Time until danger.
  const ttd = data.time_to_danger;
  const ttdEl = $("ttd-message");
  ttdEl.textContent = ttd.message[lang];
  ttdEl.classList.toggle("ttd-alert", ttd.status === "danger_expected" || ttd.status === "already_danger");

  // Reading cards.
  const graded = Object.fromEntries(risk.parameters.map((p) => [p.parameter, p]));
  const info = Object.fromEntries(risk.info.map((p) => [p.parameter, p]));
  $("readings").innerHTML = "";
  for (const [parameter, unit] of PARAMETERS) {
    const result = graded[parameter] || info[parameter];
    if (!result) continue;
    const level = graded[parameter] ? result.level : "info";
    const card = document.createElement("article");
    card.className = `reading level-${level}`;

    const name = document.createElement("span");
    name.className = "reading-name";
    name.textContent = result.name[lang];

    const value = document.createElement("span");
    value.className = "reading-value";
    value.textContent = formatValue(parameter, data.reading[parameter]);
    const unitEl = document.createElement("span");
    unitEl.className = "reading-unit";
    unitEl.textContent = unit;
    value.append(unitEl);

    const badge = document.createElement("span");
    if (level === "info") {
      badge.className = "badge badge-info";
      badge.textContent = TEXT[lang].infoOnly;
    } else {
      badge.className = `badge badge-${level}`;
      badge.innerHTML = ICONS[level] || "";
      badge.append(document.createTextNode(risk_level_name(level, lang)));
    }
    card.append(name, value, badge);
    $("readings").append(card);
  }

  // Sensor errors, if any.
  const errors = risk.sensor_errors.map((e) => e.message[lang]);
  $("sensor-errors").hidden = errors.length === 0;
  $("sensor-errors").textContent = errors.join(" ");
}

const LEVEL_WORDS = {
  safe: { en: "Safe", kn: "ಸುರಕ್ಷಿತ" },
  warning: { en: "Warning", kn: "ಎಚ್ಚರಿಕೆ" },
  danger: { en: "Danger", kn: "ಅಪಾಯ" },
  unknown: { en: "Unknown", kn: "ತಿಳಿದಿಲ್ಲ" },
};
function risk_level_name(level, lang) { return LEVEL_WORDS[level][lang]; }

function showMessage(key) {
  $("status").className = "status-banner status-unknown";
  $("status-icon").innerHTML = "";
  $("status-level").textContent = TEXT[state.lang][key];
  $("status-summary").textContent = "";
}

// ---------------------------------------------------------------- stream

function start() {
  if (state.source) state.source.close();
  state.paused = false;
  state.last = null;
  $("pause").textContent = TEXT[state.lang].pause;
  showMessage("connecting");

  const params = new URLSearchParams({ station: $("station").value, scenario: $("scenario").value });
  const source = new EventSource(`/api/simulator/stream?${params}`);
  source.addEventListener("reading", (event) => {
    if (state.paused) return;
    state.last = JSON.parse(event.data);
    render(state.last);
  });
  source.addEventListener("end", () => { source.close(); showMessage("ended"); });
  source.onerror = () => { if (source.readyState === EventSource.CLOSED) showMessage("connectionLost"); };
  state.source = source;
}

// ---------------------------------------------------------------- wiring

document.querySelectorAll(".language-toggle button").forEach((b) => {
  b.addEventListener("click", () => setLanguage(b.dataset.lang));
});
$("restart").addEventListener("click", start);
$("station").addEventListener("change", start);
$("scenario").addEventListener("change", start);
$("pause").addEventListener("click", () => {
  state.paused = !state.paused;
  $("pause").textContent = TEXT[state.lang][state.paused ? "resume" : "pause"];
});

setLanguage(loadLanguage());

// The welcome screen (welcome.js) calls start() when the farmer presses Start.
// Without a welcome screen, start straight away.
window.MeenuRaksha = { start, setLanguage };
if (!document.getElementById("welcome")) start();
