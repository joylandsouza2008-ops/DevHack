# Kannada text review

Every Kannada string in AquaNexus, next to its English version, grouped by screen.
Please check each Kannada line is correct, natural and easy for a small fish farmer in
coastal Karnataka to understand. Write any fix in the last column.

- Words in `{curly brackets}` are filled in by the app (numbers, times, names). Please keep them.
- `A  /  B` means the app shows one of two versions, depending on the situation.
- Unit symbols (mg/L, °C, km/h, pH) and the names SMS, WhatsApp, FAO, TNAU, Open-Meteo stay in English.

687 strings. Generated from the code by `python tools/kannada_review.py`; re-run it after changing any text.

## 1. Language and theme switches

Button and screen-reader labels in index.html.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `index.html language button` | English | ಕನ್ನಡ |  |
| 2 | `index.html aria-label` | Language | ಭಾಷೆ |  |
| 3 | `index.html aria-label` | Theme | ಬಣ್ಣ |  |

## 2. Welcome screen

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js welcomeTagline` | Pond water warnings before your fish are in danger. | ಮೀನುಗಳಿಗೆ ಅಪಾಯ ಬರುವ ಮೊದಲೇ ಕೊಳದ ನೀರಿನ ಎಚ್ಚರಿಕೆ. |  |
| 2 | `app.js welcomeExample` | What a warning looks like | ಎಚ್ಚರಿಕೆ ಹೀಗೆ ಕಾಣುತ್ತದೆ |  |
| 3 | `app.js welcomeExampleLevel` | Warning | ಎಚ್ಚರಿಕೆ |  |
| 4 | `app.js welcomeExampleText` | Pond 1: oxygen is low (3.8 mg/L). Run the aerator tonight. | ಕೊಳ 1: ಆಮ್ಲಜನಕ ಕಡಿಮೆ ಇದೆ (3.8 mg/L). ಇಂದು ರಾತ್ರಿ ಏರೇಟರ್ ಚಾಲೂ ಇಡಿ. |  |
| 5 | `app.js start` | Start | ಪ್ರಾರಂಭಿಸಿ |  |
| 6 | `app.js builtBy` | Built by Team Orbit | ನಿರ್ಮಾಣ: ಟೀಮ್ ಆರ್ಬಿಟ್ |  |

## 3. Pond scene (sky label)

Shown over the day/night pond picture.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `scene.js PHASE_WORDS.night` | Night | ರಾತ್ರಿ |  |
| 2 | `scene.js PHASE_WORDS.dawn` | Sunrise | ಸೂರ್ಯೋದಯ |  |
| 3 | `scene.js PHASE_WORDS.day` | Daytime | ಹಗಲು |  |
| 4 | `scene.js PHASE_WORDS.dusk` | Sunset | ಸೂರ್ಯಾಸ್ತ |  |

## 4. Top bar and demo controls

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js tagline` | Pond water early warning | ಕೊಳದ ನೀರಿನ ಮುನ್ನೆಚ್ಚರಿಕೆ |  |
| 2 | `app.js themeLight` | Light | ತಿಳಿ |  |
| 3 | `app.js themeDark` | Dark | ಗಾಢ |  |
| 4 | `app.js simulatedNote` | Not a real pond. For demonstration only. | ನಿಜವಾದ ಕೊಳವಲ್ಲ. ಪ್ರದರ್ಶನಕ್ಕಾಗಿ ಮಾತ್ರ. |  |
| 5 | `app.js pond` | Pond | ಕೊಳ |  |
| 6 | `app.js pond1` | Pond 1 | ಕೊಳ 1 |  |
| 7 | `app.js pond2` | Pond 2 | ಕೊಳ 2 |  |
| 8 | `app.js pond3` | Pond 3 | ಕೊಳ 3 |  |
| 9 | `app.js scenario` | Scenario | ಸನ್ನಿವೇಶ |  |
| 10 | `app.js scenarioNormal` | Normal day | ಸಾಮಾನ್ಯ ದಿನ |  |
| 11 | `app.js scenarioCrash` | Night oxygen crash | ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕುಸಿತ |  |
| 12 | `app.js restart` | Restart | ಮರುಪ್ರಾರಂಭಿಸಿ |  |
| 13 | `app.js pause` | Pause | ವಿರಾಮ |  |
| 14 | `app.js resume` | Resume | ಮುಂದುವರಿಸಿ |  |
| 15 | `app.js simTime` | Simulated time | ಅನುಕರಿಸಿದ ಸಮಯ |  |
| 16 | `app.js connecting` | Connecting… | ಸಂಪರ್ಕಿಸಲಾಗುತ್ತಿದೆ… |  |
| 17 | `app.js ended` | Demo finished. Press Restart to play again. | ಪ್ರದರ್ಶನ ಮುಗಿದಿದೆ. ಮತ್ತೆ ನೋಡಲು ಮರುಪ್ರಾರಂಭಿಸಿ ಒತ್ತಿ. |  |
| 18 | `app.js connectionLost` | Connection lost. Press Restart. | ಸಂಪರ್ಕ ಕಡಿದುಹೋಗಿದೆ. ಮರುಪ್ರಾರಂಭಿಸಿ ಒತ್ತಿ. |  |
| 19 | `app.js pondViewTitle` | Pond view | ಕೊಳದ ನೋಟ |  |
| 20 | `app.js pondCaption.safe` | Fish are swimming normally. | ಮೀನುಗಳು ಸಾಮಾನ್ಯವಾಗಿ ಈಜುತ್ತಿವೆ. |  |
| 21 | `app.js pondCaption.warning` | Fish are slowing down. | ಮೀನುಗಳು ನಿಧಾನವಾಗಿ ಈಜುತ್ತಿವೆ. |  |
| 22 | `app.js pondCaption.danger` | Fish are gasping for air at the surface. | ಮೀನುಗಳು ಮೇಲ್ಮೈಗೆ ಬಂದು ಗಾಳಿಗಾಗಿ ಒದ್ದಾಡುತ್ತಿವೆ. |  |
| 23 | `app.js pondCaption.unknown` | Waiting for readings. | ಅಳತೆಗಳಿಗಾಗಿ ಕಾಯಲಾಗುತ್ತಿದೆ. |  |
| 24 | `app.js simulatedTag` | Simulated data | ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಡೇಟಾ |  |
| 25 | `app.js pondsTitle` | My ponds | ನನ್ನ ಕೊಳಗಳು |  |
| 26 | `app.js pondAdd` | Add pond | ಕೊಳ ಸೇರಿಸಿ |  |
| 27 | `app.js pondsDemoMode` | Demo mode: ponds reset when the server sleeps. | ಡೆಮೊ ಮೋಡ್: ಸರ್ವರ್ ನಿದ್ರಿಸಿದಾಗ ಕೊಳಗಳು ಅಳಿಸಿಹೋಗುತ್ತವೆ. |  |
| 28 | `app.js pondsEmpty` | Add your ponds, then connect a device to see live readings from each one. | ನಿಮ್ಮ ಕೊಳಗಳನ್ನು ಸೇರಿಸಿ, ನಂತರ ಪ್ರತಿಯೊಂದರ ಲೈವ್ ಅಳತೆಗಳನ್ನು ನೋಡಲು ಸಾಧನವನ್ನು ಸಂಪರ್ಕಿಸಿ. |  |
| 29 | `app.js pondsLoadFailed` | Could not load your ponds. Check your internet. | ನಿಮ್ಮ ಕೊಳಗಳನ್ನು ತೆರೆಯಲು ಆಗಲಿಲ್ಲ. ಇಂಟರ್ನೆಟ್ ಪರಿಶೀಲಿಸಿ. |  |
| 30 | `app.js pondNoReadings` | No readings yet | ಇನ್ನೂ ಅಳತೆಗಳಿಲ್ಲ |  |
| 31 | `app.js pondLastReading` | Last reading: {t} | ಕೊನೆಯ ಅಳತೆ: {t} |  |
| 32 | `app.js pondConnectFirst` | Connect a device to see this pond's readings. | ಈ ಕೊಳದ ಅಳತೆಗಳನ್ನು ನೋಡಲು ಸಾಧನವನ್ನು ಸಂಪರ್ಕಿಸಿ. |  |
| 33 | `app.js pondBack` | All ponds | ಎಲ್ಲಾ ಕೊಳಗಳು |  |
| 34 | `app.js pondEdit` | Edit | ಬದಲಿಸಿ |  |
| 35 | `app.js pondDelete` | Delete pond | ಕೊಳ ಅಳಿಸಿ |  |
| 36 | `app.js pondDeleteConfirm` | Delete "{n}" with its device, readings and alerts? | "{n}" ಅನ್ನು ಅದರ ಸಾಧನ, ಅಳತೆಗಳು ಮತ್ತು ಎಚ್ಚರಿಕೆಗಳೊಂದಿಗೆ ಅಳಿಸಬೇಕೇ? |  |
| 37 | `app.js pondNotFound` | Pond not found | ಕೊಳ ಸಿಗಲಿಲ್ಲ |  |
| 38 | `app.js pondNotFoundHelp` | This pond is not in your farm. It may have been deleted, or it belongs to another farm code. | ಈ ಕೊಳ ನಿಮ್ಮ ಫಾರ್ಮ್‌ನಲ್ಲಿಲ್ಲ. ಅದನ್ನು ಅಳಿಸಿರಬಹುದು, ಅಥವಾ ಅದು ಬೇರೆ ಫಾರ್ಮ್ ಕೋಡ್‌ಗೆ ಸೇರಿರಬಹುದು. |  |
| 39 | `app.js pondSize` | Size | ಗಾತ್ರ |  |
| 40 | `app.js pondFish` | Fish | ಮೀನು |  |
| 41 | `app.js pondPlaceLabel` | Where is the pond? | ಕೊಳ ಎಲ್ಲಿದೆ? |  |
| 42 | `app.js pondDistrictLabel` | District | ಜಿಲ್ಲೆ |  |
| 43 | `app.js pondVillageLabel` | Taluk / village | ತಾಲ್ಲೂಕು / ಊರು |  |
| 44 | `app.js pondPlaceHelp` | For tonight's weather at the pond. Only the village name is saved: no GPS, no address. | ಕೊಳದ ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನಕ್ಕಾಗಿ. ಊರಿನ ಹೆಸರು ಮಾತ್ರ ಉಳಿಸಲಾಗುತ್ತದೆ: GPS ಇಲ್ಲ, ವಿಳಾಸ ಇಲ್ಲ. |  |
| 45 | `app.js pondDistrictNone` | Not chosen | ಆರಿಸಿಲ್ಲ |  |
| 46 | `app.js pondVillageNone` | Choose taluk / village | ತಾಲ್ಲೂಕು / ಊರು ಆರಿಸಿ |  |
| 47 | `app.js pondVillageFirst` | Choose a district first | ಮೊದಲು ಜಿಲ್ಲೆ ಆರಿಸಿ |  |
| 48 | `app.js pondTaluk` | {t} taluk | {t} ತಾಲ್ಲೂಕು |  |
| 49 | `app.js pondVillageMissing` | Choose the taluk / village too, or set the district back to "Not chosen". | ತಾಲ್ಲೂಕು / ಊರನ್ನೂ ಆರಿಸಿ, ಅಥವಾ ಜಿಲ್ಲೆಯನ್ನು "ಆರಿಸಿಲ್ಲ" ಗೆ ಹಿಂತಿರುಗಿಸಿ. |  |
| 50 | `app.js pondWeatherNoPlace` | Choose where this pond is to see tonight's weather for its village. | ಈ ಕೊಳದ ಊರಿನ ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ ನೋಡಲು, ಕೊಳ ಎಲ್ಲಿದೆ ಎಂದು ಆರಿಸಿ. |  |
| 51 | `app.js pondWeatherChoose` | Choose the village | ಊರು ಆರಿಸಿ |  |
| 52 | `app.js pondReadingsTitle` | Readings | ಅಳತೆಗಳು |  |
| 53 | `app.js pondChartTitle` | Oxygen, last 12 hours | ಆಮ್ಲಜನಕ, ಕಳೆದ 12 ಗಂಟೆಗಳು |  |
| 54 | `app.js pondChartOxygen` | Oxygen (mg/L) | ಆಮ್ಲಜನಕ (mg/L) |  |
| 55 | `app.js pondChartWarnLine` | Warning below 5 | 5 ಕ್ಕಿಂತ ಕಡಿಮೆ: ಎಚ್ಚರಿಕೆ |  |
| 56 | `app.js pondChartDangerLine` | Danger below 3 | 3 ಕ್ಕಿಂತ ಕಡಿಮೆ: ಅಪಾಯ |  |
| 57 | `app.js pondChartSummary` | Oxygen went from {a} to {b} mg/L over the last {n} readings. | ಕೊನೆಯ {n} ಅಳತೆಗಳಲ್ಲಿ ಆಮ್ಲಜನಕ {a} ರಿಂದ {b} mg/L ಗೆ ಬದಲಾಗಿದೆ. |  |
| 58 | `app.js pondChartNone` | Not enough oxygen readings for a chart yet. | ಚಾರ್ಟ್‌ಗೆ ಇನ್ನೂ ಸಾಕಷ್ಟು ಆಮ್ಲಜನಕ ಅಳತೆಗಳಿಲ್ಲ. |  |
| 59 | `app.js pondDialogAdd` | Add a pond | ಕೊಳ ಸೇರಿಸಿ |  |
| 60 | `app.js pondDialogEdit` | Edit pond | ಕೊಳವನ್ನು ಬದಲಿಸಿ |  |
| 61 | `app.js pondNameLabel` | Pond name | ಕೊಳದ ಹೆಸರು |  |
| 62 | `app.js pondNameHelp` | For example: Pond near road. Don't use your own name or phone number. | ಉದಾ: ರಸ್ತೆ ಬದಿಯ ಕೊಳ. ನಿಮ್ಮ ಸ್ವಂತ ಹೆಸರು ಅಥವಾ ಫೋನ್ ಸಂಖ್ಯೆ ಬಳಸಬೇಡಿ. |  |
| 63 | `app.js pondSizeLabel` | Size (optional) | ಗಾತ್ರ (ಐಚ್ಛಿಕ) |  |
| 64 | `app.js pondSizeHelp` | For example: 0.5 acre | ಉದಾ: 0.5 ಎಕರೆ |  |
| 65 | `app.js pondFishLabel` | Fish type (optional) | ಮೀನಿನ ಪ್ರಕಾರ (ಐಚ್ಛಿಕ) |  |
| 66 | `app.js pondFishHelp` | For example: rohu, catla | ಉದಾ: ರೋಹು, ಕಾಟ್ಲಾ |  |
| 67 | `app.js pondSave` | Save | ಉಳಿಸಿ |  |
| 68 | `app.js pondCancel` | Cancel | ರದ್ದುಮಾಡಿ |  |
| 69 | `app.js pondNameMissing` | Type a name for the pond. | ಕೊಳಕ್ಕೆ ಹೆಸರು ಬರೆಯಿರಿ. |  |
| 70 | `app.js pondSaveFailed` | Could not save. Check your internet and try again. | ಉಳಿಸಲು ಆಗಲಿಲ್ಲ. ಇಂಟರ್ನೆಟ್ ಪರಿಶೀಲಿಸಿ, ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ. |  |
| 71 | `app.js pondAlertsTitle` | Alerts from my ponds | ನನ್ನ ಕೊಳಗಳ ಎಚ್ಚರಿಕೆಗಳು |  |
| 72 | `app.js pondAlertsHelp` | From your own devices, newest first. | ನಿಮ್ಮ ಸ್ವಂತ ಸಾಧನಗಳಿಂದ, ಹೊಸದು ಮೊದಲು. |  |
| 73 | `app.js pondAlertsEmpty` | No warnings from your ponds yet. | ನಿಮ್ಮ ಕೊಳಗಳಿಂದ ಇನ್ನೂ ಎಚ್ಚರಿಕೆಗಳಿಲ್ಲ. |  |

## 5. Pond view, risk level and readings

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js gaugeTitle` | Risk level | ಅಪಾಯದ ಮಟ್ಟ |  |
| 2 | `app.js readingsTitle` | Latest readings | ಇತ್ತೀಚಿನ ಅಳತೆಗಳು |  |
| 3 | `app.js infoOnly` | For information | ಮಾಹಿತಿಗಾಗಿ |  |

## 6. Time until danger and oxygen chart

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js ttdTitle` | Time until danger | ಅಪಾಯದವರೆಗಿನ ಸಮಯ |  |
| 2 | `app.js countdownLabel` | Danger expected in | ಅಪಾಯಕ್ಕೆ ಉಳಿದ ಸಮಯ |  |
| 3 | `app.js chartTitle` | Dissolved oxygen, last 12 hours | ಕರಗಿದ ಆಮ್ಲಜನಕ, ಕಳೆದ 12 ಗಂಟೆಗಳು |  |
| 4 | `app.js duration` | {h} h {m} min  /  {m} min | {h} ಗಂಟೆ {m} ನಿಮಿಷ  /  {m} ನಿಮಿಷ |  |
| 5 | `app.js around` | around {clock} | ಸುಮಾರು {clock} ಹೊತ್ತಿಗೆ |  |
| 6 | `app.js chartSummary` | Now {now} mg/L. Lowest in this period: {min} mg/L. | ಈಗ {now} mg/L. ಈ ಅವಧಿಯ ಕನಿಷ್ಠ: {min} mg/L. |  |

## 7. Pond health score

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js healthTitle` | Pond health score | ಕೊಳದ ಆರೋಗ್ಯ ಅಂಕ |  |
| 2 | `app.js healthScale` | Safe 75‑100 · Warning 40‑74 · Danger 0‑39 | ಸುರಕ್ಷಿತ 75‑100 · ಎಚ್ಚರಿಕೆ 40‑74 · ಅಪಾಯ 0‑39 |  |
| 3 | `app.js healthText.safe` | {s} out of 100. All readings are in the safe range. | 100 ರಲ್ಲಿ {s}. ಎಲ್ಲಾ ಅಳತೆಗಳು ಸುರಕ್ಷಿತ ಮಟ್ಟದಲ್ಲಿವೆ. |  |
| 4 | `app.js healthText.warning` | {s} out of 100. The water needs attention. | 100 ರಲ್ಲಿ {s}. ನೀರಿನ ಕಡೆ ಗಮನ ಕೊಡಿ. |  |
| 5 | `app.js healthText.danger` | {s} out of 100. The water is dangerous for fish. | 100 ರಲ್ಲಿ {s}. ನೀರು ಮೀನುಗಳಿಗೆ ಅಪಾಯಕಾರಿಯಾಗಿದೆ. |  |
| 6 | `app.js healthText.unknown` | Waiting for readings. | ಅಳತೆಗಳಿಗಾಗಿ ಕಾಯಲಾಗುತ್ತಿದೆ. |  |

## 8. Tonight's weather

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js weatherTitle` | Tonight's weather | ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ |  |
| 2 | `app.js weatherLoading` | Checking the forecast… | ಮುನ್ಸೂಚನೆ ನೋಡಲಾಗುತ್ತಿದೆ… |  |
| 3 | `app.js weatherUnavailable` | No internet and no saved forecast. Tonight's weather is not known. | ಇಂಟರ್ನೆಟ್ ಇಲ್ಲ, ಉಳಿಸಿದ ಮುನ್ಸೂಚನೆಯೂ ಇಲ್ಲ. ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ ತಿಳಿದಿಲ್ಲ. |  |
| 4 | `app.js crashRisk` | Oxygen crash risk: {level} | ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯ: {level} |  |
| 5 | `app.js weatherDetails` | Day cloud {c}% · Night wind {w} km/h · Night {t} °C · Forecast: Open-Meteo | ಹಗಲಿನ ಮೋಡ {c}% · ರಾತ್ರಿ ಗಾಳಿ {w} km/h · ರಾತ್ರಿ {t} °C · ಮುನ್ಸೂಚನೆ: Open-Meteo |  |
| 6 | `app.js weatherOffline` | No connection: showing the forecast saved on {when}.  /  No connection. | ಸಂಪರ್ಕ ಇಲ್ಲ: {when} ರಂದು ಉಳಿಸಿದ ಮುನ್ಸೂಚನೆ ತೋರಿಸಲಾಗುತ್ತಿದೆ.  /  ಸಂಪರ್ಕ ಇಲ್ಲ. |  |
| 7 | `app.js weatherUpdated` | Updated just now  /  Updated {min} min ago  /  Updated ${Math.floor(min / 60)} h ago | ಈಗಷ್ಟೇ ನವೀಕರಿಸಲಾಗಿದೆ  /  {min} ನಿಮಿಷ ಹಿಂದೆ ನವೀಕರಿಸಲಾಗಿದೆ  /  ${Math.floor(min / 60)} ಗಂಟೆ ಹಿಂದೆ ನವೀಕರಿಸಲಾಗಿದೆ |  |
| 8 | `app.js weatherDemoNote` | This is the weather for the demo pond, in Mangaluru. Each of your own ponds shows the weather for its village on its page. | ಇದು ಮಂಗಳೂರಿನಲ್ಲಿರುವ ಡೆಮೊ ಕೊಳದ ಹವಾಮಾನ. ನಿಮ್ಮ ಪ್ರತಿ ಕೊಳದ ಪುಟದಲ್ಲಿ ಅದರ ಊರಿನ ಹವಾಮಾನ ಕಾಣುತ್ತದೆ. |  |
| 9 | `app.js weatherWhyTitle` | Why the weather matters | ಹವಾಮಾನ ಏಕೆ ಮುಖ್ಯ |  |
| 10 | `app.js weatherWhy` | Water plants make oxygen only in sunlight. After a cloudy day, on a calm, warm night, they use up oxygen and no wind mixes in fresh air, so oxygen is lowest just before sunrise. That is when fish die. | ನೀರಿನ ಸಸ್ಯಗಳು ಬಿಸಿಲಿನಲ್ಲಿ ಮಾತ್ರ ಆಮ್ಲಜನಕ ತಯಾರಿಸುತ್ತವೆ. ಮೋಡ ಕವಿದ ದಿನದ ನಂತರ, ಗಾಳಿ ಇಲ್ಲದ ಬೆಚ್ಚಗಿನ ರಾತ್ರಿಯಲ್ಲಿ ಅವು ಆಮ್ಲಜನಕವನ್ನು ಬಳಸಿಕೊಳ್ಳುತ್ತವೆ, ಹೊಸ ಗಾಳಿ ನೀರಿಗೆ ಬೆರೆಯುವುದಿಲ್ಲ. ಆದ್ದರಿಂದ ಸೂರ್ಯೋದಯಕ್ಕೆ ಸ್ವಲ್ಪ ಮೊದಲು ಆಮ್ಲಜನಕ ಅತ್ಯಂತ ಕಡಿಮೆ ಇರುತ್ತದೆ. ಆಗಲೇ ಮೀನುಗಳು ಸಾಯುತ್ತವೆ. |  |

## 9. What to do now (checklist)

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js actionsTitle` | What to do now | ಈಗ ಏನು ಮಾಡಬೇಕು |  |
| 2 | `app.js actionsSource` | Based on FAO, TNAU and university extension guides. No chemicals. | FAO, TNAU ಮತ್ತು ವಿಶ್ವವಿದ್ಯಾಲಯದ ಕೃಷಿ ವಿಸ್ತರಣಾ ಮಾರ್ಗದರ್ಶಿಗಳನ್ನು ಆಧರಿಸಿದೆ. ಯಾವುದೇ ರಾಸಾಯನಿಕಗಳಿಲ್ಲ. |  |
| 3 | `app.js actionsProgress` | All {total} done.  /  {done} of {total} done | ಎಲ್ಲಾ {total} ಮುಗಿದಿವೆ.  /  {total} ರಲ್ಲಿ {done} ಮುಗಿದಿದೆ |  |

## 10. Alert preview (SMS / WhatsApp)

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js alertTitle` | Alert preview | ಎಚ್ಚರಿಕೆ ಸಂದೇಶದ ಮುನ್ನೋಟ |  |
| 2 | `app.js previewNote` | Preview only. No real SMS or WhatsApp message is sent. | ಮುನ್ನೋಟ ಮಾತ್ರ. ಯಾವುದೇ ನಿಜವಾದ SMS ಅಥವಾ WhatsApp ಸಂದೇಶ ಕಳುಹಿಸುವುದಿಲ್ಲ. |  |
| 3 | `app.js alertFor` | Alert for | ಯಾವುದಕ್ಕೆ ಎಚ್ಚರಿಕೆ |  |
| 4 | `app.js alertForSim` | Simulated | ಅನುಕರಿಸಿದ |  |
| 5 | `app.js alertForSensor` | Live sensor | ಲೈವ್ ಸೆನ್ಸರ್ |  |
| 6 | `app.js alertForKit` | Test kit | ಟೆಸ್ಟ್ ಕಿಟ್ |  |
| 7 | `app.js alertsCalm` | Nothing to do now. Steps appear here when the pond has a Warning or Danger. | ಈಗ ಮಾಡಬೇಕಾದ್ದು ಏನೂ ಇಲ್ಲ. ಕೊಳದಲ್ಲಿ ಎಚ್ಚರಿಕೆ ಅಥವಾ ಅಪಾಯ ಬಂದಾಗ ಹಂತಗಳು ಇಲ್ಲಿ ಕಾಣಿಸುತ್ತವೆ. |  |

## 11. Test-kit readings

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js kitTitle` | Enter test-kit readings | ಟೆಸ್ಟ್ ಕಿಟ್ ಅಳತೆಗಳನ್ನು ನಮೂದಿಸಿ |  |
| 2 | `app.js kitHelp` | Type the numbers from your pond test kit. Leave a box empty if you did not test it. | ನಿಮ್ಮ ಕೊಳದ ಟೆಸ್ಟ್ ಕಿಟ್‌ನ ಸಂಖ್ಯೆಗಳನ್ನು ಬರೆಯಿರಿ. ಪರೀಕ್ಷಿಸದಿದ್ದರೆ ಆ ಡಬ್ಬಿಯನ್ನು ಖಾಲಿ ಬಿಡಿ. |  |
| 3 | `app.js kitDO` | Dissolved oxygen | ಕರಗಿದ ಆಮ್ಲಜನಕ |  |
| 4 | `app.js kitNoUnit` | no unit | ಘಟಕ ಇಲ್ಲ |  |
| 5 | `app.js kitTemp` | Water temperature | ನೀರಿನ ತಾಪಮಾನ |  |
| 6 | `app.js kitAmmonia` | Total ammonia | ಒಟ್ಟು ಅಮೋನಿಯಾ |  |
| 7 | `app.js kitCheck` | Check readings | ಅಳತೆ ಪರಿಶೀಲಿಸಿ |  |
| 8 | `app.js kitClear` | Clear | ಅಳಿಸಿ |  |
| 9 | `app.js kitEmpty` | Enter at least one reading. | ಕನಿಷ್ಠ ಒಂದು ಅಳತೆ ನಮೂದಿಸಿ. |  |
| 10 | `app.js kitBadNumber` | Use numbers only, like 6.5. | ಸಂಖ್ಯೆಗಳನ್ನು ಮಾತ್ರ ಬರೆಯಿರಿ, ಉದಾ: 6.5. |  |
| 11 | `app.js kitFailed` | Could not check the readings. Please try again. | ಅಳತೆ ಪರಿಶೀಲಿಸಲು ಆಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ. |  |

## 12. Live sensor

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js liveSensorHint` | Waiting for a sensor. Run the demo sensor. | ಸೆನ್ಸರ್‌ಗಾಗಿ ಕಾಯಲಾಗುತ್ತಿದೆ. ಡೆಮೊ ಸೆನ್ಸರ್ ಚಲಾಯಿಸಿ. |  |
| 2 | `app.js liveTitle` | Live sensor | ಲೈವ್ ಸೆನ್ಸರ್ |  |
| 3 | `app.js liveWaiting` | Connecting to the live sensor… | ಲೈವ್ ಸೆನ್ಸರ್‌ಗೆ ಸಂಪರ್ಕಿಸಲಾಗುತ್ತಿದೆ… |  |
| 4 | `app.js liveNoReading` | No reading from the {pond} sensor yet. Readings appear here as soon as the sensor sends one. | {pond} ಸೆನ್ಸರ್‌ನಿಂದ ಇನ್ನೂ ಯಾವುದೇ ಅಳತೆ ಬಂದಿಲ್ಲ. ಸೆನ್ಸರ್ ಅಳತೆ ಕಳುಹಿಸಿದ ತಕ್ಷಣ ಇಲ್ಲಿ ಕಾಣಿಸುತ್ತದೆ. |  |
| 5 | `app.js liveMeasured` | Measured {when} · received {ago} | ಅಳತೆ ಸಮಯ {when} · {ago} ಬಂದಿದೆ |  |
| 6 | `app.js liveAgo` | {s} s ago  /  ${Math.floor(s / 60)} min ago | {s} ಸೆಕೆಂಡ್ ಹಿಂದೆ  /  ${Math.floor(s / 60)} ನಿಮಿಷ ಹಿಂದೆ |  |
| 7 | `app.js liveStale` | No new reading for {min} min. Check the sensor's power and Wi-Fi. | {min} ನಿಮಿಷಗಳಿಂದ ಹೊಸ ಅಳತೆ ಬಂದಿಲ್ಲ. ಸೆನ್ಸರ್‌ನ ವಿದ್ಯುತ್ ಮತ್ತು Wi-Fi ಪರಿಶೀಲಿಸಿ. |  |
| 8 | `app.js liveLost` | Lost connection to the server. Trying again… | ಸರ್ವರ್ ಸಂಪರ್ಕ ಕಡಿದುಹೋಗಿದೆ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಲಾಗುತ್ತಿದೆ… |  |
| 9 | `app.js liveNote` | Demo readings are kept in the server's memory only. They are cleared when the server sleeps or restarts. | ಡೆಮೊ ಅಳತೆಗಳು ಸರ್ವರ್‌ನ ಮೆಮೊರಿಯಲ್ಲಿ ಮಾತ್ರ ಇರುತ್ತವೆ. ಅವು ಸರ್ವರ್ ನಿದ್ರಿಸಿದಾಗ ಅಥವಾ ಮರುಪ್ರಾರಂಭವಾದಾಗ ಅಳಿಸಿಹೋಗುತ್ತವೆ. |  |

## 13. Fish disease guide (page labels)

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js guideTitle` | Fish disease guide | ಮೀನು ರೋಗ ಮಾರ್ಗದರ್ಶಿ |  |
| 2 | `app.js guideIntro` | Common diseases of carp ponds: the signs to look for, when they happen and how to prevent them. | ಗೆಂಡೆ ಮೀನಿನ ಕೊಳಗಳ ಸಾಮಾನ್ಯ ರೋಗಗಳು: ಗಮನಿಸಬೇಕಾದ ಲಕ್ಷಣಗಳು, ಅವು ಯಾವಾಗ ಬರುತ್ತವೆ ಮತ್ತು ಹೇಗೆ ತಡೆಯುವುದು. |  |
| 3 | `app.js guideLoading` | Loading the guide… | ಮಾರ್ಗದರ್ಶಿ ತೆರೆಯಲಾಗುತ್ತಿದೆ… |  |
| 4 | `app.js guideFailed` | Could not load the disease guide. Please try again. | ರೋಗ ಮಾರ್ಗದರ್ಶಿ ತೆರೆಯಲು ಆಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ. |  |
| 5 | `app.js guideDrawing` | drawing of a fish with the signs | ಲಕ್ಷಣಗಳಿರುವ ಮೀನಿನ ಚಿತ್ರ |  |
| 6 | `app.js guideAgent` | Cause | ಕಾರಣ |  |
| 7 | `app.js guideBody` | Signs on the body | ದೇಹದ ಮೇಲಿನ ಲಕ್ಷಣಗಳು |  |
| 8 | `app.js guideBehaviour` | How the fish behave | ಮೀನುಗಳ ವರ್ತನೆ |  |
| 9 | `app.js guideWhen` | When it is most common | ಯಾವಾಗ ಹೆಚ್ಚು ಬರುತ್ತದೆ |  |
| 10 | `app.js guidePrevention` | Prevention | ತಡೆಗಟ್ಟುವಿಕೆ |  |
| 11 | `app.js guideDo` | What to do | ಏನು ಮಾಡಬೇಕು |  |
| 12 | `app.js guideSourcesShort` | Sources | ಮೂಲಗಳು |  |
| 13 | `app.js guideRead` | Read about it | ಇದರ ಬಗ್ಗೆ ಓದಿ |  |
| 14 | `app.js guideSources` | Sources for every entry | ಪ್ರತಿ ಮಾಹಿತಿಯ ಮೂಲಗಳು |  |
| 15 | `app.js checkerTitle` | Symptom checker | ಲಕ್ಷಣ ಪರಿಶೀಲಕ |  |
| 16 | `app.js checkerHelp` | Tick the signs you see on your fish. You get possible matches, not a diagnosis. | ನಿಮ್ಮ ಮೀನುಗಳಲ್ಲಿ ಕಾಣುವ ಲಕ್ಷಣಗಳನ್ನು ಗುರುತಿಸಿ. ನಿಮಗೆ ಸಾಧ್ಯವಿರುವ ಹೊಂದಾಣಿಕೆಗಳು ಸಿಗುತ್ತವೆ, ರೋಗನಿರ್ಣಯವಲ್ಲ. |  |
| 17 | `app.js checkerBody` | On the body | ದೇಹದ ಮೇಲೆ |  |
| 18 | `app.js checkerBehaviour` | How the fish behave | ಮೀನುಗಳ ವರ್ತನೆ |  |
| 19 | `app.js checkerCheck` | Show possible matches | ಸಾಧ್ಯವಿರುವ ಹೊಂದಾಣಿಕೆಗಳನ್ನು ತೋರಿಸಿ |  |
| 20 | `app.js checkerClear` | Clear | ಅಳಿಸಿ |  |
| 21 | `app.js checkerEmpty` | Tick at least one sign. | ಕನಿಷ್ಠ ಒಂದು ಲಕ್ಷಣ ಗುರುತಿಸಿ. |  |
| 22 | `app.js checkerMatches` | Possible matches | ಸಾಧ್ಯವಿರುವ ಹೊಂದಾಣಿಕೆಗಳು |  |
| 23 | `app.js checkerMatched` | Matching signs | ಹೊಂದುವ ಲಕ್ಷಣಗಳು |  |
| 24 | `app.js checkerMore` | {n} more diseases match fewer of your signs. | ಇನ್ನೂ {n} ರೋಗಗಳು ನಿಮ್ಮ ಕಡಿಮೆ ಲಕ್ಷಣಗಳಿಗೆ ಹೊಂದುತ್ತವೆ. |  |
| 25 | `app.js libraryTitle` | Disease library | ರೋಗಗಳ ಪಟ್ಟಿ |  |
| 26 | `app.js libraryHelp` | Tap a disease to read more. | ಹೆಚ್ಚು ಓದಲು ಒಂದು ರೋಗದ ಮೇಲೆ ಒತ್ತಿ. |  |
| 27 | `app.js noPhotoTitle` | Why there's no photo check | ಫೋಟೋ ಪರಿಶೀಲನೆ ಏಕೆ ಇಲ್ಲ |  |
| 28 | `app.js noPhotoText` | We tested a computer model that guesses the disease from a fish photo. The public photos are mostly aquarium fish, not carps in ponds, and the model was wrong about one time in three. That is not safe enough for your fish, so the app does not do it. | ಮೀನಿನ ಫೋಟೋದಿಂದ ರೋಗವನ್ನು ಊಹಿಸುವ ಕಂಪ್ಯೂಟರ್ ಮಾದರಿಯನ್ನು ನಾವು ಪರೀಕ್ಷಿಸಿದೆವು. ಸಾರ್ವಜನಿಕ ಫೋಟೋಗಳು ಹೆಚ್ಚಾಗಿ ಅಕ್ವೇರಿಯಂ ಮೀನುಗಳದ್ದು, ಕೊಳದ ಗೆಂಡೆ ಮೀನುಗಳದ್ದಲ್ಲ, ಮತ್ತು ಮಾದರಿ ಸುಮಾರು ಮೂರರಲ್ಲಿ ಒಂದು ಬಾರಿ ತಪ್ಪಾಗಿತ್ತು. ಇದು ನಿಮ್ಮ ಮೀನುಗಳಿಗೆ ಸಾಕಷ್ಟು ಸುರಕ್ಷಿತವಲ್ಲ, ಆದ್ದರಿಂದ ಆ್ಯಪ್ ಇದನ್ನು ಮಾಡುವುದಿಲ್ಲ. |  |
| 29 | `app.js noPhotoLink` | See the test results | ಪರೀಕ್ಷೆಯ ಫಲಿತಾಂಶಗಳನ್ನು ನೋಡಿ |  |
| 30 | `app.js likelyTitle` | Diseases more likely now | ಈಗ ಹೆಚ್ಚು ಸಾಧ್ಯತೆಯಿರುವ ರೋಗಗಳು |  |
| 31 | `app.js likelyNote` | This does not mean your fish are sick. Watch them closely and use the Fish disease guide if you see signs. | ಇದರ ಅರ್ಥ ನಿಮ್ಮ ಮೀನುಗಳಿಗೆ ರೋಗ ಬಂದಿದೆ ಎಂದಲ್ಲ. ಅವುಗಳನ್ನು ಗಮನವಿಟ್ಟು ನೋಡಿ, ಲಕ್ಷಣಗಳು ಕಂಡರೆ ಮೀನು ರೋಗ ಮಾರ್ಗದರ್ಶಿ ಬಳಸಿ. |  |

## 14. Ask AquaNexus assistant (page labels)

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js assistantTitle` | Ask AquaNexus | AquaNexus ಅನ್ನು ಕೇಳಿ |  |
| 2 | `app.js assistantLabel` | AI assistant: can make mistakes | AI ಸಹಾಯಕ: ತಪ್ಪುಗಳಾಗಬಹುದು |  |
| 3 | `app.js assistantHelp` | Ask about your readings, safe levels, tonight's weather, pond care (cleaning, water, feeding) or fish diseases. Answers come only from this app's own information. | ನಿಮ್ಮ ಅಳತೆಗಳು, ಸುರಕ್ಷಿತ ಮಟ್ಟಗಳು, ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ, ಕೊಳದ ಆರೈಕೆ (ಸ್ವಚ್ಛತೆ, ನೀರು, ಆಹಾರ) ಅಥವಾ ಮೀನು ರೋಗಗಳ ಬಗ್ಗೆ ಕೇಳಿ. ಉತ್ತರಗಳು ಈ ಆ್ಯಪ್‌ನ ಸ್ವಂತ ಮಾಹಿತಿಯಿಂದ ಮಾತ್ರ ಬರುತ್ತವೆ. |  |
| 4 | `app.js assistantPrivacy` | Do not type your name, phone number or other personal details. | ನಿಮ್ಮ ಹೆಸರು, ಫೋನ್ ಸಂಖ್ಯೆ ಅಥವಾ ಇತರ ವೈಯಕ್ತಿಕ ವಿವರಗಳನ್ನು ಬರೆಯಬೇಡಿ. |  |
| 5 | `app.js assistantSuggested` | Suggested questions (ready answers) | ಸೂಚಿಸಿದ ಪ್ರಶ್ನೆಗಳು (ಸಿದ್ಧ ಉತ್ತರಗಳು) |  |
| 6 | `app.js assistantAsk` | Your question | ನಿಮ್ಮ ಪ್ರಶ್ನೆ |  |
| 7 | `app.js assistantSend` | Ask | ಪ್ರಶ್ನೆ ಕೇಳಿ |  |
| 8 | `app.js assistantYou` | You | ನೀವು |  |
| 9 | `app.js assistantThinking` | Thinking… | ಯೋಚಿಸುತ್ತಿದೆ… |  |
| 10 | `app.js assistantAiAnswer` | AI answer | AI ಉತ್ತರ |  |
| 11 | `app.js assistantReady` | Ready answer from the app | ಆ್ಯಪ್‌ನ ಸಿದ್ಧ ಉತ್ತರ |  |
| 12 | `app.js assistantSafety` | Safety answer from the app | ಆ್ಯಪ್‌ನ ಸುರಕ್ಷತಾ ಉತ್ತರ |  |
| 13 | `app.js assistantListen` | Listen | ಆಲಿಸಿ |  |
| 14 | `app.js assistantNotice` | Message from the app | ಆ್ಯಪ್‌ನ ಸಂದೇಶ |  |
| 15 | `app.js assistantRelated` | You could ask: | ನೀವು ಹೀಗೆ ಕೇಳಬಹುದು: |  |
| 16 | `app.js assistantEmpty` | Type a question first, or tap a suggested question. | ಮೊದಲು ಪ್ರಶ್ನೆ ಬರೆಯಿರಿ, ಅಥವಾ ಸೂಚಿಸಿದ ಪ್ರಶ್ನೆಯೊಂದನ್ನು ಒತ್ತಿ. |  |
| 17 | `app.js assistantFailed` | Could not reach the app server. Tap a suggested question for a ready answer. | ಆ್ಯಪ್ ಸರ್ವರ್ ತಲುಪಲು ಆಗಲಿಲ್ಲ. ಸಿದ್ಧ ಉತ್ತರಕ್ಕಾಗಿ ಸೂಚಿಸಿದ ಪ್ರಶ್ನೆಯೊಂದನ್ನು ಒತ್ತಿ. |  |

## 15. Voice alert

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js voiceListen` | Listen to alert | ಎಚ್ಚರಿಕೆ ಕೇಳಿ |  |
| 2 | `app.js voiceStop` | Stop | ನಿಲ್ಲಿಸಿ |  |
| 3 | `app.js voiceNoKannada` | Sorry, this phone has no Kannada voice, so the alert cannot be read aloud in Kannada. Please read the alert on the screen, or switch to English to hear it. | ಕ್ಷಮಿಸಿ, ಈ ಫೋನ್‌ನಲ್ಲಿ ಕನ್ನಡ ಧ್ವನಿ ಇಲ್ಲ, ಆದ್ದರಿಂದ ಎಚ್ಚರಿಕೆಯನ್ನು ಕನ್ನಡದಲ್ಲಿ ಓದಿ ಹೇಳಲು ಆಗುವುದಿಲ್ಲ. ದಯವಿಟ್ಟು ಪರದೆಯ ಮೇಲಿನ ಎಚ್ಚರಿಕೆಯನ್ನು ಓದಿ, ಅಥವಾ ಕೇಳಲು English ಆಯ್ಕೆಮಾಡಿ. |  |
| 4 | `app.js voiceNoEnglish` | Sorry, this phone has no English voice. Please read the alert on the screen. | ಕ್ಷಮಿಸಿ, ಈ ಫೋನ್‌ನಲ್ಲಿ ಇಂಗ್ಲಿಷ್ ಧ್ವನಿ ಇಲ್ಲ. ದಯವಿಟ್ಟು ಪರದೆಯ ಮೇಲಿನ ಎಚ್ಚರಿಕೆಯನ್ನು ಓದಿ. |  |
| 5 | `app.js voiceUnsupported` | Sorry, this browser cannot read aloud. Please read the alert on the screen. | ಕ್ಷಮಿಸಿ, ಈ ಬ್ರೌಸರ್ ಓದಿ ಹೇಳಲು ಆಗುವುದಿಲ್ಲ. ದಯವಿಟ್ಟು ಪರದೆಯ ಮೇಲಿನ ಎಚ್ಚರಿಕೆಯನ್ನು ಓದಿ. |  |

## 16. Alert history

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js historyTitle` | Alert history | ಎಚ್ಚರಿಕೆಗಳ ಇತಿಹಾಸ |  |
| 2 | `app.js historyHelp` | Past warnings, newest first. Saved on this phone only. | ಹಿಂದಿನ ಎಚ್ಚರಿಕೆಗಳು, ಹೊಸದು ಮೊದಲು. ಈ ಫೋನ್‌ನಲ್ಲಿ ಮಾತ್ರ ಉಳಿಸಲಾಗಿದೆ. |  |
| 3 | `app.js historyEmpty` | No warnings yet. | ಇನ್ನೂ ಯಾವುದೇ ಎಚ್ಚರಿಕೆ ಇಲ್ಲ. |  |
| 4 | `app.js historyClear` | Clear history | ಇತಿಹಾಸ ಅಳಿಸಿ |  |
| 5 | `app.js historyClearConfirm` | Delete all saved alerts from this phone? | ಈ ಫೋನ್‌ನಲ್ಲಿ ಉಳಿಸಿದ ಎಲ್ಲಾ ಎಚ್ಚರಿಕೆಗಳನ್ನು ಅಳಿಸಬೇಕೆ? |  |
| 6 | `app.js historyKit` | Test kit | ಟೆಸ್ಟ್ ಕಿಟ್ |  |
| 7 | `app.js historySensor` | Live sensor | ಲೈವ್ ಸೆನ್ಸರ್ |  |
| 8 | `app.js historyDemo` | Demo device | ಡೆಮೊ ಸಾಧನ |  |
| 9 | `app.js historySimTime` | Simulated time | ಅನುಕರಿಸಿದ ಸಮಯ |  |
| 10 | `app.js historyActionTaken` | Action taken: | ತೆಗೆದುಕೊಂಡ ಕ್ರಮ: |  |
| 11 | `app.js historyNoAction` | No action ticked yet. | ಇನ್ನೂ ಯಾವುದೇ ಕ್ರಮವನ್ನು ಗುರುತಿಸಿಲ್ಲ. |  |

## 17. Data sources panel (footer)

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js sourcesTitle` | Data sources | ಡೇಟಾ ಮೂಲಗಳು |  |
| 2 | `app.js sourcesClose` | Close | ಮುಚ್ಚಿ |  |
| 3 | `app.js sourcesIntro` | The simulated pond uses these open datasets and public services. Only the Live sensor card and the devices in My ponds show readings sent by a pond sensor. | ಅನುಕರಿಸಿದ ಕೊಳವು ಈ ಮುಕ್ತ ಡೇಟಾಸೆಟ್‌ಗಳು ಮತ್ತು ಸಾರ್ವಜನಿಕ ಸೇವೆಗಳನ್ನು ಬಳಸುತ್ತದೆ. ಕೊಳದ ಸೆನ್ಸರ್ ಕಳುಹಿಸಿದ ಅಳತೆಗಳನ್ನು ಲೈವ್ ಸೆನ್ಸರ್ ಕಾರ್ಡ್ ಮತ್ತು ನನ್ನ ಕೊಳಗಳು ವಿಭಾಗದ ಸಾಧನಗಳು ಮಾತ್ರ ತೋರಿಸುತ್ತವೆ. |  |
| 4 | `app.js sourcesPondsUse` | Real sensor readings from 3 fish ponds in Andhra Pradesh (2022-23). Their daily levels shape the simulated demo pond, and we test our oxygen predictions on them. | ಆಂಧ್ರಪ್ರದೇಶದ 3 ಮೀನು ಕೊಳಗಳ ನಿಜವಾದ ಸೆನ್ಸರ್ ಅಳತೆಗಳು (2022-23). ಅವುಗಳ ದೈನಂದಿನ ಮಟ್ಟಗಳಿಂದ ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಪ್ರದರ್ಶನ ಕೊಳವನ್ನು ಮಾಡಲಾಗಿದೆ, ಮತ್ತು ನಮ್ಮ ಆಮ್ಲಜನಕ ಮುನ್ಸೂಚನೆಗಳನ್ನು ಅವುಗಳ ಮೇಲೆ ಪರೀಕ್ಷಿಸಲಾಗಿದೆ. |  |
| 5 | `app.js sourcesPondsUseOnline` | Real sensor readings from 3 fish ponds in Andhra Pradesh (2022-23). We test our oxygen predictions on them. Their licence is unknown, so this online demo does not include them: its demo pond uses typical healthy values instead. | ಆಂಧ್ರಪ್ರದೇಶದ 3 ಮೀನು ಕೊಳಗಳ ನಿಜವಾದ ಸೆನ್ಸರ್ ಅಳತೆಗಳು (2022-23). ನಮ್ಮ ಆಮ್ಲಜನಕ ಮುನ್ಸೂಚನೆಗಳನ್ನು ಅವುಗಳ ಮೇಲೆ ಪರೀಕ್ಷಿಸಲಾಗಿದೆ. ಅವುಗಳ ಪರವಾನಗಿ ತಿಳಿದಿಲ್ಲ, ಆದ್ದರಿಂದ ಈ ಆನ್‌ಲೈನ್ ಡೆಮೊದಲ್ಲಿ ಅವು ಇಲ್ಲ: ಇದರ ಪ್ರದರ್ಶನ ಕೊಳವು ಸಾಮಾನ್ಯ ಆರೋಗ್ಯಕರ ಮೌಲ್ಯಗಳನ್ನು ಬಳಸುತ್ತದೆ. |  |
| 6 | `app.js sourcesPondsLicence` | Licence: unknown (not stated by the uploader). | ಪರವಾನಗಿ: ತಿಳಿದಿಲ್ಲ (ಅಪ್‌ಲೋಡ್ ಮಾಡಿದವರು ತಿಳಿಸಿಲ್ಲ). |  |
| 7 | `app.js sourcesMeteoUse` | Tonight's real weather forecast for the night oxygen-crash warning: for Mangaluru (the demo pond), or for the village you chose for each of your ponds. | ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಎಚ್ಚರಿಕೆಗಾಗಿ ಇಂದು ರಾತ್ರಿಯ ನಿಜವಾದ ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ: ಮಂಗಳೂರಿನದು (ಡೆಮೊ ಕೊಳ), ಅಥವಾ ನಿಮ್ಮ ಪ್ರತಿ ಕೊಳಕ್ಕೆ ನೀವು ಆರಿಸಿದ ಊರಿನದು. |  |
| 8 | `app.js sourcesMeteoLicence` | Licence: data CC BY 4.0. Free API, non-commercial use only. | ಪರವಾನಗಿ: ಡೇಟಾ CC BY 4.0. ಉಚಿತ API, ವಾಣಿಜ್ಯೇತರ ಬಳಕೆಗೆ ಮಾತ್ರ. |  |
| 9 | `app.js sourcesGuidesUse` | Published guides and research papers behind the Safe / Warning / Danger limits and the “What to do now” steps. | ಸುರಕ್ಷಿತ / ಎಚ್ಚರಿಕೆ / ಅಪಾಯ ಮಿತಿಗಳು ಮತ್ತು “ಈಗ ಏನು ಮಾಡಬೇಕು” ಹಂತಗಳಿಗೆ ಆಧಾರವಾದ ಪ್ರಕಟಿತ ಮಾರ್ಗದರ್ಶಿಗಳು ಮತ್ತು ಸಂಶೋಧನಾ ಲೇಖನಗಳು. |  |
| 10 | `app.js sourcesGuidesLicence` | Copyright of each publisher. We cite their facts; we don't copy them. | ಹಕ್ಕುಸ್ವಾಮ್ಯ ಆಯಾ ಪ್ರಕಾಶಕರದು. ನಾವು ಅವುಗಳ ಮಾಹಿತಿಯನ್ನು ಉಲ್ಲೇಖಿಸುತ್ತೇವೆ, ನಕಲು ಮಾಡುವುದಿಲ್ಲ. |  |
| 11 | `app.js sourcesMendeleyUse` | Checked but not used: some values are impossible (e.g. water at 84 °C). | ಪರಿಶೀಲಿಸಲಾಗಿದೆ, ಆದರೆ ಬಳಸಿಲ್ಲ: ಕೆಲವು ಮೌಲ್ಯಗಳು ಅಸಾಧ್ಯ (ಉದಾ: 84 °C ನೀರು). |  |
| 12 | `app.js sourcesMendeleyLicence` | Licence: CC BY 4.0. | ಪರವಾನಗಿ: CC BY 4.0. |  |
| 13 | `app.js sourcesFishUse` | Fish disease photos for research only. Not used in the app. | ಮೀನು ರೋಗದ ಫೋಟೋಗಳು, ಸಂಶೋಧನೆಗೆ ಮಾತ್ರ. ಆಪ್‌ನಲ್ಲಿ ಬಳಸಿಲ್ಲ. |  |
| 14 | `app.js sourcesFishLicence` | Licence: CC0 (public domain). | ಪರವಾನಗಿ: CC0 (ಸಾರ್ವಜನಿಕ ಸ್ವತ್ತು). |  |
| 15 | `app.js sourcesFull` | Full list with links and licences | ಲಿಂಕ್‌ಗಳು ಮತ್ತು ಪರವಾನಗಿಗಳ ಪೂರ್ಣ ಪಟ್ಟಿ |  |

## 18. Terms & Privacy panel (footer)

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js termsTitle` | Terms & Privacy | ನಿಯಮಗಳು ಮತ್ತು ಗೌಪ್ಯತೆ |  |
| 2 | `app.js termsClose` | Close | ಮುಚ್ಚಿ |  |
| 3 | `app.js termsWhatTitle` | What this is | ಇದು ಏನು |  |
| 4 | `app.js termsWhat` | AquaNexus is a free early-warning helper for small fish ponds, built by Team Orbit for DevHack 2026. It helps you decide what to check and when. It does not replace your fisheries officer, KVK or vet, and it cannot promise that your fish will be safe. | AquaNexus ಸಣ್ಣ ಮೀನು ಕೊಳಗಳಿಗಾಗಿ ಉಚಿತ ಮುನ್ನೆಚ್ಚರಿಕೆ ಸಹಾಯಕ. ಇದನ್ನು ಟೀಮ್ ಆರ್ಬಿಟ್ DevHack 2026 ಗಾಗಿ ನಿರ್ಮಿಸಿದೆ. ಏನನ್ನು, ಯಾವಾಗ ಪರಿಶೀಲಿಸಬೇಕು ಎಂದು ನಿರ್ಧರಿಸಲು ಇದು ಸಹಾಯ ಮಾಡುತ್ತದೆ. ಇದು ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿ, KVK ಅಥವಾ ಪಶುವೈದ್ಯರ ಬದಲಿಯಲ್ಲ, ಮತ್ತು ನಿಮ್ಮ ಮೀನುಗಳು ಸುರಕ್ಷಿತವಾಗಿರುತ್ತವೆ ಎಂದು ಖಾತರಿ ನೀಡುವುದಿಲ್ಲ. |  |
| 5 | `app.js termsLimitsTitle` | Limits of the data | ಡೇಟಾದ ಮಿತಿಗಳು |  |
| 6 | `app.js termsLimits` | The demo pond's readings are simulated, not from a real pond. Weather forecasts can be wrong. The disease guide shows possible causes, never a diagnosis. The AI assistant can make mistakes. Always confirm before you act. | ಡೆಮೊ ಕೊಳದ ಅಳತೆಗಳು ಅನುಕರಿಸಿದವು (ಸಿಮ್ಯುಲೇಟೆಡ್), ನಿಜವಾದ ಕೊಳದವಲ್ಲ. ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ ತಪ್ಪಾಗಬಹುದು. ರೋಗ ಮಾರ್ಗದರ್ಶಿ ಸಾಧ್ಯವಿರುವ ಕಾರಣಗಳನ್ನು ಮಾತ್ರ ತೋರಿಸುತ್ತದೆ, ರೋಗನಿರ್ಣಯವನ್ನಲ್ಲ. AI ಸಹಾಯಕ ತಪ್ಪು ಮಾಡಬಹುದು. ಕ್ರಮ ಕೈಗೊಳ್ಳುವ ಮೊದಲು ಯಾವಾಗಲೂ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ. |  |
| 7 | `app.js termsTreatTitle` | No chemical or medicine advice | ರಾಸಾಯನಿಕ ಅಥವಾ ಔಷಧಿ ಸಲಹೆ ಇಲ್ಲ |  |
| 8 | `app.js termsTreat` | The app never suggests chemicals, medicines or amounts to add to the pond. Treatment must come from a fisheries officer or KVK. | ಆ್ಯಪ್ ಎಂದಿಗೂ ಕೊಳಕ್ಕೆ ಹಾಕಬೇಕಾದ ರಾಸಾಯನಿಕ, ಔಷಧಿ ಅಥವಾ ಪ್ರಮಾಣವನ್ನು ಸೂಚಿಸುವುದಿಲ್ಲ. ಚಿಕಿತ್ಸೆಯನ್ನು ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿ ಅಥವಾ KVK ಮಾತ್ರ ನೀಡಬೇಕು. |  |
| 9 | `app.js termsPrivacyTitle` | Privacy | ಗೌಪ್ಯತೆ |  |
| 10 | `app.js termsNoAccount` | No account and no sign-up. | ಖಾತೆ ಇಲ್ಲ, ನೋಂದಣಿ ಇಲ್ಲ. |  |
| 11 | `app.js termsPonds` | My ponds: your pond names, sizes, fish types, device readings and alerts are saved on our server under your farm code. We keep only a scrambled copy (hash) of the farm code and of device keys. No name, phone number or email is asked for. Anyone with your farm code can see and change your ponds. | ನನ್ನ ಕೊಳಗಳು: ನಿಮ್ಮ ಕೊಳಗಳ ಹೆಸರು, ಗಾತ್ರ, ಮೀನಿನ ಪ್ರಕಾರ, ಸಾಧನದ ಅಳತೆಗಳು ಮತ್ತು ಎಚ್ಚರಿಕೆಗಳು ನಿಮ್ಮ ಫಾರ್ಮ್ ಕೋಡ್ ಅಡಿಯಲ್ಲಿ ನಮ್ಮ ಸರ್ವರ್‌ನಲ್ಲಿ ಉಳಿಯುತ್ತವೆ. ಫಾರ್ಮ್ ಕೋಡ್ ಮತ್ತು ಸಾಧನದ ಕೀಗಳ ಗೂಢ ಪ್ರತಿಯನ್ನು (ಹ್ಯಾಶ್) ಮಾತ್ರ ಇಡುತ್ತೇವೆ. ಹೆಸರು, ಫೋನ್ ಸಂಖ್ಯೆ ಅಥವಾ ಇಮೇಲ್ ಕೇಳುವುದಿಲ್ಲ. ನಿಮ್ಮ ಫಾರ್ಮ್ ಕೋಡ್ ಇರುವ ಯಾರಾದರೂ ನಿಮ್ಮ ಕೊಳಗಳನ್ನು ನೋಡಬಹುದು ಮತ್ತು ಬದಲಿಸಬಹುದು. |  |
| 12 | `app.js termsKeep` | Device readings are kept for 48 hours and alerts for 14 days. | ಸಾಧನದ ಅಳತೆಗಳನ್ನು 48 ಗಂಟೆ ಮತ್ತು ಎಚ್ಚರಿಕೆಗಳನ್ನು 14 ದಿನ ಇಡಲಾಗುತ್ತದೆ. |  |
| 13 | `app.js termsDemo` | Demo mode: data resets when the server sleeps. | ಡೆಮೊ ಮೋಡ್: ಸರ್ವರ್ ನಿದ್ರಿಸಿದಾಗ ಡೇಟಾ ಅಳಿಸಿಹೋಗುತ್ತದೆ. |  |
| 14 | `app.js termsLocation` | The app never asks for your GPS location or address. For each of your ponds you can choose a village from a list: only the village name is saved, and that pond's weather is for that village. The demo pond's weather is for Mangaluru. Your phone gets the forecast straight from Open-Meteo, so Open-Meteo sees your internet address, as any website would, and the village's position on the map (not yours). | ಆ್ಯಪ್ ನಿಮ್ಮ GPS ಸ್ಥಳ ಅಥವಾ ವಿಳಾಸವನ್ನು ಎಂದಿಗೂ ಕೇಳುವುದಿಲ್ಲ. ನಿಮ್ಮ ಪ್ರತಿ ಕೊಳಕ್ಕೆ ಪಟ್ಟಿಯಿಂದ ಒಂದು ಊರನ್ನು ಆರಿಸಬಹುದು: ಊರಿನ ಹೆಸರು ಮಾತ್ರ ಉಳಿಸಲಾಗುತ್ತದೆ, ಮತ್ತು ಆ ಕೊಳದ ಹವಾಮಾನ ಆ ಊರಿನದು. ಡೆಮೊ ಕೊಳದ ಹವಾಮಾನ ಮಂಗಳೂರಿನದು. ನಿಮ್ಮ ಫೋನ್ ಮುನ್ಸೂಚನೆಯನ್ನು ನೇರವಾಗಿ Open-Meteo ಯಿಂದ ಪಡೆಯುತ್ತದೆ, ಆದ್ದರಿಂದ ಯಾವುದೇ ವೆಬ್‌ಸೈಟ್‌ನಂತೆ Open-Meteo ನಿಮ್ಮ ಇಂಟರ್ನೆಟ್ ವಿಳಾಸವನ್ನು ನೋಡುತ್ತದೆ, ಮತ್ತು ಊರಿನ ನಕ್ಷೆಯ ಸ್ಥಾನವನ್ನು (ನಿಮ್ಮದಲ್ಲ). |  |
| 15 | `app.js termsBrowser` | Your language, theme, ticked steps, alert history, the last weather forecast, your Shop cart and your farm code are saved only in this browser. Clearing the browser's data removes them. | ನಿಮ್ಮ ಭಾಷೆ, ಥೀಮ್, ಗುರುತು ಹಾಕಿದ ಹಂತಗಳು, ಎಚ್ಚರಿಕೆಗಳ ಇತಿಹಾಸ, ಕೊನೆಯ ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ, ಅಂಗಡಿಯ ಕಾರ್ಟ್ ಮತ್ತು ನಿಮ್ಮ ಫಾರ್ಮ್ ಕೋಡ್ ಈ ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಮಾತ್ರ ಉಳಿಯುತ್ತವೆ. ಬ್ರೌಸರ್‌ನ ಡೇಟಾ ಅಳಿಸಿದರೆ ಅವು ಹೋಗುತ್ತವೆ. |  |
| 16 | `app.js termsServer` | Test-kit numbers and the readings on screen go to our server to be checked, and are not saved there. Readings sent to the demo Live sensor card are kept in the server's memory only and are cleared when the server sleeps or restarts. | ಟೆಸ್ಟ್-ಕಿಟ್ ಅಳತೆಗಳು ಮತ್ತು ಪರದೆಯ ಮೇಲಿನ ಅಳತೆಗಳು ಪರಿಶೀಲನೆಗಾಗಿ ನಮ್ಮ ಸರ್ವರ್‌ಗೆ ಹೋಗುತ್ತವೆ, ಅಲ್ಲಿ ಉಳಿಸಲಾಗುವುದಿಲ್ಲ. ಡೆಮೊ ಲೈವ್ ಸೆನ್ಸರ್ ಕಾರ್ಡ್‌ಗೆ ಕಳುಹಿಸಿದ ಅಳತೆಗಳು ಸರ್ವರ್‌ನ ಮೆಮೊರಿಯಲ್ಲಿ ಮಾತ್ರ ಇರುತ್ತವೆ ಮತ್ತು ಸರ್ವರ್ ನಿದ್ರಿಸಿದಾಗ ಅಥವಾ ಮರುಪ್ರಾರಂಭವಾದಾಗ ಅಳಿಸಿಹೋಗುತ್ತವೆ. |  |
| 17 | `app.js termsAi` | Questions to the assistant are sent, with the readings on screen and the level, cause and time of your recent alerts, to the AI service (now Google Gemini) to get an answer. Google's own terms apply to what it receives. Don't type your name, phone number or other personal details. | ಸಹಾಯಕನಿಗೆ ಕೇಳುವ ಪ್ರಶ್ನೆಗಳು, ಪರದೆಯ ಮೇಲಿನ ಅಳತೆಗಳು ಮತ್ತು ಇತ್ತೀಚಿನ ಎಚ್ಚರಿಕೆಗಳ ಮಟ್ಟ, ಕಾರಣ ಹಾಗೂ ಸಮಯದ ಜೊತೆಗೆ, ಉತ್ತರ ಪಡೆಯಲು AI ಸೇವೆಗೆ (ಈಗ Google Gemini) ಹೋಗುತ್ತವೆ. ಅದು ಪಡೆಯುವುದಕ್ಕೆ Google ನ ಸ್ವಂತ ನಿಯಮಗಳು ಅನ್ವಯಿಸುತ್ತವೆ. ನಿಮ್ಮ ಹೆಸರು, ಫೋನ್ ಸಂಖ್ಯೆ ಅಥವಾ ಇತರ ವೈಯಕ್ತಿಕ ವಿವರಗಳನ್ನು ಟೈಪ್ ಮಾಡಬೇಡಿ. |  |
| 18 | `app.js termsLogs` | To keep the site working and stop misuse, our server and our host (Render) keep short technical records, such as which page was asked for and the internet address it came from. | ಸೈಟ್ ಸರಿಯಾಗಿ ನಡೆಯಲು ಮತ್ತು ದುರುಪಯೋಗ ತಡೆಯಲು, ನಮ್ಮ ಸರ್ವರ್ ಮತ್ತು ನಮ್ಮ ಹೋಸ್ಟ್ (Render) ಸಣ್ಣ ತಾಂತ್ರಿಕ ದಾಖಲೆಗಳನ್ನು ಇಡುತ್ತವೆ, ಉದಾಹರಣೆಗೆ ಯಾವ ಪುಟ ಕೇಳಲಾಯಿತು ಮತ್ತು ಅದು ಬಂದ ಇಂಟರ್ನೆಟ್ ವಿಳಾಸ. |  |
| 19 | `app.js termsNoAds` | No ads, no tracking, and nothing about you is sold. | ಜಾಹೀರಾತುಗಳಿಲ್ಲ, ಟ್ರ್ಯಾಕಿಂಗ್ ಇಲ್ಲ, ಮತ್ತು ನಿಮ್ಮ ಬಗ್ಗೆ ಏನನ್ನೂ ಮಾರಾಟ ಮಾಡುವುದಿಲ್ಲ. |  |
| 20 | `app.js termsDataTitle` | Open data and licences | ಮುಕ್ತ ಡೇಟಾ ಮತ್ತು ಪರವಾನಗಿಗಳು |  |
| 21 | `app.js termsData` | The app uses open datasets and public services. The Data sources list shows each one and its licence. | ಆ್ಯಪ್ ಮುಕ್ತ ಡೇಟಾಸೆಟ್‌ಗಳು ಮತ್ತು ಸಾರ್ವಜನಿಕ ಸೇವೆಗಳನ್ನು ಬಳಸುತ್ತದೆ. ಪ್ರತಿಯೊಂದನ್ನೂ ಅದರ ಪರವಾನಗಿಯೊಂದಿಗೆ ಡೇಟಾ ಮೂಲಗಳ ಪಟ್ಟಿ ತೋರಿಸುತ್ತದೆ. |  |
| 22 | `app.js termsDataButton` | Open Data sources | ಡೇಟಾ ಮೂಲಗಳನ್ನು ತೆರೆಯಿರಿ |  |
| 23 | `app.js termsContactTitle` | Contact | ಸಂಪರ್ಕ |  |
| 24 | `app.js termsContact` | AquaNexus is made by Team Orbit. For questions or problems, reach us through our GitHub page. | AquaNexus ಅನ್ನು ಟೀಮ್ ಆರ್ಬಿಟ್ ತಯಾರಿಸಿದೆ. ಪ್ರಶ್ನೆಗಳು ಅಥವಾ ಸಮಸ್ಯೆಗಳಿದ್ದರೆ ನಮ್ಮ GitHub ಪುಟದ ಮೂಲಕ ಸಂಪರ್ಕಿಸಿ. |  |
| 25 | `app.js termsContactLink` | Team Orbit on GitHub | GitHub ನಲ್ಲಿ ಟೀಮ್ ಆರ್ಬಿಟ್ |  |

## 19. Footer (privacy, source code)

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js footerCode` | Source code on GitHub | GitHub ನಲ್ಲಿ ಸೋರ್ಸ್ ಕೋಡ್ |  |
| 2 | `app.js footerPrivacy` | Privacy: no account needed. The app never uses your camera, photos or location. Alert history is saved on this phone. Test-kit numbers go to our server only to check them. Assistant questions, with the readings and recent alert levels, may also go to an AI service. | ಗೌಪ್ಯತೆ: ಖಾತೆ ಬೇಕಾಗಿಲ್ಲ. ಆ್ಯಪ್ ನಿಮ್ಮ ಕ್ಯಾಮೆರಾ, ಫೋಟೋ ಅಥವಾ ಸ್ಥಳವನ್ನು ಬಳಸುವುದಿಲ್ಲ. ಎಚ್ಚರಿಕೆಗಳ ಇತಿಹಾಸ ಈ ಫೋನ್‌ನಲ್ಲೇ ಉಳಿಯುತ್ತದೆ. ಟೆಸ್ಟ್-ಕಿಟ್ ಅಳತೆಗಳು ಪರಿಶೀಲನೆಗಾಗಿ ಮಾತ್ರ ನಮ್ಮ ಸರ್ವರ್‌ಗೆ ಹೋಗುತ್ತವೆ. ಸಹಾಯಕನಿಗೆ ಕೇಳುವ ಪ್ರಶ್ನೆಗಳು, ಅಳತೆಗಳು ಮತ್ತು ಇತ್ತೀಚಿನ ಎಚ್ಚರಿಕೆಗಳ ಮಟ್ಟದ ಜೊತೆಗೆ, AI ಸೇವೆಗೂ ಹೋಗಬಹುದು. |  |
| 3 | `app.js footerCredit` | AquaNexus by Team Orbit (Nexus Orbit) | AquaNexus · ನಿರ್ಮಾಣ: ಟೀಮ್ ಆರ್ಬಿಟ್ (Nexus Orbit) |  |

## 20. Other page labels

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js simBasisPondsdata` | Demo data modelled on Pondsdata: its daily levels with a simulated day-night oxygen cycle. Not real readings. | Pondsdata ಆಧಾರಿತ ಡೆಮೊ ಡೇಟಾ: ಅದರ ದೈನಂದಿನ ಮಟ್ಟಗಳು ಮತ್ತು ಅನುಕರಿಸಿದ ಹಗಲು-ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಚಕ್ರ. ನಿಜವಾದ ಅಳತೆಗಳಲ್ಲ. |  |
| 2 | `app.js simBasisTypical` | Demo data from typical healthy pond values with a simulated day-night oxygen cycle. Not real readings. | ಸಾಮಾನ್ಯ ಆರೋಗ್ಯಕರ ಕೊಳದ ಮೌಲ್ಯಗಳು ಮತ್ತು ಅನುಕರಿಸಿದ ಹಗಲು-ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಚಕ್ರದಿಂದ ಮಾಡಿದ ಡೆಮೊ ಡೇಟಾ. ನಿಜವಾದ ಅಳತೆಗಳಲ್ಲ. |  |
| 3 | `app.js tabPond` | Pond | ಕೊಳ |  |
| 4 | `app.js tabAlerts` | Alerts | ಎಚ್ಚರಿಕೆ |  |
| 5 | `app.js tabWeather` | Weather | ಹವೆ |  |
| 6 | `app.js tabDiseases` | Diseases | ರೋಗ |  |
| 7 | `app.js tabAsk` | Ask | ಕೇಳಿ |  |
| 8 | `app.js tabShop` | Shop | ಅಂಗಡಿ |  |
| 9 | `app.js tabMore` | More | ಇತರೆ |  |
| 10 | `app.js tabWeatherShort` | Sky | ಹವೆ |  |
| 11 | `app.js tabDiseasesShort` | Fish | ರೋಗ |  |
| 12 | `app.js titleWeather` | Weather | ಹವಾಮಾನ |  |
| 13 | `app.js titleDiseases` | Fish diseases | ಮೀನು ರೋಗಗಳು |  |
| 14 | `app.js titleMore` | More | ಇನ್ನಷ್ಟು |  |
| 15 | `app.js demoPondTitle` | Demo pond | ಡೆಮೊ ಕೊಳ |  |
| 16 | `app.js deviceOnline` | Device online | ಸಾಧನ ಆನ್‌ಲೈನ್ |  |
| 17 | `app.js deviceOfflineSince` | Offline since {t} | {t} ರಿಂದ ಆಫ್‌ಲೈನ್ |  |
| 18 | `app.js deviceWaiting` | Device connected. Waiting for the first reading. | ಸಾಧನ ಸಂಪರ್ಕಗೊಂಡಿದೆ. ಮೊದಲ ಅಳತೆಗಾಗಿ ಕಾಯಲಾಗುತ್ತಿದೆ. |  |
| 19 | `app.js deviceNone` | No device | ಸಾಧನವಿಲ್ಲ |  |
| 20 | `app.js deviceTitle` | Device | ಸಾಧನ |  |
| 21 | `app.js deviceConnect` | Connect a device | ಸಾಧನ ಸಂಪರ್ಕಿಸಿ |  |
| 22 | `app.js deviceNewKey` | New key | ಹೊಸ ಕೀ |  |
| 23 | `app.js deviceRemove` | Remove device | ಸಾಧನ ತೆಗೆಯಿರಿ |  |
| 24 | `app.js deviceRemoveConfirm` | Remove this device? It will stop sending readings to this pond. | ಈ ಸಾಧನವನ್ನು ತೆಗೆಯಬೇಕೇ? ಇದು ಈ ಕೊಳಕ್ಕೆ ಅಳತೆ ಕಳುಹಿಸುವುದನ್ನು ನಿಲ್ಲಿಸುತ್ತದೆ. |  |
| 25 | `app.js deviceNewKeyConfirm` | Make a new key? The old key stops working at once. | ಹೊಸ ಕೀ ಮಾಡಬೇಕೇ? ಹಳೆಯ ಕೀ ತಕ್ಷಣ ಕೆಲಸ ನಿಲ್ಲಿಸುತ್ತದೆ. |  |
| 26 | `app.js deviceKeyOnce` | Save this key now. It is shown only once. AquaNexus keeps only a scrambled copy (a hash). | ಈ ಕೀಯನ್ನು ಈಗಲೇ ಉಳಿಸಿ. ಇದನ್ನು ಒಮ್ಮೆ ಮಾತ್ರ ತೋರಿಸಲಾಗುತ್ತದೆ. AquaNexus ಅದರ ಗೂಢ ಪ್ರತಿಯನ್ನು (ಹ್ಯಾಶ್) ಮಾತ್ರ ಇಡುತ್ತದೆ. |  |
| 27 | `app.js deviceIdLabel` | Device ID | ಸಾಧನದ ID |  |
| 28 | `app.js deviceKeyLabel` | Device key | ಸಾಧನದ ಕೀ |  |
| 29 | `app.js deviceUrlLabel` | Address | ವಿಳಾಸ |  |
| 30 | `app.js copy` | Copy | ನಕಲಿಸಿ |  |
| 31 | `app.js copied` | Copied | ನಕಲಾಗಿದೆ |  |
| 32 | `app.js copyByHand` | Copy by hand | ಕೈಯಾರೆ ನಕಲಿಸಿ |  |
| 33 | `app.js deviceSetupTitle` | Set up the device | ಸಾಧನವನ್ನು ಸಿದ್ಧಪಡಿಸಿ |  |
| 34 | `app.js deviceKeyDone` | I have saved the key | ನಾನು ಕೀ ಉಳಿಸಿದ್ದೇನೆ |  |
| 35 | `app.js deviceStep1` | Open the ESP32 sketch in docs/sensor-api.md. Put the device ID and key in it. | docs/sensor-api.md ನಲ್ಲಿರುವ ESP32 ಸ್ಕೆಚ್ ತೆರೆಯಿರಿ. ಅದರಲ್ಲಿ ಸಾಧನದ ID ಮತ್ತು ಕೀ ಹಾಕಿ. |  |
| 36 | `app.js deviceStep2` | It sends each reading to POST {url} with the header X-Sensor-Key. | ಇದು ಪ್ರತಿ ಅಳತೆಯನ್ನು X-Sensor-Key ಹೆಡರ್ ಜೊತೆಗೆ POST {url} ಗೆ ಕಳುಹಿಸುತ್ತದೆ. |  |
| 37 | `app.js deviceStep3` | At most one reading every {s} seconds. Leave out values the device does not measure. | {s} ಸೆಕೆಂಡಿಗೆ ಹೆಚ್ಚೆಂದರೆ ಒಂದು ಅಳತೆ. ಸಾಧನ ಅಳೆಯದ ಮೌಲ್ಯಗಳನ್ನು ಬಿಟ್ಟುಬಿಡಿ. |  |
| 38 | `app.js deviceStep4` | Switch it on. The pond shows Device online when the first reading arrives. | ಸ್ವಿಚ್ ಆನ್ ಮಾಡಿ. ಮೊದಲ ಅಳತೆ ಬಂದಾಗ ಕೊಳ "ಸಾಧನ ಆನ್‌ಲೈನ್" ಎಂದು ತೋರಿಸುತ್ತದೆ. |  |
| 39 | `app.js deviceLastRefused` | Last reading refused: | ಕೊನೆಯ ಅಳತೆ ತಿರಸ್ಕರಿಸಲಾಗಿದೆ: |  |
| 40 | `app.js farmTitle` | My farm code | ನನ್ನ ಫಾರ್ಮ್ ಕೋಡ್ |  |
| 41 | `app.js farmHelp` | This code keeps your ponds together. Type it on another phone to open the same ponds. No name, phone number or email is needed. | ಈ ಕೋಡ್ ನಿಮ್ಮ ಕೊಳಗಳನ್ನು ಒಟ್ಟಿಗೆ ಇಡುತ್ತದೆ. ಅದೇ ಕೊಳಗಳನ್ನು ತೆರೆಯಲು ಇನ್ನೊಂದು ಫೋನ್‌ನಲ್ಲಿ ಇದನ್ನು ಬರೆಯಿರಿ. ಹೆಸರು, ಫೋನ್ ಸಂಖ್ಯೆ ಅಥವಾ ಇಮೇಲ್ ಬೇಕಾಗಿಲ್ಲ. |  |
| 42 | `app.js farmWarn` | Anyone with this code can see and change your ponds. Share it only with people you trust. | ಈ ಕೋಡ್ ಇರುವ ಯಾರಾದರೂ ನಿಮ್ಮ ಕೊಳಗಳನ್ನು ನೋಡಬಹುದು ಮತ್ತು ಬದಲಿಸಬಹುದು. ನೀವು ನಂಬುವವರೊಂದಿಗೆ ಮಾತ್ರ ಹಂಚಿಕೊಳ್ಳಿ. |  |
| 43 | `app.js farmCopy` | Copy code | ಕೋಡ್ ನಕಲಿಸಿ |  |
| 44 | `app.js farmNotSaved` | This browser is not saving the code. Write it down. | ಈ ಬ್ರೌಸರ್ ಕೋಡ್ ಉಳಿಸುತ್ತಿಲ್ಲ. ಅದನ್ನು ಬರೆದಿಟ್ಟುಕೊಳ್ಳಿ. |  |
| 45 | `app.js farmUseLabel` | Code from another phone | ಇನ್ನೊಂದು ಫೋನ್‌ನ ಕೋಡ್ |  |
| 46 | `app.js farmOpen` | Open these ponds | ಈ ಕೊಳಗಳನ್ನು ತೆರೆಯಿರಿ |  |
| 47 | `app.js farmBad` | That is not a farm code. It has 12 letters and numbers, like K7QM-3XRP-9TFD. | ಇದು ಫಾರ್ಮ್ ಕೋಡ್ ಅಲ್ಲ. ಇದರಲ್ಲಿ K7QM-3XRP-9TFD ತರಹ 12 ಅಕ್ಷರ ಮತ್ತು ಅಂಕಿಗಳಿರುತ್ತವೆ. |  |
| 48 | `app.js farmSwitchConfirm` | Open the ponds for this code? Write down your current code first if you want to come back to it. | ಈ ಕೋಡ್‌ನ ಕೊಳಗಳನ್ನು ತೆರೆಯಬೇಕೇ? ಹಿಂತಿರುಗಲು ಬಯಸಿದರೆ ಮೊದಲು ನಿಮ್ಮ ಈಗಿನ ಕೋಡ್ ಬರೆದಿಟ್ಟುಕೊಳ್ಳಿ. |  |
| 49 | `app.js farmSwitched` | Now showing the ponds for {c}. | ಈಗ {c} ಕೋಡ್‌ನ ಕೊಳಗಳನ್ನು ತೋರಿಸಲಾಗುತ್ತಿದೆ. |  |
| 50 | `app.js stripAllSafe` | All your ponds are safe | ನಿಮ್ಮ ಎಲ್ಲಾ ಕೊಳಗಳು ಸುರಕ್ಷಿತ |  |
| 51 | `app.js titleShop` | Shop | ಅಂಗಡಿ |  |
| 52 | `app.js shopIntro` | Sensors and spare parts that work with AquaNexus. Make a list and share it. | AquaNexus ಜೊತೆ ಕೆಲಸ ಮಾಡುವ ಸೆನ್ಸರ್‌ಗಳು ಮತ್ತು ಬಿಡಿಭಾಗಗಳು. ಪಟ್ಟಿ ಮಾಡಿ ಹಂಚಿಕೊಳ್ಳಿ. |  |
| 53 | `app.js shopNotForSale` | Not for sale yet. Orders open after our pilot with farmers. | ಇನ್ನೂ ಮಾರಾಟಕ್ಕಿಲ್ಲ. ರೈತರೊಂದಿಗಿನ ನಮ್ಮ ಪ್ರಾಯೋಗಿಕ ಯೋಜನೆಯ ನಂತರ ಆರ್ಡರ್‌ಗಳು ಆರಂಭವಾಗುತ್ತವೆ. |  |
| 54 | `app.js shopOnePondTitle` | Before you buy | ಖರೀದಿಸುವ ಮೊದಲು |  |
| 55 | `app.js shopOnePond` | One sensor watches one pond. For several ponds, each needs its own sensor. Start with the free app and the test kit. | ಒಂದು ಸೆನ್ಸರ್ ಒಂದೇ ಕೊಳವನ್ನು ಗಮನಿಸುತ್ತದೆ. ಹಲವು ಕೊಳಗಳಿದ್ದರೆ, ಪ್ರತಿಯೊಂದಕ್ಕೂ ಬೇರೆ ಸೆನ್ಸರ್ ಬೇಕು. ಉಚಿತ ಆ್ಯಪ್ ಮತ್ತು ಟೆಸ್ಟ್ ಕಿಟ್‌ನಿಂದ ಪ್ರಾರಂಭಿಸಿ. |  |
| 56 | `app.js shopPriceNote` | Estimated component cost. Prices may change. | ಅಂದಾಜು ಬಿಡಿಭಾಗಗಳ ವೆಚ್ಚ. ಬೆಲೆಗಳು ಬದಲಾಗಬಹುದು. |  |
| 57 | `app.js shopWiringTitle` | How the kit is wired | ಕಿಟ್‌ನ ವೈರಿಂಗ್ ಹೇಗಿದೆ |  |
| 58 | `app.js shopWiringOpen` | Open the diagram full size | ಚಿತ್ರವನ್ನು ಪೂರ್ಣ ಗಾತ್ರದಲ್ಲಿ ತೆರೆಯಿರಿ |  |
| 59 | `app.js shopWiringProposed` | Proposed design, not yet built | ಪ್ರಸ್ತಾವಿತ ವಿನ್ಯಾಸ, ಇನ್ನೂ ನಿರ್ಮಿಸಿಲ್ಲ |  |
| 60 | `app.js shopWiringCaption` | Solar power, battery, ESP32 board, 4G modem and the oxygen, temperature and pH sensors. Part names are in English. | ಸೌರ ವಿದ್ಯುತ್, ಬ್ಯಾಟರಿ, ESP32 ಬೋರ್ಡ್, 4G ಮೋಡೆಮ್ ಮತ್ತು ಆಮ್ಲಜನಕ, ತಾಪಮಾನ, pH ಸೆನ್ಸರ್‌ಗಳು. ಭಾಗಗಳ ಹೆಸರುಗಳು ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿವೆ. |  |
| 61 | `app.js shopWiringAlt` | Wiring diagram. A 10 W solar panel charges an 18650 battery pack through a CN3791 charger. The pack powers the ESP32 board (through a 3.3 V regulator), a switched 12 V supply for the oxygen probe, and an A7670C 4G modem. The ESP32 reads the optical oxygen probe over isolated RS485, a DS18B20 temperature sensor, and the pH probe through an isolator and an ADS1115 converter. | ವೈರಿಂಗ್ ಚಿತ್ರ. 10 W ಸೌರ ಫಲಕವು CN3791 ಚಾರ್ಜರ್ ಮೂಲಕ 18650 ಬ್ಯಾಟರಿ ಪ್ಯಾಕ್ ಅನ್ನು ಚಾರ್ಜ್ ಮಾಡುತ್ತದೆ. ಬ್ಯಾಟರಿಯು ESP32 ಬೋರ್ಡ್ (3.3 V ರೆಗ್ಯುಲೇಟರ್ ಮೂಲಕ), ಆಮ್ಲಜನಕ ಪ್ರೋಬ್‌ಗೆ 12 V ಮತ್ತು A7670C 4G ಮೋಡೆಮ್‌ಗೆ ವಿದ್ಯುತ್ ನೀಡುತ್ತದೆ. ESP32 ಆಮ್ಲಜನಕ ಪ್ರೋಬ್, DS18B20 ತಾಪಮಾನ ಸೆನ್ಸರ್ ಮತ್ತು pH ಪ್ರೋಬ್‌ನ ಅಳತೆಗಳನ್ನು ಓದುತ್ತದೆ. |  |
| 62 | `app.js shopLoadFailed` | Could not load the products. Check your internet and reload the page. | ವಸ್ತುಗಳ ಪಟ್ಟಿ ತೆರೆಯಲು ಆಗಲಿಲ್ಲ. ಇಂಟರ್ನೆಟ್ ಪರಿಶೀಲಿಸಿ, ಪುಟವನ್ನು ಮತ್ತೆ ತೆರೆಯಿರಿ. |  |
| 63 | `app.js shopMeasures` | What it measures | ಏನನ್ನು ಅಳೆಯುತ್ತದೆ |  |
| 64 | `app.js shopWhy` | Why you need it | ಇದು ಏಕೆ ಬೇಕು |  |
| 65 | `app.js shopAdd` | Add to cart | ಕಾರ್ಟ್‌ಗೆ ಸೇರಿಸಿ |  |
| 66 | `app.js shopAdded` | Added to cart: | ಕಾರ್ಟ್‌ಗೆ ಸೇರಿಸಲಾಗಿದೆ: |  |
| 67 | `app.js estWord` | est. | ಅಂದಾಜು |  |
| 68 | `app.js cartTitle` | Cart | ಕಾರ್ಟ್ |  |
| 69 | `app.js cartAria` | Cart: {n} items | ಕಾರ್ಟ್: {n} ವಸ್ತುಗಳು |  |
| 70 | `app.js cartEmpty` | Your cart is empty. Add items from the Shop. | ನಿಮ್ಮ ಕಾರ್ಟ್ ಖಾಲಿಯಾಗಿದೆ. ಅಂಗಡಿಯಿಂದ ವಸ್ತುಗಳನ್ನು ಸೇರಿಸಿ. |  |
| 71 | `app.js cartTotal` | Estimated total | ಅಂದಾಜು ಒಟ್ಟು |  |
| 72 | `app.js cartRemove` | Remove | ತೆಗೆಯಿರಿ |  |
| 73 | `app.js cartLess` | One less | ಒಂದು ಕಡಿಮೆ |  |
| 74 | `app.js cartMore` | One more | ಒಂದು ಹೆಚ್ಚು |  |
| 75 | `app.js cartQty` | Quantity | ಪ್ರಮಾಣ |  |
| 76 | `app.js cartCheckout` | Checkout | ಚೆಕ್‌ಔಟ್ |  |
| 77 | `app.js cartClear` | Clear cart | ಕಾರ್ಟ್ ಖಾಲಿ ಮಾಡಿ |  |
| 78 | `app.js cartCleared` | Cart cleared. | ಕಾರ್ಟ್ ಖಾಲಿ ಮಾಡಲಾಗಿದೆ. |  |
| 79 | `app.js cartMemory` | This browser is not saving the cart. It is kept only until you close the page. | ಈ ಬ್ರೌಸರ್ ಕಾರ್ಟ್ ಅನ್ನು ಉಳಿಸುತ್ತಿಲ್ಲ. ಪುಟ ಮುಚ್ಚುವವರೆಗೆ ಮಾತ್ರ ಇರುತ್ತದೆ. |  |
| 80 | `app.js checkoutTitle` | Checkout | ಚೆಕ್‌ಔಟ್ |  |
| 81 | `app.js checkoutSoon` | Coming soon. Orders open after our pilot with farmers. No payment is taken and no details are collected. | ಶೀಘ್ರದಲ್ಲೇ ಬರಲಿದೆ. ರೈತರೊಂದಿಗಿನ ನಮ್ಮ ಪ್ರಾಯೋಗಿಕ ಯೋಜನೆಯ ನಂತರ ಆರ್ಡರ್‌ಗಳು ಆರಂಭವಾಗುತ್ತವೆ. ಯಾವುದೇ ಹಣ ಪಡೆಯುವುದಿಲ್ಲ ಮತ್ತು ಯಾವುದೇ ವಿವರಗಳನ್ನು ಸಂಗ್ರಹಿಸುವುದಿಲ್ಲ. |  |
| 82 | `app.js checkoutShare` | Copy your list to share it with your cooperative. | ನಿಮ್ಮ ಸಹಕಾರ ಸಂಘದೊಂದಿಗೆ ಹಂಚಿಕೊಳ್ಳಲು ಪಟ್ಟಿಯನ್ನು ನಕಲಿಸಿ. |  |
| 83 | `app.js copyList` | Copy my list | ನನ್ನ ಪಟ್ಟಿ ನಕಲಿಸಿ |  |
| 84 | `app.js checkoutBack` | Back to cart | ಕಾರ್ಟ್‌ಗೆ ಹಿಂತಿರುಗಿ |  |
| 85 | `app.js copyDone` | List copied. You can paste it into WhatsApp or SMS. | ಪಟ್ಟಿ ನಕಲಾಗಿದೆ. WhatsApp ಅಥವಾ SMS ನಲ್ಲಿ ಅಂಟಿಸಬಹುದು. |  |
| 86 | `app.js copyFailed` | Could not copy. Select the list above and copy it by hand. | ನಕಲಿಸಲು ಆಗಲಿಲ್ಲ. ಮೇಲಿನ ಪಟ್ಟಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ ಕೈಯಾರೆ ನಕಲಿಸಿ. |  |
| 87 | `app.js copyHeading` | AquaNexus: my list (estimated prices, not an order) | AquaNexus: ನನ್ನ ಪಟ್ಟಿ (ಅಂದಾಜು ಬೆಲೆಗಳು, ಆರ್ಡರ್ ಅಲ್ಲ) |  |
| 88 | `app.js stripDangerIn` | Danger in {d} | ಅಪಾಯಕ್ಕೆ ಉಳಿದ ಸಮಯ: {d} |  |
| 89 | `app.js stripNoDanger` | No danger expected | ಅಪಾಯದ ನಿರೀಕ್ಷೆ ಇಲ್ಲ |  |
| 90 | `app.js stripActNow` | Act now: tap to see | ಈಗಲೇ ಕ್ರಮ ಕೈಗೊಳ್ಳಿ: ನೋಡಲು ಒತ್ತಿ |  |
| 91 | `app.js stripAttention` | Needs attention: tap to see | ಗಮನ ಕೊಡಿ: ನೋಡಲು ಒತ್ತಿ |  |
| 92 | `app.js settingsTitle` | Settings | ಸೆಟ್ಟಿಂಗ್‌ಗಳು |  |
| 93 | `app.js settingsLanguage` | Language | ಭಾಷೆ |  |
| 94 | `app.js settingsTheme` | Colours | ಬಣ್ಣಗಳು |  |
| 95 | `app.js aboutTitle` | About this app | ಈ ಆ್ಯಪ್ ಬಗ್ಗೆ |  |

## 21. Messages from the server: Data labels

Shown on every simulated, test-kit or live-sensor reading.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `simulator.SIMULATED_LABEL` | Simulated data | ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಡೇಟಾ |  |
| 2 | `main.MANUAL_LABEL` | Manual test-kit reading | ಕೈಯಿಂದ ನಮೂದಿಸಿದ ಟೆಸ್ಟ್ ಕಿಟ್ ಅಳತೆ |  |
| 3 | `sensor.LIVE_LABEL` | Live sensor | ಲೈವ್ ಸೆನ್ಸರ್ |  |
| 4 | `sensor.DEMO_LABEL` | Demo device: simulated readings, not a real pond | ಡೆಮೊ ಸಾಧನ: ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಅಳತೆಗಳು, ನಿಜವಾದ ಕೊಳವಲ್ಲ |  |

## 22. Messages from the server: Live sensor: why a reading was refused

Sent back to the sensor and shown on the Live sensor card.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `sensor.REJECTED` | Reading rejected. Check the sensor. | ಅಳತೆಯನ್ನು ತಿರಸ್ಕರಿಸಲಾಗಿದೆ. ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ. |  |
| 2 | `sensor.NO_VALUES` | The reading has no values. Check the sensor. | ಅಳತೆಯಲ್ಲಿ ಯಾವುದೇ ಮೌಲ್ಯಗಳಿಲ್ಲ. ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ. |  |
| 3 | `sensor.WRONG_KEY` | Missing or wrong sensor key. | ಸೆನ್ಸರ್ ಕೀ ಇಲ್ಲ ಅಥವಾ ತಪ್ಪಾಗಿದೆ. |  |
| 4 | `sensor.CLOCK_AHEAD` | The sensor's clock is ahead of the real time. Check the sensor clock. | ಸೆನ್ಸರ್‌ನ ಗಡಿಯಾರ ನಿಜವಾದ ಸಮಯಕ್ಕಿಂತ ಮುಂದಿದೆ. ಸೆನ್ಸರ್ ಗಡಿಯಾರ ಪರಿಶೀಲಿಸಿ. |  |
| 5 | `sensor.NO_TIME_ZONE` | The timestamp has no time zone. Add +05:30 or Z. Check the sensor clock. | ಸಮಯದಲ್ಲಿ ಟೈಮ್ ಝೋನ್ ಇಲ್ಲ. +05:30 ಅಥವಾ Z ಸೇರಿಸಿ. ಸೆನ್ಸರ್ ಗಡಿಯಾರ ಪರಿಶೀಲಿಸಿ. |  |
| 6 | `sensor.TOO_OLD` | The timestamp is more than a day old. Check the sensor clock. | ಸಮಯ ಒಂದು ದಿನಕ್ಕಿಂತ ಹಳೆಯದು. ಸೆನ್ಸರ್ ಗಡಿಯಾರ ಪರಿಶೀಲಿಸಿ. |  |

## 23. Messages from the server: Risk card: level names, parameter names and reasons

`{value}` and `{unit}` are filled in by the app, e.g. 4.1 mg/L. `{name}` is a parameter name.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `risk_messages.LEVEL_NAMES.safe` | Safe | ಸುರಕ್ಷಿತ |  |
| 2 | `risk_messages.LEVEL_NAMES.warning` | Warning | ಎಚ್ಚರಿಕೆ |  |
| 3 | `risk_messages.LEVEL_NAMES.danger` | Danger | ಅಪಾಯ |  |
| 4 | `risk_messages.LEVEL_NAMES.unknown` | Unknown | ತಿಳಿದಿಲ್ಲ |  |
| 5 | `risk_messages.PARAMETER_NAMES.dissolved_oxygen` | Dissolved oxygen | ಕರಗಿದ ಆಮ್ಲಜನಕ |  |
| 6 | `risk_messages.PARAMETER_NAMES.ph` | pH | ಪಿಎಚ್ (pH) |  |
| 7 | `risk_messages.PARAMETER_NAMES.temperature` | Water temperature | ನೀರಿನ ತಾಪಮಾನ |  |
| 8 | `risk_messages.PARAMETER_NAMES.ammonia` | Ammonia | ಅಮೋನಿಯಾ |  |
| 9 | `risk_messages.PARAMETER_NAMES.nitrate` | Nitrate | ನೈಟ್ರೇಟ್ |  |
| 10 | `risk_messages.PARAMETER_NAMES.turbidity` | Turbidity | ನೀರಿನ ಮಬ್ಬು (ಟರ್ಬಿಡಿಟಿ) |  |
| 11 | `risk_messages.PARAMETER_NAMES.salinity` | Salinity | ಲವಣಾಂಶ |  |
| 12 | `risk_messages.REASONS.dissolved_oxygen/low/warning` | Oxygen is low ({value} {unit}). Fish may stop eating. Run the aerator. | ಆಮ್ಲಜನಕ ಕಡಿಮೆ ಇದೆ ({value} {unit}). ಮೀನುಗಳು ಆಹಾರ ತಿನ್ನುವುದನ್ನು ನಿಲ್ಲಿಸಬಹುದು. ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ. |  |
| 13 | `risk_messages.REASONS.dissolved_oxygen/low/danger` | Oxygen is very low ({value} {unit}). Fish can die. Turn on the aerator now and add fresh water. | ಆಮ್ಲಜನಕ ತುಂಬಾ ಕಡಿಮೆ ಇದೆ ({value} {unit}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ತಕ್ಷಣ ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ ಮತ್ತು ಹೊಸ ನೀರು ಹಾಕಿ. |  |
| 14 | `risk_messages.REASONS.ph/low/warning` | Water is acidic (pH {value}). Fish grow slowly. Contact your fisheries officer for advice on correcting pH. | ನೀರು ಆಮ್ಲೀಯವಾಗಿದೆ (pH {value}). ಮೀನುಗಳು ನಿಧಾನವಾಗಿ ಬೆಳೆಯುತ್ತವೆ. pH ಸರಿಪಡಿಸುವ ಬಗ್ಗೆ ಸಲಹೆಗಾಗಿ ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ. |  |
| 15 | `risk_messages.REASONS.ph/low/danger` | Water is very acidic (pH {value}). Fish can die. Add fresh water and contact your fisheries officer today. | ನೀರು ತುಂಬಾ ಆಮ್ಲೀಯವಾಗಿದೆ (pH {value}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ಹೊಸ ನೀರು ಹಾಕಿ ಮತ್ತು ಇಂದೇ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ. |  |
| 16 | `risk_messages.REASONS.ph/high/warning` | Water is alkaline (pH {value}). Ammonia becomes more harmful. Add fresh water and stop adding fertiliser. | ನೀರು ಕ್ಷಾರೀಯವಾಗಿದೆ (pH {value}). ಅಮೋನಿಯಾ ಹೆಚ್ಚು ಹಾನಿಕಾರಕವಾಗುತ್ತದೆ. ಹೊಸ ನೀರು ಹಾಕಿ ಮತ್ತು ಗೊಬ್ಬರ ಹಾಕುವುದನ್ನು ನಿಲ್ಲಿಸಿ. |  |
| 17 | `risk_messages.REASONS.ph/high/danger` | Water is very alkaline (pH {value}). Fish can die. Add fresh water now and contact your fisheries officer. | ನೀರು ತುಂಬಾ ಕ್ಷಾರೀಯವಾಗಿದೆ (pH {value}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ತಕ್ಷಣ ಹೊಸ ನೀರು ಹಾಕಿ ಮತ್ತು ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ. |  |
| 18 | `risk_messages.REASONS.temperature/low/warning` | Water is cool ({value} {unit}). Fish eat less. Reduce the feed. | ನೀರು ತಣ್ಣಗಿದೆ ({value} {unit}). ಮೀನುಗಳು ಕಡಿಮೆ ತಿನ್ನುತ್ತವೆ. ಆಹಾರ ಕಡಿಮೆ ಮಾಡಿ. |  |
| 19 | `risk_messages.REASONS.temperature/low/danger` | Water is too cold ({value} {unit}). Fish are stressed and may fall sick. Feed very little. | ನೀರು ತುಂಬಾ ತಣ್ಣಗಿದೆ ({value} {unit}). ಮೀನುಗಳಿಗೆ ಒತ್ತಡ ಉಂಟಾಗಿ ರೋಗ ಬರಬಹುದು. ತುಂಬಾ ಕಡಿಮೆ ಆಹಾರ ನೀಡಿ. |  |
| 20 | `risk_messages.REASONS.temperature/high/warning` | Water is warm ({value} {unit}). Oxygen will drop. Run the aerator and add fresh water. | ನೀರು ಬಿಸಿಯಾಗಿದೆ ({value} {unit}). ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗುತ್ತದೆ. ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ ಮತ್ತು ಹೊಸ ನೀರು ಹಾಕಿ. |  |
| 21 | `risk_messages.REASONS.temperature/high/danger` | Water is too hot ({value} {unit}). Fish can die. Add fresh water now, run the aerator and stop feeding. | ನೀರು ತುಂಬಾ ಬಿಸಿಯಾಗಿದೆ ({value} {unit}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ತಕ್ಷಣ ಹೊಸ ನೀರು ಹಾಕಿ, ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ ಮತ್ತು ಆಹಾರ ನಿಲ್ಲಿಸಿ. |  |
| 22 | `risk_messages.REASONS.ammonia/high/warning` | Harmful ammonia is rising ({value} {unit}). Reduce the feed and add fresh water. | ಹಾನಿಕಾರಕ ಅಮೋನಿಯಾ ಹೆಚ್ಚುತ್ತಿದೆ ({value} {unit}). ಆಹಾರ ಕಡಿಮೆ ಮಾಡಿ ಮತ್ತು ಹೊಸ ನೀರು ಹಾಕಿ. |  |
| 23 | `risk_messages.REASONS.ammonia/high/danger` | Harmful ammonia is very high ({value} {unit}). Fish can die. Stop feeding today and add fresh water. | ಹಾನಿಕಾರಕ ಅಮೋನಿಯಾ ತುಂಬಾ ಹೆಚ್ಚಾಗಿದೆ ({value} {unit}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ಇಂದು ಆಹಾರ ನೀಡುವುದನ್ನು ನಿಲ್ಲಿಸಿ ಮತ್ತು ಹೊಸ ನೀರು ಹಾಕಿ. |  |
| 24 | `risk_messages.REASONS.nitrate/high/warning` | Nitrate is high ({value} {unit}). Change some of the water and reduce the feed. | ನೈಟ್ರೇಟ್ ಹೆಚ್ಚಾಗಿದೆ ({value} {unit}). ಸ್ವಲ್ಪ ನೀರು ಬದಲಾಯಿಸಿ ಮತ್ತು ಆಹಾರ ಕಡಿಮೆ ಮಾಡಿ. |  |
| 25 | `risk_messages.ALL_SAFE` | All readings are in the safe range. | ಎಲ್ಲಾ ಅಳತೆಗಳು ಸುರಕ್ಷಿತ ಮಟ್ಟದಲ್ಲಿವೆ. |  |
| 26 | `risk_messages.SENSOR_ERROR` | {name} reading looks wrong ({value}). Check the sensor. | {name} ಅಳತೆ ತಪ್ಪಾಗಿರುವಂತೆ ಕಾಣುತ್ತಿದೆ ({value}). ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ. |  |
| 27 | `risk_messages.TEST_KIT_ERROR` | {name} reading looks impossible ({value}). Check your test kit and test again. | {name} ಅಳತೆ ಅಸಾಧ್ಯವೆಂದು ಕಾಣುತ್ತಿದೆ ({value}). ನಿಮ್ಮ ಟೆಸ್ಟ್ ಕಿಟ್ ಪರಿಶೀಲಿಸಿ ಮತ್ತೆ ಪರೀಕ್ಷಿಸಿ. |  |
| 28 | `risk_messages.AMMONIA_NEEDS_PH_AND_TEMPERATURE` | Ammonia could not be checked because pH or temperature is missing. | pH ಅಥವಾ ತಾಪಮಾನ ಇಲ್ಲದ ಕಾರಣ ಅಮೋನಿಯಾ ಪರಿಶೀಲಿಸಲು ಆಗಲಿಲ್ಲ. |  |
| 29 | `risk_messages.NO_VALID_READINGS` | No valid readings. Check the sensors. | ಸರಿಯಾದ ಅಳತೆಗಳು ಇಲ್ಲ. ಸೆನ್ಸರ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ. |  |
| 30 | `risk_messages.NO_VALID_TEST_KIT_READINGS` | No valid readings. Check your test kit. | ಸರಿಯಾದ ಅಳತೆಗಳು ಇಲ್ಲ. ನಿಮ್ಮ ಟೆಸ್ಟ್ ಕಿಟ್ ಪರಿಶೀಲಿಸಿ. |  |

## 24. Messages from the server: Time until danger (messages)

`{rate}` e.g. 0.6, `{danger}` e.g. 3, `{clock}` e.g. 03:20, `{hours}` e.g. 6. `{duration_kn}` is one of the two duration phrases below.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `risk_messages.TIME_TO_DANGER.danger_expected` | Oxygen is falling (about {rate} mg/L per hour). At this rate it may reach the danger level ({danger} mg/L) in {duration}, around {clock}. Get the aerator ready now. | ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗುತ್ತಿದೆ (ಗಂಟೆಗೆ ಸುಮಾರು {rate} mg/L). ಇದೇ ವೇಗದಲ್ಲಿ {duration_kn} ({clock} ಹೊತ್ತಿಗೆ) ಅಪಾಯದ ಮಟ್ಟ ({danger} mg/L) ತಲುಪಬಹುದು. ಈಗಲೇ ಏರೇಟರ್ ಸಿದ್ಧಪಡಿಸಿ. |  |
| 2 | `risk_messages.TIME_TO_DANGER.already_danger` | Oxygen is already at the danger level. | ಆಮ್ಲಜನಕ ಈಗಾಗಲೇ ಅಪಾಯದ ಮಟ್ಟದಲ್ಲಿದೆ. |  |
| 3 | `risk_messages.TIME_TO_DANGER.falling_slowly` | Oxygen is falling slowly. No danger expected in the next {hours} hours. | ಆಮ್ಲಜನಕ ನಿಧಾನವಾಗಿ ಕಡಿಮೆಯಾಗುತ್ತಿದೆ. ಮುಂದಿನ {hours} ಗಂಟೆಗಳಲ್ಲಿ ಅಪಾಯ ನಿರೀಕ್ಷಿಸಿಲ್ಲ. |  |
| 4 | `risk_messages.TIME_TO_DANGER.not_falling` | Oxygen is not falling. | ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗುತ್ತಿಲ್ಲ. |  |
| 5 | `risk_messages.TIME_TO_DANGER.not_enough_data` | Not enough recent oxygen readings to estimate. | ಅಂದಾಜು ಮಾಡಲು ಇತ್ತೀಚಿನ ಆಮ್ಲಜನಕ ಅಳತೆಗಳು ಸಾಕಷ್ಟಿಲ್ಲ. |  |
| 6 | `time_to_danger._duration (under 1 hour)` | about {minutes} minutes | ಸುಮಾರು {minutes} ನಿಮಿಷಗಳಲ್ಲಿ |  |
| 7 | `time_to_danger._duration (1 hour or more)` | about {text} hours | ಸುಮಾರು {text} ಗಂಟೆಗಳಲ್ಲಿ |  |

## 25. Messages from the server: Tonight's weather (messages)

`{night}` is one or more of the night words joined together, e.g. "cloudy, still".

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `weather.MANGALURU.name` | Mangaluru | ಮಂಗಳೂರು |  |
| 2 | `weather.LEVEL_NAMES.low` | Low | ಕಡಿಮೆ |  |
| 3 | `weather.LEVEL_NAMES.medium` | Medium | ಮಧ್ಯಮ |  |
| 4 | `weather.LEVEL_NAMES.high` | High | ಹೆಚ್ಚು |  |
| 5 | `weather.FACTOR_WORDS.cloudy` | cloudy | ಮೋಡ ಕವಿದ |  |
| 6 | `weather.FACTOR_WORDS.still` | still | ಗಾಳಿಯಿಲ್ಲದ |  |
| 7 | `weather.FACTOR_WORDS.warm` | warm | ಸೆಖೆಯ |  |
| 8 | `weather.ADVICE.low` | Weather looks fine tonight: low risk of an oxygen crash. | ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ ಸರಿಯಾಗಿದೆ: ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯ ಕಡಿಮೆ. |  |
| 9 | `weather.ADVICE.medium` | {night} night ahead: check the pond late at night and before dawn. | {night} ರಾತ್ರಿ ಬರಲಿದೆ: ತಡರಾತ್ರಿ ಮತ್ತು ಬೆಳಗಾಗುವ ಮೊದಲು ಕೊಳವನ್ನು ನೋಡಿ. |  |
| 10 | `weather.ADVICE.high` | {night} night ahead: keep the aerator ready. | {night} ರಾತ್ರಿ ಬರಲಿದೆ: ಏರೇಟರ್ ಸಿದ್ಧವಾಗಿಡಿ. |  |
| 11 | `weather.UNAVAILABLE` | No internet and no saved forecast. Tonight's weather is not known. | ಇಂಟರ್ನೆಟ್ ಇಲ್ಲ, ಉಳಿಸಿದ ಮುನ್ಸೂಚನೆಯೂ ಇಲ್ಲ. ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ ತಿಳಿದಿಲ್ಲ. |  |

## 26. Messages from the server: What to do now (checklist items)

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `actions.ACTIONS.aerator_now` | Run the aerator now. If you have none, splash the water hard with a paddle or stick. | ಈಗಲೇ ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ. ಏರೇಟರ್ ಇಲ್ಲದಿದ್ದರೆ ಹುಟ್ಟು ಅಥವಾ ಕೋಲಿನಿಂದ ನೀರನ್ನು ಜೋರಾಗಿ ಬಡಿಯಿರಿ. |  |
| 2 | `actions.ACTIONS.stop_feeding` | Stop feeding until the reading is back to normal. | ಅಳತೆ ಸಾಮಾನ್ಯ ಸ್ಥಿತಿಗೆ ಬರುವವರೆಗೆ ಆಹಾರ ನೀಡುವುದನ್ನು ನಿಲ್ಲಿಸಿ. |  |
| 3 | `actions.ACTIONS.cool_water` | Let in cooler water and drain off the warmest water from the top. | ತಂಪಾದ ನೀರು ಒಳಗೆ ಬಿಡಿ ಮತ್ತು ಮೇಲಿನ ಬಿಸಿ ನೀರನ್ನು ಹೊರಗೆ ಬಿಡಿ. |  |
| 4 | `actions.ACTIONS.fresh_water` | Let in fresh, clean water and drain some of the stale bottom water. | ಶುದ್ಧ ಹೊಸ ನೀರು ಒಳಗೆ ಬಿಡಿ ಮತ್ತು ತಳದ ಹಳೆಯ ನೀರನ್ನು ಸ್ವಲ್ಪ ಹೊರಗೆ ಬಿಡಿ. |  |
| 5 | `actions.ACTIONS.water_change` | Change a quarter to half of the pond water, only if your new water is clean. | ಹೊಸ ನೀರು ಶುದ್ಧವಾಗಿದ್ದರೆ ಮಾತ್ರ, ಕೊಳದ ಕಾಲು ಭಾಗದಿಂದ ಅರ್ಧದಷ್ಟು ನೀರನ್ನು ಬದಲಾಯಿಸಿ. |  |
| 6 | `actions.ACTIONS.aerator_night` | Run the aerator tonight, from late evening until after sunrise. | ಇಂದು ರಾತ್ರಿ ಸಂಜೆ ತಡವಾಗಿನಿಂದ ಸೂರ್ಯೋದಯದ ನಂತರದವರೆಗೆ ಏರೇಟರ್ ಚಾಲೂ ಇಡಿ. |  |
| 7 | `actions.ACTIONS.reduce_feeding` | Give less feed today. Do not overfeed. | ಇಂದು ಕಡಿಮೆ ಆಹಾರ ನೀಡಿ. ಹೆಚ್ಚು ಆಹಾರ ಹಾಕಬೇಡಿ. |  |
| 8 | `actions.ACTIONS.no_fertiliser` | Do not add fertiliser or manure for now. | ಸದ್ಯಕ್ಕೆ ಗೊಬ್ಬರ ಅಥವಾ ಸಗಣಿ ಹಾಕಬೇಡಿ. |  |
| 9 | `actions.ACTIONS.watch_fish` | Watch for fish gasping at the surface, especially before sunrise. | ಮೀನುಗಳು ಮೇಲ್ಮೈಗೆ ಬಂದು ಗಾಳಿಗಾಗಿ ಒದ್ದಾಡುತ್ತಿವೆಯೇ ನೋಡಿ, ವಿಶೇಷವಾಗಿ ಸೂರ್ಯೋದಯದ ಮೊದಲು. |  |
| 10 | `actions.ACTIONS.retest_oxygen_evening` | Test oxygen again late this evening (8–10 pm) to see if it will fall too low at night. | ರಾತ್ರಿ ಆಮ್ಲಜನಕ ತುಂಬಾ ಕಡಿಮೆಯಾಗುತ್ತದೆಯೇ ಎಂದು ತಿಳಿಯಲು ಇಂದು ರಾತ್ರಿ 8–10 ಗಂಟೆಗೆ ಮತ್ತೆ ಪರೀಕ್ಷಿಸಿ. |  |
| 11 | `actions.ACTIONS.retest_ph_morning` | Test pH again early tomorrow morning. pH is highest in the afternoon and falls by morning. | ನಾಳೆ ಬೆಳಿಗ್ಗೆ ಬೇಗ pH ಮತ್ತೆ ಪರೀಕ್ಷಿಸಿ. ಮಧ್ಯಾಹ್ನ pH ಅತಿ ಹೆಚ್ಚಿರುತ್ತದೆ, ಬೆಳಿಗ್ಗೆಗೆ ಕಡಿಮೆಯಾಗುತ್ತದೆ. |  |
| 12 | `actions.ACTIONS.retest_ph_afternoon` | Test pH again this afternoon. pH is lowest in the early morning and rises during the day. | ಇಂದು ಮಧ್ಯಾಹ್ನ pH ಮತ್ತೆ ಪರೀಕ್ಷಿಸಿ. ಬೆಳಿಗ್ಗೆ pH ಅತಿ ಕಡಿಮೆ ಇರುತ್ತದೆ, ಹಗಲಿನಲ್ಲಿ ಏರುತ್ತದೆ. |  |

## 27. Messages from the server: Fish disease guide: diseases

Disease names, signs, seasons, prevention and what to do. Scientific names (e.g. Aphanomyces invadans) stay in Latin.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `diseases.DISEASES.eus.name` | Epizootic ulcerative syndrome (EUS, red spot disease) | ಎಪಿಜೂಟಿಕ್ ಅಲ್ಸರೇಟಿವ್ ಸಿಂಡ್ರೋಮ್ (EUS, ಕೆಂಪು ಚುಕ್ಕೆ ಹುಣ್ಣು ರೋಗ) |  |
| 2 | `diseases.DISEASES.eus.body` | Starts as red spots. These become deep open sores that go into the muscle. Older sores can have a raised white edge. | ಕೆಂಪು ಚುಕ್ಕೆಗಳಾಗಿ ಆರಂಭವಾಗುತ್ತದೆ. ಅವು ಸ್ನಾಯುವಿನೊಳಗೆ ಹೋಗುವ ಆಳವಾದ ತೆರೆದ ಹುಣ್ಣುಗಳಾಗುತ್ತವೆ. ಹಳೆಯ ಹುಣ್ಣುಗಳಿಗೆ ಎದ್ದ ಬಿಳಿ ಅಂಚು ಇರಬಹುದು. |  |
| 3 | `diseases.DISEASES.eus.behaviour` | Many fish can die in an outbreak. | ರೋಗ ಹರಡಿದಾಗ ಅನೇಕ ಮೀನುಗಳು ಸಾಯಬಹುದು. |  |
| 4 | `diseases.DISEASES.eus.when` | In cool weather, and when runoff makes the water acidic. Spreads with floods and when fish are moved. Chinese carps resist it. | ತಂಪಾದ ಹವಾಮಾನದಲ್ಲಿ, ಮತ್ತು ಹರಿದು ಬಂದ ನೀರು ಕೊಳವನ್ನು ಆಮ್ಲೀಯಗೊಳಿಸಿದಾಗ. ಪ್ರವಾಹದಿಂದ ಮತ್ತು ಮೀನುಗಳನ್ನು ಸಾಗಿಸಿದಾಗ ಹರಡುತ್ತದೆ. ಚೀನೀ ಗೆಂಡೆಗಳು ಇದನ್ನು ತಡೆದುಕೊಳ್ಳುತ್ತವೆ. |  |
| 5 | `diseases.DISEASES.eus.prevention[0]` | Dry the pond completely before stocking. Ask your fisheries officer about liming. | ಮೀನು ಬಿಡುವ ಮೊದಲು ಕೊಳವನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ಒಣಗಿಸಿ. ಸುಣ್ಣ ಹಾಕುವ ಬಗ್ಗೆ ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯನ್ನು ಕೇಳಿ. |  |
| 6 | `diseases.DISEASES.eus.prevention[1]` | Keep wild fish out of the pond. Stock hatchery-reared seed. | ಕಾಡು ಮೀನುಗಳು ಕೊಳಕ್ಕೆ ಬರದಂತೆ ತಡೆಯಿರಿ. ಮೊಟ್ಟೆಕೇಂದ್ರದಲ್ಲಿ ಬೆಳೆಸಿದ ಮರಿಗಳನ್ನು ಬಿಡಿ. |  |
| 7 | `diseases.DISEASES.eus.prevention[2]` | Clean nets and tools before using them in another pond. | ಬಲೆ ಮತ್ತು ಸಾಧನಗಳನ್ನು ಬೇರೆ ಕೊಳದಲ್ಲಿ ಬಳಸುವ ಮೊದಲು ಸ್ವಚ್ಛಗೊಳಿಸಿ. |  |
| 8 | `diseases.DISEASES.eus.do[0]` | Ulcers can also come from other diseases, so a laboratory test is needed to be sure. | ಹುಣ್ಣುಗಳು ಬೇರೆ ರೋಗಗಳಿಂದಲೂ ಬರಬಹುದು, ಆದ್ದರಿಂದ ಖಚಿತಪಡಿಸಲು ಪ್ರಯೋಗಾಲಯ ಪರೀಕ್ಷೆ ಬೇಕು. |  |
| 9 | `diseases.DISEASES.aeromoniasis.name` | Aeromonas infection (dropsy, haemorrhagic septicaemia) | ಏರೋಮೋನಾಸ್ ಸೋಂಕು (ಹೊಟ್ಟೆ ಊತ / ಡ್ರಾಪ್ಸಿ, ರಕ್ತಸ್ರಾವ ರೋಗ) |  |
| 10 | `diseases.DISEASES.aeromoniasis.body` | Large red, bleeding patches on the skin, often at the fin bases and vent, that can become sores. Swollen belly, scales standing out, bulging eyes, rotting fins. | ಚರ್ಮದ ಮೇಲೆ, ಹೆಚ್ಚಾಗಿ ಈಜುರೆಕ್ಕೆಗಳ ಬುಡ ಮತ್ತು ಗುದದ ಬಳಿ, ದೊಡ್ಡ ಕೆಂಪು ರಕ್ತಸ್ರಾವದ ಕಲೆಗಳು, ಅವು ಹುಣ್ಣಾಗಬಹುದು. ಊದಿದ ಹೊಟ್ಟೆ, ಎದ್ದ ಹುರುಪೆಗಳು, ಉಬ್ಬಿದ ಕಣ್ಣುಗಳು, ಕೊಳೆಯುವ ಈಜುರೆಕ್ಕೆಗಳು. |  |
| 11 | `diseases.DISEASES.aeromoniasis.behaviour` | Sick fish swim slowly. Many can die soon after the red patches appear. | ರೋಗಪೀಡಿತ ಮೀನುಗಳು ನಿಧಾನವಾಗಿ ಈಜುತ್ತವೆ. ಕೆಂಪು ಕಲೆಗಳು ಕಾಣಿಸಿದ ಸ್ವಲ್ಪ ಸಮಯದಲ್ಲೇ ಅನೇಕ ಮೀನುಗಳು ಸಾಯಬಹುದು. |  |
| 12 | `diseases.DISEASES.aeromoniasis.when` | When fish are stressed: crowding, low oxygen, dirty water with a lot of waste, rough handling, high or changing temperature, and high ammonia. | ಮೀನುಗಳು ಒತ್ತಡದಲ್ಲಿದ್ದಾಗ: ಹೆಚ್ಚು ಮೀನು ತುಂಬಿದಾಗ, ಕಡಿಮೆ ಆಮ್ಲಜನಕ, ಹೆಚ್ಚು ತ್ಯಾಜ್ಯವಿರುವ ಕೊಳಕು ನೀರು, ಒರಟು ನಿರ್ವಹಣೆ, ಹೆಚ್ಚಿನ ಅಥವಾ ಬದಲಾಗುವ ತಾಪಮಾನ, ಮತ್ತು ಹೆಚ್ಚಿನ ಅಮೋನಿಯಾ. |  |
| 13 | `diseases.DISEASES.aeromoniasis.prevention[0]` | Do not overstock. Crowding builds up waste and uses up oxygen. | ಹೆಚ್ಚು ಮೀನು ಬಿಡಬೇಡಿ. ದಟ್ಟಣೆಯಿಂದ ತ್ಯಾಜ್ಯ ಹೆಚ್ಚುತ್ತದೆ ಮತ್ತು ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗುತ್ತದೆ. |  |
| 14 | `diseases.DISEASES.aeromoniasis.prevention[1]` | Keep oxygen and ammonia in the safe range. Do not overfeed. | ಆಮ್ಲಜನಕ ಮತ್ತು ಅಮೋನಿಯಾವನ್ನು ಸುರಕ್ಷಿತ ಮಟ್ಟದಲ್ಲಿಡಿ. ಹೆಚ್ಚು ಆಹಾರ ಹಾಕಬೇಡಿ. |  |
| 15 | `diseases.DISEASES.aeromoniasis.prevention[2]` | Handle and transport fish gently and as little as possible, not in hot weather. | ಮೀನುಗಳನ್ನು ನಿಧಾನವಾಗಿ, ಸಾಧ್ಯವಾದಷ್ಟು ಕಡಿಮೆ ನಿರ್ವಹಿಸಿ ಮತ್ತು ಸಾಗಿಸಿ, ಬಿಸಿ ಹವಾಮಾನದಲ್ಲಿ ಬೇಡ. |  |
| 16 | `diseases.DISEASES.aeromoniasis.do[0]` | Do not buy medicines yourself. In Indian carp ponds, several drugs tried for dropsy did not work. | ನೀವೇ ಔಷಧಿ ಖರೀದಿಸಬೇಡಿ. ಭಾರತದ ಗೆಂಡೆ ಮೀನಿನ ಕೊಳಗಳಲ್ಲಿ, ಡ್ರಾಪ್ಸಿಗೆ ಪ್ರಯತ್ನಿಸಿದ ಹಲವು ಔಷಧಿಗಳು ಫಲ ನೀಡಲಿಲ್ಲ. |  |
| 17 | `diseases.DISEASES.gill_disease.name` | Bacterial gill disease (gill rot) | ಬ್ಯಾಕ್ಟೀರಿಯಾದ ಕಿವಿರು ರೋಗ (ಕಿವಿರು ಕೊಳೆ) |  |
| 18 | `diseases.DISEASES.gill_disease.body` | Gills are pale and rotten, often covered with mud and slime. The fish looks dark, especially the head. The gill cover can be red inside, or rot through. | ಕಿವಿರುಗಳು ಬಿಳಿಚಿ ಕೊಳೆತಿರುತ್ತವೆ, ಹೆಚ್ಚಾಗಿ ಕೆಸರು ಮತ್ತು ಲೋಳೆಯಿಂದ ಮುಚ್ಚಿರುತ್ತವೆ. ಮೀನು, ವಿಶೇಷವಾಗಿ ತಲೆ, ಕಪ್ಪಾಗಿ ಕಾಣುತ್ತದೆ. ಕಿವಿರು ಮುಚ್ಚಳ ಒಳಗೆ ಕೆಂಪಾಗಿರಬಹುದು ಅಥವಾ ಕೊಳೆತು ತೂತಾಗಬಹುದು. |  |
| 19 | `diseases.DISEASES.gill_disease.behaviour` | Our sources describe the body signs only. | ನಮ್ಮ ಮೂಲಗಳು ದೇಹದ ಲಕ್ಷಣಗಳನ್ನು ಮಾತ್ರ ವಿವರಿಸುತ್ತವೆ. |  |
| 20 | `diseases.DISEASES.gill_disease.when` | Warm water: it starts above 20 °C and is worst at 28-35 °C. Grass carp is hit hardest. | ಬೆಚ್ಚಗಿನ ನೀರಿನಲ್ಲಿ: 20 °C ಮೇಲೆ ಆರಂಭವಾಗುತ್ತದೆ, 28-35 °C ನಲ್ಲಿ ಹೆಚ್ಚು. ಹುಲ್ಲು ಗೆಂಡೆ (ಗ್ರಾಸ್ ಕಾರ್ಪ್) ಹೆಚ್ಚು ಬಾಧಿತವಾಗುತ್ತದೆ. |  |
| 21 | `diseases.DISEASES.gill_disease.prevention[0]` | Keep the water clean and do not overstock. | ನೀರನ್ನು ಶುದ್ಧವಾಗಿಡಿ ಮತ್ತು ಹೆಚ್ಚು ಮೀನು ಬಿಡಬೇಡಿ. |  |
| 22 | `diseases.DISEASES.gill_disease.prevention[1]` | In the hot months, check the pond every morning. | ಬಿಸಿ ತಿಂಗಳುಗಳಲ್ಲಿ ಪ್ರತಿದಿನ ಬೆಳಿಗ್ಗೆ ಕೊಳವನ್ನು ಪರಿಶೀಲಿಸಿ. |  |
| 23 | `diseases.DISEASES.columnaris.name` | Columnaris disease (fin and skin rot) | ಕಾಲಮ್ನಾರಿಸ್ ರೋಗ (ಈಜುರೆಕ್ಕೆ ಮತ್ತು ಚರ್ಮ ಕೊಳೆ) |  |
| 24 | `diseases.DISEASES.columnaris.body` | In rohu, rot starts at the edges of the fins and spreads to the body. White sores and bleeding spots. Patches covered with white-yellow slime. Gills can be eaten away. | ರೋಹುವಿನಲ್ಲಿ, ಕೊಳೆ ಈಜುರೆಕ್ಕೆಗಳ ಅಂಚಿನಿಂದ ಆರಂಭವಾಗಿ ದೇಹಕ್ಕೆ ಹರಡುತ್ತದೆ. ಬಿಳಿ ಹುಣ್ಣುಗಳು ಮತ್ತು ರಕ್ತಸ್ರಾವದ ಚುಕ್ಕೆಗಳು. ಬಿಳಿ-ಹಳದಿ ಲೋಳೆಯಿಂದ ಮುಚ್ಚಿದ ಕಲೆಗಳು. ಕಿವಿರುಗಳು ಸವೆದುಹೋಗಬಹುದು. |  |
| 25 | `diseases.DISEASES.columnaris.behaviour` | Many fish can die. | ಅನೇಕ ಮೀನುಗಳು ಸಾಯಬಹುದು. |  |
| 26 | `diseases.DISEASES.columnaris.when` | Above 18 °C, and more when the water is warmer. Crowding, handling and injuries set it off. | 18 °C ಮೇಲೆ, ನೀರು ಹೆಚ್ಚು ಬೆಚ್ಚಗಾದಂತೆ ಹೆಚ್ಚು. ದಟ್ಟಣೆ, ನಿರ್ವಹಣೆ ಮತ್ತು ಗಾಯಗಳು ಇದನ್ನು ಪ್ರಚೋದಿಸುತ್ತವೆ. |  |
| 27 | `diseases.DISEASES.columnaris.prevention[0]` | Avoid crowding and rough netting, which injure the skin. | ಚರ್ಮಕ್ಕೆ ಗಾಯ ಮಾಡುವ ದಟ್ಟಣೆ ಮತ್ತು ಒರಟು ಬಲೆ ಹಾಕುವಿಕೆಯನ್ನು ತಪ್ಪಿಸಿ. |  |
| 28 | `diseases.DISEASES.columnaris.prevention[1]` | Do not handle fish when the water is very warm. | ನೀರು ತುಂಬಾ ಬೆಚ್ಚಗಿರುವಾಗ ಮೀನುಗಳನ್ನು ನಿರ್ವಹಿಸಬೇಡಿ. |  |
| 29 | `diseases.DISEASES.saprolegniasis.name` | Saprolegniasis (cotton wool disease) | ಸಾಪ್ರೊಲೆಗ್ನಿಯಾಸಿಸ್ (ಹತ್ತಿ ಬೂಷ್ಟು ರೋಗ) |  |
| 30 | `diseases.DISEASES.saprolegniasis.body` | A white, grey or brownish cotton-wool growth on any part of the body, usually on a wound. Lots of slime. Under the growth the muscle rots. | ದೇಹದ ಯಾವುದೇ ಭಾಗದಲ್ಲಿ, ಸಾಮಾನ್ಯವಾಗಿ ಗಾಯದ ಮೇಲೆ, ಬಿಳಿ, ಬೂದು ಅಥವಾ ಕಂದು ಹತ್ತಿಯಂತಹ ಬೆಳವಣಿಗೆ. ಹೆಚ್ಚು ಲೋಳೆ. ಬೆಳವಣಿಗೆಯ ಕೆಳಗೆ ಸ್ನಾಯು ಕೊಳೆಯುತ್ತದೆ. |  |
| 31 | `diseases.DISEASES.saprolegniasis.behaviour` | Fish rub against things, stop eating and move slowly. | ಮೀನುಗಳು ವಸ್ತುಗಳಿಗೆ ಉಜ್ಜಿಕೊಳ್ಳುತ್ತವೆ, ತಿನ್ನುವುದನ್ನು ನಿಲ್ಲಿಸುತ್ತವೆ ಮತ್ತು ನಿಧಾನವಾಗಿ ಚಲಿಸುತ್ತವೆ. |  |
| 32 | `diseases.DISEASES.saprolegniasis.when` | Any time of year, after injuries from netting, transport, stocking, spawning or crowding, or on sores from another disease. Worse in crowded ponds in the cool months. | ವರ್ಷದ ಯಾವುದೇ ಸಮಯದಲ್ಲಿ, ಬಲೆ, ಸಾಗಣೆ, ಮೀನು ಬಿಡುವಿಕೆ, ಮೊಟ್ಟೆ ಇಡುವಿಕೆ ಅಥವಾ ದಟ್ಟಣೆಯಿಂದಾದ ಗಾಯಗಳ ನಂತರ, ಅಥವಾ ಬೇರೆ ರೋಗದ ಹುಣ್ಣುಗಳ ಮೇಲೆ. ತಂಪು ತಿಂಗಳುಗಳಲ್ಲಿ ದಟ್ಟ ಕೊಳಗಳಲ್ಲಿ ಹೆಚ್ಚು. |  |
| 33 | `diseases.DISEASES.saprolegniasis.prevention[0]` | Net, carry and stock fish gently so they are not injured. | ಮೀನುಗಳಿಗೆ ಗಾಯವಾಗದಂತೆ ನಿಧಾನವಾಗಿ ಬಲೆ ಹಾಕಿ, ಸಾಗಿಸಿ ಮತ್ತು ಬಿಡಿ. |  |
| 34 | `diseases.DISEASES.saprolegniasis.prevention[1]` | Do not overcrowd the pond. | ಕೊಳದಲ್ಲಿ ಹೆಚ್ಚು ದಟ್ಟಣೆ ಮಾಡಬೇಡಿ. |  |
| 35 | `diseases.DISEASES.saprolegniasis.do[0]` | The mould usually grows on a wound or another disease. Look for the first problem too (EUS, anchor worm, injuries). | ಬೂಷ್ಟು ಸಾಮಾನ್ಯವಾಗಿ ಗಾಯ ಅಥವಾ ಬೇರೆ ರೋಗದ ಮೇಲೆ ಬೆಳೆಯುತ್ತದೆ. ಮೊದಲ ಸಮಸ್ಯೆಯನ್ನೂ ಹುಡುಕಿ (EUS, ಲಂಗರು ಹುಳು, ಗಾಯಗಳು). |  |
| 36 | `diseases.DISEASES.argulosis.name` | Argulosis (fish louse) | ಆರ್ಗುಲೋಸಿಸ್ (ಮೀನು ಹೇನು) |  |
| 37 | `diseases.DISEASES.argulosis.body` | Flat, round lice you can see on the skin. They hold on with suckers and hooks and can also swim off. Red bleeding spots and loose scales. | ಚರ್ಮದ ಮೇಲೆ ಕಣ್ಣಿಗೆ ಕಾಣುವ ಚಪ್ಪಟೆ, ದುಂಡಗಿನ ಹೇನುಗಳು. ಅವು ಹೀರುಬಟ್ಟಲು ಮತ್ತು ಕೊಕ್ಕೆಗಳಿಂದ ಹಿಡಿದುಕೊಳ್ಳುತ್ತವೆ ಮತ್ತು ಈಜಿ ಹೋಗಬಹುದು. ಕೆಂಪು ರಕ್ತಸ್ರಾವದ ಚುಕ್ಕೆಗಳು ಮತ್ತು ಸಡಿಲ ಹುರುಪೆಗಳು. |  |
| 38 | `diseases.DISEASES.argulosis.behaviour` | Fish become weak and thin and grow slowly. Some can die. | ಮೀನುಗಳು ದುರ್ಬಲ ಮತ್ತು ಸಣಕಲಾಗುತ್ತವೆ ಮತ್ತು ನಿಧಾನವಾಗಿ ಬೆಳೆಯುತ್ತವೆ. ಕೆಲವು ಸಾಯಬಹುದು. |  |
| 39 | `diseases.DISEASES.argulosis.when` | Common in carp ponds. In a West Bengal study, most cases were in September and October. | ಗೆಂಡೆ ಮೀನಿನ ಕೊಳಗಳಲ್ಲಿ ಸಾಮಾನ್ಯ. ಪಶ್ಚಿಮ ಬಂಗಾಳದ ಒಂದು ಅಧ್ಯಯನದಲ್ಲಿ, ಹೆಚ್ಚಿನ ಪ್ರಕರಣಗಳು ಸೆಪ್ಟೆಂಬರ್ ಮತ್ತು ಅಕ್ಟೋಬರ್‌ನಲ್ಲಿದ್ದವು. |  |
| 40 | `diseases.DISEASES.argulosis.prevention[0]` | Before stocking, dry the pond and remove wild fish. | ಮೀನು ಬಿಡುವ ಮೊದಲು, ಕೊಳವನ್ನು ಒಣಗಿಸಿ ಮತ್ತು ಕಾಡು ಮೀನುಗಳನ್ನು ತೆಗೆದುಹಾಕಿ. |  |
| 41 | `diseases.DISEASES.argulosis.prevention[1]` | Check a few fingerlings for lice before you stock them. | ಮರಿಗಳನ್ನು ಬಿಡುವ ಮೊದಲು ಕೆಲವು ಮರಿಗಳಲ್ಲಿ ಹೇನುಗಳಿವೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ. |  |
| 42 | `diseases.DISEASES.flukes.name` | Gill and skin flukes (Dactylogyrus, Gyrodactylus) | ಕಿವಿರು ಮತ್ತು ಚರ್ಮದ ಹುಳುಗಳು (ಡ್ಯಾಕ್ಟಿಲೋಗೈರಸ್, ಗೈರೊಡ್ಯಾಕ್ಟಿಲಸ್) |  |
| 43 | `diseases.DISEASES.flukes.body` | Too much slime, pale or swollen gills, faded body colour, falling scales. The worms are too small to see without a microscope. | ಅತಿಯಾದ ಲೋಳೆ, ಬಿಳಿಚಿದ ಅಥವಾ ಊದಿದ ಕಿವಿರುಗಳು, ಮಸುಕಾದ ದೇಹದ ಬಣ್ಣ, ಉದುರುವ ಹುರುಪೆಗಳು. ಹುಳುಗಳು ಸೂಕ್ಷ್ಮದರ್ಶಕವಿಲ್ಲದೆ ಕಾಣದಷ್ಟು ಸಣ್ಣವು. |  |
| 44 | `diseases.DISEASES.flukes.behaviour` | Hard breathing with the gill covers open. Fish swim slowly. | ಕಿವಿರು ಮುಚ್ಚಳ ತೆರೆದು ಕಷ್ಟದ ಉಸಿರಾಟ. ಮೀನುಗಳು ನಿಧಾನವಾಗಿ ಈಜುತ್ತವೆ. |  |
| 45 | `diseases.DISEASES.flukes.when` | Mostly in fry and small fish up to about 3 g. The worms do best at 20-25 °C. | ಹೆಚ್ಚಾಗಿ ಸುಮಾರು 3 ಗ್ರಾಂ ವರೆಗಿನ ಮರಿಗಳು ಮತ್ತು ಸಣ್ಣ ಮೀನುಗಳಲ್ಲಿ. ಹುಳುಗಳು 20-25 °C ನಲ್ಲಿ ಚೆನ್ನಾಗಿ ಬೆಳೆಯುತ್ತವೆ. |  |
| 46 | `diseases.DISEASES.flukes.prevention[0]` | Look at a sample of fry before stocking. Stock only healthy seed. | ಬಿಡುವ ಮೊದಲು ಕೆಲವು ಮರಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ. ಆರೋಗ್ಯಕರ ಮರಿಗಳನ್ನು ಮಾತ್ರ ಬಿಡಿ. |  |
| 47 | `diseases.DISEASES.flukes.prevention[1]` | Keep fry at a sensible density in good water. | ಮರಿಗಳನ್ನು ಉತ್ತಮ ನೀರಿನಲ್ಲಿ ಸೂಕ್ತ ಸಂಖ್ಯೆಯಲ್ಲಿ ಇಡಿ. |  |
| 48 | `diseases.DISEASES.white_spot.name` | White spot disease (Ich) | ಬಿಳಿ ಚುಕ್ಕೆ ರೋಗ (ಇಕ್) |  |
| 49 | `diseases.DISEASES.white_spot.body` | Many white spots the size of a pin head on the skin, fins and gills. In bad cases the skin looks covered by a white film. | ಚರ್ಮ, ಈಜುರೆಕ್ಕೆ ಮತ್ತು ಕಿವಿರುಗಳ ಮೇಲೆ ಗುಂಡುಸೂಜಿ ತಲೆಯ ಗಾತ್ರದ ಅನೇಕ ಬಿಳಿ ಚುಕ್ಕೆಗಳು. ತೀವ್ರವಾದಾಗ ಚರ್ಮ ಬಿಳಿ ಪದರದಿಂದ ಮುಚ್ಚಿದಂತೆ ಕಾಣುತ್ತದೆ. |  |
| 50 | `diseases.DISEASES.white_spot.behaviour` | Fish swim slowly near the surface, rub against things or jump. They breathe with difficulty and stop eating. Many can die. | ಮೀನುಗಳು ಮೇಲ್ಮೈ ಹತ್ತಿರ ನಿಧಾನವಾಗಿ ಈಜುತ್ತವೆ, ವಸ್ತುಗಳಿಗೆ ಉಜ್ಜಿಕೊಳ್ಳುತ್ತವೆ ಅಥವಾ ಜಿಗಿಯುತ್ತವೆ. ಕಷ್ಟದಿಂದ ಉಸಿರಾಡುತ್ತವೆ ಮತ್ತು ತಿನ್ನುವುದನ್ನು ನಿಲ್ಲಿಸುತ್ತವೆ. ಅನೇಕ ಸಾಯಬಹುದು. |  |
| 51 | `diseases.DISEASES.white_spot.when` | Cooler water, 15-25 °C. Mostly in nursery and rearing ponds and in crowded ponds. | ತಂಪಾದ ನೀರು, 15-25 °C. ಹೆಚ್ಚಾಗಿ ನರ್ಸರಿ ಮತ್ತು ಪಾಲನಾ ಕೊಳಗಳಲ್ಲಿ ಮತ್ತು ದಟ್ಟ ಕೊಳಗಳಲ್ಲಿ. |  |
| 52 | `diseases.DISEASES.white_spot.prevention[0]` | Keep new fingerlings apart and check them before stocking. | ಹೊಸ ಮರಿಗಳನ್ನು ಪ್ರತ್ಯೇಕವಾಗಿಟ್ಟು ಬಿಡುವ ಮೊದಲು ಪರಿಶೀಲಿಸಿ. |  |
| 53 | `diseases.DISEASES.white_spot.prevention[1]` | Rear fry at a sensible density. | ಮರಿಗಳನ್ನು ಸೂಕ್ತ ಸಂಖ್ಯೆಯಲ್ಲಿ ಬೆಳೆಸಿ. |  |
| 54 | `diseases.DISEASES.anchor_worm.name` | Anchor worm (Lernaea) | ಲಂಗರು ಹುಳು (ಲರ್ನಿಯಾ) |  |
| 55 | `diseases.DISEASES.anchor_worm.body` | Thin, rod-like parasites stuck into the skin, anywhere on the body. Only the back end hangs out. The skin around is red, swollen and can rot; cotton-wool mould often grows there. | ದೇಹದ ಯಾವುದೇ ಭಾಗದಲ್ಲಿ ಚರ್ಮದೊಳಗೆ ಸಿಕ್ಕಿಕೊಂಡ ತೆಳುವಾದ ಕಡ್ಡಿಯಂತಹ ಪರಾವಲಂಬಿಗಳು. ಹಿಂಭಾಗ ಮಾತ್ರ ಹೊರಗೆ ನೇತಾಡುತ್ತದೆ. ಸುತ್ತಲಿನ ಚರ್ಮ ಕೆಂಪಾಗಿ, ಊದಿಕೊಂಡು ಕೊಳೆಯಬಹುದು; ಅಲ್ಲಿ ಹೆಚ್ಚಾಗಿ ಹತ್ತಿ ಬೂಷ್ಟು ಬೆಳೆಯುತ್ತದೆ. |  |
| 56 | `diseases.DISEASES.anchor_worm.behaviour` | Fish are restless, eat less, get thin and move slowly. One or two worms can stunt a small fish. | ಮೀನುಗಳು ಚಡಪಡಿಸುತ್ತವೆ, ಕಡಿಮೆ ತಿನ್ನುತ್ತವೆ, ಸಣಕಲಾಗುತ್ತವೆ ಮತ್ತು ನಿಧಾನವಾಗಿ ಚಲಿಸುತ್ತವೆ. ಒಂದೆರಡು ಹುಳುಗಳು ಸಣ್ಣ ಮೀನಿನ ಬೆಳವಣಿಗೆ ಕುಂಠಿತಗೊಳಿಸಬಹುದು. |  |
| 57 | `diseases.DISEASES.anchor_worm.when` | A long season in warm water (15-33 °C). Often in nursery and rearing ponds. | ಬೆಚ್ಚಗಿನ ನೀರಿನಲ್ಲಿ (15-33 °C) ದೀರ್ಘ ಕಾಲ. ಹೆಚ್ಚಾಗಿ ನರ್ಸರಿ ಮತ್ತು ಪಾಲನಾ ಕೊಳಗಳಲ್ಲಿ. |  |
| 58 | `diseases.DISEASES.anchor_worm.prevention[0]` | Check fingerlings for worms before stocking. | ಮರಿಗಳನ್ನು ಬಿಡುವ ಮೊದಲು ಹುಳುಗಳಿವೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ. |  |
| 59 | `diseases.DISEASES.anchor_worm.prevention[1]` | Before stocking, dry the pond and remove wild fish. | ಮೀನು ಬಿಡುವ ಮೊದಲು, ಕೊಳವನ್ನು ಒಣಗಿಸಿ ಮತ್ತು ಕಾಡು ಮೀನುಗಳನ್ನು ತೆಗೆದುಹಾಕಿ. |  |

## 28. Messages from the server: Fish disease guide: symptom checker and notes

The signs a farmer can tick, cause types, the steps for any disease, and the notes shown with every result.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `diseases.SIGNS.red_sores` | Red spots or open sores (ulcers) on the body | ದೇಹದ ಮೇಲೆ ಕೆಂಪು ಚುಕ್ಕೆಗಳು ಅಥವಾ ತೆರೆದ ಹುಣ್ಣುಗಳು |  |
| 2 | `diseases.SIGNS.red_patches` | Red, bleeding patches on the skin or fins | ಚರ್ಮ ಅಥವಾ ಈಜುರೆಕ್ಕೆಗಳ ಮೇಲೆ ಕೆಂಪು, ರಕ್ತಸ್ರಾವದ ಕಲೆಗಳು |  |
| 3 | `diseases.SIGNS.swollen_belly` | Swollen belly | ಊದಿಕೊಂಡ ಹೊಟ್ಟೆ |  |
| 4 | `diseases.SIGNS.raised_scales` | Scales standing out, like a pine cone | ಪೈನ್ ಕಾಯಿಯಂತೆ ಎದ್ದು ನಿಂತ ಹುರುಪೆಗಳು |  |
| 5 | `diseases.SIGNS.pop_eye` | Bulging eyes | ಉಬ್ಬಿದ ಕಣ್ಣುಗಳು |  |
| 6 | `diseases.SIGNS.white_spots` | Many tiny white spots, like pin heads, on skin, fins or gills | ಚರ್ಮ, ಈಜುರೆಕ್ಕೆ ಅಥವಾ ಕಿವಿರುಗಳ ಮೇಲೆ ಗುಂಡುಸೂಜಿ ತಲೆಯಂತಹ ಅನೇಕ ಸಣ್ಣ ಬಿಳಿ ಚುಕ್ಕೆಗಳು |  |
| 7 | `diseases.SIGNS.cotton` | White, grey or brownish cotton-wool growth on the body | ದೇಹದ ಮೇಲೆ ಬಿಳಿ, ಬೂದು ಅಥವಾ ಕಂದು ಹತ್ತಿಯಂತಹ ಬೆಳವಣಿಗೆ |  |
| 8 | `diseases.SIGNS.fin_rot` | Fins rotting from the edges, or white-yellow patches on the skin | ಅಂಚಿನಿಂದ ಕೊಳೆಯುತ್ತಿರುವ ಈಜುರೆಕ್ಕೆಗಳು, ಅಥವಾ ಚರ್ಮದ ಮೇಲೆ ಬಿಳಿ-ಹಳದಿ ಕಲೆಗಳು |  |
| 9 | `diseases.SIGNS.gill_rot` | Gills look rotten, covered with mud and slime | ಕಿವಿರುಗಳು ಕೊಳೆತಂತೆ, ಕೆಸರು ಮತ್ತು ಲೋಳೆಯಿಂದ ಮುಚ್ಚಿದಂತೆ ಕಾಣುತ್ತವೆ |  |
| 10 | `diseases.SIGNS.pale_gills` | Pale gills | ಬಿಳಿಚಿದ ಕಿವಿರುಗಳು |  |
| 11 | `diseases.SIGNS.lice` | Small, flat, round lice you can see on the skin | ಚರ್ಮದ ಮೇಲೆ ಕಣ್ಣಿಗೆ ಕಾಣುವ ಸಣ್ಣ, ಚಪ್ಪಟೆ, ದುಂಡಗಿನ ಹೇನುಗಳು |  |
| 12 | `diseases.SIGNS.threads` | Thin threads hanging from the skin, with a swollen red spot around each | ಚರ್ಮದಿಂದ ನೇತಾಡುವ ತೆಳುವಾದ ದಾರಗಳು, ಪ್ರತಿಯೊಂದರ ಸುತ್ತ ಊದಿದ ಕೆಂಪು ಜಾಗ |  |
| 13 | `diseases.SIGNS.loose_scales` | Loose or falling scales | ಸಡಿಲವಾದ ಅಥವಾ ಉದುರುವ ಹುರುಪೆಗಳು |  |
| 14 | `diseases.SIGNS.much_mucus` | Too much slime on the body or gills | ದೇಹ ಅಥವಾ ಕಿವಿರುಗಳ ಮೇಲೆ ಅತಿಯಾದ ಲೋಳೆ |  |
| 15 | `diseases.SIGNS.colour_change` | Body colour has changed (darker or faded) | ದೇಹದ ಬಣ್ಣ ಬದಲಾಗಿದೆ (ಕಪ್ಪಾಗಿದೆ ಅಥವಾ ಮಸುಕಾಗಿದೆ) |  |
| 16 | `diseases.SIGNS.thin_weak` | Thin, weak fish that grow slowly | ಸಣಕಲು, ದುರ್ಬಲ, ನಿಧಾನವಾಗಿ ಬೆಳೆಯುವ ಮೀನುಗಳು |  |
| 17 | `diseases.SIGNS.gasping` | Gasping at the surface | ನೀರಿನ ಮೇಲ್ಮೈಯಲ್ಲಿ ಉಸಿರಿಗಾಗಿ ಏದುಸಿರು |  |
| 18 | `diseases.SIGNS.fast_breathing` | Hard, fast breathing with gill covers held open | ಕಿವಿರು ಮುಚ್ಚಳ ತೆರೆದಿಟ್ಟು ಕಷ್ಟದ, ವೇಗದ ಉಸಿರಾಟ |  |
| 19 | `diseases.SIGNS.rubbing` | Rubbing against the bottom or sides, or jumping | ತಳ ಅಥವಾ ಬದಿಗಳಿಗೆ ಉಜ್ಜಿಕೊಳ್ಳುವುದು, ಅಥವಾ ನೀರಿನಿಂದ ಜಿಗಿಯುವುದು |  |
| 20 | `diseases.SIGNS.slow_surface` | Swimming slowly, alone or near the surface | ನಿಧಾನವಾಗಿ, ಒಂಟಿಯಾಗಿ ಅಥವಾ ಮೇಲ್ಮೈ ಹತ್ತಿರ ಈಜುವುದು |  |
| 21 | `diseases.SIGNS.not_eating` | Not eating | ಆಹಾರ ತಿನ್ನುತ್ತಿಲ್ಲ |  |
| 22 | `diseases.CAUSE_TYPES.water_mould` | Water mould (fungus-like) | ನೀರಿನ ಬೂಷ್ಟು (ಶಿಲೀಂಧ್ರದಂತಹದು) |  |
| 23 | `diseases.CAUSE_TYPES.bacteria` | Bacteria | ಬ್ಯಾಕ್ಟೀರಿಯಾ |  |
| 24 | `diseases.CAUSE_TYPES.protozoan` | Parasite: tiny single-celled animal | ಪರಾವಲಂಬಿ: ಏಕಕೋಶದ ಸೂಕ್ಷ್ಮ ಜೀವಿ |  |
| 25 | `diseases.CAUSE_TYPES.worm` | Parasite: tiny worm (fluke) | ಪರಾವಲಂಬಿ: ಸಣ್ಣ ಹುಳು (ಫ್ಲೂಕ್) |  |
| 26 | `diseases.CAUSE_TYPES.crustacean` | Parasite: crustacean (relative of shrimps) | ಪರಾವಲಂಬಿ: ಕಠಿಣಚರ್ಮಿ (ಸೀಗಡಿಯ ಸಂಬಂಧಿ) |  |
| 27 | `diseases.COMMON_STEPS[0]` | Take out dead and dying fish every day. Dead fish spread disease. | ಸತ್ತ ಮತ್ತು ಸಾಯುತ್ತಿರುವ ಮೀನುಗಳನ್ನು ಪ್ರತಿದಿನ ಹೊರತೆಗೆಯಿರಿ. ಸತ್ತ ಮೀನುಗಳು ರೋಗ ಹರಡುತ್ತವೆ. |  |
| 28 | `diseases.COMMON_STEPS[1]` | Do not move fish, water or nets from this pond to another pond. | ಈ ಕೊಳದಿಂದ ಬೇರೆ ಕೊಳಕ್ಕೆ ಮೀನು, ನೀರು ಅಥವಾ ಬಲೆಗಳನ್ನು ಸಾಗಿಸಬೇಡಿ. |  |
| 29 | `diseases.COMMON_STEPS[2]` | Give less feed and keep the water quality good. | ಕಡಿಮೆ ಆಹಾರ ನೀಡಿ ಮತ್ತು ನೀರಿನ ಗುಣಮಟ್ಟವನ್ನು ಚೆನ್ನಾಗಿಡಿ. |  |
| 30 | `diseases.COMMON_STEPS[3]` | Call your fisheries officer or KVK today. Take a few sick fish, alive or just dead and kept wet. | ಇಂದೇ ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿ ಅಥವಾ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರಕ್ಕೆ (KVK) ಕರೆ ಮಾಡಿ. ಕೆಲವು ರೋಗಪೀಡಿತ ಮೀನುಗಳನ್ನು, ಜೀವಂತವಾಗಿ ಅಥವಾ ಈಗ ತಾನೇ ಸತ್ತು ಒದ್ದೆಯಾಗಿಟ್ಟು, ತೆಗೆದುಕೊಂಡು ಹೋಗಿ. |  |
| 31 | `diseases.TREATMENT_NOTE` | No medicines or chemicals here. Any treatment must be prescribed by a fisheries officer or KVK. | ಇಲ್ಲಿ ಯಾವುದೇ ಔಷಧಿ ಅಥವಾ ರಾಸಾಯನಿಕಗಳಿಲ್ಲ. ಯಾವುದೇ ಚಿಕಿತ್ಸೆಯನ್ನು ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿ ಅಥವಾ KVK ಸೂಚಿಸಬೇಕು. |  |
| 32 | `diseases.NOT_A_DIAGNOSIS` | These are possible matches, not a diagnosis. Many fish diseases look alike. Confirm with your fisheries officer. | ಇವು ಸಾಧ್ಯವಿರುವ ಹೊಂದಾಣಿಕೆಗಳು, ರೋಗನಿರ್ಣಯವಲ್ಲ. ಅನೇಕ ಮೀನು ರೋಗಗಳು ಒಂದೇ ರೀತಿ ಕಾಣುತ್ತವೆ. ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯೊಂದಿಗೆ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ. |  |
| 33 | `diseases.NO_MATCH` | No disease in this guide matches these signs. Confirm with your fisheries officer. | ಈ ಲಕ್ಷಣಗಳಿಗೆ ಈ ಮಾರ್ಗದರ್ಶಿಯ ಯಾವುದೇ ರೋಗ ಹೊಂದುವುದಿಲ್ಲ. ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯೊಂದಿಗೆ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ. |  |
| 34 | `diseases.GASPING_NOTE` | Gasping at the surface is most often low oxygen, not disease. Check oxygen and run the aerator first. | ಮೇಲ್ಮೈಯಲ್ಲಿ ಏದುಸಿರು ಹೆಚ್ಚಾಗಿ ಕಡಿಮೆ ಆಮ್ಲಜನಕದಿಂದ, ರೋಗದಿಂದಲ್ಲ. ಮೊದಲು ಆಮ್ಲಜನಕ ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ. |  |
| 35 | `diseases.LIKELY_NOTE` | This does not mean your fish are sick. Watch them closely and use the Fish disease guide if you see signs. | ಇದರ ಅರ್ಥ ನಿಮ್ಮ ಮೀನುಗಳಿಗೆ ರೋಗ ಬಂದಿದೆ ಎಂದಲ್ಲ. ಅವುಗಳನ್ನು ಗಮನವಿಟ್ಟು ನೋಡಿ, ಲಕ್ಷಣಗಳು ಕಂಡರೆ ಮೀನು ರೋಗ ಮಾರ್ಗದರ್ಶಿ ಬಳಸಿ. |  |

## 29. Messages from the server: Fish disease guide: risky readings

Why a reading makes a disease more likely.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `diseases.READING_LINKS.dissolved_oxygen/low[0][1]` | Low oxygen stresses fish and is linked to Aeromonas outbreaks. | ಕಡಿಮೆ ಆಮ್ಲಜನಕ ಮೀನುಗಳಿಗೆ ಒತ್ತಡ ತರುತ್ತದೆ ಮತ್ತು ಏರೋಮೋನಾಸ್ ರೋಗಕ್ಕೆ ಸಂಬಂಧಿಸಿದೆ. |  |
| 2 | `diseases.READING_LINKS.ammonia/high[0][1]` | High ammonia makes fish more likely to catch Aeromonas. | ಹೆಚ್ಚಿನ ಅಮೋನಿಯಾ ಮೀನುಗಳಿಗೆ ಏರೋಮೋನಾಸ್ ಸೋಂಕು ತಗಲುವ ಸಾಧ್ಯತೆ ಹೆಚ್ಚಿಸುತ್ತದೆ. |  |
| 3 | `diseases.READING_LINKS.temperature/high[0][1]` | Columnaris spreads more easily in warmer water. | ಬೆಚ್ಚಗಿನ ನೀರಿನಲ್ಲಿ ಕಾಲಮ್ನಾರಿಸ್ ಸುಲಭವಾಗಿ ಹರಡುತ್ತದೆ. |  |
| 4 | `diseases.READING_LINKS.temperature/high[1][1]` | Gill rot is worst at 28-35 °C. | ಕಿವಿರು ಕೊಳೆ 28-35 °C ನಲ್ಲಿ ಹೆಚ್ಚು. |  |
| 5 | `diseases.READING_LINKS.temperature/high[2][1]` | High water temperature stresses fish and is linked to Aeromonas outbreaks. | ಹೆಚ್ಚಿನ ನೀರಿನ ತಾಪಮಾನ ಮೀನುಗಳಿಗೆ ಒತ್ತಡ ತರುತ್ತದೆ ಮತ್ತು ಏರೋಮೋನಾಸ್ ರೋಗಕ್ಕೆ ಸಂಬಂಧಿಸಿದೆ. |  |
| 6 | `diseases.READING_LINKS.temperature/low[0][1]` | EUS outbreaks happen at low water temperatures. | ಕಡಿಮೆ ನೀರಿನ ತಾಪಮಾನದಲ್ಲಿ EUS ಹರಡುತ್ತದೆ. |  |
| 7 | `diseases.READING_LINKS.temperature/low[1][1]` | The white spot parasite multiplies best at 15-25 °C. | ಬಿಳಿ ಚುಕ್ಕೆ ಪರಾವಲಂಬಿ 15-25 °C ನಲ್ಲಿ ಹೆಚ್ಚು ವೃದ್ಧಿಯಾಗುತ್ತದೆ. |  |
| 8 | `diseases.READING_LINKS.ph/low[0][1]` | EUS outbreaks are linked to acidic water. | EUS ಹರಡುವಿಕೆ ಆಮ್ಲೀಯ ನೀರಿಗೆ ಸಂಬಂಧಿಸಿದೆ. |  |

## 30. Messages from the server: Ask AquaNexus assistant

Labels, safety replies and the suggested questions. Ready answers are built from the texts in the other sections. AI replies in Kannada are written by the AI and are not in this sheet.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `assistant.LABEL` | AI assistant: can make mistakes | AI ಸಹಾಯಕ: ತಪ್ಪುಗಳಾಗಬಹುದು |  |
| 2 | `assistant.I_DONT_KNOW` | I can't answer that from the app's information. For that, please ask your fisheries officer or KVK. | ಆ್ಯಪ್‌ನ ಮಾಹಿತಿಯಿಂದ ನಾನು ಅದಕ್ಕೆ ಉತ್ತರಿಸಲು ಆಗುವುದಿಲ್ಲ. ಅದಕ್ಕಾಗಿ ದಯವಿಟ್ಟು ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿ ಅಥವಾ KVK ಅನ್ನು ಕೇಳಿ. |  |
| 3 | `assistant.CAN_HELP` | I can help with: your pond readings and what to do now, safe levels, tonight's oxygen risk, pond care (cleaning, changing water, feeding, aerators, daily checks, how many fish), fish diseases and the Shop. Try one of these questions: | ನಾನು ಇವುಗಳಲ್ಲಿ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ: ನಿಮ್ಮ ಕೊಳದ ಅಳತೆಗಳು ಮತ್ತು ಈಗ ಏನು ಮಾಡಬೇಕು, ಸುರಕ್ಷಿತ ಮಟ್ಟಗಳು, ಇಂದು ರಾತ್ರಿಯ ಆಮ್ಲಜನಕ ಅಪಾಯ, ಕೊಳದ ಆರೈಕೆ (ಸ್ವಚ್ಛಗೊಳಿಸುವುದು, ನೀರು ಬದಲಾಯಿಸುವುದು, ಆಹಾರ, ಏರೇಟರ್, ದಿನನಿತ್ಯ ಪರಿಶೀಲನೆ, ಎಷ್ಟು ಮೀನು), ಮೀನು ರೋಗಗಳು ಮತ್ತು ಅಂಗಡಿ. ಈ ಪ್ರಶ್ನೆಗಳಲ್ಲಿ ಒಂದನ್ನು ಪ್ರಯತ್ನಿಸಿ: |  |
| 4 | `assistant.CONFIRM` | Please confirm with your fisheries officer / KVK. | ದಯವಿಟ್ಟು ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿ / KVK ಜೊತೆ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ. |  |
| 5 | `assistant.NO_TREATMENT` | I can't suggest medicines, chemicals or amounts to add, and I can't say which disease your fish have. The Fish disease guide shows possible matches for the signs you see. | ನಾನು ಔಷಧಿ, ರಾಸಾಯನಿಕ ಅಥವಾ ಪ್ರಮಾಣಗಳನ್ನು ಸೂಚಿಸಲು ಆಗುವುದಿಲ್ಲ, ಮತ್ತು ನಿಮ್ಮ ಮೀನುಗಳಿಗೆ ಯಾವ ರೋಗ ಎಂದು ಹೇಳಲು ಆಗುವುದಿಲ್ಲ. ನೀವು ನೋಡುವ ಲಕ್ಷಣಗಳಿಗೆ ಸಾಧ್ಯವಿರುವ ಹೊಂದಾಣಿಕೆಗಳನ್ನು ಮೀನು ರೋಗ ಮಾರ್ಗದರ್ಶಿ ತೋರಿಸುತ್ತದೆ. |  |
| 6 | `assistant.FALLBACK_NOTE` | The AI assistant is not available right now. Tap a question below for a ready answer from the app. | AI ಸಹಾಯಕ ಈಗ ಲಭ್ಯವಿಲ್ಲ. ಆ್ಯಪ್‌ನ ಸಿದ್ಧ ಉತ್ತರಕ್ಕಾಗಿ ಕೆಳಗಿನ ಪ್ರಶ್ನೆಯೊಂದನ್ನು ಒತ್ತಿ. |  |
| 7 | `assistant.LIMITED_NOTE` | Too many questions for now. Please wait a minute, or tap a question below for a ready answer. | ಸದ್ಯಕ್ಕೆ ತುಂಬಾ ಪ್ರಶ್ನೆಗಳು. ದಯವಿಟ್ಟು ಒಂದು ನಿಮಿಷ ಕಾಯಿರಿ, ಅಥವಾ ಸಿದ್ಧ ಉತ್ತರಕ್ಕಾಗಿ ಕೆಳಗಿನ ಪ್ರಶ್ನೆಯೊಂದನ್ನು ಒತ್ತಿ. |  |
| 8 | `assistant.SIMULATED_NOTE` | These are simulated readings from the demo pond, not a real pond. | ಇವು ಡೆಮೊ ಕೊಳದ ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಅಳತೆಗಳು, ನಿಜವಾದ ಕೊಳದ್ದಲ್ಲ. |  |
| 9 | `assistant.QUESTIONS.pond_now` | Is my pond safe right now? | ನನ್ನ ಕೊಳ ಈಗ ಸುರಕ್ಷಿತವಾಗಿದೆಯೇ? |  |
| 10 | `assistant.QUESTIONS.what_to_do` | What should I do now? | ನಾನು ಈಗ ಏನು ಮಾಡಬೇಕು? |  |
| 11 | `assistant.QUESTIONS.tonight` | Is there a risk of an oxygen crash tonight? | ಇಂದು ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯವಿದೆಯೇ? |  |
| 12 | `assistant.QUESTIONS.pond_clean` | When should I clean my pond? | ನನ್ನ ಕೊಳವನ್ನು ಯಾವಾಗ ಸ್ವಚ್ಛಗೊಳಿಸಬೇಕು? |  |
| 13 | `assistant.QUESTIONS.safe_levels` | What are the safe levels for oxygen, pH, temperature and ammonia? | ಆಮ್ಲಜನಕ, pH, ತಾಪಮಾನ ಮತ್ತು ಅಮೋನಿಯಾದ ಸುರಕ್ಷಿತ ಮಟ್ಟಗಳು ಯಾವುವು? |  |
| 14 | `assistant.QUESTIONS.likely_now` | Which diseases are more likely with my readings? | ನನ್ನ ಅಳತೆಗಳಿಂದ ಯಾವ ರೋಗಗಳ ಸಾಧ್ಯತೆ ಹೆಚ್ಚು? |  |
| 15 | `assistant.QUESTIONS.sick_fish` | My fish look sick. What should I do? | ನನ್ನ ಮೀನುಗಳು ರೋಗಪೀಡಿತವಾಗಿ ಕಾಣುತ್ತಿವೆ. ನಾನು ಏನು ಮಾಡಬೇಕು? |  |
| 16 | `assistant.QUESTIONS.prevent` | How can I prevent fish diseases? | ಮೀನು ರೋಗಗಳನ್ನು ಹೇಗೆ ತಡೆಯಬಹುದು? |  |
| 17 | `assistant.QUESTIONS.shop_which` | Which sensor or kit should I buy? | ನಾನು ಯಾವ ಸೆನ್ಸರ್ ಅಥವಾ ಕಿಟ್ ಖರೀದಿಸಬೇಕು? |  |
| 18 | `assistant.QUESTIONS.shop_test_kit` | How do I use the test kit? | ಟೆಸ್ಟ್ ಕಿಟ್ ಅನ್ನು ಹೇಗೆ ಬಳಸುವುದು? |  |
| 19 | `assistant.NO_READINGS` | There are no readings yet. Press Start, enter test-kit readings, or connect a sensor. | ಇನ್ನೂ ಯಾವುದೇ ಅಳತೆಗಳಿಲ್ಲ. ಪ್ರಾರಂಭಿಸಿ ಒತ್ತಿ, ಟೆಸ್ಟ್ ಕಿಟ್ ಅಳತೆಗಳನ್ನು ನಮೂದಿಸಿ, ಅಥವಾ ಸೆನ್ಸರ್ ಸಂಪರ್ಕಿಸಿ. |  |
| 20 | `assistant.ALL_SAFE_ACTION` | All readings are in the safe range. No action is needed now. | ಎಲ್ಲಾ ಅಳತೆಗಳು ಸುರಕ್ಷಿತ ಮಟ್ಟದಲ್ಲಿವೆ. ಈಗ ಯಾವುದೇ ಕ್ರಮದ ಅಗತ್ಯವಿಲ್ಲ. |  |
| 21 | `assistant.NO_LIKELY` | None of your readings makes a disease in the guide more likely right now. | ನಿಮ್ಮ ಯಾವುದೇ ಅಳತೆ ಈಗ ಮಾರ್ಗದರ್ಶಿಯ ಯಾವುದೇ ರೋಗದ ಸಾಧ್ಯತೆಯನ್ನು ಹೆಚ್ಚಿಸುವುದಿಲ್ಲ. |  |
| 22 | `assistant.USE_CHECKER` | Use the symptom checker in the Fish disease guide to see possible matches. | ಸಾಧ್ಯವಿರುವ ಹೊಂದಾಣಿಕೆಗಳನ್ನು ನೋಡಲು ಮೀನು ರೋಗ ಮಾರ್ಗದರ್ಶಿಯ ಲಕ್ಷಣ ಪರಿಶೀಲಕ ಬಳಸಿ. |  |
| 23 | `assistant.LEVELS_INTRO` | Safe, Warning and Danger levels used by the app: | ಆ್ಯಪ್ ಬಳಸುವ ಸುರಕ್ಷಿತ, ಎಚ್ಚರಿಕೆ ಮತ್ತು ಅಪಾಯ ಮಟ್ಟಗಳು: |  |
| 24 | `assistant.AMMONIA_NOTE` | (the toxic part, NH3, worked out from total ammonia, pH and temperature) | (ವಿಷಕಾರಿ ಭಾಗ NH3, ಒಟ್ಟು ಅಮೋನಿಯಾ, pH ಮತ್ತು ತಾಪಮಾನದಿಂದ ಲೆಕ್ಕ ಹಾಕಲಾಗುತ್ತದೆ) |  |
| 25 | `assistant.BAND.from_to_below` | {a} to below {b} | {a} ರಿಂದ {b} ಕ್ಕಿಂತ ಕಡಿಮೆ |  |
| 26 | `assistant.BAND.below` | below {a} | {a} ಕ್ಕಿಂತ ಕಡಿಮೆ |  |
| 27 | `assistant.BAND.above` | above {a} | {a} ಕ್ಕಿಂತ ಹೆಚ್ಚು |  |
| 28 | `assistant.BAND.or_more` | {a} or more | {a} ಅಥವಾ ಹೆಚ್ಚು |  |
| 29 | `assistant.BAND.up_to` | up to {b} | {b} ವರೆಗೆ |  |
| 30 | `assistant.BAND.to_below` | to below {b} | ರಿಂದ {b} ಕ್ಕಿಂತ ಕಡಿಮೆ |  |
| 31 | `assistant.BAND.or` | or | ಅಥವಾ |  |
| 32 | `assistant.BAND.line` | {name}: Safe {safe}. Warning {warning}. Danger {danger}. | {name}: ಸುರಕ್ಷಿತ {safe}. ಎಚ್ಚರಿಕೆ {warning}. ಅಪಾಯ {danger}. |  |
| 33 | `assistant.BAND.no_danger` | {name}: Safe {safe}. Otherwise Warning (no Danger level). | {name}: ಸುರಕ್ಷಿತ {safe}. ಇಲ್ಲದಿದ್ದರೆ ಎಚ್ಚರಿಕೆ (ಅಪಾಯ ಮಟ್ಟ ಇಲ್ಲ). |  |
| 34 | `assistant._answer (tonight)` | Oxygen crash risk tonight: {level}. | ಇಂದು ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯ: {level}. |  |

## 31. Messages from the server: Ask AquaNexus: pond care basics

Ready answers to pond care questions (backend/pond_care.py). Each answer is its sentences joined together, ending with the fisheries officer note.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `pond_care.OFFICER_NOTE` | For liming, chemicals, medicines or amounts of anything, ask your fisheries officer or KVK. | ಸುಣ್ಣ ಹಾಕುವುದು, ರಾಸಾಯನಿಕಗಳು, ಔಷಧಿಗಳು ಅಥವಾ ಯಾವುದರ ಪ್ರಮಾಣಕ್ಕಾಗಿ ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿ ಅಥವಾ KVK ಅನ್ನು ಕೇಳಿ. |  |
| 2 | `pond_care.TOPICS.water_change.title` | Changing water | ನೀರು ಬದಲಾಯಿಸುವುದು |  |
| 3 | `pond_care.TOPICS.water_change.text[0]` | Change part of the water, not all of it, when the water smells bad, is very green, or oxygen is low (fish gasp at the surface at dawn). | ನೀರು ಕೆಟ್ಟ ವಾಸನೆ ಬಂದಾಗ, ತುಂಬಾ ಹಸಿರಾಗಿದ್ದಾಗ, ಅಥವಾ ಆಮ್ಲಜನಕ ಕಡಿಮೆ ಇದ್ದಾಗ (ಬೆಳಗಿನ ಜಾವ ಮೀನುಗಳು ಮೇಲ್ಮೈಯಲ್ಲಿ ಉಸಿರಿಗಾಗಿ ಒದ್ದಾಡಿದಾಗ) ನೀರಿನ ಒಂದು ಭಾಗವನ್ನು ಬದಲಾಯಿಸಿ, ಎಲ್ಲವನ್ನೂ ಅಲ್ಲ. |  |
| 4 | `pond_care.TOPICS.water_change.text[1]` | Let some water out and fill in clean water. | ಸ್ವಲ್ಪ ನೀರನ್ನು ಹೊರಬಿಟ್ಟು ಶುದ್ಧ ನೀರನ್ನು ತುಂಬಿಸಿ. |  |
| 5 | `pond_care.TOPICS.water_change.text[2]` | Don't empty the pond while the fish are in it. | ಮೀನುಗಳು ಒಳಗಿರುವಾಗ ಕೊಳವನ್ನು ಖಾಲಿ ಮಾಡಬೇಡಿ. |  |
| 6 | `pond_care.TOPICS.cleaning.title` | Cleaning the pond or tank | ಕೊಳ ಅಥವಾ ಟ್ಯಾಂಕ್ ಸ್ವಚ್ಛಗೊಳಿಸುವುದು |  |
| 7 | `pond_care.TOPICS.cleaning.text[0]` | While fish are growing, don't fully drain or scrub the pond. | ಮೀನುಗಳು ಬೆಳೆಯುತ್ತಿರುವಾಗ ಕೊಳವನ್ನು ಪೂರ್ತಿ ಖಾಲಿ ಮಾಡಬೇಡಿ ಅಥವಾ ಉಜ್ಜಬೇಡಿ. |  |
| 8 | `pond_care.TOPICS.cleaning.text[1]` | Every day, take out leftover feed and dead fish. | ಪ್ರತಿದಿನ ಉಳಿದ ಆಹಾರ ಮತ್ತು ಸತ್ತ ಮೀನುಗಳನ್ನು ಹೊರತೆಗೆಯಿರಿ. |  |
| 9 | `pond_care.TOPICS.cleaning.text[2]` | Between crops, after the harvest: drain the pond, remove the black sludge from the bottom, let the bottom dry in the sun until it cracks, then fill it again. | ಎರಡು ಬೆಳೆಗಳ ನಡುವೆ, ಕೊಯ್ಲಿನ ನಂತರ: ಕೊಳದ ನೀರನ್ನು ಖಾಲಿ ಮಾಡಿ, ತಳದ ಕಪ್ಪು ಕೆಸರನ್ನು ತೆಗೆಯಿರಿ, ತಳ ಬಿರುಕು ಬಿಡುವವರೆಗೆ ಬಿಸಿಲಿನಲ್ಲಿ ಒಣಗಿಸಿ, ನಂತರ ಮತ್ತೆ ನೀರು ತುಂಬಿಸಿ. |  |
| 10 | `pond_care.TOPICS.cleaning.tank` | In a tank: change part of the water and clean the bottom while the fish stay in. | ಟ್ಯಾಂಕ್‌ನಲ್ಲಿ: ಮೀನುಗಳು ಒಳಗೇ ಇರುವಾಗ ನೀರಿನ ಒಂದು ಭಾಗವನ್ನು ಬದಲಾಯಿಸಿ ಮತ್ತು ತಳವನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿ. |  |
| 11 | `pond_care.TOPICS.feeding.title` | Feeding | ಆಹಾರ ನೀಡುವುದು |  |
| 12 | `pond_care.TOPICS.feeding.text[0]` | Feed at the same set times every day. | ಪ್ರತಿದಿನ ಅದೇ ನಿಗದಿತ ಸಮಯಗಳಲ್ಲಿ ಆಹಾರ ನೀಡಿ. |  |
| 13 | `pond_care.TOPICS.feeding.text[1]` | Give less feed on cloudy or very hot days. | ಮೋಡ ಕವಿದ ಅಥವಾ ತುಂಬಾ ಬಿಸಿಯಾದ ದಿನಗಳಲ್ಲಿ ಕಡಿಮೆ ಆಹಾರ ನೀಡಿ. |  |
| 14 | `pond_care.TOPICS.feeding.text[2]` | Stop feeding if the fish don't eat or the oxygen is low. | ಮೀನುಗಳು ತಿನ್ನದಿದ್ದರೆ ಅಥವಾ ಆಮ್ಲಜನಕ ಕಡಿಮೆ ಇದ್ದರೆ ಆಹಾರ ನೀಡುವುದನ್ನು ನಿಲ್ಲಿಸಿ. |  |
| 15 | `pond_care.TOPICS.feeding.text[3]` | If feed is left over, give less next time and take the leftover out. | ಆಹಾರ ಉಳಿದರೆ, ಮುಂದಿನ ಬಾರಿ ಕಡಿಮೆ ನೀಡಿ ಮತ್ತು ಉಳಿದದ್ದನ್ನು ಹೊರತೆಗೆಯಿರಿ. |  |
| 16 | `pond_care.TOPICS.feeding.text[4]` | For how much feed suits your fish, ask your fisheries officer or KVK. | ನಿಮ್ಮ ಮೀನುಗಳಿಗೆ ಎಷ್ಟು ಆಹಾರ ಸರಿ ಎಂದು ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿ ಅಥವಾ KVK ಅನ್ನು ಕೇಳಿ. |  |
| 17 | `pond_care.TOPICS.aeration.title` | Aerators | ಏರೇಟರ್ |  |
| 18 | `pond_care.TOPICS.aeration.text[0]` | Run the aerator at night and before dawn, when oxygen is lowest. | ಆಮ್ಲಜನಕ ಅತಿ ಕಡಿಮೆ ಇರುವ ರಾತ್ರಿ ಮತ್ತು ಬೆಳಗಿನ ಜಾವಕ್ಕೆ ಮೊದಲು ಏರೇಟರ್ ಚಾಲನೆ ಮಾಡಿ. |  |
| 19 | `pond_care.TOPICS.aeration.text[1]` | It matters most after a cloudy, warm, still day. | ಮೋಡ ಕವಿದ, ಬಿಸಿಯಾದ, ಗಾಳಿಯಿಲ್ಲದ ದಿನದ ನಂತರ ಇದು ಅತ್ಯಂತ ಮುಖ್ಯ. |  |
| 20 | `pond_care.TOPICS.aeration.text[2]` | If fish gasp at the surface, run it at once. | ಮೀನುಗಳು ಮೇಲ್ಮೈಯಲ್ಲಿ ಉಸಿರಿಗಾಗಿ ಒದ್ದಾಡಿದರೆ, ತಕ್ಷಣ ಚಾಲನೆ ಮಾಡಿ. |  |
| 21 | `pond_care.TOPICS.aeration.text[3]` | The Weather page shows tonight's oxygen crash risk. | ಇಂದು ರಾತ್ರಿಯ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯವನ್ನು ಹವಾಮಾನ ಪುಟ ತೋರಿಸುತ್ತದೆ. |  |
| 22 | `pond_care.TOPICS.stocking.title` | How many fish | ಎಷ್ಟು ಮೀನು |  |
| 23 | `pond_care.TOPICS.stocking.text[0]` | Don't put too many fish in one pond: crowded fish get stressed, use up the oxygen and dirty the water. | ಒಂದೇ ಕೊಳದಲ್ಲಿ ತುಂಬಾ ಮೀನುಗಳನ್ನು ಹಾಕಬೇಡಿ: ಕಿಕ್ಕಿರಿದ ಮೀನುಗಳು ಒತ್ತಡಕ್ಕೆ ಒಳಗಾಗುತ್ತವೆ, ಆಮ್ಲಜನಕವನ್ನು ಮುಗಿಸುತ್ತವೆ ಮತ್ತು ನೀರನ್ನು ಕೊಳಕು ಮಾಡುತ್ತವೆ. |  |
| 24 | `pond_care.TOPICS.stocking.text[1]` | For how many fish to put in your pond, follow your hatchery or fisheries officer. | ನಿಮ್ಮ ಕೊಳಕ್ಕೆ ಎಷ್ಟು ಮೀನು ಹಾಕಬೇಕು ಎಂದು ನಿಮ್ಮ ಮರಿ ಉತ್ಪಾದನಾ ಕೇಂದ್ರ (ಹ್ಯಾಚರಿ) ಅಥವಾ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯ ಸಲಹೆ ಪಾಲಿಸಿ. |  |
| 25 | `pond_care.TOPICS.checks.title` | Daily and weekly checks | ದಿನನಿತ್ಯ ಮತ್ತು ವಾರದ ಪರಿಶೀಲನೆ |  |
| 26 | `pond_care.TOPICS.checks.text[0]` | Every day at dawn, watch the fish: gasping at the surface means low oxygen. | ಪ್ರತಿದಿನ ಬೆಳಗಿನ ಜಾವ ಮೀನುಗಳನ್ನು ಗಮನಿಸಿ: ಮೇಲ್ಮೈಯಲ್ಲಿ ಉಸಿರಿಗಾಗಿ ಒದ್ದಾಡುವುದು ಎಂದರೆ ಆಮ್ಲಜನಕ ಕಡಿಮೆ. |  |
| 27 | `pond_care.TOPICS.checks.text[1]` | Every day, look at the water colour and smell it: very green water or a rotten-egg smell are warning signs. | ಪ್ರತಿದಿನ ನೀರಿನ ಬಣ್ಣ ನೋಡಿ ಮತ್ತು ವಾಸನೆ ಗಮನಿಸಿ: ತುಂಬಾ ಹಸಿರು ನೀರು ಅಥವಾ ಕೊಳೆತ ಮೊಟ್ಟೆಯ ವಾಸನೆ ಎಚ್ಚರಿಕೆಯ ಲಕ್ಷಣಗಳು. |  |
| 28 | `pond_care.TOPICS.checks.text[2]` | Take out leftover feed and dead fish. | ಉಳಿದ ಆಹಾರ ಮತ್ತು ಸತ್ತ ಮೀನುಗಳನ್ನು ಹೊರತೆಗೆಯಿರಿ. |  |
| 29 | `pond_care.TOPICS.checks.text[3]` | Once a week, test the water with the test kit and enter the readings in the app. | ವಾರಕ್ಕೊಮ್ಮೆ ಟೆಸ್ಟ್ ಕಿಟ್‌ನಿಂದ ನೀರನ್ನು ಪರೀಕ್ಷಿಸಿ ಮತ್ತು ಅಳತೆಗಳನ್ನು ಆ್ಯಪ್‌ನಲ್ಲಿ ನಮೂದಿಸಿ. |  |

## 32. Messages from the server: My ponds and devices (server messages)

Shown on the Pond page, the status strip and to devices (backend/ponds.py). The cause words follow the pond name in the strip, e.g. "Pond 2: Danger · low oxygen".

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `ponds.DEMO_MODE` | Demo mode: ponds reset when the server sleeps. | ಡೆಮೊ ಮೋಡ್: ಸರ್ವರ್ ನಿದ್ರಿಸಿದಾಗ ಕೊಳಗಳು ಅಳಿಸಿಹೋಗುತ್ತವೆ. |  |
| 2 | `ponds.BAD_FARM_CODE` | Missing or wrong farm code. | ಫಾರ್ಮ್ ಕೋಡ್ ಇಲ್ಲ ಅಥವಾ ತಪ್ಪಾಗಿದೆ. |  |
| 3 | `ponds.NOT_FOUND` | Pond not found. | ಕೊಳ ಸಿಗಲಿಲ್ಲ. |  |
| 4 | `ponds.TOO_MANY_PONDS` | You can add up to 20 ponds. | ನೀವು 20 ಕೊಳಗಳವರೆಗೆ ಸೇರಿಸಬಹುದು. |  |
| 5 | `ponds.HAS_DEVICE` | This pond already has a device. Remove it first, or make a new key. | ಈ ಕೊಳಕ್ಕೆ ಈಗಾಗಲೇ ಸಾಧನವಿದೆ. ಮೊದಲು ಅದನ್ನು ತೆಗೆಯಿರಿ, ಅಥವಾ ಹೊಸ ಕೀ ಮಾಡಿ. |  |
| 6 | `ponds.NO_DEVICE` | This pond has no device. | ಈ ಕೊಳಕ್ಕೆ ಯಾವುದೇ ಸಾಧನವಿಲ್ಲ. |  |
| 7 | `ponds.TOO_SOON` | Too many readings. Send at most one reading every 30 seconds. | ತುಂಬಾ ಅಳತೆಗಳು. 30 ಸೆಕೆಂಡಿಗೆ ಒಂದಕ್ಕಿಂತ ಹೆಚ್ಚು ಅಳತೆ ಕಳುಹಿಸಬೇಡಿ. |  |
| 8 | `ponds.CAUSE_WORDS dissolved_oxygen low` | low oxygen | ಕಡಿಮೆ ಆಮ್ಲಜನಕ |  |
| 9 | `ponds.CAUSE_WORDS ph low` | low pH | ಕಡಿಮೆ pH |  |
| 10 | `ponds.CAUSE_WORDS ph high` | high pH | ಹೆಚ್ಚು pH |  |
| 11 | `ponds.CAUSE_WORDS temperature high` | hot water | ಬಿಸಿ ನೀರು |  |
| 12 | `ponds.CAUSE_WORDS temperature low` | cold water | ತಣ್ಣನೆಯ ನೀರು |  |
| 13 | `ponds.CAUSE_WORDS ammonia high` | high ammonia | ಹೆಚ್ಚು ಅಮೋನಿಯಾ |  |
| 14 | `ponds.CAUSE_WORDS nitrate high` | high nitrate | ಹೆಚ್ಚು ನೈಟ್ರೇಟ್ |  |

## 33. Messages from the server: Shop: assistant answers

Ready answers to Shop questions (backend/shop.py). `{name}` is a product name, `{n}` a number of ponds or alerts, `{price}` e.g. ಅಂದಾಜು ₹23,000, `{budget}` e.g. 5,000.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `shop.TEXT.not_for_sale` | Not for sale yet. No payment is taken. | ಇನ್ನೂ ಮಾರಾಟಕ್ಕಿಲ್ಲ. ಯಾವುದೇ ಹಣ ಪಡೆಯುವುದಿಲ್ಲ. |  |
| 2 | `shop.TEXT.orders` | Orders open after our pilot with farmers. You can make a list in the Shop tab and copy it for your cooperative. | ರೈತರೊಂದಿಗಿನ ನಮ್ಮ ಪ್ರಾಯೋಗಿಕ ಯೋಜನೆಯ ನಂತರ ಆರ್ಡರ್‌ಗಳು ಆರಂಭವಾಗುತ್ತವೆ. ಅಂಗಡಿ ಟ್ಯಾಬ್‌ನಲ್ಲಿ ಪಟ್ಟಿ ಮಾಡಿ, ನಿಮ್ಮ ಸಹಕಾರ ಸಂಘಕ್ಕಾಗಿ ನಕಲಿಸಬಹುದು. |  |
| 3 | `shop.TEXT.start` | Start with the free app and a test kit. | ಉಚಿತ ಆ್ಯಪ್ ಮತ್ತು ಟೆಸ್ಟ್ ಕಿಟ್‌ನಿಂದ ಪ್ರಾರಂಭಿಸಿ. |  |
| 4 | `shop.TEXT.get` | Get the {name}, and keep using the free app and a test kit. | {name} ಪಡೆಯಿರಿ, ಜೊತೆಗೆ ಉಚಿತ ಆ್ಯಪ್ ಮತ್ತು ಟೆಸ್ಟ್ ಕಿಟ್ ಬಳಸುತ್ತಿರಿ. |  |
| 5 | `shop.TEXT.for` | What it is for: | ಇದು ಯಾವುದಕ್ಕೆ: |  |
| 6 | `shop.TEXT.where` | Where: | ಎಲ್ಲಿ: |  |
| 7 | `shop.TEXT.how` | How: | ಹೇಗೆ: |  |
| 8 | `shop.TEXT.why` | Why: | ಏಕೆ: |  |
| 9 | `shop.TEXT.care` | Care: | ಆರೈಕೆ: |  |
| 10 | `shop.TEXT.why_need` | Why you need it: | ಇದು ಏಕೆ ಬೇಕು: |  |
| 11 | `shop.TEXT.see_shop` | See the Shop tab: {prices}. | ಅಂಗಡಿ ಟ್ಯಾಬ್ ನೋಡಿ: {prices}. |  |
| 12 | `shop.TEXT.see_shop_how` | See the Shop tab for how to use each one. | ಪ್ರತಿಯೊಂದನ್ನು ಹೇಗೆ ಬಳಸುವುದು ಎಂದು ಅಂಗಡಿ ಟ್ಯಾಬ್‌ನಲ್ಲಿ ನೋಡಿ. |  |
| 13 | `shop.TEXT.one_sensor` | One sensor watches one pond. For several ponds, each needs its own sensor. | ಒಂದು ಸೆನ್ಸರ್ ಒಂದೇ ಕೊಳವನ್ನು ಗಮನಿಸುತ್ತದೆ. ಹಲವು ಕೊಳಗಳಿದ್ದರೆ, ಪ್ರತಿಯೊಂದಕ್ಕೂ ಬೇರೆ ಸೆನ್ಸರ್ ಬೇಕು. |  |
| 14 | `shop.TEXT.one_pond` | One sensor watches one pond. | ಒಂದು ಸೆನ್ಸರ್ ಒಂದೇ ಕೊಳವನ್ನು ಗಮನಿಸುತ್ತದೆ. |  |
| 15 | `shop.TEXT.n_ponds` | For {n} ponds you need {n} sensors, one in each pond. | {n} ಕೊಳಗಳಿಗೆ {n} ಸೆನ್ಸರ್‌ಗಳು ಬೇಕು, ಪ್ರತಿ ಕೊಳಕ್ಕೆ ಒಂದು. |  |
| 16 | `shop.TEXT.several` | Each pond needs its own sensor. | ಪ್ರತಿ ಕೊಳಕ್ಕೂ ಅದರದೇ ಸೆನ್ಸರ್ ಬೇಕು. |  |
| 17 | `shop.TEXT.kit_all_ponds` | One test kit can check all your ponds, one sample at a time. | ಒಂದೇ ಟೆಸ್ಟ್ ಕಿಟ್‌ನಿಂದ ಎಲ್ಲಾ ಕೊಳಗಳನ್ನು, ಒಂದೊಂದಾಗಿ ಪರೀಕ್ಷಿಸಬಹುದು. |  |
| 18 | `shop.TEXT.crash_high` | tonight's oxygen crash risk is High | ಇಂದು ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯ ಹೆಚ್ಚು |  |
| 19 | `shop.TEXT.night_low` | your pond had low oxygen at night {n} times recently | ಇತ್ತೀಚೆಗೆ ನಿಮ್ಮ ಕೊಳದಲ್ಲಿ ರಾತ್ರಿ {n} ಬಾರಿ ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗಿತ್ತು |  |
| 20 | `shop.TEXT.night_low_1` | your pond had low oxygen at night recently | ಇತ್ತೀಚೆಗೆ ನಿಮ್ಮ ಕೊಳದಲ್ಲಿ ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗಿತ್ತು |  |
| 21 | `shop.TEXT.ph_often` | pH went out of the safe range {n} times recently | ಇತ್ತೀಚೆಗೆ pH {n} ಬಾರಿ ಸುರಕ್ಷಿತ ಮಟ್ಟ ಮೀರಿತ್ತು |  |
| 22 | `shop.TEXT.ph_tip` | Check pH every week with the test kit. The Full Pond kit also watches pH day and night. | ಪ್ರತಿ ವಾರ ಟೆಸ್ಟ್ ಕಿಟ್‌ನಿಂದ pH ಪರೀಕ್ಷಿಸಿ. ಫುಲ್ ಪಾಂಡ್ ಕಿಟ್ ಹಗಲು-ರಾತ್ರಿ pH ಅನ್ನೂ ಗಮನಿಸುತ್ತದೆ. |  |
| 23 | `shop.TEXT.no_need` | there are no night oxygen problems and tonight's crash risk is not High, so a sensor is not needed yet | ರಾತ್ರಿಯ ಆಮ್ಲಜನಕ ಸಮಸ್ಯೆ ಇಲ್ಲ ಮತ್ತು ಇಂದು ರಾತ್ರಿ ಕುಸಿತದ ಅಪಾಯ ಹೆಚ್ಚಿಲ್ಲ, ಆದ್ದರಿಂದ ಈಗ ಸೆನ್ಸರ್ ಬೇಕಿಲ್ಲ |  |
| 24 | `shop.TEXT.budget` | The {name} is {price}, more than your budget of ₹{budget}. Start with the test kit and the free app. | {name} ಬೆಲೆ {price}, ಇದು ನಿಮ್ಮ ₹{budget} ಬಜೆಟ್‌ಗಿಂತ ಹೆಚ್ಚು. ಟೆಸ್ಟ್ ಕಿಟ್ ಮತ್ತು ಉಚಿತ ಆ್ಯಪ್‌ನಿಂದ ಪ್ರಾರಂಭಿಸಿ. |  |
| 25 | `shop.TEXT.simulated` | (simulated data) | (ಅನುಕರಿಸಿದ ಡೇಟಾ) |  |

## 34. Messages from the server: Shop: products

frontend/shop-data.json: shown on the Shop page and used by the assistant.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `shop-data.json test-kit.name` | Ammonia + pH test kit | ಅಮೋನಿಯಾ + pH ಟೆಸ್ಟ್ ಕಿಟ್ |  |
| 2 | `shop-data.json test-kit.desc` | Drops and a colour chart for a weekly check by hand. | ವಾರಕ್ಕೊಮ್ಮೆ ಕೈಯಿಂದ ಪರೀಕ್ಷಿಸಲು ಹನಿಗಳು ಮತ್ತು ಬಣ್ಣದ ಚಾರ್ಟ್. |  |
| 3 | `shop-data.json test-kit.short` | weekly ammonia and pH check | ವಾರದ ಅಮೋನಿಯಾ ಮತ್ತು pH ಪರೀಕ್ಷೆ |  |
| 4 | `shop-data.json test-kit.measures` | Ammonia, pH | ಅಮೋನಿಯಾ, pH |  |
| 5 | `shop-data.json test-kit.why` | Type the results into the app's test-kit form (More page) to see if the pond is safe. | ಫಲಿತಾಂಶವನ್ನು ಆ್ಯಪ್‌ನ ಟೆಸ್ಟ್ ಕಿಟ್ ಫಾರ್ಮ್‌ನಲ್ಲಿ (ಇತರೆ ಪುಟ) ನಮೂದಿಸಿ, ಕೊಳ ಸುರಕ್ಷಿತವೇ ಎಂದು ನೋಡಿ. |  |
| 6 | `shop-data.json test-kit.solves` | Shows ammonia and pH problems that you cannot see by looking at the water. | ನೀರನ್ನು ನೋಡಿ ತಿಳಿಯಲಾಗದ ಅಮೋನಿಯಾ ಮತ್ತು pH ಸಮಸ್ಯೆಗಳನ್ನು ತೋರಿಸುತ್ತದೆ. |  |
| 7 | `shop-data.json test-kit.where` | Take the water sample from about 30 cm deep, away from the inlet and the aerator, early in the morning. | ಒಳಹರಿವು ಮತ್ತು ಏರೇಟರ್‌ನಿಂದ ದೂರ, ಸುಮಾರು 30 cm ಆಳದಿಂದ, ಬೆಳಿಗ್ಗೆ ಬೇಗ ನೀರಿನ ಮಾದರಿ ತೆಗೆದುಕೊಳ್ಳಿ. |  |
| 8 | `shop-data.json test-kit.steps[1]` | Fill the kit's tube with pond water from about 30 cm deep, early in the morning. | ಕಿಟ್‌ನ ಟ್ಯೂಬ್‌ಗೆ ಸುಮಾರು 30 cm ಆಳದ ಕೊಳದ ನೀರನ್ನು ಬೆಳಿಗ್ಗೆ ಬೇಗ ತುಂಬಿಸಿ. |  |
| 9 | `shop-data.json test-kit.steps[2]` | Add the test drops to the tube as the kit's leaflet shows, and shake gently. | ಕಿಟ್‌ನ ಕರಪತ್ರದಲ್ಲಿ ತೋರಿಸಿದಂತೆ ಟೆಸ್ಟ್ ಹನಿಗಳನ್ನು ಟ್ಯೂಬ್‌ಗೆ ಸೇರಿಸಿ, ನಿಧಾನವಾಗಿ ಅಲುಗಾಡಿಸಿ. |  |
| 10 | `shop-data.json test-kit.steps[3]` | Wait for the colour, then match it with the colour chart. | ಬಣ್ಣ ಬರುವವರೆಗೆ ಕಾಯಿರಿ, ನಂತರ ಅದನ್ನು ಬಣ್ಣದ ಚಾರ್ಟ್‌ಗೆ ಹೋಲಿಸಿ. |  |
| 11 | `shop-data.json test-kit.steps[4]` | Type the numbers into AquaNexus: More page, Enter test-kit readings. | ಸಂಖ್ಯೆಗಳನ್ನು AquaNexus ನಲ್ಲಿ ನಮೂದಿಸಿ: ಇತರೆ ಪುಟ, ಟೆಸ್ಟ್ ಕಿಟ್ ಅಳತೆಗಳನ್ನು ನಮೂದಿಸಿ. |  |
| 12 | `shop-data.json test-kit.care[1]` | Rinse the tubes with clean water after each test. | ಪ್ರತಿ ಪರೀಕ್ಷೆಯ ನಂತರ ಟ್ಯೂಬ್‌ಗಳನ್ನು ಶುದ್ಧ ನೀರಿನಿಂದ ತೊಳೆಯಿರಿ. |  |
| 13 | `shop-data.json test-kit.care[2]` | Keep the kit cool, dry and out of the sun, and check the expiry date: old drops give wrong colours. | ಕಿಟ್ ಅನ್ನು ತಂಪಾದ, ಒಣ ಜಾಗದಲ್ಲಿ ಬಿಸಿಲಿನಿಂದ ದೂರ ಇಡಿ. ಅವಧಿ ಮುಗಿಯುವ ದಿನಾಂಕ ನೋಡಿ: ಹಳೆಯ ಹನಿಗಳು ತಪ್ಪು ಬಣ್ಣ ಕೊಡುತ್ತವೆ. |  |
| 14 | `shop-data.json night-watch.name` | Night-Watch kit | ನೈಟ್-ವಾಚ್ ಕಿಟ್ |  |
| 15 | `shop-data.json night-watch.desc` | Optical oxygen (DO) and temperature sensor, ESP32 board, 4G, solar panel, in a waterproof IP65 box. | ಆಪ್ಟಿಕಲ್ ಆಮ್ಲಜನಕ (DO) ಮತ್ತು ತಾಪಮಾನ ಸೆನ್ಸರ್, ESP32 ಬೋರ್ಡ್, 4G, ಸೌರ ಫಲಕ, ನೀರು ನುಗ್ಗದ IP65 ಪೆಟ್ಟಿಗೆಯಲ್ಲಿ. |  |
| 16 | `shop-data.json night-watch.short` | warns of a night oxygen crash | ರಾತ್ರಿಯ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಬಗ್ಗೆ ಎಚ್ಚರಿಸುತ್ತದೆ |  |
| 17 | `shop-data.json night-watch.measures` | Dissolved oxygen, water temperature | ಕರಗಿದ ಆಮ್ಲಜನಕ, ನೀರಿನ ತಾಪಮಾನ |  |
| 18 | `shop-data.json night-watch.why` | Watches oxygen all night and warns you before dawn, when fish are most at risk. | ರಾತ್ರಿಯಿಡೀ ಆಮ್ಲಜನಕವನ್ನು ಗಮನಿಸಿ, ಮೀನುಗಳಿಗೆ ಹೆಚ್ಚು ಅಪಾಯವಿರುವ ಬೆಳಗಿನ ಜಾವಕ್ಕೂ ಮೊದಲೇ ಎಚ್ಚರಿಸುತ್ತದೆ. |  |
| 19 | `shop-data.json night-watch.solves` | Warns you about a night oxygen crash before dawn, while you are asleep. | ನೀವು ನಿದ್ರಿಸುತ್ತಿರುವಾಗ, ರಾತ್ರಿಯ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಬಗ್ಗೆ ಬೆಳಗಾಗುವ ಮೊದಲೇ ಎಚ್ಚರಿಸುತ್ತದೆ. |  |
| 20 | `shop-data.json night-watch.where` | Hang the oxygen probe near the pond bottom, away from the aerator. Fix the box on a pole in the shade, with the solar panel in the sun. | ಆಮ್ಲಜನಕ ಪ್ರೋಬ್ ಅನ್ನು ಕೊಳದ ತಳದ ಹತ್ತಿರ, ಏರೇಟರ್‌ನಿಂದ ದೂರ ತೂಗುಹಾಕಿ. ಪೆಟ್ಟಿಗೆಯನ್ನು ಕಂಬದ ಮೇಲೆ ನೆರಳಿನಲ್ಲಿ ಇಡಿ, ಸೌರ ಫಲಕ ಬಿಸಿಲಿನಲ್ಲಿರಲಿ. |  |
| 21 | `shop-data.json night-watch.steps[1]` | Fix the box on a pole at the pond edge, in the shade. | ಪೆಟ್ಟಿಗೆಯನ್ನು ಕೊಳದ ದಡದಲ್ಲಿ ಕಂಬದ ಮೇಲೆ ನೆರಳಿನಲ್ಲಿ ಜೋಡಿಸಿ. |  |
| 22 | `shop-data.json night-watch.steps[2]` | Point the solar panel at the sun. | ಸೌರ ಫಲಕವನ್ನು ಸೂರ್ಯನ ಕಡೆಗೆ ತಿರುಗಿಸಿ. |  |
| 23 | `shop-data.json night-watch.steps[3]` | Hang the probe near the pond bottom, away from the aerator. | ಪ್ರೋಬ್ ಅನ್ನು ಕೊಳದ ತಳದ ಹತ್ತಿರ, ಏರೇಟರ್‌ನಿಂದ ದೂರ ತೂಗುಹಾಕಿ. |  |
| 24 | `shop-data.json night-watch.steps[4]` | Switch it on. It sends readings every 5 minutes at night, and AquaNexus warns you if oxygen falls. | ಸ್ವಿಚ್ ಆನ್ ಮಾಡಿ. ಇದು ರಾತ್ರಿ ಪ್ರತಿ 5 ನಿಮಿಷಕ್ಕೊಮ್ಮೆ ಅಳತೆ ಕಳುಹಿಸುತ್ತದೆ, ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾದರೆ AquaNexus ಎಚ್ಚರಿಸುತ್ತದೆ. |  |
| 25 | `shop-data.json night-watch.care[1]` | Rinse the probe with clean water every week and gently wipe off algae and slime. | ಪ್ರತಿ ವಾರ ಪ್ರೋಬ್ ಅನ್ನು ಶುದ್ಧ ನೀರಿನಿಂದ ತೊಳೆದು, ಪಾಚಿ ಮತ್ತು ಲೋಳೆಯನ್ನು ನಿಧಾನವಾಗಿ ಒರೆಸಿ. |  |
| 26 | `shop-data.json night-watch.care[2]` | Replace the DO sensor cap when it wears out (listed as a spare in the Shop). | DO ಸೆನ್ಸರ್ ಕ್ಯಾಪ್ ಸವೆದಾಗ ಬದಲಾಯಿಸಿ (ಅಂಗಡಿಯಲ್ಲಿ ಬಿಡಿಭಾಗವಾಗಿ ಪಟ್ಟಿ ಮಾಡಲಾಗಿದೆ). |  |
| 27 | `shop-data.json night-watch.care[3]` | Wipe dust and bird droppings off the solar panel every month. | ಪ್ರತಿ ತಿಂಗಳು ಸೌರ ಫಲಕದ ಮೇಲಿನ ಧೂಳು ಮತ್ತು ಹಕ್ಕಿ ಹಿಕ್ಕೆಯನ್ನು ಒರೆಸಿ. |  |
| 28 | `shop-data.json full-pond.name` | Full Pond kit | ಫುಲ್ ಪಾಂಡ್ ಕಿಟ್ |  |
| 29 | `shop-data.json full-pond.desc` | The Night-Watch kit plus an industrial pH probe with a signal isolator. | ನೈಟ್-ವಾಚ್ ಕಿಟ್ ಜೊತೆಗೆ ಸಿಗ್ನಲ್ ಐಸೊಲೇಟರ್ ಇರುವ ಕೈಗಾರಿಕಾ pH ಪ್ರೋಬ್. |  |
| 30 | `shop-data.json full-pond.short` | Night-Watch plus pH | ನೈಟ್-ವಾಚ್ ಜೊತೆಗೆ pH |  |
| 31 | `shop-data.json full-pond.measures` | Dissolved oxygen, water temperature, pH | ಕರಗಿದ ಆಮ್ಲಜನಕ, ನೀರಿನ ತಾಪಮಾನ, pH |  |
| 32 | `shop-data.json full-pond.why` | Adds pH, day and night, to the overnight oxygen watch. | ರಾತ್ರಿಯ ಆಮ್ಲಜನಕ ಕಾವಲಿನ ಜೊತೆಗೆ ಹಗಲು-ರಾತ್ರಿ pH ಅನ್ನೂ ಗಮನಿಸುತ್ತದೆ. |  |
| 33 | `shop-data.json full-pond.solves` | Warns about night oxygen crashes, and also shows when pH goes out of range, day and night. | ರಾತ್ರಿಯ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಬಗ್ಗೆ ಎಚ್ಚರಿಸುತ್ತದೆ, ಮತ್ತು pH ಮಿತಿ ಮೀರಿದಾಗಲೂ ಹಗಲು-ರಾತ್ರಿ ತೋರಿಸುತ್ತದೆ. |  |
| 34 | `shop-data.json full-pond.where` | As the Night-Watch kit. Hang the pH probe next to the oxygen probe, away from the aerator. | ನೈಟ್-ವಾಚ್ ಕಿಟ್‌ನಂತೆಯೇ. pH ಪ್ರೋಬ್ ಅನ್ನು ಆಮ್ಲಜನಕ ಪ್ರೋಬ್‌ನ ಪಕ್ಕದಲ್ಲಿ, ಏರೇಟರ್‌ನಿಂದ ದೂರ ತೂಗುಹಾಕಿ. |  |
| 35 | `shop-data.json full-pond.steps[1]` | Fix the box on a pole at the pond edge, in the shade. | ಪೆಟ್ಟಿಗೆಯನ್ನು ಕೊಳದ ದಡದಲ್ಲಿ ಕಂಬದ ಮೇಲೆ ನೆರಳಿನಲ್ಲಿ ಜೋಡಿಸಿ. |  |
| 36 | `shop-data.json full-pond.steps[2]` | Point the solar panel at the sun. | ಸೌರ ಫಲಕವನ್ನು ಸೂರ್ಯನ ಕಡೆಗೆ ತಿರುಗಿಸಿ. |  |
| 37 | `shop-data.json full-pond.steps[3]` | Hang both probes near the pond bottom, away from the aerator. | ಎರಡೂ ಪ್ರೋಬ್‌ಗಳನ್ನು ಕೊಳದ ತಳದ ಹತ್ತಿರ, ಏರೇಟರ್‌ನಿಂದ ದೂರ ತೂಗುಹಾಕಿ. |  |
| 38 | `shop-data.json full-pond.steps[4]` | Switch it on. It sends oxygen, temperature and pH readings every 5 minutes at night. | ಸ್ವಿಚ್ ಆನ್ ಮಾಡಿ. ಇದು ರಾತ್ರಿ ಪ್ರತಿ 5 ನಿಮಿಷಕ್ಕೊಮ್ಮೆ ಆಮ್ಲಜನಕ, ತಾಪಮಾನ ಮತ್ತು pH ಅಳತೆ ಕಳುಹಿಸುತ್ತದೆ. |  |
| 39 | `shop-data.json full-pond.care[1]` | Rinse the probe with clean water every week and gently wipe off algae and slime. | ಪ್ರತಿ ವಾರ ಪ್ರೋಬ್ ಅನ್ನು ಶುದ್ಧ ನೀರಿನಿಂದ ತೊಳೆದು, ಪಾಚಿ ಮತ್ತು ಲೋಳೆಯನ್ನು ನಿಧಾನವಾಗಿ ಒರೆಸಿ. |  |
| 40 | `shop-data.json full-pond.care[2]` | Replace the DO sensor cap when it wears out (listed as a spare in the Shop). | DO ಸೆನ್ಸರ್ ಕ್ಯಾಪ್ ಸವೆದಾಗ ಬದಲಾಯಿಸಿ (ಅಂಗಡಿಯಲ್ಲಿ ಬಿಡಿಭಾಗವಾಗಿ ಪಟ್ಟಿ ಮಾಡಲಾಗಿದೆ). |  |
| 41 | `shop-data.json full-pond.care[3]` | Recalibrate the pH probe every month, as the kit's guide shows. | ಕಿಟ್‌ನ ಮಾರ್ಗದರ್ಶಿಯಲ್ಲಿ ತೋರಿಸಿದಂತೆ ಪ್ರತಿ ತಿಂಗಳು pH ಪ್ರೋಬ್ ಅನ್ನು ಮರು-ಮಾಪನಾಂಕ (ರಿಕ್ಯಾಲಿಬ್ರೇಟ್) ಮಾಡಿ. |  |
| 42 | `shop-data.json full-pond.care[4]` | Wipe dust and bird droppings off the solar panel every month. | ಪ್ರತಿ ತಿಂಗಳು ಸೌರ ಫಲಕದ ಮೇಲಿನ ಧೂಳು ಮತ್ತು ಹಕ್ಕಿ ಹಿಕ್ಕೆಯನ್ನು ಒರೆಸಿ. |  |
| 43 | `shop-data.json full-pond.price_note` | depending on probes | ಪ್ರೋಬ್‌ಗಳನ್ನು ಅವಲಂಬಿಸಿ |  |
| 44 | `shop-data.json do-cap.name` | Spare: DO sensor cap | ಬಿಡಿಭಾಗ: DO ಸೆನ್ಸರ್ ಕ್ಯಾಪ್ |  |
| 45 | `shop-data.json do-cap.desc` | Replacement cap for the optical oxygen sensor. | ಆಪ್ಟಿಕಲ್ ಆಮ್ಲಜನಕ ಸೆನ್ಸರ್‌ಗೆ ಬದಲಿ ಕ್ಯಾಪ್. |  |
| 46 | `shop-data.json do-cap.short` | keeps oxygen readings right | ಆಮ್ಲಜನಕ ಅಳತೆ ಸರಿಯಾಗಿರಲು |  |
| 47 | `shop-data.json do-cap.measures` | Part of the oxygen sensor | ಆಮ್ಲಜನಕ ಸೆನ್ಸರ್‌ನ ಭಾಗ |  |
| 48 | `shop-data.json do-cap.why` | The cap wears out over time and must be replaced to keep oxygen readings right. | ಕಾಲಾನಂತರದಲ್ಲಿ ಕ್ಯಾಪ್ ಸವೆಯುತ್ತದೆ. ಆಮ್ಲಜನಕದ ಅಳತೆ ಸರಿಯಾಗಿರಲು ಅದನ್ನು ಬದಲಾಯಿಸಬೇಕು. |  |
| 49 | `shop-data.json do-cap.solves` | A worn cap gives wrong oxygen readings. A new cap makes them right again. | ಸವೆದ ಕ್ಯಾಪ್ ತಪ್ಪು ಆಮ್ಲಜನಕ ಅಳತೆ ಕೊಡುತ್ತದೆ. ಹೊಸ ಕ್ಯಾಪ್ ಅವುಗಳನ್ನು ಮತ್ತೆ ಸರಿಮಾಡುತ್ತದೆ. |  |
| 50 | `shop-data.json do-cap.where` | On the tip of the Night-Watch oxygen probe. | ನೈಟ್-ವಾಚ್ ಆಮ್ಲಜನಕ ಪ್ರೋಬ್‌ನ ತುದಿಯಲ್ಲಿ. |  |
| 51 | `shop-data.json do-cap.steps[1]` | Switch the box off and lift the probe out of the water. | ಪೆಟ್ಟಿಗೆಯನ್ನು ಆಫ್ ಮಾಡಿ, ಪ್ರೋಬ್ ಅನ್ನು ನೀರಿನಿಂದ ಹೊರತೆಗೆಯಿರಿ. |  |
| 52 | `shop-data.json do-cap.steps[2]` | Unscrew the old cap and screw on the new one. Do not touch the inside of the cap. | ಹಳೆಯ ಕ್ಯಾಪ್ ತಿರುಗಿಸಿ ತೆಗೆದು, ಹೊಸದನ್ನು ತಿರುಗಿಸಿ ಹಾಕಿ. ಕ್ಯಾಪ್‌ನ ಒಳಭಾಗವನ್ನು ಮುಟ್ಟಬೇಡಿ. |  |
| 53 | `shop-data.json do-cap.steps[3]` | Put the probe back in the water, switch on, and set it up as the cap's leaflet shows. | ಪ್ರೋಬ್ ಅನ್ನು ಮತ್ತೆ ನೀರಿಗೆ ಇಳಿಸಿ, ಸ್ವಿಚ್ ಆನ್ ಮಾಡಿ, ಕ್ಯಾಪ್‌ನ ಕರಪತ್ರದಲ್ಲಿ ತೋರಿಸಿದಂತೆ ಹೊಂದಿಸಿ. |  |
| 54 | `shop-data.json do-cap.care` | Keep the spare cap in its sealed pack until you use it. | ಬಳಸುವವರೆಗೆ ಬಿಡಿ ಕ್ಯಾಪ್ ಅನ್ನು ಅದರ ಮುಚ್ಚಿದ ಪ್ಯಾಕ್‌ನಲ್ಲೇ ಇಡಿ. |  |
| 55 | `shop-data.json solar-10w.name` | Spare: 10 W solar panel + charge board | ಬಿಡಿಭಾಗ: 10 W ಸೌರ ಫಲಕ + ಚಾರ್ಜ್ ಬೋರ್ಡ್ |  |
| 56 | `shop-data.json solar-10w.desc` | Panel and charging board that keep the sensor box powered. | ಸೆನ್ಸರ್ ಪೆಟ್ಟಿಗೆಗೆ ವಿದ್ಯುತ್ ನೀಡುವ ಫಲಕ ಮತ್ತು ಚಾರ್ಜಿಂಗ್ ಬೋರ್ಡ್. |  |
| 57 | `shop-data.json solar-10w.short` | keeps the sensor box charged | ಸೆನ್ಸರ್ ಪೆಟ್ಟಿಗೆಯನ್ನು ಚಾರ್ಜ್ ಇಡುತ್ತದೆ |  |
| 58 | `shop-data.json solar-10w.measures` | Power for the sensor box | ಸೆನ್ಸರ್ ಪೆಟ್ಟಿಗೆಗೆ ವಿದ್ಯುತ್ |  |
| 59 | `shop-data.json solar-10w.why` | Replaces a panel or board damaged by weather, so the sensor keeps running. | ಹವಾಮಾನದಿಂದ ಹಾಳಾದ ಫಲಕ ಅಥವಾ ಬೋರ್ಡ್ ಬದಲಿಸಿ, ಸೆನ್ಸರ್ ನಿಲ್ಲದಂತೆ ನೋಡಿಕೊಳ್ಳುತ್ತದೆ. |  |
| 60 | `shop-data.json solar-10w.solves` | Keeps the sensor box charged, so it does not stop at night. | ಸೆನ್ಸರ್ ಪೆಟ್ಟಿಗೆಯನ್ನು ಚಾರ್ಜ್ ಆಗಿ ಇಡುತ್ತದೆ, ಆದ್ದರಿಂದ ಅದು ರಾತ್ರಿ ನಿಲ್ಲುವುದಿಲ್ಲ. |  |
| 61 | `shop-data.json solar-10w.where` | On the box's pole, in full sun, away from tree shade. | ಪೆಟ್ಟಿಗೆಯ ಕಂಬದ ಮೇಲೆ, ಮರದ ನೆರಳಿಲ್ಲದ ಪೂರ್ಣ ಬಿಸಿಲಿನಲ್ಲಿ. |  |
| 62 | `shop-data.json solar-10w.steps[1]` | Switch the box off. | ಪೆಟ್ಟಿಗೆಯನ್ನು ಆಫ್ ಮಾಡಿ. |  |
| 63 | `shop-data.json solar-10w.steps[2]` | Unplug the old panel and board, and plug in the new ones. | ಹಳೆಯ ಫಲಕ ಮತ್ತು ಬೋರ್ಡ್ ತೆಗೆದು, ಹೊಸವನ್ನು ಜೋಡಿಸಿ. |  |
| 64 | `shop-data.json solar-10w.steps[3]` | Point the panel at the sun and switch the box on. | ಫಲಕವನ್ನು ಸೂರ್ಯನ ಕಡೆಗೆ ತಿರುಗಿಸಿ, ಪೆಟ್ಟಿಗೆಯನ್ನು ಆನ್ ಮಾಡಿ. |  |
| 65 | `shop-data.json solar-10w.care` | Wipe dust and bird droppings off the solar panel every month. | ಪ್ರತಿ ತಿಂಗಳು ಸೌರ ಫಲಕದ ಮೇಲಿನ ಧೂಳು ಮತ್ತು ಹಕ್ಕಿ ಹಿಕ್ಕೆಯನ್ನು ಒರೆಸಿ. |  |

## 35. Messages from the server: Alert preview (SMS / WhatsApp)

The SMS and WhatsApp text is built from the risk card and time-until-danger messages above, plus these.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `alerts.POND_NAMES.station1` | Pond 1 | ಕೊಳ 1 |  |
| 2 | `alerts.POND_NAMES.station2` | Pond 2 | ಕೊಳ 2 |  |
| 3 | `alerts.POND_NAMES.station3` | Pond 3 | ಕೊಳ 3 |  |
| 4 | `alerts.APP_NAME` | AquaNexus | AquaNexus |  |
| 5 | `alerts.NO_ALERT` | No alert would be sent: the readings are not in Warning or Danger. | ಯಾವುದೇ ಎಚ್ಚರಿಕೆ ಕಳುಹಿಸುವುದಿಲ್ಲ: ಅಳತೆಗಳು ಎಚ್ಚರಿಕೆ ಅಥವಾ ಅಪಾಯದ ಮಟ್ಟದಲ್ಲಿಲ್ಲ. |  |
