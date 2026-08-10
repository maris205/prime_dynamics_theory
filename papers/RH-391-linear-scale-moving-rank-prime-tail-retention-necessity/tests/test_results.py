from __future__ import annotations

from copy import deepcopy
import importlib.util
import json

import pytest

import build_result
from build_result import build_payload, pretty_json_bytes
from build_schema import build_schema, exact_schema
from moving_rank_necessity import loads_strict


def _validate_exact_instance(instance: object, schema: dict[str, object], path: str = "$") -> None:
    kind = schema.get("type")
    if kind == "object":
        if type(instance) is not dict:
            raise ValueError(f"{path}: object required")
        properties = schema["properties"]
        required = schema["required"]
        if set(instance) != set(properties) or sorted(instance) != required or schema["additionalProperties"] is not False:
            raise ValueError(f"{path}: object membership changed")
        for key in required:
            _validate_exact_instance(instance[key], properties[key], f"{path}.{key}")
        return
    if kind == "array":
        if type(instance) is not list or len(instance) != schema["minItems"] or len(instance) != schema["maxItems"]:
            raise ValueError(f"{path}: fixed array changed")
        items = schema.get("prefixItems", [])
        if schema["items"] is not False or len(items) != len(instance):
            raise ValueError(f"{path}: array closure changed")
        for index, (item, item_schema) in enumerate(zip(instance, items)):
            _validate_exact_instance(item, item_schema, f"{path}[{index}]")
        return
    exact_types = {"boolean": bool, "integer": int, "string": str, "null": type(None)}
    if kind not in exact_types or type(instance) is not exact_types[kind] or instance != schema.get("const"):
        raise ValueError(f"{path}: exact scalar changed")


def _official_validate_if_available(instance: object, schema: dict[str, object]) -> None:
    if importlib.util.find_spec("jsonschema") is None:
        return
    import jsonschema
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(schema).validate(instance)


def _stored(name: str) -> dict[str, object]:
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    return loads_strict((root / "results" / name).read_text(encoding="utf-8"))


def test_stored_result_is_exact_fresh_payload() -> None:
    stored = _stored("result.json")
    fresh = build_payload()
    assert stored == fresh
    assert pretty_json_bytes(fresh) == (json.dumps(stored, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def test_top_level_status_and_all_pass() -> None:
    payload = build_payload()
    assert payload["paper"] == "RH-391"
    assert payload["status"] == "RH-391_linear_scale_moving_rank_prime_tail_retention_necessity_certified"
    assert payload["all_pass"] is True


def test_certificate_and_mutation_fixture() -> None:
    payload = build_payload()
    assert payload["certificate_fixture"] == {
        "canonical_bytes": 10_062,
        "sha256": "cc2874435e62205a3e969e841d80d37243d95826855bd242f0eff3478dccf367",
        "pass": True,
    }
    assert payload["mutations"]["count"] == 24
    assert payload["mutations"]["all_pass"] is True


def test_source_closure_is_97_plus_2() -> None:
    locks = build_payload()["source_locks"]
    assert (locks["git_count"], locks["remote_count"], locks["logical_count"]) == (97, 2, 99)
    assert locks["pass"] is True


def test_theorem_separates_linear_and_optional_profile_regimes() -> None:
    theorem = build_payload()["theorem"]
    assert "r<=C*x" in theorem["linear_rank_regime"]
    assert "additionally" in theorem["optional_profile_regime"]
    assert theorem["lambda_pair_lower"].endswith("a0/(1+a0)")
    assert theorem["sublinear_pair_lower"].endswith("1/2")


def test_theorem_uses_same_rank_pair_and_fixed_h() -> None:
    theorem = build_payload()["theorem"]
    assert "fixed positive integer h_*<=600" in theorem["fixed_gap_extraction"]
    assert theorem["necessity_scope"] == "same rank at both endpoints; pairwise P/J/I hierarchy only"


def test_source_roles_do_not_use_jy_at_linear_rank() -> None:
    roles = build_payload()["source_roles"]
    assert "not invoked" in roles["johnston_yang"]
    assert roles["excluded_as_irrelevant"] == ["RH-389", "TPC-137", "Tao active-log source"]


def test_all_gates_and_forbidden_claims_remain_false() -> None:
    payload = build_payload()
    assert not any(payload["gates"].values())
    assert not any(payload["forbidden_claims"].values())


def test_forbidden_membership_deletion_and_addition_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    deleted = dict(build_result.FORBIDDEN)
    del deleted["arbitrary_surrogate_necessity"]
    monkeypatch.setattr(build_result, "FORBIDDEN", deleted)
    with pytest.raises(ValueError, match="membership"):
        build_result.build_payload()
    added = dict(deleted)
    added["arbitrary_surrogate_necessity"] = False
    added["new_unsealed_claim"] = False
    monkeypatch.setattr(build_result, "FORBIDDEN", added)
    with pytest.raises(ValueError, match="membership"):
        build_result.build_payload()


def test_declarations_are_exact_and_offline() -> None:
    declarations = build_payload()["declarations"]
    assert declarations["network_fetch_performed_by_build"] is False
    assert declarations["external_payload_vendored"] is False
    assert declarations["finite_rows_are_analytic_proof"] is False
    assert (declarations["git_source_rows"], declarations["remote_logical_objects"], declarations["logical_source_rows"]) == (97, 2, 99)


def test_stored_schema_is_exact_fresh_schema() -> None:
    assert _stored("result.schema.json") == build_schema()


def test_schema_is_closed_draft_2020_12() -> None:
    schema = build_schema()
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["$id"].endswith("RH-391-result.schema.json")
    assert schema["additionalProperties"] is False
    _official_validate_if_available(build_payload(), schema)


def test_schema_accepts_exact_payload() -> None:
    schema, payload = build_schema(), build_payload()
    _validate_exact_instance(payload, schema)
    _official_validate_if_available(payload, schema)


def test_schema_rejects_extra_missing_and_changed_leaf() -> None:
    schema = build_schema()
    extra = build_payload()
    extra["extra"] = False
    with pytest.raises(ValueError):
        _validate_exact_instance(extra, schema)
    missing = build_payload()
    del missing["theorem"]
    with pytest.raises(ValueError):
        _validate_exact_instance(missing, schema)
    changed = build_payload()
    changed["theorem"]["coarse_pair_lower"] += "#"
    with pytest.raises(ValueError):
        _validate_exact_instance(changed, schema)


def test_schema_rejects_bool_int_confusion() -> None:
    payload = build_payload()
    payload["mutations"]["count"] = True
    with pytest.raises(ValueError):
        _validate_exact_instance(payload, build_schema())


def test_schema_rejects_reordered_or_truncated_fixed_arrays() -> None:
    schema = build_schema()
    reordered = build_payload()
    reordered["source_roles"]["excluded_as_irrelevant"].reverse()
    with pytest.raises(ValueError):
        _validate_exact_instance(reordered, schema)
    truncated = build_payload()
    truncated["gates"].pop("E_completed_zeta_divisor_equality")
    with pytest.raises(ValueError):
        _validate_exact_instance(truncated, schema)


def test_exact_schema_rejects_unsupported_float() -> None:
    with pytest.raises(TypeError, match="unsupported schema primitive"):
        exact_schema(1.5)


def test_stored_result_strict_loader_has_no_duplicate_or_nonfinite_values() -> None:
    stored = _stored("result.json")
    assert json.dumps(stored, allow_nan=False)
    with pytest.raises(ValueError):
        loads_strict('{"status":"a","status":"b"}')
