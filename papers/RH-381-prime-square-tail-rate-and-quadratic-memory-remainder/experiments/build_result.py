"""Build the immutable-source-locked RH-381 result ledger."""

from __future__ import annotations

import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path

from prime_square_tail import verify_certificate


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_COMMITS = {
    "rh374_release": "2bb3baa6a09491c2d679d10c0dbcd39587d1f831",
    "rh379_release": "9ae9802ed17529ef4adfb81d7e2158d47c3c8d22",
    "rh380_release": "dd94b9cfebdbf5df92084ba870b10d3a4d432bee",
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
    "rh_mvp2_archive": (
        "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/summary.json",
        "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
    ),
}

EXPECTED_GROUP_DIGESTS = {
    "rh374_release": "1110169db1afe2bcb1242cd8284665be9681f955ff942b23908a9401635695ff",
    "rh379_release": "c029ccbe0b499a38f675292c2260cfde5d4b7aede6c6ddee9f87d2c816ecd848",
    "rh380_release": "3c488551cf9b8bdf6a4509b1f39af2119ea6b2ac401bda3cb63f87df38a0e751",
    "rh_mvp2_archive": "c22c0a9e4702c3bc615acfc19e564cbfd7d08a3bc845b28c659511065c05989b",
}
EXPECTED_ALL_SOURCE_DIGEST = "e4487f2f776cb42e202e9f0c01d4c6d922b0eeedfad7730df194eedb71bed314"
SOURCE_FILES = tuple(path for paths in SOURCE_GROUPS.values() for path in paths)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _safe_source_path(relative: str) -> None:
    prefix = "prime_dynamics_theory/"
    path = Path(relative)
    if not relative.startswith(prefix) or path.is_absolute() or ".." in path.parts:
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
    lines = []
    for entry in entries:
        group = entry["group"]
        commit = entry["commit"]
        path = entry["path"]
        sha = entry["sha256"]
        _safe_source_path(path)
        if group not in SOURCE_COMMITS or commit != SOURCE_COMMITS[group]:
            raise ValueError("source digest line has a group/commit mismatch")
        if len(sha) != 64 or any(character not in "0123456789abcdef" for character in sha):
            raise ValueError("source digest line has an invalid SHA-256")
        lines.append(f"{group}|{commit}|{path}|{sha}")
    return tuple(sorted(lines))


def lines_digest(lines: tuple[str, ...] | list[str]) -> str:
    serialized = "\n".join(sorted(lines)) + "\n"
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def validate_source_contract(
    source_commits: dict[str, str], source_groups: dict[str, tuple[str, ...]]
) -> None:
    if source_commits != SOURCE_COMMITS:
        raise ValueError("RH-381 source commits were rebound")
    if source_groups != SOURCE_GROUPS:
        raise ValueError("RH-381 source membership was rebound")
    if len(SOURCE_FILES) != 25 or len(set(SOURCE_FILES)) != 25:
        raise ValueError("RH-381 source membership is not the frozen 25-file set")
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
            entries.append(
                {
                    "group": group,
                    "commit": commit,
                    "path": relative,
                    "sha256": live_sha,
                }
            )
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
        raise RuntimeError("the frozen 25-source digest contract failed")
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


def _load(relative: str) -> dict[str, object]:
    _safe_source_path(relative)
    value = json.loads((WORKSPACE / relative).read_text())
    if not isinstance(value, dict):
        raise ValueError(f"predecessor JSON root is not an object: {relative}")
    return value


def predecessor_checks() -> dict[str, object]:
    rh374 = _load(
        "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/results/result.json"
    )
    rh379 = _load(
        "prime_dynamics_theory/papers/RH-379-phasewise-chowla-free-memory-supremum/results/result.json"
    )
    rh380 = _load(
        "prime_dynamics_theory/papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/results/result.json"
    )
    mvp2 = _load(
        "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/summary.json"
    )
    increment = rh380.get("theorem", {}).get("increment")
    checks = {
        "rh374_status_pass": rh374.get("status") == "RH-374_square_clock_euler_product_capacity_floor",
        "rh379_status_pass": rh379.get("status") == "RH-379_phasewise_chowla_free_memory_supremum",
        "rh380_status_pass": rh380.get("status") == "RH-380_square_clock_monotonicity_and_finite_clock_nonattainment",
        "rh380_increment_anchor_pass": isinstance(increment, str) and "M_y*(4/pi^2-H_(y+1))" in increment,
        "rh380_fixed_clock_scope_pass": "fixed finite q" in str(rh380.get("theorem", {}).get("factor_class", "")),
        "mvp2_gates_pass": mvp2.get("gates") == {"A": False, "B": False, "C": False, "D": False, "E": False},
    }
    return {**checks, "all_pass": all(checks.values())}


@lru_cache(maxsize=1)
def build_payload() -> dict[str, object]:
    source_locks = build_source_locks()
    predecessor = predecessor_checks()
    certificate = verify_certificate()
    if not predecessor["all_pass"] or not certificate["all_pass"]:
        raise RuntimeError("RH-381 predecessor or exact certificate failed")
    return {
        "status": "RH-381_prime_square_tail_rate_and_quadratic_memory_remainder",
        "source_commits": SOURCE_COMMITS,
        "source_locks": source_locks,
        "predecessor_checks": predecessor,
        "certificate": certificate,
        "theorem": {
            "factor_class": "fixed finite q before N tends to infinity; universally safe phasewise lag-two tables with c11(r)=0 at every phase",
            "tail": "T_y=sum_(j>=y) 1/(p_(j+1)^2-1)",
            "x_limit": "X_infinity=(2e_4-4e_5+6e_6-8e_7+10e_8)/e_1>=6e_8/e_1>0",
            "x_bound": "abs(X_j-X_infinity)<=170*T_j",
            "h_bound": "0<=4/pi^2-H_(j+1)<=(4/pi^2)*T_(j+1)",
            "memory_bound": "0<=M_j/A_j<=1",
            "tail_identities": "sum a_(j+1)T_j=(T_y^2+sum a_(j+1)^2)/2 and sum a_(j+1)T_(j+1)=(T_y^2-sum a_(j+1)^2)/2",
            "rate_bound": "abs(B_infinity-G(q_y)-(2X_infinity/pi^2)T_y)<=342*T_y^2/pi^2",
            "ratio_limit": "(B_infinity-G(q_y))/T_y tends to 2X_infinity/pi^2>0",
            "prime_distribution_input": "no prime number theorem or p_y-scale asymptotic is used",
        },
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "first_unresolved_object": "a two-scale second-order expansion or phase-weighted shift-two cancellation",
            "notes": [
                "The N-limit is taken at fixed finite q before the cofinal square-clock index tends to infinity.",
                "The theorem is restricted to universally safe phasewise tables with c11(r)=0 at every phase.",
                "The 170 and 342 constants are explicit safe bounds and are not claimed optimal.",
                "No exact second-order coefficient, p_y asymptotic, prime-number-theorem substitution, or q=q(N) statement is made.",
                "Finite diagnostics reproduce exact identities and outward enclosures; they are not regression evidence for the theorem.",
                "No adaptive-capacity convergence, intrinsic operator, determinant, trace formula, zero identification, Hilbert--Polya construction, RH implication, or Gate promotion is claimed.",
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


def main() -> None:
    payload = build_payload()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "source_lock_count": payload["source_locks"]["count"],
                "source_digest": payload["source_locks"]["all_source_digest"],
                "canonical_fixture_sha256": payload["certificate"]["canonical_fixture_sha256"],
                "interval_fixture_sha256": payload["certificate"]["interval_fixture_sha256"],
                "all_pass": payload["certificate"]["all_pass"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
