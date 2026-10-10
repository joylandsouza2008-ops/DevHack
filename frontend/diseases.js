// Fish disease guide (card on the dashboard): disease library, symptom
// checker and "diseases more likely now" notes for risky readings.
//
// The data and the matching come from the server (backend/diseases.py,
// GET /api/diseases and POST /api/diseases/check), so the page works offline
// with the local server. Sources for every entry: docs/diseases.md.
//
// Rules: possible matches only, never a diagnosis; no medicines or doses.
// The drawings are simple original SVGs. Disease marks use the magenta accent
// (decoration), never the Safe / Warning / Danger colours (DESIGN.md).

(function () {
  "use strict";

  let guide = null;            // GET /api/diseases, once
  let lastCheck = null;        // last POST /api/diseases/check result
  let words = null;            // page labels in the current language (TEXT[lang] from app.js)
  let lang = "kn";

  const $ = (id) => document.getElementById(id);

  function make(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  // ---------------------------------------------------------------- drawings
  // One outline fish (head left, tail right) plus the marks of each disease.

  const BODY = "M12 34C26 12 70 9 90 27L111 13 105 34 111 55 90 41C70 59 26 56 12 34Z";
  const SWOLLEN = "M12 34C26 12 70 9 90 27L111 13 105 34 111 55 90 41C76 66 26 64 12 34Z";
  const MARKS = {
    eus: '<circle class="mark" cx="58" cy="36" r="6"/><circle class="mark-ring" cx="58" cy="36" r="8.5"/>' +
      '<circle class="mark" cx="76" cy="31" r="3.5"/><circle class="mark" cx="44" cy="42" r="2.5"/>',
    aeromoniasis: '<path class="mark-line" d="M60 24l4 3-4 3M68 23l4 3-4 3M76 24l4 3-4 3M64 33l4 3-4 3M72 33l4 3-4 3"/>' +
      '<circle class="mark" cx="50" cy="47" r="3"/><circle class="mark" cx="86" cy="40" r="2.5"/>',
    gill_disease: '<path class="shade" d="M12 34C17 25 26 19 40 17Q47 34 40 51C26 49 17 43 12 34Z"/>' +
      '<path class="mark-line" d="M36 24l4 4M34 30l5 4M34 37l5 4M36 44l4 3"/>',
    columnaris: '<path class="mark-line" d="M105 34l6-6-4-3 5-4M105 34l6 6-4 3 5 4"/>' +
      '<path class="mark" d="M58 16c6-2 14-1 18 3-3 4-15 5-18-3Z"/><circle class="mark" cx="64" cy="40" r="2.5"/>',
    saprolegniasis: '<path class="tuft" d="M58 30c-3-6 4-9 6-5 1-5 9-4 8 1 5-1 7 6 2 8-1 4-8 5-10 1-4 3-9-1-6-5Z"/>' +
      '<path class="tuft" d="M80 38c-2-4 3-6 5-3 2-3 7-1 5 3 3 2 0 6-3 4-2 3-7 1-7-4Z"/>',
    argulosis: '<ellipse class="mark-flat" cx="56" cy="30" rx="5.5" ry="4.5"/><ellipse class="mark-flat" cx="74" cy="40" rx="5" ry="4"/>' +
      '<ellipse class="mark-flat" cx="44" cy="40" rx="4" ry="3.2"/><circle class="mark" cx="56" cy="30" r="1.2"/>' +
      '<circle class="mark" cx="74" cy="40" r="1.2"/><circle class="mark" cx="44" cy="40" r="1"/>',
    flukes: '<path class="mark-line" d="M44 22c3 2-1 4 2 6M47 33c3 2-1 4 2 6M44 43c3 2-1 4 2 6"/>' +
      '<path class="gap" d="M40 19Q48 34 40 49"/>',
    white_spot: [[32, 26], [46, 22], [54, 32], [64, 24], [70, 36], [80, 30], [50, 44], [62, 46], [40, 38], [86, 38], [74, 46], [58, 18]]
      .map(([x, y]) => `<circle class="spot" cx="${x}" cy="${y}" r="1.8"/>`).join(""),
    anchor_worm: '<circle class="mark-ring" cx="56" cy="22" r="3"/><path class="mark-line" d="M56 20l-4-12M52 8l-2-3M52 8l2-3"/>' +
      '<circle class="mark-ring" cx="72" cy="44" r="3"/><path class="mark-line" d="M72 46l5 11M77 57l-2 3M77 57l3 1"/>' +
      '<circle class="mark-ring" cx="84" cy="30" r="2.5"/><path class="mark-line" d="M85 28l6-10"/>',
  };

  function fishSVG(id, label) {
    const body = id === "aeromoniasis" ? SWOLLEN : BODY;
    const eye = id === "aeromoniasis" ? '<circle class="eye-pop" cx="26" cy="29" r="5"/><circle class="pupil" cx="25" cy="29" r="2.4"/>'
      : '<circle class="pupil" cx="26" cy="29" r="2.4"/>';
    const gill = id === "flukes" ? "" : '<path class="line" d="M40 19Q47 34 40 49"/>';
    const safeLabel = label.replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);   // label comes from the server
    return `<svg class="fish-art" viewBox="0 0 120 68" role="img" aria-label="${safeLabel}">` +
      `<path class="fin" d="M50 15Q60 3 72 14"/><path class="fin" d="M52 52Q58 62 66 54"/>` +
      `<path class="fish" d="${body}"/>${gill}${eye}${MARKS[id] || ""}</svg>`;
  }

  // ---------------------------------------------------------------- library

  function list(tag, items) {
    const el = make(tag);
    el.append(...items.map((item) => make("li", "", item[lang])));
    return el;
  }

  function field(label, content) {
    const box = make("div", "disease-field");
    box.append(make("h4", "", label), typeof content === "string" ? make("p", "", content) : content);
    return box;
  }

  function diseaseEntry(id, d) {
    const other = lang === "kn" ? "en" : "kn";
    const entry = make("details", "disease");
    entry.id = `disease-${id}`;
    const summary = make("summary");
    summary.innerHTML = fishSVG(id, `${d.name[lang]}: ${words.guideDrawing}`);
    const title = make("span", "disease-title");
    const name = make("span", "disease-name", d.name[lang]);
    const otherName = make("span", "disease-other", d.name[other]);
    otherName.lang = other;
    title.append(name, otherName, make("span", "badge badge-info", guide.cause_types[d.cause][lang]));
    summary.append(title);

    const body = make("div", "disease-body");
    const agent = make("p", "disease-agent");
    agent.append(`${words.guideAgent}: `, make("em", "", d.agent));
    body.append(
      agent,
      field(words.guideBody, d.body[lang]),
      field(words.guideBehaviour, d.behaviour[lang]),
      field(words.guideWhen, d.when[lang]),
      field(words.guidePrevention, list("ul", d.prevention)),
      field(words.guideDo, list("ol", [...d.do, ...guide.common_steps])),
      make("p", "guide-warning", guide.treatment_note[lang]),
      make("p", "disease-sources", `${words.guideSourcesShort}: ${d.sources.map((s) => guide.sources[s]).join(" · ")}`),
    );
    entry.append(summary, body);
    return entry;
  }

  function renderLibrary() {
    $("disease-library").replaceChildren(...Object.entries(guide.diseases).map(([id, d]) => diseaseEntry(id, d)));
  }

  // Open a disease in the library and scroll to it (from a checker result or a reading note).
  function show(id) {
    const entry = $(`disease-${id}`);
    if (!entry) return;
    entry.open = true;
    entry.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
    entry.querySelector("summary").focus({ preventScroll: true });
  }

  function showButton(id, text) {
    const button = make("button", "button-ghost guide-link", text);
    button.type = "button";
    button.addEventListener("click", () => show(id));
    return button;
  }

  // ---------------------------------------------------------------- symptom checker

  function renderSigns() {
    const ticked = new Set([...document.querySelectorAll("#checker-form input:checked")].map((b) => b.value));
    for (const group of ["body", "behaviour"]) {
      const box = $(`checker-${group}`);
      box.replaceChildren(...Object.entries(guide.signs).filter(([, s]) => s.group === group).map(([id, s]) => {
        const label = make("label", "action-item");
        label.innerHTML = '<input type="checkbox" name="sign">' +
          '<span class="action-box" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="m5 12.5 4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>' +
          '<span class="action-text"></span>';
        const input = label.querySelector("input");
        input.value = id;
        input.checked = ticked.has(id);
        label.querySelector(".action-text").textContent = s[lang];
        return label;
      }));
    }
  }

  function renderResult() {
    const box = $("checker-result");
    box.hidden = !lastCheck;
    if (!lastCheck) return;
    const parts = lastCheck.notes.map((n) => make("p", "guide-note", n[lang]));
    if (lastCheck.matches.length) {
      parts.push(make("h4", "", words.checkerMatches));
      const items = make("ol", "match-list");
      items.append(...lastCheck.matches.map((m) => {
        const item = make("li", "match");
        item.append(make("strong", "", m.name[lang]),
          make("span", "match-signs", `${words.checkerMatched}: ${m.matched_signs.map((s) => guide.signs[s][lang]).join(", ")}`),
          showButton(m.id, words.guideRead));
        return item;
      }));
      parts.push(items);
      if (lastCheck.more) parts.push(make("p", "match-more", words.checkerMore(lastCheck.more)));
    }
    parts.push(make("p", "guide-warning", lastCheck.treatment_note[lang]));
    // Always last: possible matches only, confirm with the fisheries officer.
    parts.push(make("p", "checker-message", lastCheck.message[lang]));
    box.replaceChildren(...parts);
  }

  async function submitCheck(event) {
    event.preventDefault();
    const signs = [...document.querySelectorAll("#checker-form input:checked")].map((b) => b.value);
    const error = $("checker-error");
    error.hidden = signs.length > 0;
    error.textContent = signs.length ? "" : words.checkerEmpty;
    if (!signs.length) { lastCheck = null; renderResult(); return; }
    try {
      const response = await fetch("/api/diseases/check", {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ signs }),
      });
      if (!response.ok) throw new Error(response.statusText);
      lastCheck = await response.json();
    } catch {
      error.hidden = false;
      error.textContent = words.guideFailed;
      return;
    }
    renderResult();
    $("checker-result").focus();
  }

  // ---------------------------------------------------------------- "more likely now" for a reading

  // Fill `box` with the diseases this reading makes more likely (risk.likely_diseases), or hide it.
  function renderLikely(box, likely, language, t) {
    box.hidden = !likely || likely.length === 0;
    if (box.hidden) { box.replaceChildren(); return; }
    const key = `${language}|${likely.map((d) => d.id).join(",")}`;
    if (box.dataset.key === key) return;           // same note: keep it (and keyboard focus) as it is
    box.dataset.key = key;
    const items = make("ul", "likely-list");
    items.append(...likely.map((d) => {
      const item = make("li");
      item.append(make("strong", "", d.name[language]), " ",
        make("span", "", d.reasons.map((r) => r[language]).join(" ")), " ",
        showButton(d.id, t.guideRead));
      return item;
    }));
    const title = make("h3", "likely-title", t.likelyTitle);
    title.id = `${box.id}-title`;
    box.replaceChildren(title, items,
      make("p", "likely-note", guide ? guide.likely_note[language] : t.likelyNote));
  }

  // ---------------------------------------------------------------- setup

  function render(language, t) {
    lang = language;
    words = t;
    if (!guide) return;
    $("guide-treatment").textContent = guide.treatment_note[lang];
    renderSigns();
    const open = [...document.querySelectorAll("#disease-library details[open]")].map((d) => d.id);
    renderLibrary();
    open.forEach((id) => { $(id).open = true; });   // keep open entries open when the language changes
    renderResult();
  }

  async function init(language, t) {
    lang = language;
    words = t;
    $("checker-form").addEventListener("submit", submitCheck);
    $("checker-form").addEventListener("reset", () => {
      lastCheck = null;
      $("checker-error").hidden = true;
      renderResult();
    });
    $("checker-result").tabIndex = -1;
    try {
      const response = await fetch("/api/diseases");
      if (!response.ok) throw new Error(response.statusText);
      guide = await response.json();
    } catch {
      $("guide-loading").textContent = words.guideFailed;
      return;
    }
    $("guide-loading").hidden = true;
    $("guide-content").hidden = false;
    render(lang, words);
  }

  window.DiseaseGuide = { init, render, renderLikely, show, fishSVG };
})();
