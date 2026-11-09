"""Dog or not: compare three designs for the first stage of recognition.

  python evaluation/recognition/gate_check.py [--per-set 200]

Designs
  A. YOLO only (current): a dog box with confidence 0.35 or more.
  B. YOLO, and when it finds no dog, the CLIP scene check on the whole photo.
  C. CLIP scene check only.

Image sets (each clean and through the feeder camera simulation):
  dog faces (DogFaceNet close ups), whole dogs (COCO crops), cats (COCO crops),
  people (COCO crops), person heads (top of COCO person boxes), scenes without
  animals or people (COCO, whole and zoomed).
The CLIP threshold is chosen on even numbered images and measured on odd numbered ones.
Targets: at least 95% of dogs found, at most 2% of any other set taken for a dog.
Writes results_gate.md and results_gate.json next to this file.
"""

import argparse
import json
import pathlib
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from evaluation.recognition.common import DATA_ROOT, HERE, feeder_camera, list_dogfacenet  # noqa: E402

COCO = DATA_ROOT / "coco"
DOG_SETS = ["dog_faces", "whole_dogs"]
# The 2% limit protects people and empty scenes (the spec: a person or no animal gets nothing).
# Cats are reported but do not set the threshold: cats are a later version, and a cat taken for
# a dog is then judged an unknown dog by the identity stage.
LIMITED_SETS = ["people", "person_heads", "scenes_no_animal"]
TARGET_DOG, TARGET_OTHER = 0.95, 0.02
YOLO_MIN = 0.35


def crop(image, box, pad=0.1):
    x, y, w, h = box
    return image.crop((max(0, x - w * pad), max(0, y - h * pad),
                       min(image.width, x + w * (1 + pad)), min(image.height, y + h * (1 + pad))))


def build_sets(per_set, rng):
    """Return {set name: [callables that open the image]} so images are loaded one at a time."""
    sets = {}
    paths, _ = list_dogfacenet()
    sets["dog_faces"] = [lambda p=paths[i]: Image.open(p).convert("RGB")
                         for i in rng.choice(len(paths), per_set, replace=False)]

    data = json.loads((COCO / "instances_val2017.json").read_text())
    names = {c["id"]: c["name"] for c in data["categories"]}
    files = {im["id"]: COCO / "val2017" / im["file_name"] for im in data["images"]}
    by_image = {}
    for a in data["annotations"]:
        by_image.setdefault(a["image_id"], []).append(a)

    def largest(category, min_side):
        out = []
        for image_id, anns in by_image.items():
            boxes = [a["bbox"] for a in anns if names[a["category_id"]] == category and not a["iscrowd"]
                     and min(a["bbox"][2], a["bbox"][3]) >= min_side]
            if boxes:
                out.append((files[image_id], max(boxes, key=lambda b: b[2] * b[3])))
        return out

    def pick(items, n):
        idx = rng.choice(len(items), min(n, len(items)), replace=False)
        return [items[i] for i in sorted(idx)]

    sets["whole_dogs"] = [lambda f=f, b=b: crop(Image.open(f).convert("RGB"), b) for f, b in pick(largest("dog", 64), per_set)]
    sets["cats"] = [lambda f=f, b=b: crop(Image.open(f).convert("RGB"), b) for f, b in pick(largest("cat", 64), per_set)]
    people = pick(largest("person", 96), per_set * 2)
    sets["people"] = [lambda f=f, b=b: crop(Image.open(f).convert("RGB"), b) for f, b in people[:per_set]]
    heads = [(f, (b[0], b[1], b[2], min(b[3], b[2] * 1.1) * 0.6)) for f, b in people[per_set:] if b[3] >= 200]
    sets["person_heads"] = [lambda f=f, b=b: crop(Image.open(f).convert("RGB"), b, pad=0.05) for f, b in heads]

    animal_or_person = {"dog", "cat", "person"}
    empty = [files[i] for i in files
             if not any(names[a["category_id"]] in animal_or_person for a in by_image.get(i, []))]
    chosen = pick(empty, per_set)
    half = len(chosen) // 2

    def zoom(f, seed):
        im = Image.open(f).convert("RGB")
        r = np.random.default_rng(seed)
        w, h = im.width // 2, im.height // 2
        x, y = int(r.integers(0, im.width - w)), int(r.integers(0, im.height - h))
        return im.crop((x, y, x + w, y + h))

    sets["scenes_no_animal"] = ([lambda f=f: Image.open(f).convert("RGB") for f in chosen[:half]]
                                + [lambda f=f, s=s: zoom(f, s) for s, f in enumerate(chosen[half:])])
    return sets


def measure(sets):
    from kibbly_ai.config import load_settings
    from kibbly_ai.perception.models import YoloDetector
    from kibbly_ai.perception.scene import ClipSceneClassifier
    yolo = YoloDetector(load_settings().yolo_weights, min_confidence=YOLO_MIN)
    clip = ClipSceneClassifier()
    records = []
    for name, loaders in sets.items():
        for i, load in enumerate(loaders):
            base = load()
            for condition in ("clean", "feeder"):
                image = feeder_camera(base, seed=i) if condition == "feeder" else base
                yolo_dog = any(d.label == "dog" for d in yolo.detect(image))
                probs = clip.classify([image])[0]
                records.append({"set": name, "index": i, "condition": condition,
                                "yolo_dog": yolo_dog, "p_dog": probs["dog"], "probs": probs})
        print(f"  {name}: {len(loaders)} images", flush=True)
    return records


def decide(r, design, t):
    if design == "A":
        return r["yolo_dog"]
    if design == "B":
        return r["yolo_dog"] or r["p_dog"] >= t
    return r["p_dog"] >= t


def rates(records, design, t, half):
    out = {}
    for s in sorted({r["set"] for r in records}):
        for condition in ("clean", "feeder"):
            rs = [r for r in records if r["set"] == s and r["condition"] == condition and r["index"] % 2 == half]
            if rs:
                out[(s, condition)] = sum(decide(r, design, t) for r in rs) / len(rs)
    return out


def choose(records, design):
    if design == "A":
        return None
    best = None
    for t in np.round(np.arange(0.05, 1.0, 0.01), 2):
        r = rates(records, design, t, half=0)
        worst_other = max(v for (s, _), v in r.items() if s in LIMITED_SETS)
        dog = np.mean([v for (s, _), v in r.items() if s in DOG_SETS])
        if worst_other <= TARGET_OTHER and (best is None or dog > best[1]):
            best = (float(t), dog)
    if best is None:
        raise SystemExit(f"design {design}: no threshold keeps every limited set at {TARGET_OTHER:.0%} or less")
    return best[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-set", type=int, default=200)
    args = parser.parse_args()
    cache = DATA_ROOT / "cache" / "recognition" / f"gate_records_{args.per_set}.json"
    if cache.exists():
        records = json.loads(cache.read_text())
    else:
        records = measure(build_sets(args.per_set, np.random.default_rng(11)))
        cache.write_text(json.dumps(records))

    results = {}
    for design in ("A", "B", "C"):
        t = choose(records, design)
        results[design] = {"threshold": t, "rates": rates(records, design, t, half=1)}

    sets = sorted({k for d in results.values() for k in d["rates"]}, key=lambda k: (k[0] not in DOG_SETS, k))
    label = {"A": "A. YOLO only", "B": "B. YOLO, then CLIP scene check", "C": "C. CLIP scene check only"}
    lines = ["# Dog or not: first stage of recognition\n",
             "Share of images taken for a dog, measured on held out images (odd numbered). "
             f"Targets: dog sets at least {TARGET_DOG:.0%}; people, person heads and scenes without animals "
             f"at most {TARGET_OTHER:.0%}. Cats are reported without a target (later version).\n",
             "| set | images | " + " | ".join(label[d] for d in results) + " |",
             "|---|---|" + "---|" * len(results)]
    for key in sets:
        n = sum(1 for r in records if r["set"] == key[0] and r["condition"] == key[1] and r["index"] % 2 == 1)
        cells = []
        for d in results:
            v = results[d]["rates"][key]
            if key[0] in DOG_SETS:
                flag = "" if v >= TARGET_DOG else " (miss)"
            elif key[0] in LIMITED_SETS:
                flag = "" if v <= TARGET_OTHER else " (miss)"
            else:
                flag = " (no target)"
            cells.append(f"{100 * v:.1f}%{flag}")
        lines.append(f"| {key[0]}, {key[1]} | {n} | " + " | ".join(cells) + " |")
    lines += ["", "CLIP dog probability threshold (chosen on even numbered images): "
              + ", ".join(f"{label[d]}: {results[d]['threshold']}" for d in results if results[d]["threshold"]), ""]
    (HERE / "results_gate.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (HERE / "results_gate.json").write_text(json.dumps(
        {d: {"threshold": v["threshold"], "rates": {f"{k[0]}|{k[1]}": x for k, x in v["rates"].items()}}
         for d, v in results.items()}, indent=2), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
