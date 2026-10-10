"""
Tests for the live sensor API (POST /api/sensor/{pond_id}) and the demo
device in tools/fake_sensor.py. No server or internet needed.

Run from the project folder with:   python -m pytest tests/test_sensor_api.py -v
"""

import json
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from backend import sensor
from backend import main
from backend.main import app
from tools import fake_sensor

client = TestClient(app)
KEY = "test-key-for-pond1"


@pytest.fixture(autouse=True)
def fresh_store(monkeypatch):
    """Every test starts like a freshly woken server: pond1 has a key, no readings yet."""
    monkeypatch.setenv("SENSOR_KEY_POND1", KEY)
    monkeypatch.delenv("SENSOR_KEY_POND2", raising=False)
    sensor.store.clear()
    yield
    sensor.store.clear()


@pytest.fixture
def no_rate_limit(monkeypatch):
    """For tests that send many readings at once (the rate limit is tested in tests/test_security.py)."""
    monkeypatch.setattr(main.request_limiter, "limits", {rule: (10_000, 10_000) for rule in main.request_limiter.limits})


def now_ist() -> str:
    return datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(timespec="seconds")


def good_reading(**changes) -> dict:
    reading = {"timestamp": now_ist(), "dissolved_oxygen": 6.2, "ph": 7.4,
               "temperature": 29.0, "ammonia": 0.3}
    reading.update(changes)
    return reading


def post(reading: dict, pond: str = "pond1", key: str | None = KEY):
    headers = {"X-Sensor-Key": key} if key is not None else {}
    return client.post(f"/api/sensor/{pond}", json=reading, headers=headers)


def stream_events(pond: str = "pond1") -> list[tuple[str, dict]]:
    """Read the dashboard stream once (seconds=0 closes it right after the current state)."""
    text = client.get(f"/api/sensor/{pond}/stream", params={"seconds": 0}).text
    events = []
    for block in text.strip().split("\n\n"):
        lines = dict(line.split(": ", 1) for line in block.splitlines())
        events.append((lines["event"], json.loads(lines["data"])))
    return events


# ----------------------------------------------------------------- the key

def test_good_reading_is_accepted_and_graded():
    r = post(good_reading())
    assert r.status_code == 201
    assert r.json()["accepted"] is True
    assert r.json()["level"] == "safe"


def test_missing_key_is_refused_and_nothing_is_stored():
    r = post(good_reading(), key=None)
    assert r.status_code == 401
    assert r.json()["error"] == "wrong_key"
    assert client.get("/api/sensor/pond1").json()["latest"] is None


def test_wrong_key_is_refused_and_not_shown_on_dashboard():
    assert post(good_reading(), key="guess").status_code == 401
    state = client.get("/api/sensor/pond1").json()
    assert state["latest"] is None and state["rejected"] is None


def test_one_ponds_key_does_not_work_for_another_pond(monkeypatch):
    monkeypatch.setenv("SENSOR_KEY_POND2", "other-key")
    assert post(good_reading(), pond="pond2", key=KEY).status_code == 401


def test_pond_without_a_key_on_the_server_says_not_set_up():
    r = post(good_reading(), pond="pond2", key="anything")
    assert r.status_code == 503
    assert r.json()["error"] == "not_set_up"
    assert "SENSOR_KEY_POND2" in r.json()["message"]["en"]


def test_unknown_pond_is_refused():
    assert post(good_reading(), pond="pond9").status_code == 422


def test_key_is_never_in_the_code_or_the_page():
    assert KEY not in client.get("/").text
    assert "SENSOR_KEY_POND1" not in client.get("/app.js").text


# ----------------------------------------------------------------- validation

@pytest.mark.parametrize("parameter, value", [
    ("dissolved_oxygen", 45.0),     # above 30 mg/L: impossible
    ("dissolved_oxygen", 0.0),      # exactly 0: a dead probe
    ("ph", 14.5),
    ("temperature", -3.0),
    ("ammonia", -0.5),
])
def test_impossible_value_is_rejected_with_check_the_sensor(parameter, value):
    r = post(good_reading(**{parameter: value}))
    assert r.status_code == 422
    body = r.json()
    assert body["accepted"] is False
    assert body["error"] == "check_the_sensor"
    assert "Check the sensor" in body["message"]["en"]
    assert "ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ" in body["message"]["kn"]
    assert body["sensor_errors"][0]["parameter"] == parameter
    assert "Check the sensor" in body["sensor_errors"][0]["message"]["en"]


def test_rejected_reading_is_not_stored_but_shown_as_a_fault():
    post(good_reading(dissolved_oxygen=6.0))
    post(good_reading(dissolved_oxygen=99.0))
    state = client.get("/api/sensor/pond1").json()
    assert state["latest"]["reading"]["dissolved_oxygen"] == 6.0       # the bad value never replaced it
    assert state["rejected"]["error"] == "check_the_sensor"
    post(good_reading(dissolved_oxygen=6.1))
    assert client.get("/api/sensor/pond1").json()["rejected"] is None   # a good reading clears the fault


@pytest.mark.parametrize("value", [b"NaN", b"Infinity"])
def test_not_a_number_from_a_broken_probe_is_rejected(value):
    body = b'{"timestamp": "%s", "ph": %s}' % (now_ist().encode(), value)
    r = client.post("/api/sensor/pond1", content=body,
                    headers={"X-Sensor-Key": KEY, "Content-Type": "application/json"})
    assert r.status_code == 422
    assert r.json()["error"] == "check_the_sensor"
    assert "Check the sensor" in r.json()["sensor_errors"][0]["message"]["en"]


def test_text_instead_of_a_number_is_rejected():
    assert post(good_reading(ph="low")).status_code == 422


def test_reading_with_no_values_is_rejected():
    r = post({"timestamp": now_ist()})
    assert r.status_code == 422
    assert r.json()["error"] == "no_values"


def test_timestamp_is_required():
    reading = good_reading()
    del reading["timestamp"]
    assert post(reading).status_code == 422


def test_timestamp_without_time_zone_is_rejected():
    r = post(good_reading(timestamp="2026-10-10T21:30:00"))
    assert r.status_code == 422
    assert r.json()["error"] == "bad_timestamp"
    assert "+05:30" in r.json()["message"]["en"]


def test_clock_ahead_and_very_old_timestamps_are_rejected():
    ahead = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()
    old = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
    assert post(good_reading(timestamp=ahead)).json()["error"] == "bad_timestamp"
    assert post(good_reading(timestamp=old)).json()["error"] == "bad_timestamp"
    # A few seconds of clock difference is normal.
    slightly_ahead = (datetime.now(timezone.utc) + timedelta(seconds=30)).isoformat()
    assert post(good_reading(timestamp=slightly_ahead)).status_code == 201


def test_sensor_without_ammonia_probe_is_fine():
    reading = good_reading()
    del reading["ammonia"]
    assert post(reading).status_code == 201


def test_low_oxygen_from_the_sensor_is_danger():
    r = post(good_reading(dissolved_oxygen=2.4))
    assert r.json()["level"] == "danger"
    assert "Oxygen" in r.json()["summary"]["en"]


# ----------------------------------------------------------------- what the dashboard gets

def test_latest_is_empty_before_the_first_reading():
    state = client.get("/api/sensor/pond1").json()
    assert state["latest"] is None
    assert state["label"] == sensor.LIVE_LABEL


def test_stream_sends_the_latest_reading_with_live_sensor_label():
    post(good_reading(dissolved_oxygen=3.8))
    events = stream_events()
    assert [name for name, _ in events] == ["sensor", "end"]
    latest = events[0][1]["latest"]
    assert latest["source"] == "live_sensor"
    assert latest["label"] == {"en": "Live sensor", "kn": "ಲೈವ್ ಸೆನ್ಸರ್"}
    assert latest["risk"]["level"] == "warning"
    assert latest["risk"]["actions"]                      # checklist for Warning
    assert latest["demo"] is False and latest["demo_label"] is None
    assert "[Live sensor]" in latest["alert"]["sms"]["en"]
    assert "Pond 1" in latest["alert"]["sms"]["en"]


def test_stream_before_any_reading_says_waiting():
    events = stream_events()
    assert events[0][0] == "sensor"
    assert events[0][1]["latest"] is None


def test_ponds_are_kept_apart(monkeypatch):
    monkeypatch.setenv("SENSOR_KEY_POND2", "key2")
    post(good_reading(dissolved_oxygen=6.5))
    post(good_reading(dissolved_oxygen=4.0), pond="pond2", key="key2")
    assert client.get("/api/sensor/pond1").json()["latest"]["reading"]["dissolved_oxygen"] == 6.5
    assert client.get("/api/sensor/pond2").json()["latest"]["reading"]["dissolved_oxygen"] == 4.0
    assert client.get("/api/sensor/pond3").json()["latest"] is None


def test_store_forgets_everything_on_restart_and_keeps_a_limited_history(no_rate_limit):
    for i in range(sensor.HISTORY_LENGTH + 5):
        post(good_reading(dissolved_oxygen=5 + (i % 10) / 10))
    assert sensor.store.count("pond1") == sensor.HISTORY_LENGTH
    sensor.store.clear()                                  # what free Render's sleep does
    assert client.get("/api/sensor/pond1").json()["latest"] is None


# ----------------------------------------------------------------- demo device (tools/fake_sensor.py)

def test_demo_device_readings_are_accepted_and_labelled_as_demo():
    sent = []
    device = fake_sensor.FakeSensor(scenario="falling", seed=1)
    for _ in range(3):
        payload = device.next_reading()
        assert payload["demo"] is True
        sent.append(post(payload))
    assert all(r.status_code == 201 for r in sent)
    latest = client.get("/api/sensor/pond1").json()["latest"]
    assert latest["demo"] is True
    assert latest["demo_label"]["en"].startswith("Demo device")
    assert "simulated readings" in latest["demo_label"]["en"]
    post({**device.next_reading(), "dissolved_oxygen": 3.5})       # a Warning, so an alert is written
    assert "Demo device" in client.get("/api/sensor/pond1").json()["latest"]["alert"]["sms"]["en"]


def test_demo_device_falling_scenario_reaches_danger(no_rate_limit):
    device = fake_sensor.FakeSensor(scenario="falling", seed=2)
    levels = []
    for _ in range(60):
        levels.append(post(device.next_reading()).json()["level"])
    assert levels[0] == "safe"
    assert "warning" in levels and levels[-1] == "danger"


def test_demo_device_fault_sends_an_impossible_value_that_is_rejected():
    device = fake_sensor.FakeSensor(scenario="normal", fault_every=2, seed=3)
    first, second = device.next_reading(), device.next_reading()
    assert post(first).status_code == 201
    assert post(second).json()["error"] == "check_the_sensor"


def test_demo_device_send_uses_the_key_header_and_reports_refusals():
    calls = []

    def fake_open(request, timeout):
        calls.append(request)
        raise fake_sensor.HTTPError(request.full_url, 422, "Unprocessable", {},
                                    __import__("io").BytesIO(b'{"message": {"en": "Reading rejected. Check the sensor."}}'))

    status, body = fake_sensor.send("http://127.0.0.1:8000", "pond1", "abc", {"ph": 7}, opener=fake_open)
    assert status == 422 and "Check the sensor" in body["message"]["en"]
    assert calls[0].get_header("X-sensor-key") == "abc"
    assert calls[0].full_url == "http://127.0.0.1:8000/api/sensor/pond1"
