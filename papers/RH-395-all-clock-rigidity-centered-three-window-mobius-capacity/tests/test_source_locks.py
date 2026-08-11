from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path

import pytest

import source_locks as locks


RH394_RELEASE = "6b3d616851cd2d7cba66371d0aa9f25b8e8bf2f7"
RH394_DIRECTORY = "papers/RH-394-odd-parity-terminal-log-mobius-compiler"
RH394_RESULT = "935de4967e504e5c32f6d27980ec044c3cffccfbab534440730470de8b1ae610"
RH375_RELEASE = "071fed1b2a5d8488b9d2e35a99a753953b233584"
RH375_DIRECTORY = "papers/RH-375-all-clock-one-site-mobius-capacity-supremum"
RH394_STANDARD8 = (
    "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
    "references.bib", "results/result.json", "results/result.schema.json",
    "src/odd_parity_compiler/core.py",
)
RH375_STANDARD8 = (
    "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
    "references.bib", "results/result.json", "results/result.schema.json",
    "src/all_clock_capacity/core.py",
)
RH375_BLOBS = {
    "README.md": ("4949823c38e81dce9b04d46405a7a1d1bbd156375d2332f9a9ea90a7b8927c11", 2612),
    "THEOREM_LEDGER.md": ("93afb2db541ca58cf563d4ba7bed06634f5d3be77e9059c11498d6e83c417ec8", 1912),
    "UPDATED_ROADMAP.md": ("678ffa5ed6ca5a44070e0cf4e3c0634e1507154c0a9410d68599ab7d5b934432", 1237),
    "main.tex": ("7d96987b0236d2788a781565bc03195c59ad2b72d07f1ff8988f8a3fef4a5117", 16125),
    "references.bib": ("67939f140d06425e110258cc982dc8d5af0888899bd9d29a5dc8bfbaef7505be", 1620),
    "results/result.json": ("81d905c2476abc36fdd1ab0e468ad33d85f4df9db35afbd3bc79bf0771fe0a08", 18515),
    "results/result.schema.json": ("5d570cfc9515de8953e18eaf78176934c81bf479d741172e5a602a2d1839ba02", 629),
    "src/all_clock_capacity/core.py": ("575a5d2371f1bc0d29b33bc15e983f3e41c9b5b9ceb60d97369a1ef73f51a694", 16962),
}
GROUP_SIZES = {
    "rh394_immutable_closure": 128,
    "rh394_standard8": 8,
    "rh394_prior_external_locks": 4,
    "rh375_direct_all_clock_release8": 8,
}
GROUP_DIGESTS = {
    "rh394_immutable_closure": "0a44007f1e5888ed9b1cc6eae380b25fec38e17fe7e4329594625538d36c579b",
    "rh394_standard8": "cab0bfbc807eb5ed2e8c85435a3348fb48d823327a77c740dc281c195fed9e47",
    "rh394_prior_external_locks": "e9d259e020d0bef964630388a58487efcdc0a48ee895a6c335f35d0269f6d7e2",
    "rh375_direct_all_clock_release8": "14ef15bf6df11e32a05925e5a103c8e2d16ed26abb62620153f9387d84c840ce",
}
ALL_GIT = "9b5e0c04bb3189ddcb802ccb65d5f6b3cc8aa081000acd9fa781fd9f81e50ec9"
LOGICAL = "5c4b81ea2f7bdd661fe4374d1174ef3a1909a8327d5982aa01510e4201340bd3"
REMOTE_KEYS = (
    "johnston-yang-arxiv-2204.01980v2",
    "maynard-annals-2015-small-gaps",
    "tao-cambridge-2016-logarithmic-chowla",
    "tao-teravainen-arxiv-1708.02610v2",
)
REMOTE_CANONICAL = (
    "d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786",
    "bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e",
    "d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84",
    "a1448fb540b6f8fcf17cace1ff7d7218a6126cb3265699bbd43c444fcc558058",
)
REMOTE_PRETTY = (
    "d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058",
    "9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba",
    "825b3455be5eac151b7478f537fa6c503ae8eb02004cd8da821ca802d4ebdd8f",
    "52ade551d8bef9aa35e850d03cefede1239cb9611b9211fdcda522f02fb501ec",
)
REMOTE_ROLES = {
    "johnston-yang-arxiv-2204.01980v2": "inherited_closure_only_via_RH394",
    "maynard-annals-2015-small-gaps": "inherited_closure_only_via_RH394",
    "tao-cambridge-2016-logarithmic-chowla": "inherited_two_point_provenance_via_RH394",
    "tao-teravainen-arxiv-1708.02610v2": "inherited_odd_parity_input_via_RH394",
}
PAYLOADS = frozenset({
    "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2",
    "572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd",
    "2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602",
    "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349",
    "a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2",
    "232bdb1ad6e46789bfc124a589d6c3afda803eaf3ba2f93278fc31be3aa276ad",
})


def require(condition: object, message: str = "requirement failed") -> None:
    if condition is not True:
        raise RuntimeError(message)


def test_runtime_require_is_not_optimization_stripped() -> None:
    with pytest.raises(RuntimeError, match="runtime sentinel"):
        require(False, "runtime sentinel")


def test_exact_148_plus_4_source_closure() -> None:
    require(locks.SOURCE_RELEASE == RH394_RELEASE, "RH394 release")
    require(locks.SOURCE_DIRECTORY == RH394_DIRECTORY, "RH394 directory")
    require(locks.SOURCE_RESULT_SHA256 == RH394_RESULT, "RH394 result")
    require(locks.STANDARD8 == RH394_STANDARD8, "RH394 standard8")
    require(locks.RH375_RELEASE == RH375_RELEASE, "RH375 release")
    require(locks.RH375_DIRECTORY == RH375_DIRECTORY, "RH375 directory")
    require(locks.RH375_STANDARD8 == RH375_STANDARD8, "RH375 standard8")
    closure = locks.build_source_closure()
    require(closure["pass"] is True, "closure pass")
    require(
        tuple(closure[key] for key in ("git_count", "remote_count", "logical_count"))
        == (148, 4, 152),
        "closure counts",
    )
    git = closure["git"]
    require(git["group_sizes"] == GROUP_SIZES, "group sizes")
    require(git["group_digests"] == GROUP_DIGESTS, "group digests")
    require(git["all_git_source_digest"] == ALL_GIT, "all Git digest")
    require(type(git["path_unique_count"]) is int and git["path_unique_count"] == 148)
    require(closure["logical_source_digest"] == LOGICAL, "logical digest")
    require(closure["logical_digest_pass"] is True, "logical pass")
    require(
        closure["direct_predecessors"]["rh394_terminal_log"]["role"]
        == "direct_terminal_log_three_shift_table_law_and_phase_densities",
        "RH394 role",
    )
    endpoint = closure["direct_predecessors"]["rh375_one_site_endpoint"]
    require(endpoint["terminal_clock_analytic_input"] is False, "RH375 firewall")
    require("combinatorics_only" in endpoint["role"], "RH375 role")


def test_group_order_commits_and_paths_are_exact() -> None:
    entries = locks.build_git_source_locks()["entries"]
    require(type(entries) is list and len(entries) == 148)
    offsets = (0, 128, 136, 140, 148)
    labels = tuple(GROUP_SIZES)
    for label, start, stop in zip(labels, offsets, offsets[1:]):
        rows = entries[start:stop]
        require(len(rows) == GROUP_SIZES[label], label)
        require(all(row["group"] == label for row in rows), label)
    require(all(row["commit"] == RH394_RELEASE for row in entries[:140]))
    require(all(row["commit"] == RH375_RELEASE for row in entries[140:]))
    expected_tail = [
        f"prime_dynamics_theory/{RH375_DIRECTORY}/{relative}"
        for relative in RH375_STANDARD8
    ]
    require([row["path"] for row in entries[140:]] == expected_tail)


def test_rh375_release_manifest_and_eight_blob_literals() -> None:
    raw_manifest = locks.git_blob(
        RH375_RELEASE, f"{RH375_DIRECTORY}/results/dependency_manifest.json"
    )
    manifest = locks.loads_strict(raw_manifest.decode("utf-8"))
    require(type(manifest) is dict and manifest["status"] == "RH-375_fixed_publication_manifest")
    require(type(manifest["publication_artifacts"]) is dict)
    require(all(relative in manifest["publication_artifacts"] for relative in RH375_STANDARD8))
    require(tuple(RH375_BLOBS) == RH375_STANDARD8)
    for relative, (expected_sha, expected_bytes) in RH375_BLOBS.items():
        blob = locks.git_blob(RH375_RELEASE, f"{RH375_DIRECTORY}/{relative}")
        require(len(blob) == expected_bytes, relative)
        require(locks.digest_bytes(blob) == expected_sha, relative)
        require(manifest["publication_artifacts"][relative] == expected_sha, relative)


def test_remote_locks_are_offline_exact_rights_scoped_and_payload_free() -> None:
    remote = locks.build_remote_source_locks()
    require(remote["pass"] is True, "remote pass")
    require(remote["network_fetch_performed"] is False, "offline build")
    require(remote["offline_configuration_pass"] is True, "offline configuration")
    require(remote["external_payload_hash_hits"] == [], "payload exclusion")
    require(remote["canonical_digests"] == list(REMOTE_CANONICAL), "canonical identities")
    require(remote["local_lock_blob_digests"] == list(REMOTE_PRETTY), "pretty identities")
    require(remote["source_keys"] == list(REMOTE_KEYS), "remote keys")
    require(remote["source_roles"] == REMOTE_ROLES, "remote roles")
    require(remote["redistributable_in_release"] == [False, False, True, False], "rights")
    require(remote["local_lock_objects_exact_pass"] is True, "inherited objects")
    require(remote["local_release_copies_byte_exact_pass"] is True, "inherited bytes")
    require(remote["all_lock_literals_sealed_pass"] is True, "lock literals")
    require(locks.REMOTE_PAYLOAD_HASHES == PAYLOADS and len(PAYLOADS) == 6)


def test_all_pretty_locks_are_release_exact_and_tt_locators_are_sealed() -> None:
    for relative, expected_sha in zip(locks.LOCAL_EXTERNAL_LOCKS, REMOTE_PRETTY):
        local = locks.ROOT / relative
        released = locks.git_blob(RH394_RELEASE, f"{RH394_DIRECTORY}/{relative}")
        require(local.read_bytes() == released, relative)
        require(locks.digest(local) == expected_sha, relative)
    direct = locks.ROOT / "results" / "tao_teravainen_external_source_lock.json"
    obj = locks.loads_strict(direct.read_text(encoding="utf-8"))
    require(locks.digest_bytes(locks.canonical_json_bytes(obj)) == REMOTE_CANONICAL[3])
    require(obj["arxiv_id_version"] == "1708.02610v2")
    require([locator["label"] for locator in obj["locators"]] == [
        "Corollary 1.8", "Remark 1.5", "Theorem A.1",
    ])


def test_release_commit_rebinding_and_exact_types_fail_closed() -> None:
    for kwargs in ({"commit": "0" * 40}, {"commit": True}, {"rh375_commit": "0" * 40}, {"rh375_commit": True}):
        with pytest.raises(ValueError, match="rebound"):
            locks.build_git_source_locks(**kwargs)
    with pytest.raises(TypeError):
        locks.digest_bytes("not bytes")
    with pytest.raises(TypeError):
        locks.digest("not a path")
    with pytest.raises(ValueError, match="duplicate JSON key"):
        locks.loads_strict('{"source_key":"a","source_key":"b"}')
    require(
        locks.canonical_json_bytes({"accent": "Teräväinen"})
        == '{"accent":"Teräväinen"}'.encode("utf-8")
    )
    with pytest.raises(ValueError):
        locks.source_digest_lines([
            {"group": "g", "commit": RH394_RELEASE, "path": "bad", "sha256": "0" * 64}
        ])


def test_coordinated_constant_and_comparator_rebinding_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(locks, "SOURCE_RELEASE", "0" * 40)
    monkeypatch.setattr(locks, "RH375_RELEASE", "1" * 40)
    monkeypatch.setattr(locks, "EXPECTED_GROUP_SIZES", dict(GROUP_SIZES))
    monkeypatch.setattr(locks, "EXPECTED_GROUP_DIGESTS", dict(GROUP_DIGESTS))
    monkeypatch.setattr(locks, "EXPECTED_ALL_GIT_SOURCE_DIGEST", ALL_GIT)
    monkeypatch.setattr(locks, "EXPECTED_LOGICAL_SOURCE_DIGEST", LOGICAL)
    monkeypatch.setattr(locks, "exact_equal", lambda left, right: True)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_git_source_locks(commit=locks.SOURCE_RELEASE, rh375_commit=locks.RH375_RELEASE)


def test_group_path_and_rh375_blob_mutations_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    groups = dict(locks.EXPECTED_GROUP_DIGESTS)
    groups["rh375_direct_all_clock_release8"] = "0" * 64
    monkeypatch.setattr(locks, "EXPECTED_GROUP_DIGESTS", groups)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_git_source_locks()
    monkeypatch.undo()
    monkeypatch.setattr(locks, "RH375_STANDARD8", tuple(reversed(RH375_STANDARD8)))
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_git_source_locks()
    monkeypatch.undo()
    hashes = dict(locks.RH375_STANDARD8_SHA256)
    hashes["main.tex"] = "0" * 64
    monkeypatch.setattr(locks, "RH375_STANDARD8_SHA256", hashes)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_git_source_locks()


def test_inherited_remote_object_digest_role_and_payload_mutations_fail(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    released = deepcopy(locks.released_source_result())
    released["source_locks"]["remote"]["objects"][3]["pages"] += 1
    monkeypatch.setattr(locks, "released_source_result", lambda: released)
    require(locks.build_remote_source_locks()["pass"] is False, "remote mutation")
    monkeypatch.undo()
    monkeypatch.setattr(locks, "TAO_TERAVAINEN_CANONICAL_SHA256", "0" * 64)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_remote_source_locks()
    monkeypatch.undo()
    roles = dict(locks.EXPECTED_REMOTE_ROLES)
    roles[REMOTE_KEYS[3]] = "direct"
    monkeypatch.setattr(locks, "EXPECTED_REMOTE_ROLES", roles)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_remote_source_locks()
    monkeypatch.undo()
    monkeypatch.setattr(locks, "REMOTE_PAYLOAD_HASHES", PAYLOADS | {"0" * 64})
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_remote_source_locks()


def test_digest_and_git_blob_helper_bombs_do_not_self_certify(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(locks, "digest", lambda path: "0" * 64)
    require(locks.build_git_source_locks()["pass"] is False, "digest bomb")
    monkeypatch.undo()
    locks.released_source_result.cache_clear()
    monkeypatch.setattr(locks, "digest_bytes", lambda data: "0" * 64)
    with pytest.raises(RuntimeError, match="released source result digest"):
        locks.build_git_source_locks()


def test_source_module_has_no_network_client_or_bare_assert() -> None:
    text = Path(locks.__file__).read_text(encoding="utf-8")
    require("import requests" not in text, "requests dependency")
    require("urllib.request" not in text, "urllib dependency")
    require('network_fetch_performed": True' not in text, "network claim")
    for path in (Path(__file__), Path(locks.__file__)):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), str(path))
