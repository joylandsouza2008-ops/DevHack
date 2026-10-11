// Tests for the Shop cart (frontend/shop.js) and products (frontend/shop-data.js).
// No browser needed: the cart is given a pretend localStorage.
// Run from the project folder with:   node --test tests/js

const test = require("node:test");
const assert = require("node:assert/strict");
const S = require("../../frontend/shop.js");
const { PRODUCTS } = require("../../frontend/shop-data.js");

const IDS = PRODUCTS.map((p) => p.id);
const EN = { estWord: "est.", cartTotal: "Estimated total", shopPriceNote: "Estimated component cost. Prices may change.",
  copyHeading: "AquaNexus: my list (estimated prices, not an order)" };

// A pretend localStorage. `broken` makes every call throw, like a blocked private window.
function fakeStorage({ broken = false, start = {} } = {}) {
  const data = { ...start };
  const guard = () => { if (broken) throw new Error("SecurityError"); };
  return {
    data,
    getItem: (k) => { guard(); return k in data ? data[k] : null; },
    setItem: (k, v) => { guard(); data[k] = String(v); },
    removeItem: (k) => { guard(); delete data[k]; },
  };
}

test("every product has the fields the page shows, in English and Kannada", () => {
  assert.equal(PRODUCTS.length, 5);
  for (const p of PRODUCTS) {
    assert.match(p.id, /^[a-z0-9-]+$/);
    assert.ok(Number.isInteger(p.price) && p.price > 0, p.id);
    assert.ok(p.icon, p.id);
    for (const field of ["name", "desc", "measures", "why"]) {
      assert.ok(p[field].en && p[field].kn, `${p.id}.${field}`);
      assert.match(p[field].kn, /[ಀ-೿]/, `${p.id}.${field} Kannada`);
    }
  }
});

test("the estimated prices match the brief", () => {
  const price = Object.fromEntries(PRODUCTS.map((p) => [p.id, p.price]));
  assert.deepEqual(price, { "test-kit": 1200, "night-watch": 23000, "full-pond": 35000, "do-cap": 4000, "solar-10w": 1500 });
});

test("no product claims to be cheaper than other products", () => {
  const all = JSON.stringify(PRODUCTS).toLowerCase();
  for (const word of ["cheaper", "cheapest", "lowest price", "best price", "than other", "ಅಗ್ಗ"]) {
    assert.ok(!all.includes(word), word);
  }
});

test("prices always say they are estimates, with Indian digit grouping", () => {
  assert.equal(S.formatPrice(1200, "est."), "est. ₹1,200");
  assert.equal(S.formatPrice(23000, "est."), "est. ₹23,000");
  assert.equal(S.formatPrice(123456, "ಅಂದಾಜು"), "ಅಂದಾಜು ₹1,23,456");
  assert.equal(S.formatPrice(500, "est."), "est. ₹500");
});

test("add, change quantity, remove and clear", () => {
  const store = fakeStorage();
  const cart = S.createCart(store, IDS);
  cart.add("night-watch");
  cart.add("test-kit");
  cart.add("test-kit");
  assert.equal(cart.count(), 3);
  assert.equal(cart.qty("test-kit"), 2);
  cart.setQty("test-kit", 1);
  assert.equal(cart.qty("test-kit"), 1);
  cart.setQty("test-kit", 0);                    // below 1 removes the item
  assert.equal(cart.qty("test-kit"), 0);
  cart.remove("night-watch");
  assert.equal(cart.count(), 0);
  cart.add("do-cap");
  cart.clear();
  assert.deepEqual(cart.items(), []);
  assert.equal(store.data[S.STORAGE_KEY], undefined, "an empty cart leaves nothing behind");
});

test("the cart is saved under aquanexus_cart and comes back after a reload", () => {
  const store = fakeStorage();
  const first = S.createCart(store, IDS);
  first.add("full-pond");
  first.add("solar-10w");
  first.add("solar-10w");
  assert.equal(S.STORAGE_KEY, "aquanexus_cart");
  const again = S.createCart(store, IDS);        // like reloading the page
  assert.deepEqual(again.items(), [{ id: "full-pond", qty: 1 }, { id: "solar-10w", qty: 2 }]);
});

test("unknown items and bad quantities in a saved cart are dropped", () => {
  const saved = JSON.stringify([{ id: "test-kit", qty: 2 }, { id: "laptop", qty: 1 }, { id: "do-cap", qty: -3 },
    { id: "night-watch", qty: 1.5 }, { id: "test-kit", qty: 9 }, null, "x", { id: "solar-10w", qty: 999 }]);
  const cart = S.createCart(fakeStorage({ start: { aquanexus_cart: saved } }), IDS);
  assert.deepEqual(cart.items(), [{ id: "test-kit", qty: 2 }, { id: "solar-10w", qty: S.MAX_QTY }]);
  cart.add("laptop");
  assert.equal(cart.qty("laptop"), 0);
});

test("a broken saved cart (not JSON) starts empty instead of crashing", () => {
  const cart = S.createCart(fakeStorage({ start: { aquanexus_cart: "{not json" } }), IDS);
  assert.deepEqual(cart.items(), []);
  cart.add("test-kit");
  assert.equal(cart.count(), 1);
});

test("blocked storage: the cart still works, in memory", () => {
  const cart = S.createCart(fakeStorage({ broken: true }), IDS);
  assert.equal(cart.isMemoryOnly(), true);
  cart.add("night-watch");
  cart.add("night-watch");
  assert.equal(cart.qty("night-watch"), 2);
  const none = S.createCart(null, IDS);
  none.add("test-kit");
  assert.equal(none.count(), 1);
});

test("storage that fails on save (full) switches to memory and keeps the items", () => {
  const store = fakeStorage();
  store.setItem = () => { throw new Error("QuotaExceededError"); };
  const cart = S.createCart(store, IDS);
  cart.add("do-cap");
  assert.equal(cart.isMemoryOnly(), true);
  assert.equal(cart.qty("do-cap"), 1);
});

test("quantity stops at the maximum", () => {
  const cart = S.createCart(fakeStorage(), IDS);
  for (let i = 0; i < S.MAX_QTY + 5; i++) cart.add("test-kit");
  assert.equal(cart.qty("test-kit"), S.MAX_QTY);
});

test("the copied list is plain text: names, quantities, estimated prices and total", () => {
  const items = [{ id: "night-watch", qty: 1 }, { id: "test-kit", qty: 2 }];
  assert.equal(S.total(items, PRODUCTS), 25400);
  assert.equal(S.listText(items, PRODUCTS, "en", EN), [
    "AquaNexus: my list (estimated prices, not an order)",
    "- Night-Watch kit × 1: est. ₹23,000",
    "- Ammonia + pH test kit × 2: est. ₹2,400",
    "Estimated total: est. ₹25,400",
    "Estimated component cost. Prices may change.",
  ].join("\n"));
});
