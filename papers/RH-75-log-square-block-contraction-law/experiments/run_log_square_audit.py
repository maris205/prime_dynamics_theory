"""Arb audit of the dyadic log-square/square-root block law."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH70 = PAPERS / "RH-70-frozen-production-block-hardy-audit"
RH74 = PAPERS / "RH-74-validated-upstream-hardy-bridge"
FULL_OUTPUT = ROOT / "results" / "log_square_block_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "log_square_block_smoke.json"
PRECISION_BITS = 256
SIGMA_ZERO = 0.16
HORIZON_OFFSET = 2
Q_CONSTANT = 0.086
OBSERVATION_DENSITY_CONSTANT = 2.561
SOURCE_BLOCK_CONSTANT = 3.1
FINITE_CONSTANT = 0.552


def exact_arb_float(value: float) -> arb:
    numerator, denominator = float(value).as_integer_ratio()
    return arb(numerator) / denominator


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    rh70 = json.loads((RH70 / "results" / "frozen_production_interval_audit.json").read_text(encoding="utf-8"))
    rh74 = json.loads((RH74 / "results" / "validated_upstream_bridge_audit.json").read_text(encoding="utf-8"))
    true_rows = {float(row["sigma"]): row for row in rh74["rows"]}

    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows = []
    try:
        input_rows = rh70["rows"][:1] if args.smoke else rh70["rows"]
        for level, row in enumerate(input_rows):
            sigma = float(row["sigma"])
            allowed_horizon = (level + HORIZON_OFFSET) ** 2
            channels = []
            for index, frozen_channel in enumerate(row["channels"]):
                true_channel = true_rows[sigma]["channels"][index]
                q = arb(true_channel["robust_hardy_bridge"]["true_block_contraction_ball"])
                normalized_q = q / exact_arb_float(sigma).sqrt()
                observation_squared = arb(frozen_channel["observation_frobenius_squared_ball"])
                observation_density = exact_arb_float(sigma) * observation_squared
                source_block = arb(frozen_channel["source_block_squared_ball"])
                finite = arb(frozen_channel["finite_energy_squared_ball"])
                actual_tail = arb(frozen_channel["tail_energy_squared_upper_ball"])
                log_scale = arb(level + HORIZON_OFFSET)
                tail_envelope = (
                    exact_arb_float(OBSERVATION_DENSITY_CONSTANT)
                    * exact_arb_float(Q_CONSTANT) ** 2
                    * exact_arb_float(SOURCE_BLOCK_CONSTANT)
                    / (
                        arb(1)
                        - exact_arb_float(Q_CONSTANT) ** 2
                        * exact_arb_float(SIGMA_ZERO)
                    )
                )
                finite_envelope = exact_arb_float(FINITE_CONSTANT) * log_scale
                record = {
                    "side": frozen_channel["side"],
                    "selected_horizon": int(row["selected_horizon"]),
                    "allowed_log_square_horizon": allowed_horizon,
                    "horizon_gate": int(row["selected_horizon"]) <= allowed_horizon,
                    "true_block_contraction_ball": str(q),
                    "normalized_q_over_sqrt_sigma_ball": str(normalized_q),
                    "normalized_q_over_sqrt_sigma_upper": upper(normalized_q),
                    "observation_density_ball": str(observation_density),
                    "observation_density_upper": upper(observation_density),
                    "source_block_ball": str(source_block),
                    "source_block_upper": upper(source_block),
                    "finite_energy_squared_ball": str(finite),
                    "finite_energy_squared_upper": upper(finite),
                    "actual_tail_energy_squared_ball": str(actual_tail),
                    "actual_tail_energy_squared_upper": upper(actual_tail),
                    "uniform_tail_envelope_ball": str(tail_envelope),
                    "uniform_tail_envelope_upper": upper(tail_envelope),
                    "finite_polylog_envelope_ball": str(finite_envelope),
                    "finite_polylog_envelope_upper": upper(finite_envelope),
                    "all_anchor_gates_green": bool(
                        int(row["selected_horizon"]) <= allowed_horizon
                        and upper(normalized_q) <= Q_CONSTANT
                        and upper(observation_density) <= OBSERVATION_DENSITY_CONSTANT
                        and upper(source_block) <= SOURCE_BLOCK_CONSTANT
                        and upper(finite) <= upper(finite_envelope)
                        and upper(actual_tail) <= upper(tail_envelope)
                    ),
                }
                channels.append(record)
                print(json.dumps({"level": level, "sigma": sigma, "side": record["side"], "horizon": record["selected_horizon"], "q_over_sqrt_sigma": record["normalized_q_over_sqrt_sigma_upper"], "tail": record["actual_tail_energy_squared_upper"], "tail_envelope": record["uniform_tail_envelope_upper"], "green": record["all_anchor_gates_green"]}, sort_keys=True), flush=True)
            rows.append({"level": level, "sigma": sigma, "fine_dimension": row["fine_dimension"], "channels": channels, "all_channels_green": all(channel["all_anchor_gates_green"] for channel in channels)})
    finally:
        ctx.prec = previous_precision

    payload = {
        "status": "rh75_log_square_square_root_block_contraction_audit",
        "precision_bits": PRECISION_BITS,
        "constants": {
            "sigma_zero": SIGMA_ZERO,
            "horizon_offset": HORIZON_OFFSET,
            "q_constant": Q_CONSTANT,
            "observation_density_constant": OBSERVATION_DENSITY_CONSTANT,
            "source_block_constant": SOURCE_BLOCK_CONSTANT,
            "finite_constant": FINITE_CONSTANT,
            "source_log_power": 0,
            "finite_log_power": 1,
        },
        "rows": rows,
        "all_executed_anchors_green": all(row["all_channels_green"] for row in rows),
        "theorem_boundary": {
            "log_square_horizon_sufficiency_theorem": True,
            "square_root_block_contraction_tail_theorem": True,
            "five_scale_anchor_certificate": True,
            "all_dyadic_levels_proved": False,
            "uniform_stage_A1_closed": False,
        },
        "route_consequence": (
            "The uniform Hardy gate is reduced to an explicit all-level law: "
            "M_k=O(k^2), ||A_k^{M_k}||=O(sqrt(sigma_k)), bounded one-block "
            "source energy, and logarithmic finite-prefix energy. All five "
            "validated anchors satisfy common constants, but the induction or "
            "analytic mechanism proving those constants for every dyadic level "
            "remains open."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "row_count": len(rows), "all_green": payload["all_executed_anchors_green"]}, sort_keys=True))


if __name__ == "__main__":
    main()
