"""Build 256-bit Arb cutoff uppers on all RH-50 production scales."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_production_cutoff_ledger.json"
SCALES = (
    (0.01, 2048),
    (0.004, 5120),
    (0.002, 10240),
    (0.001, 20480),
    (0.0005, 40960),
)


def upper_float(value: arb) -> float:
    return float(np.nextafter(float(value.upper()), np.inf))


def arb_cutoff_bound(sigma_string: str, dimension: int, multiple: float):
    n = int(dimension)
    h = arb(1) / n
    sigma = arb(sigma_string)
    declared = arb(str(multiple))
    half_width = int(math.ceil(float(multiple) * float(sigma_string) * n)) + 2
    effective = arb(half_width) * h / sigma
    exp_half = (-(effective * effective) / 2).exp()
    omitted_mass = (
        2
        * arb(1).exp().sqrt()
        * exp_half
        * (h + sigma / effective)
        / (sigma - h)
    )
    alpha = omitted_mass / (1 - omitted_mass)
    omitted_square = (
        4
        * arb(1).exp()
        * exp_half
        * exp_half
        * (h + sigma / (2 * effective))
        / (sigma - h) ** 2
    )
    renormalization_square = (
        arb(1).exp()
        * alpha
        * alpha
        * (4 * h + 2 * arb.pi().sqrt() * sigma)
        / (sigma - h) ** 2
    )
    two_norm = (omitted_square + renormalization_square).sqrt()
    return {
        "sigma": float(sigma_string),
        "dimension": n,
        "declared_multiple": float(multiple),
        "support_half_width": half_width,
        "effective_multiple_upper": upper_float(effective),
        "omitted_mass_upper": upper_float(omitted_mass),
        "two_norm_upper": upper_float(two_norm),
        "arb_two_norm_ball": str(two_norm),
    }


def main() -> None:
    previous = ctx.prec
    ctx.prec = 256
    try:
        rows = []
        for sigma, dimension in SCALES:
            sigma_string = format(sigma, ".10g")
            adaptive_multiple = max(5.0, 2.0 * math.sqrt(math.log(dimension)))
            rows.append(
                {
                    "sigma": sigma,
                    "dimension": dimension,
                    "fixed_eight": arb_cutoff_bound(
                        sigma_string, dimension, 8.0
                    ),
                    "adaptive": arb_cutoff_bound(
                        sigma_string, dimension, adaptive_multiple
                    ),
                }
            )
    finally:
        ctx.prec = previous
    payload = {
        "status": "arb_256_production_scale_exact_real_cutoff_uppers",
        "evidence_level": "256-bit Arb interval evaluation of RH-39 formulas",
        "precision_bits": 256,
        "rows": rows,
        "largest_dimension": max(row["dimension"] for row in rows),
        "maximum_fixed_eight_two_norm_upper": max(
            row["fixed_eight"]["two_norm_upper"] for row in rows
        ),
        "all_fixed_eight_above_adaptive_requirement": all(
            row["adaptive"]["declared_multiple"] <= 8.0 for row in rows
        ),
        "scope": (
            "exact-real Markov matrix cutoff only; intrinsic factors, normalized "
            "sources, and directional Hardy traces are not enclosed by this ledger"
        ),
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
