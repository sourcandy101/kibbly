"""Shared helpers for the recognition evaluation: dataset listing, feeder camera simulation, cache paths."""

import io
import os
import pathlib

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

DATA_ROOT = pathlib.Path(os.environ.get("KIBBLY_DATA_ROOT", "D:/kibbly_data"))
DOGFACENET = DATA_ROOT / "dogfacenet" / "extracted" / "after_4_bis"
CACHE = DATA_ROOT / "cache" / "recognition"
HERE = pathlib.Path(__file__).resolve().parent


def list_dogfacenet():
    """Return (paths, labels): one entry per image, label = dog folder name."""
    paths, labels = [], []
    for dog in sorted(DOGFACENET.iterdir(), key=lambda p: int(p.name)):
        for image in sorted(dog.iterdir()):
            paths.append(str(image))
            labels.append(dog.name)
    return paths, labels


def feeder_camera(image: Image.Image, seed: int) -> Image.Image:
    """Approximate an ESP32-CAM shot of a close dog: lower resolution, blur, dim light,
    color cast and strong JPEG compression. Deterministic for a given seed."""
    rng = np.random.default_rng(seed)
    image = image.convert("RGB")
    w, h = image.size
    small = image.resize((max(1, w // 2), max(1, h // 2)), Image.BILINEAR)
    image = small.resize((w, h), Image.BILINEAR)
    image = image.filter(ImageFilter.GaussianBlur(radius=float(rng.uniform(0.5, 1.2))))
    image = ImageEnhance.Brightness(image).enhance(float(rng.uniform(0.45, 0.8)))
    r, g, b = image.split()
    cast = float(rng.uniform(0.85, 1.15))
    r = r.point(lambda v: min(255, int(v * cast)))
    b = b.point(lambda v: min(255, int(v / cast)))
    image = Image.merge("RGB", (r, g, b))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=int(rng.integers(20, 40)))
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def color_signature(image: Image.Image) -> np.ndarray:
    """Coarse HSV color histogram, used to build look alike households independently of the models."""
    hsv = np.asarray(image.convert("RGB").resize((64, 64)).convert("HSV")).reshape(-1, 3)
    hist, _ = np.histogramdd(hsv, bins=(8, 4, 4), range=((0, 256), (0, 256), (0, 256)))
    hist = hist.ravel()
    return hist / hist.sum()


def cache_file(model: str, condition: str) -> pathlib.Path:
    return CACHE / f"{model}_{condition}.npz"
