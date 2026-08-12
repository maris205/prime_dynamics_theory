from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
import subprocess
from pathlib import Path

import pytest

import build_schema as schema_builder


EXPECTED_NODE_COUNTS = {
    "object": 568,
    "array": 140,
    "boolean": 518,
    "integer": 420,
    "string": 1838,
    "null": 0,
}


def require(condition: object, message: str = "requirement failed") -> None:
    if condition is not True:
        raise RuntimeError(message)


@pytest.fixture(scope="module")
def payload() -> dict[str, object]:
    return schema_builder._frozen_payload(compare_fresh=False)


@pytest.fixture(scope="module")
def schema() -> dict[str, object]:
    value = schema_builder.loads_strict(
        schema_builder.OUTPUT.read_text(encoding="utf-8")
    )
    require(type(value) is dict)
    return value


def test_runtime_require_survives_optimized_mode() -> None:
    with pytest.raises(RuntimeError):
        require(False, "optimized sentinel")


def test_frozen_result_and_schema_identities(
    schema: dict[str, object], payload: dict[str, object],
) -> None:
    result_raw = (schema_builder.ROOT / "results" / "result.json").read_bytes()
    result_canonical = schema_builder.canonical_bytes(payload)
    require(len(result_raw) == 151768)
    require(sha256(result_raw).hexdigest() == "d21f3ab160c7cb5cfca1ff04ac7d2104ea8a7802b36eb3e2f07e32cbe1d27e4f")
    require(len(result_canonical) == 105495)
    require(sha256(result_canonical).hexdigest() == "d2445cc883371ccfd96eeb09f908d62d232fcb5cde5ea9170aa2029956047c2a")
    schema_raw = schema_builder.OUTPUT.read_bytes()
    schema_canonical = schema_builder.canonical_bytes(schema)
    require(len(schema_raw) == schema_builder.SCHEMA_PRETTY_BYTES == 670920)
    require(sha256(schema_raw).hexdigest() == schema_builder.SCHEMA_PRETTY_SHA256 == "4f16580a613e3e0c3930fd53e3a418023fac96e2cfa15f74ed447a60bea38f83")
    require(len(schema_canonical) == schema_builder.SCHEMA_FIXTURE_BYTES == 257468)
    require(sha256(schema_canonical).hexdigest() == schema_builder.SCHEMA_FIXTURE_SHA256 == "c3a5b2a02b027cc18b67e63b32f0a238990a4754fe4f2f2ce3c8d1acf756b910")


def test_recursive_exact_closure_and_node_counts(
    schema: dict[str, object], payload: dict[str, object],
) -> None:
    require(schema["$schema"] == "https://json-schema.org/draft/2020-12/schema")
    require(schema["$id"] == "https://example.invalid/schemas/RH-397-result.schema.json")
    require(schema["title"] == "RH-397 exact Stage-1 result")
    schema_builder.validate_exact_instance(payload, schema)
    counts = {key: 0 for key in EXPECTED_NODE_COUNTS}

    def walk(node: object) -> None:
        require(type(node) is dict)
        kind = node["type"]
        require(type(kind) is str and kind in counts)
        counts[kind] += 1
        if kind == "object":
            require(node["additionalProperties"] is False)
            require(node["required"] == sorted(node["properties"]))
            require(set(node["required"]) == set(node["properties"]))
            for child in node["properties"].values():
                walk(child)
        elif kind == "array":
            require(node["items"] is False)
            require(type(node["minItems"]) is int)
            require(type(node["maxItems"]) is int)
            require(node["minItems"] == node["maxItems"])
            require(len(node.get("prefixItems", [])) == node["minItems"])
            for child in node.get("prefixItems", []):
                walk(child)
        else:
            require(set(node) == {"type", "const"})

    walk(schema)
    require(counts == EXPECTED_NODE_COUNTS)
    require(sum(counts.values()) == 3484)


def test_independent_and_fresh_validation(
    schema: dict[str, object], payload: dict[str, object],
) -> None:
    require(schema_builder.validate_schema_artifact(schema, payload, compare_fresh=False) is True)
    require(schema_builder.validate_schema_artifact(schema, payload, compare_fresh=True) is True)
    fresh = schema_builder.build_schema(compare_fresh_result=True)
    require(schema_builder.exact_equal(fresh, schema) is True)


def test_official_draft202012_validation(
    schema: dict[str, object], payload: dict[str, object],
) -> None:
    status = schema_builder.official_validation_status(payload, schema)
    require(status["draft"] == "2020-12")
    if status["available"] is True:
        require(status["schema_valid"] is True)
        require(status["instance_valid"] is True)
    else:
        require(status == {
            "available": False,
            "draft": "2020-12",
            "schema_valid": None,
            "instance_valid": None,
        })
    script = (
        "import importlib.metadata,json,sys;"
        "from jsonschema import Draft202012Validator as V;"
        "p=json.load(open(sys.argv[1],encoding='utf-8'));"
        "s=json.load(open(sys.argv[2],encoding='utf-8'));"
        "V.check_schema(s);"
        "print(importlib.metadata.version('jsonschema'),len(list(V(s).iter_errors(p))))"
    )
    completed = subprocess.run(
        [
            "/usr/bin/python3", "-B", "-c", script,
            str(schema_builder.ROOT / "results" / "result.json"),
            str(schema_builder.OUTPUT),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    require(completed.stdout.strip() == "4.26.0 0")


def test_all_32_mutations_are_distinct_and_rejected(
    schema: dict[str, object], payload: dict[str, object],
) -> None:
    require(len(schema_builder.SCHEMA_MUTATION_NAMES) == 32)
    require(len(set(schema_builder.SCHEMA_MUTATION_NAMES)) == 32)
    digests: list[str] = []
    for name in schema_builder.SCHEMA_MUTATION_NAMES:
        changed_schema, changed_payload = schema_builder.mutate_schema(
            schema, payload, name
        )
        require(
            schema_builder.validate_schema_artifact(
                changed_schema, changed_payload, compare_fresh=False
            ) is False,
            name,
        )
        digests.append(sha256(schema_builder.canonical_bytes(
            [changed_schema, changed_payload]
        )).hexdigest())
    require(len(set(digests)) == 32)
    with pytest.raises(ValueError):
        schema_builder.mutate_schema(schema, payload, "not_a_mutation")


def test_local_evaluator_rejects_open_shapes_types_and_order(
    schema: dict[str, object], payload: dict[str, object],
) -> None:
    attacks: list[tuple[dict[str, object], dict[str, object]]] = []
    changed = deepcopy(payload)
    changed["schema_version"] = True
    attacks.append((schema, changed))
    changed_schema = deepcopy(schema)
    changed_schema["properties"]["summary"]["additionalProperties"] = True
    attacks.append((changed_schema, payload))
    changed_schema = deepcopy(schema)
    changed_schema["properties"]["core_mutation_audit"]["minItems"] = 60.0
    attacks.append((changed_schema, payload))
    changed_schema = deepcopy(schema)
    changed_schema["properties"]["result_mutation_names"]["prefixItems"].reverse()
    attacks.append((changed_schema, payload))
    changed_schema = deepcopy(schema)
    changed_schema["required"].reverse()
    attacks.append((changed_schema, payload))
    for changed_schema, changed_payload in attacks:
        with pytest.raises(ValueError):
            schema_builder.validate_exact_instance(changed_payload, changed_schema)


def test_false_path_uses_no_rebindable_global(
    schema: dict[str, object], payload: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def bomb(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("forbidden global called")

    for name in schema_builder.SCHEMA_BUILDER_NAMES + schema_builder.SCHEMA_HELPER_NAMES:
        monkeypatch.setattr(schema_builder, name, bomb)
    for name in (
        "sha256", "json", "deepcopy", "SCHEMA_DRAFT", "SCHEMA_ID",
        "SCHEMA_TITLE", "SCHEMA_FIXTURE_BYTES", "SCHEMA_FIXTURE_SHA256",
        "RESULT_CANONICAL_SHA256", "SCHEMA_MUTATION_NAMES",
    ):
        monkeypatch.setattr(schema_builder, name, bomb)
    require(schema_builder.validate_schema_artifact(schema, payload, compare_fresh=False) is True)
    changed = deepcopy(schema)
    changed["$id"] = "wrong"
    require(schema_builder.validate_schema_artifact(changed, payload, compare_fresh=False) is False)


def test_factory_rejects_poisoned_compiler_and_builder() -> None:
    def wrong_compiler(_payload: object) -> dict[str, object]:
        return {"type": "object"}

    def wrong_builder(*, compare_fresh_result: bool = False) -> dict[str, object]:
        del compare_fresh_result
        return {"type": "object"}

    with pytest.raises((RuntimeError, TypeError, ValueError)):
        schema_builder.make_schema_validator(wrong_compiler, schema_builder.build_schema)
    with pytest.raises((RuntimeError, TypeError, ValueError)):
        schema_builder.make_schema_validator(schema_builder.exact_schema, wrong_builder)
    with pytest.raises(TypeError):
        schema_builder.make_schema_validator(None, schema_builder.build_schema)

    payload = schema_builder._frozen_payload(compare_fresh=False)

    def reordered_compiler(value: object) -> dict[str, object]:
        compiled = schema_builder.exact_schema(value)
        nested = compiled["properties"]["summary"]["properties"]
        compiled["properties"]["summary"]["properties"] = dict(
            reversed(tuple(nested.items()))
        )
        return compiled

    def reordered_builder(*, compare_fresh_result: bool = False) -> dict[str, object]:
        del compare_fresh_result
        compiled = reordered_compiler(payload)
        compiled["$schema"] = schema_builder.SCHEMA_DRAFT
        compiled["$id"] = schema_builder.SCHEMA_ID
        compiled["title"] = schema_builder.SCHEMA_TITLE
        return compiled

    with pytest.raises((RuntimeError, TypeError, ValueError)):
        schema_builder.make_schema_validator(reordered_compiler, reordered_builder)

    def tuple_compiler(value: object) -> dict[str, object]:
        compiled = schema_builder.exact_schema(value)
        compiled["properties"]["result_mutation_names"]["prefixItems"] = tuple(
            compiled["properties"]["result_mutation_names"]["prefixItems"]
        )
        return compiled

    def tuple_builder(*, compare_fresh_result: bool = False) -> dict[str, object]:
        del compare_fresh_result
        compiled = tuple_compiler(payload)
        compiled["$schema"] = schema_builder.SCHEMA_DRAFT
        compiled["$id"] = schema_builder.SCHEMA_ID
        compiled["title"] = schema_builder.SCHEMA_TITLE
        return compiled

    with pytest.raises((RuntimeError, TypeError, ValueError)):
        schema_builder.make_schema_validator(tuple_compiler, tuple_builder)


def test_strict_json_ast_and_factory_surface() -> None:
    require(schema_builder.loads_strict('{"a":1}') == {"a": 1})
    with pytest.raises(ValueError):
        schema_builder.loads_strict('{"a":1,"a":2}')
    with pytest.raises(ValueError):
        schema_builder.loads_strict('{"a":NaN}')
    package_root = Path(__file__).resolve().parents[1]
    for path in (Path(__file__), package_root / "experiments" / "build_schema.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue
            keys = [
                key.value for key in node.keys
                if isinstance(key, ast.Constant) and type(key.value) is str
            ]
            require(len(keys) == len(set(keys)), f"duplicate dict key in {path.name}")
