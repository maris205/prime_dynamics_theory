"""256-bit Arb/Acb audit of the finite Fourier-ring obstruction."""

from __future__ import annotations

import json
from pathlib import Path

from flint import acb, arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_fourier_ring_audit.json"
DIMENSION = 8
HORIZON = 4
DEPTH = 4


def real_contains_zero(value: arb) -> bool:
    return float(value.lower()) <= 0.0 <= float(value.upper())


def complex_contains_zero(value: acb) -> bool:
    return real_contains_zero(value.real) and real_contains_zero(value.imag)


def fourier_inner(power_difference: int) -> acb:
    total = acb(0)
    for index in range(DIMENSION):
        angle = 2 * arb.pi() * index * power_difference / DIMENSION
        total += acb(angle.cos(), angle.sin())
    return total / DIMENSION


def main() -> None:
    ctx.prec = 256
    diagonal = fourier_inner(0)
    off_diagonal = [fourier_inner(value) for value in range(1, DIMENSION)]
    target_correlations = [
        fourier_inner(HORIZON - power) for power in range(DEPTH)
    ]
    contraction = arb("0.99")
    metric_scalar = 1 / (1 - contraction * contraction)
    payload = {
        "status": "arb_exact_fourier_ring_block_depth_audit",
        "evidence_level": (
            "256-bit Arb/Acb certification of the displayed finite DFT "
            "orthogonality witness; not a production phase audit"
        ),
        "precision_bits": 256,
        "dimension": DIMENSION,
        "horizon": HORIZON,
        "depth": DEPTH,
        "diagonal_inner_product_ball": str(diagonal),
        "off_diagonal_inner_product_balls": [
            str(value) for value in off_diagonal
        ],
        "target_correlation_balls": [
            str(value) for value in target_correlations
        ],
        "contraction_ball": str(contraction),
        "canonical_metric_scalar_ball": str(metric_scalar),
        "unit_norm_certified": (
            float(diagonal.real.lower()) > 0.999
            and float(diagonal.real.upper()) < 1.001
            and real_contains_zero(diagonal.imag)
        ),
        "all_distinct_fourier_vectors_orthogonal_certified": all(
            complex_contains_zero(value) for value in off_diagonal
        ),
        "target_orthogonal_to_depth_space_certified": all(
            complex_contains_zero(value) for value in target_correlations
        ),
        "strict_stability_and_positive_metric_certified": (
            float(contraction.lower()) > 0.0
            and float(contraction.upper()) < 1.0
            and float(metric_scalar.lower()) > 0.0
        ),
        "production_interval_audit_executed": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
