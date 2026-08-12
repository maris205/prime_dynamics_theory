from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

import pytest

import source_locks as locks


RH397_RELEASE = "dd63a109dcfa72365c749e0b183820d2611af733"
RH397_DIRECTORY = "papers/RH-397-odd-lag-half-span-overlap-mobius-capacity"
RH397_RESULT = "d21f3ab160c7cb5cfca1ff04ac7d2104ea8a7802b36eb3e2f07e32cbe1d27e4f"
RH396_RELEASE = "cd57086fa90939d56656c3f952a08ffad9aabefe"
RH396_DIRECTORY = "papers/RH-396-euler-run-spectrum-fixed-lag-centered-mobius-capacity"
RH394_RELEASE = "6b3d616851cd2d7cba66371d0aa9f25b8e8bf2f7"
RH394_DIRECTORY = "papers/RH-394-odd-parity-terminal-log-mobius-compiler"
RH392_RELEASE = "9768c1cb5f56d959406c19119315afd542b6c30f"
RH392_DIRECTORY = "papers/RH-392-fixed-lag-terminal-log-mobius-capacity-landscape"
RH395_RELEASE = "20de7202518f4488cbd9c7d63bf94aaa3dc94476"
RH395_DIRECTORY = "papers/RH-395-all-clock-rigidity-centered-three-window-mobius-capacity"
RH375_RELEASE = "071fed1b2a5d8488b9d2e35a99a753953b233584"
RH375_DIRECTORY = "papers/RH-375-all-clock-one-site-mobius-capacity-supremum"
STANDARD8 = (
    "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
    "references.bib", "results/result.json", "results/result.schema.json",
    "src/odd_lag_half_span_capacity/core.py",
)
STANDARD8_BLOBS = {
    "README.md": ("18ad513bb327e0c6460c105159fab2c2954cf52023706387c3f6402e95c4a763", 4191),
    "THEOREM_LEDGER.md": ("210263daa48fee1876e7632db9864dfa4b99422a78f1f2166057cd0d3dff1096", 5301),
    "UPDATED_ROADMAP.md": ("e68115ccbe8953828df78d3fd31f46eacd1fe1141abde7bbb2c243f14fd7b243", 2777),
    "main.tex": ("a0ded93cfcd46f48b602e3f276a39e01e99ba8c37d3961316540f3925064ec11", 27620),
    "references.bib": ("2ef184fbd1594af83c0a16fd8f868c3572d91d86c30d40f98271781ca0044b3b", 505),
    "results/result.json": (RH397_RESULT, 151768),
    "results/result.schema.json": ("4f16580a613e3e0c3930fd53e3a418023fac96e2cfa15f74ed447a60bea38f83", 670920),
    "src/odd_lag_half_span_capacity/core.py": ("4b247c0a580c06cfaeb22f29d5b9f80d52bee44fcb44ebd978153bc79e04bcd0", 75206),
}
PRIOR_LOCKS = (
    "results/external_source_lock.json", "results/maynard_external_source_lock.json",
    "results/tao_external_source_lock.json", "results/tao_teravainen_external_source_lock.json",
)
GROUP_SIZES = {
    "rh397_immutable_closure": 172,
    "rh397_standard8": 8,
    "rh397_prior_external_locks": 4,
}
GROUP_DIGESTS = {
    "rh397_immutable_closure": "fd2d749a09316b9c412780e61882e5f1ac050af609cd0a96c0d1aea79ac4c82d",
    "rh397_standard8": "eb7355565e8429765cb967192c00e261998147abb68fb0307517695621bdfd62",
    "rh397_prior_external_locks": "e044509ee377c35cea8642b67a75ca5dc4ba861f455228bde7341418791bce20",
}
ALL_GIT = "e7341caa25f0787a2e48a4d9c156e0d785b6c2a5516172bdfb25c2ac45377ea8"
LOGICAL = "4cc752fb7baae977bb15a9420101c5ed37727b1f3f7eecf72afce9dec3c73b13"
DIRECT_ROLE = "direct_release_and_provenance_predecessor_only"
RH396_ROLE = (
    "sole_load_bearing_theorem_and_analytic_endpoint_input_equations_18_21_"
    "Theorem_1_3_equation_22_Corollary_1_4_equation_23"
)
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
    REMOTE_KEYS[0]: "inherited_closure_only_via_RH394",
    REMOTE_KEYS[1]: "inherited_closure_only_via_RH394",
    REMOTE_KEYS[2]: "inherited_two_point_provenance_via_RH394",
    REMOTE_KEYS[3]: "inherited_odd_parity_input_via_RH394",
}
REMOTE_SEALS = (
    (REMOTE_KEYS[0], "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2", 278380, 22, False),
    (REMOTE_KEYS[1], "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349", 528115, 31, False),
    (REMOTE_KEYS[2], "a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2", 534086, 36, True),
    (REMOTE_KEYS[3], "232bdb1ad6e46789bfc124a589d6c3afda803eaf3ba2f93278fc31be3aa276ad", 398251, 41, False),
)
PAYLOADS = frozenset({
    "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2",
    "572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd",
    "2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602",
    "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349",
    "a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2",
    "232bdb1ad6e46789bfc124a589d6c3afda803eaf3ba2f93278fc31be3aa276ad",
})
SOURCE_ROLES = {
    "RH397": {
        "commit": RH397_RELEASE,
        "directory": RH397_DIRECTORY,
        "role": DIRECT_ROLE,
        "analytic_input": False,
    },
    "RH396": {
        "commit": RH396_RELEASE,
        "directory": RH396_DIRECTORY,
        "role": RH396_ROLE,
        "analytic_input": True,
    },
    "RH394": {
        "commit": RH394_RELEASE,
        "directory": RH394_DIRECTORY,
        "role": "transitive_fixed_distinct_three_shift_provenance_only_via_RH396",
        "analytic_input": False,
    },
    "RH392": {
        "commit": RH392_RELEASE,
        "directory": RH392_DIRECTORY,
        "role": "transitive_fixed_lag_comparison_only",
        "analytic_input": False,
    },
    "RH395": {
        "commit": RH395_RELEASE,
        "directory": RH395_DIRECTORY,
        "role": "transitive_relation_saturation_and_tropical_comparison_only",
        "analytic_input": False,
    },
    "RH375": {
        "commit": RH375_RELEASE,
        "directory": RH375_DIRECTORY,
        "role": "transitive_one_site_MWIS_and_square_clock_comparison_only",
        "analytic_input": False,
    },
}


def require(condition: object, message: str = "requirement failed") -> None:
    if condition is not True:
        raise RuntimeError(message)


def independent_lines_digest(rows: list[dict[str, object]]) -> str:
    require(type(rows) is list, "independent rows type")
    encoded = "".join(
        f"{row['group']}\t{row['commit']}\t{row['path']}\t{row['sha256']}\n"
        for row in rows
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def test_runtime_require_is_not_optimization_stripped() -> None:
    with pytest.raises(RuntimeError, match="runtime sentinel"):
        require(False, "runtime sentinel")


def test_exact_184_plus_4_source_closure_and_role_firewalls() -> None:
    require(locks.SOURCE_RELEASE == RH397_RELEASE, "RH397 release")
    require(locks.SOURCE_DIRECTORY == RH397_DIRECTORY, "RH397 directory")
    require(locks.SOURCE_RESULT_SHA256 == RH397_RESULT, "RH397 result")
    require(locks.STANDARD8 == STANDARD8, "RH397 standard8")
    closure = locks.build_source_closure()
    require(type(closure) is dict, "closure type")
    require(closure["pass"] is True, "closure pass")
    require(
        tuple(
            closure[key]
            for key in ("git_count", "remote_count", "logical_count")
        )
        == (184, 4, 188),
        "closure counts",
    )
    require(all(type(closure[key]) is int for key in ("git_count", "remote_count", "logical_count")), "count types")
    direct = closure["direct_predecessor"]
    require(type(direct) is dict and set(direct) == {"commit", "directory", "result_sha256", "role"})
    require(
        direct["commit"] == RH397_RELEASE
        and direct["directory"] == RH397_DIRECTORY
    )
    require(direct["result_sha256"] == RH397_RESULT)
    require(direct["role"] == DIRECT_ROLE)
    git = closure["git"]
    require(git["group_sizes"] == GROUP_SIZES, "group sizes")
    require(git["group_digests"] == GROUP_DIGESTS, "group digests")
    require(git["all_git_source_digest"] == ALL_GIT, "all Git digest")
    require(type(git["path_unique_count"]) is int and git["path_unique_count"] == 184)
    require(closure["logical_source_digest"] == LOGICAL, "logical digest")
    require(closure["logical_digest_pass"] is True, "logical pass")
    logical_bytes = (
        ALL_GIT + "\n" + "\n".join(REMOTE_CANONICAL) + "\n"
    ).encode("utf-8")
    require(sha256(logical_bytes).hexdigest() == LOGICAL, "independent logical")
    roles = closure["source_roles"]
    require(roles == SOURCE_ROLES, "exact source roles")
    require(tuple(roles) == tuple(SOURCE_ROLES), "source role order")
    require(roles["RH397"]["analytic_input"] is False, "RH397 analytic firewall")
    require(roles["RH396"]["analytic_input"] is True, "RH396 analytic authority")
    require(
        [name for name, role in roles.items() if role["analytic_input"] is True]
        == ["RH396"],
        "sole analytic authority",
    )


def test_group_order_commits_and_paths_are_exact() -> None:
    entries = locks.build_git_source_locks()["entries"]
    require(type(entries) is list and len(entries) == 184)
    offsets = (0, 172, 180, 184)
    for label, start, stop in zip(tuple(GROUP_SIZES), offsets, offsets[1:]):
        rows = entries[start:stop]
        require(len(rows) == GROUP_SIZES[label], label)
        require(all(row["group"] == label for row in rows), label)
        require(independent_lines_digest(rows) == GROUP_DIGESTS[label], label)
    require(all(type(row) is dict and set(row) == {"group", "commit", "path", "sha256"} for row in entries))
    require(all(all(type(value) is str for value in row.values()) for row in entries))
    require(all(row["commit"] == RH397_RELEASE for row in entries))
    predecessor = locks.released_source_result()["source_closure"]["git"]["entries"]
    require(type(predecessor) is list and len(predecessor) == 172)
    for current, inherited in zip(entries[:172], predecessor):
        require(current["path"] == inherited["path"] and current["sha256"] == inherited["sha256"])
        require(current["group"] == "rh397_immutable_closure")
        require(current["commit"] == RH397_RELEASE)
    expected_tail = [
        f"prime_dynamics_theory/{RH397_DIRECTORY}/{relative}"
        for relative in STANDARD8 + PRIOR_LOCKS
    ]
    require([row["path"] for row in entries[172:]] == expected_tail)
    require(independent_lines_digest(entries) == ALL_GIT, "independent all Git")


def test_rh397_standard_eight_release_blob_literals() -> None:
    require(tuple(STANDARD8_BLOBS) == STANDARD8)
    for relative, (expected_sha, expected_bytes) in STANDARD8_BLOBS.items():
        blob = locks.git_blob(RH397_RELEASE, f"{RH397_DIRECTORY}/{relative}")
        require(len(blob) == expected_bytes, relative)
        require(locks.digest_bytes(blob) == expected_sha, relative)
        require(locks.STANDARD8_SHA256[relative] == expected_sha, relative)


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
    signatures = tuple(locks._remote_literal_signature(item) for item in remote["objects"])
    require(signatures == REMOTE_SEALS, "independent remote literal seals")
    require(locks.REMOTE_PAYLOAD_HASHES == PAYLOADS and len(PAYLOADS) == 6)
    require(type(remote["objects"]) is list and len(remote["objects"]) == 4)
    require(all(type(item) is dict for item in remote["objects"]))
    require(all(type(item["bytes"]) is int and type(item["pages"]) is int for item in remote["objects"]))
    require(all(type(item["redistributable_in_release"]) is bool for item in remote["objects"]))
    require(all(item["mime"] == "application/pdf" and item["pdf_vendored"] is False for item in remote["objects"]), "nonvendor")
    require(remote["objects"][0]["source_tar_vendored"] is False, "source tar nonvendor")
    require(locks._remote_payload_hits() == [], "tree payload hits")


def test_pretty_locks_are_release_exact_and_tt_locators_are_sealed() -> None:
    for relative, expected_sha in zip(locks.LOCAL_EXTERNAL_LOCKS, REMOTE_PRETTY):
        local = locks.ROOT / relative
        released = locks.git_blob(RH397_RELEASE, f"{RH397_DIRECTORY}/{relative}")
        require(local.read_bytes() == released, relative)
        require(sha256(local.read_bytes()).hexdigest() == expected_sha, relative)
        require(locks.digest(local) == expected_sha, relative)
    direct = locks.ROOT / "results" / "tao_teravainen_external_source_lock.json"
    obj = locks.loads_strict(direct.read_text(encoding="utf-8"))
    require(locks.digest_bytes(locks.canonical_json_bytes(obj)) == REMOTE_CANONICAL[3])
    require(obj["arxiv_id_version"] == "1708.02610v2")
    require([locator["label"] for locator in obj["locators"]] == ["Corollary 1.8", "Remark 1.5", "Theorem A.1"])


def test_release_commit_rebinding_and_exact_types_fail_closed() -> None:
    for commit in ("0" * 40, True, 17):
        with pytest.raises(ValueError, match="rebound"):
            locks.build_git_source_locks(commit=commit)
    with pytest.raises(TypeError):
        locks.digest_bytes("not bytes")
    with pytest.raises(TypeError):
        locks.digest("not a path")
    with pytest.raises(ValueError, match="duplicate JSON key"):
        locks.loads_strict('{"source_key":"a","source_key":"b"}')
    for token in ("NaN", "Infinity", "-Infinity"):
        with pytest.raises(ValueError, match="non-finite JSON constant"):
            locks.loads_strict('{"value":' + token + '}')
    with pytest.raises(TypeError, match="exact text"):
        locks.loads_strict(b"{}")
    with pytest.raises(ValueError, match="exact lowercase 40-hex"):
        locks.git_blob(True, "README.md")
    require(locks.canonical_json_bytes({"accent": "Teräväinen"}) == '{"accent":"Teräväinen"}'.encode("utf-8"))
    with pytest.raises(ValueError):
        locks.source_digest_lines(
            [
                {
                    "group": "g",
                    "commit": RH397_RELEASE,
                    "path": "bad",
                    "sha256": "0" * 64,
                }
            ]
        )


def test_coordinated_constant_and_comparator_rebinding_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(locks, "SOURCE_RELEASE", "0" * 40)
    monkeypatch.setattr(locks, "SOURCE_RESULT_SHA256", "1" * 64)
    monkeypatch.setattr(locks, "EXPECTED_GROUP_SIZES", dict(GROUP_SIZES))
    monkeypatch.setattr(locks, "EXPECTED_GROUP_DIGESTS", dict(GROUP_DIGESTS))
    monkeypatch.setattr(locks, "EXPECTED_ALL_GIT_SOURCE_DIGEST", ALL_GIT)
    monkeypatch.setattr(locks, "EXPECTED_LOGICAL_SOURCE_DIGEST", LOGICAL)
    monkeypatch.setattr(locks, "exact_equal", lambda left, right: True)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_git_source_locks(commit=locks.SOURCE_RELEASE)


def test_group_path_and_standard_blob_mutations_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    groups = dict(locks.EXPECTED_GROUP_DIGESTS)
    groups["rh397_standard8"] = "0" * 64
    monkeypatch.setattr(locks, "EXPECTED_GROUP_DIGESTS", groups)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_git_source_locks()


def test_source_role_and_predecessor_row_mutations_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    roles = deepcopy(locks.SOURCE_ROLE_CONTRACT)
    roles["RH397"]["analytic_input"] = True
    roles["RH396"]["analytic_input"] = False
    monkeypatch.setattr(locks, "SOURCE_ROLE_CONTRACT", roles)
    with pytest.raises(ValueError, match="source role contract changed"):
        locks.build_source_closure()
    monkeypatch.undo()
    monkeypatch.setattr(locks, "DIRECT_PREDECESSOR_ROLE", "analytic_predecessor")
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_source_closure()
    monkeypatch.undo()
    released = deepcopy(locks.released_source_result())
    released["source_closure"]["git"]["entries"].pop()
    monkeypatch.setattr(locks, "released_source_result", lambda: released)
    with pytest.raises(RuntimeError, match="not 172 rows"):
        locks.build_git_source_locks()
    monkeypatch.undo()
    monkeypatch.setattr(locks, "STANDARD8", tuple(reversed(STANDARD8)))
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_git_source_locks()
    monkeypatch.undo()
    hashes = dict(locks.STANDARD8_SHA256)
    hashes["main.tex"] = "0" * 64
    monkeypatch.setattr(locks, "STANDARD8_SHA256", hashes)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_git_source_locks()


def test_inherited_remote_object_digest_role_literal_and_payload_mutations_fail(monkeypatch: pytest.MonkeyPatch) -> None:
    released = deepcopy(locks.released_source_result())
    released["source_closure"]["remote"]["objects"][3]["pages"] += 1
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
    seals = list(locks.REMOTE_LITERAL_SEALS)
    seals[2] = (*seals[2][:-1], False)
    monkeypatch.setattr(locks, "REMOTE_LITERAL_SEALS", tuple(seals))
    monkeypatch.setattr(locks, "exact_equal", lambda left, right: True)
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_remote_source_locks()
    monkeypatch.undo()
    monkeypatch.setattr(locks, "REMOTE_PAYLOAD_HASHES", PAYLOADS | {"0" * 64})
    with pytest.raises(ValueError, match="immutable source constant contract"):
        locks.build_remote_source_locks()


def test_digest_and_git_blob_helper_bombs_do_not_self_certify(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(locks, "digest", lambda path: "0" * 64)
    require(locks.build_git_source_locks()["pass"] is False, "digest bomb")
    monkeypatch.undo()
    locks.released_source_result.cache_clear()
    monkeypatch.setattr(locks, "digest_bytes", lambda data: "0" * 64)
    with pytest.raises(RuntimeError, match="released source result digest"):
        locks.build_git_source_locks()
    monkeypatch.undo()
    payload = next(iter(PAYLOADS))
    monkeypatch.setattr(locks, "digest", lambda path: payload)
    remote = locks.build_remote_source_locks()
    require(remote["pass"] is False, "payload digest bomb")
    require(remote["external_payload_exclusion_pass"] is False, "payload exclusion bomb")


def test_source_module_has_no_network_client_or_bare_assert() -> None:
    text = Path(locks.__file__).read_text(encoding="utf-8")
    for forbidden in ("import requests", "urllib.request", "import socket", "http.client", "curl ", "wget "):
        require(forbidden not in text, forbidden)
    require('network_fetch_performed\": True' not in text, "network claim")
    for path in (Path(__file__), Path(locks.__file__)):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), str(path))


def test_only_git_show_transport_is_available(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[object, object, object, object]] = []

    class Completed:
        returncode = 0
        stdout = b"sealed"

    def fake_run(command: object, *, cwd: object, capture_output: object, check: object) -> Completed:
        calls.append((command, cwd, capture_output, check))
        return Completed()

    locks.git_blob.cache_clear()
    monkeypatch.setattr(locks.subprocess, "run", fake_run)
    require(locks.git_blob(RH397_RELEASE, "README.md") == b"sealed")
    require(
        calls
        == [
            (
                ["git", "show", f"{RH397_RELEASE}:README.md"],
                locks.REPO,
                True,
                False,
            )
        ]
    )
    locks.git_blob.cache_clear()
