"""Build the RH-374 source-locked result ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from square_clock import verify_certificate


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_FILES = [
    "henon_mobius_correlations/THEOREM_PACKAGE.md",
    "henon_mobius_correlations/henon_mobius/arithmetic.py",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/README.md",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/results/result.json",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/README.md",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/results/result.json",
    "prime_dynamics_theory/papers/RH-373-composite-clock-mobius-capacity-floor/README.md",
    "prime_dynamics_theory/papers/RH-373-composite-clock-mobius-capacity-floor/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-373-composite-clock-mobius-capacity-floor/results/result.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
]

SOURCE_COMMITS = {
    "henon_mobius_correlations": "34490443f50cfe9af9ff93888e51e7e7e534a5a7",
    "rh366_release": "0396fab97bbe3348c8237f8734dec0e1893fd3bf",
    "rh371_release": "241b78a89ccbc0bad96d9ef20ee9256d61b4eaca",
    "rh372_release": "7a7b10b74722b520b145064923af8df6d4e2e73f",
    "rh373_release": "e46a0b0ef0e459fc26711c379ce8c1b68deb9c58",
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
    payload = {
        "status": "RH-374_square_clock_euler_product_capacity_floor",
        "source_locks": {"count": len(sources), "files": sources, "pass": True},
        "source_commits": SOURCE_COMMITS,
        "certificate": certificate,
        "theorem": {
            "clocks": "q_y=4*prod_{i<=y}p_i^2 with p_1=3",
            "fixed_clock_optimum_scope": (
                "universally safe one-site phase/current-input factors at fixed q_y"
            ),
            "fixed_clock_optimum": "B_y=(4+2*O_y/A_y)/pi^2",
            "run_formula": (
                "O_y=P_y*sum_{j in {1,3,5,7}}"
                "(E_j-2*E_(j+1)+E_(j+2))"
            ),
            "recurrence": "A'=(p^2-1)A; O'=(p^2-1)O+L_even",
            "strict_monotonicity": True,
            "q900_improvement_over_rh373": "1/(24*pi^2)",
            "euler_limit": (
                "B_infinity=(4+2*C)/pi^2 with "
                "C=sum_odd(e_j-2e_(j+1)+e_(j+2))/e_1"
            ),
            "capacity_statement": "liminf K_N/N >= B_infinity",
            "quantifier": (
                "fix y before N tends to infinity; one scalar liminf dominates all B_y"
            ),
        },
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "notes": [
                "The exact optimum is only for fixed-q_y universally safe one-site phase/current-input factors.",
                "No optimizer over arbitrary memory transducers or all clocks is claimed.",
                "No q(N), uniform-in-q Davenport estimate, or infinite selector is used.",
                "The ordinary limit of the adaptive RH-366 capacity remains open.",
                "Finite Mobius endpoints and the decimal Euler enclosure are diagnostics, not asymptotic evidence.",
                "No intrinsic operator, prime-power trace, zero identification, Hilbert--Polya construction, or RH implication is claimed.",
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
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "source_lock_count": len(sources),
        "all_pass": certificate["all_pass"],
        "q900_pi2_coefficient": certificate["q900_vs_rh373"]["q900_pi2_coefficient"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
