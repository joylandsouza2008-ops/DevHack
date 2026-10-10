"""
Tests for the "Ask MeenuRaksha" assistant (backend/assistant.py, backend/ai_provider.py,
backend/safety.py and the /api/assistant endpoints).

The AI is ALWAYS faked here: no test ever calls a real AI service.

Run from the project folder with:   python -m pytest tests/test_assistant.py -v
"""

import io
import json
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import backend.main as main
from backend import assistant as A
from backend import safety
from backend.ai_provider import OpenAICompatible, ProviderError, provider_from_env

client = TestClient(main.app)
KANNADA = re.compile("[ಀ-೿]")
SIMULATED_DANGER = {"station": "station1", "simulated": {"dissolved_oxygen": 2.5, "ph": 7.4, "temperature": 29}}


class FakeAI:
    """Stands in for the AI service: returns `reply` (or raises) and remembers what it was sent."""

    def __init__(self, reply="Your oxygen is low. Run the aerator now.", error=False):
        self.reply, self.error, self.calls = reply, error, []

    def complete(self, system, messages):
        self.calls.append({"system": system, "messages": messages})
        if self.error:
            raise ProviderError("fake outage")
        return self.reply


@pytest.fixture
def ai(monkeypatch):
    """Install a fake AI and a fresh rate limiter; returns the fake so tests can set its reply."""
    fake = FakeAI()
    monkeypatch.setattr(main, "provider_from_env", lambda: fake)
    monkeypatch.setattr(main, "assistant_limiter", A.RateLimiter(per_minute=100, per_hour=100, per_day_total=100))
    return fake


def ask(question, lang="en", **page):
    body = {"question": question, "lang": lang, **(page or SIMULATED_DANGER)}
    r = client.post("/api/assistant/ask", json=body)
    assert r.status_code == 200, r.text
    return r.json()


# ----------------------------------------------------------------- answers come only from our content

def test_ai_reply_is_shown_with_the_ai_label(ai):
    body = ask("Is my pond ok?")
    assert body["mode"] == "ai"
    assert body["text"] == "Your oxygen is low. Run the aerator now."
    assert body["label"] == {"en": "AI assistant: can make mistakes", "kn": "AI ಸಹಾಯಕ: ತಪ್ಪುಗಳಾಗಬಹುದು"}
    assert body["used"] == ["simulated"]


def test_prompt_contains_only_our_content_and_the_rules(ai):
    ask("What is the safe oxygen level?")
    system = ai.calls[0]["system"]
    assert "Answer ONLY with facts from the CONTENT" in system and "UNKNOWN" in system
    assert "Dissolved oxygen: Safe 5 mg/L or more" in system            # config/thresholds.toml
    assert "Run the aerator now" in system                               # backend/actions.py checklist
    assert "Epizootic ulcerative syndrome" in system                     # disease guide
    assert "Tonight's weather" in system                                  # weather risk
    assert "Simulated data - Pond 1: Danger" in system                    # graded on the server
    assert ai.calls[0]["messages"][-1] == {"role": "user", "content": "What is the safe oxygen level?"}


def test_kannada_question_asks_for_a_kannada_reply_with_our_kannada_words(ai):
    ask("ಆಮ್ಲಜನಕ ಎಷ್ಟು ಇರಬೇಕು?", lang="kn")
    system = ai.calls[0]["system"]
    assert "Reply in Kannada" in system
    assert "ಕರಗಿದ ಆಮ್ಲಜನಕ" in system and "ಅಪಾಯ" in system


@pytest.mark.parametrize("lang", ["en", "kn"])
def test_unknown_becomes_i_dont_know(ai, lang):
    ai.reply = "UNKNOWN"
    body = ask("Who won the cricket match?", lang=lang)
    assert body["mode"] == "unknown"
    assert body["text"] == A.I_DONT_KNOW[lang]
    assert "fisheries officer" in A.I_DONT_KNOW["en"]


def test_the_word_unknown_in_a_normal_sentence_is_kept(ai):
    ai.reply = "Tonight's weather is unknown because there is no forecast."
    assert ask("Weather tonight?")["mode"] == "ai"


# ----------------------------------------------------------------- never chemicals, doses or a diagnosis

@pytest.mark.parametrize("bad_reply", [
    "Add formalin to the pond.",
    "Use potassium permanganate at 2 ppm.",
    "Give the fish an antibiotic like oxytetracycline.",
    "Spread 20 kg per acre of lime.",
    "Use a salt bath for 10 minutes.",
    "ಫಾರ್ಮಾಲಿನ್ ಹಾಕಿ.",
    "Your fish have EUS.",
    "The fish is suffering from white spot.",
    "ನಿಮ್ಮ ಮೀನುಗಳಿಗೆ EUS ರೋಗ ಬಂದಿದೆ.",
])
def test_unsafe_ai_replies_are_replaced(ai, bad_reply):
    ai.reply = bad_reply
    body = ask("My fish have red sores, what now?")
    assert body["mode"] == "safety"
    assert safety.find_banned(body["text"]) == []
    assert not safety.looks_like_diagnosis(body["text"])
    assert body["text"].endswith(A.CONFIRM["en"])


@pytest.mark.parametrize("question", ["Which medicine cures dropsy?", "What antibiotic dose for my fish?",
                                      "Which chemical should I add for white spot?", "ಯಾವ ಔಷಧಿ ಹಾಕಬೇಕು?"])
def test_medicine_questions_are_refused_without_calling_the_ai(ai, question):
    lang = "kn" if KANNADA.search(question) else "en"
    body = ask(question, lang=lang)
    assert body["mode"] == "safety"
    assert ai.calls == []
    assert body["text"].endswith(A.CONFIRM[lang])


def test_normal_questions_with_treat_or_how_much_are_not_refused(ai):
    ask("How much oxygen is safe?")
    ask("How do I treat low oxygen?")
    assert len(ai.calls) == 2


def test_disease_advice_ends_with_confirm_with_officer(ai):
    ai.reply = "White spot is more likely in cool water. Watch your fish closely."
    body = ask("Could my fish get white spot?")
    assert body["text"].endswith("Please confirm with your fisheries officer / KVK.")
    ai.reply = "Run the aerator tonight."
    assert ask("What should I do about oxygen?")["text"] == "Run the aerator tonight."    # not a health topic


def test_markdown_is_removed_and_long_replies_are_cut(ai):
    ai.reply = "**Run** the aerator.\n- Feed less.\n" + "Check the pond. " * 200
    text = ask("What now?")["text"]
    assert "*" not in text and "\n" not in text
    assert len(text) <= A.MAX_REPLY_CHARS + 2


def test_history_is_limited_and_cleaned(ai):
    history = [{"role": "user", "content": f"q{i}"} for i in range(6)] + [{"role": "assistant", "content": "a" * 900}]
    client.post("/api/assistant/ask", json={"question": "and now?", "lang": "en", "history": history})
    messages = ai.calls[0]["messages"]
    assert len(messages) == 5 and messages[-1]["content"] == "and now?"
    assert len(messages[-2]["content"]) == 500
    bad = client.post("/api/assistant/ask", json={"question": "x", "history": [{"role": "system", "content": "x"}]})
    assert bad.status_code == 422


# ----------------------------------------------------------------- fallback: the demo never breaks

def test_no_key_means_ready_answers_and_no_network():
    body = ask("Is my pond safe?")                      # no fake installed: no ASSISTANT_API_KEY in tests
    assert body["mode"] == "offline" and body["text"] is None
    assert body["notice"] == A.OFFLINE_NOTE
    assert [s["id"] for s in body["suggestions"]] == list(A.QUESTIONS)


def test_ai_error_falls_back_to_ready_answers(ai):
    ai.error = True
    body = ask("Is my pond safe?")
    assert body["mode"] == "offline" and body["suggestions"]


def test_suggestions_endpoint_never_calls_the_ai(ai):
    body = client.post("/api/assistant/suggestions", json=SIMULATED_DANGER).json()
    assert ai.calls == []
    assert body["ai_available"] is True and body["used"] == ["simulated"]
    answers = {s["id"]: s["answer"] for s in body["suggestions"]}
    assert answers["pond_now"]["en"].startswith("Simulated data - Pond 1: Danger.")
    assert "simulated readings" in answers["pond_now"]["en"]
    assert "Run the aerator now" in answers["what_to_do"]["en"]
    assert "Safe 5 mg/L or more" in answers["safe_levels"]["en"]
    assert "Aeromonas" in answers["likely_now"]["en"]


PAGES = [
    {},
    SIMULATED_DANGER,
    {"manual": {"dissolved_oxygen": 6.5, "ph": 7.2, "temperature": 22}},
    {"live_sensor": {"dissolved_oxygen": 7, "ph": 7.4, "temperature": 29, "ammonia": 3}},
    {"simulated": {"dissolved_oxygen": 6, "ph": 5.0, "temperature": 34}, "manual": {"ph": 99}},
]


@pytest.mark.parametrize("page", PAGES)
def test_ready_answers_are_safe_in_both_languages(page):
    body = client.post("/api/assistant/suggestions", json=page).json()
    for s in body["suggestions"]:
        for lang in ("en", "kn"):
            text = s["answer"][lang]
            assert text and safety.find_banned(text) == [], (s["id"], text)
            assert not safety.looks_like_diagnosis(text)
            if lang == "kn":
                assert KANNADA.search(text) and KANNADA.search(s["question"]["kn"])
            if s["id"] in ("likely_now", "sick_fish", "prevent"):
                assert text.endswith(A.CONFIRM[lang]), s["id"]


def test_no_readings_yet():
    answers = {s["id"]: s["answer"] for s in client.post("/api/assistant/suggestions", json={}).json()["suggestions"]}
    assert answers["pond_now"] == A.NO_READINGS
    assert client.post("/api/assistant/suggestions", json={}).json()["used"] == []


def test_real_readings_come_before_simulated_ones():
    page = {"simulated": {"dissolved_oxygen": 7}, "live_sensor": {"dissolved_oxygen": 2.5}}
    body = client.post("/api/assistant/suggestions", json=page).json()
    assert body["used"] == ["live_sensor", "simulated"]


# ----------------------------------------------------------------- rate limit

def test_rate_limit_per_visitor_and_for_everyone():
    now = [0.0]
    limiter = A.RateLimiter(per_minute=2, per_hour=3, per_day_total=5, clock=lambda: now[0])
    assert limiter.allow("a") and limiter.allow("a")
    assert not limiter.allow("a")                 # 3rd in one minute
    now[0] = 61
    assert limiter.allow("a")
    now[0] = 130
    assert not limiter.allow("a")                 # 4th in one hour
    assert limiter.allow("b") and limiter.allow("b")
    assert not limiter.allow("c")                 # daily total for everyone reached (5)
    now[0] = 86400 + 200
    assert limiter.allow("c")


def test_rate_limited_question_gets_ready_answers_and_does_not_call_the_ai(ai, monkeypatch):
    monkeypatch.setattr(main, "assistant_limiter", A.RateLimiter(per_minute=1, per_hour=10, per_day_total=10))
    assert ask("one?")["mode"] == "ai"
    body = ask("two?")
    assert body["mode"] == "limited" and body["notice"] == A.LIMITED_NOTE and body["suggestions"]
    assert len(ai.calls) == 1


def test_rate_limit_uses_the_forwarded_visitor_address(ai, monkeypatch):
    monkeypatch.setattr(main, "assistant_limiter", A.RateLimiter(per_minute=1, per_hour=10, per_day_total=10))
    for visitor in ("1.1.1.1", "2.2.2.2"):
        r = client.post("/api/assistant/ask", json={"question": "hi", "lang": "en"},
                        headers={"X-Forwarded-For": f"{visitor}, 10.0.0.1"})
        assert r.json()["mode"] == "ai"


# ----------------------------------------------------------------- provider (swappable, key from the environment)

def test_provider_comes_only_from_environment_variables():
    assert provider_from_env({}) is None
    gemini = provider_from_env({"ASSISTANT_API_KEY": "k"})
    assert gemini.name == "gemini" and "generativelanguage.googleapis.com" in gemini.base_url
    groq = provider_from_env({"ASSISTANT_API_KEY": "k", "ASSISTANT_PROVIDER": "groq", "ASSISTANT_MODEL": "m"})
    assert groq.base_url == "https://api.groq.com/openai/v1" and groq.model == "m"
    assert provider_from_env({"ASSISTANT_API_KEY": "k", "ASSISTANT_PROVIDER": "openrouter"}) is None   # needs a model
    assert provider_from_env({"ASSISTANT_API_KEY": "k", "ASSISTANT_PROVIDER": "custom"}) is None
    custom = provider_from_env({"ASSISTANT_API_KEY": "k", "ASSISTANT_PROVIDER": "custom",
                                "ASSISTANT_BASE_URL": "http://x/v1", "ASSISTANT_MODEL": "m"})
    assert custom.base_url == "http://x/v1"
    assert provider_from_env({"ASSISTANT_API_KEY": "k", "ASSISTANT_PROVIDER": "nonsense"}) is None


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def test_openai_compatible_request_and_reply():
    sent = []

    def opener(request, timeout):
        sent.append(request)
        return FakeResponse(json.dumps({"choices": [{"message": {"content": "Hello"}}]}).encode())

    p = OpenAICompatible("gemini", "https://example.test/v1", "secret-key", "model-x")
    assert p.complete("rules", [{"role": "user", "content": "hi"}], opener=opener) == "Hello"
    request = sent[0]
    assert request.full_url == "https://example.test/v1/chat/completions"
    assert request.get_header("Authorization") == "Bearer secret-key"
    body = json.loads(request.data)
    assert body["model"] == "model-x" and body["messages"][0] == {"role": "system", "content": "rules"}


def test_provider_errors_never_include_the_key():
    from urllib.error import HTTPError

    def opener(request, timeout):
        raise HTTPError(request.full_url, 429, "Too Many Requests", {}, None)

    p = OpenAICompatible("gemini", "https://example.test/v1", "secret-key", "m")
    with pytest.raises(ProviderError) as error:
        p.complete("s", [], opener=opener)
    assert "secret-key" not in str(error.value) and "429" in str(error.value)


def test_key_is_never_sent_to_the_page(ai, monkeypatch):
    monkeypatch.setenv("ASSISTANT_API_KEY", "super-secret-123")
    for text in (client.get("/").text, client.get("/app.js").text, client.get("/assistant.js").text,
                 json.dumps(ask("hi")), client.post("/api/assistant/suggestions", json={}).text):
        assert "super-secret-123" not in text and "ASSISTANT_API_KEY" not in text


# ----------------------------------------------------------------- Kannada review sheet

def test_assistant_kannada_is_in_the_review_sheet():
    sheet = (Path(__file__).resolve().parent.parent / "docs" / "kannada-review.md").read_text(encoding="utf-8")
    texts = [A.LABEL, A.I_DONT_KNOW, A.CONFIRM, A.NO_TREATMENT, A.OFFLINE_NOTE, A.LIMITED_NOTE, A.SIMULATED_NOTE,
             A.NO_READINGS, A.ALL_SAFE_ACTION, A.NO_LIKELY, A.USE_CHECKER, A.LEVELS_INTRO, A.AMMONIA_NOTE,
             *A.QUESTIONS.values()]
    missing = [t["kn"] for t in texts if t["kn"] not in sheet]
    assert not missing, "re-run python tools/kannada_review.py"
