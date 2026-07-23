"""Gap-aware quotient prices and stopped-budget bookkeeping."""

from __future__ import annotations

import math


def _finite_nonnegative(value: float, name: str) -> float:
    number = float(value)
    if not math.isfinite(number) or number < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return number


def gap_weighted_loss(coupling_frobenius: float, gap: float) -> float:
    """Return the local quotient price ||C||_F^2 / gap."""
    coupling = _finite_nonnegative(coupling_frobenius, "coupling")
    spectral_gap = float(gap)
    if not math.isfinite(spectral_gap) or spectral_gap <= 0.0:
        raise ValueError("gap must be finite and positive")
    return math.nextafter(coupling**2 / spectral_gap, math.inf)


def total_debit_upper(
    candidate_count: int,
    propagation_factor: float,
    coupling_frobenius: float,
    gap: float,
) -> float:
    """Bound the total debit for a uniform candidate envelope."""
    if int(candidate_count) < 0:
        raise ValueError("candidate count must be nonnegative")
    propagation = _finite_nonnegative(propagation_factor, "propagation factor")
    local = gap_weighted_loss(coupling_frobenius, gap)
    return math.nextafter(int(candidate_count) * propagation * local, math.inf)


def stopped_allowance(endpoint_gate: float, reference_lower: float, baseline_upper: float, safety_fraction: float) -> float:
    """Return rho*(Gamma R_- - H_0^+)_+, with validation."""
    gate = float(endpoint_gate)
    reference = _finite_nonnegative(reference_lower, "reference lower")
    baseline = _finite_nonnegative(baseline_upper, "baseline upper")
    fraction = float(safety_fraction)
    if not math.isfinite(gate) or gate <= 1.0:
        raise ValueError("endpoint gate must exceed one")
    if not math.isfinite(fraction) or not 0.0 <= fraction < 1.0:
        raise ValueError("safety fraction must lie in [0,1)")
    return fraction * max(0.0, gate * reference - baseline)


def total_price_fits(total_debit: float, allowance: float) -> bool:
    """Check the strict stopped-budget admission inequality."""
    debit = _finite_nonnegative(total_debit, "total debit")
    budget = _finite_nonnegative(allowance, "allowance")
    return debit <= budget


def quotient_decay_exponent(coupling_decay: float, gap_decay: float, propagation_growth: float) -> float:
    """Return signed sigma exponent 2*chi-gamma-p of a propagated price."""
    chi = float(coupling_decay)
    gamma = float(gap_decay)
    propagation = float(propagation_growth)
    if not all(math.isfinite(value) for value in (chi, gamma, propagation)):
        raise ValueError("exponents must be finite")
    return 2.0 * chi - gamma - propagation


def quotient_growth_power(coupling_decay: float, gap_decay: float, propagation_growth: float) -> float:
    """Return the nonnegative growth power of a propagated quotient price."""
    return max(0.0, -quotient_decay_exponent(coupling_decay, gap_decay, propagation_growth))
