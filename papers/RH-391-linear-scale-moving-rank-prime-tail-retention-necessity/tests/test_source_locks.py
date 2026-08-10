from __future__ import annotations

from pathlib import Path

import pytest

import source_locks as locks


def test_source_closure_exact_counts_and_digests() -> None:
    closure = locks.build_source_closure()
    assert (closure["git_count"], closure["remote_count"], closure["logical_count"]) == (97, 2, 99)
    assert closure["git"]["all_git_source_digest"] == locks.EXPECTED_ALL_GIT_SOURCE_DIGEST
    assert closure["logical_source_digest"] == locks.EXPECTED_LOGICAL_SOURCE_DIGEST
    assert closure["pass"] is True


def test_git_groups_are_exact_87_8_2() -> None:
    git = locks.build_git_source_locks()
    assert git["group_sizes"] == {"rh390_immutable_closure": 87, "rh390_standard8": 8, "rh390_prior_external_locks": 2}
    assert git["group_digests"] == locks.EXPECTED_GROUP_DIGESTS
    assert git["count"] == 97


def test_git_rows_are_unique_release_bound_and_live_exact() -> None:
    git = locks.build_git_source_locks()
    entries = git["entries"]
    assert len({row["path"] for row in entries}) == 97
    assert {row["commit"] for row in entries} == {locks.RH390_RELEASE}
    assert git["release_identity_pass"] is True
    assert git["live_identity_pass"] is True


def test_remote_objects_and_pretty_locks_are_exact() -> None:
    remote = locks.build_remote_source_locks()
    assert remote["canonical_digests"] == [locks.JY_CANONICAL_SHA256, locks.MAYNARD_CANONICAL_SHA256]
    assert remote["local_lock_blob_digests"] == [locks.JY_LOCK_BLOB_SHA256, locks.MAYNARD_LOCK_BLOB_SHA256]
    assert remote["local_lock_objects_exact_pass"] is True
    assert remote["pass"] is True


def test_no_remote_payload_is_vendored_and_no_network_fetch_occurs() -> None:
    remote = locks.build_remote_source_locks()
    assert remote["external_payload_hash_hits"] == []
    assert remote["external_payload_exclusion_pass"] is True
    assert remote["network_fetch_performed"] is False
    assert remote["redistributable_in_release"] is False


def test_release_rebinding_is_rejected() -> None:
    with pytest.raises(ValueError, match="rebound"):
        locks.build_git_source_locks(commit="0" * 40)
    with pytest.raises(ValueError):
        locks.git_blob("bad", "README.md")


def test_mutable_and_unsafe_source_paths_are_rejected() -> None:
    for path in ("prime_dynamics_theory/AGENTS.md", "prime_dynamics_theory/RH_HANDOFF.md", "prime_dynamics_theory/../secret", "/absolute"):
        with pytest.raises(ValueError):
            locks._repo_relative(path)


def test_duplicate_source_paths_are_rejected() -> None:
    row = {"group": "g", "commit": locks.RH390_RELEASE, "path": "prime_dynamics_theory/README.md", "sha256": "0" * 64}
    with pytest.raises(ValueError, match="duplicate"):
        locks.source_digest_lines([row, dict(row)])


def test_lock_files_are_byte_identical_to_released_rh390() -> None:
    root = Path(__file__).resolve().parents[1]
    for name, expected in (("external_source_lock.json", locks.JY_LOCK_BLOB_SHA256), ("maynard_external_source_lock.json", locks.MAYNARD_LOCK_BLOB_SHA256)):
        assert locks.digest(root / "results" / name) == expected
        assert locks.digest_bytes(locks.git_blob(locks.RH390_RELEASE, f"{locks.RH390_DIRECTORY}/results/{name}")) == expected


def test_released_result_identity_and_source_contract() -> None:
    result = locks.released_rh390_result()
    assert result["paper"] == "RH-390"
    assert result["source_locks"]["git_count"] == 87
    assert result["source_locks"]["logical_count"] == 89


def test_digest_helpers_enforce_exact_input_types() -> None:
    with pytest.raises(TypeError):
        locks.digest_bytes("not bytes")
    with pytest.raises(TypeError):
        locks.lines_digest(("ok", 1))
    with pytest.raises(TypeError):
        locks.digest("not a path")
