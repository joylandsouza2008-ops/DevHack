# How MeenuRaksha works

A plain-words guide to the whole app: what each part does, which file does it, and questions judges
might ask. For the full details, follow the links to the other pages in `docs/`.

## The big picture

```
 readings (simulated pond, test kit, or a real sensor)
        │
        ▼
 risk rules ──► Safe / Warning / Danger + the reason, in Kannada and English
        │
        ├──► action checklist (what to do now, no chemicals)
        ├──► health score 0–100
        ├──► "time until danger" (if oxygen keeps falling)
        ├──► diseases made more likely by this reading
        └──► SMS / WhatsApp alert preview (nothing is really sent)

 weather forecast ──► tonight's oxygen crash risk (Low / Medium / High)
 disease guide    ──► symptom checker: "possible matches", never a diagnosis
 AI assistant     ──► answers questions using only the app's own content
```

The **server** (Python, FastAPI, in `backend/`) does all the thinking. The **page** (HTML and JavaScript, in
`frontend/`) shows the results. The page only gets data from our own server, plus the weather forecast.

---

## 1. Risk rules: Safe / Warning / Danger

**File:** `backend/risk_classifier.py`. **Numbers:** `config/thresholds.toml` (the only place they live).

The app checks each reading against fixed limits taken from FAO, TNAU and other fisheries sources:

| Reading | Safe | Warning | Danger |
|---|---|---|---|
| Dissolved oxygen | 5 mg/L or more | 3 to below 5 | below 3 |
| pH | 6.5–8.5 | 5.5–6.5 or 8.5–9.5 | below 5.5 or above 9.5 |
| Temperature | 25–32 °C | 20–25 or 32 to below 35 | below 20 or 35 and above |
| Ammonia (toxic NH3) | below 0.02 mg/L | up to 0.05 | above 0.05 |
| Nitrate | below 10 mg/L NO3-N | anything higher (there is no Danger level) | |

Step by step:
1. **Impossible values are thrown out** as sensor faults, e.g. oxygen of exactly 0 or a water temperature of 0 °C.
   The farmer sees "Check the sensor", not a false Danger.
2. **Units are converted where needed.** Sensors measure *total* ammonia, but only the NH3 part harms fish. How much
   of it is NH3 depends on pH and temperature, so the app works it out with a standard formula (Emerson et al. 1975).
3. **Each reading is graded:** inside the safe range → Safe, else inside the warning range → Warning, else Danger.
4. **The pond's level is the worst grade.** One reading in Danger makes the whole pond Danger.
5. **The reason is written in Kannada and English** (`backend/risk_messages.py`), for example "Oxygen is very low
   (2.5 mg/L)".

These are plain rules, not machine learning. That is on purpose: farmers and officers can check every limit
against its source (`docs/thresholds.md`).

After grading, three more things are built from the result:
- **Action checklist** (`backend/actions.py`): steps the farmer can tick off, such as "run the aerator" or "stop
  feeding". Each one comes from a source. There are no chemicals or doses.
- **Health score** (`backend/health_score.py`): one number from 0 to 100. Each level has its own range of scores
  (Safe 75–100, Warning 40–74, Danger 0–39), so the score can never disagree with the status.
- **Alert preview** (`backend/alerts.py`): the SMS or WhatsApp text the farmer would get for Warning or Danger. It is
  only a preview, and no message is sent.

## 2. Time until danger

**File:** `backend/time_to_danger.py`. **Details:** `docs/time_to_danger.md`.

Fish usually die in the early morning, after oxygen has been sliding down all night. This feature warns
*before* that point.

1. Take the oxygen readings from the last 2 hours (at least 4 readings covering at least 1 hour).
2. Draw the best straight line through them. Its slope tells how fast oxygen is falling, in mg/L per hour.
3. Check how well the points fit that line (a score called R², from 0 to 1). If the points just jump around
   (sensor noise) and the score is below 0.6, it is not counted as a fall.
4. If oxygen is falling faster than 0.3 mg/L per hour, extend the line to see when it reaches 3 mg/L (Danger).
   The app shows this only if it is less than 6 hours away, rounded to 10 minutes.

Example: *"Oxygen is falling (about 1.2 mg/L per hour). At this rate it may reach the danger level (3 mg/L) in about
2 hours, around 03:10. Get the aerator ready now."*

**Honest result:** in the simulated night crash, the first warning came 6 hours before Danger. On the real Kaggle
pond data it was **no better than chance**, because that data has no real gradual oxygen falls, only random sensor
jumps. It still needs testing on real sensor data.

**Why not a machine-learning forecast?** We trained one (`ml/train_do_forecast.py`), but it was usually off by about
4.5 mg/L. That is wider than the whole Warning band (3–5 mg/L), so it would mislead farmers. It is kept as an
experiment in `docs/do_forecast.md` and is **not shown** in the app.

## 3. Tonight's weather risk

**Files:** `backend/weather.py` (server) and `frontend/weather.js` (the same rules in the browser).
**Details:** `docs/night_crash.md`.

At night, algae stop making oxygen but everything in the pond keeps using it. Some weather makes this worse.
The app downloads the free Open-Meteo forecast for Mangaluru and counts three risk factors:

| Factor | Rule |
|---|---|
| Cloudy day | average cloud cover from 06:00 to 18:00 is 75 % or more (less sunlight, so less oxygen made in the day) |
| Still night | average wind at night is below 7 km/h (less air mixed into the water) |
| Warm night | average night air temperature is 28 °C or more (warm water holds less oxygen) |

0 factors → **Low**, 1 → **Medium**, 2 or 3 → **High** (*"keep the aerator ready"*).

The forecast is saved, so with no internet the app shows the last saved one and says it is offline. The phone
downloads the forecast itself, because the free Render server was often refused by the weather service. If that
fails, the phone asks our server.

This is **real** forecast data, not simulated.

## 4. Simulator (demo data)

**File:** `backend/simulator.py`.

We have no real pond sensors, so the demo pond's readings are **made up** by the simulator. Real ponds follow a
daily rhythm: oxygen rises with sunlight, peaks in the afternoon and falls through the night. The simulator makes
that rhythm, starting from the daily levels in the Kaggle Pondsdata file (or fixed typical levels if the file isn't
there, as on the online demo).

- Scenario **normal**: a healthy day, reads Safe.
- Scenario **oxygen_crash**: on the first night, oxygen slides down to Danger before dawn, then recovers.
  Warning comes hours before Danger, so the early warning can be shown.

The page plays it through `/api/simulator/stream`, one reading per second, each one 20 simulated minutes apart.

**Rules:** simulated data is always labelled **"Simulated data" / "ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಡೇಟಾ"** wherever it is
shown. It is never used to train a model or to report accuracy.

## 5. Sensor API (real sensors)

**Files:** `backend/sensor.py`, `backend/main.py`. **Details:** `docs/sensor-api.md`.

A real sensor box, such as an ESP32 with probes, can send readings to `POST /api/sensor/pond1` (or pond2, pond3).

1. **Key check.** Each pond has a secret key, kept only in a server environment variable (`SENSOR_KEY_POND1` …).
   The sensor sends the key in the `X-Sensor-Key` header. A wrong key is refused, and the check takes the same time
   for every wrong key, so it can't be guessed letter by letter.
2. **Clock check.** The timestamp must include a time zone, must not be in the future (5 minutes leeway), and must
   not be more than a day old.
3. **Value check.** Impossible values (or a broken probe sending "NaN") → the whole reading is refused with "Check
   the sensor", and the dashboard shows it.
4. **Store and show.** Good readings are graded by the same risk rules, kept in memory (the last 200 per pond), and
   pushed to the dashboard straight away through `/api/sensor/pond1/stream`.

Readings live in memory only, so they are lost when the free server sleeps or restarts. `tools/fake_sensor.py` is
a pretend sensor for demos. Its readings are labelled "Demo device".

## 6. Fish disease guide

**Files:** `backend/diseases.py`, `frontend/diseases.js`. **Details:** `docs/diseases.md`.

- **Library of 9 common carp-pond diseases** (EUS, Aeromonas or dropsy, gill rot, columnaris, cotton wool disease,
  fish louse, flukes, white spot, anchor worm). Each has its signs, when it is common, prevention and what to do,
  in English and Kannada, from FAO and published sources.
- **Symptom checker:** the farmer ticks the signs they see. Each disease gets 2 points per key sign and 1 point per
  other sign, and the top 3 are shown as **"possible matches"**. It is never a diagnosis.
- **"More likely now":** risky readings point to related diseases, e.g. low oxygen and high temperature.
- **Strict rules:** no medicine names, no chemicals, no doses. Every result says to confirm with a fisheries officer
  or KVK. `backend/safety.py` checks all text against a banned-word list.

**Why no photo check?** We tested one (`docs/fish-disease-baseline.md`). The honest score was 68 %, and much of that
came from the photo backgrounds, not the disease. It was never tested on Indian carp. That is not safe enough to
show farmers, so it stays research only.

## 7. AI assistant: "Ask MeenuRaksha"

**Files:** `backend/assistant.py`, `backend/ai_provider.py`, `backend/safety.py`, `frontend/assistant.js`.
**Details:** `docs/assistant.md`.

The farmer types a question in Kannada or English. Safety comes first:

1. **Questions asking for a medicine, chemical or dose are refused before the AI sees them.**
2. Otherwise the server builds a block of **our own content**: the current readings, the limits, the checklist,
   the disease guide and tonight's weather. The AI is told to answer **only** from that content, and to reply
   "UNKNOWN" if the answer isn't there. The app then shows "I don't know, please ask your fisheries officer."
3. **Every AI reply is checked.** A reply with a chemical name, an amount like "20 kg per acre", or a diagnosis like
   "your fish have EUS" is replaced with a safe answer.
4. Anything about disease gets "Please confirm with your fisheries officer / KVK" added at the end.
5. Each reply is labelled "AI assistant: can make mistakes", along with the data it used (e.g. "Simulated data").

The AI key is only on the server (an environment variable), never in the page. The provider can be swapped
(Gemini, Groq, OpenRouter). There are rate limits so the free quota can't be used up. With no key, no internet or
too many questions, **suggested questions with ready answers** built from our content still work, without any AI.

## 8. Security, in one paragraph

`backend/security.py` adds per-minute limits on the assistant and the sensor API, refuses requests over 32 KB, and
adds browser security headers (for example, the page may run only our own scripts). Text from the server or the
AI is always shown as plain text, so it can't run as code. Keys come only from environment variables. Full table:
`docs/security.md`.

---

## Which file does what

### Server (`backend/`)

| File | What it does |
|---|---|
| `main.py` | The web server: every API address (`/api/...`), and serves the page |
| `risk_classifier.py` | Readings → Safe / Warning / Danger, using `config/thresholds.toml` |
| `risk_messages.py` | The reason text, in English and Kannada |
| `actions.py` | The "what to do now" checklist (no chemicals) |
| `health_score.py` | The 0–100 health score |
| `alerts.py` | SMS / WhatsApp preview text (nothing is sent) |
| `time_to_danger.py` | "Time until danger" from the oxygen trend |
| `weather.py` | Tonight's oxygen crash risk from the Open-Meteo forecast |
| `simulator.py` | Made-up demo readings (normal day, night crash), always labelled simulated |
| `sensor.py` | Real sensor: key check, clock check, readings kept in memory |
| `diseases.py` | Disease guide, symptom checker, "more likely now" |
| `assistant.py` | The chat: our content, ready answers, safety, rate limit |
| `ai_provider.py` | Talks to the AI service; provider and key from environment variables |
| `safety.py` | Banned words (chemicals, doses) and diagnosis check, shared by the guide and chat |
| `security.py` | Rate limits, request size limit, security headers |
| `do_features.py`, `do_forecast.py` | The oxygen forecast experiment (not shown in the app) |

### Page (`frontend/`)

| File | What it does |
|---|---|
| `index.html` | The page layout |
| `styles.css`, `welcome.css`, `fonts/` | Look and feel (see `DESIGN.md`); fonts are stored locally so they work offline |
| `app.js` | The main dashboard: status, readings, checklist, alert preview, test kit, live sensor, history |
| `weather.js` | Downloads tonight's forecast and applies the crash-risk rules |
| `assistant.js` | The chat card |
| `diseases.js` | The disease guide and symptom checker |
| `history.js` | Past alerts, saved in the browser |
| `voice.js` | Reads an alert aloud when the farmer taps the speaker |
| `do-chart.js`, `gauge.js`, `health-ring.js`, `pond-view.js` | The oxygen chart, risk gauge, score ring and pond picture |
| `motion.js`, `cursor-fx.js`, `scene.js`, `welcome.js` | Animations (GSAP), the day/night sky, the welcome screen |
| `theme.js` | Picks light or dark before the page appears |
| `debug.js` | Counts for spotting slowdowns, only with `?debug` in the address |
| `vendor/` | GSAP and Chart.js, stored locally |

### Other folders

| Folder | What it holds |
|---|---|
| `config/thresholds.toml` | Every limit number, with its source |
| `ml/` | Training and test scripts for the experiments (oxygen forecast, time-until-danger check, disease photos) |
| `models/` | The saved oxygen-forecast model |
| `tools/` | `fake_sensor.py` (demo sensor), `kannada_review.py` (Kannada review sheet) |
| `tests/` | Automatic tests (`python -m pytest` and `node --test tests/js`) |
| `docs/` | Explanations, results, screenshots |

---

## 20 questions judges might ask

1. **Where is the machine learning?**
   The risk level uses clear rules from fisheries sources, because farmers need answers they can trust and check.
   We did train an oxygen forecast model (scikit-learn), but its typical error (±4.5 mg/L) was too big to show.
   We report that honestly in `docs/do_forecast.md`.

2. **Why trust your Safe / Warning / Danger limits?**
   Each one comes from FAO, TNAU or a published paper, or is marked as our judgement next to its source
   (`docs/thresholds.md`). They are all in one file, so an expert can change them without touching code.

3. **Is the dashboard data real?**
   The demo pond is **simulated**, and it is labelled "Simulated data" everywhere it appears. The weather forecast is
   real. Real readings can come from a test kit typed in by hand, or from a real sensor through the sensor API.

4. **Why simulate at all?**
   We have no sensors, and the public pond data is mostly sensor noise with no daily oxygen cycle, so it can't show
   what an early warning looks like. The simulator is never used for training or accuracy.

5. **How accurate is "time until danger"?**
   On the simulated crash it warned 6 hours ahead. On real Kaggle data it was no better than chance, because that
   data has no real gradual falls. We say this openly. It must be tested on real sensor data next.

6. **What happens with a broken sensor?**
   Impossible values (like oxygen 0 or "NaN") are refused with "Check the sensor", so they never cause a false alarm.
   Wrong clocks are refused too.

7. **Why does ammonia need pH and temperature?**
   Only the NH3 part of ammonia is toxic. The warmer and more alkaline the water, the more of it there is. We
   convert total ammonia to NH3 with a standard formula before grading.

8. **How does the weather warning work?**
   It counts three risk factors in the forecast: a cloudy day, a still night and a warm night. 0 means Low, 1 means
   Medium, 2 or more means High.

9. **Does it work without internet?**
   Mostly yes. Fonts and libraries are stored locally, the last forecast is saved, the alert history is saved in the
   browser, and the chat falls back to ready answers. Only fresh weather and the AI need internet.

10. **Can a farmer who can't read well use it?**
    Every alert is in Kannada and uses colour, icon and word together. A speaker button reads it aloud. The
    checklist gives simple steps.

11. **Does it send real SMS or WhatsApp messages?**
    No. It shows a preview of the message. Sending would need a paid SMS or WhatsApp service, which can be added
    later.

12. **Can the AI give dangerous advice?**
    Questions asking for chemicals or doses are refused before the AI sees them. Every reply is checked for chemical
    names, amounts and diagnoses, and replaced if it fails. The AI may only use our own content, and the chat is
    labelled "can make mistakes".

13. **What if someone tricks the AI ("ignore your rules")?**
    The rule check doesn't depend on the AI obeying. A dose question is refused before the AI, and an unsafe reply is
    replaced after it. We have tests for exactly this.

14. **Why don't you diagnose diseases from photos?**
    We tried. The honest score was 68 %, much of it from photo backgrounds, and it was never tested on Indian carp.
    A wrong diagnosis could lead to the wrong treatment, so the app shows "possible matches" from ticked signs and
    sends farmers to their fisheries officer.

15. **Why no medicine or dose advice?**
    Wrong chemicals or doses can kill fish and harm people. In India, treatment should come from a fisheries officer
    or KVK, so the app always points there.

16. **How would a real farmer connect a sensor?**
    An ESP32 with probes sends a reading every few seconds to `/api/sensor/pond1` with the pond's key. The steps and
    an example are in `docs/sensor-api.md`.

17. **Is it secure?**
    Keys live only in server environment variables, sensor keys are checked in a way that can't be guessed letter by
    letter, there are rate limits and security headers, and AI text can't run as code. See `docs/security.md`.

18. **What does it cost to run?**
    It runs on Render's free plan with the free Open-Meteo forecast. The AI uses a provider's free tier, with limits
    so the quota isn't used up. Note: the free plan sleeps after 15 minutes with no visitors (about 1 minute to wake
    up), and live readings are kept in memory only. We haven't priced sensor hardware yet.

19. **Is the Kannada correct?**
    All fixed Kannada text is collected in `docs/kannada-review.md` for a native-speaker review before release. AI
    chat replies in Kannada are not covered by that review, which is one more reason the chat is labelled "can make
    mistakes".

20. **What would you do next?**
    Test with real sensors in a real pond and check "time until danger" on real night-time oxygen falls. Then send
    real SMS alerts, add more locations for the weather, and get the Kannada and the advice reviewed by fisheries
    officers.
