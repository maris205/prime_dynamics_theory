"""Immutable 87-Git-plus-two-remote source closure for RH-390."""

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

from growing_rank_filtration.core import canonical_json_bytes, exact_equal, loads_strict  # noqa: E402


RH388_RELEASE = "8e6f89ee1e58e67c53c5f4719c05e881107113ac"
RH388_DIRECTORY = "papers/RH-388-rank-one-p2-tail-resummation"
RH388_RESULT_SHA256 = "b80e29174e6616bc7f4c2de999069ba9d745d80d7c46f88ae8046bf2b5b41665"
STANDARD8 = (
    "README.md",
    "THEOREM_LEDGER.md",
    "UPDATED_ROADMAP.md",
    "main.tex",
    "references.bib",
    "results/result.json",
    "results/result.schema.json",
    "src/rank_one_p2/core.py",
)
PRIOR_EXTERNAL_LOCKS = (
    "results/external_source_lock.json",
    "results/maynard_external_source_lock.json",
)
EXPECTED_GROUP_SIZES = {
    "rh388_immutable_closure": 77,
    "rh388_standard8": 8,
    "rh388_prior_external_locks": 2,
}
EXPECTED_GROUP_DIGESTS = {
    "rh388_immutable_closure": "58f4b206af77d7f7fcbf1e40f4cd26f65d122abed6132e1f223ecb986a41674a",
    "rh388_standard8": "2309e1d1fd5a2578b3cbcabb150f6ccdaddb2f33efa8dee53f487786c3b08963",
    "rh388_prior_external_locks": "16699df9407ffded0a9d78027b55ff42a711d9968f1d77326a7411eb2c50f8de",
}
EXPECTED_ALL_GIT_SOURCE_DIGEST = "b86cb21288fe9c48304d90ae812829f5e44f4fac0a2b725a09e5c1512ca60cab"
JY_CANONICAL_SHA256 = "d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786"
MAYNARD_CANONICAL_SHA256 = "bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e"
JY_LOCK_BLOB_SHA256 = "d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058"
MAYNARD_LOCK_BLOB_SHA256 = "9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba"
EXPECTED_LOGICAL_SOURCE_DIGEST = "2255b26dd68adf09f447e251eb5d38c8b1d31fbaa1c26befd8c04165097ed922"
REMOTE_PAYLOAD_HASHES = {
    "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2",
    "572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd",
    "2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602",
    "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349",
}
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
    hashes = [
        RH388_RESULT_SHA256,
        EXPECTED_ALL_GIT_SOURCE_DIGEST,
        JY_CANONICAL_SHA256,
        MAYNARD_CANONICAL_SHA256,
        JY_LOCK_BLOB_SHA256,
        MAYNARD_LOCK_BLOB_SHA256,
        EXPECTED_LOGICAL_SOURCE_DIGEST,
        *EXPECTED_GROUP_DIGESTS.values(),
        *REMOTE_PAYLOAD_HASHES,
    ]
    if any(type(value) is not str or not SHA256_RE.fullmatch(value) for value in hashes):
        raise ValueError("sealed SHA-256 constant is malformed")
    if type(RH388_RELEASE) is not str or not COMMIT_RE.fullmatch(RH388_RELEASE):
        raise ValueError("RH-388 release commit is malformed")
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
        ["git", "show", f"{commit}:{relative}"],
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(f"release blob unavailable: {commit}:{relative}")
    return completed.stdout


@lru_cache(maxsize=1)
def released_rh388_result() -> dict[str, object]:
    data = git_blob(RH388_RELEASE, f"{RH388_DIRECTORY}/results/result.json")
    if digest_bytes(data) != RH388_RESULT_SHA256:
        raise RuntimeError("released RH-388 result digest changed")
    result = loads_strict(data.decode("utf-8"))
    if result.get("status") != "RH-388_rank_one_P2_tail_resummation_certified":
        raise RuntimeError("released RH-388 status changed")
    locks = result.get("source_locks")
    if type(locks) is not dict:
        raise RuntimeError("released RH-388 source contract is not an object")
    if (locks.get("git_count"), locks.get("remote_count"), locks.get("logical_count")) != (77, 2, 79):
        raise RuntimeError("released RH-388 source counts changed")
    return result


def source_digest_lines(entries: list[dict[str, object]]) -> tuple[str, ...]:
    if type(entries) is not list:
        raise TypeError("source entries must be an exact list")
    lines: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise ValueError("source row membership changed")
        group = entry["group"]
        commit = entry["commit"]
        path = entry["path"]
        source_sha = entry["sha256"]
        if not all(type(item) is str for item in (group, commit, path, source_sha)):
            raise TypeError("source row types changed")
        _repo_relative(path)  # type: ignore[arg-type]
        if path in seen:
            raise ValueError("duplicate source path")
        seen.add(path)  # type: ignore[arg-type]
        if not COMMIT_RE.fullmatch(commit) or not SHA256_RE.fullmatch(source_sha):  # type: ignore[arg-type]
            raise ValueError("source identifier format failed")
        lines.append(f"{group}\t{commit}\t{path}\t{source_sha}")
    return tuple(lines)


def lines_digest(lines: tuple[str, ...] | list[str]) -> str:
    if type(lines) not in (tuple, list) or any(type(line) is not str for line in lines):
        raise TypeError("digest lines must be exact text")
    return digest_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def _source_paths() -> dict[str, tuple[tuple[str, str | None], ...]]:
    released_entries = released_rh388_result()["source_locks"]["git"]["entries"]  # type: ignore[index]
    if type(released_entries) is not list or len(released_entries) != 77:
        raise RuntimeError("released RH-388 immutable closure is not 77 rows")
    inherited: list[tuple[str, str | None]] = []
    for row in released_entries:
        if type(row) is not dict or set(row) != {"group", "commit", "path", "sha256"}:
            raise ValueError("released inherited row membership changed")
        path = row["path"]
        source_sha = row["sha256"]
        if type(path) is not str or type(source_sha) is not str:
            raise TypeError("released inherited row types changed")
        inherited.append((path, source_sha))
    standard = tuple((f"prime_dynamics_theory/{RH388_DIRECTORY}/{relative}", None) for relative in STANDARD8)
    external = tuple(
        (
            f"prime_dynamics_theory/{RH388_DIRECTORY}/{relative}",
            JY_LOCK_BLOB_SHA256 if relative.endswith("/external_source_lock.json") else MAYNARD_LOCK_BLOB_SHA256,
        )
        for relative in PRIOR_EXTERNAL_LOCKS
    )
    return {
        "rh388_immutable_closure": tuple(inherited),
        "rh388_standard8": standard,
        "rh388_prior_external_locks": external,
    }


def build_git_source_locks(*, commit: str = RH388_RELEASE) -> dict[str, object]:
    _validate_constants()
    if type(commit) is not str or commit != RH388_RELEASE:
        raise ValueError("RH-388 release commit was rebound")
    groups = _source_paths()
    entries: list[dict[str, object]] = []
    group_sizes: dict[str, int] = {}
    group_digests: dict[str, str] = {}
    release_pass = True
    live_pass = True
    for group in EXPECTED_GROUP_SIZES:
        rows = groups[group]
        if type(rows) is not tuple or len(rows) != EXPECTED_GROUP_SIZES[group]:
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
    digest_pass = group_digests == EXPECTED_GROUP_DIGESTS and all_digest == EXPECTED_ALL_GIT_SOURCE_DIGEST
    return {
        "all_git_source_digest": all_digest,
        "count": len(entries),
        "digest_contract_pass": digest_pass,
        "entries": entries,
        "group_digests": group_digests,
        "group_sizes": group_sizes,
        "live_identity_pass": live_pass,
        "pass": release_pass and live_pass and digest_pass and len(entries) == 87,
        "release_identity_pass": release_pass,
    }


def _remote_payload_hits() -> list[str]:
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        try:
            source_sha = digest(path)
        except OSError:
            continue
        if source_sha in REMOTE_PAYLOAD_HASHES:
            hits.append(path.relative_to(ROOT).as_posix())
    return sorted(hits)


def build_remote_source_locks() -> dict[str, object]:
    _validate_constants()
    released_remote = released_rh388_result()["source_locks"]["remote"]  # type: ignore[index]
    if type(released_remote) is not dict or released_remote.get("count") != 2:
        raise RuntimeError("released RH-388 remote closure changed")
    objects = released_remote.get("objects")
    if type(objects) is not list or len(objects) != 2 or any(type(item) is not dict for item in objects):
        raise RuntimeError("released remote source objects changed")
    ordered_objects = sorted((deepcopy(item) for item in objects), key=lambda item: item["source_key"])  # type: ignore[index]
    expected_keys = ["johnston-yang-arxiv-2204.01980v2", "maynard-annals-2015-small-gaps"]
    if [item["source_key"] for item in ordered_objects] != expected_keys:
        raise RuntimeError("remote source order changed")
    canonical_digests = [digest_bytes(canonical_json_bytes(item)) for item in ordered_objects]
    expected_canonical = [JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256]
    local_paths = [
        ROOT / "results" / "external_source_lock.json",
        ROOT / "results" / "maynard_external_source_lock.json",
    ]
    stored_objects = [loads_strict(path.read_text(encoding="utf-8")) for path in local_paths]
    local_blob_digests = [digest(path) for path in local_paths]
    expected_blobs = [JY_LOCK_BLOB_SHA256, MAYNARD_LOCK_BLOB_SHA256]
    exact_objects = all(exact_equal(stored, released) for stored, released in zip(stored_objects, ordered_objects))
    hits = _remote_payload_hits()
    contract_pass = (
        canonical_digests == expected_canonical
        and local_blob_digests == expected_blobs
        and exact_objects
        and released_remote.get("canonical_digests") == expected_canonical
        and hits == []
    )
    return {
        "canonical_digests": canonical_digests,
        "count": 2,
        "external_payload_exclusion_pass": hits == [],
        "external_payload_hash_hits": hits,
        "local_lock_blob_digests": local_blob_digests,
        "local_lock_objects_exact_pass": exact_objects,
        "network_fetch_performed": False,
        "objects": ordered_objects,
        "pass": contract_pass,
        "redistributable_in_release": False,
        "source_keys": expected_keys,
    }


def build_source_closure() -> dict[str, object]:
    git = build_git_source_locks()
    remote = build_remote_source_locks()
    logical = digest_bytes(
        (git["all_git_source_digest"] + "\n" + "\n".join(remote["canonical_digests"]) + "\n").encode("utf-8")  # type: ignore[arg-type]
    )
    logical_pass = logical == EXPECTED_LOGICAL_SOURCE_DIGEST
    return {
        "git": git,
        "git_count": 87,
        "logical_count": 89,
        "logical_digest_pass": logical_pass,
        "logical_source_digest": logical,
        "pass": git["pass"] is True and remote["pass"] is True and logical_pass,
        "remote": remote,
        "remote_count": 2,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_source_closure(), sort_keys=True))
