from __future__ import annotations

import math


LAMBDA = 1.678573510428322


def tail_slope() -> float:
    return 1.0 / math.log(10.0 / 7.0)


def localization_slope(multiplier: float = LAMBDA) -> float:
    if multiplier <= 1.0:
        raise ValueError("multiplier must exceed one")
    return 1.0 / math.log(multiplier)


def tail_decay_exponent(slope: float) -> float:
    return slope * math.log(10.0 / 7.0) - 1.0


def clearance_exponent(slope: float, multiplier: float = LAMBDA) -> float:
    return slope * math.log(multiplier) - 1.0
