import copy
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from experiments.build_result import (  # noqa: E402
    EXPECTED_ALL_SOURCE_DIGEST,
    EXPECTED_GROUP_DIGESTS,
    SOURCE_COMMITS,
    SOURCE_FILES,
    SOURCE_GROUPS,
    WORKSPACE,
    build_payload,
    build_source_locks,
    digest,
    lines_digest,
    load_json,
    serialized_payload,
    source_digest_lines,
)
from experiments.build_schema import build_schema, serialized_schema  # noqa: E402


def validate_exact_schema(value: object, schema: dict[str, object]) -> None:
    if "const" in schema and value != schema["const"]:
        raise ValueError("const mismatch")
    kind = schema.get("type")
    if kind == "object":
        if type(value) is not dict:
            raise TypeError("object type mismatch")
        properties = schema["properties"]
        if schema.get("additionalProperties") is not False or set(value) != set(properties):
            raise ValueError("object membership mismatch")
        for key, child in value.items():
            validate_exact_schema(child, properties[key])
    elif kind == "array":
        if type(value) is not list:
            raise TypeError("array type mismatch")
        if not schema.get("items") is False or len(value) != len(schema["prefixItems"]):
            raise ValueError("array membership mismatch")
        for child, child_schema in zip(value, schema["prefixItems"]):
            validate_exact_schema(child, child_schema)
    elif kind == "boolean" and type(value) is not bool:
        raise TypeError("boolean type mismatch")
    elif kind == "integer" and type(value) is not int:
        raise TypeError("integer type mismatch")
    elif kind == "string" and type(value) is not str:
        raise TypeError("string type mismatch")


def test_result_full_regeneration_and_33_release_blob_locks() -> None:
    stored = (ROOT / "results/result.json").read_text()
    regenerated = build_payload()
    assert serialized_payload(regenerated) == stored
    locks = build_source_locks()
    assert locks["count"] == len(SOURCE_FILES) == 33
    assert len(set(SOURCE_FILES)) == 33
    assert locks["group_digests"] == EXPECTED_GROUP_DIGESTS
    assert locks["all_source_digest"] == EXPECTED_ALL_SOURCE_DIGEST
    assert locks["release_blob_identity_pass"] and locks["digest_contract_pass"] and locks["pass"]
    for entry in locks["entries"]:
        assert entry["sha256"] == digest(WORKSPACE / entry["path"])
        assert "AGENTS.md" not in entry["path"] and "RH_HANDOFF.md" not in entry["path"]


def test_source_commit_membership_path_duplicate_and_digest_mutations_fail() -> None:
    bad_commits = dict(SOURCE_COMMITS)
    bad_commits["rh381_release"] = "0" * 40
    with pytest.raises(ValueError, match="commits were rebound"):
        build_source_locks(source_commits=bad_commits)
    bad_groups = copy.deepcopy(SOURCE_GROUPS)
    bad_groups["rh381_release"] = bad_groups["rh381_release"][:-1]
    with pytest.raises(ValueError, match="membership was rebound"):
        build_source_locks(source_groups=bad_groups)
    entries = build_source_locks()["entries"]
    unsafe = copy.deepcopy(entries)
    unsafe[0]["path"] = "prime_dynamics_theory/../RH_HANDOFF.md"
    with pytest.raises(ValueError, match="unsafe"):
        source_digest_lines(unsafe)
    duplicate = copy.deepcopy(entries)
    duplicate[-1] = copy.deepcopy(duplicate[0])
    with pytest.raises(ValueError, match="duplicates"):
        source_digest_lines(duplicate)
    mutated_lines = list(source_digest_lines(entries))
    mutated_lines[0] = mutated_lines[0][:-1] + ("0" if mutated_lines[0][-1] != "0" else "1")
    assert lines_digest(mutated_lines) != EXPECTED_ALL_SOURCE_DIGEST


def test_strict_json_loader_rejects_duplicate_nonfinite_and_nonobject(tmp_path: Path) -> None:
    candidates = {
        "duplicate": '{"x":1,"x":2}',
        "nan": '{"x":NaN}',
        "infinity": '{"x":Infinity}',
        "minus_infinity": '{"x":-Infinity}',
        "array": "[]",
    }
    for label, text in candidates.items():
        path = tmp_path / f"{label}.json"
        path.write_text(text)
        with pytest.raises(ValueError):
            load_json(path)


def test_schema_full_regeneration_is_recursively_closed_and_exact() -> None:
    stored_text = (ROOT / "results/result.schema.json").read_text()
    schema = build_schema()
    assert serialized_schema(schema) == stored_text
    payload = load_json(ROOT / "results/result.json")
    validate_exact_schema(payload, schema)

    def visit(node: object) -> None:
        if type(node) is not dict:
            return
        if node.get("type") == "object":
            assert node.get("additionalProperties") is False
            assert set(node["required"]) == set(node["properties"])
        if node.get("type") == "array":
            assert node.get("items") is False
            assert len(node["prefixItems"]) == node["minItems"] == node["maxItems"]
        for child in node.values():
            if type(child) is dict:
                visit(child)
            elif type(child) is list:
                for item in child:
                    visit(item)

    visit(schema)


def test_schema_rejects_type_and_value_mutations() -> None:
    schema = build_schema()
    payload = load_json(ROOT / "results/result.json")
    for mutation in (
        lambda value: value["source_locks"].__setitem__("count", True),
        lambda value: value["certificate"]["coefficient_ledger"].__setitem__("published", 550),
        lambda value: value["certificate"]["one_tail_sign_mutation"].__setitem__("wrong_sign_rejected", False),
        lambda value: value["gates"].__setitem__("A_canonical_intrinsic_dynamical_spectral_determinant", True),
    ):
        candidate = copy.deepcopy(payload)
        mutation(candidate)
        with pytest.raises((TypeError, ValueError)):
            validate_exact_schema(candidate, schema)


def test_builder_optimized_mode_and_boundary_language() -> None:
    payload = load_json(ROOT / "results/result.json")
    assert payload["theorem"]["remainder"] == "abs(R_y)<=3301*T_y^3/(6*pi^2)<551*T_y^3/pi^2 for every y>=1"
    assert "Y_infinity-2m_infinity" in payload["theorem"]["two_scale_expansion"]
    assert payload["claim_boundary"]["route_a"] == "GO"
    assert payload["claim_boundary"]["route_b"] == "STOP_SCOPED"
    assert not any(payload["gates"].values())
    environment = dict(os.environ)
    environment["PYTHONPATH"] = f"{ROOT / 'src'}:{ROOT}"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = "from experiments.build_result import build_payload; p=build_payload(); print(p['source_locks']['count'],p['certificate']['all_pass'])"
    completed = subprocess.run([sys.executable, "-OO", "-c", command], check=True, capture_output=True, text=True, env=environment)
    assert completed.stdout.strip() == "33 True"
