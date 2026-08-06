"""Build the RH-371 theorem ledger and exact finite audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from distance_capacity import (
    ENDPOINT,
    PAIR_ORDER,
    PERIOD_WORDS,
    cyclic_pair_ledger,
    finite_checks,
    open_pair_ledger,
)


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_LOCKS = {
    "henon_mobius_correlations/henon_mobius/capacity.py": "1c415c1e4f8adfeaa0bd27b7fd04cb0f5b88a0acb50a81e9553a9b3239450833",
    "henon_mobius_correlations/THEOREM_PACKAGE.md": "634fd9543ceab91c19766015141e83636d64213f131d5c1b098385ef68c3b102",
    "henon_mobius_correlations/tests/test_capacity.py": "0f70143c2f0dc880eef19ca625ddb69f2ecd9556e4cced3e357d6141cd188188",
    "henon_mobius_correlations/paper/sections/6_capacity_audit.tex": "7c04a7c403ca1879f61e4238144d9044f77f05441fdfd3ccc76cc4c743ba2a37",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/main.tex": "7df165bd63d43f52dc217dea6691d231d8e40c00c148ab7e1aa4abcac55060fb",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md": "d357192bfb80da578459cdac4add37840b8e1e47c5b2188ca0e49e7b096cbb23",
    "prime_dynamics_theory/papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json": "6a125ca90b0964945f95b39397b6e83f15a23ad24c94d2e8b9c90d320db8e418",
    "prime_dynamics_theory/papers/RH-370-fold-compatible-ulam-spike-barrier/UPDATED_ROADMAP.md": "9fc7eafad7763d32d49a617ecdd87ec1b64e625112e6dc39084bd8715397e6f5",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json": "b27f120f77c4bbf3afd3a4486fd800a8de93a2db52236c835809aa488d113751",
}

SOURCE_COMMITS = {
    "henon_mobius_correlations": "34490443f50cfe9af9ff93888e51e7e7e534a5a7",
    "prime_dynamics_theory_rh366_release": "6da1b94deaa865bbb297546f3de238433184772a",
    "prime_dynamics_theory_rh370_release": "9ad958a1f326eae6f43f026c84ab9378a4a42f16",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def source_audit() -> dict[str, object]:
    rows = []
    for relative, expected in SOURCE_LOCKS.items():
        path = WORKSPACE / relative
        actual = digest(path) if path.is_file() else "MISSING"
        rows.append({
            "path": relative,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "pass": actual == expected,
        })
    return {"rows": rows, "pass": all(row["pass"] for row in rows)}


def build_payload() -> dict[str, object]:
    checks = finite_checks()
    gates = {
        "A_canonical_intrinsic_dynamical_spectral_determinant": False,
        "B_time_oriented_scattering_or_unitary_completion": False,
        "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "capacity_limit_proved": False,
        "cyclic_ledger_is_open_prefix_ledger": False,
        "periodic_witness_is_mobius": False,
        "pair_data_is_sufficient_for_capacity": False,
        "finite_endpoint_is_asymptotic_evidence": False,
        "adaptive_optimizer_is_canonical_coupling": False,
        "canonical_spectral_determinant_constructed": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_identified": False,
        "riemann_hypothesis_proved": False,
    }
    return {
        "status": "RH-371_eight_run_distance_two_capacity_obstruction",
        "route_verdict": {"route_a": "GO", "route_b": "STOP_SCOPED"},
        "gates": gates,
        "false_claims": false_claims,
        "source_commits": SOURCE_COMMITS,
        "source_audit": source_audit(),
        "exact_theorems": {
            "run_reduction": "W_sigma=E_sigma+sum_{k=1}^8(-1)^(k+1) C_sigma,k for every N",
            "capacity_identity": "K_N=max(abs(-M_N+2W_+),abs(-M_N-2W_-))",
            "mod9_cutoff": "every nine odd step-two positions include a multiple of 9",
            "density_criterion": "K_N/N converges iff max(R_+(N),R_-(N))/N converges",
            "cyclic_pair_obstruction": "u and v have identical cyclic ordered pair ledgers but different capacities",
            "periodic_capacities": "K_(18q)(u^q)=10q and K_(18q)(v^q)=12q",
        },
        "finite_checks": checks,
        "periodic_audit": {
            "pair_order": PAIR_ORDER,
            "words": PERIOD_WORDS,
            "cyclic_ledger_equal": cyclic_pair_ledger(PERIOD_WORDS["u"]) == cyclic_pair_ledger(PERIOD_WORDS["v"]),
            "cyclic_ledger_rows": len(cyclic_pair_ledger(PERIOD_WORDS["u"])),
            "cyclic_pair_cells": 18 * len(PAIR_ORDER),
            "open_lag2_u": open_pair_ledger(PERIOD_WORDS["u"], 2),
            "open_lag2_v": open_pair_ledger(PERIOD_WORDS["v"], 2),
            "open_lag2_differs": open_pair_ledger(PERIOD_WORDS["u"], 2) != open_pair_ledger(PERIOD_WORDS["v"], 2),
            "interpretation": "cyclic/periodic ledger only; not an open-prefix or Mobius counterexample",
        },
        "endpoint": {
            "N": ENDPOINT,
            "interpretation": "exact finite reproduction only; no asymptotic fit",
            **checks["endpoint"],
        },
        "overlap_ledger": {
            "RH-366": "supplies the frozen distance-two constraint, path MWIS, and bracket; the capacity limit remains open",
            "henon_mobius_correlations": "supplies the source implementation and brute-force checks",
            "RH-370": "identifies the run-reduction candidate but does not prove the capacity theorem",
            "distinct_edge": True,
        },
        "claim_boundary": {
            "route_b_first_blocker": "no theorem for convergence of the alternating eight-run Mobius envelope",
            "physical_coordinate": "actual_same_clock_unnormalized_head_transport_open",
            "notes": [
                "The eight-run identity is an exact finite-prefix theorem, not an asymptotic limit.",
                "The pair obstruction is cyclic/periodic and synthetic; its words are not Mobius.",
                "Open-prefix pair ledgers differ and are not claimed equal.",
                "The adaptive optimizer reads the complete Mobius prefix and is not a canonical trace.",
                "No Hilbert--Polya operator, von Mangoldt trace, zero identification, or RH implication is claimed.",
            ],
        },
    }


def main() -> None:
    payload = build_payload()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "source_lock_pass": payload["source_audit"]["pass"],
        "finite_checks": payload["finite_checks"]["all_pass"],
        "cyclic_ledger_equal": payload["periodic_audit"]["cyclic_ledger_equal"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
