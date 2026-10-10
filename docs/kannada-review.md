# Kannada text review

Every Kannada string in MeenuRaksha, next to its English version, grouped by screen.
Please check each Kannada line is correct, natural and easy for a small fish farmer in
coastal Karnataka to understand. Write any fix in the last column.

- Words in `{curly brackets}` are filled in by the app (numbers, times, names). Please keep them.
- `A  /  B` means the app shows one of two versions, depending on the situation.
- Unit symbols (mg/L, °C, km/h, pH) and the names SMS, WhatsApp, FAO, TNAU, Open-Meteo stay in English.

321 strings. Generated from the code by `python tools/kannada_review.py`; re-run it after changing any text.

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

## 14. Voice alert

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `app.js voiceListen` | Listen to alert | ಎಚ್ಚರಿಕೆ ಕೇಳಿ |  |
| 2 | `app.js voiceStop` | Stop | ನಿಲ್ಲಿಸಿ |  |
| 3 | `app.js voiceNoKannada` | Sorry, this phone has no Kannada voice, so the alert cannot be read aloud in Kannada. Please read the alert on the screen, or switch to English to hear it. | ಕ್ಷಮಿಸಿ, ಈ ಫೋನ್‌ನಲ್ಲಿ ಕನ್ನಡ ಧ್ವನಿ ಇಲ್ಲ, ಆದ್ದರಿಂದ ಎಚ್ಚರಿಕೆಯನ್ನು ಕನ್ನಡದಲ್ಲಿ ಓದಿ ಹೇಳಲು ಆಗುವುದಿಲ್ಲ. ದಯವಿಟ್ಟು ಪರದೆಯ ಮೇಲಿನ ಎಚ್ಚರಿಕೆಯನ್ನು ಓದಿ, ಅಥವಾ ಕೇಳಲು English ಆಯ್ಕೆಮಾಡಿ. |  |
| 4 | `app.js voiceNoEnglish` | Sorry, this phone has no English voice. Please read the alert on the screen. | ಕ್ಷಮಿಸಿ, ಈ ಫೋನ್‌ನಲ್ಲಿ ಇಂಗ್ಲಿಷ್ ಧ್ವನಿ ಇಲ್ಲ. ದಯವಿಟ್ಟು ಪರದೆಯ ಮೇಲಿನ ಎಚ್ಚರಿಕೆಯನ್ನು ಓದಿ. |  |
| 5 | `app.js voiceUnsupported` | Sorry, this browser cannot read aloud. Please read the alert on the screen. | ಕ್ಷಮಿಸಿ, ಈ ಬ್ರೌಸರ್ ಓದಿ ಹೇಳಲು ಆಗುವುದಿಲ್ಲ. ದಯವಿಟ್ಟು ಪರದೆಯ ಮೇಲಿನ ಎಚ್ಚರಿಕೆಯನ್ನು ಓದಿ. |  |

## 15. Alert history

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

## 16. Data sources panel (footer)

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

## 17. Messages from the server: Data labels

Shown on every simulated, test-kit or live-sensor reading.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `simulator.SIMULATED_LABEL` | Simulated data | ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಡೇಟಾ |  |
| 2 | `main.MANUAL_LABEL` | Manual test-kit reading | ಕೈಯಿಂದ ನಮೂದಿಸಿದ ಟೆಸ್ಟ್ ಕಿಟ್ ಅಳತೆ |  |
| 3 | `sensor.LIVE_LABEL` | Live sensor | ಲೈವ್ ಸೆನ್ಸರ್ |  |
| 4 | `sensor.DEMO_LABEL` | Demo device: simulated readings, not a real pond | ಡೆಮೊ ಸಾಧನ: ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಅಳತೆಗಳು, ನಿಜವಾದ ಕೊಳವಲ್ಲ |  |

## 18. Messages from the server: Live sensor: why a reading was refused

Sent back to the sensor and shown on the Live sensor card.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `sensor.REJECTED` | Reading rejected. Check the sensor. | ಅಳತೆಯನ್ನು ತಿರಸ್ಕರಿಸಲಾಗಿದೆ. ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ. |  |
| 2 | `sensor.NO_VALUES` | The reading has no values. Check the sensor. | ಅಳತೆಯಲ್ಲಿ ಯಾವುದೇ ಮೌಲ್ಯಗಳಿಲ್ಲ. ಸೆನ್ಸರ್ ಪರಿಶೀಲಿಸಿ. |  |
| 3 | `sensor.WRONG_KEY` | Missing or wrong sensor key. | ಸೆನ್ಸರ್ ಕೀ ಇಲ್ಲ ಅಥವಾ ತಪ್ಪಾಗಿದೆ. |  |
| 4 | `sensor.CLOCK_AHEAD` | The sensor's clock is ahead of the real time. Check the sensor clock. | ಸೆನ್ಸರ್‌ನ ಗಡಿಯಾರ ನಿಜವಾದ ಸಮಯಕ್ಕಿಂತ ಮುಂದಿದೆ. ಸೆನ್ಸರ್ ಗಡಿಯಾರ ಪರಿಶೀಲಿಸಿ. |  |
| 5 | `sensor.NO_TIME_ZONE` | The timestamp has no time zone. Add +05:30 or Z. Check the sensor clock. | ಸಮಯದಲ್ಲಿ ಟೈಮ್ ಝೋನ್ ಇಲ್ಲ. +05:30 ಅಥವಾ Z ಸೇರಿಸಿ. ಸೆನ್ಸರ್ ಗಡಿಯಾರ ಪರಿಶೀಲಿಸಿ. |  |
| 6 | `sensor.TOO_OLD` | The timestamp is more than a day old. Check the sensor clock. | ಸಮಯ ಒಂದು ದಿನಕ್ಕಿಂತ ಹಳೆಯದು. ಸೆನ್ಸರ್ ಗಡಿಯಾರ ಪರಿಶೀಲಿಸಿ. |  |

## 19. Messages from the server: Risk card: level names, parameter names and reasons

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

## 20. Messages from the server: Time until danger (messages)

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

## 21. Messages from the server: Tonight's weather (messages)

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

## 22. Messages from the server: What to do now (checklist items)

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

## 23. Messages from the server: Fish disease guide: diseases

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

## 24. Messages from the server: Fish disease guide: symptom checker and notes

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

## 25. Messages from the server: Fish disease guide: risky readings

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

## 26. Messages from the server: Alert preview (SMS / WhatsApp)

The SMS and WhatsApp text is built from the risk card and time-until-danger messages above, plus these.

| # | Where in the code | English | Kannada | Correct? / suggestion |
|---|---|---|---|---|
| 1 | `alerts.POND_NAMES.station1` | Pond 1 | ಕೊಳ 1 |  |
| 2 | `alerts.POND_NAMES.station2` | Pond 2 | ಕೊಳ 2 |  |
| 3 | `alerts.POND_NAMES.station3` | Pond 3 | ಕೊಳ 3 |  |
| 4 | `alerts.APP_NAME` | MeenuRaksha | ಮೀನುರಕ್ಷಾ |  |
| 5 | `alerts.NO_ALERT` | No alert would be sent: the readings are not in Warning or Danger. | ಯಾವುದೇ ಎಚ್ಚರಿಕೆ ಕಳುಹಿಸುವುದಿಲ್ಲ: ಅಳತೆಗಳು ಎಚ್ಚರಿಕೆ ಅಥವಾ ಅಪಾಯದ ಮಟ್ಟದಲ್ಲಿಲ್ಲ. |  |
