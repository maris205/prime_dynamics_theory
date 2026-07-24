"""Exact scalar inversion for RH-137 Young envelopes."""

from __future__ import annotations

import math
from typing import Iterable, Mapping, Sequence


def _nn(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def young_map(state: float, metric: float, frame: float, birth: float) -> float:
    y = _nn(state, "state")
    a = _nn(metric, "metric")
    b = _nn(frame, "frame")
    q = _nn(birth, "birth")
    return q + (math.sqrt(a * y) + math.sqrt(b)) ** 2


def preimage_radius(target: float, metric: float, frame: float, birth: float, cap: float = 1.0) -> float:
    """Supremal y in [0,cap] with F(y)<target for a Young map F."""
    t = _nn(target, "target")
    a = _nn(metric, "metric")
    b = _nn(frame, "frame")
    q = _nn(birth, "birth")
    ceiling = _nn(cap, "cap")
    if t <= q + b:
        return 0.0
    if a == 0.0:
        return ceiling
    slack = math.sqrt(t - q) - math.sqrt(b)
    if slack <= 0.0:
        return 0.0
    return min(ceiling, max(0.0, slack * slack / a))


def controlled_preimage(target: float, candidates: Iterable[Mapping[str, float]], cap: float = 1.0) -> dict[str, float | int]:
    pool = list(candidates)
    if not pool:
        raise ValueError("at least one control candidate is required")
    radii = [preimage_radius(target, item["metric"], item["frame"], item["birth"], cap) for item in pool]
    index = max(range(len(pool)), key=radii.__getitem__)
    floors = [young_map(0.0, item["metric"], item["frame"], item["birth"]) for item in pool]
    return {"radius": radii[index], "control_index": index, "minimum_floor": min(floors)}


def backward_kernel(sequence: Sequence[Iterable[Mapping[str, float]]], ceiling: float = 1.0, cap: float = 1.0) -> dict[str, object]:
    target = _nn(ceiling, "ceiling")
    radii = [target]
    choices = []
    floors = []
    for candidates in reversed(sequence):
        result = controlled_preimage(target, candidates, cap)
        target = float(result["radius"])
        radii.append(target)
        choices.append(int(result["control_index"]))
        floors.append(float(result["minimum_floor"]))
    return {
        "radii": list(reversed(radii)),
        "control_indices": list(reversed(choices)),
        "minimum_floors": list(reversed(floors)),
    }

