"""Sharp global wedge-Lipschitz bounds and their Weyl domination."""

from __future__ import annotations

import math
import numpy as np


def _spectrum(values: list[float] | tuple[float, ...] | np.ndarray) -> np.ndarray:
    singular = np.asarray(values, dtype=float)
    if singular.ndim != 1 or singular.size < 4:
        raise ValueError("at least four singular values are required")
    if np.any(~np.isfinite(singular)) or np.any(singular < 0.0):
        raise ValueError("singular values must be finite and nonnegative")
    return np.sort(singular)[::-1]


def _radius(value: float) -> float:
    radius = float(value)
    if not math.isfinite(radius) or radius < 0.0:
        raise ValueError("the perturbation radius must be finite and nonnegative")
    return radius


def normalized_four_volume(values: list[float] | tuple[float, ...] | np.ndarray) -> float:
    """Return ``s1*s2*s3*s4/s1**4``."""
    singular = _spectrum(values)
    if singular[0] == 0.0:
        return 0.0
    return float(np.prod(singular[:4]) / singular[0] ** 4)


def wedge_lipschitz_radius(operator_norm: float, perturbation_radius: float, order: int = 4) -> float:
    """Return the sharp norm-only radius for ``wedge^order``.

    If ``||A||<=alpha`` and ``||E||<=delta``, multilinearity gives
    ``||wedge^k(A+E)-wedge^k(A)|| <= (alpha+delta)^k-alpha^k``.
    """
    alpha = float(operator_norm)
    delta = _radius(perturbation_radius)
    degree = int(order)
    if not math.isfinite(alpha) or alpha < 0.0:
        raise ValueError("the operator norm must be finite and nonnegative")
    if degree < 1:
        raise ValueError("the exterior order must be positive")
    return float((alpha + delta) ** degree - alpha**degree)


def global_wedge_lower_bound(
    recent_singular_values: list[float] | tuple[float, ...] | np.ndarray,
    perturbation_radius: float,
) -> dict[str, float]:
    """Lower-bound normalized four-volume through the global wedge map."""
    singular = _spectrum(recent_singular_values)
    delta = _radius(perturbation_radius)
    alpha = float(singular[0])
    recent_volume = float(np.prod(singular[:4]))
    loss = wedge_lipschitz_radius(alpha, delta, 4)
    denominator = (alpha + delta) ** 4
    lower = max(0.0, recent_volume - loss) / denominator if denominator else 0.0
    return {
        "recent_exterior_norm": recent_volume,
        "global_wedge_loss": loss,
        "normalized_lower": float(lower),
        "relative_radius": delta / alpha if alpha else math.inf,
    }


def product_weyl_lower_bound(
    recent_singular_values: list[float] | tuple[float, ...] | np.ndarray,
    perturbation_radius: float,
) -> float:
    """Return the usual singular-value-product Weyl lower bound."""
    singular = _spectrum(recent_singular_values)
    delta = _radius(perturbation_radius)
    denominator = (singular[0] + delta) ** 4
    if denominator == 0.0:
        return 0.0
    return float(np.prod(np.maximum(singular[:4] - delta, 0.0)) / denominator)


def positivity_radius(values: list[float] | tuple[float, ...] | np.ndarray) -> dict[str, float]:
    """Compare maximum positive radii for global-wedge and product-Weyl routes."""
    singular = _spectrum(values)
    alpha = float(singular[0])
    if alpha == 0.0:
        return {"global": 0.0, "product_weyl": 0.0, "relative_efficiency": 0.0}
    volume = normalized_four_volume(singular)
    global_radius = alpha * ((1.0 + volume) ** 0.25 - 1.0)
    direct_radius = float(singular[3])
    return {
        "global": global_radius,
        "product_weyl": direct_radius,
        "relative_efficiency": global_radius / direct_radius if direct_radius else 0.0,
    }


def sharp_scalar_example(operator_norm: float, perturbation_radius: float, order: int = 4) -> dict[str, float]:
    """Scalar identity example attaining the global Lipschitz radius."""
    alpha = float(operator_norm)
    delta = _radius(perturbation_radius)
    degree = int(order)
    if not math.isfinite(alpha) or alpha < 0.0 or degree < 1:
        raise ValueError("invalid scalar example parameters")
    exact = abs((alpha + delta) ** degree - alpha**degree)
    bound = wedge_lipschitz_radius(alpha, delta, degree)
    return {"exact_difference": exact, "bound": bound, "error": abs(exact - bound)}
