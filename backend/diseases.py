"""
Fish disease guide: common diseases of Indian carp ponds, a symptom checker
and the link between risky water readings and diseases.

What this file does:
    SOURCES       the real publications behind every entry (FAO, NACA documents
                  hosted by FAO, peer-reviewed papers). Full list: docs/diseases.md.
    SIGNS         the signs a farmer can tick in the symptom checker.
    DISEASES      one entry per disease: names, cause type, signs, when it is
                  most common, prevention, what to do, sources.
    COMMON_STEPS  what to do for any suspected disease.
    check(signs)  "possible matches" for the ticked signs. NEVER a diagnosis.
    likely_diseases(risk)  diseases that become more likely with this reading
                  (e.g. low oxygen, high temperature).

Rules for this file (see docs/diseases.md):
  - Every statement comes from a source listed in SOURCES.
  - No chemical treatments, medicines or doses. Treatment must be prescribed
    by a fisheries officer or a KVK (Krishi Vigyan Kendra).
  - The checker shows possible matches only, and always ends with
    "confirm with your fisheries officer".
Kannada text should be reviewed by a native speaker before release.
"""

from __future__ import annotations

# Short keys used in DISEASES["sources"]; the full references are in docs/diseases.md.
SOURCES = {
    "fao2001": "FAO & NACA (2001). Asia Diagnostic Guide to Aquatic Animal Diseases. FAO Fisheries Technical Paper 402/2.",
    "naca1985": "FAR&TC Dhauli, ICAR-CIFRI (now ICAR-CIFA) (1985). Diseases and health care in composite fish culture. NACA/TR/85/15, FAO document repository.",
    "naca1989": "Li Shaoqi (1989). Main fish diseases and their control. Integrated Fish Farming in China, NACA Technical Manual 7, FAO document repository.",
    "declercq2013": "Declercq et al. (2013). Columnaris disease in fish: a review. Veterinary Research 44:27.",
    "semwal2023": "Semwal et al. (2023). A review on pathogenicity of Aeromonas hydrophila. Heliyon 9:e14088.",
    "patra2016": "Patra et al. (2016). Argulus infecting cultured carps in West Bengal. Molecular Biology Research Communications 5:156-166.",
    "flagg1978": "Flagg & Hinck (1978). Influence of ammonia on aeromonad susceptibility in channel catfish. Proc. SEAFWA, 415-419.",
    "snieszko1974": "Snieszko (1974). The effects of environmental stress on outbreaks of infectious diseases of fishes. Journal of Fish Biology 6:197-208.",
}

# What the farmer can tick. "body" = what you see on the fish, "behaviour" = how it acts.
SIGNS = {
    "red_sores": {"group": "body", "en": "Red spots or open sores (ulcers) on the body",
                  "kn": "ದೇಹದ ಮೇಲೆ ಕೆಂಪು ಚುಕ್ಕೆಗಳು ಅಥವಾ ತೆರೆದ ಹುಣ್ಣುಗಳು"},
    "red_patches": {"group": "body", "en": "Red, bleeding patches on the skin or fins",
                    "kn": "ಚರ್ಮ ಅಥವಾ ಈಜುರೆಕ್ಕೆಗಳ ಮೇಲೆ ಕೆಂಪು, ರಕ್ತಸ್ರಾವದ ಕಲೆಗಳು"},
    "swollen_belly": {"group": "body", "en": "Swollen belly", "kn": "ಊದಿಕೊಂಡ ಹೊಟ್ಟೆ"},
    "raised_scales": {"group": "body", "en": "Scales standing out, like a pine cone",
                      "kn": "ಪೈನ್ ಕಾಯಿಯಂತೆ ಎದ್ದು ನಿಂತ ಹುರುಪೆಗಳು"},
    "pop_eye": {"group": "body", "en": "Bulging eyes", "kn": "ಉಬ್ಬಿದ ಕಣ್ಣುಗಳು"},
    "white_spots": {"group": "body", "en": "Many tiny white spots, like pin heads, on skin, fins or gills",
                    "kn": "ಚರ್ಮ, ಈಜುರೆಕ್ಕೆ ಅಥವಾ ಕಿವಿರುಗಳ ಮೇಲೆ ಗುಂಡುಸೂಜಿ ತಲೆಯಂತಹ ಅನೇಕ ಸಣ್ಣ ಬಿಳಿ ಚುಕ್ಕೆಗಳು"},
    "cotton": {"group": "body", "en": "White, grey or brownish cotton-wool growth on the body",
               "kn": "ದೇಹದ ಮೇಲೆ ಬಿಳಿ, ಬೂದು ಅಥವಾ ಕಂದು ಹತ್ತಿಯಂತಹ ಬೆಳವಣಿಗೆ"},
    "fin_rot": {"group": "body", "en": "Fins rotting from the edges, or white-yellow patches on the skin",
                "kn": "ಅಂಚಿನಿಂದ ಕೊಳೆಯುತ್ತಿರುವ ಈಜುರೆಕ್ಕೆಗಳು, ಅಥವಾ ಚರ್ಮದ ಮೇಲೆ ಬಿಳಿ-ಹಳದಿ ಕಲೆಗಳು"},
    "gill_rot": {"group": "body", "en": "Gills look rotten, covered with mud and slime",
                 "kn": "ಕಿವಿರುಗಳು ಕೊಳೆತಂತೆ, ಕೆಸರು ಮತ್ತು ಲೋಳೆಯಿಂದ ಮುಚ್ಚಿದಂತೆ ಕಾಣುತ್ತವೆ"},
    "pale_gills": {"group": "body", "en": "Pale gills", "kn": "ಬಿಳಿಚಿದ ಕಿವಿರುಗಳು"},
    "lice": {"group": "body", "en": "Small, flat, round lice you can see on the skin",
             "kn": "ಚರ್ಮದ ಮೇಲೆ ಕಣ್ಣಿಗೆ ಕಾಣುವ ಸಣ್ಣ, ಚಪ್ಪಟೆ, ದುಂಡಗಿನ ಹೇನುಗಳು"},
    "threads": {"group": "body", "en": "Thin threads hanging from the skin, with a swollen red spot around each",
                "kn": "ಚರ್ಮದಿಂದ ನೇತಾಡುವ ತೆಳುವಾದ ದಾರಗಳು, ಪ್ರತಿಯೊಂದರ ಸುತ್ತ ಊದಿದ ಕೆಂಪು ಜಾಗ"},
    "loose_scales": {"group": "body", "en": "Loose or falling scales", "kn": "ಸಡಿಲವಾದ ಅಥವಾ ಉದುರುವ ಹುರುಪೆಗಳು"},
    "much_mucus": {"group": "body", "en": "Too much slime on the body or gills",
                   "kn": "ದೇಹ ಅಥವಾ ಕಿವಿರುಗಳ ಮೇಲೆ ಅತಿಯಾದ ಲೋಳೆ"},
    "colour_change": {"group": "body", "en": "Body colour has changed (darker or faded)",
                      "kn": "ದೇಹದ ಬಣ್ಣ ಬದಲಾಗಿದೆ (ಕಪ್ಪಾಗಿದೆ ಅಥವಾ ಮಸುಕಾಗಿದೆ)"},
    "thin_weak": {"group": "body", "en": "Thin, weak fish that grow slowly",
                  "kn": "ಸಣಕಲು, ದುರ್ಬಲ, ನಿಧಾನವಾಗಿ ಬೆಳೆಯುವ ಮೀನುಗಳು"},
    "gasping": {"group": "behaviour", "en": "Gasping at the surface", "kn": "ನೀರಿನ ಮೇಲ್ಮೈಯಲ್ಲಿ ಉಸಿರಿಗಾಗಿ ಏದುಸಿರು"},
    "fast_breathing": {"group": "behaviour", "en": "Hard, fast breathing with gill covers held open",
                       "kn": "ಕಿವಿರು ಮುಚ್ಚಳ ತೆರೆದಿಟ್ಟು ಕಷ್ಟದ, ವೇಗದ ಉಸಿರಾಟ"},
    "rubbing": {"group": "behaviour", "en": "Rubbing against the bottom or sides, or jumping",
                "kn": "ತಳ ಅಥವಾ ಬದಿಗಳಿಗೆ ಉಜ್ಜಿಕೊಳ್ಳುವುದು, ಅಥವಾ ನೀರಿನಿಂದ ಜಿಗಿಯುವುದು"},
    "slow_surface": {"group": "behaviour", "en": "Swimming slowly, alone or near the surface",
                     "kn": "ನಿಧಾನವಾಗಿ, ಒಂಟಿಯಾಗಿ ಅಥವಾ ಮೇಲ್ಮೈ ಹತ್ತಿರ ಈಜುವುದು"},
    "not_eating": {"group": "behaviour", "en": "Not eating", "kn": "ಆಹಾರ ತಿನ್ನುತ್ತಿಲ್ಲ"},
}

CAUSE_TYPES = {
    "water_mould": {"en": "Water mould (fungus-like)", "kn": "ನೀರಿನ ಬೂಷ್ಟು (ಶಿಲೀಂಧ್ರದಂತಹದು)"},
    "bacteria": {"en": "Bacteria", "kn": "ಬ್ಯಾಕ್ಟೀರಿಯಾ"},
    "protozoan": {"en": "Parasite: tiny single-celled animal", "kn": "ಪರಾವಲಂಬಿ: ಏಕಕೋಶದ ಸೂಕ್ಷ್ಮ ಜೀವಿ"},
    "worm": {"en": "Parasite: tiny worm (fluke)", "kn": "ಪರಾವಲಂಬಿ: ಸಣ್ಣ ಹುಳು (ಫ್ಲೂಕ್)"},
    "crustacean": {"en": "Parasite: crustacean (relative of shrimps)", "kn": "ಪರಾವಲಂಬಿ: ಕಠಿಣಚರ್ಮಿ (ಸೀಗಡಿಯ ಸಂಬಂಧಿ)"},
}

# Signs marked "key" count double in the checker: they point most clearly to that disease.
DISEASES = {
    "eus": {
        "name": {"en": "Epizootic ulcerative syndrome (EUS, red spot disease)",
                 "kn": "ಎಪಿಜೂಟಿಕ್ ಅಲ್ಸರೇಟಿವ್ ಸಿಂಡ್ರೋಮ್ (EUS, ಕೆಂಪು ಚುಕ್ಕೆ ಹುಣ್ಣು ರೋಗ)"},
        "cause": "water_mould",
        "agent": "Aphanomyces invadans",
        "key_signs": ["red_sores"],
        "other_signs": ["red_patches"],
        "body": {"en": "Starts as red spots. These become deep open sores that go into the muscle. Older sores can have a raised white edge.",
                 "kn": "ಕೆಂಪು ಚುಕ್ಕೆಗಳಾಗಿ ಆರಂಭವಾಗುತ್ತದೆ. ಅವು ಸ್ನಾಯುವಿನೊಳಗೆ ಹೋಗುವ ಆಳವಾದ ತೆರೆದ ಹುಣ್ಣುಗಳಾಗುತ್ತವೆ. ಹಳೆಯ ಹುಣ್ಣುಗಳಿಗೆ ಎದ್ದ ಬಿಳಿ ಅಂಚು ಇರಬಹುದು."},
        "behaviour": {"en": "Many fish can die in an outbreak.",
                      "kn": "ರೋಗ ಹರಡಿದಾಗ ಅನೇಕ ಮೀನುಗಳು ಸಾಯಬಹುದು."},
        "when": {"en": "In cool weather, and when runoff makes the water acidic. Spreads with floods and when fish are moved. Chinese carps resist it.",
                 "kn": "ತಂಪಾದ ಹವಾಮಾನದಲ್ಲಿ, ಮತ್ತು ಹರಿದು ಬಂದ ನೀರು ಕೊಳವನ್ನು ಆಮ್ಲೀಯಗೊಳಿಸಿದಾಗ. ಪ್ರವಾಹದಿಂದ ಮತ್ತು ಮೀನುಗಳನ್ನು ಸಾಗಿಸಿದಾಗ ಹರಡುತ್ತದೆ. ಚೀನೀ ಗೆಂಡೆಗಳು ಇದನ್ನು ತಡೆದುಕೊಳ್ಳುತ್ತವೆ."},
        "prevention": [
            {"en": "Dry the pond completely before stocking. Ask your fisheries officer about liming.",
             "kn": "ಮೀನು ಬಿಡುವ ಮೊದಲು ಕೊಳವನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ಒಣಗಿಸಿ. ಸುಣ್ಣ ಹಾಕುವ ಬಗ್ಗೆ ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯನ್ನು ಕೇಳಿ."},
            {"en": "Keep wild fish out of the pond. Stock hatchery-reared seed.",
             "kn": "ಕಾಡು ಮೀನುಗಳು ಕೊಳಕ್ಕೆ ಬರದಂತೆ ತಡೆಯಿರಿ. ಮೊಟ್ಟೆಕೇಂದ್ರದಲ್ಲಿ ಬೆಳೆಸಿದ ಮರಿಗಳನ್ನು ಬಿಡಿ."},
            {"en": "Clean nets and tools before using them in another pond.",
             "kn": "ಬಲೆ ಮತ್ತು ಸಾಧನಗಳನ್ನು ಬೇರೆ ಕೊಳದಲ್ಲಿ ಬಳಸುವ ಮೊದಲು ಸ್ವಚ್ಛಗೊಳಿಸಿ."},
        ],
        "do": [{"en": "Ulcers can also come from other diseases, so a laboratory test is needed to be sure.",
                "kn": "ಹುಣ್ಣುಗಳು ಬೇರೆ ರೋಗಗಳಿಂದಲೂ ಬರಬಹುದು, ಆದ್ದರಿಂದ ಖಚಿತಪಡಿಸಲು ಪ್ರಯೋಗಾಲಯ ಪರೀಕ್ಷೆ ಬೇಕು."}],
        "sources": ["fao2001"],
    },
    "aeromoniasis": {
        "name": {"en": "Aeromonas infection (dropsy, haemorrhagic septicaemia)",
                 "kn": "ಏರೋಮೋನಾಸ್ ಸೋಂಕು (ಹೊಟ್ಟೆ ಊತ / ಡ್ರಾಪ್ಸಿ, ರಕ್ತಸ್ರಾವ ರೋಗ)"},
        "cause": "bacteria",
        "agent": "Aeromonas hydrophila and related bacteria",
        "key_signs": ["swollen_belly", "raised_scales"],
        "other_signs": ["red_patches", "red_sores", "pop_eye", "fin_rot", "slow_surface"],
        "body": {"en": "Large red, bleeding patches on the skin, often at the fin bases and vent, that can become sores. Swollen belly, scales standing out, bulging eyes, rotting fins.",
                 "kn": "ಚರ್ಮದ ಮೇಲೆ, ಹೆಚ್ಚಾಗಿ ಈಜುರೆಕ್ಕೆಗಳ ಬುಡ ಮತ್ತು ಗುದದ ಬಳಿ, ದೊಡ್ಡ ಕೆಂಪು ರಕ್ತಸ್ರಾವದ ಕಲೆಗಳು, ಅವು ಹುಣ್ಣಾಗಬಹುದು. ಊದಿದ ಹೊಟ್ಟೆ, ಎದ್ದ ಹುರುಪೆಗಳು, ಉಬ್ಬಿದ ಕಣ್ಣುಗಳು, ಕೊಳೆಯುವ ಈಜುರೆಕ್ಕೆಗಳು."},
        "behaviour": {"en": "Sick fish swim slowly. Many can die soon after the red patches appear.",
                      "kn": "ರೋಗಪೀಡಿತ ಮೀನುಗಳು ನಿಧಾನವಾಗಿ ಈಜುತ್ತವೆ. ಕೆಂಪು ಕಲೆಗಳು ಕಾಣಿಸಿದ ಸ್ವಲ್ಪ ಸಮಯದಲ್ಲೇ ಅನೇಕ ಮೀನುಗಳು ಸಾಯಬಹುದು."},
        "when": {"en": "When fish are stressed: crowding, low oxygen, dirty water with a lot of waste, rough handling, high or changing temperature, and high ammonia.",
                 "kn": "ಮೀನುಗಳು ಒತ್ತಡದಲ್ಲಿದ್ದಾಗ: ಹೆಚ್ಚು ಮೀನು ತುಂಬಿದಾಗ, ಕಡಿಮೆ ಆಮ್ಲಜನಕ, ಹೆಚ್ಚು ತ್ಯಾಜ್ಯವಿರುವ ಕೊಳಕು ನೀರು, ಒರಟು ನಿರ್ವಹಣೆ, ಹೆಚ್ಚಿನ ಅಥವಾ ಬದಲಾಗುವ ತಾಪಮಾನ, ಮತ್ತು ಹೆಚ್ಚಿನ ಅಮೋನಿಯಾ."},
        "prevention": [
            {"en": "Do not overstock. Crowding builds up waste and uses up oxygen.",
             "kn": "ಹೆಚ್ಚು ಮೀನು ಬಿಡಬೇಡಿ. ದಟ್ಟಣೆಯಿಂದ ತ್ಯಾಜ್ಯ ಹೆಚ್ಚುತ್ತದೆ ಮತ್ತು ಆಮ್ಲಜನಕ ಕಡಿಮೆಯಾಗುತ್ತದೆ."},
            {"en": "Keep oxygen and ammonia in the safe range. Do not overfeed.",
             "kn": "ಆಮ್ಲಜನಕ ಮತ್ತು ಅಮೋನಿಯಾವನ್ನು ಸುರಕ್ಷಿತ ಮಟ್ಟದಲ್ಲಿಡಿ. ಹೆಚ್ಚು ಆಹಾರ ಹಾಕಬೇಡಿ."},
            {"en": "Handle and transport fish gently and as little as possible, not in hot weather.",
             "kn": "ಮೀನುಗಳನ್ನು ನಿಧಾನವಾಗಿ, ಸಾಧ್ಯವಾದಷ್ಟು ಕಡಿಮೆ ನಿರ್ವಹಿಸಿ ಮತ್ತು ಸಾಗಿಸಿ, ಬಿಸಿ ಹವಾಮಾನದಲ್ಲಿ ಬೇಡ."},
        ],
        "do": [{"en": "Do not buy medicines yourself. In Indian carp ponds, several drugs tried for dropsy did not work.",
                "kn": "ನೀವೇ ಔಷಧಿ ಖರೀದಿಸಬೇಡಿ. ಭಾರತದ ಗೆಂಡೆ ಮೀನಿನ ಕೊಳಗಳಲ್ಲಿ, ಡ್ರಾಪ್ಸಿಗೆ ಪ್ರಯತ್ನಿಸಿದ ಹಲವು ಔಷಧಿಗಳು ಫಲ ನೀಡಲಿಲ್ಲ."}],
        "sources": ["naca1985", "semwal2023", "naca1989", "flagg1978"],
    },
    "gill_disease": {
        "name": {"en": "Bacterial gill disease (gill rot)", "kn": "ಬ್ಯಾಕ್ಟೀರಿಯಾದ ಕಿವಿರು ರೋಗ (ಕಿವಿರು ಕೊಳೆ)"},
        "cause": "bacteria",
        "agent": "Myxococcus piscicolus (the name used in the source)",
        "key_signs": ["gill_rot"],
        "other_signs": ["pale_gills", "colour_change"],
        "body": {"en": "Gills are pale and rotten, often covered with mud and slime. The fish looks dark, especially the head. The gill cover can be red inside, or rot through.",
                 "kn": "ಕಿವಿರುಗಳು ಬಿಳಿಚಿ ಕೊಳೆತಿರುತ್ತವೆ, ಹೆಚ್ಚಾಗಿ ಕೆಸರು ಮತ್ತು ಲೋಳೆಯಿಂದ ಮುಚ್ಚಿರುತ್ತವೆ. ಮೀನು, ವಿಶೇಷವಾಗಿ ತಲೆ, ಕಪ್ಪಾಗಿ ಕಾಣುತ್ತದೆ. ಕಿವಿರು ಮುಚ್ಚಳ ಒಳಗೆ ಕೆಂಪಾಗಿರಬಹುದು ಅಥವಾ ಕೊಳೆತು ತೂತಾಗಬಹುದು."},
        "behaviour": {"en": "Our sources describe the body signs only.",
                      "kn": "ನಮ್ಮ ಮೂಲಗಳು ದೇಹದ ಲಕ್ಷಣಗಳನ್ನು ಮಾತ್ರ ವಿವರಿಸುತ್ತವೆ."},
        "when": {"en": "Warm water: it starts above 20 °C and is worst at 28-35 °C. Grass carp is hit hardest.",
                 "kn": "ಬೆಚ್ಚಗಿನ ನೀರಿನಲ್ಲಿ: 20 °C ಮೇಲೆ ಆರಂಭವಾಗುತ್ತದೆ, 28-35 °C ನಲ್ಲಿ ಹೆಚ್ಚು. ಹುಲ್ಲು ಗೆಂಡೆ (ಗ್ರಾಸ್ ಕಾರ್ಪ್) ಹೆಚ್ಚು ಬಾಧಿತವಾಗುತ್ತದೆ."},
        "prevention": [
            {"en": "Keep the water clean and do not overstock.",
             "kn": "ನೀರನ್ನು ಶುದ್ಧವಾಗಿಡಿ ಮತ್ತು ಹೆಚ್ಚು ಮೀನು ಬಿಡಬೇಡಿ."},
            {"en": "In the hot months, check the pond every morning.",
             "kn": "ಬಿಸಿ ತಿಂಗಳುಗಳಲ್ಲಿ ಪ್ರತಿದಿನ ಬೆಳಿಗ್ಗೆ ಕೊಳವನ್ನು ಪರಿಶೀಲಿಸಿ."},
        ],
        "do": [],
        "sources": ["naca1989", "naca1985"],
    },
    "columnaris": {
        "name": {"en": "Columnaris disease (fin and skin rot)", "kn": "ಕಾಲಮ್ನಾರಿಸ್ ರೋಗ (ಈಜುರೆಕ್ಕೆ ಮತ್ತು ಚರ್ಮ ಕೊಳೆ)"},
        "cause": "bacteria",
        "agent": "Flavobacterium columnare",
        "key_signs": ["fin_rot"],
        "other_signs": ["red_sores", "red_patches", "gill_rot", "much_mucus"],
        "body": {"en": "In rohu, rot starts at the edges of the fins and spreads to the body. White sores and bleeding spots. Patches covered with white-yellow slime. Gills can be eaten away.",
                 "kn": "ರೋಹುವಿನಲ್ಲಿ, ಕೊಳೆ ಈಜುರೆಕ್ಕೆಗಳ ಅಂಚಿನಿಂದ ಆರಂಭವಾಗಿ ದೇಹಕ್ಕೆ ಹರಡುತ್ತದೆ. ಬಿಳಿ ಹುಣ್ಣುಗಳು ಮತ್ತು ರಕ್ತಸ್ರಾವದ ಚುಕ್ಕೆಗಳು. ಬಿಳಿ-ಹಳದಿ ಲೋಳೆಯಿಂದ ಮುಚ್ಚಿದ ಕಲೆಗಳು. ಕಿವಿರುಗಳು ಸವೆದುಹೋಗಬಹುದು."},
        "behaviour": {"en": "Many fish can die.", "kn": "ಅನೇಕ ಮೀನುಗಳು ಸಾಯಬಹುದು."},
        "when": {"en": "Above 18 °C, and more when the water is warmer. Crowding, handling and injuries set it off.",
                 "kn": "18 °C ಮೇಲೆ, ನೀರು ಹೆಚ್ಚು ಬೆಚ್ಚಗಾದಂತೆ ಹೆಚ್ಚು. ದಟ್ಟಣೆ, ನಿರ್ವಹಣೆ ಮತ್ತು ಗಾಯಗಳು ಇದನ್ನು ಪ್ರಚೋದಿಸುತ್ತವೆ."},
        "prevention": [
            {"en": "Avoid crowding and rough netting, which injure the skin.",
             "kn": "ಚರ್ಮಕ್ಕೆ ಗಾಯ ಮಾಡುವ ದಟ್ಟಣೆ ಮತ್ತು ಒರಟು ಬಲೆ ಹಾಕುವಿಕೆಯನ್ನು ತಪ್ಪಿಸಿ."},
            {"en": "Do not handle fish when the water is very warm.",
             "kn": "ನೀರು ತುಂಬಾ ಬೆಚ್ಚಗಿರುವಾಗ ಮೀನುಗಳನ್ನು ನಿರ್ವಹಿಸಬೇಡಿ."},
        ],
        "do": [],
        "sources": ["naca1985", "declercq2013"],
    },
    "saprolegniasis": {
        "name": {"en": "Saprolegniasis (cotton wool disease)", "kn": "ಸಾಪ್ರೊಲೆಗ್ನಿಯಾಸಿಸ್ (ಹತ್ತಿ ಬೂಷ್ಟು ರೋಗ)"},
        "cause": "water_mould",
        "agent": "Saprolegnia and Achlya",
        "key_signs": ["cotton"],
        "other_signs": ["much_mucus", "rubbing", "not_eating", "slow_surface"],
        "body": {"en": "A white, grey or brownish cotton-wool growth on any part of the body, usually on a wound. Lots of slime. Under the growth the muscle rots.",
                 "kn": "ದೇಹದ ಯಾವುದೇ ಭಾಗದಲ್ಲಿ, ಸಾಮಾನ್ಯವಾಗಿ ಗಾಯದ ಮೇಲೆ, ಬಿಳಿ, ಬೂದು ಅಥವಾ ಕಂದು ಹತ್ತಿಯಂತಹ ಬೆಳವಣಿಗೆ. ಹೆಚ್ಚು ಲೋಳೆ. ಬೆಳವಣಿಗೆಯ ಕೆಳಗೆ ಸ್ನಾಯು ಕೊಳೆಯುತ್ತದೆ."},
        "behaviour": {"en": "Fish rub against things, stop eating and move slowly.",
                      "kn": "ಮೀನುಗಳು ವಸ್ತುಗಳಿಗೆ ಉಜ್ಜಿಕೊಳ್ಳುತ್ತವೆ, ತಿನ್ನುವುದನ್ನು ನಿಲ್ಲಿಸುತ್ತವೆ ಮತ್ತು ನಿಧಾನವಾಗಿ ಚಲಿಸುತ್ತವೆ."},
        "when": {"en": "Any time of year, after injuries from netting, transport, stocking, spawning or crowding, or on sores from another disease. Worse in crowded ponds in the cool months.",
                 "kn": "ವರ್ಷದ ಯಾವುದೇ ಸಮಯದಲ್ಲಿ, ಬಲೆ, ಸಾಗಣೆ, ಮೀನು ಬಿಡುವಿಕೆ, ಮೊಟ್ಟೆ ಇಡುವಿಕೆ ಅಥವಾ ದಟ್ಟಣೆಯಿಂದಾದ ಗಾಯಗಳ ನಂತರ, ಅಥವಾ ಬೇರೆ ರೋಗದ ಹುಣ್ಣುಗಳ ಮೇಲೆ. ತಂಪು ತಿಂಗಳುಗಳಲ್ಲಿ ದಟ್ಟ ಕೊಳಗಳಲ್ಲಿ ಹೆಚ್ಚು."},
        "prevention": [
            {"en": "Net, carry and stock fish gently so they are not injured.",
             "kn": "ಮೀನುಗಳಿಗೆ ಗಾಯವಾಗದಂತೆ ನಿಧಾನವಾಗಿ ಬಲೆ ಹಾಕಿ, ಸಾಗಿಸಿ ಮತ್ತು ಬಿಡಿ."},
            {"en": "Do not overcrowd the pond.", "kn": "ಕೊಳದಲ್ಲಿ ಹೆಚ್ಚು ದಟ್ಟಣೆ ಮಾಡಬೇಡಿ."},
        ],
        "do": [{"en": "The mould usually grows on a wound or another disease. Look for the first problem too (EUS, anchor worm, injuries).",
                "kn": "ಬೂಷ್ಟು ಸಾಮಾನ್ಯವಾಗಿ ಗಾಯ ಅಥವಾ ಬೇರೆ ರೋಗದ ಮೇಲೆ ಬೆಳೆಯುತ್ತದೆ. ಮೊದಲ ಸಮಸ್ಯೆಯನ್ನೂ ಹುಡುಕಿ (EUS, ಲಂಗರು ಹುಳು, ಗಾಯಗಳು)."}],
        "sources": ["naca1985", "naca1989"],
    },
    "argulosis": {
        "name": {"en": "Argulosis (fish louse)", "kn": "ಆರ್ಗುಲೋಸಿಸ್ (ಮೀನು ಹೇನು)"},
        "cause": "crustacean",
        "agent": "Argulus (e.g. A. bengalensis, A. siamensis)",
        "key_signs": ["lice"],
        "other_signs": ["red_patches", "loose_scales", "thin_weak"],
        "body": {"en": "Flat, round lice you can see on the skin. They hold on with suckers and hooks and can also swim off. Red bleeding spots and loose scales.",
                 "kn": "ಚರ್ಮದ ಮೇಲೆ ಕಣ್ಣಿಗೆ ಕಾಣುವ ಚಪ್ಪಟೆ, ದುಂಡಗಿನ ಹೇನುಗಳು. ಅವು ಹೀರುಬಟ್ಟಲು ಮತ್ತು ಕೊಕ್ಕೆಗಳಿಂದ ಹಿಡಿದುಕೊಳ್ಳುತ್ತವೆ ಮತ್ತು ಈಜಿ ಹೋಗಬಹುದು. ಕೆಂಪು ರಕ್ತಸ್ರಾವದ ಚುಕ್ಕೆಗಳು ಮತ್ತು ಸಡಿಲ ಹುರುಪೆಗಳು."},
        "behaviour": {"en": "Fish become weak and thin and grow slowly. Some can die.",
                      "kn": "ಮೀನುಗಳು ದುರ್ಬಲ ಮತ್ತು ಸಣಕಲಾಗುತ್ತವೆ ಮತ್ತು ನಿಧಾನವಾಗಿ ಬೆಳೆಯುತ್ತವೆ. ಕೆಲವು ಸಾಯಬಹುದು."},
        "when": {"en": "Common in carp ponds. In a West Bengal study, most cases were in September and October.",
                 "kn": "ಗೆಂಡೆ ಮೀನಿನ ಕೊಳಗಳಲ್ಲಿ ಸಾಮಾನ್ಯ. ಪಶ್ಚಿಮ ಬಂಗಾಳದ ಒಂದು ಅಧ್ಯಯನದಲ್ಲಿ, ಹೆಚ್ಚಿನ ಪ್ರಕರಣಗಳು ಸೆಪ್ಟೆಂಬರ್ ಮತ್ತು ಅಕ್ಟೋಬರ್‌ನಲ್ಲಿದ್ದವು."},
        "prevention": [
            {"en": "Before stocking, dry the pond and remove wild fish.",
             "kn": "ಮೀನು ಬಿಡುವ ಮೊದಲು, ಕೊಳವನ್ನು ಒಣಗಿಸಿ ಮತ್ತು ಕಾಡು ಮೀನುಗಳನ್ನು ತೆಗೆದುಹಾಕಿ."},
            {"en": "Check a few fingerlings for lice before you stock them.",
             "kn": "ಮರಿಗಳನ್ನು ಬಿಡುವ ಮೊದಲು ಕೆಲವು ಮರಿಗಳಲ್ಲಿ ಹೇನುಗಳಿವೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ."},
        ],
        "do": [],
        "sources": ["naca1985", "patra2016", "naca1989"],
    },
    "flukes": {
        "name": {"en": "Gill and skin flukes (Dactylogyrus, Gyrodactylus)",
                 "kn": "ಕಿವಿರು ಮತ್ತು ಚರ್ಮದ ಹುಳುಗಳು (ಡ್ಯಾಕ್ಟಿಲೋಗೈರಸ್, ಗೈರೊಡ್ಯಾಕ್ಟಿಲಸ್)"},
        "cause": "worm",
        "agent": "Dactylogyrus (gills) and Gyrodactylus (skin and gills)",
        "key_signs": ["fast_breathing"],
        "other_signs": ["much_mucus", "pale_gills", "colour_change", "loose_scales", "slow_surface", "gasping"],
        "body": {"en": "Too much slime, pale or swollen gills, faded body colour, falling scales. The worms are too small to see without a microscope.",
                 "kn": "ಅತಿಯಾದ ಲೋಳೆ, ಬಿಳಿಚಿದ ಅಥವಾ ಊದಿದ ಕಿವಿರುಗಳು, ಮಸುಕಾದ ದೇಹದ ಬಣ್ಣ, ಉದುರುವ ಹುರುಪೆಗಳು. ಹುಳುಗಳು ಸೂಕ್ಷ್ಮದರ್ಶಕವಿಲ್ಲದೆ ಕಾಣದಷ್ಟು ಸಣ್ಣವು."},
        "behaviour": {"en": "Hard breathing with the gill covers open. Fish swim slowly.",
                      "kn": "ಕಿವಿರು ಮುಚ್ಚಳ ತೆರೆದು ಕಷ್ಟದ ಉಸಿರಾಟ. ಮೀನುಗಳು ನಿಧಾನವಾಗಿ ಈಜುತ್ತವೆ."},
        "when": {"en": "Mostly in fry and small fish up to about 3 g. The worms do best at 20-25 °C.",
                 "kn": "ಹೆಚ್ಚಾಗಿ ಸುಮಾರು 3 ಗ್ರಾಂ ವರೆಗಿನ ಮರಿಗಳು ಮತ್ತು ಸಣ್ಣ ಮೀನುಗಳಲ್ಲಿ. ಹುಳುಗಳು 20-25 °C ನಲ್ಲಿ ಚೆನ್ನಾಗಿ ಬೆಳೆಯುತ್ತವೆ."},
        "prevention": [
            {"en": "Look at a sample of fry before stocking. Stock only healthy seed.",
             "kn": "ಬಿಡುವ ಮೊದಲು ಕೆಲವು ಮರಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ. ಆರೋಗ್ಯಕರ ಮರಿಗಳನ್ನು ಮಾತ್ರ ಬಿಡಿ."},
            {"en": "Keep fry at a sensible density in good water.",
             "kn": "ಮರಿಗಳನ್ನು ಉತ್ತಮ ನೀರಿನಲ್ಲಿ ಸೂಕ್ತ ಸಂಖ್ಯೆಯಲ್ಲಿ ಇಡಿ."},
        ],
        "do": [],
        "sources": ["naca1985", "naca1989"],
    },
    "white_spot": {
        "name": {"en": "White spot disease (Ich)", "kn": "ಬಿಳಿ ಚುಕ್ಕೆ ರೋಗ (ಇಕ್)"},
        "cause": "protozoan",
        "agent": "Ichthyophthirius multifiliis",
        "key_signs": ["white_spots"],
        "other_signs": ["rubbing", "slow_surface", "much_mucus", "gasping"],
        "body": {"en": "Many white spots the size of a pin head on the skin, fins and gills. In bad cases the skin looks covered by a white film.",
                 "kn": "ಚರ್ಮ, ಈಜುರೆಕ್ಕೆ ಮತ್ತು ಕಿವಿರುಗಳ ಮೇಲೆ ಗುಂಡುಸೂಜಿ ತಲೆಯ ಗಾತ್ರದ ಅನೇಕ ಬಿಳಿ ಚುಕ್ಕೆಗಳು. ತೀವ್ರವಾದಾಗ ಚರ್ಮ ಬಿಳಿ ಪದರದಿಂದ ಮುಚ್ಚಿದಂತೆ ಕಾಣುತ್ತದೆ."},
        "behaviour": {"en": "Fish swim slowly near the surface, rub against things or jump. They breathe with difficulty and stop eating. Many can die.",
                      "kn": "ಮೀನುಗಳು ಮೇಲ್ಮೈ ಹತ್ತಿರ ನಿಧಾನವಾಗಿ ಈಜುತ್ತವೆ, ವಸ್ತುಗಳಿಗೆ ಉಜ್ಜಿಕೊಳ್ಳುತ್ತವೆ ಅಥವಾ ಜಿಗಿಯುತ್ತವೆ. ಕಷ್ಟದಿಂದ ಉಸಿರಾಡುತ್ತವೆ ಮತ್ತು ತಿನ್ನುವುದನ್ನು ನಿಲ್ಲಿಸುತ್ತವೆ. ಅನೇಕ ಸಾಯಬಹುದು."},
        "when": {"en": "Cooler water, 15-25 °C. Mostly in nursery and rearing ponds and in crowded ponds.",
                 "kn": "ತಂಪಾದ ನೀರು, 15-25 °C. ಹೆಚ್ಚಾಗಿ ನರ್ಸರಿ ಮತ್ತು ಪಾಲನಾ ಕೊಳಗಳಲ್ಲಿ ಮತ್ತು ದಟ್ಟ ಕೊಳಗಳಲ್ಲಿ."},
        "prevention": [
            {"en": "Keep new fingerlings apart and check them before stocking.",
             "kn": "ಹೊಸ ಮರಿಗಳನ್ನು ಪ್ರತ್ಯೇಕವಾಗಿಟ್ಟು ಬಿಡುವ ಮೊದಲು ಪರಿಶೀಲಿಸಿ."},
            {"en": "Rear fry at a sensible density.", "kn": "ಮರಿಗಳನ್ನು ಸೂಕ್ತ ಸಂಖ್ಯೆಯಲ್ಲಿ ಬೆಳೆಸಿ."},
        ],
        "do": [],
        "sources": ["naca1985", "naca1989"],
    },
    "anchor_worm": {
        "name": {"en": "Anchor worm (Lernaea)", "kn": "ಲಂಗರು ಹುಳು (ಲರ್ನಿಯಾ)"},
        "cause": "crustacean",
        "agent": "Lernaea",
        "key_signs": ["threads"],
        "other_signs": ["red_patches", "thin_weak", "not_eating", "slow_surface", "cotton"],
        "body": {"en": "Thin, rod-like parasites stuck into the skin, anywhere on the body. Only the back end hangs out. The skin around is red, swollen and can rot; cotton-wool mould often grows there.",
                 "kn": "ದೇಹದ ಯಾವುದೇ ಭಾಗದಲ್ಲಿ ಚರ್ಮದೊಳಗೆ ಸಿಕ್ಕಿಕೊಂಡ ತೆಳುವಾದ ಕಡ್ಡಿಯಂತಹ ಪರಾವಲಂಬಿಗಳು. ಹಿಂಭಾಗ ಮಾತ್ರ ಹೊರಗೆ ನೇತಾಡುತ್ತದೆ. ಸುತ್ತಲಿನ ಚರ್ಮ ಕೆಂಪಾಗಿ, ಊದಿಕೊಂಡು ಕೊಳೆಯಬಹುದು; ಅಲ್ಲಿ ಹೆಚ್ಚಾಗಿ ಹತ್ತಿ ಬೂಷ್ಟು ಬೆಳೆಯುತ್ತದೆ."},
        "behaviour": {"en": "Fish are restless, eat less, get thin and move slowly. One or two worms can stunt a small fish.",
                      "kn": "ಮೀನುಗಳು ಚಡಪಡಿಸುತ್ತವೆ, ಕಡಿಮೆ ತಿನ್ನುತ್ತವೆ, ಸಣಕಲಾಗುತ್ತವೆ ಮತ್ತು ನಿಧಾನವಾಗಿ ಚಲಿಸುತ್ತವೆ. ಒಂದೆರಡು ಹುಳುಗಳು ಸಣ್ಣ ಮೀನಿನ ಬೆಳವಣಿಗೆ ಕುಂಠಿತಗೊಳಿಸಬಹುದು."},
        "when": {"en": "A long season in warm water (15-33 °C). Often in nursery and rearing ponds.",
                 "kn": "ಬೆಚ್ಚಗಿನ ನೀರಿನಲ್ಲಿ (15-33 °C) ದೀರ್ಘ ಕಾಲ. ಹೆಚ್ಚಾಗಿ ನರ್ಸರಿ ಮತ್ತು ಪಾಲನಾ ಕೊಳಗಳಲ್ಲಿ."},
        "prevention": [
            {"en": "Check fingerlings for worms before stocking.",
             "kn": "ಮರಿಗಳನ್ನು ಬಿಡುವ ಮೊದಲು ಹುಳುಗಳಿವೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ."},
            {"en": "Before stocking, dry the pond and remove wild fish.",
             "kn": "ಮೀನು ಬಿಡುವ ಮೊದಲು, ಕೊಳವನ್ನು ಒಣಗಿಸಿ ಮತ್ತು ಕಾಡು ಮೀನುಗಳನ್ನು ತೆಗೆದುಹಾಕಿ."},
        ],
        "do": [],
        "sources": ["naca1985", "naca1989"],
    },
}

# What to do for ANY suspected disease (no chemicals, no medicines).
COMMON_STEPS = [
    {"en": "Take out dead and dying fish every day. Dead fish spread disease.",
     "kn": "ಸತ್ತ ಮತ್ತು ಸಾಯುತ್ತಿರುವ ಮೀನುಗಳನ್ನು ಪ್ರತಿದಿನ ಹೊರತೆಗೆಯಿರಿ. ಸತ್ತ ಮೀನುಗಳು ರೋಗ ಹರಡುತ್ತವೆ."},
    {"en": "Do not move fish, water or nets from this pond to another pond.",
     "kn": "ಈ ಕೊಳದಿಂದ ಬೇರೆ ಕೊಳಕ್ಕೆ ಮೀನು, ನೀರು ಅಥವಾ ಬಲೆಗಳನ್ನು ಸಾಗಿಸಬೇಡಿ."},
    {"en": "Give less feed and keep the water quality good.",
     "kn": "ಕಡಿಮೆ ಆಹಾರ ನೀಡಿ ಮತ್ತು ನೀರಿನ ಗುಣಮಟ್ಟವನ್ನು ಚೆನ್ನಾಗಿಡಿ."},
    {"en": "Call your fisheries officer or KVK today. Take a few sick fish, alive or just dead and kept wet.",
     "kn": "ಇಂದೇ ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿ ಅಥವಾ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರಕ್ಕೆ (KVK) ಕರೆ ಮಾಡಿ. ಕೆಲವು ರೋಗಪೀಡಿತ ಮೀನುಗಳನ್ನು, ಜೀವಂತವಾಗಿ ಅಥವಾ ಈಗ ತಾನೇ ಸತ್ತು ಒದ್ದೆಯಾಗಿಟ್ಟು, ತೆಗೆದುಕೊಂಡು ಹೋಗಿ."},
]
COMMON_STEPS_SOURCES = ["naca1989", "naca1985", "semwal2023"]

TREATMENT_NOTE = {
    "en": "No medicines or chemicals here. Any treatment must be prescribed by a fisheries officer or KVK.",
    "kn": "ಇಲ್ಲಿ ಯಾವುದೇ ಔಷಧಿ ಅಥವಾ ರಾಸಾಯನಿಕಗಳಿಲ್ಲ. ಯಾವುದೇ ಚಿಕಿತ್ಸೆಯನ್ನು ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿ ಅಥವಾ KVK ಸೂಚಿಸಬೇಕು.",
}
NOT_A_DIAGNOSIS = {
    "en": "These are possible matches, not a diagnosis. Many fish diseases look alike. Confirm with your fisheries officer.",
    "kn": "ಇವು ಸಾಧ್ಯವಿರುವ ಹೊಂದಾಣಿಕೆಗಳು, ರೋಗನಿರ್ಣಯವಲ್ಲ. ಅನೇಕ ಮೀನು ರೋಗಗಳು ಒಂದೇ ರೀತಿ ಕಾಣುತ್ತವೆ. ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯೊಂದಿಗೆ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
}
NO_MATCH = {
    "en": "No disease in this guide matches these signs. Confirm with your fisheries officer.",
    "kn": "ಈ ಲಕ್ಷಣಗಳಿಗೆ ಈ ಮಾರ್ಗದರ್ಶಿಯ ಯಾವುದೇ ರೋಗ ಹೊಂದುವುದಿಲ್ಲ. ನಿಮ್ಮ ಮೀನುಗಾರಿಕೆ ಅಧಿಕಾರಿಯೊಂದಿಗೆ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
}
# Gasping is the classic sign of low oxygen (docs/actions.md), so say that first.
GASPING_NOTE = {
    "en": "Gasping at the surface is most often low oxygen, not disease. Check oxygen and run the aerator first.",
    "kn": "ಮೇಲ್ಮೈಯಲ್ಲಿ ಏದುಸಿರು ಹೆಚ್ಚಾಗಿ ಕಡಿಮೆ ಆಮ್ಲಜನಕದಿಂದ, ರೋಗದಿಂದಲ್ಲ. ಮೊದಲು ಆಮ್ಲಜನಕ ಪರಿಶೀಲಿಸಿ ಮತ್ತು ಏರೇಟರ್ ಚಾಲೂ ಮಾಡಿ.",
}
MAX_MATCHES = 3

# Risky readings that make a disease more likely: (parameter, direction) -> [(disease, why, sources)].
# Only links stated in the sources; see docs/diseases.md.
READING_LINKS = {
    ("dissolved_oxygen", "low"): [
        ("aeromoniasis", {"en": "Low oxygen stresses fish and is linked to Aeromonas outbreaks.",
                          "kn": "ಕಡಿಮೆ ಆಮ್ಲಜನಕ ಮೀನುಗಳಿಗೆ ಒತ್ತಡ ತರುತ್ತದೆ ಮತ್ತು ಏರೋಮೋನಾಸ್ ರೋಗಕ್ಕೆ ಸಂಬಂಧಿಸಿದೆ."},
         ["semwal2023", "snieszko1974"]),
    ],
    ("ammonia", "high"): [
        ("aeromoniasis", {"en": "High ammonia makes fish more likely to catch Aeromonas.",
                          "kn": "ಹೆಚ್ಚಿನ ಅಮೋನಿಯಾ ಮೀನುಗಳಿಗೆ ಏರೋಮೋನಾಸ್ ಸೋಂಕು ತಗಲುವ ಸಾಧ್ಯತೆ ಹೆಚ್ಚಿಸುತ್ತದೆ."},
         ["flagg1978", "snieszko1974"]),
    ],
    ("temperature", "high"): [
        ("columnaris", {"en": "Columnaris spreads more easily in warmer water.",
                        "kn": "ಬೆಚ್ಚಗಿನ ನೀರಿನಲ್ಲಿ ಕಾಲಮ್ನಾರಿಸ್ ಸುಲಭವಾಗಿ ಹರಡುತ್ತದೆ."},
         ["naca1985", "declercq2013"]),
        ("gill_disease", {"en": "Gill rot is worst at 28-35 °C.", "kn": "ಕಿವಿರು ಕೊಳೆ 28-35 °C ನಲ್ಲಿ ಹೆಚ್ಚು."},
         ["naca1989"]),
        ("aeromoniasis", {"en": "High water temperature stresses fish and is linked to Aeromonas outbreaks.",
                          "kn": "ಹೆಚ್ಚಿನ ನೀರಿನ ತಾಪಮಾನ ಮೀನುಗಳಿಗೆ ಒತ್ತಡ ತರುತ್ತದೆ ಮತ್ತು ಏರೋಮೋನಾಸ್ ರೋಗಕ್ಕೆ ಸಂಬಂಧಿಸಿದೆ."},
         ["semwal2023"]),
    ],
    ("temperature", "low"): [
        ("eus", {"en": "EUS outbreaks happen at low water temperatures.",
                 "kn": "ಕಡಿಮೆ ನೀರಿನ ತಾಪಮಾನದಲ್ಲಿ EUS ಹರಡುತ್ತದೆ."},
         ["fao2001"]),
        ("white_spot", {"en": "The white spot parasite multiplies best at 15-25 °C.",
                        "kn": "ಬಿಳಿ ಚುಕ್ಕೆ ಪರಾವಲಂಬಿ 15-25 °C ನಲ್ಲಿ ಹೆಚ್ಚು ವೃದ್ಧಿಯಾಗುತ್ತದೆ."},
         ["naca1989"]),
    ],
    ("ph", "low"): [
        ("eus", {"en": "EUS outbreaks are linked to acidic water.",
                 "kn": "EUS ಹರಡುವಿಕೆ ಆಮ್ಲೀಯ ನೀರಿಗೆ ಸಂಬಂಧಿಸಿದೆ."},
         ["fao2001"]),
    ],
}
LIKELY_NOTE = {
    "en": "This does not mean your fish are sick. Watch them closely and use the Fish disease guide if you see signs.",
    "kn": "ಇದರ ಅರ್ಥ ನಿಮ್ಮ ಮೀನುಗಳಿಗೆ ರೋಗ ಬಂದಿದೆ ಎಂದಲ್ಲ. ಅವುಗಳನ್ನು ಗಮನವಿಟ್ಟು ನೋಡಿ, ಲಕ್ಷಣಗಳು ಕಂಡರೆ ಮೀನು ರೋಗ ಮಾರ್ಗದರ್ಶಿ ಬಳಸಿ.",
}


def check(signs: list[str]) -> dict:
    """
    Possible matches for the ticked signs, best first (at most MAX_MATCHES).
    A disease scores 2 for each of its key signs that was ticked and 1 for each
    other sign. The result always carries the "not a diagnosis" note.
    """
    ticked = [s for s in dict.fromkeys(signs) if s in SIGNS]
    matches = []
    for disease_id, d in DISEASES.items():
        key = [s for s in ticked if s in d["key_signs"]]
        other = [s for s in ticked if s in d["other_signs"]]
        score = 2 * len(key) + len(other)
        if score:
            matches.append({"id": disease_id, "name": d["name"], "score": score,
                            "matched_signs": key + other})
    # Highest score first; on a tie, the disease that explains more of the ticked signs.
    matches.sort(key=lambda m: (-m["score"], -len(m["matched_signs"])))
    notes = [GASPING_NOTE] if "gasping" in ticked else []
    return {
        "signs": ticked,
        "matches": matches[:MAX_MATCHES],
        "more": max(0, len(matches) - MAX_MATCHES),
        "notes": notes,
        "message": NOT_A_DIAGNOSIS if matches else NO_MATCH,
        "treatment_note": TREATMENT_NOTE,
    }


def likely_diseases(risk: dict) -> list[dict]:
    """Diseases made more likely by the Warning/Danger readings in `risk` (from classify().to_dict())."""
    found: dict[str, dict] = {}
    for p in risk.get("parameters", []):
        if p["level"] not in ("warning", "danger"):
            continue
        for disease_id, why, sources in READING_LINKS.get((p["parameter"], p["direction"]), []):
            entry = found.setdefault(disease_id, {"id": disease_id, "name": DISEASES[disease_id]["name"],
                                                  "reasons": [], "sources": []})
            entry["reasons"].append(why)
            entry["sources"] += [s for s in sources if s not in entry["sources"]]
    return list(found.values())


def library() -> dict:
    """Everything the page needs to show the guide (no doses anywhere)."""
    return {
        "signs": SIGNS,
        "cause_types": CAUSE_TYPES,
        "diseases": DISEASES,
        "common_steps": COMMON_STEPS,
        "treatment_note": TREATMENT_NOTE,
        "not_a_diagnosis": NOT_A_DIAGNOSIS,
        "likely_note": LIKELY_NOTE,
        "sources": SOURCES,
    }
