# Image-based fish disease detection: research plan

Status: **research only**. Nothing has been trained yet. Researched 4 October 2026.

PS 1.1 mentions "image-based disease detection". The idea: a farmer photographs a sick-looking fish,
and the app says which disease it *might* be, in Kannada and English, with advice to confirm with a
fisheries officer. This page covers which datasets exist, which one to use, and what model to build.

## Summary

- **No public dataset covers rohu or catla diseases properly.** Some papers report rohu disease
  models (for example a hybrid CNN tested on 1,672 diseased rohu images), but they did not release their data.
- **Best option: Biswas et al., "Freshwater Fish Disease Aquaculture in South Asia"** (Kaggle, CC0).
  It has 7 freshwater classes, partly collected in Odisha, India, and a licence that allows anything.
  It also has serious quality problems (see below). We must clean it before training, and our
  accuracy numbers will be lower than the 95–99 % that papers report on it.
- **Model:** MobileNetV3-Small, starting from a model that is already trained on general images
  (transfer learning). Export it to ONNX (about 2–3 MB after int8 quantisation) and run it **in
  the browser** with ONNX Runtime Web. Photos never leave the phone and it works offline.
- **Training time:** about 15–30 minutes on your laptop's CPU, or about 5 minutes on a free Kaggle
  T4 GPU. Both are fine for a dataset this size.

## Datasets found

Image counts were taken from each dataset's file list using the Kaggle API, not from the descriptions.
"Median file size" gives a rough idea of image quality.

| # | Dataset | Classes | Images | Species | Quality | Licence |
|---|---|---|---|---|---|---|
| 1 | [Freshwater Fish Disease Aquaculture in South Asia](https://www.kaggle.com/datasets/subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia) (Biswas et al., IEEE Access 2024) | 7: Aeromoniasis, Bacterial gill disease, Bacterial red disease, Saprolegniasis (fungal), Parasitic, "White tail" (viral), Healthy | 2,450 (250 train + 100 test per class). **Only ~1,700 unique** after removing exact duplicates (see below) | Mixed: carp, goldfish, koi, salmon, others. No species labels | Low: 128×128 or 224×224, ~3 KB each, many pre-rotated/stretched copies | **CC0** (public domain) |
| 2 | [Fresh Water Fish Disease Dataset](https://www.kaggle.com/datasets/utpolkantidas/fresh-water-fish-disease-dataset) (Kaptai Lake, Bangladesh) | 7: EUS, Red spot, Argulus, Bacterial gill rot, Tail and fin rot, Broken antennae and rostrum (prawn), Healthy | **133** (6–31 per class) | Real Bangladesh catch, including rohu, catla, mrigal | Small (~16 KB) but real fish | **Unknown**: we would need the author's permission |
| 3 | [BD Fish & Shrimp Disease](https://huggingface.co/datasets/Saon110/bd-fish-disease-dataset) (Hugging Face) | Same 7 fish classes as #1, plus 4 shrimp classes | 5,887 (2,082 fish) | As #1, plus shrimp | As #1. The fish part is a copy of #1 | CC BY-NC-SA 4.0 |
| 4 | [Fish Disease Image Datasets](https://www.kaggle.com/datasets/moonburntcat/fish-disease-image-datasets) | 5: EUS, Bacterial, Fungal, Parasitic, Viral. **No healthy class**; folders are just named 1–5 | 2,055 (~410 per class) | 11 species: carp, crucian carp, tilapia, goldfish, salmon, marine fish | Medium (~52 KB) | CC BY-SA 4.0 |
| 5 | [Diseases in Tilapia](https://www.kaggle.com/datasets/chanachai2001/diseases-in-tilapia) (Mekong basin) | 5: Streptococcosis, Parasitic, Tilapia lake virus, Motile Aeromonas septicemia, Normal | 1,795 (325–395 per class) | Nile tilapia | Good (~77 KB), real farm photos | CC BY-NC-SA 4.0 |
| 6 | [Enhancing Disease Detection in Nile Tilapia](https://www.kaggle.com/datasets/engineeringubu/enhancing-disease-detection-in-nile-tilapia) (NTD-1/NTD-2, Ubon Ratchathani Univ.) | 6 diseases + healthy (Columnaris, MAS, Parasitic, Streptococcosis, TiLV, Normal) | 3,054 | Nile tilapia, 3 commercial farms in Thailand | Good (~77 KB) | CC BY-NC-SA 4.0 |
| 7 | [SalmonScan](https://data.mendeley.com/datasets/x3fz2nfm4w/3) (Mendeley Data) | 2: Healthy, Infected | 1,208, all augmented from **115 originals** | Salmon | 600×250, augmented | CC BY 4.0 |

Also looked at, but **not disease datasets**: BD-Freshwater-Fish (Mendeley, 4,389 images of 12 species,
including rohu and catla; species ID only), a rohu freshness dataset (Kaggle), Fish-Pak, and TilapiaVision
(healthy fish only). These could help later with a "is this a fish / which species" check.

## What I found when checking dataset #1

I downloaded the Hugging Face copy of #1 (2,082 train + 368 test images, which matches the Kaggle file
count) and checked it:

1. **Duplicates.** 528 of the 2,082 training images are exact byte-for-byte copies of other images.
2. **Test images that are also in the training set.** 163 of the 368 test images (44 %) are exact copies
   of training images, and 171 (46 %) are near-copies. This is the main reason papers report 95–99 %
   accuracy: the model has already seen almost half of the test images while training.
3. **Pre-augmented images.** Many images are already rotated, flipped, or stretched at the edges. These
   are copies of the same fish, not new fish.
4. **The "Healthy" class is mostly stock photos**, for example a smiling angler holding a carp next to a
   lake, while the disease classes are close-ups on lab tables. A model can learn "lake background =
   healthy" instead of learning what the fish looks like. This is called *shortcut learning*.
5. **Label oddities.** "White tail disease" is normally a disease of freshwater prawn, but this class
   contains goldfish and other fish. "Parasitic diseases" is one broad class: it does not tell
   *Argulus* (fish louse) apart from other parasites.

None of these problems makes the dataset unusable. They do mean we must clean it and report honest numbers.

## Recommendation: dataset #1, cleaned, with #2 as an optional real-world check

**Why #1:**
- **Licence.** It is CC0, so we can use it, ship the model, and show example images without asking anyone.
  #3–#6 are non-commercial or share-alike, which is OK for a hackathon but limits later use.
  #2 has no licence at all.
- **Closest to our users.** It covers freshwater pond diseases common in Indian carp culture (Aeromonas,
  gill disease, red disease, Saprolegnia) and was partly collected in Odisha.
- **Enough images per class** for transfer learning, even after removing duplicates (~240 per class).
- **Easy to download:** 26 MB.

**Why not the others:** the tilapia sets (#5, #6) are the best-quality data, but they are for tilapia
and use diseases (TiLV, Streptococcosis) that matter less for Karnataka carp ponds. #4 has no healthy
class and unnamed folders. #7 is salmon, built from only 115 real photos.

**Dataset #2** is tiny, but it has *real* rohu, catla, and mrigal with EUS, red spot, and Argulus, which
are the diseases Karnataka farmers actually see. Use it only as a small **extra test set** to see how
the model does on Indian carps, and only after asking the author for permission (licence "Unknown").

**Cleaning steps before training:**
1. Remove exact duplicates (MD5 hash) and near-duplicates (perceptual hash).
2. Merge the original train and test folders, then make a **new** train / validation / test split
   (70/15/15) so the same fish never appears in two splits.
3. Look at every "Healthy" image and remove obvious stock photos with people or scenery, or crop them to the fish.
4. Report accuracy on the cleaned test set only, and say in the README that the original split leaks.

## Model approach

**Transfer learning with MobileNetV3-Small.** We start with a network that has already learned general
image features from ImageNet (1.2 million photos), and retrain only the last layers on our ~1,700 fish
images. Training a model from scratch would need far more data.

| Option | Size (int8) | Runs where | Notes |
|---|---|---|---|
| **MobileNetV3-Small** (recommended) | ~2–3 MB | Browser (ONNX Runtime Web or TensorFlow.js) | Fast on cheap Android phones (~50 ms per photo) |
| EfficientNet-Lite0 / B0 | ~5 MB | Browser or server | A little more accurate and a little slower |
| Frozen MobileNet features + scikit-learn LogisticRegression | ~3 MB + tiny | Server or browser | Simplest. Uses scikit-learn, which you already know. A good first step |

**Run it in the browser, not on Render.** The free Render server has 512 MB of RAM and goes to sleep
when idle. Adding PyTorch to it would make it heavier and slower. In the browser:
- the model file (~3 MB) is cached once and then **works offline**, which matters at ponds with weak signal;
- the farmer's photo **never leaves the phone**;
- the server does no extra work.

**Pipeline:** PyTorch + `timm` (training, on Kaggle) → export to ONNX → int8 quantisation →
`onnxruntime-web` in `frontend/`. Input: 224×224 photo. Output: top-3 classes with confidence.

**Safety rules for the app (same spirit as the simulated-data rule):**
- Always say **"possible sign of…"**, never "your fish has…". Show "Please confirm with your fisheries
  officer / KVK" in Kannada and English.
- If the top confidence is below about 60 %, or the photo is not a fish, show "Not sure, please take a
  clearer photo" instead of a guess.
- Label results as "Trained on public images, mostly not Indian carps".
- Training images must never be shown to users as if they were the farmer's own pond.

## Training time estimates

Your laptop: AMD Ryzen 5 7520U (4 cores), 16 GB RAM, integrated Radeon graphics. **No NVIDIA GPU**, so
training would run on the CPU. Neither PyTorch nor TensorFlow is installed yet.

These are estimates, not measurements: about 1,200 training images after cleaning (70 % of ~1,700), 224×224 input.

| Approach | Laptop (CPU) | Kaggle free GPU (T4 / P100) |
|---|---|---|
| Frozen features + scikit-learn LogisticRegression | ~2–4 min (feature extraction), then seconds | ~1 min |
| MobileNetV3-Small fine-tune, 20 epochs | ~15–30 min | ~3–5 min |
| EfficientNet-B0 fine-tune, 20 epochs | ~45–90 min | ~5–10 min |

Both options work. **Kaggle is better** because the dataset is already on Kaggle (no download), you
get 30 free GPU hours a week, and your laptop stays free. Export the ONNX file from the notebook and
commit it to `frontend/models/`.

## Next steps (when we decide to build it)

1. Kaggle notebook: download #1, remove duplicates, make the new split, and save a cleaning report.
2. Baseline: frozen MobileNetV3 features + LogisticRegression. Write the honest accuracy to `docs/`.
3. Fine-tune MobileNetV3-Small, export to ONNX, quantise to int8, and check the size is under 5 MB.
4. Add a "Check a fish photo" page using `onnxruntime-web`, styled per DESIGN.md, with Kannada and
   English text and the safety rules above.
5. Ask the author of #2 for permission. If they agree, report accuracy on real rohu/catla/mrigal photos separately.

## Sources

- Biswas et al., [Empirical Evaluation of Deep Learning Techniques for Fish Disease Detection in Aquaculture Systems](https://ieeexplore.ieee.org/abstract/document/10759657), IEEE Access 2024 (paper behind dataset #1)
- [panda992/fish_disease_datasets](https://huggingface.co/datasets/panda992/fish_disease_datasets): Hugging Face copy of #1, used for the duplicate check
- [Adaptive artificial multiple intelligence fusion system for Nile Tilapia](https://www.sciencedirect.com/science/article/pii/S2352513424005064) (NTD-1/NTD-2 paper)
- [SalmonScan, Data in Brief](https://www.sciencedirect.com/science/article/pii/S2352340924003573)
- [BD-Freshwater-Fish, Data in Brief 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11648155/) (species only, includes rohu and catla)
- [Fish Type and Disease Classification for Indian Major Carp](https://www.researchgate.net/publication/378717978_Fish_Type_and_Disease_Classification_Using_Deep_Learning_Model_Based_Customized_CNN_with_Resnet_50_Technique) (data not public)
- [SLCAM-AquaNet](https://link.springer.com/article/10.1007/s42452-026-08461-z): lightweight model for catla/rohu disease (data not public)
