"""Generate the recursively closed official Draft 2020-12 RH-390 schema."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "result.schema.json"
if str(ROOT / "experiments") not in sys.path:
    sys.path.insert(0, str(ROOT / "experiments"))

from build_result import build_payload, pretty_json_bytes  # noqa: E402


def exact_schema(value: object) -> dict[str, object]:
    if type(value) is dict:
        properties = {key: exact_schema(value[key]) for key in sorted(value)}
        return {
            "type": "object",
            "properties": properties,
            "required": sorted(properties),
            "additionalProperties": False,
        }
    if type(value) is list:
        schema: dict[str, object] = {
            "type": "array",
            "items": False,
            "minItems": len(value),
            "maxItems": len(value),
        }
        if value:
            schema["prefixItems"] = [exact_schema(item) for item in value]
        return schema
    if type(value) is bool:
        return {"type": "boolean", "const": value}
    if type(value) is int:
        return {"type": "integer", "const": value}
    if type(value) is str:
        return {"type": "string", "const": value}
    if value is None:
        return {"type": "null", "const": None}
    raise TypeError(f"unsupported schema primitive: {type(value).__name__}")


def build_schema() -> dict[str, object]:
    schema = exact_schema(build_payload())
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = "https://example.invalid/schemas/RH-390-result.schema.json"
    schema["title"] = "RH-390 exact release result"
    return schema


def main() -> None:
    schema = build_schema()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_json_bytes(schema))
    print(json.dumps({"draft": schema["$schema"], "closed": True}, sort_keys=True))


if __name__ == "__main__":
    main()
