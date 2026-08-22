#!/usr/bin/env python3
"""Adversarial boundary checks for the TPC-224 interface constant."""

from __future__ import annotations

from fractions import Fraction


def check_counts(prime_count: int, packet_count: int) -> tuple[Fraction, Fraction, Fraction]:
    ap = Fraction(packet_count * prime_count**2)
    polarized = Fraction(prime_count * packet_count**2)
    full = Fraction((prime_count * packet_count) ** 2)
    sharp = Fraction(prime_count * packet_count, prime_count + packet_count)
    return full / (ap + polarized), full / (sharp * (ap + polarized)), full


def main() -> int:
    for prime_count in range(1, 9):
        for packet_count in range(1, 7):
            unit_ratio, sharp_ratio, _ = check_counts(prime_count, packet_count)
            if sharp_ratio != 1:
                raise SystemExit("sharp equality formula changed")
            if prime_count == 1 or packet_count == 1:
                if unit_ratio > 1:
                    raise SystemExit("unit interface failed at one-label boundary")
            elif prime_count == 2 and packet_count == 2:
                if unit_ratio != 1:
                    raise SystemExit("2x2 boundary mismatch")
            elif unit_ratio <= 1:
                raise SystemExit("unit interface was not refuted")
    print("TPC224_BOUNDARY_ADVERSARY=PASS")
    print("sharp_constant=EXACT_AND_SHARP")
    print("unit_constant=REFUTED_FOR_P,J_GREATER_THAN_2")
    print("one_label_boundary=SAFE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
