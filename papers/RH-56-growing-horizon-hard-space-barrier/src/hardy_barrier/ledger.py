"""Exact scalar ledgers used by RH-56."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


def _unit_interval(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or not 0.0 < result < 1.0:
        raise ValueError(f"{name} must lie in (0,1)")
    return result


@dataclass(frozen=True)
class StrongSpaceLedger:
    """Power cost of a two-stage strong-space Hardy estimate."""

    hardy_radius: float
    strong_rate: float
    entrance_power: float
    horizon_coefficient: float
    energy_power: float


def strong_space_ledger(
    hardy_radius: float, strong_rate: float, entrance_power: float
) -> StrongSpaceLedger:
    r"""Return the optimized two-stage exponent.

    If the strong-space prefactor is ``sigma^-p`` and its tail decays as
    ``theta^m``, choose ``M=p log(1/sigma)/log(1/theta)`` so that the
    prefactor has been mixed away.  The initial Hardy weight then costs
    ``sigma^-alpha`` with

    ``alpha = p log(1/r)/log(1/theta)``.
    """

    radius = _unit_interval(hardy_radius, "hardy_radius")
    rate = _unit_interval(strong_rate, "strong_rate")
    power = float(entrance_power)
    if not math.isfinite(power) or power < 0.0:
        raise ValueError("entrance_power must be finite and nonnegative")
    horizon = power / math.log(1.0 / rate)
    exponent = horizon * math.log(1.0 / radius)
    return StrongSpaceLedger(radius, rate, power, horizon, exponent)


def critical_strong_rate(
    hardy_radius: float, total_entrance_power: float, total_budget: float
) -> float:
    r"""Largest common decay rate allowed by a total exponent budget.

    The common-rate inequality is

    ``p_total log(1/r)/log(1/theta) <= budget``.
    """

    radius = _unit_interval(hardy_radius, "hardy_radius")
    power = float(total_entrance_power)
    budget = float(total_budget)
    if not math.isfinite(power) or power <= 0.0:
        raise ValueError("total_entrance_power must be positive")
    if not math.isfinite(budget) or budget <= 0.0:
        raise ValueError("total_budget must be positive")
    return radius ** (power / budget)


@dataclass(frozen=True)
class OverlapHardyBound:
    """Square-summed directional modal overlap bound."""

    weighted_overlap_sum: float
    energy_upper: float
    maximum_radius_ratio: float


def overlap_hardy_upper(
    modal_radii: Iterable[float], overlap_weights: Iterable[float], radius: float
) -> OverlapHardyBound:
    r"""Bound a Hardy energy by absolute modal overlaps.

    For a diagonalizable operator, write the normalized directional response
    as ``sum_j mu_j^m Z_j``.  Minkowski in ``ell^2_m(S_2)`` gives

    ``E <= sum_j ||Z_j||_S2 / sqrt(1-|mu_j/r|^2)``.

    The function evaluates this sufficient bound from nonnegative uppers for
    ``||Z_j||_S2``.  It deliberately does not infer those overlaps from a
    spectral radius or an eigenvector condition number.
    """

    hardy_radius = _unit_interval(radius, "radius")
    radii = tuple(float(value) for value in modal_radii)
    weights = tuple(float(value) for value in overlap_weights)
    if len(radii) != len(weights):
        raise ValueError("modal radii and overlap weights must have equal length")
    total = 0.0
    maximum = 0.0
    for modal_radius, weight in zip(radii, weights):
        if not math.isfinite(modal_radius) or modal_radius < 0.0:
            raise ValueError("modal radii must be finite and nonnegative")
        if modal_radius >= hardy_radius:
            raise ValueError("every modal radius must be below the Hardy radius")
        if not math.isfinite(weight) or weight < 0.0:
            raise ValueError("overlap weights must be finite and nonnegative")
        ratio = modal_radius / hardy_radius
        maximum = max(maximum, ratio)
        total += weight / math.sqrt(1.0 - ratio * ratio)
    return OverlapHardyBound(total, total, maximum)
