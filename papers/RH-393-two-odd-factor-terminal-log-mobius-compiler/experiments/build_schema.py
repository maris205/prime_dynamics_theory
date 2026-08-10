"""Generate and independently check the closed Draft 2020-12 RH-393 schema."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "result.schema.json"
if str(ROOT / "experiments") not in sys.path:
    sys.path.insert(0, str(ROOT / "experiments"))

from build_result import build_payload, pretty_json_bytes  # noqa: E402


SCHEMA_DRAFT = "https://json-schema.org/draft/2020-12/schema"
SCHEMA_ID = "https://example.invalid/schemas/RH-393-result.schema.json"
SCHEMA_TITLE = "RH-393 exact Stage-1 result"


def exact_schema(value: object) -> dict[str, object]:
    """Compile one finite JSON value to a recursively closed exact schema."""
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise TypeError("JSON object keys must be strings")
        properties = {key: exact_schema(value[key]) for key in sorted(value)}
        return {
            "type": "object", "properties": properties,
            "required": sorted(properties), "additionalProperties": False,
        }
    if type(value) is list:
        schema: dict[str, object] = {
            "type": "array", "items": False,
            "minItems": len(value), "maxItems": len(value),
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


def _require_keys(value: object, expected: set[str], path: str) -> dict[str, object]:
    if type(value) is not dict or set(value) != expected:
        raise ValueError(f"{path}: schema keyword membership changed")
    return value


def validate_exact_instance(instance: object, schema: object, path: str = "$") -> None:
    """Evaluate the exact-schema fragment without invoking a schema builder."""
    if type(path) is not str:
        raise TypeError("path must be an exact string")

    def visit(value: object, node: object, current_path: str) -> None:
        if type(node) is not dict or type(node.get("type")) is not str:
            raise ValueError(f"{current_path}: typed schema object required")
        kind = node["type"]
        if kind == "object":
            root = current_path == "$"
            expected = {"type", "properties", "required", "additionalProperties"}
            if root:
                expected |= {"$schema", "$id", "title"}
            if set(node) != expected:
                raise ValueError(f"{current_path}: schema keyword membership changed")
            if root and (
                node["$schema"] != "https://json-schema.org/draft/2020-12/schema"
                or node["$id"] != "https://example.invalid/schemas/RH-393-result.schema.json"
                or node["title"] != "RH-393 exact Stage-1 result"
            ):
                raise ValueError("$: schema identity changed")
            if type(value) is not dict:
                raise ValueError(f"{current_path}: object required")
            properties, required = node["properties"], node["required"]
            if type(properties) is not dict or any(
                type(key) is not str for key in properties
            ):
                raise ValueError(f"{current_path}: properties changed")
            if type(required) is not list or any(type(key) is not str for key in required):
                raise ValueError(f"{current_path}: required changed")
            if required != sorted(properties) or node["additionalProperties"] is not False:
                raise ValueError(f"{current_path}: object closure changed")
            if set(value) != set(properties):
                raise ValueError(f"{current_path}: object membership changed")
            for key in required:
                visit(value[key], properties[key], f"{current_path}.{key}")
            return
        if kind == "array":
            expected = {"type", "items", "minItems", "maxItems"}
            if "prefixItems" in node:
                expected.add("prefixItems")
            if set(node) != expected:
                raise ValueError(f"{current_path}: schema keyword membership changed")
            if type(value) is not list:
                raise ValueError(f"{current_path}: array required")
            minimum, maximum = node["minItems"], node["maxItems"]
            if (
                type(minimum) is not int or type(minimum) is bool
                or type(maximum) is not int or type(maximum) is bool
                or minimum < 0 or maximum != minimum or len(value) != minimum
                or node["items"] is not False
            ):
                raise ValueError(f"{current_path}: fixed-array closure changed")
            prefix = node.get("prefixItems", [])
            if (
                type(prefix) is not list or len(prefix) != len(value)
                or (not value and "prefixItems" in node)
            ):
                raise ValueError(f"{current_path}: positional schema changed")
            for index, item in enumerate(value):
                visit(item, prefix[index], f"{current_path}[{index}]")
            return
        scalar_types = {
            "boolean": bool, "integer": int, "string": str, "null": type(None),
        }
        if set(node) != {"type", "const"}:
            raise ValueError(f"{current_path}: schema keyword membership changed")
        if (
            kind not in scalar_types or type(value) is not scalar_types[kind]
            or type(node["const"]) is not scalar_types[kind]
        ):
            raise ValueError(f"{current_path}: exact scalar type changed")
        if value != node["const"]:
            raise ValueError(f"{current_path}: scalar value changed")

    visit(instance, schema, path)


def build_schema() -> dict[str, object]:
    payload = build_payload()
    schema = exact_schema(payload)
    schema["$schema"] = SCHEMA_DRAFT
    schema["$id"] = SCHEMA_ID
    schema["title"] = SCHEMA_TITLE
    validate_exact_instance(payload, schema)
    return schema


def main() -> None:
    payload = build_payload()
    schema = build_schema()
    validate_exact_instance(payload, schema)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_json_bytes(schema))
    print(json.dumps({
        "draft": SCHEMA_DRAFT, "closed": True, "instance_valid": True,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
