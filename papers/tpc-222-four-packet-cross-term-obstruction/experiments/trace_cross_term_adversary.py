#!/usr/bin/env python3
from __future__ import annotations

from fractions import Fraction


def main():
    plus = (1, 1, 1, 1)
    minus = (1, -1, 1, -1)
    plus_energy = sum(plus) ** 2
    minus_energy = sum(minus) ** 2
    trace = 4
    if plus_energy != 16 or minus_energy != 0 or trace != 4:
        raise SystemExit("trace/cross-term adversary failed")
    if Fraction(plus_energy, trace) != 4:
        raise SystemExit("trace endpoint not saturated")
    print("TPC222_TRACE_CROSS_TERM_ADVERSARY=PASS")
    print(f"trace={trace} plus_energy={plus_energy} minus_energy={minus_energy}")
    print("same_diagonal=True signed_energy_nonidentifiability=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
