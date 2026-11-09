"""Storage: where documents live. Local JSON files for development and tests, Firestore in production."""

from kibbly_ai.config import Settings
from kibbly_ai.storage.base import Storage
from kibbly_ai.storage.local_json import LocalJsonStorage


def make_storage(settings: Settings) -> Storage:
    if settings.storage == "local":
        return LocalJsonStorage(settings.data_dir)
    if settings.storage == "firestore":
        raise NotImplementedError("Firestore storage is added in step 7 (server API).")
    raise ValueError(f"unknown storage {settings.storage}")


__all__ = ["Storage", "LocalJsonStorage", "make_storage"]
