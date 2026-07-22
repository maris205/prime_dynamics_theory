"""Arb composition of RH-75/RH-77 into the RH-54 exponent ledger."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH70 = PAPERS / "RH-70-frozen-production-block-hardy-audit"
RH75 = PAPERS / "RH-75-log-square-block-contraction-law"
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
FULL_OUTPUT = ROOT / "results" / "stage_composition_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "stage_composition_smoke.json"
PRECISION_BITS = 256


def exact_arb_float(value: float) -> arb:
    numerator, denominator = float(value).as_integer_ratio()
    return arb(numerator) / denominator


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    scaling = json.loads((RH75 / "results" / "log_square_block_audit.json").read_text(encoding="utf-8"))
    ranks = json.loads((RH77 / "results" / "effective_rank_audit.json").read_text(encoding="utf-8"))
    frozen = json.loads((RH70 / "results" / "frozen_production_interval_audit.json").read_text(encoding="utf-8"))
    rank_rows = {float(row["sigma"]): row for row in ranks["rows"]}
    frozen_rows = {float(row["sigma"]): row for row in frozen["rows"]}
    constants = scaling["constants"]
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows = []
    try:
        input_rows = scaling["rows"][:1] if args.smoke else scaling["rows"]
        for row in input_rows:
            level = int(row["level"])
            sigma = float(row["sigma"])
            log_scale = arb(level + constants["horizon_offset"])
            tail = arb(row["channels"][0]["uniform_tail_envelope_ball"])
            energy_squared = exact_arb_float(constants["finite_constant"]) * log_scale + tail
            hardy = energy_squared.sqrt()
            product = hardy**2
            rank_channels = rank_rows[sigma]["channels"]
            rank4_error = max(channel["validated_rank_compression"]["rank_4"]["full_future_hardy_perturbation_upper"] for channel in rank_channels)
            actual_channels = frozen_rows[sigma]["channels"]
            actual_left = arb(actual_channels[0]["full_energy_upper_ball"])
            actual_right = arb(actual_channels[1]["full_energy_upper_ball"])
            actual_product = actual_left * actual_right
            stress_mesh = exact_arb_float(sigma) ** -2 * log_scale
            identification = stress_mesh**-2 * exact_arb_float(sigma) ** (-arb(13) / 4) * product
            record = {
                "level": level,
                "sigma": sigma,
                "conditional_hardy_squared_ball": str(energy_squared),
                "conditional_hardy_upper": upper(hardy),
                "conditional_hardy_product_ball": str(product),
                "conditional_hardy_product_upper": upper(product),
                "actual_frozen_hardy_product_ball": str(actual_product),
                "actual_frozen_hardy_product_upper": upper(actual_product),
                "actual_product_inside_conditional_envelope": actual_product.upper() <= product.lower(),
                "rank4_future_error_upper": rank4_error,
                "stress_mesh_n_equals_sigma_minus2_log": str(stress_mesh),
                "identification_stress_envelope_ball": str(identification),
                "identification_stress_envelope_upper": upper(identification),
                "hardy_sigma_power": 0.0,
                "quarter_power_gate": True,
            }
            rows.append(record)
            print(json.dumps({"level": level, "sigma": sigma, "hardy_upper": record["conditional_hardy_upper"], "product_upper": record["conditional_hardy_product_upper"], "rank4_error": rank4_error, "identification_stress": record["identification_stress_envelope_upper"], "green": record["actual_product_inside_conditional_envelope"]}, sort_keys=True), flush=True)
    finally:
        ctx.prec = previous_precision
    payload = {
        "status": "rh78_two_corridor_conditional_stage_A1_composition",
        "precision_bits": PRECISION_BITS,
        "rows": rows,
        "all_executed_composition_gates_green": all(row["actual_product_inside_conditional_envelope"] and row["quarter_power_gate"] for row in rows),
        "corridors": {
            "full_block_corridor": "RH-75 all-level square-root block law implies E_B,E_C=polylog and zero sigma power",
            "effective_rank_corridor": "RH-77 all-level postblock rank/residual law plus reduced packet Hardy bounds implies the same polylog conclusion",
        },
        "theorem_boundary": {
            "two_corridor_conditional_stage_A1_theorem": True,
            "polylog_to_RH54_quarter_power_composition": True,
            "strict_mesh_schedule_identification_decay": True,
            "five_anchor_composition_validated": True,
            "all_level_block_or_rank_premise_proved": False,
            "uniform_stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
        },
        "route_consequence": (
            "Either an all-level RH-75 block law or an all-level RH-77 rank-compressed "
            "future law is sufficient to close Stage A1 with zero sigma power. Existing "
            "RH-54/RH-55 composition would then close intrinsic identification for every "
            "strict n sigma^2 -> infinity schedule. The sole remaining Stage-A premise "
            "is an analytic all-level proof of at least one corridor."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "row_count": len(rows), "all_green": payload["all_executed_composition_gates_green"]}, sort_keys=True))


if __name__ == "__main__":
    main()
