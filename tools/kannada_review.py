"""
Writes docs/kannada-review.md: every Kannada string in the app next to its
English version, grouped by screen, for a native speaker to review.

The strings are read straight from the code (backend/*.py dictionaries and the
TEXT table in frontend/app.js), so re-run this after changing any text:

    python tools/kannada_review.py

Needs Node.js (it reads frontend/app.js with node).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUT = ROOT / "docs" / "kannada-review.md"
KANNADA = re.compile("[\u0C80-\u0CFF]")

# Screen headings for the frontend TEXT keys (first matching prefix wins).
FRONTEND_SCREENS = [
    ("Welcome screen", ["appName", "welcomeTagline", "welcomeExample", "start", "builtBy"]),
    ("Top bar and demo controls", ["tagline", "theme", "simulated", "pond", "scenario", "restart", "pause",
                                   "resume", "simTime", "connecting", "ended", "connectionLost"]),
    ("Pond view, risk level and readings", ["pondViewTitle", "pondCaption", "gaugeTitle", "readingsTitle",
                                            "infoOnly"]),
    ("Time until danger and oxygen chart", ["ttdTitle", "countdownLabel", "duration", "around", "chart"]),
    ("Pond health score", ["health"]),
    ("Tonight's weather", ["weather", "crashRisk"]),
    ("What to do now (checklist)", ["actions"]),
    ("Alert preview (SMS / WhatsApp)", ["alert", "previewNote"]),
    ("Test-kit readings", ["kit"]),
    ("Live sensor", ["live"]),
    ("Fish disease guide (page labels)", ["guide", "checker", "library", "noPhoto", "likely"]),
    ("Ask MeenuRaksha assistant (page labels)", ["assistant"]),
    ("Voice alert", ["voice"]),
    ("Alert history", ["history"]),
    ("Data sources panel (footer)", ["sources"]),
    ("Terms & Privacy panel (footer)", ["terms"]),
    ("Footer (privacy, source code)", ["footer"]),
]


def frontend_text() -> dict:
    """{"en": {key: text}, "kn": {...}} from the TEXT table in frontend/app.js."""
    script = r"""
const src = require("fs").readFileSync(process.argv[1], "utf8");
const start = src.indexOf("const TEXT = {");
const end = src.indexOf("\n};", start) + 3;
const TEXT = eval("(" + src.slice(start + "const TEXT = ".length, end - 1) + ")");
const flat = (obj, prefix = "") => Object.entries(obj).flatMap(([k, v]) => {
  const key = prefix ? `${prefix}.${k}` : k;
  if (typeof v === "function") {
    // Show the text the function builds, with ${...} where the app fills in a value.
    const body = v.toString().split("=>").slice(1).join("=>").trim();
    const parts = body.match(/`[^`]*`|"[^"]*"/g) || [body];
    const text = parts.map((p) => p.slice(1, -1)).join("  /  ")
      .replace(/\$\{String\((\w+)\)\.padStart\([^)]*\)\}/g, "{$1}")   // ${String(m).padStart(2, "0")} -> {m}
      .replace(/\$\{(\w+)\}/g, "{$1}");                                // ${now} -> {now}, like the server text
    return [[key, text]];
  }
  if (typeof v === "object") return flat(v, key);
  return [[key, v]];
});
console.log(JSON.stringify({ en: Object.fromEntries(flat(TEXT.en)), kn: Object.fromEntries(flat(TEXT.kn)) }));
"""
    out = subprocess.run(["node", "-e", script, str(ROOT / "frontend" / "app.js")],
                         capture_output=True, check=True, encoding="utf-8")
    return json.loads(out.stdout)


def pairs_in(obj, path=""):
    """Every {"en": ..., "kn": ...} pair inside a (nested) dictionary, as (path, en, kn)."""
    if isinstance(obj, dict):
        if isinstance(obj.get("en"), str) and isinstance(obj.get("kn"), str):
            yield path, obj["en"], obj["kn"]
            return
        for key, value in obj.items():
            name = "/".join(map(str, key)) if isinstance(key, tuple) else str(key)
            yield from pairs_in(value, f"{path}.{name}" if path else name)
    elif isinstance(obj, (list, tuple)):
        for i, value in enumerate(obj):
            yield from pairs_in(value, f"{path}[{i}]")


def backend_groups() -> list[tuple[str, str, list]]:
    """(heading, note, rows) for the text the API sends to the page."""
    from backend import actions, alerts, assistant, diseases, main, risk_messages, sensor, simulator, weather

    def rows(module, *names):
        return [(f"{module.__name__.split('.')[-1]}.{p}", en, kn)
                for name in names for p, en, kn in pairs_in(getattr(module, name), name)]

    msg_names = [n for n in vars(risk_messages) if n.isupper() and n != "TIME_TO_DANGER"]
    return [
        ("Data labels", "Shown on every simulated, test-kit or live-sensor reading.",
         rows(simulator, "SIMULATED_LABEL") + rows(main, "MANUAL_LABEL")
         + rows(sensor, "LIVE_LABEL", "DEMO_LABEL")),
        ("Live sensor: why a reading was refused", "Sent back to the sensor and shown on the Live sensor card.",
         rows(sensor, "REJECTED", "NO_VALUES", "WRONG_KEY", "CLOCK_AHEAD", "NO_TIME_ZONE", "TOO_OLD")),
        ("Risk card: level names, parameter names and reasons",
         "`{value}` and `{unit}` are filled in by the app, e.g. 4.1 mg/L. `{name}` is a parameter name.",
         rows(risk_messages, *msg_names)),
        ("Time until danger (messages)",
         "`{rate}` e.g. 0.6, `{danger}` e.g. 3, `{clock}` e.g. 03:20, `{hours}` e.g. 6. "
         "`{duration_kn}` is one of the two duration phrases below.",
         rows(risk_messages, "TIME_TO_DANGER") + [
             ("time_to_danger._duration (under 1 hour)", "about {minutes} minutes", "ಸುಮಾರು {minutes} ನಿಮಿಷಗಳಲ್ಲಿ"),
             ("time_to_danger._duration (1 hour or more)", "about {text} hours", "ಸುಮಾರು {text} ಗಂಟೆಗಳಲ್ಲಿ"),
         ]),
        ("Tonight's weather (messages)",
         "`{night}` is one or more of the night words joined together, e.g. \"cloudy, still\".",
         rows(weather, "MANGALURU", "LEVEL_NAMES", "FACTOR_WORDS", "ADVICE", "UNAVAILABLE")),
        ("What to do now (checklist items)", "", rows(actions, "ACTIONS")),
        ("Fish disease guide: diseases", "Disease names, signs, seasons, prevention and what to do. "
         "Scientific names (e.g. Aphanomyces invadans) stay in Latin.",
         rows(diseases, "DISEASES")),
        ("Fish disease guide: symptom checker and notes", "The signs a farmer can tick, cause types, the steps "
         "for any disease, and the notes shown with every result.",
         rows(diseases, "SIGNS", "CAUSE_TYPES", "COMMON_STEPS", "TREATMENT_NOTE", "NOT_A_DIAGNOSIS", "NO_MATCH",
              "GASPING_NOTE", "LIKELY_NOTE")),
        ("Fish disease guide: risky readings", "Why a reading makes a disease more likely.",
         rows(diseases, "READING_LINKS")),
        ("Ask MeenuRaksha assistant", "Labels, safety replies and the suggested questions. Ready answers are "
         "built from the texts in the other sections. AI replies in Kannada are written by the AI and are not in "
         "this sheet.",
         rows(assistant, "LABEL", "I_DONT_KNOW", "CONFIRM", "NO_TREATMENT", "OFFLINE_NOTE", "LIMITED_NOTE",
              "SIMULATED_NOTE", "QUESTIONS", "NO_READINGS", "ALL_SAFE_ACTION", "NO_LIKELY", "USE_CHECKER",
              "LEVELS_INTRO", "AMMONIA_NOTE") + [
             *[(f"assistant.BAND.{key}", en, kn) for key, en, kn in
               ((k, assistant.BAND["en"][k].strip(), assistant.BAND["kn"][k].strip()) for k in assistant.BAND["en"])
               if KANNADA.search(kn)],
             ("assistant._answer (tonight)", "Oxygen crash risk tonight: {level}.", "ಇಂದು ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯ: {level}."),
         ]),
        ("Alert preview (SMS / WhatsApp)", "The SMS and WhatsApp text is built from the risk card "
         "and time-until-danger messages above, plus these.",
         rows(alerts, "POND_NAMES", "APP_NAME", "NO_ALERT")),
    ]


def cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", "<br>")


def table(rows) -> list[str]:
    lines = ["| # | Where in the code | English | Kannada | Correct? / suggestion |", "|---|---|---|---|---|"]
    lines += [f"| {i} | `{where}` | {cell(en)} | {cell(kn)} |  |" for i, (where, en, kn) in enumerate(rows, 1)]
    return lines


def main() -> None:
    text = frontend_text()
    keys = [k for k in text["kn"] if KANNADA.search(text["kn"][k])]
    used = set()
    sections = []
    for heading, prefixes in FRONTEND_SCREENS:
        rows = []
        for key in keys:
            if key not in used and any(key.startswith(p) for p in prefixes):
                used.add(key)
                rows.append((f"app.js {key}", text["en"][key], text["kn"][key]))
        sections.append((heading, "", rows))
    left = [k for k in keys if k not in used]
    if left:
        sections.append(("Other page labels", "", [(f"app.js {k}", text["en"][k], text["kn"][k]) for k in left]))

    sections.insert(1, ("Pond scene (sky label)", "Shown over the day/night pond picture.", [
        ("scene.js PHASE_WORDS." + k, en, kn) for k, en, kn in
        [("night", "Night", "ರಾತ್ರಿ"), ("dawn", "Sunrise", "ಸೂರ್ಯೋದಯ"),
         ("day", "Daytime", "ಹಗಲು"), ("dusk", "Sunset", "ಸೂರ್ಯಾಸ್ತ")]]))
    sections.insert(0, ("Language and theme switches", "Button and screen-reader labels in index.html.", [
        ("index.html language button", "English", "ಕನ್ನಡ"),
        ("index.html aria-label", "Language", "ಭಾಷೆ"),
        ("index.html aria-label", "Theme", "ಬಣ್ಣ"),
    ]))
    sections += [(f"Messages from the server: {h}", note, rows) for h, note, rows in backend_groups()]

    total = sum(len(rows) for _, _, rows in sections)
    out = [
        "# Kannada text review",
        "",
        "Every Kannada string in MeenuRaksha, next to its English version, grouped by screen.",
        "Please check each Kannada line is correct, natural and easy for a small fish farmer in",
        "coastal Karnataka to understand. Write any fix in the last column.",
        "",
        "- Words in `{curly brackets}` are filled in by the app (numbers, times, names). Please keep them.",
        "- `A  /  B` means the app shows one of two versions, depending on the situation.",
        "- Unit symbols (mg/L, °C, km/h, pH) and the names SMS, WhatsApp, FAO, TNAU, Open-Meteo stay in English.",
        "",
        f"{total} strings. Generated from the code by `python tools/kannada_review.py`; "
        "re-run it after changing any text.",
        "",
    ]
    number = 0
    for heading, note, rows in sections:
        if not rows:
            continue
        number += 1
        out += [f"## {number}. {heading}", ""]
        if note:
            out += [note, ""]
        out += table(rows) + [""]
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({total} strings)")


if __name__ == "__main__":
    main()
