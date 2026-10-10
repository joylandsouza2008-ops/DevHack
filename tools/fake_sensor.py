"""
A pretend pond sensor, for demos: sends a reading to AquaNexus every few
seconds, exactly like a real ESP32 sensor would (POST /api/sensor/{pond_id}).

Every reading it sends says demo = true, so the dashboard labels it
"Demo device: simulated readings, not a real pond". The numbers are made up
here, not measured, and must never be used to train or test the model.

Uses only Python's standard library, so it runs on any laptop.

Local server (two PowerShell windows):
    $env:SENSOR_KEY_POND1 = "my-local-test-key"
    uvicorn backend.main:app --reload
and in the second window:
    $env:SENSOR_KEY_POND1 = "my-local-test-key"
    python tools/fake_sensor.py

The live Render link (use the key you saved in Render's Environment tab):
    python tools/fake_sensor.py --url https://meenuraksha.onrender.com --key <the pond1 key>

Options:
    --pond pond2            send to another pond (its key is SENSOR_KEY_POND2)
    --scenario falling      oxygen drops a little with every reading: Safe -> Warning -> Danger
    --every 5               seconds between readings (default 5)
    --count 20              stop after 20 readings (default: run until Ctrl+C)
    --fault-every 10        every 10th reading is impossible (oxygen 0), to show "Check the sensor"
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

IST = timezone(timedelta(hours=5, minutes=30))     # India Standard Time, +05:30
DEVICE_NAME = "fake-sensor (demo)"


class FakeSensor:
    """Makes one made-up reading at a time. `scenario` is "normal" or "falling"."""

    def __init__(self, scenario: str = "normal", fault_every: int = 0, seed: int | None = None) -> None:
        if scenario not in ("normal", "falling"):
            raise ValueError("scenario must be 'normal' or 'falling'")
        self.scenario = scenario
        self.fault_every = fault_every
        self.random = random.Random(seed)
        self.step = 0

    def next_reading(self) -> dict:
        self.step += 1
        wobble = lambda size: self.random.uniform(-size, size)     # small sensor noise
        if self.scenario == "falling":
            oxygen = max(1.0, 6.5 - 0.08 * (self.step - 1)) + wobble(0.03)
        else:
            oxygen = 6.4 + wobble(0.3)
        if self.fault_every and self.step % self.fault_every == 0:
            oxygen = 0.0                                         # a dead probe: the server must refuse it
        return {
            "timestamp": datetime.now(IST).isoformat(timespec="seconds"),
            "dissolved_oxygen": round(oxygen, 2),
            "ph": round(7.5 + wobble(0.1), 2),
            "temperature": round(29.0 + wobble(0.3), 1),
            "ammonia": round(0.25 + wobble(0.03), 3),
            "device": DEVICE_NAME,
            "demo": True,
        }


def send(base_url: str, pond: str, key: str, reading: dict, opener=urlopen, timeout: float = 70):
    """POST one reading. Returns (HTTP status, reply as a dictionary).
    The long timeout lets a sleeping free Render server wake up (about 1 minute)."""
    request = Request(f"{base_url.rstrip('/')}/api/sensor/{pond}", method="POST",
                      data=json.dumps(reading).encode("utf-8"),
                      headers={"Content-Type": "application/json", "X-Sensor-Key": key})
    try:
        with opener(request, timeout=timeout) as response:
            return response.status, json.loads(response.read() or b"{}")
    except HTTPError as error:              # the server answered, but refused the reading
        try:
            return error.code, json.loads(error.read() or b"{}")
        except ValueError:
            return error.code, {}


def describe(status: int, reply: dict) -> str:
    if status == 201:
        return f"accepted: {reply['level'].upper()} - {reply['summary']['en']}"
    message = reply.get("message", {})
    text = message.get("en", "") if isinstance(message, dict) else ""
    details = " ".join(e["message"]["en"] for e in reply.get("sensor_errors", []) if e.get("message"))
    return f"REFUSED ({status}): {text} {details}".strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pretend pond sensor (demo device) for AquaNexus.")
    parser.add_argument("--url", default="http://127.0.0.1:8000", help="server address")
    parser.add_argument("--pond", default="pond1", choices=["pond1", "pond2", "pond3"])
    parser.add_argument("--key", help="the pond's sensor key (default: the SENSOR_KEY_POND1 / _POND2 / _POND3 variable)")
    parser.add_argument("--scenario", default="normal", choices=["normal", "falling"])
    parser.add_argument("--every", type=float, default=5.0, help="seconds between readings")
    parser.add_argument("--count", type=int, help="stop after this many readings")
    parser.add_argument("--fault-every", type=int, default=0, help="send an impossible reading every N readings")
    args = parser.parse_args(argv)

    key = args.key or os.environ.get(f"SENSOR_KEY_{args.pond.upper()}")
    if not key:
        print(f"No key. Use --key, or set SENSOR_KEY_{args.pond.upper()} first.", file=sys.stderr)
        return 2

    device = FakeSensor(args.scenario, args.fault_every)
    print(f"DEMO DEVICE (simulated readings, not a real pond) -> {args.url} {args.pond}, "
          f"every {args.every:g} s. Ctrl+C to stop.")
    sent = 0
    try:
        while args.count is None or sent < args.count:
            reading = device.next_reading()
            values = (f"DO {reading['dissolved_oxygen']}  pH {reading['ph']}  "
                      f"{reading['temperature']} °C  ammonia {reading['ammonia']}")
            try:
                print(f"{reading['timestamp'][11:19]}  {values}  ->  {describe(*send(args.url, args.pond, key, reading))}")
            except (URLError, TimeoutError, ConnectionError) as error:
                print(f"{reading['timestamp'][11:19]}  could not reach the server ({error}). Trying again.")
            sent += 1
            if args.count is None or sent < args.count:
                time.sleep(args.every)
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
