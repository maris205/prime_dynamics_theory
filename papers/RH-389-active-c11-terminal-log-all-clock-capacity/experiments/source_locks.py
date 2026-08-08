"""Immutable 95-Git-plus-three-remote source closure for RH-389."""

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

from verify_tao_source import (  # noqa: E402
    canonical_json_bytes,
    exact_equal,
    loads_strict,
    tao_source_lock,
)


RH388_RELEASE = "8e6f89ee1e58e67c53c5f4719c05e881107113ac"
RH388_DIRECTORY = "papers/RH-388-rank-one-p2-tail-resummation"
RH388_RESULT_SHA256 = "b80e29174e6616bc7f4c2de999069ba9d745d80d7c46f88ae8046bf2b5b41665"
TPC137_RELEASE = "0a67723ee2d0dd3171ee294816b8902b6e65285d"
TPC137_DIRECTORY = "papers/tpc-137-prime-square-fixed-two-log-closure"
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
TPC137_RELEASE8 = (
    ".gitattributes",
    ".gitignore",
    "README.md",
    "experiments/tpc137_prime_square_log_audit.json",
    "experiments/tpc137_prime_square_log_audit.py",
    "main.tex",
    "references.bib",
    "tpc-137-prime-square-fixed-two-log-closure.pdf",
)
EXPECTED_GROUP_SIZES = {
    "rh388_immutable_closure": 77,
    "rh388_standard8": 8,
    "rh388_prior_external_locks": 2,
    "tpc137_release8": 8,
}
EXPECTED_GROUP_DIGESTS = {
    "rh388_immutable_closure": "58f4b206af77d7f7fcbf1e40f4cd26f65d122abed6132e1f223ecb986a41674a",
    "rh388_standard8": "2309e1d1fd5a2578b3cbcabb150f6ccdaddb2f33efa8dee53f487786c3b08963",
    "rh388_prior_external_locks": "16699df9407ffded0a9d78027b55ff42a711d9968f1d77326a7411eb2c50f8de",
    "tpc137_release8": "30deeeaed84782bb603058c3d6b521aa427eb44c04792640520593a149f32f7a",
}
EXPECTED_ALL_GIT_SOURCE_DIGEST = "b7ff5b520d5e926f19346a1ac6e49fbccf07c5fe24de60758179e9959e673353"
JY_CANONICAL_SHA256 = "d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786"
MAYNARD_CANONICAL_SHA256 = "bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e"
TAO_CANONICAL_SHA256 = "d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84"
JY_LOCK_BLOB_SHA256 = "d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058"
MAYNARD_LOCK_BLOB_SHA256 = "9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba"
TAO_LOCK_BLOB_SHA256 = "825b3455be5eac151b7478f537fa6c503ae8eb02004cd8da821ca802d4ebdd8f"
EXPECTED_LOGICAL_SOURCE_DIGEST = "99a9e6d4372a081b028c28acba7de539850b4092b64063d9553ca261809e3e74"
REMOTE_PAYLOAD_HASHES = {
    "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2",
    "572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd",
    "2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602",
    "3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349",
    "a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2",
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
        TAO_CANONICAL_SHA256,
        JY_LOCK_BLOB_SHA256,
        MAYNARD_LOCK_BLOB_SHA256,
        TAO_LOCK_BLOB_SHA256,
        EXPECTED_LOGICAL_SOURCE_DIGEST,
        *EXPECTED_GROUP_DIGESTS.values(),
        *REMOTE_PAYLOAD_HASHES,
    ]
    if any(type(value) is not str or not SHA256_RE.fullmatch(value) for value in hashes):
        raise ValueError("sealed SHA-256 constant is malformed")
    for commit in (RH388_RELEASE, TPC137_RELEASE):
        if type(commit) is not str or not COMMIT_RE.fullmatch(commit):
            raise ValueError("sealed release commit is malformed")
    if list(EXPECTED_GROUP_SIZES) != list(EXPECTED_GROUP_DIGESTS):
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
    if type(relative) is not str:
        raise TypeError("release path must be exact text")
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
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
    if type(result) is not dict or result.get("status") != "RH-388_rank_one_P2_tail_resummation_certified":
        raise RuntimeError("released RH-388 status changed")
    locks = result.get("source_locks")
    if type(locks) is not dict or locks.get("git_count") != 77 or locks.get("remote_count") != 2:
        raise RuntimeError("released RH-388 source contract changed")
    return result


def source_digest_lines(entries: list[dict[str, object]]) -> tuple[str, ...]:
    lines: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise ValueError("source row membership changed")
        group, commit, path, source_sha = (entry[key] for key in ("group", "commit", "path", "sha256"))
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


def _source_paths() -> dict[str, tuple[tuple[str, str, str | None], ...]]:
    released_entries = released_rh388_result()["source_locks"]["git"]["entries"]  # type: ignore[index]
    if type(released_entries) is not list or len(released_entries) != 77:
        raise RuntimeError("released RH-388 inherited closure is not 77 rows")
    inherited: list[tuple[str, str, str | None]] = []
    for row in released_entries:
        if type(row) is not dict or set(row) != {"group", "commit", "path", "sha256"}:
            raise ValueError("released inherited row membership changed")
        inherited.append((row["path"], RH388_RELEASE, row["sha256"]))  # type: ignore[arg-type]
    standard = tuple(
        (f"prime_dynamics_theory/{RH388_DIRECTORY}/{relative}", RH388_RELEASE, None)
        for relative in STANDARD8
    )
    prior = tuple(
        (f"prime_dynamics_theory/{RH388_DIRECTORY}/{relative}", RH388_RELEASE, None)
        for relative in PRIOR_EXTERNAL_LOCKS
    )
    tpc = tuple(
        (f"prime_dynamics_theory/{TPC137_DIRECTORY}/{relative}", TPC137_RELEASE, None)
        for relative in TPC137_RELEASE8
    )
    return {
        "rh388_immutable_closure": tuple(inherited),
        "rh388_standard8": standard,
        "rh388_prior_external_locks": prior,
        "tpc137_release8": tpc,
    }


def build_git_source_locks(
    *,
    rh388_commit: str = RH388_RELEASE,
    tpc137_commit: str = TPC137_RELEASE,
) -> dict[str, object]:
    _validate_constants()
    if type(rh388_commit) is not str or rh388_commit != RH388_RELEASE:
        raise ValueError("RH-388 release commit was rebound")
    if type(tpc137_commit) is not str or tpc137_commit != TPC137_RELEASE:
        raise ValueError("TPC-137 release commit was rebound")
    entries: list[dict[str, object]] = []
    group_sizes: dict[str, int] = {}
    group_digests: dict[str, str] = {}
    release_pass = True
    live_pass = True
    groups = _source_paths()
    for group in EXPECTED_GROUP_SIZES:
        rows = groups[group]
        if type(rows) is not tuple or len(rows) != EXPECTED_GROUP_SIZES[group]:
            raise RuntimeError(f"source group size changed: {group}")
        current: list[dict[str, object]] = []
        for workspace_path, commit, expected_sha in rows:
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
        "pass": release_pass and live_pass and digest_pass and len(entries) == 95,
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


def _load_local_lock(name: str) -> tuple[dict[str, object], str]:
    if type(name) is not str or name not in {
        "external_source_lock.json",
        "maynard_external_source_lock.json",
        "tao_external_source_lock.json",
    }:
        raise ValueError("local remote-lock name changed")
    path = ROOT / "results" / name
    value = loads_strict(path.read_text(encoding="utf-8"))
    if type(value) is not dict:
        raise ValueError("local remote lock is not an object")
    return value, digest(path)


def build_remote_source_locks() -> dict[str, object]:
    _validate_constants()
    released_remote = released_rh388_result()["source_locks"]["remote"]  # type: ignore[index]
    if type(released_remote) is not dict or released_remote.get("count") != 2:
        raise RuntimeError("released RH-388 remote source closure changed")
    inherited = released_remote.get("objects")
    if type(inherited) is not list or len(inherited) != 2 or any(type(row) is not dict for row in inherited):
        raise RuntimeError("released inherited remote objects changed")
    inherited_by_key = {row["source_key"]: row for row in inherited}
    if set(inherited_by_key) != {
        "johnston-yang-arxiv-2204.01980v2",
        "maynard-annals-2015-small-gaps",
    }:
        raise RuntimeError("released inherited remote keys changed")
    jy = inherited_by_key["johnston-yang-arxiv-2204.01980v2"]
    maynard = inherited_by_key["maynard-annals-2015-small-gaps"]
    tao = tao_source_lock()
    local_jy, jy_blob = _load_local_lock("external_source_lock.json")
    local_maynard, maynard_blob = _load_local_lock("maynard_external_source_lock.json")
    local_tao, tao_blob = _load_local_lock("tao_external_source_lock.json")
    expected_release_blobs = {
        "external_source_lock.json": git_blob(RH388_RELEASE, f"{RH388_DIRECTORY}/results/external_source_lock.json"),
        "maynard_external_source_lock.json": git_blob(RH388_RELEASE, f"{RH388_DIRECTORY}/results/maynard_external_source_lock.json"),
    }
    local_release_copy_pass = (
        (ROOT / "results" / "external_source_lock.json").read_bytes() == expected_release_blobs["external_source_lock.json"]
        and (ROOT / "results" / "maynard_external_source_lock.json").read_bytes() == expected_release_blobs["maynard_external_source_lock.json"]
    )
    ordered = sorted(
        (
            (jy["source_key"], digest_bytes(canonical_json_bytes(jy)), jy),
            (maynard["source_key"], digest_bytes(canonical_json_bytes(maynard)), maynard),
            (tao["source_key"], digest_bytes(canonical_json_bytes(tao)), tao),
        ),
        key=lambda row: row[0],
    )
    expected_keys = [
        "johnston-yang-arxiv-2204.01980v2",
        "maynard-annals-2015-small-gaps",
        "tao-cambridge-2016-logarithmic-chowla",
    ]
    canonical_digests = [row[1] for row in ordered]
    expected_digests = [JY_CANONICAL_SHA256, MAYNARD_CANONICAL_SHA256, TAO_CANONICAL_SHA256]
    hits = _remote_payload_hits()
    object_pass = (
        exact_equal(local_jy, jy)
        and exact_equal(local_maynard, maynard)
        and exact_equal(local_tao, tao)
    )
    blob_pass = [jy_blob, maynard_blob, tao_blob] == [
        JY_LOCK_BLOB_SHA256,
        MAYNARD_LOCK_BLOB_SHA256,
        TAO_LOCK_BLOB_SHA256,
    ]
    contract_pass = (
        [row[0] for row in ordered] == expected_keys
        and canonical_digests == expected_digests
        and object_pass
        and blob_pass
        and local_release_copy_pass
        and hits == []
    )
    return {
        "canonical_digests": canonical_digests,
        "count": 3,
        "external_payload_exclusion_pass": hits == [],
        "external_payload_hash_hits": hits,
        "local_lock_blob_digests": [jy_blob, maynard_blob, tao_blob],
        "local_lock_objects_exact_pass": object_pass,
        "local_release_copies_byte_exact_pass": local_release_copy_pass,
        "network_fetch_performed": False,
        "objects": [row[2] for row in ordered],
        "pass": contract_pass,
        "redistributable_in_release": [False, False, True],
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
        "git_count": 95,
        "logical_count": 98,
        "logical_digest_pass": logical_pass,
        "logical_source_digest": logical,
        "pass": git["pass"] is True and remote["pass"] is True and logical_pass,
        "remote": remote,
        "remote_count": 3,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_source_closure(), sort_keys=True))
