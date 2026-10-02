# Tonight's oxygen crash risk — weather rules

The bottom toolbar of the dashboard shows **Tonight's weather** for Mangaluru with an **oxygen crash risk** of **Low**, **Medium** or **High**. It is worked out from the free [Open-Meteo](https://open-meteo.com/) forecast (no API key) by `backend/weather.py`, and served at `GET /api/weather/tonight`.

This is **real forecast data, not simulated data**. It is not a pond reading and it is never used to train or test a model. It only rates how much the *weather* favours a night-time oxygen crash.

The numbers live in [`config/thresholds.toml`](../config/thresholds.toml) under `[night_crash]`. Change them there; this document should be updated to match.

## Why the weather matters

At night algae make no oxygen, but fish, algae and bacteria keep using it, so dissolved oxygen falls until sunrise [1][2]. The weather decides how low it gets:

| Risk factor | What we check | Cut-off | Why it matters | Basis |
|---|---|---|---|---|
| **Cloudy day** | Mean cloud cover, 06:00–18:00 the day before tonight | ≥ 75 % | Less sunlight means algae make less oxygen in the day, so the pond starts the night with less. | **Cause sourced:** "Oxygen production decreases during cloudy days" [1]; "during cloudy weather … a marked decrease in oxygen production from photosynthesis" [2]. **The 75 % cut-off is our judgement.** |
| **Still night** | Mean wind speed at 10 m, 18:00–06:00 | < 7 km/h | Wind and waves push air into the water. With no wind, little oxygen gets in from the air. | **Cause sourced:** oxygen transfer from the air "is minimal because there is little or no wind/wave action" [2]; wind action improves mixing [1]. **The 7 km/h cut-off is our judgement**, anchored to the Beaufort scale: below 7 km/h (4 knots) is "light air" or calm; "light breeze" starts at 4 knots [4]. Wind at the pond surface is lower than at 10 m. |
| **Warm night** | Mean air temperature, 18:00–06:00 | ≥ 28 °C | Warm water holds less oxygen, and fish and bacteria breathe faster. | **Cause sourced:** "The warmer the water, the less dissolved oxygen it can hold" [1]; warm water "is much less capable of holding oxygen" [2]; "most oxygen depletions occur in warm weather and usually follow a period of cloudy, overcast conditions" [3]. **The 28 °C cut-off is our judgement:** typical Mangaluru nights are about 24–27 °C. |

## How the level is chosen

Count the factors that are met:

| Factors | Level | Message (English) | Message (Kannada) |
|---|---|---|---|
| 0 | 🟢 **Low** | Weather looks fine tonight: low risk of an oxygen crash. | ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ ಸರಿಯಾಗಿದೆ: ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯ ಕಡಿಮೆ. |
| 1 | 🟡 **Medium** | *Still* night ahead: check the pond late at night and before dawn. | *ಗಾಳಿಯಿಲ್ಲದ* ರಾತ್ರಿ ಬರಲಿದೆ: ತಡರಾತ್ರಿ ಮತ್ತು ಬೆಳಗಾಗುವ ಮೊದಲು ಕೊಳವನ್ನು ನೋಡಿ. |
| 2 or 3 | 🔴 **High** | *Cloudy, still* night ahead: keep the aerator ready. | *ಮೋಡ ಕವಿದ, ಗಾಳಿಯಿಲ್ಲದ* ರಾತ್ರಿ ಬರಲಿದೆ: ಏರೇಟರ್ ಸಿದ್ಧವಾಗಿಡಿ. |

The words in *italics* change with the factors (cloudy / still / warm). Equal weights and the "count the factors" rule are **our judgement**: the sources say these conditions make a crash more likely, especially together [2][3], but give no formula. The advice to have the aerator ready follows [3], which says pond owners should plan aeration "before oxygen depletions occur", and [2], which recommends emergency aeration when oxygen drops below 4 mg/L.

The level uses the same colour + icon pairs as the pond status (green / amber / red), always with the word.

## "Tonight" and offline use

- **Tonight** is 18:00 to 06:00 (Asia/Kolkata). Before 06:00, it is the night we are already in.
- The server saves each forecast to `data/weather_cache.json` and re-downloads at most every 30 minutes.
- **No internet:** the saved forecast is used and the toolbar says *"Offline: showing the forecast saved on …"*. The forecast covers three days, so a saved copy still works the next night. If nothing usable is saved, the toolbar says the weather is not known.
- The download gives up after 8 seconds and runs off the main loop, so the rest of the app (simulator, alerts, chart) works the same with or without internet.

## Limits

- One location (Mangaluru). Ponds far inland may have different weather.
- Air temperature, not pond water temperature.
- This is a weather warning, not a measurement. A pond with few algae and few fish may be fine on a High night; a heavily stocked pond can crash on a Low night. The pond's own oxygen readings always come first.

## Sources

1. FAO. *Management for freshwater fish culture: ponds and water practices*, Ch. 2 "Improving pond water quality". https://www.fao.org/fishery/static/FAO_Training/FAO_Training/General/x6709e/x6709e02.htm
2. Francis-Floyd, R. *Dissolved Oxygen for Fish Production*, Fact Sheet FA-27, University of Florida IFAS Extension. https://ask.ifas.ufl.edu/publication/fa002
3. Burtle, G. J. *Oxygen Depletion in Ponds*, Circular 1048, University of Georgia Cooperative Extension. https://fieldreport.caes.uga.edu/publications/C1048/
4. UK Met Office. *Beaufort wind force scale*. https://weather.metoffice.gov.uk/guides/coast-and-sea/beaufort-scale
5. Open-Meteo weather forecast API (data CC BY 4.0). https://open-meteo.com/en/docs
