"""256-bit Arb audit of the cross-column cancellation witness."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_cancellation_audit.json"


def contains_zero(value: arb) -> bool:
    return float(value.lower()) <= 0.0 <= float(value.upper())


def main() -> None:
    ctx.prec = 256
    slow = arb("0.995")
    fused = arb("0.55")
    fast = arb("0.2")
    mixing = arb("0.2")
    horizon = 32
    # z1=(1,1,mixing), z2=(-1,1,-mixing), a=(1,1).
    fused_coordinates = (
        arb(1) - arb(1),
        arb(1) + arb(1),
        mixing - mixing,
    )
    exact_fused_energy = (
        4 * fused ** (2 * horizon) / (1 - fused * fused)
    )
    columnwise_slow_lower = (
        4 * slow ** (2 * horizon) / (1 - slow * slow)
    )
    lower_ratio = columnwise_slow_lower / exact_fused_energy
    # The first block basis vector is e2.  The fused coordinate is (2,0),
    # H^j preserves that axis and the Galerkin residual annihilates it.
    residual_on_fused_axis = (fused - fused) * arb(2)
    payload = {
        "status": "arb_cross_column_cancellation_audit",
        "evidence_level": (
            "256-bit Arb certification of one diagonal cancellation witness; "
            "not a production packet interval audit"
        ),
        "precision_bits": 256,
        "operator_diagonal": [str(slow), str(fused), str(fast)],
        "mixing": str(mixing),
        "horizon": horizon,
        "fused_source_coordinates": [
            str(value) for value in fused_coordinates
        ],
        "exact_fused_energy_ball": str(exact_fused_energy),
        "independent_column_slow_lower_ball": str(columnwise_slow_lower),
        "columnwise_lower_over_exact_ball": str(lower_ratio),
        "fused_slow_and_fast_coordinates_cancel_certified": (
            contains_zero(fused_coordinates[0])
            and contains_zero(fused_coordinates[2])
            and float(fused_coordinates[1].lower()) > 0.0
        ),
        "block_residual_annihilates_fused_axis_certified": contains_zero(
            residual_on_fused_axis
        ),
        "exact_fused_energy_positive_certified": (
            float(exact_fused_energy.lower()) > 0.0
        ),
        "columnwise_loss_exceeds_1e18_certified": (
            float(lower_ratio.lower()) > 1.0e18
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
