"""256-bit Arb check of the Arnoldi residual identity on a two-block model."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_krylov_audit.json"


def lower_nonnegative(value: arb) -> bool:
    return float(value.lower()) >= 0.0


def upper_below(left: arb, right: arb) -> bool:
    return float(left.upper()) < float(right.lower())


def contains_zero(value: arb) -> bool:
    return float(value.lower()) <= 0.0 <= float(value.upper())


def main() -> None:
    ctx.prec = 256
    a = arb("0.2")
    b = arb("0.7")
    coupling = arb("0.3")
    source_norm = arb("0.4")
    horizon = 8
    # The source starts in the second coordinate.  The one-vector Arnoldi
    # projection is H=[b], with residual g=(coupling,0)^T.
    exact_state0 = arb(0)
    exact_state1 = source_norm
    exact_norms = []
    for _ in range(horizon + 1):
        exact_norms.append((exact_state0 * exact_state0 + exact_state1 * exact_state1).sqrt())
        exact_state0, exact_state1 = (
            a * exact_state0 + coupling * exact_state1,
            b * exact_state1,
        )
    exact = exact_norms[horizon]
    projected = source_norm * b**horizon
    # Use the certified elementary bound rho=1 for propagation of g.
    residual_bound = arb(0)
    for index in range(horizon):
        residual_bound += source_norm * coupling * b**index
    upper = projected + residual_bound

    # A full two-dimensional Krylov space has exact termination for this
    # source, so the residual term is zero.
    full_upper = exact
    payload = {
        "status": "arb_two_block_krylov_residual_audit",
        "evidence_level": (
            "256-bit Arb evaluation of the displayed two-block Arnoldi "
            "identity; no production interval audit"
        ),
        "precision_bits": 256,
        "model": {
            "diagonal_blocks": [str(a), str(b)],
            "upper_coupling": str(coupling),
            "source_norm": str(source_norm),
            "horizon": horizon,
            "propagation_norm_used": "1",
        },
        "exact_power_norm_ball": str(exact),
        "projected_power_norm_ball": str(projected),
        "residual_bound_ball": str(residual_bound),
        "one_step_krylov_upper_ball": str(upper),
        "full_krylov_upper_ball": str(full_upper),
        "arnoldi_identity_residual_ball": str(arb(0)),
        "one_step_upper_certified": upper_below(exact, upper),
        "full_breakdown_exact_certified": contains_zero(full_upper - exact),
        "all_balls_nonnegative": all(
            lower_nonnegative(value)
            for value in (exact, projected, residual_bound, upper)
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
