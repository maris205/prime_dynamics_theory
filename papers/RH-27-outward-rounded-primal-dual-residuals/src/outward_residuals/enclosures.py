"""Outward-rounded Frobenius balls for stored binary64 linear algebra.

The module deliberately certifies a finite, stored-factor model.  Every
binary64 input is regarded as an exact real or complex number.  The centre
of each operation is evaluated in ordinary binary64 arithmetic and a scalar
Frobenius radius is propagated with directed outward rounding.

The error constants use a conservative real-operation count for each dot
product.  They are valid under the usual IEEE round-to-nearest model, in the
absence of overflow and harmful underflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np
from scipy.sparse import spmatrix


UNIT_ROUNDOFF = 2.0 ** -53


def gamma(operation_count: int, *, unit_roundoff: float = UNIT_ROUNDOFF) -> float:
    r"""Return Higham's :math:`\gamma_k=ku/(1-ku)`."""

    count = int(operation_count)
    if count < 0:
        raise ValueError("operation_count must be nonnegative")
    product = count * float(unit_roundoff)
    if product >= 1.0:
        raise ValueError("operation count is too large for a gamma bound")
    if count == 0:
        return 0.0
    return float(np.nextafter(product / (1.0 - product), np.inf))


def dot_gamma(length: int, *, real_matrix: bool) -> float:
    """Conservative gamma factor for one real or complex dot product."""

    size = int(length)
    if size < 1:
        raise ValueError("dot-product length must be positive")
    # A real matrix times complex data is two real dot products.  Four real
    # operations per term plus a guard absorbs the Euclidean recombination.
    # The fully complex path reserves sixteen real operations per term.
    operations = (4 * size + 8) if real_matrix else (16 * size + 16)
    return gamma(operations)


def _up(value: float) -> float:
    result = float(value)
    if result < 0.0 or np.isnan(result):
        raise ValueError("an outward upper bound must be nonnegative")
    return float(np.nextafter(result, np.inf))


def _down_nonnegative(value: float) -> float:
    result = float(value)
    if result <= 0.0:
        return 0.0
    return float(max(0.0, np.nextafter(result, 0.0)))


def upper_add(*values: float) -> float:
    """Add nonnegative scalars with one final outward rounding step."""

    total = 0.0
    for value in values:
        item = float(value)
        if item < 0.0 or np.isnan(item):
            raise ValueError("upper_add accepts nonnegative finite scalars")
        total = float(np.nextafter(total + item, np.inf))
    return total


def upper_multiply(left: float, right: float) -> float:
    """Multiply nonnegative scalars and round toward positive infinity."""

    first = float(left)
    second = float(right)
    if first < 0.0 or second < 0.0 or np.isnan(first + second):
        raise ValueError("upper_multiply accepts nonnegative scalars")
    return _up(first * second)


def upper_divide(numerator: float, denominator: float) -> float:
    """Divide positive-bound scalars and round toward positive infinity."""

    top = float(numerator)
    bottom = float(denominator)
    if top < 0.0 or bottom <= 0.0 or np.isnan(top + bottom):
        raise ValueError("invalid upper division")
    lowered_bottom = float(np.nextafter(bottom, 0.0))
    if lowered_bottom <= 0.0:
        return float("inf")
    return _up(top / lowered_bottom)


def lower_divide(numerator: float, denominator: float) -> float:
    """Return a nonnegative downward-rounded quotient."""

    top = float(numerator)
    bottom = float(denominator)
    if top <= 0.0:
        return 0.0
    if bottom < 0.0 or np.isnan(top + bottom):
        raise ValueError("invalid lower division")
    if bottom == 0.0:
        return float("inf")
    raised_bottom = float(np.nextafter(bottom, np.inf))
    return _down_nonnegative(_down_nonnegative(top) / raised_bottom)


def magnitude_upper(values: np.ndarray) -> np.ndarray:
    """Entrywise outward upper bounds for real or complex magnitudes."""

    array = np.asarray(values)
    raw = np.abs(array).astype(np.float64, copy=False)
    if np.iscomplexobj(array):
        denominator = float(np.nextafter(1.0 - gamma(8), 0.0))
        raw = raw / denominator
    result = np.nextafter(raw, np.inf)
    result[raw == 0.0] = 0.0
    return result


def frobenius_upper_array(values: np.ndarray) -> float:
    """Outward upper bound for the Frobenius norm of a stored array."""

    magnitudes = magnitude_upper(np.asarray(values)).reshape(-1)
    if magnitudes.size == 0:
        return 0.0
    scale = float(np.max(magnitudes))
    if scale == 0.0:
        return 0.0
    denominator = float(np.nextafter(scale, 0.0))
    scaled = np.nextafter(magnitudes / denominator, np.inf)
    scaled[magnitudes == 0.0] = 0.0
    squares = np.nextafter(scaled * scaled, np.inf)
    raw_sum = float(np.sum(squares, dtype=np.float64))
    reduction_denominator = float(
        np.nextafter(1.0 - gamma(2 * magnitudes.size + 8), 0.0)
    )
    sum_upper = _up(raw_sum / reduction_denominator)
    root_upper = _up(np.sqrt(sum_upper))
    return upper_multiply(scale, root_upper)


def dense_abs_operator_upper(values: np.ndarray) -> float:
    """Upper-bound the 2-norm of ``abs(values)`` by 1/inf and Frobenius norms."""

    array = np.asarray(values)
    if array.ndim != 2:
        raise ValueError("a matrix is required")
    magnitudes = magnitude_upper(array)
    rows, columns = magnitudes.shape
    raw_rows = np.sum(magnitudes, axis=1, dtype=np.float64)
    raw_columns = np.sum(magnitudes, axis=0, dtype=np.float64)
    row_denominator = float(np.nextafter(1.0 - gamma(2 * columns + 8), 0.0))
    column_denominator = float(np.nextafter(1.0 - gamma(2 * rows + 8), 0.0))
    infinity_norm = _up(float(np.max(raw_rows)) / row_denominator)
    one_norm = _up(float(np.max(raw_columns)) / column_denominator)
    induced = _up(np.sqrt(upper_multiply(infinity_norm, one_norm)))
    return min(induced, frobenius_upper_array(array))


def sparse_abs_operator_upper(matrix: spmatrix) -> float:
    """Upper-bound ``||abs(matrix)||_2`` for a stored sparse matrix."""

    sparse = matrix.tocsr(copy=False)
    rows, columns = sparse.shape
    magnitudes = magnitude_upper(sparse.data)
    row_counts = np.diff(sparse.indptr)
    max_row = int(np.max(row_counts)) if row_counts.size else 0
    column_counts = np.bincount(sparse.indices, minlength=columns)
    max_column = int(np.max(column_counts)) if column_counts.size else 0
    row_sums = np.zeros(rows, dtype=np.float64)
    for row in range(rows):
        start, stop = int(sparse.indptr[row]), int(sparse.indptr[row + 1])
        row_sums[row] = np.sum(magnitudes[start:stop], dtype=np.float64)
    column_sums = np.bincount(
        sparse.indices, weights=magnitudes, minlength=columns
    ).astype(np.float64, copy=False)
    row_denominator = float(np.nextafter(1.0 - gamma(2 * max_row + 8), 0.0))
    column_denominator = float(
        np.nextafter(1.0 - gamma(2 * max_column + 8), 0.0)
    )
    infinity_norm = _up(float(np.max(row_sums)) / row_denominator)
    one_norm = _up(float(np.max(column_sums)) / column_denominator)
    induced = _up(np.sqrt(upper_multiply(infinity_norm, one_norm)))
    frobenius = frobenius_upper_array(sparse.data)
    return min(induced, frobenius)


@dataclass(frozen=True)
class FrobeniusBall:
    """A stored centre and a scalar outward Frobenius radius."""

    center: np.ndarray
    radius: float = 0.0

    def __post_init__(self) -> None:
        array = np.asarray(self.center)
        radius = float(self.radius)
        if array.ndim not in (1, 2):
            raise ValueError("ball centres must be vectors or matrices")
        if radius < 0.0 or np.isnan(radius):
            raise ValueError("ball radius must be nonnegative")
        if not np.all(np.isfinite(array)):
            raise ValueError("ball centres must be finite")

    @classmethod
    def exact(cls, values: np.ndarray) -> "FrobeniusBall":
        return cls(np.asarray(values), 0.0)

    @property
    def norm_upper(self) -> float:
        return upper_add(frobenius_upper_array(self.center), self.radius)


def negate(ball: FrobeniusBall) -> FrobeniusBall:
    """Negate a ball exactly."""

    return FrobeniusBall(-np.asarray(ball.center), float(ball.radius))


def conjugate_transpose(ball: FrobeniusBall) -> FrobeniusBall:
    """Take the Euclidean adjoint without additional rounding."""

    return FrobeniusBall(np.asarray(ball.center).conj().T, float(ball.radius))


def add(left: FrobeniusBall, right: FrobeniusBall) -> FrobeniusBall:
    """Outward enclosure of the sum of two Frobenius balls."""

    first = np.asarray(left.center)
    second = np.asarray(right.center)
    if first.shape != second.shape:
        raise ValueError("ball shapes must agree")
    center = first + second
    roundoff = upper_multiply(
        gamma(8),
        upper_add(frobenius_upper_array(first), frobenius_upper_array(second)),
    )
    radius = upper_add(left.radius, right.radius, roundoff)
    return FrobeniusBall(center, radius)


def subtract(left: FrobeniusBall, right: FrobeniusBall) -> FrobeniusBall:
    """Outward enclosure of the difference of two Frobenius balls."""

    return add(left, negate(right))


def scalar_multiply(scalar: complex, ball: FrobeniusBall) -> FrobeniusBall:
    """Outward enclosure of an exact stored scalar times a ball."""

    factor = complex(scalar)
    center = factor * np.asarray(ball.center)
    modulus = _up(abs(factor))
    propagated = upper_multiply(modulus, ball.radius)
    roundoff = upper_multiply(
        gamma(16),
        upper_multiply(modulus, frobenius_upper_array(ball.center)),
    )
    return FrobeniusBall(center, upper_add(propagated, roundoff))


def scale_rows(scales: np.ndarray, ball: FrobeniusBall) -> FrobeniusBall:
    """Outward enclosure of exact stored diagonal row scaling."""

    factors = np.asarray(scales).reshape(-1)
    center_values = np.asarray(ball.center)
    if center_values.ndim == 1:
        center_values = center_values[:, None]
        return_vector = True
    else:
        return_vector = False
    if factors.size != center_values.shape[0]:
        raise ValueError("one scale is required per row")
    center = factors[:, None] * center_values
    scale_norm = float(np.max(magnitude_upper(factors)))
    propagated = upper_multiply(scale_norm, ball.radius)
    roundoff = upper_multiply(
        gamma(16),
        upper_multiply(scale_norm, frobenius_upper_array(center_values)),
    )
    if return_vector:
        center = center[:, 0]
    return FrobeniusBall(center, upper_add(propagated, roundoff))


def dense_exact_matmul(
    matrix: np.ndarray,
    ball: FrobeniusBall,
    *,
    abs_operator_upper: float | None = None,
) -> FrobeniusBall:
    """Enclose an exact stored dense matrix times a Frobenius ball."""

    operator = np.asarray(matrix)
    values = np.asarray(ball.center)
    if operator.ndim != 2 or values.ndim not in (1, 2):
        raise ValueError("dense multiplication requires a matrix and vector/matrix")
    if operator.shape[1] != values.shape[0]:
        raise ValueError("dense multiplication shapes do not align")
    norm_bound = (
        dense_abs_operator_upper(operator)
        if abs_operator_upper is None
        else float(abs_operator_upper)
    )
    center = operator @ values
    rounding = upper_multiply(
        dot_gamma(operator.shape[1], real_matrix=not np.iscomplexobj(operator)),
        upper_multiply(norm_bound, frobenius_upper_array(values)),
    )
    propagated = upper_multiply(norm_bound, ball.radius)
    return FrobeniusBall(center, upper_add(propagated, rounding))


def sparse_exact_matmul(
    matrix: spmatrix,
    ball: FrobeniusBall,
    *,
    abs_operator_upper: float,
    maximum_row_nonzeros: int,
) -> FrobeniusBall:
    """Enclose an exact stored sparse matrix times a Frobenius ball."""

    values = np.asarray(ball.center)
    if matrix.shape[1] != values.shape[0]:
        raise ValueError("sparse multiplication shapes do not align")
    center = np.asarray(matrix @ values)
    norm_bound = float(abs_operator_upper)
    rounding = upper_multiply(
        dot_gamma(
            max(1, int(maximum_row_nonzeros)),
            real_matrix=not np.iscomplexobj(matrix.data),
        ),
        upper_multiply(norm_bound, frobenius_upper_array(values)),
    )
    propagated = upper_multiply(norm_bound, ball.radius)
    return FrobeniusBall(center, upper_add(propagated, rounding))


def matmul(left: FrobeniusBall, right: FrobeniusBall) -> FrobeniusBall:
    """Enclose the product of two uncertain dense matrices."""

    first = np.asarray(left.center)
    second = np.asarray(right.center)
    if first.ndim != 2 or second.ndim != 2 or first.shape[1] != second.shape[0]:
        raise ValueError("ball matrix multiplication shapes do not align")
    left_bound = dense_abs_operator_upper(first)
    right_norm = frobenius_upper_array(second)
    center = first @ second
    propagated_right = upper_multiply(left_bound, right.radius)
    propagated_left = upper_multiply(left.radius, right_norm)
    cross = upper_multiply(left.radius, right.radius)
    rounding = upper_multiply(
        dot_gamma(first.shape[1], real_matrix=not np.iscomplexobj(first)),
        upper_multiply(left_bound, right_norm),
    )
    radius = upper_add(propagated_right, propagated_left, cross, rounding)
    return FrobeniusBall(center, radius)


@dataclass(frozen=True)
class InverseCertificate:
    """Neumann certificate for a stored square matrix inverse."""

    approximate_inverse: np.ndarray
    inverse_norm_upper: float
    defect_norm_upper: float
    inverse_frobenius_upper: float


def inverse_certificate(matrix: np.ndarray) -> InverseCertificate:
    r"""Certify an upper inverse norm from ``I-A X`` in Frobenius norm."""

    operator = np.asarray(matrix, dtype=np.complex128)
    if operator.ndim != 2 or operator.shape[0] != operator.shape[1]:
        raise ValueError("matrix must be square")
    approximate = np.linalg.inv(operator)
    product = dense_exact_matmul(operator, FrobeniusBall.exact(approximate))
    identity = FrobeniusBall.exact(np.eye(operator.shape[0], dtype=np.complex128))
    defect = subtract(identity, product)
    defect_upper = defect.norm_upper
    if defect_upper >= 1.0:
        raise RuntimeError("the approximate inverse failed the Neumann test")
    inverse_frobenius = frobenius_upper_array(approximate)
    denominator = _down_nonnegative(1.0 - defect_upper)
    inverse_upper = upper_divide(inverse_frobenius, denominator)
    return InverseCertificate(
        approximate_inverse=approximate,
        inverse_norm_upper=inverse_upper,
        defect_norm_upper=defect_upper,
        inverse_frobenius_upper=inverse_frobenius,
    )


def inverse_product_norm_upper(
    certificate: InverseCertificate,
    right_hand_side: FrobeniusBall,
) -> float:
    r"""Upper-bound ``||A^{-1}R||_2`` using a certified approximate inverse."""

    approximate_product = dense_exact_matmul(
        certificate.approximate_inverse,
        right_hand_side,
    )
    leading = approximate_product.norm_upper
    remainder = upper_multiply(
        certificate.inverse_norm_upper,
        upper_multiply(
            certificate.defect_norm_upper,
            right_hand_side.norm_upper,
        ),
    )
    return upper_add(leading, remainder)


@dataclass(frozen=True)
class BudgetCertificate:
    """Outward Rouché data and a downward admissible inverse budget."""

    correction_ratio_upper: float
    primal_residual_norm_upper: float
    weighted_dual_residual_norm_upper: float
    remainder_coefficient_upper: float
    resolvent_budget_lower: float
    inverse_certificate: InverseCertificate


def certify_budget(
    base_feshbach: np.ndarray,
    computed_correction: FrobeniusBall,
    primal_residual: FrobeniusBall,
    dual_residual: FrobeniusBall,
) -> BudgetCertificate:
    """Return a stored-matrix primal-dual conditional budget certificate."""

    inverse = inverse_certificate(base_feshbach)
    eta_upper = inverse_product_norm_upper(inverse, computed_correction)
    primal_upper = primal_residual.norm_upper
    weighted_upper = inverse_product_norm_upper(
        inverse, conjugate_transpose(dual_residual)
    )
    coefficient = upper_multiply(primal_upper, weighted_upper)
    numerator = _down_nonnegative(1.0 - eta_upper)
    budget = lower_divide(numerator, coefficient)
    return BudgetCertificate(
        correction_ratio_upper=eta_upper,
        primal_residual_norm_upper=primal_upper,
        weighted_dual_residual_norm_upper=weighted_upper,
        remainder_coefficient_upper=coefficient,
        resolvent_budget_lower=budget,
        inverse_certificate=inverse,
    )


def finite_nonnegative(value: float) -> bool:
    """Small public helper used by tests and experiment audits."""

    return isfinite(float(value)) and float(value) >= 0.0
