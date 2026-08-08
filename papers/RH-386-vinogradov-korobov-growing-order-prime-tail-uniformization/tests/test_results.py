from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from jsonschema import Draft202012Validator
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

import build_result  # noqa: E402
import build_schema  # noqa: E402
from vk_prime_tail import exact_equal, loads_strict  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_result_is_exact_fresh_regeneration() -> None:
    stored = loads_strict((ROOT / "results" / "result.json").read_text())
    fresh = build_result.build_payload()
    assert exact_equal(stored, fresh)
    assert (ROOT / "results" / "result.json").read_text() == build_result.serialized_payload(fresh)
    assert stored["all_pass"] is True
    assert sha256(ROOT / "results" / "result.json") == "b59fc7921ef89d556fbc81a409ada9304fafc92424b0f4a79f97aa4d57f25ff4"


def test_source_closure_is_exact_59_plus_1() -> None:
    payload = build_result.build_payload()
    locks = payload["source_locks"]
    assert locks["git_count"] == 59
    assert locks["remote_count"] == 1
    assert locks["logical_count"] == 60
    assert locks["git"]["group_sizes"] == {"rh384_immutable_closure": 51, "rh384_standard8": 8}
    assert locks["git"]["group_digests"] == build_result.EXPECTED_GROUP_DIGESTS
    assert locks["git"]["all_git_source_digest"] == "6247477a1744ccfe676ebd1c20b4d659c597ce0749f3d3a9a0b1c8aa2c87069d"
    assert locks["git"]["pass"] is True
    assert locks["remote"]["pass"] is True
    assert locks["remote"]["network_fetch_performed"] is False
    paths = [entry["path"] for entry in locks["git"]["entries"]]
    assert len(paths) == len(set(paths)) == 59
    assert "prime_dynamics_theory/AGENTS.md" not in paths
    assert "prime_dynamics_theory/RH_HANDOFF.md" not in paths


def test_source_commit_and_membership_rebinding_fail_closed() -> None:
    commits = dict(build_result.SOURCE_COMMITS)
    commits["rh384_standard8"] = "0" * 40
    with pytest.raises(ValueError):
        build_result.build_git_source_locks(commits=commits)

    groups = build_result.source_groups()
    groups["rh384_standard8"] = groups["rh384_standard8"][:-1]
    with pytest.raises(ValueError):
        build_result.build_git_source_locks(groups=groups)


def test_sealed_digest_constants_reject_bad_format(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(build_result, "EXPECTED_ALL_GIT_SOURCE_DIGEST", "unsealed")
    with pytest.raises(ValueError):
        build_result._validate_sealed_constants()


def test_remote_lock_rebinding_fails_result_build(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    lock = loads_strict((ROOT / "results" / "external_source_lock.json").read_text())
    lock["redistributable_in_release"] = True
    bad = tmp_path / "external_source_lock.json"
    bad.write_text(json.dumps(lock, sort_keys=True))

    original = Path.read_text

    def redirected(self: Path, *args: object, **kwargs: object) -> str:
        if self == ROOT / "results" / "external_source_lock.json":
            return bad.read_text()
        return original(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", redirected)
    with pytest.raises(RuntimeError):
        build_result.build_remote_source_lock(build_result.build_certificate())


def test_schema_is_fresh_official_and_recursively_closed() -> None:
    stored_schema = loads_strict((ROOT / "results" / "result.schema.json").read_text())
    fresh_schema = build_schema.build_schema()
    assert exact_equal(stored_schema, fresh_schema)
    Draft202012Validator.check_schema(stored_schema)
    instance = loads_strict((ROOT / "results" / "result.json").read_text())
    assert list(Draft202012Validator(stored_schema).iter_errors(instance)) == []

    def check_closed(schema: object) -> None:
        if type(schema) is not dict:
            return
        if schema.get("type") == "object":
            assert schema.get("additionalProperties") is False
            assert set(schema.get("required", [])) == set(schema.get("properties", {}))
            for child in schema["properties"].values():
                check_closed(child)
        if schema.get("type") == "array":
            assert schema.get("items") is False
            assert schema.get("minItems") == schema.get("maxItems") == len(schema.get("prefixItems", []))
            for child in schema["prefixItems"]:
                check_closed(child)

    check_closed(stored_schema)
    assert sha256(ROOT / "results" / "result.schema.json") == "a5f679c5ceccbb485dc526512994e0c2fa66dd94c69c8aed479599bdfb386330"


def test_schema_rejects_bool_for_integer_and_extra_member() -> None:
    schema = loads_strict((ROOT / "results" / "result.schema.json").read_text())
    validator = Draft202012Validator(schema)
    instance = loads_strict((ROOT / "results" / "result.json").read_text())
    attacked = deepcopy(instance)
    attacked["certificate"]["counts"]["oracle_rows_total"] = True
    assert list(validator.iter_errors(attacked))
    attacked = deepcopy(instance)
    attacked["certificate"]["unexpected"] = "escape"
    assert list(validator.iter_errors(attacked))


def test_result_strict_json_rejects_duplicate_and_nonfinite() -> None:
    for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":-Infinity}', "[]"):
        with pytest.raises(ValueError):
            loads_strict(text)


def test_optimized_result_builder_matches_frozen_hash() -> None:
    code = (
        "import hashlib;from build_result import build_payload,serialized_payload;"
        "b=serialized_payload(build_payload()).encode();print(len(b),hashlib.sha256(b).hexdigest())"
    )
    completed = subprocess.run(
        [sys.executable, "-OO", "-B", "-c", code],
        cwd=ROOT / "experiments",
        env={
            **__import__("os").environ,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": f"{ROOT / 'src'}:{ROOT / 'experiments'}",
        },
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    result = ROOT / "results" / "result.json"
    assert completed.stdout.strip() == f"{result.stat().st_size} {sha256(result)}"


def test_all_claim_firewalls_are_false() -> None:
    payload = build_result.build_payload()
    assert payload["gates"] == {
        "A_intrinsic_determinant": False,
        "B_scattering_completion": False,
        "C_self_adjoint_generator": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    assert not any(payload["forbidden_claims"].values())
