"""Build the recognizer the server uses, from the models chosen in step 4.

Heavy: importing torch and loading YOLO, CLIP and DINOv2 takes about 20 seconds and
downloads weights on the first run. The API loads this lazily, on the first recognition
call, not at startup, so the server (and the tests) start instantly.
"""

import json
import os
import pathlib

from kibbly_ai.config import Settings
from kibbly_ai.perception.gallery import Gallery
from kibbly_ai.perception.recognizer import Recognizer


def setup_caches() -> None:
    """Keep model downloads on D: even when the shell did not load the user variables."""
    os.environ.setdefault("HF_HOME", "D:/ai_cache/huggingface")
    os.environ.setdefault("YOLO_CONFIG_DIR", "D:/ai_cache/ultralytics")


def load_names(gallery_dir: pathlib.Path) -> dict:
    names_file = pathlib.Path(gallery_dir) / "names.json"
    if names_file.exists():
        return json.loads(names_file.read_text(encoding="utf-8"))
    return {}


def load_recognizer(settings: Settings) -> Recognizer:
    """Detector, scene check, embedder and the enrolled gallery, wired into a Recognizer."""
    setup_caches()
    from kibbly_ai.perception.models import ProjectedEmbedder, YoloDetector
    from kibbly_ai.perception.scene import ClipSceneClassifier

    gallery_dir = pathlib.Path(settings.gallery_dir)
    if not (gallery_dir / "gallery.json").exists():
        raise FileNotFoundError(
            f"no enrolled dogs at {gallery_dir}. Run tools/enroll.py or set KIBBLY_GALLERY_DIR."
        )
    gallery = Gallery.load(gallery_dir)
    detector = YoloDetector(settings.yolo_weights, min_confidence=0.25)
    scene = ClipSceneClassifier()
    embedder = ProjectedEmbedder()
    return Recognizer(detector, embedder, gallery, scene=scene)
