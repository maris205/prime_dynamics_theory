from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
if str(EXPERIMENTS) not in sys.path:
    sys.path.insert(0, str(EXPERIMENTS))

import build_result  # noqa: E402
import build_schema  # noqa: E402
from integral_resummation import canonical_json_bytes, exact_equal, loads_strict  # noqa: E402


def test_result_is_fresh_exact_and_all_pass() -> None:
    stored = loads_strict((ROOT / "results" / "result.json").read_text())
    fresh = build_result.build_payload()
    assert exact_equal(stored, fresh)
    assert stored["all_pass"] is True
    assert stored["certificate_fixture"] == {
        "canonical_bytes": 10785,
        "sha256": "3c89e51662bbc2f1c7712f4205ff8cde88e9eb80636e2779d06154e914459b4b",
        "pass": True,
    }


def test_source_closure_is_exact_68_plus_one() -> None:
    locks = build_result.build_git_source_locks()
    assert locks["count"] == 68
    assert locks["group_sizes"] == {"rh386_immutable_closure": 59, "rh386_standard8": 8, "rh386_external_lock": 1}
    assert locks["group_digests"] == build_result.EXPECTED_GROUP_DIGESTS
    assert locks["all_git_source_digest"] == build_result.EXPECTED_ALL_GIT_SOURCE_DIGEST
    assert locks["pass"] is True
    payload = build_result.build_payload()
    assert (payload["source_locks"]["git_count"], payload["source_locks"]["remote_count"], payload["source_locks"]["logical_count"]) == (68, 1, 69)
    assert payload["source_locks"]["logical_source_digest"] == build_result.EXPECTED_LOGICAL_SOURCE_DIGEST
    assert payload["source_locks"]["logical_digest_pass"] is True


def test_source_commit_rebinding_and_duplicate_paths_fail_closed() -> None:
    with pytest.raises(ValueError):
        build_result.build_git_source_locks(commit="0" * 40)
    row = {"group": "g", "commit": build_result.RH386_RELEASE, "path": "prime_dynamics_theory/papers/x", "sha256": "0" * 64}
    with pytest.raises(ValueError):
        build_result.source_digest_lines([row, dict(row)])


def test_logical_digest_constant_is_sealed_and_rebinding_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(build_result, "EXPECTED_LOGICAL_SOURCE_DIGEST", "0" * 64)
    payload = build_result.build_payload()
    assert payload["source_locks"]["logical_digest_pass"] is False
    assert payload["source_locks"]["pass"] is False
    assert payload["all_pass"] is False
    monkeypatch.setattr(build_result, "EXPECTED_LOGICAL_SOURCE_DIGEST", "not-a-sha")
    with pytest.raises(ValueError):
        build_result.build_payload()


def test_remote_lock_is_exact_offline_and_payloads_are_absent() -> None:
    remote = build_result.build_remote_source_lock()
    assert remote["count"] == 1
    assert remote["lock_object_sha256"] == build_result.REMOTE_LOCK_CANONICAL_SHA256
    assert remote["network_fetch_performed"] is False
    assert remote["external_payload_hash_hits"] == []
    assert remote["external_payload_exclusion_pass"] is True
    assert remote["pass"] is True


def test_remote_full_object_mutations_are_distinguished() -> None:
    lock = loads_strict((ROOT / "results" / "external_source_lock.json").read_text())
    attacks = [
        ("sha256", "0" * 64),
        ("bytes", 278381),
        ("versioned_url", "https://arxiv.org/pdf/2204.01980"),
        ("version_of_record_doi", "10.0/wrong"),
        ("redistributable_in_release", True),
    ]
    for key, bad in attacks:
        candidate = deepcopy(lock)
        candidate[key] = bad
        assert not exact_equal(candidate, lock)
        assert canonical_json_bytes(candidate) != canonical_json_bytes(lock)


def test_schema_is_fresh_closed_and_validates_exact_result() -> None:
    stored = loads_strict((ROOT / "results" / "result.schema.json").read_text())
    fresh = build_schema.build_schema()
    assert exact_equal(stored, fresh)
    assert stored["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert stored["additionalProperties"] is False
    jsonschema = pytest.importorskip("jsonschema")
    jsonschema.Draft202012Validator.check_schema(stored)
    errors = list(jsonschema.Draft202012Validator(stored).iter_errors(build_result.build_payload()))
    assert errors == []


def test_schema_rejects_bool_for_int_and_extra_members() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = build_schema.build_schema()
    candidate = build_result.build_payload()
    candidate["certificate"]["ledger_rows"][0]["l1_gradient_bound"] = True
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(candidate))
    candidate = build_result.build_payload()
    candidate["extra"] = 1
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(candidate))


def test_optimized_builder_matches_stored_result() -> None:
    code = (
        "import json,sys;sys.path[:0]=['src','experiments'];"
        "from build_result import build_payload;"
        "print(json.dumps(build_payload(),sort_keys=True,separators=(',',':'),allow_nan=False))"
    )
    completed = subprocess.run([sys.executable, "-B", "-OO", "-c", code], cwd=ROOT, capture_output=True, text=True, check=False)
    assert completed.returncode == 0, completed.stderr
    assert loads_strict(completed.stdout) == build_result.build_payload()
