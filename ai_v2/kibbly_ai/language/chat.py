"""Ask Kibbly: a grounded chat about one dog.

The model answers only from the facts it is given (the dog's profile and its own logs),
never invents data, and never gives a medical diagnosis. On any health question it says
what the logs show and recommends a vet. If the model cannot be reached, a plain template
answer is returned instead, so the app always gets something.
"""

import json

from kibbly_ai.language.providers import LLMProvider, ProviderError

SYSTEM = (
    "You are Kibbly, the assistant inside a smart dog feeder app. "
    "Answer the owner's question about their dog using ONLY the facts given below. "
    "If the facts do not contain the answer, say you do not have that information yet. "
    "Never diagnose an illness and never give medical or medication advice: if the question is "
    "about health or symptoms, say briefly what the logs show and recommend seeing a vet. "
    "Never invent numbers, meals or events. Keep it to two or three short, warm, plain sentences. "
    'Reply as JSON: {"answer": "..."}.'
)

FALLBACK = "I can't reach the assistant right now. Please try again in a moment."


def build_facts(dog: dict, facts: list = None) -> str:
    """A short, plain facts block from the dog profile and any extra log lines."""
    lines = []
    name = dog.get("name", "the dog")
    parts = []
    if dog.get("breed"):
        parts.append(str(dog["breed"]))
    if dog.get("age_months") is not None:
        months = int(dog["age_months"])
        parts.append(f"{months // 12} years {months % 12} months old" if months >= 12 else f"{months} months old")
    if dog.get("weight_kg") is not None:
        parts.append(f"{dog['weight_kg']} kg")
    for key in ("sex", "activity", "body_condition"):
        if dog.get(key):
            parts.append(str(dog[key]))
    lines.append(f"{name}: " + ", ".join(parts) if parts else name)
    if dog.get("neutered") is not None:
        lines.append(f"{name} is {'neutered' if dog['neutered'] else 'not neutered'}.")
    for fact in (facts or []):
        lines.append(str(fact))
    if not (facts or []):
        lines.append("No meal history has been recorded yet.")
    return "\n".join(lines)


def ask(provider: LLMProvider, dog: dict, question: str, facts: list = None) -> dict:
    facts_block = build_facts(dog, facts)
    user = f"Facts:\n{facts_block}\n\nQuestion: {question}"
    try:
        raw = provider.generate(SYSTEM, user, json_output=True)
        answer = json.loads(raw).get("answer", "").strip()
        if not answer:
            raise ValueError("empty answer")
    except (ProviderError, ValueError, json.JSONDecodeError, KeyError):
        answer = FALLBACK
    return {"answer": answer, "model": provider.name, "grounded_on": facts_block}
