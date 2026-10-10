"""
Make a "where is the fish" mask for every cleaned fish-disease photo (research only, not used by the app).

Run from the project folder, in its own terminal (slow: about 5 seconds per image on a laptop CPU,
so roughly 30-40 minutes for all ~440 images):
    python -m ml.make_fish_masks

It is RESUMABLE: masks that already exist are skipped, so you can stop it any time with Ctrl+C and
run the same command again later to continue. A half-written mask is never left behind.

Input:  data/fish-disease/clean/manifest.csv and the images it lists (made by ml/clean_fish_disease.py)
Output: data/fish-disease/fish_masks/<split>/<class>/<name>.png
        black-and-white pictures, same size as the photo: white = fish, black = background.

How: rembg's "isnet-general-use" model (MIT licence) finds the main object in a photo and cuts it out
of the background. The model file (~180 MB) is downloaded automatically the first time.
Needs: pip install -r requirements-train.txt
"""

from __future__ import annotations

import csv
import time

from PIL import Image

from ml.fish_disease_common import CLEAN_DIR, MANIFEST, MASK_DIR, load_rgb

MODEL = "isnet-general-use"


def mask_path(manifest_file: str):
    """'train/healthy/Healthy Fish (5).jpg' -> data/fish-disease/fish_masks/train/healthy/Healthy Fish (5).png"""
    return (MASK_DIR / manifest_file).with_suffix(".png")


def mask_is_done(path, size) -> bool:
    """True if the mask file exists, opens, and has the same size as the photo."""
    try:
        with Image.open(path) as m:
            m.load()
            return m.size == size
    except (OSError, ValueError):
        return False


def main() -> None:
    with open(MANIFEST, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    todo = []
    for r in rows:
        with Image.open(CLEAN_DIR / r["file"]) as im:
            size = im.size
        if not mask_is_done(mask_path(r["file"]), size):
            todo.append(r)
    print(f"{len(rows)} images, {len(rows) - len(todo)} masks already done, {len(todo)} to go.")
    if not todo:
        print("All masks are done.")
        return

    from rembg import new_session, remove  # imported here so the "all done" check above is instant

    print(f"Loading the {MODEL} model (downloads ~180 MB the first time)...")
    session = new_session(MODEL)
    start = time.time()
    for n, r in enumerate(todo, 1):
        out = mask_path(r["file"])
        out.parent.mkdir(parents=True, exist_ok=True)
        mask = remove(load_rgb(CLEAN_DIR / r["file"]), session=session, only_mask=True)
        tmp = out.with_suffix(".tmp.png")
        mask.save(tmp)
        tmp.replace(out)  # only now does the finished mask appear, so Ctrl+C never leaves half a file
        per_image = (time.time() - start) / n
        print(f"  {n}/{len(todo)}  {r['file']}  (about {per_image * (len(todo) - n) / 60:.0f} min left)",
              flush=True)
    print("All masks are done.")


if __name__ == "__main__":
    main()
