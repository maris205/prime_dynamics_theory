"""Immutable 117-Git-plus-three-remote source closure for RH-393."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
WORKSPACE = ROOT.parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from two_odd_compiler.core import canonical_json_bytes, exact_equal, loads_strict  # noqa: E402


SOURCE_RELEASE = "9768c1cb5f56d959406c19119315afd542b6c30f"
SOURCE_DIRECTORY = "papers/RH-392-fixed-lag-terminal-log-mobius-capacity-landscape"
SOURCE_RESULT_SHA256 = "83bab4eb57f1d4d2d31c646946df16203b155d49d78942f74a40df239e404bc0"
STANDARD8 = (
    "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
    "references.bib", "results/result.json", "results/result.schema.json",
    "src/fixed_lag_capacity/core.py",
)
PRIOR_EXTERNAL_LOCKS = (
    "results/external_source_lock.json", "results/maynard_external_source_lock.json",
    "results/tao_external_source_lock.json",
)
EXPECTED_GROUP_SIZES = {
    "rh392_immutable_closure": 106,
    "rh392_standard8": 8,
    "rh392_prior_external_locks": 3,
}
EXPECTED_GROUP_DIGESTS = {
    "rh392_immutable_closure": "cf36abdfa3a81f8781d86f1bb96747248eced62d2cd83a5e03de7de0c614bc28",
    "rh392_standard8": "5a20f8e8a65fbcf8add5b3c9bb5318527c94a349ca541236603efbcfa86ec8bf",
    "rh392_prior_external_locks": "8a69e04cbac166b36834f7b9e21e2cd8799f95d365330143ee261038c7da2863",
}
EXPECTED_ALL_GIT_SOURCE_DIGEST = "2c187ec15a427ffb0b06a48679f8419be82152fe16ea914c2a86437549117220"
EXPECTED_LOGICAL_SOURCE_DIGEST = "9315d7c01651ed8b4d94f98c3e4019ad11e28469ee6722903721db280b9f92eb"
JY_CANONICAL_SHA256 = "d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786"
MAYNARD_CANONICAL_SHA256 = "bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e"
TAO_CANONICAL_SHA256 = "d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84"
JY_LOCK_BLOB_SHA256 = "d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058"
MAYNARD_LOCK_BLOB_SHA256 = "9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba"
TAO_LOCK_BLOB_SHA256 = "825b3455be5eac151b7478f537fa6c503ae8eb02004cd8da821ca802d4ebdd8f"
REMOTE_PAYLOAD_HASHES = frozenset({
    "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2",
    "572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd",
    "2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602",
    "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349",
    "a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2",
})
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


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
    expected_payload_hashes = frozenset({
        "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2",
        "572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd",
        "2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602",
        "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349",
        "a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2",
    })
    if (
        type(REMOTE_PAYLOAD_HASHES) is not frozenset
        or REMOTE_PAYLOAD_HASHES != expected_payload_hashes
        or len(REMOTE_PAYLOAD_HASHES) != 5
    ):
        raise ValueError("remote payload hash membership changed")
    hashes = [
        SOURCE_RESULT_SHA256, EXPECTED_ALL_GIT_SOURCE_DIGEST, EXPECTED_LOGICAL_SOURCE_DIGEST,
        JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256, TAO_CANONICAL_SHA256,
        JY_LOCK_BLOB_SHA256, MAYNARD_LOCK_BLOB_SHA256, TAO_LOCK_BLOB_SHA256,
        *EXPECTED_GROUP_DIGESTS.values(), *REMOTE_PAYLOAD_HASHES,
    ]
    if any(type(value) is not str or not SHA256_RE.fullmatch(value) for value in hashes):
        raise ValueError("sealed SHA-256 constant is malformed")
    if type(SOURCE_RELEASE) is not str or not COMMIT_RE.fullmatch(SOURCE_RELEASE):
        raise ValueError("source release commit is malformed")
    if set(EXPECTED_GROUP_SIZES) != set(EXPECTED_GROUP_DIGESTS):
        raise ValueError("source group constants disagree")


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
    if type(result) is not dict or result.get("status") != "RH-392_fixed_lag_terminal_log_mobius_capacity_landscape_certified":
        raise RuntimeError("released source status changed")
    locks = result.get("source_locks")
    if type(locks) is not dict or (locks.get("git_count"), locks.get("remote_count"), locks.get("logical_count")) != (106, 3, 109):
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


def _source_paths() -> dict[str, tuple[tuple[str, str | None], ...]]:
    inherited_rows = released_source_result()["source_locks"]["git"]["entries"]
    if type(inherited_rows) is not list or len(inherited_rows) != 106:
        raise RuntimeError("released immutable closure is not 106 rows")
    inherited: list[tuple[str, str | None]] = []
    for row in inherited_rows:
        if type(row) is not dict or set(row) != {"group", "commit", "path", "sha256"} or type(row["path"]) is not str or type(row["sha256"]) is not str:
            raise ValueError("released inherited source row changed")
        inherited.append((row["path"], row["sha256"]))
    standard = tuple((f"prime_dynamics_theory/{SOURCE_DIRECTORY}/{relative}", None) for relative in STANDARD8)
    expected_pretty = (JY_LOCK_BLOB_SHA256, MAYNARD_LOCK_BLOB_SHA256, TAO_LOCK_BLOB_SHA256)
    external = tuple(
        (f"prime_dynamics_theory/{SOURCE_DIRECTORY}/{relative}", expected_sha)
        for relative, expected_sha in zip(PRIOR_EXTERNAL_LOCKS, expected_pretty)
    )
    return {
        "rh392_immutable_closure": tuple(inherited),
        "rh392_standard8": standard,
        "rh392_prior_external_locks": external,
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
        for workspace_path, expected_sha in rows:
            relative = _repo_relative(workspace_path)
            blob_sha = digest_bytes(git_blob(commit, relative))
            if expected_sha is not None and blob_sha != expected_sha:
                release_pass = False
            live_path = WORKSPACE / workspace_path
            if not live_path.is_file() or digest(live_path) != blob_sha:
                live_pass = False
            row = {"group": group, "commit": commit, "path": workspace_path, "sha256": blob_sha}
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
        "pass": release_pass and live_pass and digest_pass and len(entries) == 117 and path_count == 117,
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
    if type(released) is not dict or released.get("count") != 3 or type(released.get("objects")) is not list:
        raise RuntimeError("released remote closure changed")
    objects = sorted((deepcopy(item) for item in released["objects"]), key=lambda item: item["source_key"])
    keys = [
        "johnston-yang-arxiv-2204.01980v2",
        "maynard-annals-2015-small-gaps",
        "tao-cambridge-2016-logarithmic-chowla",
    ]
    if [item["source_key"] for item in objects] != keys:
        raise RuntimeError("remote source order changed")
    canonical = [digest_bytes(canonical_json_bytes(item)) for item in objects]
    expected_canonical = [JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256, TAO_CANONICAL_SHA256]
    paths = [
        ROOT / "results" / "external_source_lock.json",
        ROOT / "results" / "maynard_external_source_lock.json",
        ROOT / "results" / "tao_external_source_lock.json",
    ]
    stored = [loads_strict(path.read_text(encoding="utf-8")) for path in paths]
    blobs = [digest(path) for path in paths]
    expected_blobs = [JY_LOCK_BLOB_SHA256, MAYNARD_LOCK_BLOB_SHA256, TAO_LOCK_BLOB_SHA256]
    exact_objects = all(exact_equal(local, remote) for local, remote in zip(stored, objects))
    release_paths = [WORKSPACE / "prime_dynamics_theory" / SOURCE_DIRECTORY / "results" / name for name in (
        "external_source_lock.json", "maynard_external_source_lock.json", "tao_external_source_lock.json",
    )]
    byte_exact = all(local.read_bytes() == inherited.read_bytes() for local, inherited in zip(paths, release_paths))
    hits = _remote_payload_hits()
    passed = (
        canonical == expected_canonical and blobs == expected_blobs and exact_objects and byte_exact
        and released.get("canonical_digests") == expected_canonical and hits == []
    )
    return {
        "canonical_digests": canonical, "count": 3,
        "external_payload_exclusion_pass": hits == [], "external_payload_hash_hits": hits,
        "local_lock_blob_digests": blobs, "local_lock_objects_exact_pass": exact_objects,
        "local_release_copies_byte_exact_pass": byte_exact, "network_fetch_performed": False,
        "objects": objects, "pass": passed,
        "redistributable_in_release": [False, False, True], "source_keys": keys,
    }


def build_source_closure() -> dict[str, object]:
    git = build_git_source_locks()
    remote = build_remote_source_locks()
    logical = digest_bytes((git["all_git_source_digest"] + "\n" + "\n".join(remote["canonical_digests"]) + "\n").encode("utf-8"))
    return {
        "git": git, "git_count": 117, "logical_count": 120,
        "logical_digest_pass": logical == EXPECTED_LOGICAL_SOURCE_DIGEST,
        "logical_source_digest": logical,
        "pass": git["pass"] is True and remote["pass"] is True and logical == EXPECTED_LOGICAL_SOURCE_DIGEST,
        "remote": remote, "remote_count": 3,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_source_closure(), sort_keys=True))
