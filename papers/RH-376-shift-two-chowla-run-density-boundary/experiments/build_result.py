"""Build the RH-376 source-locked result ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from shift_two_chowla import verify_certificate


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
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/README.md",
    "prime_dynamics_theory/papers/RH-375-all-clock-one-site-mobius-capacity-supremum/results/result.json",
    "prime_dynamics_theory/papers/tpc-193-literal-fixed-atom-candidate-mechanism-gate/README.md",
    "prime_dynamics_theory/papers/tpc-193-literal-fixed-atom-candidate-mechanism-gate/main.tex",
    "prime_dynamics_theory/papers/tpc-193-literal-fixed-atom-candidate-mechanism-gate/references.bib",
    "prime_dynamics_theory/papers/tpc-193-literal-fixed-atom-candidate-mechanism-gate/experiments/tpc193_literal_fixed_atom_candidate_mechanism_gate.json",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json",
]

SOURCE_COMMITS = {
    "rh371_release": "241b78a89ccbc0bad96d9ef20ee9256d61b4eaca",
    "rh374_release": "2bb3baa6a09491c2d679d10c0dbcd39587d1f831",
    "rh375_release": "071fed1b2a5d8488b9d2e35a99a753953b233584",
    "tpc193_release": "14d7a1dfd82b0575b43a65c8254fce3cf53acda5",
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
        raise RuntimeError("finite certificate failed")
    payload = {
        "status": "RH-376_shift_two_chowla_run_density_boundary",
        "source_locks": {"count": len(sources), "files": sources, "pass": True},
        "source_commits": SOURCE_COMMITS,
        "certificate": certificate,
        "theorem": {
            "common_endpoint": "all sums use 1<=n<=N-2",
            "boolean_identity": "4C_(sigma,2)=Q2+sigma*U2+sigma*V2+D2 for sigma in {-1,+1}",
            "squarefree_pair_density": "Q2/N -> kappa2=product_p(1-2/p^2)",
            "masked_cancellation": "U2=o(N) and V2=o(N), by fixed-cutoff AP cancellation",
            "rigidity": "if D2/N has a Cesaro limit, the frozen logarithmic affine theorem forces that limit to be zero",
            "equivalence": "for either fixed sigma, C_(sigma,2)/N converges iff D2=o(N); then its limit is kappa2/4",
        },
        "claim_boundary": {
            "route_a": "GO",
            "route_b": "STOP_SCOPED",
            "notes": [
                "C_(sigma,2) counts overlapping two-site same-sign intervals, not maximal or exact-length-two runs.",
                "Ordinary shift-two Cesaro Chowla is not proved; the result is an equivalence and hardness boundary.",
                "No failure of convergence is proved for either signed interval density.",
                "No conclusion is drawn about the RH-371 eight-run envelope or convergence of K_N/N.",
                "The cutoff proof fixes the square-divisor cutoff before N tends to infinity; no growing-modulus theorem is used.",
                "Run lengths k>=3 and all memory-dependent classes remain open.",
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
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "source_lock_count": len(sources),
        "all_pass": certificate["all_pass"],
        "pointwise_identity_count": certificate["pointwise_identity_count"],
        "cumulative_prefix_count": certificate["cumulative_prefix_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
