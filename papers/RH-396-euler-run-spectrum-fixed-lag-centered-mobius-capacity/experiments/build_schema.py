"""Generate the recursively closed Draft 2020-12 RH-396 result schema."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "result.schema.json"
if str(ROOT / "experiments") not in sys.path:
    sys.path.insert(0, str(ROOT / "experiments"))

from build_result import (  # noqa: E402
    build_payload,
    canonical_bytes,
    exact_equal,
    loads_strict,
    pretty_json_bytes,
    validate_result_payload,
)


SCHEMA_DRAFT = "https://json-schema.org/draft/2020-12/schema"
SCHEMA_ID = "https://example.invalid/schemas/RH-396-result.schema.json"
SCHEMA_TITLE = "RH-396 exact Stage-1 result"
RESULT_BUILDER_BYTES = 53_755
RESULT_BUILDER_SHA256 = "d7678d1098a61bdb6f7c5c2c96ee6588e840365b09fedd015f1800146372a376"
RESULT_TEST_BYTES = 15_768
RESULT_TEST_SHA256 = "30691e20742bf7135c6960a90bf9f8b038af01b2595a4af85145a0ce87656075"
RESULT_PRETTY_BYTES = 290_629
RESULT_PRETTY_SHA256 = "a7ea39793a255a9b51f2e1b8523293bf4f4a9fdd0934263f9950417ca28371d4"
RESULT_CANONICAL_BYTES = 159_548
RESULT_CANONICAL_SHA256 = "acda92bfc13344aced86dcae698c75a41ca0fe5097aaaf6141bc2ca88563db12"
SCHEMA_FIXTURE_BYTES = 482_712
SCHEMA_FIXTURE_SHA256 = "adc10d848052eb09412d893292b27b2cd6cbf8227a169476e78691efde5d446c"


SCHEMA_MUTATION_NAMES = (
    "draft", "id", "title", "root_extra", "root_required_missing",
    "root_additional_true", "property_removed", "property_extra",
    "scalar_type", "scalar_const", "integer_float_const",
    "boolean_integer_const", "array_items_open", "array_min", "array_max",
    "array_prefix_removed", "array_prefix_reordered", "nested_object_open",
    "nested_required_missing", "nested_keyword_extra", "payload_title",
    "payload_phase_sum", "payload_four_state", "payload_normalization",
    "payload_endpoint", "payload_source_count", "payload_float",
    "payload_forbidden",
)
SCHEMA_BUILDER_NAMES = (
    "build_schema", "_frozen_payload", "exact_schema", "build_payload",
    "validate_result_payload",
)
SCHEMA_HELPER_NAMES = (
    "validate_exact_instance", "canonical_bytes", "pretty_json_bytes",
    "loads_strict", "exact_equal", "_validate_result_seals",
)


def _validate_result_seals() -> None:
    expected = {
        "draft": "https://json-schema.org/draft/2020-12/schema",
        "id": "https://example.invalid/schemas/RH-396-result.schema.json",
        "title": "RH-396 exact Stage-1 result",
        "builder_bytes": 53755,
        "builder_sha": "d7678d1098a61bdb6f7c5c2c96ee6588e840365b09fedd015f1800146372a376",
        "test_bytes": 15768,
        "test_sha": "30691e20742bf7135c6960a90bf9f8b038af01b2595a4af85145a0ce87656075",
        "pretty_bytes": 290629,
        "pretty_sha": "a7ea39793a255a9b51f2e1b8523293bf4f4a9fdd0934263f9950417ca28371d4",
        "canonical_bytes": 159548,
        "canonical_sha": "acda92bfc13344aced86dcae698c75a41ca0fe5097aaaf6141bc2ca88563db12",
    }
    actual = {
        "draft": SCHEMA_DRAFT, "id": SCHEMA_ID, "title": SCHEMA_TITLE,
        "builder_bytes": RESULT_BUILDER_BYTES,
        "builder_sha": RESULT_BUILDER_SHA256,
        "test_bytes": RESULT_TEST_BYTES, "test_sha": RESULT_TEST_SHA256,
        "pretty_bytes": RESULT_PRETTY_BYTES,
        "pretty_sha": RESULT_PRETTY_SHA256,
        "canonical_bytes": RESULT_CANONICAL_BYTES,
        "canonical_sha": RESULT_CANONICAL_SHA256,
    }
    if actual != expected:
        raise ValueError("frozen result/schema identity constants changed")
    if len(SCHEMA_MUTATION_NAMES) != 28 or len(set(SCHEMA_MUTATION_NAMES)) != 28:
        raise ValueError("schema mutation contract changed")


def exact_schema(value: object) -> dict[str, object]:
    """Compile an exact, recursively closed schema for one JSON value."""
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise TypeError("JSON object keys must be exact strings")
        properties = {key: exact_schema(value[key]) for key in sorted(value)}
        return {
            "type": "object",
            "properties": properties,
            "required": sorted(properties),
            "additionalProperties": False,
        }
    if type(value) is list:
        node: dict[str, object] = {
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
    raise TypeError(f"unsupported exact JSON primitive: {type(value).__name__}")


def validate_exact_instance(instance: object, schema: object, path: str = "$") -> None:
    """Evaluate the exact-schema subset without relying on ``assert``."""
    if type(path) is not str:
        raise TypeError("validation path must be exact text")

    def visit(value: object, node: object, current: str) -> None:
        if type(node) is not dict or type(node.get("type")) is not str:
            raise ValueError(f"{current}: typed schema object required")
        kind = node["type"]
        if kind == "object":
            allowed = {"type", "properties", "required", "additionalProperties"}
            if current == "$":
                allowed |= {"$schema", "$id", "title"}
            if set(node) != allowed:
                raise ValueError(f"{current}: object schema membership changed")
            if current == "$" and (
                node["$schema"] != "https://json-schema.org/draft/2020-12/schema"
                or node["$id"] != "https://example.invalid/schemas/RH-396-result.schema.json"
                or node["title"] != "RH-396 exact Stage-1 result"
            ):
                raise ValueError("$: schema identity changed")
            if type(value) is not dict:
                raise ValueError(f"{current}: exact object required")
            properties = node["properties"]
            required = node["required"]
            if (
                type(properties) is not dict
                or type(required) is not list
                or any(type(key) is not str for key in properties)
                or any(type(key) is not str for key in required)
                or required != sorted(properties)
                or node["additionalProperties"] is not False
                or set(value) != set(properties)
            ):
                raise ValueError(f"{current}: recursively closed object changed")
            for key in required:
                visit(value[key], properties[key], f"{current}.{key}")
            return
        if kind == "array":
            allowed = {"type", "items", "minItems", "maxItems"}
            if "prefixItems" in node:
                allowed.add("prefixItems")
            if set(node) != allowed or type(value) is not list:
                raise ValueError(f"{current}: exact array schema changed")
            minimum = node["minItems"]
            maximum = node["maxItems"]
            prefix = node.get("prefixItems", [])
            if (
                type(minimum) is not int or type(minimum) is bool
                or type(maximum) is not int or type(maximum) is bool
                or minimum < 0 or maximum != minimum or len(value) != minimum
                or node["items"] is not False
                or type(prefix) is not list or len(prefix) != len(value)
                or (not value and "prefixItems" in node)
            ):
                raise ValueError(f"{current}: fixed array closure changed")
            for index, item in enumerate(value):
                visit(item, prefix[index], f"{current}[{index}]")
            return
        scalar_types = {
            "boolean": bool, "integer": int, "string": str,
            "null": type(None),
        }
        if set(node) != {"type", "const"} or kind not in scalar_types:
            raise ValueError(f"{current}: exact scalar schema changed")
        expected_type = scalar_types[kind]
        if (
            type(value) is not expected_type
            or type(node["const"]) is not expected_type
            or value != node["const"]
        ):
            raise ValueError(f"{current}: exact scalar changed")

    visit(instance, schema, path)


def _frozen_payload(*, compare_fresh: bool = True) -> dict[str, object]:
    if type(compare_fresh) is not bool:
        raise TypeError("compare_fresh must be exact bool")
    _validate_result_seals()
    for path, size, digest in (
        (ROOT / "experiments" / "build_result.py", RESULT_BUILDER_BYTES, RESULT_BUILDER_SHA256),
        (ROOT / "tests" / "test_result.py", RESULT_TEST_BYTES, RESULT_TEST_SHA256),
        (ROOT / "results" / "result.json", RESULT_PRETTY_BYTES, RESULT_PRETTY_SHA256),
    ):
        raw = path.read_bytes()
        if len(raw) != size or sha256(raw).hexdigest() != digest:
            raise RuntimeError(f"frozen file identity changed: {path.name}")
    result_path = ROOT / "results" / "result.json"
    stored = loads_strict(result_path.read_text(encoding="utf-8"))
    if type(stored) is not dict:
        raise RuntimeError("stored result is not an object")
    canonical = canonical_bytes(stored)
    if (
        len(canonical) != RESULT_CANONICAL_BYTES
        or sha256(canonical).hexdigest() != RESULT_CANONICAL_SHA256
        or validate_result_payload(stored, compare_fresh=False) is not True
    ):
        raise RuntimeError("stored result canonical seal changed")
    if compare_fresh and not exact_equal(stored, build_payload()):
        raise RuntimeError("stored and fresh result differ")
    return stored


def build_schema(*, compare_fresh_result: bool = True) -> dict[str, object]:
    if type(compare_fresh_result) is not bool:
        raise TypeError("compare_fresh_result must be exact bool")
    payload = _frozen_payload(compare_fresh=compare_fresh_result)
    schema = exact_schema(payload)
    schema["$schema"] = SCHEMA_DRAFT
    schema["$id"] = SCHEMA_ID
    schema["title"] = SCHEMA_TITLE
    validate_exact_instance(payload, schema)
    return schema


def official_validation_status(instance: object, schema: object) -> dict[str, object]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return {
            "available": False,
            "draft": "2020-12",
            "schema_valid": None,
            "instance_valid": None,
        }
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(instance))
    return {
        "available": True,
        "draft": "2020-12",
        "schema_valid": True,
        "instance_valid": not errors,
    }


def _make_schema_validator():
    """Capture an exact false-mode schema validator over local primitives."""
    from hashlib import sha256 as local_sha256
    from json import dumps as local_dumps

    schema_bytes_literal = 482712
    schema_sha_literal = "adc10d848052eb09412d893292b27b2cd6cbf8227a169476e78691efde5d446c"
    result_bytes_literal = 159548
    result_sha_literal = "acda92bfc13344aced86dcae698c75a41ca0fe5097aaaf6141bc2ca88563db12"

    def encode(value: object) -> bytes:
        return local_dumps(
            value, ensure_ascii=False, allow_nan=False, sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def compile_local(value: object) -> dict[str, object]:
        if type(value) is dict:
            if any(type(key) is not str for key in value):
                raise TypeError("non-string JSON key")
            properties = {key: compile_local(value[key]) for key in sorted(value)}
            return {
                "type": "object",
                "properties": properties,
                "required": sorted(properties),
                "additionalProperties": False,
            }
        if type(value) is list:
            node: dict[str, object] = {
                "type": "array", "items": False,
                "minItems": len(value), "maxItems": len(value),
            }
            if value:
                node["prefixItems"] = [compile_local(item) for item in value]
            return node
        if type(value) is bool:
            return {"type": "boolean", "const": value}
        if type(value) is int:
            return {"type": "integer", "const": value}
        if type(value) is str:
            return {"type": "string", "const": value}
        if value is None:
            return {"type": "null", "const": None}
        raise TypeError("unsupported JSON value")

    def same(left: object, right: object) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return set(left) == set(right) and all(
                same(left[key], right[key]) for key in left
            )
        if type(left) is list:
            return len(left) == len(right) and all(
                same(a, b) for a, b in zip(left, right)
            )
        return left == right

    def semantic(schema: object, payload: object) -> bool:
        try:
            schema_raw = encode(schema)
            payload_raw = encode(payload)
        except (TypeError, ValueError, OverflowError):
            return False
        if not (
            len(schema_raw) == schema_bytes_literal
            and local_sha256(schema_raw).hexdigest() == schema_sha_literal
            and len(payload_raw) == result_bytes_literal
            and local_sha256(payload_raw).hexdigest() == result_sha_literal
            and type(schema) is dict
            and type(payload) is dict
        ):
            return False
        expected = compile_local(payload)
        expected["$schema"] = "https://json-schema.org/draft/2020-12/schema"
        expected["$id"] = "https://example.invalid/schemas/RH-396-result.schema.json"
        expected["title"] = "RH-396 exact Stage-1 result"
        return same(schema, expected)

    independent_semantic = semantic
    fresh_builder = build_schema

    def verifier(
        schema: object, payload: object, *, compare_fresh: bool = True,
    ) -> bool:
        if type(compare_fresh) is not bool:
            return False
        try:
            if not independent_semantic(schema, payload):
                return False
            return not compare_fresh or same(
                schema, fresh_builder(compare_fresh_result=False)
            )
        except (
            ArithmeticError, AttributeError, KeyError, TypeError, ValueError,
            RuntimeError, IndexError,
        ):
            return False

    return verifier


validate_schema_artifact = _make_schema_validator()
del _make_schema_validator


def mutate_schema(
    schema: dict[str, object], payload: dict[str, object], name: str,
) -> tuple[dict[str, object], dict[str, object]]:
    if (
        type(schema) is not dict or type(payload) is not dict
        or type(name) is not str or name not in SCHEMA_MUTATION_NAMES
    ):
        raise ValueError("unknown schema mutation")
    changed_schema = deepcopy(schema)
    changed_payload = deepcopy(payload)
    properties = changed_schema["properties"]
    actions = {
        "draft": lambda: changed_schema.__setitem__("$schema", "draft-07"),
        "id": lambda: changed_schema.__setitem__("$id", "wrong"),
        "title": lambda: changed_schema.__setitem__("title", "wrong"),
        "root_extra": lambda: changed_schema.__setitem__("extra", 0),
        "root_required_missing": lambda: changed_schema["required"].pop(),
        "root_additional_true": lambda: changed_schema.__setitem__("additionalProperties", True),
        "property_removed": lambda: properties.pop("title"),
        "property_extra": lambda: properties.__setitem__("extra", {"type": "integer", "const": 0}),
        "scalar_type": lambda: properties["schema_version"].__setitem__("type", "number"),
        "scalar_const": lambda: properties["paper"].__setitem__("const", "RH-395"),
        "integer_float_const": lambda: properties["schema_version"].__setitem__("const", 1.0),
        "boolean_integer_const": lambda: properties["all_pass"].__setitem__("const", 1),
        "array_items_open": lambda: properties["core_mutation_audit"].__setitem__("items", {}),
        "array_min": lambda: properties["core_mutation_audit"].__setitem__("minItems", 31),
        "array_max": lambda: properties["core_mutation_audit"].__setitem__("maxItems", 33),
        "array_prefix_removed": lambda: properties["core_mutation_audit"].pop("prefixItems"),
        "array_prefix_reordered": lambda: properties["core_mutation_audit"]["prefixItems"].reverse(),
        "nested_object_open": lambda: properties["summary"].__setitem__("additionalProperties", True),
        "nested_required_missing": lambda: properties["summary"]["required"].pop(),
        "nested_keyword_extra": lambda: properties["summary"].__setitem__("description", "wrong"),
        "payload_title": lambda: changed_payload.__setitem__("title", "wrong"),
        "payload_phase_sum": lambda: changed_payload["theorem_contracts"]["phase_densities"].__setitem__("phase_sum", "K_|S|"),
        "payload_four_state": lambda: changed_payload["theorem_contracts"]["tropical_capacity"].__setitem__("four_state_scope", "all q"),
        "payload_normalization": lambda: changed_payload["summary"].__setitem__("normalization", "alpha is weighted"),
        "payload_endpoint": lambda: changed_payload["theorem_contracts"]["strict_nonattainment"].__setitem__("finite_strictness", "attained"),
        "payload_source_count": lambda: changed_payload["source_closure"].__setitem__("git_count", 159),
        "payload_float": lambda: changed_payload.__setitem__("schema_version", 1.0),
        "payload_forbidden": lambda: changed_payload["forbidden"].__setitem__("growing_h", True),
    }
    if set(actions) != set(SCHEMA_MUTATION_NAMES):
        raise RuntimeError("schema mutation action table changed")
    actions[name]()
    return changed_schema, changed_payload


def main() -> None:
    payload = _frozen_payload(compare_fresh=True)
    schema = build_schema(compare_fresh_result=False)
    validate_exact_instance(payload, schema)
    if validate_schema_artifact(schema, payload, compare_fresh=False) is not True:
        raise RuntimeError("fresh schema failed independent validation")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(pretty_json_bytes(schema))
    official = official_validation_status(payload, schema)
    print(json.dumps({
        "draft": "2020-12", "closed": True,
        "bytes": len(OUTPUT.read_bytes()),
        "sha256": sha256(OUTPUT.read_bytes()).hexdigest(),
        "official_validator_available": official["available"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
