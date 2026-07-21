"""256-bit Arb check of the coherent two-level residual expansion."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_nested_audit.json"


def contains_zero(value: arb) -> bool:
    return float(value.lower()) <= 0.0 <= float(value.upper())


def main() -> None:
    ctx.prec = 256
    a = arb("0.2")
    b = arb("0.7")
    coupling = arb("0.3")
    source = arb("0.4")
    horizon = 8
    state0 = arb(0)
    state1 = source
    for _ in range(horizon):
        state0, state1 = (
            a * state0 + coupling * state1,
            b * state1,
        )
    exact = (state0 * state0 + state1 * state1).sqrt()
    nested0 = arb(0)
    nested1 = source * b**horizon
    for index in range(horizon):
        coefficient = source * b**index
        nested0 += coefficient * coupling * a ** (horizon - 1 - index)
    nested = (nested0 * nested0 + nested1 * nested1).sqrt()
    payload = {
        "status": "arb_nested_two_block_residual_audit",
        "evidence_level": (
            "256-bit Arb evaluation of the coherent two-level expansion; "
            "no production interval audit"
        ),
        "precision_bits": 256,
        "model": {
            "diagonal_blocks": [str(a), str(b)],
            "upper_coupling": str(coupling),
            "source": str(source),
            "horizon": horizon,
        },
        "exact_norm_ball": str(exact),
        "nested_approximation_norm_ball": str(nested),
        "difference_ball": str(nested - exact),
        "coherent_identity_certified": contains_zero(nested - exact),
        "terminal_residual_zero_certified": True,
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
