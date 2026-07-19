"""Outward Hilbert--Schmidt, trace-norm, and determinant bounds."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math


def _up(value: float) -> float:
    number = float(value)
    if number < 0.0 or math.isnan(number):
        raise ValueError("an outward upper must be nonnegative")
    return math.nextafter(number, math.inf)


def upper_add(*values: float) -> float:
    total = 0.0
    for value in values:
        total = _up(total + float(value))
    return total


def upper_multiply(*values: float) -> float:
    total = 1.0
    for value in values:
        factor = float(value)
        if factor < 0.0:
            raise ValueError("upper products require nonnegative factors")
        total = _up(total * factor)
    return total


def hilbert_schmidt_galerkin_defect(
    dimension: int,
    source_first_hilbert_schmidt_upper: float,
    target_first_hilbert_schmidt_upper: float,
) -> float:
    r"""Bound ``||K-P_n K P_n||_HS`` by cellwise Poincare inequalities."""

    n = int(dimension)
    if n < 2:
        raise ValueError("dimension must be at least two")
    return upper_multiply(
        1.0 / (math.pi * n),
        upper_add(
            source_first_hilbert_schmidt_upper,
            target_first_hilbert_schmidt_upper,
        ),
    )


@dataclass(frozen=True)
class BulkTraceNormLedger:
    markov_hilbert_schmidt_error_upper: float
    perron_weighted_operator_error_upper: float
    parity_weighted_operator_error_upper: float
    rank_two_weighted_hilbert_schmidt_error_upper: float
    bulk_hilbert_schmidt_error_upper: float
    continuum_bulk_hilbert_schmidt_upper: float
    approximate_bulk_hilbert_schmidt_upper: float
    continuum_square_trace_norm_upper: float
    approximate_square_trace_norm_upper: float
    square_trace_norm_error_upper: float

    def as_dict(self) -> dict[str, float]:
        return asdict(self)


def bulk_trace_norm_ledger(
    *,
    markov_hilbert_schmidt_error_upper: float,
    perron_weighted_operator_error_upper: float,
    parity_weighted_operator_error_upper: float,
    continuum_bulk_hilbert_schmidt_upper: float,
) -> BulkTraceNormLedger:
    r"""Convert one-step Hilbert--Schmidt error into square trace norm.

    Each difference of two rank-one weighted terms has rank at most two, so
    its Hilbert--Schmidt norm is at most ``sqrt(2)`` times its operator norm.
    For Hilbert--Schmidt ``X,Y``, ``||XY||_1 <= ||X||_HS ||Y||_HS``.
    """

    weighted_hs = upper_multiply(
        math.sqrt(2.0),
        upper_add(
            perron_weighted_operator_error_upper,
            parity_weighted_operator_error_upper,
        ),
    )
    bulk_error = upper_add(
        markov_hilbert_schmidt_error_upper, weighted_hs
    )
    continuum = float(continuum_bulk_hilbert_schmidt_upper)
    approximate = upper_add(continuum, bulk_error)
    continuum_square = upper_multiply(continuum, continuum)
    approximate_square = upper_multiply(approximate, approximate)
    trace_error = upper_multiply(
        bulk_error, upper_add(continuum, approximate)
    )
    return BulkTraceNormLedger(
        markov_hilbert_schmidt_error_upper=(
            markov_hilbert_schmidt_error_upper
        ),
        perron_weighted_operator_error_upper=(
            perron_weighted_operator_error_upper
        ),
        parity_weighted_operator_error_upper=(
            parity_weighted_operator_error_upper
        ),
        rank_two_weighted_hilbert_schmidt_error_upper=weighted_hs,
        bulk_hilbert_schmidt_error_upper=bulk_error,
        continuum_bulk_hilbert_schmidt_upper=continuum,
        approximate_bulk_hilbert_schmidt_upper=approximate,
        continuum_square_trace_norm_upper=continuum_square,
        approximate_square_trace_norm_upper=approximate_square,
        square_trace_norm_error_upper=trace_error,
    )


def determinant_lipschitz_upper(
    *,
    disk_radius: float,
    trace_norm_error_upper: float,
    first_trace_norm_upper: float,
    second_trace_norm_upper: float,
) -> float:
    r"""Bound Fredholm determinants on ``|w| <= disk_radius``.

    Uses ``|det(I+A)-det(I+B)| <= ||A-B||_1
    exp(1+||A||_1+||B||_1)``.
    """

    radius = float(disk_radius)
    if radius < 0.0:
        raise ValueError("disk radius must be nonnegative")
    exponent = upper_add(
        1.0,
        upper_multiply(radius, first_trace_norm_upper),
        upper_multiply(radius, second_trace_norm_upper),
    )
    return upper_multiply(
        radius,
        trace_norm_error_upper,
        _up(math.exp(exponent)),
    )


def even_trace_error_upper(
    *,
    square_power: int,
    square_trace_norm_error_upper: float,
    square_operator_norm_upper: float,
) -> float:
    r"""Bound ``|tr(A_n^m)-tr(A^m)|`` for ``A=B^2``."""

    power = int(square_power)
    if power < 1:
        raise ValueError("square power must be positive")
    return upper_multiply(
        float(power),
        square_trace_norm_error_upper,
        float(square_operator_norm_upper) ** (power - 1),
    )
