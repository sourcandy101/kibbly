"""Ask Kibbly chat: grounding and the fallback, with a fake provider (no model)."""

import json

from fastapi.testclient import TestClient

from kibbly_ai.api.app import create_app
from kibbly_ai.language import chat
from kibbly_ai.language.providers import FakeProvider, ProviderError


class BrokenProvider(FakeProvider):
    def generate(self, system, user, json_output=True):
        raise ProviderError("Ollama down")


BISCUIT = {"name": "Biscuit", "breed": "Labrador", "weight_kg": 28, "age_months": 32, "neutered": True}


def test_facts_block_lists_the_dog_and_logs():
    block = chat.build_facts(BISCUIT, ["Ate 280 g at breakfast."])
    assert "Biscuit" in block and "Labrador" in block
    assert "Ate 280 g at breakfast." in block


def test_facts_block_notes_when_there_is_no_history():
    assert "No meal history" in chat.build_facts(BISCUIT, [])


def test_ask_passes_safety_and_facts_to_the_model():
    provider = FakeProvider([json.dumps({"answer": "Biscuit ate well today."})])
    result = chat.ask(provider, BISCUIT, "How did Biscuit eat?", ["Ate 280 g at breakfast."])
    assert result["answer"] == "Biscuit ate well today."
    system, user = provider.calls[0]
    assert "vet" in system.lower() and "only" in system.lower()
    assert "Ate 280 g at breakfast." in user and "How did Biscuit eat?" in user


def test_ask_falls_back_when_the_model_is_down():
    result = chat.ask(BrokenProvider([]), BISCUIT, "anything")
    assert result["answer"] == chat.FALLBACK


def test_ask_falls_back_on_bad_json():
    result = chat.ask(FakeProvider(["not json at all"]), BISCUIT, "anything")
    assert result["answer"] == chat.FALLBACK


def test_chat_endpoint_with_an_inline_dog():
    provider = FakeProvider([json.dumps({"answer": "Biscuit is doing fine."})])
    app = create_app(provider_factory=lambda: provider)
    r = TestClient(app).post("/chat", json={"question": "How is Biscuit?", "dog": BISCUIT,
                                            "facts": ["Ate 280 g at breakfast."]})
    assert r.status_code == 200
    body = r.json()
    assert body["dog"] == "Biscuit"
    assert body["answer"] == "Biscuit is doing fine."


def test_chat_endpoint_needs_a_dog():
    app = create_app(provider_factory=lambda: FakeProvider([]))
    assert TestClient(app).post("/chat", json={"question": "hi"}).status_code == 400
