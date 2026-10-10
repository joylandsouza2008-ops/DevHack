// Pages inside the one app: Pond, Alerts, Weather, Diseases, Ask, More.
// The address ends in #/pond, #/alerts ... so the phone's back button works,
// and nothing new is downloaded when you switch (the app stays fast and works
// offline). Every page is already in index.html; switching just shows one and
// hides the others. The simulator keeps running underneath (app.js).
//
// Clean-up when leaving a page: its short animations jump to their end (so no
// card is left half-faded), and the looping ones (pond view, health ring,
// sky) pause by themselves because a hidden page is "off screen" for them.
// The ?debug counts (debug.js) show whether anything piles up.

(function () {
  "use strict";

  const PAGES = ["pond", "alerts", "weather", "diseases", "ask", "more"];
  const HOME = "pond";

  // "#/alerts" -> "alerts". Anything unknown (or empty) -> the Pond page.
  function pageFromHash(hash) {
    const name = String(hash || "").replace(/^#\/?/, "").split(/[/?]/)[0].toLowerCase();
    return PAGES.includes(name) ? name : HOME;
  }

  const api = { PAGES, HOME, pageFromHash };
  if (typeof module !== "undefined" && module.exports) { module.exports = api; return; }   // Node tests

  const gsap = window.gsap;
  const reduceQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  const reduce = () => reduceQuery.matches || !gsap;
  const pages = Object.fromEntries(PAGES.map((p) => [p, document.getElementById(`page-${p}`)]));
  const scrollTops = {};                     // where each page was scrolled to, for the back button
  let current = null;
  let titles = {};                           // page name -> title in the current language

  // Finish (never freeze half-way) every short animation inside a page that is
  // being hidden. A card killed at opacity 0.4 would stay faded on the next visit.
  function settle(page) {
    if (!gsap) return;
    const targets = [page, ...page.querySelectorAll(".te-word, .in-view, .status-icon, .status-text")];
    gsap.getTweensOf(targets).forEach((t) => {
      if (t.vars.repeat === -1) return;      // loops pause by themselves when hidden
      t.progress(1).kill();
    });
  }

  function markTabs(name) {
    document.querySelectorAll("[data-tab]").forEach((tab) => {
      if (tab.dataset.tab === name) tab.setAttribute("aria-current", "page");
      else tab.removeAttribute("aria-current");
    });
  }

  function setTitle() {
    if (current && titles[current]) document.title = `${titles[current]} · AquaNexus`;
  }

  function show(name, { focus = true } = {}) {
    const next = pages[name];
    if (!next) return;
    if (current === name) { markTabs(name); return; }
    const previous = current && pages[current];
    if (previous) {
      scrollTops[current] = window.scrollY;
      settle(previous);
      previous.hidden = true;
    }
    current = name;
    next.hidden = false;
    markTabs(name);
    setTitle();
    window.scrollTo(0, scrollTops[name] || 0);
    // A light fade-and-rise. Only one page transition runs at a time.
    if (!reduce() && previous) {
      gsap.killTweensOf(Object.values(pages));
      gsap.fromTo(next, { opacity: 0, y: 10 },
        { opacity: 1, y: 0, duration: 0.28, ease: "power2.out", clearProps: "opacity,transform" });
    }
    if (focus && previous) focusPage();
    document.dispatchEvent(new CustomEvent("pagechange", { detail: { page: name } }));
  }

  // Move keyboard / screen-reader focus to the new page's heading.
  function focusPage() {
    const heading = pages[current] && pages[current].querySelector(".page-title");
    if (heading) heading.focus({ preventScroll: true });
  }

  function onHashChange() {
    const name = pageFromHash(location.hash);
    if (`#/${name}` !== location.hash) history.replaceState(null, "", `#/${name}`);
    show(name);
  }

  // The language changed: new page titles (for the browser tab and history list).
  function setTitles(map) {
    titles = map;
    setTitle();
  }

  function init() {
    PAGES.forEach((p) => { if (pages[p]) pages[p].hidden = true; });
    const name = pageFromHash(location.hash);
    if (`#/${name}` !== location.hash) history.replaceState(null, "", `#/${name}`);
    show(name, { focus: false });
    window.addEventListener("hashchange", onHashChange);
    // Tapping the tab of the page you are on: back to the top of it.
    document.querySelectorAll("[data-tab]").forEach((tab) => {
      tab.addEventListener("click", () => {
        if (tab.dataset.tab === current) window.scrollTo({ top: 0, behavior: reduce() ? "auto" : "smooth" });
      });
    });
  }

  window.Router = { ...api, init, show, current: () => current, focusPage, setTitles };
})();
