// Voice alerts: reads the current alert aloud with the phone's own speech
// voices (the browser's Web Speech API). Nothing plays by itself: speech only
// starts when the farmer taps the speaker button.
//
// It never switches language on its own: if Kannada is chosen and the device
// has no Kannada voice, speak() reports "no-voice" and the page says so
// politely. Voices installed on the device are preferred, because online
// voices do not work without internet.
//
// pickVoice is a plain function so it can be tested with Node: node --test tests/js

(function () {
  "use strict";

  const LANG_PREFIX = { kn: "kn", en: "en" };

  // Choose the best voice for "kn" or "en" from a list of SpeechSynthesisVoice.
  // Order: offline voice for India (kn-IN / en-IN), any offline voice, then online ones.
  function pickVoice(voices, lang) {
    const prefix = LANG_PREFIX[lang];
    const matching = voices.filter((v) => (v.lang || "").toLowerCase().replace("_", "-").startsWith(prefix));
    const rank = (v) => (v.localService ? 0 : 2) + ((v.lang || "").toUpperCase().endsWith("IN") ? 0 : 1);
    return matching.sort((a, b) => rank(a) - rank(b))[0] || null;
  }

  // Some browsers load their voice list a moment after the page; wait briefly.
  function voices() {
    const synth = window.speechSynthesis;
    const now = synth.getVoices();
    if (now.length) return Promise.resolve(now);
    return new Promise((resolve) => {
      const done = () => { synth.removeEventListener("voiceschanged", done); resolve(synth.getVoices()); };
      synth.addEventListener("voiceschanged", done);
      setTimeout(done, 1500);
    });
  }

  function supported() {
    return typeof window !== "undefined" && "speechSynthesis" in window && "SpeechSynthesisUtterance" in window;
  }

  function speaking() {
    return supported() && window.speechSynthesis.speaking;
  }

  function stop() {
    if (supported()) window.speechSynthesis.cancel();
  }

  // Resolves with "started", "unsupported" or "no-voice". onEnd runs when
  // speech finishes or is stopped.
  async function speak(text, lang, onEnd) {
    if (!supported()) return "unsupported";
    const voice = pickVoice(await voices(), lang);
    if (!voice) return "no-voice";
    stop();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = voice;
    utterance.lang = voice.lang;
    utterance.rate = 0.9;                       // a little slower: clearer outdoors
    utterance.onend = utterance.onerror = () => onEnd && onEnd();
    window.speechSynthesis.speak(utterance);
    return "started";
  }

  const api = { pickVoice, supported, speaking, speak, stop };
  if (typeof module !== "undefined" && module.exports) module.exports = api;   // Node tests
  if (typeof window !== "undefined") window.VoiceAlert = api;
})();
