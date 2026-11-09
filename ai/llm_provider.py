"""Swappable LLM providers for Kibbly AI features.

Every feature talks to an LLMProvider, never to a vendor API directly,
so the model can be changed without touching feature code.
"""

import json
import os
import urllib.error
import urllib.request


class LLMProvider:
    """Base interface: send a system prompt and a user prompt, get text back."""

    name = "base"

    def generate(self, system: str, user: str) -> str:
        raise NotImplementedError


class OllamaProvider(LLMProvider):
    """Local model served by Ollama (free, runs on the laptop)."""

    def __init__(self, model: str = None, url: str = "http://localhost:11434/api/chat", timeout: int = 120):
        self.model = model or os.environ.get("KIBBLY_MODEL", "gemma3:1b")
        self.url = url
        self.timeout = timeout
        self.name = f"ollama:{self.model}"

    def generate(self, system: str, user: str) -> str:
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.2},
        }
        request = urllib.request.Request(
            self.url,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Ollama is not reachable at {self.url}: {exc}") from exc
        return payload["message"]["content"]


# FUTURE PROVIDER STUB
# Add a Claude or Gemini provider here when the team chooses one.
# It only needs to implement generate(system, user) and return the model text.
class CloudProvider(LLMProvider):
    """Placeholder for a hosted provider such as Claude or Gemini (not implemented yet)."""

    name = "cloud:not_configured"

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.environ.get("KIBBLY_API_KEY")
        self.model = model

    def generate(self, system: str, user: str) -> str:
        raise NotImplementedError("Choose a cloud provider and implement its HTTP call here.")
