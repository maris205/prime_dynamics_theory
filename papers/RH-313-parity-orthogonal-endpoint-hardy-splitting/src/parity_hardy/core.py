from __future__ import annotations


def singular_coefficient(order: int) -> float:
    n = int(order)
    if n < 1:
        raise ValueError("order must be positive")
    return 0.0 if n == 1 else -1.0 / n


def parity_projection(coefficients: list[complex], parity: str) -> list[complex]:
    if parity not in {"even", "odd"}:
        raise ValueError("parity must be even or odd")
    keep = 0 if parity == "even" else 1
    return [value if index % 2 == keep else 0.0 for index, value in enumerate(coefficients)]


def split_energy(coefficients: list[complex]) -> tuple[float, float, float]:
    even = sum(abs(value) ** 2 for index, value in enumerate(coefficients) if index % 2 == 0)
    odd = sum(abs(value) ** 2 for index, value in enumerate(coefficients) if index % 2 == 1)
    return float(even), float(odd), float(even + odd)
