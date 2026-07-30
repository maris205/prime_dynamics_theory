from __future__ import annotations

import math


def minimal_multiplicity(order: int, moment: float, radius_cap: float) -> int:
    d = int(order)
    if d < 1 or radius_cap <= 0.0:
        raise ValueError("invalid packet data")
    if moment == 0.0:
        return 0
    return max(1, math.ceil(abs(moment) / (d * radius_cap**d)))


def packet_radius(order: int, multiplicity: int, moment: float) -> float:
    d = int(order)
    copies = int(multiplicity)
    if d < 1 or copies < 1:
        raise ValueError("packet order and multiplicity must be positive")
    return (abs(moment) / (d * copies)) ** (1.0 / d)


def packet_rank(order: int, multiplicity: int) -> int:
    d = int(order)
    copies = int(multiplicity)
    if d < 1 or copies < 0:
        raise ValueError("invalid packet rank data")
    return d * copies


def packet_squared_mass(order: int, multiplicity: int, moment: float) -> float:
    if multiplicity == 0 and moment == 0.0:
        return 0.0
    return packet_rank(order, multiplicity) * packet_radius(order, multiplicity, moment) ** 2


def packet_power_sum(order: int, multiplicity: int, moment: float, power: int) -> float:
    d = int(order)
    copies = int(multiplicity)
    n = int(power)
    if d < 1 or copies < 1 or n < 1:
        raise ValueError("invalid packet moment data")
    if n % d:
        return 0.0
    multiple = n // d
    return float(moment**multiple / (d * copies) ** (multiple - 1))
