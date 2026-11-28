"""The daily summary and its flags: exact numbers, no model."""

from kibbly_ai.engines import stats


def meal(status="completed", planned=45, dispensed=45, eaten=45, left=0, blocked=0):
    visits = [{"outcome": "blocked"} for _ in range(blocked)]
    return {"status": status, "planned_grams": planned, "grams_dispensed": dispensed,
            "grams_eaten": eaten, "grams_left_in_bowl": left, "visits": visits}


def test_counts_and_grams_add_up():
    s = stats.daily_summary([meal(eaten=45), meal(eaten=40, left=5), meal(status="missed_no_show",
                                                                         dispensed=0, eaten=0)])
    assert s.meals_planned == 3 and s.meals_completed == 2 and s.meals_missed == 1
    assert s.grams_eaten == 85 and s.grams_left_in_bowl == 5


def test_eating_drop_flags_and_needs_vet():
    # ate 95 vs baseline 132 -> about 28% down
    s = stats.daily_summary([meal(eaten=40, left=5), meal(eaten=35, left=10), meal(eaten=20, left=25)],
                            baseline_grams_eaten=132)
    assert s.change_vs_baseline_percent <= -20
    assert any(f["code"] == "eating_drop" for f in s.flags)
    assert s.needs_vet is True


def test_repeated_leftovers_flag():
    s = stats.daily_summary([meal(eaten=30, left=15), meal(eaten=35, left=10)])
    assert any(f["code"] == "repeated_leftovers" for f in s.flags)


def test_two_missed_meals_need_a_vet():
    s = stats.daily_summary([meal(status="missed_no_show", dispensed=0, eaten=0),
                             meal(status="not_served_jam", dispensed=0, eaten=0), meal()])
    assert s.meals_missed == 2 and s.needs_vet is True


def test_blocked_attempts_counted():
    s = stats.daily_summary([meal(blocked=2), meal(blocked=1)])
    assert s.blocked_attempts == 3


def test_a_normal_day_has_no_flags():
    s = stats.daily_summary([meal(), meal(), meal()], baseline_grams_eaten=135)
    assert s.flags == [] and s.needs_vet is False
