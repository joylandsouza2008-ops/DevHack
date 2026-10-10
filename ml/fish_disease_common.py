"""
Shared helpers for the fish-disease image experiments (research only, not used by the app).

Used by:
    ml/clean_fish_disease.py           (step 1: clean the dataset, make a new split)
    ml/train_fish_disease_baseline.py  (step 2: frozen MobileNetV3 + LogisticRegression)

Needs the extra training packages:  pip install -r requirements-train.txt
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

PROJECT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT / "data" / "fish-disease" / "Freshwater Fish Disease Aquaculture in south asia"
CLEAN_DIR = PROJECT / "data" / "fish-disease" / "clean"
MANIFEST = CLEAN_DIR / "manifest.csv"  # one row per kept image: file, class, split, group, source
MASK_DIR = PROJECT / "data" / "fish-disease" / "fish_masks"  # fish masks (ml/make_fish_masks.py), kept outside
                                                             # CLEAN_DIR so re-cleaning does not delete them

# Original folder name -> our short class id. "Viral diseases White tail disease" is left out on
# purpose: white tail is a prawn disease and the folder contains goldfish and other fish.
CLASSES = {
    "Bacterial diseases - Aeromoniasis": "aeromoniasis",
    "Bacterial gill disease": "bacterial_gill",
    "Bacterial Red disease": "bacterial_red",
    "Fungal diseases Saprolegniasis": "saprolegniasis",
    "Parasitic diseases": "parasitic",
    "Healthy Fish": "healthy",
}
DROPPED_CLASSES = ["Viral diseases White tail disease"]

# Short English names for charts and tables
CLASS_LABELS = {
    "aeromoniasis": "Aeromoniasis",
    "bacterial_gill": "Bacterial gill",
    "bacterial_red": "Bacterial red",
    "saprolegniasis": "Saprolegniasis (fungal)",
    "parasitic": "Parasitic",
    "healthy": "Healthy",
}
CLASS_IDS = list(CLASS_LABELS)

# Chart colours (same family as ml/train_do_forecast.py)
C_INK, C_MUTED, C_ACCENT, C_GRID = "#0f2a36", "#56707b", "#2a78d6", "#e6eef1"


def load_rgb(path: Path) -> Image.Image:
    """Open any image (jpg / png / webp, with or without transparency) as plain RGB."""
    im = Image.open(path)
    if im.mode in ("RGBA", "LA", "P"):
        # Transparent background -> white, so "see-through" PNGs look like the white-background JPGs
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        im = Image.alpha_composite(bg, im)
    return im.convert("RGB")


def load_backbone(name: str = "small"):
    """
    A MobileNetV3 network already trained on ImageNet, with its last (classification) layer cut off.
    We only use it to turn each photo into a list of numbers ("features"); it is never retrained here.
    Returns (model, preprocess) where preprocess resizes + normalises a PIL image the way the model expects.
    """
    import torch
    import torchvision

    if name == "small":
        weights = torchvision.models.MobileNet_V3_Small_Weights.IMAGENET1K_V1
        net = torchvision.models.mobilenet_v3_small(weights=weights)
    elif name == "large":
        weights = torchvision.models.MobileNet_V3_Large_Weights.IMAGENET1K_V2
        net = torchvision.models.mobilenet_v3_large(weights=weights)
    else:
        raise ValueError(name)
    # features -> average pool -> flat vector (576 numbers for small, 960 for large)
    model = torch.nn.Sequential(net.features, net.avgpool, torch.nn.Flatten()).eval()
    return model, weights.transforms()


def embed(images: list[Image.Image], model, preprocess, batch_size: int = 64) -> np.ndarray:
    """Turn a list of PIL images into a (n_images, n_features) array, one row per image."""
    import torch

    rows = []
    with torch.no_grad():
        for i in range(0, len(images), batch_size):
            x = torch.stack([preprocess(im) for im in images[i:i + batch_size]])
            rows.append(model(x).numpy())
    return np.concatenate(rows).astype(np.float32)
