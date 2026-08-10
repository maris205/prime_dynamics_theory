from __future__ import annotations

from copy import deepcopy
import importlib.util

import pytest

import build_result
import build_schema as schema_layer
import fixed_lag_capacity.core as core


@pytest.fixture(scope="module")
def payload() -> dict[str, object]:
    return build_result.build_payload()


@pytest.fixture(scope="module")
def schema() -> dict[str, object]:
    return schema_layer.build_schema()


def _must_reject(instance: object, schema: object) -> None:
    with pytest.raises(ValueError):
        schema_layer.validate_exact_instance(instance, schema)


def _schema_counts(schema: dict[str, object]) -> dict[str, int]:
    counts = {"object": 0, "array": 0, "boolean": 0, "integer": 0, "string": 0, "null": 0, "nodes": 0}

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
            if set(node) != expected or node["additionalProperties"] is not False:
                raise AssertionError("open or malformed object schema")
            if node["required"] != sorted(node["properties"]):
                raise AssertionError("object required membership drift")
            for child in node["properties"].values():
                visit(child)
        elif kind == "array":
            expected = {"type", "items", "minItems", "maxItems"}
            if "prefixItems" in node:
                expected.add("prefixItems")
            prefix = node.get("prefixItems", [])
            if set(node) != expected or node["items"] is not False or len(prefix) != node["minItems"] or node["minItems"] != node["maxItems"]:
                raise AssertionError("open or malformed array schema")
            for child in prefix:
                visit(child)
        elif kind in {"boolean", "integer", "string", "null"}:
            if set(node) != {"type", "const"}:
                raise AssertionError("unsealed scalar schema")
        else:
            raise AssertionError("unsupported schema node")

    visit(schema, root=True)
    return counts


def test_stored_schema_is_strict_fresh_and_byte_identical(schema: dict[str, object]) -> None:
    raw = schema_layer.OUTPUT.read_bytes()
    stored = core.loads_strict(raw.decode("utf-8"))
    assert core.exact_equal(stored, schema)
    assert raw == build_result.pretty_json_bytes(schema)
    assert schema["$schema"] == schema_layer.SCHEMA_DRAFT
    assert schema["$id"] == schema_layer.SCHEMA_ID
    assert schema["title"] == schema_layer.SCHEMA_TITLE


def test_every_schema_node_is_recursively_closed(schema: dict[str, object]) -> None:
    assert _schema_counts(schema) == {
        "object": 856,
        "array": 1758,
        "boolean": 2660,
        "integer": 14365,
        "string": 2465,
        "null": 4,
        "nodes": 22108,
    }


def test_independent_evaluator_accepts_exact_instance(payload: dict[str, object], schema: dict[str, object]) -> None:
    schema_layer.validate_exact_instance(payload, schema)


def test_independent_evaluator_calls_no_builder(
    payload: dict[str, object], schema: dict[str, object], monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("schema or result builder was called")

    monkeypatch.setattr(schema_layer, "exact_schema", forbidden)
    monkeypatch.setattr(schema_layer, "build_schema", forbidden)
    monkeypatch.setattr(schema_layer, "build_payload", forbidden)
    schema_layer.validate_exact_instance(deepcopy(payload), deepcopy(schema))


def test_official_draft202012_when_available_without_skip(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    # The independent evaluator is mandatory in every environment.  An installed
    # official implementation is an additional gate, never a skipped test.
    schema_layer.validate_exact_instance(payload, schema)
    if importlib.util.find_spec("jsonschema") is not None:
        import jsonschema

        jsonschema.Draft202012Validator.check_schema(schema)
        assert list(jsonschema.Draft202012Validator(schema).iter_errors(payload)) == []


def test_instance_extra_missing_scalar_and_type_attacks_fail(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    extra = deepcopy(payload)
    extra["extra"] = False
    _must_reject(extra, schema)

    missing = deepcopy(payload)
    del missing["theorems"]["one_site_density"]
    _must_reject(missing, schema)

    changed = deepcopy(payload)
    changed["theorems"]["capacity"]["formula"] = "6/pi^2+kappa_h/2"
    _must_reject(changed, schema)

    bool_int = deepcopy(payload)
    bool_int["mutations"]["count"] = True
    _must_reject(bool_int, schema)

    int_bool = deepcopy(payload)
    int_bool["all_pass"] = 1
    _must_reject(int_bool, schema)

    float_int = deepcopy(payload)
    float_int["source_locks"]["logical_count"] = 109.0
    _must_reject(float_int, schema)


def test_instance_fixed_array_order_length_and_leaf_attacks_fail(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    reordered = deepcopy(payload)
    reordered["mutations"]["names"].reverse()
    _must_reject(reordered, schema)

    truncated = deepcopy(payload)
    truncated["certificate"]["truth_rows"].pop()
    _must_reject(truncated, schema)

    extended = deepcopy(payload)
    extended["source_locks"]["remote"]["objects"].append({})
    _must_reject(extended, schema)

    extra_nested = deepcopy(payload)
    extra_nested["certificate"]["landscape_rows"][0]["extra"] = 0
    _must_reject(extra_nested, schema)


def test_schema_opening_rebinding_and_keyword_attacks_fail(
    payload: dict[str, object], schema: dict[str, object],
) -> None:
    open_root = deepcopy(schema)
    open_root["additionalProperties"] = True
    _must_reject(payload, open_root)

    open_nested = deepcopy(schema)
    open_nested["properties"]["theorems"]["additionalProperties"] = True
    _must_reject(payload, open_nested)

    open_array = deepcopy(schema)
    open_array["properties"]["certificate"]["properties"]["truth_rows"]["items"] = {}
    _must_reject(payload, open_array)

    missing_prefix = deepcopy(schema)
    del missing_prefix["properties"]["mutations"]["properties"]["names"]["prefixItems"]
    _must_reject(payload, missing_prefix)

    bool_length = deepcopy(schema)
    bool_length["properties"]["mutations"]["properties"]["names"]["minItems"] = True
    _must_reject(payload, bool_length)

    rebound_leaf = deepcopy(schema)
    rebound_leaf["properties"]["title"]["const"] = "wrong title"
    _must_reject(payload, rebound_leaf)

    extra_keyword = deepcopy(schema)
    extra_keyword["unevaluatedProperties"] = False
    _must_reject(payload, extra_keyword)

    wrong_id = deepcopy(schema)
    wrong_id["$id"] = "https://example.invalid/schemas/other.json"
    _must_reject(payload, wrong_id)


def test_exact_schema_strict_primitive_and_key_guards() -> None:
    assert schema_layer.exact_schema(True) == {"type": "boolean", "const": True}
    assert schema_layer.exact_schema(1) == {"type": "integer", "const": 1}
    assert schema_layer.exact_schema(None) == {"type": "null", "const": None}
    assert schema_layer.exact_schema([]) == {
        "type": "array", "items": False, "minItems": 0, "maxItems": 0,
    }
    with pytest.raises(TypeError, match="unsupported schema primitive"):
        schema_layer.exact_schema(1.5)
    with pytest.raises(TypeError, match="keys must be strings"):
        schema_layer.exact_schema({1: "bad"})
    with pytest.raises(TypeError, match="path"):
        schema_layer.validate_exact_instance({}, {}, path=1)
