from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

import build_archive  # noqa: E402
import verify_archive  # noqa: E402
from vk_prime_tail import exact_equal, loads_strict  # noqa: E402
from vk_prime_tail.core import (  # noqa: E402
    JOHNSTON_YANG_SHA256,
    JOHNSTON_YANG_MAIN_TEX_SHA256,
    JOHNSTON_YANG_SOURCE_TAR_SHA256,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_manifest_is_exact_fresh_regeneration() -> None:
    stored = loads_strict((ROOT / "results" / "dependency_manifest.json").read_text())
    fresh = build_archive.build_payload()
    assert exact_equal(stored, fresh)
    assert (ROOT / "results" / "dependency_manifest.json").read_text() == build_archive.serialized_payload(fresh)
    assert stored["publication_file_count"] == len(build_archive.LOCAL_MEMBERS)
    assert stored["external_git_input_count"] == 59
    assert stored["remote_logical_input_count"] == 1
    assert all(stored[key] is True for key in verify_archive.BOOLEAN_KEYS)


def test_archive_verification_is_failure_free() -> None:
    manifest = loads_strict((ROOT / "results" / "dependency_manifest.json").read_text())
    fresh = verify_archive.verify_manifest(manifest)
    stored = loads_strict((ROOT / "results" / "archive_verification.json").read_text())
    assert exact_equal(stored, fresh)
    assert stored["status"] == "RH-386_archive_verified"
    assert stored["failure_count"] == 0
    assert stored["failures"] == []


def test_nonredistributed_external_payloads_are_excluded() -> None:
    members = set(build_archive.LOCAL_MEMBERS)
    assert "results/external_source_lock.json" in members
    assert "experiments/verify_remote_source.py" in members
    assert {member for member in members if member.endswith(".pdf")} == build_archive.PUBLICATION_PDFS
    hashes = {sha256(ROOT / member) for member in members}
    assert JOHNSTON_YANG_SHA256 not in hashes
    assert JOHNSTON_YANG_SOURCE_TAR_SHA256 not in hashes
    assert JOHNSTON_YANG_MAIN_TEX_SHA256 not in hashes
    assert build_archive.external_payload_exclusion() is True


def test_manifest_hash_and_membership_mutations_fail() -> None:
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
    assert result["status"] == "RH-386_archive_failed"
    assert result["failure_count"] > 0


def test_remote_count_type_and_lock_hash_mutations_fail() -> None:
    manifest = build_archive.build_payload()
    attacked = deepcopy(manifest)
    attacked["remote_logical_input_count"] = True
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    attacked = deepcopy(manifest)
    attacked["remote_source_lock_sha256"] = "0" * 64
    assert verify_archive.verify_manifest(attacked)["failure_count"] > 0


@pytest.mark.parametrize("value", [[], None, 1, "not-an-object"])
def test_nonobject_manifest_is_standard_fail_closed(value: object) -> None:
    result = verify_archive.verify_manifest(value)
    assert result["status"] == "RH-386_archive_failed"
    assert result["failure_count"] == 1
    assert result["failures"] == ["manifest:top_level_not_an_object"]
    assert all(result[key] is False for key in verify_archive.BOOLEAN_KEYS)


def test_publication_pdfs_are_byte_identical() -> None:
    assert (ROOT / "main.pdf").read_bytes() == (
        ROOT / "vinogradov-korobov-growing-order-prime-tail-uniformization.pdf"
    ).read_bytes()


def test_no_python_cache_is_a_publication_member() -> None:
    assert all("__pycache__" not in member and not member.endswith((".pyc", ".pyo")) for member in build_archive.LOCAL_MEMBERS)


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
