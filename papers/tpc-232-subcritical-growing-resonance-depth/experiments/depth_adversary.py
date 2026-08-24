#!/usr/bin/env python3
"""Adversarial boundary checks for TPC-232."""

from __future__ import annotations

import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from growing_resonance_depth import (  # noqa: E402
    DepthFailure,
    channel_weight_sum,
    positive_multipliers,
    support_scan,
)


class AdversaryFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise AdversaryFailure(message)


def rejects(callable_object, message: str) -> None:
    try:
        callable_object()
    except DepthFailure:
        return
    raise AdversaryFailure(message)


def main() -> int:
    try:
        rejects(lambda: support_scan(True, 1), "bool Q accepted")
        rejects(lambda: support_scan(101, True), "bool L accepted")
        rejects(lambda: support_scan(101, 25), "unsafe depth accepted")
        need(gcd(4, 4 * 3 * 8) > 1, "nonprimitive m=4 fixture lost")
        need(4 not in positive_multipliers(25, 3, 37), "nonprimitive m=4 admitted")
        need(support_scan(25, 4)["resonance_channels"] == 1, "Q25 anchor")
        need(support_scan(25, 3)["resonance_channels"] == 0, "primitive L3 stop")
        for L in range(1, 80):
            weight = channel_weight_sum(L)
            need(type(weight) is Fraction and weight <= 4 * L, f"weight bound at L={L}")
    except (AdversaryFailure, OSError, ValueError) as error:
        print(f"TPC232_DEPTH_ADVERSARY=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC232_DEPTH_ADVERSARY=PASS")
    print("unsafe_depth_rejected=YES")
    print("coefficient_weight_L1_to_L79=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
