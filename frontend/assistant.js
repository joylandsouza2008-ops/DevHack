// "Ask MeenuRaksha" farmer assistant chat (card on the dashboard).
//
// The page never talks to the AI and never sees a key: it sends the question
// and the readings it is showing to our server (POST /api/assistant/ask), which
// answers only from the app's own content and checks every reply
// (backend/assistant.py). Every answer is labelled: "AI answer" or
// "Ready answer from the app", plus the data it used ("Simulated data", ...).
//
// When the AI can't answer (no key, no internet, error, too many questions),
// the suggested questions give READY answers built from our content, so the
// demo never breaks. Each reply has a speaker button (voice.js) that reads it aloud.

(function () {
  "use strict";

  const SPEAKER = '<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9H4Z" fill="currentColor"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';

  let lang = "kn";
  let words = null;                 // TEXT[lang] from app.js
  let page = () => ({});            // the readings the page is showing (from app.js)
  let suggestions = [];             // last ready answers from the server: [{id, question, answer}]
  let label = null;                 // "AI assistant: can make mistakes"
  let notice = null;                // {en, kn} from the server, or a page-text key
  let voiceNote = null;
  let speakingId = null;
  const messages = [];              // {id, role: "user" | "assistant", kind, text | texts, lang, used}
  let nextId = 1;
  let busy = false;
  const READING_ANSWERS = ["pond_now", "what_to_do", "likely_now"];   // ready answers built from the readings

  const $ = (id) => document.getElementById(id);
  const V = () => window.VoiceAlert;

  function make(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  // Text of a message in the language it is shown in. Ready answers exist in both
  // languages and follow the page; AI answers stay in the language they were asked in.
  function messageText(m) {
    if (m.key) return { text: words[m.key], lang };          // page text, e.g. "could not reach the server"
    return m.texts ? { text: m.texts[lang], lang } : { text: m.text, lang: m.lang };
  }

  async function post(url, body) {
    const response = await fetch(url, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error(response.statusText);
    return response.json();
  }

  // ---------------------------------------------------------------- render

  function usedTags(used) {
    return (used || []).map((source) => source === "simulated" ? make("span", "sim-tag", words.simulatedTag)
      : make("span", "badge badge-info", source === "manual" ? words.historyKit : words.historySensor));
  }

  function bubble(m) {
    const item = make("li", `chat-message chat-${m.role}${m.kind ? ` chat-${m.kind}` : ""}`);
    if (m.role === "user") {
      item.append(make("span", "visually-hidden", `${words.assistantYou}: `), make("p", "chat-text", m.text));
      return item;
    }
    if (m.kind === "pending") {
      item.append(make("p", "chat-text chat-pending", words.assistantThinking));
      return item;
    }
    const { text, lang: textLang } = messageText(m);
    const meta = make("div", "chat-meta");
    const kindWord = { ai: words.assistantAiAnswer, unknown: words.assistantAiAnswer,
      ready: words.assistantReady, safety: words.assistantSafety, notice: words.assistantNotice }[m.kind]
      || words.assistantReady;
    meta.append(make("span", m.kind === "ai" || m.kind === "unknown" ? "chat-kind chat-kind-ai" : "chat-kind", kindWord),
      ...usedTags(m.used));
    const body = make("p", "chat-text", text);
    body.lang = textLang;
    const speak = make("button", "button-secondary voice-button chat-speak");
    speak.type = "button";
    speak.innerHTML = SPEAKER;
    speak.append(make("span", "", speakingId === m.id ? words.voiceStop : words.assistantListen));
    speak.setAttribute("aria-pressed", String(speakingId === m.id));
    speak.addEventListener("click", () => toggleSpeak(m));
    item.append(meta, body, speak);
    return item;
  }

  function renderSuggestions() {
    $("suggestion-list").replaceChildren(...suggestions.map((s) => {
      const button = make("button", "suggestion", s.question[lang]);
      button.type = "button";
      button.disabled = busy;
      button.addEventListener("click", () => askSuggestion(s.id));
      return button;
    }));
  }

  function render() {
    if (!words) return;
    $("assistant-label").textContent = label ? label[lang] : words.assistantLabel;
    $("chat-log").replaceChildren(...messages.map(bubble));
    $("chat-log").hidden = messages.length === 0;
    const note = $("assistant-notice");
    note.hidden = !notice;
    note.textContent = !notice ? "" : typeof notice === "string" ? words[notice] : notice[lang];
    const vn = $("chat-voice-note");
    vn.hidden = !voiceNote;
    vn.textContent = voiceNote ? words[voiceNote] : "";
    renderSuggestions();
    $("chat-send").disabled = busy;
  }

  function scrollToLatest() {
    const log = $("chat-log");
    const last = log.lastElementChild;
    if (last) last.scrollIntoView({ block: "nearest", behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }

  // ---------------------------------------------------------------- voice (only when tapped)

  async function toggleSpeak(m) {
    if (speakingId === m.id) { V().stop(); speakingId = null; render(); return; }
    V().stop();
    const { text, lang: textLang } = messageText(m);
    speakingId = m.id;
    const result = await V().speak(text, textLang, () => { if (speakingId === m.id) { speakingId = null; render(); } });
    // Never fall back to another language's voice: say why nothing plays.
    voiceNote = result === "unsupported" ? "voiceUnsupported"
      : result === "no-voice" ? (textLang === "kn" ? "voiceNoKannada" : "voiceNoEnglish") : null;
    if (result !== "started") speakingId = null;
    render();
  }

  // ---------------------------------------------------------------- asking

  async function refreshSuggestions() {
    try {
      const body = await post("/api/assistant/suggestions", page());
      suggestions = body.suggestions;
      label = body.label;
    } catch { /* keep the last ready answers we have */ }
  }

  async function askSuggestion(id) {
    if (busy) return;
    busy = true;
    render();
    await refreshSuggestions();                     // ready answers for the readings shown right now
    busy = false;
    const s = suggestions.find((x) => x.id === id);
    if (!s) { render(); return; }
    notice = null;
    messages.push({ id: nextId++, role: "user", text: s.question[lang] });
    messages.push({ id: nextId++, role: "assistant", kind: "ready", texts: s.answer,
      used: READING_ANSWERS.includes(id) ? page().used : [] });
    render();
    scrollToLatest();
  }

  function history() {
    // Earlier AI turns only (ready answers are not sent back to the AI).
    const turns = [];
    messages.forEach((m, i) => {
      const next = messages[i + 1];
      if (m.role === "user" && next && next.kind === "ai") {
        turns.push({ role: "user", content: m.text }, { role: "assistant", content: next.text });
      }
    });
    return turns.slice(-4);
  }

  async function submit(event) {
    event.preventDefault();
    const input = $("chat-input");
    const question = input.value.trim();
    if (!question || busy) { if (!question) { notice = "assistantEmpty"; render(); } return; }
    busy = true;
    notice = null;
    const past = history();
    messages.push({ id: nextId++, role: "user", text: question });
    const pending = { id: nextId++, role: "assistant", kind: "pending" };
    messages.push(pending);
    input.value = "";
    render();
    scrollToLatest();
    let body = null;
    try {
      body = await post("/api/assistant/ask", { ...page(), question, lang, history: past });
    } catch { /* server not reachable: ready answers below */ }
    messages.splice(messages.indexOf(pending), 1);
    busy = false;
    if (body && body.label) label = body.label;
    if (body && body.text) {
      const kind = body.mode === "safety" ? "safety" : body.mode === "unknown" ? "unknown" : "ai";
      messages.push({ id: nextId++, role: "assistant", kind, text: body.text, lang: body.lang,
        used: kind === "ai" ? body.used : [] });          // refusals and "I don't know" use no readings
    } else {
      // No AI answer: say why in the chat, and point to the suggested questions (ready answers).
      messages.push(body ? { id: nextId++, role: "assistant", kind: "notice", texts: body.notice }
        : { id: nextId++, role: "assistant", kind: "notice", key: "assistantFailed" });
      if (body && body.suggestions) suggestions = body.suggestions;
    }
    render();
    scrollToLatest();
    if (!body || !body.text) $("suggestion-list").querySelector("button")?.focus({ preventScroll: true });
  }

  // ---------------------------------------------------------------- setup

  function setLanguage(language, t) {
    lang = language;
    words = t;
    voiceNote = null;
    render();
  }

  function init(getPage, language, t) {
    page = () => {
      const p = getPage();
      p.used = ["live_sensor", "manual", "simulated"].filter((s) => p[s]);
      return p;
    };
    lang = language;
    words = t;
    $("chat-form").addEventListener("submit", submit);
    $("chat-input").addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); $("chat-form").requestSubmit(); }
    });
    $("assistant-notice").tabIndex = -1;
    refreshSuggestions().then(render);
    render();
  }

  window.Assistant = { init, setLanguage, refreshSuggestions };
})();
