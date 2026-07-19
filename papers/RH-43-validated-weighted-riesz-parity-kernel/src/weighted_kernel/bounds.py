"""Outward bounds for validated weighted-Riesz factors and Schur lifts."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math


def _up(value: float) -> float:
    number = float(value)
    if number < 0.0 or math.isnan(number):
        raise ValueError("an outward upper must be nonnegative")
    return math.nextafter(number, math.inf)


def _down(value: float) -> float:
    number = float(value)
    if number <= 0.0:
        return 0.0
    return math.nextafter(number, 0.0)


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


def upper_divide(numerator: float, denominator: float) -> float:
    bottom = _down(denominator)
    if bottom <= 0.0:
        return math.inf
    return _up(float(numerator) / bottom)


def upper_sqrt(value: float) -> float:
    return _up(math.sqrt(_up(value)))


@dataclass(frozen=True)
class FactorCorrectionLedger:
    projection_norm_upper: float
    right_block_residual_upper: float
    left_block_residual_upper: float
    overlap_block_upper: float
    correction_norm_upper: float
    correction_neumann_product_upper: float
    corrected_contour_resolvent_upper: float
    weighted_term_error_upper: float
    approximate_weighted_term_norm_upper: float
    eigenvalue_center_error_upper: float
    admissible: bool

    def as_dict(self) -> dict[str, float | bool]:
        return asdict(self)


def factor_correction_ledger(
    *,
    contour_radius: float,
    contour_maximum_modulus: float,
    contour_resolvent_upper: float,
    approximate_eigenvalue_modulus: float,
    right_norm_upper: float,
    left_norm_upper: float,
    right_residual_upper: float,
    left_residual_upper: float,
    gram_lower: float,
    gram_upper: float,
    grushin_scalar_error_upper: float,
) -> FactorCorrectionLedger:
    r"""Validate an intrinsic rank-one weighted term from two-sided residuals.

    For ``P=r l^T/(l^T r)`` and ``R=A-lambda I``, the corrected matrix

    ``A_tilde=lambda P+(I-P)A(I-P)``

    differs from ``A`` by ``-RP-PR+PRP``.  The correction commutes with
    ``P`` and has weighted Riesz term exactly ``lambda P``.
    """

    g_lower = float(gram_lower)
    if g_lower <= 0.0 or float(gram_upper) < g_lower:
        raise ValueError("the Gram enclosure must exclude zero")
    projection = upper_divide(
        upper_multiply(right_norm_upper, left_norm_upper), g_lower
    )
    right_block = upper_divide(
        upper_multiply(right_residual_upper, left_norm_upper), g_lower
    )
    left_block = upper_divide(
        upper_multiply(right_norm_upper, left_residual_upper), g_lower
    )
    overlap = min(
        upper_multiply(projection, right_block),
        upper_multiply(projection, left_block),
    )
    correction = upper_add(right_block, left_block, overlap)
    base = float(contour_resolvent_upper)
    product = upper_multiply(base, correction)
    admissible = bool(math.isfinite(product) and product < 1.0)
    corrected = (
        upper_divide(base, _down(1.0 - product))
        if admissible
        else math.inf
    )
    weighted_error = (
        weighted_lipschitz_upper(
            contour_radius=contour_radius,
            contour_maximum_modulus=contour_maximum_modulus,
            first_resolvent_upper=base,
            second_resolvent_upper=corrected,
            perturbation_upper=correction,
        )
        if admissible
        else math.inf
    )
    approximate_norm = upper_multiply(
        approximate_eigenvalue_modulus, projection
    )
    eigenvalue_error = upper_multiply(
        gram_upper, grushin_scalar_error_upper
    )
    return FactorCorrectionLedger(
        projection_norm_upper=projection,
        right_block_residual_upper=right_block,
        left_block_residual_upper=left_block,
        overlap_block_upper=overlap,
        correction_norm_upper=correction,
        correction_neumann_product_upper=product,
        corrected_contour_resolvent_upper=corrected,
        weighted_term_error_upper=weighted_error,
        approximate_weighted_term_norm_upper=approximate_norm,
        eigenvalue_center_error_upper=eigenvalue_error,
        admissible=admissible,
    )


def weighted_lipschitz_upper(
    *,
    contour_radius: float,
    contour_maximum_modulus: float,
    first_resolvent_upper: float,
    second_resolvent_upper: float,
    perturbation_upper: float,
) -> float:
    """Bound the difference of two weighted Riesz terms on one circle."""

    return upper_multiply(
        contour_radius,
        contour_maximum_modulus,
        first_resolvent_upper,
        second_resolvent_upper,
        perturbation_upper,
    )


@dataclass(frozen=True)
class WeightedSchurTransport:
    coarse_dimension: int
    top_left_difference_upper: float
    top_right_upper: float
    bottom_left_upper: float
    bottom_right_upper: float
    weighted_term_difference_upper: float

    def as_dict(self) -> dict[str, float | int]:
        return asdict(self)


def weighted_schur_transport(
    *,
    coarse_dimension: int,
    contour_radius: float,
    contour_maximum_modulus: float,
    coarse_resolvent_upper: float,
    detail_to_coarse_upper: float,
    coarse_to_detail_upper: float,
    detail_resolvent_upper: float,
    schur_inverse_upper: float,
) -> WeightedSchurTransport:
    r"""Bound ``Q(T)-diag(Q(A),0)`` through a Schur decomposition.

    The detail block has no spectrum in the parity circle.  Resolvent block
    formulas therefore leave only the self-energy correction in the
    top-left block and the three coupling blocks.
    """

    factor = upper_multiply(contour_radius, contour_maximum_modulus)
    top_left = upper_multiply(
        factor,
        schur_inverse_upper,
        detail_to_coarse_upper,
        detail_resolvent_upper,
        coarse_to_detail_upper,
        coarse_resolvent_upper,
    )
    top_right = upper_multiply(
        factor,
        schur_inverse_upper,
        detail_to_coarse_upper,
        detail_resolvent_upper,
    )
    bottom_left = upper_multiply(
        factor,
        detail_resolvent_upper,
        coarse_to_detail_upper,
        schur_inverse_upper,
    )
    bottom_right = upper_multiply(
        factor,
        detail_resolvent_upper,
        coarse_to_detail_upper,
        schur_inverse_upper,
        detail_to_coarse_upper,
        detail_resolvent_upper,
    )
    frobenius_square = upper_add(
        upper_multiply(top_left, top_left),
        upper_multiply(top_right, top_right),
        upper_multiply(bottom_left, bottom_left),
        upper_multiply(bottom_right, bottom_right),
    )
    return WeightedSchurTransport(
        coarse_dimension=int(coarse_dimension),
        top_left_difference_upper=top_left,
        top_right_upper=top_right,
        bottom_left_upper=bottom_left,
        bottom_right_upper=bottom_right,
        weighted_term_difference_upper=upper_sqrt(frobenius_square),
    )


@dataclass(frozen=True)
class IntrinsicKernelEnvelope:
    projection_operator_norm_upper: float
    weighted_operator_norm_upper: float
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


def intrinsic_kernel_envelope(
    *,
    contour_radius: float,
    contour_maximum_modulus: float,
    contour_minimum_modulus: float,
    contour_resolvent_upper: float,
    kernel_source_first_upper: float,
    kernel_target_first_upper: float,
    kernel_source_second_upper: float,
    kernel_source_target_upper: float,
    kernel_target_second_upper: float,
    midpoint_dimension: int,
) -> IntrinsicKernelEnvelope:
    """Bound the smooth rank-one kernel of the intrinsic weighted term."""

    projection = upper_multiply(
        contour_radius, contour_resolvent_upper
    )
    weighted = upper_multiply(
        contour_radius,
        contour_maximum_modulus,
        contour_resolvent_upper,
    )
    source_first = upper_multiply(
        kernel_source_first_upper, projection
    )
    target_first = upper_multiply(
        projection, kernel_target_first_upper
    )
    source_second = upper_multiply(
        kernel_source_second_upper, projection
    )
    target_second = upper_multiply(
        projection, kernel_target_second_upper
    )
    source_target = upper_divide(
        upper_multiply(
            kernel_source_first_upper,
            projection,
            kernel_target_first_upper,
        ),
        contour_minimum_modulus,
    )
    source_second_target_second = upper_divide(
        upper_multiply(
            kernel_source_second_upper,
            projection,
            kernel_target_second_upper,
        ),
        contour_minimum_modulus,
    )
    n = int(midpoint_dimension)
    h = 1.0 / n
    second = upper_multiply(
        _up(1.0 / math.sqrt(320.0)),
        h * h,
        upper_add(source_second, target_second),
    )
    fourth = upper_multiply(
        _up(1.0 / 320.0),
        h**4,
        source_second_target_second,
    )
    midpoint = upper_add(second, fourth)
    return IntrinsicKernelEnvelope(
        projection_operator_norm_upper=projection,
        weighted_operator_norm_upper=weighted,
        kernel_hilbert_schmidt_upper=weighted,
        source_first_hilbert_schmidt_upper=source_first,
        target_first_hilbert_schmidt_upper=target_first,
        source_second_hilbert_schmidt_upper=source_second,
        source_target_hilbert_schmidt_upper=source_target,
        target_second_hilbert_schmidt_upper=target_second,
        source_second_target_second_hilbert_schmidt_upper=(
            source_second_target_second
        ),
        midpoint_to_cell_average_upper=midpoint,
        midpoint_dimension=n,
    )


def deflated_cutoff_upper(
    matrix_cutoff_upper: float, weighted_cutoff_upper: float
) -> float:
    """Bound full versus sparse intrinsically deflated operators."""

    return upper_add(matrix_cutoff_upper, weighted_cutoff_upper)
