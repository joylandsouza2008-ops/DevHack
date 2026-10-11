// Alert history: a log of past Warning and Danger alerts, saved in this
// browser (localStorage) so it survives a refresh.
//
// Each entry keeps: when it happened, Safe/Warning/Danger, the cause (in
// English and Kannada), the suggested actions, and which ones the farmer
// ticked as done ("action taken"). Simulated alerts are stored with
// source = "simulated" and always shown with the "Simulated data" tag.
//
// The list logic (addEntry, markDone) is plain functions so it can be tested
// with Node: node --test tests/js

(function () {
  "use strict";

  const STORAGE_KEY = "meenuraksha-history";
  const MAX_ENTRIES = 50;            // oldest entries are dropped after this

  // Add one alert to the front of the list (newest first). The same alert is
  // not added twice (e.g. replaying the same demo after Restart).
  function addEntry(list, entry) {
    if (list.some((e) => e.id === entry.id)) return list;
    return [entry, ...list].slice(0, MAX_ENTRIES);
  }

  // Record which actions were ticked for an alert. Only the newest entry with
  // this checklist key changes: ticks belong to the alert happening now.
  function markDone(list, key, doneIds) {
    const index = list.findIndex((e) => e.key === key);
    if (index === -1) return list;
    const copy = list.slice();
    copy[index] = { ...copy[index], done: [...doneIds] };
    return copy;
  }

  // Build an entry from one API result (simulated stream or test kit).
  function entryFrom(data, key) {
    const risk = data.risk;
    return {
      id: `${data.source}|${data.station || "kit"}|${data.time}|${risk.level}|${risk.causes.join(",")}`,
      key,
      source: data.source,                     // "simulated", "manual" or "live_sensor"
      demo: Boolean(data.demo),                // live_sensor from a demo device (made-up readings)
      station: data.station || null,
      time: data.time,
      level: risk.level,
      causes: risk.causes,                     // e.g. ["dissolved_oxygen"]: for the assistant's Shop advice
      summary: risk.summary,                   // {en, kn}
      actions: risk.actions.map((a) => ({ id: a.id, en: a.en, kn: a.kn })),
      done: [],
    };
  }

  function load() {
    try {
      const list = JSON.parse(localStorage.getItem(STORAGE_KEY));
      return Array.isArray(list) ? list.slice(0, MAX_ENTRIES) : [];
    } catch {
      return [];                               // nothing saved, or storage blocked
    }
  }

  function save(list) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(list)); } catch { /* storage full or blocked */ }
  }

  // What the assistant gets from the history (for Shop advice such as "night oxygen
  // problems"): only source, level, causes and time of the newest alerts. Older
  // entries have no causes field, so they are read from the entry id.
  function recentAlerts(list, max = 20) {
    return list.filter((e) => e.level === "warning" || e.level === "danger").slice(0, max).map((e) => ({
      source: e.source,
      level: e.level,
      causes: (e.causes || String(e.id).split("|")[4]?.split(",") || []).filter(Boolean).slice(0, 6),
      time: e.time ? String(e.time).slice(0, 40) : null,
    }));
  }

  const api = { STORAGE_KEY, MAX_ENTRIES, addEntry, markDone, entryFrom, load, save, recentAlerts };
  if (typeof module !== "undefined" && module.exports) module.exports = api;   // Node tests
  if (typeof window !== "undefined") window.AlertHistory = api;
})();
