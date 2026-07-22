"""Arb audit of square and shrinking/fixed-disk determinant transfer."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH78 = PAPERS / "RH-78-two-corridor-stage-A1-composition"
FULL_OUTPUT = ROOT / "results" / "determinant_transfer_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "determinant_transfer_smoke.json"
PRECISION_BITS = 256
BULK_HS_CONSTANT = 1.55
FIXED_DISK_RADIUS = 0.01
SHRINKING_DISK_MULTIPLE = 0.01


def exact_arb_float(value: float) -> arb:
    numerator, denominator = float(value).as_integer_ratio()
    return arb(numerator) / denominator


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def determinant_upper(radius: arb, epsilon: arb, bulk: arb) -> arb:
    square = epsilon * (arb(2) * bulk + epsilon)
    return radius * square * (arb(1) + radius * bulk**2 + radius * (bulk + epsilon) ** 2).exp()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    inherited = json.loads((RH78 / "results" / "stage_composition_audit.json").read_text(encoding="utf-8"))
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows = []
    try:
        input_rows = inherited["rows"][:1] if args.smoke else inherited["rows"]
        for row in input_rows:
            sigma = exact_arb_float(float(row["sigma"]))
            epsilon = arb(row["identification_stress_envelope_ball"])
            bulk = exact_arb_float(BULK_HS_CONSTANT) / sigma.sqrt()
            square = epsilon * (arb(2) * bulk + epsilon)
            fixed_radius = exact_arb_float(FIXED_DISK_RADIUS)
            shrinking_radius = exact_arb_float(SHRINKING_DISK_MULTIPLE) * sigma
            fixed = determinant_upper(fixed_radius, epsilon, bulk)
            shrinking = determinant_upper(shrinking_radius, epsilon, bulk)
            record = {
                "level": row["level"],
                "sigma": row["sigma"],
                "conditional_intrinsic_hs_error_ball": str(epsilon),
                "conditional_intrinsic_hs_error_upper": upper(epsilon),
                "bulk_hs_upper_ball": str(bulk),
                "square_trace_error_ball": str(square),
                "square_trace_error_upper": upper(square),
                "fixed_disk_radius": FIXED_DISK_RADIUS,
                "fixed_disk_determinant_error_ball": str(fixed),
                "fixed_disk_determinant_error_upper": upper(fixed),
                "shrinking_disk_radius_ball": str(shrinking_radius),
                "shrinking_disk_determinant_error_ball": str(shrinking),
                "shrinking_disk_determinant_error_upper": upper(shrinking),
            }
            rows.append(record)
            print(json.dumps({"level": record["level"], "sigma": record["sigma"], "square_error": record["square_trace_error_upper"], "fixed_disk": record["fixed_disk_determinant_error_upper"], "shrinking_disk": record["shrinking_disk_determinant_error_upper"]}, sort_keys=True), flush=True)
    finally:
        ctx.prec = previous_precision
    shrinking_values = [row["shrinking_disk_determinant_error_upper"] for row in rows]
    fixed_values = [row["fixed_disk_determinant_error_upper"] for row in rows]
    payload = {
        "status": "rh79_intrinsic_determinant_diagonal_transfer",
        "precision_bits": PRECISION_BITS,
        "constants": {"bulk_hs_constant": BULK_HS_CONSTANT, "fixed_disk_radius": FIXED_DISK_RADIUS, "shrinking_disk_multiple": SHRINKING_DISK_MULTIPLE},
        "rows": rows,
        "all_executed_shrinking_disk_gates_green": all(right < left for left, right in zip(shrinking_values, shrinking_values[1:])),
        "fixed_disk_standard_bound_eventually_worsens": len(fixed_values) < 2 or fixed_values[-1] > min(fixed_values),
        "theorem_boundary": {
            "intrinsic_square_trace_transfer": True,
            "shrinking_disk_determinant_transfer": True,
            "strict_mesh_diagonal_limit_interchange": True,
            "fixed_disk_standard_continuity_sufficient": False,
            "pole_renormalized_limit_closed": False,
            "stage_A5_closed": False,
        },
        "route_consequence": (
            "Conditional Stage-A identification is strong enough to transfer bulk squares "
            "in trace norm and determinants on disks |w|=O(sigma). The standard determinant "
            "continuity bound is not uniform on a fixed disk because the bulk trace norm is "
            "O(sigma^-1), producing exp(O(R/sigma)). Entry to A5 therefore requires pole "
            "renormalization or a sharper relative determinant argument, not merely stronger "
            "finite-dimensional precision."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "row_count": len(rows), "shrinking_green": payload["all_executed_shrinking_disk_gates_green"]}, sort_keys=True))


if __name__ == "__main__":
    main()
