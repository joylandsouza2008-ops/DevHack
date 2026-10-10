// Tonight's oxygen crash risk, worked out in the browser.
//
// Why this exists: the free Render server could not download the forecast
// from Open-Meteo (cloud servers share IP addresses, and free weather services
// often refuse or limit them). The phone has its own internet, and Open-Meteo
// allows web pages to call it directly, so the page downloads the forecast
// itself and applies the SAME rules as backend/weather.py:
//   cloudy day (06:00-18:00) + still night + warm night -> count the factors,
//   0 = Low, 1 = Medium, 2 or 3 = High.
// The numbers below must match config/thresholds.toml [night_crash]
// (a test checks this: node --test tests/js).
//
// Real weather data, not simulated. Never used to train a model.

(function () {
  "use strict";

  const LOCATION = { name: { en: "Mangaluru", kn: "ಮಂಗಳೂರು" }, latitude: 12.9141, longitude: 74.8560 };
  const RULES = { cloudy_day_min_cloud_pct: 75, still_night_max_wind_kmh: 7, warm_night_min_temp_c: 28 };
  const HOUR = 3600 * 1000;
  const IST_OFFSET = 5.5 * HOUR;             // India is UTC+05:30 all year

  const LEVEL_NAMES = {
    low:    { en: "Low",    kn: "ಕಡಿಮೆ" },
    medium: { en: "Medium", kn: "ಮಧ್ಯಮ" },
    high:   { en: "High",   kn: "ಹೆಚ್ಚು" },
  };
  const FACTOR_WORDS = {
    cloudy: { en: "cloudy", kn: "ಮೋಡ ಕವಿದ" },
    still:  { en: "still",  kn: "ಗಾಳಿಯಿಲ್ಲದ" },
    warm:   { en: "warm",   kn: "ಸೆಖೆಯ" },
  };
  const ADVICE = {
    low:    { en: "Weather looks fine tonight: low risk of an oxygen crash.",
              kn: "ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ ಸರಿಯಾಗಿದೆ: ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯ ಕಡಿಮೆ." },
    medium: { en: "{night} night ahead: check the pond late at night and before dawn.",
              kn: "{night} ರಾತ್ರಿ ಬರಲಿದೆ: ತಡರಾತ್ರಿ ಮತ್ತು ಬೆಳಗಾಗುವ ಮೊದಲು ಕೊಳವನ್ನು ನೋಡಿ." },
    high:   { en: "{night} night ahead: keep the aerator ready.",
              kn: "{night} ರಾತ್ರಿ ಬರಲಿದೆ: ಏರೇಟರ್ ಸಿದ್ಧವಾಗಿಡಿ." },
  };

  function forecastUrl() {
    const query = new URLSearchParams({
      latitude: LOCATION.latitude, longitude: LOCATION.longitude,
      hourly: "temperature_2m,cloud_cover,wind_speed_10m",
      timezone: "Asia/Kolkata", past_days: 1, forecast_days: 3,
    });
    return `https://api.open-meteo.com/v1/forecast?${query}`;
  }

  // Forecast hours are India time with no zone ("2026-10-10T18:00"). They are
  // read as if UTC, and "now" is shifted by +05:30 to match, so the
  // phone's own time zone setting never matters.
  const hourValue = (text) => Date.parse(`${text}Z`);
  const indiaNow = (nowMs) => nowMs + IST_OFFSET;
  const isoMinutes = (ms) => new Date(ms).toISOString().slice(0, 16);

  // (day start, night start, night end). Before 06:00, "tonight" is the night we are in.
  function tonightWindow(nowIndia) {
    const d = new Date(nowIndia);
    let day = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate());
    if (d.getUTCHours() < 6) day -= 24 * HOUR;
    return [day + 6 * HOUR, day + 18 * HOUR, day + 30 * HOUR];
  }

  const mean = (list) => list.reduce((a, b) => a + b, 0) / list.length;
  const round1 = (x) => Math.round(x * 10) / 10;

  function summarise(forecast, nowIndia) {
    const hourly = forecast && forecast.hourly;
    if (!hourly || !Array.isArray(hourly.time)) return null;
    const [dayStart, nightStart, nightEnd] = tonightWindow(nowIndia);
    const times = hourly.time.map(hourValue);
    const values = (name, start, end) => times
      .map((t, i) => [t, (hourly[name] || [])[i]])
      .filter(([t, v]) => t >= start && t < end && v !== null && v !== undefined)
      .map(([, v]) => v);
    const cloud = values("cloud_cover", dayStart, nightStart);
    const wind = values("wind_speed_10m", nightStart, nightEnd);
    const temp = values("temperature_2m", nightStart, nightEnd);
    if (cloud.length < 6 || wind.length < 6 || temp.length < 6) return null;   // need half of each 12 h window
    return {
      night_start: isoMinutes(nightStart), night_end: isoMinutes(nightEnd),
      day_cloud_cover_pct: Math.round(mean(cloud)),
      night_wind_speed_kmh: round1(mean(wind)),
      night_temperature_c: round1(mean(temp)),
    };
  }

  function rateCrashRisk(cloudPct, windKmh, tempC, rules = RULES) {
    const factors = [];
    if (cloudPct >= rules.cloudy_day_min_cloud_pct) factors.push("cloudy");
    if (windKmh < rules.still_night_max_wind_kmh) factors.push("still");
    if (tempC >= rules.warm_night_min_temp_c) factors.push("warm");
    const level = factors.length === 0 ? "low" : factors.length === 1 ? "medium" : "high";
    const message = {};
    for (const lang of ["en", "kn"]) {
      let night = factors.map((f) => FACTOR_WORDS[f][lang]).join(", ");
      if (lang === "en") night = night.charAt(0).toUpperCase() + night.slice(1);
      message[lang] = ADVICE[level][lang].replace("{night}", night);
    }
    return { level, level_name: LEVEL_NAMES[level], factors, message };
  }

  // Same shape as GET /api/weather/tonight. savedAtMs = when the forecast was
  // downloaded; null result means the forecast doesn't reach tonight.
  function tonightFromForecast(forecast, savedAtMs, nowMs, offline) {
    const weather = summarise(forecast, indiaNow(nowMs));
    if (!weather) return null;
    return {
      source: "open-meteo", location: LOCATION.name, offline, status: "ok",
      saved_at: new Date(savedAtMs).toISOString(),
      ...weather,
      ...rateCrashRisk(weather.day_cloud_cover_pct, weather.night_wind_speed_kmh, weather.night_temperature_c),
    };
  }

  // Download straight from Open-Meteo. Throws on no internet, a slow reply or a bad answer.
  async function download(fetchFn = fetch, timeoutMs = 8000) {
    const controller = typeof AbortController !== "undefined" ? new AbortController() : null;
    const timer = controller && setTimeout(() => controller.abort(), timeoutMs);
    try {
      const response = await fetchFn(forecastUrl(), controller ? { signal: controller.signal } : {});
      if (!response.ok) throw new Error(`Open-Meteo replied ${response.status}`);
      const forecast = await response.json();
      if (!forecast || !forecast.hourly) throw new Error("Open-Meteo reply has no hourly forecast");
      return forecast;
    } finally {
      if (timer) clearTimeout(timer);
    }
  }

  // Minutes since the forecast was downloaded. The server's saved_at has no
  // zone and is India time; the browser's has a "Z".
  function minutesSince(savedAt, nowMs) {
    if (!savedAt) return null;
    const hasZone = /(Z|[+-]\d\d:\d\d)$/.test(savedAt);
    const ms = Date.parse(hasZone ? savedAt : `${savedAt}+05:30`);
    return Number.isNaN(ms) ? null : Math.max(0, Math.floor((nowMs - ms) / 60000));
  }

  const STORAGE_KEY = "meenuraksha-weather-forecast";   // last forecast this browser downloaded

  const readSaved = (storage) => { try { return JSON.parse(storage.getItem(STORAGE_KEY)); } catch { return null; } };
  const writeSaved = (storage, value) => { try { storage.setItem(STORAGE_KEY, JSON.stringify(value)); } catch { /* storage blocked */ } };

  // The whole plan, in order:
  //   1. download from Open-Meteo in this browser (works even when our server can't);
  //   2. else ask our server (GET /api/weather/tonight);
  //   3. else the newest saved forecast (this browser's, or the server's), marked offline;
  //   4. else null: the page says tonight's weather is not known.
  // fetchFn, storage and nowMs can be swapped out in tests, so no test touches the internet.
  async function loadTonight({ fetchFn = fetch, storage = null, nowMs = Date.now(), log = () => {} } = {}) {
    try {
      const forecast = await download(fetchFn);
      const result = tonightFromForecast(forecast, nowMs, nowMs, false);
      if (result) {
        if (storage) writeSaved(storage, { saved_at: nowMs, forecast });
        return result;
      }
      log("Open-Meteo forecast does not reach tonight");
    } catch (error) {
      log(`Weather download in the browser failed: ${error && error.message}`);
    }

    let server = null;
    try {
      const response = await fetchFn("/api/weather/tonight");
      if (response.ok) server = await response.json();
    } catch (error) {
      log(`Weather from our server failed: ${error && error.message}`);
    }
    if (server && server.status === "ok" && !server.offline) return server;

    const saved = storage && readSaved(storage);
    const mine = saved && saved.forecast ? tonightFromForecast(saved.forecast, saved.saved_at, nowMs, true) : null;
    const theirs = server && server.status === "ok" ? { ...server, offline: true } : null;
    const age = (w) => minutesSince(w.saved_at, nowMs);
    const copies = [mine, theirs].filter(Boolean).sort((a, b) => age(a) - age(b));
    return copies[0] || null;
  }

  const api = { LOCATION, RULES, STORAGE_KEY, forecastUrl, tonightWindow, summarise, rateCrashRisk,
                tonightFromForecast, download, minutesSince, loadTonight };
  if (typeof module !== "undefined" && module.exports) module.exports = api;   // Node tests
  if (typeof window !== "undefined") window.TonightWeather = api;
})();
