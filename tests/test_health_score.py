"""
Tests for the pond health score (backend/health_score.py).

The most important check: the score can never contradict the status
(Danger always low, Safe always high), for thousands of random readings.

Run from the project folder with:   python -m pytest tests/test_health_score.py
"""

import random

from fastapi.testclient import TestClient

from backend.health_score import BANDS, health_score
from backend.main import app
from backend.risk_classifier import classify, load_thresholds

THRESHOLDS = load_thresholds()     # read once: the random test below classifies 5000 readings


def score(reading):
    risk = classify(reading, THRESHOLDS).to_dict()
    return risk["level"], health_score(risk)


def test_bands_do_not_overlap_and_cover_0_to_100():
    assert BANDS["danger"] == (0, 39)
    assert BANDS["warning"] == (40, 74)
    assert BANDS["safe"] == (75, 100)


def test_safe_score_follows_oxygen_headroom():
    base = {"ph": 7.4, "temperature": 28}
    assert score({**base, "dissolved_oxygen": 5.0}) == ("safe", 75)
    assert score({**base, "dissolved_oxygen": 6.0}) == ("safe", 88)
    assert score({**base, "dissolved_oxygen": 7.0}) == ("safe", 100)
    assert score({**base, "dissolved_oxygen": 12.0}) == ("safe", 100)


def test_safe_without_oxygen_reading_is_100():
    assert score({"ph": 7.4, "temperature": 28}) == ("safe", 100)


def test_warning_examples_from_docs():
    # DO in Warning, the other three Safe -> 40 + 34 * 3/4
    reading = {"dissolved_oxygen": 4.0, "ph": 7.2, "temperature": 29, "ammonia": 0.05}
    assert score(reading) == ("warning", 66)
    # DO and pH in Warning, two Safe -> 40 + 34 * 2/4
    reading = {"dissolved_oxygen": 4.0, "ph": 9.0, "temperature": 29, "ammonia": 0.01}
    assert score(reading) == ("warning", 57)


def test_danger_examples_from_docs():
    reading = {"dissolved_oxygen": 2.5, "ph": 7.2, "temperature": 29, "ammonia": 0.05}
    assert score(reading) == ("danger", 29)
    reading = {"dissolved_oxygen": 2.5, "ph": 9.0, "temperature": 29, "ammonia": 0.01}
    assert score(reading) == ("danger", 24)


def test_more_problems_means_lower_score():
    one = {"dissolved_oxygen": 2.5, "ph": 7.2, "temperature": 29}
    two = {"dissolved_oxygen": 2.5, "ph": 10.5, "temperature": 29}
    three = {"dissolved_oxygen": 2.5, "ph": 10.5, "temperature": 37}
    assert score(one)[1] > score(two)[1] > score(three)[1]


def test_unknown_status_has_no_score():
    assert score({}) == ("unknown", None)
    assert score({"dissolved_oxygen": 0.0}) == ("unknown", None)   # sensor fault only
    assert score({"turbidity": 30}) == ("unknown", None)           # information only


def test_score_never_contradicts_status_for_random_readings():
    rng = random.Random(2026)
    seen = set()
    for _ in range(5000):
        reading = {
            "dissolved_oxygen": rng.uniform(0.0, 14.0),
            "ph": rng.uniform(4.0, 11.0),
            "temperature": rng.uniform(15.0, 40.0),
            "ammonia": rng.uniform(0.0, 3.0),
            "nitrate": rng.uniform(0.0, 120.0),
        }
        for key in list(reading):          # sometimes leave readings out
            if rng.random() < 0.2:
                del reading[key]
        level, value = score(reading)
        if level == "unknown":
            assert value is None
            continue
        low, high = BANDS[level]
        assert low <= value <= high, (reading, level, value)
        assert isinstance(value, int)
        seen.add(level)
    assert seen == {"safe", "warning", "danger"}


def test_api_returns_health_score():
    client = TestClient(app)
    body = client.post("/api/risk", json={"dissolved_oxygen": 2.5, "ph": 7.2, "temperature": 29}).json()
    assert body["level"] == "danger"
    assert body["health_score"] == 26        # 39 * 2/3
    body = client.post("/api/manual", json={"dissolved_oxygen": 7.5, "ph": 7.4}).json()
    assert body["risk"]["health_score"] == 100
