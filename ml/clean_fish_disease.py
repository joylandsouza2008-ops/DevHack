"""
Step 1 of docs/disease-detection-plan.md: clean the fish-disease photos and make a new, honest split.

Run from the project folder (takes about 4 minutes on a laptop CPU):
    python -m ml.clean_fish_disease
    python -m ml.clean_fish_disease --reuse-pairs   (re-use the saved near-duplicate pairs: ~20 seconds)

Input:  data/fish-disease/Freshwater Fish Disease Aquaculture in south asia/{Train,Test}/<class>/
        ml/fish_disease_healthy_review.csv   (my by-eye decisions for the "Healthy" photos)
Output: data/fish-disease/clean/{train,val,test}/<class>/   cleaned images (not in git)
        data/fish-disease/clean/manifest.csv                one row per kept image
        docs/fish-disease-split.csv                         same list, kept in git so the split is fixed
        docs/fish-disease-cleaning.md                       the cleaning report
        docs/figures/fish_disease_cleaning_examples.png     examples of removed / cropped images

What it does, step by step:
  1. Read every image from the original Train AND Test folders (the original Test folder is
     entirely copied from Train, so its split is useless). Skip the "White tail" class.
  2. Exact duplicates: two files with identical pixels are one image. If the same image is
     filed under two different diseases, it is removed (we can't know which label is right).
  3. Near-duplicates: the dataset is "pre-augmented": one photo is saved many times rotated,
     zoomed, mirrored or with stretched edges. We find these copies in three stages:
       a. candidates: for each image, its 15 most similar images by MobileNetV3 features
          (a pre-trained network's description of the image);
       b. perceptual hash (a 64-bit fingerprint of the picture; tiny differences = same photo);
       c. keypoint matching (OpenCV ORB): find the same small details in both images, fit a
          rotation + zoom that lines them up, overlay the images and measure how well they match.
     Images that match are joined into one "photo group" (also through chains: if A~B and B~C,
     then A, B, C are one group). Inside a group we keep the best copy and drop direct copies of it.
  4. Healthy review: stock photos with people (anglers, hands), scenery (underwater lake beds,
     fish jumping out of a lake), drawings and fishing lures are removed; a stock-photo watermark
     bar at the bottom is cropped off. Rotated copies of a removed photo are removed too.
  5. New 70 / 15 / 15 split, done per class and per photo GROUP, so copies or other shots of the
     same fish always end up in the same split. Fixed random seed, so the split is repeatable.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import imagehash
import matplotlib

matplotlib.use("Agg")  # draw charts to files, no window
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps

from ml.fish_disease_common import (
    CLASS_IDS, CLASS_LABELS, CLASSES, CLEAN_DIR, C_INK, C_MUTED, DROPPED_CLASSES, MANIFEST, PROJECT,
    RAW_DIR, embed, load_backbone, load_rgb,
)

REVIEW_FILE = PROJECT / "ml" / "fish_disease_healthy_review.csv"
SPLIT_FILE = PROJECT / "docs" / "fish-disease-split.csv"
REPORT_FILE = PROJECT / "docs" / "fish-disease-cleaning.md"
FIGURE_FILE = PROJECT / "docs" / "figures" / "fish_disease_cleaning_examples.png"
PAIRS_CACHE = CLEAN_DIR.parent / "same_photo_pairs.json"  # saved so `--reuse-pairs` skips the slow step 2

SEED = 42
SPLITS = {"train": 0.70, "val": 0.15, "test": 0.15}
CROP_BOTTOM = 0.14  # stock watermark bars take up about the bottom 10-13 % of the picture

# Near-duplicate rules. Chosen by looking at a few hundred image pairs by eye (see the report).
N_NEIGHBOURS = 15  # candidates per image, by feature similarity
PHASH_MAX = 4      # perceptual-hash difference (out of 64 bits) that still means "same photo"
INLIERS_SURE = 60  # this many matched keypoints that agree on one rotation+zoom = same photo
INLIERS_HIGH = 40  # 40-59 matches: the overlaid images must correlate at least OVERLAY_LOW
OVERLAY_LOW = 0.10  # (0.0 means the overlay failed: seen on two different photos with 41 and 55 matches)
INLIERS_MIN = 12   # fewer than this is never enough...
OVERLAY_MIN = 0.45  # ...and with 12-39 matches, the overlaid images must correlate this well
# (Keypoints alone are fooled by the repeating scale pattern on carp; the overlay check is not.)

ORB_SIZE = 256


# ---------------------------------------------------------------- 1. read images, exact duplicates

def read_images():
    """Return a list of unique images: dict(pixels-hash, image, copies=[(split, folder, filename)], classes)."""
    by_hash: dict[str, dict] = {}
    n_files = Counter()
    for split in ["Train", "Test"]:
        for folder in sorted((RAW_DIR / split).iterdir()):
            if folder.name in DROPPED_CLASSES:
                continue
            cls = CLASSES[folder.name]
            for path in sorted(folder.iterdir(), key=_file_order):
                im = load_rgb(path)
                h = hashlib.md5(im.tobytes() + str(im.size).encode()).hexdigest()
                n_files[cls] += 1
                if h not in by_hash:
                    by_hash[h] = {"hash": h, "image": im, "path": path, "copies": [], "classes": set()}
                by_hash[h]["copies"].append(f"{split}/{folder.name}/{path.name}")
                by_hash[h]["classes"].add(cls)
    return list(by_hash.values()), n_files


def _file_order(path: Path):
    """'Healthy Fish (12).jpg' -> (12, '.jpg'), so files sort 1, 2, 3 ... not 1, 10, 100."""
    m = re.search(r"\((\d+)\)", path.name)
    return (int(m.group(1)) if m else 0, path.suffix)


# ---------------------------------------------------------------- 2. near-duplicate detection

def _dihedral_hashes(im: Image.Image) -> list[int]:
    """Perceptual hash of the image as-is, mirrored, flipped and rotated (as 64-bit integers)."""
    views = [im, ImageOps.mirror(im), ImageOps.flip(im), im.rotate(90, expand=True),
             im.rotate(270, expand=True), im.rotate(180)]
    return [int(str(imagehash.phash(v)), 16) for v in views]


class KeypointMatcher:
    """Checks whether two images are copies of the same photo (allowing rotation, zoom, mirroring)."""

    def __init__(self, images):
        cv2.setRNGSeed(SEED)
        self.orb = cv2.ORB_create(1000)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        self.gray, self.kp, self.gray_m, self.kp_m = [], [], [], []
        for im in images:
            g = cv2.cvtColor(np.array(im.resize((ORB_SIZE, ORB_SIZE))), cv2.COLOR_RGB2GRAY)
            gm = np.ascontiguousarray(g[:, ::-1])  # mirrored
            self.gray.append(g)
            self.gray_m.append(gm)
            self.kp.append(self.orb.detectAndCompute(g, None))
            self.kp_m.append(self.orb.detectAndCompute(gm, None))

    def _match(self, ga, ka, gb, kb) -> tuple[int, float]:
        (pa, da), (pb, db) = ka, kb
        if da is None or db is None or len(pa) < 8 or len(pb) < 8:
            return 0, 0.0
        # keep matches that are clearly better than the second-best option (Lowe's ratio test)
        good = [m[0] for m in self.bf.knnMatch(da, db, k=2) if len(m) == 2 and m[0].distance < 0.75 * m[1].distance]
        if len(good) < 6:
            return 0, 0.0
        a = np.float32([pa[g.queryIdx].pt for g in good])
        b = np.float32([pb[g.trainIdx].pt for g in good])
        M, mask = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=6)
        if mask is None:
            return 0, 0.0
        inliers = int(mask.sum())
        # overlay: move image A onto image B and correlate the pixels where they overlap
        warped = cv2.warpAffine(ga, M, (ORB_SIZE, ORB_SIZE))
        inside = cv2.warpAffine(np.full_like(ga, 255), M, (ORB_SIZE, ORB_SIZE))
        inside = cv2.erode(inside, np.ones((9, 9), np.uint8)) > 0
        if inside.sum() < 0.1 * ORB_SIZE * ORB_SIZE:
            return inliers, 0.0
        x = warped[inside].astype(float)
        y = gb[inside].astype(float)
        x -= x.mean()
        y -= y.mean()
        return inliers, float((x * y).sum() / np.sqrt((x * x).sum() * (y * y).sum() + 1e-9))

    def compare(self, i: int, j: int) -> tuple[int, float]:
        """Best (inliers, overlay correlation) of A->B and mirrored-A->B."""
        return max(self._match(self.gray[i], self.kp[i], self.gray[j], self.kp[j]),
                   self._match(self.gray_m[i], self.kp_m[i], self.gray[j], self.kp[j]),
                   key=lambda r: (r[1], r[0]))


def find_same_photo_pairs(images) -> dict[tuple[int, int], str]:
    """Return {(i, j): why} for every pair of images judged to be copies of the same photo."""
    print("  features (MobileNetV3-Large)...")
    model, prep = load_backbone("large")
    feats = embed(images, model, prep)
    feats /= np.linalg.norm(feats, axis=1, keepdims=True)
    sim = feats @ feats.T
    np.fill_diagonal(sim, -1)

    print("  perceptual hashes...")
    hashes = np.array([_dihedral_hashes(im) for im in images], dtype=np.uint64)

    pairs: dict[tuple[int, int], str] = {}
    # (b) perceptual hash, checked for ALL pairs (fast)
    for i in range(len(images)):
        diff = np.bitwise_count(hashes[i, 0] ^ hashes[:, :]).min(axis=1)
        for j in np.nonzero(diff <= PHASH_MAX)[0]:
            if j != i:
                pairs[(min(i, int(j)), max(i, int(j)))] = f"perceptual hash differs by {int(diff[j])}/64 bits"

    # (c) keypoint matching, checked for each image's nearest neighbours by features
    print("  keypoint matching...")
    matcher = KeypointMatcher(images)
    candidates = {(min(i, int(j)), max(i, int(j))) for i in range(len(images))
                  for j in np.argsort(-sim[i])[:N_NEIGHBOURS]}
    for i, j in sorted(candidates - pairs.keys()):
        inliers, overlay = max(matcher.compare(i, j), matcher.compare(j, i))
        if (inliers >= INLIERS_SURE or (inliers >= INLIERS_HIGH and overlay >= OVERLAY_LOW)
                or (inliers >= INLIERS_MIN and overlay >= OVERLAY_MIN)):
            pairs[(i, j)] = f"{inliers} matching keypoints, overlay correlation {overlay:.2f}"
    return pairs


def photo_groups(n: int, pairs) -> list[int]:
    """Union-find: group id for each image, where linked images (also via chains) share a group."""
    parent = list(range(n))

    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j in pairs:
        parent[root(i)] = root(j)
    return [root(i) for i in range(n)]


# ---------------------------------------------------------------- 3. decide what to keep

def read_review() -> dict[str, dict]:
    with open(REVIEW_FILE, newline="", encoding="utf-8") as f:
        return {row["file"]: row for row in csv.DictReader(f)}


def decide(items, pairs, review):
    """Set item['status'] (kept / removed), item['reason'], item['group'] and item['crop'].

    Removals only follow DIRECT links (an image and its direct copies), never long chains:
    a chain A~B~C~D can wander from one photo to a different photo of a similar-looking fish."""
    neighbours = defaultdict(set)
    for i, j in pairs:
        neighbours[i].add(j)
        neighbours[j].add(i)
    for it in items:
        it["crop"] = False
        it["review"] = None
        for copy in it["copies"]:
            name = copy.split("/")[-1]
            if copy.startswith("Train/Healthy Fish/") and name in review:
                it["review"] = review[name]

    # a) Label conflicts: an image filed under two classes, or a direct copy of an image in another
    #    class - plus its own direct copies in the same class.
    conflict: dict[int, set] = {}
    for k, it in enumerate(items):
        if len(it["classes"]) > 1:
            conflict[k] = set(it["classes"])
    for i, j in pairs:
        if items[i]["classes"] != items[j]["classes"]:
            both = items[i]["classes"] | items[j]["classes"]
            for k, other in [(i, j), (j, i)]:
                conflict.setdefault(k, set()).update(both)
                items[k].setdefault("conflict_with", other)
    for k in list(conflict):
        for n in neighbours[k]:
            if n not in conflict and items[n]["classes"] == items[k]["classes"]:
                conflict[n] = set(conflict[k])
    for k, classes in conflict.items():
        exact = len(items[k]["classes"]) > 1
        _remove(items[k], "label_conflict", ("exact same image" if exact else "copy of the same photo")
                + " filed under: " + ", ".join(sorted(CLASS_LABELS[c] for c in classes)))

    # b) Healthy review: removed photos, plus their direct (rotated / cropped) copies.
    by_review = [k for k, it in enumerate(items)
                 if "status" not in it and it["review"] and it["review"]["action"] == "remove"]
    for k in by_review:
        _remove(items[k], "healthy_review", items[k]["review"]["reason"])
    for k in by_review:
        for n in neighbours[k]:
            if "status" not in items[n]:
                _remove(items[n], "healthy_review", "copy of a removed photo ("
                        + _short(items[k]) + ": " + items[k]["review"]["reason"] + ")")

    # c) Photo groups for the split: links between images of the same class (chains allowed here:
    #    putting two different photos in the same split costs nothing, and it is the safe side).
    groups = photo_groups(len(items), [(i, j) for i, j in pairs if items[i]["classes"] == items[j]["classes"]])
    members = defaultdict(list)
    for k, it in enumerate(items):
        it["group"] = groups[k]
        if "status" not in it:
            members[it["group"]].append(k)

    for g, ks in members.items():
        # Keep the best copy first (biggest picture, then the lowest file number, usually the original),
        # then keep any other member that is NOT a direct copy of something already kept
        # (e.g. a second photo of the same fish). All of them stay in the same split later.
        order = sorted(ks, key=lambda k: (-items[k]["image"].size[0] * items[k]["image"].size[1],
                                          _file_order(items[k]["path"])))
        kept: list[int] = []
        for k in order:
            dup_of = next((q for q in kept if q in neighbours[k]), None)
            if dup_of is None:
                kept.append(k)
                items[k]["status"], items[k]["reason"], items[k]["kind"] = "kept", "", ""
                if items[k]["review"] and items[k]["review"]["action"] == "crop_bottom":
                    items[k]["crop"] = True
            else:
                _remove(items[k], "near_duplicate",
                        f"copy of {_short(items[dup_of])} ({pairs[(min(k, dup_of), max(k, dup_of))]})")
                items[k]["dup_of"] = dup_of


def _remove(it, kind, reason):
    it["status"], it["kind"], it["reason"] = "removed", kind, reason


def _short(it) -> str:
    return it["copies"][0]


# ---------------------------------------------------------------- 4. split by group

def split_groups(items) -> None:
    """70/15/15 per class, moving whole photo groups. Big groups are placed first, each into the
    split that is furthest below its target."""
    rng = random.Random(SEED)
    for cls in CLASS_IDS:
        groups = defaultdict(list)
        for it in items:
            if it["status"] == "kept" and cls in it["classes"]:
                groups[it["group"]].append(it)
        glist = list(groups.values())
        rng.shuffle(glist)
        glist.sort(key=len, reverse=True)  # stable sort: same-size groups stay shuffled
        total = sum(len(g) for g in glist)
        count = dict.fromkeys(SPLITS, 0)
        for g in glist:
            best = max(SPLITS, key=lambda s: SPLITS[s] * total - count[s])
            count[best] += len(g)
            for it in g:
                it["split"] = best


# ---------------------------------------------------------------- 5. write files + report

def output_name(it) -> str:
    cls = next(iter(it["classes"]))
    stem = Path(_short(it)).stem
    suffix = ".png" if it["crop"] else Path(_short(it)).suffix.lower()
    return f"{it['split']}/{cls}/{stem}{suffix}"


def write_clean(items) -> None:
    if CLEAN_DIR.exists():
        shutil.rmtree(CLEAN_DIR)
    rows = []
    for it in items:
        if it["status"] != "kept":
            continue
        out = CLEAN_DIR / output_name(it)
        out.parent.mkdir(parents=True, exist_ok=True)
        if it["crop"]:
            im = it["image"]
            im.crop((0, 0, im.width, round(im.height * (1 - CROP_BOTTOM)))).save(out)
        else:
            shutil.copyfile(it["path"], out)
        rows.append({"file": output_name(it), "class": next(iter(it["classes"])), "split": it["split"],
                     "group": f"g{it['group']}", "cropped": int(it["crop"]), "source": _short(it)})
    rows.sort(key=lambda r: r["file"])
    for path in [MANIFEST, SPLIT_FILE]:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    removed = [{"source": _short(it), "class": "/".join(sorted(it["classes"])), "kind": it["kind"],
                "reason": it["reason"]} for it in items if it["status"] == "removed"]
    with open(CLEAN_DIR / "removed.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(removed[0]))
        w.writeheader()
        w.writerows(removed)


def draw_examples(items) -> None:
    """One row per kind of change, with the original images."""
    by_name = {}
    for it in items:
        for c in it["copies"]:
            by_name[c] = it
    rng = random.Random(SEED)

    rows = []
    # near-duplicates: the biggest group's kept image + 4 removed copies of it
    dup_groups = defaultdict(list)
    for k, it in enumerate(items):
        if it.get("kind") == "near_duplicate":
            dup_groups[it["dup_of"]].append(it)
    keep_k = max(dup_groups, key=lambda k: len(dup_groups[k]))
    rows.append(("Near-duplicates: 1 photo kept (left), its pre-augmented copies removed",
                 [(items[keep_k], "kept")] + [(it, "removed") for it in dup_groups[keep_k][:5]]))
    # label conflicts: direct cross-class copies, one pair per class combination
    pick, seen = [], set()
    for it in items:
        other = it.get("conflict_with")
        if other is None or len(it["classes"]) > 1:
            continue
        combo = frozenset(it["classes"] | items[other]["classes"])
        if combo in seen:
            continue
        seen.add(combo)
        pick += [(x, " + ".join(sorted(CLASS_LABELS[c] for c in x["classes"]))) for x in (it, items[other])]
    rows.append(("Same photo filed under different diseases: all copies removed", pick[:6]))
    # Healthy review: people / scenery / not a real fish
    shown = ["Healthy Fish (19).jpg", "Healthy Fish (147).jpg", "Healthy Fish (15).jpg",
             "Healthy Fish (41).jpg", "Healthy Fish (129).jpg", "Healthy Fish (106).jpg"]
    rows.append(("Healthy: stock photos removed (hands, scenery, lure, drawing)",
                 [(by_name[f"Train/Healthy Fish/{n}"], by_name[f"Train/Healthy Fish/{n}"]["review"]["reason"]
                   .split(" (")[0]) for n in shown]))
    # Healthy crops: before / after
    crops = [it for it in items if it["crop"]]
    rng.shuffle(crops)
    pairs = []
    for it in crops[:3]:
        pairs += [(it, "before"), (it, "after crop")]
    rows.append(("Healthy: stock-photo watermark bar cropped off", pairs))

    ncol = 6
    fig, axes = plt.subplots(len(rows), ncol, figsize=(12, 2.6 * len(rows)))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.05, hspace=0.6, wspace=0.12)
    for r, (title, cells) in enumerate(rows):
        top = axes[r, 0].get_position()
        fig.text(top.x0, top.y1 + 0.012, title, fontsize=11, color=C_INK, fontweight="bold")
        for c in range(ncol):
            ax = axes[r, c]
            ax.axis("off")
            if c >= len(cells):
                continue
            it, label = cells[c]
            im = it["image"]
            if label == "after crop":
                im = im.crop((0, 0, im.width, round(im.height * (1 - CROP_BOTTOM))))
            ax.imshow(im)
            ax.text(0.5, -0.04, _wrap(label), transform=ax.transAxes, ha="center", va="top",
                    fontsize=8, color=C_MUTED)
    fig.text(0.01, 0.005, "Images: Biswas et al., Freshwater Fish Disease Aquaculture in South Asia (Kaggle, CC0).",
             fontsize=7.5, color=C_MUTED)
    fig.savefig(FIGURE_FILE, dpi=110, facecolor="white")
    plt.close(fig)


def _wrap(text: str, width: int = 26) -> str:
    words, lines, line = text.split(), [], ""
    for w in words:
        if len(line) + len(w) + 1 > width and line:
            lines.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    lines.append(line)
    return "\n".join(lines[:2])


def write_report(items, n_files, n_raw_dropped) -> None:
    def count(pred, cls):
        return sum(1 for it in items if cls in it["classes"] and pred(it))

    kinds = ["label_conflict", "healthy_review", "near_duplicate"]
    table = ["| Class | Files (Train + Test) | Unique images | Label conflicts | Healthy review | Near-duplicates "
             "| **Kept** | Photo groups | Train / Val / Test |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    tot = Counter()
    for cls in CLASS_IDS:
        unique = count(lambda it: True, cls)
        removed = {k: count(lambda it, k=k: it.get("kind") == k, cls) for k in kinds}
        kept = [it for it in items if cls in it["classes"] and it["status"] == "kept"]
        groups = len({it["group"] for it in kept})
        sp = Counter(it["split"] for it in kept)
        table.append(f"| {CLASS_LABELS[cls]} | {n_files[cls]} | {unique} | {removed['label_conflict']} | "
                     f"{removed['healthy_review'] or '–'} | {removed['near_duplicate']} | **{len(kept)}** | {groups} | "
                     f"{sp['train']} / {sp['val']} / {sp['test']} |")
        for k, v in [("files", n_files[cls]), ("unique", unique), ("kept", len(kept)), ("groups", groups),
                     ("train", sp["train"]), ("val", sp["val"]), ("test", sp["test"])] + list(removed.items()):
            tot[k] += v
    table.append(f"| **Total** | {tot['files']} | {tot['unique']} | {tot['label_conflict']} | {tot['healthy_review']} | "
                 f"{tot['near_duplicate']} | **{tot['kept']}** | {tot['groups']} | "
                 f"{tot['train']} / {tot['val']} / {tot['test']} |")

    n_test_in_train = sum(1 for it in items if any(c.startswith("Test/") for c in it["copies"])
                          and any(c.startswith("Train/") for c in it["copies"]))
    n_test_unique = sum(1 for it in items if any(c.startswith("Test/") for c in it["copies"]))
    review = read_review()
    n_rev_remove = sum(1 for r in review.values() if r["action"] == "remove")
    n_rev_crop = sum(1 for r in review.values() if r["action"] == "crop_bottom")
    n_cropped = sum(1 for it in items if it["crop"])
    disease_groups = [len({it["group"] for it in items if c in it["classes"] and it["status"] == "kept"})
                      for c in CLASS_IDS if c != "healthy"]
    g_min, g_max = min(disease_groups), max(disease_groups)
    healthy_kept = sum(1 for it in items if "healthy" in it["classes"] and it["status"] == "kept")

    text = f"""# Fish-disease photos: cleaning report

Step 1 of [disease-detection-plan.md](disease-detection-plan.md). Made by `python -m ml.clean_fish_disease`.
Dataset: Biswas et al., *Freshwater Fish Disease Aquaculture in South Asia* (Kaggle, CC0), dataset #1 in the plan.

## Summary

- **The original Test folder is useless.** {n_test_in_train} of the {n_test_unique} unique images in `Test/` are exact
  copies of images in `Train/`. A model scored on that split has already seen the test images.
- **Most images are copies.** The {tot['files']} files (6 classes, Train + Test) contain {len(items)} unique images.
  Each disease photo was saved many times: rotated, zoomed, mirrored or with the edges stretched. Removing those
  copies (and the problem images below) leaves **{tot['kept']} images in only {tot['groups']} independent photo groups**.
- **"White tail disease" is dropped** ({n_raw_dropped} files): it is a prawn disease, but the folder holds goldfish and
  other fish. We use 6 classes.
- **Healthy:** {n_rev_remove} stock photos were removed by hand (anglers, hands holding the fish, underwater lake
  scenery, a fishing lure, drawings), plus the copies of those photos; {n_cropped} kept photos had a stock-photo
  watermark bar cropped off the bottom.
- **New split:** 70 / 15 / 15 per class, by **photo group**, so every copy or extra shot of the same fish is in only
  one of train, validation or test.

## Counts

{chr(10).join(table)}

*Photo groups* = images linked as copies of the same photo or the same fish. The split keeps each group whole.
Disease classes now have only {min(count(lambda it: it['status'] == 'kept', c) for c in CLASS_IDS if c != 'healthy')}–{max(count(lambda it: it['status'] == 'kept', c) for c in CLASS_IDS if c != 'healthy')} images each, while Healthy has {healthy_kept}.
**The classes are unbalanced and small**; that limits what any model can learn from this data.

![Examples of removed and cropped images](figures/fish_disease_cleaning_examples.png)

## How duplicates were found

1. **Exact duplicates:** images with identical pixels (MD5 hash of the decoded image).
2. **Near-duplicates.** Candidate pairs: each image's {N_NEIGHBOURS} most similar images by MobileNetV3-Large features.
   A pair counts as *the same photo* if any of these is true:
   - perceptual hash (also tried mirrored, flipped and rotated) differs by at most {PHASH_MAX} of 64 bits; or
   - OpenCV ORB keypoint matching finds at least {INLIERS_SURE} matching points that agree on one rotation + zoom
     (or {INLIERS_HIGH}–{INLIERS_SURE - 1} points and, after lining the images up, a pixel correlation of at least {OVERLAY_LOW}); or
   - at least {INLIERS_MIN} such points **and** after lining the two images up, their pixels correlate at least
     {OVERLAY_MIN}. This extra check is needed because the repeating scale pattern of carp fools keypoint matching
     between two *different* carp.
   The thresholds were set by looking at a few hundred pairs by eye. Feature similarity alone was **not** used as a
   rule: different carp on a white background look "very similar" to the network.
3. Linked images form a **photo group** (chains count: if A~B and B~C, all three are one group). In each group the
   biggest image is kept, plus any member that is not a direct copy of a kept one (for example a second shot of the
   same fish); everything else is removed as a near-duplicate.
4. If a group contains images from two classes, the **whole group is removed** (label conflict: the same photo is
   labelled as two different diseases, so we cannot trust either label).

## Healthy class review

Every one of the 250 unique Healthy images was looked at by eye. Decisions are in
[`ml/fish_disease_healthy_review.csv`](../ml/fish_disease_healthy_review.csv) ({n_rev_remove} remove, {n_rev_crop} crop).
Removed: people or hands in the picture, fishing gear, underwater or lake scenery where the fish is small,
fishing lures, fish models, drawings and paintings. Cropped: a stock-photo watermark bar along the bottom.
Kept: a single fish filling most of the frame, including fish on grass, ice or a market floor.

## Problems that cleaning does NOT fix

- **Shortcut risk remains.** Healthy photos are mostly *stock photos of carp* on white or plain backgrounds.
  The disease photos are mostly *aquarium fish and goldfish*, often close-ups on lab tables or in hands, with arrows
  and circles drawn on them. A model can partly tell the classes apart by **species, background and photo style**
  instead of by disease signs. Step 2 measures this with a "background only" test.
- **Very few independent disease photos** ({g_min}–{g_max} photo groups per disease class). Test-set numbers are based on a few dozen images
  per class, so they are rough.
- **Not Indian carps.** Almost no rohu, catla or mrigal with disease. Results will not transfer directly to Karnataka ponds.

## Files

- Cleaned images: `data/fish-disease/clean/{{train,val,test}}/<class>/` (not in git; re-create with the command above).
- [`docs/fish-disease-split.csv`](fish-disease-split.csv): every kept image, its split, photo group and original file.
- `data/fish-disease/clean/removed.csv`: every removed image and why.
"""
    REPORT_FILE.write_text(text, encoding="utf-8")


def main() -> None:
    print("1. Reading images...")
    items, n_files = read_images()
    n_raw_dropped = sum(1 for s in ["Train", "Test"] for c in DROPPED_CLASSES for _ in (RAW_DIR / s / c).iterdir())
    print(f"   {sum(n_files.values())} files, {len(items)} unique images (6 classes); "
          f"{n_raw_dropped} White-tail files skipped")

    print("2. Finding near-duplicates...")
    if "--reuse-pairs" in sys.argv and PAIRS_CACHE.exists():
        saved = json.loads(PAIRS_CACHE.read_text(encoding="utf-8"))
        pairs = {(p["i"], p["j"]): p["why"] for p in saved["pairs"]}
    else:
        pairs = find_same_photo_pairs([it["image"] for it in items])
        PAIRS_CACHE.write_text(json.dumps({"files": [it["copies"][0] for it in items], "pairs": [
            {"i": i, "j": j, "why": why} for (i, j), why in sorted(pairs.items())]}), encoding="utf-8")
    print(f"   {len(pairs)} same-photo pairs")

    print("3. Deciding what to keep...")
    decide(items, pairs, read_review())
    split_groups(items)
    print("   " + str(Counter(it.get("kind") or "kept" for it in items)))

    print("4. Writing cleaned images, split list, report and figure...")
    write_clean(items)
    FIGURE_FILE.parent.mkdir(parents=True, exist_ok=True)
    draw_examples(items)
    write_report(items, n_files, n_raw_dropped)
    print(f"   done: {MANIFEST}, {REPORT_FILE.relative_to(PROJECT)}, {FIGURE_FILE.relative_to(PROJECT)}")


if __name__ == "__main__":
    main()
