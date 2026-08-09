from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
for directory in (ROOT, ROOT / "experiments", ROOT / "src"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from experiments import build_archive, build_result, build_schema, source_locks, verify_archive  # noqa: E402
from growing_rank_filtration.core import exact_equal, loads_strict  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_manifest_is_exact_fresh_regeneration() -> None:
    stored_path = ROOT / "results" / "dependency_manifest.json"
    stored = loads_strict(stored_path.read_text(encoding="utf-8"))
    fresh = build_archive.build_payload()
    assert exact_equal(stored, fresh)
    assert stored_path.read_text(encoding="utf-8") == build_archive.serialized_payload(fresh)
    assert stored["publication_file_count"] == len(build_archive.LOCAL_MEMBERS) == 34
    assert stored["release_stage_file_count"] == 36
    assert stored["external_git_input_count"] == 87
    assert stored["remote_logical_input_count"] == 2
    assert stored["logical_source_digest"] == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
    assert all(stored[key] is True for key in verify_archive.BOOLEAN_KEYS)


def test_archive_verification_is_failure_free() -> None:
    manifest = loads_strict((ROOT / "results" / "dependency_manifest.json").read_text(encoding="utf-8"))
    fresh = verify_archive.verify_manifest(manifest)
    stored = loads_strict((ROOT / "results" / "archive_verification.json").read_text(encoding="utf-8"))
    assert exact_equal(stored, fresh)
    assert stored["status"] == "RH-390_archive_verified"
    assert stored["failure_count"] == 0
    assert stored["failures"] == []


def test_four_external_payloads_are_excluded_from_members_and_tree() -> None:
    members = set(build_archive.LOCAL_MEMBERS)
    assert {
        "results/external_source_lock.json",
        "results/maynard_external_source_lock.json",
        "experiments/source_locks.py",
    }.issubset(members)
    assert len(build_archive.REMOTE_PAYLOAD_HASHES) == 4
    assert {member for member in members if member.endswith(".pdf")} == build_archive.PUBLICATION_PDFS
    member_hashes = {sha256(ROOT / member) for member in members}
    tree_hashes = {sha256(path) for path in ROOT.rglob("*") if path.is_file()}
    assert member_hashes.isdisjoint(build_archive.REMOTE_PAYLOAD_HASHES)
    assert tree_hashes.isdisjoint(build_archive.REMOTE_PAYLOAD_HASHES)
    assert build_archive.external_payload_exclusion() is True


def test_two_offline_remote_replays_make_zero_requests() -> None:
    rows = list(build_archive.offline_remote_replay())
    assert [row["source_key"] for row in rows] == [
        "johnston-yang-arxiv-2204.01980v2",
        "maynard-annals-2015-small-gaps",
    ]
    assert all(row["status"] == "NETWORK_DISABLED" for row in rows)
    assert all(row["network_opt_in"] is False and type(row["requests_made"]) is int and row["requests_made"] == 0 for row in rows)


def test_manifest_hash_membership_and_path_mutations_fail_closed() -> None:
    manifest = build_archive.build_payload()
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"]["README.md"] = "0" * 64
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"]["unexpected.pdf"] = "0" * 64
    attacked["publication_file_count"] += 1
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"]["../outside"] = "0" * 64
    attacked["publication_file_count"] += 1
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"]["x" * 5000] = "0" * 64
    attacked["publication_file_count"] += 1
    result = verify_archive.verify_manifest(attacked)
    assert result["status"] == "RH-390_archive_failed"
    assert result["failure_count"] > 0


def test_manifest_nested_nonobject_and_invalid_hash_fail_closed() -> None:
    manifest = build_archive.build_payload()
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"] = []
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["external_git_inputs"] = None
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"]["README.md"] = True
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0


def test_remote_count_digest_order_logical_and_offline_mutations_fail() -> None:
    manifest = build_archive.build_payload()
    attacked = deepcopy(manifest)
    attacked["remote_logical_input_count"] = True
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["remote_source_lock_sha256"][1] = "0" * 64
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["remote_source_lock_sha256"].reverse()
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["logical_source_digest"] = "0" * 64
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["offline_remote_replay"][0]["requests_made"] = 1
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0


def test_boolean_stage_count_and_source_commit_rebinding_fail() -> None:
    manifest = build_archive.build_payload()
    attacked = deepcopy(manifest)
    attacked["semantic_pdf_match"] = 1
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["release_stage_file_count"] = True
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["source_commits"]["rh388_release"] = "0" * 40
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0


@pytest.mark.parametrize("value", [[], None, 1, "not-an-object"])
def test_nonobject_manifest_is_standard_fail_closed(value: object) -> None:
    result = verify_archive.verify_manifest(value)
    assert result["status"] == "RH-390_archive_failed"
    assert result["failure_count"] == 1
    assert result["failures"] == ["manifest:top_level_not_an_object"]
    assert result["release_stage_file_count"] == 0
    assert all(result[key] is False for key in verify_archive.BOOLEAN_KEYS)


def test_publication_pdfs_are_byte_identical() -> None:
    assert (ROOT / "main.pdf").read_bytes() == (ROOT / "growing-rank-prime-tail-filtration.pdf").read_bytes()


def test_no_cache_symlink_or_special_file_is_a_publication_member() -> None:
    assert all("__pycache__" not in member and not member.endswith((".pyc", ".pyo")) for member in build_archive.LOCAL_MEMBERS)
    assert all((ROOT / member).is_file() and not (ROOT / member).is_symlink() for member in build_archive.LOCAL_MEMBERS)
    assert list(ROOT.rglob("__pycache__")) == []
    assert list(ROOT.rglob(".pytest_cache")) == []


def test_normal_and_optimized_four_objects_are_fresh_exact() -> None:
    result = build_result.build_payload()
    schema = build_schema.build_schema()
    manifest = build_archive.build_payload()
    report = verify_archive.verify_manifest(manifest)
    names = ("result.json", "result.schema.json", "dependency_manifest.json", "archive_verification.json")
    stored = [loads_strict((ROOT / "results" / name).read_text(encoding="utf-8")) for name in names]
    assert all(exact_equal(left, right) for left, right in zip(stored, (result, schema, manifest, report)))
    code = (
        "import hashlib,json,sys;sys.path[:0]=['src','experiments','.'];"
        "import build_result,build_schema,build_archive,verify_archive;"
        "objs=[build_result.build_payload(),build_schema.build_schema(),build_archive.build_payload()];"
        "objs.append(verify_archive.verify_manifest(objs[2]));"
        "print(' '.join(hashlib.sha256((json.dumps(o,indent=2,sort_keys=True,allow_nan=False)+'\\n').encode()).hexdigest() for o in objs))"
    )
    completed = subprocess.run(
        [sys.executable, "-OO", "-B", "-c", code],
        cwd=ROOT,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": f"{ROOT / 'src'}:{ROOT}:{ROOT / 'experiments'}"},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip().split() == [sha256(ROOT / "results" / name) for name in names]


def test_official_schema_is_closed_and_accepts_the_stored_result() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = loads_strict((ROOT / "results" / "result.schema.json").read_text(encoding="utf-8"))
    result = loads_strict((ROOT / "results" / "result.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(result)) == []


def test_outer_archive_verifier_replays_without_writing() -> None:
    manifest = loads_strict((ROOT / "results" / "dependency_manifest.json").read_text(encoding="utf-8"))
    report = verify_archive.verify_manifest(manifest)
    assert report["status"] == "RH-390_archive_verified"
    assert report["failure_count"] == 0
    assert verify_archive.serialized_report(report) == (ROOT / "results" / "archive_verification.json").read_text(encoding="utf-8")
