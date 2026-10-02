// Tests for the alert history list logic (frontend/history.js).
// Run from the project folder with:   node --test tests/js

const test = require("node:test");
const assert = require("node:assert/strict");
const H = require("../../frontend/history.js");

function streamEvent(level, time, causes = ["dissolved_oxygen"]) {
  return {
    source: "simulated", station: "station1", time,
    risk: {
      level, causes,
      summary: { en: "Oxygen is low.", kn: "ಆಮ್ಲಜನಕ ಕಡಿಮೆ." },
      actions: [{ id: "aerator_now", en: "Run the aerator now.", kn: "ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ.", sources: [1] }],
    },
  };
}

test("an entry keeps time, level, cause, actions and is marked simulated", () => {
  const entry = H.entryFrom(streamEvent("danger", "2026-10-02T21:40:00"), "k1");
  assert.equal(entry.source, "simulated");
  assert.equal(entry.station, "station1");
  assert.equal(entry.time, "2026-10-02T21:40:00");
  assert.equal(entry.level, "danger");
  assert.deepEqual(entry.summary, { en: "Oxygen is low.", kn: "ಆಮ್ಲಜನಕ ಕಡಿಮೆ." });
  assert.deepEqual(entry.actions, [{ id: "aerator_now", en: "Run the aerator now.", kn: "ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ." }]);
  assert.deepEqual(entry.done, []);
});

test("test-kit entries are marked manual, not simulated", () => {
  const data = { ...streamEvent("warning", "2026-10-02T10:00"), source: "manual", station: undefined };
  const entry = H.entryFrom(data, "k");
  assert.equal(entry.source, "manual");
  assert.equal(entry.station, null);
});

test("newest entry first, and the same alert is not added twice", () => {
  let list = [];
  list = H.addEntry(list, H.entryFrom(streamEvent("warning", "T1"), "a"));
  list = H.addEntry(list, H.entryFrom(streamEvent("danger", "T2"), "b"));
  list = H.addEntry(list, H.entryFrom(streamEvent("danger", "T2"), "b"));   // replayed demo
  assert.deepEqual(list.map((e) => e.time), ["T2", "T1"]);
});

test("the list is capped so storage never fills up", () => {
  let list = [];
  for (let i = 0; i < H.MAX_ENTRIES + 10; i++) list = H.addEntry(list, H.entryFrom(streamEvent("warning", `T${i}`), "k"));
  assert.equal(list.length, H.MAX_ENTRIES);
  assert.equal(list[0].time, `T${H.MAX_ENTRIES + 9}`);
});

test("ticked actions are saved on the newest matching entry only", () => {
  let list = [];
  list = H.addEntry(list, H.entryFrom(streamEvent("danger", "T1"), "same"));
  list = H.addEntry(list, H.entryFrom(streamEvent("danger", "T2"), "same"));
  const marked = H.markDone(list, "same", new Set(["aerator_now"]));
  assert.deepEqual(marked[0].done, ["aerator_now"]);
  assert.deepEqual(marked[1].done, []);
  assert.deepEqual(list[0].done, [], "original list is not changed");
  assert.equal(H.markDone(list, "missing", ["x"]), list);
});

test("load / save survive a refresh, and bad storage gives an empty list", () => {
  const store = {};
  global.localStorage = { getItem: (k) => store[k] ?? null, setItem: (k, v) => { store[k] = v; } };
  const list = H.addEntry([], H.entryFrom(streamEvent("danger", "T1"), "k"));
  H.save(list);
  assert.deepEqual(H.load(), list);
  store[H.STORAGE_KEY] = "not json";
  assert.deepEqual(H.load(), []);
  global.localStorage = { getItem: () => { throw new Error("blocked"); }, setItem: () => { throw new Error("blocked"); } };
  assert.deepEqual(H.load(), []);
  assert.doesNotThrow(() => H.save(list));
  delete global.localStorage;
});
