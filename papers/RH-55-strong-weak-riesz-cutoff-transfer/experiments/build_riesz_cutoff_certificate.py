"""Compose the RH-55 analytic and numerical closure ledger."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "results" / "riesz_cutoff_pilot.json"
ARB = ROOT / "results" / "arb_riesz_cutoff_ledger.json"
OUTPUT = ROOT / "results" / "riesz_cutoff_closure_certificate.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    pilot = load(PILOT)
    arb = load(ARB)
    payload = {
        "status": (
            "rigorous_adaptive_strong_weak_riesz_cutoff_transfer_with_"
            "midpoint_ulam_contour_inheritance"
        ),
        "scope": (
            "adaptive sparse-to-full unweighted and weighted intrinsic Riesz "
            "transfer for the conditioned folded-Gaussian Ulam/midpoint family"
        ),
        "evidence_levels": {
            "analytic": [
                "conditioned-kernel derivative and midpoint-to-Ulam estimates",
                "common strong-space peripheral contours",
                "two-sided sandwiched Riesz perturbation identity",
                "mass-only and Gaussian-shape adaptive exponent theorems",
                "fixed-window strong-BV route no-go",
            ],
            "binary64_diagnostic": pilot["evidence_level"],
            "arb_formula_audit": arb["evidence_level"],
        },
        "midpoint_ulam_theorem": {
            "kernel_derivative": (
                "sup_x integral (|d_xx k_sigma|+|d_yy k_sigma|) dy "
                "= O(sigma^-2)"
            ),
            "row_l1": "O(h^2 sigma^-2)",
            "piecewise_bv": "O(h sigma^-2)",
            "schedule": "h=o(sigma^2)",
            "consequence": (
                "fixed strong-space contours pass from exact Ulam to the full "
                "discretely normalized midpoint family"
            ),
        },
        "sandwich_riesz_theorem": {
            "projector_identity": (
                "Pi(T;Gamma)=(2 pi i)^-1 integral_Gamma "
                "z^-2 T(z-T)^-1T dz"
            ),
            "weighted_identity": (
                "W(T;Gamma)=(2 pi i)^-1 integral_Gamma "
                "z^-1 T(z-T)^-1T dz"
            ),
            "sandwich_defect": (
                "D<=rho M R + S M Mtilde tau_1 R + "
                "S Mtilde tau_0"
            ),
            "norms": {
                "R": "||T||_(L1->B)",
                "S": "||Ttilde||_(L1->L2)",
                "rho": "||T-Ttilde||_(L1->L2)",
                "tau_0": "||T-Ttilde||_(L1->B)",
                "tau_1": "||T-Ttilde||_(B->B)",
                "M_and_Mtilde": "strong-space contour resolvent suprema",
            },
            "global_l2_contour_required": False,
        },
        "mass_only_route": {
            "row_identity": "||Delta row_i||_l1=2q_i",
            "norms": {
                "rho": "O(Q_h h^-1/2)",
                "tau_0_tau_1": "O(Q_h/h)",
            },
            "riesz_defect": "O(Q_h/(h sigma^(3/2)))",
            "adaptive_tail": "Q_h=O(h^kappa/sqrt(log(1/h)))",
            "all_strict_mesh_schedules_threshold": "kappa>=7/4",
            "threshold_is_necessary": False,
        },
        "gaussian_shape_route": {
            "norms": {
                "rho": "O(exp(-L_h^2/2) sigma^-1/2)",
                "tau_0_tau_1": "O(exp(-L_h^2/2) sigma^-1)",
            },
            "riesz_defect": "O(exp(-L_h^2/2) sigma^-5/2)",
            "adaptive_riesz_defect": "O(h^kappa sigma^-5/2)",
            "all_strict_mesh_schedules_threshold": "kappa>=5/4",
            "threshold_is_necessary": False,
            "rh39_kappa_two_conclusion": "o(sigma^(3/2))",
        },
        "fixed_window_no_go": {
            "conclusion": (
                "fixed L does not yield a vanishing full-kernel perturbation "
                "through the present strong-BV sandwich route"
            ),
            "does_not_claim_actual_riesz_divergence": True,
        },
        "program_conclusion": {
            "midpoint_to_ulam_contour_inheritance_closed": True,
            "adaptive_sparse_full_projector_modulus_closed": True,
            "adaptive_sparse_full_weighted_riesz_modulus_closed": True,
            "rh54_factor_aware_cutoff_premise_closed": True,
            "stage_A3_analytic_factor_transfer_component_closed": True,
            "production_intrinsic_riesz_interval_eigensolver_executed": False,
            "stage_A1_uniform_hardy_budget_closed": False,
            "stage_A3_production_interval_program_closed": False,
            "stage_A4_unconditional_identification_closed": False,
        },
        "binary64_audit": {
            "midpoint_ulam_levels": len(pilot["midpoint_ulam_audit"]),
            "factor_rows": len(pilot["archived_intrinsic_factor_audit"]),
            "extrema": pilot["extrema"],
            "interval_validated": False,
        },
        "arb_audit": {
            "status": arb["status"],
            "precision_bits": arb["precision_bits"],
            "omitted_mass_upper_ball": arb["omitted_mass_upper_ball"],
            "adaptive_below_sqrt_sigma_certified": arb[
                "adaptive_schedule_audit"
            ]["below_sqrt_sigma_certified"],
            "production_intrinsic_riesz_interval_eigensolver_executed": arb[
                "production_intrinsic_riesz_interval_eigensolver_executed"
            ],
        },
        "limitations": [
            "The strong-space constants are asymptotic and are not production-scale interval contour constants.",
            "The binary64 midpoint quadrature and inherited RH-54 eigensolver defects are diagnostics, not interval enclosures.",
            "The Arb run validates formula arithmetic but not a folded-Gaussian intrinsic Riesz eigensolver.",
            "The kappa thresholds are sufficient for the stated proof routes and are not claimed necessary for actual Riesz stability.",
            "The fixed-window result is a strong-BV proof-route no-go, not an actual projector-divergence theorem.",
            "Stage A1 still lacks a dyadically uniform Hardy/Stein trace budget, so Stage A4 remains conditional.",
            "No arithmetic trace formula, prime-power identity, zeta-zero spectral identity, self-adjoint Hilbert--Polya operator, T log T law, Riemann-hypothesis conclusion, or TPC twin-prime conclusion is claimed.",
        ],
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(OUTPUT.relative_to(ROOT)),
                "status": payload["status"],
                "program_conclusion": payload["program_conclusion"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
