"""Compute and cache the vectors of every DogFaceNet image, clean and through the feeder camera simulation.

  python evaluation/recognition/embed_dataset.py

Writes D:/kibbly_data/cache/recognition/<model>_<condition>.npz and colors.npz.
DINOv2 is run once with cls_mean pooling; the cls vectors are its first half.
"""

import sys
import time

import numpy as np
from PIL import Image

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))

from evaluation.recognition.common import CACHE, cache_file, color_signature, feeder_camera, list_dogfacenet  # noqa: E402
from kibbly_ai.perception.base import normalize  # noqa: E402
from kibbly_ai.perception.models import ClipEmbedder, DinoV2Embedder  # noqa: E402


def load(paths, condition, offset=0):
    images = []
    for i, p in enumerate(paths):
        image = Image.open(p).convert("RGB")
        images.append(feeder_camera(image, seed=offset + i) if condition == "feeder" else image)
    return images


def run():
    CACHE.mkdir(parents=True, exist_ok=True)
    paths, labels = list_dogfacenet()
    print(f"{len(paths)} images of {len(set(labels))} dogs", flush=True)

    colors = cache_file("colors", "clean")
    if not colors.exists():
        np.savez(colors, colors=np.stack([color_signature(Image.open(p)) for p in paths]),
                 labels=np.array(labels), paths=np.array(paths))

    dino, clip = DinoV2Embedder(pooling="cls_mean"), ClipEmbedder()
    for condition in ("clean", "feeder"):
        if cache_file("dinov2_small_cls", condition).exists() and cache_file("clip_b32", condition).exists():
            print(f"skip {condition} (cached)", flush=True)
            continue
        start, dino_vectors, clip_vectors = time.time(), [], []
        for i in range(0, len(paths), 128):  # small chunks: the laptop has 8 GB of RAM
            images = load(paths[i:i + 128], condition, offset=i)
            dino_vectors.append(dino.embed(images))
            clip_vectors.append(clip.embed(images))
            print(f"  {condition} {min(i + 128, len(paths))}/{len(paths)} {time.time() - start:.0f}s", flush=True)
        dino_vectors = np.concatenate(dino_vectors)
        half = dino_vectors.shape[1] // 2
        outputs = {"dinov2_small_cls_mean": dino_vectors, "dinov2_small_cls": normalize(dino_vectors[:, :half]),
                   "clip_b32": np.concatenate(clip_vectors)}
        for name, v in outputs.items():
            np.savez(cache_file(name, condition), vectors=v, labels=np.array(labels), paths=np.array(paths))
        print(f"{condition}: {len(paths)} images, both models, {time.time() - start:.0f}s "
              f"({1000 * (time.time() - start) / len(paths):.0f} ms per image)", flush=True)


if __name__ == "__main__":
    run()
