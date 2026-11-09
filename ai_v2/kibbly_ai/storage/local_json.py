"""Local storage: one folder per collection, one JSON file per document. For development and tests."""

import json
import pathlib

from kibbly_ai import contracts
from kibbly_ai.storage.base import Storage


class LocalJsonStorage(Storage):
    name = "local_json"

    def __init__(self, root):
        self.root = pathlib.Path(root)

    def _path(self, collection: str, doc_id: str) -> pathlib.Path:
        if collection not in contracts.COLLECTIONS:
            raise KeyError(f"unknown collection {collection}")
        if not doc_id.replace("_", "").replace("-", "").isalnum():
            raise ValueError(f"unsafe document id {doc_id!r}")
        return self.root / collection / f"{doc_id}.json"

    def _write(self, collection: str, doc_id: str, document: dict) -> None:
        path = self._path(collection, doc_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(document, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(path)  # atomic on the same disk: a crash never leaves half a file

    def get(self, collection: str, doc_id: str):
        path = self._path(collection, doc_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def query(self, collection: str, **equals) -> list:
        folder = self.root / collection
        if collection not in contracts.COLLECTIONS:
            raise KeyError(f"unknown collection {collection}")
        if not folder.exists():
            return []
        results = []
        for path in sorted(folder.glob("*.json")):
            document = json.loads(path.read_text(encoding="utf-8"))
            if all(document.get(key) == value for key, value in equals.items()):
                results.append(document)
        return results
