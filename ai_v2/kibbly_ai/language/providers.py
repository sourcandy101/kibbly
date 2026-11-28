"""Swappable language model providers. Features call generate() and never a vendor API directly."""

import json
import urllib.error
import urllib.request

from kibbly_ai.config import Settings


class ProviderError(RuntimeError):
    """The model could not be reached or gave no answer. Callers fall back to a template."""


class LLMProvider:
    name = "base"

    def generate(self, system: str, user: str, json_output: bool = True) -> str:
        raise NotImplementedError

    def generate_stream(self, system: str, user: str):
        """Yield the answer in pieces as it is written. The default yields it in one piece,
        so providers without real streaming (and the fake) still work."""
        yield self.generate(system, user, json_output=False)


class OllamaProvider(LLMProvider):
    """Local model served by Ollama. Default gemma3:4b (chosen by benchmark, see ai_v2/scope.md)."""

    def __init__(self, model: str, url: str, timeout: int = 180, temperature: float = 0.2,
                 num_predict: int = 256, keep_alive: str = "30m"):
        self.model, self.url, self.timeout, self.temperature = model, url, timeout, temperature
        self.num_predict, self.keep_alive = num_predict, keep_alive
        self.name = f"ollama:{model}"

    def generate(self, system: str, user: str, json_output: bool = True) -> str:
        body = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "stream": False,
            # keep_alive holds the model in memory so the next answer is not a cold start;
            # num_predict caps the length so a short answer does not run on.
            "keep_alive": self.keep_alive,
            "options": {"temperature": self.temperature, "num_predict": self.num_predict},
        }
        if json_output:
            body["format"] = "json"
        if self.model.startswith("qwen"):
            body["think"] = False  # reasoning mode only slows short wording tasks
        request = urllib.request.Request(self.url, data=json.dumps(body).encode("utf-8"),
                                         headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ProviderError(f"Ollama not reachable at {self.url}: {exc}") from exc
        return payload["message"]["content"]

    def generate_stream(self, system: str, user: str):
        """Stream the answer token by token, so the app can show it as it is written."""
        body = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "stream": True,
            "keep_alive": self.keep_alive,
            "options": {"temperature": self.temperature, "num_predict": self.num_predict},
        }
        if self.model.startswith("qwen"):
            body["think"] = False
        request = urllib.request.Request(self.url, data=json.dumps(body).encode("utf-8"),
                                         headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                for line in response:            # Ollama streams one JSON object per line
                    line = line.strip()
                    if not line:
                        continue
                    chunk = json.loads(line.decode("utf-8"))
                    piece = chunk.get("message", {}).get("content", "")
                    if piece:
                        yield piece
                    if chunk.get("done"):
                        break
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ProviderError(f"Ollama not reachable at {self.url}: {exc}") from exc


class FakeProvider(LLMProvider):
    """Returns fixed answers in order. For tests: no model, no network, same result every time."""

    name = "fake"

    def __init__(self, answers):
        self.answers = list(answers)
        self.calls = []

    def generate(self, system: str, user: str, json_output: bool = True) -> str:
        self.calls.append((system, user))
        if not self.answers:
            raise ProviderError("FakeProvider has no answer left")
        return self.answers.pop(0)


def make_provider(settings: Settings) -> LLMProvider:
    if settings.llm == "ollama":
        return OllamaProvider(settings.model, settings.ollama_url)
    if settings.llm == "cloud":
        raise NotImplementedError("Cloud provider is added in step 6 (meal insights).")
    raise ValueError(f"unknown llm {settings.llm}")
