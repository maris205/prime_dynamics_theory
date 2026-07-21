"""256-bit Arb audit of the two-block Hardy Gram identities.

This is an exact scalar/block model check.  It does not enclose a production
folded-Gaussian eigenspace or Riesz projector.
"""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_block_audit.json"


def main() -> None:
    ctx.prec = 256
    mu1 = arb("0.72")
    mu2 = arb("-0.61")
    radius = arb(1)
    z1 = arb("0.37")
    z2 = arb("-0.29")

    k11 = z1 * z1 / (1 - mu1 * mu1)
    k22 = z2 * z2 / (1 - mu2 * mu2)
    k12 = z1 * z2 / (1 - mu1 * mu2)
    exact_squared = k11 + k22 + 2 * k12
    square_sum_squared = k11 + k22
    signed_fusion_ratio = exact_squared / square_sum_squared
    correlation = k12 / (k11 * k22).sqrt()
    coherence_constant = 1 + abs(correlation)
    coherence_squared = coherence_constant * square_sum_squared
    absolute_upper = k11.sqrt() + k22.sqrt()

    # For a real 2-by-2 correlation matrix, the largest eigenvalue is
    # exactly 1+|c|.  The same value is the Gershgorin row-sum bound.
    payload = {
        "status": "arb_two_block_hardy_cross_stein_identity_audit",
        "evidence_level": (
            "256-bit Arb evaluation of a two-mode exact Cauchy/Gram model; "
            "no production interval eigensolver"
        ),
        "precision_bits": 256,
        "radius_ball": str(radius),
        "modal_values": [str(mu1), str(mu2)],
        "channel_overlaps": [str(z1), str(z2)],
        "gram_entries": {
            "k11": str(k11),
            "k12": str(k12),
            "k22": str(k22),
        },
        "exact_energy_squared_ball": str(exact_squared),
        "square_sum_energy_squared_ball": str(square_sum_squared),
        "signed_fusion_ratio_ball": str(signed_fusion_ratio),
        "normalized_correlation_ball": str(correlation),
        "coherence_constant_ball": str(coherence_constant),
        "coherence_upper_squared_ball": str(coherence_squared),
        "absolute_block_upper_ball": str(absolute_upper),
        "gram_determinant_ball": str(k11 * k22 - k12 * k12),
        "gram_positive_certified": float(k11.lower()) > 0
        and float(k22.lower()) > 0
        and float((k11 * k22 - k12 * k12).lower()) > 0,
        "coherence_bound_certified": float(exact_squared.upper())
        <= float(coherence_squared.upper()),
        "absolute_triangle_bound_certified": float(exact_squared.upper())
        <= float((absolute_upper * absolute_upper).upper()),
        "production_interval_riesz_projector_executed": False,
        "arithmetic_scope": (
            "The certificate validates the scalar geometric-series kernel, "
            "positive Gram reconstruction, and the two-block coherence "
            "inequality only."
        ),
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
