"""Perception tests with fake models: fast, no downloads. A real model test runs only if the data exists."""

import pathlib

import numpy as np
import pytest
from PIL import Image

from kibbly_ai.perception.base import Detection, Detector, Embedder, normalize
from kibbly_ai.perception.enrollment import build_references, most_varied
from kibbly_ai.perception.gallery import Gallery
from kibbly_ai.perception.recognizer import RecognitionSettings, Recognizer

DOGFACENET = pathlib.Path("D:/kibbly_data/dogfacenet/extracted/after_4_bis")


class FakeDetector(Detector):
    """Reads what to 'see' from the image color: red = dog, blue = person, black = nothing."""
    name = "fake"

    def detect(self, image):
        r, g, b = image.getpixel((0, 0))[:3]
        box = (10.0, 10.0, image.width - 10.0, image.height - 10.0)
        if r > 200:
            return [Detection("dog", 0.9, box), Detection("dog", 0.8, (0.0, 0.0, 5.0, 5.0))]
        if b > 200:
            return [Detection("person", 0.9, box)]
        return []


class FakeEmbedder(Embedder):
    """Vector from the green channel: images with the same green value describe the same dog."""
    name = "fake"
    dim = 3

    def embed(self, images):
        out = []
        for im in images:
            g = im.getpixel((im.width // 2, im.height // 2))[1] / 255.0
            out.append([np.cos(g * 3), np.sin(g * 3), 0.2])
        return normalize(np.array(out))


def photo(red=255, green=0, blue=0):
    return Image.new("RGB", (64, 64), (red, green, blue))


@pytest.fixture
def recognizer():
    embedder = FakeEmbedder()
    gallery = Gallery("fake")
    gallery.enroll("dog_biscuit", embedder.embed([photo(green=10)]))
    gallery.enroll("dog_mochi", embedder.embed([photo(green=200)]))
    return Recognizer(FakeDetector(), embedder, gallery, RecognitionSettings(accept_score=0.95, min_margin=0.02))


def test_known_dog_is_recognized(recognizer):
    result = recognizer.recognize(photo(green=12))
    assert result.classification == "known_dog" and result.dog_id == "dog_biscuit"
    assert 0.95 <= result.confidence <= 1.0
    assert [m.dog_id for m in result.matches] == ["dog_biscuit", "dog_mochi"]


def test_largest_dog_is_used(recognizer):
    assert recognizer.recognize(photo(green=200)).detection.area > 1000


def test_stranger_is_unknown(recognizer):
    result = recognizer.recognize(photo(green=110))
    assert result.classification == "unknown_dog" and result.dog_id is None


def test_person_and_empty_are_not_a_dog(recognizer):
    assert recognizer.recognize(photo(red=0, blue=255)).classification == "not_a_dog"
    assert recognizer.recognize(photo(red=0)).classification == "not_a_dog"


def test_restricting_candidates(recognizer):
    result = recognizer.recognize(photo(green=12), dog_ids=["dog_mochi"])
    assert result.classification == "unknown_dog"


def test_close_call_between_two_dogs_is_unsure():
    embedder = FakeEmbedder()
    gallery = Gallery("fake")
    gallery.enroll("dog_a", embedder.embed([photo(green=100)]))
    gallery.enroll("dog_b", embedder.embed([photo(green=104)]))
    rec = Recognizer(FakeDetector(), embedder, gallery, RecognitionSettings(accept_score=0.5, min_margin=0.05))
    result = rec.recognize(photo(green=102))
    assert result.classification == "unknown_dog" and "unsure" in result.reason


def test_two_frames_are_averaged(recognizer):
    result = recognizer.recognize_frames([photo(green=12), photo(green=8)])
    assert result.classification == "known_dog" and result.dog_id == "dog_biscuit"


def test_frames_without_a_dog_are_skipped(recognizer):
    result = recognizer.recognize_frames([photo(red=0), photo(green=200)])
    assert result.dog_id == "dog_mochi"
    assert recognizer.recognize_frames([photo(red=0), photo(red=0, blue=255)]).classification == "not_a_dog"


class FakeScene:
    """Says dog for green photos (close up face the detector misses), nothing otherwise."""
    name = "fake_scene"

    def classify(self, images):
        return [{"dog": 0.9 if im.getpixel((0, 0))[1] > 100 and im.getpixel((0, 0))[0] < 50 else 0.05,
                 "cat": 0.0, "person": 0.05, "nothing": 0.05} for im in images]


def test_scene_check_finds_a_dog_the_detector_missed():
    embedder = FakeEmbedder()
    gallery = Gallery("fake")
    gallery.enroll("dog_mochi", embedder.embed([photo(red=0, green=200)]))
    settings = RecognitionSettings(accept_score=0.95, min_margin=0.0)
    without = Recognizer(FakeDetector(), embedder, gallery, settings)
    with_scene = Recognizer(FakeDetector(), embedder, gallery, settings, scene=FakeScene())
    close_up = photo(red=0, green=200)
    assert without.recognize(close_up).classification == "not_a_dog"
    result = with_scene.recognize(close_up)
    assert result.dog_id == "dog_mochi" and result.detection.source == "scene_check"
    assert with_scene.recognize(photo(red=0, blue=255)).classification == "not_a_dog"


def test_default_settings_come_from_the_evaluation():
    settings = RecognitionSettings()
    assert (settings.accept_score, settings.min_margin, settings.min_scene_dog) == (0.485, 0.08, 0.89)


def test_projection_weights_are_shipped_and_valid():
    from kibbly_ai.perception.models import PROJECTION
    with np.load(PROJECTION) as data:
        matrix = data["matrix"]
    assert matrix.shape == (384, 384) and np.isfinite(matrix).all()


@pytest.mark.skipif(not DOGFACENET.exists(), reason="DogFaceNet not downloaded")
def test_projected_embedder_tells_two_dogs_apart():
    from kibbly_ai.perception.models import ProjectedEmbedder
    embedder = ProjectedEmbedder()
    a = sorted((DOGFACENET / "0").iterdir())
    b = sorted((DOGFACENET / "1").iterdir())
    vectors = embedder.embed([Image.open(p) for p in (a[0], a[1], b[0])])
    assert embedder.name == "dinov2_small_cls_proj" and vectors.shape == (3, 384)
    assert float(vectors[0] @ vectors[1]) > float(vectors[0] @ vectors[2])


def test_gallery_must_match_embedder():
    with pytest.raises(ValueError):
        Recognizer(FakeDetector(), FakeEmbedder(), Gallery("clip_b32"))


def test_gallery_save_and_load(tmp_path):
    gallery = Gallery("fake")
    gallery.enroll("dog_biscuit", np.array([[1.0, 0, 0], [0, 1.0, 0]]))
    gallery.save(tmp_path)
    loaded = Gallery.load(tmp_path)
    assert loaded.dog_ids == ["dog_biscuit"] and loaded.reference_count("dog_biscuit") == 2


def test_most_varied_picks_spread_vectors():
    vectors = normalize(np.array([[1, 0, 0], [0.99, 0.01, 0], [0, 1, 0], [0, 0, 1]]))
    chosen = most_varied(vectors, 3)
    assert len(set(chosen)) == 3 and {2, 3} <= set(chosen)


def textured(seed, blur=0.0):
    from PIL import ImageFilter
    rng = np.random.default_rng(seed)
    noise = rng.integers(0, 255, (120, 160, 3), dtype=np.uint8)
    noise[:, :, 0] = 255  # red: the fake detector sees a dog
    image = Image.fromarray(noise)
    return image.filter(ImageFilter.GaussianBlur(blur)) if blur else image


def test_soft_photos_enroll_but_heavy_blur_is_dropped():
    from kibbly_ai.perception.enrollment import sharpness
    soft = [textured(i, blur=0.8) for i in range(4)]         # soft camera, still some detail
    blurred = textured(9, blur=6)                            # heavy motion blur
    assert all(sharpness(im) >= 8 for im in soft) and sharpness(blurred) < 8
    # min_dog_confidence 0.85: the fake detector's second, smaller dog (0.8) is ignored
    vectors, report = build_references(soft + [blurred], FakeDetector(), FakeEmbedder(), k=5,
                                       min_dog_confidence=0.85)
    assert report["usable"] == 4 and report["dropped"]["blurry"] == 1


def test_build_references_drops_frames_without_a_dog():
    frames = [photo(red=0), photo(red=0, blue=255)]
    vectors, report = build_references(frames, FakeDetector(), FakeEmbedder(), k=5)
    assert len(vectors) == 0 and report["dropped"]["no_single_dog"] == 2



@pytest.mark.skipif(not DOGFACENET.exists(), reason="DogFaceNet not downloaded")
def test_real_models_tell_two_dogs_apart():
    from kibbly_ai.perception.models import DinoV2Embedder
    embedder = DinoV2Embedder()
    a = sorted((DOGFACENET / "0").iterdir())
    b = sorted((DOGFACENET / "1").iterdir())
    vectors = embedder.embed([Image.open(p) for p in (a[0], a[1], b[0])])
    same, different = float(vectors[0] @ vectors[1]), float(vectors[0] @ vectors[2])
    assert vectors.shape == (3, 384)
    assert same > different
