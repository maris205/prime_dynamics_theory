"""Build the offline, immutable-source-locked RH-386 result ledger."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from vk_prime_tail import (  # noqa: E402
    build_certificate,
    auxiliary_attack_results,
    canonical_json_bytes,
    exact_equal,
    loads_strict,
    mutation_results,
    payload_sha256,
    verify_certificate,
)


RH384_RELEASE = "386b66a55c9263353c7d407fd712be7e6279f1e6"
RH384_DIRECTORY = "papers/RH-384-prime-tail-scale-separation"
RH384_RESULT_SHA256 = "4365c693461cdc4d5d986c97e7dcf4bbfcac6ff2136e1a20779d4b4e46078c69"
RH384_SOURCE_DIGEST = "90434e0468ecc062cb522da096a267748725b5dca8e59c642bb7711f45a3e0e4"
RH384_MAIN_SHA256 = "f38a39739ec472c3d0c846638739e9e5cb57b6679f60f8f90ba1e2a6188186ef"
SOURCE_COMMITS = {
    "rh384_immutable_closure": RH384_RELEASE,
    "rh384_standard8": RH384_RELEASE,
}
STANDARD8 = (
    "README.md",
    "THEOREM_LEDGER.md",
    "UPDATED_ROADMAP.md",
    "main.tex",
    "references.bib",
    "results/result.json",
    "results/result.schema.json",
    "src/prime_tail_scales/core.py",
)
EXPECTED_GROUP_SIZES = {"rh384_immutable_closure": 51, "rh384_standard8": 8}
EXPECTED_GROUP_DIGESTS = {
    "rh384_immutable_closure": "a070fef658256fa4744d88faa7bf56f1308979e8ee20393c2fd78d84a127c970",
    "rh384_standard8": "82bbab8d99ae27b4629aeab53c8681c2c4e8b8bfa713b728fda3d9b320027aae",
}
EXPECTED_ALL_GIT_SOURCE_DIGEST = "6247477a1744ccfe676ebd1c20b4d659c597ce0749f3d3a9a0b1c8aa2c87069d"
CERTIFICATE_FIXTURE_BYTES = 29_717
CERTIFICATE_FIXTURE_SHA256 = "64761d3a85afdee4682982ad545d20a66d2ed69926764bcc9580e0dc8c5f8710"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")


def digest_bytes(data: bytes) -> str:
    if type(data) is not bytes:
        raise TypeError("digest input must be bytes")
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _validate_sealed_constants() -> None:
    values = {
        "RH-384 result": RH384_RESULT_SHA256,
        "RH-384 source digest": RH384_SOURCE_DIGEST,
        "RH-384 main": RH384_MAIN_SHA256,
        "certificate": CERTIFICATE_FIXTURE_SHA256,
        "all git sources": EXPECTED_ALL_GIT_SOURCE_DIGEST,
        **{f"group {key}": value for key, value in EXPECTED_GROUP_DIGESTS.items()},
    }
    for label, value in values.items():
        if type(value) is not str or not SHA256.fullmatch(value):
            raise ValueError(f"{label} must be a sealed SHA-256")
    if type(CERTIFICATE_FIXTURE_BYTES) is not int or CERTIFICATE_FIXTURE_BYTES <= 0:
        raise ValueError("certificate byte fixture must be a positive exact integer")
    if set(EXPECTED_GROUP_DIGESTS) != set(EXPECTED_GROUP_SIZES):
        raise ValueError("source group digest membership changed")


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
        raise ValueError("source commit must be 40 lowercase hex characters")
    path = Path(relative)
    if type(relative) is not str or path.is_absolute() or ".." in path.parts:
        raise ValueError("unsafe release-blob path")
    completed = subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(f"release blob unavailable: {commit}:{relative}")
    return completed.stdout


def _strict_load_bytes(data: bytes) -> dict[str, object]:
    if type(data) is not bytes:
        raise TypeError("released JSON must be bytes")
    return loads_strict(data.decode("utf-8"))


@lru_cache(maxsize=1)
def released_rh384_result() -> dict[str, object]:
    relative = f"{RH384_DIRECTORY}/results/result.json"
    data = git_blob(RH384_RELEASE, relative)
    if digest_bytes(data) != RH384_RESULT_SHA256:
        raise RuntimeError("released RH-384 result digest changed")
    result = _strict_load_bytes(data)
    if result.get("status") != "RH-384_prime_tail_scale_separation":
        raise RuntimeError("released RH-384 status changed")
    locks = result.get("source_locks")
    if type(locks) is not dict:
        raise RuntimeError("released RH-384 source lock is absent")
    if locks.get("count") != 51 or locks.get("all_source_digest") != RH384_SOURCE_DIGEST:
        raise RuntimeError("released RH-384 closure contract changed")
    return result


@lru_cache(maxsize=1)
def released_rh384_closure() -> tuple[tuple[str, str], ...]:
    locks = released_rh384_result()["source_locks"]
    entries = locks.get("entries")
    if type(entries) is not list or len(entries) != 51:
        raise RuntimeError("released RH-384 closure is not 51 rows")
    rows: list[tuple[str, str]] = []
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise ValueError("released RH-384 source row membership changed")
        workspace_path = entry["path"]
        expected_sha = entry["sha256"]
        _repo_relative(workspace_path)
        if type(expected_sha) is not str or not SHA256.fullmatch(expected_sha):
            raise ValueError("released RH-384 source digest is malformed")
        rows.append((workspace_path, expected_sha))
    if len({path for path, _ in rows}) != 51:
        raise RuntimeError("released RH-384 closure contains duplicate paths")
    return tuple(rows)


def source_groups() -> dict[str, tuple[tuple[str, str | None], ...]]:
    standard = tuple(
        (f"prime_dynamics_theory/{RH384_DIRECTORY}/{relative}", None)
        for relative in STANDARD8
    )
    return {
        "rh384_immutable_closure": released_rh384_closure(),
        "rh384_standard8": standard,
    }


def source_digest_lines(entries: list[dict[str, object]]) -> tuple[str, ...]:
    lines: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise ValueError("source row membership changed")
        group, commit, path, source_sha = (
            entry["group"], entry["commit"], entry["path"], entry["sha256"]
        )
        if not all(type(item) is str for item in (group, commit, path, source_sha)):
            raise TypeError("source row types changed")
        _repo_relative(path)
        if path in seen:
            raise ValueError("source paths contain duplicates")
        seen.add(path)
        if not COMMIT.fullmatch(commit) or not SHA256.fullmatch(source_sha):
            raise ValueError("source identifier format failed")
        lines.append(f"{group}\t{commit}\t{path}\t{source_sha}")
    return tuple(lines)


def lines_digest(lines: tuple[str, ...] | list[str]) -> str:
    if type(lines) not in (tuple, list) or any(type(line) is not str for line in lines):
        raise TypeError("digest lines must be an exact tuple/list of text")
    return digest_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def build_git_source_locks(
    *,
    commits: dict[str, str] | None = None,
    groups: dict[str, tuple[tuple[str, str | None], ...]] | None = None,
) -> dict[str, object]:
    _validate_sealed_constants()
    selected_commits = dict(SOURCE_COMMITS if commits is None else commits)
    selected_groups = source_groups() if groups is None else groups
    if selected_commits != SOURCE_COMMITS:
        raise ValueError("source commits were rebound")
    if set(selected_groups) != set(EXPECTED_GROUP_SIZES):
        raise ValueError("source group membership changed")
    entries: list[dict[str, object]] = []
    group_sizes: dict[str, int] = {}
    group_digests: dict[str, str] = {}
    declared_pass = True
    live_pass = True
    for group, expected_size in EXPECTED_GROUP_SIZES.items():
        rows = selected_groups[group]
        if type(rows) is not tuple or len(rows) != expected_size:
            raise ValueError("source group size changed")
        commit = selected_commits[group]
        group_entries: list[dict[str, object]] = []
        for workspace_path, declared_sha in rows:
            relative = _repo_relative(workspace_path)
            blob_sha = digest_bytes(git_blob(commit, relative))
            if declared_sha is not None and blob_sha != declared_sha:
                declared_pass = False
            live_path = WORKSPACE / workspace_path
            if not live_path.is_file() or digest(live_path) != blob_sha:
                live_pass = False
            entry = {"group": group, "commit": commit, "path": workspace_path, "sha256": blob_sha}
            entries.append(entry)
            group_entries.append(entry)
        group_sizes[group] = len(group_entries)
        group_digests[group] = lines_digest(source_digest_lines(group_entries))
    if len(entries) != 59 or len({entry["path"] for entry in entries}) != 59:
        raise RuntimeError("Git source closure is not 59 unique rows")
    all_digest = lines_digest(source_digest_lines(entries))
    digest_pass = group_digests == EXPECTED_GROUP_DIGESTS and all_digest == EXPECTED_ALL_GIT_SOURCE_DIGEST
    return {
        "status": "RH-386_immutable_git_source_lock",
        "count": 59,
        "group_sizes": group_sizes,
        "group_digests": group_digests,
        "all_git_source_digest": all_digest,
        "entries": entries,
        "release_blob_identity_pass": declared_pass,
        "live_file_identity_pass": live_pass,
        "declared_hash_identity_pass": declared_pass,
        "digest_contract_pass": digest_pass,
        "mutable_root_files_excluded": True,
        "pass": declared_pass and live_pass and digest_pass,
    }


def build_remote_source_lock(certificate: dict[str, object]) -> dict[str, object]:
    file_lock = loads_strict((ROOT / "results" / "external_source_lock.json").read_text())
    expected = certificate["remote_source_lock"]
    exact_pass = exact_equal(file_lock, expected)
    if not exact_pass:
        raise RuntimeError("external source-lock file differs from the certificate")
    lock_sha = payload_sha256(file_lock)
    return {
        "count": 1,
        "objects": [file_lock],
        "lock_object_sha256": lock_sha,
        "network_fetch_performed": False,
        "redistributable_in_release": False,
        "pass": exact_pass and file_lock["redistributable_in_release"] is False and file_lock["pdf_vendored"] is False,
    }


def predecessor_checks(certificate: dict[str, object]) -> dict[str, object]:
    released = released_rh384_result()
    prior = released["certificate"]["partitions"]
    current = certificate["partitions"]
    prior_projection = [
        [row["partition"], row["degree"], row["length"], row["constant"], row["p_exponent"]]
        for row in prior
    ]
    current_projection = [
        [row["partition"], row["degree_d"], row["length"], row["leading_constant"], row["p_exponent"]]
        for row in current
    ]
    checks = {
        "rh384_status": released["status"] == "RH-384_prime_tail_scale_separation",
        "rh384_partition_regression_66": exact_equal(prior_projection, current_projection),
        "rh384_regression_label_reproduction_only": all(
            row["rh384_regression_role"] == "reproduction_only" for row in current
        ),
        "rh384_main_hash": digest_bytes(git_blob(RH384_RELEASE, f"{RH384_DIRECTORY}/main.tex")) == RH384_MAIN_SHA256,
        "new_source_is_johnston_yang_not_rh384_pnt": certificate["source_theorem"]["locator"]
        == "Johnston--Yang Theorem 1.4 equation (1.8)",
    }
    return {"checks": checks, "all_pass": all(value is True for value in checks.values())}


GATES = {
    "A_intrinsic_determinant": False,
    "B_scattering_completion": False,
    "C_self_adjoint_generator": False,
    "D_von_mangoldt_weighted_prime_power_traces": False,
    "E_completed_zeta_divisor_equality": False,
}

FORBIDDEN_CLAIMS = {
    "growing_clock": False,
    "active_phasewise_c11": False,
    "adaptive_capacity_limit": False,
    "effective_threshold": False,
    "operator_or_trace": False,
    "riemann_zero_identification": False,
    "proof_of_RH": False,
    "finite_fit_as_VK_proof": False,
    "vendored_nonredistributable_source_pdf": False,
}


def build_payload() -> dict[str, object]:
    _validate_sealed_constants()
    certificate = verify_certificate()
    certificate_bytes = len(canonical_json_bytes(certificate))
    certificate_sha = payload_sha256(certificate)
    fixture_pass = certificate_bytes == CERTIFICATE_FIXTURE_BYTES and certificate_sha == CERTIFICATE_FIXTURE_SHA256
    if not fixture_pass:
        raise RuntimeError("certificate fixture changed")
    mutations = mutation_results()
    auxiliary_attacks = auxiliary_attack_results()
    git_locks = build_git_source_locks()
    remote_lock = build_remote_source_lock(certificate)
    predecessors = predecessor_checks(certificate)
    logical_digest = digest_bytes(
        (git_locks["all_git_source_digest"] + "\n" + remote_lock["lock_object_sha256"] + "\n").encode("utf-8")
    )
    all_pass = all((
        certificate["all_pass"] is True,
        fixture_pass,
        len(mutations) == 24 and all(row["rejected"] is True for row in mutations),
        len(auxiliary_attacks) == 7 and all(row["rejected"] is True for row in auxiliary_attacks),
        git_locks["pass"] is True,
        remote_lock["pass"] is True,
        predecessors["all_pass"] is True,
        not any(GATES.values()),
        not any(FORBIDDEN_CLAIMS.values()),
    ))
    return {
        "status": "RH-386_VK_growing_order_prime_tail_uniformization_certified",
        "paper": "RH-386",
        "title": "Vinogradov--Korobov Growing-Order Prime-Tail Uniformization",
        "certificate_fixture": {
            "canonical_bytes": certificate_bytes,
            "sha256": certificate_sha,
            "pass": fixture_pass,
        },
        "certificate": certificate,
        "mutations": {
            "count": len(mutations),
            "rejected": sum(row["rejected"] is True for row in mutations),
            "rows": mutations,
            "verification_mode": "field-level semantic verification; strict JSON attacks use the strict loader",
        },
        "auxiliary_attacks": {
            "count": len(auxiliary_attacks),
            "rejected": sum(row["rejected"] is True for row in auxiliary_attacks),
            "rows": auxiliary_attacks,
            "scope": "source metadata exact types plus duplicate/nonfinite strict JSON",
        },
        "source_locks": {
            "git": git_locks,
            "remote": remote_lock,
            "git_count": 59,
            "remote_count": 1,
            "logical_count": 60,
            "logical_source_digest": logical_digest,
            "pass": git_locks["pass"] is True and remote_lock["pass"] is True,
        },
        "predecessor_checks": predecessors,
        "theorem": {
            "variables": "x=p_y, L=log(x), V=L^(3/5)*(log L)^(-1/5), eta=0.027*L^1.801*exp(-0.1853*V)",
            "single_r": "abs(log(P_r/J_r))<=14r*eta when 7r*eta<=1/2",
            "power_kernel": "0<=log(J_r/I_2r)<=r/(x^2-1); hence <=4r/x^2 under the declared coarse condition",
            "leading_kernel": "abs(log(I_2r/K_r))<=1/((2r-1)L)",
            "partition_exact": "abs(log(P_lambda/J_lambda))<=14d*eta",
            "partition_power": "add d/(x^2-1)",
            "partition_leading": "add H/L",
            "refined": "abs(log(P_lambda/M_lambda)+H/L)<=14d*eta+d/(x^2-1)+2H2/L^2",
            "conditions": "d*eta+d/x^2->0; leading formula additionally requires H/L->0",
            "sufficient": "log d=o(V), H=o(L)",
            "single_r_uniform": "log R=o(V), or R<=exp((0.1853-delta)V) for fixed delta in (0,0.1853)",
            "sharpness": "lambda=1^k and k/L->c gives P_lambda/M_lambda->exp(-c)",
        },
        "claim_boundary": certificate["claim_boundary"],
        "gates": GATES,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "declarations": {
            "data_code_availability": "analytic proof, exact artifact, tests, schemas, and source-lock records included; remote PDF not redistributed",
            "author_contributions": "single author responsible for all applicable roles",
            "funding": "none",
            "competing_interests": "none",
            "ethics": "not applicable",
            "ai_assistance": "AI-assisted proof and artifact auditing disclosed; author retains responsibility",
        },
        "all_pass": all_pass,
    }


def serialized_payload(payload: dict[str, object]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> None:
    payload = build_payload()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(serialized_payload(payload))
    print(json.dumps({
        "status": payload["status"],
        "oracle_rows": payload["certificate"]["counts"]["oracle_rows_total"],
        "mutations_rejected": payload["mutations"]["rejected"],
        "git_sources": payload["source_locks"]["git_count"],
        "remote_sources": payload["source_locks"]["remote_count"],
        "all_pass": payload["all_pass"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
