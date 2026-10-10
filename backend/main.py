"""
MeenuRaksha web server (FastAPI).

Start it from the project folder:
    uvicorn backend.main:app --reload
then open http://127.0.0.1:8000 (the page) or http://127.0.0.1:8000/docs
(interactive API documentation, generated automatically by FastAPI).

Endpoints:
    GET  /api/health                 is the server running?
    POST /api/risk                   current risk + reasons + action checklist + health score for one set of readings
    POST /api/manual                 the same for readings typed in from a test kit (marked "manual")
    POST /api/time-to-danger         "time until danger" from recent DO readings
    GET  /api/simulator/scenarios    available demo scenarios and ponds
    GET  /api/simulator/stream       live stream of SIMULATED readings (Server-Sent Events)
    GET  /api/diseases               the fish disease guide (library, signs, sources)
    POST /api/diseases/check         "possible matches" for the signs a farmer ticked (never a diagnosis)
    POST /api/assistant/suggestions  "Ask MeenuRaksha": suggested questions with ready answers (no AI)
    POST /api/assistant/ask          "Ask MeenuRaksha": one question, answered only from the app's content
    GET  /api/weather/tonight        tonight's oxygen crash risk from the real weather forecast
    POST /api/sensor/{pond_id}       one reading from a REAL pond sensor (needs the pond's key)
    GET  /api/sensor/{pond_id}       the latest live-sensor reading for a pond
    GET  /api/sensor/{pond_id}/stream  live-sensor readings as they arrive (Server-Sent Events)
    /                                the web page (files in frontend/)

The DO forecast model is deliberately NOT exposed: its typical error (±4.5 mg/L)
is wider than the whole Warning band. See docs/do_forecast.md.
"""

from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import pandas as pd
from fastapi import FastAPI, Header, HTTPException, Query, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend import assistant, diseases, sensor
from backend.actions import checklist
from backend.ai_provider import provider_from_env
from backend.alerts import POND_NAMES, compose_alert
from backend.do_features import STEP_MINUTES
from backend.health_score import health_score
from backend.risk_classifier import classify
from backend.simulator import SCENARIOS, SIMULATED, SIMULATED_LABEL, simulate_readings
from backend.time_to_danger import estimate_time_to_danger
from backend.weather import tonight_crash_risk

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
STATIONS = ("station1", "station2", "station3")
HISTORY_HOURS = 2          # simulated readings generated before the stream starts, for the trend

# Readings a farmer types in from a test kit. Always shown with this label,
# so they are never confused with simulated readings.
MANUAL = "manual"
MANUAL_LABEL = {"en": "Manual test-kit reading", "kn": "ಕೈಯಿಂದ ನಮೂದಿಸಿದ ಟೆಸ್ಟ್ ಕಿಟ್ ಅಳತೆ"}

app = FastAPI(title="MeenuRaksha API",
              description="Pond water-quality early warning for small aquaculture farmers.")


# ----------------------------------------------------------------- request shapes

class Readings(BaseModel):
    """One set of sensor readings. Leave out anything not measured."""
    dissolved_oxygen: float | None = Field(None, description="mg/L", examples=[4.1])
    ph: float | None = Field(None, examples=[7.2])
    temperature: float | None = Field(None, description="°C", examples=[29.0])
    ammonia: float | None = Field(None, description="mg/L total ammonia", examples=[0.05])
    nitrate: float | None = Field(None, description="mg/L NO3", examples=[20.0])
    turbidity: float | None = Field(None, description="sensor units, information only", examples=[30.0])


class TestKitReadings(BaseModel):
    """Readings typed in from a cheap pond test kit. Leave out anything not tested."""
    dissolved_oxygen: float | None = Field(None, description="mg/L", examples=[4.5])
    ph: float | None = Field(None, examples=[7.5])
    temperature: float | None = Field(None, description="°C", examples=[29.0])
    ammonia: float | None = Field(None, description="mg/L total ammonia", examples=[0.5])


class SensorReading(BaseModel):
    """
    One reading from a real pond sensor. `timestamp` is when the sensor
    measured it, with a time zone (e.g. 2026-10-10T21:30:00+05:30). Leave out
    any probe the sensor doesn't have, but send at least one value.
    """
    timestamp: datetime = Field(..., examples=["2026-10-10T21:30:00+05:30"])
    dissolved_oxygen: float | None = Field(None, description="mg/L", examples=[5.8])
    ph: float | None = Field(None, examples=[7.4])
    temperature: float | None = Field(None, description="°C", examples=[29.5])
    ammonia: float | None = Field(None, description="mg/L total ammonia", examples=[0.3])
    device: str | None = Field(None, max_length=40, description="optional name, e.g. esp32-pond1")
    demo: bool = Field(False, description="true for a demo device that sends made-up readings")


class SignsSeen(BaseModel):
    """Signs the farmer ticked in the symptom checker (ids from GET /api/diseases)."""
    signs: list[str] = Field(..., max_length=50, examples=[["white_spots", "rubbing"]])


class PageReadings(BaseModel):
    """The readings the page is showing right now (the server grades them again itself)."""
    station: Literal["station1", "station2", "station3"] = "station1"
    simulated: Readings | None = None
    manual: Readings | None = None
    live_sensor: Readings | None = None


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., max_length=1500)


class Question(PageReadings):
    """One question for "Ask MeenuRaksha"."""
    question: str = Field(..., min_length=1, max_length=500)
    lang: Literal["en", "kn"] = "kn"
    history: list[ChatMessage] = Field(default_factory=list, max_length=8)


class DOReading(BaseModel):
    time: datetime
    dissolved_oxygen: float | None = Field(None, description="mg/L")


class DOHistory(BaseModel):
    """Recent dissolved-oxygen readings for one pond (the last 1–2 hours is enough)."""
    readings: list[DOReading] = Field(..., min_length=1)


# ----------------------------------------------------------------- API

def assess(reading: dict, source: str = "sensor") -> dict:
    """Risk result plus the action checklist (empty when Safe), the 0–100 health score
    and the diseases this reading makes more likely (backend/diseases.py)."""
    risk = classify(reading, source=source).to_dict()
    risk["actions"] = checklist(risk)
    risk["health_score"] = health_score(risk)
    risk["likely_diseases"] = diseases.likely_diseases(risk)
    return risk


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/risk")
def current_risk(readings: Readings) -> dict:
    """Safe / Warning / Danger for these readings, with the reason in English and Kannada."""
    return assess(readings.model_dump(exclude_none=True))


@app.post("/api/manual")
def manual_reading(readings: TestKitReadings) -> dict:
    """
    Readings from a test kit, graded by the same classifier. Impossible values
    say "check your test kit". Marked source = "manual" with its own label.
    """
    values = readings.model_dump(exclude_none=True)
    if not values:
        raise HTTPException(status_code=422, detail="Enter at least one reading.")
    risk = assess(values, source=MANUAL)
    return {
        "source": MANUAL,
        "label": MANUAL_LABEL,
        "time": datetime.now().isoformat(timespec="minutes"),
        "reading": values,
        "risk": risk,
        "alert": compose_alert(risk, label=MANUAL_LABEL),
    }


@app.get("/api/diseases")
def disease_guide() -> dict:
    """The fish disease guide: diseases, the signs to tick, and the sources. No medicines or doses."""
    return diseases.library()


@app.post("/api/diseases/check")
def disease_check(seen: SignsSeen) -> dict:
    """Possible matches for the ticked signs. Never a diagnosis: always says to confirm with a fisheries officer."""
    return diseases.check(seen.signs)


# ----------------------------------------------------------------- "Ask MeenuRaksha" assistant
# The AI is called from here only; its provider and key come from environment
# variables (backend/ai_provider.py). Safety rules: backend/assistant.py.

assistant_limiter = assistant.RateLimiter()


def _visitor(request: Request) -> str:
    """Who is asking, for the per-visitor rate limit. Render puts the visitor's address first in
    X-Forwarded-For. It can be faked, which is why there is also a daily total for everyone."""
    forwarded = request.headers.get("x-forwarded-for", "")
    return forwarded.split(",")[0].strip() or (request.client.host if request.client else "unknown")


def _evaluate(page: PageReadings) -> list[dict]:
    readings = {source: getattr(page, source).model_dump(exclude_none=True) if getattr(page, source) else None
                for source in ("simulated", "manual", "live_sensor")}
    return assistant.evaluate(readings, page.station, assess)


@app.post("/api/assistant/suggestions")
def assistant_suggestions(page: PageReadings) -> dict:
    """Suggested questions with ready answers built from the app's content. Never calls the AI."""
    evals = _evaluate(page)
    return {"label": assistant.LABEL, "ai_available": provider_from_env() is not None,
            "used": [e["source"] for e in evals],
            "suggestions": assistant.suggestions(evals, tonight_crash_risk())}


@app.post("/api/assistant/ask")
def assistant_ask(question: Question, request: Request) -> dict:
    """
    One question, answered only from the app's content, in English or Kannada.
    No key, an error or the rate limit -> mode "offline" / "limited" plus the
    suggested questions with ready answers, so the page always has something to show.
    """
    evals = _evaluate(question)
    weather = tonight_crash_risk()
    result = assistant.ask(question.question, question.lang, evals, weather, provider_from_env(),
                           assistant_limiter, _visitor(request), [m.model_dump() for m in question.history])
    result.update(label=assistant.LABEL, used=[e["source"] for e in evals])
    if result["text"] is None:
        result["suggestions"] = assistant.suggestions(evals, weather)
    return result


@app.post("/api/time-to-danger")
def time_to_danger(history: DOHistory) -> dict:
    """If DO has been falling, roughly when it will reach the danger level."""
    series = pd.Series({r.time: r.dissolved_oxygen for r in history.readings}, dtype="float64")
    series.index = pd.to_datetime(series.index)
    return estimate_time_to_danger(series)


@app.get("/api/weather/tonight")
def weather_tonight() -> dict:
    """
    Tonight's oxygen crash risk (Low / Medium / High) for Mangaluru, from the
    Open-Meteo forecast. With no internet it uses the last saved forecast and
    says offline = true. A plain `def` (not async) so a slow download never
    blocks the simulator stream.
    """
    return tonight_crash_risk()


# ----------------------------------------------------------------- live sensor
# A real sensor POSTs here with its pond's key in the X-Sensor-Key header.
# Readings are kept in memory only (backend/sensor.py). See docs/sensor-api.md.

SENSOR_VALUES = {"dissolved_oxygen", "ph", "temperature", "ammonia"}
PondId = Literal["pond1", "pond2", "pond3"]
SENSOR_CHECK_SECONDS = 0.5     # how often the dashboard stream looks for a new reading
SENSOR_PING_SECONDS = 15       # keep-alive, so proxies don't close a quiet stream


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _refuse(status: int, pond_id: str, error: str, message: dict,
            details: list | None = None, show_on_dashboard: bool = True) -> JSONResponse:
    """Tell the sensor clearly why its reading was refused (and show bad readings on the dashboard)."""
    body = {"accepted": False, "error": error, "message": message, "sensor_errors": details or []}
    if show_on_dashboard:
        sensor.store.reject(pond_id, {**body, "received_at": _now().isoformat(timespec="seconds")})
    return JSONResponse(status_code=status, content=body)


@app.post("/api/sensor/{pond_id}", status_code=201)
def sensor_reading(reading: SensorReading, pond_id: PondId,
                   x_sensor_key: str | None = Header(None, description="this pond's secret key")):
    """
    One reading from a real pond sensor (pond_id: pond1, pond2 or pond3).
    Needs the pond's key in the `X-Sensor-Key` header; the server compares it
    with the SENSOR_KEY_POND1 / _POND2 / _POND3 environment variable.
    Impossible values are refused with "Check the sensor" and nothing is stored.
    """
    expected = sensor.sensor_key(pond_id)
    if expected is None:
        variable = sensor.key_variable(pond_id)
        return _refuse(503, pond_id, "not_set_up",
                       {"en": f"No sensor key is set on the server for {pond_id} ({variable}).",
                        "kn": f"{pond_id} ಗಾಗಿ ಸರ್ವರ್‌ನಲ್ಲಿ ಸೆನ್ಸರ್ ಕೀ ಹೊಂದಿಸಿಲ್ಲ ({variable})."},
                       show_on_dashboard=False)
    if not sensor.key_matches(x_sensor_key, expected):
        # Not shown on the dashboard: someone guessing keys must not change what farmers see.
        return _refuse(401, pond_id, "wrong_key", sensor.WRONG_KEY, show_on_dashboard=False)

    values = reading.model_dump(include=SENSOR_VALUES, exclude_none=True)
    if not values:
        return _refuse(422, pond_id, "no_values", sensor.NO_VALUES)
    clock_problem = sensor.check_timestamp(reading.timestamp, _now())
    if clock_problem:
        return _refuse(422, pond_id, "bad_timestamp", clock_problem)

    # NaN / Infinity (a broken probe) would otherwise count as "not measured".
    broken = sensor.not_a_number_errors(values)
    if broken:
        return _refuse(422, pond_id, "check_the_sensor", sensor.REJECTED, broken)
    risk = assess(values, source="sensor")
    if risk["sensor_errors"]:
        # One impossible value means the whole reading can't be trusted.
        return _refuse(422, pond_id, "check_the_sensor", sensor.REJECTED, risk["sensor_errors"])

    entry = {
        "source": sensor.SOURCE,
        "label": sensor.LIVE_LABEL,
        "demo": reading.demo,
        "demo_label": sensor.DEMO_LABEL if reading.demo else None,
        "pond_id": pond_id,
        "station": pond_id.replace("pond", "station"),     # same pond names as the simulator
        "device": reading.device,
        "time": reading.timestamp.isoformat(),
        "received_at": _now().isoformat(timespec="seconds"),
        "reading": values,
        "risk": risk,
        # Preview only: no real SMS or WhatsApp message is sent.
        "alert": compose_alert(risk, label=sensor.DEMO_LABEL if reading.demo else sensor.LIVE_LABEL,
                               pond=sensor.SENSOR_PONDS[pond_id]),
    }
    sensor.store.add(pond_id, entry)
    return {"accepted": True, "level": risk["level"], "summary": risk["summary"],
            "received_at": entry["received_at"]}


def _sensor_state(pond_id: str) -> tuple[int, dict]:
    """(version, what the dashboard needs to show this pond's live sensor)."""
    version, latest, rejected = sensor.store.snapshot(pond_id)
    return version, {
        "pond_id": pond_id,
        "pond": sensor.SENSOR_PONDS[pond_id],
        "source": sensor.SOURCE,
        "label": sensor.LIVE_LABEL,
        "server_time": _now().isoformat(timespec="seconds"),
        "latest": latest,          # None until the sensor sends its first good reading
        "rejected": rejected,      # the last refused reading; cleared by the next good one
    }


@app.get("/api/sensor/{pond_id}")
def sensor_latest(pond_id: PondId) -> dict:
    """This pond's latest live-sensor reading (latest = null if none since the server started)."""
    return _sensor_state(pond_id)[1]


@app.get("/api/sensor/{pond_id}/stream")
async def sensor_stream(
    pond_id: PondId,
    seconds: float | None = Query(None, ge=0, description="close the stream after this many seconds (for tests)"),
):
    """
    Server-Sent Events for the dashboard: a `sensor` event straight away with
    the current state, another each time this pond's sensor sends a reading
    (good or refused), and a `ping` with the server time every 15 s.
    """
    async def events():
        started = last_ping = time.monotonic()
        sent = None
        while True:
            if sensor.store.version(pond_id) != sent:
                sent, state = _sensor_state(pond_id)
                yield f"event: sensor\ndata: {json.dumps(state, ensure_ascii=False)}\n\n"
            elif time.monotonic() - last_ping >= SENSOR_PING_SECONDS:
                last_ping = time.monotonic()
                yield f"event: ping\ndata: {json.dumps({'server_time': _now().isoformat(timespec='seconds')})}\n\n"
            if seconds is not None and time.monotonic() - started >= seconds:
                yield "event: end\ndata: {}\n\n"
                return
            await asyncio.sleep(SENSOR_CHECK_SECONDS)

    return StreamingResponse(events(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache"})


@app.get("/api/simulator/scenarios")
def scenarios() -> dict:
    return {"scenarios": list(SCENARIOS), "stations": list(STATIONS),
            "source": SIMULATED, "label": SIMULATED_LABEL}


def _default_start(scenario: str) -> pd.Timestamp:
    """Normal: start now. Crash: start at 18:00 today so the night arrives quickly in the demo."""
    now = pd.Timestamp.now().floor(f"{STEP_MINUTES}min")
    return now.normalize() + pd.Timedelta(hours=18) if scenario == "oxygen_crash" else now


@app.get("/api/simulator/stream")
async def simulator_stream(
    station: Literal["station1", "station2", "station3"] = "station1",
    scenario: Literal["normal", "oxygen_crash"] = "normal",
    start: datetime | None = Query(None, description="simulated start time (default depends on scenario)"),
    hours: int = Query(36, ge=1, le=72, description="simulated hours to play"),
    interval: float = Query(1.0, ge=0, le=10, description="real seconds between readings"),
    count: int | None = Query(None, ge=1, description="stop after this many readings (for tests)"),
    skip: int = Query(0, ge=0, description="readings to skip, to resume a paused demo with the same `start`"),
    seed: int = 0,
):
    """
    Server-Sent Events stream of SIMULATED readings, one every `interval`
    seconds, each 20 simulated minutes apart. Every event carries
    source = "simulated" and the "Simulated data" label: the page must show it.
    """
    first = pd.Timestamp(start) if start else _default_start(scenario)
    history_start = first - pd.Timedelta(hours=HISTORY_HOURS)
    try:
        # Start the simulation 2 h early so "time until danger" has a trend from the first reading.
        sim = simulate_readings(station, start=history_start, hours=hours + HISTORY_HOURS,
                                scenario=scenario, seed=seed)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    # The scenario (e.g. when the night crash happens) depends on `start`, so a
    # resumed demo keeps the same `start` and skips the readings already shown.
    first_index = int(sim.index.searchsorted(first)) + skip
    steps = range(first_index, len(sim) if count is None else min(len(sim), first_index + count))

    async def events():
        for i in steps:
            row = sim.iloc[i]
            reading = row.drop("source").to_dict()
            risk = assess(reading)
            ttd = estimate_time_to_danger(sim["dissolved_oxygen"].iloc[: i + 1])
            payload = {
                "source": SIMULATED,
                "label": SIMULATED_LABEL,
                "station": station,
                "scenario": scenario,
                "time": sim.index[i].isoformat(),
                "reading": reading,
                "risk": risk,
                "time_to_danger": ttd,
                # Preview only: no real SMS or WhatsApp message is sent.
                "alert": compose_alert(risk, ttd, SIMULATED_LABEL, POND_NAMES[station]),
            }
            yield f"event: reading\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"
            if interval:
                await asyncio.sleep(interval)
        yield "event: end\ndata: {}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache"})


# ----------------------------------------------------------------- web page
# Mounted last so /api/... routes take priority. html=True serves index.html at "/".
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
