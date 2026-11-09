"""Detector and speed check.

  python evaluation/recognition/detector_check.py [--images 400]

1. Close up dog faces (DogFaceNet, like a dog right in front of the feeder camera), clean and
   through the feeder camera simulation: how often YOLO finds a dog.
2. People: the two street photos shipped with Ultralytics must give no dog.
3. Empty scenes: plain and noisy images must give no dog.
4. Time of the full pipeline (detect, crop, describe) per photo on this computer.

Writes results_detector.md next to this file.
"""

import argparse
import pathlib
import sys
import time

import numpy as np
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from evaluation.recognition.common import HERE, feeder_camera, list_dogfacenet  # noqa: E402
from kibbly_ai.perception.models import DinoV2Embedder, YoloDetector  # noqa: E402
from kibbly_ai.perception.recognizer import RecognitionSettings, crop_box  # noqa: E402

MIN_DOG = RecognitionSettings().min_dog_confidence


def labels_of(detector, image):
    return [(d.label, d.confidence) for d in detector.detect(image)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", type=int, default=400)
    args = parser.parse_args()

    import ultralytics
    from kibbly_ai.config import load_settings
    detector = YoloDetector(load_settings().yolo_weights, min_confidence=0.10)
    embedder = DinoV2Embedder()
    paths, _ = list_dogfacenet()
    rng = np.random.default_rng(3)
    sample = sorted(rng.choice(len(paths), args.images, replace=False))

    lines = ["# Detector and speed check\n",
             f"Detector: YOLO11n, dog accepted at confidence {MIN_DOG} or more. Sample: {args.images} DogFaceNet images.\n",
             "| test | images | dog found | other result |", "|---|---|---|---|"]
    for condition in ("clean", "feeder"):
        found, other = 0, {}
        for i in sample:
            image = Image.open(paths[i]).convert("RGB")
            if condition == "feeder":
                image = feeder_camera(image, seed=int(i))
            dets = labels_of(detector, image)
            if any(lab == "dog" and conf >= MIN_DOG for lab, conf in dets):
                found += 1
            else:
                top = max(dets, key=lambda x: x[1])[0] if dets else "nothing"
                other[top] = other.get(top, 0) + 1
        detail = ", ".join(f"{k}: {v}" for k, v in sorted(other.items(), key=lambda kv: -kv[1])) or "none"
        lines.append(f"| close up dog faces, {condition} | {len(sample)} | {100 * found / len(sample):.1f}% | {detail} |")
        print(lines[-1], flush=True)

    assets = pathlib.Path(ultralytics.__file__).parent / "assets"
    people = [p for p in sorted(assets.glob("*.jpg"))]
    false_dogs = sum(any(l == "dog" and c >= MIN_DOG for l, c in labels_of(detector, Image.open(p).convert("RGB")))
                     for p in people)
    lines.append(f"| people (street photos) | {len(people)} | {false_dogs} with a dog | must be 0 |")

    empties = [Image.new("RGB", (640, 480), (200, 190, 170)),
               Image.fromarray(rng.integers(0, 255, (480, 640, 3), dtype=np.uint8)),
               Image.new("RGB", (640, 480), (20, 20, 25))]
    false_dogs = sum(any(l == "dog" and c >= MIN_DOG for l, c in labels_of(detector, im)) for im in empties)
    lines.append(f"| empty scenes (plain, noise, dark) | {len(empties)} | {false_dogs} with a dog | must be 0 |")

    frame = Image.open(paths[sample[0]]).convert("RGB").resize((640, 480))
    for _ in range(3):
        detector.detect(frame)
        embedder.embed([frame])
    times = []
    for i in sample[:30]:
        image = Image.open(paths[i]).convert("RGB").resize((640, 480))
        start = time.perf_counter()
        dets = [d for d in detector.detect(image) if d.label == "dog"]
        crop = crop_box(image, max(dets, key=lambda d: d.area).box, 0.1) if dets else image
        embedder.embed([crop])
        times.append(time.perf_counter() - start)
    lines += ["", f"Full pipeline on a 640 x 480 photo (detect, crop, describe with DINOv2 small): "
              f"median {1000 * np.median(times):.0f} ms, slowest {1000 * max(times):.0f} ms over {len(times)} photos."]
    (HERE / "results_detector.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[-4:]))


if __name__ == "__main__":
    main()
