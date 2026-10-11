// Shop page (#/shop): product cards, a cart in a side drawer, and a
// "Checkout" panel that only says "Coming soon". Products: shop-data.json,
// the same file the assistant uses (backend/shop.py), so they never disagree.
//
// Nothing is sold and nothing is sent anywhere. There is no payment, no form
// for a name, phone or address, and nothing is sent: the page only downloads
// the product list (shop-data.json, a plain file). The cart lives only in
// this browser (localStorage "aquanexus_cart"). If the browser blocks
// storage (some private windows), the cart still works, in memory, until the
// page is closed. "Copy my list" puts plain text on the clipboard so a farmer
// can share it with their cooperative.
//
// Prices are estimates, always shown as "est. ₹X". A product with price_max has
// a range, "est. ₹X–Y", followed by its price_note ("depending on probes").

(function () {
  "use strict";

  const STORAGE_KEY = "aquanexus_cart";
  const MAX_QTY = 20;                          // per item: a list for a cooperative, not a warehouse

  // ---------------------------------------------------------------- pure helpers (also used by the Node tests)

  // 1200 -> "1,200", 123456 -> "1,23,456" (Indian grouping, same in both languages).
  function groupIndian(n) {
    const s = String(Math.round(Math.abs(n)));
    if (s.length <= 3) return s;
    const last3 = s.slice(-3);
    const rest = s.slice(0, -3).replace(/\B(?=(\d{2})+(?!\d))/g, ",");
    return `${rest},${last3}`;
  }

  // "est. ₹1,200" (English) or "ಅಂದಾಜು ₹1,200" (Kannada): every price says it is an estimate.
  // With a higher `max`: a range, "est. ₹23,000–71,000".
  function formatPrice(rupees, estWord, max) {
    const range = max > rupees ? `–${groupIndian(max)}` : "";
    return `${estWord} ₹${groupIndian(rupees)}${range}`;
  }

  // One product's price for `qty` of it, with its note if it has a range:
  // "est. ₹23,000–71,000 depending on probes".
  function productPrice(p, qty, lang, estWord) {
    const text = formatPrice(p.price * qty, estWord, (p.price_max || 0) * qty);
    return p.price_max && p.price_note ? `${text} ${p.price_note[lang]}` : text;
  }

  // Keep only known products with a whole quantity from 1 to MAX_QTY. Anything
  // else (an old or edited saved cart) is dropped, never shown.
  function cleanItems(raw, knownIds) {
    if (!Array.isArray(raw)) return [];
    const seen = new Set();
    const items = [];
    for (const entry of raw) {
      if (!entry || typeof entry !== "object") continue;
      const { id } = entry;
      const qty = Number(entry.qty);
      if (typeof id !== "string" || !knownIds.includes(id) || seen.has(id)) continue;
      if (!Number.isInteger(qty) || qty < 1) continue;
      seen.add(id);
      items.push({ id, qty: Math.min(qty, MAX_QTY) });
    }
    return items;
  }

  // The cart. `storage` is localStorage (or a stand-in in tests). Every read and
  // write is wrapped in try/catch: if storage fails once, the cart carries on in
  // memory and stops trying to save.
  function createCart(storage, knownIds) {
    let items = [];
    let memoryOnly = !storage;

    try {
      const saved = storage ? storage.getItem(STORAGE_KEY) : null;
      items = cleanItems(saved ? JSON.parse(saved) : [], knownIds);
    } catch {
      items = [];
      memoryOnly = true;
    }

    function save() {
      if (memoryOnly) return;
      try {
        if (items.length) storage.setItem(STORAGE_KEY, JSON.stringify(items));
        else storage.removeItem(STORAGE_KEY);
      } catch {
        memoryOnly = true;                       // full or blocked: keep going in memory
      }
    }

    const find = (id) => items.find((i) => i.id === id);

    return {
      items: () => items.map((i) => ({ ...i })),
      qty: (id) => (find(id) ? find(id).qty : 0),
      count: () => items.reduce((sum, i) => sum + i.qty, 0),
      isMemoryOnly: () => memoryOnly,
      add(id) {
        if (!knownIds.includes(id)) return;
        const item = find(id);
        if (item) item.qty = Math.min(item.qty + 1, MAX_QTY);
        else items.push({ id, qty: 1 });
        save();
      },
      setQty(id, qty) {
        const item = find(id);
        if (!item || !Number.isInteger(qty)) return;
        if (qty < 1) items = items.filter((i) => i.id !== id);
        else item.qty = Math.min(qty, MAX_QTY);
        save();
      },
      remove(id) {
        items = items.filter((i) => i.id !== id);
        save();
      },
      clear() {
        items = [];
        save();
      },
    };
  }

  // Estimated total as { low, high }: they differ when a product has a price range.
  function total(items, products) {
    return items.reduce((sum, i) => {
      const p = products.find((x) => x.id === i.id);
      if (!p) return sum;
      return { low: sum.low + p.price * i.qty, high: sum.high + (p.price_max || p.price) * i.qty };
    }, { low: 0, high: 0 });
  }

  function formatTotal(items, products, estWord) {
    const { low, high } = total(items, products);
    return formatPrice(low, estWord, high);
  }

  // The text "Copy my list" puts on the clipboard. Plain text only: names,
  // quantities, estimated prices and the estimated total.
  function listText(items, products, lang, words) {
    const lines = [words.copyHeading];
    for (const i of items) {
      const p = products.find((x) => x.id === i.id);
      if (!p) continue;
      lines.push(`- ${p.name[lang]} × ${i.qty}: ${productPrice(p, i.qty, lang, words.estWord)}`);
    }
    lines.push(`${words.cartTotal}: ${formatTotal(items, products, words.estWord)}`);
    lines.push(words.shopPriceNote);
    return lines.join("\n");
  }

  const api = { STORAGE_KEY, MAX_QTY, groupIndian, formatPrice, productPrice, cleanItems, createCart, total, formatTotal, listText };
  if (typeof module !== "undefined" && module.exports) { module.exports = api; return; }   // Node tests

  // ---------------------------------------------------------------- page

  let PRODUCTS = [];                           // filled from shop-data.json (load below)
  const gsap = window.gsap;
  const reduceQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  const reduce = () => reduceQuery.matches || !gsap;
  const $ = (id) => document.getElementById(id);

  let lang = "kn";
  let words = null;                            // TEXT[lang] from app.js
  let toastTimer = null;

  function browserStorage() {
    try { return window.localStorage; } catch { return null; }       // blocked in some private windows
  }
  let cart = createCart(null, []);             // empty until the products have loaded
  let loadFailed = false;

  function make(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  // Simple line drawings for the cards (fixed strings, no outside text in them).
  const ICONS = {
    testKit: '<rect x="14" y="10" width="12" height="38" rx="5"/><path d="M14 22h12"/><circle cx="44" cy="20" r="6"/><circle cx="44" cy="36" r="6"/><path d="M40 48h8"/>',
    nightWatch: '<path d="M38 12a14 14 0 1 0 10 22A11 11 0 0 1 38 12Z"/><rect x="10" y="40" width="20" height="14" rx="3"/><path d="M20 40v-8M14 54v4M26 54v4"/>',
    fullPond: '<path d="M6 40c6-4 10-4 16 0s10 4 16 0 10-4 16 0"/><path d="M6 50c6-4 10-4 16 0s10 4 16 0 10-4 16 0"/><rect x="22" y="8" width="16" height="22" rx="3"/><path d="M30 30v8"/>',
    sensorCap: '<rect x="20" y="8" width="20" height="30" rx="4"/><path d="M18 38h24v8a6 6 0 0 1-6 6H24a6 6 0 0 1-6-6v-8Z"/><path d="M26 18h8"/>',
    solar: '<path d="M10 40 18 14h28l8 26H10Z"/><path d="M14 27h36M24 14l-4 26M40 14l4 26M32 14v26"/><path d="M32 40v12M22 52h20"/>',
  };
  function icon(name) {
    const span = make("span", "shop-icon");
    span.setAttribute("aria-hidden", "true");
    span.innerHTML = `<svg viewBox="0 0 64 64">${ICONS[name] || ""}</svg>`;
    return span;
  }

  function renderGrid() {
    const grid = $("shop-grid");
    grid.replaceChildren(...PRODUCTS.map((p) => {
      const card = make("li", "card shop-card");
      const head = make("div", "shop-card-head");
      const title = make("h2", "shop-name", p.name[lang]);
      title.id = `shop-name-${p.id}`;
      head.append(icon(p.icon), title);
      const price = make("p", "shop-price", productPrice(p, 1, lang, words.estWord));
      const facts = make("dl", "shop-facts");
      facts.append(make("dt", "", words.shopMeasures), make("dd", "", p.measures[lang]),
        make("dt", "", words.shopWhy), make("dd", "", p.why[lang]));
      const add = make("button", "button-primary shop-add", words.shopAdd);
      add.type = "button";
      add.dataset.add = p.id;
      add.setAttribute("aria-describedby", title.id);
      card.append(head, make("p", "shop-desc", p.desc[lang]), facts, price, add);
      return card;
    }));
  }

  function renderLoadError() {
    $("shop-error").hidden = !loadFailed;
    if (loadFailed && words) $("shop-error").textContent = words.shopLoadFailed;
  }

  // The product list: one small plain file, also read by the assistant.
  async function loadProducts() {
    try {
      const response = await fetch("/shop-data.json");
      if (!response.ok) throw new Error(response.statusText);
      PRODUCTS = (await response.json()).products;
      cart = createCart(browserStorage(), PRODUCTS.map((p) => p.id));
      loadFailed = false;
    } catch {
      loadFailed = true;                       // weak signal: say so, and offer nothing to add
    }
    if (words) render(lang, words);
  }

  function renderBadge() {
    const n = cart.count();
    $("cart-count").textContent = String(n);
    $("cart-open").setAttribute("aria-label", words.cartAria.replace("{n}", n));
    // The Shop tab: count badge hidden at 0; the tab's name then is just its word.
    const tabBadge = $("tab-cart-count");
    tabBadge.textContent = String(n);
    tabBadge.hidden = n === 0;
    if (n) $("tab-shop").setAttribute("aria-label", `${words.tabShop}, ${words.cartAria.replace("{n}", n)}`);
    else $("tab-shop").removeAttribute("aria-label");
  }

  // The drawer is rebuilt on every change; focus goes back to the same control.
  function renderDrawer(focusKey) {
    const items = cart.items();
    const list = $("cart-list");
    list.replaceChildren(...items.map((i) => {
      const p = PRODUCTS.find((x) => x.id === i.id);
      const row = make("li", "cart-item");
      row.append(make("p", "cart-item-name", p.name[lang]));
      const controls = make("div", "cart-item-controls");
      const less = make("button", "cart-step", "−");
      less.type = "button";
      less.dataset.act = "less"; less.dataset.id = i.id;
      less.setAttribute("aria-label", `${words.cartLess}: ${p.name[lang]}`);
      less.disabled = i.qty <= 1;
      const qty = make("span", "cart-qty", String(i.qty));
      qty.setAttribute("aria-label", `${words.cartQty}: ${i.qty}`);
      const more = make("button", "cart-step", "+");
      more.type = "button";
      more.dataset.act = "more"; more.dataset.id = i.id;
      more.setAttribute("aria-label", `${words.cartMore}: ${p.name[lang]}`);
      more.disabled = i.qty >= MAX_QTY;
      const remove = make("button", "button-ghost cart-remove", words.cartRemove);
      remove.type = "button";
      remove.dataset.act = "remove"; remove.dataset.id = i.id;
      remove.setAttribute("aria-label", `${words.cartRemove}: ${p.name[lang]}`);
      controls.append(less, qty, more, remove);
      row.append(controls, make("p", "cart-item-price", productPrice(p, i.qty, lang, words.estWord)));
      return row;
    }));
    $("cart-empty").hidden = items.length > 0;
    $("cart-foot").hidden = items.length === 0;
    $("cart-total").textContent = formatTotal(items, PRODUCTS, words.estWord);
    $("cart-memory").hidden = !cart.isMemoryOnly();
    renderBadge();
    if (focusKey) {
      const [act, id] = focusKey;
      const again = list.querySelector(`[data-act="${act}"][data-id="${id}"]`);
      const target = again && !again.disabled ? again
        : list.querySelector(`[data-id="${id}"]:not(:disabled)`) || list.querySelector("button:not(:disabled)") || $("cart-close");
      target.focus();
    }
  }

  function renderCheckout() {
    $("checkout-list").textContent = listText(cart.items(), PRODUCTS, lang, words);
  }

  // One small message at the bottom of the screen. A new one replaces the old
  // (no stacking), and only one short fade runs at a time.
  function toast(text) {
    const box = $("shop-toast");
    box.textContent = text;
    box.hidden = false;
    clearTimeout(toastTimer);
    if (!reduce()) {
      gsap.killTweensOf(box);
      gsap.fromTo(box, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.2, ease: "power2.out", clearProps: "opacity,transform" });
    }
    toastTimer = setTimeout(() => { box.hidden = true; }, 2600);
  }

  function bumpBadge() {
    if (reduce()) return;
    const badge = $("cart-count");
    gsap.killTweensOf(badge);
    gsap.fromTo(badge, { scale: 1.3 }, { scale: 1, duration: 0.25, ease: "power2.out", clearProps: "transform" });
  }

  async function copyList() {
    const text = listText(cart.items(), PRODUCTS, lang, words);
    const status = $("copy-status");
    let ok = false;
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        ok = true;
      }
    } catch { ok = false; }
    if (!ok) {
      // Older phones: copy from a hidden text box.
      const area = make("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.className = "visually-hidden";
      document.body.append(area);
      area.select();
      try { ok = document.execCommand("copy"); } catch { ok = false; }
      area.remove();
      $("copy-list").focus();
    }
    status.textContent = ok ? words.copyDone : words.copyFailed;
    status.dataset.ok = String(ok);
  }

  function openDrawer() {
    renderDrawer();
    $("cart-drawer").showModal();
  }

  function init() {
    $("shop-grid").addEventListener("click", (e) => {
      const button = e.target.closest("[data-add]");
      if (!button) return;
      const p = PRODUCTS.find((x) => x.id === button.dataset.add);
      cart.add(p.id);
      renderBadge();
      bumpBadge();
      toast(`${words.shopAdded} ${p.name[lang]}`);
    });
    $("cart-open").addEventListener("click", openDrawer);
    $("cart-close").addEventListener("click", () => $("cart-drawer").close());
    $("cart-list").addEventListener("click", (e) => {
      const button = e.target.closest("[data-act]");
      if (!button || button.disabled) return;
      const { act, id } = button.dataset;
      if (act === "less") cart.setQty(id, cart.qty(id) - 1);
      if (act === "more") cart.setQty(id, cart.qty(id) + 1);
      if (act === "remove") cart.remove(id);
      renderDrawer([act, id]);
    });
    $("cart-clear").addEventListener("click", () => {
      cart.clear();
      renderDrawer();
      $("cart-close").focus();
      toast(words.cartCleared);
    });
    $("cart-checkout").addEventListener("click", () => {
      renderCheckout();
      $("copy-status").textContent = "";
      $("cart-drawer").close();
      $("checkout-dialog").showModal();
    });
    $("copy-list").addEventListener("click", copyList);
    $("checkout-close").addEventListener("click", () => $("checkout-dialog").close());
    $("checkout-back").addEventListener("click", () => { $("checkout-dialog").close(); openDrawer(); });
    // Leaving the Shop (for example with the phone's back button) closes its panels.
    document.addEventListener("pagechange", (e) => {
      if (e.detail.page === "shop") return;
      ["cart-drawer", "checkout-dialog"].forEach((id) => { if ($(id).open) $(id).close(); });
    });
    // Tap outside a panel to close it, as with the other panels.
    ["cart-drawer", "checkout-dialog"].forEach((id) => {
      $(id).addEventListener("click", (e) => { if (e.target === $(id)) $(id).close(); });
    });
  }

  // The language changed (app.js setLanguage).
  function render(newLang, newWords) {
    lang = newLang;
    words = newWords;
    renderGrid();
    renderLoadError();
    renderBadge();
    if ($("cart-drawer").open) renderDrawer();
    if ($("checkout-dialog").open) renderCheckout();
  }

  init();
  loadProducts();
  window.Shop = { ...api, render, cart: () => cart };
})();
