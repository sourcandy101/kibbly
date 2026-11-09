import json

import pytest

from kibbly_ai.language.providers import FakeProvider, OllamaProvider, ProviderError


def test_fake_provider_returns_answers_in_order():
    fake = FakeProvider(['{"a": 1}', '{"a": 2}'])
    assert json.loads(fake.generate("s", "u"))["a"] == 1
    assert json.loads(fake.generate("s", "u"))["a"] == 2
    assert len(fake.calls) == 2
    with pytest.raises(ProviderError):
        fake.generate("s", "u")


def test_unreachable_ollama_raises_provider_error():
    provider = OllamaProvider("gemma3:4b", "http://127.0.0.1:9/api/chat", timeout=2)
    with pytest.raises(ProviderError):
        provider.generate("s", "u")
