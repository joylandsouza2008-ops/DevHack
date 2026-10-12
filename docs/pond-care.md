# Pond care basics ("Ask AquaNexus")

Everyday pond questions, such as *"When should I clean the pond?"* or *"How much should I feed?"*, get a short answer
in plain words, in English and Kannada. Before this, the assistant said "I don't know" to them.

| | |
|---|---|
| Code | `backend/pond_care.py` (topics, the words that point to each, ready answers) |
| Used by | `backend/assistant.py`: added to the AI's content; a **ready answer** when there is no AI key, the AI is down, the rate limit is reached or the AI replies `UNKNOWN` |
| Suggested question | **When should I clean my pond?** / ನನ್ನ ಕೊಳವನ್ನು ಯಾವಾಗ ಸ್ವಚ್ಛಗೊಳಿಸಬೇಕು? |
| Tests | `tests/test_assistant.py`, section "pond care basics" |

## Rules

- **No chemical names, liming, medicines or amounts.** Every answer ends with *"For liming, chemicals, medicines or
  amounts of anything, ask your fisheries officer or KVK."* Questions that ask for a chemical or medicine are still
  refused before they reach the AI (`backend/safety.py`).
- **No numbers.** Sources give feed rates and stocking numbers, but these depend on the fish, the pond and the
  hatchery, so the app sends the farmer to the fisheries officer, KVK or hatchery instead. The tests check that no
  digit, unit, lime, fertiliser or salt appears in any pond care answer.

## Similar words it understands

| Topic | Words (English, Kannada, Kannada typed in English letters) |
|---|---|
| Changing water | change / exchange / replace / add / fresh … water, water change, *neeru badal…*, ನೀರು … ಬದಲ…, ಹೊಸ ನೀರು |
| Cleaning | clean, wash, scrub, sludge, silt, drain, desilt, *swachha*, ಸ್ವಚ್ಛ, ಶುಚಿ, ತೊಳೆ, ಕೆಸರು, ಹೂಳು |
| Feeding | feed, food, *aahara*, ಆಹಾರ, ಮೇವು |
| Aerators | aerator, aeration, paddle wheel, ಏರೇಟರ್ |
| How many fish | stock, how many fish, overcrowd, fingerlings, density, ಎಷ್ಟು ಮೀನು, ಮೀನು ಮರಿ |
| Daily and weekly checks | daily, weekly, every day, routine, what should I check, ಪ್ರತಿದಿನ, ವಾರಕ್ಕೊಮ್ಮೆ |

**Pond, tank, kere (ಕೆರೆ), ಕೊಳ** all get the same answers. A question that names a **tank** (ಟ್ಯಾಂಕ್, ತೊಟ್ಟಿ) gets the
tank step first in the cleaning answer.

"ಆಹಾರ ಎಷ್ಟು ಹಾಕಬೇಕು?" (*how much feed to put in?*) is a feeding question, not a dose question: `safety.py` no longer
refuses "ಎಷ್ಟು ಹಾಕ" when the question is about feed and has no other medicine or chemical word.

## What it says, and where it comes from

| Answer (English) | Source |
|---|---|
| **Cleaning.** While fish are growing, don't fully drain or scrub the pond. | During a crop the advice is partial measures: "addition of clean water, bottom raking" [1, ch. 9]; drain only "some of the surface water and replace it with fresh water" [2]. Full draining, sludge removal and drying come after the harvest [1, ch. 5][3]. |
| Every day, take out leftover feed and dead fish. | "The feeding tray should be cleaned daily before the application of fresh feed" [1, ch. 9]; "unconsumed food is decaying on the bottom" and uses oxygen [2]; dead fish spread disease [4] (same step as the Fish disease guide). |
| Between crops: drain, remove the black sludge, sun-dry the bottom until it cracks, then refill. | "After complete dewatering, the pond bed is allowed to dry and develop cracks in the silt mass … dried silt is cut and removed" [1, ch. 5]; "Removal of bottom sludge should preferably be undertaken after every harvest" [3]. |
| In a tank: change part of the water and clean the bottom while the fish stay in. | A siphon that removes bottom waste during partial water changes [5]. **Our judgement:** we found no farmer guide for fish tanks in India, so this step is general practice, kept in plain words. |
| **Changing water.** Change part of the water when it smells bad, is very green or oxygen is low. Let some out and fill in clean water. | Low oxygen: "increasing the inflow of well-oxygenated … water"; a smell of "rotten egg rising from the water"; too much plankton: "drain off some of the surface water and replace it with fresh water" [2]. "Add freshwater in the pond" when oxygen is short [1, ch. 10]. "Frequent exchange of water can prevent building up of hydrogen sulphide" [6]. |
| **Feeding.** Feed at the same set times every day. | Feed "daily in the morning hours" [1, ch. 9]; twice a day [7]. |
| Give less feed on cloudy or very hot days. Stop if the fish don't eat or oxygen is low. | "avoiding overfeeding"; "reducing or even stopping their supplementary feed" when oxygen is low [2]; "Stop feeding … till normality is restored" [1, ch. 10]; "Fish normally stop feeding if they are sick" [1, ch. 9]. **Less feed on cloudy or hot days is our judgement** from these: cloudy and warm weather lower oxygen (see `docs/night_crash.md`), and less feed means less oxygen used [2]. |
| If feed is left over, give less next time. | Uneaten feed decays and uses oxygen [2]; avoid overfeeding [2]. |
| **Aerators.** Run them at night and before dawn, most of all after a cloudy, warm, still day. | Oxygen is lowest "during the last part of the night"; act "about two hours before sunrise" [2]; low oxygen "especially during the early morning hours", remedy: "a mechanical churner/aerator" [1, ch. 10]; cloudy, warm, still weather: `docs/night_crash.md`. |
| **Daily and weekly checks.** Watch the fish at dawn; look at the water colour and smell; test kit weekly. | "A single measurement just before sunrise"; fish "surfacing for gulping air"; "Daily observation of fish in each pond"; "The visual colour of the pond water is a simple but important reflection" [1, ch. 9]; rotten-egg smell [2]. **Weekly test kit: our judgement** (the sources say "routine" monitoring [1, ch. 9]). |
| **How many fish.** Don't overcrowd; follow your hatchery or fisheries officer for numbers. | "Overstocking may lead to biological crowding resulting in waste build up"; "follow the recommended stocking density" [1, ch. 9]; "Under crowded conditions fish … suffer stress" [8]. |
| Liming, chemicals, medicines, amounts → fisheries officer or KVK. | App rule (`CLAUDE.md`, `docs/diseases.md`). Liming and pond disinfection appear in the sources [8]; we leave them to the officer. |

## Sources (read on 12 October 2026)

1. Kumar, D. (1992). *Fish culture in undrainable ponds: a manual for extension.* FAO Fisheries Technical Paper 325.
   FAO, Rome. Ch. 5 "Renovation of existing ponds" https://www.fao.org/4/t0555e/T0555E05.htm · Ch. 9 "Pond
   management" https://www.fao.org/4/t0555e/T0555E09.htm · Ch. 10 "Management of common hazards"
   https://www.fao.org/4/t0555e/T0555E10.htm
2. FAO. *Management for freshwater fish culture: ponds and water practices*, Ch. 2 "Improving pond water quality".
   https://www.fao.org/fishery/static/FAO_Training/FAO_Training/General/x6709e/x6709e02.htm
3. Tamil Nadu Agricultural University (TNAU) Agritech Portal, Fisheries. *Catfish: pond preparation.*
   https://agritech.tnau.ac.in/fishery/fish_cul_freshwater_catfish_pond.html
4. Li Shaoqi (1989). Main fish diseases and their control. In *Integrated Fish Farming in China*, ch. 6. NACA
   Technical Manual 7. https://www.fao.org/4/ac264e/ac264e07.htm (cited for the same step in `docs/diseases.md`).
5. ICAR-Central Institute of Fisheries Education (ICAR-CIFE). *Power operated solid waste removal device from
   aquaria.* https://www.cife.edu.in/ITMU/tech-all-pdf/18_POWER%20OPERATED%20SOLID%20WASTE%20REMOVAL%20DEVICE%20FROM%20AQUARIA.pdf
6. TNAU Agritech Portal, Fisheries. *Water quality management.* https://agritech.tnau.ac.in/fishery/fish_water.html
7. Vikaspedia (Government of India). *Carp culture in ponds.*
   https://en.vikaspedia.in/viewcontent/agriculture/fisheries/fish-production/culture-fisheries/culture-techniques-of-fishes/carp-culture-in-ponds?lgn=en
8. Freshwater Aquaculture Research and Training Centre, Dhauli (CIFRI; the centre became **ICAR-CIFA** in 1987)
   (1985). *Lecture Notes on Composite Fish Culture and its Extension in India*, ch. 1. NACA/TR/85/15.
   https://www.fao.org/4/ac229e/AC229E01.htm

**Not reached:** ICAR-CIFA's own website (cifa.nic.in) refused the connection on 12 October 2026, so its current
farmer leaflets could not be checked. The CIFA material used here is the 1985 lecture notes from the same centre [8].
**Ask a fisheries officer to check these answers before release.** The Kannada is in `docs/kannada-review.md` for a
native speaker to review.
