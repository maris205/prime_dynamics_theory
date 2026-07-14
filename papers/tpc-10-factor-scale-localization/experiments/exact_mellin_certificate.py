"""Generate the exact five-node Mellin-jet certificate for TPC-10.

Only Python's standard library is used.  Every rational quantity is kept as
``fractions.Fraction`` until JSON serialization.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence


NODES = (-4, -2, 0, 2, 4)
MU_PLUS = tuple(Fraction(x, 8) for x in (1, 0, 6, 0, 1))
MU_MINUS = tuple(Fraction(x, 8) for x in (0, 4, 0, 4, 0))
ANNIHILATOR = (1, -4, 6, -4, 1)
WINDOW = (0, 0, 1, 0, 0)


def moment(weights: Sequence[Fraction], order: int) -> Fraction:
    return sum((weight * (node**order) for node, weight in zip(NODES, weights)), Fraction())


def integer_moment(weights: Sequence[int], order: int) -> int:
    return sum(weight * (node**order) for node, weight in zip(NODES, weights))


def pairing(left: Iterable[Fraction | int], right: Iterable[Fraction | int]) -> Fraction:
    return sum((Fraction(a) * Fraction(b) for a, b in zip(left, right)), Fraction())


def best_polynomial_value(node: int) -> Fraction:
    """q(x)=5/8-x^2/16."""

    return Fraction(5, 8) - Fraction(node * node, 16)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def as_text(value: Fraction | int) -> str:
    return str(Fraction(value))


def build_certificate() -> dict[str, object]:
    plus_moments = [moment(MU_PLUS, k) for k in range(4)]
    minus_moments = [moment(MU_MINUS, k) for k in range(4)]
    annihilator_moments = [integer_moment(ANNIHILATOR, k) for k in range(4)]
    q_values = [best_polynomial_value(x) for x in NODES]
    residual = [Fraction(v) - q for v, q in zip(WINDOW, q_values)]
    l1_norm = sum(abs(c) for c in ANNIHILATOR)
    window_pairing = pairing(ANNIHILATOR, WINDOW)

    return {
        "target": {
            "h": 2,
            "r": 81,
            "r_plus_h": 83,
            "r_plus_h_is_prime": is_prime(83),
            "factor_pairs": [[1, 81], [3, 27], [9, 9], [27, 3], [81, 1]],
            "normalized_log_nodes": list(NODES),
        },
        "profiles": {
            "mu_plus": [as_text(x) for x in MU_PLUS],
            "mu_minus": [as_text(x) for x in MU_MINUS],
            "mu_plus_moments_0_to_3": [as_text(x) for x in plus_moments],
            "mu_minus_moments_0_to_3": [as_text(x) for x in minus_moments],
            "central_window_mu_plus": as_text(pairing(MU_PLUS, WINDOW)),
            "central_window_mu_minus": as_text(pairing(MU_MINUS, WINDOW)),
        },
        "minimax": {
            "annihilator": list(ANNIHILATOR),
            "annihilator_moments_0_to_3": annihilator_moments,
            "annihilator_l1_norm": l1_norm,
            "window_pairing": as_text(window_pairing),
            "sharp_radius": as_text(window_pairing / l1_norm),
            "best_polynomial": "5/8-x^2/16",
            "best_polynomial_values": [as_text(x) for x in q_values],
            "residual_values": [as_text(x) for x in residual],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = build_certificate()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
