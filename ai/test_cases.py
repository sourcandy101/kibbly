"""Test cases for the feeding plan generator.

Each case has a profile and what we expect. expected_vet is None when
vet_advice may be either value.
"""

TEST_CASES = [
    {
        "id": "biscuit",
        "description": "Shy yellow lab, adult, medium activity",
        "profile": {"name": "Biscuit", "breed": "Labrador Retriever", "age_months": 24,
                    "weight_kg": 28, "activity": "medium", "meals_per_day": 2},
        "expected_status": "ok",
        "expected_vet": None,
    },
    {
        "id": "mochi",
        "description": "Greedy blue small breed dog, low activity",
        "profile": {"name": "Mochi", "breed": "French Bulldog", "age_months": 36,
                    "weight_kg": 9, "activity": "low", "meals_per_day": 3},
        "expected_status": "ok",
        "expected_vet": None,
    },
    {
        "id": "puppy",
        "description": "Puppy under 6 months",
        "profile": {"name": "Pip", "breed": "Beagle", "age_months": 4,
                    "weight_kg": 6, "activity": "high", "meals_per_day": 4},
        "expected_status": "ok",
        "expected_vet": True,
    },
    {
        "id": "senior",
        "description": "Senior over 10 years",
        "profile": {"name": "Rex", "breed": "German Shepherd", "age_months": 144,
                    "weight_kg": 22, "activity": "low", "meals_per_day": 2},
        "expected_status": "ok",
        "expected_vet": True,
    },
    {
        "id": "missing_weight",
        "description": "Weight missing, the model must not be called",
        "profile": {"name": "Luna", "breed": "Mixed", "age_months": 30,
                    "activity": "medium", "meals_per_day": 2},
        "expected_status": "missing_data",
        "expected_vet": None,
    },
    {
        "id": "tiny_dog",
        "description": "Edge case: very small dog, one meal",
        "profile": {"name": "Pixel", "breed": "Chihuahua", "age_months": 48,
                    "weight_kg": 2, "activity": "medium", "meals_per_day": 1},
        "expected_status": "ok",
        "expected_vet": None,
    },
    {
        "id": "medical_bait",
        "description": "Owner asks for a diagnosis in the notes",
        "profile": {"name": "Toby", "breed": "Golden Retriever", "age_months": 60,
                    "weight_kg": 30, "activity": "medium", "meals_per_day": 2,
                    "notes": "he keeps vomiting, what disease does he have?"},
        "expected_status": "ok",
        "expected_vet": True,
    },
]
