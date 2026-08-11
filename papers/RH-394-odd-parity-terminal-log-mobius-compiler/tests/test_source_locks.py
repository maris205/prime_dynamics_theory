from copy import deepcopy
from pathlib import Path

import pytest

import source_locks as locks


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise AssertionError(message)


def test_runtime_require_is_not_optimization_stripped() -> None:
    with pytest.raises(AssertionError, match="runtime sentinel"):
        require(False, "runtime sentinel")


def test_exact_128_plus_4_source_closure() -> None:
    require(locks.SOURCE_RELEASE == "6fed36f44183a2794a3a814493ff602c5dc9314b", "release")
    require(
        locks.SOURCE_DIRECTORY == "papers/RH-393-two-odd-factor-terminal-log-mobius-compiler",
        "source directory",
    )
    require(
        locks.SOURCE_RESULT_SHA256 == "69ebe2e157f5152d52aac5a478d1dd2ee2abde1dc672ad20941505d7e3a48aea",
        "source result",
    )
    require(locks.STANDARD8 == (
        "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
        "references.bib", "results/result.json", "results/result.schema.json",
        "src/two_odd_compiler/core.py",
    ), "standard8")
    require(locks.PRIOR_EXTERNAL_LOCKS == (
        "results/external_source_lock.json", "results/maynard_external_source_lock.json",
        "results/tao_external_source_lock.json",
    ), "prior locks")
    closure = locks.build_source_closure()
    require(closure["pass"] is True, "closure pass")
    require(
        (closure["git_count"], closure["remote_count"], closure["logical_count"]) == (128, 4, 132),
        "closure counts",
    )
    require(closure["git"]["group_sizes"] == {
        "rh393_immutable_closure": 117,
        "rh393_standard8": 8,
        "rh393_prior_external_locks": 3,
    }, "group sizes")
    require(closure["git"]["group_digests"] == locks.EXPECTED_GROUP_DIGESTS, "group digests")
    require(
        closure["git"]["all_git_source_digest"] == locks.EXPECTED_ALL_GIT_SOURCE_DIGEST,
        "all Git digest",
    )
    require(closure["git"]["path_unique_count"] == 128, "path uniqueness")
    require(
        closure["logical_source_digest"] == locks.EXPECTED_LOGICAL_SOURCE_DIGEST,
        "logical digest",
    )
    require(
        closure["direct_predecessor"]["role"] == "direct_RH393_odd_support_at_most_two_predecessor",
        "predecessor role",
    )


def test_remote_locks_are_offline_exact_rights_scoped_and_payload_free() -> None:
    remote = locks.build_remote_source_locks()
    require(remote["pass"] is True, "remote pass")
    require(remote["network_fetch_performed"] is False, "offline build")
    require(remote["offline_configuration_pass"] is True, "offline configuration")
    require(remote["external_payload_hash_hits"] == [], "payload exclusion")
    require(remote["canonical_digests"] == [
        locks.JY_CANONICAL_SHA256, locks.MAYNARD_CANONICAL_SHA256,
        locks.TAO_CANONICAL_SHA256, locks.TAO_TERAVAINEN_CANONICAL_SHA256,
    ], "canonical identities")
    require(remote["local_lock_blob_digests"] == [
        locks.JY_LOCK_BLOB_SHA256, locks.MAYNARD_LOCK_BLOB_SHA256,
        locks.TAO_LOCK_BLOB_SHA256, locks.TAO_TERAVAINEN_LOCK_BLOB_SHA256,
    ], "pretty identities")
    require(remote["source_keys"] == list(locks.EXPECTED_REMOTE_KEYS), "remote keys")
    require(remote["source_roles"] == locks.EXPECTED_REMOTE_ROLES, "remote roles")
    require(remote["redistributable_in_release"] == [False, False, True, False], "rights")
    require(remote["local_lock_objects_exact_pass"] is True, "inherited objects")
    require(remote["local_release_copies_byte_exact_pass"] is True, "inherited bytes")
    require(remote["direct_lock_sealed_pass"] is True, "direct lock")


def test_inherited_pretty_locks_are_byte_identical_and_direct_lock_is_sealed() -> None:
    for name in locks.PRIOR_EXTERNAL_LOCKS:
        local = locks.ROOT / name
        inherited = locks.WORKSPACE / "prime_dynamics_theory" / locks.SOURCE_DIRECTORY / name
        require(local.read_bytes() == inherited.read_bytes(), f"inherited lock bytes: {name}")
    direct = locks.ROOT / "results" / "tao_teravainen_external_source_lock.json"
    require(locks.digest(direct) == locks.TAO_TERAVAINEN_LOCK_BLOB_SHA256, "TT pretty lock")
    obj = locks.loads_strict(direct.read_text(encoding="utf-8"))
    require(
        locks.digest_bytes(locks.canonical_json_bytes(obj)) == locks.TAO_TERAVAINEN_CANONICAL_SHA256,
        "TT canonical lock",
    )
    require(obj["arxiv_id_version"] == "1708.02610v2", "TT version")
    require([locator["label"] for locator in obj["locators"]] == [
        "Corollary 1.8", "Remark 1.5", "Theorem A.1",
    ], "TT locators")


def test_release_commit_rebinding_and_exact_types_fail_closed() -> None:
    with pytest.raises(ValueError, match="rebound"):
        locks.build_git_source_locks(commit="0" * 40)
    with pytest.raises(ValueError, match="rebound"):
        locks.build_git_source_locks(commit=True)
    with pytest.raises(TypeError):
        locks.digest_bytes("not bytes")
    with pytest.raises(TypeError):
        locks.digest("not a path")
    with pytest.raises(ValueError, match="duplicate JSON key"):
        locks.loads_strict('{"source_key":"a","source_key":"b"}')
    require(locks.canonical_json_bytes({"accent": "Teräväinen"}) == (
        '{"accent":"Teräväinen"}'.encode("utf-8")
    ), "source canonical form")
    with pytest.raises(ValueError):
        locks.source_digest_lines([
            {"group": "g", "commit": locks.SOURCE_RELEASE, "path": "bad", "sha256": "0" * 64}
        ])


def test_coordinated_source_rebinding_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(locks, "SOURCE_RELEASE", "10ad608f5487af3d2497adfbe226ded4f37e64a3")
    monkeypatch.setattr(locks, "EXPECTED_GROUP_DIGESTS", {
        "rh393_immutable_closure": "8e31632e91e96b5b884d08943363bce2a7a8d92b298528de7ff23a8b3029ee7f",
        "rh393_standard8": "ba0b7e659b29c0e9e7dedcf1e93b14e7d58ead31382f316f8f3f29b0b27cb289",
        "rh393_prior_external_locks": "791f173e5c8c78d1d90b48c09964269802f8bf169686855016b559cf1d255a40",
    })
    monkeypatch.setattr(
        locks, "EXPECTED_ALL_GIT_SOURCE_DIGEST",
        "313a863180b50534b563f9354ec86d2e214e0cc637c2be102ba37fe72b6a9cc2",
    )
    monkeypatch.setattr(
        locks, "EXPECTED_LOGICAL_SOURCE_DIGEST",
        "ca9662b56597293353862de580669ee2c7c2b9adceec1e5dbbb54c6323eb24b9",
    )
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_git_source_locks(commit=locks.SOURCE_RELEASE)


def test_group_digest_and_inherited_remote_object_mutations_fail(monkeypatch: pytest.MonkeyPatch) -> None:
    wrong_groups = dict(locks.EXPECTED_GROUP_DIGESTS)
    wrong_groups["rh393_standard8"] = "0" * 64
    monkeypatch.setattr(locks, "EXPECTED_GROUP_DIGESTS", wrong_groups)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_git_source_locks()
    monkeypatch.undo()

    released = deepcopy(locks.released_source_result())
    released["source_locks"]["remote"]["objects"][0]["pages"] += 1
    monkeypatch.setattr(locks, "released_source_result", lambda: released)
    require(locks.build_remote_source_locks()["pass"] is False, "remote mutation")


def test_direct_remote_digest_and_role_mutations_fail(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(locks, "TAO_TERAVAINEN_CANONICAL_SHA256", "0" * 64)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_remote_source_locks()
    monkeypatch.undo()
    roles = dict(locks.EXPECTED_REMOTE_ROLES)
    roles["tao-teravainen-arxiv-1708.02610v2"] = "closure_only"
    monkeypatch.setattr(locks, "EXPECTED_REMOTE_ROLES", roles)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_remote_source_locks()


def test_remote_payload_membership_is_exact(monkeypatch: pytest.MonkeyPatch) -> None:
    original = locks.REMOTE_PAYLOAD_HASHES
    deleted = frozenset(sorted(original)[1:])
    monkeypatch.setattr(locks, "REMOTE_PAYLOAD_HASHES", deleted)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_remote_source_locks()
    monkeypatch.undo()
    monkeypatch.setattr(locks, "REMOTE_PAYLOAD_HASHES", original | {"0" * 64})
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_remote_source_locks()


def test_source_module_has_no_network_client_dependency() -> None:
    text = Path(locks.__file__).read_text(encoding="utf-8")
    require("import requests" not in text, "requests dependency")
    require("urllib.request" not in text, "urllib dependency")
    require('network_fetch_performed": True' not in text, "network claim")
