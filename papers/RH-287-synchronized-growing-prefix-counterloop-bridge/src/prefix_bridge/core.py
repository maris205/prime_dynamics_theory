from __future__ import annotations


def admissible_level(errors: list[float]) -> int:
    """Largest j with max(errors[:j-1]) <= 1/j for orders 2,...,j."""

    best = 1
    running = 0.0
    for index, error in enumerate(errors, start=2):
        running = max(running, abs(float(error)))
        if running <= 1.0 / index:
            best = index
    return best


def prefix_weight_upper(max_error: float, horizon: int, radius: float) -> float:
    if max_error < 0.0 or horizon < 2 or radius <= 0.0:
        raise ValueError("invalid prefix parameters")
    return max_error * sum(radius**order / order for order in range(2, horizon + 1))
