"""The daily report: model wording and the template fallback, with a fake provider."""

from fastapi.testclient import TestClient

from kibbly_ai.api.app import create_app
from kibbly_ai.engines import stats
from kibbly_ai.language import report
from kibbly_ai.language.providers import FakeProvider, ProviderError


class BrokenProvider(FakeProvider):
    def generate(self, system, user, json_output=True):
        raise ProviderError("down")


def a_summary():
    meals = [{"status": "completed", "planned_grams": 45, "grams_dispensed": 45, "grams_eaten": 20,
              "grams_left_in_bowl": 25}]
    return stats.daily_summary(meals, baseline_grams_eaten=132).as_dict()


def test_facts_block_has_the_numbers_and_flags():
    block = report.facts_block("Mochi", a_summary())
    assert "20 g" in block and "Mochi" in block
    assert "vet" in block.lower()  # eating drop set needs_vet


def test_report_uses_the_model_when_available():
    result = report.daily_report(FakeProvider(["Mochi ate less than usual today."]), "Mochi", a_summary())
    assert result["report"] == "Mochi ate less than usual today."
    assert result["source"].startswith("fake")


def test_report_falls_back_to_a_template():
    result = report.daily_report(BrokenProvider([]), "Mochi", a_summary())
    assert result["source"] == "template"
    assert "Mochi" in result["report"] and "vet" in result["report"].lower()


def test_reports_endpoint_with_inline_meals():
    app = create_app(provider_factory=lambda: FakeProvider(["All good."]))
    r = TestClient(app).post("/reports/daily", json={
        "dog_name": "Biscuit",
        "meals": [{"status": "completed", "planned_grams": 280, "grams_dispensed": 280,
                   "grams_eaten": 280, "grams_left_in_bowl": 0}],
    })
    assert r.status_code == 200
    body = r.json()
    assert body["summary"]["grams_eaten"] == 280
    assert body["report"] == "All good."


def test_reports_endpoint_needs_meals_or_dog_id():
    app = create_app(provider_factory=lambda: FakeProvider([]))
    assert TestClient(app).post("/reports/daily", json={"dog_name": "x"}).status_code == 400
