"""Hilbert--Schmidt to square/determinant continuity formulas."""

from __future__ import annotations

import math


def square_trace_error(hs_error: float, bulk_hs_upper: float) -> float:
    epsilon = float(hs_error)
    bulk = float(bulk_hs_upper)
    if epsilon < 0.0 or bulk < 0.0:
        raise ValueError("norm bounds must be nonnegative")
    return math.nextafter(epsilon * (2.0 * bulk + epsilon), math.inf)


def determinant_disk_error(radius: float, hs_error: float, bulk_hs_upper: float) -> float:
    disk = float(radius)
    epsilon = float(hs_error)
    bulk = float(bulk_hs_upper)
    if min(disk, epsilon, bulk) < 0.0:
        raise ValueError("determinant inputs must be nonnegative")
    square = square_trace_error(epsilon, bulk)
    exponent = 1.0 + disk * bulk * bulk + disk * (bulk + epsilon) ** 2
    return math.nextafter(disk * square * math.exp(exponent), math.inf)
