"""Scalar theorems for normalized factors and robust blockwise Hardy tails."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Sequence


def normalized_matrix_difference_upper(
    reference_norm: float,
    difference_upper: float,
) -> float:
    """Bound ||B/||B||-B0/||B0|||| from ||B-B0||."""

    base = float(reference_norm)
    error = float(difference_upper)
    if base <= 0.0 or error < 0.0 or error >= base:
        raise ValueError("normalization is not separated from zero")
    if error == 0.0:
        return 0.0
    return math.nextafter(2.0 * error / (base - error), math.inf)


def volterra_power_defects(
    reference_power_bounds: Sequence[float],
    operator_error: float,
) -> tuple[float, ...]:
    r"""Majorize powers through the discrete Volterra identity.

    If C_k >= ||A0^k|| and ||A-A0|| <= eps, then

      D_k = eps sum_{j<k} C_{k-1-j}(C_j+D_j)

    bounds ||A^k-A0^k||.
    """

    bounds = tuple(float(value) for value in reference_power_bounds)
    epsilon = float(operator_error)
    if not bounds or bounds[0] < 1.0 or epsilon < 0.0:
        raise ValueError("invalid Volterra inputs")
    defects = [0.0]
    for k in range(1, len(bounds)):
        total = 0.0
        for j in range(k):
            term = bounds[k - 1 - j] * (bounds[j] + defects[j])
            total = math.nextafter(total + term, math.inf)
        defects.append(math.nextafter(epsilon * total, math.inf))
    return tuple(defects)


@dataclass(frozen=True)
class RobustBridgeLedger:
    block_horizon: int
    block_multiple: int
    total_horizon: int
    reference_block_contraction: float
    true_block_contraction_upper: float
    finite_difference_energy_squared_upper: float
    true_tail_energy_squared_upper: float
    reference_tail_energy_squared_upper: float
    difference_tail_energy_squared_upper: float
    bridge_energy_upper: float
    block_contraction_certified: bool

    def as_dict(self) -> dict[str, float | int | bool]:
        return asdict(self)


def robust_block_bridge(
    *,
    reference_power_bounds: Sequence[float],
    reference_state_prefix_bounds: Sequence[float],
    reference_source_norm: float,
    reference_observation_norm: float,
    operator_error: float,
    source_error: float,
    observation_error: float,
    block_horizon: int,
    block_multiple: int,
) -> RobustBridgeLedger:
    """Bound the full Hardy norm of a true/reference transfer difference."""

    m = int(block_horizon)
    blocks = int(block_multiple)
    if m <= 0 or blocks <= 0:
        raise ValueError("block horizons must be positive")
    total_horizon = m * blocks
    powers = tuple(float(value) for value in reference_power_bounds)
    states = tuple(float(value) for value in reference_state_prefix_bounds)
    if len(powers) < total_horizon + 1 or len(states) != m:
        raise ValueError("incomplete prefix bounds")
    x0 = float(reference_source_norm)
    y0 = float(reference_observation_norm)
    ea = float(operator_error)
    ex = float(source_error)
    ey = float(observation_error)
    if min(x0, y0, ea, ex, ey) < 0.0:
        raise ValueError("norm bounds must be nonnegative")

    defects = volterra_power_defects(powers, ea)
    true_powers = tuple(
        math.nextafter(powers[k] + defects[k], math.inf)
        for k in range(len(powers))
    )
    q0 = powers[m]
    q = true_powers[m]
    contraction = bool(q0 < 1.0 and q < 1.0)
    if not contraction:
        raise ValueError("true/reference block contraction did not close")

    x_true = math.nextafter(x0 + ex, math.inf)
    finite = 0.0
    for k in range(total_horizon):
        state_error = math.nextafter(
            defects[k] * x_true + powers[k] * ex,
            math.inf,
        )
        response_error = math.nextafter(
            ey * true_powers[k] * x_true + y0 * state_error,
            math.inf,
        )
        finite = math.nextafter(finite + response_error**2, math.inf)

    true_source_block = 0.0
    reference_source_block = 0.0
    for r in range(m):
        state_error = math.nextafter(
            defects[r] * x_true + powers[r] * ex,
            math.inf,
        )
        true_state = math.nextafter(states[r] + state_error, math.inf)
        true_source_block = math.nextafter(
            true_source_block + true_state**2, math.inf
        )
        reference_source_block = math.nextafter(
            reference_source_block + states[r] ** 2, math.inf
        )

    y_true = math.nextafter(y0 + ey, math.inf)
    true_tail = math.nextafter(
        y_true**2
        * q ** (2 * blocks)
        * true_source_block
        / (1.0 - q * q),
        math.inf,
    )
    reference_tail = math.nextafter(
        y0**2
        * q0 ** (2 * blocks)
        * reference_source_block
        / (1.0 - q0 * q0),
        math.inf,
    )
    difference_tail = math.nextafter(
        2.0 * (true_tail + reference_tail), math.inf
    )
    bridge = math.nextafter(math.sqrt(finite + difference_tail), math.inf)
    return RobustBridgeLedger(
        block_horizon=m,
        block_multiple=blocks,
        total_horizon=total_horizon,
        reference_block_contraction=q0,
        true_block_contraction_upper=q,
        finite_difference_energy_squared_upper=finite,
        true_tail_energy_squared_upper=true_tail,
        reference_tail_energy_squared_upper=reference_tail,
        difference_tail_energy_squared_upper=difference_tail,
        bridge_energy_upper=bridge,
        block_contraction_certified=contraction,
    )
