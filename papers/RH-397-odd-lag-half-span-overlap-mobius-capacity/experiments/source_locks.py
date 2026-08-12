"""Immutable 172-Git-plus-four-remote source closure for RH-397."""

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

SOURCE_RELEASE = "cd57086fa90939d56656c3f952a08ffad9aabefe"
SOURCE_DIRECTORY = "papers/RH-396-euler-run-spectrum-fixed-lag-centered-mobius-capacity"
SOURCE_RESULT_SHA256 = "a7ea39793a255a9b51f2e1b8523293bf4f4a9fdd0934263f9950417ca28371d4"
STANDARD8 = (
    "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
    "references.bib", "results/result.json", "results/result.schema.json",
    "src/fixed_lag_centered_capacity/core.py",
)
STANDARD8_SHA256 = {
    "README.md": "251bf8a516204941ea65a210e1f9fec955226c3751d3637c8b5b6dfb0fdfab78",
    "THEOREM_LEDGER.md": "1a885510340c18cb5f206cd8f650fb881200a6a010797318131e267f3679c91b",
    "UPDATED_ROADMAP.md": "b28916175f9849d1bdf4c5479248004f5bff9c341eef10361752a9711e236b0e",
    "main.tex": "5d9a8c6c9a39436d07a94e082fffc003cfba91ece1d3859c11e2facbd5ffe99d",
    "references.bib": "2a5f201d51355bf0eb930484b4c9d3ad3d02bc145eed11809b0ab533956c599f",
    "results/result.json": SOURCE_RESULT_SHA256,
    "results/result.schema.json": "b78f958c60b1651446a3e0ac2af7a2e696cba2642a6414237877d997ff51691a",
    "src/fixed_lag_centered_capacity/core.py": "728546daa86fac7b51ab06facff2fccc771ad5128a9f7324f2db36d400a3bf0d",
}
PRIOR_EXTERNAL_LOCKS = (
    "results/external_source_lock.json", "results/maynard_external_source_lock.json",
    "results/tao_external_source_lock.json",
    "results/tao_teravainen_external_source_lock.json",
)
LOCAL_EXTERNAL_LOCKS = PRIOR_EXTERNAL_LOCKS

RH394_RELEASE = "6b3d616851cd2d7cba66371d0aa9f25b8e8bf2f7"
RH394_DIRECTORY = "papers/RH-394-odd-parity-terminal-log-mobius-compiler"
RH392_RELEASE = "9768c1cb5f56d959406c19119315afd542b6c30f"
RH392_DIRECTORY = "papers/RH-392-fixed-lag-terminal-log-mobius-capacity-landscape"
RH395_RELEASE = "20de7202518f4488cbd9c7d63bf94aaa3dc94476"
RH395_DIRECTORY = "papers/RH-395-all-clock-rigidity-centered-three-window-mobius-capacity"
RH375_RELEASE = "071fed1b2a5d8488b9d2e35a99a753953b233584"
RH375_DIRECTORY = "papers/RH-375-all-clock-one-site-mobius-capacity-supremum"

EXPECTED_GROUP_SIZES = {
    "rh396_immutable_closure": 160,
    "rh396_standard8": 8,
    "rh396_prior_external_locks": 4,
}
EXPECTED_GROUP_DIGESTS = {
    "rh396_immutable_closure": "c331c37d3447ac1f54063287f5c79034b117e5c9516f3727d5eac5a148d9bd12",
    "rh396_standard8": "dbe2380bc2a6a060c69ca852625d9c2a7f20d82797108ed17fd1c0d231fa541a",
    "rh396_prior_external_locks": "57d0e03fff2be3fb1466834fefdc5fdc001e87686eb1e5898918d820163a57ea",
}
EXPECTED_ALL_GIT_SOURCE_DIGEST = "b3f5688380762a4e3c27d512311f4c0d22173c434cc40459fc77bb3eb87fb5c4"
EXPECTED_LOGICAL_SOURCE_DIGEST = "e9588b58f75e02e31ba5ffb279aea267074ec72f717afa84670f320d6c1030e0"

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
REMOTE_LITERAL_SEALS = (
    (EXPECTED_REMOTE_KEYS[0], "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2", 278380, 22, False),
    (EXPECTED_REMOTE_KEYS[1], "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349", 528115, 31, False),
    (EXPECTED_REMOTE_KEYS[2], "a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2", 534086, 36, True),
    (EXPECTED_REMOTE_KEYS[3], "232bdb1ad6e46789bfc124a589d6c3afda803eaf3ba2f93278fc31be3aa276ad", 398251, 41, False),
)
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
    return json.loads(text, object_pairs_hook=_pairs_no_duplicates, parse_constant=_reject_constant)


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(exact_equal(left[key], right[key]) for key in left)
    if type(left) in (list, tuple):
        return len(left) == len(right) and all(exact_equal(a, b) for a, b in zip(left, right))
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
        return left == right

    expected_contract = {
        "source_release": "cd57086fa90939d56656c3f952a08ffad9aabefe",
        "source_directory": "papers/RH-396-euler-run-spectrum-fixed-lag-centered-mobius-capacity",
        "source_result_sha256": "a7ea39793a255a9b51f2e1b8523293bf4f4a9fdd0934263f9950417ca28371d4",
        "rh394_release": "6b3d616851cd2d7cba66371d0aa9f25b8e8bf2f7",
        "rh394_directory": "papers/RH-394-odd-parity-terminal-log-mobius-compiler",
        "rh392_release": "9768c1cb5f56d959406c19119315afd542b6c30f",
        "rh392_directory": "papers/RH-392-fixed-lag-terminal-log-mobius-capacity-landscape",
        "rh395_release": "20de7202518f4488cbd9c7d63bf94aaa3dc94476",
        "rh395_directory": "papers/RH-395-all-clock-rigidity-centered-three-window-mobius-capacity",
        "rh375_release": "071fed1b2a5d8488b9d2e35a99a753953b233584",
        "rh375_directory": "papers/RH-375-all-clock-one-site-mobius-capacity-supremum",
        "standard8": (
            "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
            "references.bib", "results/result.json", "results/result.schema.json",
            "src/fixed_lag_centered_capacity/core.py",
        ),
        "standard8_sha256": {
            "README.md": "251bf8a516204941ea65a210e1f9fec955226c3751d3637c8b5b6dfb0fdfab78",
            "THEOREM_LEDGER.md": "1a885510340c18cb5f206cd8f650fb881200a6a010797318131e267f3679c91b",
            "UPDATED_ROADMAP.md": "b28916175f9849d1bdf4c5479248004f5bff9c341eef10361752a9711e236b0e",
            "main.tex": "5d9a8c6c9a39436d07a94e082fffc003cfba91ece1d3859c11e2facbd5ffe99d",
            "references.bib": "2a5f201d51355bf0eb930484b4c9d3ad3d02bc145eed11809b0ab533956c599f",
            "results/result.json": "a7ea39793a255a9b51f2e1b8523293bf4f4a9fdd0934263f9950417ca28371d4",
            "results/result.schema.json": "b78f958c60b1651446a3e0ac2af7a2e696cba2642a6414237877d997ff51691a",
            "src/fixed_lag_centered_capacity/core.py": "728546daa86fac7b51ab06facff2fccc771ad5128a9f7324f2db36d400a3bf0d",
        },
        "prior_locks": (
            "results/external_source_lock.json", "results/maynard_external_source_lock.json",
            "results/tao_external_source_lock.json", "results/tao_teravainen_external_source_lock.json",
        ),
        "group_sizes": {"rh396_immutable_closure": 160, "rh396_standard8": 8, "rh396_prior_external_locks": 4},
        "group_digests": {
            "rh396_immutable_closure": "c331c37d3447ac1f54063287f5c79034b117e5c9516f3727d5eac5a148d9bd12",
            "rh396_standard8": "dbe2380bc2a6a060c69ca852625d9c2a7f20d82797108ed17fd1c0d231fa541a",
            "rh396_prior_external_locks": "57d0e03fff2be3fb1466834fefdc5fdc001e87686eb1e5898918d820163a57ea",
        },
        "all_git": "b3f5688380762a4e3c27d512311f4c0d22173c434cc40459fc77bb3eb87fb5c4",
        "logical": "e9588b58f75e02e31ba5ffb279aea267074ec72f717afa84670f320d6c1030e0",
        "canonical": (
            "d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786",
            "bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e",
            "d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84",
            "a1448fb540b6f8fcf17cace1ff7d7218a6126cb3265699bbd43c444fcc558058",
        ),
        "pretty": (
            "d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058",
            "9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba",
            "825b3455be5eac151b7478f537fa6c503ae8eb02004cd8da821ca802d4ebdd8f",
            "52ade551d8bef9aa35e850d03cefede1239cb9611b9211fdcda522f02fb501ec",
        ),
        "remote_keys": (
            "johnston-yang-arxiv-2204.01980v2", "maynard-annals-2015-small-gaps",
            "tao-cambridge-2016-logarithmic-chowla", "tao-teravainen-arxiv-1708.02610v2",
        ),
        "remote_roles": {
            "johnston-yang-arxiv-2204.01980v2": "inherited_closure_only_via_RH394",
            "maynard-annals-2015-small-gaps": "inherited_closure_only_via_RH394",
            "tao-cambridge-2016-logarithmic-chowla": "inherited_two_point_provenance_via_RH394",
            "tao-teravainen-arxiv-1708.02610v2": "inherited_odd_parity_input_via_RH394",
        },
        "literal_seals": (
            ("johnston-yang-arxiv-2204.01980v2", "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2", 278380, 22, False),
            ("maynard-annals-2015-small-gaps", "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349", 528115, 31, False),
            ("tao-cambridge-2016-logarithmic-chowla", "a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2", 534086, 36, True),
            ("tao-teravainen-arxiv-1708.02610v2", "232bdb1ad6e46789bfc124a589d6c3afda803eaf3ba2f93278fc31be3aa276ad", 398251, 41, False),
        ),
        "payloads": frozenset({
            "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2",
            "572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd",
            "2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602",
            "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349",
            "a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2",
            "232bdb1ad6e46789bfc124a589d6c3afda803eaf3ba2f93278fc31be3aa276ad",
        }),
    }
    actual_contract = {
        "source_release": SOURCE_RELEASE, "source_directory": SOURCE_DIRECTORY,
        "source_result_sha256": SOURCE_RESULT_SHA256, "standard8": STANDARD8,
        "rh394_release": RH394_RELEASE, "rh394_directory": RH394_DIRECTORY,
        "rh392_release": RH392_RELEASE, "rh392_directory": RH392_DIRECTORY,
        "rh395_release": RH395_RELEASE, "rh395_directory": RH395_DIRECTORY,
        "rh375_release": RH375_RELEASE, "rh375_directory": RH375_DIRECTORY,
        "standard8_sha256": STANDARD8_SHA256, "prior_locks": PRIOR_EXTERNAL_LOCKS,
        "group_sizes": EXPECTED_GROUP_SIZES, "group_digests": EXPECTED_GROUP_DIGESTS,
        "all_git": EXPECTED_ALL_GIT_SOURCE_DIGEST, "logical": EXPECTED_LOGICAL_SOURCE_DIGEST,
        "canonical": (JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256, TAO_CANONICAL_SHA256, TAO_TERAVAINEN_CANONICAL_SHA256),
        "pretty": (JY_LOCK_BLOB_SHA256, MAYNARD_LOCK_BLOB_SHA256, TAO_LOCK_BLOB_SHA256, TAO_TERAVAINEN_LOCK_BLOB_SHA256),
        "remote_keys": EXPECTED_REMOTE_KEYS, "remote_roles": EXPECTED_REMOTE_ROLES,
        "literal_seals": REMOTE_LITERAL_SEALS, "payloads": REMOTE_PAYLOAD_HASHES,
    }
    if not same(actual_contract, expected_contract):
        raise ValueError("immutable source constant contract changed")
    hashes = [
        SOURCE_RESULT_SHA256, *STANDARD8_SHA256.values(), *EXPECTED_GROUP_DIGESTS.values(),
        EXPECTED_ALL_GIT_SOURCE_DIGEST, EXPECTED_LOGICAL_SOURCE_DIGEST,
        JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256, TAO_CANONICAL_SHA256,
        TAO_TERAVAINEN_CANONICAL_SHA256, JY_LOCK_BLOB_SHA256, MAYNARD_LOCK_BLOB_SHA256,
        TAO_LOCK_BLOB_SHA256, TAO_TERAVAINEN_LOCK_BLOB_SHA256, *REMOTE_PAYLOAD_HASHES,
    ]
    if any(type(value) is not str or not SHA256_RE.fullmatch(value) for value in hashes):
        raise ValueError("sealed SHA-256 constant is malformed")
    commits = (SOURCE_RELEASE, RH394_RELEASE, RH392_RELEASE, RH395_RELEASE, RH375_RELEASE)
    if any(type(commit) is not str or not COMMIT_RE.fullmatch(commit) for commit in commits):
        raise ValueError("sealed release commit is malformed")
    if tuple(STANDARD8_SHA256) != STANDARD8 or LOCAL_EXTERNAL_LOCKS != PRIOR_EXTERNAL_LOCKS:
        raise ValueError("source file order changed")


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
        ["git", "show", f"{commit}:{relative}"], cwd=REPO, capture_output=True, check=False
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
    if type(result) is not dict or result.get("status") != "RH-396_STAGE1_CERTIFIED":
        raise RuntimeError("released source status changed")
    closure = result.get("source_closure")
    if type(closure) is not dict or tuple(closure.get(key) for key in ("git_count", "remote_count", "logical_count")) != (160, 4, 164):
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


def _source_paths() -> dict[str, tuple[tuple[str, str, str], ...]]:
    inherited_rows = released_source_result()["source_closure"]["git"]["entries"]
    if type(inherited_rows) is not list or len(inherited_rows) != 160:
        raise RuntimeError("released immutable closure is not 160 rows")
    inherited: list[tuple[str, str, str]] = []
    for row in inherited_rows:
        if type(row) is not dict or set(row) != {"group", "commit", "path", "sha256"}:
            raise ValueError("released inherited source row changed")
        if type(row["path"]) is not str or type(row["sha256"]) is not str:
            raise TypeError("released inherited source row types changed")
        inherited.append((row["path"], row["sha256"], SOURCE_RELEASE))
    standard = tuple(
        (f"prime_dynamics_theory/{SOURCE_DIRECTORY}/{relative}", STANDARD8_SHA256[relative], SOURCE_RELEASE)
        for relative in STANDARD8
    )
    external_hashes = (JY_LOCK_BLOB_SHA256, MAYNARD_LOCK_BLOB_SHA256, TAO_LOCK_BLOB_SHA256, TAO_TERAVAINEN_LOCK_BLOB_SHA256)
    external = tuple(
        (f"prime_dynamics_theory/{SOURCE_DIRECTORY}/{relative}", expected_sha, SOURCE_RELEASE)
        for relative, expected_sha in zip(PRIOR_EXTERNAL_LOCKS, external_hashes)
    )
    return {
        "rh396_immutable_closure": tuple(inherited),
        "rh396_standard8": standard,
        "rh396_prior_external_locks": external,
    }


def build_git_source_locks(*, commit: str = SOURCE_RELEASE) -> dict[str, object]:
    _validate_constants()
    if type(commit) is not str or commit != SOURCE_RELEASE:
        raise ValueError("source release commit was rebound")
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
            if row_commit != commit:
                raise RuntimeError(f"source group commit changed: {group}")
            relative = _repo_relative(workspace_path)
            blob_sha = digest_bytes(git_blob(row_commit, relative))
            if blob_sha != expected_sha:
                release_pass = False
            live_path = WORKSPACE / workspace_path
            if not live_path.is_file() or digest(live_path) != blob_sha:
                live_pass = False
            row = {"group": group, "commit": row_commit, "path": workspace_path, "sha256": blob_sha}
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
        "pass": release_pass and live_pass and digest_pass and len(entries) == 172 and path_count == 172,
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


def _remote_literal_signature(item: dict[str, object]) -> tuple[object, ...]:
    return (
        item.get("source_key"), item.get("sha256"), item.get("bytes"), item.get("pages"),
        item.get("redistributable_in_release"),
    )


def build_remote_source_locks() -> dict[str, object]:
    _validate_constants()
    released = released_source_result()["source_closure"]["remote"]
    if type(released) is not dict or released.get("count") != 4 or type(released.get("objects")) is not list or len(released["objects"]) != 4:
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
    expected_canonical = [JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256, TAO_CANONICAL_SHA256, TAO_TERAVAINEN_CANONICAL_SHA256]
    blobs = [digest(path) for path in paths]
    expected_blobs = [JY_LOCK_BLOB_SHA256, MAYNARD_LOCK_BLOB_SHA256, TAO_LOCK_BLOB_SHA256, TAO_TERAVAINEN_LOCK_BLOB_SHA256]
    exact_inherited = all(exact_equal(local, remote) for local, remote in zip(stored, inherited))
    release_blobs = [git_blob(SOURCE_RELEASE, f"{SOURCE_DIRECTORY}/{relative}") for relative in PRIOR_EXTERNAL_LOCKS]
    byte_exact = all(local.read_bytes() == predecessor for local, predecessor in zip(paths, release_blobs))
    literal_sealed = (
        tuple(_remote_literal_signature(item) for item in stored) == REMOTE_LITERAL_SEALS
        and all(item.get("mime") == "application/pdf" and item.get("pdf_vendored") is False for item in stored)
        and all(item.get("network_verification", {}).get("default") == "disabled" for item in stored)
        and all(item.get("network_verification", {}).get("fixed_url_only") is True for item in stored)
        and stored[0].get("source_tar_vendored") is False
    )
    offline = all(
        item.get("network_verification", {}).get("default") == "disabled"
        and item.get("network_verification", {}).get("fixed_url_only") is True
        and item.get("pdf_vendored") is False for item in objects
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
        "direct_predecessor": {
            "commit": SOURCE_RELEASE, "directory": SOURCE_DIRECTORY,
            "result_sha256": SOURCE_RESULT_SHA256,
            "role": "direct_collision_aware_fixed_table_density_projection_and_finite_optimizer_predecessor",
        },
        "source_roles": {
            "RH394": {
                "commit": RH394_RELEASE, "directory": RH394_DIRECTORY,
                "role": "sole_analytic_input_inherited_through_RH396_for_fixed_distinct_three_shifts",
            },
            "RH396": "direct_collision_aware_fixed_table_density_projection_and_finite_optimizer_predecessor",
            "RH392": {
                "commit": RH392_RELEASE, "directory": RH392_DIRECTORY,
                "role": "transitive_fixed_lag_comparison_only",
                "analytic_input": False,
            },
            "RH395": {
                "commit": RH395_RELEASE, "directory": RH395_DIRECTORY,
                "role": "transitive_relation_saturation_and_tropical_comparison_only",
                "analytic_input": False,
            },
            "RH375": {
                "commit": RH375_RELEASE, "directory": RH375_DIRECTORY,
                "role": "transitive_one_site_MWIS_and_square_clock_comparison_only",
                "analytic_input": False,
            },
        },
        "git": git, "git_count": 172, "logical_count": 176,
        "logical_digest_pass": logical == EXPECTED_LOGICAL_SOURCE_DIGEST,
        "logical_source_digest": logical,
        "pass": git["pass"] is True and remote["pass"] is True and logical == EXPECTED_LOGICAL_SOURCE_DIGEST,
        "remote": remote, "remote_count": 4,
    }


if __name__ == "__main__":
    print(json.dumps(build_source_closure(), sort_keys=True))
