"""Immutable 77-Git-plus-two-remote source closure for RH-388."""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
WORKSPACE = ROOT.parents[2]
if str(ROOT / "experiments") not in sys.path:
    sys.path.insert(0, str(ROOT / "experiments"))

from verify_remote_source import (  # noqa: E402
    canonical_json_bytes,
    exact_equal,
    loads_strict,
    maynard_source_lock,
)


RH387_RELEASE = "dedd8e8d2c44564e66524a646f9cf5fb9a389c77"
RH387_DIRECTORY = "papers/RH-387-all-order-prime-tail-integral-resummation"
RH387_RESULT_SHA256 = "d71c69de7e5d05c5ac558a17d2a6089815334d19b43a74ecfde219affcc1e16c"
STANDARD8 = (
    "README.md",
    "THEOREM_LEDGER.md",
    "UPDATED_ROADMAP.md",
    "main.tex",
    "references.bib",
    "results/result.json",
    "results/result.schema.json",
    "src/integral_resummation/core.py",
)
EXPECTED_GROUP_SIZES = {
    "rh387_immutable_closure": 68,
    "rh387_standard8": 8,
    "rh387_external_lock": 1,
}
EXPECTED_GROUP_DIGESTS = {
    "rh387_immutable_closure": "d4d516d5671d1a64ce288a31e2ae9d18141a0b6770e3ecbff6a381e4796e6e60",
    "rh387_standard8": "643488e81c1110bd6a3d5a96dba59c2e8d029ab41b0db2e460d564f1918f62fb",
    "rh387_external_lock": "4d84c2a8623fb21ef9102dd14d0b6b1e47a3ce6eb12f1e39e43b2e1439057573",
}
EXPECTED_ALL_GIT_SOURCE_DIGEST = "d7f2ee43f56631c8f3442db8fcc6fb423a801b5af7607351623cd449a92c3f73"
JY_CANONICAL_SHA256 = "d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786"
MAYNARD_CANONICAL_SHA256 = "bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e"
MAYNARD_LOCK_BLOB_SHA256 = "9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba"
EXPECTED_LOGICAL_SOURCE_DIGEST = "bffce602d6e3b568eb96662820f08aa457ff5d0de4065f3c9eeac53d8d8dfa39"
RH387_EXTERNAL_LOCK_BLOB_SHA256 = "d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058"
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
    hasher = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _validate_constants() -> None:
    hashes = [
        RH387_RESULT_SHA256,
        EXPECTED_ALL_GIT_SOURCE_DIGEST,
        JY_CANONICAL_SHA256,
        MAYNARD_CANONICAL_SHA256,
        MAYNARD_LOCK_BLOB_SHA256,
        EXPECTED_LOGICAL_SOURCE_DIGEST,
        RH387_EXTERNAL_LOCK_BLOB_SHA256,
        *EXPECTED_GROUP_DIGESTS.values(),
        *REMOTE_PAYLOAD_HASHES,
    ]
    if any(type(value) is not str or not SHA256_RE.fullmatch(value) for value in hashes):
        raise ValueError("sealed SHA-256 constant is malformed")
    if type(RH387_RELEASE) is not str or not COMMIT_RE.fullmatch(RH387_RELEASE):
        raise ValueError("RH-387 release commit is malformed")
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
def released_rh387_result() -> dict[str, object]:
    data = git_blob(RH387_RELEASE, f"{RH387_DIRECTORY}/results/result.json")
    if digest_bytes(data) != RH387_RESULT_SHA256:
        raise RuntimeError("released RH-387 result digest changed")
    result = loads_strict(data.decode("utf-8"))
    if type(result) is not dict or result.get("status") != "RH-387_all_order_integral_resummation_certified":
        raise RuntimeError("released RH-387 status changed")
    locks = result.get("source_locks")
    if type(locks) is not dict or locks.get("git_count") != 68 or locks.get("remote_count") != 1:
        raise RuntimeError("released RH-387 source contract changed")
    return result


def source_digest_lines(entries: list[dict[str, object]]) -> tuple[str, ...]:
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
    released_entries = released_rh387_result()["source_locks"]["git"]["entries"]  # type: ignore[index]
    if type(released_entries) is not list or len(released_entries) != 68:
        raise RuntimeError("released RH-387 inherited closure is not 68 rows")
    inherited: list[tuple[str, str | None]] = []
    for row in released_entries:
        if type(row) is not dict or set(row) != {"group", "commit", "path", "sha256"}:
            raise ValueError("released inherited row membership changed")
        inherited.append((row["path"], row["sha256"]))  # type: ignore[arg-type]
    standard = tuple((f"prime_dynamics_theory/{RH387_DIRECTORY}/{relative}", None) for relative in STANDARD8)
    external = ((f"prime_dynamics_theory/{RH387_DIRECTORY}/results/external_source_lock.json", RH387_EXTERNAL_LOCK_BLOB_SHA256),)
    return {
        "rh387_immutable_closure": tuple(inherited),
        "rh387_standard8": standard,
        "rh387_external_lock": external,
    }


def build_git_source_locks(*, commit: str = RH387_RELEASE) -> dict[str, object]:
    _validate_constants()
    if type(commit) is not str or commit != RH387_RELEASE:
        raise ValueError("RH-387 release commit was rebound")
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
        "pass": release_pass and live_pass and digest_pass and len(entries) == 77,
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
    released_remote = released_rh387_result()["source_locks"]["remote"]  # type: ignore[index]
    if type(released_remote) is not dict or released_remote.get("count") != 1:
        raise RuntimeError("released RH-387 remote source closure changed")
    objects = released_remote.get("objects")
    if type(objects) is not list or len(objects) != 1 or type(objects[0]) is not dict:
        raise RuntimeError("released Johnston--Yang object changed")
    jy = objects[0]
    jy_sha = digest_bytes(canonical_json_bytes(jy))
    stored_jy_path = ROOT / "results" / "external_source_lock.json"
    stored_jy = loads_strict(stored_jy_path.read_text(encoding="utf-8"))
    stored_jy_blob_sha = digest(stored_jy_path)
    maynard = maynard_source_lock()
    maynard_sha = digest_bytes(canonical_json_bytes(maynard))
    stored_maynard = loads_strict((ROOT / "results" / "maynard_external_source_lock.json").read_text(encoding="utf-8"))
    blob_sha = digest(ROOT / "results" / "maynard_external_source_lock.json")
    ordered = sorted(((jy["source_key"], jy_sha, jy), (maynard["source_key"], maynard_sha, maynard)), key=lambda row: row[0])
    if [row[0] for row in ordered] != ["johnston-yang-arxiv-2204.01980v2", "maynard-annals-2015-small-gaps"]:
        raise RuntimeError("remote source order changed")
    hits = _remote_payload_hits()
    contract_pass = (
        jy_sha == JY_CANONICAL_SHA256
        and exact_equal(stored_jy, jy)
        and stored_jy_blob_sha == RH387_EXTERNAL_LOCK_BLOB_SHA256
        and maynard_sha == MAYNARD_CANONICAL_SHA256
        and blob_sha == MAYNARD_LOCK_BLOB_SHA256
        and exact_equal(stored_maynard, maynard)
        and released_remote.get("lock_object_sha256") == JY_CANONICAL_SHA256
        and hits == []
    )
    return {
        "canonical_digests": [row[1] for row in ordered],
        "count": 2,
        "external_payload_exclusion_pass": hits == [],
        "external_payload_hash_hits": hits,
        "network_fetch_performed": False,
        "local_lock_blob_digests": [stored_jy_blob_sha, blob_sha],
        "local_lock_objects_exact_pass": exact_equal(stored_jy, jy) and exact_equal(stored_maynard, maynard),
        "objects": [row[2] for row in ordered],
        "pass": contract_pass,
        "redistributable_in_release": False,
        "source_keys": [row[0] for row in ordered],
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
        "git_count": 77,
        "logical_count": 79,
        "logical_digest_pass": logical_pass,
        "logical_source_digest": logical,
        "pass": git["pass"] is True and remote["pass"] is True and logical_pass,
        "remote": remote,
        "remote_count": 2,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_source_closure(), sort_keys=True))
