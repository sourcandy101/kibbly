"""Settings read from environment variables, with defaults for the demo laptop."""

import os
import pathlib
from dataclasses import dataclass

AI_V2_DIR = pathlib.Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    storage: str = "local"                 # local or firestore
    data_dir: pathlib.Path = AI_V2_DIR / "data" / "local_store"
    llm: str = "ollama"                    # ollama or cloud
    model: str = "gemma3:4b"
    ollama_url: str = "http://localhost:11434/api/chat"
    feeder_key: str = "demo_feeder_key"    # shared secret the ESP32-CAM sends in X-Kibbly-Key


def load_settings() -> Settings:
    defaults = Settings()
    return Settings(
        storage=os.environ.get("KIBBLY_STORAGE", defaults.storage),
        data_dir=pathlib.Path(os.environ.get("KIBBLY_DATA_DIR", defaults.data_dir)),
        llm=os.environ.get("KIBBLY_LLM", defaults.llm),
        model=os.environ.get("KIBBLY_MODEL", defaults.model),
        ollama_url=os.environ.get("KIBBLY_OLLAMA_URL", defaults.ollama_url),
        feeder_key=os.environ.get("KIBBLY_FEEDER_KEY", defaults.feeder_key),
    )
