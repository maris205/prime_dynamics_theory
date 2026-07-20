"""Deterministic finite-horizon and infinite-tail Hardy certificates."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np


def _square_matrix(value: np.ndarray, name: str) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError(f"{name} must be square")
    return result


def _source_matrix(value: np.ndarray, dimension: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result[:, None]
    if result.ndim != 2 or result.shape[0] != dimension:
        raise ValueError("source has incompatible shape")
    return result


def _observation_matrix(value: np.ndarray, dimension: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result[None, :]
    if result.ndim != 2 or result.shape[1] != dimension:
        raise ValueError("observation has incompatible shape")
    return result


def _positive_horizon(value: int) -> int:
    result = int(value)
    if result < 1:
        raise ValueError("horizon must be positive")
    return result


@dataclass(frozen=True)
class DeterministicHardyCertificate:
    """Finite exact trace sum plus an explicit infinite-tail upper."""

    horizon: int
    main_energy_squared: float
    block_power_norm: float
    contraction_margin: float
    source_block_energy: float
    simple_tail_upper: float
    stein_tail_upper: float
    energy_squared_upper: float
    energy_upper: float


def deterministic_main_sum(
    operator: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
    horizon: int,
) -> float:
    r"""Return ``sum_(m=0)^(M-1) ||Y A^m X||_F^2`` exactly by columns.

    The word ``exactly`` refers to the deterministic trace identity rather
    than arithmetic rounding: no random trace estimator is used.
    """

    a = _square_matrix(operator, "operator")
    x = _source_matrix(source, a.shape[0])
    y = _observation_matrix(observation, a.shape[0])
    count = _positive_horizon(horizon)
    state = x.copy()
    total = 0.0
    for _ in range(count):
        image = y @ state
        total += float(np.linalg.norm(image, "fro") ** 2)
        state = a @ state
    return total


def finite_source_gramian(
    operator: np.ndarray, source: np.ndarray, horizon: int
) -> np.ndarray:
    r"""Return ``S_M=sum_(m=0)^(M-1) A^m X X^* (A^*)^m``."""

    a = _square_matrix(operator, "operator")
    x = _source_matrix(source, a.shape[0])
    count = _positive_horizon(horizon)
    state = x.copy()
    result = np.zeros_like(a)
    for _ in range(count):
        result += state @ state.conjugate().T
        state = a @ state
    return 0.5 * (result + result.conjugate().T)


def deterministic_hardy_certificate(
    operator: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
    horizon: int,
) -> DeterministicHardyCertificate:
    r"""Certify the full Hardy energy when ``q_M=||A^M||_2<1``.

    Two valid tail estimates are evaluated.  The simple estimate groups the
    time series into blocks.  The sharper Stein estimate uses

    ``alpha=||A^M S_M (A^*)^M||_2/(1-q_M^2)``.

    Their minimum is still an upper bound and is reported as the certificate.
    """

    a = _square_matrix(operator, "operator")
    x = _source_matrix(source, a.shape[0])
    y = _observation_matrix(observation, a.shape[0])
    count = _positive_horizon(horizon)
    power = np.linalg.matrix_power(a, count)
    q = float(np.linalg.norm(power, 2))
    margin = 1.0 - q * q
    if margin <= 0.0:
        raise ValueError("the selected block power is not a contraction")

    main = deterministic_main_sum(a, x, y, count)
    source_gramian = finite_source_gramian(a, x, count)
    source_block_energy = float(np.trace(source_gramian).real)
    observation_norm_squared = float(np.linalg.norm(y, "fro") ** 2)
    simple_tail = (
        float(np.linalg.norm(y, 2) ** 2)
        * q
        * q
        * source_block_energy
        / margin
    )
    residual = power @ source_gramian @ power.conjugate().T
    residual = 0.5 * (residual + residual.conjugate().T)
    stein_tail = (
        float(np.linalg.norm(residual, 2))
        * observation_norm_squared
        / margin
    )
    tail = min(simple_tail, stein_tail)
    upper_squared = main + tail
    return DeterministicHardyCertificate(
        horizon=count,
        main_energy_squared=main,
        block_power_norm=q,
        contraction_margin=margin,
        source_block_energy=source_block_energy,
        simple_tail_upper=simple_tail,
        stein_tail_upper=stein_tail,
        energy_squared_upper=upper_squared,
        energy_upper=math.sqrt(max(upper_squared, 0.0)),
    )


@dataclass(frozen=True)
class FiniteHorizonPerturbationBound:
    """Telescoping upper for two finite-horizon Hardy trace sums."""

    horizon: int
    reference_energy: float
    perturbed_energy: float
    sequence_difference_upper: float
    energy_squared_difference_upper: float


def finite_horizon_perturbation_bound(
    operator: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
    perturbed_operator: np.ndarray,
    perturbed_source: np.ndarray,
    perturbed_observation: np.ndarray,
    horizon: int,
    *,
    operator_defect_upper: float | None = None,
    source_defect_upper: float | None = None,
    observation_defect_upper: float | None = None,
) -> FiniteHorizonPerturbationBound:
    r"""Bound finite sums using ``A^m-B^m`` telescoping.

    Optional defect uppers permit outward-rounded or analytic matrix bounds.
    If omitted, the corresponding binary64 spectral/Frobenius norm is used.
    """

    a = _square_matrix(operator, "operator")
    b = _square_matrix(perturbed_operator, "perturbed_operator")
    if a.shape != b.shape:
        raise ValueError("operators have incompatible shapes")
    x = _source_matrix(source, a.shape[0])
    xt = _source_matrix(perturbed_source, a.shape[0])
    y = _observation_matrix(observation, a.shape[0])
    yt = _observation_matrix(perturbed_observation, a.shape[0])
    if x.shape[1] != xt.shape[1] or y.shape[0] != yt.shape[0]:
        raise ValueError("directional factors have incompatible shapes")
    count = _positive_horizon(horizon)

    da = (
        float(operator_defect_upper)
        if operator_defect_upper is not None
        else float(np.linalg.norm(a - b, 2))
    )
    dx = (
        float(source_defect_upper)
        if source_defect_upper is not None
        else float(np.linalg.norm(x - xt, "fro"))
    )
    dy = (
        float(observation_defect_upper)
        if observation_defect_upper is not None
        else float(np.linalg.norm(y - yt, 2))
    )
    if min(da, dx, dy) < 0.0 or not all(
        math.isfinite(value) for value in (da, dx, dy)
    ):
        raise ValueError("defect uppers must be finite and nonnegative")

    norm_x = float(np.linalg.norm(x, "fro"))
    norm_xt = float(np.linalg.norm(xt, "fro"))
    norm_y = float(np.linalg.norm(y, 2))
    norm_yt = float(np.linalg.norm(yt, 2))
    powers_a = [np.eye(a.shape[0], dtype=np.complex128)]
    powers_b = [np.eye(b.shape[0], dtype=np.complex128)]
    for _ in range(1, count):
        powers_a.append(a @ powers_a[-1])
        powers_b.append(b @ powers_b[-1])
    norms_a = [float(np.linalg.norm(value, 2)) for value in powers_a]
    norms_b = [float(np.linalg.norm(value, 2)) for value in powers_b]
    reference_squares = []
    perturbed_squares = []
    difference_squares = []
    for power in range(count):
        a_power = norms_a[power]
        b_power = norms_b[power]
        if power == 0:
            power_difference = 0.0
        else:
            power_difference = da * sum(
                norms_a[power - 1 - index] * norms_b[index]
                for index in range(power)
            )
        reference_bound = norm_y * a_power * norm_x
        perturbed_bound = norm_yt * b_power * norm_xt
        difference = (
            dy * a_power * norm_x
            + norm_yt * power_difference * norm_x
            + norm_yt * b_power * dx
        )
        reference_squares.append(reference_bound * reference_bound)
        perturbed_squares.append(perturbed_bound * perturbed_bound)
        difference_squares.append(difference * difference)

    reference_energy = math.sqrt(sum(reference_squares))
    perturbed_energy = math.sqrt(sum(perturbed_squares))
    sequence_difference = math.sqrt(sum(difference_squares))
    squared_difference = sequence_difference * (
        reference_energy + perturbed_energy
    )
    return FiniteHorizonPerturbationBound(
        horizon=count,
        reference_energy=reference_energy,
        perturbed_energy=perturbed_energy,
        sequence_difference_upper=sequence_difference,
        energy_squared_difference_upper=squared_difference,
    )


def power_defect_upper(
    operator_norm: float,
    perturbed_operator_norm: float,
    operator_defect: float,
    horizon: int,
) -> float:
    r"""Return the telescoping bound for ``||A^M-B^M||``."""

    a = float(operator_norm)
    b = float(perturbed_operator_norm)
    defect = float(operator_defect)
    count = _positive_horizon(horizon)
    if min(a, b, defect) < 0.0:
        raise ValueError("norm bounds must be nonnegative")
    return defect * sum(a ** (count - 1 - index) * b**index for index in range(count))


def semigroup_power_defect_upper(
    reference_power_norms: list[float] | tuple[float, ...],
    perturbed_power_norms: list[float] | tuple[float, ...],
    operator_defect: float,
    horizon: int,
) -> float:
    r"""Use finite-time semigroup ledgers in the power telescoping bound.

    Each ledger must contain upper bounds for powers zero through ``M-1``.
    This avoids the usually wasteful replacement ``||A^j|| <= ||A||^j``.
    """

    count = _positive_horizon(horizon)
    left = tuple(float(value) for value in reference_power_norms)
    right = tuple(float(value) for value in perturbed_power_norms)
    defect = float(operator_defect)
    if len(left) < count or len(right) < count:
        raise ValueError("power ledgers must contain powers zero through M-1")
    if defect < 0.0 or min(left[:count] + right[:count]) < 0.0:
        raise ValueError("norm bounds must be nonnegative")
    return defect * sum(
        left[count - 1 - index] * right[index] for index in range(count)
    )


def full_energy_squared_perturbation_upper(
    finite_squared_difference_upper: float,
    reference_tail_upper: float,
    perturbed_tail_upper: float,
) -> float:
    """Promote a finite-horizon difference to the two infinite energies."""

    finite = float(finite_squared_difference_upper)
    left_tail = float(reference_tail_upper)
    right_tail = float(perturbed_tail_upper)
    if min(finite, left_tail, right_tail) < 0.0:
        raise ValueError("energy bounds must be nonnegative")
    return finite + left_tail + right_tail


def transfer_block_contraction(
    reference_power_norm: float,
    operator_norm: float,
    perturbed_operator_norm: float,
    operator_defect: float,
    horizon: int,
) -> float:
    r"""Transfer a block contraction to a perturbed operator."""

    return float(reference_power_norm) + power_defect_upper(
        operator_norm,
        perturbed_operator_norm,
        operator_defect,
        horizon,
    )


def transfer_block_contraction_from_ledgers(
    reference_power_norm: float,
    reference_power_norms: list[float] | tuple[float, ...],
    perturbed_power_norms: list[float] | tuple[float, ...],
    operator_defect: float,
    horizon: int,
) -> float:
    """Transfer ``||A^M||<1`` using finite-time semigroup norm ledgers."""

    return float(reference_power_norm) + semigroup_power_defect_upper(
        reference_power_norms,
        perturbed_power_norms,
        operator_defect,
        horizon,
    )
