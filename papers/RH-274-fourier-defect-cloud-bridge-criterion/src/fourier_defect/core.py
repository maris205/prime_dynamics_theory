from __future__ import annotations

import cmath
import math

BETA = 1.0 / (0.85 * math.sqrt(1.678573510428322))


def ideal_roots(N: int, beta: float = BETA, shift: float = 0.0) -> list[complex]:
    L = N + 1
    positive = [beta * cmath.exp(1j * (j * math.pi / L + shift)) for j in range(1, L)]
    return positive + [z.conjugate() for z in positive]


def common_shift_moment(N: int, n: int, shift: float, beta: float = BETA) -> complex:
    return sum(z**n for z in ideal_roots(N, beta, shift))


def moment_error_bound(n: int, beta: float, phase_l1: float, radial_l1: float = 0.0, radius_cap: float | None = None) -> float:
    cap = beta if radius_cap is None else radius_cap
    return 2 * n * cap**n * phase_l1 + 2 * n * cap ** (n - 1) * radial_l1
