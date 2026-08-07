"""Source-lock, schema, regeneration, and boundary tests for RH-384."""

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
    _strict_load,
    build_payload,
    build_source_locks,
    digest,
    lines_digest,
    serialized_payload,
    source_digest_lines,
)
from experiments.build_schema import build_schema, serialized_schema  # noqa: E402
from prime_tail_scales import CERTIFICATE_FIXTURE_SHA256, payload_sha256, verify_certificate  # noqa: E402


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
        if type(value) is not list or schema.get("items") is not False:
            raise TypeError("array type mismatch")
        prefix_items = schema.get("prefixItems", [])
        if type(prefix_items) is not list or len(value) != len(prefix_items):
            raise ValueError("array length mismatch")
        for child, child_schema in zip(value, prefix_items):
            validate_exact_schema(child, child_schema)
    elif kind == "boolean" and type(value) is not bool:
        raise TypeError("boolean type mismatch")
    elif kind == "integer" and type(value) is not int:
        raise TypeError("integer type mismatch")
    elif kind == "string" and type(value) is not str:
        raise TypeError("string type mismatch")


def test_full_result_regeneration_and_51_release_blob_locks() -> None:
    stored = (ROOT / "results/result.json").read_text()
    assert serialized_payload(build_payload()) == stored
    locks = build_source_locks()
    assert locks["count"] == len(SOURCE_FILES) == 51
    assert list(locks["group_sizes"].values()) == [7, 8, 8, 8, 8, 8, 2, 2]
    assert locks["group_digests"] == EXPECTED_GROUP_DIGESTS
    assert locks["all_source_digest"] == EXPECTED_ALL_SOURCE_DIGEST
    assert locks["release_blob_identity_pass"] and locks["declared_hash_identity_pass"]
    for entry in locks["entries"]:
        assert entry["sha256"] == digest(WORKSPACE / entry["path"])
        assert "AGENTS.md" not in entry["path"] and "RH_HANDOFF.md" not in entry["path"]


def test_source_commit_membership_digest_and_path_mutations_fail() -> None:
    bad_commits = dict(SOURCE_COMMITS)
    bad_commits["rh2_pnt_release"] = "0" * 40
    with pytest.raises(ValueError, match="commits were rebound"):
        build_source_locks(source_commits=bad_commits)
    bad_groups = copy.deepcopy(SOURCE_GROUPS)
    bad_groups["rh2_pnt_release"] = bad_groups["rh2_pnt_release"][:-1]
    with pytest.raises(ValueError, match="membership was rebound"):
        build_source_locks(source_groups=bad_groups)
    entries = build_source_locks()["entries"]
    bad = copy.deepcopy(entries)
    bad[0]["path"] = "prime_dynamics_theory/../RH_HANDOFF.md"
    with pytest.raises(ValueError, match="unsafe"):
        source_digest_lines(bad)
    duplicate = copy.deepcopy(entries)
    duplicate[-1] = copy.deepcopy(duplicate[0])
    with pytest.raises(ValueError, match="duplicates"):
        source_digest_lines(duplicate)
    lines = list(source_digest_lines(entries))
    lines[0] += "0"
    assert lines_digest(lines) != EXPECTED_ALL_SOURCE_DIGEST


def test_strict_json_loader_rejects_duplicate_nonfinite_and_nonobject(tmp_path: Path) -> None:
    for index, text in enumerate(('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', "[]")):
        path = tmp_path / f"bad-{index}.json"
        path.write_text(text)
        with pytest.raises(ValueError):
            _strict_load(path)


def test_schema_regeneration_is_recursively_closed_and_exact() -> None:
    schema = build_schema()
    assert serialized_schema(schema) == (ROOT / "results/result.schema.json").read_text()
    payload = _strict_load(ROOT / "results/result.json")
    validate_exact_schema(payload, schema)
    candidate = copy.deepcopy(payload)
    candidate["certificate"]["counts"]["partitions"] = 65
    with pytest.raises(ValueError):
        validate_exact_schema(candidate, schema)
    candidate = copy.deepcopy(payload)
    candidate["gates"]["E_completed_zeta_divisor_equality"] = True
    with pytest.raises(ValueError):
        validate_exact_schema(candidate, schema)
    candidate = copy.deepcopy(payload)
    candidate["source_locks"]["count"] = True
    with pytest.raises((TypeError, ValueError)):
        validate_exact_schema(candidate, schema)


def test_schema_is_official_draft_2020_12_valid() -> None:
    script = """
import json
import sys
from jsonschema import Draft202012Validator
schema = json.load(open(sys.argv[1]))
instance = json.load(open(sys.argv[2]))
Draft202012Validator.check_schema(schema)
errors = list(Draft202012Validator(schema).iter_errors(instance))
if errors:
    raise SystemExit(errors[0].message)
"""
    attempts = []
    candidates = (sys.executable, "/usr/bin/python3")
    for executable in dict.fromkeys(candidates):
        completed = subprocess.run(
            [executable, "-c", script, str(ROOT / "results/result.schema.json"), str(ROOT / "results/result.json")],
            capture_output=True,
            text=True,
        )
        attempts.append(f"{executable}: {completed.stderr.strip()}")
        if completed.returncode == 0:
            return
    pytest.fail("official Draft 2020-12 validation unavailable or failed: " + " | ".join(attempts))


def test_boundary_and_optimized_mode() -> None:
    payload = _strict_load(ROOT / "results/result.json")
    assert payload_sha256(verify_certificate()) == CERTIFICATE_FIXTURE_SHA256
    assert payload["claim_boundary"]["route_a"] == "GO"
    assert payload["claim_boundary"]["route_b"] == "STOP_SCOPED"
    assert not any(payload["gates"].values())
    assert not any(payload["forbidden_claims"].values())
    environment = dict(os.environ)
    environment["PYTHONPATH"] = f"{ROOT / 'src'}:{ROOT}"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = "from experiments.build_result import build_payload; p=build_payload(); print(p['source_locks']['count'],p['all_pass'])"
    completed = subprocess.run(
        [sys.executable, "-OO", "-c", command],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    assert completed.stdout.strip() == "51 True"


def test_json_round_trip_has_exact_types_and_no_nonfinite_constants() -> None:
    text = (ROOT / "results/result.json").read_text()
    payload = json.loads(text, parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    assert type(payload["source_locks"]["count"]) is int
    assert type(payload["certificate"]["all_pass"]) is bool

    def reject_nonfinite_numeric_values(value: object) -> None:
        if type(value) is dict:
            for child in value.values():
                reject_nonfinite_numeric_values(child)
        elif type(value) is list:
            for child in value:
                reject_nonfinite_numeric_values(child)
        elif type(value) is float:
            assert value == value and value not in (float("inf"), float("-inf"))

    reject_nonfinite_numeric_values(payload)
