"""Generate the recursively closed Draft 2020-12 RH-397 result schema."""

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
SCHEMA_ID = "https://example.invalid/schemas/RH-397-result.schema.json"
SCHEMA_TITLE = "RH-397 exact Stage-1 result"
RESULT_BUILDER_BYTES = 37_221
RESULT_BUILDER_SHA256 = "5ccbc206c98020ec1afc08c7aa7a7157031907be3d5ad48e707b13f03a0ef3a2"
RESULT_TEST_BYTES = 9_296
RESULT_TEST_SHA256 = "a0e3418ca4e9ba266c249a6e375cd7664c43b81e5d888d4dfc0a1d9fffe8e3fc"
RESULT_PRETTY_BYTES = 151_768
RESULT_PRETTY_SHA256 = "d21f3ab160c7cb5cfca1ff04ac7d2104ea8a7802b36eb3e2f07e32cbe1d27e4f"
RESULT_CANONICAL_BYTES = 105_495
RESULT_CANONICAL_SHA256 = "d2445cc883371ccfd96eeb09f908d62d232fcb5cde5ea9170aa2029956047c2a"
SCHEMA_FIXTURE_BYTES = 257_468
SCHEMA_FIXTURE_SHA256 = "c3a5b2a02b027cc18b67e63b32f0a238990a4754fe4f2f2ce3c8d1acf756b910"
SCHEMA_PRETTY_BYTES = 670_920
SCHEMA_PRETTY_SHA256 = "4f16580a613e3e0c3930fd53e3a418023fac96e2cfa15f74ed447a60bea38f83"


SCHEMA_MUTATION_NAMES = (
    "draft", "id", "title", "result_hash", "schema_bytes", "schema_hash",
    "root_open", "nested_object_open", "required_missing",
    "required_extra", "required_unsorted", "array_items_open",
    "array_min_float", "array_min_bool", "array_max_wrong", "prefix_drop",
    "prefix_reverse", "primitive_const", "primitive_type", "bool_as_integer",
    "certificate_rows_open", "core_audit_items_open", "source_entries_open",
    "theorem_nested_open", "forbidden_nested_open", "mutation_order_open",
    "payload_extra", "payload_type", "payload_list_order",
    "official_draft_claim", "factory_rebind", "compiler_rebind",
)
SCHEMA_BUILDER_NAMES = (
    "build_schema", "_frozen_payload", "exact_schema", "build_payload",
    "validate_result_payload", "make_schema_validator",
)
SCHEMA_HELPER_NAMES = (
    "validate_exact_instance", "canonical_bytes", "pretty_json_bytes",
    "loads_strict", "exact_equal", "_validate_result_seals",
)


def _validate_result_seals() -> None:
    expected = {
        "draft": "https://json-schema.org/draft/2020-12/schema",
        "id": "https://example.invalid/schemas/RH-397-result.schema.json",
        "title": "RH-397 exact Stage-1 result",
        "builder_bytes": 37221,
        "builder_sha": "5ccbc206c98020ec1afc08c7aa7a7157031907be3d5ad48e707b13f03a0ef3a2",
        "test_bytes": 9296,
        "test_sha": "a0e3418ca4e9ba266c249a6e375cd7664c43b81e5d888d4dfc0a1d9fffe8e3fc",
        "pretty_bytes": 151768,
        "pretty_sha": "d21f3ab160c7cb5cfca1ff04ac7d2104ea8a7802b36eb3e2f07e32cbe1d27e4f",
        "canonical_bytes": 105495,
        "canonical_sha": "d2445cc883371ccfd96eeb09f908d62d232fcb5cde5ea9170aa2029956047c2a",
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
    if len(SCHEMA_MUTATION_NAMES) != 32 or len(set(SCHEMA_MUTATION_NAMES)) != 32:
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
                or node["$id"] != "https://example.invalid/schemas/RH-397-result.schema.json"
                or node["title"] != "RH-397 exact Stage-1 result"
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


def make_schema_validator(compiler: object, builder: object):
    """Construct a sealed validator and reject a poisoned compiler or builder.

    The returned ``compare_fresh=False`` path captures every primitive it uses.
    It therefore remains independent of all public builders, helpers, constants,
    modules, and comparators after construction.
    """

    from copy import deepcopy as local_deepcopy
    from hashlib import sha256 as local_sha256
    from json import dumps as local_dumps

    if not callable(compiler) or not callable(builder):
        raise TypeError("schema compiler and builder must be callable")

    schema_bytes_literal = 257468
    schema_sha_literal = "c3a5b2a02b027cc18b67e63b32f0a238990a4754fe4f2f2ce3c8d1acf756b910"
    schema_pretty_bytes_literal = 670920
    schema_pretty_sha_literal = "4f16580a613e3e0c3930fd53e3a418023fac96e2cfa15f74ed447a60bea38f83"
    result_bytes_literal = 105495
    result_sha_literal = "d2445cc883371ccfd96eeb09f908d62d232fcb5cde5ea9170aa2029956047c2a"
    result_pretty_bytes_literal = 151768
    result_pretty_sha_literal = "d21f3ab160c7cb5cfca1ff04ac7d2104ea8a7802b36eb3e2f07e32cbe1d27e4f"
    node_counts_literal = {
        "object": 568, "array": 140, "boolean": 518,
        "integer": 420, "string": 1838, "null": 0,
    }

    def encode(value: object) -> bytes:
        return local_dumps(
            value, ensure_ascii=False, allow_nan=False, sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def pretty(value: object) -> bytes:
        return (local_dumps(
            value, ensure_ascii=False, allow_nan=False, sort_keys=False,
            indent=2,
        ) + "\n").encode("utf-8")

    def exact_json(value: object) -> bool:
        if type(value) is dict:
            return all(
                type(key) is str and exact_json(item)
                for key, item in value.items()
            )
        if type(value) is list:
            return all(exact_json(item) for item in value)
        return type(value) in (bool, int, str) or value is None

    def same(left: object, right: object) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return tuple(left) == tuple(right) and all(
                same(left[key], right[key]) for key in left
            )
        if type(left) is list:
            return len(left) == len(right) and all(
                same(a, b) for a, b in zip(left, right)
            )
        return left == right

    def counts(node: object) -> dict[str, int]:
        output = {
            "object": 0, "array": 0, "boolean": 0,
            "integer": 0, "string": 0, "null": 0,
        }

        def visit(current: object) -> None:
            if type(current) is not dict or type(current.get("type")) is not str:
                raise ValueError("typed schema node required")
            kind = current["type"]
            if kind not in output:
                raise ValueError("unknown exact schema node")
            output[kind] += 1
            if kind == "object":
                properties = current.get("properties")
                if type(properties) is not dict:
                    raise ValueError("object properties required")
                for child in properties.values():
                    visit(child)
            elif kind == "array":
                prefix = current.get("prefixItems", [])
                if type(prefix) is not list:
                    raise ValueError("array prefix must be a list")
                for child in prefix:
                    visit(child)

        visit(node)
        return output

    payload_at_construction = _frozen_payload(compare_fresh=False)
    compiled = compiler(payload_at_construction)
    if type(compiled) is not dict:
        raise RuntimeError("schema compiler returned a non-object")
    compiled["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    compiled["$id"] = "https://example.invalid/schemas/RH-397-result.schema.json"
    compiled["title"] = "RH-397 exact Stage-1 result"
    built = builder(compare_fresh_result=False)
    compiled_raw = encode(compiled)
    payload_raw = encode(payload_at_construction)
    compiled_pretty = pretty(compiled)
    payload_pretty = pretty(payload_at_construction)
    if not (
        exact_json(compiled)
        and exact_json(payload_at_construction)
        and len(compiled_raw) == schema_bytes_literal
        and local_sha256(compiled_raw).hexdigest() == schema_sha_literal
        and len(compiled_pretty) == schema_pretty_bytes_literal
        and local_sha256(compiled_pretty).hexdigest() == schema_pretty_sha_literal
        and len(payload_raw) == result_bytes_literal
        and local_sha256(payload_raw).hexdigest() == result_sha_literal
        and len(payload_pretty) == result_pretty_bytes_literal
        and local_sha256(payload_pretty).hexdigest() == result_pretty_sha_literal
        and counts(compiled) == node_counts_literal
        and same(compiled, built)
    ):
        raise RuntimeError("schema validator factory inputs are not frozen")

    expected_schema = local_deepcopy(compiled)
    expected_payload = local_deepcopy(payload_at_construction)
    captured_builder = builder

    def semantic(schema: object, payload: object) -> bool:
        try:
            schema_raw = encode(schema)
            payload_raw_local = encode(payload)
            schema_pretty = pretty(schema)
            payload_pretty_local = pretty(payload)
            return (
                type(schema) is dict
                and type(payload) is dict
                and exact_json(schema)
                and exact_json(payload)
                and len(schema_raw) == schema_bytes_literal
                and local_sha256(schema_raw).hexdigest() == schema_sha_literal
                and len(schema_pretty) == schema_pretty_bytes_literal
                and local_sha256(schema_pretty).hexdigest() == schema_pretty_sha_literal
                and len(payload_raw_local) == result_bytes_literal
                and local_sha256(payload_raw_local).hexdigest() == result_sha_literal
                and len(payload_pretty_local) == result_pretty_bytes_literal
                and local_sha256(payload_pretty_local).hexdigest() == result_pretty_sha_literal
                and counts(schema) == node_counts_literal
                and schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
                and schema.get("$id") == "https://example.invalid/schemas/RH-397-result.schema.json"
                and schema.get("title") == "RH-397 exact Stage-1 result"
                and same(schema, expected_schema)
                and same(payload, expected_payload)
            )
        except (
            ArithmeticError, AttributeError, KeyError, TypeError, ValueError,
            RuntimeError, IndexError, OverflowError,
        ):
            return False

    def verifier(
        schema: object, payload: object, *, compare_fresh: bool = True,
    ) -> bool:
        if type(compare_fresh) is not bool:
            return False
        if not semantic(schema, payload):
            return False
        if not compare_fresh:
            return True
        try:
            return same(
                schema, captured_builder(compare_fresh_result=False)
            )
        except (
            ArithmeticError, AttributeError, KeyError, TypeError, ValueError,
            RuntimeError, IndexError,
        ):
            return False

    return verifier


validate_schema_artifact = make_schema_validator(exact_schema, build_schema)


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
        "result_hash": lambda: changed_payload.__setitem__("paper", "RH-397-mutated"),
        "schema_bytes": lambda: changed_schema.__setitem__("x-schema-bytes", 257467),
        "schema_hash": lambda: changed_schema.__setitem__("x-schema-sha256", "0" * 64),
        "root_open": lambda: changed_schema.__setitem__("additionalProperties", True),
        "nested_object_open": lambda: properties["summary"].__setitem__("additionalProperties", True),
        "required_missing": lambda: changed_schema["required"].pop(),
        "required_extra": lambda: changed_schema["required"].append("extra"),
        "required_unsorted": lambda: changed_schema["required"].reverse(),
        "array_items_open": lambda: properties["result_mutation_names"].__setitem__("items", {}),
        "array_min_float": lambda: properties["core_mutation_audit"].__setitem__("minItems", 60.0),
        "array_min_bool": lambda: properties["core_mutation_audit"].__setitem__("minItems", True),
        "array_max_wrong": lambda: properties["core_mutation_audit"].__setitem__("maxItems", 61),
        "prefix_drop": lambda: properties["core_mutation_audit"].pop("prefixItems"),
        "prefix_reverse": lambda: properties["core_mutation_audit"]["prefixItems"].reverse(),
        "primitive_const": lambda: properties["paper"].__setitem__("const", "RH-396"),
        "primitive_type": lambda: properties["schema_version"].__setitem__("type", "number"),
        "bool_as_integer": lambda: properties["all_pass"].update({"type": "integer", "const": 1}),
        "certificate_rows_open": lambda: properties["certificate"]["properties"]["rows"].__setitem__("items", {}),
        "core_audit_items_open": lambda: properties["core_mutation_audit"].__setitem__("items", {}),
        "source_entries_open": lambda: properties["source_closure"]["properties"]["git"]["properties"]["entries"].__setitem__("items", {}),
        "theorem_nested_open": lambda: properties["theorem_contracts"]["properties"]["model_and_quantifiers"].__setitem__("additionalProperties", True),
        "forbidden_nested_open": lambda: properties["forbidden"].__setitem__("additionalProperties", True),
        "mutation_order_open": lambda: properties["result_mutation_names"]["prefixItems"].reverse(),
        "payload_extra": lambda: changed_payload.__setitem__("extra", 0),
        "payload_type": lambda: changed_payload.__setitem__("schema_version", 1.0),
        "payload_list_order": lambda: changed_payload["result_mutation_names"].reverse(),
        "official_draft_claim": lambda: changed_schema.__setitem__("$schema", "https://json-schema.org/draft/2019-09/schema"),
        "factory_rebind": lambda: changed_schema.__setitem__("x-factory-rebind", True),
        "compiler_rebind": lambda: changed_schema.__setitem__("x-compiler-rebind", True),
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
