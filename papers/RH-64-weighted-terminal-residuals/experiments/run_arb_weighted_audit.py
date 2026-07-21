"""256-bit Arb audit of the two-block Lyapunov metric."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_weighted_audit.json"


def contains_zero(value: arb) -> bool:
    return float(value.lower()) <= 0.0 <= float(value.upper())


def lower_positive(value: arb) -> bool:
    return float(value.lower()) > 0.0


def upper_less_than_one(value: arb) -> bool:
    return float(value.upper()) < 1.0


def main() -> None:
    ctx.prec = 256
    a = arb("0.2")
    b = arb("0.7")
    coupling = arb("0.3")
    m11 = 1 / (1 - a * a)
    m12 = a * coupling * m11 / (1 - a * b)
    m22 = (
        1 + coupling * coupling * m11 + 2 * b * coupling * m12
    ) / (1 - b * b)
    determinant = m11 * m22 - m12 * m12
    trace = m11 + m22
    discriminant = ((m11 - m22) ** 2 + 4 * m12 * m12).sqrt()
    maximum_eigenvalue = (trace + discriminant) / 2
    metric_q = (1 - 1 / maximum_eigenvalue).sqrt()
    residual11 = m11 - a * a * m11 - 1
    residual12 = m12 - a * coupling * m11 - a * b * m12
    residual22 = (
        m22
        - coupling * coupling * m11
        - 2 * b * coupling * m12
        - b * b * m22
        - 1
    )
    payload = {
        "status": "arb_two_block_lyapunov_weighted_residual_audit",
        "evidence_level": (
            "256-bit Arb audit of the displayed two-block Lyapunov metric; "
            "no production interval calculation"
        ),
        "precision_bits": 256,
        "metric_entries": [str(m11), str(m12), str(m22)],
        "metric_determinant_ball": str(determinant),
        "maximum_metric_eigenvalue_ball": str(maximum_eigenvalue),
        "metric_contraction_ball": str(metric_q),
        "lyapunov_residual_balls": [
            str(residual11),
            str(residual12),
            str(residual22),
        ],
        "metric_positive_definite_certified": (
            lower_positive(m11)
            and lower_positive(m22)
            and lower_positive(determinant)
        ),
        "lyapunov_identity_certified": all(
            contains_zero(value)
            for value in (residual11, residual12, residual22)
        ),
        "strict_metric_contraction_certified": upper_less_than_one(metric_q),
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
