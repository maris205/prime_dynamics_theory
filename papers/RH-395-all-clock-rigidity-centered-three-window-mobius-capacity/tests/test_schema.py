from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

import pytest

import build_schema as schema_builder


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


def test_schema_pretty_and_canonical_fixtures(schema: dict[str, object]) -> None:
    pretty = schema_builder.OUTPUT.read_bytes()
    canonical = schema_builder.canonical_bytes(schema)
    require(len(pretty) == 678979)
    require(sha256(pretty).hexdigest() == "2eb368a88cc7e3363a3c4f216ea7d3efd423b4faf9bcdec003d36316b2bfe643")
    require(len(canonical) == schema_builder.SCHEMA_FIXTURE_BYTES == 265717)
    require(sha256(canonical).hexdigest() == schema_builder.SCHEMA_FIXTURE_SHA256 == "1958e593b29b5095efc15eb3a447db12236504d81f447bc6626fde75978d2849")


def test_exact_schema_identity_and_recursive_closure(
    schema: dict[str, object], payload: dict[str, object]
) -> None:
    require(schema["$schema"] == "https://json-schema.org/draft/2020-12/schema")
    require(schema["$id"] == "https://example.invalid/schemas/RH-395-result.schema.json")
    require(schema["title"] == "RH-395 exact Stage-1 result")
    schema_builder.validate_exact_instance(payload, schema)

    object_nodes = 0
    array_nodes = 0

    def walk(node: object) -> None:
        nonlocal object_nodes, array_nodes
        if type(node) is not dict:
            return
        if node.get("type") == "object":
            object_nodes += 1
            require(node["additionalProperties"] is False)
            require(node["required"] == sorted(node["properties"]))
            for child in node["properties"].values():
                walk(child)
        elif node.get("type") == "array":
            array_nodes += 1
            require(node["items"] is False)
            require(node["minItems"] == node["maxItems"])
            for child in node.get("prefixItems", []):
                walk(child)

    walk(schema)
    require(object_nodes > 100)
    require(array_nodes > 100)


def test_independent_false_and_fresh_schema_validation(
    schema: dict[str, object], payload: dict[str, object]
) -> None:
    require(schema_builder.validate_schema_artifact(schema, payload, compare_fresh=False) is True)
    require(schema_builder.validate_schema_artifact(schema, payload, compare_fresh=True) is True)


def test_fresh_schema_and_fresh_result_replay(schema: dict[str, object]) -> None:
    fresh = schema_builder.build_schema(compare_fresh_result=True)
    require(schema_builder.exact_equal(fresh, schema) is True)


def test_official_draft202012_validator_when_available(
    schema: dict[str, object], payload: dict[str, object]
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


def test_every_schema_or_payload_mutation_is_rejected(
    schema: dict[str, object], payload: dict[str, object]
) -> None:
    require(len(schema_builder.SCHEMA_MUTATION_NAMES) == 24)
    require(len(set(schema_builder.SCHEMA_MUTATION_NAMES)) == 24)
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


def test_local_evaluator_rejects_bool_int_and_open_shapes(
    schema: dict[str, object], payload: dict[str, object]
) -> None:
    attacks: list[tuple[dict[str, object], dict[str, object]]] = []
    changed_payload = deepcopy(payload)
    changed_payload["schema_version"] = True
    attacks.append((schema, changed_payload))
    changed_schema = deepcopy(schema)
    changed_schema["properties"]["summary"]["additionalProperties"] = True
    attacks.append((changed_schema, payload))
    changed_schema = deepcopy(schema)
    changed_schema["properties"]["result_mutation_names"]["items"] = {}
    attacks.append((changed_schema, payload))
    for changed_schema, changed_payload in attacks:
        with pytest.raises(ValueError):
            schema_builder.validate_exact_instance(changed_payload, changed_schema)


def test_false_mode_uses_no_global_builder_or_helper(
    schema: dict[str, object], payload: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def bomb(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("forbidden global called")

    for name in schema_builder.SCHEMA_BUILDER_NAMES + schema_builder.SCHEMA_HELPER_NAMES:
        monkeypatch.setattr(schema_builder, name, bomb)
    monkeypatch.setattr(schema_builder, "sha256", bomb)
    monkeypatch.setattr(schema_builder, "json", bomb)
    require(schema_builder.validate_schema_artifact(schema, payload, compare_fresh=False) is True)


def test_coordinated_schema_constant_rebinding_fails_closed(
    schema: dict[str, object], payload: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(schema_builder, "SCHEMA_DRAFT", "wrong")
    monkeypatch.setattr(schema_builder, "SCHEMA_ID", "wrong")
    monkeypatch.setattr(schema_builder, "SCHEMA_TITLE", "wrong")
    monkeypatch.setattr(schema_builder, "SCHEMA_FIXTURE_BYTES", 1)
    monkeypatch.setattr(schema_builder, "SCHEMA_FIXTURE_SHA256", "0" * 64)
    monkeypatch.setattr(schema_builder, "SCHEMA_MUTATION_NAMES", ("fake",))
    require(schema_builder.validate_schema_artifact(schema, payload, compare_fresh=False) is True)
    changed = deepcopy(schema)
    changed["$id"] = "wrong"
    require(schema_builder.validate_schema_artifact(changed, payload, compare_fresh=False) is False)


def test_no_bare_asserts_and_strict_json() -> None:
    require(schema_builder.loads_strict('{"a":1}') == {"a": 1})
    with pytest.raises(ValueError):
        schema_builder.loads_strict('{"a":1,"a":2}')
    package_root = Path(__file__).resolve().parents[1]
    for path in (Path(__file__), package_root / "experiments" / "build_schema.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
