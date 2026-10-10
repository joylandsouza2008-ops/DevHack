# Data sources

AquaNexus has **no real sensors**. Instead it uses the open datasets, public API and published guides below.
The app shows the same list (shorter) under **Data sources / ಡೇಟಾ ಮೂಲಗಳು** in the footer.

Licences were checked on each source's own page on 9 October 2026.

## Datasets and API

| Source | Link | What we use it for | Licence |
|---|---|---|---|
| **Pondsdata** (Kaggle, uploaded by apgopi) | https://www.kaggle.com/datasets/apgopi/pondsdata | Real sensor readings from 3 fish ponds in Guntur, Andhra Pradesh (Feb 2022 – Jan 2023, about every 20 min). The simulator (`backend/simulator.py`) builds its **simulated** demo pond from them; without the file (fresh clone, online demo) it uses fixed typical levels instead. Also used to train and test the DO forecast and to check "time until danger". Its `label` column is **not** used (undocumented). | **Unknown.** Kaggle lists the licence as "Unknown" and the uploader gives no terms. We use it for this non-commercial hackathon project only, don't redistribute it (it is not in git), and would ask the uploader before any wider use. |
| **Aquaculture – Water Quality Dataset** (Mendeley Data, Veeramsetty, Arabelli & Bernatin) | https://data.mendeley.com/datasets/y78ty2g293/2 (DOI 10.17632/y78ty2g293.2) | **Checked, not used by the app or any model.** It looks synthetic: some values are physically impossible (water up to 84 °C, pH 0–14), so its readings and labels can't be trusted for real ponds. See [thresholds.md](thresholds.md#decisions-made). | **CC BY 4.0** (credit the authors) |
| **Open-Meteo weather forecast API** | https://open-meteo.com/en/docs | Tonight's real forecast for Mangaluru (cloud cover, night wind, night temperature) for the night oxygen-crash warning ([night_crash.md](night_crash.md)). Real, not simulated, and never used to train a model. | Data **CC BY 4.0**. The free API is for **non-commercial use only** ([terms](https://open-meteo.com/en/terms)); a commercial version would need a paid plan. Credited in the app ("Forecast: Open-Meteo"). |
| **Freshwater Fish Disease Aquaculture in South Asia** (Kaggle, Biswas et al.) | https://www.kaggle.com/datasets/subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia | **Research only, not in the app.** Fish disease photos for the image experiments ([fish-disease-cleaning.md](fish-disease-cleaning.md), [fish-disease-baseline.md](fish-disease-baseline.md)). | **CC0** (public domain) |

Simulated readings are labelled "Simulated data" / "ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಡೇಟಾ" wherever the app shows them, and are never used to train a model or report accuracy.

## Threshold and action sources

The Safe / Warning / Danger limits ([thresholds.md](thresholds.md)), the night oxygen-crash rules ([night_crash.md](night_crash.md)) and the "What to do now" checklist ([actions.md](actions.md)) come from these published guides and papers. We only take facts (numbers) and short quotes from them, with a citation; nothing is copied into the app wholesale. Each stays under its publisher's copyright.

| Source | Link | What we use it for |
|---|---|---|
| FAO, *Management for freshwater fish culture: ponds and water practices*, Ch. 2 | https://www.fao.org/fishery/static/FAO_Training/FAO_Training/General/x6709e/x6709e02.htm | DO, pH, temperature and turbidity limits; aerator, feed and water actions; crash causes |
| FAO, *Selected aspects of warmwater fish culture*, Ch. 9 (Indian major carps) | https://www.fao.org/4/t8389e/T8389E09.htm | DO needs of Indian carps |
| FAO, Cultured Aquatic Species Information Programme, *Catla catla* | https://www.fao.org/fishery/docs/DOCUMENT/aquaculture/CulturedSpecies/file/en/en_catla.htm | Catla temperature range |
| TNAU Agritech Portal, *Water quality management* (fisheries) | https://agritech.tnau.ac.in/fishery/fish_water.html | DO, temperature and ammonia limits; actions |
| Francis-Floyd, *Dissolved Oxygen for Fish Production* (FA-27), UF/IFAS Extension | https://ask.ifas.ufl.edu/publication/fa002 | Aerator and feed actions; crash causes |
| Francis-Floyd et al., *Ammonia in Aquatic Systems* (FA-16), UF/IFAS Extension | https://ask.ifas.ufl.edu/publication/FA031 | Ammonia actions (feed, water change) |
| Boyd, *The inevitable pH fluctuations of aquaculture pond water*, Global Seafood Alliance (2017) | https://www.globalseafood.org/advocate/the-inevitable-ph-fluctuations-of-aquaculture-pond-water/ | pH re-testing advice |
| Burtle, *Oxygen Depletion in Ponds* (C1048), University of Georgia Extension | https://fieldreport.caes.uga.edu/publications/C1048/ | Night crash weather conditions |
| UK Met Office, *Beaufort wind force scale* | https://weather.metoffice.gov.uk/guides/coast-and-sea/beaufort-scale | "Calm night" wind cut-off |
| Tilak, Lakshmi & Susan (2002), *J. Environ. Biol.* 23(2):147–149 | https://pubmed.ncbi.nlm.nih.gov/12602850/ | Catla ammonia and nitrate toxicity |
| Camargo, Alonso & Salamanca (2005), *Chemosphere* 58(9):1255–1267 | https://doi.org/10.1016/j.chemosphere.2004.10.044 | Nitrate limit |
| Emerson, Russo, Lund & Thurston (1975), *J. Fish. Res. Board Can.* 32:2379–2383 | (journal article, no free link) | Formula for toxic NH₃ from total ammonia, pH and temperature |
| FAO/NACA *Asia Diagnostic Guide to Aquatic Animal Diseases* (2001); NACA carp-disease chapters (1985, 1989) in FAO's document repository; 5 peer-reviewed papers | Full list: [diseases.md](diseases.md#references) | Fish disease guide: signs, seasons, prevention, links to risky readings |
