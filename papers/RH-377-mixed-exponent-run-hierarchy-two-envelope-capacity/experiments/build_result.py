"""Build the source-locked RH-377 result ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from mixed_run_hierarchy import verify_certificate


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_FILES = [
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/README.md",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/main.tex",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/src/distance_capacity/core.py",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/results/result.json",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/references.bib",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/README.md",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/main.tex",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/references.bib",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/src/shift_two_chowla/core.py",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/results/result.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
]

SOURCE_COMMITS = {
    "rh371_release": "241b78a89ccbc0bad96d9ef20ee9256d61b4eaca",
    "rh374_release": "2bb3baa6a09491c2d679d10c0dbcd39587d1f831",
    "rh376_release": "0cf6179084bc8151318bb8f0955e529c12c0661a",
    "rh_mvp2_archive": "c0aed13a34b8bbc53061aed23738660adcd3624c",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> None:
    sources = {relative: digest(WORKSPACE / relative) for relative in SOURCE_FILES}
    certificate = verify_certificate()
    if not certificate["all_pass"]:
        raise RuntimeError("RH-377 exact finite certificate failed")
    payload = {
        "status": "RH-377_mixed_exponent_run_hierarchy_two_envelope_capacity",
        "source_locks": {"count": len(sources), "files": sources, "pass": True},
        "source_commits": SOURCE_COMMITS,
        "certificate": certificate,
        "theorem": {
            "common_endpoint": "for each k, 1<=n<=N-2(k-1) with n odd",
            "mixed_identity": "2^k C_(sigma,k)=H_(k,0)+A_k+sigma*(H_(k,1)+B_k), 1<=k<=8",
            "deterministic_layers": "H_(k,0)/N -> Delta_k=e_k/2 with e_k=product_(p odd)(1-k/p^2), and H_(k,1)=o(N)",
            "simultaneous_density_boundary": "all 16 signed densities exist iff A_k/N (2<=k<=8) and B_k/N (3<=k<=8) all exist",
            "formal_map": "466 formal |S|>=2 coordinates map to 13 disjoint aggregate blocks with rank 13 and kernel 453",
            "capacity_reduction": "K_N/N converges iff (U_N+abs(V_N))/N converges",
            "conditional_constant": "full mixed-exponent cancellation would give 2/pi^2+sum_(k=1)^8 (-1)^(k+1)e_k/2^k",
            "synthetic_boundary": "a stationary ternary chain matches raw, square-only, and one-sign masked algebra but has a nonzero directional two-sign masked moment",
        },
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "first_unresolved_object": "ordinary convergence of (U_N+abs(V_N))/N",
            "notes": [
                "The 466-to-13 rank is a formal block-sum map, not an arithmetic minimal-dimension theorem for Mobius correlations.",
                "A single signed density supplies one A_k+sigma B_k combination and does not force A_k/N and B_k/N separately to converge.",
                "The stationary ternary chain is synthetic, is not Mobius, and does not match Mobius squarefree densities.",
                "Finite rows reproduce exact identities only and are not evidence for asymptotic cancellation or convergence.",
                "Full mixed-exponent cancellation is sufficient for the displayed conditional constant, not necessary and not proved.",
                "No capacity limit, intrinsic operator, trace formula, zeta-zero identification, Hilbert--Polya construction, or RH implication is claimed.",
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
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "source_lock_count": len(sources),
                "all_pass": certificate["all_pass"],
                "boolean_cases": certificate["boolean_and_formal_rank"][
                    "boolean_case_count"
                ],
                "window_updates": certificate["mobius_finite_residual_ledger"][
                    "window_updates"
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
