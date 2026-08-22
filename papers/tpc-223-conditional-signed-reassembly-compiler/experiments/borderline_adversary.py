#!/usr/bin/env python3
"""Adversarial boundary checks for the strict TPC-223 gate."""

from __future__ import annotations

from fractions import Fraction


def classify(ap: Fraction, polarized: Fraction, loss: Fraction) -> str:
    margin = min(ap, polarized) - loss - Fraction(1, 400)
    if margin > 0:
        return "STRICT_PASS"
    if margin == 0:
        return "BORDERLINE"
    return "NO_STRICT_SAVING"


def main() -> int:
    if classify(Fraction(1, 400), Fraction(1, 400), Fraction(0)) != "BORDERLINE":
        raise SystemExit("borderline accepted")
    if classify(Fraction(0), Fraction(1, 10), Fraction(0)) != "NO_STRICT_SAVING":
        raise SystemExit("missing AP channel accepted")
    if classify(Fraction(1, 10), Fraction(0), Fraction(0)) != "NO_STRICT_SAVING":
        raise SystemExit("missing polarized channel accepted")
    if classify(Fraction(1, 100), Fraction(1, 80), Fraction(1, 100)) != "NO_STRICT_SAVING":
        raise SystemExit("loss-dominated ledger accepted")
    print("TPC223_BOUNDARY_ADVERSARY=PASS")
    print("borderline=REJECTED_AS_STRICT")
    print("missing_channel=REJECTED")
    print("loss_dominated=REJECTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
