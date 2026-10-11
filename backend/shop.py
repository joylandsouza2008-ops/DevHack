"""
Shop questions for "Ask AquaNexus": "can I buy products?", "which sensor do I
need?", "how do I use the test kit?", in English or Kannada.

The products come from frontend/shop-data.json, the SAME file the Shop page
shows, so the assistant and the Shop can never disagree on a product, a
feature or a price. Nothing is for sale yet and no payment is ever taken.

What this file does:
    PRODUCTS                 the Shop products (frontend/shop-data.json)
    classify(question)       is this a Shop question, and which kind?
                             ("buy", "recommend", "use", or None)
    recommend(...)           what to get, and why, from the farmer's own situation:
                             recent alerts, tonight's crash risk, and what they
                             say (number of ponds, budget)
    answer(...)              a ready answer in English and Kannada (no AI)
    content_lines(...)       the Shop facts the AI may use
    reply_is_honest(...)     an AI reply only uses Shop prices and makes no
                             "cheaper than" claims

Rules (also in the AI's instructions, backend/assistant.py):
    - Default advice: start with the free app and a test kit.
    - The Night-Watch sensor kit only for night oxygen problems or a High
      crash risk tonight. pH monitoring only if pH is often out of range.
    - Always say why, in one line. Several ponds: one sensor watches one pond.
    - End with "See the Shop tab" and the estimated prices.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

SHOP_FILE = Path(__file__).resolve().parent.parent / "frontend" / "shop-data.json"
PRODUCTS: dict[str, dict] = {p["id"]: p for p in json.loads(SHOP_FILE.read_text(encoding="utf-8"))["products"]}

NIGHT_HOURS = set(range(18, 24)) | set(range(0, 6))      # 18:00 to 06:00, as for tonight's weather
PH_OFTEN = 2                                             # pH out of range this many times = "often"

TEXT = {
    "en": {
        "not_for_sale": "Not for sale yet. No payment is taken.",
        "orders": "Orders open after our pilot with farmers. You can make a list in the Shop tab and copy it for your cooperative.",
        "start": "Start with the free app and a test kit.",
        "get": "Get the {name}, and keep using the free app and a test kit.",
        "for": "What it is for:", "where": "Where:", "how": "How:", "why": "Why:", "care": "Care:",
        "why_need": "Why you need it:",
        "see_shop": "See the Shop tab: {prices}.",
        "see_shop_how": "See the Shop tab for how to use each one.",
        "one_sensor": "One sensor watches one pond. For several ponds, each needs its own sensor.",
        "one_pond": "One sensor watches one pond.",
        "n_ponds": "For {n} ponds you need {n} sensors, one in each pond.",
        "several": "Each pond needs its own sensor.",
        "kit_all_ponds": "One test kit can check all your ponds, one sample at a time.",
        "crash_high": "tonight's oxygen crash risk is High",
        "night_low": "your pond had low oxygen at night {n} times recently",
        "night_low_1": "your pond had low oxygen at night recently",
        "ph_often": "pH went out of the safe range {n} times recently",
        "ph_tip": "Check pH every week with the test kit. The Full Pond kit also watches pH day and night.",
        "no_need": "there are no night oxygen problems and tonight's crash risk is not High, so a sensor is not needed yet",
        "budget": "The {name} is {price}, more than your budget of ₹{budget}. Start with the test kit and the free app.",
        "simulated": " (simulated data)",
        "and": "; ",
    },
    "kn": {
        "not_for_sale": "ಇನ್ನೂ ಮಾರಾಟಕ್ಕಿಲ್ಲ. ಯಾವುದೇ ಹಣ ಪಡೆಯುವುದಿಲ್ಲ.",
        "orders": "ರೈತರೊಂದಿಗಿನ ನಮ್ಮ ಪ್ರಾಯೋಗಿಕ ಯೋಜನೆಯ ನಂತರ ಆರ್ಡರ್‌ಗಳು ಆರಂಭವಾಗುತ್ತವೆ. ಅಂಗಡಿ ಟ್ಯಾಬ್‌ನಲ್ಲಿ ಪಟ್ಟಿ ಮಾಡಿ, ನಿಮ್ಮ ಸಹಕಾರ ಸಂಘಕ್ಕಾಗಿ ನಕಲಿಸಬಹುದು.",
        "start": "ಉಚಿತ ಆ್ಯಪ್ ಮತ್ತು ಟೆಸ್ಟ್ ಕಿಟ್‌ನಿಂದ ಪ್ರಾರಂಭಿಸಿ.",
        "get": "{name} ಪಡೆಯಿರಿ, ಜೊತೆಗೆ ಉಚಿತ ಆ್ಯಪ್ ಮತ್ತು ಟೆಸ್ಟ್ ಕಿಟ್ ಬಳಸುತ್ತಿರಿ.",
        "for": "ಇದು ಯಾವುದಕ್ಕೆ:", "where": "ಎಲ್ಲಿ:", "how": "ಹೇಗೆ:", "why": "ಏಕೆ:", "care": "ಆರೈಕೆ:",
        "why_need": "ಇದು ಏಕೆ ಬೇಕು:",
        "see_shop_how": "ಪ್ರತಿಯೊಂದನ್ನು ಹೇಗೆ ಬಳಸುವುದು ಎಂದು ಅಂಗಡಿ ಟ್ಯಾಬ್‌ನಲ್ಲಿ ನೋಡಿ.",
        "one_sensor": "ಒಂದು ಸೆನ್ಸರ್ ಒಂದೇ ಕೊಳವನ್ನು ಗಮನಿಸುತ್ತದೆ. ಹಲವು ಕೊಳಗಳಿದ್ದರೆ, ಪ್ರತಿಯೊಂದಕ್ಕೂ ಬೇರೆ ಸೆನ್ಸರ್ ಬೇಕು.",
        "see_shop": "ಅಂಗಡಿ ಟ್ಯಾಬ್ ನೋಡಿ: {prices}.",
        "one_pond": "ಒಂದು ಸೆನ್ಸರ್ ಒಂದೇ ಕೊಳವನ್ನು ಗಮನಿಸುತ್ತದೆ.",
        "n_ponds": "{n} ಕೊಳಗಳಿಗೆ {n} ಸೆನ್ಸರ್‌ಗಳು ಬೇಕು, ಪ್ರತಿ ಕೊಳಕ್ಕೆ ಒಂದು.",
        "several": "ಪ್ರತಿ ಕೊಳಕ್ಕೂ ಅದರದೇ ಸೆನ್ಸರ್ ಬೇಕು.",
        "kit_all_ponds": "ಒಂದೇ ಟೆಸ್ಟ್ ಕಿಟ್‌ನಿಂದ ಎಲ್ಲಾ ಕೊಳಗಳನ್ನು, ಒಂದೊಂದಾಗಿ ಪರೀಕ್ಷಿಸಬಹುದು.",
        "crash_high": "ಇಂದು ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯ ಹೆಚ್ಚು",
        "night_low": "ಇತ್ತೀಚೆಗೆ ನಿಮ್ಮ ಕೊಳದಲ್ಲಿ ರಾತ್ರಿ {n} ಬಾರಿ ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗಿತ್ತು",
        "night_low_1": "ಇತ್ತೀಚೆಗೆ ನಿಮ್ಮ ಕೊಳದಲ್ಲಿ ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗಿತ್ತು",
        "ph_often": "ಇತ್ತೀಚೆಗೆ pH {n} ಬಾರಿ ಸುರಕ್ಷಿತ ಮಟ್ಟ ಮೀರಿತ್ತು",
        "ph_tip": "ಪ್ರತಿ ವಾರ ಟೆಸ್ಟ್ ಕಿಟ್‌ನಿಂದ pH ಪರೀಕ್ಷಿಸಿ. ಫುಲ್ ಪಾಂಡ್ ಕಿಟ್ ಹಗಲು-ರಾತ್ರಿ pH ಅನ್ನೂ ಗಮನಿಸುತ್ತದೆ.",
        "no_need": "ರಾತ್ರಿಯ ಆಮ್ಲಜನಕ ಸಮಸ್ಯೆ ಇಲ್ಲ ಮತ್ತು ಇಂದು ರಾತ್ರಿ ಕುಸಿತದ ಅಪಾಯ ಹೆಚ್ಚಿಲ್ಲ, ಆದ್ದರಿಂದ ಈಗ ಸೆನ್ಸರ್ ಬೇಕಿಲ್ಲ",
        "budget": "{name} ಬೆಲೆ {price}, ಇದು ನಿಮ್ಮ ₹{budget} ಬಜೆಟ್‌ಗಿಂತ ಹೆಚ್ಚು. ಟೆಸ್ಟ್ ಕಿಟ್ ಮತ್ತು ಉಚಿತ ಆ್ಯಪ್‌ನಿಂದ ಪ್ರಾರಂಭಿಸಿ.",
        "simulated": " (ಅನುಕರಿಸಿದ ಡೇಟಾ)",
        "and": "; ",
    },
}
EST = {"en": "est.", "kn": "ಅಂದಾಜು"}


# ----------------------------------------------------------------- prices

def group_indian(n: int) -> str:
    """1200 -> "1,200", 123456 -> "1,23,456" (same as the Shop page)."""
    s = str(int(n))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    head = re.sub(r"(\d)(?=(\d{2})+$)", r"\1,", head)
    return f"{head},{tail}"


def price(rupees: int, lang: str, most: int | None = None) -> str:
    """"est. ₹23,000" / "ಅಂದಾಜು ₹23,000": every price says it is an estimate.
    With a higher `most`, a range: "est. ₹23,000–71,000"."""
    top = f"–{group_indian(most)}" if most and most > rupees else ""
    return f"{EST[lang]} ₹{group_indian(rupees)}{top}"


def product_price(p: dict, lang: str) -> str:
    """A product's price as the Shop page shows it, e.g. "est. ₹23,000–71,000 depending on probes"."""
    text = price(p["price"], lang, p.get("price_max"))
    return f"{text} {p['price_note'][lang]}" if p.get("price_max") and p.get("price_note") else text


def _prices(ids: list[str], lang: str) -> str:
    return ", ".join(f"{PRODUCTS[i]['name'][lang]} {product_price(PRODUCTS[i], lang)}" for i in ids)


# ----------------------------------------------------------------- reading the question

# Matched in lower case. Kannada is matched as written. Note: ಕೊಳ is "pond", ಕೊಳ್ಳ is "buy".
BUY_WORDS = ["buy", "purchase", "order", "for sale", "sell", "price", "cost", "shop",   # not "how much": dose questions
             "ಖರೀದಿ", "ಕೊಳ್ಳ", "ಕೊಂಡುಕೊ", "ಬೆಲೆ", "ಮಾರಾಟ", "ಆರ್ಡರ್", "ಅಂಗಡಿ"]
USE_PATTERN = re.compile(r"\bhow\b.*\b(use|using|install|set ?up|fit|mount|work|clean|care|look after)\b"
                         r"|\b(use|using|install|set ?up) (the|my|a|this)\b"
                         r"|ಹೇಗೆ\s*(ಬಳಸ|ಉಪಯೋಗ|ಅಳವಡಿಸ|ಜೋಡಿಸ)|ಬಳಸುವುದು\s*ಹೇಗೆ|ಬಳಸುವ\s*ವಿಧಾನ|ಬಳಕೆ")
RECOMMEND_PATTERN = re.compile(r"\b(which|what)\b.*\b(buy|get|need|sensor|kit|product|device)"
                               r"|\bshould i (buy|get)\b|\bdo i need\b|\bneed an?\b.*\b(sensor|kit)\b|\brecommend"
                               r"|ಯಾವ\s*(ಸೆನ್ಸರ್|ಕಿಟ್|ವಸ್ತು|ಉತ್ಪನ್ನ)|ಯಾವುದನ್ನು|ಏನು\s*ಖರೀದಿ|ಏನನ್ನು\s*ಖರೀದಿ"
                               r"|(ಸೆನ್ಸರ್|ಕಿಟ್)\S*\s*ಬೇಕ")
# Product names, most specific first. A plain "sensor" means the Night-Watch kit.
PRODUCT_WORDS = [
    ("test-kit", ["test kit", "test-kit", "testkit", "ಟೆಸ್ಟ್ ಕಿಟ್", "ಪರೀಕ್ಷಾ ಕಿಟ್"]),
    ("full-pond", ["full pond", "full-pond", "ಫುಲ್ ಪಾಂಡ್"]),
    ("do-cap", ["sensor cap", "do cap", "cap", "ಕ್ಯಾಪ್"]),
    ("solar-10w", ["solar", "panel", "charge board", "ಸೌರ", "ಸೋಲಾರ್"]),
    ("night-watch", ["night-watch", "night watch", "nightwatch", "sensor", "probe", "ನೈಟ್", "ಸೆನ್ಸರ್", "ಪ್ರೋಬ್"]),
]
NUMBER_WORDS = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                "ಎರಡು": 2, "ಮೂರು": 3, "ನಾಲ್ಕು": 4, "ಐದು": 5, "ಆರು": 6, "ಏಳು": 7, "ಎಂಟು": 8, "ಒಂಬತ್ತು": 9, "ಹತ್ತು": 10}
SEVERAL_WORDS = ["several", "many", "multiple", "a few", "more than one", "ಹಲವು", "ಅನೇಕ", "ಕೆಲವು"]
POND_WORD = r"(ponds|ಕೊಳಗಳ|ಕೊಳಗಳು|ಕೊಳಗಳಿ|ಕೊಳ)"
# Questions about the pond itself, not the Shop ("I have 3 ponds, is the oxygen safe?").
POND_STATUS_WORDS = ["safe", "oxygen", "ammonia", "temperature", "disease", "sick", "tonight", "weather", "now",
                     "ಸುರಕ್ಷಿತ", "ಆಮ್ಲಜನಕ", "ಅಮೋನಿಯಾ", "ತಾಪಮಾನ", "ರೋಗ", "ರಾತ್ರಿ", "ಹವಾಮಾನ", "ಈಗ"]


def _has(low: str, words: list[str]) -> bool:
    for w in words:
        if w.isascii():
            if re.search(rf"(?<![a-z]){re.escape(w)}(?![a-z])", low):
                return True
        elif w in low:
            return True
    return False


def product_in(question: str) -> str | None:
    """Which Shop product the question names, if any."""
    low = question.lower()
    for pid, words in PRODUCT_WORDS:
        if _has(low, words):
            return pid
    return None


def pond_count(question: str) -> int | None:
    """How many ponds the farmer says they have: a number, 0 for "several", None if not said."""
    low = question.lower()
    m = re.search(rf"(\d+)\s*{POND_WORD}", low)
    if m:
        return int(m.group(1))
    for word, n in NUMBER_WORDS.items():
        if re.search(rf"{word}\s*{POND_WORD}", low):
            return n
    if re.search(POND_WORD, low) and _has(low, SEVERAL_WORDS):
        return 0
    return None


def budget(question: str) -> int | None:
    """A budget in rupees, if the farmer gives one ("my budget is ₹5000", "5000 ರೂಪಾಯಿ")."""
    low = question.lower().replace(",", "")
    m = re.search(r"(?:₹|\brs\.?|\binr\b|rupees?|ರೂ\.?|ರೂಪಾಯಿ)\s*(\d{3,7})|(\d{3,7})\s*(?:₹|rs\b|rupees?|ರೂ|ರೂಪಾಯಿ)", low)
    if m:
        return int(m.group(1) or m.group(2))
    m = re.search(r"(?:budget|ಬಜೆಟ್)\D{0,12}(\d{3,7})", low)
    return int(m.group(1)) if m else None


def classify(question: str) -> str | None:
    """"use", "recommend", "buy", or None when the question is not about the Shop."""
    low = question.lower()
    product = product_in(question)
    if product and USE_PATTERN.search(low):
        return "use"
    if RECOMMEND_PATTERN.search(low):
        return "recommend"
    ponds = pond_count(question)
    if ponds is not None and ponds != 1 and not _has(low, POND_STATUS_WORDS):
        return "recommend"                       # "I have 3 ponds": what to get for them
    if _has(low, BUY_WORDS):
        return "buy"
    return None


# ----------------------------------------------------------------- the farmer's situation

def _hour(time: str | None) -> int | None:
    m = re.search(r"[T ](\d{2}):\d{2}", time or "")
    return int(m.group(1)) if m else None


def situation(evals: list[dict], weather: dict, alerts: list[dict] | None) -> dict:
    """Night oxygen problems, pH problems and tonight's risk, from the page's own data."""
    alerts = alerts or []
    night_low = [a for a in alerts if "dissolved_oxygen" in (a.get("causes") or []) and _hour(a.get("time")) in NIGHT_HOURS]
    ph_alerts = [a for a in alerts if "ph" in (a.get("causes") or [])]
    ph_now = [e for e in evals if any(p["parameter"] == "ph" and p["level"] != "safe"
                                      for p in e["risk"].get("parameters", []))]
    # A pH reading showing now is usually also in the alert history: count it once.
    ph_count = max(len(ph_alerts), len(ph_now))
    crash_high = weather.get("status") == "ok" and weather.get("level") == "high"
    return {
        "night_low": len(night_low),
        "night_low_simulated": any(a.get("source") == "simulated" for a in night_low),
        "ph_count": ph_count,
        "ph_simulated": any(a.get("source") == "simulated" for a in ph_alerts) or any(e["source"] == "simulated" for e in ph_now),
        "crash_high": crash_high,
    }


def recommend(evals: list[dict], weather: dict, alerts: list[dict] | None, question: str = "") -> dict:
    """
    What to get and why, from the farmer's situation:
        {"product": id, "also": [ids to price], "reasons": {en, kn}, "ponds", "budget", "situation"}
    """
    s = situation(evals, weather, alerts)
    night_problem = s["crash_high"] or s["night_low"] > 0
    ph_often = s["ph_count"] >= PH_OFTEN

    def reasons(lang: str) -> str:
        t = TEXT[lang]
        out = []
        if s["crash_high"]:
            out.append(t["crash_high"])
        if s["night_low"]:
            line = t["night_low"].format(n=s["night_low"]) if s["night_low"] > 1 else t["night_low_1"]
            out.append(line + (t["simulated"] if s["night_low_simulated"] else ""))
        if ph_often:
            out.append(t["ph_often"].format(n=s["ph_count"]) + (t["simulated"] if s["ph_simulated"] else ""))
        if not night_problem and not ph_often:
            out.append(t["no_need"])
        return t["and"].join(out)

    if night_problem:
        product = "full-pond" if ph_often else "night-watch"
        also = [product, "test-kit"]
    else:
        product = "test-kit"
        also = ["test-kit", "full-pond"] if ph_often else ["test-kit", "night-watch"]
    return {"product": product, "also": also, "reasons": {lg: reasons(lg) for lg in ("en", "kn")},
            "ph_tip": ph_often and not night_problem, "ponds": pond_count(question), "budget": budget(question),
            "situation": s}


# ----------------------------------------------------------------- ready answers (no AI)

def _sentence(text: str) -> str:
    text = text.strip()
    return text if text.endswith((".", "?", "!")) else text + "."


def _steps(product: dict, lang: str) -> str:
    return " ".join(f"{i}. {step[lang]}" for i, step in enumerate(product["steps"], 1))


def _ponds_lines(rec: dict, lang: str) -> list[str]:
    t, n = TEXT[lang], rec["ponds"]
    if n is None or n == 1:
        return []
    lines = [t["one_pond"], t["n_ponds"].format(n=n) if n > 1 else t["several"]]
    if rec["product"] == "test-kit":
        lines.append(t["kit_all_ponds"])
    return lines


def _recommendation(rec: dict, lang: str) -> list[str]:
    """Head, what it is for, where, how and why (one line) for the recommended product."""
    t = TEXT[lang]
    p = PRODUCTS[rec["product"]]
    head = t["start"] if rec["product"] == "test-kit" else t["get"].format(name=p["name"][lang])
    lines = [head, f"{p['name'][lang]}: {p['desc'][lang]}", f"{t['for']} {p['solves'][lang]}",
             f"{t['where']} {p['where'][lang]}", f"{t['how']} {_steps(p, lang)}",
             f"{t['why']} {_sentence(rec['reasons'][lang])}"]
    if rec["ph_tip"]:
        lines.append(t["ph_tip"])
    if rec["budget"] and p["price"] > rec["budget"] and rec["product"] != "test-kit":
        lines.append(t["budget"].format(name=p["name"][lang], price=product_price(p, lang), budget=group_indian(rec["budget"])))
    return lines + _ponds_lines(rec, lang)


def _ending(ids: list[str], lang: str) -> list[str]:
    t = TEXT[lang]
    return [t["not_for_sale"], t["see_shop"].format(prices=_prices(ids, lang))]


def answer(kind: str, question: str, evals: list[dict], weather: dict, alerts: list[dict] | None) -> dict:
    """A ready Shop answer in both languages: {"en": ..., "kn": ...}."""
    rec = recommend(evals, weather, alerts, question)
    out = {}
    for lang in ("en", "kn"):
        t = TEXT[lang]
        if kind == "use":
            p = PRODUCTS[product_in(question) or "test-kit"]
            lines = [f"{p['name'][lang]}: {p['desc'][lang]}", f"{t['for']} {p['solves'][lang]}",
                     f"{t['where']} {p['where'][lang]}", f"{t['how']} {_steps(p, lang)}",
                     f"{t['care']} {' '.join(c[lang] for c in p['care'])}",
                     f"{t['why_need']} {p['why'][lang]}"]
            ids = [p["id"]]
        elif kind == "buy":
            # "Can I buy?", kept short (about 500 characters): what to start with and
            # why, one sensor per pond, one line per product, then "not for sale yet".
            # The chat keeps line breaks, so each product gets its own line.
            p = PRODUCTS[rec["product"]]
            head = t["start"] if rec["product"] == "test-kit" else t["get"].format(name=p["name"][lang])
            ponds = [t["n_ponds"].format(n=rec["ponds"])] if rec["ponds"] and rec["ponds"] > 1 else []
            lines = [f"{head} {t['why']} {_sentence(rec['reasons'][lang])}", " ".join([t["one_sensor"]] + ponds)]
            lines += [f"- {q['name'][lang]} ({product_price(q, lang)}): {q['short'][lang]}" for q in PRODUCTS.values()]
            lines.append(f"{t['not_for_sale']} {t['see_shop_how']}")
            out[lang] = "\n".join(lines)
            continue
        else:                                    # "recommend"
            lines = _recommendation(rec, lang)
            ids = rec["also"]
        out[lang] = " ".join(lines + _ending(ids, lang))
    return out


# ----------------------------------------------------------------- for the AI

def content_lines(lang: str, evals: list[dict], weather: dict, alerts: list[dict] | None, question: str) -> list[str]:
    """The Shop facts and this farmer's recommendation, as plain text for the AI's content."""
    langs = ["en", "kn"] if lang == "kn" else ["en"]
    out = ["\n## Shop (frontend/shop-data.json). The ONLY products and prices that exist. "
           "Prices are estimates: always write them as 'est. ₹X' (or 'est. ₹X–Y' with its note for a range). "
           "Not for sale yet. No payment is taken."]
    for p in PRODUCTS.values():
        for lg in langs:
            out.append(f"- {p['name'][lg]} ({product_price(p, lg)}): {p['desc'][lg]} Measures: {p['measures'][lg]}. "
                       f"For: {p['solves'][lg]} Where: {p['where'][lg]} How: {_steps(p, lg)} "
                       f"Care: {' '.join(c[lg] for c in p['care'])} Why you need it: {p['why'][lg]}")
    rec = recommend(evals, weather, alerts, question)
    out.append("\n## Shop recommendation for this farmer (worked out by the app from their own readings, "
               "alerts, tonight's risk and what they said). Use it for 'what should I buy' questions.")
    for lg in langs:
        out.append(f"- ({lg}) " + " ".join(_recommendation(rec, lg) + _ending(rec["also"], lg)))
    return out


CHEAPER = re.compile(r"cheap(er|est)|lowest price|best price|less than other|than other (brands|products)|ಅಗ್ಗ|ಕಡಿಮೆ ಬೆಲೆ", re.I)


def allowed_amounts(question: str) -> set[int]:
    """Rupee amounts an answer may mention: Shop prices, a few of them together, and the farmer's own budget."""
    prices = [p["price"] for p in PRODUCTS.values()] + [p["price_max"] for p in PRODUCTS.values() if p.get("price_max")]
    amounts = {p * n for p in prices for n in range(1, 11)}
    amounts |= {a + b for a in prices for b in prices}
    if budget(question):
        amounts.add(budget(question))
    return amounts


def reply_is_honest(text: str, question: str) -> bool:
    """False if an AI reply names a price that is not from the Shop, or claims to be cheaper than others."""
    if CHEAPER.search(text):
        return False
    allowed = allowed_amounts(question)
    for m in re.finditer(r"(?:₹|\brs\.?|\brupees?)\s*(\d[\d,]*)", text, re.I):
        if int(m.group(1).replace(",", "") or 0) not in allowed:
            return False
    return True
