"""
MeenuRaksha web server (FastAPI).

Start it from the project folder:
    uvicorn backend.main:app --reload
then open http://127.0.0.1:8000 (the page) or http://127.0.0.1:8000/docs
(interactive API documentation, generated automatically by FastAPI).

Endpoints:
    GET  /api/health                 is the server running?
    POST /api/risk                   current risk + reasons for one set of readings
    POST /api/time-to-danger         "time until danger" from recent DO readings
    GET  /api/simulator/scenarios    available demo scenarios and ponds
    GET  /api/simulator/stream       live stream of SIMULATED readings (Server-Sent Events)
    /                                the web page (files in frontend/)

The DO forecast model is deliberately NOT exposed: its typical error (±4.5 mg/L)
is wider than the whole Warning band. See docs/do_forecast.md.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Literal

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.do_features import STEP_MINUTES
from backend.risk_classifier import classify
from backend.simulator import SCENARIOS, SIMULATED, SIMULATED_LABEL, simulate_readings
from backend.time_to_danger import estimate_time_to_danger

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
STATIONS = ("station1", "station2", "station3")
HISTORY_HOURS = 2          # simulated readings generated before the stream starts, for the trend

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


class DOReading(BaseModel):
    time: datetime
    dissolved_oxygen: float | None = Field(None, description="mg/L")


class DOHistory(BaseModel):
    """Recent dissolved-oxygen readings for one pond (the last 1–2 hours is enough)."""
    readings: list[DOReading] = Field(..., min_length=1)


# ----------------------------------------------------------------- API

@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/risk")
def current_risk(readings: Readings) -> dict:
    """Safe / Warning / Danger for these readings, with the reason in English and Kannada."""
    return classify(readings.model_dump(exclude_none=True)).to_dict()


@app.post("/api/time-to-danger")
def time_to_danger(history: DOHistory) -> dict:
    """If DO has been falling, roughly when it will reach the danger level."""
    series = pd.Series({r.time: r.dissolved_oxygen for r in history.readings}, dtype="float64")
    series.index = pd.to_datetime(series.index)
    return estimate_time_to_danger(series)


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
    first_index = int(sim.index.searchsorted(first))
    steps = range(first_index, len(sim) if count is None else min(len(sim), first_index + count))

    async def events():
        for i in steps:
            row = sim.iloc[i]
            reading = row.drop("source").to_dict()
            payload = {
                "source": SIMULATED,
                "label": SIMULATED_LABEL,
                "station": station,
                "scenario": scenario,
                "time": sim.index[i].isoformat(),
                "reading": reading,
                "risk": classify(reading).to_dict(),
                "time_to_danger": estimate_time_to_danger(sim["dissolved_oxygen"].iloc[: i + 1]),
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
