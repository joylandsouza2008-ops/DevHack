"""
Tests for "My ponds and devices" (backend/ponds.py, backend/db.py and the
/api/ponds and /api/sensor/{device_id} endpoints in backend/main.py):
add / edit / delete ponds, connect a device, wrong keys, the rate limit,
offline status, the worst pond, alerts per pond, storage modes, the demo
devices in tools/fake_sensor.py and the Kannada labels.

Every test gets an empty in-memory database (tests/conftest.py). The clock is
faked where time matters. No internet, no real database server.

Run from the project folder with:   python -m pytest tests/test_ponds.py -v
"""

import io
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError

import pytest
from fastapi.testclient import TestClient

import backend.main as main
from backend import db, ponds
from tools import fake_sensor

client = TestClient(main.app)
ROOT = Path(__file__).resolve().parent.parent
KANNADA = re.compile("[ಀ-೿]")
T0 = datetime(2026, 10, 11, 2, 0, tzinfo=timezone.utc)


@pytest.fixture
def clock(monkeypatch):
    """A clock the test moves by hand: clock.now, clock.move(seconds=...)."""
    class Clock:
        now = T0

        def move(self, **delta):
            self.now += timedelta(**delta)
    c = Clock()
    monkeypatch.setattr(main, "_now", lambda: c.now)
    return c


def farm(code=None):
    return {"X-Farm-Code": code or ponds.new_farm_code()}


def add(headers, name="Pond near road", **extra):
    r = client.post("/api/ponds", json={"pond_name": name, **extra}, headers=headers)
    assert r.status_code == 201, r.text
    return r.json()


def connect(headers, pond_id):
    r = client.post(f"/api/ponds/{pond_id}/device", headers=headers)
    assert r.status_code == 201, r.text
    return r.json()


def reading(clock, **values):
    return {"timestamp": clock.now.isoformat(), **(values or {"dissolved_oxygen": 6.4, "ph": 7.4, "temperature": 29})}


def send(device, body, key=None):
    return client.post(f"/api/sensor/{device['device_id']}", json=body,
                       headers={"X-Sensor-Key": device["key"] if key is None else key})


def listing(headers):
    r = client.get("/api/ponds", headers=headers)
    assert r.status_code == 200, r.text
    return r.json()


# ----------------------------------------------------------------- farm codes

def test_farm_codes_are_long_random_and_forgiving_to_type():
    code = ponds.new_farm_code()
    assert re.fullmatch(r"[0-9A-HJKMNP-TV-Z]{4}-[0-9A-HJKMNP-TV-Z]{4}-[0-9A-HJKMNP-TV-Z]{4}", code)
    assert len({ponds.new_farm_code() for _ in range(200)}) == 200
    assert ponds.normalize_farm_code("k7qm 3xrp-9tfd") == "K7QM3XRP9TFD"
    assert ponds.normalize_farm_code("K7QM-3XRP-9TFO") == "K7QM3XRP9TF0"          # O typed for 0
    for bad in (None, "", "short", "K7QM-3XRP-9TFD-EXTRA", "K7QM-3XRP-9TF!", "UUUU-UUUU-UUUU"):
        assert ponds.normalize_farm_code(bad) is None, bad


def test_missing_or_bad_farm_code_is_refused():
    assert client.get("/api/ponds").status_code == 400
    assert client.get("/api/ponds", headers={"X-Farm-Code": "not-a-code"}).status_code == 400
    assert client.post("/api/ponds", json={"pond_name": "x"}).status_code == 400


def test_the_server_never_stores_the_farm_code():
    h = farm("K7QM-3XRP-9TFD")
    add(h)
    dump = json.dumps(main.farms().db.query("SELECT * FROM farms") + main.farms().db.query("SELECT * FROM ponds"))
    assert "K7QM" not in dump and ponds.farm_id("K7QM3XRP9TFD") in dump


# ----------------------------------------------------------------- add, edit, delete

def test_add_list_edit_and_delete_a_pond(clock):
    h = farm()
    pond = add(h, "Pond near road", size="0.5 acre", fish="Rohu")
    assert re.fullmatch(r"p-[a-z0-9]{10}", pond["id"])
    assert (pond["name"], pond["size"], pond["fish"], pond["level"], pond["device"]) == \
        ("Pond near road", "0.5 acre", "Rohu", "none", None)
    assert [p["name"] for p in listing(h)["ponds"]] == ["Pond near road"]

    r = client.patch(f"/api/ponds/{pond['id']}", json={"pond_name": "  Big   pond ", "size": "1 acre"}, headers=h)
    assert r.status_code == 200 and (r.json()["name"], r.json()["size"], r.json()["fish"]) == ("Big pond", "1 acre", "Rohu")
    r = client.patch(f"/api/ponds/{pond['id']}", json={"fish": None}, headers=h)
    assert r.json()["fish"] is None and r.json()["name"] == "Big pond"

    assert client.delete(f"/api/ponds/{pond['id']}", headers=h).json() == {"deleted": True}
    assert listing(h)["ponds"] == []
    assert client.get(f"/api/ponds/{pond['id']}", headers=h).status_code == 404


def test_deleting_a_pond_removes_its_device_readings_and_alerts(clock):
    h = farm()
    pond = add(h)
    device = connect(h, pond["id"])
    assert send(device, reading(clock, dissolved_oxygen=2.5)).status_code == 201
    client.delete(f"/api/ponds/{pond['id']}", headers=h)
    store = main.farms()
    for table in ("devices", "readings", "alerts"):
        assert store.db.query(f"SELECT * FROM {table}") == [], table
    clock.move(seconds=31)
    assert send(device, reading(clock)).status_code == 401              # its key is gone too


def test_delete_all_my_data_erases_the_whole_farm_and_nothing_else(clock):
    """DPDP 'right to erasure': More page -> Delete all my data -> DELETE /api/farm."""
    h, other = farm(), farm()
    first, second = add(h, "Pond 1"), add(h, "Pond 2")
    device = connect(h, first["id"])
    connect(h, second["id"])
    assert send(device, reading(clock, dissolved_oxygen=2.5)).status_code == 201   # a reading and a Danger alert
    kept = add(other, "Neighbour's pond")

    r = client.delete("/api/farm", headers=h)
    assert r.status_code == 200
    assert r.json() == {"deleted": {"ponds": 2, "devices": 2, "readings": 1, "alerts": 1}}

    store = main.farms()
    farm_hash = ponds.farm_id(ponds.normalize_farm_code(h["X-Farm-Code"]))
    assert store.db.query("SELECT * FROM farms WHERE id = ?", (farm_hash,)) == []
    for table in ("devices", "readings", "alerts"):
        assert store.db.query(f"SELECT * FROM {table}") == [], table
    assert listing(h)["ponds"] == [] and listing(h)["alerts"] == []
    assert [p["id"] for p in listing(other)["ponds"]] == [kept["id"]]       # another farm is untouched
    clock.move(seconds=31)
    assert send(device, reading(clock)).status_code == 401                   # device keys stop working

    # Again, or for a farm with nothing saved: fine, nothing to delete.
    assert client.delete("/api/farm", headers=h).json() == \
        {"deleted": {"ponds": 0, "devices": 0, "readings": 0, "alerts": 0}}


def test_delete_all_needs_a_farm_code():
    assert client.delete("/api/farm").status_code == 400
    assert client.delete("/api/farm", headers={"X-Farm-Code": "not-a-code"}).status_code == 400


def test_pond_names_are_checked():
    h = farm()
    assert client.post("/api/ponds", json={"pond_name": ""}, headers=h).status_code == 422
    assert client.post("/api/ponds", json={"pond_name": "x" * 41}, headers=h).status_code == 422
    assert client.post("/api/ponds", json={"pond_name": "ok", "size": "x" * 21}, headers=h).status_code == 422
    assert client.post("/api/ponds", json={"pond_name": "<script>alert(1)</script>"}, headers=h).status_code == 201


def test_a_farm_can_have_up_to_20_ponds():
    h = farm()
    for n in range(ponds.MAX_PONDS):
        main.request_limiter.clear()                # the per-minute request limit is tested elsewhere
        add(h, f"Pond {n}")
    main.request_limiter.clear()
    r = client.post("/api/ponds", json={"pond_name": "One too many"}, headers=h)
    assert r.status_code == 409 and r.json()["message"]["kn"]


def test_one_farm_can_never_see_or_change_another_farms_ponds(clock):
    mine, theirs = farm(), farm()
    pond = add(mine)
    connect(mine, pond["id"])
    assert listing(theirs)["ponds"] == []
    for method, path in (("GET", ""), ("PATCH", ""), ("DELETE", ""), ("POST", "/device"),
                         ("POST", "/device/new-key"), ("DELETE", "/device")):
        r = client.request(method, f"/api/ponds/{pond['id']}{path}", headers=theirs,
                           json={"pond_name": "hacked"} if method == "PATCH" else None)
        assert r.status_code == 404, (method, path)
    assert listing(mine)["ponds"][0]["name"] == "Pond near road"


# ----------------------------------------------------------------- devices

def test_connect_a_device_shows_the_key_once_and_stores_only_its_hash(clock):
    h = farm()
    pond = add(h)
    device = connect(h, pond["id"])
    assert re.fullmatch(r"dev-[a-z0-9]{10}", device["device_id"]) and len(device["key"]) >= 32
    assert device["endpoint"] == f"/api/sensor/{device['device_id']}" and device["header"] == "X-Sensor-Key"
    # The key never comes back, and the database holds only its hash.
    seen = json.dumps(listing(h)) + client.get(f"/api/ponds/{pond['id']}", headers=h).text
    assert device["key"] not in seen and device["device_id"] in seen
    rows = json.dumps(main.farms().db.query("SELECT * FROM devices"))
    assert device["key"] not in rows and ponds.key_hash(device["key"]) in rows
    # One device per pond.
    assert client.post(f"/api/ponds/{pond['id']}/device", headers=h).status_code == 409


def test_right_key_is_accepted_and_wrong_or_missing_keys_are_refused(clock):
    h = farm()
    device = connect(h, add(h)["id"])
    r = send(device, reading(clock))
    assert r.status_code == 201 and r.json()["accepted"] and r.json()["level"] == "safe"
    for key in ("wrong-key", device["key"][:-1], ""):
        clock.move(seconds=31)
        r = send(device, reading(clock), key=key)
        assert r.status_code == 401 and r.json()["error"] == "wrong_key", key
    r = client.post(f"/api/sensor/{device['device_id']}", json=reading(clock))      # no header at all
    assert r.status_code == 401
    r = client.post("/api/sensor/dev-0000000000", json=reading(clock), headers={"X-Sensor-Key": device["key"]})
    assert r.status_code == 401                                         # unknown device: same answer
    assert client.post("/api/sensor/dev-NOPE", json=reading(clock), headers={"X-Sensor-Key": "x"}).status_code == 422


def test_wrong_keys_never_change_what_the_farmer_sees(clock):
    h = farm()
    device = connect(h, add(h)["id"])
    send(device, reading(clock, temperature=84), key="guess")
    pond = listing(h)["ponds"][0]
    assert pond["device"]["last_error"] is None and pond["reading"] is None


def test_new_key_replaces_the_old_one_and_remove_device_stops_it(clock):
    h = farm()
    pond = add(h)
    device = connect(h, pond["id"])
    r = client.post(f"/api/ponds/{pond['id']}/device/new-key", headers=h)
    assert r.status_code == 200 and r.json()["device_id"] == device["device_id"]
    new = r.json()
    assert new["key"] != device["key"]
    assert send(device, reading(clock)).status_code == 401              # old key
    assert send(new, reading(clock)).status_code == 201                 # new key
    assert client.delete(f"/api/ponds/{pond['id']}/device", headers=h).json() == {"removed": True}
    clock.move(seconds=31)
    assert send(new, reading(clock)).status_code == 401
    assert listing(h)["ponds"][0]["device"] is None
    assert listing(h)["ponds"][0]["reading"] is not None                 # the pond keeps its readings
    assert client.delete(f"/api/ponds/{pond['id']}/device", headers=h).status_code == 404
    assert client.post(f"/api/ponds/{pond['id']}/device/new-key", headers=h).status_code == 404


def test_rate_limit_one_reading_per_device_every_30_seconds(clock):
    h = farm()
    device = connect(h, add(h)["id"])
    assert send(device, reading(clock)).status_code == 201
    clock.move(seconds=10)
    r = send(device, reading(clock))
    assert r.status_code == 429 and r.json()["error"] == "too_soon"
    assert r.headers["retry-after"] == "20" and r.json()["message"]["kn"]
    clock.move(seconds=20)
    assert send(device, reading(clock)).status_code == 201
    # A refused reading counts too, so a broken device can't flood the server.
    clock.move(seconds=30)
    assert send(device, reading(clock, temperature=84)).status_code == 422
    clock.move(seconds=5)
    assert send(device, reading(clock)).status_code == 429


def test_rate_limit_is_per_device(clock):
    h = farm()
    a, b = connect(h, add(h, "A")["id"]), connect(h, add(h, "B")["id"])
    assert send(a, reading(clock)).status_code == 201
    assert send(b, reading(clock)).status_code == 201


# ----------------------------------------------------------------- what a device can send

def test_any_of_the_six_values_can_be_sent_and_missing_values_are_fine(clock):
    h = farm()
    device = connect(h, add(h)["id"])
    body = reading(clock, dissolved_oxygen=6.1, ph=7.6, temperature=29.5, ammonia=0.2, turbidity=35, salinity=2.5)
    assert send(device, body).status_code == 201
    pond = listing(h)["ponds"][0]
    assert pond["reading"] == {"dissolved_oxygen": 6.1, "ph": 7.6, "temperature": 29.5, "ammonia": 0.2,
                               "turbidity": 35.0, "salinity": 2.5}
    detail = client.get(f"/api/ponds/{pond['id']}", headers=h).json()
    info = {p["parameter"]: p for p in detail["risk"]["info"]}
    assert set(info) == {"turbidity", "salinity"} and info["salinity"]["name"]["kn"] == "ಲವಣಾಂಶ"
    clock.move(seconds=31)
    assert send(device, reading(clock, ph=7.2)).status_code == 201       # only pH: fine
    assert listing(h)["ponds"][0]["reading"] == {"ph": 7.2}


@pytest.mark.parametrize("values", [{"temperature": 84}, {"dissolved_oxygen": 0}, {"ph": 15},
                                    {"salinity": 60}, {"turbidity": 5000}, {"ph": 7.4, "temperature": 84}])
def test_impossible_values_are_refused_and_nothing_is_stored(clock, values):
    h = farm()
    device = connect(h, add(h)["id"])
    r = send(device, reading(clock, **values))
    assert r.status_code == 422 and r.json()["error"] == "check_the_sensor" and r.json()["sensor_errors"]
    pond = listing(h)["ponds"][0]
    assert pond["reading"] is None
    assert pond["device"]["last_error"]["error"] == "check_the_sensor"   # the farmer sees why
    clock.move(seconds=31)
    assert send(device, reading(clock)).status_code == 201
    assert listing(h)["ponds"][0]["device"]["last_error"] is None          # a good reading clears it


def test_no_values_and_bad_clocks_are_refused(clock):
    h = farm()
    device = connect(h, add(h)["id"])
    assert send(device, {"timestamp": clock.now.isoformat()}).json()["error"] == "no_values"
    clock.move(seconds=31)
    ahead = (clock.now + timedelta(hours=1)).isoformat()
    assert send(device, {"timestamp": ahead, "ph": 7.4}).json()["error"] == "bad_timestamp"


# ----------------------------------------------------------------- online / offline

def test_device_is_online_for_15_minutes_after_a_reading(clock):
    h = farm()
    device = connect(h, add(h)["id"])
    assert listing(h)["ponds"][0]["device"]["online"] is False          # connected, nothing sent yet
    assert listing(h)["ponds"][0]["device"]["last_seen"] is None
    send(device, reading(clock))
    sent_at = clock.now
    clock.move(minutes=14, seconds=59)
    assert listing(h)["ponds"][0]["device"]["online"] is True
    clock.move(seconds=2)
    d = listing(h)["ponds"][0]["device"]
    assert d["online"] is False and d["last_seen"] == sent_at.isoformat(timespec="seconds")   # "Offline since 2:00"


# ----------------------------------------------------------------- worst pond and alerts

def test_worst_pond_is_the_one_for_the_status_strip(clock):
    h = farm()
    safe, warning, danger = (connect(h, add(h, n)["id"]) for n in ("Pond 1", "Pond 2", "Pond 3"))
    add(h, "No device")
    send(safe, reading(clock))
    send(warning, reading(clock, dissolved_oxygen=4.2))
    send(danger, reading(clock, dissolved_oxygen=2.4))
    data = listing(h)
    worst = next(p for p in data["ponds"] if p["id"] == data["worst"])
    assert worst["name"] == "Pond 3" and worst["level"] == "danger"
    assert worst["cause"] == {"en": "low oxygen", "kn": "ಕಡಿಮೆ ಆಮ್ಲಜನಕ"}
    assert worst["level_name"]["en"] == "Danger"


def test_no_worst_pond_without_readings():
    h = farm()
    add(h)
    assert listing(h)["worst"] is None


def test_worst_pond_rules():
    def s(level, received):
        return {"id": level + received, "level": level, "reading": {}, "received_at": received}
    assert ponds.worst([s("safe", "2"), s("warning", "1")])["level"] == "warning"
    assert ponds.worst([s("danger", "1"), s("danger", "3")])["id"] == "danger3"     # newest on a tie
    assert ponds.worst([{"id": "x", "level": "none", "reading": None, "received_at": None}]) is None


def test_alerts_come_from_all_ponds_labelled_with_the_pond_name(clock):
    h = farm()
    road, back = connect(h, add(h, "Pond near road")["id"]), connect(h, add(h, "Back pond")["id"])
    send(road, reading(clock, dissolved_oxygen=4.2))                   # Warning
    send(back, reading(clock))                                         # Safe: no alert
    clock.move(seconds=31)
    send(road, reading(clock, dissolved_oxygen=4.1))                   # still Warning: no new alert
    send(back, reading(clock, ph=9.6))                                 # Danger, pH
    clock.move(seconds=31)
    send(road, reading(clock, dissolved_oxygen=2.3))                   # Warning -> Danger: new alert
    alerts = listing(h)["alerts"]
    assert [(a["pond_name"], a["level"], a["causes"]) for a in alerts] == [
        ("Pond near road", "danger", ["dissolved_oxygen"]),
        ("Back pond", "danger", ["ph"]),
        ("Pond near road", "warning", ["dissolved_oxygen"]),
    ]
    assert all(a["summary"]["en"] and KANNADA.search(a["summary"]["kn"]) for a in alerts)
    assert listing(farm())["alerts"] == []                             # another farm sees none


def test_demo_device_readings_are_marked_simulated(clock):
    h = farm()
    device = connect(h, add(h)["id"])
    send(device, {**reading(clock, dissolved_oxygen=2.4), "demo": True})
    data = listing(h)
    assert data["ponds"][0]["demo"] is True and data["alerts"][0]["demo"] is True


# ----------------------------------------------------------------- one pond's dashboard

def test_pond_dashboard_has_risk_actions_history_and_time_to_danger(clock):
    h = farm()
    pond = add(h)
    device = connect(h, pond["id"])
    for oxygen in (6.4, 6.0, 5.6, 5.2, 4.8, 4.4):                      # falling 0.4 every 30 s... over 3 min
        send(device, {"timestamp": clock.now.isoformat(), "dissolved_oxygen": oxygen})
        clock.move(minutes=20)                                         # (spread out so it is a real trend)
    detail = client.get(f"/api/ponds/{pond['id']}", headers=h).json()
    assert detail["risk"]["level"] == "warning" and detail["risk"]["actions"]
    assert [r["dissolved_oxygen"] for r in detail["history"]] == [6.4, 6.0, 5.6, 5.2, 4.8, 4.4]
    assert detail["time_to_danger"]["status"] == "danger_expected"
    assert detail["device"]["online"] is False                          # 20 minutes since the last reading


def test_old_readings_are_dropped_after_48_hours(clock):
    h = farm()
    device = connect(h, add(h)["id"])
    send(device, reading(clock))
    clock.move(hours=49)
    send(device, {"timestamp": clock.now.isoformat(), "ph": 7.4})
    assert len(main.farms().db.query("SELECT * FROM readings")) == 1


def test_timed_clean_up_also_cleans_a_pond_whose_device_went_quiet(clock):
    h = farm()
    quiet = connect(h, add(h, "Quiet pond")["id"])
    send(quiet, reading(clock, dissolved_oxygen=2.0))              # Danger: one reading and one alert
    db_ = main.farms().db
    count = lambda table: len(db_.query(f"SELECT * FROM {table}"))
    assert (count("readings"), count("alerts")) == (1, 1)
    # The device never sends again. After 47 h the reading is still kept...
    clock.move(hours=47)
    main.clean_up_old_pond_data()
    assert (count("readings"), count("alerts")) == (1, 1)
    # ...after 49 h the reading is gone, the alert (kept 14 days) stays...
    clock.move(hours=2)
    main.clean_up_old_pond_data()
    assert (count("readings"), count("alerts")) == (0, 1)
    # ...and after 15 days the alert is gone too. The pond itself is kept.
    clock.move(days=14)
    main.clean_up_old_pond_data()
    assert (count("readings"), count("alerts")) == (0, 0)
    assert [p["name"] for p in listing(h)["ponds"]] == ["Quiet pond"]


def test_clean_up_runs_on_startup_and_then_every_hour(monkeypatch):
    calls = []
    monkeypatch.setattr(main, "clean_up_old_pond_data", lambda: calls.append("clean"))
    with TestClient(main.app):                                      # starting the app runs the clean-up once
        pass
    assert calls == ["clean"]
    assert main.CLEAN_UP_EVERY == 60 * 60


def test_clean_up_failure_is_logged_not_raised(monkeypatch, caplog):
    class Broken:
        def delete_old(self, now):
            raise RuntimeError("database asleep")
    monkeypatch.setattr(main, "farms", lambda: Broken())
    main.clean_up_old_pond_data()                                   # no exception: the timer keeps running
    assert "Clean-up of old pond data failed (RuntimeError)" in caplog.text


# ----------------------------------------------------------------- storage

def test_memory_storage_is_demo_mode_and_says_so():
    data = listing(farm())
    assert data["storage"] == "memory" and data["demo_mode"] is True
    assert data["demo_mode_note"]["en"] == "Demo mode: ponds reset when the server sleeps."
    assert KANNADA.search(data["demo_mode_note"]["kn"])


def test_sqlite_file_keeps_ponds_after_a_restart(tmp_path, monkeypatch):
    path = tmp_path / "aquanexus.db"
    monkeypatch.setattr(main, "_farm_store", ponds.FarmStore(db.sqlite_file(path)))
    h = farm()
    add(h, "Kept pond")
    data = listing(h)
    assert data["storage"] == "sqlite" and data["demo_mode"] is False and data["demo_mode_note"] is None
    monkeypatch.setattr(main, "_farm_store", ponds.FarmStore(db.sqlite_file(path)))   # a "restart"
    assert [p["name"] for p in listing(h)["ponds"]] == ["Kept pond"]


def test_choosing_the_database(monkeypatch, tmp_path):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("RENDER", raising=False)
    monkeypatch.setenv("SQLITE_PATH", str(tmp_path / "local.db"))
    assert db.open_from_env().kind == "sqlite" and (tmp_path / "local.db").exists()
    monkeypatch.setenv("RENDER", "true")                                # Render without a database
    assert db.open_from_env().kind == "memory"
    calls = []
    monkeypatch.setattr(db, "postgres", lambda url: calls.append(url) or db.memory())
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pw@host/db")
    db.open_from_env()
    assert calls == ["postgresql://user:pw@host/db"]


def test_a_broken_database_url_falls_back_to_memory(monkeypatch, caplog):
    def broken(url):
        raise OSError("could not connect")
    monkeypatch.setattr(db, "postgres", broken)
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:secret-password@host/db")
    store = db.open_from_env()
    assert store.kind == "memory"
    assert "secret-password" not in caplog.text                        # the URL (with its password) is never logged


def test_postgres_gets_its_own_placeholders():
    class FakeCursor:
        description = [("x",)]

        def __init__(self, seen):
            self.seen = seen

        def execute(self, sql, params):
            self.seen.append((sql, params))

        def fetchall(self):
            return [(1,)]

    class FakeConnection:
        def __init__(self):
            self.seen = []

        def cursor(self):
            return FakeCursor(self.seen)

        def commit(self):
            pass

    conn = FakeConnection()
    database = db.Database("postgres", conn, placeholder="%s")
    database.query("SELECT x FROM ponds WHERE id = ? AND farm_id = ?", ("a", "b"))
    assert conn.seen[-1] == ("SELECT x FROM ponds WHERE id = %s AND farm_id = %s", ("a", "b"))
    assert all("?" not in sql for sql, _ in conn.seen)


def test_pond_names_go_in_as_values_never_as_sql(clock):
    h = farm()
    pond = add(h, "x'); DROP TABLE ponds; --")
    assert listing(h)["ponds"][0]["name"] == "x'); DROP TABLE ponds; --"
    assert client.get(f"/api/ponds/{pond['id']}", headers=h).status_code == 200


def test_the_database_file_and_keys_are_never_in_git():
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "data/" in gitignore                                        # data/aquanexus.db
    assert ".env" in gitignore
    assert "psycopg" in (ROOT / "requirements.txt").read_text(encoding="utf-8")


# ----------------------------------------------------------------- the demo devices (tools/fake_sensor.py)

def opener_for_testclient(request, timeout=0):
    """Lets tools/fake_sensor.py talk to the app in-process, as if it were a real server."""
    path = request.full_url.split("://", 1)[1].split("/", 1)[1]
    r = client.request(request.get_method(), "/" + path, content=request.data, headers=dict(request.header_items()))
    if r.status_code >= 400:
        raise HTTPError(request.full_url, r.status_code, "error", {}, io.BytesIO(r.content))

    class Reply(io.BytesIO):
        status = r.status_code

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False
    return Reply(r.content)


def test_fake_sensor_sets_up_several_demo_ponds_with_devices(clock):
    code = ponds.new_farm_code()
    devices = fake_sensor.setup_demo_ponds("http://testserver", code, 3, opener=opener_for_testclient)
    assert [d["name"] for d in devices] == ["Demo pond 1", "Demo pond 2", "Demo pond 3"]
    assert [d["scenario"] for d in devices] == ["night_crash", "normal", "normal"]
    sensors = [fake_sensor.FakeSensor(d["scenario"], seed=n) for n, d in enumerate(devices)]
    for _ in range(10):
        for d, s in zip(devices, sensors):
            body = fake_sensor.device_reading({**s.next_reading(), "timestamp": clock.now.isoformat()}, fake_sensor.random.Random(1))
            status, reply = fake_sensor.send("http://testserver", d["device_id"], d["key"], body, opener=opener_for_testclient)
            assert status == 201, reply
        clock.move(seconds=30)
    data = listing({"X-Farm-Code": code})
    levels = {p["name"]: p["level"] for p in data["ponds"]}
    assert levels == {"Demo pond 1": "danger", "Demo pond 2": "safe", "Demo pond 3": "safe"}
    assert all(p["demo"] for p in data["ponds"])                       # labelled simulated in the app
    assert data["ponds"][0]["reading"]["salinity"] and data["ponds"][0]["reading"]["turbidity"]


def test_fake_sensor_night_crash_goes_safe_warning_danger():
    sensor = fake_sensor.FakeSensor("night_crash", seed=4)
    oxygen = [sensor.next_reading()["dissolved_oxygen"] for _ in range(12)]
    assert oxygen[0] > 6 and min(oxygen[3:7]) < 5 and oxygen[9] < 3
    assert all(r >= 1.4 for r in oxygen)                               # never an impossible value


def test_fake_sensor_device_mode_needs_a_farm_code(capsys):
    assert fake_sensor.main(["--devices", "3"]) == 2
    assert "farm-code" in capsys.readouterr().err
    assert fake_sensor.main(["--device", "dev-abc"]) == 2              # no key


# ----------------------------------------------------------------- Kannada labels

def test_every_pond_message_has_kannada():
    for name in ("DEMO_MODE", "BAD_FARM_CODE", "NOT_FOUND", "TOO_MANY_PONDS", "HAS_DEVICE", "NO_DEVICE", "TOO_SOON"):
        text = getattr(ponds, name)
        assert text["en"] and KANNADA.search(text["kn"]), name
    for key, words in ponds.CAUSE_WORDS.items():
        assert words["en"] and KANNADA.search(words["kn"]), key


def test_every_new_page_label_has_kannada():
    app = (ROOT / "frontend" / "app.js").read_text(encoding="utf-8")
    kn = app[app.index("\n  kn: {"):]
    keys = ["pondsTitle", "pondAdd", "pondsDemoMode", "pondsEmpty", "deviceOnline", "deviceOfflineSince", "deviceConnect",
            "deviceNewKey", "deviceRemove", "deviceKeyOnce", "farmTitle", "farmHelp", "farmWarn", "pondAlertsTitle",
            "stripAllSafe", "pondNameHelp", "deviceStep2", "demoPondTitle", "pondPlaceLabel", "pondDistrictLabel",
            "pondVillageLabel", "pondPlaceHelp", "pondDistrictNone", "pondVillageNone", "pondVillageFirst", "pondTaluk",
            "pondVillageMissing", "pondWeatherNoPlace", "pondWeatherChoose", "weatherDemoNote"]
    for key in keys:
        line = re.search(rf"\b{key}: ([^\n]+)", kn)
        assert line and KANNADA.search(line.group(1)), key


def test_page_has_the_ponds_sections():
    html = (ROOT / "frontend" / "index.html").read_text(encoding="utf-8")
    pond_page = html[html.index('id="page-pond"'):html.index('id="page-alerts"')]
    for element in ("ponds-section", "pond-add", "pond-cards", "pond-detail", "device-connect", "device-key-box",
                    "pond-weather", "pond-weather-choose"):
        assert f'id="{element}"' in pond_page, element
    assert pond_page.index('id="ponds-section"') < pond_page.index('id="simulated-banner"')
    alerts_page = html[html.index('id="page-alerts"'):html.index('id="page-weather"')]
    assert 'id="pond-alerts-list"' in alerts_page
    more_page = html[html.index('id="page-more"'):html.index('id="page-shop"')]
    assert 'id="farm-code"' in more_page and 'id="farm-form"' in more_page
    ponds_js = (ROOT / "frontend" / "ponds.js").read_text(encoding="utf-8")
    assert '"X-Farm-Code": farmCode' in ponds_js and "?farm" not in ponds_js    # header, never the address


# ----------------------------------------------------------------- Terms: how long pond data is kept

FRONTEND = Path(__file__).resolve().parent.parent / "frontend"


def test_storage_says_demo_mode_without_a_database():
    # The tests use an in-memory database: the same as Render without DATABASE_URL.
    assert client.get("/api/storage").json() == {"demo_mode": True, "keep_readings_hours": 48, "keep_alerts_days": 14}


def test_storage_says_data_is_kept_with_a_database(tmp_path):
    main._farm_store = ponds.FarmStore(db.sqlite_file(tmp_path / "farms.db"))
    assert client.get("/api/storage").json()["demo_mode"] is False


def test_terms_show_one_storage_line_chosen_by_the_server():
    html = (FRONTEND / "index.html").read_text(encoding="utf-8")
    app = (FRONTEND / "app.js").read_text(encoding="utf-8")
    assert '<li data-i18n="termsKeep" id="terms-keep" hidden>' in html
    assert '<li data-i18n="termsDemo" id="terms-demo" hidden>' in html
    assert 'fetch("/api/storage")' in app
    assert 'termsKeep: "Device readings are kept for 48 hours and alerts for 14 days."' in app
    assert 'termsDemo: "Demo mode: data resets when the server sleeps."' in app
    # The always-shown line no longer promises how long data is kept (that depends on the server).
    for text in (html, app):
        assert "device readings (for 48 hours)" not in text and "(48 ಗಂಟೆಗಳವರೆಗೆ)" not in text
    # The promised times match the code that deletes old data.
    assert ponds.KEEP_READINGS == timedelta(hours=48) and ponds.KEEP_ALERTS == timedelta(days=14)


def test_live_sensor_card_and_terms_say_the_same_about_clearing():
    app = (FRONTEND / "app.js").read_text(encoding="utf-8")
    html = (FRONTEND / "index.html").read_text(encoding="utf-8")
    texts = {k: re.findall(rf'{k}: "([^"]*)"', app) for k in ("liveNote", "termsServer", "sourcesIntro")}
    for key in ("liveNote", "termsServer"):
        en, kn = texts[key]
        assert "cleared when the server sleeps or restarts" in en, key
        assert "ಸರ್ವರ್ ನಿದ್ರಿಸಿದಾಗ ಅಥವಾ ಮರುಪ್ರಾರಂಭವಾದಾಗ ಅಳಿಸಿಹೋಗುತ್ತವೆ" in kn, key
        assert f'data-i18n="{key}">{en}<' in html, key                 # the page's first paint says the same
    assert "the Live sensor card and the devices in My ponds" in texts["sourcesIntro"][0]


# ----------------------------------------------------------------- where the pond is (for its weather)

def test_a_pond_can_have_a_village_from_the_list(clock):
    h = farm()
    pond = add(h, "Pond near road", village="Kota")
    assert pond["village"] == "Kota"
    assert pond["location"]["taluk"] == {"en": "Brahmavar", "kn": "ಬ್ರಹ್ಮಾವರ"}
    assert pond["location"]["district"]["en"] == "Udupi" and pond["location"]["latitude"] == 13.52
    assert listing(h)["ponds"][0]["location"]["name"]["kn"] == "ಕೋಟ"

    r = client.patch(f"/api/ponds/{pond['id']}", json={"village": " Karwar "}, headers=h)
    assert r.json()["village"] == "Karwar" and r.json()["location"]["district"]["en"] == "Uttara Kannada"
    r = client.patch(f"/api/ponds/{pond['id']}", json={"size": "1 acre"}, headers=h)
    assert r.json()["village"] == "Karwar"                          # left out = unchanged
    r = client.patch(f"/api/ponds/{pond['id']}", json={"village": None}, headers=h)
    assert r.json()["village"] is None and r.json()["location"] is None


def test_village_is_optional():
    pond = add(farm(), "Pond near road")
    assert pond["village"] is None and pond["location"] is None


def test_a_village_not_in_the_list_is_refused(clock):
    h = farm()
    for village in ("Paris", "13.52, 74.70", "Kota, near the temple"):
        r = client.post("/api/ponds", json={"pond_name": "P", "village": village}, headers=h)
        assert r.status_code == 422 and r.json()["error"] == "unknown_place", village
        assert KANNADA.search(r.json()["message"]["kn"])
    assert listing(h)["ponds"] == []
    pond = add(h, "P", village="Malpe")
    r = client.patch(f"/api/ponds/{pond['id']}", json={"village": "Goa"}, headers=h)
    assert r.status_code == 422
    assert listing(h)["ponds"][0]["village"] == "Malpe"


def test_only_the_village_name_is_stored(clock):
    store = main.farms()
    add(farm(), "P", village="Gokarna")
    row = store.db.one("SELECT * FROM ponds")
    assert row["village"] == "Gokarna"
    assert set(row) == {"id", "farm_id", "name", "size", "fish", "created_at", "village"}   # no coordinates, no address


def test_an_old_database_gets_the_village_column(tmp_path):
    import sqlite3
    path = tmp_path / "old.db"
    old = sqlite3.connect(path)
    old.execute("CREATE TABLE ponds (id TEXT PRIMARY KEY, farm_id TEXT NOT NULL, name TEXT NOT NULL, "
                "size TEXT, fish TEXT, created_at TEXT NOT NULL)")
    old.execute("INSERT INTO ponds VALUES ('p-aaaaaaaaaa', 'f', 'Old pond', NULL, NULL, '2026-10-01T00:00:00')")
    old.commit()
    old.close()
    store = ponds.FarmStore(db.sqlite_file(path))
    assert store.pond("f", "p-aaaaaaaaaa")["village"] is None
    assert store.edit_pond("f", "p-aaaaaaaaaa", {"village": "Ullal"})["village"] == "Ullal"
    db.sqlite_file(path)                                            # opening it again is fine too
