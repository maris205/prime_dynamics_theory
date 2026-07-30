from __future__ import annotations

import cmath


def minimal_rank(N: int) -> int:
    if N < 1:
        raise ValueError("N must be positive")
    return 2 * N


def prefix_moments(N: int, beta: float, n: int) -> complex:
    """Moments of the unique equality-case shell of degree N."""
    return -2 * beta**n if n % 2 == 0 and n <= 2 * N else 0.0


def ideal_factor(N: int, beta: float, z: complex) -> complex:
    q = (beta * z) ** 2
    return sum(q**j for j in range(N + 1))


def equality_roots(N: int, beta: float) -> list[complex]:
    return [beta * cmath.exp(1j * j * cmath.pi / (N + 1)) for j in range(1, N + 1)] + [
        beta * cmath.exp(-1j * j * cmath.pi / (N + 1)) for j in range(1, N + 1)
    ]
