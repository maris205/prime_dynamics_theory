"""Elementary cofinal criteria used by RH-145."""

from __future__ import annotations

import math
from typing import Iterable, Mapping


def eventual_directional_floor(tail_limsup: float, base_liminf: float) -> float:
    tail = float(tail_limsup)
    base = float(base_liminf)
    if not all(math.isfinite(value) for value in (tail, base)) or tail < 0.0 or base < 0.0:
        raise ValueError("tail and base bounds must be finite and nonnegative")
    return max(0.0, 1.0 - math.sqrt(tail)) ** 4 * base


def recurrent_floor_obstruction(floors: Iterable[float]) -> bool:
    values = [float(value) for value in floors]
    if any(not math.isfinite(value) or value < 0.0 for value in values):
        raise ValueError("floors must be finite and nonnegative")
    return sum(value >= 1.0 for value in values) == len(values) and bool(values)


def suffix_statistics(rows: Iterable[Mapping[str, object]], cutoff: float) -> dict[str, float | int | None]:
    threshold = float(cutoff)
    selected = [row for row in rows if float(row["sigma"]) <= threshold]
    positive = [row for row in selected if bool(row["positive"])]
    floors = [float(row["floor"]) for row in positive]
    return {
        "count": len(selected),
        "positive_count": len(positive),
        "minimum_positive_floor": min(floors, default=None),
    }

