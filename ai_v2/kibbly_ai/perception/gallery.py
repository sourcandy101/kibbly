"""Gallery: the reference vectors of each enrolled dog, and nearest match search."""

import json
import pathlib

import numpy as np

from kibbly_ai.perception.base import Match, normalize


class Gallery:
    def __init__(self, embedder_name: str):
        self.embedder_name = embedder_name
        self._refs = {}                 # dog_id: array (k, dim)

    @property
    def dog_ids(self) -> list:
        return sorted(self._refs)

    def enroll(self, dog_id: str, vectors: np.ndarray) -> None:
        """Replace the references of a dog."""
        vectors = normalize(np.atleast_2d(vectors))
        if len(vectors) == 0:
            raise ValueError("at least one reference vector is needed")
        self._refs[dog_id] = vectors

    def remove(self, dog_id: str) -> None:
        self._refs.pop(dog_id, None)

    def reference_count(self, dog_id: str) -> int:
        return len(self._refs.get(dog_id, []))

    def match(self, vector: np.ndarray, dog_ids: list = None) -> list:
        """Score every dog (or only dog_ids) by its closest reference. Best first."""
        vector = normalize(np.atleast_2d(vector))[0]
        candidates = self.dog_ids if dog_ids is None else [d for d in dog_ids if d in self._refs]
        matches = [Match(d, float(np.max(self._refs[d] @ vector))) for d in candidates]
        return sorted(matches, key=lambda m: m.score, reverse=True)

    def save(self, folder) -> None:
        folder = pathlib.Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        np.savez(folder / "gallery.npz", **self._refs)
        (folder / "gallery.json").write_text(json.dumps({"embedder": self.embedder_name,
                                                         "dogs": {d: len(v) for d, v in self._refs.items()}}, indent=2))

    @classmethod
    def load(cls, folder) -> "Gallery":
        folder = pathlib.Path(folder)
        meta = json.loads((folder / "gallery.json").read_text())
        gallery = cls(meta["embedder"])
        with np.load(folder / "gallery.npz") as data:
            for dog_id in data.files:
                gallery._refs[dog_id] = data[dog_id]
        return gallery
