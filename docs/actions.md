# Action checklist — what to do in Warning and Danger

When the pond (or a test-kit reading) is in **Warning** or **Danger**, the app shows a short checklist the farmer can tick off. The actions live in [`backend/actions.py`](../backend/actions.py); this page is where each one comes from.

**Rules:**
- Every action comes from a real source, listed below.
- **No chemical treatments and no doses.** Only running the aerator, changing feed, and letting water in or out. Some sources also suggest chemicals, such as lime for low pH [3][5] or a phosphate fertiliser for ammonia [4]. We deliberately leave those out: the right amount depends on the pond, so a fisheries officer should decide.
- Only the problems causing the current level get actions. If oxygen is in Danger and pH is in Warning, the list is for oxygen.
- The ticks are saved only in the farmer's browser, for that alert. A new alert starts a fresh list.

## Actions and sources

| Action id | Action (English) | Based on |
|---|---|---|
| `aerator_now` | Run the aerator now. If you have none, splash the water hard with a paddle or stick. | "The most important thing to do if fish are dying from low DO is to turn on an aerator" [2]. FAO: increase "the mixing of air and water by splashing the water with your hands or with a broad stick or paddle" [1]. "Aeration is a proven technique for improving dissolved oxygen" [3]. |
| `stop_feeding` | Stop feeding until the reading is back to normal. | FAO: reduce fish oxygen demand by "reducing or even stopping their supplementary feed" [1]. For ammonia: "The first thing to do … is to reduce or stop feeding" [4]. |
| `cool_water` | Let in cooler water and drain off the warmest water from the top. | FAO: "increase the inflow of cooler water while … in shallow ponds, discharging the warmest surface water" [1]. |
| `fresh_water` | Let in fresh, clean water and drain some of the stale bottom water. | FAO: "increasing the inflow of well-oxygenated and/or cooler water" and "removing the less oxygenated bottom water … and replacing it with better oxygenated water" [1]. |
| `water_change` | Change a quarter to half of the pond water, only if your new water is clean. | "A 25% to 50% water change will help remove some ammonia, assuming the incoming water source does not contain ammonia" [4]. |
| `aerator_night` | Run the aerator tonight, from late evening until after sunrise. | Aerators "should turn on during the late evening (10pm to midnight) and turn off after daylight (7am–8am)" [2]. "Aeration can also reduce ammonia toxicity" [3]. |
| `reduce_feeding` | Give less feed today. Do not overfeed. | FAO: reduce oxygen use by "avoiding overfeeding" [1]. For ammonia, "reduce or stop feeding" [4]. Use "fertilization and feeding rates that do not result in excessive phytoplankton" to limit pH swings [5]. |
| `no_fertiliser` | Do not add fertiliser or manure for now. | Don't use fertiliser containing nitrogen when ammonia is high, "because nitrogen will add to the problem" [4]. Fertilisation that causes excess algae drives high pH [5]. |
| `watch_fish` | Watch for fish gasping at the surface, especially before sunrise. | Fish short of oxygen "may be seen at the surface 'gasping'" [2]. At night "respiration reduces the DO content until sunrise" [1]. |
| `retest_oxygen_evening` | Test oxygen again late this evening (8–10 pm) to see if it will fall too low at night. | "Measuring DO levels in the late afternoon (5pm–6pm) and late evening (8pm–10pm)" predicts night-time depletion [2]. |
| `retest_ph_morning` | Test pH again early tomorrow morning. pH is highest in the afternoon and falls by morning. | pH is lowest in the early morning and highest in the afternoon; after a high afternoon reading, "in a few hours, the pH will be lower" [5]. |
| `retest_ph_afternoon` | Test pH again this afternoon. pH is lowest in the early morning and rises during the day. | Same daily pH cycle [5]. |

## Which actions for which problem

| Problem | Warning | Danger |
|---|---|---|
| Oxygen low | aerator tonight, less feed, watch fish, re-test oxygen this evening | aerator now, stop feeding, fresh water, watch fish |
| Temperature high | cooler water, re-test oxygen this evening | cooler water, aerator now, watch fish |
| Ammonia high | less feed, no fertiliser, aerator tonight | stop feeding, change ¼–½ of the water, no fertiliser, aerator now |
| pH high | re-test in the morning, no fertiliser, less feed | same as Warning |
| pH low | re-test in the afternoon | same as Warning |
| Nitrate high | less feed, change ¼–½ of the water | (no Danger level) |
| Temperature low | — | — |

**Gaps, on purpose:**
- **pH:** the sources only give chemical fixes for the pH itself (lime, acids, alum). The checklist only covers what is safe without them: re-test at the right time of day and don't feed or fertilise too much. The alert message also tells the farmer to contact their fisheries officer.
- **Cold water:** we found no sourced action, so there is no checklist. The alert message still says to reduce feed.
- **Nitrate:** source [4] is about ammonia. Both come from feed and fish waste, so we apply its feed and water-change advice to nitrate. **This is our judgement.**
- The order of the list (most urgent first) is our judgement.

## Sources

1. FAO. *Management for freshwater fish culture: ponds and water practices*, Ch. 2 "Improving pond water quality" (sections 2.4–2.5). https://www.fao.org/fishery/static/FAO_Training/FAO_Training/General/x6709e/x6709e02.htm
2. Francis-Floyd, R. *Dissolved Oxygen for Fish Production*, FA-27, University of Florida IFAS Extension. https://ask.ifas.ufl.edu/publication/fa002
3. Tamil Nadu Agricultural University (TNAU) Agritech Portal. *Water quality management* (fisheries). https://agritech.tnau.ac.in/fishery/fish_water.html
4. Francis-Floyd, R., Watson, C., Petty, D. & Pouder, D. B. *Ammonia in Aquatic Systems*, FA-16, University of Florida IFAS Extension. https://ask.ifas.ufl.edu/publication/FA031
5. Boyd, C. E. *The inevitable pH fluctuations of aquaculture pond water*, Global Seafood Alliance, Responsible Seafood Advocate, 9 January 2017. https://www.globalseafood.org/advocate/the-inevitable-ph-fluctuations-of-aquaculture-pond-water/
