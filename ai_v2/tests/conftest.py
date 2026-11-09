import json
import pathlib

import pytest

from kibbly_ai.config import Settings
from kibbly_ai.storage import LocalJsonStorage

EXAMPLES = pathlib.Path(__file__).resolve().parents[2] / "schemas" / "examples"


def load_example(kind: str, schema: str, name: str) -> dict:
    return json.loads((EXAMPLES / kind / schema / f"{name}.json").read_text(encoding="utf-8"))


@pytest.fixture
def storage(tmp_path):
    return LocalJsonStorage(tmp_path / "store")


@pytest.fixture
def settings(tmp_path):
    return Settings(data_dir=tmp_path / "store")
