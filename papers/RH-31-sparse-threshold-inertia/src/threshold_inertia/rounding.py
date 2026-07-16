"""Outward scalar bounds for sparse LDL inertia bracketing."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


UNIT_ROUNDOFF = 2.0**-53


def gamma(operation_count: int) -> float:
    count = int(operation_count)
    if count < 0:
        raise ValueError("operation count must be nonnegative")
    product = count * UNIT_ROUNDOFF
    if product >= 1.0:
        raise ValueError("operation count is too large for a gamma bound")
    if count == 0:
        return 0.0
    return float(np.nextafter(product / (1.0 - product), np.inf))


def upper_add(*values: float) -> float:
    total = 0.0
    for value in values:
        item = float(value)
        if item < 0.0 or np.isnan(item):
            raise ValueError("upper bounds must be nonnegative")
        total = float(np.nextafter(total + item, np.inf))
    return total


def upper_multiply(left: float, right: float) -> float:
    first = float(left)
    second = float(right)
    if first < 0.0 or second < 0.0 or np.isnan(first + second):
        raise ValueError("upper bounds must be nonnegative")
    return float(np.nextafter(first * second, np.inf))


def magnitude_upper(values: np.ndarray) -> np.ndarray:
    array = np.asarray(values)
    raw = np.asarray(np.abs(array), dtype=np.float64)
    if np.iscomplexobj(array):
        raw = raw / float(np.nextafter(1.0 - gamma(8), 0.0))
    result = np.nextafter(raw, np.inf)
    result[raw == 0.0] = 0.0
    return result


def frobenius_upper_array(values: np.ndarray) -> float:
    magnitudes = magnitude_upper(np.asarray(values)).reshape(-1)
    if magnitudes.size == 0:
        return 0.0
    scale = float(np.max(magnitudes))
    if scale == 0.0:
        return 0.0
    lowered_scale = float(np.nextafter(scale, 0.0))
    scaled = np.nextafter(magnitudes / lowered_scale, np.inf)
    squares = np.nextafter(scaled * scaled, np.inf)
    raw_sum = float(np.sum(squares, dtype=np.float64))
    denominator = float(
        np.nextafter(1.0 - gamma(2 * magnitudes.size + 8), 0.0)
    )
    norm = np.sqrt(np.nextafter(raw_sum / denominator, np.inf))
    return upper_multiply(scale, float(np.nextafter(norm, np.inf)))


def sparse_frobenius_upper(matrix) -> float:
    return frobenius_upper_array(np.asarray(matrix.data))


@dataclass(frozen=True)
class LDLBackwardErrorBound:
    """A normwise bound between the input and an exact Hermitian LDL matrix."""

    matrix_dimension: int
    lower_frobenius_upper: float
    upper_frobenius_upper: float
    ldl_relation_defect_frobenius_upper: float
    absolute_lu_product_frobenius_upper: float
    ldl_center_conversion_error_upper: float
    ldl_relation_formation_error_upper: float
    gaussian_elimination_backward_error_upper: float
    ldl_conversion_error_upper: float
    input_assembly_error_upper: float
    total_error_upper: float
    elimination_operation_factor: int
    positive_pivots: int
    negative_pivots: int
    minimum_real_pivot_magnitude: float


def _segment_two_norms_upper(matrix, *, columns: bool) -> np.ndarray:
    sparse = matrix.tocsc() if columns else matrix.tocsr()
    count = sparse.shape[1] if columns else sparse.shape[0]
    magnitudes = magnitude_upper(np.asarray(sparse.data))
    maximum_terms = int(np.max(np.diff(sparse.indptr))) if count else 0
    denominator = float(
        np.nextafter(1.0 - gamma(2 * maximum_terms + 8), 0.0)
    )
    result = np.zeros(count, dtype=np.float64)
    for index in range(count):
        start = int(sparse.indptr[index])
        stop = int(sparse.indptr[index + 1])
        if start == stop:
            continue
        values = magnitudes[start:stop]
        squares = np.nextafter(values * values, np.inf)
        total = float(np.sum(squares, dtype=np.float64))
        result[index] = float(
            np.nextafter(np.sqrt(np.nextafter(total / denominator, np.inf)), np.inf)
        )
    return result


def outer_product_frobenius_upper(left, right) -> float:
    r"""Bound ``||left @ right||_F`` by paired column/row outer products."""

    if left.shape[1] != right.shape[0]:
        raise ValueError("outer-product bound requires aligned matrices")
    columns = _segment_two_norms_upper(left, columns=True)
    rows = _segment_two_norms_upper(right, columns=False)
    products = np.nextafter(columns * rows, np.inf)
    raw = float(np.sum(products, dtype=np.float64))
    denominator = float(
        np.nextafter(1.0 - gamma(2 * products.size + 8), 0.0)
    )
    return float(np.nextafter(raw / denominator, np.inf))


def hermitian_ldl_backward_error_upper(
    lower,
    upper,
    *,
    input_assembly_error_upper: float = 0.0,
    operation_factor: int = 24,
) -> LDLBackwardErrorBound:
    r"""Bound ``||A - L Re(diag(U)) L*||_2`` by a Frobenius majorant.

    The sparse no-pivot Gaussian elimination is assigned the conservative
    componentwise model

    ``|A-LU| <= gamma_{operation_factor*n+64} |L||U|``.

    The default factor 24 counts a conservative maximum of 24 real rounded
    operations per elimination level for complex multiply-add accumulation
    and division.  The additive 64 covers fixed setup operations.  This is
    deliberately looser than the standard real-arithmetic Gaussian
    elimination bounds while remaining linear in the matrix dimension.

    The conversion from ``LU`` to a Hermitian ``LDL*`` factorization is then
    bounded explicitly by ``||L||_F ||U-DL*||_F``.  The resulting exact
    Hermitian matrix has inertia given by the signs of the real diagonal D.
    """

    dimension = int(lower.shape[0])
    if lower.shape != upper.shape or lower.shape[1] != dimension:
        raise ValueError("L and U must be aligned square matrices")
    assembly = float(input_assembly_error_upper)
    if assembly < 0.0:
        raise ValueError("assembly error must be nonnegative")
    lower_norm = sparse_frobenius_upper(lower)
    upper_norm = sparse_frobenius_upper(upper)
    diagonal = np.asarray(upper.diagonal())
    real_diagonal = np.asarray(diagonal.real, dtype=np.float64)
    if np.any(real_diagonal == 0.0):
        raise ValueError("zero real pivot cannot define an inertia")
    reference = lower.conj().T.multiply(real_diagonal[:, None])
    relation_defect = upper - reference
    relation_center_norm = sparse_frobenius_upper(relation_defect)
    reference_norm = sparse_frobenius_upper(reference)
    diagonal_norm = float(
        np.nextafter(np.max(magnitude_upper(real_diagonal)), np.inf)
    )
    reference_roundoff = upper_multiply(
        gamma(16), upper_multiply(diagonal_norm, lower_norm)
    )
    subtraction_roundoff = upper_multiply(
        gamma(8), upper_add(upper_norm, reference_norm)
    )
    relation_formation_error = upper_add(
        reference_roundoff, subtraction_roundoff
    )
    relation_norm = upper_add(
        relation_center_norm, reference_roundoff, subtraction_roundoff
    )
    operation_count_factor = int(operation_factor)
    if operation_count_factor < 24:
        raise ValueError("complex elimination requires an operation factor of at least 24")
    elimination_gamma = gamma(operation_count_factor * dimension + 64)
    absolute_product = outer_product_frobenius_upper(lower, upper)
    elimination = upper_multiply(
        elimination_gamma, absolute_product
    )
    center_conversion = outer_product_frobenius_upper(
        lower, relation_defect
    )
    conversion = upper_add(
        center_conversion,
        upper_multiply(lower_norm, relation_formation_error),
    )
    total = upper_add(assembly, elimination, conversion)
    return LDLBackwardErrorBound(
        matrix_dimension=dimension,
        lower_frobenius_upper=lower_norm,
        upper_frobenius_upper=upper_norm,
        ldl_relation_defect_frobenius_upper=relation_norm,
        absolute_lu_product_frobenius_upper=absolute_product,
        ldl_center_conversion_error_upper=center_conversion,
        ldl_relation_formation_error_upper=relation_formation_error,
        gaussian_elimination_backward_error_upper=elimination,
        ldl_conversion_error_upper=conversion,
        input_assembly_error_upper=assembly,
        total_error_upper=total,
        elimination_operation_factor=operation_count_factor,
        positive_pivots=int(np.count_nonzero(real_diagonal > 0.0)),
        negative_pivots=int(np.count_nonzero(real_diagonal < 0.0)),
        minimum_real_pivot_magnitude=float(np.min(np.abs(real_diagonal))),
    )


@dataclass(frozen=True)
class InertiaBracket:
    """Two shifted LDL factorizations bracketing one exact Hermitian inertia."""

    admissible: bool
    shift: float | None
    lower_shift: float
    upper_shift: float
    lower_shift_error_upper: float
    upper_shift_error_upper: float
    positive_count: int
    negative_count: int


def inertia_bracket(
    shift: float,
    minus_shift: LDLBackwardErrorBound,
    plus_shift: LDLBackwardErrorBound,
) -> InertiaBracket:
    r"""Apply the symmetric two-shift Weyl sandwich."""

    return asymmetric_inertia_bracket(
        shift,
        shift,
        minus_shift,
        plus_shift,
    )


def asymmetric_inertia_bracket(
    lower_shift: float,
    upper_shift: float,
    minus_shift: LDLBackwardErrorBound,
    plus_shift: LDLBackwardErrorBound,
) -> InertiaBracket:
    r"""Apply the two-shift Weyl sandwich with independent distances.

    ``minus_shift`` corresponds to ``H-delta_- I`` and ``plus_shift`` to
    ``H+delta_+ I``.  If their exact Hermitian LDL centres have the same
    inertia and the respective backward errors are below ``delta_-`` and
    ``delta_+``, Weyl monotonicity sandwiches the inertia of ``H`` between
    them.  The two shift distances need not agree.
    """

    lower_delta = float(lower_shift)
    upper_delta = float(upper_shift)
    if lower_delta <= 0.0 or upper_delta <= 0.0:
        raise ValueError("bracket shifts must be positive")
    same = (
        minus_shift.positive_pivots == plus_shift.positive_pivots
        and minus_shift.negative_pivots == plus_shift.negative_pivots
    )
    admissible = bool(
        same
        and minus_shift.total_error_upper < lower_delta
        and plus_shift.total_error_upper < upper_delta
    )
    return InertiaBracket(
        admissible=admissible,
        shift=(lower_delta if lower_delta == upper_delta else None),
        lower_shift=lower_delta,
        upper_shift=upper_delta,
        lower_shift_error_upper=minus_shift.total_error_upper,
        upper_shift_error_upper=plus_shift.total_error_upper,
        positive_count=(minus_shift.positive_pivots if same else -1),
        negative_count=(minus_shift.negative_pivots if same else -1),
    )
