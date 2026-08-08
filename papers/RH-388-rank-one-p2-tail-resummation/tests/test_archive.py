from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
for directory in (ROOT, ROOT / "experiments", ROOT / "src"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from experiments import build_archive, build_result, source_locks, verify_archive  # noqa: E402
from rank_one_p2 import exact_equal, loads_strict  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_manifest_is_exact_fresh_regeneration() -> None:
    stored = loads_strict((ROOT / "results" / "dependency_manifest.json").read_text(encoding="utf-8"))
    fresh = build_archive.build_payload()
    assert exact_equal(stored, fresh)
    assert (ROOT / "results" / "dependency_manifest.json").read_text(encoding="utf-8") == build_archive.serialized_payload(fresh)
    assert stored["publication_file_count"] == len(build_archive.LOCAL_MEMBERS) == 36
    assert stored["external_git_input_count"] == 77
    assert stored["remote_logical_input_count"] == 2
    assert stored["logical_source_digest"] == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
    assert all(stored[key] is True for key in verify_archive.BOOLEAN_KEYS)


def test_archive_verification_is_failure_free() -> None:
    manifest = loads_strict((ROOT / "results" / "dependency_manifest.json").read_text(encoding="utf-8"))
    fresh = verify_archive.verify_manifest(manifest)
    stored = loads_strict((ROOT / "results" / "archive_verification.json").read_text(encoding="utf-8"))
    assert exact_equal(stored, fresh)
    assert stored["status"] == "RH-388_archive_verified"
    assert stored["failure_count"] == 0
    assert stored["failures"] == []


def test_nonredistributed_external_payloads_are_excluded() -> None:
    members = set(build_archive.LOCAL_MEMBERS)
    assert {
        "results/external_source_lock.json",
        "results/maynard_external_source_lock.json",
        "experiments/verify_remote_source.py",
        "experiments/source_locks.py",
    }.issubset(members)
    assert {member for member in members if member.endswith(".pdf")} == build_archive.PUBLICATION_PDFS
    hashes = {sha256(ROOT / member) for member in members}
    assert hashes.isdisjoint(build_archive.REMOTE_PAYLOAD_HASHES)
    assert build_archive.external_payload_exclusion() is True


def test_manifest_hash_membership_and_long_path_mutations_fail() -> None:
    manifest = build_archive.build_payload()
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"]["README.md"] = "0" * 64
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"]["unexpected.pdf"] = "0" * 64
    attacked["publication_file_count"] += 1
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"]["x" * 5000] = "0" * 64
    attacked["publication_file_count"] += 1
    result = verify_archive.verify_manifest(attacked)
    assert result["status"] == "RH-388_archive_failed"
    assert result["failure_count"] > 0


def test_remote_count_digest_order_and_logical_mutations_fail() -> None:
    manifest = build_archive.build_payload()
    attacked = deepcopy(manifest)
    attacked["remote_logical_input_count"] = True
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["remote_source_lock_sha256"][0] = "0" * 64
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["remote_source_lock_sha256"].reverse()
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["logical_source_digest"] = "0" * 64
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0


def test_boolean_and_source_commit_rebinding_fail() -> None:
    manifest = build_archive.build_payload()
    attacked = deepcopy(manifest)
    attacked["semantic_pdf_match"] = 1
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["source_commits"]["rh387_release"] = "0" * 40
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0


@pytest.mark.parametrize("value", [[], None, 1, "not-an-object"])
def test_nonobject_manifest_is_standard_fail_closed(value: object) -> None:
    result = verify_archive.verify_manifest(value)
    assert result["status"] == "RH-388_archive_failed"
    assert result["failure_count"] == 1
    assert result["failures"] == ["manifest:top_level_not_an_object"]
    assert all(result[key] is False for key in verify_archive.BOOLEAN_KEYS)


def test_publication_pdfs_are_byte_identical() -> None:
    assert (ROOT / "main.pdf").read_bytes() == (ROOT / "rank-one-p2-tail-resummation.pdf").read_bytes()


def test_no_python_cache_is_a_publication_member() -> None:
    assert all(
        "__pycache__" not in member and not member.endswith((".pyc", ".pyo"))
        for member in build_archive.LOCAL_MEMBERS
    )


def test_optimized_archive_builder_matches_stored_manifest() -> None:
    code = (
        "import hashlib;from build_archive import build_payload,serialized_payload;"
        "b=serialized_payload(build_payload()).encode();print(len(b),hashlib.sha256(b).hexdigest())"
    )
    completed = subprocess.run(
        [sys.executable, "-OO", "-B", "-c", code],
        cwd=ROOT / "experiments",
        env={
            **__import__("os").environ,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": f"{ROOT / 'src'}:{ROOT}:{ROOT / 'experiments'}",
        },
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    manifest = ROOT / "results" / "dependency_manifest.json"
    assert completed.stdout.strip() == f"{manifest.stat().st_size} {sha256(manifest)}"


def test_outer_archive_verifier_replays_successfully() -> None:
    completed = subprocess.run(
        [sys.executable, "-B", "experiments/verify_archive.py"],
        cwd=ROOT,
        env={
            **__import__("os").environ,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": f"{ROOT / 'src'}:{ROOT}",
        },
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert completed.returncode == 0, completed.stderr
    assert '"status": "RH-388_archive_verified"' in completed.stdout
