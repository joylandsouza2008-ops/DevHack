# Kannada text review

Every Kannada string in MeenuRaksha, next to its English version, grouped by screen.
Please check each Kannada line is correct, natural and easy for a small fish farmer in
coastal Karnataka to understand. Write any fix in the last column.

- Words in `{curly brackets}` are filled in by the app (numbers, times, names). Please keep them.
- `A  /  B` means the app shows one of two versions, depending on the situation.
- Unit symbols (mg/L, °C, km/h, pH) and the names SMS, WhatsApp, FAO, TNAU, Open-Meteo stay in English.

188 strings. Generated from the code by `python tools/kannada_review.py`; re-run it after changing any text.

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
| 1 | `app.js appName` | MeenuRaksha | ಮೀನುರಕ್ಷಾ |  |
| 2 | `app.js welcomeTagline` | Pond water warnings before your fish are in danger. | ಮೀನುಗಳಿಗೆ ಅಪಾಯ ಬರುವ ಮೊದಲೇ ಕೊಳದ ನೀರಿನ ಎಚ್ಚರಿಕೆ. |  |
| 3 | `app.js start` | Start | ಪ್ರಾರಂಭಿಸಿ |  |
| 4 | `app.js builtBy` | Built by Team Orbit | ನಿರ್ಮಾಣ: ಟೀಮ್ ಆರ್ಬಿಟ್ |  |

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
| 6 | `app.js weatherOffline` | Offline: showing the forecast saved on {when}.  /  Offline. | ಆಫ್‌ಲೈನ್: {when} ರಂದು ಉಳಿಸಿದ ಮುನ್ಸೂಚನೆ ತೋರಿಸಲಾಗುತ್ತಿದೆ.  /  ಆಫ್‌ಲೈನ್. |  |

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
| 1 | `app.js liveTitle` | Live sensor | ಲೈವ್ ಸೆನ್ಸರ್ |  |
| 2 | `app.js liveWaiting` | Connecting to the live sensor… | ಲೈವ್ ಸೆನ್ಸರ್‌ಗೆ ಸಂಪರ್ಕಿಸಲಾಗುತ್ತಿದೆ… |  |
| 3 | `app.js liveNoReading` | No reading from the {pond} sensor yet. Readings appear here as soon as the sensor sends one. | {pond} ಸೆನ್ಸರ್‌ನಿಂದ ಇನ್ನೂ ಯಾವುದೇ ಅಳತೆ ಬಂದಿಲ್ಲ. ಸೆನ್ಸರ್ ಅಳತೆ ಕಳುಹಿಸಿದ ತಕ್ಷಣ ಇಲ್ಲಿ ಕಾಣಿಸುತ್ತದೆ. |  |
| 4 | `app.js liveMeasured` | Measured {when} · received {ago} | ಅಳತೆ ಸಮಯ {when} · {ago} ಬಂದಿದೆ |  |
| 5 | `app.js liveAgo` | {s} s ago  /  ${Math.floor(s / 60)} min ago | {s} ಸೆಕೆಂಡ್ ಹಿಂದೆ  /  ${Math.floor(s / 60)} ನಿಮಿಷ ಹಿಂದೆ |  |
| 6 | `app.js liveStale` | No new reading for {min} min. Check the sensor's power and Wi-Fi. | {min} ನಿಮಿಷಗಳಿಂದ ಹೊಸ ಅಳತೆ ಬಂದಿಲ್ಲ. ಸೆನ್ಸರ್‌ನ ವಿದ್ಯುತ್ ಮತ್ತು Wi-Fi ಪರಿಶೀಲಿಸಿ. |  |
| 7 | `app.js liveLost` | Lost connection to the server. Trying again… | ಸರ್ವರ್ ಸಂಪರ್ಕ ಕಡಿದುಹೋಗಿದೆ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಲಾಗುತ್ತಿದೆ… |  |
| 8 | `app.js liveNote` | Readings are kept only while the server is running. On the free server they are cleared when it sleeps. | ಸರ್ವರ್ ಚಾಲನೆಯಲ್ಲಿರುವವರೆಗೆ ಮಾತ್ರ ಅಳತೆಗಳನ್ನು ಉಳಿಸಲಾಗುತ್ತದೆ. ಉಚಿತ ಸರ್ವರ್ ನಿದ್ರೆಗೆ ಹೋದಾಗ ಅವು ಅಳಿಸಿಹೋಗುತ್ತವೆ. |  |

## 13. Voice alert

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js voiceListen` | Listen to alert | ಎಚ್ಚರಿಕೆ ಕೇಳಿ |  |
| 2 | `app.js voiceStop` | Stop | ನಿಲ್ಲಿಸಿ |  |
| 3 | `app.js voiceNoKannada` | Sorry, this phone has no Kannada voice, so the alert cannot be read aloud in Kannada. Please read the alert on the screen, or switch to English to hear it. | ಕ್ಷಮಿಸಿ, ಈ ಫೋನ್‌ನಲ್ಲಿ ಕನ್ನಡ ಧ್ವನಿ ಇಲ್ಲ, ಆದ್ದರಿಂದ ಎಚ್ಚರಿಕೆಯನ್ನು ಕನ್ನಡದಲ್ಲಿ ಓದಿ ಹೇಳಲು ಆಗುವುದಿಲ್ಲ. ದಯವಿಟ್ಟು ಪರದೆಯ ಮೇಲಿನ ಎಚ್ಚರಿಕೆಯನ್ನು ಓದಿ, ಅಥವಾ ಕೇಳಲು English ಆಯ್ಕೆಮಾಡಿ. |  |
| 4 | `app.js voiceNoEnglish` | Sorry, this phone has no English voice. Please read the alert on the screen. | ಕ್ಷಮಿಸಿ, ಈ ಫೋನ್‌ನಲ್ಲಿ ಇಂಗ್ಲಿಷ್ ಧ್ವನಿ ಇಲ್ಲ. ದಯವಿಟ್ಟು ಪರದೆಯ ಮೇಲಿನ ಎಚ್ಚರಿಕೆಯನ್ನು ಓದಿ. |  |
| 5 | `app.js voiceUnsupported` | Sorry, this browser cannot read aloud. Please read the alert on the screen. | ಕ್ಷಮಿಸಿ, ಈ ಬ್ರೌಸರ್ ಓದಿ ಹೇಳಲು ಆಗುವುದಿಲ್ಲ. ದಯವಿಟ್ಟು ಪರದೆಯ ಮೇಲಿನ ಎಚ್ಚರಿಕೆಯನ್ನು ಓದಿ. |  |

## 14. Alert history

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

## 15. Data sources panel (footer)

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js sourcesTitle` | Data sources | ಡೇಟಾ ಮೂಲಗಳು |  |
| 2 | `app.js sourcesClose` | Close | ಮುಚ್ಚಿ |  |
| 3 | `app.js sourcesIntro` | The simulated pond uses these open datasets and public services. Only the Live sensor card shows readings sent by a pond sensor. | ಅನುಕರಿಸಿದ ಕೊಳವು ಈ ಮುಕ್ತ ಡೇಟಾಸೆಟ್‌ಗಳು ಮತ್ತು ಸಾರ್ವಜನಿಕ ಸೇವೆಗಳನ್ನು ಬಳಸುತ್ತದೆ. ಕೊಳದ ಸೆನ್ಸರ್ ಕಳುಹಿಸಿದ ಅಳತೆಗಳನ್ನು ಲೈವ್ ಸೆನ್ಸರ್ ಕಾರ್ಡ್ ಮಾತ್ರ ತೋರಿಸುತ್ತದೆ. |  |
| 4 | `app.js sourcesPondsUse` | Real sensor readings from 3 fish ponds in Andhra Pradesh (2022-23). Used to make the simulated demo pond and to test our oxygen predictions. | ಆಂಧ್ರಪ್ರದೇಶದ 3 ಮೀನು ಕೊಳಗಳ ನಿಜವಾದ ಸೆನ್ಸರ್ ಅಳತೆಗಳು (2022-23). ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಪ್ರದರ್ಶನ ಕೊಳವನ್ನು ಮಾಡಲು ಮತ್ತು ನಮ್ಮ ಆಮ್ಲಜನಕ ಮುನ್ಸೂಚನೆಗಳನ್ನು ಪರೀಕ್ಷಿಸಲು ಬಳಸಲಾಗಿದೆ. |  |
| 5 | `app.js sourcesPondsLicence` | Licence: unknown (not stated by the uploader). | ಪರವಾನಗಿ: ತಿಳಿದಿಲ್ಲ (ಅಪ್‌ಲೋಡ್ ಮಾಡಿದವರು ತಿಳಿಸಿಲ್ಲ). |  |
| 6 | `app.js sourcesMeteoUse` | Tonight's real weather forecast for Mangaluru, for the night oxygen-crash warning. | ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಎಚ್ಚರಿಕೆಗಾಗಿ ಮಂಗಳೂರಿನ ಇಂದು ರಾತ್ರಿಯ ನಿಜವಾದ ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ. |  |
| 7 | `app.js sourcesMeteoLicence` | Licence: data CC BY 4.0. Free API, non-commercial use only. | ಪರವಾನಗಿ: ಡೇಟಾ CC BY 4.0. ಉಚಿತ API, ವಾಣಿಜ್ಯೇತರ ಬಳಕೆಗೆ ಮಾತ್ರ. |  |
| 8 | `app.js sourcesGuidesUse` | Published guides and research papers behind the Safe / Warning / Danger limits and the “What to do now” steps. | ಸುರಕ್ಷಿತ / ಎಚ್ಚರಿಕೆ / ಅಪಾಯ ಮಿತಿಗಳು ಮತ್ತು “ಈಗ ಏನು ಮಾಡಬೇಕು” ಹಂತಗಳಿಗೆ ಆಧಾರವಾದ ಪ್ರಕಟಿತ ಮಾರ್ಗದರ್ಶಿಗಳು ಮತ್ತು ಸಂಶೋಧನಾ ಲೇಖನಗಳು. |  |
| 9 | `app.js sourcesGuidesLicence` | Copyright of each publisher. We cite their facts; we don't copy them. | ಹಕ್ಕುಸ್ವಾಮ್ಯ ಆಯಾ ಪ್ರಕಾಶಕರದು. ನಾವು ಅವುಗಳ ಮಾಹಿತಿಯನ್ನು ಉಲ್ಲೇಖಿಸುತ್ತೇವೆ, ನಕಲು ಮಾಡುವುದಿಲ್ಲ. |  |
| 10 | `app.js sourcesMendeleyUse` | Checked but not used: some values are impossible (e.g. water at 84 °C). | ಪರಿಶೀಲಿಸಲಾಗಿದೆ, ಆದರೆ ಬಳಸಿಲ್ಲ: ಕೆಲವು ಮೌಲ್ಯಗಳು ಅಸಾಧ್ಯ (ಉದಾ: 84 °C ನೀರು). |  |
| 11 | `app.js sourcesMendeleyLicence` | Licence: CC BY 4.0. | ಪರವಾನಗಿ: CC BY 4.0. |  |
| 12 | `app.js sourcesFishUse` | Fish disease photos for research only. Not used in the app. | ಮೀನು ರೋಗದ ಫೋಟೋಗಳು, ಸಂಶೋಧನೆಗೆ ಮಾತ್ರ. ಆಪ್‌ನಲ್ಲಿ ಬಳಸಿಲ್ಲ. |  |
| 13 | `app.js sourcesFishLicence` | Licence: CC0 (public domain). | ಪರವಾನಗಿ: CC0 (ಸಾರ್ವಜನಿಕ ಸ್ವತ್ತು). |  |
| 14 | `app.js sourcesFull` | Full list with links and licences | ಲಿಂಕ್‌ಗಳು ಮತ್ತು ಪರವಾನಗಿಗಳ ಪೂರ್ಣ ಪಟ್ಟಿ |  |

## 16. Messages from the server: Data labels

Shown on every simulated, test-kit or live-sensor reading.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `simulator.SIMULATED_LABEL` | Simulated data | ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಡೇಟಾ |  |
| 2 | `main.MANUAL_LABEL` | Manual test-kit reading | ಕೈಯಿಂದ ನಮೂದಿಸಿದ ಟೆಸ್ಟ್ ಕಿಟ್ ಅಳತೆ |  |
| 3 | `sensor.LIVE_LABEL` | Live sensor | ಲೈವ್ ಸೆನ್ಸರ್ |  |
| 4 | `sensor.DEMO_LABEL` | Demo device: simulated readings, not a real pond | ಡೆಮೊ ಸಾಧನ: ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಅಳತೆಗಳು, ನಿಜವಾದ ಕೊಳವಲ್ಲ |  |

## 17. Messages from the server: Live sensor: why a reading was refused

Sent back to the sensor and shown on the Live sensor card.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `sensor.REJECTED` | Reading rejected. Check the sensor. | ಅಳತೆಯನ್ನು ತಿರಸ್ಕರಿಸಲಾಗಿದೆ. ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ. |  |
| 2 | `sensor.NO_VALUES` | The reading has no values. Check the sensor. | ಅಳತೆಯಲ್ಲಿ ಯಾವುದೇ ಮೌಲ್ಯಗಳಿಲ್ಲ. ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ. |  |
| 3 | `sensor.WRONG_KEY` | Missing or wrong sensor key. | ಸೆನ್ಸರ್ ಕೀ ಇಲ್ಲ ಅಥವಾ ತಪ್ಪಾಗಿದೆ. |  |
| 4 | `sensor.CLOCK_AHEAD` | The sensor's clock is ahead of the real time. Check the sensor clock. | ಸೆನ್ಸರ್‌ನ ಗಡಿಯಾರ ನಿಜವಾದ ಸಮಯಕ್ಕಿಂತ ಮುಂದಿದೆ. ಸೆನ್ಸರ್ ಗಡಿಯಾರ ಪರಿಶೀಲಿಸಿ. |  |
| 5 | `sensor.NO_TIME_ZONE` | The timestamp has no time zone. Add +05:30 or Z. Check the sensor clock. | ಸಮಯದಲ್ಲಿ ಟೈಮ್ ಝೋನ್ ಇಲ್ಲ. +05:30 ಅಥವಾ Z ಸೇರಿಸಿ. ಸೆನ್ಸರ್ ಗಡಿಯಾರ ಪರಿಶೀಲಿಸಿ. |  |
| 6 | `sensor.TOO_OLD` | The timestamp is more than a day old. Check the sensor clock. | ಸಮಯ ಒಂದು ದಿನಕ್ಕಿಂತ ಹಳೆಯದು. ಸೆನ್ಸರ್ ಗಡಿಯಾರ ಪರಿಶೀಲಿಸಿ. |  |

## 18. Messages from the server: Risk card: level names, parameter names and reasons

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
| 11 | `risk_messages.REASONS.dissolved_oxygen/low/warning` | Oxygen is low ({value} {unit}). Fish may stop eating. Run the aerator. | ಆಮ್ಲಜನಕ ಕಡಿಮೆ ಇದೆ ({value} {unit}). ಮೀನುಗಳು ಆಹಾರ ತಿನ್ನುವುದನ್ನು ನಿಲ್ಲಿಸಬಹುದು. ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ. |  |
| 12 | `risk_messages.REASONS.dissolved_oxygen/low/danger` | Oxygen is very low ({value} {unit}). Fish can die. Turn on the aerator now and add fresh water. | ಆಮ್ಲಜನಕ ತುಂಬಾ ಕಡಿಮೆ ಇದೆ ({value} {unit}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ತಕ್ಷಣ ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ ಮತ್ತು ಹೊಸ ನೀರು ಹಾಕಿ. |  |
| 13 | `risk_messages.REASONS.ph/low/warning` | Water is acidic (pH {value}). Fish grow slowly. Contact your fisheries officer for advice on correcting pH. | ನೀರು ಆಮ್ಲೀಯವಾಗಿದೆ (pH {value}). ಮೀನುಗಳು ನಿಧಾನವಾಗಿ ಬೆಳೆಯುತ್ತವೆ. pH ಸರಿಪಡಿಸುವ ಬಗ್ಗೆ ಸಲಹೆಗಾಗಿ ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ. |  |
| 14 | `risk_messages.REASONS.ph/low/danger` | Water is very acidic (pH {value}). Fish can die. Add fresh water and contact your fisheries officer today. | ನೀರು ತುಂಬಾ ಆಮ್ಲೀಯವಾಗಿದೆ (pH {value}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ಹೊಸ ನೀರು ಹಾಕಿ ಮತ್ತು ಇಂದೇ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ. |  |
| 15 | `risk_messages.REASONS.ph/high/warning` | Water is alkaline (pH {value}). Ammonia becomes more harmful. Add fresh water and stop adding fertiliser. | ನೀರು ಕ್ಷಾರೀಯವಾಗಿದೆ (pH {value}). ಅಮೋನಿಯಾ ಹೆಚ್ಚು ಹಾನಿಕಾರಕವಾಗುತ್ತದೆ. ಹೊಸ ನೀರು ಹಾಕಿ ಮತ್ತು ಗೊಬ್ಬರ ಹಾಕುವುದನ್ನು ನಿಲ್ಲಿಸಿ. |  |
| 16 | `risk_messages.REASONS.ph/high/danger` | Water is very alkaline (pH {value}). Fish can die. Add fresh water now and contact your fisheries officer. | ನೀರು ತುಂಬಾ ಕ್ಷಾರೀಯವಾಗಿದೆ (pH {value}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ತಕ್ಷಣ ಹೊಸ ನೀರು ಹಾಕಿ ಮತ್ತು ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ. |  |
| 17 | `risk_messages.REASONS.temperature/low/warning` | Water is cool ({value} {unit}). Fish eat less. Reduce the feed. | ನೀರು ತಣ್ಣಗಿದೆ ({value} {unit}). ಮೀನುಗಳು ಕಡಿಮೆ ತಿನ್ನುತ್ತವೆ. ಆಹಾರ ಕಡಿಮೆ ಮಾಡಿ. |  |
| 18 | `risk_messages.REASONS.temperature/low/danger` | Water is too cold ({value} {unit}). Fish are stressed and may fall sick. Feed very little. | ನೀರು ತುಂಬಾ ತಣ್ಣಗಿದೆ ({value} {unit}). ಮೀನುಗಳಿಗೆ ಒತ್ತಡ ಉಂಟಾಗಿ ರೋಗ ಬರಬಹುದು. ತುಂಬಾ ಕಡಿಮೆ ಆಹಾರ ನೀಡಿ. |  |
| 19 | `risk_messages.REASONS.temperature/high/warning` | Water is warm ({value} {unit}). Oxygen will drop. Run the aerator and add fresh water. | ನೀರು ಬಿಸಿಯಾಗಿದೆ ({value} {unit}). ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗುತ್ತದೆ. ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ ಮತ್ತು ಹೊಸ ನೀರು ಹಾಕಿ. |  |
| 20 | `risk_messages.REASONS.temperature/high/danger` | Water is too hot ({value} {unit}). Fish can die. Add fresh water now, run the aerator and stop feeding. | ನೀರು ತುಂಬಾ ಬಿಸಿಯಾಗಿದೆ ({value} {unit}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ತಕ್ಷಣ ಹೊಸ ನೀರು ಹಾಕಿ, ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ ಮತ್ತು ಆಹಾರ ನಿಲ್ಲಿಸಿ. |  |
| 21 | `risk_messages.REASONS.ammonia/high/warning` | Harmful ammonia is rising ({value} {unit}). Reduce the feed and add fresh water. | ಹಾನಿಕಾರಕ ಅಮೋನಿಯಾ ಹೆಚ್ಚುತ್ತಿದೆ ({value} {unit}). ಆಹಾರ ಕಡಿಮೆ ಮಾಡಿ ಮತ್ತು ಹೊಸ ನೀರು ಹಾಕಿ. |  |
| 22 | `risk_messages.REASONS.ammonia/high/danger` | Harmful ammonia is very high ({value} {unit}). Fish can die. Stop feeding today and add fresh water. | ಹಾನಿಕಾರಕ ಅಮೋನಿಯಾ ತುಂಬಾ ಹೆಚ್ಚಾಗಿದೆ ({value} {unit}). ಮೀನುಗಳು ಸಾಯಬಹುದು. ಇಂದು ಆಹಾರ ನೀಡುವುದನ್ನು ನಿಲ್ಲಿಸಿ ಮತ್ತು ಹೊಸ ನೀರು ಹಾಕಿ. |  |
| 23 | `risk_messages.REASONS.nitrate/high/warning` | Nitrate is high ({value} {unit}). Change some of the water and reduce the feed. | ನೈಟ್ರೇಟ್ ಹೆಚ್ಚಾಗಿದೆ ({value} {unit}). ಸ್ವಲ್ಪ ನೀರು ಬದಲಾಯಿಸಿ ಮತ್ತು ಆಹಾರ ಕಡಿಮೆ ಮಾಡಿ. |  |
| 24 | `risk_messages.ALL_SAFE` | All readings are in the safe range. | ಎಲ್ಲಾ ಅಳತೆಗಳು ಸುರಕ್ಷಿತ ಮಟ್ಟದಲ್ಲಿವೆ. |  |
| 25 | `risk_messages.SENSOR_ERROR` | {name} reading looks wrong ({value}). Check the sensor. | {name} ಅಳತೆ ತಪ್ಪಾಗಿರುವಂತೆ ಕಾಣುತ್ತಿದೆ ({value}). ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ. |  |
| 26 | `risk_messages.TEST_KIT_ERROR` | {name} reading looks impossible ({value}). Check your test kit and test again. | {name} ಅಳತೆ ಅಸಾಧ್ಯವೆಂದು ಕಾಣುತ್ತಿದೆ ({value}). ನಿಮ್ಮ ಟೆಸ್ಟ್ ಕಿಟ್ ಪರಿಶೀಲಿಸಿ ಮತ್ತೆ ಪರೀಕ್ಷಿಸಿ. |  |
| 27 | `risk_messages.AMMONIA_NEEDS_PH_AND_TEMPERATURE` | Ammonia could not be checked because pH or temperature is missing. | pH ಅಥವಾ ತಾಪಮಾನ ಇಲ್ಲದ ಕಾರಣ ಅಮೋನಿಯಾ ಪರಿಶೀಲಿಸಲು ಆಗಲಿಲ್ಲ. |  |
| 28 | `risk_messages.NO_VALID_READINGS` | No valid readings. Check the sensors. | ಸರಿಯಾದ ಅಳತೆಗಳು ಇಲ್ಲ. ಸೆನ್ಸರ್‌ಗಳನ್ನು ಪರಿಶೀಲಿಸಿ. |  |
| 29 | `risk_messages.NO_VALID_TEST_KIT_READINGS` | No valid readings. Check your test kit. | ಸರಿಯಾದ ಅಳತೆಗಳು ಇಲ್ಲ. ನಿಮ್ಮ ಟೆಸ್ಟ್ ಕಿಟ್ ಪರಿಶೀಲಿಸಿ. |  |

## 19. Messages from the server: Time until danger (messages)

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

## 20. Messages from the server: Tonight's weather (messages)

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

## 21. Messages from the server: What to do now (checklist items)

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

## 22. Messages from the server: Alert preview (SMS / WhatsApp)

The SMS and WhatsApp text is built from the risk card and time-until-danger messages above, plus these.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `alerts.POND_NAMES.station1` | Pond 1 | ಕೊಳ 1 |  |
| 2 | `alerts.POND_NAMES.station2` | Pond 2 | ಕೊಳ 2 |  |
| 3 | `alerts.POND_NAMES.station3` | Pond 3 | ಕೊಳ 3 |  |
| 4 | `alerts.APP_NAME` | MeenuRaksha | ಮೀನುರಕ್ಷಾ |  |
| 5 | `alerts.NO_ALERT` | No alert would be sent: the readings are not in Warning or Danger. | ಯಾವುದೇ ಎಚ್ಚರಿಕೆ ಕಳುಹಿಸುವುದಿಲ್ಲ: ಅಳತೆಗಳು ಎಚ್ಚರಿಕೆ ಅಥವಾ ಅಪಾಯದ ಮಟ್ಟದಲ್ಲಿಲ್ಲ. |  |
