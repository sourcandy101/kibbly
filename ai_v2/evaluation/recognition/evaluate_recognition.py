"""Recognition evaluation with simulated homes.

  python evaluation/recognition/evaluate_recognition.py [--homes 1500]

Method
1. Dogs are split three ways (common.split_dogs): train dogs (only used to train the learned
   layer, see train_projection.py), calibration dogs (choose the threshold) and test dogs
   (report results). No dog is in two sets.
2. A simulated home has 2 to 4 dogs. Each dog is enrolled with K clean photos (the owner's
   phone). Queries are the dog's other photos, clean or through the feeder camera simulation.
3. Strangers: 6 dogs from outside the home (same half) try to eat.
4. Look alike homes: dogs chosen with the most similar coat colors (model independent).
5. Two frame mode: the feeder takes two photos and averages the scores.
6. For every setting the threshold and margin are chosen on calibration dogs to meet the
   targets (at most 2% strangers accepted, at most 2% wrong dog accepted), then measured on
   test dogs. Target for the right dog: at least 90% accepted at the first check.

Writes results_recognition.md and results_recognition.json next to this file.
"""

import argparse
import datetime
import json
import sys
from dataclasses import dataclass

import numpy as np

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))

from evaluation.recognition.common import HERE, cache_file, split_dogs  # noqa: E402

MODELS = ["dinov2_small_cls_proj", "dinov2_small_cls", "dinov2_small_cls_mean", "clip_b32"]
TARGET_STRANGER, TARGET_WRONG, TARGET_RIGHT = 0.02, 0.02, 0.90
STRANGERS_PER_HOME = 6
THRESHOLDS = np.round(np.arange(0.30, 0.995, 0.005), 3)
MARGINS = [0.0, 0.02, 0.04, 0.06, 0.08, 0.10]


@dataclass
class Home:
    dogs: list          # dog indexes
    enroll: list        # per dog: image indexes used as references
    queries: list       # (dog index, [image indexes]) genuine query groups
    strangers: list     # (stranger dog index, [image indexes])


def load_vectors(model, condition):
    data = np.load(cache_file(model, condition))
    return data["vectors"], data["labels"]


def dog_index(labels):
    by_dog = {}
    for i, label in enumerate(labels):
        by_dog.setdefault(label, []).append(i)
    return [np.array(v) for _, v in sorted(by_dog.items(), key=lambda kv: int(kv[0]))]


def color_similarity(images_by_dog, colors):
    means = np.stack([colors[idx].mean(axis=0) for idx in images_by_dog])
    # histogram intersection between every pair of dogs
    return np.minimum(means[:, None, :], means[None, :, :]).sum(axis=2)


def make_homes(rng, dogs, images_by_dog, k, frames, count, lookalike, color_sim):
    eligible = [d for d in dogs if len(images_by_dog[d]) >= k + frames]
    strangers_pool = [d for d in dogs if len(images_by_dog[d]) >= frames]
    homes = []
    for _ in range(count):
        size = int(rng.choice([2, 3, 4]))
        if lookalike:
            anchor = int(rng.choice(eligible))
            others = [d for d in eligible if d != anchor]
            nearest = sorted(others, key=lambda d: -color_sim[anchor, d])[:10]
            members = [anchor] + [int(d) for d in rng.choice(nearest, size - 1, replace=False)]
        else:
            members = [int(d) for d in rng.choice(eligible, size, replace=False)]
        enroll, queries = [], []
        for d in members:
            images = rng.permutation(images_by_dog[d])
            enroll.append(images[:k])
            rest = images[k:]
            for start in range(0, len(rest) - frames + 1, frames):
                queries.append((d, rest[start:start + frames]))
        outsiders = [d for d in strangers_pool if d not in members]
        strangers = []
        for d in rng.choice(outsiders, STRANGERS_PER_HOME, replace=False):
            strangers.append((int(d), rng.choice(images_by_dog[d], frames, replace=False)))
        homes.append(Home(members, enroll, queries, strangers))
    return homes


def score_homes(homes, enroll_vectors, query_vectors):
    """Return arrays: is_genuine, correct (best dog is the true dog), best score, margin."""
    genuine, correct, best, margin = [], [], [], []
    for home in homes:
        refs = [enroll_vectors[idx] for idx in home.enroll]
        for true_dog, group, is_genuine in ([(d, g, True) for d, g in home.queries]
                                            + [(d, g, False) for d, g in home.strangers]):
            q = query_vectors[group]                                   # (frames, dim)
            scores = np.array([np.max(r @ q.T, axis=0).mean() for r in refs])
            order = np.argsort(-scores)
            genuine.append(is_genuine)
            correct.append(is_genuine and home.dogs[order[0]] == true_dog)
            best.append(scores[order[0]])
            margin.append(scores[order[0]] - (scores[order[1]] if len(scores) > 1 else 0.0))
    return np.array(genuine), np.array(correct), np.array(best), np.array(margin)


def rates(scored, threshold, min_margin):
    genuine, correct, best, margin = scored
    accepted = (best >= threshold) & (margin >= min_margin)
    n_gen, n_str = genuine.sum(), (~genuine).sum()
    return {
        "right_accepted": float((accepted & genuine & correct).sum() / n_gen),
        "wrong_dog_accepted": float((accepted & genuine & ~correct).sum() / n_gen),
        "stranger_accepted": float((accepted & ~genuine).sum() / n_str),
        "genuine_queries": int(n_gen),
        "stranger_queries": int(n_str),
    }


def choose(scored):
    """Best right dog rate that keeps strangers and wrong dogs within target on calibration dogs."""
    best = None
    for m in MARGINS:
        for t in THRESHOLDS:
            r = rates(scored, t, m)
            if r["stranger_accepted"] <= TARGET_STRANGER and r["wrong_dog_accepted"] <= TARGET_WRONG:
                if best is None or r["right_accepted"] > best[2]["right_accepted"]:
                    best = (float(t), float(m), r)
                break  # higher thresholds only lower the right dog rate for this margin
    return best


def run(homes_per_setting, seed):
    clean = {m: load_vectors(m, "clean") for m in MODELS}
    feeder = {m: load_vectors(m, "feeder")[0] for m in MODELS}
    labels = clean[MODELS[0]][1]
    images_by_dog = dog_index(labels)
    colors = np.load(cache_file("colors", "clean"))["colors"]
    color_sim = color_similarity(images_by_dog, colors)

    _, calibration, test = split_dogs(images_by_dog, seed)

    rows = []
    for k in (1, 3, 5):
        for frames in (1, 2):
            specs = {}
            for split_name, split in (("calibration", calibration), ("test", test)):
                for lookalike in (False, True):
                    specs[(split_name, lookalike)] = make_homes(
                        np.random.default_rng(seed + 100 * k + 10 * frames + lookalike),
                        split, images_by_dog, k, frames, homes_per_setting, lookalike, color_sim)
            for model in MODELS:
                for condition, query in (("clean", clean[model][0]), ("feeder", feeder[model])):
                    enroll = clean[model][0]
                    chosen = choose(score_homes(specs[("calibration", False)], enroll, query))
                    if chosen is None:
                        continue
                    t, m, _ = chosen
                    for lookalike in (False, True):
                        r = rates(score_homes(specs[("test", lookalike)], enroll, query), t, m)
                        rows.append({"model": model, "k": k, "frames": frames, "condition": condition,
                                     "homes": "look_alike" if lookalike else "normal",
                                     "threshold": t, "margin": m, **r,
                                     "meets_targets": (r["right_accepted"] >= TARGET_RIGHT
                                                       and r["stranger_accepted"] <= TARGET_STRANGER
                                                       and r["wrong_dog_accepted"] <= TARGET_WRONG)})
                    print(f"k={k} frames={frames} {model:22} {condition:6} t={t:.3f} m={m:.2f} "
                          f"right={rows[-2]['right_accepted']:.3f} stranger={rows[-2]['stranger_accepted']:.3f} "
                          f"wrong={rows[-2]['wrong_dog_accepted']:.3f}", flush=True)
    return {"timestamp": datetime.datetime.now().isoformat(timespec="seconds"), "seed": seed,
            "homes_per_setting": homes_per_setting, "calibration_dogs": len(calibration),
            "test_dogs": len(test), "rows": rows}


def pct(x):
    return f"{100 * x:.1f}%"


def table(rows, columns):
    head = "| " + " | ".join(c for c, _ in columns) + " |\n|" + "---|" * len(columns) + "\n"
    return head + "\n".join("| " + " | ".join(f(r) for _, f in columns) + " |" for r in rows) + "\n"


def report(data):
    rows = data["rows"]

    def pick(**kw):
        return [r for r in rows if all(r[a] == b for a, b in kw.items())]

    ok = lambda r: "yes" if r["meets_targets"] else "no"  # noqa: E731
    base = [("right dog accepted", lambda r: pct(r["right_accepted"])),
            ("stranger accepted", lambda r: pct(r["stranger_accepted"])),
            ("wrong dog accepted", lambda r: pct(r["wrong_dog_accepted"])),
            ("threshold", lambda r: f"{r['threshold']:.3f}"), ("margin", lambda r: f"{r['margin']:.2f}"),
            ("meets targets", ok)]
    main = pick(k=3, frames=1, condition="feeder", homes="normal")
    best_model = max(main, key=lambda r: r["right_accepted"])["model"]
    out = [f"# Dog recognition evaluation\n\nTimestamp: {data['timestamp']}  \nData: DogFaceNet (CC BY 4.0), "
           f"{data['calibration_dogs']} calibration dogs and {data['test_dogs']} different test dogs, "
           f"{data['homes_per_setting']} simulated homes per setting, seed {data['seed']}.\n\n"
           f"Targets: right dog accepted at least {pct(TARGET_RIGHT)}, strangers and wrong dogs accepted at most "
           f"{pct(TARGET_STRANGER)}. Thresholds are chosen on calibration dogs and measured on test dogs.\n",
           "## 1. Model comparison\n\n3 enrollment photos, 1 photo per check, feeder camera simulation, normal homes.\n",
           table(main, [("model", lambda r: r["model"])] + base),
           f"\nBest model: **{best_model}**.\n\n## 2. {best_model}: photos per dog, photos per check, image quality\n\n"
           "Normal homes.\n",
           table(pick(model=best_model, homes="normal"),
                 [("enroll photos", lambda r: str(r["k"])), ("photos per check", lambda r: str(r["frames"])),
                  ("query images", lambda r: r["condition"])] + base),
           f"\n## 3. {best_model}: look alike homes (similar coat colors)\n\nSame thresholds as normal homes, "
           "feeder camera simulation.\n",
           table(pick(model=best_model, condition="feeder"),
                 [("enroll photos", lambda r: str(r["k"])), ("photos per check", lambda r: str(r["frames"])),
                  ("homes", lambda r: r["homes"])] + base),
           "\n## 4. All models, every setting\n\n",
           table(rows, [("model", lambda r: r["model"]), ("enroll", lambda r: str(r["k"])),
                        ("frames", lambda r: str(r["frames"])), ("images", lambda r: r["condition"]),
                        ("homes", lambda r: r["homes"])] + base),
           "\n## Definitions\n\n1. **right dog accepted**: a home dog is recognized as itself at the first check.\n"
           "2. **wrong dog accepted**: a home dog is recognized as another home dog (it would eat the other dog's meal).\n"
           "3. **stranger accepted**: a dog from outside the home is recognized as a home dog.\n"
           "4. Not accepted means unknown: nothing is served and the feeder checks again a few seconds later.\n"]
    return "".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--homes", type=int, default=1500)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    data = run(args.homes, args.seed)
    (HERE / "results_recognition.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (HERE / "results_recognition.md").write_text(report(data), encoding="utf-8")
    print("written", HERE / "results_recognition.md")


if __name__ == "__main__":
    main()
