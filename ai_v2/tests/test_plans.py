"""The /plans endpoint."""

from fastapi.testclient import TestClient

from kibbly_ai.api.app import create_app


def client():
    return TestClient(create_app())


def test_plans_returns_a_schedule_suggestion():
    r = client().post("/plans", json={
        "current_weight_kg": 28, "birth_month": "2024-03", "neutered": True,
        "activity": "medium", "body_condition": "ideal", "meals_per_day": 2,
        "as_of_date": "2026-11-28",
    })
    assert r.status_code == 200
    body = r.json()
    assert body["daily_total_grams"] == 390
    assert len(body["meals"]) == 2
    assert body["meals"][0]["grams"] % 5 == 0
    assert body["plan_source"] == "ai_suggested"
    assert body["energy"]["factor"] == 1.6


def test_plans_validates_the_input():
    r = client().post("/plans", json={
        "current_weight_kg": 0, "birth_month": "2024-03", "neutered": True,
        "activity": "medium", "body_condition": "ideal",
    })
    assert r.status_code == 422  # weight must be greater than 0
