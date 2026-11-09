"""Train a small layer on top of DINOv2 so that clean and feeder quality photos of the same dog match.

  python evaluation/recognition/train_projection.py

Uses only the train dogs of split_dogs() (never calibration or test dogs).
The layer is one 384 x 384 matrix, started at the identity (no change), trained with a
contrastive loss: a clean photo of a dog must be closer to another photo of the same dog
(usually at feeder quality) than to photos of the other dogs in the batch.
20% of the train dogs are held back to pick the best training step. A penalty keeps the
layer close to the identity, so it cannot drift far from what DINOv2 already knows.

Writes:
  ai_v2/kibbly_ai/perception/weights/dinov2_projection.npz   (used by the server)
  D:/kibbly_data/cache/recognition/dinov2_small_cls_proj_<condition>.npz   (for the evaluation)
"""

import json
import pathlib
import sys

import numpy as np
import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

from evaluation.recognition.common import HERE, cache_file, images_by_dog, split_dogs  # noqa: E402
from kibbly_ai.perception.base import normalize  # noqa: E402

WEIGHTS = pathlib.Path(__file__).resolve().parents[2] / "kibbly_ai" / "perception" / "weights" / "dinov2_projection.npz"
STEPS, BATCH_DOGS, TEMPERATURE, LR, P_FEEDER, STAY_CLOSE = 1500, 64, 0.07, 5e-4, 0.7, 1e-2
VAL_SHARE, VAL_DRAWS, CHECK_EVERY = 0.2, 20, 100


def recall_at_1(W, clean, feeder, groups, dogs, seed=123):
    """Enroll one clean photo per dog, query with another photo at feeder quality: share of correct top
    matches, averaged over VAL_DRAWS random pairings (the same pairings at every check)."""
    rng = np.random.default_rng(seed)
    return float(np.mean([_recall_once(W, clean, feeder, groups, dogs, rng) for _ in range(VAL_DRAWS)]))


def _recall_once(W, clean, feeder, groups, dogs, rng):
    refs, queries, truth = [], [], []
    for j, d in enumerate(dogs):
        a, b = rng.choice(groups[d], 2, replace=False)
        refs.append(clean[a])
        queries.append(feeder[b])
        truth.append(j)
    r = normalize(np.array(refs) @ W)
    q = normalize(np.array(queries) @ W)
    return float(np.mean(np.argmax(q @ r.T, axis=1) == np.array(truth)))


def main():
    torch.manual_seed(0)
    rng = np.random.default_rng(0)
    clean_data = np.load(cache_file("dinov2_small_cls", "clean"))
    clean, labels = clean_data["vectors"], clean_data["labels"]
    feeder = np.load(cache_file("dinov2_small_cls", "feeder"))["vectors"]
    groups = images_by_dog(labels)
    train, calibration, test = split_dogs(groups)
    train = [d for d in train if len(groups[d]) >= 2]
    train = list(rng.permutation(train))
    n_val = int(len(train) * VAL_SHARE)
    val, fit = sorted(train[:n_val]), sorted(train[n_val:])
    print(f"dogs: fit {len(fit)}, validation {len(val)}, calibration {len(calibration)}, test {len(test)}")

    dim = clean.shape[1]
    W = torch.nn.Parameter(torch.eye(dim))
    optimizer = torch.optim.Adam([W], lr=LR)
    identity = torch.eye(dim)
    clean_t, feeder_t = torch.from_numpy(clean), torch.from_numpy(feeder)
    eye = np.eye(dim, dtype=np.float32)
    best = (recall_at_1(eye, clean, feeder, groups, val), 0, eye.copy())
    print(f"step 0 (no change): validation recall at 1 = {best[0]:.3f}")
    history = [{"step": 0, "val_recall_at_1": best[0]}]

    for step in range(1, STEPS + 1):
        dogs = rng.choice(fit, BATCH_DOGS, replace=False)
        a_idx, b_idx, b_feeder = [], [], []
        for d in dogs:
            a, b = rng.choice(groups[d], 2, replace=False)
            a_idx.append(a)
            b_idx.append(b)
            b_feeder.append(rng.random() < P_FEEDER)
        x1 = clean_t[a_idx]
        x2 = torch.where(torch.tensor(b_feeder)[:, None], feeder_t[b_idx], clean_t[b_idx])
        z1 = torch.nn.functional.normalize(x1 @ W, dim=1)
        z2 = torch.nn.functional.normalize(x2 @ W, dim=1)
        logits = z1 @ z2.T / TEMPERATURE
        target = torch.arange(len(dogs))
        loss = (torch.nn.functional.cross_entropy(logits, target)
                + torch.nn.functional.cross_entropy(logits.T, target)) / 2
        loss = loss + STAY_CLOSE * ((W - identity) ** 2).sum()  # stay close to no change
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if step % CHECK_EVERY == 0:
            current = W.detach().numpy().copy()
            score = recall_at_1(current, clean, feeder, groups, val)
            history.append({"step": step, "loss": float(loss.detach()), "val_recall_at_1": score})
            print(f"step {step}: loss {float(loss.detach()):.3f}, validation recall at 1 = {score:.3f}", flush=True)
            if score > best[0]:
                best = (score, step, current)

    score, step, matrix = best
    print(f"best: step {step}, validation recall at 1 = {score:.3f}")
    WEIGHTS.parent.mkdir(parents=True, exist_ok=True)
    np.savez(WEIGHTS, matrix=matrix.astype(np.float32), step=step, val_recall_at_1=score)
    for condition, vectors in (("clean", clean), ("feeder", feeder)):
        np.savez(cache_file("dinov2_small_cls_proj", condition), vectors=normalize(vectors @ matrix),
                 labels=labels, paths=clean_data["paths"])
    (HERE / "training_projection.json").write_text(json.dumps(
        {"best_step": step, "best_val_recall_at_1": score, "fit_dogs": len(fit), "validation_dogs": len(val),
         "settings": {"steps": STEPS, "batch_dogs": BATCH_DOGS, "temperature": TEMPERATURE, "lr": LR,
                      "p_feeder": P_FEEDER, "stay_close": STAY_CLOSE,
                      "validation_share": VAL_SHARE, "validation_draws": VAL_DRAWS},
         "history": history}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
