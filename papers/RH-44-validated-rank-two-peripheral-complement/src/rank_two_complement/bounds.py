"""Outward bounds specialized to the Perron and rank-two kernels."""

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


@dataclass(frozen=True)
class PerronKernelEnvelope:
    projection_operator_norm_upper: float
    kernel_hilbert_schmidt_lower: float
    kernel_hilbert_schmidt_upper: float
    source_first_hilbert_schmidt_upper: float
    target_first_hilbert_schmidt_upper: float
    source_second_hilbert_schmidt_upper: float
    source_target_hilbert_schmidt_upper: float
    target_second_hilbert_schmidt_upper: float
    source_second_target_second_hilbert_schmidt_upper: float
    midpoint_to_cell_average_upper: float
    midpoint_dimension: int

    def as_dict(self) -> dict[str, float | int]:
        return asdict(self)


def perron_kernel_envelope(
    *,
    contour_radius: float,
    contour_resolvent_upper: float,
    kernel_target_first_upper: float,
    kernel_target_second_upper: float,
    midpoint_dimension: int,
) -> PerronKernelEnvelope:
    r"""Bound the stationary kernel ``q_+(x,y)=pi(y)``.

    The Markov identity gives the exact right eigenfunction ``1`` and
    ``<pi,1>=1``.  Hence the Perron projector has kernel ``pi(y)``, all
    source derivatives vanish, and its Hilbert--Schmidt norm equals its
    operator norm.  Differentiating ``K^* pi=pi`` bounds target derivatives.
    """

    projection = upper_multiply(
        contour_radius, contour_resolvent_upper
    )
    target_first = upper_multiply(
        projection, kernel_target_first_upper
    )
    target_second = upper_multiply(
        projection, kernel_target_second_upper
    )
    n = int(midpoint_dimension)
    if n < 2:
        raise ValueError("midpoint dimension must be at least two")
    midpoint = upper_multiply(
        1.0 / math.sqrt(320.0),
        1.0 / (n * n),
        target_second,
    )
    return PerronKernelEnvelope(
        projection_operator_norm_upper=projection,
        kernel_hilbert_schmidt_lower=1.0,
        kernel_hilbert_schmidt_upper=projection,
        source_first_hilbert_schmidt_upper=0.0,
        target_first_hilbert_schmidt_upper=target_first,
        source_second_hilbert_schmidt_upper=0.0,
        source_target_hilbert_schmidt_upper=0.0,
        target_second_hilbert_schmidt_upper=target_second,
        source_second_target_second_hilbert_schmidt_upper=0.0,
        midpoint_to_cell_average_upper=midpoint,
        midpoint_dimension=n,
    )


def combine_kernel_envelopes(
    perron: PerronKernelEnvelope,
    parity: dict[str, float | int],
) -> dict[str, float | int]:
    """Add Perron and parity Hilbert--Schmidt derivative envelopes."""

    return {
        "kernel_hilbert_schmidt_upper": upper_add(
            perron.kernel_hilbert_schmidt_upper,
            float(parity["kernel_hilbert_schmidt_upper"]),
        ),
        "source_first_hilbert_schmidt_upper": upper_add(
            perron.source_first_hilbert_schmidt_upper,
            float(parity["source_first_hilbert_schmidt_upper"]),
        ),
        "target_first_hilbert_schmidt_upper": upper_add(
            perron.target_first_hilbert_schmidt_upper,
            float(parity["target_first_hilbert_schmidt_upper"]),
        ),
        "source_second_hilbert_schmidt_upper": upper_add(
            perron.source_second_hilbert_schmidt_upper,
            float(parity["source_second_hilbert_schmidt_upper"]),
        ),
        "source_target_hilbert_schmidt_upper": upper_add(
            perron.source_target_hilbert_schmidt_upper,
            float(parity["source_target_hilbert_schmidt_upper"]),
        ),
        "target_second_hilbert_schmidt_upper": upper_add(
            perron.target_second_hilbert_schmidt_upper,
            float(parity["target_second_hilbert_schmidt_upper"]),
        ),
        "source_second_target_second_hilbert_schmidt_upper": upper_add(
            perron.source_second_target_second_hilbert_schmidt_upper,
            float(
                parity[
                    "source_second_target_second_hilbert_schmidt_upper"
                ]
            ),
        ),
        "midpoint_to_cell_average_upper": upper_add(
            perron.midpoint_to_cell_average_upper,
            float(parity["midpoint_to_cell_average_upper"]),
        ),
        "midpoint_dimension": min(
            perron.midpoint_dimension,
            int(parity["midpoint_dimension"]),
        ),
    }


def rank_two_cutoff_upper(
    matrix_cutoff_upper: float,
    perron_weighted_cutoff_upper: float,
    parity_weighted_cutoff_upper: float,
) -> tuple[float, float]:
    """Return rank-two weighted and intrinsically deflated cutoff bounds."""

    weighted = upper_add(
        perron_weighted_cutoff_upper, parity_weighted_cutoff_upper
    )
    return weighted, upper_add(matrix_cutoff_upper, weighted)
