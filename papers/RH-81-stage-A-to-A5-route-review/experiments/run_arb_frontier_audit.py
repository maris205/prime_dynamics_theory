"""Arb audit of the numerical margins defining the RH-81 route verdict."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
FULL_OUTPUT = ROOT / "results" / "arb_frontier_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "arb_frontier_smoke.json"
PRECISION_BITS = 256


def summary(number: int, directory: str) -> dict:
    path = PAPERS / directory / "results" / "summary.json"
    return json.loads(path.read_text(encoding="utf-8"))


def exact_float(value: float) -> arb:
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
    rh74 = summary(74, "RH-74-validated-upstream-hardy-bridge")
    rh77 = summary(77, "RH-77-postblock-effective-rank-compression")
    rh79 = summary(79, "RH-79-intrinsic-determinant-diagonal-transfer")
    rh80 = summary(80, "RH-80-moving-cloud-relative-determinant")
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    try:
        bridge_ratio = exact_float(rh74["audit"]["maximum_bridge_to_slack_ratio"])
        bridge_remaining = arb(1) - bridge_ratio
        rank2_excess = exact_float(rh77["audit"]["minimum_rank2_capture"]) - arb("0.99")
        rank4_excess = exact_float(rh77["audit"]["minimum_rank4_capture"]) - arb("0.999999")
        shrinking_factor = exact_float(rh79["audit"]["initial_shrinking_disk_error"]) / exact_float(rh79["audit"]["final_shrinking_disk_error"])
        fixed_reversal = exact_float(rh79["audit"]["final_fixed_disk_error"]) / exact_float(rh79["audit"]["minimum_fixed_disk_error"])
        pole_contrast = exact_float(rh80["audit"]["degree_64_q_105_growth_lower"]) / exact_float(rh80["audit"]["degree_64_radius_08_error_upper"])
        rows = [
            {"metric": "finite_chain_slack_fraction_remaining", "ball": str(bridge_remaining), "certified_lower": lower(bridge_remaining), "gate": lower(bridge_remaining) > 0.99},
            {"metric": "rank2_capture_excess_over_99_percent", "ball": str(rank2_excess), "certified_lower": lower(rank2_excess), "gate": lower(rank2_excess) > 0.0},
            {"metric": "rank4_capture_excess_over_99_9999_percent", "ball": str(rank4_excess), "certified_lower": lower(rank4_excess), "gate": lower(rank4_excess) > 0.0},
            {"metric": "shrinking_disk_error_improvement_factor", "ball": str(shrinking_factor), "certified_lower": lower(shrinking_factor), "gate": lower(shrinking_factor) > 100.0},
            {"metric": "fixed_disk_reversal_factor", "ball": str(fixed_reversal), "certified_lower": lower(fixed_reversal), "gate": lower(fixed_reversal) > 10.0},
            {"metric": "fixed_pole_inside_outside_contrast", "ball": str(pole_contrast), "certified_lower": lower(pole_contrast), "gate": lower(pole_contrast) > 1e8},
        ]
    finally:
        ctx.prec = previous_precision
    if args.smoke:
        rows = rows[:2]
    payload = {
        "status": "rh81_arb_route_frontier_margin_audit",
        "precision_bits": PRECISION_BITS,
        "rows": rows,
        "all_executed_margin_gates_green": all(row["gate"] for row in rows),
        "scope": "These margins certify the archived finite-scale and model-route verdicts; they do not prove either open all-level corridor or the A5 cloud-complement theorem.",
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "row_count": len(rows), "all_green": payload["all_executed_margin_gates_green"]}, sort_keys=True))


if __name__ == "__main__":
    main()

