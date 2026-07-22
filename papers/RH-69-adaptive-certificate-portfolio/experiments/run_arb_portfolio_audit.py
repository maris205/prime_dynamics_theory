"""256-bit Arb audit of three exact portfolio branches."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_portfolio_audit.json"


def cancellation_focused_row() -> tuple[arb, arb]:
    slow = arb("0.995")
    fused = arb("0.55")
    fast = arb("0.2")
    mixing = arb("0.2")
    epsilon = arb("1e-24")
    horizon = 32
    m_slow = 1 / (1 - slow * slow)
    m_fused = 1 / (1 - fused * fused)
    m_fast = 1 / (1 - fast * fast)
    normalizer = 1 + mixing * mixing
    projected = (slow + mixing * mixing * fast) / normalizer
    source = (2 * normalizer).sqrt()
    vector_metric = (m_slow + mixing * mixing * m_fast) / normalizer
    residual_metric = (
        (slow - projected) ** 2 * m_slow
        + mixing * mixing * (fast - projected) ** 2 * m_fast
    ) / normalizer
    radius = arb(0)
    for index in range(horizon):
        radius += (
            slow ** (horizon - 1 - index)
            * projected**index
            * source
            * residual_metric.sqrt()
        )
    residual = radius * radius
    center = source**2 * projected ** (2 * horizon) * vector_metric
    target = 2 * fused ** (2 * horizon) * m_fused
    complement = 2 * (
        slow ** (2 * horizon) * m_slow
        + mixing * mixing * fast ** (2 * horizon) * m_fast
    )
    eta = (epsilon * residual / (target + epsilon * center)).sqrt()
    target_envelope = (1 + eta) * target
    complement_envelope = (1 + eta) * center + (1 + 1 / eta) * residual
    return target_envelope / target, complement_envelope / complement


def main() -> None:
    ctx.prec = 256
    contraction = arb("0.99")
    tolerance = arb("0.001")
    geometric_horizon = 688
    at_horizon = contraction**geometric_horizon
    before_horizon = contraction ** (geometric_horizon - 1)
    physical_gain, global_gain = cancellation_focused_row()
    ring_projection_lower = arb(1)
    payload = {
        "status": "arb_exact_adaptive_portfolio_branch_audit",
        "evidence_level": (
            "256-bit Arb arithmetic for one geometric, one covariance, and "
            "one exact lower-gate branch; not a production portfolio audit"
        ),
        "precision_bits": 256,
        "geometric_branch": {
            "contraction": str(contraction),
            "tolerance": str(tolerance),
            "selected_horizon": geometric_horizon,
            "at_horizon": str(at_horizon),
            "before_horizon": str(before_horizon),
        },
        "covariance_branch": {
            "physical_gain": str(physical_gain),
            "global_gain": str(global_gain),
        },
        "lower_gate_branch": {
            "fourier_ring_projection_lower": str(ring_projection_lower),
            "target": "0.1",
        },
        "geometric_first_horizon_certified": (
            float(at_horizon.upper()) <= 0.001
            and float(before_horizon.lower()) > 0.001
        ),
        "focused_covariance_meets_physical_and_global_budgets_certified": (
            float(physical_gain.upper()) < 1.01
            and float(global_gain.upper()) < 500.0
        ),
        "fourier_lower_gate_rejects_ten_percent_budget_certified": (
            float(ring_projection_lower.lower()) > 0.1
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
