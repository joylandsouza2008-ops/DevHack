// Tests for tonight's weather in the browser (frontend/weather.js).
// No test touches the internet: fetch is a fake that returns a made-up forecast.
// Run from the project folder with:   node --test tests/js

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const W = require("../../frontend/weather.js");

const HOUR = 3600 * 1000;
// 2 Oct 2026, 15:00 in India = 09:30 UTC (the same afternoon the Python tests use).
const AFTERNOON = Date.parse("2026-10-02T15:00:00+05:30");

// Open-Meteo-shaped forecast: the same values every hour for 4 days from 1 Oct, India time.
function fakeForecast({ cloud = 50, wind = 12, temp = 26, start = "2026-10-01T00:00" } = {}) {
  const first = Date.parse(`${start}Z`);
  const time = Array.from({ length: 96 }, (_, h) => new Date(first + h * HOUR).toISOString().slice(0, 16));
  return { hourly: { time, cloud_cover: time.map(() => cloud), wind_speed_10m: time.map(() => wind),
                     temperature_2m: time.map(() => temp) } };
}

// A pretend network. `openMeteo` / `server` are a reply object, or "down" to throw like no internet.
function fakeFetch({ openMeteo = "down", server = "down" } = {}) {
  const calls = [];
  const fn = async (url) => {
    calls.push(url);
    const reply = url.startsWith("https://api.open-meteo.com/") ? openMeteo : server;
    if (reply === "down") throw new TypeError("Failed to fetch");
    return { ok: reply.ok !== false, status: reply.status || 200, json: async () => reply.body };
  };
  fn.calls = calls;
  return fn;
}

function fakeStorage(initial = {}) {
  const data = { ...initial };
  return { getItem: (k) => (k in data ? data[k] : null), setItem: (k, v) => { data[k] = String(v); }, data };
}

// --- the rules: same answers, same words as backend/weather.py ---------------

test("rules match config/thresholds.toml", () => {
  const toml = fs.readFileSync(path.join(__dirname, "../../config/thresholds.toml"), "utf8");
  const section = toml.split("[night_crash]")[1].split(/\n\[/)[0];
  for (const [name, value] of Object.entries(W.RULES)) {
    const match = section.match(new RegExp(`^${name}\\s*=\\s*([\\d.]+)`, "m"));
    assert.ok(match, name);
    assert.equal(Number(match[1]), value, name);
  }
});

test("low, medium and high, with the same messages as the server", () => {
  const low = W.rateCrashRisk(40, 12, 26);
  assert.equal(low.level, "low");
  assert.equal(low.message.en, "Weather looks fine tonight: low risk of an oxygen crash.");
  assert.equal(W.rateCrashRisk(40, 3, 26).message.en.startsWith("Still night ahead"), true);
  const high = W.rateCrashRisk(90, 3, 26);
  assert.equal(high.level, "high");
  assert.equal(high.message.en, "Cloudy, still night ahead: keep the aerator ready.");
  assert.equal(high.message.kn, "ಮೋಡ ಕವಿದ, ಗಾಳಿಯಿಲ್ಲದ ರಾತ್ರಿ ಬರಲಿದೆ: ಏರೇಟರ್ ಸಿದ್ಧವಾಗಿಡಿ.");
  assert.deepEqual(high.level_name, { en: "High", kn: "ಹೆಚ್ಚು" });
  assert.deepEqual(W.rateCrashRisk(75, 6.9, 28).factors, ["cloudy", "still", "warm"]);   // edges count
  assert.deepEqual(W.rateCrashRisk(74, 7, 27.9).factors, []);
});

test("tonight is 18:00 to 06:00 India time, whatever the phone's time zone", () => {
  // summarise takes "now" already shifted to India time (+05:30).
  const s = W.summarise(fakeForecast(), AFTERNOON + 5.5 * HOUR);
  assert.equal(s.night_start, "2026-10-02T18:00");
  assert.equal(s.night_end, "2026-10-03T06:00");
  // 02:00 in India on 3 Oct is still the night of 2 Oct.
  const beforeDawn = Date.parse("2026-10-03T02:00:00+05:30") + 5.5 * HOUR;
  assert.equal(W.summarise(fakeForecast(), beforeDawn).night_start, "2026-10-02T18:00");
});

test("a forecast that doesn't reach tonight gives no answer", () => {
  assert.equal(W.tonightFromForecast(fakeForecast({ start: "2026-09-01T00:00" }), AFTERNOON, AFTERNOON, false), null);
});

// --- where the forecast comes from -------------------------------------------

test("1. downloads in the browser and saves a copy", async () => {
  const fetchFn = fakeFetch({ openMeteo: { body: fakeForecast({ cloud: 90, wind: 3 }) } });
  const storage = fakeStorage();
  const r = await W.loadTonight({ fetchFn, storage, nowMs: AFTERNOON });
  assert.equal(r.status, "ok");
  assert.equal(r.offline, false);
  assert.equal(r.level, "high");
  assert.equal(r.location.en, "Mangaluru");
  assert.equal(fetchFn.calls.length, 1);                      // the server was not needed
  assert.ok(fetchFn.calls[0].includes("timezone=Asia%2FKolkata"));
  assert.ok(storage.data[W.STORAGE_KEY]);
  assert.equal(W.minutesSince(r.saved_at, AFTERNOON + 7 * 60000), 7);
});

test("2. Open-Meteo blocked or refusing: asks our server", async () => {
  const server = { status: "ok", offline: false, level: "low", saved_at: "2026-10-02T14:50" };
  for (const openMeteo of ["down", { ok: false, status: 429, body: {} }]) {
    const fetchFn = fakeFetch({ openMeteo, server: { body: server } });
    const r = await W.loadTonight({ fetchFn, storage: fakeStorage(), nowMs: AFTERNOON });
    assert.deepEqual(r, server);
    assert.equal(fetchFn.calls[1], "/api/weather/tonight");
  }
});

test("3. no internet at all: the saved forecast, marked offline", async () => {
  const storage = fakeStorage();
  await W.loadTonight({ fetchFn: fakeFetch({ openMeteo: { body: fakeForecast({ cloud: 90, wind: 3 }) } }),
                        storage, nowMs: AFTERNOON });
  const later = AFTERNOON + 3 * HOUR;
  const r = await W.loadTonight({ fetchFn: fakeFetch(), storage, nowMs: later });
  assert.equal(r.status, "ok");
  assert.equal(r.offline, true);
  assert.equal(r.level, "high");
  assert.equal(W.minutesSince(r.saved_at, later), 180);
});

test("3. the newer of the browser's and the server's saved copies wins", async () => {
  const storage = fakeStorage({ [W.STORAGE_KEY]: JSON.stringify({ saved_at: AFTERNOON - 2 * HOUR, forecast: fakeForecast() }) });
  const server = { status: "ok", offline: true, level: "medium", saved_at: "2026-10-02T14:30" };   // 30 min old
  const r = await W.loadTonight({ fetchFn: fakeFetch({ server: { body: server } }), storage, nowMs: AFTERNOON });
  assert.equal(r.level, "medium");
  assert.equal(r.offline, true);
});

test("4. nothing anywhere: no answer, and broken saved data is ignored", async () => {
  const unavailable = { status: "unavailable", offline: true, saved_at: null, level: null };
  const storage = fakeStorage({ [W.STORAGE_KEY]: "not json" });
  assert.equal(await W.loadTonight({ fetchFn: fakeFetch({ server: { body: unavailable } }), storage, nowMs: AFTERNOON }), null);
  assert.equal(await W.loadTonight({ fetchFn: fakeFetch(), storage: null, nowMs: AFTERNOON }), null);
});

test("minutesSince reads the server's India time and the browser's UTC time alike", () => {
  const now = Date.parse("2026-10-02T15:10:00+05:30");
  assert.equal(W.minutesSince("2026-10-02T15:00", now), 10);
  assert.equal(W.minutesSince("2026-10-02T09:30:00.000Z", now), 10);
  assert.equal(W.minutesSince(null, now), null);
});
