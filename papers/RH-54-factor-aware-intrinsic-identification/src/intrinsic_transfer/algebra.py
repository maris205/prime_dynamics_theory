"""Exact finite-dimensional inequalities used by RH-54."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np


def _nonnegative(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def _positive(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return result


def _square_matrix(value: np.ndarray, name: str) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError(f"{name} must be square")
    if np.any(~np.isfinite(result)):
        raise ValueError(f"{name} must be finite")
    return result


def _source_matrix(value: np.ndarray, dimension: int, name: str) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result[:, None]
    if result.ndim != 2 or result.shape[0] != dimension:
        raise ValueError(f"{name} has incompatible shape")
    if np.any(~np.isfinite(result)):
        raise ValueError(f"{name} must be finite")
    return result


def _observation_matrix(
    value: np.ndarray, dimension: int, name: str
) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result[None, :]
    if result.ndim != 2 or result.shape[1] != dimension:
        raise ValueError(f"{name} has incompatible shape")
    if np.any(~np.isfinite(result)):
        raise ValueError(f"{name} must be finite")
    return result


def normalized_hilbert_schmidt_defect_upper(
    reference_norm: float, defect_upper: float
) -> float:
    r"""Bound ``||B/||B||_F-C/||C||_F||_F`` by ``2 eps/||B||_F``.

    The premise ``eps < ||B||_F`` keeps the perturbed coupling nonzero.  The
    bound itself follows from the reverse triangle inequality and does not
    depend on the ambient dimensions.
    """

    norm = _positive(reference_norm, "reference_norm")
    defect = _nonnegative(defect_upper, "defect_upper")
    if defect >= norm:
        raise ValueError("defect_upper must be smaller than reference_norm")
    return 2.0 * defect / norm


@dataclass(frozen=True)
class ContourComponent:
    """One contour contribution to a Riesz perturbation ledger."""

    length: float
    maximum_modulus: float
    reference_resolvent_upper: float
    perturbed_resolvent_upper: float

    def checked(self) -> "ContourComponent":
        return ContourComponent(
            _positive(self.length, "length"),
            _nonnegative(self.maximum_modulus, "maximum_modulus"),
            _positive(
                self.reference_resolvent_upper,
                "reference_resolvent_upper",
            ),
            _positive(
                self.perturbed_resolvent_upper,
                "perturbed_resolvent_upper",
            ),
        )


def contour_riesz_defect_upper(
    operator_defect: float,
    components: Iterable[ContourComponent],
) -> tuple[float, float]:
    r"""Return projector and weighted-Riesz perturbation uppers.

    For common isolating contours, the resolvent identity gives

    ``eps_P <= sum |Gamma| M Mtilde eps_T/(2 pi)`` and
    ``eps_W <= sum |Gamma| max|z| M Mtilde eps_T/(2 pi)``.

    Keeping both outputs is essential: the complement enters a source or
    observation, whereas the weighted term enters the deflated bulk.
    """

    defect = _nonnegative(operator_defect, "operator_defect")
    records = [component.checked() for component in components]
    if not records:
        raise ValueError("at least one contour component is required")
    projector = 0.0
    weighted = 0.0
    for record in records:
        common = (
            record.length
            * record.reference_resolvent_upper
            * record.perturbed_resolvent_upper
            * defect
            / (2.0 * math.pi)
        )
        projector += common
        weighted += record.maximum_modulus * common
    return projector, weighted


@dataclass(frozen=True)
class FactorAwareDefects:
    """Defect uppers for one intrinsic Hardy triple ``(A,X,Y)``."""

    operator: float
    source: float
    observation: float
    normalized_coupling: float


def factor_aware_left_defects(
    *,
    hardy_radius: float,
    markov_defect: float,
    weighted_riesz_defect: float,
    projector_defect: float,
    coupling_norm: float,
    coupling_defect: float,
    perturbed_complement_norm: float,
) -> FactorAwareDefects:
    r"""Compose sparse/full defects for ``(N_f/r,Q_f U Bhat,U*)``."""

    radius = _positive(hardy_radius, "hardy_radius")
    normalized = normalized_hilbert_schmidt_defect_upper(
        coupling_norm, coupling_defect
    )
    operator = (
        _nonnegative(markov_defect, "markov_defect")
        + _nonnegative(weighted_riesz_defect, "weighted_riesz_defect")
    ) / radius
    source = _nonnegative(projector_defect, "projector_defect") + (
        _nonnegative(perturbed_complement_norm, "perturbed_complement_norm")
        * normalized
    )
    return FactorAwareDefects(
        operator=operator,
        source=source,
        observation=0.0,
        normalized_coupling=normalized,
    )


def factor_aware_right_defects(
    *,
    hardy_radius: float,
    markov_defect: float,
    weighted_riesz_defect: float,
    projector_defect: float,
    coupling_norm: float,
    coupling_defect: float,
) -> FactorAwareDefects:
    r"""Compose sparse/full defects for ``(N_c*/r,Chat*,Q_c*)``."""

    radius = _positive(hardy_radius, "hardy_radius")
    normalized = normalized_hilbert_schmidt_defect_upper(
        coupling_norm, coupling_defect
    )
    operator = (
        _nonnegative(markov_defect, "markov_defect")
        + _nonnegative(weighted_riesz_defect, "weighted_riesz_defect")
    ) / radius
    return FactorAwareDefects(
        operator=operator,
        source=normalized,
        observation=_nonnegative(projector_defect, "projector_defect"),
        normalized_coupling=normalized,
    )


def semigroup_power_defect_upper(
    reference_power_norms: Iterable[float],
    perturbed_power_norms: Iterable[float],
    operator_defect: float,
    horizon: int,
) -> float:
    r"""Apply the exact power telescoping identity to finite-time ledgers."""

    count = int(horizon)
    if count < 1:
        raise ValueError("horizon must be positive")
    left = tuple(
        _nonnegative(value, "reference power norm")
        for value in reference_power_norms
    )
    right = tuple(
        _nonnegative(value, "perturbed power norm")
        for value in perturbed_power_norms
    )
    if len(left) < count or len(right) < count:
        raise ValueError("ledgers must contain powers zero through M-1")
    defect = _nonnegative(operator_defect, "operator_defect")
    return defect * sum(
        left[count - 1 - index] * right[index]
        for index in range(count)
    )


def transfer_block_contraction(
    reference_block_norm: float,
    reference_power_norms: Iterable[float],
    perturbed_power_norms: Iterable[float],
    operator_defect: float,
    horizon: int,
) -> float:
    """Upper-bound the perturbed block norm by ``q_M+d_M``."""

    return _nonnegative(reference_block_norm, "reference_block_norm") + (
        semigroup_power_defect_upper(
            reference_power_norms,
            perturbed_power_norms,
            operator_defect,
            horizon,
        )
    )


@dataclass(frozen=True)
class FiniteDirectionalBound:
    """RH-53 finite-time sequence and squared-energy perturbation upper."""

    horizon: int
    sequence_difference_upper: float
    energy_squared_difference_upper: float
    reference_norm_upper: float
    perturbed_norm_upper: float
    power_defect_uppers: tuple[float, ...]


def finite_directional_perturbation_bound(
    operator: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
    perturbed_operator: np.ndarray,
    perturbed_source: np.ndarray,
    perturbed_observation: np.ndarray,
    horizon: int,
    *,
    operator_defect_upper: float,
    source_defect_upper: float,
    observation_defect_upper: float,
    reference_power_norms: Iterable[float] | None = None,
    perturbed_power_norms: Iterable[float] | None = None,
) -> FiniteDirectionalBound:
    """Propagate factor-aware defects through a finite Hardy trace."""

    a = _square_matrix(operator, "operator")
    at = _square_matrix(perturbed_operator, "perturbed_operator")
    if a.shape != at.shape:
        raise ValueError("operators have incompatible shapes")
    x = _source_matrix(source, a.shape[0], "source")
    xt = _source_matrix(perturbed_source, a.shape[0], "perturbed_source")
    y = _observation_matrix(observation, a.shape[0], "observation")
    yt = _observation_matrix(
        perturbed_observation, a.shape[0], "perturbed_observation"
    )
    if x.shape[1] != xt.shape[1] or y.shape[0] != yt.shape[0]:
        raise ValueError("factors have incompatible shapes")
    count = int(horizon)
    if count < 1:
        raise ValueError("horizon must be positive")
    da = _nonnegative(operator_defect_upper, "operator_defect_upper")
    dx = _nonnegative(source_defect_upper, "source_defect_upper")
    dy = _nonnegative(observation_defect_upper, "observation_defect_upper")

    if reference_power_norms is None or perturbed_power_norms is None:
        powers_a = [np.eye(a.shape[0], dtype=np.complex128)]
        powers_at = [np.eye(a.shape[0], dtype=np.complex128)]
        for _ in range(1, count):
            powers_a.append(a @ powers_a[-1])
            powers_at.append(at @ powers_at[-1])
        norms_a = tuple(float(np.linalg.norm(value, 2)) for value in powers_a)
        norms_at = tuple(float(np.linalg.norm(value, 2)) for value in powers_at)
    else:
        norms_a = tuple(float(value) for value in reference_power_norms)
        norms_at = tuple(float(value) for value in perturbed_power_norms)
        if len(norms_a) < count or len(norms_at) < count:
            raise ValueError("power ledgers must contain powers zero through M-1")

    norm_x = float(np.linalg.norm(x, "fro"))
    norm_xt = float(np.linalg.norm(xt, "fro"))
    norm_y = float(np.linalg.norm(y, 2))
    norm_yt = float(np.linalg.norm(yt, 2))
    differences = []
    reference_terms = []
    perturbed_terms = []
    power_defects = []
    for power in range(count):
        d_power = 0.0 if power == 0 else da * sum(
            norms_a[power - 1 - index] * norms_at[index]
            for index in range(power)
        )
        power_defects.append(d_power)
        differences.append(
            dy * norms_a[power] * norm_x
            + norm_yt * d_power * norm_x
            + norm_yt * norms_at[power] * dx
        )
        reference_terms.append(norm_y * norms_a[power] * norm_x)
        perturbed_terms.append(norm_yt * norms_at[power] * norm_xt)

    sequence = math.sqrt(sum(value * value for value in differences))
    reference_upper = math.sqrt(
        sum(value * value for value in reference_terms)
    )
    perturbed_upper = math.sqrt(
        sum(value * value for value in perturbed_terms)
    )
    return FiniteDirectionalBound(
        horizon=count,
        sequence_difference_upper=sequence,
        energy_squared_difference_upper=(
            sequence * (reference_upper + perturbed_upper)
        ),
        reference_norm_upper=reference_upper,
        perturbed_norm_upper=perturbed_upper,
        power_defect_uppers=tuple(power_defects),
    )


@dataclass(frozen=True)
class GrowingHorizonTransfer:
    """Complete full-energy upper transferred from one contracting block."""

    horizon: int
    transferred_block_norm_upper: float
    contraction_margin: float
    perturbed_finite_energy_upper: float
    perturbed_source_block_energy_upper: float
    perturbed_tail_energy_squared_upper: float
    perturbed_full_energy_squared_upper: float
    perturbed_full_energy_upper: float


def growing_horizon_energy_upper(
    *,
    reference_finite_energy: float,
    finite_sequence_difference_upper: float,
    reference_block_norm: float,
    power_defect_upper: float,
    perturbed_source_norm_upper: float,
    perturbed_observation_norm_upper: float,
    perturbed_power_norms: Iterable[float],
    horizon: int,
) -> GrowingHorizonTransfer:
    r"""Transfer a complete Hardy upper using the block-geometric tail.

    If ``qtilde <= q+d < 1``, the finite perturbed energy is at most the
    reference finite energy plus the RH-53 sequence defect.  Also

    ``tr(Stilde_M) <= ||Xtilde||_F^2 sum_(j<M) ||Atilde^j||_2^2``.

    Substitution into the block-geometric tail gives a certificate that does
    not require solving the perturbed Lyapunov equation.
    """

    count = int(horizon)
    if count < 1:
        raise ValueError("horizon must be positive")
    finite = _nonnegative(reference_finite_energy, "reference_finite_energy")
    sequence = _nonnegative(
        finite_sequence_difference_upper,
        "finite_sequence_difference_upper",
    )
    q = _nonnegative(reference_block_norm, "reference_block_norm")
    d = _nonnegative(power_defect_upper, "power_defect_upper")
    qtilde = q + d
    if qtilde >= 1.0:
        raise ValueError("the transferred block is not a contraction")
    source = _nonnegative(
        perturbed_source_norm_upper, "perturbed_source_norm_upper"
    )
    observation = _nonnegative(
        perturbed_observation_norm_upper,
        "perturbed_observation_norm_upper",
    )
    powers = tuple(
        _nonnegative(value, "perturbed power norm")
        for value in perturbed_power_norms
    )
    if len(powers) < count:
        raise ValueError("power ledger must contain powers zero through M-1")
    source_block = source * source * sum(
        value * value for value in powers[:count]
    )
    tail = (
        observation
        * observation
        * qtilde
        * qtilde
        * source_block
        / (1.0 - qtilde * qtilde)
    )
    perturbed_finite = finite + sequence
    full_squared = perturbed_finite * perturbed_finite + tail
    return GrowingHorizonTransfer(
        horizon=count,
        transferred_block_norm_upper=qtilde,
        contraction_margin=1.0 - qtilde,
        perturbed_finite_energy_upper=perturbed_finite,
        perturbed_source_block_energy_upper=source_block,
        perturbed_tail_energy_squared_upper=tail,
        perturbed_full_energy_squared_upper=full_squared,
        perturbed_full_energy_upper=math.sqrt(full_squared),
    )


@dataclass(frozen=True)
class IdentificationBudget:
    """Power ledger for the RH-50 -> RH-49 -> RH-48 composition."""

    hardy_product_exponent: float
    mixed_gain_exponent: float
    identification_sigma_exponent: float
    preserves_all_strict_bulk_square_schedules: bool


def identification_budget(
    left_hardy_exponent: float, right_hardy_exponent: float
) -> IdentificationBudget:
    r"""Compose two Hardy losses with the quarter-power stable-rank cost."""

    left = _nonnegative(left_hardy_exponent, "left_hardy_exponent")
    right = _nonnegative(right_hardy_exponent, "right_hardy_exponent")
    delta = left + right
    gamma = 0.25 + delta
    return IdentificationBudget(
        hardy_product_exponent=delta,
        mixed_gain_exponent=gamma,
        identification_sigma_exponent=3.0 + gamma,
        preserves_all_strict_bulk_square_schedules=delta <= 0.25,
    )


def nonnormal_projector_example(coupling: float, perturbation: float) -> dict:
    r"""Return the two-by-two no-free-lunch family from the manuscript."""

    k = _positive(coupling, "coupling")
    c = _positive(perturbation, "perturbation")
    reference = np.asarray([[0.0, k], [0.0, 1.0]])
    error = np.asarray([[0.0, 0.0], [c / k, 0.0]])
    perturbed = reference + error
    discriminant = math.sqrt(1.0 + 4.0 * c)
    low = (1.0 - discriminant) / 2.0
    high = (1.0 + discriminant) / 2.0
    reference_projector = reference.copy()
    perturbed_projector = (perturbed - low * np.eye(2)) / discriminant
    return {
        "reference": reference,
        "perturbed": perturbed,
        "error": error,
        "eigenvalues": np.asarray([low, high]),
        "reference_projector": reference_projector,
        "perturbed_projector": perturbed_projector,
        "operator_defect": float(np.linalg.norm(error, 2)),
        "projector_defect": float(
            np.linalg.norm(perturbed_projector - reference_projector, 2)
        ),
    }
