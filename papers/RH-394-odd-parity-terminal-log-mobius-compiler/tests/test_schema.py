from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import importlib.util
from pathlib import Path

import pytest

import build_result
import build_schema as schema_layer


def require(condition: object, message: str = "requirement failed") -> None:
    if condition is not True:
        raise RuntimeError(message)


def must_reject(instance: object, schema: object) -> None:
    with pytest.raises(ValueError):
        schema_layer.validate_exact_instance(instance, schema)


@pytest.fixture(scope="module")
def payload() -> dict[str, object]:
    return schema_layer._frozen_payload()


@pytest.fixture(scope="module")
def schema() -> dict[str, object]:
    return schema_layer.build_schema()


def schema_counts(schema: dict[str, object]) -> dict[str, int]:
    counts = {
        "object": 0,
        "array": 0,
        "boolean": 0,
        "integer": 0,
        "string": 0,
        "null": 0,
        "nodes": 0,
    }

    def visit(node: object, *, root: bool = False) -> None:
        if type(node) is not dict or type(node.get("type")) is not str:
            raise RuntimeError("untyped schema node")
        kind = node["type"]
        counts[kind] += 1
        counts["nodes"] += 1
        if kind == "object":
            keywords = {"type", "properties", "required", "additionalProperties"}
            if root:
                keywords |= {"$schema", "$id", "title"}
            require(set(node) == keywords)
            require(node["additionalProperties"] is False)
            require(node["required"] == sorted(node["properties"]))
            for child in node["properties"].values():
                visit(child)
        elif kind == "array":
            keywords = {"type", "items", "minItems", "maxItems"}
            if "prefixItems" in node:
                keywords.add("prefixItems")
            prefix = node.get("prefixItems", [])
            require(set(node) == keywords)
            require(node["items"] is False)
            require(len(prefix) == node["minItems"] == node["maxItems"])
            for child in prefix:
                visit(child)
        elif kind in {"boolean", "integer", "string", "null"}:
            require(set(node) == {"type", "const"})
        else:
            raise RuntimeError("unsupported schema node")

    visit(schema, root=True)
    return counts


def test_runtime_require_survives_optimized_mode() -> None:
    with pytest.raises(RuntimeError, match="optimized sentinel"):
        require(False, "optimized sentinel")


def test_stored_schema_is_fresh_strict_and_byte_exact(
    schema: dict[str, object],
) -> None:
    raw = schema_layer.OUTPUT.read_bytes()
    stored = build_result.loads_strict(raw.decode("utf-8"))
    require(build_result.exact_equal(stored, schema))
    require(raw == build_result.pretty_json_bytes(schema))
    require(hashlib.sha256(raw).hexdigest() == (
        "8129ae146b30ca617e8536c15101eee6e12965ac9a87a6c41be9eb472cf16cb3"
    ))
    require(schema["$schema"] == "https://json-schema.org/draft/2020-12/schema")
    require(schema["$id"] == "https://example.invalid/schemas/RH-394-result.schema.json")
    require(schema["title"] == "RH-394 exact Stage-1 result")


def test_schema_result_input_seals(payload: dict[str, object]) -> None:
    require(hashlib.sha256(
        (schema_layer.ROOT / "experiments" / "build_result.py").read_bytes()
    ).hexdigest() == schema_layer.RESULT_BUILDER_SHA256)
    require(hashlib.sha256(
        (schema_layer.ROOT / "results" / "result.json").read_bytes()
    ).hexdigest() == schema_layer.RESULT_PRETTY_SHA256)
    raw = build_result.canonical_bytes(payload)
    require(len(raw) == 166_133)
    require(hashlib.sha256(raw).hexdigest() == (
        "9b69b6b8ec00d0bf7191deadef9fd7cf9005b092988cde96fa2d858029200f3a"
    ))


def test_every_node_is_recursively_closed(schema: dict[str, object]) -> None:
    require(schema_counts(schema) == {
        "object": 876,
        "array": 152,
        "boolean": 755,
        "integer": 4008,
        "string": 1021,
        "null": 3,
        "nodes": 6815,
    })


def test_independent_evaluator_accepts_exact_instance(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    schema_layer.validate_exact_instance(payload, schema)


def test_independent_evaluator_calls_no_builder(
    payload: dict[str, object], schema: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = schema_layer.validate_exact_instance

    def bomb(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("builder/helper invoked by evaluator")

    for name in (
        "exact_schema", "build_schema", "build_payload", "_frozen_payload",
        "validate_result_payload", "canonical_bytes", "loads_strict",
    ):
        monkeypatch.setattr(schema_layer, name, bomb)
    original(deepcopy(payload), deepcopy(schema))


def test_identity_and_result_seals_cannot_be_rebound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    attacks = (
        ("SCHEMA_DRAFT", "https://example.invalid/draft"),
        ("SCHEMA_ID", "https://example.invalid/wrong.schema.json"),
        ("SCHEMA_TITLE", "wrong"),
        ("RESULT_BUILDER_SHA256", "0" * 64),
        ("RESULT_PRETTY_SHA256", "1" * 64),
        ("RESULT_CANONICAL_BYTES", 166_132),
        ("RESULT_CANONICAL_SHA256", "2" * 64),
    )
    for name, value in attacks:
        monkeypatch.setattr(schema_layer, name, value)
        with pytest.raises(ValueError, match="identity/result seal"):
            schema_layer.build_schema()
        monkeypatch.undo()


def test_saved_evaluator_rejects_after_module_rebinding(
    payload: dict[str, object], schema: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = schema_layer.validate_exact_instance
    corrupt = deepcopy(payload)
    corrupt["theorems"]["odd_parity_compiler"]["limit"] = "0"
    monkeypatch.setattr(schema_layer, "validate_exact_instance", lambda *_args: None)
    monkeypatch.setattr(schema_layer, "exact_schema", lambda *_args: {})
    with pytest.raises(ValueError):
        original(corrupt, deepcopy(schema))


def test_official_draft_2020_12_contract(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    require(schema["$schema"] == "https://json-schema.org/draft/2020-12/schema")
    schema_layer.validate_exact_instance(payload, schema)
    if importlib.util.find_spec("jsonschema") is not None:
        import jsonschema

        jsonschema.Draft202012Validator.check_schema(schema)
        require(list(jsonschema.Draft202012Validator(schema).iter_errors(payload)) == [])


def test_instance_membership_scalar_and_type_attacks_fail(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    attacks = []
    changed = deepcopy(payload)
    changed["extra"] = False
    attacks.append(changed)
    changed = deepcopy(payload)
    del changed["theorems"]["phase_density"]
    attacks.append(changed)
    changed = deepcopy(payload)
    changed["theorems"]["odd_parity_compiler"]["limit"] = "0"
    attacks.append(changed)
    changed = deepcopy(payload)
    changed["mutations"]["count"] = True
    attacks.append(changed)
    changed = deepcopy(payload)
    changed["all_pass"] = 1
    attacks.append(changed)
    changed = deepcopy(payload)
    changed["source_locks"]["logical_count"] = 132.0
    attacks.append(changed)
    changed = deepcopy(payload)
    changed["finite_contracts"]["signed_four_cube"]["eligible_corner_patterns"] = 12_870.0
    attacks.append(changed)
    for item in attacks:
        must_reject(item, schema)


def test_fixed_array_order_length_and_leaf_attacks_fail(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    changed = deepcopy(payload)
    changed["mutations"]["names"].reverse()
    must_reject(changed, schema)
    changed = deepcopy(payload)
    changed["certificate"]["current_table_rows"].pop()
    must_reject(changed, schema)
    changed = deepcopy(payload)
    changed["source_locks"]["remote"]["objects"].append({})
    must_reject(changed, schema)
    changed = deepcopy(payload)
    changed["certificate"]["dimension_rows"][0]["extra"] = 0
    must_reject(changed, schema)
    changed = deepcopy(payload)
    changed["finite_contracts"]["dimensions"]["m3"]["m"] = 99
    must_reject(changed, schema)


def test_schema_opening_keyword_and_identity_attacks_fail(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    changed = deepcopy(schema)
    changed["additionalProperties"] = True
    must_reject(payload, changed)
    changed = deepcopy(schema)
    changed["properties"]["theorems"]["additionalProperties"] = True
    must_reject(payload, changed)
    changed = deepcopy(schema)
    changed["properties"]["certificate"]["properties"]["current_table_rows"]["items"] = {}
    must_reject(payload, changed)
    changed = deepcopy(schema)
    del changed["properties"]["mutations"]["properties"]["names"]["prefixItems"]
    must_reject(payload, changed)
    changed = deepcopy(schema)
    changed["properties"]["mutations"]["properties"]["names"]["minItems"] = True
    must_reject(payload, changed)
    changed = deepcopy(schema)
    changed["properties"]["title"]["const"] = "wrong"
    must_reject(payload, changed)
    changed = deepcopy(schema)
    changed["unevaluatedProperties"] = False
    must_reject(payload, changed)
    changed = deepcopy(schema)
    changed["$id"] = "https://example.invalid/schemas/other.json"
    must_reject(payload, changed)


def test_exact_schema_primitive_key_and_path_guards() -> None:
    require(schema_layer.exact_schema(True) == {"type": "boolean", "const": True})
    require(schema_layer.exact_schema(1) == {"type": "integer", "const": 1})
    require(schema_layer.exact_schema(None) == {"type": "null", "const": None})
    require(schema_layer.exact_schema([]) == {
        "type": "array", "items": False, "minItems": 0, "maxItems": 0,
    })
    with pytest.raises(TypeError, match="unsupported schema primitive"):
        schema_layer.exact_schema(1.5)
    with pytest.raises(TypeError, match="keys must be strings"):
        schema_layer.exact_schema({1: "bad"})
    with pytest.raises(TypeError, match="path"):
        schema_layer.validate_exact_instance({}, {}, path=1)


def test_no_bare_asserts() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
