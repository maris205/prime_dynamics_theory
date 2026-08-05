from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from verify_four_volume_archive import (  # noqa: E402
    MANIFEST_PATH,
    MVP1_MEMBERS,
    validate_archive_payload,
    validate_manifest_structure,
    verify_hash_map,
    verify_manifest,
)


def test_four_volume_manifest_and_hash_replay() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    result = verify_manifest(manifest, write_output=False)
    assert result["volume_count"] == 4
    assert result["numbered_source_count"] == 361
    assert result["archive_member_count"] == manifest["aggregate_archive_file_count"]
    assert result["failure_count"] == 0


def test_manifest_rejects_duplicate_root_range_and_traversal() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    duplicate = copy.deepcopy(manifest)
    duplicate["volumes"][1]["root"] = duplicate["volumes"][0]["root"]
    duplicate["volumes"][1]["source_range"] = duplicate["volumes"][0]["source_range"]
    with pytest.raises(RuntimeError):
        validate_manifest_structure(duplicate)

    traversal = copy.deepcopy(manifest)
    traversal["volumes"][0]["archive"] = "../archive_verification.json"
    with pytest.raises(RuntimeError):
        validate_manifest_structure(traversal)


def test_archive_membership_and_file_hash_mutations_fail(tmp_path: Path) -> None:
    payload = {
        "file_count": len(MVP1_MEMBERS) - 1,
        "files": {name: "0" * 64 for name in sorted(MVP1_MEMBERS)[1:]},
    }
    with pytest.raises(RuntimeError):
        validate_archive_payload(payload, set(MVP1_MEMBERS), "mutated Volume I")

    target = tmp_path / "source.txt"
    target.write_text("locked\n")
    expected = hashlib.sha256(target.read_bytes()).hexdigest()
    assert verify_hash_map({"source.txt": expected}, tmp_path, "test source") == 1
    target.write_text("changed\n")
    with pytest.raises(RuntimeError):
        verify_hash_map({"source.txt": expected}, tmp_path, "test source")


def test_outer_archive_hash_mutation_fails() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    mutated = copy.deepcopy(manifest)
    mutated["volumes"][0]["archive_sha256"] = "0" * 64
    with pytest.raises(RuntimeError, match="archive seal mismatch"):
        verify_manifest(mutated, write_output=False)
