"""Check the Kibbly data contract.

Every file in examples/valid/<schema>/ must pass its schema and every file in
examples/invalid/<schema>/ must fail it. Run after any change to a schema:

  python schemas/check_examples.py

Needs the jsonschema package (installed in ai_v2/.venv).
"""

import json
import pathlib
import sys

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

HERE = pathlib.Path(__file__).resolve().parent


def load_registry():
    """Load every schema file so that references such as common.json resolve."""
    schemas = {}
    registry = Registry()
    for path in sorted(HERE.glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        schemas[path.stem] = schema
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    return schemas, registry


def main():
    schemas, registry = load_registry()
    rows = []
    failures = 0
    for expected in ("valid", "invalid"):
        for path in sorted((HERE / "examples" / expected).glob("*/*.json")):
            name = path.parent.name
            if name not in schemas:
                rows.append((expected, name, path.stem, "FAIL", "no schema with this name"))
                failures += 1
                continue
            validator = Draft202012Validator(schemas[name], registry=registry)
            errors = list(validator.iter_errors(json.loads(path.read_text(encoding="utf-8"))))
            ok = (not errors) if expected == "valid" else bool(errors)
            reason = errors[0].message[:70] if errors else ""
            rows.append((expected, name, path.stem, "PASS" if ok else "FAIL", reason))
            failures += not ok

    print(f"Schemas: {', '.join(sorted(schemas))}\n")
    print("| expected | schema | example | result | first error |")
    print("|---|---|---|---|---|")
    for row in rows:
        print("| " + " | ".join(row) + " |")
    print(f"\n{len(rows) - failures}/{len(rows)} examples behave as expected")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
