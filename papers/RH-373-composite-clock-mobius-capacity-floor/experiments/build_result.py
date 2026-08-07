"""Build the RH-373 source-locked result ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from composite_clock import verify_certificate


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
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/results/result.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
]

SOURCE_COMMITS = {
    "henon_mobius_correlations": "34490443f50cfe9af9ff93888e51e7e7e534a5a7",
    "rh366_release": "0396fab97bbe3348c8237f8734dec0e1893fd3bf",
    "rh371_release": "241b78a89ccbc0bad96d9ef20ee9256d61b4eaca",
    "rh372_release": "7a7b10b74722b520b145064923af8df6d4e2e73f",
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
        "status": "RH-373_composite_clock_mobius_capacity_floor",
        "source_locks": {"count": len(sources), "files": sources, "pass": True},
        "source_commits": SOURCE_COMMITS,
        "certificate": certificate,
        "theorem": {
            "clock": 180,
            "phase_set_cardinality": 80,
            "density": "97/(24*pi^2)",
            "baseline": "4/pi^2",
            "improvement": "1/(24*pi^2)",
            "unconditional_statement": "liminf K_N/N >= 97/(24*pi^2)",
            "upper_bound_inherited": "limsup K_N/N <= 6/pi^2",
        },
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "notes": [
                "The q=180 phase selector is an explicit lower-bound witness, not an optimizer classification.",
                "The ordinary limit of the adaptive RH-366 capacity remains open.",
                "No supremum over clocks or memory-dependent observables is claimed.",
                "The transducer uses prescribed phase and current Mobius input and is not an intrinsic operator or trace.",
                "No Hilbert--Polya operator, zero identification, or RH implication is claimed.",
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
        "density": certificate["density_constant"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
