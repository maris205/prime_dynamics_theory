"""Compose the RH-56 theorem and evidence ledger."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "results" / "hardy_barrier_pilot.json"
ARB = ROOT / "results" / "arb_hardy_barrier_ledger.json"
SECTOR = ROOT / "results" / "arb_sector_resonance_certificate.json"
OUTPUT = ROOT / "results" / "hardy_barrier_certificate.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    pilot = load(PILOT)
    arb = load(ARB)
    sector = load(SECTOR)
    payload = {
        "status": (
            "rigorous_two_stage_strong_space_budget_barrier_with_"
            "directional_overlap_escape_route"
        ),
        "scope": (
            "growing-horizon Hardy estimates for the two normalized adjacent-"
            "Haar channels after exact Perron/parity removal"
        ),
        "evidence_levels": {
            "analytic": [
                "two-stage Hardy splitting inequality",
                "optimized strong-space entrance exponent",
                "quarter-power critical decay-rate criterion",
                "modal overlap sufficient condition",
                "separation between global edge and directional overlap budgets",
            ],
            "binary64_diagnostic": pilot["evidence_level"],
            "arb_formula_audit": arb["evidence_level"],
        },
        "two_stage_theorem": {
            "premises": (
                "initial directional output bounded by a_m, strong tail "
                "bounded by S sigma^-p theta^m after the switch, theta<r"
            ),
            "energy_square_bound": (
                "sum_(m<M) r^(-2m) a_m^2 + "
                "S^2 sigma^(-2p) (theta/r)^(2M)/(1-(theta/r)^2)"
            ),
            "optimized_horizon": (
                "M=(p/log(1/theta)) log(1/sigma)+O(1)"
            ),
            "energy_power": "alpha=p log(1/r)/log(1/theta)",
        },
        "black_box_barrier": {
            "standard_entrance_power_per_direction": 1.0,
            "allowed_total_power": 0.25,
            "common_rate_criterion": "theta <= r^8",
            "r_at_audit": pilot["hardy_radius"],
            "critical_rate": pilot["strong_space_barrier"][
                "common_rate_threshold"
            ],
            "deterministic_edge_radius": pilot["deterministic_edge_radius"],
            "validated_sector_resonance_modulus_lower": sector[
                "certified_sector_resonance_modulus_lower_ball"
            ],
            "validated_one_step_rate_lower": sector[
                "certified_one_step_rate_lower_ball"
            ],
            "edge_two_side_total_power": pilot["extrema"][
                "edge_two_side_total_power"
            ],
            "conclusion": (
            "a proof that pays a full sigma^-1 strong-space prefactor "
            "cost in each direction cannot meet RH-54's quarter-power "
            "budget even at the validated analytic-sector rate lower"
            ),
            "does_not_claim_hardy_divergence": True,
        },
        "directional_overlap_theorem": {
            "setting": (
                "for N=sum_j mu_j P_j and normalized response blocks "
                "Z_j=Y P_j X"
            ),
            "upper": (
                "E(r) <= sum_j ||Z_j||_S2 / sqrt(1-|mu_j/r|^2)"
            ),
            "success_criterion": (
                "prove the displayed mixed overlap sum uniformly, "
                "polylogarithmically, or with the two-direction total power <=1/4"
            ),
            "spectral_radius_alone_sufficient": False,
            "eigenbasis_condition_number_alone_targeted": False,
            "nondiagonalizable_extension": (
                "replace simple modal terms by Riesz/Jordan blocks with their "
                "polynomial Hardy factors"
            ),
        },
        "program_conclusion": {
            "standard_global_strong_space_route_closed": False,
            "standard_global_strong_space_route_obstructed": True,
            "directional_overlap_route_viable": True,
            "stage_A1_uniform_hardy_budget_closed": False,
            "stage_A4_unconditional_identification_closed": False,
            "next_target": (
                "endpoint-interior or cloud-sector decomposition proving "
                "mixed Haar-channel Riesz overlap sums"
            ),
        },
        "binary64_audit": {
            "all_column_rows": len(pilot["all_column_dense_audit"]),
            "production_rows": len(pilot["production_directional_audit"]),
            "tail_rows": len(pilot["deterministic_tail_audit"]),
            "extrema": pilot["extrema"],
            "interval_validated": False,
        },
        "arb_audit": {
            "status": arb["status"],
            "precision_bits": arb["precision_bits"],
            "threshold_below_point_two_eight_certified": arb[
                "threshold_below_point_two_eight_certified"
            ],
            "edge_total_exceeds_quarter_certified": arb[
                "edge_total_exceeds_quarter_certified"
            ],
            "production_operator_interval_eigensolver_executed": arb[
                "production_operator_interval_eigensolver_executed"
            ],
            "sector_resonance_status": sector["status"],
            "sector_resonance_precision_bits": sector["precision_bits"],
            "sector_full_contour_perturbation_product": sector[
                "full_contour_perturbation_product_ball"
            ],
            "sector_rate_lower_exceeds_r_to_eight_certified": sector[
                "rate_lower_exceeds_r_to_eight_certified"
            ],
        },
        "limitations": [
            "The barrier is conditional on a global one-step estimate whose two-step restriction contains the certified analytic sector and on paying the full standard sigma^-1 strong-space prefactor in each direction; it is a route no-go, not a lower bound on the actual Hardy energies.",
            "The validated analytic-sector resonance is a deterministic component-square input; it is not a production noisy-bulk eigensolver or a noisy-cloud theorem.",
            "The all-column and production matrix audits are binary64 diagnostics; production RH-50 values also use probes and a finite horizon.",
            "Arb validates scalar exponent arithmetic only, not a production transfer-operator eigensolver.",
            "The mixed overlap criterion is sufficient and remains unproved uniformly over the dyadic small-noise family.",
            "Stage A1 and unconditional Stage A4 remain open.",
            "No arithmetic trace formula, prime-power identity, zeta-zero spectral identity, self-adjoint Hilbert--Polya operator, T log T law, Riemann-hypothesis conclusion, or TPC twin-prime conclusion is claimed.",
        ],
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
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
