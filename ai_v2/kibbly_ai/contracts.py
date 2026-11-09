"""The shared data contract: loads the JSON Schemas in the repo folder schemas/.

The schemas are the single source of truth. Nothing in the AI server redefines
a field; every document is validated here before it is stored.
"""

import json
import pathlib
from functools import lru_cache

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

SCHEMAS_DIR = pathlib.Path(__file__).resolve().parents[2] / "schemas"

# Firestore collection name: (schema file name, field that holds the document id)
COLLECTIONS = {
    "homes": ("home", "home_id"),
    "dogs": ("dog", "dog_id"),
    "weights": ("weight_entry", "weight_id"),
    "schedules": ("schedule", "dog_id"),
    "meals": ("meal", "meal_id"),
    "visits": ("visit", "visit_id"),
    "daily_summaries": ("daily_summary", "summary_id"),
    "alerts": ("alert", "alert_id"),
}


class ContractError(ValueError):
    """A document does not match its schema. errors lists every problem found."""

    def __init__(self, collection: str, errors: list):
        self.collection = collection
        self.errors = errors
        super().__init__(f"{collection}: {len(errors)} problem(s): " + "; ".join(errors[:3]))


@lru_cache(maxsize=1)
def _load():
    schemas, registry = {}, Registry()
    for path in sorted(SCHEMAS_DIR.glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        schemas[path.stem] = schema
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return schemas, registry


@lru_cache(maxsize=None)
def validator_for(schema_name: str) -> Draft202012Validator:
    schemas, registry = _load()
    if schema_name not in schemas:
        raise KeyError(f"no schema named {schema_name} in {SCHEMAS_DIR}")
    return Draft202012Validator(schemas[schema_name], registry=registry)


def id_field(collection: str) -> str:
    return COLLECTIONS[collection][1]


def validate(collection: str, document: dict) -> None:
    """Raise ContractError if the document does not match the schema of its collection."""
    if collection not in COLLECTIONS:
        raise KeyError(f"unknown collection {collection}")
    schema_name = COLLECTIONS[collection][0]
    errors = []
    for error in validator_for(schema_name).iter_errors(document):
        where = "/".join(str(p) for p in error.absolute_path) or "(document)"
        errors.append(f"{where}: {error.message}")
    if collection == "visits" and "home_id" not in document:
        errors.append("home_id: required for a standalone visit")
    if errors:
        raise ContractError(collection, errors)
