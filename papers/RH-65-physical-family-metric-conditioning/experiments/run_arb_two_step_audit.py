"""256-bit Arb audit of the exact two-step conditioning witness."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_two_step_audit.json"


def contains_zero(value: arb) -> bool:
    return float(value.lower()) <= 0.0 <= float(value.upper())


def positive(value: arb) -> bool:
    return float(value.lower()) > 0.0


def exact_ledger(gap: arb, coupling: arb) -> dict[str, arb]:
    q = (1 - gap).sqrt()
    m11 = 1 / gap
    m12 = q * coupling / (gap * gap)
    m22 = 1 / gap + coupling * coupling * (1 + q * q) / (gap**3)
    trace = m11 + m22
    determinant = m11 * m22 - m12 * m12
    discriminant = ((m11 - m22) ** 2 + 4 * m12 * m12).sqrt()
    lambda_min = (trace - discriminant) / 2
    lambda_max = (trace + discriminant) / 2
    contraction = (1 - 1 / lambda_max).sqrt()
    contraction_gap = (1 / lambda_max) / (1 + contraction)
    residual11 = m11 - q * q * m11 - 1
    residual12 = m12 - q * coupling * m11 - q * q * m12
    residual22 = (
        m22
        - coupling * coupling * m11
        - 2 * q * coupling * m12
        - q * q * m22
        - 1
    )
    return {
        "m11": m11,
        "m12": m12,
        "m22": m22,
        "determinant": determinant,
        "lambda_min": lambda_min,
        "lambda_max": lambda_max,
        "condition": lambda_max / lambda_min,
        "contraction_gap": contraction_gap,
        "residual11": residual11,
        "residual12": residual12,
        "residual22": residual22,
    }


def main() -> None:
    ctx.prec = 256
    unmatched = exact_ledger(arb("0.0001"), arb("0.2"))
    matched = exact_ledger(arb("0.0001"), arb("0.00002"))
    residual_keys = ("residual11", "residual12", "residual22")
    payload = {
        "status": "arb_exact_two_step_metric_conditioning_audit",
        "evidence_level": (
            "256-bit Arb certification of two displayed family points; "
            "not a production folded-Gaussian interval audit"
        ),
        "precision_bits": 256,
        "unmatched_fixed_coupling": {
            key: str(value) for key, value in unmatched.items()
        },
        "matched_gap_scale_coupling": {
            key: str(value) for key, value in matched.items()
        },
        "unmatched_identity_certified": all(
            contains_zero(unmatched[key]) for key in residual_keys
        ),
        "matched_identity_certified": all(
            contains_zero(matched[key]) for key in residual_keys
        ),
        "positive_metrics_certified": all(
            positive(record["lambda_min"])
            and positive(record["determinant"])
            for record in (unmatched, matched)
        ),
        "fixed_coupling_condition_exceeds_1e7": (
            float(unmatched["condition"].lower()) > 1.0e7
        ),
        "fixed_coupling_metric_gap_below_1e_minus_10": (
            float(unmatched["contraction_gap"].upper()) < 1.0e-10
        ),
        "matched_condition_below_2": (
            float(matched["condition"].upper()) < 2.0
        ),
        "matched_metric_gap_over_gap_between_point_4_and_point_5": (
            float((matched["contraction_gap"] / arb("0.0001")).lower())
            > 0.4
            and float(
                (matched["contraction_gap"] / arb("0.0001")).upper()
            )
            < 0.5
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
