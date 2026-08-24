#!/usr/bin/env python3
"""Compatibility and packet-normalization attacks for TPC-235."""

from fractions import Fraction


def main() -> None:
    # V59 exponents force a growing single-clock mismatch.
    assert 2 * Fraction(1, 3) - Fraction(21, 32) == Fraction(1, 96)
    # Matching the physical modulus in the exact floor fixture misses all atoms.
    assert int(Fraction(21, 40) * 17 / 10) == 0
    assert (21 * 17) // 63 == 5
    # Packet-output unit normalization erases every nonzero polarized cross term.
    assert sum((1, 1j, -1, -1j)) == 0
    assert Fraction(9 - 1, 4) == 2
    print("TPC235_CROSSWALK_ADVERSARY=PASS")
    print("single_clock_factor=4*x^(1/96)")
    print("modulus_matched_cutoff=0_VS_5")
    print("output_normalization=POLARIZATION_ERASED")


if __name__ == "__main__":
    main()
