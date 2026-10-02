"""
Tests for tonight's oxygen crash risk (backend/weather.py).

No test touches the internet: a fake "download" function returns a made-up
forecast, or raises an error to pretend there is no internet. The saved
forecast goes to a temporary folder (pytest's tmp_path), not data/.

Run from the project folder with:   python -m pytest
"""

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

import backend.main
from backend.weather import rate_crash_risk, summarise, tonight_crash_risk, tonight_window

AFTERNOON = datetime(2026, 10, 2, 15, 0)
RULES = {"cloudy_day_min_cloud_pct": 75, "still_night_max_wind_kmh": 7, "warm_night_min_temp_c": 28}


def fake_forecast(cloud=50, wind=12, temp=26, start=datetime(2026, 10, 1)):
    """Open-Meteo-shaped forecast: the same values every hour for 4 days."""
    hours = [start + timedelta(hours=h) for h in range(96)]
    return {"hourly": {
        "time": [t.isoformat(timespec="minutes") for t in hours],
        "cloud_cover": [cloud] * 96,
        "wind_speed_10m": [wind] * 96,
        "temperature_2m": [temp] * 96,
    }}


def no_internet(latitude, longitude):
    raise OSError("no internet")


# --- the rules -----------------------------------------------------------

def test_fine_weather_is_low():
    r = rate_crash_risk(40, 12, 26, RULES)
    assert r["level"] == "low" and r["factors"] == []
    assert "low risk" in r["message"]["en"]
    assert "ಕಡಿಮೆ" in r["message"]["kn"]


def test_one_factor_is_medium():
    r = rate_crash_risk(40, 3, 26, RULES)
    assert r["level"] == "medium" and r["factors"] == ["still"]
    assert r["message"]["en"].startswith("Still night ahead")


def test_cloudy_still_night_is_high_with_aerator_advice():
    r = rate_crash_risk(90, 3, 26, RULES)
    assert r["level"] == "high"
    assert r["message"]["en"] == "Cloudy, still night ahead: keep the aerator ready."
    assert r["message"]["kn"] == "ಮೋಡ ಕವಿದ, ಗಾಳಿಯಿಲ್ಲದ ರಾತ್ರಿ ಬರಲಿದೆ: ಏರೇಟರ್ ಸಿದ್ಧವಾಗಿಡಿ."
    assert r["level_name"] == {"en": "High", "kn": "ಹೆಚ್ಚು"}


def test_all_three_factors_is_high():
    assert rate_crash_risk(100, 0, 30, RULES)["factors"] == ["cloudy", "still", "warm"]


def test_edges():
    # Exactly on the cloud and temperature limits counts; exactly 7 km/h wind is NOT still.
    assert rate_crash_risk(75, 7, 28, RULES)["factors"] == ["cloudy", "warm"]


def test_rules_are_read_from_the_config_file():
    assert rate_crash_risk(90, 3, 26)["level"] == "high"


# --- which hours count as "tonight" ----------------------------------------

def test_tonight_in_the_afternoon_is_this_evening():
    day, night, end = tonight_window(AFTERNOON)
    assert (day, night, end) == (datetime(2026, 10, 2, 6), datetime(2026, 10, 2, 18), datetime(2026, 10, 3, 6))


def test_tonight_before_dawn_is_the_night_we_are_in():
    _, night, end = tonight_window(datetime(2026, 10, 3, 2, 30))
    assert (night, end) == (datetime(2026, 10, 2, 18), datetime(2026, 10, 3, 6))


def test_summary_uses_day_clouds_and_night_wind():
    f = fake_forecast(cloud=0, wind=20)
    hourly = f["hourly"]
    for i, t in enumerate(hourly["time"]):
        hour = datetime.fromisoformat(t)
        if datetime(2026, 10, 2, 6) <= hour < datetime(2026, 10, 2, 18):
            hourly["cloud_cover"][i] = 100          # cloudy day
        if datetime(2026, 10, 2, 18) <= hour < datetime(2026, 10, 3, 6):
            hourly["wind_speed_10m"][i] = 2         # still night
    s = summarise(f, AFTERNOON)
    assert s["day_cloud_cover_pct"] == 100 and s["night_wind_speed_kmh"] == 2


def test_summary_is_none_when_forecast_does_not_reach_tonight():
    assert summarise(fake_forecast(start=datetime(2026, 9, 1)), AFTERNOON) is None


# --- internet, saved copy, offline ------------------------------------------

def test_online_saves_the_forecast(tmp_path):
    cache = tmp_path / "weather_cache.json"
    r = tonight_crash_risk(AFTERNOON, cache_file=cache, download=lambda la, lo: fake_forecast(cloud=90, wind=3))
    assert r["status"] == "ok" and r["offline"] is False and r["level"] == "high"
    assert r["location"]["en"] == "Mangaluru"
    assert cache.exists()


def test_offline_uses_the_saved_forecast(tmp_path):
    cache = tmp_path / "weather_cache.json"
    tonight_crash_risk(AFTERNOON, cache_file=cache, download=lambda la, lo: fake_forecast(cloud=90, wind=3))
    later = AFTERNOON + timedelta(hours=3)
    r = tonight_crash_risk(later, cache_file=cache, download=no_internet)
    assert r["offline"] is True
    assert r["status"] == "ok" and r["level"] == "high"
    assert r["saved_at"] == "2026-10-02T15:00"


def test_offline_with_nothing_saved_is_unavailable(tmp_path):
    r = tonight_crash_risk(AFTERNOON, cache_file=tmp_path / "none.json", download=no_internet)
    assert r["status"] == "unavailable" and r["offline"] is True and r["level"] is None
    assert "No internet" in r["message"]["en"] and r["message"]["kn"]


def test_recent_forecast_is_reused_without_downloading(tmp_path):
    cache = tmp_path / "weather_cache.json"
    tonight_crash_risk(AFTERNOON, cache_file=cache, download=lambda la, lo: fake_forecast())
    r = tonight_crash_risk(AFTERNOON + timedelta(minutes=10), cache_file=cache, download=no_internet)
    assert r["offline"] is False and r["status"] == "ok"


def test_broken_saved_file_is_ignored(tmp_path):
    cache = tmp_path / "weather_cache.json"
    cache.write_text("not json", encoding="utf-8")
    assert tonight_crash_risk(AFTERNOON, cache_file=cache, download=no_internet)["status"] == "unavailable"


# --- the API -----------------------------------------------------------------

def test_endpoint(monkeypatch):
    monkeypatch.setattr(backend.main, "tonight_crash_risk", lambda: {"status": "ok", "level": "low"})
    assert TestClient(backend.main.app).get("/api/weather/tonight").json() == {"status": "ok", "level": "low"}


def test_endpoint_without_internet_answers_quickly_and_offline():
    # tests/conftest.py blocks the real internet, so this is what a farmer
    # with no signal sees: no crash, no long wait, "offline".
    import time
    started = time.monotonic()
    r = TestClient(backend.main.app).get("/api/weather/tonight").json()
    assert time.monotonic() - started < 2
    assert r["offline"] is True and r["status"] == "unavailable"
