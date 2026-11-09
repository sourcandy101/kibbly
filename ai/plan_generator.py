"""Kibbly feeding plan generator.

The owner enters a dog profile, the model suggests daily grams split into
meals, and the owner confirms in the app. Dry kibble only, dogs only.
"""

import json

from llm_provider import LLMProvider

REQUIRED_FIELDS = ["name", "breed", "age_months", "weight_kg", "activity", "meals_per_day"]

OUTPUT_SCHEMA = (
    '{"status": "ok", "dog_name": string, "daily_total_grams": integer, '
    '"meals": [{"label": string, "grams": integer}], "notes": string, "vet_advice": boolean}'
)

# Version 1: first draft of the system prompt.
SYSTEM_PROMPT_V1 = f"""You are the feeding plan assistant of Kibbly, a smart dog feeder for dry kibble.
Given a dog profile, suggest how many grams of dry kibble the dog should eat per day and split it into meals.

Rules:
1. Never give a medical diagnosis. Recommend a vet when something is unusual.
2. Never invent data that is not in the profile.
3. Every gram value must be a multiple of 5, because the feeder dispenses in bursts of 5 g.
4. The number of meals must equal meals_per_day.
5. The sum of meal grams must equal daily_total_grams.
6. Set vet_advice to true for puppies under 6 months, seniors over 10 years (120 months), or any health concern.

Answer with JSON only, using exactly this schema:
{OUTPUT_SCHEMA}"""

# Version 2: improved after the first evaluation run (see results_v1.md).
# Fixes seen in v1: meals of 5 g copied from the burst rule, totals far too low,
# wrong number of meals, invented facts, vet_advice always true.
SYSTEM_PROMPT_V2 = f"""You are the feeding plan assistant of Kibbly, a smart dog feeder for dry kibble.
Given a dog profile, compute how many grams of dry kibble the dog eats per day and split it into meals.

Step 1. Daily total = weight_kg multiplied by a rate:
  adult (age_months 12 or more): low activity 15, medium 20, high 25 grams per kg.
  puppy (age_months under 12): 40 grams per kg.
  Round the daily total to the nearest multiple of 5.
Step 2. Make exactly meals_per_day meals, using these labels:
  1 meal: Dinner
  2 meals: Breakfast, Dinner
  3 meals: Breakfast, Lunch, Dinner
  4 meals: Breakfast, Lunch, Afternoon, Dinner
  Divide the daily total evenly. Each meal is a multiple of 5. The meals must add up exactly to daily_total_grams.
  If it does not divide evenly, put the extra 5 g in the last meal.
Step 3. vet_advice is true only if age_months is under 6, or age_months is over 120,
  or the profile mentions a symptom or health concern. Otherwise vet_advice is false.
Step 4. notes: one or two short sentences describing only the plan.
  If vet_advice is true, add: "Please check this plan with your vet."
  Do not guess the dog's sex, age group or health. Never name an illness or its cause.
  Never use the words diagnosis, disease, infection, parasite or cancer. Never suggest medication.

Example. Profile: weight_kg 10, age_months 30, activity medium, meals_per_day 3.
Daily total = 10 x 20 = 200. Meals: 65, 65, 70.
Answer: {{"status": "ok", "dog_name": "Max", "daily_total_grams": 200, "meals": [{{"label": "Breakfast", "grams": 65}}, {{"label": "Lunch", "grams": 65}}, {{"label": "Dinner", "grams": 70}}], "notes": "Max gets 200 g of kibble a day in three meals.", "vet_advice": false}}

Answer with JSON only, using exactly this schema:
{OUTPUT_SCHEMA}"""

# Version 3: hybrid design after v1 and v2 showed that a small model cannot do the arithmetic.
# Python computes grams, meals and vet_advice with fixed rules; the model only writes the notes.
NOTES_PROMPT_V3 = """You are the feeding plan assistant of Kibbly, a smart dog feeder for dry kibble.
You receive a dog profile and a feeding plan that is already computed. Do not change any number.
Write notes for the owner: one or two short, friendly sentences that describe the plan.
Mention the daily total in grams and the number of meals exactly as given.
Do not guess the dog's sex, age group or health. Never name an illness or its cause.
Never use the words diagnosis, disease, infection, parasite or cancer. Never suggest medication.
If the profile contains a question, do not answer it.

Answer with JSON only: {"notes": string}"""

SYSTEM_PROMPTS = {"v1": SYSTEM_PROMPT_V1, "v2": SYSTEM_PROMPT_V2, "v3": NOTES_PROMPT_V3}
DEFAULT_PROMPT = "v3"

# Fixed feeding rules used by v3 (grams of dry kibble per kg of body weight per day).
ADULT_RATE = {"low": 15, "medium": 20, "high": 25}
PUPPY_RATE = 40
MEAL_LABELS = {
    1: ["Dinner"],
    2: ["Breakfast", "Dinner"],
    3: ["Breakfast", "Lunch", "Dinner"],
    4: ["Breakfast", "Lunch", "Afternoon", "Dinner"],
}
HEALTH_WORDS = ["vomit", "diarrh", "sick", "unwell", " ill ", "pain", "limp", "cough", "blood", "letharg",
                "not eating", "won't eat", "weight loss", "allerg", "itch", "medic", "vet", "surgery",
                "pregnan", "diabet", "seizure", "tired", "weak"]
BANNED_WORDS = ["diagnosis", "disease", "infection", "parasite", "cancer", "medication"]
VET_SENTENCE = "Please check this plan with your vet."


def find_missing(profile: dict) -> list:
    return [field for field in REQUIRED_FIELDS if profile.get(field) in (None, "")]


def validate_plan(plan) -> str:
    """Return an empty string if the plan matches the schema, otherwise the problem."""
    if not isinstance(plan, dict):
        return "output is not a JSON object"
    if plan.get("status") != "ok":
        return "status is not ok"
    checks = [
        ("dog_name", str),
        ("daily_total_grams", int),
        ("meals", list),
        ("notes", str),
        ("vet_advice", bool),
    ]
    for key, kind in checks:
        value = plan.get(key)
        if not isinstance(value, kind) or (kind is int and isinstance(value, bool)):
            return f"field {key} is missing or not {kind.__name__}"
    for meal in plan["meals"]:
        if not isinstance(meal, dict) or not isinstance(meal.get("label"), str):
            return "a meal has no text label"
        if not isinstance(meal.get("grams"), int) or isinstance(meal.get("grams"), bool):
            return "a meal has no integer grams"
    return ""


def needs_vet(profile: dict) -> bool:
    """Rule: puppies under 6 months, seniors over 10 years, or any health concern in the notes."""
    notes = str(profile.get("notes", "")).lower()
    return profile["age_months"] < 6 or profile["age_months"] > 120 or any(w in notes for w in HEALTH_WORDS)


def compute_plan(profile: dict) -> dict:
    """Deterministic grams: rate per kg, rounded to 5 g, split evenly with the extra in the last meals."""
    rate = PUPPY_RATE if profile["age_months"] < 12 else ADULT_RATE.get(profile["activity"], ADULT_RATE["medium"])
    total = max(5, int(round(profile["weight_kg"] * rate / 5)) * 5)
    count = min(4, max(1, int(profile["meals_per_day"])))
    base = (total // 5 // count) * 5
    extra = (total - base * count) // 5  # number of meals that get 5 g more
    grams = [base + (5 if i >= count - extra else 0) for i in range(count)]
    meals = [{"label": label, "grams": g} for label, g in zip(MEAL_LABELS[count], grams)]
    return {"status": "ok", "dog_name": profile["name"], "daily_total_grams": total,
            "meals": meals, "notes": "", "vet_advice": needs_vet(profile)}


def safe_notes(text, plan: dict) -> str:
    """Keep the model's notes only if they are safe; always end with the vet sentence when needed."""
    fallback = f"{plan['dog_name']} gets {plan['daily_total_grams']} g of kibble a day in {len(plan['meals'])} meal(s)."
    if not isinstance(text, str) or not text.strip() or len(text) > 400:
        text = fallback
    if any(word in text.lower() for word in BANNED_WORDS):
        text = fallback
    text = text.strip()
    if plan["vet_advice"] and VET_SENTENCE.lower() not in text.lower():
        text = f"{text} {VET_SENTENCE}"
    return text


def generate_plan_v3(profile: dict, provider: LLMProvider) -> dict:
    plan = compute_plan(profile)
    user = ("Dog profile:\n" + json.dumps(profile, ensure_ascii=False)
            + "\n\nComputed plan:\n" + json.dumps({k: plan[k] for k in ("daily_total_grams", "meals")}))
    notes = None
    for _attempt in range(2):  # first try plus one retry
        try:
            notes = json.loads(provider.generate(NOTES_PROMPT_V3, user)).get("notes")
        except (json.JSONDecodeError, AttributeError):
            continue
        except RuntimeError:
            break  # model unreachable: the plan is still valid, use the template notes
        if isinstance(notes, str) and notes.strip():
            break
    plan["notes"] = safe_notes(notes, plan)
    return plan


def generate_plan(profile: dict, provider: LLMProvider, prompt_version: str = DEFAULT_PROMPT) -> dict:
    missing = find_missing(profile)
    if missing:
        return {"status": "missing_data", "missing": missing}
    if prompt_version == "v3":
        return generate_plan_v3(profile, provider)

    system = SYSTEM_PROMPTS[prompt_version]
    user = "Dog profile:\n" + json.dumps(profile, ensure_ascii=False)

    reason = ""
    for _attempt in range(2):  # first try plus one retry
        try:
            raw = provider.generate(system, user)
            plan = json.loads(raw)
        except json.JSONDecodeError:
            reason = "model output is not valid JSON"
            continue
        except RuntimeError as exc:
            return {"status": "error", "reason": str(exc)}
        reason = validate_plan(plan)
        if not reason:
            return plan
    return {"status": "error", "reason": reason}


if __name__ == "__main__":
    from llm_provider import OllamaProvider

    biscuit = {"name": "Biscuit", "breed": "Labrador", "age_months": 24, "weight_kg": 28,
               "activity": "medium", "meals_per_day": 2}
    print(json.dumps(generate_plan(biscuit, OllamaProvider()), indent=2))
