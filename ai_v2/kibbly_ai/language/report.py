"""Daily meal report: the numbers come from engines/stats.py, the wording from the model.

The model only phrases facts it is given; it never computes or diagnoses. If the model is
unreachable, a plain template built from the same numbers is returned, so a report always exists.
"""

from kibbly_ai.language.providers import LLMProvider, ProviderError

SYSTEM = (
    "You are Kibbly, writing a short daily meal report for a dog's owner. Use ONLY the facts given. "
    "State the key numbers plainly (grams eaten against planned, meals completed). "
    "If there are flags, mention them simply. If a vet visit is recommended, say so once. "
    "Never diagnose an illness, never invent numbers. Write two to four short, warm sentences, no lists."
)


def facts_block(dog_name: str, summary: dict) -> str:
    lines = [
        f"Dog: {dog_name}.",
        f"Meals: {summary['meals_completed']} completed, {summary['meals_missed']} missed, "
        f"of {summary['meals_planned']} planned.",
        f"Food: ate {summary['grams_eaten']} g of {summary['grams_dispensed']} g served "
        f"({summary['grams_planned']} g planned).",
    ]
    if summary.get("change_vs_baseline_percent") is not None:
        lines.append(f"Change against the usual amount: {summary['change_vs_baseline_percent']}%.")
    for flag in summary.get("flags", []):
        lines.append(f"Flag: {flag['detail']}")
    lines.append("A vet visit is recommended." if summary.get("needs_vet") else "Nothing unusual today.")
    return "\n".join(lines)


def template(dog_name: str, summary: dict) -> str:
    """A plain report from the numbers, used when the model cannot be reached."""
    parts = [f"{dog_name} ate {summary['grams_eaten']} g of {summary['grams_dispensed']} g served today, "
             f"across {summary['meals_completed']} of {summary['meals_planned']} meals."]
    for flag in summary.get("flags", []):
        parts.append(flag["detail"])
    if summary.get("needs_vet"):
        parts.append("This is unusual for this dog, so a vet visit is a good idea.")
    return " ".join(parts)


def daily_report(provider: LLMProvider, dog_name: str, summary: dict) -> dict:
    facts = facts_block(dog_name, summary)
    try:
        text = provider.generate(SYSTEM, facts, json_output=False).strip()
        source = provider.name
        if not text:
            raise ProviderError("empty report")
    except ProviderError:
        text, source = template(dog_name, summary), "template"
    return {"report": text, "source": source}
