"""256-bit Arb audit of the exact covariance sharpness tradeoff."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_covariance_tradeoff.json"


def exact_row(epsilon: arb) -> dict[str, arb]:
    slow = arb("0.995")
    fused = arb("0.55")
    fast = arb("0.2")
    mixing = arb("0.2")
    horizon = 32
    m_slow = 1 / (1 - slow * slow)
    m_fused = 1 / (1 - fused * fused)
    m_fast = 1 / (1 - fast * fast)
    normalizer = 1 + mixing * mixing
    projected = (slow + mixing * mixing * fast) / normalizer
    source_coordinate = (2 * normalizer).sqrt()
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
            * source_coordinate
            * residual_metric.sqrt()
        )
    residual_upper = radius * radius
    center_complement = (
        source_coordinate**2
        * projected ** (2 * horizon)
        * vector_metric
    )
    exact_target = 2 * fused ** (2 * horizon) * m_fused
    exact_complement = 2 * (
        slow ** (2 * horizon) * m_slow
        + mixing * mixing * fast ** (2 * horizon) * m_fast
    )
    eta = (
        epsilon
        * residual_upper
        / (exact_target + epsilon * center_complement)
    ).sqrt()
    target_envelope = (1 + eta) * exact_target
    complement_envelope = (
        (1 + eta) * center_complement
        + (1 + 1 / eta) * residual_upper
    )
    return {
        "eta": eta,
        "physical_gain": target_envelope / exact_target,
        "global_gain": complement_envelope / exact_complement,
        "weighted_gain": (
            target_envelope + epsilon * complement_envelope
        )
        / (exact_target + epsilon * exact_complement),
        "exact_target": exact_target,
        "exact_complement": exact_complement,
        "center_complement": center_complement,
        "residual_upper": residual_upper,
    }


def main() -> None:
    ctx.prec = 256
    isotropic = exact_row(arb(1))
    focused = exact_row(arb("1e-24"))
    payload = {
        "status": "arb_physical_covariance_sharpness_tradeoff_audit",
        "evidence_level": (
            "256-bit Arb certification of the exact diagonal cancellation "
            "reduction; not a production covariance audit"
        ),
        "precision_bits": 256,
        "isotropic_row": {key: str(value) for key, value in isotropic.items()},
        "focused_row": {key: str(value) for key, value in focused.items()},
        "isotropic_physical_gain_between_2_and_3_certified": (
            float(isotropic["physical_gain"].lower()) > 2.0
            and float(isotropic["physical_gain"].upper()) < 3.0
        ),
        "isotropic_global_gain_below_1_point_2_certified": (
            float(isotropic["global_gain"].upper()) < 1.2
        ),
        "focused_physical_gain_between_1_point_001_and_1_point_002_certified": (
            float(focused["physical_gain"].lower()) > 1.001
            and float(focused["physical_gain"].upper()) < 1.002
        ),
        "focused_global_gain_exceeds_400_certified": (
            float(focused["global_gain"].lower()) > 400.0
        ),
        "positive_exact_energies_certified": all(
            float(record[key].lower()) > 0.0
            for record in (isotropic, focused)
            for key in ("exact_target", "exact_complement")
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
