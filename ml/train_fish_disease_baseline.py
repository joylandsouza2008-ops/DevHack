"""
Step 2 of docs/disease-detection-plan.md: a simple, honest baseline for fish-disease photos.

Run from the project folder AFTER python -m ml.clean_fish_disease (takes about 2 minutes on a laptop CPU):
    python -m ml.train_fish_disease_baseline

Idea: a MobileNetV3 network that was already trained on ImageNet (1.2 million everyday photos) turns
each fish photo into a list of numbers ("features"). We do NOT retrain the network ("frozen").
A scikit-learn LogisticRegression then learns which feature patterns go with which disease.

What it does, step by step:
  1. Load the cleaned images and their train / val / test split (data/fish-disease/clean/manifest.csv).
  2. Features from MobileNetV3-Small (the size we would run in a phone browser) and, for comparison,
     MobileNetV3-Large.
  3. Pick the regularisation strength C on the VALIDATION set (best macro-F1), then retrain on
     train + val and score the TEST set once. The test set is not looked at before that.
  4. Extra honesty checks:
       - "always guess the biggest class" baseline;
       - 95 % ranges for test scores, by resampling whole photo groups (bootstrap);
       - background-only test: grey out the middle of every photo and train again. If the model
         still scores well, it is reading backgrounds / photo style, not disease signs;
       - the ORIGINAL Kaggle split (6 classes, raw files) to show how leakage inflates the score.
  5. Save numbers (models/fish_disease_baseline_metrics.json), a confusion-matrix chart
     (docs/figures/fish_disease_baseline_confusion.png) and the report (docs/fish-disease-baseline.md).

No model file is saved: this is a measurement, not something the app uses.
"""

from __future__ import annotations

import csv
import json
import warnings
from collections import Counter, defaultdict
from datetime import datetime, timezone

import matplotlib

matplotlib.use("Agg")  # draw charts to files, no window
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score, \
    precision_recall_fscore_support
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from ml.fish_disease_common import (
    C_INK, C_MUTED, CLASS_IDS, CLASS_LABELS, CLASSES, CLEAN_DIR, DROPPED_CLASSES, MANIFEST, PROJECT, RAW_DIR,
    embed, load_backbone, load_rgb,
)

METRICS_FILE = PROJECT / "models" / "fish_disease_baseline_metrics.json"
CHART_FILE = PROJECT / "docs" / "figures" / "fish_disease_baseline_confusion.png"
REPORT_FILE = PROJECT / "docs" / "fish-disease-baseline.md"

SEED = 42
C_GRID_VALUES = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0]
N_BOOTSTRAP = 2000
MASK_FRACTION = 0.6  # background-only test: grey box over the middle 60 % of width and height


def load_manifest():
    with open(MANIFEST, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    images = [load_rgb(CLEAN_DIR / r["file"]) for r in rows]
    return rows, images


def mask_centre(im: Image.Image) -> Image.Image:
    """Grey out the middle of the photo, leaving only the border (mostly background)."""
    im = im.copy()
    w, h = im.size
    mw, mh = int(w * MASK_FRACTION), int(h * MASK_FRACTION)
    box = ((w - mw) // 2, (h - mh) // 2, (w - mw) // 2 + mw, (h - mh) // 2 + mh)
    im.paste((124, 116, 104), box)  # ImageNet average colour = "nothing here" for the network
    return im


def model_for(c: float):
    """Scale each feature to mean 0 / std 1, then a LogisticRegression. class_weight='balanced' so the
    big Healthy class does not drown out the small disease classes."""
    return make_pipeline(StandardScaler(),
                         LogisticRegression(C=c, max_iter=5000, class_weight="balanced"))


def fit_and_score(X, y, split):
    """Choose C on validation, retrain on train+val, score test. Returns (chosen C, val scores, test predictions)."""
    tr, va, te = split == "train", split == "val", split == "test"
    val_scores = {}
    for c in C_GRID_VALUES:
        pred = model_for(c).fit(X[tr], y[tr]).predict(X[va])
        val_scores[c] = f1_score(y[va], pred, average="macro")
    best_c = max(val_scores, key=lambda c: (round(val_scores[c], 4), -c))  # ties -> stronger regularisation
    final = model_for(best_c).fit(X[tr | va], y[tr | va])
    return best_c, val_scores, final.predict(X[te])


def scores(y_true, y_pred) -> dict:
    return {"accuracy": accuracy_score(y_true, y_pred),
            "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
            "macro_f1": f1_score(y_true, y_pred, average="macro")}


def group_bootstrap(y_true, y_pred, groups, n=N_BOOTSTRAP) -> dict:
    """95 % range of each score when we resample whole photo groups (copies of one fish move together)."""
    rng = np.random.default_rng(SEED)
    by_group = defaultdict(list)
    for i, g in enumerate(groups):
        by_group[g].append(i)
    glist = list(by_group.values())
    out = defaultdict(list)
    warnings.filterwarnings("ignore", message="y_pred contains classes not in y_true")  # a resample can miss a class
    for _ in range(n):
        idx = np.concatenate([glist[k] for k in rng.integers(0, len(glist), len(glist))])
        for k, v in scores(y_true[idx], y_pred[idx]).items():
            out[k].append(v)
    return {k: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] for k, v in out.items()}


def original_split_score(model, prep) -> dict:
    """Same method on the ORIGINAL Kaggle Train/Test folders (6 classes, no cleaning) - to show the leak."""
    data = {"Train": ([], []), "Test": ([], [])}
    for split in data:
        for folder in sorted((RAW_DIR / split).iterdir()):
            if folder.name in DROPPED_CLASSES:
                continue
            for path in sorted(folder.iterdir()):
                data[split][0].append(load_rgb(path))
                data[split][1].append(CLASSES[folder.name])
    Xtr, Xte = embed(data["Train"][0], model, prep), embed(data["Test"][0], model, prep)
    pred = model_for(0.1).fit(Xtr, data["Train"][1]).predict(Xte)
    return {"n_train": len(Xtr), "n_test": len(Xte), **scores(np.array(data["Test"][1]), pred)}


def draw_confusion(y_true, y_pred, title: str) -> None:
    cm = confusion_matrix(y_true, y_pred, labels=CLASS_IDS)
    share = cm / cm.sum(axis=1, keepdims=True)
    cmap = LinearSegmentedColormap.from_list("blue", ["#ffffff", "#d6e6f7", "#7fb0e6", "#2a78d6", "#14457f"])
    fig, ax = plt.subplots(figsize=(7.6, 6.4))
    ax.imshow(share, cmap=cmap, vmin=0, vmax=1)
    labels = [CLASS_LABELS[c] for c in CLASS_IDS]
    for i in range(len(CLASS_IDS)):
        for j in range(len(CLASS_IDS)):
            if cm[i, j] == 0:
                continue
            dark = share[i, j] > 0.55
            ax.text(j, i - 0.1, str(cm[i, j]), ha="center", va="center", fontsize=12, fontweight="bold",
                    color="white" if dark else C_INK)
            ax.text(j, i + 0.22, f"{share[i, j]:.0%}", ha="center", va="center", fontsize=8.5,
                    color="white" if dark else C_MUTED)
    ax.set_xticks(range(len(labels)), labels, rotation=30, ha="right")
    ax.set_yticks(range(len(labels)), [f"{lab}  (n={n})" for lab, n in zip(labels, cm.sum(axis=1))])
    ax.tick_params(colors=C_INK, labelsize=9.5, length=0)
    ax.set_xlabel("Model's guess", color=C_INK, fontsize=10.5)
    ax.set_ylabel("True class", color=C_INK, fontsize=10.5)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(np.arange(-0.5, len(labels)), minor=True)
    ax.set_yticks(np.arange(-0.5, len(labels)), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)
    fig.suptitle(title, x=0.01, ha="left", fontsize=12, color=C_INK, fontweight="bold")
    fig.text(0.01, 0.01, "Number = test images; % = share of that true class (each row adds up to 100 %). "
             "Diagonal = correct.", fontsize=8, color=C_MUTED)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(CHART_FILE, dpi=150, facecolor="white")
    plt.close(fig)


def main() -> None:
    print("1. Loading cleaned images...")
    rows, images = load_manifest()
    y = np.array([r["class"] for r in rows])
    split = np.array([r["split"] for r in rows])
    groups = np.array([r["group"] for r in rows])
    te = split == "test"
    counts = {s: Counter(y[split == s]) for s in ["train", "val", "test"]}
    print("   " + ", ".join(f"{s}: {sum(c.values())}" for s, c in counts.items()))

    results = {}
    predictions = {}
    for name in ["small", "large"]:
        print(f"2. MobileNetV3-{name.title()} features + LogisticRegression...")
        model, prep = load_backbone(name)
        X = embed(images, model, prep)
        best_c, val_scores, pred = fit_and_score(X, y, split)
        predictions[name] = pred
        p, r, f, n = precision_recall_fscore_support(y[te], pred, labels=CLASS_IDS, zero_division=0)
        results[name] = {
            "chosen_C": best_c,
            "val_macro_f1_by_C": {str(c): round(v, 4) for c, v in val_scores.items()},
            "test": scores(y[te], pred),
            "test_95pct_range": group_bootstrap(y[te], pred, groups[te]),
            "per_class": {c: {"precision": float(p[i]), "recall": float(r[i]), "f1": float(f[i]), "n": int(n[i])}
                          for i, c in enumerate(CLASS_IDS)},
            "confusion_matrix": confusion_matrix(y[te], pred, labels=CLASS_IDS).tolist(),
        }
        print(f"   C={best_c}  test accuracy {results[name]['test']['accuracy']:.3f}, "
              f"macro-F1 {results[name]['test']['macro_f1']:.3f}")
        if name == "small":
            print("3. Background-only test (middle of each photo greyed out)...")
            Xb = embed([mask_centre(im) for im in images], model, prep)
            _, _, pred_bg = fit_and_score(Xb, y, split)
            results["background_only_small"] = {"test": scores(y[te], pred_bg),
                                                 "test_95pct_range": group_bootstrap(y[te], pred_bg, groups[te])}
            print(f"   test accuracy {results['background_only_small']['test']['accuracy']:.3f}")
            print("4. Original (leaky) Kaggle split, for comparison...")
            results["original_kaggle_split_small"] = original_split_score(model, prep)
            print(f"   test accuracy {results['original_kaggle_split_small']['accuracy']:.3f}")

    majority = Counter(y[split != "test"]).most_common(1)[0][0]
    results["majority_class"] = {"always_guess": majority, **scores(y[te], np.full(te.sum(), majority))}

    out = {
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": "Research only, not used by the app. Cleaned dataset #1 (docs/fish-disease-cleaning.md), 6 classes.",
        "n_images": {s: dict(c) for s, c in counts.items()},
        **results,
    }
    METRICS_FILE.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print("5. Chart and report...")
    acc = results["small"]["test"]["accuracy"]
    draw_confusion(y[te], predictions["small"],
                   f"Frozen MobileNetV3-Small + LogisticRegression, cleaned test set: {acc:.0%} correct")
    write_report(out)
    print(f"   done: {METRICS_FILE.relative_to(PROJECT)}, {REPORT_FILE.relative_to(PROJECT)}, "
          f"{CHART_FILE.relative_to(PROJECT)}")


def pct(x: float) -> str:
    return f"{x * 100:.0f} %"


def rng_txt(r) -> str:
    return f"{r[0] * 100:.0f}–{r[1] * 100:.0f} %"


def write_report(m: dict) -> None:
    s, l, bg, orig, maj = (m["small"], m["large"], m["background_only_small"], m["original_kaggle_split_small"],
                           m["majority_class"])
    n = m["n_images"]
    n_test = sum(n["test"].values())

    per_class = ["| Class | Test images | Precision | Recall | F1 |", "|---|---:|---:|---:|---:|"]
    for c in CLASS_IDS:
        pc = s["per_class"][c]
        per_class.append(f"| {CLASS_LABELS[c]} | {pc['n']} | {pct(pc['precision'])} | {pct(pc['recall'])} | "
                         f"{pct(pc['f1'])} |")

    def row(name, d, r=None):
        rr = r or {}
        return (f"| {name} | {pct(d['accuracy'])}" + (f" ({rng_txt(rr['accuracy'])})" if rr else "")
                + f" | {pct(d['balanced_accuracy'])} | {pct(d['macro_f1'])}"
                + (f" ({rng_txt(rr['macro_f1'])})" if rr else "") + " |")

    # biggest off-diagonal confusions
    cm = np.array(s["confusion_matrix"])
    off = sorted(((cm[i, j], i, j) for i in range(len(CLASS_IDS)) for j in range(len(CLASS_IDS)) if i != j),
                 reverse=True)[:3]
    confusions = "; ".join(f"{CLASS_LABELS[CLASS_IDS[i]]} → {CLASS_LABELS[CLASS_IDS[j]]} ({v})"
                           for v, i, j in off if v > 0)

    text = f"""# Fish-disease photos: baseline model

Step 2 of [disease-detection-plan.md](disease-detection-plan.md). Made by `python -m ml.train_fish_disease_baseline`.
Research only. **Nothing here is used by the app.**

## Setup

- Data: the cleaned dataset from [fish-disease-cleaning.md](fish-disease-cleaning.md). 6 classes. Split by photo
  group, so no copy of a test photo is in training. Train {sum(n['train'].values())}, validation
  {sum(n['val'].values())}, **test {n_test}** images.
- Model: MobileNetV3 pre-trained on ImageNet, **frozen** (not retrained), turns each photo into a list of numbers.
  A scikit-learn `LogisticRegression` (with `class_weight="balanced"`, because Healthy is much bigger) learns the
  classes from those numbers.
- C (how strongly the model is kept simple) was chosen on the validation set; the final model was trained on
  train + validation and scored **once** on the test set.
- Ranges in brackets are 95 % bootstrap ranges, resampling whole photo groups. With so few test images per class
  they are wide, and that is the honest picture.

## Results on the cleaned test set

| Model | Accuracy | Balanced accuracy | Macro-F1 |
|---|---:|---:|---:|
{row("**MobileNetV3-Small** + LogReg (C = " + str(s['chosen_C']) + ")", s['test'], s['test_95pct_range'])}
{row("MobileNetV3-Large + LogReg (C = " + str(l['chosen_C']) + ")", l['test'], l['test_95pct_range'])}
{row("Always guess *" + CLASS_LABELS[maj['always_guess']] + "*", maj)}
{row("Background only (Small, middle 60 % greyed out)", bg['test'], bg['test_95pct_range'])}
{row("Original Kaggle split, no cleaning (Small)", orig)}

*Balanced accuracy* = the average of the per-class recalls, so every class counts equally.
*Macro-F1* = the average F1 over the 6 classes. Both matter more than plain accuracy here, because the classes
are unbalanced.

### Per class (MobileNetV3-Small)

{chr(10).join(per_class)}

*Precision*: when the model says this class, how often it is right. *Recall*: of the photos that really are this
class, how many it finds.

![Confusion matrix](figures/fish_disease_baseline_confusion.png)

Most common mistakes: {confusions}.

## What these numbers mean

- **The original split's {pct(orig['accuracy'])} is not real.** On Kaggle's own Train/Test folders the same method
  scores {pct(orig['accuracy'])}, because every test image is also a training image. Papers reporting 95–99 % on this
  dataset have the same problem. On the cleaned split the honest number is **{pct(s['test']['accuracy'])}**.
- **Background-only score: {pct(bg['test']['accuracy'])}.** With the middle of every photo greyed out, the model still
  gets {pct(bg['test']['accuracy'])} right, against {pct(s['test']['accuracy'])} with the whole photo and
  {pct(maj['accuracy'])} for always guessing the biggest class. So a large part of the score comes from the
  background, photo style and species (stock photos of carp = Healthy; aquarium fish and lab close-ups = disease),
  not from disease signs. The border can still show parts of the fish, so this test overstates the shortcut a
  little, but the shortcut is clearly there. The high Healthy score ({pct(s['per_class']['healthy']['recall'])}
  found) is probably mostly this effect.
- **Bigger network, same result.** MobileNetV3-Large is not clearly better than Small
  ({pct(l['test']['accuracy'])} vs {pct(s['test']['accuracy'])}; the ranges overlap almost completely). The limit is the
  data, not the network size.
- **Test set is tiny.** {n_test} images, some classes with fewer than 15. One or two photos change a class's recall
  by 10 percentage points, so per-class numbers are rough.
- **Not tested on Indian carps.** These are mostly goldfish, aquarium fish and stock-photo carp. Results on rohu,
  catla or mrigal in a Karnataka pond will be lower and are unknown.

## Next

Step 3 (fine-tuning MobileNetV3-Small) has **not** been started. Before it, it is worth deciding whether this data
is good enough, given the background shortcut above. Possible fixes: crop every image to the fish, or add a second
dataset with healthy *and* sick fish photographed the same way.
"""
    REPORT_FILE.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
