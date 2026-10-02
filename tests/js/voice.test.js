// Tests for voice selection (frontend/voice.js).
// Run from the project folder with:   node --test tests/js

const test = require("node:test");
const assert = require("node:assert/strict");
const V = require("../../frontend/voice.js");

const voice = (name, lang, localService = true) => ({ name, lang, localService });

test("picks a Kannada voice for Kannada", () => {
  const voices = [voice("English", "en-US"), voice("Kannada", "kn-IN")];
  assert.equal(V.pickVoice(voices, "kn").name, "Kannada");
});

test("no Kannada voice -> null, never an English voice instead", () => {
  const voices = [voice("English", "en-US"), voice("Hindi", "hi-IN")];
  assert.equal(V.pickVoice(voices, "kn"), null);
  assert.equal(V.pickVoice([], "kn"), null);
});

test("prefers offline (on-device) voices, then Indian English", () => {
  const voices = [
    voice("Online India", "en-IN", false),
    voice("Offline US", "en-US", true),
    voice("Offline India", "en-IN", true),
  ];
  assert.equal(V.pickVoice(voices, "en").name, "Offline India");
  assert.equal(V.pickVoice(voices.slice(0, 2), "en").name, "Offline US");
});

test("accepts lang codes written with an underscore (some Android browsers)", () => {
  assert.equal(V.pickVoice([voice("Kannada", "kn_IN")], "kn").name, "Kannada");
});

test("speak() without speech support says so instead of failing", async () => {
  assert.equal(V.supported(), false);
  assert.equal(await V.speak("hello", "en"), "unsupported");
  assert.doesNotThrow(() => V.stop());
});
