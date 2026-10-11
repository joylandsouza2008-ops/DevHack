"""
A pretend pond sensor, for demos: sends readings to AquaNexus exactly like a
real ESP32 sensor would (POST /api/sensor/{pond_id or device_id}).

Every reading it sends says demo = true, so the app labels it "Simulated
data" / "Demo device: simulated readings, not a real pond". The numbers are
made up here, not measured, and must never be used to train or test the model.

Uses only Python's standard library, so it runs on any laptop.

1. SEVERAL LIVE PONDS ("My ponds", for the demo video)
   Copy your farm code from the app (More page, "My farm code"), then:
       python tools/fake_sensor.py --farm-code K7QM-3XRP-9TFD --devices 3
   This adds 3 ponds to that farm ("Demo pond 1" ...), connects a device to
   each, and sends a reading from every device every 30 seconds. Demo pond 1
   has a night oxygen crash (sped up: Danger in about 5 minutes). The keys stay
   in this program's memory; they are never printed or saved.
   Devices you already connected in the app:
       python tools/fake_sensor.py --device dev-k7qm3xrp9t:<its key> --device dev-...:<key>

2. THE DEMO DASHBOARD'S LIVE SENSOR CARD (pond1 / pond2 / pond3)
   Local server (two PowerShell windows):
       $env:SENSOR_KEY_POND1 = "my-local-test-key"
       uvicorn backend.main:app --reload
   and in the second window:
       $env:SENSOR_KEY_POND1 = "my-local-test-key"
       python tools/fake_sensor.py
   The live Render link:
       python tools/fake_sensor.py --url https://meenuraksha.onrender.com --key <the pond1 key>

Options:
    --url URL               server address (default http://127.0.0.1:8000)
    --pond pond2            send to another demo pond (its key is SENSOR_KEY_POND2)
    --scenario falling      oxygen drops a little with every reading: Safe -> Warning -> Danger
    --every 5               seconds between readings (default 5; 30 with --devices / --device)
    --count 20              stop after 20 rounds of readings (default: run until Ctrl+C)
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
SCENARIOS = ("normal", "falling", "night_crash")
DEVICE_EVERY = 30                                   # the server accepts one reading per device every 30 s


class FakeSensor:
    """
    Makes one made-up reading at a time. Scenarios:
      normal       steady, healthy pond
      falling      oxygen drops slowly with every reading
      night_crash  a night oxygen crash, sped up: Safe for 3 readings, then oxygen falls
                   fast (Warning after about 6 readings, Danger after about 10) and the water warms
    """

    def __init__(self, scenario: str = "normal", fault_every: int = 0, seed: int | None = None) -> None:
        if scenario not in SCENARIOS:
            raise ValueError(f"scenario must be one of {', '.join(SCENARIOS)}")
        self.scenario = scenario
        self.fault_every = fault_every
        self.random = random.Random(seed)
        self.step = 0

    def next_reading(self) -> dict:
        self.step += 1
        wobble = lambda size: self.random.uniform(-size, size)     # small sensor noise
        temperature = 29.0 + wobble(0.3)
        if self.scenario == "falling":
            oxygen = max(1.0, 6.5 - 0.08 * (self.step - 1)) + wobble(0.03)
        elif self.scenario == "night_crash":
            oxygen = max(1.5, 6.4 - 0.55 * max(0, self.step - 3)) + wobble(0.05)
            temperature = min(31.5, 29.0 + 0.15 * self.step) + wobble(0.1)
        else:
            oxygen = 6.4 + wobble(0.3)
        if self.fault_every and self.step % self.fault_every == 0:
            oxygen = 0.0                                         # a dead probe: the server must refuse it
        return {
            "timestamp": datetime.now(IST).isoformat(timespec="seconds"),
            "dissolved_oxygen": round(oxygen, 2),
            "ph": round(7.5 + wobble(0.1), 2),
            "temperature": round(temperature, 1),
            "ammonia": round(0.25 + wobble(0.03), 3),
            "device": DEVICE_NAME,
            "demo": True,
        }


def device_reading(reading: dict, rng: random.Random) -> dict:
    """A pond device can also send turbidity and salinity (information only)."""
    return {**reading, "turbidity": round(30 + rng.uniform(-3, 3), 1), "salinity": round(1.5 + rng.uniform(-0.1, 0.1), 2)}


def call(base_url: str, method: str, path: str, body: dict | None = None, headers: dict | None = None,
         opener=urlopen, timeout: float = 70):
    """One request. Returns (HTTP status, reply as a dictionary).
    The long timeout lets a sleeping free Render server wake up (about 1 minute)."""
    request = Request(f"{base_url.rstrip('/')}{path}", method=method,
                      data=json.dumps(body).encode("utf-8") if body is not None else None,
                      headers={"Content-Type": "application/json", **(headers or {})})
    try:
        with opener(request, timeout=timeout) as response:
            return response.status, json.loads(response.read() or b"{}")
    except HTTPError as error:              # the server answered, but refused
        try:
            return error.code, json.loads(error.read() or b"{}")
        except ValueError:
            return error.code, {}


def send(base_url: str, pond: str, key: str, reading: dict, opener=urlopen, timeout: float = 70):
    """POST one reading to /api/sensor/{pond} (pond1..3 or a device id)."""
    return call(base_url, "POST", f"/api/sensor/{pond}", reading, {"X-Sensor-Key": key}, opener, timeout)


def setup_demo_ponds(base_url: str, farm_code: str, count: int, opener=urlopen) -> list[dict]:
    """Add `count` demo ponds to the farm and connect a device to each.
    Returns [{"name", "pond_id", "device_id", "key", "scenario"}]. Demo pond 1 gets the night crash."""
    made = []
    farm = {"X-Farm-Code": farm_code}
    for n in range(1, count + 1):
        scenario = "night_crash" if n == 1 else "normal"
        name = f"Demo pond {n}"
        status, pond = call(base_url, "POST", "/api/ponds", {"pond_name": name, "fish": "Rohu, catla (demo)"},
                            farm, opener)
        if status != 201:
            raise RuntimeError(f"could not add {name} ({status}): {pond.get('message', {}).get('en', pond)}")
        status, device = call(base_url, "POST", f"/api/ponds/{pond['id']}/device", None, farm, opener)
        if status != 201:
            raise RuntimeError(f"could not connect a device to {name} ({status})")
        made.append({"name": name, "pond_id": pond["id"], "device_id": device["device_id"],
                     "key": device["key"], "scenario": scenario})
    return made


def describe(status: int, reply: dict) -> str:
    if status == 201:
        return f"accepted: {reply['level'].upper()} - {reply['summary']['en']}"
    message = reply.get("message", {})
    text = message.get("en", "") if isinstance(message, dict) else ""
    details = " ".join(e["message"]["en"] for e in reply.get("sensor_errors", []) if e.get("message"))
    return f"REFUSED ({status}): {text} {details}".strip()


def run_devices(args, devices: list[dict]) -> int:
    """Send one reading from every device, every `args.every` seconds."""
    rng = random.Random()
    sensors = [FakeSensor(d["scenario"], args.fault_every) for d in devices]
    every = args.every if args.every is not None else DEVICE_EVERY
    print(f"DEMO DEVICES (simulated readings, not real ponds) -> {args.url}, every {every:g} s. Ctrl+C to stop.")
    for d in devices:
        print(f"  {d['name']}: device {d['device_id']} ({d['scenario'].replace('_', ' ')})")
    rounds = 0
    try:
        while args.count is None or rounds < args.count:
            for d, sensor in zip(devices, sensors):
                reading = device_reading(sensor.next_reading(), rng)
                try:
                    result = describe(*send(args.url, d["device_id"], d["key"], reading))
                except (URLError, TimeoutError, ConnectionError) as error:
                    result = f"could not reach the server ({error}). Trying again."
                print(f"{reading['timestamp'][11:19]}  {d['name']:<12} DO {reading['dissolved_oxygen']:<5} -> {result}")
            rounds += 1
            if args.count is None or rounds < args.count:
                time.sleep(every)
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pretend pond sensor (demo device) for AquaNexus.")
    parser.add_argument("--url", default="http://127.0.0.1:8000", help="server address")
    parser.add_argument("--pond", default="pond1", choices=["pond1", "pond2", "pond3"])
    parser.add_argument("--key", help="the pond's sensor key (default: the SENSOR_KEY_POND1 / _POND2 / _POND3 variable)")
    parser.add_argument("--scenario", default="normal", choices=list(SCENARIOS))
    parser.add_argument("--every", type=float, default=None,
                        help=f"seconds between readings (default 5; {DEVICE_EVERY} for My ponds devices)")
    parser.add_argument("--count", type=int, help="stop after this many rounds of readings")
    parser.add_argument("--fault-every", type=int, default=0, help="send an impossible reading every N readings")
    parser.add_argument("--farm-code", help="My ponds: your farm code (More page in the app)")
    parser.add_argument("--devices", type=int, help="My ponds: add this many demo ponds with a device each")
    parser.add_argument("--device", action="append", default=[], metavar="ID:KEY",
                        help="My ponds: an existing device id and its key (repeat for several)")
    args = parser.parse_args(argv)

    if args.devices or args.device:
        devices = []
        if args.devices:
            if not args.farm_code:
                print("--devices needs --farm-code (copy it from the app: More page, My farm code).", file=sys.stderr)
                return 2
            try:
                devices += setup_demo_ponds(args.url, args.farm_code, args.devices)
            except (RuntimeError, URLError, TimeoutError, ConnectionError) as error:
                print(f"Could not set up the demo ponds: {error}", file=sys.stderr)
                return 1
        for n, pair in enumerate(args.device, 1):
            device_id, _, key = pair.partition(":")
            if not key:
                print(f"--device needs ID:KEY, got {pair!r}", file=sys.stderr)
                return 2
            devices.append({"name": f"Device {n}", "device_id": device_id, "key": key,
                            "scenario": "night_crash" if n == 1 and not args.devices else args.scenario})
        return run_devices(args, devices)

    key = args.key or os.environ.get(f"SENSOR_KEY_{args.pond.upper()}")
    if not key:
        print(f"No key. Use --key, or set SENSOR_KEY_{args.pond.upper()} first.", file=sys.stderr)
        return 2
    every = args.every if args.every is not None else 5.0
    device = FakeSensor(args.scenario, args.fault_every)
    print(f"DEMO DEVICE (simulated readings, not a real pond) -> {args.url} {args.pond}, "
          f"every {every:g} s. Ctrl+C to stop.")
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
                time.sleep(every)
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
