# Water-quality risk thresholds — Indian major carp ponds

MeenuRaksha grades each sensor reading as **Safe**, **Warning** or **Danger** using published aquaculture limits for Indian major carps (catla, rohu, mrigal). It does not use the dataset labels.

**Overall pond risk = the worst parameter.** If oxygen is Warning but pH is Danger, the pond is Danger, and the alert names pH as the cause.

The numbers live in [`config/thresholds.toml`](../config/thresholds.toml). Change them there; this document should be updated to match.

## Threshold table

| Parameter | 🟢 Safe | 🟡 Warning | 🔴 Danger | Basis |
|---|---|---|---|---|
| **Dissolved oxygen** (mg/L) | ≥ 5 | 3 – 5 | < 3 | **Sourced.** FAO: carp minimum 3 mg/L, preferred ≥ 5 mg/L [1]. FAO: Indian carps need at least 5–6 mg/L [2]. TNAU: optimum 5 mg/L to saturation [4]. |
| **pH** | 6.5 – 8.5 | 5.5 – 6.5 or 8.5 – 9.5 | < 5.5 or > 9.5 | **Safe is sourced:** FAO says 6.5–8.5 is most suitable [1]. **Warning/Danger cut-offs are our judgement:** FAO's lethal limits (< 4.5, ≥ 11) [1] are too late for an early warning. |
| **Temperature** (°C) | 25 – 32 | 20 – 25 or 32 – 35 | < 20 or ≥ 35 | **Safe is sourced:** catla grows best at 25–32 °C [3]. TNAU gives 24–30 °C for warmwater fish [4]. **Danger is our judgement**, set below FAO's 36 °C "dangerous" for carp [1] and above catla's ~14 °C minimum [3]. |
| **Ammonia**, toxic un-ionised NH₃ (mg/L) | < 0.02 | 0.02 – 0.05 | > 0.05 | **Sourced.** TNAU: optimum NH₃ 0.02–0.05 mg/L [4]. Calculated from total ammonia, pH and temperature [7]. |
| **Nitrate** as NO₃-N (mg/L) | < 10 | ≥ 10 | none | **Sourced + judgement.** 10 mg/L NO₃-N can harm fish in long-term exposure [6]. No Danger level, because catla's 24 h lethal level is ~1,480 mg/L [5]. |
| **Turbidity** | — | — | — | **Shown as information only.** Sources give limits in Secchi-disc cm (40–60 cm best) [1][4], but the sensor uses a different unit (probably NTU) that can't be converted. |

Edges: a value exactly on a Safe boundary (e.g. DO = 5.0, pH = 8.5, 32 °C) counts as **Safe**. 35 °C counts as **Danger**.

## Decisions made

| Decision | Choice | Why |
|---|---|---|
| Dataset labels | Not used | Kaggle labels are undocumented. The Mendeley labels come from an unrealistic, synthetic dataset. |
| Turbidity | Information only, not in the overall risk | No sourced limit in the sensor's unit. |
| Ammonia Danger limit | > 0.05 mg/L NH₃ (TNAU) | A catla study [5] found a 24 h LC50 of 0.036–0.045 mg/L NH₃-N. **Cautious alternative: Danger ≥ 0.035**, a one-number change in the config. |
| Impossible readings | Reported as **sensor error**, ignored for risk | The dataset has 0 °C and 0 mg/L DO rows, which are broken sensors, not real ponds. |

## Unit conversions

- **Ammonia:** the sensor measures *total* ammonia. Only the un-ionised part (NH₃) is toxic, and that part grows with pH and temperature. We use the Emerson et al. (1975) equation [7]:
  `pKa = 0.09018 + 2729.92 / (T °C + 273.15)`, `NH₃ = total × 1 / (10^(pKa − pH) + 1)`.
  Example: 1.0 mg/L total ammonia is about 0.002 mg/L NH₃ at pH 6.5 and 27 °C (Safe), but about 0.20 mg/L NH₃ at pH 8.5 and 30 °C (Danger).
- **Nitrate:** the sensor reports nitrate as NO₃ (ppm = mg/L). Thresholds are in NO₃-N: `NO₃-N = NO₃ × 0.2259`.

## Sensor plausibility limits (our judgement)

Readings outside these ranges are treated as sensor faults.

| Parameter | Accepted range |
|---|---|
| Dissolved oxygen | 0.1 – 30 mg/L |
| pH | 2 – 12 |
| Temperature | 5 – 45 °C |
| Total ammonia | 0 – 20 mg/L |
| Nitrate (NO₃) | 0 – 500 mg/L |
| Turbidity | 0 – 1000 |

## Open question

Dissolved oxygen readings go up to 25 mg/L, far above saturation (about 8 mg/L at 28 °C). Supersaturation can cause gas-bubble disease, but we haven't found a sourced limit yet, so high DO is not flagged.

## Sources

1. FAO. *Management for freshwater fish culture: ponds and water practices*, Ch. 2 "Improving pond water quality". https://www.fao.org/fishery/static/FAO_Training/FAO_Training/General/x6709e/x6709e02.htm
2. FAO. *Selected aspects of warmwater fish culture*, Ch. 9 "Culture of the Indian major carps". https://www.fao.org/4/t8389e/T8389E09.htm
3. FAO. Cultured Aquatic Species Information Programme — *Catla catla*. https://www.fao.org/fishery/docs/DOCUMENT/aquaculture/CulturedSpecies/file/en/en_catla.htm
4. Tamil Nadu Agricultural University (TNAU) Agritech Portal. *Water quality management* (fisheries). https://agritech.tnau.ac.in/fishery/fish_water.html
5. Tilak K.S., Lakshmi S.J., Susan T.A. (2002). The toxicity of ammonia, nitrite and nitrate to the fish, *Catla catla* (Hamilton). *Journal of Environmental Biology* 23(2):147–149. PMID 12602850. https://pubmed.ncbi.nlm.nih.gov/12602850/
6. Camargo J.A., Alonso A., Salamanca A. (2005). Nitrate toxicity to aquatic animals: a review with new data for freshwater invertebrates. *Chemosphere* 58(9):1255–1267. https://doi.org/10.1016/j.chemosphere.2004.10.044
7. Emerson K., Russo R.C., Lund R.E., Thurston R.V. (1975). Aqueous ammonia equilibrium calculations: effect of pH and temperature. *Journal of the Fisheries Research Board of Canada* 32:2379–2383.
