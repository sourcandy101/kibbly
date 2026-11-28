"""The feeder ingest and config endpoints: validate, store, and serve a home's config."""

from fastapi.testclient import TestClient

from kibbly_ai.api.app import create_app
from tests.conftest import load_example

KEY = {"X-Kibbly-Key": "demo_feeder_key"}


def client(storage):
    return TestClient(create_app(storage=storage))


def test_meals_need_the_key(storage):
    meal = load_example("valid", "meal", "biscuit_breakfast_with_mochi_blocked")
    assert client(storage).post("/feeder/meals", json=meal).status_code == 401


def test_a_valid_meal_is_stored(storage):
    meal = load_example("valid", "meal", "biscuit_breakfast_with_mochi_blocked")
    r = client(storage).post("/feeder/meals", json=meal, headers=KEY)
    assert r.status_code == 200 and r.json()["stored"] is True
    assert storage.get("meals", meal["meal_id"]) is not None


def test_an_invalid_meal_is_refused_with_errors(storage):
    bad = load_example("invalid", "meal", "local_time_instead_of_utc")
    r = client(storage).post("/feeder/meals", json=bad, headers=KEY)
    assert r.status_code == 422
    assert r.json()["detail"]["collection"] == "meals"
    assert len(r.json()["detail"]["errors"]) >= 1


def test_a_visit_and_an_alert_are_stored(storage):
    visit = load_example("valid", "visit", "mochi_between_meals")
    alert = load_example("valid", "alert", "jam")
    c = client(storage)
    assert c.post("/feeder/visits", json=visit, headers=KEY).status_code == 200
    assert c.post("/feeder/alerts", json=alert, headers=KEY).status_code == 200
    assert storage.get("visits", visit["visit_id"]) is not None
    assert storage.get("alerts", alert["alert_id"]) is not None


def test_config_returns_the_calling_order_and_meals(storage):
    for name in ("biscuit", "mochi"):
        storage.put("dogs", load_example("valid", "dog", name))
        storage.put("schedules", load_example("valid", "schedule", name))
    home_id = load_example("valid", "dog", "biscuit")["home_id"]

    body = client(storage).get(f"/feeder/config?home_id={home_id}", headers=KEY).json()
    assert body["calling_order"][0] == "dog_biscuit"  # call_order 1 comes first
    biscuit = next(d for d in body["dogs"] if d["dog_id"] == "dog_biscuit")
    assert len(biscuit["meals"]) >= 1
    assert body["thresholds"]["accept_score"] > 0
