"""Scalar forms of the RH-85 packet bounds."""

from __future__ import annotations

import math


def snapshot_transfer_bound(power_norm: float, snapshot_tail: float) -> float:
    """Outward-rounded propagated Hilbert--Schmidt residual."""

    norm = float(power_norm)
    tail = float(snapshot_tail)
    if norm < 0.0 or tail < 0.0:
        raise ValueError("bounds must be nonnegative")
    return math.nextafter(norm * tail, math.inf)


def captured_energy_lower(relative_residual: float) -> float:
    """Lower bound on captured energy from a relative residual upper."""

    residual = float(relative_residual)
    if not 0.0 <= residual <= 1.0:
        raise ValueError("relative residual must lie in [0,1]")
    return math.nextafter(1.0 - residual * residual, -math.inf)


def prefix_counterexample(horizon: int) -> dict[str, float]:
    """Closed-form rank-one failure of the unweighted prefix Gramian.

    A=diag(1/2,1), S=diag(sqrt(2(M+1)),1).  The prefix Gramian through M
    selects the first coordinate, while the terminal state is asymptotically
    concentrated on the second coordinate.
    """

    m = int(horizon)
    if m < 1:
        raise ValueError("positive horizon required")
    k2 = 2.0 * (m + 1.0)
    first_prefix = k2 * (1.0 - 4.0 ** (-(m + 1))) / (1.0 - 0.25)
    second_prefix = m + 1.0
    first_terminal = k2 * 4.0 ** (-m)
    second_terminal = 1.0
    missed_relative = math.sqrt(second_terminal / (first_terminal + second_terminal))
    return {
        "first_prefix_energy": first_prefix,
        "second_prefix_energy": second_prefix,
        "prefix_selects_transient": float(first_prefix > second_prefix),
        "terminal_missed_relative": missed_relative,
    }
