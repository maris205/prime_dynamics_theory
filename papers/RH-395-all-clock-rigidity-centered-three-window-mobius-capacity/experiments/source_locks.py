"""Immutable 148-Git-plus-four-remote source closure for RH-395."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import json
import math
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
WORKSPACE = ROOT.parents[2]


SOURCE_RELEASE = "6b3d616851cd2d7cba66371d0aa9f25b8e8bf2f7"
SOURCE_DIRECTORY = "papers/RH-394-odd-parity-terminal-log-mobius-compiler"
SOURCE_RESULT_SHA256 = "935de4967e504e5c32f6d27980ec044c3cffccfbab534440730470de8b1ae610"
STANDARD8 = (
    "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
    "references.bib", "results/result.json", "results/result.schema.json",
    "src/odd_parity_compiler/core.py",
)
PRIOR_EXTERNAL_LOCKS = (
    "results/external_source_lock.json", "results/maynard_external_source_lock.json",
    "results/tao_external_source_lock.json", "results/tao_teravainen_external_source_lock.json",
)
LOCAL_EXTERNAL_LOCKS = PRIOR_EXTERNAL_LOCKS
RH375_RELEASE = "071fed1b2a5d8488b9d2e35a99a753953b233584"
RH375_DIRECTORY = "papers/RH-375-all-clock-one-site-mobius-capacity-supremum"
RH375_STANDARD8 = (
    "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
    "references.bib", "results/result.json", "results/result.schema.json",
    "src/all_clock_capacity/core.py",
)
RH375_STANDARD8_SHA256 = {
    "README.md": "4949823c38e81dce9b04d46405a7a1d1bbd156375d2332f9a9ea90a7b8927c11",
    "THEOREM_LEDGER.md": "93afb2db541ca58cf563d4ba7bed06634f5d3be77e9059c11498d6e83c417ec8",
    "UPDATED_ROADMAP.md": "678ffa5ed6ca5a44070e0cf4e3c0634e1507154c0a9410d68599ab7d5b934432",
    "main.tex": "7d96987b0236d2788a781565bc03195c59ad2b72d07f1ff8988f8a3fef4a5117",
    "references.bib": "67939f140d06425e110258cc982dc8d5af0888899bd9d29a5dc8bfbaef7505be",
    "results/result.json": "81d905c2476abc36fdd1ab0e468ad33d85f4df9db35afbd3bc79bf0771fe0a08",
    "results/result.schema.json": "5d570cfc9515de8953e18eaf78176934c81bf479d741172e5a602a2d1839ba02",
    "src/all_clock_capacity/core.py": "575a5d2371f1bc0d29b33bc15e983f3e41c9b5b9ceb60d97369a1ef73f51a694",
}
EXPECTED_GROUP_SIZES = {
    "rh394_immutable_closure": 128,
    "rh394_standard8": 8,
    "rh394_prior_external_locks": 4,
    "rh375_direct_all_clock_release8": 8,
}
EXPECTED_GROUP_DIGESTS = {
    "rh394_immutable_closure": "0a44007f1e5888ed9b1cc6eae380b25fec38e17fe7e4329594625538d36c579b",
    "rh394_standard8": "cab0bfbc807eb5ed2e8c85435a3348fb48d823327a77c740dc281c195fed9e47",
    "rh394_prior_external_locks": "e9d259e020d0bef964630388a58487efcdc0a48ee895a6c335f35d0269f6d7e2",
    "rh375_direct_all_clock_release8": "14ef15bf6df11e32a05925e5a103c8e2d16ed26abb62620153f9387d84c840ce",
}
EXPECTED_ALL_GIT_SOURCE_DIGEST = "9b5e0c04bb3189ddcb802ccb65d5f6b3cc8aa081000acd9fa781fd9f81e50ec9"
EXPECTED_LOGICAL_SOURCE_DIGEST = "5c4b81ea2f7bdd661fe4374d1174ef3a1909a8327d5982aa01510e4201340bd3"
JY_CANONICAL_SHA256 = "d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786"
MAYNARD_CANONICAL_SHA256 = "bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e"
TAO_CANONICAL_SHA256 = "d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84"
TAO_TERAVAINEN_CANONICAL_SHA256 = "a1448fb540b6f8fcf17cace1ff7d7218a6126cb3265699bbd43c444fcc558058"
JY_LOCK_BLOB_SHA256 = "d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058"
MAYNARD_LOCK_BLOB_SHA256 = "9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba"
TAO_LOCK_BLOB_SHA256 = "825b3455be5eac151b7478f537fa6c503ae8eb02004cd8da821ca802d4ebdd8f"
TAO_TERAVAINEN_LOCK_BLOB_SHA256 = "52ade551d8bef9aa35e850d03cefede1239cb9611b9211fdcda522f02fb501ec"
EXPECTED_REMOTE_KEYS = (
    "johnston-yang-arxiv-2204.01980v2",
    "maynard-annals-2015-small-gaps",
    "tao-cambridge-2016-logarithmic-chowla",
    "tao-teravainen-arxiv-1708.02610v2",
)
EXPECTED_REMOTE_ROLES = {
    "johnston-yang-arxiv-2204.01980v2": "inherited_closure_only_via_RH394",
    "maynard-annals-2015-small-gaps": "inherited_closure_only_via_RH394",
    "tao-cambridge-2016-logarithmic-chowla": "inherited_two_point_provenance_via_RH394",
    "tao-teravainen-arxiv-1708.02610v2": "inherited_odd_parity_input_via_RH394",
}
REMOTE_PAYLOAD_HASHES = frozenset({
    "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2",
    "572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd",
    "2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602",
    "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349",
    "a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2",
    "232bdb1ad6e46789bfc124a589d6c3afda803eaf3ba2f93278fc31be3aa276ad",
})
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def _pairs_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    out: dict[str, object] = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def _reject_constant(token: str) -> object:
    raise ValueError(f"non-finite JSON constant: {token}")


def loads_strict(text: str) -> object:
    if type(text) is not str:
        raise TypeError("strict JSON input must be exact text")
    return json.loads(
        text,
        object_pairs_hook=_pairs_no_duplicates,
        parse_constant=_reject_constant,
    )


def canonical_json_bytes(value: object) -> bytes:
    """Historical source-object canonical form, independent of certificate JSON."""
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(
            exact_equal(left[key], right[key]) for key in left
        )
    if type(left) in (list, tuple):
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right)
        )
    if type(left) is float:
        return math.isfinite(left) and math.isfinite(right) and left == right
    return left == right


def digest_bytes(data: bytes) -> str:
    if type(data) is not bytes:
        raise TypeError("digest input must be exact bytes")
    return sha256(data).hexdigest()


def digest(path: Path) -> str:
    if not isinstance(path, Path):
        raise TypeError("digest path must be pathlib.Path")
    hasher = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _validate_constants() -> None:
    def same(left: object, right: object) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return set(left) == set(right) and all(same(left[key], right[key]) for key in left)
        if type(left) in (list, tuple):
            return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
        if type(left) is float:
            return math.isfinite(left) and math.isfinite(right) and left == right
        return left == right

    expected_keys = (
        "johnston-yang-arxiv-2204.01980v2",
        "maynard-annals-2015-small-gaps",
        "tao-cambridge-2016-logarithmic-chowla",
        "tao-teravainen-arxiv-1708.02610v2",
    )
    expected_roles = {
        "johnston-yang-arxiv-2204.01980v2": "inherited_closure_only_via_RH394",
        "maynard-annals-2015-small-gaps": "inherited_closure_only_via_RH394",
        "tao-cambridge-2016-logarithmic-chowla": "inherited_two_point_provenance_via_RH394",
        "tao-teravainen-arxiv-1708.02610v2": "inherited_odd_parity_input_via_RH394",
    }
    expected_payload_hashes = frozenset({
        "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2",
        "572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd",
        "2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602",
        "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349",
        "a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2",
        "232bdb1ad6e46789bfc124a589d6c3afda803eaf3ba2f93278fc31be3aa276ad",
    })
    expected_contract = {
        "source_release": "6b3d616851cd2d7cba66371d0aa9f25b8e8bf2f7",
        "source_directory": "papers/RH-394-odd-parity-terminal-log-mobius-compiler",
        "source_result_sha256": "935de4967e504e5c32f6d27980ec044c3cffccfbab534440730470de8b1ae610",
        "standard8": (
            "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
            "references.bib", "results/result.json", "results/result.schema.json",
            "src/odd_parity_compiler/core.py",
        ),
        "prior_external_locks": (
            "results/external_source_lock.json",
            "results/maynard_external_source_lock.json",
            "results/tao_external_source_lock.json",
            "results/tao_teravainen_external_source_lock.json",
        ),
        "local_external_locks": (
            "results/external_source_lock.json",
            "results/maynard_external_source_lock.json",
            "results/tao_external_source_lock.json",
            "results/tao_teravainen_external_source_lock.json",
        ),
        "rh375_release": "071fed1b2a5d8488b9d2e35a99a753953b233584",
        "rh375_directory": "papers/RH-375-all-clock-one-site-mobius-capacity-supremum",
        "rh375_standard8": (
            "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
            "references.bib", "results/result.json", "results/result.schema.json",
            "src/all_clock_capacity/core.py",
        ),
        "rh375_standard8_sha256": {
            "README.md": "4949823c38e81dce9b04d46405a7a1d1bbd156375d2332f9a9ea90a7b8927c11",
            "THEOREM_LEDGER.md": "93afb2db541ca58cf563d4ba7bed06634f5d3be77e9059c11498d6e83c417ec8",
            "UPDATED_ROADMAP.md": "678ffa5ed6ca5a44070e0cf4e3c0634e1507154c0a9410d68599ab7d5b934432",
            "main.tex": "7d96987b0236d2788a781565bc03195c59ad2b72d07f1ff8988f8a3fef4a5117",
            "references.bib": "67939f140d06425e110258cc982dc8d5af0888899bd9d29a5dc8bfbaef7505be",
            "results/result.json": "81d905c2476abc36fdd1ab0e468ad33d85f4df9db35afbd3bc79bf0771fe0a08",
            "results/result.schema.json": "5d570cfc9515de8953e18eaf78176934c81bf479d741172e5a602a2d1839ba02",
            "src/all_clock_capacity/core.py": "575a5d2371f1bc0d29b33bc15e983f3e41c9b5b9ceb60d97369a1ef73f51a694",
        },
        "group_sizes": {
            "rh394_immutable_closure": 128,
            "rh394_standard8": 8,
            "rh394_prior_external_locks": 4,
            "rh375_direct_all_clock_release8": 8,
        },
        "group_digests": {
            "rh394_immutable_closure": "0a44007f1e5888ed9b1cc6eae380b25fec38e17fe7e4329594625538d36c579b",
            "rh394_standard8": "cab0bfbc807eb5ed2e8c85435a3348fb48d823327a77c740dc281c195fed9e47",
            "rh394_prior_external_locks": "e9d259e020d0bef964630388a58487efcdc0a48ee895a6c335f35d0269f6d7e2",
            "rh375_direct_all_clock_release8": "14ef15bf6df11e32a05925e5a103c8e2d16ed26abb62620153f9387d84c840ce",
        },
        "all_git_digest": "9b5e0c04bb3189ddcb802ccb65d5f6b3cc8aa081000acd9fa781fd9f81e50ec9",
        "logical_digest": "5c4b81ea2f7bdd661fe4374d1174ef3a1909a8327d5982aa01510e4201340bd3",
        "canonical_digests": (
            "d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786",
            "bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e",
            "d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84",
            "a1448fb540b6f8fcf17cace1ff7d7218a6126cb3265699bbd43c444fcc558058",
        ),
        "pretty_digests": (
            "d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058",
            "9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba",
            "825b3455be5eac151b7478f537fa6c503ae8eb02004cd8da821ca802d4ebdd8f",
            "52ade551d8bef9aa35e850d03cefede1239cb9611b9211fdcda522f02fb501ec",
        ),
        "remote_keys": expected_keys,
        "remote_roles": expected_roles,
        "payload_hashes": expected_payload_hashes,
    }
    actual_contract = {
        "source_release": SOURCE_RELEASE,
        "source_directory": SOURCE_DIRECTORY,
        "source_result_sha256": SOURCE_RESULT_SHA256,
        "standard8": STANDARD8,
        "prior_external_locks": PRIOR_EXTERNAL_LOCKS,
        "local_external_locks": LOCAL_EXTERNAL_LOCKS,
        "rh375_release": RH375_RELEASE,
        "rh375_directory": RH375_DIRECTORY,
        "rh375_standard8": RH375_STANDARD8,
        "rh375_standard8_sha256": RH375_STANDARD8_SHA256,
        "group_sizes": EXPECTED_GROUP_SIZES,
        "group_digests": EXPECTED_GROUP_DIGESTS,
        "all_git_digest": EXPECTED_ALL_GIT_SOURCE_DIGEST,
        "logical_digest": EXPECTED_LOGICAL_SOURCE_DIGEST,
        "canonical_digests": (
            JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256,
            TAO_CANONICAL_SHA256, TAO_TERAVAINEN_CANONICAL_SHA256,
        ),
        "pretty_digests": (
            JY_LOCK_BLOB_SHA256, MAYNARD_LOCK_BLOB_SHA256,
            TAO_LOCK_BLOB_SHA256, TAO_TERAVAINEN_LOCK_BLOB_SHA256,
        ),
        "remote_keys": EXPECTED_REMOTE_KEYS,
        "remote_roles": EXPECTED_REMOTE_ROLES,
        "payload_hashes": REMOTE_PAYLOAD_HASHES,
    }
    if not same(actual_contract, expected_contract):
        raise ValueError("immutable source constant contract changed")
    if (
        type(REMOTE_PAYLOAD_HASHES) is not frozenset
        or REMOTE_PAYLOAD_HASHES != expected_payload_hashes
        or len(REMOTE_PAYLOAD_HASHES) != 6
    ):
        raise ValueError("remote payload hash membership changed")
    hashes = [
        SOURCE_RESULT_SHA256, EXPECTED_ALL_GIT_SOURCE_DIGEST, EXPECTED_LOGICAL_SOURCE_DIGEST,
        JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256, TAO_CANONICAL_SHA256,
        TAO_TERAVAINEN_CANONICAL_SHA256, JY_LOCK_BLOB_SHA256, MAYNARD_LOCK_BLOB_SHA256,
        TAO_LOCK_BLOB_SHA256, TAO_TERAVAINEN_LOCK_BLOB_SHA256,
        *EXPECTED_GROUP_DIGESTS.values(), *RH375_STANDARD8_SHA256.values(),
        *REMOTE_PAYLOAD_HASHES,
    ]
    if any(type(value) is not str or not SHA256_RE.fullmatch(value) for value in hashes):
        raise ValueError("sealed SHA-256 constant is malformed")
    if (
        type(SOURCE_RELEASE) is not str
        or type(RH375_RELEASE) is not str
        or not COMMIT_RE.fullmatch(SOURCE_RELEASE)
        or not COMMIT_RE.fullmatch(RH375_RELEASE)
    ):
        raise ValueError("source release commit is malformed")
    if tuple(RH375_STANDARD8_SHA256) != RH375_STANDARD8:
        raise ValueError("RH-375 standard-eight order changed")
    if set(EXPECTED_GROUP_SIZES) != set(EXPECTED_GROUP_DIGESTS):
        raise ValueError("source group constants disagree")
    if (
        type(EXPECTED_REMOTE_KEYS) is not tuple
        or EXPECTED_REMOTE_KEYS != expected_keys
        or type(EXPECTED_REMOTE_ROLES) is not dict
        or EXPECTED_REMOTE_ROLES != expected_roles
        or tuple(EXPECTED_REMOTE_ROLES) != EXPECTED_REMOTE_KEYS
    ):
        raise ValueError("remote role membership changed")


def _repo_relative(workspace_path: str) -> str:
    prefix = "prime_dynamics_theory/"
    if type(workspace_path) is not str or not workspace_path.startswith(prefix):
        raise ValueError("source path lacks repository prefix")
    relative = workspace_path.removeprefix(prefix)
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or relative in {"AGENTS.md", "RH_HANDOFF.md"}:
        raise ValueError("unsafe or mutable source path")
    return relative


@lru_cache(maxsize=None)
def git_blob(commit: str, relative: str) -> bytes:
    if type(commit) is not str or not COMMIT_RE.fullmatch(commit):
        raise ValueError("source commit must be exact lowercase 40-hex")
    path = Path(relative)
    if type(relative) is not str or path.is_absolute() or ".." in path.parts:
        raise ValueError("unsafe release path")
    completed = subprocess.run(
        ["git", "show", f"{commit}:{relative}"], cwd=REPO,
        capture_output=True, check=False,
    )
    if completed.returncode:
        raise RuntimeError(f"release blob unavailable: {commit}:{relative}")
    return completed.stdout


@lru_cache(maxsize=1)
def released_source_result() -> dict[str, object]:
    data = git_blob(SOURCE_RELEASE, f"{SOURCE_DIRECTORY}/results/result.json")
    if digest_bytes(data) != SOURCE_RESULT_SHA256:
        raise RuntimeError("released source result digest changed")
    result = loads_strict(data.decode("utf-8"))
    if type(result) is not dict or result.get("status") != "RH-394_odd_parity_terminal_log_mobius_compiler_certified":
        raise RuntimeError("released source status changed")
    locks = result.get("source_locks")
    if (
        type(locks) is not dict
        or tuple(locks.get(key) for key in ("git_count", "remote_count", "logical_count"))
        != (128, 4, 132)
    ):
        raise RuntimeError("released source closure changed")
    return result


def source_digest_lines(entries: list[dict[str, object]]) -> tuple[str, ...]:
    if type(entries) is not list:
        raise TypeError("source entries must be an exact list")
    lines: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise ValueError("source row membership changed")
        group, commit, path, source_sha = (entry[key] for key in ("group", "commit", "path", "sha256"))
        if not all(type(item) is str for item in (group, commit, path, source_sha)):
            raise TypeError("source row types changed")
        _repo_relative(path)
        if path in seen:
            raise ValueError("duplicate source path")
        seen.add(path)
        if not COMMIT_RE.fullmatch(commit) or not SHA256_RE.fullmatch(source_sha):
            raise ValueError("source identifier format failed")
        lines.append(f"{group}\t{commit}\t{path}\t{source_sha}")
    return tuple(lines)


def lines_digest(lines: tuple[str, ...] | list[str]) -> str:
    if type(lines) not in (tuple, list) or any(type(line) is not str for line in lines):
        raise TypeError("digest lines must be exact text")
    return digest_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def _source_paths() -> dict[str, tuple[tuple[str, str | None, str], ...]]:
    inherited_rows = released_source_result()["source_locks"]["git"]["entries"]
    if type(inherited_rows) is not list or len(inherited_rows) != 128:
        raise RuntimeError("released immutable closure is not 128 rows")
    inherited: list[tuple[str, str | None, str]] = []
    for row in inherited_rows:
        if type(row) is not dict or set(row) != {"group", "commit", "path", "sha256"} or type(row["path"]) is not str or type(row["sha256"]) is not str:
            raise ValueError("released inherited source row changed")
        inherited.append((row["path"], row["sha256"], SOURCE_RELEASE))
    standard = tuple(
        (f"prime_dynamics_theory/{SOURCE_DIRECTORY}/{relative}", None, SOURCE_RELEASE)
        for relative in STANDARD8
    )
    expected_pretty = (
        JY_LOCK_BLOB_SHA256, MAYNARD_LOCK_BLOB_SHA256,
        TAO_LOCK_BLOB_SHA256, TAO_TERAVAINEN_LOCK_BLOB_SHA256,
    )
    external = tuple(
        (f"prime_dynamics_theory/{SOURCE_DIRECTORY}/{relative}", expected_sha, SOURCE_RELEASE)
        for relative, expected_sha in zip(PRIOR_EXTERNAL_LOCKS, expected_pretty)
    )
    rh375_direct = tuple(
        (
            f"prime_dynamics_theory/{RH375_DIRECTORY}/{relative}",
            RH375_STANDARD8_SHA256[relative],
            RH375_RELEASE,
        )
        for relative in RH375_STANDARD8
    )
    return {
        "rh394_immutable_closure": tuple(inherited),
        "rh394_standard8": standard,
        "rh394_prior_external_locks": external,
        "rh375_direct_all_clock_release8": rh375_direct,
    }


def build_git_source_locks(
    *, commit: str = SOURCE_RELEASE, rh375_commit: str = RH375_RELEASE
) -> dict[str, object]:
    _validate_constants()
    if type(commit) is not str or commit != SOURCE_RELEASE:
        raise ValueError("source release commit was rebound")
    if type(rh375_commit) is not str or rh375_commit != RH375_RELEASE:
        raise ValueError("RH-375 direct release commit was rebound")
    entries: list[dict[str, object]] = []
    group_sizes: dict[str, int] = {}
    group_digests: dict[str, str] = {}
    release_pass = True
    live_pass = True
    groups = _source_paths()
    for group, expected_size in EXPECTED_GROUP_SIZES.items():
        rows = groups[group]
        if type(rows) is not tuple or len(rows) != expected_size:
            raise RuntimeError(f"source group size changed: {group}")
        current: list[dict[str, object]] = []
        for workspace_path, expected_sha, row_commit in rows:
            expected_commit = rh375_commit if group == "rh375_direct_all_clock_release8" else commit
            if row_commit != expected_commit:
                raise RuntimeError(f"source group commit changed: {group}")
            relative = _repo_relative(workspace_path)
            blob_sha = digest_bytes(git_blob(row_commit, relative))
            if expected_sha is not None and blob_sha != expected_sha:
                release_pass = False
            live_path = WORKSPACE / workspace_path
            if not live_path.is_file() or digest(live_path) != blob_sha:
                live_pass = False
            row = {
                "group": group, "commit": row_commit,
                "path": workspace_path, "sha256": blob_sha,
            }
            current.append(row)
            entries.append(row)
        group_sizes[group] = len(current)
        group_digests[group] = lines_digest(source_digest_lines(current))
    all_digest = lines_digest(source_digest_lines(entries))
    digest_pass = group_sizes == EXPECTED_GROUP_SIZES and group_digests == EXPECTED_GROUP_DIGESTS and all_digest == EXPECTED_ALL_GIT_SOURCE_DIGEST
    path_count = len({row["path"] for row in entries})
    return {
        "all_git_source_digest": all_digest, "count": len(entries),
        "digest_contract_pass": digest_pass, "entries": entries,
        "group_digests": group_digests, "group_sizes": group_sizes,
        "live_identity_pass": live_pass, "path_unique_count": path_count,
        "pass": release_pass and live_pass and digest_pass and len(entries) == 148 and path_count == 148,
        "release_identity_pass": release_pass,
    }


def _remote_payload_hits() -> list[str]:
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if path.is_file():
            try:
                source_sha = digest(path)
            except OSError:
                continue
            if source_sha in REMOTE_PAYLOAD_HASHES:
                hits.append(path.relative_to(ROOT).as_posix())
    return sorted(hits)


def build_remote_source_locks() -> dict[str, object]:
    _validate_constants()
    released = released_source_result()["source_locks"]["remote"]
    if (
        type(released) is not dict
        or type(released.get("count")) is not int
        or released.get("count") != 4
        or type(released.get("objects")) is not list
        or len(released["objects"]) != 4
    ):
        raise RuntimeError("released remote closure changed")
    inherited = sorted((deepcopy(item) for item in released["objects"]), key=lambda item: item["source_key"])
    if [item["source_key"] for item in inherited] != list(EXPECTED_REMOTE_KEYS):
        raise RuntimeError("inherited remote source order changed")
    paths = [ROOT / relative for relative in LOCAL_EXTERNAL_LOCKS]
    stored = [loads_strict(path.read_text(encoding="utf-8")) for path in paths]
    if any(type(item) is not dict for item in stored):
        raise TypeError("stored remote lock must be an exact object")
    objects = inherited
    keys = [item["source_key"] for item in objects]
    canonical = [digest_bytes(canonical_json_bytes(item)) for item in objects]
    expected_canonical = [
        JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256, TAO_CANONICAL_SHA256,
        TAO_TERAVAINEN_CANONICAL_SHA256,
    ]
    blobs = [digest(path) for path in paths]
    expected_blobs = [
        JY_LOCK_BLOB_SHA256, MAYNARD_LOCK_BLOB_SHA256, TAO_LOCK_BLOB_SHA256,
        TAO_TERAVAINEN_LOCK_BLOB_SHA256,
    ]
    exact_inherited = all(exact_equal(local, remote) for local, remote in zip(stored, inherited))
    release_blobs = [
        git_blob(SOURCE_RELEASE, f"{SOURCE_DIRECTORY}/{relative}")
        for relative in PRIOR_EXTERNAL_LOCKS
    ]
    byte_exact = all(local.read_bytes() == predecessor for local, predecessor in zip(paths, release_blobs))
    literal_sealed = (
        stored[3].get("source_key") == EXPECTED_REMOTE_KEYS[3]
        and stored[3].get("arxiv_id_version") == "1708.02610v2"
        and stored[3].get("sha256") == "232bdb1ad6e46789bfc124a589d6c3afda803eaf3ba2f93278fc31be3aa276ad"
        and stored[3].get("bytes") == 398251
        and stored[3].get("pages") == 41
        and stored[3].get("mime") == "application/pdf"
        and stored[3].get("pdf_vendored") is False
        and stored[3].get("redistributable_in_release") is False
        and stored[0].get("source_tar_vendored") is False
    )
    offline = all(
        item.get("network_verification", {}).get("default") == "disabled"
        and item.get("network_verification", {}).get("fixed_url_only") is True
        and item.get("pdf_vendored") is False
        for item in objects
    )
    rights = [item.get("redistributable_in_release") for item in objects]
    hits = _remote_payload_hits()
    passed = (
        keys == list(EXPECTED_REMOTE_KEYS) and canonical == expected_canonical
        and blobs == expected_blobs and exact_inherited and byte_exact and literal_sealed
        and released.get("canonical_digests") == expected_canonical
        and released.get("source_keys") == list(EXPECTED_REMOTE_KEYS)
        and released.get("redistributable_in_release") == [False, False, True, False]
        and rights == [False, False, True, False] and offline and hits == []
    )
    return {
        "canonical_digests": canonical, "count": 4,
        "all_lock_literals_sealed_pass": literal_sealed,
        "external_payload_exclusion_pass": hits == [], "external_payload_hash_hits": hits,
        "local_lock_blob_digests": blobs, "local_lock_objects_exact_pass": exact_inherited,
        "local_release_copies_byte_exact_pass": byte_exact, "network_fetch_performed": False,
        "objects": objects, "offline_configuration_pass": offline, "pass": passed,
        "redistributable_in_release": rights, "source_keys": keys,
        "source_roles": dict(EXPECTED_REMOTE_ROLES),
    }


def build_source_closure() -> dict[str, object]:
    git = build_git_source_locks()
    remote = build_remote_source_locks()
    logical = digest_bytes((git["all_git_source_digest"] + "\n" + "\n".join(remote["canonical_digests"]) + "\n").encode("utf-8"))
    return {
        "direct_predecessors": {
            "rh394_terminal_log": {
                "commit": SOURCE_RELEASE,
                "directory": SOURCE_DIRECTORY,
                "result_sha256": SOURCE_RESULT_SHA256,
                "role": "direct_terminal_log_three_shift_table_law_and_phase_densities",
            },
            "rh375_one_site_endpoint": {
                "commit": RH375_RELEASE,
                "directory": RH375_DIRECTORY,
                "result_sha256": RH375_STANDARD8_SHA256["results/result.json"],
                "role": (
                    "direct_squarefree_phase_density_MWIS_all_finite_clock_lift_"
                    "square_clock_divisibility_same_prime_support_saturation_"
                    "combinatorics_only"
                ),
                "terminal_clock_analytic_input": False,
            },
        },
        "git": git, "git_count": 148, "logical_count": 152,
        "logical_digest_pass": logical == EXPECTED_LOGICAL_SOURCE_DIGEST,
        "logical_source_digest": logical,
        "pass": git["pass"] is True and remote["pass"] is True and logical == EXPECTED_LOGICAL_SOURCE_DIGEST,
        "remote": remote, "remote_count": 4,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_source_closure(), sort_keys=True))
