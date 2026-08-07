"""Build the source-locked RH-378 result ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from safe_window_transducers import verify_certificate


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_FILES = [
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/main.tex",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/src/mobius_henon_dichotomy/core.py",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/README.md",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/main.tex",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/src/distance_capacity/core.py",
    "prime_dynamics_theory/papers/RH-371-eight-run-distance-two-capacity-obstruction/results/result.json",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/README.md",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/main.tex",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/src/constraint_transducers/core.py",
    "prime_dynamics_theory/papers/RH-372-bounded-constraint-graph-transducer-certificates/results/result.json",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/references.bib",
    "prime_dynamics_theory/papers/RH-374-square-clock-euler-product-capacity-floor/results/result.json",
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/README.md",
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/main.tex",
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/src/all_clock_capacity/core.py",
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/results/result.json",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/README.md",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/main.tex",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/src/shift_two_chowla/core.py",
    "prime_dynamics_theory/papers/RH-376-shift-two-chowla-run-density-boundary/results/result.json",
    "prime_dynamics_theory/papers/RH-377-mixed-exponent-run-hierarchy-two-envelope-capacity/README.md",
    "prime_dynamics_theory/papers/RH-377-mixed-exponent-run-hierarchy-two-envelope-capacity/THEOREM_LEDGER.md",
    "prime_dynamics_theory/papers/RH-377-mixed-exponent-run-hierarchy-two-envelope-capacity/main.tex",
    "prime_dynamics_theory/papers/RH-377-mixed-exponent-run-hierarchy-two-envelope-capacity/src/mixed_run_hierarchy/core.py",
    "prime_dynamics_theory/papers/RH-377-mixed-exponent-run-hierarchy-two-envelope-capacity/results/result.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
]

SOURCE_COMMITS = {
    "rh366_release": "0396fab97bbe3348c8237f8734dec0e1893fd3bf",
    "rh371_release": "241b78a89ccbc0bad96d9ef20ee9256d61b4eaca",
    "rh372_release": "7a7b10b74722b520b145064923af8df6d4e2e73f",
    "rh374_release": "2bb3baa6a09491c2d679d10c0dbcd39587d1f831",
    "rh375_release": "071fed1b2a5d8488b9d2e35a99a753953b233584",
    "rh376_release": "0cf6179084bc8151318bb8f0955e529c12c0661a",
    "rh377_release": "3c6e5658f4147891d15dac18d303a22a46d6e289",
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
        raise RuntimeError("RH-378 finite certificate failed")
    payload = {
        "status": "RH-378_safe_window_memory_and_online_capacity_transducers",
        "source_locks": {"count": len(sources), "files": sources, "pass": True},
        "source_commits": SOURCE_COMMITS,
        "certificate": certificate,
        "theorem": {
            "general_window_safety": "a fixed q-periodic ell-window table is universally distance-two safe iff all q*3^(ell+2) compatible blocks pass",
            "current_zero_basis": "current-zero scores have a canonical 2*q*3^(ell-1)-element ternary monomial basis with unique coefficients",
            "lag_two_classification": "among 512 lag-two tables exactly 13 are universally safe; their six-column coefficient matrix has rank five and relation c22=-c02-c11",
            "lag_two_asymptotic_boundary": "seven c11=0 tables have unconditional limits; each of the other six has a limit iff ordinary shift-two Chowla D2=o(N)",
            "online_capacity": "two fixed four-state orientation machines output Smax and Smin exactly, while no single deterministic causal universally safe policy attains absolute K on every input prefix",
            "state_minimality": "four reachable states are necessary for exact output realization of either frozen orientation machine",
            "ell15_truncation": "the alternating depth-eight ell=15 table is universally safe and agrees with the orientation recursion on the run-at-most-eight class",
            "ell15_narrow_minimality": "within q=1 causal contiguous stateless exact-stream realizations on that class, window length 15 is minimal",
        },
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "first_unresolved_object": "ordinary shift-two Chowla cancellation D2=o(N), and beyond it the RH-371 capacity envelope",
            "notes": [
                "The formal window-basis dimension is not an arithmetic minimal-dimension theorem.",
                "The unconditional and conditional optima are only within the 13 safe lag-two tables.",
                "The conditional lag-two optimum is not an unconditional lower bound.",
                "Two fixed orientation machines plus an endpoint maximum are not one machine that directly outputs K.",
                "The online obstruction concerns a single deterministic causal policy that must be optimal at every input prefix; it does not exclude an offline endpoint optimizer.",
                "The four-state lower bound concerns exact realization of one frozen output stream, not all capacity algorithms or encodings.",
                "The ell=15 lower bound concerns q=1 contiguous stateless windows on the run-at-most-eight class, not stateful or nonlocal models.",
                "Finite Mobius rows reproduce exact identities and are not asymptotic evidence.",
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
                "safe_lag_tables": certificate["lag_two_census"]["safe_table_count"],
                "mobius_endpoint": certificate["mobius_finite_reproduction"]["endpoint"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
