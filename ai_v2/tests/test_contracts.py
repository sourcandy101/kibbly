import pytest

from kibbly_ai import contracts
from tests.conftest import EXAMPLES, load_example

SCHEMA_TO_COLLECTION = {schema: name for name, (schema, _) in contracts.COLLECTIONS.items()}


def examples(kind):
    return sorted((p.parent.name, p.stem) for p in (EXAMPLES / kind).glob("*/*.json"))


def test_every_schema_has_a_collection():
    names = {p.stem for p in contracts.SCHEMAS_DIR.glob("*.json")} - {"common"}
    assert names == set(SCHEMA_TO_COLLECTION)


@pytest.mark.parametrize("schema,name", examples("valid"))
def test_valid_examples_pass(schema, name):
    contracts.validate(SCHEMA_TO_COLLECTION[schema], load_example("valid", schema, name))


@pytest.mark.parametrize("schema,name", examples("invalid"))
def test_invalid_examples_fail(schema, name):
    with pytest.raises(contracts.ContractError):
        contracts.validate(SCHEMA_TO_COLLECTION[schema], load_example("invalid", schema, name))


def test_standalone_visit_needs_home_id():
    visit = load_example("valid", "visit", "mochi_between_meals")
    visit.pop("home_id")
    with pytest.raises(contracts.ContractError, match="home_id"):
        contracts.validate("visits", visit)
