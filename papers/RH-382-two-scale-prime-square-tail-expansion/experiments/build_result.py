"""Build the immutable-source-locked RH-382 result ledger."""

from __future__ import annotations

import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path

from two_scale_tail import (
    CERTIFICATE_FIXTURE_BYTES,
    CERTIFICATE_FIXTURE_SHA256,
    canonical_json_bytes,
    payload_sha256,
    verify_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_COMMITS = {
    "rh374_release": "2bb3baa6a09491c2d679d10c0dbcd39587d1f831",
    "rh379_release": "9ae9802ed17529ef4adfb81d7e2158d47c3c8d22",
    "rh380_release": "dd94b9cfebdbf5df92084ba870b10d3a4d432bee",
    "rh381_release": "b6a6355b3390f3d00091a02cf77845b4f68a4a22",
    "rh_mvp2_archive": "c0aed13a34b8bbc53061aed23738660adcd3624c",
}

SOURCE_GROUPS = {
    "rh374_release": (
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/README.md",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/THEOREM_LEDGER.md",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/UPDATED_ROADMAP.md",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/main.tex",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/references.bib",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/results/result.json",
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/src/square_clock/core.py",
    ),
    "rh379_release": (
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/README.md",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/THEOREM_LEDGER.md",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/UPDATED_ROADMAP.md",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/main.tex",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/references.bib",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/results/result.json",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/results/result.schema.json",
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/src/phasewise_memory/core.py",
    ),
    "rh380_release": (
        "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/README.md",
        "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/THEOREM_LEDGER.md",
        "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/UPDATED_ROADMAP.md",
        "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/main.tex",
        "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/references.bib",
        "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/results/result.json",
        "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/results/result.schema.json",
        "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/src/finite_clock_gap/core.py",
    ),
    "rh381_release": (
        "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/README.md",
        "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/THEOREM_LEDGER.md",
        "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/UPDATED_ROADMAP.md",
        "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/main.tex",
        "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/references.bib",
        "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/results/result.json",
        "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/results/result.schema.json",
        "prime_dynamics_theory/papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/src/prime_square_tail/core.py",
    ),
    "rh_mvp2_archive": (
        "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/summary.json",
        "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
    ),
}

EXPECTED_GROUP_DIGESTS = {
    "rh374_release": "1110169db1afe2bcb1242cd8284665be9681f955ff942b23908a9401635695ff",
    "rh379_release": "c029ccbe0b499a38f675292c2260cfde5d4b7aede6c6ddee9f87d2c816ecd848",
    "rh380_release": "3c488551cf9b8bdf6a4509b1f39af2119ea6b2ac401bda3cb63f87df38a0e751",
    "rh381_release": "5d07b1b897aa36127f2f190517229534719f37ce0f3ff904d1c31adebae6c9df",
    "rh_mvp2_archive": "c22c0a9e4702c3bc615acfc19e564cbfd7d08a3bc845b28c659511065c05989b",
}
EXPECTED_ALL_SOURCE_DIGEST = "7b62b7e77ad313a52a07851e700aff197c2cc4bc3d910c6a464cd3cec0b55cb6"
SOURCE_FILES = tuple(path for paths in SOURCE_GROUPS.values() for path in paths)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def _reject_nonfinite_constant(token: str) -> object:
    raise ValueError(f"non-finite JSON constant: {token}")


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(
        path.read_text(),
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_nonfinite_constant,
    )
    if type(value) is not dict:
        raise ValueError(f"JSON root is not an object: {path}")
    return value


def _safe_source_path(relative: str) -> None:
    prefix = "prime_dynamics_theory/"
    path = Path(relative)
    if type(relative) is not str or not relative.startswith(prefix) or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe or nonrepository source path: {relative}")
    if relative in ("prime_dynamics_theory/AGENTS.md", "prime_dynamics_theory/RH_HANDOFF.md"):
        raise ValueError("mutable policy and handoff files cannot be source locked")


def _release_blob(relative: str, release: str) -> bytes:
    _safe_source_path(relative)
    repository_relative = relative.removeprefix("prime_dynamics_theory/")
    completed = subprocess.run(
        ["git", "-C", str(REPOSITORY), "show", f"{release}:{repository_relative}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def source_digest_lines(entries: list[dict[str, str]]) -> tuple[str, ...]:
    lines: list[str] = []
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise ValueError("source digest row has invalid membership")
        group, commit, path, sha = entry["group"], entry["commit"], entry["path"], entry["sha256"]
        _safe_source_path(path)
        if group not in SOURCE_COMMITS or commit != SOURCE_COMMITS[group]:
            raise ValueError("source digest row has a group/commit mismatch")
        if type(sha) is not str or len(sha) != 64 or any(character not in "0123456789abcdef" for character in sha):
            raise ValueError("source digest row has an invalid SHA-256")
        lines.append(f"{group}|{commit}|{path}|{sha}")
    if len(lines) != len(set(lines)):
        raise ValueError("source digest rows contain duplicates")
    return tuple(sorted(lines))


def lines_digest(lines: tuple[str, ...] | list[str]) -> str:
    serialized = "\n".join(sorted(lines)) + "\n"
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def validate_source_contract(source_commits: dict[str, str], source_groups: dict[str, tuple[str, ...]]) -> None:
    if source_commits != SOURCE_COMMITS:
        raise ValueError("RH-382 source commits were rebound")
    if source_groups != SOURCE_GROUPS:
        raise ValueError("RH-382 source membership was rebound")
    if len(SOURCE_FILES) != 33 or len(set(SOURCE_FILES)) != 33:
        raise ValueError("RH-382 source membership is not the frozen 33-file set")
    for path in SOURCE_FILES:
        _safe_source_path(path)


def build_source_locks(
    source_commits: dict[str, str] | None = None,
    source_groups: dict[str, tuple[str, ...]] | None = None,
) -> dict[str, object]:
    commits = SOURCE_COMMITS if source_commits is None else source_commits
    groups = SOURCE_GROUPS if source_groups is None else source_groups
    validate_source_contract(commits, groups)
    entries: list[dict[str, str]] = []
    release_blob_identity_pass = True
    for group, files in groups.items():
        commit = commits[group]
        for relative in files:
            live_sha = digest(WORKSPACE / relative)
            blob_sha = hashlib.sha256(_release_blob(relative, commit)).hexdigest()
            release_blob_identity_pass = release_blob_identity_pass and live_sha == blob_sha
            entries.append({"group": group, "commit": commit, "path": relative, "sha256": live_sha})
    lines = source_digest_lines(entries)
    group_digests = {
        group: lines_digest(tuple(line for line in lines if line.startswith(f"{group}|")))
        for group in SOURCE_GROUPS
    }
    all_digest = lines_digest(lines)
    digest_pass = group_digests == EXPECTED_GROUP_DIGESTS and all_digest == EXPECTED_ALL_SOURCE_DIGEST
    if not release_blob_identity_pass:
        raise RuntimeError("a live predecessor input differs from its declared release blob")
    if not digest_pass:
        raise RuntimeError("the frozen 33-source digest contract failed")
    return {
        "count": len(entries),
        "entries": entries,
        "group_digests": group_digests,
        "all_source_digest": all_digest,
        "release_blob_identity_pass": release_blob_identity_pass,
        "digest_contract_pass": digest_pass,
        "mutable_root_files_excluded": True,
        "pass": release_blob_identity_pass and digest_pass,
    }


def predecessor_checks() -> dict[str, object]:
    rh374 = load_json(WORKSPACE / SOURCE_GROUPS["rh374_release"][5])
    rh379 = load_json(WORKSPACE / SOURCE_GROUPS["rh379_release"][5])
    rh380 = load_json(WORKSPACE / SOURCE_GROUPS["rh380_release"][5])
    rh381 = load_json(WORKSPACE / SOURCE_GROUPS["rh381_release"][5])
    mvp2 = load_json(WORKSPACE / SOURCE_GROUPS["rh_mvp2_archive"][0])
    checks = {
        "rh374_status_pass": rh374.get("status") == "RH-374_square_clock_euler_product_capacity_floor",
        "rh379_status_pass": rh379.get("status") == "RH-379_phasewise_chowla_free_memory_supremum",
        "rh380_status_pass": rh380.get("status") == "RH-380_square_clock_monotonicity_and_finite_clock_nonattainment",
        "rh381_status_pass": rh381.get("status") == "RH-381_prime_square_tail_rate_and_quadratic_memory_remainder",
        "rh381_increment_sum_scope_pass": "fixed finite q" in str(rh381.get("theorem", {}).get("factor_class", "")),
        "rh381_tail_identity_pass": "T_y^2+sum" in str(rh381.get("theorem", {}).get("tail_identities", "")),
        "mvp2_gates_pass": mvp2.get("gates") == {"A": False, "B": False, "C": False, "D": False, "E": False},
    }
    return {**checks, "all_pass": all(checks.values())}


@lru_cache(maxsize=1)
def build_payload() -> dict[str, object]:
    source_locks = build_source_locks()
    predecessor = predecessor_checks()
    certificate = verify_certificate()
    if len(canonical_json_bytes(certificate)) != CERTIFICATE_FIXTURE_BYTES:
        raise RuntimeError("RH-382 certificate byte count differs from the frozen fixture")
    if payload_sha256(certificate) != CERTIFICATE_FIXTURE_SHA256:
        raise RuntimeError("RH-382 certificate digest differs from the frozen fixture")
    if not predecessor["all_pass"] or not certificate["all_pass"]:
        raise RuntimeError("RH-382 predecessor or exact certificate failed")
    return {
        "status": "RH-382_two_scale_prime_square_tail_expansion",
        "source_commits": SOURCE_COMMITS,
        "source_locks": source_locks,
        "predecessor_checks": predecessor,
        "certificate": certificate,
        "certificate_fixture": {
            "bytes": CERTIFICATE_FIXTURE_BYTES,
            "sha256": CERTIFICATE_FIXTURE_SHA256,
            "matches": True,
        },
        "theorem": {
            "factor_class": "fixed finite q before N tends to infinity; universally safe phasewise lag-two tables with c11(r)=0 at every phase",
            "tails": "T_y=sum_(j>=y)a_(j+1), S_y=sum_(j>=y)a_(j+1)^2, a_(j+1)=1/(p_(j+1)^2-1)",
            "coefficients": "X_infinity=2u4-4u5+6u6-8u7+10u8; Y_infinity=6u4-16u5+30u6-48u7+70u8; m_infinity=2u3-4u4+6u5-8u6+10u7-12u8",
            "two_scale_expansion": "B_infinity-G(q_y)=2X_infinity*T_y/pi^2+(Y_infinity+2m_infinity)*T_y^2/pi^2+(Y_infinity-2m_infinity)*S_y/pi^2+R_y",
            "remainder": "abs(R_y)<=3301*T_y^3/(6*pi^2)<551*T_y^3/pi^2 for every y>=1",
            "terminal": "R8=P_y*E8 is separate; E9=0 from p=3; E10 is not used or constructed",
            "prime_distribution_input": "no prime number theorem and no p_y-scale rewrite is used",
        },
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "first_unresolved_object": "an exact all-order cluster normal form or phase-weighted shift-two cancellation",
            "notes": [
                "The N-limit is taken at fixed finite q before the cofinal square-clock index tends to infinity.",
                "The theorem is restricted to universally safe phasewise tables with c11(r)=0 at every phase.",
                "The S_y scale is retained with opposite memory signs and is not collapsed into T_y^2.",
                "The p=71 wrong-sign row is exact Fraction reproduction only, not evidence for the all-y theorem.",
                "No PNT, p_y rewrite, q=q(N), active-c11 theorem, or adaptive-capacity convergence is claimed.",
                "No operator, determinant, prime-power trace, zero identification, Hilbert--Polya construction, RH implication, or Gate promotion is claimed.",
            ],
        },
        "gates": {
            "A_canonical_intrinsic_dynamical_spectral_determinant": False,
            "B_time_oriented_scattering_or_unitary_completion": False,
            "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
            "D_von_mangoldt_weighted_prime_power_traces": False,
            "E_completed_zeta_divisor_equality": False,
        },
    }


def serialized_payload(payload: dict[str, object]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> None:
    payload = build_payload()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(serialized_payload(payload))
    print(json.dumps({
        "status": payload["status"],
        "source_lock_count": payload["source_locks"]["count"],
        "source_digest": payload["source_locks"]["all_source_digest"],
        "certificate_sha256": payload["certificate_fixture"]["sha256"],
        "all_pass": payload["certificate"]["all_pass"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
