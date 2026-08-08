"""Build the offline immutable-source-locked RH-387 result."""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from integral_resummation import (  # noqa: E402
    build_certificate,
    canonical_json_bytes,
    exact_equal,
    loads_strict,
    mutation_results,
    payload_sha256,
    verify_certificate,
)


RH386_RELEASE = "9778e3515d45816665d672a641947b93906abf54"
RH386_DIRECTORY = "papers/RH-386-vinogradov-korobov-growing-order-prime-tail-uniformization"
RH386_RESULT_SHA256 = "b59fc7921ef89d556fbc81a409ada9304fafc92424b0f4a79f97aa4d57f25ff4"
STANDARD8 = (
    "README.md",
    "THEOREM_LEDGER.md",
    "UPDATED_ROADMAP.md",
    "main.tex",
    "references.bib",
    "results/result.json",
    "results/result.schema.json",
    "src/vk_prime_tail/core.py",
)
EXPECTED_GROUP_SIZES = {"rh386_immutable_closure": 59, "rh386_standard8": 8, "rh386_external_lock": 1}
EXPECTED_GROUP_DIGESTS = {
    "rh386_immutable_closure": "62f05b53900a38353dbe3ff97629e2eedaa668707a33a0e355c7b398ee810f5b",
    "rh386_standard8": "ad8708e4d229d85d6d1f82163e9a5f0db1f8e7dd5d020f24a81cf97bca2bf9fb",
    "rh386_external_lock": "b66c168d2dde73ec9297fc4ad8ff9905de58e6c5b42696bc72161e6ef09ec78c",
}
EXPECTED_ALL_GIT_SOURCE_DIGEST = "19def5cbed919da8e9652012cf011f3b5728efd4b24a9eef0911bb7346467d27"
EXPECTED_LOGICAL_SOURCE_DIGEST = "5016397fe59962954514b3b42d68e9de6dfeff0dae949791b01c6a516f5c61fe"
REMOTE_LOCK_CANONICAL_SHA256 = "d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786"
REMOTE_LOCK_BLOB_SHA256 = "d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058"
CERTIFICATE_FIXTURE_BYTES = 10_785
CERTIFICATE_FIXTURE_SHA256 = "3c89e51662bbc2f1c7712f4205ff8cde88e9eb80636e2779d06154e914459b4b"
REMOTE_PAYLOAD_HASHES = {
    "565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2",
    "572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd",
    "2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")


def digest_bytes(data: bytes) -> str:
    if type(data) is not bytes:
        raise TypeError("digest input must be bytes")
    return sha256(data).hexdigest()


def digest(path: Path) -> str:
    hasher = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _validate_constants() -> None:
    values = [RH386_RESULT_SHA256, EXPECTED_ALL_GIT_SOURCE_DIGEST, EXPECTED_LOGICAL_SOURCE_DIGEST, REMOTE_LOCK_CANONICAL_SHA256, REMOTE_LOCK_BLOB_SHA256, CERTIFICATE_FIXTURE_SHA256, *EXPECTED_GROUP_DIGESTS.values(), *REMOTE_PAYLOAD_HASHES]
    if any(type(value) is not str or not SHA256.fullmatch(value) for value in values):
        raise ValueError("sealed SHA-256 constant is malformed")
    if type(RH386_RELEASE) is not str or not COMMIT.fullmatch(RH386_RELEASE):
        raise ValueError("RH-386 release commit is malformed")
    if type(CERTIFICATE_FIXTURE_BYTES) is not int or CERTIFICATE_FIXTURE_BYTES <= 0:
        raise ValueError("certificate byte fixture must be a positive exact int")
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
    if type(commit) is not str or not COMMIT.fullmatch(commit):
        raise ValueError("source commit must be exact lowercase 40-hex")
    path = Path(relative)
    if type(relative) is not str or path.is_absolute() or ".." in path.parts:
        raise ValueError("unsafe release path")
    completed = subprocess.run(["git", "show", f"{commit}:{relative}"], cwd=REPO, capture_output=True, check=False)
    if completed.returncode:
        raise RuntimeError(f"release blob unavailable: {commit}:{relative}")
    return completed.stdout


@lru_cache(maxsize=1)
def released_rh386_result() -> dict[str, object]:
    data = git_blob(RH386_RELEASE, f"{RH386_DIRECTORY}/results/result.json")
    if digest_bytes(data) != RH386_RESULT_SHA256:
        raise RuntimeError("released RH-386 result digest changed")
    result = loads_strict(data.decode("utf-8"))
    if result.get("status") != "RH-386_VK_growing_order_prime_tail_uniformization_certified":
        raise RuntimeError("released RH-386 status changed")
    locks = result.get("source_locks")
    if type(locks) is not dict or locks.get("git_count") != 59 or locks.get("remote_count") != 1:
        raise RuntimeError("released RH-386 source contract changed")
    return result


def source_digest_lines(entries: list[dict[str, object]]) -> tuple[str, ...]:
    lines: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise ValueError("source row membership changed")
        group, commit, path, source_sha = entry["group"], entry["commit"], entry["path"], entry["sha256"]
        if not all(type(item) is str for item in (group, commit, path, source_sha)):
            raise TypeError("source row types changed")
        _repo_relative(path)
        if path in seen:
            raise ValueError("duplicate source path")
        seen.add(path)
        if not COMMIT.fullmatch(commit) or not SHA256.fullmatch(source_sha):
            raise ValueError("source identifier format failed")
        lines.append(f"{group}\t{commit}\t{path}\t{source_sha}")
    return tuple(lines)


def lines_digest(lines: tuple[str, ...] | list[str]) -> str:
    if type(lines) not in (tuple, list) or any(type(line) is not str for line in lines):
        raise TypeError("digest lines must be exact text")
    return digest_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def _source_paths() -> dict[str, tuple[tuple[str, str | None], ...]]:
    released_entries = released_rh386_result()["source_locks"]["git"]["entries"]
    if type(released_entries) is not list or len(released_entries) != 59:
        raise RuntimeError("released RH-386 inherited closure is not 59 rows")
    inherited = []
    for row in released_entries:
        if type(row) is not dict or set(row) != {"group", "commit", "path", "sha256"}:
            raise ValueError("released inherited row membership changed")
        inherited.append((row["path"], row["sha256"]))
    standard = tuple((f"prime_dynamics_theory/{RH386_DIRECTORY}/{relative}", None) for relative in STANDARD8)
    external = ((f"prime_dynamics_theory/{RH386_DIRECTORY}/results/external_source_lock.json", REMOTE_LOCK_BLOB_SHA256),)
    return {"rh386_immutable_closure": tuple(inherited), "rh386_standard8": standard, "rh386_external_lock": external}


def build_git_source_locks(*, commit: str = RH386_RELEASE) -> dict[str, object]:
    _validate_constants()
    if type(commit) is not str or commit != RH386_RELEASE:
        raise ValueError("RH-386 release commit was rebound")
    groups = _source_paths()
    entries: list[dict[str, object]] = []
    group_sizes: dict[str, int] = {}
    group_digests: dict[str, str] = {}
    declared_pass = True
    live_pass = True
    for group in EXPECTED_GROUP_SIZES:
        rows = groups[group]
        if type(rows) is not tuple or len(rows) != EXPECTED_GROUP_SIZES[group]:
            raise ValueError("source group size changed")
        current: list[dict[str, object]] = []
        for workspace_path, declared_sha in rows:
            relative = _repo_relative(workspace_path)
            blob_sha = digest_bytes(git_blob(commit, relative))
            if declared_sha is not None and (type(declared_sha) is not str or blob_sha != declared_sha):
                declared_pass = False
            live_path = WORKSPACE / workspace_path
            if not live_path.is_file() or digest(live_path) != blob_sha:
                live_pass = False
            row = {"group": group, "commit": commit, "path": workspace_path, "sha256": blob_sha}
            current.append(row)
            entries.append(row)
        group_sizes[group] = len(current)
        group_digests[group] = lines_digest(source_digest_lines(current))
    if len(entries) != 68 or len({row["path"] for row in entries}) != 68:
        raise RuntimeError("Git source closure is not 68 unique rows")
    all_digest = lines_digest(source_digest_lines(entries))
    digest_pass = group_digests == EXPECTED_GROUP_DIGESTS and all_digest == EXPECTED_ALL_GIT_SOURCE_DIGEST
    return {
        "status": "RH-387_immutable_git_source_lock",
        "count": 68,
        "group_sizes": group_sizes,
        "group_digests": group_digests,
        "all_git_source_digest": all_digest,
        "entries": entries,
        "release_blob_identity_pass": declared_pass,
        "live_file_identity_pass": live_pass,
        "digest_contract_pass": digest_pass,
        "mutable_root_files_excluded": True,
        "pass": declared_pass and live_pass and digest_pass,
    }


def build_remote_source_lock() -> dict[str, object]:
    local = loads_strict((ROOT / "results" / "external_source_lock.json").read_text())
    upstream = loads_strict(git_blob(RH386_RELEASE, f"{RH386_DIRECTORY}/results/external_source_lock.json").decode("utf-8"))
    exact_pass = exact_equal(local, upstream)
    canonical_sha = payload_sha256(local)
    payload_hits = []
    for path in ROOT.rglob("*"):
        if path.is_file() and digest(path) in REMOTE_PAYLOAD_HASHES:
            payload_hits.append(path.relative_to(ROOT).as_posix())
    return {
        "count": 1,
        "objects": [local],
        "lock_object_sha256": canonical_sha,
        "upstream_exact_pass": exact_pass,
        "canonical_digest_pass": canonical_sha == REMOTE_LOCK_CANONICAL_SHA256,
        "network_fetch_performed": False,
        "redistributable_in_release": False,
        "external_payload_hash_hits": payload_hits,
        "external_payload_exclusion_pass": not payload_hits,
        "pass": exact_pass and canonical_sha == REMOTE_LOCK_CANONICAL_SHA256 and not payload_hits and local.get("pdf_vendored") is False and local.get("source_tar_vendored") is False and local.get("redistributable_in_release") is False,
    }


GATES = {
    "A_intrinsic_determinant": False,
    "B_scattering_completion": False,
    "C_self_adjoint_generator": False,
    "D_von_mangoldt_weighted_prime_power_traces": False,
    "E_completed_zeta_divisor_equality": False,
}
FORBIDDEN = {
    "second_order_or_P2_precision": False,
    "complex_c": False,
    "active_phasewise_c11": False,
    "growing_clock": False,
    "operator_trace_or_zeros": False,
    "proof_of_RH": False,
    "vendored_external_source": False,
}


def build_payload() -> dict[str, object]:
    _validate_constants()
    certificate = build_certificate()
    verify_certificate(certificate, compare_fresh=False)
    certificate_bytes = len(canonical_json_bytes(certificate))
    certificate_sha = payload_sha256(certificate)
    fixture_pass = certificate_bytes == CERTIFICATE_FIXTURE_BYTES and certificate_sha == CERTIFICATE_FIXTURE_SHA256
    mutations = mutation_results()
    git_locks = build_git_source_locks()
    remote_lock = build_remote_source_lock()
    logical_digest = digest_bytes((git_locks["all_git_source_digest"] + "\n" + remote_lock["lock_object_sha256"] + "\n").encode("utf-8"))
    logical_digest_pass = logical_digest == EXPECTED_LOGICAL_SOURCE_DIGEST
    source_pass = git_locks["pass"] is True and remote_lock["pass"] is True and logical_digest_pass
    all_pass = all((fixture_pass, certificate["all_pass"] is True, mutations["all_pass"] is True, source_pass, not any(GATES.values()), not any(FORBIDDEN.values())))
    return {
        "status": "RH-387_all_order_integral_resummation_certified",
        "paper": "RH-387",
        "title": "All-Order Prime-Tail Integral Resummation",
        "certificate_fixture": {"canonical_bytes": certificate_bytes, "sha256": certificate_sha, "pass": fixture_pass},
        "certificate": certificate,
        "mutations": {**mutations, "verification_mode": "independently recomputed field-level semantic verification"},
        "source_locks": {"git": git_locks, "remote": remote_lock, "git_count": 68, "remote_count": 1, "logical_count": 69, "logical_source_digest": logical_digest, "logical_digest_pass": logical_digest_pass, "pass": source_pass},
        "theorem": {
            "source": "pi^2*abs(GapP-GapJ)<=3528*epsilon/(x*L)",
            "power": "pi^2*abs(GapJ-GapI)<=588/(x^3*L)",
            "combined": "pi^2*abs(GapP-GapI)<=3528*epsilon/(x*L)+588/(x^3*L)",
            "range": "x=p_y,L=log(x)>=512,c in {1,...,7}",
            "endpoint_gradient": "sup_[0,1/2]^7 ||grad F||_1<=126",
        },
        "gates": GATES,
        "forbidden_claims": FORBIDDEN,
        "declarations": {"network_fetch_performed": False, "external_payload_vendored": False, "finite_rows_are_analytic_proof": False},
        "all_pass": all_pass,
    }


def main() -> None:
    payload = build_payload()
    if payload["all_pass"] is not True:
        raise RuntimeError("RH-387 result gates failed")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps({"status": payload["status"], "all_pass": payload["all_pass"], "git": 68, "remote": 1}, sort_keys=True))


if __name__ == "__main__":
    main()
