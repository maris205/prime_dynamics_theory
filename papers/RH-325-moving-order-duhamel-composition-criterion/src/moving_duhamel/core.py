"""Moving-order Markov and trace-observation Duhamel criteria for RH-325."""

from __future__ import annotations

import math
from typing import Sequence


U_C = 1.5436890126920764
R_FIXED = U_C - 1.0
LAMBDA = 2.0 * U_C * R_FIXED
TRACE_RADIUS = 1.4
ALIAS_EXPONENT = math.log(TRACE_RADIUS) / math.log(LAMBDA)
STABILITY_GROWTH_THRESHOLD = 1.0 - ALIAS_EXPONENT
PACKET_CONDITIONING_LOWER_EXPONENT = 0.25
QUARTER_POWER_SLACK = (
    STABILITY_GROWTH_THRESHOLD - PACKET_CONDITIONING_LOWER_EXPONENT
)


def _positive_sigma(sigma: float) -> float:
    sigma = float(sigma)
    if sigma <= 0.0 or sigma >= 1.0:
        raise ValueError("sigma must lie in (0, 1)")
    return sigma


def _probability_vector(values: Sequence[float]) -> tuple[float, ...]:
    vector = tuple(float(value) for value in values)
    if not vector:
        raise ValueError("a probability vector cannot be empty")
    if any(value < 0.0 for value in vector):
        raise ValueError("probability entries must be nonnegative")
    if not math.isclose(sum(vector), 1.0, rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError("probability entries must sum to one")
    return vector


def _markov_kernel(rows: Sequence[Sequence[float]]) -> tuple[tuple[float, ...], ...]:
    kernel = tuple(_probability_vector(row) for row in rows)
    if not kernel:
        raise ValueError("a Markov kernel cannot be empty")
    width = len(kernel[0])
    if len(kernel) != width or any(len(row) != width for row in kernel):
        raise ValueError("the finite reproduction kernels must be square")
    return kernel


def l1_distance(left: Sequence[float], right: Sequence[float]) -> float:
    """Return the unhalved finite ``L1`` distance."""

    left_values = tuple(float(value) for value in left)
    right_values = tuple(float(value) for value in right)
    if len(left_values) != len(right_values):
        raise ValueError("vectors must have the same length")
    return sum(abs(a - b) for a, b in zip(left_values, right_values))


def propagate(
    distribution: Sequence[float], kernel: Sequence[Sequence[float]]
) -> tuple[float, ...]:
    """Propagate a row probability vector through a row-stochastic kernel."""

    vector = _probability_vector(distribution)
    matrix = _markov_kernel(kernel)
    if len(vector) != len(matrix):
        raise ValueError("distribution and kernel dimensions do not match")
    return tuple(
        sum(vector[source] * matrix[source][target] for source in range(len(vector)))
        for target in range(len(vector))
    )


def max_row_l1_distance(
    physical: Sequence[Sequence[float]], affine: Sequence[Sequence[float]]
) -> float:
    """Return the largest conditional-row ``L1`` distance."""

    physical_kernel = _markov_kernel(physical)
    affine_kernel = _markov_kernel(affine)
    if len(physical_kernel) != len(affine_kernel):
        raise ValueError("kernel dimensions do not match")
    return max(
        l1_distance(physical_row, affine_row)
        for physical_row, affine_row in zip(physical_kernel, affine_kernel)
    )


def integrated_row_l1_distance(
    distribution: Sequence[float],
    physical: Sequence[Sequence[float]],
    affine: Sequence[Sequence[float]],
) -> float:
    """Average the conditional-row error against an incoming law."""

    vector = _probability_vector(distribution)
    physical_kernel = _markov_kernel(physical)
    affine_kernel = _markov_kernel(affine)
    if len(vector) != len(physical_kernel) or len(vector) != len(affine_kernel):
        raise ValueError("distribution and kernel dimensions do not match")
    return sum(
        vector[index] * l1_distance(physical_kernel[index], affine_kernel[index])
        for index in range(len(vector))
    )


def retained_path_duhamel_terms(
    initial: Sequence[float],
    physical_kernels: Sequence[Sequence[Sequence[float]]],
    affine_kernels: Sequence[Sequence[Sequence[float]]],
) -> tuple[float, ...]:
    """Return the exact norms of the retained-coordinate hybrid increments."""

    if len(physical_kernels) != len(affine_kernels):
        raise ValueError("kernel lists must have the same length")
    incoming = _probability_vector(initial)
    terms: list[float] = []
    for physical, affine in zip(physical_kernels, affine_kernels):
        terms.append(integrated_row_l1_distance(incoming, physical, affine))
        incoming = propagate(incoming, physical)
    return tuple(terms)


def retained_path_duhamel_bound(
    physical_initial: Sequence[float],
    physical_kernels: Sequence[Sequence[Sequence[float]]],
    affine_kernels: Sequence[Sequence[Sequence[float]]],
    *,
    affine_initial: Sequence[float] | None = None,
) -> float:
    """Return seed mismatch plus the retained-path Duhamel sum."""

    physical_seed = _probability_vector(physical_initial)
    affine_seed = _probability_vector(
        physical_seed if affine_initial is None else affine_initial
    )
    return l1_distance(physical_seed, affine_seed) + sum(
        retained_path_duhamel_terms(
            affine_seed, physical_kernels, affine_kernels
        )
    )


def path_distribution(
    initial: Sequence[float], kernels: Sequence[Sequence[Sequence[float]]]
) -> dict[tuple[int, ...], float]:
    """Enumerate a finite retained-coordinate path law."""

    vector = _probability_vector(initial)
    paths = {(state,): mass for state, mass in enumerate(vector) if mass > 0.0}
    dimension = len(vector)
    for raw_kernel in kernels:
        kernel = _markov_kernel(raw_kernel)
        if len(kernel) != dimension:
            raise ValueError("all reproduction kernels must use one state space")
        extended: dict[tuple[int, ...], float] = {}
        for path, mass in paths.items():
            for target, probability in enumerate(kernel[path[-1]]):
                if probability > 0.0:
                    new_path = path + (target,)
                    extended[new_path] = extended.get(new_path, 0.0) + mass * probability
        paths = extended
    return paths


def retained_path_l1(
    physical_initial: Sequence[float],
    physical_kernels: Sequence[Sequence[Sequence[float]]],
    affine_kernels: Sequence[Sequence[Sequence[float]]],
    *,
    affine_initial: Sequence[float] | None = None,
) -> float:
    """Return the exact finite retained-path ``L1`` distance."""

    if affine_initial is None:
        affine_initial = physical_initial
    physical = path_distribution(physical_initial, physical_kernels)
    affine = path_distribution(affine_initial, affine_kernels)
    keys = set(physical) | set(affine)
    return sum(abs(physical.get(key, 0.0) - affine.get(key, 0.0)) for key in keys)


def endpoint_composition_l1(
    physical_initial: Sequence[float],
    physical_kernels: Sequence[Sequence[Sequence[float]]],
    affine_kernels: Sequence[Sequence[Sequence[float]]],
    *,
    affine_initial: Sequence[float] | None = None,
) -> float:
    """Return the final-marginal ``L1`` error."""

    if affine_initial is None:
        affine_initial = physical_initial
    physical = _probability_vector(physical_initial)
    affine = _probability_vector(affine_initial)
    for kernel in physical_kernels:
        physical = propagate(physical, kernel)
    for kernel in affine_kernels:
        affine = propagate(affine, kernel)
    return l1_distance(physical, affine)


def alias_clock(sigma: float) -> float:
    """Return the continuous natural first-alias clock."""

    sigma = _positive_sigma(sigma)
    return math.log(1.0 / sigma) / (2.0 * math.log(LAMBDA))


def alias_scale(sigma: float) -> float:
    """Return ``R**(-2*k_sigma)`` on the continuous natural clock."""

    sigma = _positive_sigma(sigma)
    return TRACE_RADIUS ** (-2.0 * alias_clock(sigma))


def stability_power(growth_exponent: float) -> float:
    """Return the residual power ``1 - theta - gamma``."""

    return STABILITY_GROWTH_THRESHOLD - float(growth_exponent)


def moving_order_budget(
    sigma: float,
    *,
    leg_multiplier: float = 2.0,
    local_constant: float = 1.0,
    growth_exponent: float = 0.0,
) -> dict[str, float | int]:
    """Evaluate the ``O(k)``-leg majorant and first-alias target ratio."""

    sigma = _positive_sigma(sigma)
    leg_multiplier = float(leg_multiplier)
    local_constant = float(local_constant)
    growth_exponent = float(growth_exponent)
    if leg_multiplier <= 0.0 or local_constant < 0.0 or growth_exponent < 0.0:
        raise ValueError("budget parameters lie outside their natural domains")
    clock = alias_clock(sigma)
    legs = max(1, math.ceil(leg_multiplier * clock))
    amplification = sigma ** (-growth_exponent)
    majorant = legs * local_constant * sigma * amplification
    target = clock * alias_scale(sigma)
    ratio = majorant / target
    return {
        "sigma": sigma,
        "clock": clock,
        "legs": legs,
        "amplification": amplification,
        "majorant": majorant,
        "target": target,
        "normalized_ratio": ratio,
        "residual_power": stability_power(growth_exponent),
    }


def operator_duhamel_weights(
    physical_norms: Sequence[float],
    affine_norms: Sequence[float],
    *,
    observation_norm: float = 1.0,
) -> tuple[float, ...]:
    """Return the exact prefix/suffix weights in the product identity."""

    physical = tuple(float(value) for value in physical_norms)
    affine = tuple(float(value) for value in affine_norms)
    observation_norm = float(observation_norm)
    if len(physical) != len(affine):
        raise ValueError("norm lists must have the same length")
    if observation_norm < 0.0 or any(value < 0.0 for value in physical + affine):
        raise ValueError("norms must be nonnegative")
    weights = []
    for index in range(len(physical)):
        suffix = math.prod(physical[index + 1 :])
        prefix = math.prod(affine[:index])
        weights.append(observation_norm * suffix * prefix)
    return tuple(weights)


def operator_duhamel_terms(
    physical_norms: Sequence[float],
    affine_norms: Sequence[float],
    local_errors: Sequence[float],
    *,
    observation_norm: float = 1.0,
) -> tuple[float, ...]:
    """Return the individual norm-weighted local-error terms."""

    errors = tuple(float(value) for value in local_errors)
    weights = operator_duhamel_weights(
        physical_norms, affine_norms, observation_norm=observation_norm
    )
    if len(errors) != len(weights):
        raise ValueError("the local-error list has the wrong length")
    if any(value < 0.0 for value in errors):
        raise ValueError("local errors must be nonnegative")
    return tuple(weight * error for weight, error in zip(weights, errors))


def operator_duhamel_bound(
    physical_norms: Sequence[float],
    affine_norms: Sequence[float],
    local_errors: Sequence[float],
    *,
    observation_norm: float = 1.0,
) -> float:
    """Return the full trace-observation Duhamel majorant."""

    return sum(
        operator_duhamel_terms(
            physical_norms,
            affine_norms,
            local_errors,
            observation_norm=observation_norm,
        )
    )


def phase_transport_counterexample() -> dict[str, float]:
    """Return the sharp two-state same-seed composition counterexample."""

    seed = (1.0, 0.0)
    transport = ((0.0, 1.0), (0.0, 1.0))
    physical = ((1.0, 0.0), (0.0, 1.0))
    affine = ((1.0, 0.0), (1.0, 0.0))
    local_seed_error = l1_distance(
        propagate(seed, physical), propagate(seed, affine)
    )
    transported = propagate(seed, transport)
    transported_error = l1_distance(
        propagate(transported, physical), propagate(transported, affine)
    )
    composed_error = endpoint_composition_l1(
        seed, (transport, physical), (transport, affine)
    )
    return {
        "local_seed_error": local_seed_error,
        "transported_row_error": transported_error,
        "composed_endpoint_error": composed_error,
        "correct_duhamel_term": integrated_row_l1_distance(
            transported, physical, affine
        ),
    }


def cyclic_trace_counterexample(dimension: int) -> dict[str, float | int]:
    """Return the cyclic-shift trace gap with vanishing Markov row error."""

    dimension = int(dimension)
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    epsilon = 1.0 / dimension
    row_l1 = 2.0 * epsilon
    trace_gap = dimension * epsilon
    return {
        "dimension": dimension,
        "epsilon": epsilon,
        "max_row_l1": row_l1,
        "uniform_retained_path_l1": row_l1,
        "uniform_endpoint_l1": 0.0,
        "trace_gap": trace_gap,
        "trace_to_row_ratio": trace_gap / row_l1,
    }
