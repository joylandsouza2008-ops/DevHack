"""
Tonight's oxygen crash risk, from the weather forecast.

What this file does, step by step:
    1. Download the hourly forecast (air temperature, cloud cover, wind speed)
       for the pond's location from Open-Meteo. It is free and needs no API key.
    2. Pick out "tonight": 18:00 to 06:00. Cloud cover is taken from the DAY
       before tonight (06:00 to 18:00), because clouds matter by stopping algae
       from making oxygen in daylight; at night no oxygen is made anyway.
    3. Count the risk factors: a cloudy day, a still night, a warm night.
       0 -> Low, 1 -> Medium, 2 or 3 -> High. The numbers are in
       config/thresholds.toml ([night_crash]); the reasons are in docs/night_crash.md.
    4. Save the downloaded forecast to data/weather_cache.json. With no internet,
       the saved forecast is used instead and the answer says "offline".

This is real weather data, not simulated data. It is never used to train a model.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from statistics import mean

from backend.risk_classifier import load_thresholds

MANGALURU = {"name": {"en": "Mangaluru", "kn": "ಮಂಗಳೂರು"}, "latitude": 12.9141, "longitude": 74.8560}
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
TIMEZONE = "Asia/Kolkata"
CACHE_FILE = Path(__file__).resolve().parent.parent / "data" / "weather_cache.json"
REFRESH_MINUTES = 30        # reuse a forecast younger than this instead of downloading again
TIMEOUT_SECONDS = 8         # give up quickly with no internet; the saved forecast is used instead

LEVEL_NAMES = {
    "low":    {"en": "Low",    "kn": "ಕಡಿಮೆ"},
    "medium": {"en": "Medium", "kn": "ಮಧ್ಯಮ"},
    "high":   {"en": "High",   "kn": "ಹೆಚ್ಚು"},
}

# Words used to describe the night, in the order they are joined.
FACTOR_WORDS = {
    "cloudy": {"en": "cloudy", "kn": "ಮೋಡ ಕವಿದ"},
    "still":  {"en": "still",  "kn": "ಗಾಳಿಯಿಲ್ಲದ"},
    "warm":   {"en": "warm",   "kn": "ಸೆಖೆಯ"},
}

ADVICE = {
    "low":    {"en": "Weather looks fine tonight: low risk of an oxygen crash.",
               "kn": "ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ ಸರಿಯಾಗಿದೆ: ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯ ಕಡಿಮೆ."},
    "medium": {"en": "{night} night ahead: check the pond late at night and before dawn.",
               "kn": "{night} ರಾತ್ರಿ ಬರಲಿದೆ: ತಡರಾತ್ರಿ ಮತ್ತು ಬೆಳಗಾಗುವ ಮೊದಲು ಕೊಳವನ್ನು ನೋಡಿ."},
    "high":   {"en": "{night} night ahead: keep the aerator ready.",
               "kn": "{night} ರಾತ್ರಿ ಬರಲಿದೆ: ಏರೇಟರ್ ಸಿದ್ಧವಾಗಿಡಿ."},
}

UNAVAILABLE = {
    "en": "No internet and no saved forecast. Tonight's weather is not known.",
    "kn": "ಇಂಟರ್ನೆಟ್ ಇಲ್ಲ, ಉಳಿಸಿದ ಮುನ್ಸೂಚನೆಯೂ ಇಲ್ಲ. ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ ತಿಳಿದಿಲ್ಲ.",
}


# ----------------------------------------------------------------- download and cache

def download_forecast(latitude: float, longitude: float) -> dict:
    """Hourly forecast from Open-Meteo: yesterday, today and the next two days."""
    query = urllib.parse.urlencode({
        "latitude": latitude, "longitude": longitude,
        "hourly": "temperature_2m,cloud_cover,wind_speed_10m",
        "timezone": TIMEZONE, "past_days": 1, "forecast_days": 3,
    })
    with urllib.request.urlopen(f"{OPEN_METEO_URL}?{query}", timeout=TIMEOUT_SECONDS) as response:
        return json.load(response)


def _read_cache(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _write_cache(path: Path, saved_at: datetime, forecast: dict) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"saved_at": saved_at.isoformat(), "forecast": forecast}), encoding="utf-8")
    except OSError:
        pass                # can't save: the app still works, just without an offline copy


# ----------------------------------------------------------------- rules

def tonight_window(now: datetime) -> tuple[datetime, datetime, datetime]:
    """(day start, night start, night end). Before 06:00, "tonight" is the night we are in."""
    day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if now.hour < 6:
        day -= timedelta(days=1)
    return day + timedelta(hours=6), day + timedelta(hours=18), day + timedelta(hours=30)


def summarise(forecast: dict, now: datetime) -> dict | None:
    """Average cloud cover over the day, wind and temperature over the night. None if not in the forecast."""
    hourly = forecast["hourly"]
    day_start, night_start, night_end = tonight_window(now)
    times = [datetime.fromisoformat(t) for t in hourly["time"]]

    def values(name: str, start: datetime, end: datetime) -> list[float]:
        return [v for t, v in zip(times, hourly[name]) if start <= t < end and v is not None]

    cloud = values("cloud_cover", day_start, night_start)
    wind = values("wind_speed_10m", night_start, night_end)
    temp = values("temperature_2m", night_start, night_end)
    if len(cloud) < 6 or len(wind) < 6 or len(temp) < 6:     # need at least half of each 12 h window
        return None
    return {
        "night_start": night_start.isoformat(timespec="minutes"),
        "night_end": night_end.isoformat(timespec="minutes"),
        "day_cloud_cover_pct": round(mean(cloud)),
        "night_wind_speed_kmh": round(mean(wind), 1),
        "night_temperature_c": round(mean(temp), 1),
    }


def rate_crash_risk(cloud_pct: float, wind_kmh: float, temp_c: float, rules: dict | None = None) -> dict:
    """Low / Medium / High from the weather, with the farmer's message in English and Kannada."""
    rules = rules if rules is not None else load_thresholds()["night_crash"]
    factors = []
    if cloud_pct >= rules["cloudy_day_min_cloud_pct"]:
        factors.append("cloudy")
    if wind_kmh < rules["still_night_max_wind_kmh"]:
        factors.append("still")
    if temp_c >= rules["warm_night_min_temp_c"]:
        factors.append("warm")

    level = "low" if not factors else "medium" if len(factors) == 1 else "high"
    message = {}
    for lang in ("en", "kn"):
        night = ", ".join(FACTOR_WORDS[f][lang] for f in factors)
        if lang == "en":
            night = night[:1].upper() + night[1:]
        message[lang] = ADVICE[level][lang].format(night=night)
    return {"level": level, "level_name": LEVEL_NAMES[level], "factors": factors, "message": message}


# ----------------------------------------------------------------- what the API returns

def tonight_crash_risk(now: datetime | None = None, location: dict = MANGALURU,
                       cache_file: Path = CACHE_FILE, download=download_forecast) -> dict:
    """
    Tonight's crash risk. Tries the internet first (unless the saved forecast is
    less than 30 minutes old); with no internet, uses the saved forecast and
    sets offline = True. `download` can be swapped out in tests.
    """
    now = now or datetime.now()
    cached = _read_cache(cache_file)
    saved_at = datetime.fromisoformat(cached["saved_at"]) if cached else None
    forecast, offline = None, False

    if cached and timedelta(0) <= now - saved_at < timedelta(minutes=REFRESH_MINUTES):
        forecast = cached["forecast"]
    else:
        try:
            forecast = download(location["latitude"], location["longitude"])
            saved_at = now
            _write_cache(cache_file, saved_at, forecast)
        except Exception:                   # no internet, timeout, bad reply: fall back to the saved copy
            offline = True
            forecast = cached["forecast"] if cached else None

    result = {
        "source": "open-meteo",
        "location": location["name"],
        "offline": offline,
        "saved_at": saved_at.isoformat(timespec="minutes") if saved_at and forecast else None,
    }
    weather = summarise(forecast, now) if forecast else None
    if weather is None:                     # nothing saved, or the saved forecast doesn't reach tonight
        return {**result, "status": "unavailable", "level": None, "message": UNAVAILABLE}
    rating = rate_crash_risk(weather["day_cloud_cover_pct"], weather["night_wind_speed_kmh"],
                             weather["night_temperature_c"])
    return {**result, "status": "ok", **weather, **rating}
