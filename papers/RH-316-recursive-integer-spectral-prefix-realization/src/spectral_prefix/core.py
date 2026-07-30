from __future__ import annotations

import cmath
import math


def power_sum(spectrum: list[complex], order: int) -> complex:
    n = int(order)
    if n < 1:
        raise ValueError("order must be positive")
    return sum(value**n for value in spectrum)


def _packet_roots(order: int, multiplicity: int, moment: float) -> list[complex]:
    if moment == 0.0:
        return []
    d = int(order)
    copies = int(multiplicity)
    modulus = (abs(moment) / (d * copies)) ** (1.0 / d)
    argument = 0.0 if moment > 0.0 else math.pi
    roots = [modulus * cmath.exp(1j * (argument + 2.0 * math.pi * index) / d) for index in range(d)]
    return [root for root in roots for _ in range(copies)]


def construct_prefix_spectrum(target_moments: list[float], radius_cap: float) -> list[complex]:
    if radius_cap <= 0.0:
        raise ValueError("radius cap must be positive")
    spectrum: list[complex] = []
    for order, target in enumerate(target_moments, start=1):
        residual = complex(target) - power_sum(spectrum, order)
        if abs(residual.imag) > 1e-8:
            raise RuntimeError("real target recursion lost conjugate closure")
        real_residual = float(residual.real)
        if real_residual == 0.0:
            continue
        multiplicity = max(1, math.ceil(abs(real_residual) / (order * radius_cap**order)))
        spectrum.extend(_packet_roots(order, multiplicity, real_residual))
    return spectrum


def spectral_rank(spectrum: list[complex]) -> int:
    return len(spectrum)


def squared_mass(spectrum: list[complex]) -> float:
    return float(sum(abs(value) ** 2 for value in spectrum))
