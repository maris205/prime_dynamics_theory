from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

import source_locks


def test_source_closure_is_exact_87_plus_two_remote() -> None:
    closure = source_locks.build_source_closure()
    assert closure["pass"] is True
    assert (closure["git_count"], closure["remote_count"], closure["logical_count"]) == (87, 2, 89)
    git = closure["git"]
    assert git["group_sizes"] == source_locks.EXPECTED_GROUP_SIZES
    assert git["group_digests"] == source_locks.EXPECTED_GROUP_DIGESTS
    assert git["all_git_source_digest"] == source_locks.EXPECTED_ALL_GIT_SOURCE_DIGEST
    assert git["release_identity_pass"] is True
    assert git["live_identity_pass"] is True
    assert closure["logical_source_digest"] == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
    assert closure["logical_digest_pass"] is True


def test_remote_objects_and_pretty_locks_are_exact() -> None:
    remote = source_locks.build_remote_source_locks()
    assert remote["pass"] is True
    assert remote["source_keys"] == [
        "johnston-yang-arxiv-2204.01980v2",
        "maynard-annals-2015-small-gaps",
    ]
    assert remote["canonical_digests"] == [
        source_locks.JY_CANONICAL_SHA256,
        source_locks.MAYNARD_CANONICAL_SHA256,
    ]
    assert remote["local_lock_blob_digests"] == [
        source_locks.JY_LOCK_BLOB_SHA256,
        source_locks.MAYNARD_LOCK_BLOB_SHA256,
    ]
    assert remote["local_lock_objects_exact_pass"] is True
    assert remote["network_fetch_performed"] is False
    assert remote["external_payload_hash_hits"] == []
    assert remote["redistributable_in_release"] is False


def test_local_pretty_locks_equal_released_rh388_blobs() -> None:
    for relative, local_name in zip(
        source_locks.PRIOR_EXTERNAL_LOCKS,
        ("external_source_lock.json", "maynard_external_source_lock.json"),
    ):
        released = source_locks.git_blob(
            source_locks.RH388_RELEASE,
            f"{source_locks.RH388_DIRECTORY}/{relative}",
        )
        assert released == (source_locks.ROOT / "results" / local_name).read_bytes()


def test_release_commit_and_digest_rebinding_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(ValueError, match="release commit was rebound"):
        source_locks.build_git_source_locks(commit="0" * 40)
    monkeypatch.setattr(source_locks, "EXPECTED_ALL_GIT_SOURCE_DIGEST", "0" * 64)
    assert source_locks.build_git_source_locks()["pass"] is False


def test_remote_and_logical_digest_rebinding_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(source_locks, "JY_CANONICAL_SHA256", "0" * 64)
    assert source_locks.build_remote_source_locks()["pass"] is False
    monkeypatch.undo()
    monkeypatch.setattr(source_locks, "EXPECTED_LOGICAL_SOURCE_DIGEST", "0" * 64)
    closure = source_locks.build_source_closure()
    assert closure["logical_digest_pass"] is False
    assert closure["pass"] is False


def test_malformed_sealed_constants_raise(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(source_locks, "MAYNARD_CANONICAL_SHA256", "not-64-hex")
    with pytest.raises(ValueError, match="malformed"):
        source_locks.build_source_closure()


def test_payload_scanner_detects_a_forbidden_hash(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    payload = tmp_path / "payload.bin"
    payload.write_bytes(b"forbidden-payload-fixture")
    payload_sha = sha256(payload.read_bytes()).hexdigest()
    monkeypatch.setattr(source_locks, "ROOT", tmp_path)
    monkeypatch.setattr(source_locks, "REMOTE_PAYLOAD_HASHES", {payload_sha})
    assert source_locks._remote_payload_hits() == ["payload.bin"]


def test_source_digest_rows_reject_duplicate_and_unsafe_paths() -> None:
    row = {
        "group": "g",
        "commit": source_locks.RH388_RELEASE,
        "path": "prime_dynamics_theory/papers/a",
        "sha256": "0" * 64,
    }
    with pytest.raises(ValueError, match="duplicate"):
        source_locks.source_digest_lines([row, dict(row)])
    unsafe = dict(row, path="prime_dynamics_theory/../RH_HANDOFF.md")
    with pytest.raises(ValueError, match="unsafe"):
        source_locks.source_digest_lines([unsafe])
