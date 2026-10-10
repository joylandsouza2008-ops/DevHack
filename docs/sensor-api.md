# Live sensor API

A real pond sensor (for example an ESP32 with oxygen, pH, temperature and ammonia
probes) can send its readings to AquaNexus. They appear on the dashboard in the
**Live sensor** card as they arrive. They are graded with the same Safe / Warning /
Danger rules as everything else and are always labelled **"Live sensor" / "ಲೈವ್ ಸೆನ್ಸರ್"**,
kept apart from the simulated pond.

| | |
|---|---|
| Send a reading | `POST /api/sensor/{pond_id}` with header `X-Sensor-Key` |
| Ponds | `pond1`, `pond2`, `pond3` (the Pond 1 / 2 / 3 buttons on the dashboard) |
| Latest reading | `GET /api/sensor/{pond_id}` (no key needed) |
| Live updates | `GET /api/sensor/{pond_id}/stream` (Server-Sent Events, used by the dashboard) |
| Code | `backend/main.py` (endpoints), `backend/sensor.py` (key check, clock check, memory store) |
| Tests | `tests/test_sensor_api.py` |

Interactive docs for every field: open `/docs` on the server.

## 1. The pond key

Each pond has its own secret key. Only a device that knows the key can send readings
for that pond. The key is kept **only** in an environment variable on the server:

| Pond | Environment variable |
|---|---|
| `pond1` | `SENSOR_KEY_POND1` |
| `pond2` | `SENSOR_KEY_POND2` |
| `pond3` | `SENSOR_KEY_POND3` |

The key is never in the code, in git, or in the web page. The page doesn't need it:
reading the dashboard is open, only *sending* readings needs the key.

**Make a key** (a long random password):

```
python -c "import secrets; print(secrets.token_urlsafe(24))"
```

**On Render:** open the **meenuraksha** service → **Environment** → **Add Environment
Variable**. Key: `SENSOR_KEY_POND1`, value: the key you just made. Click **Save Changes**.
Render restarts the app with the new key in about a minute. Do the same for `pond2` and `pond3` if you use them.

**On your laptop** (PowerShell, in the window where you start the server):

```powershell
$env:SENSOR_KEY_POND1 = "my-local-test-key"
uvicorn backend.main:app --reload
```

If no key is set for a pond, the server refuses every reading for it (`503 not_set_up`).

## 2. Sending a reading

```
POST /api/sensor/pond1
Content-Type: application/json
X-Sensor-Key: <the pond1 key>

{
  "timestamp": "2026-10-10T21:30:00+05:30",
  "dissolved_oxygen": 5.8,
  "ph": 7.4,
  "temperature": 29.5,
  "ammonia": 0.3,
  "device": "esp32-pond1"
}
```

| Field | Unit | Required |
|---|---|---|
| `timestamp` | When the sensor measured it, ISO 8601 **with a time zone** (`+05:30` for India, or `Z` for UTC) | yes |
| `dissolved_oxygen` | mg/L | at least one of the four values |
| `ph` | no unit | |
| `temperature` | °C (water) | |
| `ammonia` | mg/L **total** ammonia (the server works out the toxic NH₃ part from pH and temperature) | |
| `device` | any short name, up to 40 characters | no |
| `demo` | `true` only for a demo device that sends made-up readings | no (default `false`) |

Leave out a value the sensor doesn't measure. Ammonia is only graded when pH and temperature are sent too.

**Accepted** (`201`):

```json
{"accepted": true, "level": "safe", "summary": {"en": "All readings are in the safe range.", "kn": "..."},
 "received_at": "2026-10-10T16:00:01+00:00"}
```

### What gets refused

Nothing refused is stored. The sensor gets a clear reason in English and Kannada.

| Status | `error` | When |
|---|---|---|
| `401` | `wrong_key` | `X-Sensor-Key` missing or wrong |
| `503` | `not_set_up` | No key set on the server for this pond |
| `422` | `check_the_sensor` | An impossible value: "Reading rejected. Check the sensor." The whole reading is refused, because one broken probe means the others can't be trusted either |
| `422` | `bad_timestamp` | No time zone, the clock is more than 5 minutes ahead, or the time is over a day old |
| `422` | `no_values` | None of the four values was sent |
| `422` | (FastAPI's own error) | Not JSON, text instead of a number, missing `timestamp`, unknown pond |

**Impossible values** come from `plausible` in `config/thresholds.toml` (the same limits
the rest of the app uses), plus `NaN` / `Infinity`:

| Value | Refused if |
|---|---|
| Dissolved oxygen | below 0.1 or above 30 mg/L (0 means a dead probe) |
| pH | below 2 or above 12 |
| Temperature | below 5 or above 45 °C |
| Total ammonia | below 0 or above 20 mg/L |

Example refusal:

```json
{"accepted": false, "error": "check_the_sensor",
 "message": {"en": "Reading rejected. Check the sensor.", "kn": "ಅಳತೆಯನ್ನು ತಿರಸ್ಕರಿಸಲಾಗಿದೆ. ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ."},
 "sensor_errors": [{"parameter": "dissolved_oxygen", "reading": 45.0,
   "message": {"en": "Dissolved oxygen reading looks wrong (45.0). Check the sensor.", "kn": "..."}}]}
```

A refused reading for a bad value or clock is also shown on the dashboard ("check the
sensor") until the next good reading. Wrong-key attempts are **not** shown, so a stranger
can't change what the farmer sees.

## 3. What the dashboard shows

The **Live sensor** card follows the Pond 1 / 2 / 3 buttons. It shows:

- the **Live sensor · Pond 1** label, with a pond-blue dot that pulses while readings arrive;
- the Safe / Warning / Danger banner, each value with its own badge, and "Measured 21:30:05 · received 4 s ago";
- the "What to do now" checklist for Warning and Danger;
- **"No new reading for N min. Check the sensor's power and Wi-Fi."** after a minute without readings;
- the refusal message after an impossible reading;
- for a demo device, the tag **"Demo device: simulated readings, not a real pond"**.

Live-sensor warnings also go into the alert history (tagged **Live sensor**), and the alert
preview has a **Live sensor** button next to **Simulated** and **Test kit**. As everywhere
else, no real SMS or WhatsApp message is sent.

## 4. Memory only: readings are lost when the server restarts

Readings are kept in the server's memory (the last 200 per pond), not in a database or file.
On the **free Render plan** the app **sleeps after 15 minutes with no visitors**, and
Render can restart it at any time. A sleep, restart or new deploy **clears all live
readings**. The card then says "No reading from the Pond 1 sensor yet" until the sensor's
next reading, a few seconds later.

That's fine for a demo. Two more things to know:

- A sensor sending to a sleeping server has to wait **about a minute** for its first reply
  while the app wakes up. Use a long timeout (the ESP32 example below uses 70 s).
- **A sensor sending every few seconds keeps the free app awake**, which uses up the
  750 free hours a month (one app running all month uses about 744). Turn the sensor off
  when it isn't needed.

For a real farm you would store readings in a database. That isn't part of this demo.

## 5. Demo device: `tools/fake_sensor.py`

A pretend sensor for demos. It sends a made-up reading every few seconds, exactly like a
real one, with `"demo": true`, so the dashboard tags it **"Demo device: simulated readings,
not a real pond"**. It uses only Python's standard library. Its readings are made up and
are never used to train or test the model.

Locally (two PowerShell windows, same key in both):

```powershell
# window 1
$env:SENSOR_KEY_POND1 = "my-local-test-key"
uvicorn backend.main:app --reload

# window 2
$env:SENSOR_KEY_POND1 = "my-local-test-key"
python tools/fake_sensor.py --scenario falling
```

To the live Render link:

```powershell
python tools/fake_sensor.py --url https://meenuraksha.onrender.com --key <the pond1 key from Render>
```

| Option | What it does |
|---|---|
| `--scenario normal` | Healthy readings with small changes (default) |
| `--scenario falling` | Oxygen drops a little each reading: Safe → Warning (after about 20 readings) → Danger (after about 45) |
| `--every 5` | Seconds between readings (default 5) |
| `--count 20` | Stop after 20 readings (default: run until Ctrl+C) |
| `--fault-every 10` | Every 10th reading has oxygen 0, to show "Check the sensor" |
| `--pond pond2` | Send to Pond 2 (key from `SENSOR_KEY_POND2`) |

It prints each reading and the server's answer, e.g.
`21:30:05  DO 4.32  pH 7.41  29.0 °C  ammonia 0.253  ->  accepted: WARNING - Oxygen is low ...`.

## 6. ESP32 example (Arduino)

Board: any ESP32, Arduino IDE with the **esp32** boards package. No extra libraries needed.
The four `read...()` functions are **placeholders**: replace them with the code for your probes
(each probe maker gives example code, and each probe must be calibrated as its maker says).

```cpp
// AquaNexus pond sensor: sends one reading every 60 seconds.
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <time.h>

const char* WIFI_NAME     = "your-wifi-name";
const char* WIFI_PASSWORD = "your-wifi-password";
const char* SERVER        = "https://meenuraksha.onrender.com";
const char* POND_ID       = "pond1";
const char* SENSOR_KEY    = "paste-the-pond1-key-here";   // the same value as SENSOR_KEY_POND1 on Render
const unsigned long SEND_EVERY_MS = 60UL * 1000;

// ---- Replace these with your probe code ----
float readOxygen()      { return 6.2; }   // mg/L
float readPH()          { return 7.4; }
float readTemperature() { return 29.0; }  // °C
float readAmmonia()     { return 0.3; }   // mg/L total ammonia

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_NAME, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nWi-Fi connected");
  // Real time from the internet, India time (+05:30 = 19800 s). The server needs it for "timestamp".
  configTime(19800, 0, "pool.ntp.org", "time.google.com");
  struct tm now;
  while (!getLocalTime(&now)) { delay(500); }
}

void loop() {
  struct tm now;
  if (WiFi.status() == WL_CONNECTED && getLocalTime(&now)) {
    char timestamp[32];
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%S+05:30", &now);

    char body[256];
    snprintf(body, sizeof(body),
             "{\"timestamp\":\"%s\",\"dissolved_oxygen\":%.2f,\"ph\":%.2f,"
             "\"temperature\":%.1f,\"ammonia\":%.3f,\"device\":\"esp32-%s\"}",
             timestamp, readOxygen(), readPH(), readTemperature(), readAmmonia(), POND_ID);

    WiFiClientSecure client;
    client.setInsecure();   // see the note below
    HTTPClient http;
    http.setTimeout(70000);  // a sleeping free Render app takes about a minute to wake up
    http.begin(client, String(SERVER) + "/api/sensor/" + POND_ID);
    http.addHeader("Content-Type", "application/json");
    http.addHeader("X-Sensor-Key", SENSOR_KEY);

    int status = http.POST(body);
    Serial.printf("%s -> %d %s\n", body, status, http.getString().c_str());
    // 201 = accepted. 422 = refused: the reply says why (e.g. "Check the sensor").
    http.end();
  }
  delay(SEND_EVERY_MS);
}
```

Notes:

- **`setInsecure()`** keeps the example short: the connection is still encrypted, but the
  ESP32 doesn't check that it is really talking to Render, so someone on the same network
  could pretend to be the server and read the key. For a real farm, replace it with
  `client.setCACert(...)` and the root certificate of the site.
- **Don't share the sketch with the key in it**, and don't commit it to git. If a key leaks,
  make a new one and change it on Render and on the ESP32.
- For a local test, use `http://<your laptop's IP>:8000` as `SERVER`, start uvicorn with
  `--host 0.0.0.0`, and use `WiFiClient` instead of `WiFiClientSecure`.
- One reading a minute is plenty for a pond: oxygen changes over hours, not seconds.

## 7. Try it with curl

```bash
curl -X POST https://meenuraksha.onrender.com/api/sensor/pond1 \
  -H "Content-Type: application/json" -H "X-Sensor-Key: <the pond1 key>" \
  -d '{"timestamp": "2026-10-10T21:30:00+05:30", "dissolved_oxygen": 4.2, "ph": 7.3, "temperature": 29}'
```

(Change the timestamp to the current time, or it is refused as too old.)
