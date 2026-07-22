"""Scalar forms of the RH-91 bootstrap and completion logic."""

from __future__ import annotations

import math
from typing import Iterable, Sequence


def bootstrap_relative_bound(eta: float, rho: float, updates: int) -> float:
    decay = float(eta)
    contraction = float(rho)
    count = int(updates)
    if not 0.0 <= decay < 1.0 or not 0.0 < contraction < 1.0 or count < 0:
        raise ValueError("invalid bootstrap data")
    return math.nextafter(contraction ** (count / 2.0) / math.sqrt(1.0 - decay), math.inf)


def updates_for_tolerance(eta: float, rho: float, tolerance: float) -> int:
    target = float(tolerance)
    if target <= 0.0:
        raise ValueError("positive tolerance required")
    updates = 0
    while bootstrap_relative_bound(eta, rho, updates) > target:
        updates += 1
    return updates


def minimal_completion_bundles(alternatives: Sequence[Iterable[str]], common: Iterable[str] = ()) -> list[list[str]]:
    base = set(common)
    bundles = [base | set(alternative) for alternative in alternatives]
    minimal = []
    for bundle in bundles:
        if not any(other < bundle for other in bundles):
            minimal.append(sorted(bundle))
    return sorted(minimal, key=lambda item: (len(item), item))
