import math


def normalizer_lower(sigma_max: float) -> float:
    """Minimum row mass on the archived center range, attained at center 1."""
    return 0.5 * math.erf(math.sqrt(2) / sigma_max)


def neumann_resolvent_bound(base_bound: float, operator_perturbation: float) -> float:
    product = base_bound * operator_perturbation
    if product >= 1:
        raise ValueError("perturbation is outside the Neumann radius")
    return base_bound / (1 - product)
