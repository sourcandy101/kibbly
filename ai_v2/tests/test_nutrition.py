"""The nutrition engine: exact, deterministic numbers, no model."""

import pytest

from kibbly_ai.engines import nutrition


def test_age_in_months():
    assert nutrition.age_in_months("2024-03", "2026-11-28") == 32
    assert nutrition.age_in_months("2026-01", "2026-01-15") == 0
    assert nutrition.age_in_months("2030-01", "2026-11") == 0  # future birth never negative


def test_adult_neutered_plan_is_energy_based():
    # 28 kg adult neutered, medium activity, ideal: RER 70*28^0.75 ~= 852, factor 1.6, MER ~= 1363,
    # grams = 1363000/3500 ~= 389 -> 390, split over 2 meals.
    plan = nutrition.feeding_plan(28, age_months=32, neutered=True, activity="medium",
                                  body_condition="ideal", meals_per_day=2)
    assert plan.factor == 1.6
    assert plan.resting_energy_kcal == 852
    assert plan.daily_total_grams == 390
    assert [m.grams for m in plan.meals] == [195, 195]
    assert plan.kcal_source == "default"


def test_meals_are_multiples_of_five_and_sum_to_total():
    plan = nutrition.feeding_plan(9, age_months=41, neutered=True, activity="low",
                                  body_condition="overweight", meals_per_day=3)
    assert plan.factor == 1.0  # overweight: weight loss target, activity ignored
    assert all(m.grams % 5 == 0 for m in plan.meals)
    assert sum(m.grams for m in plan.meals) == plan.daily_total_grams


def test_puppy_factor_and_note():
    plan = nutrition.feeding_plan(5, age_months=3, neutered=False, activity="high",
                                  body_condition="ideal", meals_per_day=4)
    assert plan.factor == 3.0  # growing dog ignores activity and body condition
    assert any("Growing dog" in note for note in plan.notes)


def test_bag_energy_value_is_used():
    default = nutrition.feeding_plan(20, 40, True, "medium", "ideal")
    richer = nutrition.feeding_plan(20, 40, True, "medium", "ideal", kcal_per_kg=4000)
    assert richer.kcal_source == "bag"
    assert richer.daily_total_grams < default.daily_total_grams  # denser food, fewer grams


def test_high_activity_adds_to_the_factor():
    assert nutrition.life_stage_factor(40, True, "high", "ideal") == 1.8
    assert nutrition.life_stage_factor(40, True, "low", "ideal") == 1.5
    assert nutrition.life_stage_factor(40, False, "medium", "thin") == 2.1


def test_split_rejects_bad_meal_count():
    with pytest.raises(ValueError):
        nutrition.split_meals(300, 5)
