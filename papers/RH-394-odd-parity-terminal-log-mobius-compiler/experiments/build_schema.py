"""Generate the recursively closed Draft 2020-12 RH-394 result schema."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "result.schema.json"
if str(ROOT / "experiments") not in sys.path:
    sys.path.insert(0, str(ROOT / "experiments"))

from build_result import (  # noqa: E402
    build_payload, canonical_bytes, loads_strict, pretty_json_bytes,
    validate_result_payload,
)


SCHEMA_DRAFT = "https://json-schema.org/draft/2020-12/schema"
SCHEMA_ID = "https://example.invalid/schemas/RH-394-result.schema.json"
SCHEMA_TITLE = "RH-394 exact Stage-1 result"
RESULT_BUILDER_SHA256 = "a9d2b17f40022f875af33fd15c1a7f2030c9dd710cbc4b398be6a2a8bd4f4722"
RESULT_PRETTY_SHA256 = "935de4967e504e5c32f6d27980ec044c3cffccfbab534440730470de8b1ae610"
RESULT_CANONICAL_BYTES = 166_133
RESULT_CANONICAL_SHA256 = "9b69b6b8ec00d0bf7191deadef9fd7cf9005b092988cde96fa2d858029200f3a"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _validate_schema_constants() -> None:
    expected = {
        "draft": "https://json-schema.org/draft/2020-12/schema",
        "id": "https://example.invalid/schemas/RH-394-result.schema.json",
        "title": "RH-394 exact Stage-1 result",
        "builder": "a9d2b17f40022f875af33fd15c1a7f2030c9dd710cbc4b398be6a2a8bd4f4722",
        "pretty": "935de4967e504e5c32f6d27980ec044c3cffccfbab534440730470de8b1ae610",
        "canonical_bytes": 166_133,
        "canonical_sha": "9b69b6b8ec00d0bf7191deadef9fd7cf9005b092988cde96fa2d858029200f3a",
    }
    actual = {
        "draft": SCHEMA_DRAFT,
        "id": SCHEMA_ID,
        "title": SCHEMA_TITLE,
        "builder": RESULT_BUILDER_SHA256,
        "pretty": RESULT_PRETTY_SHA256,
        "canonical_bytes": RESULT_CANONICAL_BYTES,
        "canonical_sha": RESULT_CANONICAL_SHA256,
    }
    if type(actual) is not dict or actual != expected:
        raise ValueError("independent schema identity/result seal changed")
    if any(
        type(value) is not str or not SHA256_RE.fullmatch(value)
        for key, value in actual.items()
        if key in {"builder", "pretty", "canonical_sha"}
    ):
        raise ValueError("schema SHA-256 seal malformed")
    if type(RESULT_CANONICAL_BYTES) is not int or type(RESULT_CANONICAL_BYTES) is bool:
        raise ValueError("result canonical byte seal malformed")


def exact_schema(value: Any) -> dict[str, Any]:
    """Compile a finite JSON value into a recursively closed exact schema."""

    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise TypeError("JSON object keys must be strings")
        properties = {key: exact_schema(value[key]) for key in sorted(value)}
        return {
            "type": "object",
            "properties": properties,
            "required": sorted(properties),
            "additionalProperties": False,
        }
    if type(value) is list:
        node: dict[str, Any] = {
            "type": "array",
            "items": False,
            "minItems": len(value),
            "maxItems": len(value),
        }
        if value:
            node["prefixItems"] = [exact_schema(item) for item in value]
        return node
    if type(value) is bool:
        return {"type": "boolean", "const": value}
    if type(value) is int:
        return {"type": "integer", "const": value}
    if type(value) is str:
        return {"type": "string", "const": value}
    if value is None:
        return {"type": "null", "const": None}
    raise TypeError(f"unsupported schema primitive: {type(value).__name__}")


def validate_exact_instance(instance: Any, schema: Any, path: str = "$") -> None:
    """Evaluate the exact schema without calling any schema or result builder."""

    if type(path) is not str:
        raise TypeError("path must be an exact string")

    def visit(value: Any, node: Any, current_path: str) -> None:
        if type(node) is not dict or type(node.get("type")) is not str:
            raise ValueError(f"{current_path}: typed schema object required")
        kind = node["type"]
        if kind == "object":
            root = current_path == "$"
            keywords = {"type", "properties", "required", "additionalProperties"}
            if root:
                keywords |= {"$schema", "$id", "title"}
            if set(node) != keywords:
                raise ValueError(f"{current_path}: schema keyword membership changed")
            if root and (
                node["$schema"] != "https://json-schema.org/draft/2020-12/schema"
                or node["$id"] != "https://example.invalid/schemas/RH-394-result.schema.json"
                or node["title"] != "RH-394 exact Stage-1 result"
            ):
                raise ValueError("$: schema identity changed")
            if type(value) is not dict:
                raise ValueError(f"{current_path}: object required")
            properties = node["properties"]
            required = node["required"]
            if type(properties) is not dict or any(type(key) is not str for key in properties):
                raise ValueError(f"{current_path}: properties changed")
            if type(required) is not list or any(type(key) is not str for key in required):
                raise ValueError(f"{current_path}: required changed")
            if (
                required != sorted(properties)
                or node["additionalProperties"] is not False
                or set(value) != set(properties)
            ):
                raise ValueError(f"{current_path}: object closure changed")
            for key in required:
                visit(value[key], properties[key], f"{current_path}.{key}")
            return
        if kind == "array":
            keywords = {"type", "items", "minItems", "maxItems"}
            if "prefixItems" in node:
                keywords.add("prefixItems")
            if set(node) != keywords:
                raise ValueError(f"{current_path}: schema keyword membership changed")
            if type(value) is not list:
                raise ValueError(f"{current_path}: array required")
            minimum = node["minItems"]
            maximum = node["maxItems"]
            if (
                type(minimum) is not int
                or type(minimum) is bool
                or type(maximum) is not int
                or type(maximum) is bool
                or minimum < 0
                or maximum != minimum
                or len(value) != minimum
                or node["items"] is not False
            ):
                raise ValueError(f"{current_path}: fixed-array closure changed")
            prefix = node.get("prefixItems", [])
            if (
                type(prefix) is not list
                or len(prefix) != len(value)
                or (not value and "prefixItems" in node)
            ):
                raise ValueError(f"{current_path}: positional schema changed")
            for index, item in enumerate(value):
                visit(item, prefix[index], f"{current_path}[{index}]")
            return
        scalar_types = {
            "boolean": bool,
            "integer": int,
            "string": str,
            "null": type(None),
        }
        if set(node) != {"type", "const"}:
            raise ValueError(f"{current_path}: schema keyword membership changed")
        if (
            kind not in scalar_types
            or type(value) is not scalar_types[kind]
            or type(node["const"]) is not scalar_types[kind]
            or value != node["const"]
        ):
            raise ValueError(f"{current_path}: exact scalar changed")

    visit(instance, schema, path)


def _frozen_payload() -> dict[str, Any]:
    _validate_schema_constants()
    builder_path = ROOT / "experiments" / "build_result.py"
    result_path = ROOT / "results" / "result.json"
    if sha256(builder_path.read_bytes()).hexdigest() != RESULT_BUILDER_SHA256:
        raise RuntimeError("result builder file seal changed")
    if sha256(result_path.read_bytes()).hexdigest() != RESULT_PRETTY_SHA256:
        raise RuntimeError("stored result file seal changed")
    stored = loads_strict(result_path.read_text(encoding="utf-8"))
    raw = canonical_bytes(stored)
    if (
        len(raw) != RESULT_CANONICAL_BYTES
        or sha256(raw).hexdigest() != RESULT_CANONICAL_SHA256
        or validate_result_payload(stored, compare_fresh=False) is not True
    ):
        raise RuntimeError("stored result canonical seal changed")
    fresh = build_payload()
    if stored != fresh:
        raise RuntimeError("stored and fresh result differ")
    return stored


def build_schema() -> dict[str, Any]:
    payload = _frozen_payload()
    schema = exact_schema(payload)
    schema["$schema"] = SCHEMA_DRAFT
    schema["$id"] = SCHEMA_ID
    schema["title"] = SCHEMA_TITLE
    validate_exact_instance(payload, schema)
    return schema


def main() -> None:
    payload = _frozen_payload()
    schema = build_schema()
    validate_exact_instance(payload, schema)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_json_bytes(schema))
    print(json.dumps({
        "draft": SCHEMA_DRAFT,
        "closed": True,
        "instance_valid": True,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
