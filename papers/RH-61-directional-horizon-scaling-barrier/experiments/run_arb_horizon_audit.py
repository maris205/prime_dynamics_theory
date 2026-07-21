"""256-bit Arb audit of the scalar horizon envelope and slow-mode bound."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from flint import arb, ctx

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_horizon_audit.json"
sys.path.insert(0, str(ROOT / "src"))

from horizon_scaling import minimum_geometric_horizon, slow_mode_horizon_lower_bound  # noqa: E402


def upper_below(left: arb, right: arb) -> bool:
    return float(left.upper()) < float(right.lower())


def lower_above(left: arb, right: arb) -> bool:
    return float(left.lower()) > float(right.upper())


def main() -> None:
    ctx.prec = 256
    q = arb("0.99")
    amplitude = arb("0.4")
    tolerance = arb("0.01")
    real_threshold = (amplitude / tolerance).log() / (-q.log())
    horizon = slow_mode_horizon_lower_bound(0.99, 0.4, 0.01)
    at_horizon = amplitude * q**horizon
    before_horizon = amplitude * q ** max(0, horizon - 1)

    tails = (arb("0.4"), arb("0.2"))
    rates = (arb("0.8"), q)
    envelope_horizon = minimum_geometric_horizon(
        (0.4, 0.2), (0.8, 0.99), 0.01
    )
    geometric_at_horizon = (
        tails[0] * rates[0] ** envelope_horizon
        + tails[1] * rates[1] ** envelope_horizon
    )
    geometric_before = (
        tails[0] * rates[0] ** max(0, envelope_horizon - 1)
        + tails[1] * rates[1] ** max(0, envelope_horizon - 1)
    )

    # A scalar stable mode has the exact observability Stein metric
    # O=(1-q^2)^(-1); its tail is therefore an equality case for the
    # corresponding Stein certificate.
    metric = 1 / (1 - q * q)
    exact_tail_squared = amplitude * amplitude * q ** (2 * horizon) * metric
    exact_tail = exact_tail_squared.sqrt()
    lower_bound_tail = amplitude * q**horizon

    payload = {
        "status": "arb_scalar_horizon_envelope_and_slow_mode_audit",
        "evidence_level": (
            "256-bit Arb scalar equality-case audit; no production "
            "finite-matrix interval validation"
        ),
        "precision_bits": 256,
        "model": {
            "contraction": str(q),
            "amplitude": str(amplitude),
            "tolerance": str(tolerance),
            "slow_mode_horizon": horizon,
            "geometric_envelope_horizon": envelope_horizon,
            "second_packet_rate": str(rates[0]),
            "second_packet_initial_tail": str(tails[0]),
        },
        "real_threshold_ball": str(real_threshold),
        "slow_mode_at_horizon_ball": str(at_horizon),
        "slow_mode_before_horizon_ball": str(before_horizon),
        "geometric_at_horizon_ball": str(geometric_at_horizon),
        "geometric_before_horizon_ball": str(geometric_before),
        "stein_metric_ball": str(metric),
        "exact_scalar_tail_ball": str(exact_tail),
        "slow_mode_lower_bound_tail_ball": str(lower_bound_tail),
        "slow_mode_upper_at_horizon_certified": upper_below(
            at_horizon, tolerance
        ),
        "slow_mode_failure_before_horizon_certified": lower_above(
            before_horizon, tolerance
        ),
        "geometric_upper_at_horizon_certified": upper_below(
            geometric_at_horizon, tolerance
        ),
        "geometric_failure_before_horizon_certified": lower_above(
            geometric_before, tolerance
        ),
        "stein_tail_equality_case_certified": lower_above(
            exact_tail, lower_bound_tail
        ),
        "production_interval_audit_executed": False,
        "scope": (
            "The certificate validates the scalar horizon algebra and its "
            "equality-case interpretation only."
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
