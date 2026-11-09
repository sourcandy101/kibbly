"""Interfaces and result types of the perception layer.

Detector: finds dogs, cats and people in a photo.
Embedder: turns a dog image into a unit length vector that describes its look.
Both are interfaces so models can be swapped (for example a detector with a
permissive license before commercial use).
"""

from dataclasses import dataclass, field

import numpy as np
from PIL import Image

LABELS = ("dog", "cat", "person")


@dataclass(frozen=True)
class Detection:
    label: str                  # one of LABELS
    confidence: float           # detector confidence, 0 to 1
    box: tuple                  # (x1, y1, x2, y2) in pixels
    source: str = "detector"    # detector, or scene_check when the whole photo was judged a dog

    @property
    def area(self) -> float:
        x1, y1, x2, y2 = self.box
        return max(0.0, x2 - x1) * max(0.0, y2 - y1)


@dataclass
class Match:
    dog_id: str
    score: float                # cosine similarity to the closest reference image, about 0 to 1


@dataclass
class RecognitionResult:
    """What perception saw. It does not decide to serve: the engines do."""

    classification: str         # known_dog, unknown_dog, not_a_dog (same names as schemas/visit.json)
    dog_id: str = None          # set only for known_dog
    confidence: float = None    # score of the best match, clipped to 0 to 1
    margin: float = None        # best score minus the second best dog's score
    matches: list = field(default_factory=list)   # every enrolled dog, best first
    detection: Detection = None
    reason: str = ""            # short explanation for logs and the demo


class Detector:
    name = "base"

    def detect(self, image: Image.Image) -> list:
        """Return a list of Detection, any order."""
        raise NotImplementedError


class Embedder:
    name = "base"
    dim = 0

    def embed(self, images: list) -> np.ndarray:
        """Return an array of shape (len(images), dim) with unit length rows."""
        raise NotImplementedError


def normalize(vectors: np.ndarray) -> np.ndarray:
    vectors = np.asarray(vectors, dtype=np.float32)
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / np.maximum(norms, 1e-12)
