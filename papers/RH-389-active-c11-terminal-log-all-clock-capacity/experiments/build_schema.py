"""Generate the recursively closed official Draft 2020-12 RH-389 schema."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "result.schema.json"
if str(ROOT / "experiments") not in sys.path:
    sys.path.insert(0, str(ROOT / "experiments"))

from build_result import build_payload  # noqa: E402


def exact_schema(value: object) -> dict[str, object]:
    if type(value) is dict:
        properties = {key: exact_schema(value[key]) for key in sorted(value)}
        return {
            "additionalProperties": False,
            "properties": properties,
            "required": sorted(properties),
            "type": "object",
        }
    if type(value) is list:
        schema: dict[str, object] = {
            "items": False,
            "maxItems": len(value),
            "minItems": len(value),
            "type": "array",
        }
        if value:
            schema["prefixItems"] = [exact_schema(item) for item in value]
        return schema
    if type(value) is bool:
        return {"const": value, "type": "boolean"}
    if type(value) is int:
        return {"const": value, "type": "integer"}
    if type(value) is str:
        return {"const": value, "type": "string"}
    if value is None:
        return {"const": None, "type": "null"}
    raise TypeError(f"unsupported schema primitive: {type(value).__name__}")


def build_schema() -> dict[str, object]:
    schema = exact_schema(build_payload())
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = "https://example.invalid/schemas/RH-389-result.schema.json"
    schema["title"] = "RH-389 exact release result"
    return schema


def main() -> None:
    schema = build_schema()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(schema, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"closed": True, "draft": schema["$schema"]}, sort_keys=True))


if __name__ == "__main__":
    main()
