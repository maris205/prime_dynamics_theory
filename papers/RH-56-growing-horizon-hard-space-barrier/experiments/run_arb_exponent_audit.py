"""Outward-rounded audit of the RH-56 scalar exponent ledger."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_hardy_barrier_ledger.json"


def main() -> None:
    ctx.prec = 256
    radius = arb("0.85")
    lam = arb("1.678573510428322 +/- 5e-16")
    edge = 1 / lam.sqrt()
    entrance_per_side = arb(1)
    total_entrance = 2 * entrance_per_side
    budget = arb("0.25")
    threshold = radius ** (total_entrance / budget)
    edge_single = (
        entrance_per_side * (1 / radius).log() / (1 / edge).log()
    )
    edge_total = 2 * edge_single
    edge_radial_clock = 1 / (1 - (edge / radius) ** 2).sqrt()
    payload = {
        "status": "arb_outward_rounded_hardy_barrier_exponent_ledger",
        "evidence_level": (
            "256-bit Arb evaluation of exact scalar formulas; no transfer "
            "operator or intrinsic eigensolver is enclosed"
        ),
        "precision_bits": 256,
        "hardy_radius_ball": str(radius),
        "lambda_ball": str(lam),
        "edge_radius_ball": str(edge),
        "common_rate_threshold_ball": str(threshold),
        "edge_single_side_power_ball": str(edge_single),
        "edge_two_side_total_power_ball": str(edge_total),
        "edge_radial_hardy_clock_ball": str(edge_radial_clock),
        "threshold_below_point_two_eight_certified": (
            float(threshold.upper()) < 0.28
        ),
        "edge_total_exceeds_quarter_certified": (
            float(edge_total.lower()) > 0.25
        ),
        "production_operator_interval_eigensolver_executed": False,
        "arithmetic_scope": (
            "Only the exponent and radial-clock formulas are interval "
            "evaluated. The analytic theorem is symbolic."
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
