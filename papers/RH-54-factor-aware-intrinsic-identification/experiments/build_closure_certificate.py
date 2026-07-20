"""Build the theorem, numerical, and boundary certificate for RH-54."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from intrinsic_transfer import (  # noqa: E402
    identification_budget,
    nonnormal_projector_example,
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    pilot = load(ROOT / "results" / "factor_aware_transfer_pilot.json")
    smoke = load(ROOT / "results" / "factor_aware_transfer_pilot_smoke.json")
    arb = load(ROOT / "results" / "arb_factor_transfer_audit.json")
    polylog = identification_budget(0.0, 0.0)
    threshold = identification_budget(0.1, 0.15)
    beyond = identification_budget(0.1, 0.151)
    example = nonnormal_projector_example(1.0e6, 0.25)
    stress_rows = [row["comparisons"][0] for row in pilot["rows"]]
    certificate = {
        "status": (
            "rigorous_factor_aware_closure_criterion_with_nonnormal_"
            "conditioning_gate_and_five_scale_transfer_audit"
        ),
        "scope": (
            "finite-dimensional sparse-to-full transfer for intrinsic two-pole "
            "Hardy triples and conditional composition into the RH-48/49 dyadic "
            "identification theorem"
        ),
        "evidence_levels": {
            "analytic": [
                "normalized Hilbert--Schmidt coupling stability",
                "contour-conditioned projector and weighted-Riesz perturbation ledgers",
                "factor-aware left and right triple transfer",
                "finite-time semigroup and growing-block contraction transfer",
                "Hardy-exponent composition into the RH-49 quarter-power and RH-48 dyadic bounds",
                "two-by-two nonnormal no-free-lunch family",
            ],
            "binary64": pilot["evidence_level"],
            "interval": arb["evidence_level"],
        },
        "normalized_coupling_theorem": {
            "premise": "epsilon_B < ||B||_S2",
            "conclusion": (
                "||B/||B||_S2-Btilde/||Btilde||_S2||_S2 "
                "<= 2 epsilon_B/||B||_S2"
            ),
            "adaptive_asymptotic_consequence": (
                "using ||B||_S2,||C||_S2 asymp h sigma^(-3/2) and "
                "epsilon_h=O(h^2/log(1/h)^(1/4)), the normalized coupling "
                "defect is O(h sigma^(3/2)/log(1/h)^(1/4))"
            ),
        },
        "riesz_conditioning_ledger": {
            "projector": (
                "epsilon_P <= sum_Gamma length(Gamma) M_Gamma Mtilde_Gamma "
                "epsilon_T/(2 pi)"
            ),
            "weighted": (
                "epsilon_W <= sum_Gamma length(Gamma) max_Gamma|z| "
                "M_Gamma Mtilde_Gamma epsilon_T/(2 pi)"
            ),
            "necessity": (
                "operator cutoff convergence alone cannot supply a dimension-free "
                "Riesz or semigroup-transient modulus for nonnormal families"
            ),
        },
        "factor_aware_triple_transfer": {
            "left": {
                "operator": "delta_A <= (delta_T+epsilon_W,f)/r",
                "source": (
                    "delta_X <= epsilon_P,f+||Qtilde_f|| "
                    "2 delta_B/||B||_S2"
                ),
                "observation": "delta_Y=0",
            },
            "right": {
                "operator": "delta_A <= (delta_T,c+epsilon_W,c)/r",
                "source": "delta_X <= 2 delta_C/||C||_S2",
                "observation": "delta_Y <= epsilon_P,c",
            },
        },
        "growing_horizon_transfer": {
            "power_defect": (
                "d_M=delta_A sum_(j=0)^(M-1) ||A^(M-1-j)|| "
                "||Atilde^j||"
            ),
            "contraction_condition": "q_M+d_M<1",
            "ledger_requirement": (
                "actual finite-time semigroup norm uppers are used; no substitution "
                "by ||A||^j is made"
            ),
        },
        "conditional_identification_composition": {
            "hardy_product": (
                "E_B=O(sigma^(-alpha_B)), E_C=O(sigma^(-alpha_C)) "
                "implies F=O(sigma^(-delta)), delta=alpha_B+alpha_C, "
                "provided range-restricted residues are O(1)"
            ),
            "identification": (
                "||I_(n,sigma)||_S2=O(n^(-2) sigma^(-13/4-delta))"
            ),
            "all_strict_mesh_schedules_condition": "delta<=1/4",
            "polylogarithmic_case": {
                "hardy_product_exponent": polylog.hardy_product_exponent,
                "mixed_gain_exponent": polylog.mixed_gain_exponent,
                "identification_sigma_exponent": polylog.identification_sigma_exponent,
                "preserves_all_strict_schedules": (
                    polylog.preserves_all_strict_bulk_square_schedules
                ),
            },
            "threshold_case": {
                "left_exponent": 0.1,
                "right_exponent": 0.15,
                "preserves_all_strict_schedules": (
                    threshold.preserves_all_strict_bulk_square_schedules
                ),
            },
            "beyond_threshold_case": {
                "left_exponent": 0.1,
                "right_exponent": 0.151,
                "preserves_all_strict_schedules": (
                    beyond.preserves_all_strict_bulk_square_schedules
                ),
            },
        },
        "nonnormal_no_go": {
            "family": (
                "T_K=[[0,K],[0,1]], E_K=[[0,0],[c/K,0]], c=1/4"
            ),
            "K": 1.0e6,
            "operator_defect": example["operator_defect"],
            "projector_defect": example["projector_defect"],
            "defect_ratio": example["projector_defect"]
            / example["operator_defect"],
            "perturbed_eigenvalues": example["eigenvalues"].tolist(),
            "conclusion": (
                "the input defect tends to zero while the Riesz projector defect "
                "stays bounded below; contour conditioning cannot be omitted"
            ),
        },
        "floating_five_scale_audit": {
            "noise_levels": len(pilot["rows"]),
            "dimensions": [row["fine_dimension"] for row in pilot["rows"]],
            "horizons": [row["horizon"] for row in pilot["rows"]],
            "cutoff_multiples": pilot["cutoff_multiples"],
            "extrema": pilot["extrema"],
            "stress_rows": [
                {
                    "sigma": row["sigma"],
                    "dimension": row["fine_dimension"],
                    "horizon": row["horizon"],
                    "markov_spectral_defect": comparison["matrix_defects"][
                        "markov_spectral"
                    ],
                    "fine_weighted_riesz_defect": comparison[
                        "intrinsic_factor_defects"
                    ]["fine_weighted_riesz_spectral"],
                    "normalized_b_defect": comparison[
                        "intrinsic_factor_defects"
                    ]["normalized_coupling_b_actual"],
                    "left_block_margin_ratio": comparison["left"][
                        "telescope_over_sparse_contraction_margin"
                    ],
                    "right_block_margin_ratio": comparison["right"][
                        "telescope_over_sparse_contraction_margin"
                    ],
                    "left_actual_energy_squared_difference": comparison["left"][
                        "actual_full_energy_squared_difference"
                    ],
                    "left_finite_perturbation_upper": comparison["left"][
                        "finite_energy_squared_perturbation_upper"
                    ],
                    "right_actual_energy_squared_difference": comparison["right"][
                        "actual_full_energy_squared_difference"
                    ],
                    "right_finite_perturbation_upper": comparison["right"][
                        "finite_energy_squared_perturbation_upper"
                    ],
                    "left_transferred_full_energy_upper": comparison["left"][
                        "transferred_full_energy_upper"
                    ],
                    "right_transferred_full_energy_upper": comparison["right"][
                        "transferred_full_energy_upper"
                    ],
                }
                for row, comparison in zip(pilot["rows"], stress_rows)
            ],
            "interval_validated": False,
        },
        "smoke_audit": {
            "noise_levels": len(smoke["rows"]),
            "all_factor_bounds_dominate_actual": smoke["extrema"][
                "all_factor_bounds_dominate_actual"
            ],
            "all_transferred_blocks_contract": smoke["extrema"][
                "all_transferred_blocks_contract"
            ],
        },
        "arb_audit": arb,
        "program_conclusion": {
            "normalized_coupling_gate_closed": True,
            "factor_aware_finite_matrix_transfer_theorem_closed": True,
            "growing_horizon_block_robustness_closed": True,
            "conditional_RH48_to_RH53_composition_closed": True,
            "production_intrinsic_riesz_interval_enclosure_executed": False,
            "dyadically_uniform_riesz_conditioning_modulus_proved": False,
            "stage_A1_uniform_hardy_budget_closed": False,
            "stage_A3_fully_closed": False,
            "stage_A4_unconditional_identification_closed": False,
            "next_gate": (
                "prove a dyadically uniform analytic Hardy/Stein trace budget and "
                "a strong/weak or contour-conditioned Riesz modulus, or validate "
                "both with production-scale outward arithmetic"
            ),
        },
        "limitations": [
            "The factor-aware algebra is rigorous, but the five-scale folded-Gaussian audit is binary64 and not an interval enclosure.",
            "The Arb execution validates a small abstract factor ledger; it is not the N=40960 production matrix or its intrinsic Riesz factors.",
            "Five noise levels cannot prove a dyadically uniform Riesz-conditioning modulus or a uniform/polylogarithmic Stage A1 Hardy budget.",
            "Therefore Stage A3 and unconditional Stage A4 remain open; the result is a complete closure criterion rather than an unconditional small-noise identification theorem.",
            "No arithmetic trace formula, prime-power identity, zeta-zero spectral identity, self-adjoint Hilbert--Polya operator, T log T counting law, or Riemann-hypothesis conclusion is claimed.",
            "The TPC twin-prime branch is independent and is not a premise of this theorem.",
        ],
    }
    output = ROOT / "results" / "intrinsic_identification_closure_certificate.json"
    output.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output.relative_to(ROOT))}, sort_keys=True))


if __name__ == "__main__":
    main()
