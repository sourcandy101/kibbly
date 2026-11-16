"""Enrollment: build a dog's reference images from the owner's photos and video.

1. Sample frames from the video (about 3 per second).
2. Keep frames with one clear dog, cropped.
3. Drop blurry crops (variance of the Laplacian below a limit).
4. Describe every crop, then keep the most varied ones (farthest point sampling).
"""

import cv2
import numpy as np
from PIL import Image

from kibbly_ai.perception.base import Detector, Embedder
from kibbly_ai.perception.recognizer import crop_box


def sample_video_frames(path: str, per_second: float = 3.0, max_frames: int = 300) -> list:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise ValueError(f"cannot open video {path}")
    fps = capture.get(cv2.CAP_PROP_FPS) or 30.0
    step = max(1, int(round(fps / per_second)))
    frames, index = [], 0
    while len(frames) < max_frames:
        ok, frame = capture.read()
        if not ok:
            break
        if index % step == 0:
            frames.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        index += 1
    capture.release()
    return frames


def sharpness(image: Image.Image) -> float:
    """Variance of the Laplacian on the image scaled to 224 pixels high, so the value does not
    depend on the photo size."""
    image = image.convert("RGB")
    scale = 224 / max(1, image.height)
    image = image.resize((max(1, round(image.width * scale)), 224))
    gray = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())


def most_varied(vectors: np.ndarray, k: int) -> list:
    """Indexes of k vectors spread as far apart as possible, starting from the most typical one."""
    if len(vectors) <= k:
        return list(range(len(vectors)))
    center = vectors.mean(axis=0)
    chosen = [int(np.argmax(vectors @ center))]
    closest = vectors @ vectors[chosen[0]]
    while len(chosen) < k:
        nxt = int(np.argmin(closest))
        chosen.append(nxt)
        closest = np.maximum(closest, vectors @ vectors[nxt])
    return chosen


def build_references(images: list, detector: Detector, embedder: Embedder, k: int = 12,
                     min_sharpness: float = 8.0, min_dog_confidence: float = 0.5, padding: float = 0.10,
                     scene=None, min_scene_dog: float = 0.89):
    """Return (vectors, report). report explains what was kept, for the app and for debugging.
    With a scene classifier, a photo where the detector finds no dog is kept whole if the scene
    check says dog (close ups, as in recognition).
    Blur: a crop is dropped below min_sharpness, measured at a fixed size. Measured values: heavy
    motion blur 2 to 4, simulated feeder camera 17 to 37, clean photos 37 to over 2,000 (fur
    texture changes it a lot, so no rule relative to the batch is used)."""
    candidates, dropped = [], {"no_single_dog": 0, "blurry": 0}
    for image in images:
        dogs = [d for d in detector.detect(image) if d.label == "dog" and d.confidence >= min_dog_confidence]
        if len(dogs) == 1:
            crop = crop_box(image, dogs[0].box, padding)
        elif not dogs and scene is not None and scene.classify([image])[0]["dog"] >= min_scene_dog:
            crop = image
        else:
            dropped["no_single_dog"] += 1
            continue
        candidates.append((crop, sharpness(crop)))
    crops = []
    for crop, value in candidates:
        if value < min_sharpness:
            dropped["blurry"] += 1
        else:
            crops.append(crop)
    if not crops:
        return np.zeros((0, embedder.dim), dtype=np.float32), {"kept": 0, "usable": 0, "dropped": dropped}
    vectors = embedder.embed(crops)
    keep = most_varied(vectors, k)
    return vectors[keep], {"kept": len(keep), "usable": len(crops), "dropped": dropped}
