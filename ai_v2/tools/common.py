"""Shared helpers for the hands on test tools: camera access, model loading, galleries, saving photos."""

import datetime
import io
import json
import os
import pathlib
import sys
import time
import urllib.request

AI_V2 = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AI_V2))

from PIL import Image  # noqa: E402

DATA_ROOT = pathlib.Path(os.environ.get("KIBBLY_DATA_ROOT", "D:/kibbly_data"))
DEFAULT_GALLERY = DATA_ROOT / "galleries" / "demo"
REAL_PHOTOS = DATA_ROOT / "real"
EMBEDDER_NAME = "dinov2_small_cls_proj"


def setup_caches():
    """Keep model downloads on D: even when the shell did not load the user variables."""
    os.environ.setdefault("HF_HOME", str(pathlib.Path("D:/ai_cache/huggingface")))
    os.environ.setdefault("YOLO_CONFIG_DIR", str(pathlib.Path("D:/ai_cache/ultralytics")))


def camera_url(ip: str, path: str) -> str:
    host = ip if ip.startswith("http") else f"http://{ip}"
    return host.rstrip("/") + path


def fetch_status(ip: str, timeout: float = 5.0) -> dict:
    with urllib.request.urlopen(camera_url(ip, "/status"), timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_photo(ip: str, flash: bool = False, timeout: float = 10.0):
    """Return (PIL image, JPEG bytes, seconds taken)."""
    start = time.perf_counter()
    with urllib.request.urlopen(camera_url(ip, "/capture" + ("?flash=1" if flash else "")), timeout=timeout) as r:
        data = r.read()
    seconds = time.perf_counter() - start
    return Image.open(io.BytesIO(data)).convert("RGB"), data, seconds


def session_folder(kind: str) -> pathlib.Path:
    folder = REAL_PHOTOS / f"{datetime.datetime.now():%Y-%m-%d_%H%M%S}_{kind}"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def load_models(with_embedder: bool = True):
    """Detector, scene check and (optionally) the embedder used by the recognizer defaults."""
    setup_caches()
    from kibbly_ai.config import load_settings
    from kibbly_ai.perception.models import ProjectedEmbedder, YoloDetector
    from kibbly_ai.perception.scene import ClipSceneClassifier
    detector = YoloDetector(load_settings().yolo_weights, min_confidence=0.25)
    scene = ClipSceneClassifier()
    embedder = ProjectedEmbedder() if with_embedder else None
    return detector, scene, embedder


def load_gallery(folder: pathlib.Path):
    """Return (Gallery, names). A new empty gallery if the folder has none."""
    from kibbly_ai.perception.gallery import Gallery
    names_file = folder / "names.json"
    if (folder / "gallery.json").exists():
        gallery = Gallery.load(folder)
    else:
        gallery = Gallery(EMBEDDER_NAME)
    names = json.loads(names_file.read_text(encoding="utf-8")) if names_file.exists() else {}
    return gallery, names


def save_gallery(gallery, names: dict, folder: pathlib.Path):
    gallery.save(folder)
    (folder / "names.json").write_text(json.dumps(names, indent=2, ensure_ascii=False), encoding="utf-8")
