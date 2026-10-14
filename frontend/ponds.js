// My ponds and devices: the farmer's own ponds (Pond page), one pond's full
// dashboard (#/pond/<id>), connecting a device, the farm code (More page) and
// alerts from all ponds (Alerts page). Server side: backend/ponds.py.
//
// No account and no personal data. A random FARM CODE, made here on the first
// visit and kept in this browser, groups the ponds; typing it on another phone
// opens the same ponds. It is sent in the X-Farm-Code header, never in the
// address. Device keys are shown ONCE and never saved in the browser.
//
// These are REAL readings from the farmer's devices, kept apart from the
// simulated demo pond. A demo device (tools/fake_sensor.py) still gets the
// "Simulated data" tag. The page asks the server for news every 20 seconds.
//
// Each pond can have a village, picked from a list (district, then taluk /
// village; GET /api/places, backend/places.py). No GPS and no address: only
// the village name is saved. The pond's page shows tonight's weather for that
// village (weather.js, the real Open-Meteo forecast).

(function () {
  "use strict";

  const FARM_KEY = "aquanexus_farm_code";
  const ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";   // no I, L, O or U: hard to misread
  const CODE_LENGTH = 12;
  const POND_HASH = /^#\/pond\/(p-[a-z0-9]{10})$/;
  const POLL_MS = 20000, POLL_EMPTY_MS = 60000;

  // ---------------------------------------------------------------- pure helpers (also used by the Node tests)

  // 12 random characters from the alphabet, from random bytes (crypto.getRandomValues in the browser).
  function makeFarmCode(bytes) {
    let code = "";
    for (let i = 0; i < CODE_LENGTH; i++) code += ALPHABET[bytes[i] % 32];
    return code;
  }

  // "k7qm 3xrp-9tfd" -> "K7QM3XRP9TFD" (O read as 0, I and L as 1). null if it isn't a farm code.
  function normalizeFarmCode(text) {
    const s = String(text || "").replace(/[\s-]/g, "").toUpperCase()
      .replace(/O/g, "0").replace(/[IL]/g, "1");
    return s.length === CODE_LENGTH && [...s].every((c) => ALPHABET.includes(c)) ? s : null;
  }

  // "K7QM3XRP9TFD" -> "K7QM-3XRP-9TFD" (easier to read out and type).
  function formatFarmCode(code) {
    return code.match(/.{1,4}/g).join("-");
  }

  // "#/pond/p-abc..." -> "p-abc...", anything else -> null.
  function pondFromHash(hash) {
    const m = POND_HASH.exec(String(hash || ""));
    return m ? m[1] : null;
  }

  // Every key this app saves in the browser starts with one of these
  // (language, theme, ticked steps, alert history, weather, cart, farm code).
  const OUR_KEYS = /^(meenuraksha|aquanexus)[-_:]/;

  // "Delete all my data", browser side: removes the app's keys (and nobody else's) from `storage`.
  function clearSavedData(storage) {
    if (!storage) return;
    const keys = [];
    for (let i = 0; i < storage.length; i++) keys.push(storage.key(i));
    keys.filter((k) => OUR_KEYS.test(k)).forEach((k) => storage.removeItem(k));
  }

  const api = { ALPHABET, CODE_LENGTH, makeFarmCode, normalizeFarmCode, formatFarmCode, pondFromHash, clearSavedData };
  if (typeof module !== "undefined" && module.exports) { module.exports = api; return; }   // Node tests

  // ---------------------------------------------------------------- page

  const $ = (id) => document.getElementById(id);
  const ICON = {
    safe: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm-1.5 14.5-4-4 1.4-1.4 2.6 2.6 5.6-5.6 1.4 1.4-7 7Z"/></svg>',
    warning: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M1 21h22L12 2 1 21Zm12-3h-2v-2h2v2Zm0-4h-2v-4h2v4Z"/></svg>',
    danger: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M15.7 3H8.3L3 8.3v7.4L8.3 21h7.4l5.3-5.3V8.3L15.7 3ZM13 17h-2v-2h2v2Zm0-4h-2V7h2v6Z"/></svg>',
  };
  const LEVELS = { safe: { en: "Safe", kn: "ಸುರಕ್ಷಿತ" }, warning: { en: "Warning", kn: "ಎಚ್ಚರಿಕೆ" },
    danger: { en: "Danger", kn: "ಅಪಾಯ" } };      // same words as app.js LEVEL_WORDS
  const UNITS = { dissolved_oxygen: ["mg/L", 1], ph: ["", 2], temperature: ["°C", 1], ammonia: ["mg/L", 3],
    turbidity: ["NTU", 1], salinity: ["ppt", 1] };

  let lang = "kn";
  let words = null;                   // TEXT[lang] from app.js
  let farmCode = null;                // normalised, e.g. K7QM3XRP9TFD
  let codeSaved = true;
  let data = null;                    // GET /api/ponds
  let detail = null;                  // GET /api/ponds/<id> for the open pond
  let openId = null;
  let shownKey = null;                // {pondId, device_id, key}: in memory only, gone after "I have saved it"
  let loadFailed = false;
  let timer = null;
  let chart = null;
  let editing = null;                 // pond id being edited, or null when adding
  let placeList = null;               // GET /api/places: districts -> taluks -> villages (null until loaded)
  let pondWeather = null;             // {village, at, done, result}: tonight's weather for the open pond's village

  function make(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  // ---- farm code (kept in this browser; a code in memory if storage is blocked)

  function loadFarmCode() {
    try {
      const saved = normalizeFarmCode(localStorage.getItem(FARM_KEY));
      if (saved) return saved;
    } catch { codeSaved = false; }
    const fresh = makeFarmCode(crypto.getRandomValues(new Uint8Array(CODE_LENGTH)));
    saveFarmCode(fresh);
    return fresh;
  }

  function saveFarmCode(code) {
    try { localStorage.setItem(FARM_KEY, code); codeSaved = true; } catch { codeSaved = false; }
  }

  // ---- server

  async function call(path, options = {}) {
    const response = await fetch(path, {
      ...options,
      headers: { "Content-Type": "application/json", "X-Farm-Code": farmCode, ...(options.headers || {}) },
    });
    const body = await response.json().catch(() => ({}));
    if (!response.ok) { const error = new Error(body.error || response.statusText); error.status = response.status; error.body = body; throw error; }
    return body;
  }

  async function refresh() {
    clearTimeout(timer);
    try {
      data = await call("/api/ponds");
      loadFailed = false;
      if (openId) await loadDetail();
    } catch {
      loadFailed = true;
    }
    renderAll();
    document.dispatchEvent(new CustomEvent("pondschange"));
    const wait = data && data.ponds.length ? POLL_MS : POLL_EMPTY_MS;
    timer = setTimeout(() => { if (!document.hidden) refresh(); else timer = null; }, wait);
  }

  async function loadDetail() {
    try {
      detail = await call(`/api/ponds/${openId}`);
    } catch (error) {
      detail = error.status === 404 ? { missing: true } : detail;
    }
  }

  // ---- time words

  function timeText(iso) {
    const d = new Date(iso);
    const locale = lang === "kn" ? "kn-IN" : "en-IN";
    const time = d.toLocaleTimeString(locale, { hour: "numeric", minute: "2-digit" });
    const sameDay = d.toDateString() === new Date().toDateString();
    return sameDay ? time : `${d.toLocaleDateString(locale, { day: "numeric", month: "short" })}, ${time}`;
  }

  function deviceLine(pond) {
    const d = pond.device;
    if (!d) return { text: words.deviceNone, state: "none" };
    if (d.online) return { text: words.deviceOnline, state: "online" };
    if (!d.last_seen) return { text: words.deviceWaiting, state: "waiting" };
    return { text: words.deviceOfflineSince(timeText(d.last_seen)), state: "offline" };
  }

  function badge(level, levelName) {
    const span = make("span", `badge badge-${level}`);
    span.innerHTML = ICON[level] || "";        // fixed icons only; the word goes in as text
    span.append(levelName);
    return span;
  }

  // ---------------------------------------------------------------- the list of ponds (Pond page)

  function pondCard(pond) {
    const item = make("li", `card pond-tile level-${pond.level}`);
    const link = make("a", "pond-tile-link");
    link.href = `#/pond/${pond.id}`;
    const head = make("div", "pond-tile-head");
    head.append(make("h3", "pond-tile-name", pond.name));
    if (pond.level_name) head.append(badge(pond.level, pond.level_name[lang]));
    link.append(head);
    if (pond.location) link.append(make("p", "pond-tile-place", `${pond.location.name[lang]}, ${pond.location.district[lang]}`));
    if (pond.cause) link.append(make("p", "pond-tile-cause", pond.cause[lang]));
    link.append(make("p", "pond-tile-time", pond.measured_at ? words.pondLastReading(timeText(pond.measured_at)) : words.pondNoReadings));
    const dev = deviceLine(pond);
    const line = make("p", `pond-tile-device device-${dev.state}`);
    line.append(make("span", "device-dot"), make("span", "", dev.text));
    line.firstChild.setAttribute("aria-hidden", "true");
    link.append(line);
    if (pond.demo) link.append(make("span", "sim-tag", words.simulatedTag));
    item.append(link);
    return item;
  }

  function renderList() {
    const ponds = data ? data.ponds : [];
    $("pond-cards").replaceChildren(...ponds.map(pondCard));
    $("ponds-empty").hidden = loadFailed || ponds.length > 0;
    $("ponds-error").hidden = !loadFailed;
    $("ponds-error").textContent = loadFailed ? words.pondsLoadFailed : "";
    $("ponds-demo").hidden = !(data && data.demo_mode);
  }

  // ---------------------------------------------------------------- one pond's dashboard (#/pond/<id>)

  function valueRow(parameter, value, risk) {
    const [unit, decimals] = UNITS[parameter] || ["", 1];
    const result = risk && [...risk.parameters, ...risk.info].find((p) => p.parameter === parameter);
    const row = make("div", "live-value");
    const dd = make("dd");
    dd.append(make("span", "reading-number", Number(value).toFixed(decimals)));
    if (unit) dd.append(make("span", "reading-unit", unit));   // smaller and muted (styles.css)
    if (result && ICON[result.level]) dd.append(" ", badge(result.level, LEVELS[result.level][lang]));
    else if (result && result.level === "unknown") dd.append(" ", make("span", "badge badge-info", words.infoOnly));
    row.append(make("dt", "", result ? result.name[lang] : parameter), dd);
    return row;
  }

  function renderChart(history) {
    const points = history.filter((r) => typeof r.dissolved_oxygen === "number");
    const canvas = $("pond-detail-chart");
    if (chart) { chart.destroy(); chart = null; }
    $("pond-detail-chart-wrap").hidden = points.length < 2;
    if (points.length < 2) { $("pond-detail-chart-summary").textContent = words.pondChartNone; return; }
    const first = points[0].dissolved_oxygen, last = points[points.length - 1].dissolved_oxygen;
    $("pond-detail-chart-summary").textContent = words.pondChartSummary(first.toFixed(1), last.toFixed(1), points.length);
    if (!window.Chart) return;
    const css = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    const labels = points.map((r) => new Date(r.time).toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" }));
    const flat = (y) => points.map(() => y);
    chart = new window.Chart(canvas, {
      type: "line",
      data: { labels, datasets: [
        { label: words.pondChartOxygen, data: points.map((r) => r.dissolved_oxygen), borderColor: css("--primary"),
          backgroundColor: css("--primary"), borderWidth: 3, pointRadius: 2, tension: 0.25 },
        { label: words.pondChartWarnLine, data: flat(5), borderColor: css("--text-secondary"), borderDash: [6, 4],
          borderWidth: 1.5, pointRadius: 0 },
        { label: words.pondChartDangerLine, data: flat(3), borderColor: css("--text-secondary"), borderDash: [2, 3],
          borderWidth: 1.5, pointRadius: 0 },
      ] },
      options: {
        animation: false, maintainAspectRatio: false, responsive: true,
        plugins: { legend: { labels: { color: css("--text"), font: { size: 14 } } } },
        scales: {
          x: { ticks: { color: css("--text-secondary"), maxTicksLimit: 6 }, grid: { color: css("--hairline") } },
          y: { suggestedMin: 0, suggestedMax: 10, ticks: { color: css("--text-secondary") }, grid: { color: css("--hairline") },
            title: { display: true, text: "mg/L", color: css("--text-secondary") } },
        },
      },
    });
  }

  function renderDevice(pond) {
    const box = $("device-status");
    const dev = deviceLine(pond);
    box.className = `pond-tile-device device-${dev.state}`;
    box.replaceChildren(make("span", "device-dot"), make("span", "", pond.device ? `${pond.device.id} · ${dev.text}` : dev.text));
    box.firstChild.setAttribute("aria-hidden", "true");
    const error = pond.device && pond.device.last_error;
    $("device-error").hidden = !error;
    if (error) {
      $("device-error").textContent = `${words.deviceLastRefused} ${[error.message[lang], ...error.sensor_errors.map((e) => e.message[lang])].join(" ")}`;
    }
    $("device-connect").hidden = Boolean(pond.device);
    $("device-new-key").hidden = !pond.device;
    $("device-remove").hidden = !pond.device;

    const key = shownKey && shownKey.pondId === pond.id ? shownKey : null;
    $("device-key-box").hidden = !key;
    if (!key) return;
    const url = `${location.origin}/api/sensor/${key.device_id}`;
    $("device-id-value").textContent = key.device_id;
    $("device-key-value").textContent = key.key;
    $("device-url-value").textContent = url;
    $("device-steps").replaceChildren(...[
      words.deviceStep1, words.deviceStep2(url), words.deviceStep3(key.every_seconds), words.deviceStep4,
    ].map((text) => make("li", "", text)));
  }

  function renderDetail() {
    const section = $("pond-detail");
    $("page-pond").classList.toggle("showing-pond", Boolean(openId));
    section.hidden = !openId;
    if (!openId) { if (chart) { chart.destroy(); chart = null; } return; }
    const missing = detail && detail.missing;
    $("pond-detail-missing").hidden = !missing;
    $("pond-detail-body").hidden = !detail || missing;
    if (!detail || missing) { $("pond-detail-name").textContent = missing ? words.pondNotFound : "…"; return; }

    const pond = detail;
    $("pond-detail-name").textContent = pond.name;
    const meta = [placeText(pond.location), pond.size && `${words.pondSize}: ${pond.size}`,
      pond.fish && `${words.pondFish}: ${pond.fish}`].filter(Boolean);
    $("pond-detail-meta").textContent = meta.join(" · ");
    $("pond-detail-meta").hidden = !meta.length;
    $("pond-detail-demo").hidden = !pond.demo;

    const risk = pond.risk;
    const level = risk ? risk.level : "unknown";
    $("pond-detail-status").className = `status-banner status-${level}`;
    $("pond-detail-status-icon").innerHTML = ICON[level] || "";
    $("pond-detail-status-level").textContent = risk ? risk.level_name[lang] : words.pondNoReadings;
    $("pond-detail-status-summary").textContent = risk ? risk.summary[lang] : (pond.device ? words.deviceWaiting : words.pondConnectFirst);
    $("pond-detail-time").textContent = pond.measured_at ? words.pondLastReading(timeText(pond.measured_at)) : "";

    const ttd = pond.time_to_danger;
    const ttdText = ttd && ttd.status !== "not_enough_data" && ttd.message ? ttd.message[lang] : "";
    $("pond-detail-ttd").hidden = !ttdText;
    $("pond-detail-ttd").textContent = ttdText;

    $("pond-detail-readings").hidden = !pond.reading;
    if (pond.reading) {
      const order = Object.keys(UNITS).filter((p) => p in pond.reading);
      $("pond-detail-values").replaceChildren(...order.map((p) => valueRow(p, pond.reading[p], risk)));
    }
    const actions = risk ? risk.actions : [];
    $("pond-detail-actions").hidden = !actions.length;
    $("pond-detail-action-list").replaceChildren(...actions.map((a) => make("li", "", a[lang])));
    if (window.DiseaseGuide && risk) window.DiseaseGuide.renderLikely($("pond-detail-likely"), risk.likely_diseases, lang, words);
    else $("pond-detail-likely").hidden = true;
    renderChart(pond.history || []);
    renderPondWeather(pond);
    renderDevice(pond);
    if (pond.location) ensurePondWeather(pond.location);
  }

  // "Kota · Brahmavar taluk · Udupi" (null: no place chosen).
  function placeText(location) {
    if (!location) return null;
    return [location.name[lang], words.pondTaluk(location.taluk[lang]), location.district[lang]].join(" · ");
  }

  // ---------------------------------------------------------------- tonight's weather for the open pond's village
  // Real forecast (weather.js: Open-Meteo in the browser, then our server, then a saved copy). Not simulated.

  const CRASH_BADGE = { low: "safe", medium: "warning", high: "danger" };   // same pairs as app.js
  const WEATHER_MAX_AGE_MS = 30 * 60 * 1000;                                // download again after 30 minutes

  function browserStorage() {
    try { return window.localStorage; } catch { return null; }
  }

  function ensurePondWeather(location) {
    const same = pondWeather && pondWeather.village === location.village;
    if (same && Date.now() - pondWeather.at < WEATHER_MAX_AGE_MS) return;
    // Keep showing the old answer for this village while the new one downloads.
    pondWeather = { village: location.village, at: Date.now(), done: same && pondWeather.done, result: same ? pondWeather.result : null };
    loadPondWeather(location);
  }

  async function loadPondWeather(location) {
    let result = null;
    try {
      result = await window.TonightWeather.loadTonight({ location, storage: browserStorage(), log: (text) => console.warn(text) });
    } catch { result = null; }
    if (!pondWeather || pondWeather.village !== location.village) return;   // another pond was opened meanwhile
    pondWeather.result = result;
    pondWeather.done = true;
    if (detail && !detail.missing) renderPondWeather(detail);
  }

  // The forecast's saved time: the server's has no zone (India time), the browser's ends in "Z".
  function savedText(savedAt) {
    return timeText(/(Z|[+-]\d\d:\d\d)$/.test(savedAt) ? savedAt : `${savedAt}+05:30`);
  }

  function renderPondWeather(pond) {
    const location = pond.location;
    const mine = location && pondWeather && pondWeather.village === location.village ? pondWeather : null;
    const w = mine && mine.done ? mine.result : null;
    const ok = Boolean(w && w.status === "ok");
    $("pond-weather-place").textContent = location ? ` · ${location.name[lang]}` : "";
    $("pond-weather-choose-row").hidden = Boolean(location);
    const badgeBox = $("pond-weather-badge");
    badgeBox.hidden = !ok;
    if (ok) {
      const level = CRASH_BADGE[w.level];
      badgeBox.className = `badge weather-badge badge-${level}`;
      badgeBox.innerHTML = ICON[level] || "";                 // fixed icons only; the words go in as text
      badgeBox.append(words.crashRisk(w.level_name[lang]));
    }
    let message = words.weatherLoading;
    if (!location) message = words.pondWeatherNoPlace;
    else if (mine && mine.done) message = w ? w.message[lang] : words.weatherUnavailable;
    $("pond-weather-message").textContent = message;
    $("pond-weather-details").textContent = ok
      ? words.weatherDetails(w.day_cloud_cover_pct, w.night_wind_speed_kmh, w.night_temperature_c) : "";
    const minutes = ok ? window.TonightWeather.minutesSince(w.saved_at, Date.now()) : null;
    $("pond-weather-updated").hidden = minutes === null;
    $("pond-weather-updated").textContent = minutes === null ? "" : words.weatherUpdated(minutes);
    const offline = Boolean(mine && mine.done && (!w || w.offline));
    $("pond-weather-offline").hidden = !offline;
    $("pond-weather-offline").textContent = offline ? words.weatherOffline(w && w.saved_at ? savedText(w.saved_at) : null) : "";
  }

  async function openFromHash(focus) {
    const id = pondFromHash(location.hash);
    if (id === openId) return;
    if (openId && openId !== id) shownKey = null;      // a key is never shown again after leaving its pond
    openId = id;
    detail = null;
    renderDetail();
    if (!id) return;
    window.scrollTo(0, 0);
    await loadDetail();
    renderDetail();
    if (focus) $("pond-detail-name").focus({ preventScroll: true });
  }

  // ---------------------------------------------------------------- alerts from all ponds (Alerts page)

  function renderAlerts() {
    const alerts = data ? data.alerts : [];
    const hasPonds = Boolean(data && data.ponds.length);
    $("pond-alerts-card").hidden = !hasPonds;
    $("pond-alerts-empty").hidden = alerts.length > 0;
    $("pond-alerts-list").replaceChildren(...alerts.map((a) => {
      const item = make("li", `history-item level-${a.level}`);
      const meta = make("div", "history-meta");
      meta.append(badge(a.level, a.level_name[lang]), make("span", "history-time", timeText(a.time)),
        make("strong", "history-where", a.pond_name));
      if (a.demo) meta.append(make("span", "sim-tag", words.simulatedTag));
      item.append(meta, make("p", "history-cause", a.summary[lang]));
      return item;
    }));
  }

  // ---------------------------------------------------------------- farm code (More page)

  function renderFarm() {
    $("farm-code").textContent = formatFarmCode(farmCode);
    $("farm-not-saved").hidden = codeSaved;
    if (justDeleted) {
      $("delete-all-status").textContent = DELETED_TEXT[lang];
      $("delete-all-status").dataset.ok = "true";
    }
  }

  // ---- delete all my data (More page)
  // The server deletes first; only if that worked is this browser cleared. Then the
  // page reloads, so nothing stays in memory, with ?deleted=1 to say it is done.

  const DELETED_PARAM = "deleted";
  const DELETED_TEXT = { en: "All your data was deleted. This phone now has a new, empty farm code.",
    kn: "ನಿಮ್ಮ ಎಲ್ಲಾ ಡೇಟಾ ಅಳಿಸಲಾಗಿದೆ. ಈ ಫೋನ್‌ಗೆ ಈಗ ಹೊಸ, ಖಾಲಿ ಫಾರ್ಮ್ ಕೋಡ್ ಇದೆ." };
  let justDeleted = false;

  async function deleteAll() {
    const status = $("delete-all-status");
    if (!window.confirm(words.deleteAllConfirm(formatFarmCode(farmCode)))) return;
    const button = $("delete-all");
    button.disabled = true;
    status.textContent = words.deleteAllBusy;
    status.dataset.ok = "true";
    try {
      await call("/api/farm", { method: "DELETE" });
    } catch {
      button.disabled = false;
      status.textContent = words.deleteAllFailed;
      status.dataset.ok = "false";
      return;
    }
    clearTimeout(timer);
    clearSavedData(browserStorage());
    window.location.replace(`/?${DELETED_PARAM}=1#/more`);
  }

  // After the reload: show "deleted" once, then take ?deleted=1 out of the address.
  function noteDeleted() {
    const params = new URLSearchParams(window.location.search);
    if (!params.has(DELETED_PARAM)) return;
    justDeleted = true;
    params.delete(DELETED_PARAM);
    const query = params.toString();
    history.replaceState(null, "", window.location.pathname + (query ? `?${query}` : "") + window.location.hash);
  }

  async function copyText(text, button) {
    let ok = false;
    try { if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); ok = true; } } catch { ok = false; }
    const label = button.querySelector("span") || button;
    const before = label.textContent;
    label.textContent = ok ? words.copied : words.copyByHand;
    setTimeout(() => { label.textContent = before; }, 2000);
  }

  function useCode(event) {
    event.preventDefault();
    const code = normalizeFarmCode($("farm-input").value);
    const status = $("farm-status");
    if (!code) { status.textContent = words.farmBad; status.dataset.ok = "false"; return; }
    if (code === farmCode) { status.textContent = words.farmSwitched(formatFarmCode(code)); status.dataset.ok = "true"; return; }
    if (!window.confirm(words.farmSwitchConfirm)) return;
    farmCode = code;
    saveFarmCode(code);
    data = null;
    $("farm-input").value = "";
    status.textContent = words.farmSwitched(formatFarmCode(code));
    status.dataset.ok = "true";
    renderFarm();
    refresh();
  }

  // ---------------------------------------------------------------- add, edit, delete, devices

  // The place list, downloaded once. Without it (no internet) the place can be chosen later.
  async function loadPlaces() {
    if (placeList) return;
    try {
      const response = await fetch("/api/places");
      if (response.ok) placeList = (await response.json()).districts;
    } catch { placeList = null; }
  }

  function option(value, text) {
    const node = make("option", "", text);
    node.value = value;
    return node;
  }

  // District dropdown: "Not chosen", then the three districts (value = position in the list).
  function fillDistricts(selected) {
    $("pond-district").replaceChildren(option("", words.pondDistrictNone),
      ...(placeList || []).map((d, i) => option(String(i), d.name[lang])));
    $("pond-district").value = selected;
  }

  // Village dropdown for the chosen district, grouped by taluk. Its value is the village name (what is saved).
  function fillVillages(selected) {
    const district = $("pond-district").value === "" ? null : placeList[Number($("pond-district").value)];
    const groups = district ? district.taluks.map((t) => {
      const group = make("optgroup");
      group.label = words.pondTaluk(t.name[lang]);
      group.append(...t.places.map((p) => option(p.village, p.name[lang])));
      return group;
    }) : [];
    $("pond-village").replaceChildren(option("", district ? words.pondVillageNone : words.pondVillageFirst), ...groups);
    $("pond-village").disabled = !district;
    $("pond-village").value = selected || "";
  }

  function fillPlace(location) {
    const index = location && placeList ? placeList.findIndex((d) => d.name.en === location.district.en) : -1;
    fillDistricts(index >= 0 ? String(index) : "");
    fillVillages(index >= 0 ? location.village : null);
  }

  async function openDialog(pond, focusId = "pond-name") {
    editing = pond ? pond.id : null;
    $("pond-dialog-title").textContent = pond ? words.pondDialogEdit : words.pondDialogAdd;
    $("pond-name").value = pond ? pond.name : "";
    $("pond-size").value = pond && pond.size ? pond.size : "";
    $("pond-fish").value = pond && pond.fish ? pond.fish : "";
    $("pond-form-error").hidden = true;
    await loadPlaces();
    fillPlace(pond && pond.location);
    $("pond-place-help").closest("fieldset").hidden = !placeList;
    $("pond-dialog").showModal();
    $(placeList ? focusId : "pond-name").focus();
  }

  async function savePond(event) {
    event.preventDefault();
    const name = $("pond-name").value.trim();
    const error = $("pond-form-error");
    if (!name) { error.textContent = words.pondNameMissing; error.hidden = false; $("pond-name").focus(); return; }
    const village = $("pond-village").value || null;
    if (placeList && $("pond-district").value !== "" && !village) {
      error.textContent = words.pondVillageMissing; error.hidden = false; $("pond-village").focus(); return;
    }
    const fields = { pond_name: name, size: $("pond-size").value.trim() || null, fish: $("pond-fish").value.trim() || null };
    if (placeList) fields.village = village;          // no list (offline): leave the saved village as it is
    const body = JSON.stringify(fields);
    try {
      if (editing) await call(`/api/ponds/${editing}`, { method: "PATCH", body });
      else await call("/api/ponds", { method: "POST", body });
    } catch (e) {
      error.textContent = e.body && e.body.message ? e.body.message[lang] : words.pondSaveFailed;
      error.hidden = false;
      return;
    }
    $("pond-dialog").close();
    await refresh();
  }

  async function deletePond() {
    if (!detail || detail.missing || !window.confirm(words.pondDeleteConfirm(detail.name))) return;
    try { await call(`/api/ponds/${openId}`, { method: "DELETE" }); } catch { /* already gone: go back anyway */ }
    location.hash = "#/pond";
    await refresh();
  }

  async function deviceAction(kind) {
    if (kind === "new-key" && !window.confirm(words.deviceNewKeyConfirm)) return;
    if (kind === "remove" && !window.confirm(words.deviceRemoveConfirm)) return;
    const path = `/api/ponds/${openId}/device`;
    try {
      if (kind === "remove") { await call(path, { method: "DELETE" }); shownKey = null; }
      else {
        const made = await call(kind === "new-key" ? `${path}/new-key` : path, { method: "POST" });
        shownKey = { pondId: openId, ...made };
      }
    } catch (e) {
      window.alert(e.body && e.body.message ? e.body.message[lang] : words.pondSaveFailed);
    }
    await refresh();
    if (shownKey && kind !== "remove") $("device-key-box").scrollIntoView({ block: "nearest" });
  }

  // ---------------------------------------------------------------- setup

  function renderAll() {
    if (!words) return;
    renderList();
    renderDetail();
    renderAlerts();
    renderFarm();
  }

  function init() {
    noteDeleted();
    farmCode = loadFarmCode();
    $("pond-add").addEventListener("click", () => openDialog(null));
    $("pond-form").addEventListener("submit", savePond);
    $("pond-cancel").addEventListener("click", () => $("pond-dialog").close());
    $("pond-dialog").addEventListener("click", (e) => { if (e.target === e.currentTarget) e.currentTarget.close(); });
    $("pond-edit").addEventListener("click", () => detail && !detail.missing && openDialog(detail));
    $("pond-weather-choose").addEventListener("click", () => detail && !detail.missing && openDialog(detail, "pond-district"));
    $("pond-district").addEventListener("change", () => fillVillages(null));
    $("pond-delete").addEventListener("click", deletePond);
    $("device-connect").addEventListener("click", () => deviceAction("connect"));
    $("device-new-key").addEventListener("click", () => deviceAction("new-key"));
    $("device-remove").addEventListener("click", () => deviceAction("remove"));
    $("device-key-done").addEventListener("click", () => { shownKey = null; renderDetail(); $("device-status").scrollIntoView({ block: "nearest" }); });
    document.querySelectorAll("[data-copy]").forEach((b) => {
      b.addEventListener("click", () => copyText($(b.dataset.copy).textContent, b));
    });
    $("farm-copy").addEventListener("click", () => copyText(formatFarmCode(farmCode), $("farm-copy")));
    $("farm-form").addEventListener("submit", useCode);
    $("delete-all").addEventListener("click", deleteAll);
    window.addEventListener("hashchange", () => openFromHash(true));
    document.addEventListener("visibilitychange", () => { if (!document.hidden && !timer) refresh(); });
    openFromHash(false);
    refresh();
  }

  // The language changed (app.js setLanguage).
  function render(newLang, newWords) {
    lang = newLang;
    words = newWords;
    renderAll();
    if ($("pond-dialog").open && placeList) {          // dropdowns open in the old language: refill, keep the choice
      const [district, village] = [$("pond-district").value, $("pond-village").value];
      fillDistricts(district);
      fillVillages(village);
    }
  }

  // The pond in the worst state, for the status strip (null: no pond has a reading).
  function worst() {
    return data && data.worst ? data.ponds.find((p) => p.id === data.worst) || null : null;
  }

  init();
  window.Ponds = { ...api, render, worst, refresh, deviceLine: (p) => (words ? deviceLine(p) : null), timeText };
})();
