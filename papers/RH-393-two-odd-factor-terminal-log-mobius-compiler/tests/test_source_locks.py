from copy import deepcopy
from pathlib import Path

import pytest

import source_locks as locks


def test_exact_117_plus_3_source_closure() -> None:
    assert locks.SOURCE_RELEASE == "9768c1cb5f56d959406c19119315afd542b6c30f"
    assert locks.SOURCE_DIRECTORY == "papers/RH-392-fixed-lag-terminal-log-mobius-capacity-landscape"
    assert locks.SOURCE_RESULT_SHA256 == "83bab4eb57f1d4d2d31c646946df16203b155d49d78942f74a40df239e404bc0"
    assert locks.STANDARD8 == (
        "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
        "references.bib", "results/result.json", "results/result.schema.json",
        "src/fixed_lag_capacity/core.py",
    )
    assert locks.PRIOR_EXTERNAL_LOCKS == (
        "results/external_source_lock.json", "results/maynard_external_source_lock.json",
        "results/tao_external_source_lock.json",
    )
    closure = locks.build_source_closure()
    assert closure["pass"] is True
    assert (closure["git_count"], closure["remote_count"], closure["logical_count"]) == (117, 3, 120)
    assert closure["git"]["group_sizes"] == {
        "rh392_immutable_closure": 106,
        "rh392_standard8": 8,
        "rh392_prior_external_locks": 3,
    }
    assert closure["git"]["group_digests"] == locks.EXPECTED_GROUP_DIGESTS
    assert closure["git"]["all_git_source_digest"] == locks.EXPECTED_ALL_GIT_SOURCE_DIGEST
    assert closure["git"]["path_unique_count"] == 117
    assert closure["logical_source_digest"] == locks.EXPECTED_LOGICAL_SOURCE_DIGEST


def test_remote_locks_are_offline_exact_and_payload_free() -> None:
    remote = locks.build_remote_source_locks()
    assert remote["pass"] is True
    assert remote["network_fetch_performed"] is False
    assert remote["external_payload_hash_hits"] == []
    assert remote["canonical_digests"] == [
        locks.JY_CANONICAL_SHA256, locks.MAYNARD_CANONICAL_SHA256, locks.TAO_CANONICAL_SHA256,
    ]
    assert remote["local_lock_blob_digests"] == [
        locks.JY_LOCK_BLOB_SHA256, locks.MAYNARD_LOCK_BLOB_SHA256, locks.TAO_LOCK_BLOB_SHA256,
    ]
    assert remote["local_lock_objects_exact_pass"] is True
    assert remote["local_release_copies_byte_exact_pass"] is True


def test_pretty_locks_are_byte_identical_to_released_copies() -> None:
    names = ("external_source_lock.json", "maynard_external_source_lock.json", "tao_external_source_lock.json")
    for name in names:
        local = locks.ROOT / "results" / name
        inherited = locks.WORKSPACE / "prime_dynamics_theory" / locks.SOURCE_DIRECTORY / "results" / name
        assert local.read_bytes() == inherited.read_bytes()


def test_release_commit_rebinding_and_exact_types_fail_closed() -> None:
    with pytest.raises(ValueError, match="rebound"):
        locks.build_git_source_locks(commit="0" * 40)
    with pytest.raises(ValueError, match="rebound"):
        locks.build_git_source_locks(commit=True)
    with pytest.raises(TypeError):
        locks.digest_bytes("not bytes")
    with pytest.raises(TypeError):
        locks.digest("not a path")
    with pytest.raises(ValueError):
        locks.source_digest_lines([] + [{"group": "g", "commit": locks.SOURCE_RELEASE, "path": "bad", "sha256": "0" * 64}])


def test_group_digest_and_remote_object_mutations_fail(monkeypatch: pytest.MonkeyPatch) -> None:
    wrong_groups = dict(locks.EXPECTED_GROUP_DIGESTS)
    wrong_groups["rh392_standard8"] = "0" * 64
    monkeypatch.setattr(locks, "EXPECTED_GROUP_DIGESTS", wrong_groups)
    assert locks.build_git_source_locks()["pass"] is False
    monkeypatch.undo()

    released = deepcopy(locks.released_source_result())
    released["source_locks"]["remote"]["objects"][0]["pages"] += 1
    monkeypatch.setattr(locks, "released_source_result", lambda: released)
    assert locks.build_remote_source_locks()["pass"] is False


def test_remote_payload_membership_is_exact(monkeypatch: pytest.MonkeyPatch) -> None:
    original = locks.REMOTE_PAYLOAD_HASHES
    deleted = frozenset(sorted(original)[1:])
    monkeypatch.setattr(locks, "REMOTE_PAYLOAD_HASHES", deleted)
    with pytest.raises(ValueError, match="membership"):
        locks.build_remote_source_locks()
    monkeypatch.undo()
    monkeypatch.setattr(locks, "REMOTE_PAYLOAD_HASHES", original | {"0" * 64})
    with pytest.raises(ValueError, match="membership"):
        locks.build_remote_source_locks()


def test_source_module_has_no_network_client_dependency() -> None:
    text = Path(locks.__file__).read_text(encoding="utf-8")
    assert "import requests" not in text
    assert "urllib.request" not in text
    assert "network_fetch_performed\": True" not in text
