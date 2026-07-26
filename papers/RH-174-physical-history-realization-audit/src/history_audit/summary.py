"""Small deterministic reducers used by the RH-174 archive."""

from __future__ import annotations

import statistics


def metric_summary(records: list[dict[str, object]], key: str) -> dict[str, float]:
    values = [float(record[key]) for record in records if key in record]
    if not values:
        raise ValueError(f"metric {key!r} is absent")
    return {
        "minimum": min(values),
        "median": statistics.median(values),
        "maximum": max(values),
    }


def threshold_count(records: list[dict[str, object]], key: str, threshold: float) -> int:
    return sum(float(record[key]) <= float(threshold) for record in records if key in record)
