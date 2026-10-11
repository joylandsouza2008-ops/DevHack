"""
"My ponds and devices": a farmer's own ponds, one IoT device per pond, and
the live readings and alerts from all of them. The web endpoints are in
backend/main.py; the data lives in backend/db.py.

No accounts and no personal data:
  - A FARM CODE (e.g. K7QM-3XRP-9TFD) groups a farmer's ponds. The page makes it
    on the first visit and keeps it in the browser; typing it on another phone
    opens the same ponds. The server stores only a hash of it, never the code.
    Anyone with the code can see and change those ponds, so it is long and random.
  - Each device gets an ID (public, in the address) and a secret KEY, shown once.
    The server stores only a hash of the key.

What this file does:
    normalize_farm_code / farm_id     check a farm code and turn it into the stored id
    FarmStore                          ponds, devices, readings and alerts (add, change, read)
    pond_summary(...)                  one pond's card: status, last reading, device online/offline
    worst(...)                         the pond in the worst state, for the status strip
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
from datetime import datetime, timedelta

from backend import risk_messages as msg
from backend.db import Database

# Crockford base32: no I, L, O or U, so a code read aloud or typed is hard to get wrong.
CODE_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
FARM_CODE_LENGTH = 12                       # 60 random bits: impossible to guess
ID_ALPHABET = "abcdefghijkmnpqrstuvwxyz23456789"
POND_ID = re.compile(r"^p-[a-z0-9]{10}$")
DEVICE_ID = re.compile(r"^dev-[a-z0-9]{10}$")

DEVICE_VALUES = ("dissolved_oxygen", "ph", "temperature", "ammonia", "turbidity", "salinity")
ONLINE_MINUTES = 15                         # a reading in the last 15 minutes = Online
MIN_SECONDS_BETWEEN = int(os.environ.get("DEVICE_MIN_SECONDS", "30"))   # one reading per device per 30 s
MAX_PONDS = 20                              # per farm
KEEP_READINGS = timedelta(hours=48)
KEEP_ALERTS = timedelta(days=14)
HISTORY_HOURS = 12                          # readings shown on a pond's chart
HISTORY_POINTS = 150                        # at most this many points on the chart

DEMO_MODE = {"en": "Demo mode: ponds reset when the server sleeps.",
             "kn": "ಡೆಮೊ ಮೋಡ್: ಸರ್ವರ್ ನಿದ್ರಿಸಿದಾಗ ಕೊಳಗಳು ಅಳಿಸಿಹೋಗುತ್ತವೆ."}
BAD_FARM_CODE = {"en": "Missing or wrong farm code.", "kn": "ಫಾರ್ಮ್ ಕೋಡ್ ಇಲ್ಲ ಅಥವಾ ತಪ್ಪಾಗಿದೆ."}
NOT_FOUND = {"en": "Pond not found.", "kn": "ಕೊಳ ಸಿಗಲಿಲ್ಲ."}
TOO_MANY_PONDS = {"en": f"You can add up to {MAX_PONDS} ponds.", "kn": f"ನೀವು {MAX_PONDS} ಕೊಳಗಳವರೆಗೆ ಸೇರಿಸಬಹುದು."}
HAS_DEVICE = {"en": "This pond already has a device. Remove it first, or make a new key.",
              "kn": "ಈ ಕೊಳಕ್ಕೆ ಈಗಾಗಲೇ ಸಾಧನವಿದೆ. ಮೊದಲು ಅದನ್ನು ತೆಗೆಯಿರಿ, ಅಥವಾ ಹೊಸ ಕೀ ಮಾಡಿ."}
NO_DEVICE = {"en": "This pond has no device.", "kn": "ಈ ಕೊಳಕ್ಕೆ ಯಾವುದೇ ಸಾಧನವಿಲ್ಲ."}
TOO_SOON = {"en": f"Too many readings. Send at most one reading every {MIN_SECONDS_BETWEEN} seconds.",
            "kn": f"ತುಂಬಾ ಅಳತೆಗಳು. {MIN_SECONDS_BETWEEN} ಸೆಕೆಂಡಿಗೆ ಒಂದಕ್ಕಿಂತ ಹೆಚ್ಚು ಅಳತೆ ಕಳುಹಿಸಬೇಡಿ."}

# Short words for the status strip: "Pond 2: Danger · low oxygen".
CAUSE_WORDS = {
    ("dissolved_oxygen", "low"): {"en": "low oxygen", "kn": "ಕಡಿಮೆ ಆಮ್ಲಜನಕ"},
    ("ph", "low"): {"en": "low pH", "kn": "ಕಡಿಮೆ pH"},
    ("ph", "high"): {"en": "high pH", "kn": "ಹೆಚ್ಚು pH"},
    ("temperature", "high"): {"en": "hot water", "kn": "ಬಿಸಿ ನೀರು"},
    ("temperature", "low"): {"en": "cold water", "kn": "ತಣ್ಣನೆಯ ನೀರು"},
    ("ammonia", "high"): {"en": "high ammonia", "kn": "ಹೆಚ್ಚು ಅಮೋನಿಯಾ"},
    ("nitrate", "high"): {"en": "high nitrate", "kn": "ಹೆಚ್ಚು ನೈಟ್ರೇಟ್"},
}
LEVEL_ORDER = {"none": -1, "unknown": -1, "safe": 0, "warning": 1, "danger": 2}


# ----------------------------------------------------------------- codes, ids and keys

def new_farm_code() -> str:
    """A new farm code, e.g. K7QM-3XRP-9TFD. (The page makes its own; this one is for tools and tests.)"""
    code = "".join(secrets.choice(CODE_ALPHABET) for _ in range(FARM_CODE_LENGTH))
    return "-".join(code[i:i + 4] for i in range(0, FARM_CODE_LENGTH, 4))


def normalize_farm_code(code: str | None) -> str | None:
    """'k7qm 3xrp-9tfd' -> 'K7QM3XRP9TFD'. O is read as 0, I and L as 1. None if it isn't a farm code."""
    if not code:
        return None
    s = re.sub(r"[\s-]", "", code).upper().translate(str.maketrans("OIL", "011"))
    return s if len(s) == FARM_CODE_LENGTH and all(c in CODE_ALPHABET for c in s) else None


def farm_id(code: str) -> str:
    """What the server stores instead of the farm code (a one-way hash)."""
    return hashlib.sha256(f"aquanexus-farm:{code}".encode()).hexdigest()


def _random_id(prefix: str) -> str:
    return prefix + "".join(secrets.choice(ID_ALPHABET) for _ in range(10))


def key_hash(key: str) -> str:
    """Device keys are long and random, so a plain SHA-256 is enough (no password stretching needed)."""
    return hashlib.sha256(f"aquanexus-device:{key}".encode()).hexdigest()


def _iso(t: datetime) -> str:
    return t.isoformat(timespec="seconds")


def _clean(text: str | None) -> str | None:
    text = " ".join((text or "").split())
    return text or None


# ----------------------------------------------------------------- the store

class FarmStore:
    """Ponds, devices, readings and alerts. Every call that changes a pond checks it belongs to the farm."""

    def __init__(self, database: Database) -> None:
        self.db = database

    # ---- ponds

    def ponds(self, farm: str) -> list[dict]:
        return self.db.query("SELECT * FROM ponds WHERE farm_id = ? ORDER BY created_at, name", (farm,))

    def pond(self, farm: str, pond_id: str) -> dict | None:
        return self.db.one("SELECT * FROM ponds WHERE id = ? AND farm_id = ?", (pond_id, farm))

    def add_pond(self, farm: str, name: str, size: str | None, fish: str | None, now: datetime) -> dict | None:
        """The new pond, or None if the farm already has MAX_PONDS."""
        if len(self.ponds(farm)) >= MAX_PONDS:
            return None
        self.db.execute("INSERT INTO farms (id, created_at) VALUES (?, ?) ON CONFLICT (id) DO NOTHING", (farm, _iso(now)))
        pond_id = _random_id("p-")
        self.db.execute("INSERT INTO ponds (id, farm_id, name, size, fish, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                        (pond_id, farm, _clean(name), _clean(size), _clean(fish), _iso(now)))
        return self.pond(farm, pond_id)

    def edit_pond(self, farm: str, pond_id: str, changes: dict) -> dict | None:
        if not self.pond(farm, pond_id):
            return None
        for column in ("name", "size", "fish"):
            if column in changes:
                value = _clean(changes[column])
                if column == "name" and not value:
                    continue                    # a pond always keeps a name
                self.db.execute(f"UPDATE ponds SET {column} = ? WHERE id = ? AND farm_id = ?", (value, pond_id, farm))
        return self.pond(farm, pond_id)

    def delete_pond(self, farm: str, pond_id: str) -> bool:
        if not self.pond(farm, pond_id):
            return False
        for table in ("readings", "alerts", "devices"):
            self.db.execute(f"DELETE FROM {table} WHERE pond_id = ?", (pond_id,))
        self.db.execute("DELETE FROM ponds WHERE id = ? AND farm_id = ?", (pond_id, farm))
        return True

    # ---- devices

    def device_for_pond(self, pond_id: str) -> dict | None:
        return self.db.one("SELECT * FROM devices WHERE pond_id = ?", (pond_id,))

    def device(self, device_id: str) -> dict | None:
        return self.db.one("SELECT * FROM devices WHERE id = ?", (device_id,))

    def connect_device(self, farm: str, pond_id: str, now: datetime) -> tuple[str, str] | None:
        """(device id, key) for a pond with no device yet. The key is returned here ONLY."""
        if not self.pond(farm, pond_id) or self.device_for_pond(pond_id):
            return None
        device_id, key = _random_id("dev-"), secrets.token_urlsafe(24)
        self.db.execute("INSERT INTO devices (id, pond_id, key_hash, created_at) VALUES (?, ?, ?, ?)",
                        (device_id, pond_id, key_hash(key), _iso(now)))
        return device_id, key

    def new_key(self, farm: str, pond_id: str) -> tuple[str, str] | None:
        """A new key for the pond's device; the old key stops working at once."""
        device = self.device_for_pond(pond_id) if self.pond(farm, pond_id) else None
        if not device:
            return None
        key = secrets.token_urlsafe(24)
        self.db.execute("UPDATE devices SET key_hash = ? WHERE id = ?", (key_hash(key), device["id"]))
        return device["id"], key

    def remove_device(self, farm: str, pond_id: str) -> bool:
        if not self.pond(farm, pond_id) or not self.device_for_pond(pond_id):
            return False
        self.db.execute("DELETE FROM devices WHERE pond_id = ?", (pond_id,))
        return True

    @staticmethod
    def key_ok(device: dict | None, key: str | None) -> bool:
        """Right key for this device? Same amount of work for unknown devices and wrong keys."""
        expected = device["key_hash"] if device else key_hash("no-such-device")
        sent = key_hash(key or "")
        return device is not None and key is not None and hmac.compare_digest(sent, expected)

    def seconds_to_wait(self, device: dict, now: datetime) -> int:
        """0 if the device may send now, else how long to wait (one reading per MIN_SECONDS_BETWEEN)."""
        last = device.get("last_try")
        if not last:
            return 0
        gap = (now - datetime.fromisoformat(last)).total_seconds()
        return max(0, int(MIN_SECONDS_BETWEEN - gap + 0.999)) if gap < MIN_SECONDS_BETWEEN else 0

    def note_try(self, device_id: str, now: datetime, error: dict | None = None) -> None:
        """Every reading with the right key counts for the rate limit, accepted or not."""
        self.db.execute("UPDATE devices SET last_try = ?, last_error = ? WHERE id = ?",
                        (_iso(now), json.dumps(error, ensure_ascii=False) if error else None, device_id))

    # ---- readings and alerts

    def add_reading(self, device: dict, values: dict, risk: dict, measured_at: datetime, demo: bool,
                    now: datetime) -> None:
        pond_id = device["pond_id"]
        pond = self.db.one("SELECT * FROM ponds WHERE id = ?", (pond_id,))
        previous = self.latest(pond_id)
        level, causes = risk["level"], sorted(risk["causes"])
        data = {"values": values, "causes": causes}
        self.db.execute("INSERT INTO readings (pond_id, device_id, received_at, measured_at, level, demo, data_json) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (pond_id, device["id"], _iso(now), measured_at.isoformat(), level, int(demo), json.dumps(data)))
        self.db.execute("UPDATE devices SET last_seen = ?, last_error = NULL WHERE id = ?", (_iso(now), device["id"]))
        # A new alert when the pond enters Warning / Danger, or its level or cause changes.
        before = (previous["level"], previous["causes"]) if previous else None
        if level in ("warning", "danger") and before != (level, causes):
            self.db.execute("INSERT INTO alerts (pond_id, farm_id, time, level, causes, summary_json, demo) "
                            "VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (pond_id, pond["farm_id"], _iso(now), level, ",".join(causes),
                             json.dumps(risk["summary"], ensure_ascii=False), int(demo)))
        self.delete_old(now)

    def delete_old(self, now: datetime) -> None:
        """
        Keep the database small, as the Terms promise: delete readings older than
        48 hours and alerts older than 14 days, for EVERY pond. Runs after each
        new reading, and on a timer (backend/main.py) so a pond whose device has
        gone quiet is cleaned too.
        """
        self.db.execute("DELETE FROM readings WHERE received_at < ?", (_iso(now - KEEP_READINGS),))
        self.db.execute("DELETE FROM alerts WHERE time < ?", (_iso(now - KEEP_ALERTS),))

    @staticmethod
    def _reading(row: dict | None) -> dict | None:
        if not row:
            return None
        data = json.loads(row["data_json"])
        return {"received_at": row["received_at"], "measured_at": row["measured_at"], "level": row["level"],
                "demo": bool(row["demo"]), "values": data["values"], "causes": data["causes"]}

    def latest(self, pond_id: str) -> dict | None:
        return self._reading(self.db.one("SELECT * FROM readings WHERE pond_id = ? ORDER BY received_at DESC LIMIT 1",
                                         (pond_id,)))

    def history(self, pond_id: str, now: datetime) -> list[dict]:
        """Readings from the last HISTORY_HOURS, oldest first, thinned to at most HISTORY_POINTS."""
        rows = self.db.query("SELECT * FROM readings WHERE pond_id = ? AND received_at >= ? ORDER BY received_at",
                             (pond_id, _iso(now - timedelta(hours=HISTORY_HOURS))))
        step = max(1, -(-len(rows) // HISTORY_POINTS))
        keep = rows[::step]
        if rows and keep[-1] is not rows[-1]:
            keep.append(rows[-1])               # always show the newest reading
        return [self._reading(r) for r in keep]

    def alerts(self, farm: str, limit: int = 30) -> list[dict]:
        rows = self.db.query("SELECT a.*, p.name AS pond_name FROM alerts a JOIN ponds p ON p.id = a.pond_id "
                             "WHERE a.farm_id = ? ORDER BY a.time DESC LIMIT ?", (farm, limit))
        return [{"pond_id": r["pond_id"], "pond_name": r["pond_name"], "time": r["time"], "level": r["level"],
                 "level_name": msg.LEVEL_NAMES[r["level"]], "causes": [c for c in r["causes"].split(",") if c],
                 "summary": json.loads(r["summary_json"]), "demo": bool(r["demo"])} for r in rows]


# ----------------------------------------------------------------- what the page shows

def cause_words(risk: dict) -> dict | None:
    """{"en": "low oxygen", "kn": ...} for the worst cause, or None when the pond is Safe."""
    worst = [p for p in risk["parameters"] if p["parameter"] in risk["causes"]]
    if not worst:
        return None
    p = worst[0]
    words = CAUSE_WORDS.get((p["parameter"], p["direction"]))
    return words or {lang: p["name"][lang] for lang in ("en", "kn")}


def device_status(device: dict | None, now: datetime) -> dict | None:
    if not device:
        return None
    last_seen = device.get("last_seen")
    online = bool(last_seen) and now - datetime.fromisoformat(last_seen) <= timedelta(minutes=ONLINE_MINUTES)
    error = json.loads(device["last_error"]) if device.get("last_error") else None
    return {"id": device["id"], "connected_at": device["created_at"], "last_seen": last_seen,
            "online": online, "last_error": error}


def pond_summary(pond: dict, latest: dict | None, device: dict | None, now: datetime, assess) -> dict:
    """One pond's card. `assess` is backend.main.assess (passed in to avoid a circular import)."""
    risk = assess(latest["values"], source="sensor") if latest else None
    return {
        "id": pond["id"], "name": pond["name"], "size": pond["size"], "fish": pond["fish"],
        "level": risk["level"] if risk else "none",
        "level_name": risk["level_name"] if risk else None,
        "summary": risk["summary"] if risk else None,
        "cause": cause_words(risk) if risk else None,
        "reading": latest["values"] if latest else None,
        "measured_at": latest["measured_at"] if latest else None,
        "received_at": latest["received_at"] if latest else None,
        "demo": bool(latest and latest["demo"]),
        "device": device_status(device, now),
    }


def worst(summaries: list[dict]) -> dict | None:
    """The pond in the worst state (Danger > Warning > Safe), newest reading first on a tie.
    Only ponds with a reading count."""
    with_readings = [s for s in summaries if s["reading"] is not None]
    if not with_readings:
        return None
    return max(with_readings, key=lambda s: (LEVEL_ORDER.get(s["level"], -1), s["received_at"] or ""))
