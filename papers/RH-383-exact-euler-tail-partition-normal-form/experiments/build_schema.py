"""Generate the recursively closed Draft 2020-12 RH-383 result schema."""

from __future__ import annotations

import json

from experiments.build_result import ROOT, load_json


OUTPUT = ROOT / "results" / "result.schema.json"
RESULT = ROOT / "results" / "result.json"


def exact_schema(value: object) -> dict[str, object]:
    """Return a closed exact structural schema; bool remains distinct from int."""

    if type(value) is dict:
        properties = {key: exact_schema(child) for key, child in value.items()}
        return {
            "type": "object",
            "additionalProperties": False,
            "required": list(value),
            "properties": properties,
        }
    if type(value) is list:
        return {
            "type": "array",
            "minItems": len(value),
            "maxItems": len(value),
            "prefixItems": [exact_schema(child) for child in value],
            "items": False,
        }
    if type(value) is bool:
        return {"type": "boolean", "const": value}
    if type(value) is int:
        return {"type": "integer", "const": value}
    if type(value) is str:
        return {"type": "string", "const": value}
    raise TypeError(f"unsupported JSON primitive: {type(value).__name__}")


def build_schema() -> dict[str, object]:
    payload = load_json(RESULT)
    schema = exact_schema(payload)
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.invalid/RH-383/result.schema.json",
        "title": "RH-383 exact result ledger",
        **schema,
    }


def serialized_schema(schema: dict[str, object]) -> str:
    return json.dumps(schema, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> None:
    schema = build_schema()
    OUTPUT.write_text(serialized_schema(schema))
    print(json.dumps({"status": "RH-383_closed_schema_built", "bytes": OUTPUT.stat().st_size}, sort_keys=True))


if __name__ == "__main__":
    main()
