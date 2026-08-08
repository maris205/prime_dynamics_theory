from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

import source_locks  # noqa: E402


def test_source_closure_is_exact_95_git_plus_three_remote() -> None:
    closure = source_locks.build_source_closure()
    assert closure["pass"] is True
    assert (closure["git_count"], closure["remote_count"], closure["logical_count"]) == (95, 3, 98)
    assert closure["logical_source_digest"] == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
    assert closure["logical_digest_pass"] is True
    git = closure["git"]
    assert git["group_sizes"] == source_locks.EXPECTED_GROUP_SIZES
    assert git["group_digests"] == source_locks.EXPECTED_GROUP_DIGESTS
    assert git["all_git_source_digest"] == source_locks.EXPECTED_ALL_GIT_SOURCE_DIGEST
    assert git["release_identity_pass"] is True
    assert git["live_identity_pass"] is True
    assert len(git["entries"]) == 95


def test_remote_objects_are_ordered_exact_and_local_copies_are_locked() -> None:
    remote = source_locks.build_remote_source_locks()
    assert remote["pass"] is True
    assert remote["source_keys"] == [
        "johnston-yang-arxiv-2204.01980v2",
        "maynard-annals-2015-small-gaps",
        "tao-cambridge-2016-logarithmic-chowla",
    ]
    assert remote["canonical_digests"] == [
        source_locks.JY_CANONICAL_SHA256,
        source_locks.MAYNARD_CANONICAL_SHA256,
        source_locks.TAO_CANONICAL_SHA256,
    ]
    assert remote["local_lock_blob_digests"] == [
        source_locks.JY_LOCK_BLOB_SHA256,
        source_locks.MAYNARD_LOCK_BLOB_SHA256,
        source_locks.TAO_LOCK_BLOB_SHA256,
    ]
    assert remote["local_lock_objects_exact_pass"] is True
    assert remote["local_release_copies_byte_exact_pass"] is True
    assert remote["redistributable_in_release"] == [False, False, True]
    assert remote["external_payload_hash_hits"] == []
    assert remote["external_payload_exclusion_pass"] is True


def test_release_commits_and_git_digests_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(ValueError, match="RH-388"):
        source_locks.build_git_source_locks(rh388_commit="0" * 40)
    with pytest.raises(ValueError, match="TPC-137"):
        source_locks.build_git_source_locks(tpc137_commit="0" * 40)
    monkeypatch.setattr(source_locks, "EXPECTED_ALL_GIT_SOURCE_DIGEST", "0" * 64)
    assert source_locks.build_git_source_locks()["pass"] is False
    assert source_locks.build_source_closure()["pass"] is False


def test_remote_canonical_pretty_and_logical_rebinding_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(source_locks, "TAO_CANONICAL_SHA256", "0" * 64)
    assert source_locks.build_remote_source_locks()["pass"] is False
    assert source_locks.build_source_closure()["pass"] is False
    monkeypatch.undo()
    monkeypatch.setattr(source_locks, "EXPECTED_LOGICAL_SOURCE_DIGEST", "0" * 64)
    closure = source_locks.build_source_closure()
    assert closure["logical_digest_pass"] is False
    assert closure["pass"] is False


def test_source_row_membership_duplicates_and_exact_types_fail_closed() -> None:
    good = [{"group": "g", "commit": "0" * 40, "path": "prime_dynamics_theory/papers/a", "sha256": "1" * 64}]
    assert len(source_locks.source_digest_lines(good)) == 1
    for candidate in (
        [{**good[0], "extra": 1}],
        [good[0], good[0]],
        [{**good[0], "sha256": True}],
    ):
        with pytest.raises((TypeError, ValueError)):
            source_locks.source_digest_lines(candidate)


def test_source_closure_matches_optimized_mode() -> None:
    code = (
        "import json,sys;"
        f"sys.path.insert(0,{str(ROOT / 'experiments')!r});"
        "import source_locks;"
        "print(json.dumps(source_locks.build_source_closure(),sort_keys=True,separators=(',',':')))"
    )
    completed = subprocess.run(
        [sys.executable, "-OO", "-c", code],
        cwd=ROOT,
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout) == source_locks.build_source_closure()
