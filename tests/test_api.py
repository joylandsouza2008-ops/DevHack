"""
Tests for the FastAPI backend. FastAPI's TestClient calls the app directly,
so no server needs to be running.

Run from the project folder with:   python -m pytest
"""

import json

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.simulator import DATA_FILE

client = TestClient(app)


def test_health():
    assert client.get("/api/health").json() == {"status": "ok"}


def test_risk_danger_with_reasons_in_both_languages():
    r = client.post("/api/risk", json={"dissolved_oxygen": 2.5, "ph": 7.2, "temperature": 29})
    assert r.status_code == 200
    body = r.json()
    assert body["level"] == "danger"
    assert body["causes"] == ["dissolved_oxygen"]
    assert body["level_name"] == {"en": "Danger", "kn": "ಅಪಾಯ"}
    assert "Oxygen is very low" in body["summary"]["en"]
    assert "ಆಮ್ಲಜನಕ" in body["summary"]["kn"]


def test_risk_safe():
    r = client.post("/api/risk", json={"dissolved_oxygen": 7.0, "ph": 7.4, "temperature": 28})
    assert r.json()["level"] == "safe"


def test_risk_rejects_text_instead_of_numbers():
    assert client.post("/api/risk", json={"dissolved_oxygen": "low"}).status_code == 422


def test_time_to_danger_endpoint():
    readings = [{"time": f"2026-10-03T00:{m:02d}:00", "dissolved_oxygen": v}
                for m, v in zip([0, 20, 40], [7.4, 7.0, 6.6])]
    readings += [{"time": f"2026-10-03T01:{m:02d}:00", "dissolved_oxygen": v}
                 for m, v in zip([0, 20, 40], [6.2, 5.8, 5.4])]
    body = client.post("/api/time-to-danger", json={"readings": readings}).json()
    assert body["status"] == "danger_expected"
    assert "around 03:40" in body["message"]["en"]


def test_forecast_model_is_not_exposed():
    paths = {route.path for route in app.routes}
    assert not any("forecast" in p for p in paths)


def test_page_is_served_with_simulated_label_and_local_fonts():
    html = client.get("/").text
    assert "Simulated data" in html
    assert "/fonts/fonts.css" in html
    assert "googleapis" not in html          # works offline
    assert client.get("/fonts/fonts.css").status_code == 200
    assert client.get("/app.js").status_code == 200


def read_events(response):
    events = []
    for block in response.text.strip().split("\n\n"):
        lines = dict(line.split(": ", 1) for line in block.splitlines())
        events.append((lines["event"], json.loads(lines["data"])))
    return events


@pytest.mark.skipif(not DATA_FILE.exists(), reason="Pondsdata not downloaded (see README)")
def test_simulator_stream_is_labelled_simulated():
    r = client.get("/api/simulator/stream", params={"count": 3, "interval": 0, "start": "2026-10-02T12:00:00"})
    assert r.headers["content-type"].startswith("text/event-stream")
    events = read_events(r)
    readings = [data for name, data in events if name == "reading"]
    assert len(readings) == 3 and events[-1][0] == "end"
    for data in readings:
        assert data["source"] == "simulated"
        assert data["label"]["en"] == "Simulated data"
        assert data["risk"]["level"] == "safe"
        assert data["time_to_danger"]["status"] in {"not_falling", "falling_slowly"}
    assert [d["time"] for d in readings] == ["2026-10-02T12:00:00", "2026-10-02T12:20:00", "2026-10-02T12:40:00"]


@pytest.mark.skipif(not DATA_FILE.exists(), reason="Pondsdata not downloaded (see README)")
def test_simulator_stream_crash_warns_before_danger():
    r = client.get("/api/simulator/stream", params={"scenario": "oxygen_crash", "count": 30, "interval": 0,
                                                     "start": "2026-10-02T20:00:00"})
    readings = [data for name, data in read_events(r) if name == "reading"]
    first_alert = next(d["time"] for d in readings if d["time_to_danger"]["status"] == "danger_expected")
    first_danger = next(d["time"] for d in readings if d["risk"]["level"] == "danger")
    assert first_alert < first_danger


def test_simulator_rejects_unknown_scenario():
    assert client.get("/api/simulator/stream", params={"scenario": "tsunami"}).status_code == 422
