"""Build the RH-375 source-locked result ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from all_clock_capacity import verify_certificate


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_FILES = [
    "henon_mobius_correlations/THEOREM_PACKAGE.md",
    "henon_mobius_correlations/henon_mobius/arithmetic.py",
    "henon_mobius_correlations/henon_mobius/capacity.py",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/README.md",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/results/result.json",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/README.md",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/main.tex",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/results/result.json",
    "prime_dynamics_theory/papers/RH-373-composite-clock-mobius-capacity-floor/README.md",
    "prime_dynamics_theory/papers/RH-373-composite-clock-mobius-capacity-floor/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-373-composite-clock-mobius-capacity-floor/main.tex",
    "prime_dynamics_theory/papers/RH-373-composite-clock-mobius-capacity-floor/results/result.json",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/README.md",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/main.tex",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/references.bib",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/results/result.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
]

SOURCE_COMMITS = {
    "henon_mobius_correlations": "34490443f50cfe9af9ff93888e51e7e7e534a5a7",
    "rh366_release": "0396fab97bbe3348c8237f8734dec0e1893fd3bf",
    "rh371_release": "241b78a89ccbc0bad96d9ef20ee9256d61b4eaca",
    "rh372_release": "7a7b10b74722b520b145064923af8df6d4e2e73f",
    "rh373_release": "e46a0b0ef0e459fc26711c379ce8c1b68deb9c58",
    "rh374_release": "2bb3baa6a09491c2d679d10c0dbcd39587d1f831",
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
        "status": "RH-375_all_clock_one_site_mobius_capacity_supremum",
        "source_locks": {"count": len(sources), "files": sources, "pass": True},
        "source_commits": SOURCE_COMMITS,
        "certificate": certificate,
        "theorem": {
            "factor_class": (
                "fixed finite q, q-periodic (not necessarily minimal-period), "
                "universally safe one-site phase/current-input factors"
            ),
            "fixed_clock_formula": (
                "F(q)=max_{I intersect (I+2)=empty} sum_{r in I} delta_(q,r)"
            ),
            "divisibility_monotonicity": "q divides Q implies F(q)<=F(Q)",
            "cofinal_saturation": (
                "if q_y divides Q and Q has the same prime support as q_y, "
                "then F(Q)=F(q_y)=B_y"
            ),
            "all_clock_supremum": "sup_{q finite} F(q)=B_infinity",
            "nonattainment": "F(q)<B_infinity for every finite q",
            "capacity_relation": (
                "B_infinity remains a liminf floor for RH-366, but no adaptive "
                "capacity convergence is asserted"
            ),
        },
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "notes": [
                "The optimum is exact only over fixed finite-clock universally safe one-site factors.",
                "The special square-clock replication is not a general cyclic-cover MWIS theorem.",
                "No memory-dependent observable, q(N), infinite selector, or uniform-in-q Davenport estimate is used.",
                "No adaptive-capacity limit or identification with its liminf is claimed.",
                "Finite scans are reproduction only, not all-clock theorem evidence.",
                "No intrinsic operator, trace, zero identification, Hilbert--Polya construction, or RH implication is claimed.",
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
        "bounded_scan_max_pi2_F": certificate["bounded_clock_scan"]["maximum_pi2_F"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
