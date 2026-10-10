// XSS test for the "Ask AquaNexus" chat (frontend/assistant.js) and the disease
// drawings (frontend/diseases.js): text from the server or the AI must be shown as
// plain text, never turned into HTML.
//
// A tiny pretend page (no browser needed) records every innerHTML write, so the
// test can check that the attack text only ever goes in through textContent.
// Run from the project folder with:   node --test tests/js

const test = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");

const ATTACK = '<script>alert("x")</script><img src=x onerror=alert(1)>';
const htmlWrites = [];

class FakeElement {
  constructor(tag) {
    this.tagName = tag.toUpperCase();
    this.children = [];
    this.listeners = {};
    this.attributes = {};
    this.className = "";
    this.hidden = false;
    this._text = "";
    this.value = "";
  }
  set textContent(v) { this._text = String(v); this.children = []; }
  get textContent() { return this._text + this.children.map((c) => (typeof c === "string" ? c : c.textContent)).join(""); }
  set innerHTML(v) { htmlWrites.push(String(v)); this._html = String(v); this.children = []; }
  get innerHTML() { return this._html || ""; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; }
  setAttribute(k, v) { this.attributes[k] = String(v); }
  addEventListener(type, fn) { this.listeners[type] = fn; }
  querySelector() { return null; }
  get lastElementChild() { return this.children[this.children.length - 1] || null; }
  scrollIntoView() {}
  focus() {}
  requestSubmit() {}
  // every element below this one (for finding the chat bubbles)
  all() { return this.children.flatMap((c) => (typeof c === "string" ? [] : [c, ...c.all()])); }
}

const elements = {};
global.window = global;
global.document = {
  createElement: (tag) => new FakeElement(tag),
  getElementById: (id) => (elements[id] ||= new FakeElement("div")),
};
global.matchMedia = () => ({ matches: true });
window.VoiceAlert = { stop() {}, speak: async () => "started" };

// Every page text is just its own name: enough for this test.
const words = new Proxy({}, { get: (_, key) => String(key) });

// The pretend server sends the attack text in an AI answer AND in a suggested question.
global.fetch = async (url) => ({
  ok: true,
  json: async () => (url === "/api/assistant/ask"
    ? { text: ATTACK, mode: "ai", lang: "en", used: ["simulated"], label: { en: ATTACK, kn: ATTACK } }
    : { label: { en: "AI assistant", kn: "AI" },
        suggestions: [{ id: "pond_now", question: { en: ATTACK, kn: ATTACK }, answer: { en: ATTACK, kn: ATTACK } }] }),
});

require(path.join(__dirname, "../../frontend/assistant.js"));
require(path.join(__dirname, "../../frontend/diseases.js"));

test("an AI reply with <script> or <img onerror> is shown as plain text", async () => {
  window.Assistant.init(() => ({ station: "station1", simulated: { dissolved_oxygen: 5 } }), "en", words);
  await new Promise((r) => setTimeout(r, 0));                 // suggestions arrive
  elements["chat-input"].value = "Is my pond ok?";
  await elements["chat-form"].listeners.submit({ preventDefault() {} });

  const bubbles = elements["chat-log"].all().filter((e) => e.className.includes("chat-text"));
  assert.ok(bubbles.some((b) => b.textContent === ATTACK), "the reply is shown, as text");
  assert.equal(elements["assistant-label"].textContent, ATTACK, "the label is shown as text too");
  assert.ok(elements["suggestion-list"].children.some((b) => b.textContent === ATTACK), "suggested question as text");

  // Nothing from the server ever went through innerHTML (only our own speaker icon did).
  for (const html of htmlWrites) {
    assert.ok(!html.includes("<script") && !html.includes("onerror"), `unsafe innerHTML write: ${html}`);
  }
});

test("disease names put into the drawing's label are escaped", () => {
  const svg = window.DiseaseGuide.fishSVG("eus", '"><img src=x onerror=alert(1)>');
  assert.ok(!svg.includes("<img"));
  assert.ok(svg.includes('aria-label="&#34;&#62;&#60;img src=x onerror=alert(1)&#62;"'));
});
