"""256-bit Arb audit of a two-block flag-metric Stein certificate."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_flag_metric_audit.json"


def contains_zero(value: arb) -> bool:
    return float(value.lower()) <= 0.0 <= float(value.upper())


def lower_nonnegative(value: arb) -> bool:
    return float(value.lower()) >= 0.0


def main() -> None:
    ctx.prec = 256
    a = arb("0.2")
    b = arb("0.7")
    coupling = arb("0.3")
    source_outer = arb("0.4")
    y1 = arb("0.8")
    y2 = arb("0.6")
    scale1 = arb("0.25")
    scale2 = arb(1)

    h1 = 1 / (1 - a * a)
    h2 = 1 / (1 - b * b)
    p1 = scale1 * scale1 * h1
    p2 = scale2 * scale2 * h2

    r11 = p1 * (1 - a * a)
    r12 = -p1 * a * coupling
    r22 = p2 * (1 - b * b) - p1 * coupling * coupling
    determinant = r11 * r22 - r12 * r12
    sharp_kappa = (
        y1 * y1 * r22
        - 2 * y1 * y2 * r12
        + y2 * y2 * r11
    ) / determinant
    kappa_safety_factor = arb("1.000001")
    kappa = kappa_safety_factor * sharp_kappa

    supersolution11 = kappa * r11 - y1 * y1
    supersolution12 = kappa * r12 - y1 * y2
    supersolution22 = kappa * r22 - y2 * y2
    supersolution_determinant = (
        supersolution11 * supersolution22 - supersolution12**2
    )

    o11 = y1 * y1 / (1 - a * a)
    o12 = (y1 * y2 + a * coupling * o11) / (1 - a * b)
    o22 = (
        y2 * y2
        + coupling * coupling * o11
        + 2 * b * coupling * o12
    ) / (1 - b * b)
    exact_outer_energy_squared = source_outer**2 * o22
    metric_outer_upper_squared = kappa * p2 * source_outer**2
    gap = metric_outer_upper_squared - exact_outer_energy_squared

    local_residuals = (
        h1 - a * a * h1 - 1,
        h2 - b * b * h2 - 1,
    )
    payload = {
        "status": "arb_two_block_flag_metric_stein_audit",
        "evidence_level": (
            "256-bit Arb evaluation of a two-scalar-block flag metric, "
            "exact dissipation, and packetwise Stein supersolution; no "
            "production interval Schur metric"
        ),
        "precision_bits": 256,
        "model": {
            "diagonal_blocks": [str(a), str(b)],
            "upper_coupling": str(coupling),
            "outer_packet_source": str(source_outer),
            "observation": [str(y1), str(y2)],
            "scales": [str(scale1), str(scale2)],
        },
        "local_metrics": [str(h1), str(h2)],
        "local_lyapunov_residual_balls": [
            str(value) for value in local_residuals
        ],
        "dissipation": {
            "r11": str(r11),
            "r12": str(r12),
            "r22": str(r22),
            "determinant": str(determinant),
        },
        "sharp_kappa_ball": str(sharp_kappa),
        "kappa_safety_factor": str(kappa_safety_factor),
        "certified_kappa_ball": str(kappa),
        "supersolution_residual": {
            "s11": str(supersolution11),
            "s12": str(supersolution12),
            "s22": str(supersolution22),
            "determinant": str(supersolution_determinant),
        },
        "exact_outer_packet_energy_squared_ball": str(
            exact_outer_energy_squared
        ),
        "metric_outer_upper_squared_ball": str(metric_outer_upper_squared),
        "upper_minus_exact_gap_ball": str(gap),
        "local_lyapunov_identities_certified": all(
            contains_zero(value) for value in local_residuals
        ),
        "dissipation_positive_definite_certified": (
            lower_nonnegative(r11)
            and lower_nonnegative(r22)
            and float(determinant.lower()) > 0.0
        ),
        "supersolution_positive_semidefinite_certified": (
            lower_nonnegative(supersolution11)
            and lower_nonnegative(supersolution22)
            and float(supersolution_determinant.lower()) > 0.0
        ),
        "packet_upper_certified": float(gap.lower()) > 0.0,
        "production_interval_schur_metric_executed": False,
        "arithmetic_scope": (
            "Only the displayed two-scalar-block model is interval "
            "evaluated. The folded-Gaussian flag metrics remain binary64 "
            "diagnostics."
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
