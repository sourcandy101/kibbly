"""Nutrition engine: how much food a dog needs, and a suggested schedule.

Energy based, as agreed in scope.md (replaces the flat grams per kg rule of ai/):

  resting energy  RER = 70 * weight_kg ** 0.75        kcal per day
  daily energy    MER = RER * life stage factor       kcal per day
  daily food      grams = MER / kibble energy density

The factor comes from standard small animal guidance (puppy, adult, neuter,
activity, body condition). The owner confirms or edits the result in the app;
nothing here decides on its own. Pure code, no model.
"""

from dataclasses import dataclass

DEFAULT_KCAL_PER_KG = 3500          # typical dry food, used when the bag value is unknown
GRAM_STEP = 5                        # the feeder and the schema work in multiples of 5 g
MIN_DAILY_GRAMS = 10

# Default meal times and labels per number of meals a day (owner can change them).
MEAL_TEMPLATES = {
    1: [("08:00", "Breakfast")],
    2: [("08:00", "Breakfast"), ("18:00", "Dinner")],
    3: [("08:00", "Breakfast"), ("13:00", "Lunch"), ("18:00", "Dinner")],
    4: [("07:00", "Breakfast"), ("12:00", "Lunch"), ("17:00", "Dinner"), ("21:00", "Supper")],
}


@dataclass(frozen=True)
class Meal:
    slot: int
    label: str
    local_time: str
    grams: int


@dataclass(frozen=True)
class FeedingPlan:
    daily_total_grams: int
    meals: list
    resting_energy_kcal: int
    daily_energy_kcal: int
    factor: float
    kcal_per_kg_used: int
    kcal_source: str                 # "bag" or "default"
    notes: list


def age_in_months(birth_month: str, as_of_date: str) -> int:
    """birth_month and as_of_date are 'YYYY-MM' (as_of may be 'YYYY-MM-DD'). Never negative."""
    by, bm = (int(part) for part in birth_month.split("-")[:2])
    ay, am = (int(part) for part in as_of_date.split("-")[:2])
    return max(0, (ay - by) * 12 + (am - bm))


def life_stage_factor(age_months: int, neutered: bool, activity: str, body_condition: str) -> float:
    """The multiplier on resting energy. Growing dogs ignore activity and body condition."""
    if age_months < 4:
        return 3.0
    if age_months < 12:
        return 2.0
    if body_condition == "overweight":
        return 1.0                   # weight loss target, below maintenance
    factor = 1.6 if neutered else 1.8
    if body_condition == "thin":
        factor += 0.3
    factor += {"low": -0.1, "medium": 0.0, "high": 0.2}[activity]
    return round(factor, 2)


def round_to_step(grams: float) -> int:
    return int(round(grams / GRAM_STEP) * GRAM_STEP)


def split_meals(total_grams: int, meals_per_day: int) -> list:
    """Split the daily grams into meals, each a multiple of 5 g, summing to the total."""
    template = MEAL_TEMPLATES.get(meals_per_day)
    if template is None:
        raise ValueError(f"meals_per_day must be 1 to 4, got {meals_per_day}")
    base_steps = (total_grams // GRAM_STEP) // meals_per_day
    remainder_steps = (total_grams // GRAM_STEP) - base_steps * meals_per_day
    meals = []
    for index, (local_time, label) in enumerate(template):
        steps = base_steps + (1 if index < remainder_steps else 0)
        meals.append(Meal(index + 1, label, local_time, steps * GRAM_STEP))
    return meals


def feeding_plan(weight_kg: float, age_months: int, neutered: bool, activity: str,
                 body_condition: str, meals_per_day: int = 2, kcal_per_kg: int = None) -> FeedingPlan:
    rer = 70 * (weight_kg ** 0.75)
    factor = life_stage_factor(age_months, neutered, activity, body_condition)
    mer = rer * factor

    kcal_source = "bag" if kcal_per_kg else "default"
    kcal_per_kg = kcal_per_kg or DEFAULT_KCAL_PER_KG
    daily_grams = max(MIN_DAILY_GRAMS, round_to_step(mer * 1000 / kcal_per_kg))
    meals = split_meals(daily_grams, meals_per_day)

    notes = []
    if age_months < 12:
        notes.append("Growing dog: weigh monthly and update the plan, as the amount changes quickly.")
    if body_condition == "overweight":
        notes.append("Set for gentle weight loss. Check the weight in two weeks and adjust.")
    if body_condition == "thin":
        notes.append("Set a little above maintenance to reach an ideal weight.")
    if kcal_source == "default":
        notes.append(f"No energy value for the food, so {DEFAULT_KCAL_PER_KG} kcal/kg is assumed. "
                     "Enter the value from the bag for a more exact amount.")
    notes.append("A suggestion to confirm or edit, not veterinary advice. Ask your vet if unsure.")

    return FeedingPlan(
        daily_total_grams=sum(m.grams for m in meals),
        meals=meals,
        resting_energy_kcal=int(round(rer)),
        daily_energy_kcal=int(round(mer)),
        factor=factor,
        kcal_per_kg_used=kcal_per_kg,
        kcal_source=kcal_source,
        notes=notes,
    )
