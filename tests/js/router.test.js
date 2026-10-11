// Tests for the page addresses (frontend/router.js): #/pond, #/alerts ...
// Run from the project folder with:   node --test tests/js

const test = require("node:test");
const assert = require("node:assert/strict");
const R = require("../../frontend/router.js");

test("there are seven pages, six tabs, and Pond is home", () => {
  assert.deepEqual(R.PAGES, ["pond", "alerts", "weather", "diseases", "ask", "more", "shop"]);
  assert.deepEqual(R.TABS, ["pond", "alerts", "weather", "diseases", "ask", "more"]);
  assert.equal(R.HOME, "pond");
});

test("each page address opens that page", () => {
  for (const page of R.PAGES) assert.equal(R.pageFromHash(`#/${page}`), page);
});

test("small differences in the address still work", () => {
  assert.equal(R.pageFromHash("#alerts"), "alerts");
  assert.equal(R.pageFromHash("#/ALERTS"), "alerts");
  assert.equal(R.pageFromHash("#/weather/"), "weather");
  assert.equal(R.pageFromHash("#/more?x=1"), "more");
});

test("no address or an unknown one opens the Pond page", () => {
  for (const hash of ["", "#", "#/", "#/nothing", "#/<script>", undefined, null]) {
    assert.equal(R.pageFromHash(hash), "pond", String(hash));
  }
});

test("the Shop page opens from #/shop and lights up the More tab", () => {
  assert.equal(R.pageFromHash("#/shop"), "shop");
  assert.equal(R.pageFromHash("#/SHOP/"), "shop");
  assert.equal(R.tabFor("shop"), "more");
  for (const tab of R.TABS) assert.equal(R.tabFor(tab), tab);
});
