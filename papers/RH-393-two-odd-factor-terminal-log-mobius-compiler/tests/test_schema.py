from __future__ import annotations

from copy import deepcopy
import importlib.util

import pytest

import build_result
import build_schema as schema_layer
import two_odd_compiler.core as core


def require(condition: bool, message: str = "test requirement failed") -> None:
    if condition is not True:
        raise AssertionError(message)


@pytest.fixture(scope="module")
def payload() -> dict[str, object]:
    return build_result.build_payload()


@pytest.fixture(scope="module")
def schema() -> dict[str, object]:
    return schema_layer.build_schema()


def must_reject(instance: object, schema: object) -> None:
    with pytest.raises(ValueError):
        schema_layer.validate_exact_instance(instance, schema)


def schema_counts(schema: dict[str, object]) -> dict[str, int]:
    counts = {
        "object": 0, "array": 0, "boolean": 0, "integer": 0,
        "string": 0, "null": 0, "nodes": 0,
    }

    def visit(node: object, *, root: bool = False) -> None:
        if type(node) is not dict or type(node.get("type")) is not str:
            raise AssertionError("untyped schema node")
        kind = node["type"]
        counts[kind] += 1
        counts["nodes"] += 1
        if kind == "object":
            expected = {"type", "properties", "required", "additionalProperties"}
            if root:
                expected |= {"$schema", "$id", "title"}
            require(set(node) == expected)
            require(node["additionalProperties"] is False)
            require(node["required"] == sorted(node["properties"]))
            for child in node["properties"].values():
                visit(child)
        elif kind == "array":
            expected = {"type", "items", "minItems", "maxItems"}
            if "prefixItems" in node:
                expected.add("prefixItems")
            prefix = node.get("prefixItems", [])
            require(set(node) == expected)
            require(node["items"] is False)
            require(len(prefix) == node["minItems"] == node["maxItems"])
            for child in prefix:
                visit(child)
        elif kind in {"boolean", "integer", "string", "null"}:
            require(set(node) == {"type", "const"})
        else:
            raise AssertionError("unsupported schema node")

    visit(schema, root=True)
    return counts


def test_stored_schema_is_strict_fresh_and_byte_identical(schema: dict[str, object]) -> None:
    raw = schema_layer.OUTPUT.read_bytes()
    stored = core.loads_strict(raw.decode("utf-8"))
    require(core.exact_equal(stored, schema))
    require(raw == build_result.pretty_json_bytes(schema))
    require(schema["$schema"] == schema_layer.SCHEMA_DRAFT)
    require(schema["$id"] == schema_layer.SCHEMA_ID)
    require(schema["title"] == schema_layer.SCHEMA_TITLE)


def test_every_schema_node_is_recursively_closed(schema: dict[str, object]) -> None:
    require(schema_counts(schema) == {
        "object": 794, "array": 837, "boolean": 1729,
        "integer": 5099, "string": 832, "null": 0, "nodes": 9291,
    })


def test_independent_evaluator_accepts_exact_instance(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    schema_layer.validate_exact_instance(payload, schema)


def test_independent_evaluator_calls_no_builder(
    payload: dict[str, object], schema: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("schema/result builder was called")

    monkeypatch.setattr(schema_layer, "exact_schema", forbidden)
    monkeypatch.setattr(schema_layer, "build_schema", forbidden)
    monkeypatch.setattr(schema_layer, "build_payload", forbidden)
    schema_layer.validate_exact_instance(deepcopy(payload), deepcopy(schema))


def test_schema_identity_constants_cannot_be_coordinately_rebound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    attacks = (
        ("SCHEMA_DRAFT", "https://example.invalid/draft"),
        ("SCHEMA_ID", "https://example.invalid/wrong.schema.json"),
        ("SCHEMA_TITLE", "wrong title"),
    )
    for name, value in attacks:
        monkeypatch.setattr(schema_layer, name, value)
        with pytest.raises(ValueError, match="schema identity"):
            schema_layer.build_schema()
        monkeypatch.undo()


def test_saved_evaluator_recurses_without_module_helpers(
    payload: dict[str, object], schema: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = schema_layer.validate_exact_instance
    corrupt = deepcopy(payload)
    corrupt["theorems"]["two_odd_factor_compiler"]["limit"] = "0"
    monkeypatch.setattr(schema_layer, "validate_exact_instance", lambda *_args: None)
    monkeypatch.setattr(schema_layer, "_require_keys", lambda *_args: {})
    with pytest.raises(ValueError):
        original(corrupt, deepcopy(schema))


def test_official_draft202012_when_available_without_skip(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    schema_layer.validate_exact_instance(payload, schema)
    if importlib.util.find_spec("jsonschema") is not None:
        import jsonschema

        jsonschema.Draft202012Validator.check_schema(schema)
        require(list(jsonschema.Draft202012Validator(schema).iter_errors(payload)) == [])


def test_instance_extra_missing_scalar_and_type_attacks_fail(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    extra = deepcopy(payload)
    extra["extra"] = False
    must_reject(extra, schema)
    missing = deepcopy(payload)
    del missing["theorems"]["phase_density"]
    must_reject(missing, schema)
    changed = deepcopy(payload)
    changed["theorems"]["two_odd_factor_compiler"]["limit"] = "0"
    must_reject(changed, schema)
    bool_int = deepcopy(payload)
    bool_int["mutations"]["count"] = True
    must_reject(bool_int, schema)
    int_bool = deepcopy(payload)
    int_bool["all_pass"] = 1
    must_reject(int_bool, schema)
    float_int = deepcopy(payload)
    float_int["source_locks"]["logical_count"] = 120.0
    must_reject(float_int, schema)


def test_fixed_array_order_length_and_leaf_attacks_fail(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    reordered = deepcopy(payload)
    reordered["mutations"]["names"].reverse()
    must_reject(reordered, schema)
    truncated = deepcopy(payload)
    truncated["certificate"]["truth_rows"].pop()
    must_reject(truncated, schema)
    extended = deepcopy(payload)
    extended["source_locks"]["remote"]["objects"].append({})
    must_reject(extended, schema)
    extra_nested = deepcopy(payload)
    extra_nested["certificate"]["landscape_rows"][0]["extra"] = 0
    must_reject(extra_nested, schema)


def test_schema_opening_rebinding_and_keyword_attacks_fail(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    open_root = deepcopy(schema)
    open_root["additionalProperties"] = True
    must_reject(payload, open_root)
    open_nested = deepcopy(schema)
    open_nested["properties"]["theorems"]["additionalProperties"] = True
    must_reject(payload, open_nested)
    open_array = deepcopy(schema)
    open_array["properties"]["certificate"]["properties"]["truth_rows"]["items"] = {}
    must_reject(payload, open_array)
    missing_prefix = deepcopy(schema)
    del missing_prefix["properties"]["mutations"]["properties"]["names"]["prefixItems"]
    must_reject(payload, missing_prefix)
    bool_length = deepcopy(schema)
    bool_length["properties"]["mutations"]["properties"]["names"]["minItems"] = True
    must_reject(payload, bool_length)
    rebound_leaf = deepcopy(schema)
    rebound_leaf["properties"]["title"]["const"] = "wrong title"
    must_reject(payload, rebound_leaf)
    extra_keyword = deepcopy(schema)
    extra_keyword["unevaluatedProperties"] = False
    must_reject(payload, extra_keyword)
    wrong_id = deepcopy(schema)
    wrong_id["$id"] = "https://example.invalid/schemas/other.json"
    must_reject(payload, wrong_id)


def test_exact_schema_strict_primitive_and_key_guards() -> None:
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


def test_schema_identity_rebinding_fails(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    changed = deepcopy(schema)
    changed["title"] = "RH-392"
    must_reject(payload, changed)
