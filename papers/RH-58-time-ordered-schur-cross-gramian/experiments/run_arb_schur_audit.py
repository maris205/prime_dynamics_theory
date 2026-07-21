"""256-bit Arb audit of a two-block time-ordered Schur recursion."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_schur_audit.json"


def contains_zero(value: arb) -> bool:
    return float(value.lower()) <= 0.0 <= float(value.upper())


def main() -> None:
    ctx.prec = 256
    a = arb("0.2")
    b = arb("0.7")
    coupling = arb("0.3")
    x1 = arb("0.5")
    x2 = arb("0.4")
    y1 = arb("0.8")
    y2 = arb("0.6")

    g22 = x2 * x2 / (1 - b * b)
    g12 = (x1 * x2 + coupling * b * g22) / (1 - a * b)
    g11 = (
        x1 * x1
        + 2 * a * coupling * g12
        + coupling * coupling * g22
    ) / (1 - a * a)

    o11 = y1 * y1 / (1 - a * a)
    o12 = (y1 * y2 + a * coupling * o11) / (1 - a * b)
    o22 = (
        y2 * y2
        + coupling * coupling * o11
        + 2 * b * coupling * o12
    ) / (1 - b * b)

    controllability_residuals = (
        g11 - (a * a * g11 + 2 * a * coupling * g12 + coupling**2 * g22) - x1**2,
        g12 - (a * b * g12 + coupling * b * g22) - x1 * x2,
        g22 - b * b * g22 - x2 * x2,
    )
    observability_residuals = (
        o11 - a * a * o11 - y1 * y1,
        o12 - (a * b * o12 + a * coupling * o11) - y1 * y2,
        o22
        - (b * b * o22 + 2 * b * coupling * o12 + coupling**2 * o11)
        - y2 * y2,
    )

    primal_energy_squared = (
        y1 * y1 * g11 + 2 * y1 * y2 * g12 + y2 * y2 * g22
    )
    dual_energy_squared = (
        x1 * x1 * o11 + 2 * x1 * x2 * o12 + x2 * x2 * o22
    )
    state_packet_sum = primal_energy_squared
    source_packet_sum = dual_energy_squared

    horizon = 2
    gain11 = (1 + a * a) / (1 - a**4)
    gain12 = (1 + a * b) / (1 - a**2 * b**2)
    gain22 = (1 + b * b) / (1 - b**4)
    gamma22 = gain22 * x2 * x2
    gamma12 = gain12 * (x1 * x2 + coupling * gamma22 * b)
    gamma11 = gain11 * (
        x1 * x1
        + 2 * a * coupling * gamma12
        + coupling * coupling * gamma22
    )
    path_energy_squared = (
        y1 * y1 * gamma11
        + 2 * y1 * y2 * gamma12
        + y2 * y2 * gamma22
    )

    payload = {
        "status": "arb_two_block_time_ordered_schur_cross_stein_audit",
        "evidence_level": (
            "256-bit Arb evaluation of an exact two-scalar-block Schur "
            "recursion and block-power majorant; no production interval Schur form"
        ),
        "precision_bits": 256,
        "model": {
            "diagonal_blocks": [str(a), str(b)],
            "upper_coupling": str(coupling),
            "source": [str(x1), str(x2)],
            "observation": [str(y1), str(y2)],
            "block_horizon": horizon,
        },
        "controllability_blocks": {
            "g11": str(g11),
            "g12": str(g12),
            "g22": str(g22),
        },
        "observability_blocks": {
            "o11": str(o11),
            "o12": str(o12),
            "o22": str(o22),
        },
        "controllability_residual_balls": [
            str(value) for value in controllability_residuals
        ],
        "observability_residual_balls": [
            str(value) for value in observability_residuals
        ],
        "primal_energy_squared_ball": str(primal_energy_squared),
        "dual_energy_squared_ball": str(dual_energy_squared),
        "state_packet_sum_ball": str(state_packet_sum),
        "source_packet_sum_ball": str(source_packet_sum),
        "block_stein_gains": {
            "gain11": str(gain11),
            "gain12": str(gain12),
            "gain22": str(gain22),
        },
        "scalar_path_energy_squared_upper_ball": str(path_energy_squared),
        "all_recursion_residuals_contain_zero": all(
            contains_zero(value)
            for value in controllability_residuals + observability_residuals
        ),
        "primal_dual_identity_certified": (
            float((primal_energy_squared - dual_energy_squared).lower()) <= 0.0
            <= float((primal_energy_squared - dual_energy_squared).upper())
        ),
        "path_majorant_certified": float(path_energy_squared.lower())
        >= float(primal_energy_squared.upper()),
        "production_interval_schur_executed": False,
        "arithmetic_scope": (
            "Only a two-scalar-block exact model is interval evaluated. "
            "The folded-Gaussian Schur packets remain binary64 diagnostics."
        ),
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
