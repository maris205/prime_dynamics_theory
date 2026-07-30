from __future__ import annotations

import math


LAMBDA = 1.678573510428322
R_H = 0.85
Q_STAR = 1.0 / (R_H * LAMBDA)
Q = 0.5
RHO_STAR = 1.0 / Q_STAR
BASE = Q_STAR / Q


def escaping_multiplicity(order: int) -> int:
    k = int(order)
    if k < 1:
        raise ValueError("order must be positive")
    return math.ceil(BASE**k)


def endpoint_packet_coefficient(order: int, multiplicity: int | None = None) -> float:
    k = int(order)
    copies = escaping_multiplicity(k) if multiplicity is None else int(multiplicity)
    if k < 1 or copies < 1:
        raise ValueError("invalid endpoint packet data")
    if copies < escaping_multiplicity(k):
        raise ValueError("multiplicity does not enforce the modulus cap")
    return 1.0


def strict_radius_packet_coefficient(order: int, radius: float) -> float:
    k = int(order)
    rho = float(radius)
    if k < 1 or not 0.0 < rho < RHO_STAR:
        raise ValueError("invalid strict radius data")
    return endpoint_packet_coefficient(k) * (Q_STAR * rho) ** k


def higher_endpoint_packet_coefficient(
    order: int, multiple: int, multiplicity: int | None = None
) -> float:
    k = int(order)
    m = int(multiple)
    copies = escaping_multiplicity(k) if multiplicity is None else int(multiplicity)
    if k < 1 or m < 1 or copies < escaping_multiplicity(k):
        raise ValueError("invalid higher packet coefficient data")
    return 1.0 / (m * copies ** (m - 1))


def packet_squared_mass(order: int, multiplicity: int | None = None) -> float:
    k = int(order)
    copies = escaping_multiplicity(k) if multiplicity is None else int(multiplicity)
    if k < 1 or copies < escaping_multiplicity(k):
        raise ValueError("invalid packet mass data")
    return k * Q_STAR**2 * copies ** (1.0 - 2.0 / k)


def packet_mass_upper(order: int, multiplicity: int | None = None) -> float:
    k = int(order)
    copies = escaping_multiplicity(k) if multiplicity is None else int(multiplicity)
    if k < 1 or copies < 1:
        raise ValueError("invalid packet mass data")
    if copies < escaping_multiplicity(k):
        raise ValueError("multiplicity does not enforce the modulus cap")
    return k * copies * Q**2
