#!/usr/bin/env python3
"""Adversarial mutations for the TPC-231 determinant and singular factors."""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from finite_resonance_sieve import (  # noqa: E402
    exceptional_correction,
    forms_3716,
    predicted_root_count_3716,
    root_count_3716,
)


class AdversaryFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise AdversaryFailure(message)


def mutated_root_count(Q: int, ell: int) -> int:
    return sum(1 for k in range(ell) if (forms_3716(Q, k)[0] * (forms_3716(Q, k)[1] + 1)) % ell == 0)


def main() -> int:
    require(root_count_3716(25, 5) == predicted_root_count_3716(25, 5) == 1, "positive exceptional root")
    require(mutated_root_count(25, 5) == 2, "determinant mutation was not exposed")
    require(root_count_3716(25, 2) == 1, "parity root")
    require(2 != predicted_root_count_3716(25, 2), "parity mutation survived")
    require(exceptional_correction(25) == Fraction(4, 3), "positive correction")
    require(Fraction(6, 3) != exceptional_correction(25), "wrong Euler factor survived")
    require(root_count_3716(55, 5) == 1 and root_count_3716(55, 11) == 1, "two exceptional divisors")
    require(root_count_3716(55, 13) == 2, "generic dimension")
    print("TPC231_SIEVE_ADVERSARY=PASS")
    print("determinant_plus_one_mutation=CAUGHT")
    print("exceptional_root_to_generic_mutation=CAUGHT")
    print("singular_factor_mutation=CAUGHT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
