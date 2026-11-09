"""Recognition pipeline: find the dog, describe it, match it to the enrolled dogs.

Finding the dog: the detector looks for a dog box. If it finds none, the scene check
judges the whole photo (YOLO misses close up faces, see evaluation/recognition/README.md).
The thresholds here only label what was seen (known dog, unknown dog, not a dog).
Whether to serve is decided by the engines from this result.
"""

from dataclasses import dataclass

from PIL import Image

from kibbly_ai.perception.base import Detection, Detector, Embedder, Match, RecognitionResult
from kibbly_ai.perception.gallery import Gallery
from kibbly_ai.perception.scene import SceneClassifier


@dataclass(frozen=True)
class RecognitionSettings:
    # Chosen in step 4.6 (evaluation/recognition/results_recognition.md) for the embedder
    # dinov2_small_cls_proj (DINOv2 small with the learned layer), 3 enrollment photos,
    # 2 photos per check, feeder camera simulation, at most 2% strangers on calibration dogs.
    accept_score: float = 0.485
    min_margin: float = 0.08        # best dog must beat the second best by this much, else unsure
    min_dog_confidence: float = 0.35
    min_scene_dog: float = 0.89     # CLIP dog probability, chosen by evaluation/recognition/gate_check.py
    crop_padding: float = 0.10      # grow the dog box by 10% on each side


def crop_box(image: Image.Image, box, padding: float) -> Image.Image:
    x1, y1, x2, y2 = box
    pad_x, pad_y = (x2 - x1) * padding, (y2 - y1) * padding
    return image.crop((max(0, x1 - pad_x), max(0, y1 - pad_y),
                       min(image.width, x2 + pad_x), min(image.height, y2 + pad_y)))


class Recognizer:
    def __init__(self, detector: Detector, embedder: Embedder, gallery: Gallery,
                 settings: RecognitionSettings = RecognitionSettings(), scene: SceneClassifier = None):
        if gallery.embedder_name != embedder.name:
            raise ValueError(f"gallery built with {gallery.embedder_name}, embedder is {embedder.name}")
        self.detector, self.embedder, self.gallery = detector, embedder, gallery
        self.settings, self.scene = settings, scene

    def find_dog(self, image: Image.Image):
        """The largest dog box; else the whole photo if the scene check says dog; else None."""
        dogs = [d for d in self.detector.detect(image)
                if d.label == "dog" and d.confidence >= self.settings.min_dog_confidence]
        if dogs:
            return max(dogs, key=lambda d: d.area)
        if self.scene is not None:
            p_dog = self.scene.classify([image])[0]["dog"]
            if p_dog >= self.settings.min_scene_dog:
                return Detection("dog", p_dog, (0.0, 0.0, float(image.width), float(image.height)), "scene_check")
        return None

    def recognize(self, image: Image.Image, dog_ids: list = None) -> RecognitionResult:
        return self.recognize_frames([image], dog_ids)

    def recognize_frames(self, images: list, dog_ids: list = None) -> RecognitionResult:
        """Several photos of the same visit (the feeder sends 2): scores are averaged per dog.
        Frames without a dog are skipped; if none has a dog the result is not_a_dog."""
        found = [(image, self.find_dog(image)) for image in images]
        found = [(image, dog) for image, dog in found if dog is not None]
        if not found:
            return RecognitionResult("not_a_dog", reason=f"no dog found in {len(images)} photo(s)")
        crops = [image if dog.source == "scene_check" else crop_box(image, dog.box, self.settings.crop_padding)
                 for image, dog in found]
        vectors = self.embedder.embed(crops)
        per_frame = [{m.dog_id: m.score for m in self.gallery.match(v, dog_ids)} for v in vectors]
        averaged = {d: sum(f[d] for f in per_frame) / len(per_frame) for d in per_frame[0]}
        return self._label(averaged, detection=max((dog for _, dog in found), key=lambda d: d.area))

    def classify(self, vector, dog_ids: list = None, detection=None) -> RecognitionResult:
        """Label an already computed vector. Used by the evaluation."""
        return self._label({m.dog_id: m.score for m in self.gallery.match(vector, dog_ids)}, detection)

    def _label(self, scores: dict, detection=None) -> RecognitionResult:
        matches = sorted((Match(d, s) for d, s in scores.items()), key=lambda m: m.score, reverse=True)
        if not matches:
            return RecognitionResult("unknown_dog", detection=detection, reason="no dog enrolled")
        best = matches[0]
        margin = best.score - matches[1].score if len(matches) > 1 else best.score
        confidence = min(1.0, max(0.0, best.score))
        if best.score < self.settings.accept_score:
            return RecognitionResult("unknown_dog", None, confidence, margin, matches, detection,
                                     f"best match {best.dog_id} {best.score:.2f} below {self.settings.accept_score:.2f}")
        if margin < self.settings.min_margin:
            return RecognitionResult("unknown_dog", None, confidence, margin, matches, detection,
                                     f"unsure between {best.dog_id} and {matches[1].dog_id}")
        return RecognitionResult("known_dog", best.dog_id, confidence, margin, matches, detection,
                                 f"{best.dog_id} {best.score:.2f}")
