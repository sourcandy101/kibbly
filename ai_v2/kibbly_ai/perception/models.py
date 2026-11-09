"""Real model implementations. Heavy imports happen inside the classes so tests stay fast.

YoloDetector: Ultralytics YOLO11n, AGPL 3.0 (prototype only, see ai_v2/scope.md).
DinoV2Embedder: facebook/dinov2-small, Apache 2.0.
ClipEmbedder: openai/clip-vit-base-patch32, MIT.
"""

import numpy as np
from PIL import Image

from kibbly_ai.perception.base import LABELS, Detection, Detector, Embedder, normalize


class YoloDetector(Detector):
    def __init__(self, weights: str = "yolo11n.pt", min_confidence: float = 0.25):
        from ultralytics import YOLO
        self.model = YOLO(weights)
        self.min_confidence = min_confidence
        self.name = f"yolo:{weights.replace(chr(92), '/').split('/')[-1]}"

    def detect(self, image: Image.Image) -> list:
        result = self.model(image, verbose=False, conf=self.min_confidence)[0]
        detections = []
        for cls, conf, box in zip(result.boxes.cls, result.boxes.conf, result.boxes.xyxy):
            label = result.names[int(cls)]
            if label in LABELS:
                detections.append(Detection(label, float(conf), tuple(float(v) for v in box)))
        return detections


class _TorchEmbedder(Embedder):
    batch_size = 16

    def __init__(self, threads: int = 4):
        import torch
        torch.set_num_threads(threads)
        self.torch = torch

    def embed(self, images: list) -> np.ndarray:
        if not images:
            return np.zeros((0, self.dim), dtype=np.float32)
        chunks = []
        with self.torch.no_grad():
            for start in range(0, len(images), self.batch_size):
                batch = [im.convert("RGB") for im in images[start:start + self.batch_size]]
                chunks.append(self._forward(batch))
        return normalize(np.concatenate(chunks))

    def _forward(self, batch: list) -> np.ndarray:
        raise NotImplementedError


class DinoV2Embedder(_TorchEmbedder):
    """pooling cls: the class token. cls_mean: class token joined with the mean of the patch tokens."""

    def __init__(self, model_name: str = "facebook/dinov2-small", pooling: str = "cls", threads: int = 4):
        super().__init__(threads)
        from transformers import AutoImageProcessor, AutoModel
        self.processor = AutoImageProcessor.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).eval()
        self.pooling = pooling
        hidden = self.model.config.hidden_size
        self.dim = hidden * 2 if pooling == "cls_mean" else hidden
        self.name = f"dinov2_small_{pooling}"

    def _forward(self, batch):
        out = self.model(**self.processor(images=batch, return_tensors="pt")).last_hidden_state
        cls = out[:, 0]
        if self.pooling == "cls_mean":
            cls = self.torch.cat([normalize_t(self.torch, cls), normalize_t(self.torch, out[:, 1:].mean(dim=1))], dim=1)
        return cls.numpy()


class ClipEmbedder(_TorchEmbedder):
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32", threads: int = 4):
        super().__init__(threads)
        from transformers import CLIPModel, CLIPProcessor
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model = CLIPModel.from_pretrained(model_name).eval()
        self.dim = self.model.config.projection_dim
        self.name = "clip_b32"

    def _forward(self, batch):
        features = self.model.get_image_features(**self.processor(images=batch, return_tensors="pt"))
        if not self.torch.is_tensor(features):  # some transformers versions return an output object
            features = features.pooler_output
        return features.numpy()


PROJECTION = __import__("pathlib").Path(__file__).resolve().parent / "weights" / "dinov2_projection.npz"


class ProjectedEmbedder(Embedder):
    """DINOv2 small class token followed by the learned 384 x 384 layer (evaluation/recognition/
    train_projection.py), trained on DogFaceNet train dogs so that clean and feeder quality
    photos of the same dog match better."""

    def __init__(self, base: Embedder = None, weights=PROJECTION):
        import numpy as np
        self.base = base or DinoV2Embedder(pooling="cls")
        with np.load(weights) as data:
            self.matrix = data["matrix"].astype(np.float32)
        self.dim = self.matrix.shape[1]
        self.name = "dinov2_small_cls_proj"

    def embed(self, images: list) -> np.ndarray:
        return normalize(self.base.embed(images) @ self.matrix)


def normalize_t(torch, x):
    return x / x.norm(dim=1, keepdim=True).clamp_min(1e-12)


def make_embedder(name: str) -> Embedder:
    if name == "dinov2_small_cls":
        return DinoV2Embedder(pooling="cls")
    if name == "dinov2_small_cls_mean":
        return DinoV2Embedder(pooling="cls_mean")
    if name == "clip_b32":
        return ClipEmbedder()
    if name == "dinov2_small_cls_proj":
        return ProjectedEmbedder()
    raise ValueError(f"unknown embedder {name}")
