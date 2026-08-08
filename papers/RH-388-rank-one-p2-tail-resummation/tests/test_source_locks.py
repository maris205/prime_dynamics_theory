from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

import source_locks  # noqa: E402


def test_source_closure_is_exact_77_git_plus_two_remote() -> None:
    closure = source_locks.build_source_closure()
    assert closure["pass"] is True
    assert closure["git_count"] == 77
    assert closure["remote_count"] == 2
    assert closure["logical_count"] == 79
    assert closure["logical_source_digest"] == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
    assert closure["logical_digest_pass"] is True
    git = closure["git"]
    assert git["group_sizes"] == source_locks.EXPECTED_GROUP_SIZES
    assert git["group_digests"] == source_locks.EXPECTED_GROUP_DIGESTS
    assert git["all_git_source_digest"] == source_locks.EXPECTED_ALL_GIT_SOURCE_DIGEST
    assert git["release_identity_pass"] is True
    assert git["live_identity_pass"] is True
    assert len(git["entries"]) == 77


def test_remote_objects_are_ordered_exact_and_nonredistributable() -> None:
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
    assert remote["redistributable_in_release"] is False
    assert remote["local_lock_objects_exact_pass"] is True
    assert remote["local_lock_blob_digests"] == [
        source_locks.RH387_EXTERNAL_LOCK_BLOB_SHA256,
        source_locks.MAYNARD_LOCK_BLOB_SHA256,
    ]
    assert remote["network_fetch_performed"] is False
    assert remote["external_payload_exclusion_pass"] is True
    assert remote["external_payload_hash_hits"] == []


def test_release_commit_and_sealed_digest_rebinding_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(ValueError, match="rebound"):
        source_locks.build_git_source_locks(commit="0" * 40)
    monkeypatch.setattr(source_locks, "EXPECTED_ALL_GIT_SOURCE_DIGEST", "0" * 64)
    assert source_locks.build_git_source_locks()["pass"] is False
    assert source_locks.build_source_closure()["pass"] is False


def test_remote_and_logical_rebinding_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(source_locks, "MAYNARD_CANONICAL_SHA256", "0" * 64)
    assert source_locks.build_remote_source_locks()["pass"] is False
    assert source_locks.build_source_closure()["pass"] is False


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
    optimized = json.loads(completed.stdout)
    assert optimized == source_locks.build_source_closure()
