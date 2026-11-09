"""Scene check: is the whole photo a dog, a cat, a person or nothing?

Used when the detector finds no dog box. YOLO is trained on whole animals seen from a
distance and misses close up faces, while the ultrasonic sensor already says something
is in front of the feeder. CLIP is weak at telling two dogs apart but strong at this
kind of category question, so it answers it from the whole photo.
"""

import numpy as np
from PIL import Image

PROMPTS = {
    "dog": ["a photo of a dog", "a close up photo of a dog's face", "a dog eating from a bowl",
            "a blurry photo of a dog in dim light"],
    "cat": ["a photo of a cat", "a close up photo of a cat's face"],
    "person": ["a photo of a person", "a close up photo of a person's face", "a person's hand",
               "a person's legs and feet"],
    "nothing": ["a photo of an empty floor", "a photo of an empty room", "an empty bowl on the floor",
                "a photo of furniture", "a dark blurry photo"],
}


class SceneClassifier:
    name = "base"

    def classify(self, images: list) -> list:
        """Return one dict per image: {"dog": p, "cat": p, "person": p, "nothing": p}, summing to 1."""
        raise NotImplementedError


class ClipSceneClassifier(SceneClassifier):
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32", threads: int = 4):
        import torch
        from transformers import CLIPModel, CLIPProcessor
        torch.set_num_threads(threads)
        self.torch = torch
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model = CLIPModel.from_pretrained(model_name).eval()
        self.name = "clip_b32_scene"
        self.groups, texts = [], []
        for group, prompts in PROMPTS.items():
            self.groups += [group] * len(prompts)
            texts += prompts
        with torch.no_grad():
            text = self.model.get_text_features(**self.processor(text=texts, return_tensors="pt", padding=True))
            text = text if torch.is_tensor(text) else text.pooler_output
        self.text = (text / text.norm(dim=1, keepdim=True)).numpy()
        self.scale = float(self.model.logit_scale.detach().exp())

    def classify(self, images: list) -> list:
        with self.torch.no_grad():
            feats = self.model.get_image_features(**self.processor(images=[i.convert("RGB") for i in images],
                                                                   return_tensors="pt"))
            feats = feats if self.torch.is_tensor(feats) else feats.pooler_output
        feats = (feats / feats.norm(dim=1, keepdim=True)).numpy()
        logits = self.scale * feats @ self.text.T
        probs = np.exp(logits - logits.max(axis=1, keepdims=True))
        probs /= probs.sum(axis=1, keepdims=True)
        out = []
        for row in probs:
            groups = {g: 0.0 for g in PROMPTS}
            for g, p in zip(self.groups, row):
                groups[g] += float(p)
            out.append(groups)
        return out
