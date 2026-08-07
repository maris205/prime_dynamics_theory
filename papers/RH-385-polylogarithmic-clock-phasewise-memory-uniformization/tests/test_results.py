"""Source-lock, strict JSON, schema, and regeneration tests for RH-385."""

from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import experiments.build_result as build_result_module


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.build_result import (  # noqa: E402
    EXPECTED_ALL_SOURCE_DIGEST,
    EXPECTED_GROUP_DIGESTS,
    SOURCE_COMMITS,
    _strict_load,
    build_payload,
    build_source_locks,
    lines_digest,
    serialized_payload,
    source_digest_lines,
    source_groups,
)
from experiments.build_schema import build_schema, serialized_schema  # noqa: E402


def _validate_exact(value: object, schema: dict[str, object]) -> None:
    if "const" in schema:
        if type(value) is not type(schema["const"]) or value != schema["const"]:
            raise ValueError("const mismatch")
    kind = schema.get("type")
    if kind == "object":
        if type(value) is not dict or schema.get("additionalProperties") is not False:
            raise TypeError("object mismatch")
        properties = schema["properties"]
        if set(value) != set(properties):
            raise ValueError("object membership mismatch")
        for key, child in value.items():
            _validate_exact(child, properties[key])
    elif kind == "array":
        if type(value) is not list:
            raise TypeError("array mismatch")
        if len(value) != schema.get("minItems") or len(value) != schema.get("maxItems"):
            raise ValueError("array length mismatch")
        if "prefixItems" in schema:
            prefix = schema["prefixItems"]
            if schema.get("items") is not False or len(value) != len(prefix):
                raise ValueError("prefix array mismatch")
            for child, child_schema in zip(value, prefix):
                _validate_exact(child, child_schema)
        elif value:
            for child in value:
                _validate_exact(child, schema["items"])
    elif kind == "boolean" and type(value) is not bool:
        raise TypeError("boolean mismatch")
    elif kind == "integer" and type(value) is not int:
        raise TypeError("integer mismatch")
    elif kind == "string" and type(value) is not str:
        raise TypeError("string mismatch")


def test_full_result_regeneration_and_sealed_source_locks() -> None:
    stored = (ROOT / "results/result.json").read_text()
    payload = build_payload()
    assert serialized_payload(payload) == stored
    locks = payload["source_locks"]
    assert locks["count"] == 67
    assert locks["group_sizes"] == {
        "rh384_immutable_closure": 51,
        "rh384_standard8": 8,
        "rh366_davenport_standard8": 8,
    }
    assert locks["group_digests"] == EXPECTED_GROUP_DIGESTS
    assert locks["all_source_digest"] == EXPECTED_ALL_SOURCE_DIGEST
    assert all(locks[key] is True for key in (
        "release_blob_identity_pass", "live_file_identity_pass",
        "declared_hash_identity_pass", "digest_contract_pass",
    ))


def test_source_commit_group_and_sealed_digest_mutations_fail(monkeypatch: pytest.MonkeyPatch) -> None:
    bad_commits = dict(SOURCE_COMMITS)
    bad_commits["rh366_davenport_standard8"] = "0" * 40
    with pytest.raises(ValueError, match="commits were rebound"):
        build_source_locks(commits=bad_commits)
    bad_groups = source_groups()
    bad_groups["rh384_standard8"] = bad_groups["rh384_standard8"][:-1]
    with pytest.raises(ValueError, match="membership was rebound"):
        build_source_locks(groups=bad_groups)
    with monkeypatch.context() as patch:
        patch.setattr(build_result_module, "EXPECTED_ALL_SOURCE_DIGEST", "TO_BE_" + "SEALED")
        with pytest.raises(ValueError, match="sealed 64-hex"):
            build_result_module.build_source_locks()
    with monkeypatch.context() as patch:
        patch.setattr(build_result_module, "CERTIFICATE_FIXTURE_SHA256", "0" * 63)
        with pytest.raises(ValueError, match="sealed 64-hex"):
            build_result_module.build_payload()


def test_source_digest_duplicate_and_path_escape_fail() -> None:
    entries = build_source_locks()["entries"]
    duplicate = deepcopy(entries)
    duplicate[-1] = deepcopy(duplicate[0])
    with pytest.raises(ValueError, match="duplicates"):
        source_digest_lines(duplicate)
    escaped = deepcopy(entries)
    escaped[0]["path"] = "prime_dynamics_theory/../RH_HANDOFF.md"
    with pytest.raises(ValueError, match="unsafe"):
        source_digest_lines(escaped)
    lines = list(source_digest_lines(entries))
    lines[0] += "0"
    assert lines_digest(lines) != EXPECTED_ALL_SOURCE_DIGEST


def test_mutable_root_files_are_not_locked() -> None:
    paths = [row["path"] for row in build_source_locks()["entries"]]
    assert len(paths) == len(set(paths)) == 67
    assert all("AGENTS.md" not in path and "RH_HANDOFF.md" not in path for path in paths)


def test_strict_json_loader_rejects_duplicate_nonfinite_and_nonobject(tmp_path: Path) -> None:
    for index, text in enumerate(('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', "[]")):
        path = tmp_path / f"bad-{index}.json"
        path.write_text(text)
        with pytest.raises(ValueError):
            _strict_load(path)


def test_schema_regeneration_is_recursively_closed_and_strictly_typed() -> None:
    schema = build_schema()
    assert serialized_schema(schema) == (ROOT / "results/result.schema.json").read_text()
    payload = _strict_load(ROOT / "results/result.json")
    _validate_exact(payload, schema)
    mutated = deepcopy(payload)
    mutated["source_locks"]["count"] = True
    with pytest.raises(TypeError):
        _validate_exact(mutated, schema)
    mutated = deepcopy(payload)
    mutated["certificate"]["truth_tables"][0]["truth"][0] = False
    with pytest.raises(TypeError):
        _validate_exact(mutated, schema)
    mutated = deepcopy(payload)
    mutated["unexpected"] = 1
    with pytest.raises(ValueError):
        _validate_exact(mutated, schema)


def test_schema_is_official_draft_2020_12_valid() -> None:
    script = """
import json,sys
from jsonschema import Draft202012Validator
schema=json.load(open(sys.argv[1])); instance=json.load(open(sys.argv[2]))
Draft202012Validator.check_schema(schema)
errors=list(Draft202012Validator(schema).iter_errors(instance))
if errors: raise SystemExit(errors[0].message)
"""
    attempts = []
    for executable in dict.fromkeys((sys.executable, "/usr/bin/python3")):
        completed = subprocess.run(
            [executable, "-c", script, str(ROOT / "results/result.schema.json"), str(ROOT / "results/result.json")],
            capture_output=True, text=True,
        )
        attempts.append(f"{executable}:{completed.stderr.strip()}")
        if completed.returncode == 0:
            return
    pytest.fail("official Draft 2020-12 validation failed: " + " | ".join(attempts))


def test_optimized_python_mode_and_exact_types() -> None:
    environment = dict(os.environ)
    environment["PYTHONPATH"] = f"{ROOT / 'src'}:{ROOT}"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    command = (
        "from experiments.build_result import build_payload; "
        "p=build_payload(); print(p['source_locks']['count'],p['all_pass'])"
    )
    completed = subprocess.run(
        [sys.executable, "-OO", "-c", command], check=True,
        capture_output=True, text=True, env=environment,
    )
    assert completed.stdout.strip() == "67 True"


def test_claim_boundary_gates_and_outer_replay() -> None:
    payload = _strict_load(ROOT / "results/result.json")
    assert payload["claim_boundary"]["route_a"] == "GO"
    assert payload["claim_boundary"]["route_b"] == "STOP_SCOPED"
    assert payload["claim_boundary"]["finite_artifact_role"] == "reproduction_not_analytic_proof"
    assert not any(payload["gates"].values())
    assert not any(payload["forbidden_claims"].values())
    replay = payload["outer_four_volume_replay"]
    assert [replay[key] for key in (
        "volume_count", "archive_member_count", "dependency_hash_count",
        "result_hash_count", "numbered_source_count", "failure_count",
    )] == [4, 73, 1548, 8, 361, 0]
