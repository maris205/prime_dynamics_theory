#!/usr/bin/env python3
"""Exact endpoint adversaries for the TPC-219 P-collapse ledger."""

from fractions import Fraction
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from longitudinal_transverse import ledger  # noqa: E402


def main() -> int:
    aligned = ledger(tuple((Fraction(3), Fraction(-2)) for _ in range(4)))
    balanced = ledger(((Fraction(1), Fraction(0)), (Fraction(-1), Fraction(0)),
                       (Fraction(1), Fraction(0)), (Fraction(-1), Fraction(0))))
    if aligned["transverse"] != "0" or aligned["shell"] != aligned["p_times_diagonal"]:
        raise SystemExit("aligned endpoint failed")
    if balanced["shell"] != "0" or balanced["transverse"] != balanced["diagonal"]:
        raise SystemExit("balanced endpoint failed")
    print("TPC219_ALIGNMENT_ADVERSARY=PASS")
    print("aligned_transverse=0")
    print("aligned_ratio=P")
    print("balanced_shell=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
