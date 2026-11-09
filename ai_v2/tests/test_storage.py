import pytest

from kibbly_ai.contracts import ContractError
from tests.conftest import load_example


def test_put_then_get_returns_same_document(storage):
    dog = load_example("valid", "dog", "biscuit")
    assert storage.put("dogs", dog) == "dog_biscuit"
    assert storage.get("dogs", "dog_biscuit") == dog


def test_get_missing_returns_none(storage):
    assert storage.get("dogs", "dog_nobody") is None


def test_query_filters_by_field(storage):
    storage.put("meals", load_example("valid", "meal", "biscuit_breakfast_with_mochi_blocked"))
    storage.put("meals", load_example("valid", "meal", "mochi_breakfast_leftovers"))
    storage.put("meals", load_example("valid", "meal", "biscuit_dinner_offline"))
    assert [m["meal_id"] for m in storage.query("meals", dog_id="dog_biscuit")] == ["meal_0101", "meal_0105"]
    assert len(storage.query("meals", home_id="home_amira")) == 3
    assert storage.query("alerts") == []


def test_invalid_document_is_never_written(storage):
    bad = load_example("invalid", "dog", "sex_not_in_list")
    with pytest.raises(ContractError):
        storage.put("dogs", bad)
    assert storage.get("dogs", bad["dog_id"]) is None


def test_unknown_collection_is_refused(storage):
    with pytest.raises(KeyError):
        storage.get("cats", "cat_1")


def test_unsafe_id_is_refused(storage):
    with pytest.raises(ValueError):
        storage.get("dogs", "../secrets")
