# Fish disease guide: sources

The **Fish disease guide** in the app covers nine diseases common in Indian carp ponds. It has:

- a **library**: name in English and Kannada, cause type, signs on the body and in behaviour, when it is most
  common, prevention, and what to do;
- a **symptom checker**: the farmer ticks the signs they see and gets up to three **possible matches**, never a
  diagnosis. Every result ends with "Confirm with your fisheries officer";
- a **link to the readings**: when a reading is in Warning or Danger (e.g. low oxygen), the app notes which diseases
  become more likely, and why.

The data lives in [`backend/diseases.py`](../backend/diseases.py); the page is in `frontend/diseases.js`.
This page lists where every statement comes from. Tests (`tests/test_diseases.py`) check that every disease
has a section here naming each of its sources.

## Rules

- **Only real sources:** FAO, NACA technical documents published in FAO's document repository (one written by
  the ICAR centre that became ICAR-CIFA), and peer-reviewed papers. Every source below was read by us at the link
  given, except where the table says "abstract only".
- **No chemical treatments, medicines or doses.** Several sources give drug and chemical doses (formalin,
  malachite green, organophosphates, antibiotics, salt baths, pond chemicals). We leave all of them out. The
  app says: *"No medicines or chemicals here. Any treatment must be prescribed by a fisheries officer or KVK."*
  The one chemical word left is FAO's advice to **dry and lime the pond before stocking**, which the app gives as
  "ask your fisheries officer about liming", with no amount.
- **Possible matches, not a diagnosis.** Many fish diseases look alike (FAO says other diseases can cause
  EUS-like ulcers [fao2001]). Only a laboratory can confirm most of them.
- **Simplified wording.** The app's sentences are short paraphrases of the sources for farmers. The tables below
  quote or closely paraphrase the source text each sentence is based on.
- **Illustrations** are simple original drawings (`frontend/diseases.js`), not copied photos. The marks on the
  fish (sores, spots, lice) are drawn in the magenta accent, not in the Safe/Warning/Danger colours, which are
  reserved for pond status (DESIGN.md).

## References

| Key | Reference | Read |
|---|---|---|
| [fao2001] | Bondad-Reantaso, M.G., McGladdery, S.E., East, I. & Subasinghe, R.P. (eds) (2001). *Asia Diagnostic Guide to Aquatic Animal Diseases*. FAO Fisheries Technical Paper 402/2. FAO and NACA, Rome. Section F.11 Epizootic Ulcerative Syndrome. https://www.fao.org/4/y1679e/y1679e00.htm | Full chapter F.11 |
| [naca1985] | Freshwater Aquaculture Research and Training Centre, Dhauli (CIFRI; the centre became ICAR-CIFA in 1987) (1985). Diseases and health care in composite fish culture. In: *Lecture Notes on Composite Fish Culture and its Extension in India*, chapter 12. NACA/TR/85/15, NACA, Bangkok. https://www.fao.org/4/ac229e/AC229E12.htm | Full chapter |
| [naca1989] | Li Shaoqi (1989). Main fish diseases and their control. In: *Integrated Fish Farming in China*, chapter 6. NACA Technical Manual 7, NACA, Bangkok. https://www.fao.org/4/ac264e/ac264e07.htm | Full chapter |
| [declercq2013] | Declercq, A.M., Haesebrouck, F., Van den Broeck, W., Bossier, P. & Decostere, A. (2013). Columnaris disease in fish: a review with emphasis on bacterium-host interactions. *Veterinary Research* 44: 27. https://doi.org/10.1186/1297-9716-44-27 | Full text (signs, environmental factors) |
| [semwal2023] | Semwal, A., Kumar, A. & Kumar, N. (2023). A review on pathogenicity of *Aeromonas hydrophila* and their mitigation through medicinal herbs in aquaculture. *Heliyon* 9(3): e14088. https://doi.org/10.1016/j.heliyon.2023.e14088 | Full text (signs, stress factors) |
| [patra2016] | Patra, A., Mondal, A., Banerjee, S., Adikesavalu, H., Joardar, S.N. & Abraham, T. (2016). Molecular characterization of *Argulus bengalensis* and *Argulus siamensis* (Crustacea: Argulidae) infecting the cultured carps in West Bengal, India using 18S rRNA gene sequences. *Molecular Biology Research Communications* 5(3): 156–166. https://doi.org/10.22099/mbrc.2016.3752 | Abstract and article page |
| [flagg1978] | Flagg, R.M. & Hinck, L.W. (1978). Influence of ammonia on aeromonad susceptibility in channel catfish. *Proceedings of the Annual Conference of the Southeastern Association of Fish and Wildlife Agencies*, pp. 415–419. https://seafwa.org/journal/1978/influence-ammonia-aeromonad-susceptibility-channel-catfish | **Abstract only** (the PDF is a scan) |
| [snieszko1974] | Snieszko, S.F. (1974). The effects of environmental stress on outbreaks of infectious diseases of fishes. *Journal of Fish Biology* 6(2): 197–208. https://doi.org/10.1111/j.1095-8649.1974.tb04537.x | **Abstract only** |

**Sources we looked for but could not use:**

- **TNAU Agritech** and **ICAR** pages (`agritech.tnau.ac.in`, `krishi.icar.gov.in`, `epubs.icar.org.in`) could not be
  reached from our tools, so we could not read them. Several Indian surveys there look useful (EUS worst in winter
  in Assam; argulosis and dropsy as main problems in Andhra Pradesh and West Bengal). They are not cited because we
  have not read them.
- **NFDB:** we found no NFDB disease-guideline document online.
- [naca1989] is from China. We use it for signs, water temperatures and seasons of the same pathogens; the months it
  gives are for China and are not used.

A fisheries scientist should check this page before the guide is used with farmers.

## The diseases

<a id="eus"></a>
### Epizootic ulcerative syndrome (EUS, red spot disease)

| In the app | Source |
|---|---|
| Cause: water mould *Aphanomyces invadans* (an oomycete, fungus-like) | "caused by the Oomycete fungus *Aphanomyces invadans* … also known as Red spot disease" [fao2001] |
| Starts as red spots; becomes deep sores into the muscle; older sores can have a raised white edge | "Initial lesions may appear as red spots, which become deeper as the infection progresses and penetrate underlying musculature. Some advanced lesions may have a raised whitish border." [fao2001] |
| Many fish can die | "High mortalities are usually associated with EUS outbreaks" [fao2001] |
| Cool weather, acidic runoff | outbreaks "associated with acidified water (due to acid sulfate soil runoff), along with low temperatures" [fao2001] |
| Spreads with floods and when fish are moved | "The spread of EUS is thought to be due to flooding and movement of affected and/or carrier fish." [fao2001] |
| Chinese carps resist it | "some important culture species including tilapia, milkfish and Chinese carps have been shown to be resistant" [fao2001] |
| Prevention: dry (and lime) the pond, keep wild fish out, hatchery-reared seed, clean nets and tools | "drying and liming of ponds prior to stocking; exclusion of wild fish; use of … hatchery-reared fry; … disinfection of contaminated nets and equipment" [fao2001]. We leave out FAO's salt baths and treated fry (treatments). |
| Ulcers can come from other diseases; a lab test is needed | "other diseases may also result in similar clinical lesions … it is, therefore, important to confirm the presence of *A. invadans*" [fao2001] |
| Behaviour signs | Not described in [fao2001]; the app only says many fish can die. |

<a id="aeromoniasis"></a>
### Aeromonas infection (dropsy, haemorrhagic septicaemia)

| In the app | Source |
|---|---|
| Cause: bacteria, *Aeromonas hydrophila* and related | "Dropsy condition among Indian major carps is a common bacterial disease. The etiological agent is a species of *Aeromonas*"; *A. hydrophila* isolated "from diseased specimens of catla, rohu and silver carp" [naca1985] |
| Large red bleeding patches that can become sores; many fish can die soon after | "large haemorrhagic skin lesions are the most commonly observed signs and heavy mortality may occur very shortly after the advent of lesions" [naca1985] |
| Fin bases and vent; swollen belly, scales standing out, bulging eyes, rotting fins | "reddish lesions on the fin bases and anal area"; "blisters, dropsy, abscesses, gill and anal haemorrhages, exophthalmia", scale protrusion, tail and fin rot; "bloated abdomen" [semwal2023] |
| Scales like a pine cone; swims slowly | Vertical scale ("pinecone") disease, caused by *Pseudomonas punctata* or *Aeromonas*: scales stand out "resembling pinecones", abdominal distension, slow swimming [naca1989] |
| When fish are stressed: crowding, low oxygen, dirty water with waste, rough handling, high or changing temperature | "Stress conditions such as crowding, low dissolved oxygen, higher organic content … physical injuries, temperature fluctuation"; elevated temperature and hypoxic conditions [semwal2023] |
| … and high ammonia | "Host susceptibility to *A. hydrophila* was related to ammonia concentration and time of exposure" (channel catfish) [flagg1978] |
| Prevention: don't overstock (waste, oxygen); keep oxygen and ammonia safe, don't overfeed; handle and transport gently | Overcrowding leads to "waste build up, decreased availability of feed and dissolved oxygen, deterioration of water quality" [naca1985]; fish are less susceptible when "handling, stocking levels, diet, transportation and water quality" stress is minimised [semwal2023] |
| Don't buy medicines yourself; drugs tried for dropsy did not work | mixed dropsy infections in catla: "several drugs have been tried without a positive response" [naca1985] |

<a id="gill_disease"></a>
### Bacterial gill disease (gill rot)

| In the app | Source |
|---|---|
| Cause: bacteria (*Myxococcus piscicolus* in the source) | "Bacterial gill rot. Pathogen — *Myxococcus piscicolus*" [naca1989] |
| Pale, rotten gills covered with mud and slime; dark fish, especially the head; gill cover red inside or rotted through | "Diseased fish are black in appearance, especially the head. The gill filaments, which are often covered with mud and mucus, are putrid and pale. … hyperemia and inflammation … on the inside and outside of the opercula. The epidermis of the opercula often rots away" [naca1989] |
| Starts above 20 °C, worst at 28–35 °C; grass carp hit hardest | "seldom appears when the water temperature is below 15 °C and begins to occur when the water temperature is above 20 °C. Its optimum temperature range is 28–35 °C"; "grass carp is the main victim" [naca1989] |
| Prevention: clean water, don't overstock | General prevention: "stocking density, water quality regulation, proper feeding and proper handling" [naca1985] |
| Check the pond every morning in the hot months | "Pond inspection is essential in the morning … during the epidemic season" [naca1989] |
| Behaviour signs | Not described in our sources; the app says so. |

<a id="columnaris"></a>
### Columnaris disease (fin and skin rot)

| In the app | Source |
|---|---|
| Cause: bacteria, *Flavobacterium columnare* | *Flexibacter columnaris* [naca1985]; "*Flavobacterium columnare* is the causative agent of columnaris disease" [declercq2013] |
| In rohu, rot starts at the fin edges and spreads to the body; white sores and bleeding spots; gills eaten away | "In rohu, necrotic lesions begin at the outer margin of the fins and spread towards the body. White ulcerations and haemorrhages may also be observed … Erosion of the gill lamellae" [naca1985] |
| White-yellow slime on patches | "The lesions typically are covered with yellowish-white mucus." [declercq2013] |
| Many fish can die | skin lesions, fin erosion and gill necrosis "with a high degree of mortality" [declercq2013] |
| Above 18 °C, more in warmer water | "Disease outbreaks usually occur at temperature above 18 °C" [naca1985]; "Transmission of columnaris disease is more efficient in higher temperatures" [declercq2013] |
| Crowding, handling and injuries set it off; prevention: avoid crowding, rough netting, handling in warm water | "The stress of crowding, handling or holding them at above normal temperatures, as well as the stress of the external injury, facilitates the transmission and outbreak" [naca1985] |

<a id="saprolegniasis"></a>
### Saprolegniasis (cotton wool disease)

| In the app | Source |
|---|---|
| Cause: water moulds *Saprolegnia* and *Achlya* | "The most common pathogenic genera are *Saprolegnia* and *Achlya*" [naca1989] |
| White, grey or brownish cotton-wool growth on any part, usually on a wound | "white brownish cotton ball like growth … occurring on any part of the body" [naca1985]; "Hyphae develop into a grey, flocculent mass" [naca1989] |
| Lots of slime; muscle rots; fish rub, stop eating, move slowly | "the fish secretes a great deal of mucus. The diseased fish behaves abnormally, fidgeting and rubbing against solid materials. As the mould continues to grow, morbid muscle rots and the fish loses its appetite, moves slowly" [naca1989] |
| Any time of year; after injuries from netting, transport, stocking, spawning, crowding, or on sores from another disease | "Injury produced by spawning, netting, crowding or lesions caused by other diseases are the common sites" [naca1985]; "common … year-round … The mould invades wounds inflicted during netting, transporting, and stocking" [naca1989] |
| Worse in crowded ponds in the cool months | "particularly prevalent in overwintering ponds with a high stocking density" [naca1989] |
| Prevention: gentle handling, don't overcrowd | "Avoid lesions caused by catching, transporting, or stocking" [naca1989] |
| Look for the first problem too | moulds "are considered to be secondary invaders following physical or physiological injury" [naca1985] |

<a id="argulosis"></a>
### Argulosis (fish louse)

| In the app | Source |
|---|---|
| Cause: crustacean parasite *Argulus* (*A. bengalensis*, *A. siamensis* in Indian carps) | Lernaea and Argulus are the crustacean parasites of major carps [naca1985]; *A. bengalensis* and *A. siamensis* on cultured carps in West Bengal [patra2016] |
| Flat lice you can see; hold on with suckers and hooks, can swim off | "Argulus attaches itself to the body of the fish by means of suckers and hooks but it can also swim freely in water" [naca1985]; *Argulus* is among the pathogens visible to the naked eye [naca1989] |
| Red bleeding spots, loose scales; weak, thin, slow growth; some can die | "Infected fish become very weak and emaciated. The common symptoms of argulosis are stunted growth, loose scales, haemorrhagic spots"; "argulosis associated with mortality of major carp" [naca1985] |
| Most cases in September and October (West Bengal) | infection frequency "high in September (17%) and October (12.9%)" [patra2016] |
| Prevention: dry the pond and remove wild fish; check fingerlings before stocking | wild fish are "one of the potential source of fish pathogenic organisms"; dewatering and sun drying the bottom; "Before stocking, proper sample size should be examined to check their health status" [naca1985]. We leave out the source's pesticide pond treatment. |

<a id="flukes"></a>
### Gill and skin flukes (*Dactylogyrus*, *Gyrodactylus*)

| In the app | Source |
|---|---|
| Cause: tiny monogenean worms; *Dactylogyrus* on gills, *Gyrodactylus* on skin and gills | "*Gyrodactylus* infects skin and gills whereas *Dactylogyrus* affects only the gills" [naca1985] |
| Too much slime, faded colour, falling scales, gill fanning | "Excessive mucus secretions, decolouration of body, dropping of scales and faning of gills are the most common symptoms" [naca1985] |
| Pale or swollen gills, gill covers open, hard breathing, slow swimming | "gills become pale, the operculum opens, dyspnea occurs, and there is evident dropsy of the gills … The infected fish swims slowly" [naca1989] |
| Worms seen only with a microscope | identified "through microscopic observation" of gill filaments [naca1989] |
| Mostly fry up to about 3 g; best at 20–25 °C | "Carp larvae and fry up to the weight of about 3 g are more prone" [naca1985]; "The optimum temperature for the parasite is 20–25 °C" [naca1989] |
| Prevention: check a sample of fry, stock healthy seed, sensible density, good water | "stock the pond only with healthy … fry and fingerlings … Before stocking, proper sample size should be examined" [naca1985] |

<a id="white_spot"></a>
### White spot disease (Ich)

| In the app | Source |
|---|---|
| Cause: single-celled parasite *Ichthyophthirius multifiliis* | [naca1985], [naca1989] |
| Pin-head white spots on skin, fins and gills | "pin-head size white spots on the skin, fins and gills" [naca1985] |
| White film in bad cases; slow near the surface, rubbing, jumping, hard breathing, not eating, many deaths | "In a serious case, the skin is covered with a white membrane. The diseased fish swims … slowly, spending much of its time near the surface. It also continually rubs itself against other objects or jumps out of the water … mass mortality because of dyspnea and a loss of appetite" [naca1989] |
| Cooler water, 15–25 °C; crowded ponds | "The optimum water temperature for the proliferation of the parasite is 15–25 °C … Fish in high-density, overwintering ponds are more susceptible" [naca1989] |
| Nursery and rearing ponds | "large scale mortalities … common in nursery and rearing ponds" [naca1985] |
| Prevention: keep new fingerlings apart and check them; sensible density | "rear fry at a reasonable density, quarantine and disinfect fingerlings before stocking" [naca1989]. We leave out the disinfection chemicals. |

<a id="anchor_worm"></a>
### Anchor worm (*Lernaea*)

| In the app | Source |
|---|---|
| Cause: crustacean parasite *Lernaea* | [naca1985], [naca1989] |
| Rod-like parasites anywhere on the body; only the back end hangs out | "a minute rod-like external parasite which attaches itself to the host fish anywhere on the body … Its anterior portion is buried deep into the skin … only the posterior portion is visible hanging" [naca1985] |
| Skin around is red, swollen, can rot; cotton-wool mould grows there | "The areas that *Lernaea* has penetrated are inflammed and swollen, and tissues are necrotic. The wounds are often invaded by *Saprolegnia*." [naca1989]; injuries "lead to secondary fungal or bacterial infections" [naca1985] |
| Restless, eat less, thin, slow; one or two can stunt a small fish | "the diseased fish behaves uneasily, has a poor appetite, is thin, and moves slowly … On a young fish, just one or two parasites can retard growth" [naca1989] |
| Long season in warm water (15–33 °C); nursery and rearing ponds | epidemic season "when the water temperature is 15–33 °C" [naca1989]; "large scale damage in nursery and rearing ponds" [naca1985] |
| Prevention: check fingerlings; dry the pond, remove wild fish | General prevention [naca1985]. We leave out the source's pesticide and chemical baths. |

## What to do for any suspected disease

Shown under every disease and after every checker result:

| In the app | Source |
|---|---|
| Take out dead and dying fish every day: dead fish spread disease | "Fish carrying parasites or the carcasses of diseased fish is a primary source of invasive diseases" [naca1989] |
| Don't move fish, water or nets to another pond | disease spreads with "pond water from a diseased pond, diseased or contaminated silt, feeds and equipment"; "The transportation of diseased fish should be strictly prohibited"; nets "must be disinfected after each use" [naca1989] |
| Give less feed and keep the water quality good | "During the epidemic season, feeding should be limited" [naca1989]; "water quality regulation, proper feeding" [naca1985]; less stress from water quality and diet [semwal2023] |
| Call your fisheries officer or KVK; take a few sick fish, alive or just dead and kept wet | "The fish must be alive or recently dead and the body must be kept damp" for diagnosis [naca1989] |
| No medicines or chemicals here; treatment only as prescribed by a fisheries officer or KVK | Our rule (see Rules above) |

## Link to the live readings

When a parameter is in Warning or Danger, the app lists these diseases as "more likely now", with the reason and a
note that the fish are not necessarily sick. Only links stated in the sources are used. There are deliberately **no
links for high pH or nitrate**: our sources don't give one.

| Reading | More likely | Why (source) |
|---|---|---|
| Oxygen low | Aeromonas infection | low dissolved oxygen is a stress condition for *A. hydrophila* infection [semwal2023]; environmental stress triggers outbreaks of infectious fish diseases [snieszko1974] |
| Ammonia high | Aeromonas infection | susceptibility related to ammonia concentration [flagg1978]; stress from fish metabolic products [snieszko1974] |
| Temperature high (above 32 °C) | Columnaris, gill rot, Aeromonas infection | columnaris transmission "more efficient in higher temperatures" [declercq2013], holding fish "at above normal temperatures" [naca1985]; gill rot optimum 28–35 °C [naca1989]; elevated temperature for *Aeromonas* [semwal2023] |
| Temperature low (below 25 °C) | EUS, white spot | EUS outbreaks with "low temperatures" [fao2001]; Ich optimum 15–25 °C [naca1989] |
| pH low (below 6.5) | EUS | outbreaks "associated with acidified water" [fao2001] |

## Why there's no photo check

We tried to recognise diseases from fish photos and decided not to put it in the app:

- The public photo dataset is mostly goldfish, aquarium fish and stock photos, **not Indian carps in ponds**.
- Most of its "test" photos are copies of training photos. After removing the copies, the honest score is
  **68 %**: about one photo in three is wrong.
- A model still gets **55 %** with the fish greyed out, so much of the score comes from the background, not the disease.

That is far too unreliable for a decision about a farmer's fish.
Details: [fish-disease-baseline.md](fish-disease-baseline.md) and [fish-disease-cleaning.md](fish-disease-cleaning.md).
