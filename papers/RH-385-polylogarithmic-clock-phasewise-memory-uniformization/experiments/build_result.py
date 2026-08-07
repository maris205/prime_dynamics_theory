"""Build the exact RH-385 finite reproduction ledger."""

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

from polylog_clock import (  # noqa: E402
    CERTIFICATE_FIXTURE_SHA256,
    MUTATION_NAMES,
    apply_mutation,
    build_certificate,
    payload_sha256,
    verify_certificate,
)


RH384_RELEASE = "386b66a55c9263353c7d407fd712be7e6279f1e6"
RH366_RELEASE = "0396fab97bbe3348c8237f8734dec0e1893fd3bf"
SOURCE_COMMITS = {
    "rh384_immutable_closure": RH384_RELEASE,
    "rh384_standard8": RH384_RELEASE,
    "rh366_davenport_standard8": RH366_RELEASE,
}
RH384_DIRECTORY = "papers/RH-384-prime-tail-scale-separation"
RH366_DIRECTORY = "papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance"
STANDARD8 = (
    "README.md",
    "THEOREM_LEDGER.md",
    "UPDATED_ROADMAP.md",
    "main.tex",
    "references.bib",
    "results/result.json",
    "results/result.schema.json",
    "src/{package}/core.py",
)
EXPECTED_GROUP_SIZES = {
    "rh384_immutable_closure": 51,
    "rh384_standard8": 8,
    "rh366_davenport_standard8": 8,
}
EXPECTED_GROUP_DIGESTS = {
    "rh384_immutable_closure": "a070fef658256fa4744d88faa7bf56f1308979e8ee20393c2fd78d84a127c970",
    "rh384_standard8": "82bbab8d99ae27b4629aeab53c8681c2c4e8b8bfa713b728fda3d9b320027aae",
    "rh366_davenport_standard8": "9ecb03f818a94fa9fc25fb2a21e477fc662f85ab011a0c2fb0c660d182395f5c",
}
EXPECTED_ALL_SOURCE_DIGEST = "14a401e81d5d1868a8b3148478ca26f8975d0bde08b0a0117d4808571a2c5d79"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")


def _validate_sealed_digest_constants() -> None:
    if type(EXPECTED_GROUP_DIGESTS) is not dict or set(EXPECTED_GROUP_DIGESTS) != set(EXPECTED_GROUP_SIZES):
        raise ValueError("sealed source group digest membership failed")
    values = {
        "certificate fixture": CERTIFICATE_FIXTURE_SHA256,
        "all-source digest": EXPECTED_ALL_SOURCE_DIGEST,
        **{f"source group {group}": value for group, value in EXPECTED_GROUP_DIGESTS.items()},
    }
    for label, value in values.items():
        if type(value) is not str or not SHA256.fullmatch(value):
            raise ValueError(f"{label} must be a sealed 64-hex SHA-256")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def _strict_load(path: Path) -> dict[str, object]:
    value = json.loads(
        path.read_text(),
        object_pairs_hook=_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if type(value) is not dict:
        raise ValueError(f"JSON root is not an object: {path}")
    return value


def _strict_load_bytes(data: bytes) -> dict[str, object]:
    value = json.loads(
        data,
        object_pairs_hook=_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if type(value) is not dict:
        raise ValueError("released JSON root is not an object")
    return value


def _repo_relative(workspace_path: str) -> str:
    prefix = "prime_dynamics_theory/"
    if type(workspace_path) is not str or not workspace_path.startswith(prefix):
        raise ValueError(f"source path lacks repository prefix: {workspace_path!r}")
    relative = workspace_path[len(prefix) :]
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or relative in ("AGENTS.md", "RH_HANDOFF.md"):
        raise ValueError(f"unsafe or mutable source path: {workspace_path}")
    return relative


@lru_cache(maxsize=None)
def git_blob(commit: str, repo_relative: str) -> bytes:
    if type(commit) is not str or not COMMIT.fullmatch(commit):
        raise ValueError("invalid source commit")
    path = Path(repo_relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("unsafe release-blob path")
    completed = subprocess.run(
        ["git", "show", f"{commit}:{repo_relative}"],
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"release blob unavailable: {commit}:{repo_relative}: "
            f"{completed.stderr.decode(errors='replace').strip()}"
        )
    return completed.stdout


@lru_cache(maxsize=1)
def _released_rh384_closure() -> tuple[tuple[str, str], ...]:
    released = _strict_load_bytes(git_blob(
        RH384_RELEASE, f"{RH384_DIRECTORY}/results/result.json"
    ))
    locks = released.get("source_locks")
    if type(locks) is not dict or type(locks.get("entries")) is not list:
        raise RuntimeError("released RH-384 source closure is absent")
    entries = locks["entries"]
    if len(entries) != 51:
        raise RuntimeError("released RH-384 source closure does not contain 51 entries")
    output: list[tuple[str, str]] = []
    for entry in entries:
        if type(entry) is not dict:
            raise TypeError("released RH-384 lock row is not an object")
        path = entry.get("path")
        expected = entry.get("sha256")
        _repo_relative(path)
        if type(expected) is not str or not SHA256.fullmatch(expected):
            raise ValueError("released RH-384 lock has an invalid digest")
        output.append((path, expected))
    if len({path for path, _ in output}) != 51:
        raise RuntimeError("released RH-384 source closure has duplicate paths")
    return tuple(output)


def _standard_paths(directory: str, package: str) -> tuple[str, ...]:
    return tuple(
        f"prime_dynamics_theory/{directory}/{relative.format(package=package)}"
        for relative in STANDARD8
    )


def source_groups() -> dict[str, tuple[tuple[str, str | None], ...]]:
    return {
        "rh384_immutable_closure": _released_rh384_closure(),
        "rh384_standard8": tuple(
            (path, None) for path in _standard_paths(RH384_DIRECTORY, "prime_tail_scales")
        ),
        "rh366_davenport_standard8": tuple(
            (path, None) for path in _standard_paths(RH366_DIRECTORY, "mobius_henon_dichotomy")
        ),
    }


def source_digest_lines(entries: list[dict[str, object]]) -> tuple[str, ...]:
    seen: set[str] = set()
    lines: list[str] = []
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise ValueError("source-lock row membership failed")
        group, commit, path, sha = (
            entry["group"], entry["commit"], entry["path"], entry["sha256"]
        )
        if not all(type(value) is str for value in (group, commit, path, sha)):
            raise TypeError("source-lock row types failed")
        _repo_relative(path)
        if path in seen:
            raise ValueError("source-lock paths contain duplicates")
        seen.add(path)
        if not COMMIT.fullmatch(commit) or not SHA256.fullmatch(sha):
            raise ValueError("source-lock identifier format failed")
        lines.append(f"{group}\t{commit}\t{path}\t{sha}")
    return tuple(lines)


def lines_digest(lines: tuple[str, ...] | list[str]) -> str:
    return digest_bytes(("\n".join(lines) + "\n").encode())


def build_source_locks(
    *,
    commits: dict[str, str] | None = None,
    groups: dict[str, tuple[tuple[str, str | None], ...]] | None = None,
) -> dict[str, object]:
    _validate_sealed_digest_constants()
    selected_commits = dict(SOURCE_COMMITS if commits is None else commits)
    selected_groups = source_groups() if groups is None else groups
    if selected_commits != SOURCE_COMMITS:
        raise ValueError("source commits were rebound")
    if set(selected_groups) != set(EXPECTED_GROUP_SIZES):
        raise ValueError("source groups were rebound")
    entries: list[dict[str, object]] = []
    group_digests: dict[str, str] = {}
    release_pass = True
    live_pass = True
    declared_pass = True
    group_sizes: dict[str, int] = {}
    for group, expected_size in EXPECTED_GROUP_SIZES.items():
        rows = selected_groups[group]
        if type(rows) is not tuple or len(rows) != expected_size:
            raise ValueError("source group membership was rebound")
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
            entry = {
                "group": group,
                "commit": commit,
                "path": workspace_path,
                "sha256": blob_sha,
            }
            entries.append(entry)
            group_entries.append(entry)
        group_sizes[group] = len(group_entries)
        group_digests[group] = lines_digest(source_digest_lines(group_entries))
    if len(entries) != 67 or len({entry["path"] for entry in entries}) != 67:
        raise RuntimeError("source lock is not 67 unique files")
    all_digest = lines_digest(source_digest_lines(entries))
    digest_contract_pass = (
        group_digests == EXPECTED_GROUP_DIGESTS
        and all_digest == EXPECTED_ALL_SOURCE_DIGEST
    )
    release_pass = release_pass and declared_pass
    return {
        "status": "RH-385_immutable_source_lock",
        "count": len(entries),
        "group_sizes": group_sizes,
        "group_digests": group_digests,
        "all_source_digest": all_digest,
        "entries": entries,
        "release_blob_identity_pass": release_pass,
        "live_file_identity_pass": live_pass,
        "declared_hash_identity_pass": declared_pass,
        "digest_contract_pass": digest_contract_pass,
        "mutable_root_files_excluded": True,
    }


def _outer_replay() -> dict[str, object]:
    verification_path = (
        WORKSPACE
        / "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json"
    )
    summary_path = (
        WORKSPACE
        / "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/summary.json"
    )
    verification = _strict_load(verification_path)
    summary = _strict_load(summary_path)
    expected = {
        "volume_count": 4,
        "archive_member_count": 73,
        "dependency_hash_count": 1548,
        "result_hash_count": 8,
        "numbered_source_count": 361,
        "failure_count": 0,
    }
    observed = {key: verification.get(key) for key in expected}
    return {
        **observed,
        "expected": expected,
        "gates_false": type(summary.get("gates")) is dict and not any(summary["gates"].values()),
        "forbidden_claims_false": type(summary.get("forbidden_claims")) is dict
        and not any(summary["forbidden_claims"].values()),
        "pass": observed == expected,
    }


def _mutation_results(certificate: dict[str, object]) -> list[dict[str, object]]:
    rows = []
    for name in MUTATION_NAMES:
        rejected = False
        error = ""
        try:
            verify_certificate(apply_mutation(certificate, name))
        except (ArithmeticError, KeyError, RuntimeError, TypeError, ValueError) as exc:
            rejected = True
            error = type(exc).__name__
        rows.append({"name": name, "rejected": rejected, "error_class": error})
    return rows


def build_payload() -> dict[str, object]:
    _validate_sealed_digest_constants()
    certificate = build_certificate()
    verify_certificate(certificate)
    certificate_sha = payload_sha256(certificate)
    fixture_pass = certificate_sha == CERTIFICATE_FIXTURE_SHA256
    locks = build_source_locks()
    mutations = _mutation_results(certificate)
    replay = _outer_replay()
    gates = {
        "A_intrinsic_dynamical_spectral_determinant": False,
        "B_time_oriented_scattering_completion": False,
        "C_self_adjoint_generator_with_T_log_T": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    forbidden = {
        "unrestricted_growing_clock": False,
        "polynomial_clock_uniformity": False,
        "B_depends_on_N": False,
        "active_phasewise_c11": False,
        "adaptive_capacity_limit": False,
        "projectively_compatible_infinite_selector": False,
        "effective_finite_threshold": False,
        "intrinsic_operator_or_trace": False,
        "riemann_zeros_identified": False,
        "riemann_hypothesis_proved": False,
    }
    all_pass = all((
        certificate.get("all_pass") is True,
        fixture_pass,
        locks["count"] == 67,
        locks["release_blob_identity_pass"] is True,
        locks["live_file_identity_pass"] is True,
        locks["declared_hash_identity_pass"] is True,
        locks["digest_contract_pass"] is True,
        len(mutations) == 24 and all(row["rejected"] for row in mutations),
        replay["pass"] is True,
        replay["gates_false"] is True,
        replay["forbidden_claims_false"] is True,
        not any(gates.values()),
        not any(forbidden.values()),
    ))
    return {
        "status": "RH-385_polylogarithmic_clock_uniformization_certified",
        "theorem_contract": {
            "fixed_parameter": "B>0",
            "clock_budget": "H_B(N)=floor((log N)^B)",
            "class": "RH-379 universally safe q-periodic lag-two families with c11(r)=0 at every phase",
            "zero_padding": "mu_0(m)=mu(m) for m>=1 and 0 for m<=0",
            "finite_score": "S_N(q,f)=N^-1 sum_(n<=N) mu(n) f_(n mod q)(mu_0(n-2),mu(n))",
            "fixed_clock_limit": "L_q(f)=sum_(r mod q)[c02(r)delta_(q,r)+c22(r)theta_(q,r)]",
            "uniform_limit": "sup_(1<=q<=H_B(N),f in F_q)|S_N(q,f)-L_q(f)|->0",
            "ledger": "4sqrt(Q)D_*(N)/N+13tau_P+6Q/N+4/N",
            "cutoff": "P=floor(sqrt(log log N)), eventually P>=2",
            "common_period": "Q=lcm(q,M_P), M_P=(product_(p<=P)p)^2; neither asserted minimal",
            "davenport": "D_*(N)/N <<_A (log N)^(-A), choose fixed A>B/2",
            "optimizer_limits": [
                "sup_(q<=H_B(N))|G_N(q)-G(q)|->0",
                "max_(q<=H_B(N))G_N(q)->B_infinity",
            ],
            "diagonal": "after nonempty, y_B(N)=max{y:q_y<=H_B(N)} and the positive q_y optimizer tends to B_infinity",
        },
        "source_locks": locks,
        "certificate_sha256": certificate_sha,
        "certificate_canonical_bytes": len(canonical_bytes(certificate)),
        "certificate_fixture_pass": fixture_pass,
        "certificate": certificate,
        "mutations": mutations,
        "outer_four_volume_replay": replay,
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "first_route_b_blocker": "fixed logarithmic Davenport savings do not pay polynomial Fourier mass; active c11 meets shift-two Chowla at q=1",
            "finite_artifact_role": "reproduction_not_analytic_proof",
        },
        "gates": gates,
        "forbidden_claims": forbidden,
        "declarations": {
            "new_external_dataset": False,
            "human_or_animal_subjects": False,
            "conflict_of_interest": False,
            "specific_funding": False,
            "ai_assisted_workflow_disclosed": True,
        },
        "all_pass": all_pass,
    }


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def serialized_payload(payload: dict[str, object]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> None:
    payload = build_payload()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(serialized_payload(payload))
    print(json.dumps({
        "status": payload["status"],
        "all_pass": payload["all_pass"],
        "source_count": payload["source_locks"]["count"],
        "certificate_sha256": payload["certificate_sha256"],
        "certificate_canonical_bytes": payload["certificate_canonical_bytes"],
        "mutation_count": len(payload["mutations"]),
    }, sort_keys=True))
    if payload["all_pass"] is not True:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
