"""Exact rank/degree/cycle-length bookkeeping."""

from __future__ import annotations

import math


def cycle_clock_translation(half_clock: float, cloud_degree: int, *, rank_offset: int = 2) -> dict[str, float | int]:
    clock = float(half_clock)
    degree = int(cloud_degree)
    offset = int(rank_offset)
    if clock <= 0.0 or degree < 0 or offset < 0:
        raise ValueError("invalid clock, degree, or offset")
    rank = math.ceil(clock) + offset
    length = degree + 1
    defect = clock - degree
    gap = rank - length
    translated_gap = math.ceil(defect) + offset - 1
    return {
        "half_clock": clock,
        "cloud_degree": degree,
        "cycle_length": length,
        "clock_rank": rank,
        "degree_defect": defect,
        "rank_cycle_gap": gap,
        "translated_rank_cycle_gap": translated_gap,
    }


def possible_gap_values(defect_lower: float, defect_upper: float, *, rank_offset: int = 2) -> tuple[int, ...]:
    lower = float(defect_lower)
    upper = float(defect_upper)
    if upper < lower:
        raise ValueError("upper endpoint must dominate lower endpoint")
    start = math.ceil(lower)
    stop = math.ceil(upper)
    return tuple(range(start + int(rank_offset) - 1, stop + int(rank_offset)))
