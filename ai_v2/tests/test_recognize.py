"""The recognition endpoints, with a fake recognizer and a fake camera: fast, no models."""

import io

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from kibbly_ai.api.app import create_app
from kibbly_ai.perception.base import Detection, Match, RecognitionResult

KEY = {"X-Kibbly-Key": "demo_feeder_key"}


def jpeg_bytes(color=(255, 0, 0)):
    buffer = io.BytesIO()
    Image.new("RGB", (32, 32), color).save(buffer, "JPEG")
    return buffer.getvalue()


class FakeRecognizer:
    def __init__(self, result):
        self.result = result
        self.frames_seen = None
        self.dog_ids_seen = "unset"

    def recognize(self, image, dog_ids=None):
        self.dog_ids_seen = dog_ids
        return self.result

    def recognize_frames(self, images, dog_ids=None):
        self.frames_seen = len(images)
        self.dog_ids_seen = dog_ids
        return self.result


def known(dog_id="dog_biscuit"):
    return RecognitionResult("known_dog", dog_id=dog_id, confidence=0.81, margin=0.42,
                             matches=[Match("dog_biscuit", 0.81), Match("dog_mochi", 0.39)],
                             detection=Detection("dog", 0.9, (0, 0, 10, 10)), reason="dog_biscuit 0.81")


def client_with(result, camera=None):
    recognizer = FakeRecognizer(result)
    app = create_app(recognizer_provider=lambda: recognizer, camera=camera)
    return TestClient(app), recognizer


def test_recognize_needs_the_key():
    client, _ = client_with(known())
    assert client.post("/recognize", content=jpeg_bytes(), headers={"Content-Type": "image/jpeg"}).status_code == 401
    assert client.post("/recognize", content=jpeg_bytes(), headers={**KEY, "X-Kibbly-Key": "wrong"}).status_code == 401


def test_recognize_serves_this_meals_dog():
    client, _ = client_with(known("dog_biscuit"))
    r = client.post("/recognize?meal_dog=dog_biscuit", content=jpeg_bytes(),
                    headers={**KEY, "Content-Type": "image/jpeg"})
    assert r.status_code == 200
    body = r.json()
    assert body["classification"] == "known_dog"
    assert body["dog_id"] == "dog_biscuit"
    assert body["decision"]["action"] == "serve"
    assert body["decision"]["allow_dispense"] is True


def test_recognize_blocks_another_dog():
    client, _ = client_with(known("dog_mochi"))
    body = client.post("/recognize?meal_dog=dog_biscuit", content=jpeg_bytes(),
                       headers={**KEY, "Content-Type": "image/jpeg"}).json()
    assert body["decision"]["action"] == "block"


def test_recognize_rejects_an_empty_body():
    client, _ = client_with(known())
    assert client.post("/recognize", content=b"", headers={**KEY, "Content-Type": "image/jpeg"}).status_code == 400


def test_recognize_rejects_a_non_image():
    client, _ = client_with(known())
    r = client.post("/recognize", content=b"not an image", headers={**KEY, "Content-Type": "image/jpeg"})
    assert r.status_code == 400


def test_dog_ids_limit_is_passed_through():
    client, recognizer = client_with(known())
    client.post("/recognize?dog_ids=dog_biscuit,dog_mochi", content=jpeg_bytes(),
                headers={**KEY, "Content-Type": "image/jpeg"})
    assert recognizer.dog_ids_seen == ["dog_biscuit", "dog_mochi"]


def test_live_pulls_frames_from_the_camera():
    pulled = {}

    def fake_camera(ip, frames, gap, flash):
        pulled["ip"] = ip
        return [Image.new("RGB", (32, 32)) for _ in range(frames)], 0.2

    client, recognizer = client_with(known("dog_biscuit"), camera=fake_camera)
    r = client.post("/recognize/live", json={"camera_ip": "192.168.1.50", "frames": 2, "meal_dog": "dog_biscuit"},
                    headers=KEY)
    assert r.status_code == 200
    body = r.json()
    assert pulled["ip"] == "192.168.1.50"
    assert recognizer.frames_seen == 2
    assert body["frames"] == 2
    assert body["decision"]["action"] == "serve"


def test_live_reports_a_camera_it_cannot_reach():
    def broken_camera(ip, frames, gap, flash):
        raise OSError("timed out")

    client, _ = client_with(known(), camera=broken_camera)
    r = client.post("/recognize/live", json={"camera_ip": "10.0.0.9"}, headers=KEY)
    assert r.status_code == 502


def test_recognition_not_ready_is_reported():
    def broken_provider():
        raise FileNotFoundError("no enrolled dogs")

    app = create_app(recognizer_provider=broken_provider)
    r = TestClient(app).post("/recognize", content=jpeg_bytes(), headers={**KEY, "Content-Type": "image/jpeg"})
    assert r.status_code == 503
