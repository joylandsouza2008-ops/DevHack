// Tests for the farm code and pond addresses (frontend/ponds.js) and the
// router's pond dashboard address (frontend/router.js).
// Run from the project folder with:   node --test tests/js

const test = require("node:test");
const assert = require("node:assert/strict");
const P = require("../../frontend/ponds.js");
const R = require("../../frontend/router.js");

test("a farm code is 12 characters from the easy-to-read alphabet", () => {
  const bytes = Uint8Array.from({ length: 12 }, (_, i) => i * 37);
  const code = P.makeFarmCode(bytes);
  assert.equal(code.length, 12);
  for (const c of code) assert.ok(P.ALPHABET.includes(c), c);
  assert.ok(!/[ILOU]/.test(P.ALPHABET), "no I, L, O or U");
  assert.equal(P.formatFarmCode("K7QM3XRP9TFD"), "K7QM-3XRP-9TFD");
});

test("every byte value maps to a letter (no bias towards some letters)", () => {
  const seen = new Set();
  for (let b = 0; b < 256; b++) seen.add(P.makeFarmCode(new Uint8Array(12).fill(b))[0]);
  assert.equal(seen.size, 32);
});

test("a typed farm code is forgiving: spaces, dashes, small letters, O for 0, I or L for 1", () => {
  assert.equal(P.normalizeFarmCode("k7qm 3xrp-9tfd"), "K7QM3XRP9TFD");
  assert.equal(P.normalizeFarmCode("K7QM-3XRP-9TFO"), "K7QM3XRP9TF0");
  assert.equal(P.normalizeFarmCode("I7QM-3XRP-9TFL"), "17QM3XRP9TF1");
  for (const bad of ["", null, undefined, "short", "K7QM-3XRP-9TFD-1", "K7QM-3XRP-9TF!", "UUUU-UUUU-UUUU"]) {
    assert.equal(P.normalizeFarmCode(bad), null, String(bad));
  }
});

test("only a real pond id opens a pond dashboard", () => {
  assert.equal(P.pondFromHash("#/pond/p-k7qm3xrp9t"), "p-k7qm3xrp9t");
  for (const hash of ["#/pond", "#/pond/", "#/pond/p-short", "#/pond/<script>", "#/alerts/p-k7qm3xrp9t", "", null]) {
    assert.equal(P.pondFromHash(hash), null, String(hash));
  }
});

test("the router keeps a pond dashboard address and tidies the others", () => {
  assert.equal(R.canonicalHash("#/pond/p-k7qm3xrp9t"), "#/pond/p-k7qm3xrp9t");
  assert.equal(R.pageFromHash("#/pond/p-k7qm3xrp9t"), "pond");
  assert.equal(R.canonicalHash("#/alerts/"), "#/alerts");
  assert.equal(R.canonicalHash("#/pond/<script>"), "#/pond");
  assert.equal(R.canonicalHash(""), "#/pond");
});

test("delete all my data clears only this app's saved keys", () => {
  const saved = new Map([
    ["meenuraksha-lang", "en"], ["meenuraksha-theme", "dark"], ["meenuraksha-ticks:danger-low-do", "[1]"],
    ["meenuraksha-history", "[]"], ["meenuraksha-weather-forecast:Kota", "{}"],
    ["aquanexus_farm_code", "K7QM3XRP9TFD"], ["aquanexus_cart", "[]"],
    ["some-other-site-key", "keep"],
  ]);
  const storage = {
    get length() { return saved.size; },
    key: (i) => [...saved.keys()][i] ?? null,
    removeItem: (k) => saved.delete(k),
  };
  P.clearSavedData(storage);
  assert.deepEqual([...saved.keys()], ["some-other-site-key"]);
  P.clearSavedData(null);              // storage blocked: nothing to do, no error
});
