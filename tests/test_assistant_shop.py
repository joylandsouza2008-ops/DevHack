"""
Shop questions in "Ask AquaNexus" (backend/shop.py, backend/assistant.py):
"can I buy products?", "which sensor should I buy?", "how do I use the test
kit?", "I have 3 ponds", in English and Kannada.

Checks that every answer says what the product is for, where to use it, how,
and why it is recommended; that advice follows the farmer's own situation
(default: the free app and a test kit; the Night-Watch kit only for night
oxygen problems or a High crash risk; pH only when pH is often out of range);
and that answers stay honest and safe (Shop prices only, "Not for sale yet",
no "cheaper" claims, no chemicals or doses).

The AI is ALWAYS faked here: no test ever calls a real AI service.

Run from the project folder with:   python -m pytest tests/test_assistant_shop.py -v
"""

import json
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import backend.main as main
from backend import assistant as A
from backend import safety, shop
from backend.ai_provider import ProviderError

client = TestClient(main.app)
KANNADA = re.compile("[ಀ-೿]")
SHOP_JSON = json.loads((Path(__file__).resolve().parent.parent / "frontend" / "shop-data.json").read_text(encoding="utf-8"))

CALM = {"status": "ok", "level": "low", "level_name": {"en": "Low", "kn": "ಕಡಿಮೆ"},
        "message": {"en": "Low risk tonight.", "kn": "ಇಂದು ರಾತ್ರಿ ಅಪಾಯ ಕಡಿಮೆ."}}
HIGH = {"status": "ok", "level": "high", "level_name": {"en": "High", "kn": "ಹೆಚ್ಚು"},
        "message": {"en": "High risk tonight: keep the aerator ready.", "kn": "ಇಂದು ರಾತ್ರಿ ಹೆಚ್ಚು ಅಪಾಯ."}}
SAFE_POND = {"station": "station1", "simulated": {"dissolved_oxygen": 6.5, "ph": 7.4, "temperature": 29}}
NIGHT_LOW_O2 = [{"source": "simulated", "level": "danger", "causes": ["dissolved_oxygen"], "time": "2026-10-10T04:30:00+05:30"},
                {"source": "simulated", "level": "warning", "causes": ["dissolved_oxygen"], "time": "2026-10-09T23:10:00+05:30"}]
DAY_LOW_O2 = [{"source": "manual", "level": "warning", "causes": ["dissolved_oxygen"], "time": "2026-10-10T14:00:00+05:30"}]
PH_OFTEN = [{"source": "manual", "level": "warning", "causes": ["ph"], "time": "2026-10-08T07:00:00+05:30"},
            {"source": "manual", "level": "warning", "causes": ["ph"], "time": "2026-10-09T07:00:00+05:30"}]

# What a recommendation must contain: what it is for, where, how and why.
PARTS = {"en": ["What it is for:", "Where:", "How:", "Why:"], "kn": ["ಇದು ಯಾವುದಕ್ಕೆ:", "ಎಲ್ಲಿ:", "ಹೇಗೆ:", "ಏಕೆ:"]}
NOT_FOR_SALE = {"en": "Not for sale yet. No payment is taken.", "kn": "ಇನ್ನೂ ಮಾರಾಟಕ್ಕಿಲ್ಲ. ಯಾವುದೇ ಹಣ ಪಡೆಯುವುದಿಲ್ಲ."}
SEE_SHOP = {"en": "See the Shop tab:", "kn": "ಅಂಗಡಿ ಟ್ಯಾಬ್ ನೋಡಿ:"}
START = {"en": "Start with the free app and a test kit.", "kn": "ಉಚಿತ ಆ್ಯಪ್ ಮತ್ತು ಟೆಸ್ಟ್ ಕಿಟ್‌ನಿಂದ ಪ್ರಾರಂಭಿಸಿ."}
ONE_POND = {"en": "One sensor watches one pond.", "kn": "ಒಂದು ಸೆನ್ಸರ್ ಒಂದೇ ಕೊಳವನ್ನು ಗಮನಿಸುತ್ತದೆ."}

QUESTIONS = {
    "buy": {"en": "Can I buy products?", "kn": "ನಾನು ಉತ್ಪನ್ನಗಳನ್ನು ಖರೀದಿಸಬಹುದೇ?"},
    "which": {"en": "Which sensor should I buy?", "kn": "ನಾನು ಯಾವ ಸೆನ್ಸರ್ ಖರೀದಿಸಬೇಕು?"},
    "test_kit": {"en": "How do I use the test kit?", "kn": "ಟೆಸ್ಟ್ ಕಿಟ್ ಅನ್ನು ಹೇಗೆ ಬಳಸುವುದು?"},
    "ponds": {"en": "I have 3 ponds", "kn": "ನನಗೆ 3 ಕೊಳಗಳಿವೆ"},
}


class FakeAI:
    def __init__(self, reply="", error=False):
        self.reply, self.error, self.calls = reply, error, []

    def complete(self, system, messages):
        self.calls.append({"system": system, "messages": messages})
        if self.error:
            raise ProviderError("Gemini unreachable")
        return self.reply


@pytest.fixture
def no_ai(monkeypatch):
    monkeypatch.setattr(main, "provider_from_env", lambda: None)
    monkeypatch.setattr(main, "tonight_crash_risk", lambda: CALM)


def with_ai(monkeypatch, reply="", error=False, weather=CALM):
    fake = FakeAI(reply, error)
    monkeypatch.setattr(main, "provider_from_env", lambda: fake)
    monkeypatch.setattr(main, "tonight_crash_risk", lambda: weather)
    monkeypatch.setattr(main, "assistant_limiter", A.RateLimiter(per_minute=100, per_hour=100, per_day_total=100))
    return fake


def ask(question, lang="en", alerts=(), page=SAFE_POND):
    r = client.post("/api/assistant/ask", json={**page, "question": question, "lang": lang, "recent_alerts": list(alerts)})
    assert r.status_code == 200, r.text
    return r.json()


def evals(page=SAFE_POND):
    return A.evaluate({k: v for k, v in page.items() if k != "station"}, page["station"], main.assess)


def honest_and_safe(text: str, question: str = ""):
    assert not safety.find_banned(text), safety.find_banned(text)        # no chemicals or doses, ever
    assert not safety.looks_like_diagnosis(text)
    assert not shop.CHEAPER.search(text), "no 'cheaper than other brands' claims"
    assert shop.reply_is_honest(text, question), "only Shop prices (and the farmer's own budget)"
    for m in re.finditer(r"₹([\d,]+)", text):                           # every price is an estimate
        assert re.search(rf"(est\.|ಅಂದಾಜು) ₹{m.group(1)}", text) or "budget" in text or "ಬಜೆಟ್" in text, m.group(0)


# ----------------------------------------------------------------- one source of product data

def test_assistant_uses_the_same_products_as_the_shop_page():
    assert list(shop.PRODUCTS) == [p["id"] for p in SHOP_JSON["products"]]
    assert {p["id"]: p["price"] for p in SHOP_JSON["products"]} == {i: p["price"] for i, p in shop.PRODUCTS.items()}
    assert shop.SHOP_FILE.name == "shop-data.json" and shop.SHOP_FILE.parent.name == "frontend"


def test_every_product_has_checked_content_for_the_assistant():
    for p in shop.PRODUCTS.values():
        for field in ("name", "desc", "measures", "solves", "where", "why"):
            assert p[field]["en"] and KANNADA.search(p[field]["kn"]), (p["id"], field)
        assert 3 <= len(p["steps"]) <= 5, p["id"]
        assert p["care"], p["id"]
        for line in p["steps"] + p["care"]:
            assert line["en"] and KANNADA.search(line["kn"]), p["id"]
            honest_and_safe(line["en"])
            honest_and_safe(line["kn"])


def test_product_facts_from_the_brief():
    kit, nw, full = shop.PRODUCTS["test-kit"], shop.PRODUCTS["night-watch"], shop.PRODUCTS["full-pond"]
    assert "30 cm" in kit["where"]["en"] and "early in the morning" in kit["where"]["en"]
    assert "AquaNexus" in kit["steps"][-1]["en"]                         # type the numbers into the app
    assert "near the pond bottom" in nw["where"]["en"] and "away from the aerator" in nw["where"]["en"]
    assert "pole" in nw["where"]["en"] and "shade" in nw["where"]["en"]
    assert "every 5 minutes at night" in nw["steps"][-1]["en"]
    assert "night oxygen crash" in nw["solves"]["en"]
    care = " ".join(c["en"] for c in full["care"])
    assert "Rinse the probe" in care and "DO sensor cap" in care and "pH probe every month" in care


# ----------------------------------------------------------------- the four questions, English and Kannada

@pytest.mark.parametrize("lang", ["en", "kn"])
def test_can_i_buy_products(no_ai, lang):
    body = ask(QUESTIONS["buy"][lang], lang)
    assert body["mode"] == "ready" and body["texts"]["en"] and KANNADA.search(body["texts"]["kn"])
    text = body["text"]
    assert text == body["texts"][lang]
    assert NOT_FOR_SALE[lang] in text and SEE_SHOP[lang] in text and START[lang] in text
    assert PARTS[lang][0] in text and PARTS[lang][3] in text              # what it is for, and why
    for p in shop.PRODUCTS.values():                                     # every product and its estimated price
        assert f"{p['name'][lang]} {shop.product_price(p, lang)}" in text
        for field in ("solves", "where"):                                # what it is for, and where
            assert p[field][lang] in text, (p["id"], field)
        assert shop._steps(p, lang) in text, p["id"]                     # how to use it
    assert shop.TEXT[lang]["recommend"] in text                          # and a recommendation
    honest_and_safe(text)


def test_full_pond_kit_price_is_a_range_in_both_languages():
    full = shop.PRODUCTS["full-pond"]
    assert shop.product_price(full, "en") == "est. ₹23,000–71,000 depending on probes"
    assert shop.product_price(full, "kn") == "ಅಂದಾಜು ₹23,000–71,000 ಪ್ರೋಬ್‌ಗಳನ್ನು ಅವಲಂಬಿಸಿ"
    assert shop.reply_is_honest("The Full Pond kit is est. ₹23,000–₹71,000.", "")
    assert not shop.reply_is_honest("The Full Pond kit is est. ₹35,000.", "")


@pytest.mark.parametrize("lang", ["en", "kn"])
def test_which_sensor_should_i_buy_defaults_to_the_free_app_and_a_test_kit(no_ai, lang):
    text = ask(QUESTIONS["which"][lang], lang)["text"]
    assert text.startswith(START[lang])
    for part in PARTS[lang]:
        assert part in text, part
    kit = shop.PRODUCTS["test-kit"]
    assert kit["solves"][lang] in text and kit["where"][lang] in text and kit["steps"][0][lang] in text
    assert shop.TEXT[lang]["no_need"] in text                            # why: no night oxygen problems
    assert NOT_FOR_SALE[lang] in text and SEE_SHOP[lang] in text and shop.price(1200, lang) in text
    honest_and_safe(text)


@pytest.mark.parametrize("lang", ["en", "kn"])
def test_how_do_i_use_the_test_kit(no_ai, lang):
    text = ask(QUESTIONS["test_kit"][lang], lang)["text"]
    kit = shop.PRODUCTS["test-kit"]
    assert kit["solves"][lang] in text                                   # what it is for
    assert kit["where"][lang] in text                                    # where (30 cm deep, early morning)
    for i, step in enumerate(kit["steps"], 1):                           # how, in steps
        assert f"{i}. {step[lang]}" in text
    assert kit["care"][0][lang] in text                                  # care
    assert shop.TEXT[lang]["why_need"] in text and kit["why"][lang] in text   # why you need it
    assert NOT_FOR_SALE[lang] in text and shop.price(1200, lang) in text
    honest_and_safe(text)


@pytest.mark.parametrize("lang", ["en", "kn"])
def test_i_have_3_ponds(no_ai, lang):
    text = ask(QUESTIONS["ponds"][lang], lang)["text"]
    assert ONE_POND[lang] in text
    assert shop.TEXT[lang]["n_ponds"].format(n=3) in text
    assert shop.TEXT[lang]["kit_all_ponds"] in text                     # default advice: one kit checks them all
    for part in PARTS[lang]:
        assert part in text, part
    honest_and_safe(text)


@pytest.mark.parametrize("lang", ["en", "kn"])
def test_several_ponds_without_a_number(no_ai, lang):
    q = {"en": "Which sensor do I need for my many ponds?", "kn": "ನನ್ನ ಹಲವು ಕೊಳಗಳಿಗೆ ಯಾವ ಸೆನ್ಸರ್ ಬೇಕು?"}[lang]
    text = ask(q, lang)["text"]
    assert ONE_POND[lang] in text and shop.TEXT[lang]["several"] in text


# ----------------------------------------------------------------- advice follows the farmer's situation

@pytest.mark.parametrize("lang", ["en", "kn"])
def test_high_crash_risk_recommends_the_night_watch_kit(monkeypatch, lang):
    monkeypatch.setattr(main, "provider_from_env", lambda: None)
    monkeypatch.setattr(main, "tonight_crash_risk", lambda: HIGH)
    text = ask(QUESTIONS["which"][lang], lang)["text"]
    nw = shop.PRODUCTS["night-watch"]
    assert text.startswith(shop.TEXT[lang]["get"].format(name=nw["name"][lang]))
    assert nw["solves"][lang] in text                                    # what for: night oxygen crash
    assert nw["where"][lang] in text                                     # where: near the bottom, away from the aerator
    assert nw["steps"][-1][lang] in text                                 # how: readings every 5 minutes at night
    assert f"{PARTS[lang][3]} {shop.TEXT[lang]['crash_high']}" in text   # why, in one line
    assert shop.price(23000, lang) in text and SEE_SHOP[lang] in text and NOT_FOR_SALE[lang] in text
    honest_and_safe(text)


def test_night_oxygen_alerts_recommend_the_night_watch_kit_and_say_simulated(no_ai):
    text = ask("Which sensor should I buy?", alerts=NIGHT_LOW_O2)["text"]
    assert text.startswith("Get the Night-Watch kit")
    assert "your pond had low oxygen at night 2 times recently (simulated data)" in text


def test_daytime_low_oxygen_alone_does_not_push_a_sensor(no_ai):
    text = ask("Which sensor should I buy?", alerts=DAY_LOW_O2)["text"]
    assert text.startswith(START["en"]) and "Get the Night-Watch kit" not in text


def test_ph_often_out_of_range_adds_ph_monitoring():
    # Night problems + pH often out: the Full Pond kit (Night-Watch + pH).
    rec = shop.recommend(evals(), HIGH, PH_OFTEN)
    assert rec["product"] == "full-pond" and "pH went out of the safe range 2 times recently" in rec["reasons"]["en"]
    # pH often out, no night problems: the test kit, with a pH tip.
    text = shop.answer("recommend", "which sensor?", evals(), CALM, PH_OFTEN)["en"]
    assert text.startswith(START["en"]) and shop.TEXT["en"]["ph_tip"] in text and shop.product_price(shop.PRODUCTS["full-pond"], "en") in text
    # pH out just once: not "often", so no pH monitoring.
    once = shop.recommend(evals(), HIGH, PH_OFTEN[:1])
    assert once["product"] == "night-watch"


def test_a_ph_reading_out_of_range_now_counts():
    page = {"station": "station1", "simulated": {"dissolved_oxygen": 6.5, "ph": 9.6, "temperature": 29}}
    s = shop.situation(evals(page), CALM, PH_OFTEN[:1])
    assert s["ph_count"] == 1                     # the current reading and its alert are the same event
    s = shop.situation(evals(page), CALM, [])
    assert s["ph_count"] == 1 and s["ph_simulated"]


def test_budget_below_the_sensor_price_is_said_plainly():
    q = "My budget is ₹5,000. Which sensor should I buy?"
    text = shop.answer("recommend", q, evals(), HIGH, [])["en"]
    assert "The Night-Watch kit is est. ₹23,000, more than your budget of ₹5,000." in text
    honest_and_safe(text, q)


# ----------------------------------------------------------------- the AI path

def test_ai_gets_the_shop_facts_the_recommendation_and_the_rules(monkeypatch):
    fake = with_ai(monkeypatch, reply="Start with the free app and a test kit (est. ₹1,200). Not for sale yet. "
                                      "No payment is taken. See the Shop tab.")
    body = ask("Which sensor should I buy?", alerts=NIGHT_LOW_O2)
    assert body["mode"] == "ai"
    system = fake.calls[0]["system"]
    assert "## Shop (frontend/shop-data.json)" in system and "## Shop recommendation for this farmer" in system
    assert "Get the Night-Watch kit" in system                       # worked out from the farmer's night alerts
    for p in shop.PRODUCTS.values():
        assert f"{p['name']['en']} ({shop.product_price(p, 'en')})" in system
    assert "Never invent a product, feature or price" in system and "cheaper than other brands" in system


def test_ai_reply_with_an_invented_price_is_replaced(monkeypatch):
    with_ai(monkeypatch, reply="Buy the Night-Watch kit for just ₹9,999 today.")
    body = ask("Which sensor should I buy?")
    assert body["mode"] == "ready" and "9,999" not in body["text"] and body["text"].startswith(START["en"])


def test_ai_reply_claiming_cheaper_than_other_brands_is_replaced(monkeypatch):
    with_ai(monkeypatch, reply="The Night-Watch kit (est. ₹23,000) is cheaper than other brands.")
    body = ask("Which sensor should I buy?")
    assert body["mode"] == "ready" and "cheaper" not in body["text"]


def test_ai_unknown_on_a_shop_question_gives_the_ready_answer(monkeypatch):
    with_ai(monkeypatch, reply="UNKNOWN")
    body = ask("How do I use the test kit?")
    assert body["mode"] == "ready" and "1. " in body["text"]


def test_ai_reply_with_a_chemical_keeps_the_safety_message(monkeypatch):
    with_ai(monkeypatch, reply="Use the test kit, then add potassium permanganate.")
    body = ask("How do I use the test kit?")
    assert body["mode"] == "safety" and "permanganate" not in body["text"]


@pytest.mark.parametrize("lang", ["en", "kn"])
def test_gemini_unreachable_gives_a_ready_shop_answer(monkeypatch, lang):
    with_ai(monkeypatch, error=True)
    body = ask(QUESTIONS["which"][lang], lang)
    assert body["mode"] == "ready" and body["text"].startswith(START[lang])
    assert body["notice"] is None and "suggestions" not in body


def test_rate_limited_shop_question_still_gets_a_ready_answer(monkeypatch):
    with_ai(monkeypatch, reply="ok")
    monkeypatch.setattr(main, "assistant_limiter", A.RateLimiter(per_minute=0, per_hour=0, per_day_total=0))
    assert ask("Can I buy products?")["mode"] == "ready"


def test_non_shop_questions_are_not_taken_as_shop_questions():
    for q in list(A.QUESTIONS.values())[:7]:
        for lang in ("en", "kn"):
            assert shop.classify(q[lang]) is None, q[lang]
    for q in ("How much lime per acre should I spread?", "So how much exactly?",
              "I have 3 ponds, is the oxygen safe?", "What should I do now?"):
        assert shop.classify(q) is None, q


def test_dose_questions_are_still_refused_first(no_ai):
    body = ask("Which chemical should I buy for my pond?")
    assert body["mode"] == "safety"


# ----------------------------------------------------------------- suggested questions and the page

def test_shop_suggested_questions_have_ready_answers():
    s = {x["id"]: x for x in A.suggestions(evals(), HIGH, NIGHT_LOW_O2)}
    assert s["shop_which"]["answer"]["en"].startswith("Get the Night-Watch kit")
    assert KANNADA.search(s["shop_which"]["answer"]["kn"])
    assert "1. " in s["shop_test_kit"]["answer"]["en"]
    for x in (s["shop_which"], s["shop_test_kit"]):
        for lang in ("en", "kn"):
            honest_and_safe(x["answer"][lang])


def test_all_shop_answers_are_honest_and_safe_in_every_situation():
    for weather in (CALM, HIGH):
        for alerts in ([], NIGHT_LOW_O2, PH_OFTEN, NIGHT_LOW_O2 + PH_OFTEN):
            for kind in ("buy", "recommend", "use"):
                for q in ("which sensor", "I have 4 ponds", "how do I use the solar panel", "how to fit the DO cap"):
                    for lang, text in shop.answer(kind, q, evals(), weather, alerts).items():
                        honest_and_safe(text)
                        assert NOT_FOR_SALE[lang] in text


def test_recent_alerts_are_checked_by_the_api():
    bad = {**SAFE_POND, "question": "which sensor?", "recent_alerts": [{"source": "simulated", "level": "safe"}]}
    assert client.post("/api/assistant/ask", json=bad).status_code == 422
    many = {**SAFE_POND, "question": "which sensor?", "recent_alerts": NIGHT_LOW_O2 * 11}
    assert client.post("/api/assistant/ask", json=many).status_code == 422


def test_page_sends_only_level_cause_and_time_of_recent_alerts():
    front = Path(__file__).resolve().parent.parent / "frontend"
    history = (front / "history.js").read_text(encoding="utf-8")
    assert "function recentAlerts(" in history and "source: e.source," in history and "summary" not in \
        history[history.index("function recentAlerts("):history.index("const api")]
    assert "recent_alerts: H.recentAlerts(state.history)" in (front / "app.js").read_text(encoding="utf-8")
    chat = (front / "assistant.js").read_text(encoding="utf-8")
    assert 'body.mode === "ready"' in chat and "texts: body.texts" in chat   # shown as a ready answer, with Listen
