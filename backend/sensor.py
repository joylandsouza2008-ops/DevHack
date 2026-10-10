"""
Live readings from a real pond sensor (for example an ESP32 with probes).

The sensor sends one reading at a time to POST /api/sensor/{pond_id}
(see backend/main.py and docs/sensor-api.md). This file holds the parts that
are not about the web:

  1. sensor_key(pond_id)   the pond's secret key, read from an environment
                           variable such as SENSOR_KEY_POND1. Never in the code.
  2. key_matches(...)      compares the key the sensor sent with that secret.
  3. check_timestamp(...)  rejects readings with a missing time zone or a clock
                           that is ahead of the server.
  4. SensorStore           keeps the latest readings in memory, one list per pond.

Memory only: when the server restarts (free Render sleeps after 15 minutes
with no visitors) all live readings are gone. The next reading from the sensor
fills the dashboard again.
"""

from __future__ import annotations

import hmac
import math
import os
import threading
from collections import deque
from datetime import datetime, timedelta, timezone

from backend import risk_messages as msg
from backend.alerts import POND_NAMES

# Pond IDs a sensor can send to, matching the Pond 1 / 2 / 3 buttons on the dashboard.
SENSOR_PONDS = {f"pond{n}": POND_NAMES[f"station{n}"] for n in (1, 2, 3)}

SOURCE = "live_sensor"
LIVE_LABEL = {"en": "Live sensor", "kn": "ಲೈವ್ ಸೆನ್ಸರ್"}
# A device that sends made-up readings (tools/fake_sensor.py) says demo = true.
DEMO_LABEL = {"en": "Demo device: simulated readings, not a real pond",
              "kn": "ಡೆಮೊ ಸಾಧನ: ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಅಳತೆಗಳು, ನಿಜವಾದ ಕೊಳವಲ್ಲ"}

# Messages the sensor (and the dashboard) get back when a reading is refused.
REJECTED = {"en": "Reading rejected. Check the sensor.",
            "kn": "ಅಳತೆಯನ್ನು ತಿರಸ್ಕರಿಸಲಾಗಿದೆ. ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ."}
NO_VALUES = {"en": "The reading has no values. Check the sensor.",
             "kn": "ಅಳತೆಯಲ್ಲಿ ಯಾವುದೇ ಮೌಲ್ಯಗಳಿಲ್ಲ. ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ."}
WRONG_KEY = {"en": "Missing or wrong sensor key.", "kn": "ಸೆನ್ಸರ್ ಕೀ ಇಲ್ಲ ಅಥವಾ ತಪ್ಪಾಗಿದೆ."}
CLOCK_AHEAD = {"en": "The sensor's clock is ahead of the real time. Check the sensor clock.",
               "kn": "ಸೆನ್ಸರ್‌ನ ಗಡಿಯಾರ ನಿಜವಾದ ಸಮಯಕ್ಕಿಂತ ಮುಂದಿದೆ. ಸೆನ್ಸರ್ ಗಡಿಯಾರ ಪರಿಶೀಲಿಸಿ."}
NO_TIME_ZONE = {"en": "The timestamp has no time zone. Add +05:30 or Z. Check the sensor clock.",
                "kn": "ಸಮಯದಲ್ಲಿ ಟೈಮ್ ಝೋನ್ ಇಲ್ಲ. +05:30 ಅಥವಾ Z ಸೇರಿಸಿ. ಸೆನ್ಸರ್ ಗಡಿಯಾರ ಪರಿಶೀಲಿಸಿ."}
TOO_OLD = {"en": "The timestamp is more than a day old. Check the sensor clock.",
           "kn": "ಸಮಯ ಒಂದು ದಿನಕ್ಕಿಂತ ಹಳೆಯದು. ಸೆನ್ಸರ್ ಗಡಿಯಾರ ಪರಿಶೀಲಿಸಿ."}

CLOCK_TOLERANCE = timedelta(minutes=5)    # small clock differences are normal
MAX_AGE = timedelta(days=1)               # older readings are a clock fault, not "live"
HISTORY_LENGTH = 200                      # readings kept per pond (about 17 min at one every 5 s)


def key_variable(pond_id: str) -> str:
    """Name of the environment variable that holds this pond's key, e.g. SENSOR_KEY_POND1."""
    return f"SENSOR_KEY_{pond_id.upper()}"


def sensor_key(pond_id: str) -> str | None:
    """The pond's secret key, or None if it has not been set on this server."""
    return os.environ.get(key_variable(pond_id)) or None


def key_matches(sent: str | None, expected: str) -> bool:
    """True if the sensor sent the right key. compare_digest takes the same time
    for every wrong key, so the key can't be guessed one letter at a time."""
    return sent is not None and hmac.compare_digest(sent.encode(), expected.encode())


def check_timestamp(timestamp: datetime, now: datetime | None = None) -> dict | None:
    """None if the time is fine, otherwise the message to send back."""
    if timestamp.tzinfo is None:
        return NO_TIME_ZONE
    now = now or datetime.now(timezone.utc)
    if timestamp > now + CLOCK_TOLERANCE:
        return CLOCK_AHEAD
    if timestamp < now - MAX_AGE:
        return TOO_OLD
    return None


def not_a_number_errors(values: dict) -> list:
    """'Check the sensor' messages for NaN or Infinity values (a broken probe), in the
    same shape as the classifier's sensor_errors."""
    return [{"parameter": parameter, "reading": str(value),
             "message": {lang: text.format(name=msg.PARAMETER_NAMES[parameter][lang], value=str(value))
                         for lang, text in msg.SENSOR_ERROR.items()}}
            for parameter, value in values.items() if not math.isfinite(value)]


class SensorStore:
    """
    Latest readings for each pond, in memory. The POST handler adds readings,
    the dashboard stream reads them. `version` goes up by one on every change,
    so the stream only has to compare numbers to know something new arrived.
    A lock keeps the two from getting in each other's way.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._readings: dict[str, deque] = {}
        self._rejected: dict[str, dict] = {}
        self._version: dict[str, int] = {}

    def add(self, pond_id: str, entry: dict) -> None:
        with self._lock:
            self._readings.setdefault(pond_id, deque(maxlen=HISTORY_LENGTH)).append(entry)
            self._rejected.pop(pond_id, None)      # a good reading clears the old fault
            self._version[pond_id] = self._version.get(pond_id, 0) + 1

    def reject(self, pond_id: str, rejection: dict) -> None:
        with self._lock:
            self._rejected[pond_id] = rejection
            self._version[pond_id] = self._version.get(pond_id, 0) + 1

    def version(self, pond_id: str) -> int:
        with self._lock:
            return self._version.get(pond_id, 0)

    def snapshot(self, pond_id: str) -> tuple[int, dict | None, dict | None]:
        """(version, latest reading or None, latest rejection or None)."""
        with self._lock:
            readings = self._readings.get(pond_id)
            latest = readings[-1] if readings else None
            return self._version.get(pond_id, 0), latest, self._rejected.get(pond_id)

    def count(self, pond_id: str) -> int:
        """How many readings are kept for this pond (at most HISTORY_LENGTH)."""
        with self._lock:
            return len(self._readings.get(pond_id, ()))

    def clear(self) -> None:
        """Forget everything (what a server restart does; used by the tests)."""
        with self._lock:
            self._readings.clear()
            self._rejected.clear()
            self._version.clear()


store = SensorStore()
