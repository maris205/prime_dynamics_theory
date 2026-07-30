def hardy_lower(power: int, hardy_radius: float = 0.85) -> float:
    if power < 1:
        raise ValueError("power must be positive")
    return hardy_radius ** (-power)


def fixed_rank_contour_compatible(ranks: list[int]) -> bool:
    return len(set(ranks)) <= 1
