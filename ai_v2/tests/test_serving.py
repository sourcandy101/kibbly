"""The serving decision: a pure rule over a RecognitionResult, no models."""

from kibbly_ai.engines import serving
from kibbly_ai.perception.base import Detection, Match, RecognitionResult


def known(dog_id="dog_biscuit", reason=""):
    return RecognitionResult("known_dog", dog_id=dog_id, confidence=0.8, margin=0.3,
                             matches=[Match(dog_id, 0.8)], detection=Detection("dog", 0.9, (0, 0, 10, 10)),
                             reason=reason)


def unknown(reason=""):
    return RecognitionResult("unknown_dog", confidence=0.4, margin=0.2, reason=reason)


def not_a_dog():
    return RecognitionResult("not_a_dog", reason="no dog found")


def test_meal_dog_is_served():
    d = serving.decide(known("dog_biscuit"), meal_dog="dog_biscuit")
    assert d.action == serving.SERVE and d.allow_dispense is True


def test_other_dog_is_blocked():
    d = serving.decide(known("dog_mochi"), meal_dog="dog_biscuit")
    assert d.action == serving.BLOCK and d.allow_dispense is False


def test_known_dog_without_a_meal_is_blocked():
    d = serving.decide(known("dog_biscuit"), meal_dog=None)
    assert d.action == serving.BLOCK and d.allow_dispense is False


def test_unknown_dog_gets_a_small_portion():
    d = serving.decide(unknown(reason="best match dog_biscuit 0.40 below 0.49"), meal_dog="dog_biscuit")
    assert d.action == serving.UNKNOWN_PORTION and d.allow_dispense is True


def test_unsure_waits_without_dispensing():
    d = serving.decide(unknown(reason="unsure between dog_biscuit and dog_mochi"), meal_dog="dog_biscuit")
    assert d.action == serving.WAIT and d.allow_dispense is False


def test_no_dog_does_nothing():
    d = serving.decide(not_a_dog(), meal_dog="dog_biscuit")
    assert d.action == serving.NOTHING and d.allow_dispense is False
