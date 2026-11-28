"""Meal statistics and the daily summary: all numbers and flags in code, no model.

Feeds the daily meal report (language/report.py). Flags and needs_vet are rules here,
so the report only puts them into words. Mirrors the fields of schemas/daily_summary.json.
"""

from dataclasses import dataclass, field

COMPLETED = {"completed", "partial", "served_offline"}
MISSED = {"missed_no_show", "not_served_empty_tank", "not_served_jam", "not_served_power_cut"}
DROP_PERCENT = -20          # eating this much below baseline raises a flag


@dataclass
class DailySummary:
    meals_planned: int = 0
    meals_completed: int = 0
    meals_missed: int = 0
    grams_planned: int = 0
    grams_dispensed: int = 0
    grams_eaten: int = 0
    grams_left_in_bowl: int = 0
    blocked_attempts: int = 0
    change_vs_baseline_percent: int = None
    flags: list = field(default_factory=list)
    needs_vet: bool = False

    def as_dict(self) -> dict:
        return self.__dict__


def daily_summary(meals: list, baseline_grams_eaten: float = None) -> DailySummary:
    """meals: the dog's meal documents for one day (schemas/meal.json)."""
    s = DailySummary(meals_planned=len(meals))
    leftovers = 0
    for meal in meals:
        status = meal.get("status")
        if status in COMPLETED:
            s.meals_completed += 1
        elif status in MISSED:
            s.meals_missed += 1
        s.grams_planned += meal.get("planned_grams", 0)
        s.grams_dispensed += meal.get("grams_dispensed", 0)
        s.grams_eaten += meal.get("grams_eaten", 0)
        s.grams_left_in_bowl += meal.get("grams_left_in_bowl", 0)
        if meal.get("grams_left_in_bowl", 0) > 0:
            leftovers += 1
        for visit in meal.get("visits", []):
            if visit.get("outcome") == "blocked":
                s.blocked_attempts += 1

    if baseline_grams_eaten:
        s.change_vs_baseline_percent = round((s.grams_eaten - baseline_grams_eaten) / baseline_grams_eaten * 100)

    if s.change_vs_baseline_percent is not None and s.change_vs_baseline_percent <= DROP_PERCENT:
        s.flags.append({"code": "eating_drop",
                        "detail": f"Ate {abs(s.change_vs_baseline_percent)}% less than the usual amount."})
        s.needs_vet = True
    if s.meals_missed >= 1:
        s.flags.append({"code": "missed_meal",
                        "detail": f"Missed {s.meals_missed} of {s.meals_planned} meals."})
        if s.meals_missed >= 2:
            s.needs_vet = True
    if s.meals_completed and leftovers >= s.meals_completed:
        s.flags.append({"code": "repeated_leftovers",
                        "detail": f"Left food at {leftovers} of {s.meals_completed} meals."})
    return s
