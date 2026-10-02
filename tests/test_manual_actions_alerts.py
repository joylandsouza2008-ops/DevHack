"""
Tests for the three farmer features:
  - manual test-kit entry   (POST /api/manual)
  - action checklist        (backend/actions.py)
  - SMS / WhatsApp preview  (backend/alerts.py)

Run from the project folder with:   python -m pytest
"""

import re

import pytest
from fastapi.testclient import TestClient

from backend.actions import ACTIONS, PLAN, checklist
from backend.alerts import compose_alert
from backend.main import MANUAL_LABEL, app
from backend.risk_classifier import classify
from backend.simulator import SIMULATED_LABEL

client = TestClient(app)


def risk(**reading):
    return classify(reading).to_dict()


# --- manual test-kit entry -------------------------------------------------------

def test_manual_reading_uses_the_same_classifier_and_is_marked_manual():
    body = client.post("/api/manual", json={"dissolved_oxygen": 2.5, "ph": 7.2, "temperature": 29}).json()
    assert body["source"] == "manual"
    assert body["label"] == MANUAL_LABEL
    assert body["label"] != SIMULATED_LABEL
    expected = risk(dissolved_oxygen=2.5, ph=7.2, temperature=29)
    assert body["risk"]["level"] == expected["level"] == "danger"
    assert body["risk"]["summary"] == expected["summary"]


def test_manual_impossible_value_says_check_your_test_kit():
    body = client.post("/api/manual", json={"ph": 15, "dissolved_oxygen": 6}).json()
    error = body["risk"]["sensor_errors"][0]
    assert error["parameter"] == "ph"
    assert "Check your test kit" in error["message"]["en"]
    assert "ಟೆಸ್ಟ್ ಕಿಟ್" in error["message"]["kn"]
    assert "sensor" not in error["message"]["en"].lower()
    assert body["risk"]["level"] == "safe"            # the impossible pH is ignored, oxygen is fine


def test_manual_all_impossible_is_unknown_with_test_kit_message():
    body = client.post("/api/manual", json={"temperature": 80}).json()
    assert body["risk"]["level"] == "unknown"
    assert body["risk"]["summary"]["en"] == "No valid readings. Check your test kit."


def test_manual_needs_at_least_one_reading():
    assert client.post("/api/manual", json={}).status_code == 422


def test_manual_rejects_text():
    assert client.post("/api/manual", json={"ph": "seven"}).status_code == 422


def test_manual_ignores_fields_a_test_kit_does_not_have():
    body = client.post("/api/manual", json={"ph": 7.0, "turbidity": 30}).json()
    assert "turbidity" not in body["reading"]


def test_sensor_readings_still_say_check_the_sensor():
    r = classify({"ph": 15})
    assert "Check the sensor" in r.sensor_errors[0]["message"]["en"]


# --- action checklist ------------------------------------------------------------

def test_no_checklist_when_safe():
    assert checklist(risk(dissolved_oxygen=7, ph=7.4, temperature=28)) == []


def test_low_oxygen_danger_starts_with_the_aerator():
    items = checklist(risk(dissolved_oxygen=2.0))
    assert items[0]["id"] == "aerator_now"
    assert "stop_feeding" in [a["id"] for a in items]
    assert items[0]["kn"] and items[0]["sources"]


def test_warning_checklist_for_low_oxygen():
    ids = [a["id"] for a in checklist(risk(dissolved_oxygen=4.0))]
    assert ids == ["aerator_night", "reduce_feeding", "watch_fish", "retest_oxygen_evening"]


def test_two_causes_are_merged_without_repeats():
    # Oxygen and temperature both in Danger: both ask for the aerator, shown once.
    ids = [a["id"] for a in checklist(risk(dissolved_oxygen=2.0, temperature=36))]
    assert ids.count("aerator_now") == 1
    assert "cool_water" in ids and "stop_feeding" in ids


def test_only_the_worst_causes_get_actions():
    # Oxygen Danger + pH Warning: the list is for oxygen only.
    ids = [a["id"] for a in checklist(risk(dissolved_oxygen=2.0, ph=9.0))]
    assert "retest_ph_morning" not in ids


def test_api_risk_includes_actions():
    body = client.post("/api/risk", json={"dissolved_oxygen": 2.5}).json()
    assert body["actions"][0]["id"] == "aerator_now"


def test_every_action_has_a_source_and_both_languages():
    for action in ACTIONS.values():
        assert action["en"] and action["kn"] and action["sources"]
    for ids in PLAN.values():
        assert all(a in ACTIONS for a in ids)


CHEMICALS = re.compile(r"lime|chemical|potassium|permanganate|salt|alum|acid|dose|kg|gram|ppm|"
                       r"ಸುಣ್ಣ|ರಾಸಾಯನಿಕ|ಉಪ್ಪು", re.IGNORECASE)


@pytest.mark.parametrize("action_id", list(ACTIONS))
def test_no_action_suggests_chemicals_or_doses(action_id):
    action = ACTIONS[action_id]
    assert not CHEMICALS.search(action["en"]), action["en"]
    assert not CHEMICALS.search(action["kn"]), action["kn"]


def test_every_cited_source_is_listed_in_the_docs():
    from pathlib import Path
    doc = (Path(__file__).resolve().parent.parent / "docs" / "actions.md").read_text(encoding="utf-8")
    for action_id, action in ACTIONS.items():
        assert f"`{action_id}`" in doc, f"{action_id} missing from docs/actions.md"
        for n in action["sources"]:
            assert re.search(rf"^{n}\. ", doc, re.MULTILINE), f"source {n} missing from docs/actions.md"


# --- SMS / WhatsApp preview -------------------------------------------------------

def test_alert_uses_the_same_message_as_the_app():
    r = risk(dissolved_oxygen=2.5)
    alert = compose_alert(r, label=SIMULATED_LABEL, pond={"en": "Pond 1", "kn": "ಕೊಳ 1"})
    assert alert["send"] is True
    for lang in ("en", "kn"):
        assert r["summary"][lang] in alert["sms"][lang]
        assert r["summary"][lang] in alert["whatsapp"][lang]
        assert SIMULATED_LABEL[lang] in alert["sms"][lang]
    assert alert["sms"]["en"].startswith("MeenuRaksha: DANGER - Pond 1.")
    assert "*ಅಪಾಯ* - ಕೊಳ 1" in alert["whatsapp"]["kn"]


def test_alert_adds_time_until_danger_when_expected():
    ttd = {"status": "danger_expected", "message": {"en": "Oxygen is falling.", "kn": "ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗುತ್ತಿದೆ."}}
    alert = compose_alert(risk(dissolved_oxygen=4.0), ttd)
    assert "Oxygen is falling." in alert["sms"]["en"]
    assert "ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗುತ್ತಿದೆ." in alert["whatsapp"]["kn"]


def test_no_alert_when_safe():
    alert = compose_alert(risk(dissolved_oxygen=7.0))
    assert alert["send"] is False
    assert "No alert would be sent" in alert["sms"]["en"]


def test_stream_carries_alert_preview_and_actions():
    with client.stream("GET", "/api/simulator/stream",
                       params={"scenario": "oxygen_crash", "interval": 0, "count": 1}) as r:
        if r.status_code == 503:
            pytest.skip("dataset not downloaded")
        text = "".join(r.iter_text())
    assert '"alert"' in text and '"actions"' in text


def test_page_has_the_three_features_with_preview_label():
    html = client.get("/").text
    assert 'id="kit-form"' in html and 'id="actions-card"' in html and 'id="alert-bubble"' in html
    assert "No real SMS or WhatsApp message is sent" in html
