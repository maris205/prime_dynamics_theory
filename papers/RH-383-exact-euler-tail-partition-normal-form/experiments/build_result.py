"""Build the immutable-source-locked RH-383 result ledger."""

from __future__ import annotations

import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path

from euler_tail_normal_form import (
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
    "rh382_release": "32afe96176ac00f4f261cf7097e0342a5c5194f1",
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
    "rh382_release": (
        "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/README.md",
        "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/THEOREM_LEDGER.md",
        "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/UPDATED_ROADMAP.md",
        "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/main.tex",
        "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/references.bib",
        "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/results/result.json",
        "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/results/result.schema.json",
        "prime_dynamics_theory/papers/RH-382-two-scale-prime-square-tail-expansion/src/two_scale_tail/core.py",
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
    "rh382_release": "ca26217907f59b219ba2d2b3e4e77ec6e344d036c3a8a92ab5683497d3309f7e",
    "rh_mvp2_archive": "c22c0a9e4702c3bc615acfc19e564cbfd7d08a3bc845b28c659511065c05989b",
}
EXPECTED_ALL_SOURCE_DIGEST = "492100fe3b6b823a39b58cec25b0dcddf6d52c02bd1941f0978611f01a2b8db9"
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
    if type(relative) is not str:
        raise TypeError("source path must be a string")
    path = Path(relative)
    if not relative.startswith(prefix) or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe or nonrepository source path: {relative}")
    if relative in ("prime_dynamics_theory/AGENTS.md", "prime_dynamics_theory/RH_HANDOFF.md"):
        raise ValueError("mutable root policy and handoff files cannot be source locked")


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
    return hashlib.sha256(("\n".join(sorted(lines)) + "\n").encode("utf-8")).hexdigest()


def validate_source_contract(
    source_commits: dict[str, str],
    source_groups: dict[str, tuple[str, ...]],
) -> None:
    if source_commits != SOURCE_COMMITS:
        raise ValueError("RH-383 source commits were rebound")
    if source_groups != SOURCE_GROUPS:
        raise ValueError("RH-383 source membership was rebound")
    if len(SOURCE_FILES) != 41 or len(set(SOURCE_FILES)) != 41:
        raise ValueError("RH-383 source membership is not the frozen 41-file set")
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
    digest_contract_pass = group_digests == EXPECTED_GROUP_DIGESTS and all_digest == EXPECTED_ALL_SOURCE_DIGEST
    if not release_blob_identity_pass:
        raise RuntimeError("a live predecessor input differs from its declared release blob")
    if not digest_contract_pass:
        raise RuntimeError("the frozen 41-source digest contract failed")
    return {
        "count": len(entries),
        "entries": entries,
        "group_digests": group_digests,
        "all_source_digest": all_digest,
        "release_blob_identity_pass": release_blob_identity_pass,
        "digest_contract_pass": digest_contract_pass,
        "mutable_root_files_excluded": True,
        "pass": release_blob_identity_pass and digest_contract_pass,
    }


def predecessor_checks() -> dict[str, object]:
    rows = {
        key: load_json(WORKSPACE / SOURCE_GROUPS[key][5])
        for key in ("rh374_release", "rh379_release", "rh380_release", "rh381_release", "rh382_release")
    }
    mvp2 = load_json(WORKSPACE / SOURCE_GROUPS["rh_mvp2_archive"][0])
    checks = {
        "rh374_status_pass": rows["rh374_release"].get("status") == "RH-374_square_clock_euler_product_capacity_floor",
        "rh379_status_pass": rows["rh379_release"].get("status") == "RH-379_phasewise_chowla_free_memory_supremum",
        "rh380_status_pass": rows["rh380_release"].get("status") == "RH-380_square_clock_monotonicity_and_finite_clock_nonattainment",
        "rh381_status_pass": rows["rh381_release"].get("status") == "RH-381_prime_square_tail_rate_and_quadratic_memory_remainder",
        "rh382_status_pass": rows["rh382_release"].get("status") == "RH-382_two_scale_prime_square_tail_expansion",
        "rh382_two_scale_sign_pass": "Y_infinity-2m_infinity" in str(rows["rh382_release"].get("theorem", {}).get("two_scale_expansion", "")),
        "mvp2_gates_pass": mvp2.get("gates") == {"A": False, "B": False, "C": False, "D": False, "E": False},
    }
    return {**checks, "all_pass": all(checks.values())}


@lru_cache(maxsize=1)
def build_payload() -> dict[str, object]:
    source_locks = build_source_locks()
    predecessor = predecessor_checks()
    certificate = verify_certificate()
    if len(canonical_json_bytes(certificate)) != CERTIFICATE_FIXTURE_BYTES:
        raise RuntimeError("RH-383 certificate byte count differs from the frozen fixture")
    if payload_sha256(certificate) != CERTIFICATE_FIXTURE_SHA256:
        raise RuntimeError("RH-383 certificate digest differs from the frozen fixture")
    if not predecessor["all_pass"] or not certificate["all_pass"]:
        raise RuntimeError("RH-383 predecessor or exact certificate failed")
    return {
        "status": "RH-383_exact_euler_tail_partition_normal_form",
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
            "power_sums": "P_r(y)=sum_(j>=y)a_(j+1)^r; Phi_c(y)=sum_(r>=1)c^r P_r(y)/r; a_(j+1)=1/(p_(j+1)^2-1)",
            "endpoint_ratios": "U_m^(y)=u_m exp(Phi_(m-1)(y)); H_y=(4/pi^2)exp(-Phi_1(y))",
            "endpoint_normal_form": "pi^2(B_infinity-G(q_y))=2(C(u)-C(U^(y)))-4W(U^(y))(1-exp(-Phi_1(y)))",
            "partition_compiler": "gamma_lambda=-(2/z_lambda)sum alpha_m u_m(m-1)^d-(4/z_lambda)sum beta_m u_m((m-1)^d-product_r((m-1)^r-1)^k_r)",
            "m2_cancellation": "the m=2 contribution vanishes exactly for every nonempty partition",
            "cubic_block": "gamma_111, gamma_21 and gamma_3 are frozen exactly in the manuscript and certificate",
            "remainder": "for exact integer D>=1 and rho_y=7T_y<=7/8, abs(R_(D,y))<=92*rho_y^(D+1)/(3*pi^2)<31*rho_y^(D+1)/pi^2",
            "terminal": "R8=P_y*E8 is separate; E9=0 from p=3; E10 is not used or constructed",
            "prime_distribution_input": "no prime number theorem and no p_y-scale rewrite is used",
        },
        "reproduction": {
            "finite_rows_only": True,
            "three_independent_oracles": [
                "endpoint C/W canonical partition compiler",
                "ordered increment Gamma/h/e/Phi compiler with successor tail",
                "A_c/F_c telescope direct-gap compiler",
            ],
            "q_sign_redundancy": "432 c-labeled rows share 72 tail/degree positions and are not 432 separate theorems",
            "low_order_redundancy": "33 endpoint-labeled bundles repeat the same three symbolic coefficient identities and are not 33 separate theorems",
        },
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "first_unresolved_object": "a phase-weighted shift-two correlation theorem for active c11(r), or a new theorem-backed independent route",
            "notes": [
                "The N-limit is taken at fixed finite q before the cofinal square-clock index tends to infinity.",
                "The theorem is restricted to universally safe phasewise tables with c11(r)=0 at every phase.",
                "The partition loss sign is controlled by partition length, not total degree.",
                "The memory increment uses the strict successor tail j+1.",
                "The general 92/3 bound does not inherit RH-381 or RH-382's sharper special-purpose constants.",
                "Finite rows reproduce and attack symbolic identities; they are not fits or asymptotic evidence.",
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
        "forbidden_claims": {
            "hilbert_polya_operator_constructed": False,
            "riemann_zeros_identified": False,
            "von_mangoldt_trace_formula_proved": False,
            "riemann_hypothesis_proved": False,
            "active_c11_controlled": False,
            "adaptive_capacity_limit_proved": False,
            "growing_clock_q_of_N_used": False,
            "prime_number_theorem_used": False,
            "p_y_asymptotic_claimed": False,
            "finite_fit_promoted": False,
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
        "source_count": payload["source_locks"]["count"],
        "source_digest": payload["source_locks"]["all_source_digest"],
        "certificate_bytes": payload["certificate_fixture"]["bytes"],
        "certificate_sha256": payload["certificate_fixture"]["sha256"],
        "all_pass": payload["certificate"]["all_pass"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
