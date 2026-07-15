"""Componentwise complex-disc enclosures for stored binary64 operations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse import spmatrix

from .enclosures import (
    FrobeniusBall,
    dot_gamma,
    frobenius_upper_array,
    gamma,
    magnitude_upper,
)


def _array_up(values: np.ndarray) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if np.any(array < 0.0) or np.any(np.isnan(array)):
        raise ValueError("componentwise upper bounds must be nonnegative")
    return np.nextafter(array, np.inf)


def _array_add(*values: np.ndarray) -> np.ndarray:
    if not values:
        raise ValueError("at least one array is required")
    total = np.zeros_like(np.asarray(values[0]), dtype=np.float64)
    for value in values:
        item = np.asarray(value, dtype=np.float64)
        if item.shape != total.shape or np.any(item < 0.0):
            raise ValueError("componentwise radii must have matching shapes")
        total = _array_up(total + item)
    return total


def _array_multiply(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    first = np.asarray(left, dtype=np.float64)
    second = np.asarray(right, dtype=np.float64)
    return _array_up(first * second)


def _positive_dense_product_upper(
    left: np.ndarray, right: np.ndarray
) -> np.ndarray:
    first = np.asarray(left, dtype=np.float64)
    second = np.asarray(right, dtype=np.float64)
    if first.ndim != 2 or second.ndim not in (1, 2):
        raise ValueError("positive dense product requires matrix data")
    if first.shape[1] != second.shape[0]:
        raise ValueError("positive dense product shapes do not align")
    raw = np.asarray(first @ second, dtype=np.float64)
    denominator = float(
        np.nextafter(
            1.0 - dot_gamma(first.shape[1], real_matrix=True),
            0.0,
        )
    )
    return _array_up(raw / denominator)


def _positive_sparse_product_upper(
    matrix: spmatrix,
    right: np.ndarray,
    *,
    maximum_row_nonzeros: int,
) -> np.ndarray:
    values = np.asarray(right, dtype=np.float64)
    raw = np.asarray(matrix @ values, dtype=np.float64)
    denominator = float(
        np.nextafter(
            1.0
            - dot_gamma(max(1, int(maximum_row_nonzeros)), real_matrix=True),
            0.0,
        )
    )
    return _array_up(raw / denominator)


@dataclass(frozen=True)
class ComponentwiseBall:
    """A floating centre with one outward complex-disc radius per entry."""

    center: np.ndarray
    radius: np.ndarray

    def __post_init__(self) -> None:
        center = np.asarray(self.center)
        radius = np.asarray(self.radius, dtype=np.float64)
        if center.ndim not in (1, 2) or radius.shape != center.shape:
            raise ValueError("centre and componentwise radius shapes must agree")
        if np.any(radius < 0.0) or np.any(np.isnan(radius)):
            raise ValueError("componentwise radii must be nonnegative")
        if not np.all(np.isfinite(center)):
            raise ValueError("componentwise centres must be finite")

    @classmethod
    def exact(cls, values: np.ndarray) -> "ComponentwiseBall":
        array = np.asarray(values)
        return cls(array, np.zeros(array.shape, dtype=np.float64))

    @property
    def radius_frobenius_upper(self) -> float:
        return frobenius_upper_array(self.radius)

    @property
    def norm_upper(self) -> float:
        return self.as_frobenius_ball().norm_upper

    def as_frobenius_ball(self) -> FrobeniusBall:
        return FrobeniusBall(
            np.asarray(self.center), self.radius_frobenius_upper
        )


def componentwise_negate(ball: ComponentwiseBall) -> ComponentwiseBall:
    return ComponentwiseBall(-np.asarray(ball.center), np.asarray(ball.radius))


def componentwise_adjoint(ball: ComponentwiseBall) -> ComponentwiseBall:
    return ComponentwiseBall(
        np.asarray(ball.center).conj().T,
        np.asarray(ball.radius).T,
    )


def componentwise_add(
    left: ComponentwiseBall, right: ComponentwiseBall
) -> ComponentwiseBall:
    first = np.asarray(left.center)
    second = np.asarray(right.center)
    if first.shape != second.shape:
        raise ValueError("componentwise ball shapes must agree")
    center = first + second
    local_scale = _array_add(magnitude_upper(first), magnitude_upper(second))
    roundoff = _array_multiply(
        np.full(first.shape, gamma(8), dtype=np.float64), local_scale
    )
    radius = _array_add(left.radius, right.radius, roundoff)
    return ComponentwiseBall(center, radius)


def componentwise_subtract(
    left: ComponentwiseBall, right: ComponentwiseBall
) -> ComponentwiseBall:
    return componentwise_add(left, componentwise_negate(right))


def componentwise_scalar_multiply(
    scalar: complex, ball: ComponentwiseBall
) -> ComponentwiseBall:
    factor = complex(scalar)
    center = factor * np.asarray(ball.center)
    modulus = float(magnitude_upper(np.asarray([factor]))[0])
    propagated = _array_multiply(
        np.full(ball.center.shape, modulus, dtype=np.float64), ball.radius
    )
    rounding_scale = _array_multiply(
        np.full(ball.center.shape, gamma(16), dtype=np.float64),
        np.full(ball.center.shape, modulus, dtype=np.float64),
    )
    roundoff = _array_multiply(rounding_scale, magnitude_upper(ball.center))
    return ComponentwiseBall(center, _array_add(propagated, roundoff))


def componentwise_scale_rows(
    scales: np.ndarray, ball: ComponentwiseBall
) -> ComponentwiseBall:
    factors = np.asarray(scales).reshape(-1)
    center_values = np.asarray(ball.center)
    was_vector = center_values.ndim == 1
    if was_vector:
        center_values = center_values[:, None]
        radii = np.asarray(ball.radius)[:, None]
    else:
        radii = np.asarray(ball.radius)
    if factors.size != center_values.shape[0]:
        raise ValueError("one scale is required per row")
    magnitudes = magnitude_upper(factors)[:, None]
    center = factors[:, None] * center_values
    propagated = _array_multiply(magnitudes, radii)
    rounding_scale = _array_multiply(
        np.full(magnitudes.shape, gamma(16), dtype=np.float64), magnitudes
    )
    roundoff = _array_multiply(rounding_scale, magnitude_upper(center_values))
    radius = _array_add(propagated, roundoff)
    if was_vector:
        center = center[:, 0]
        radius = radius[:, 0]
    return ComponentwiseBall(center, radius)


def componentwise_dense_exact_matmul(
    matrix: np.ndarray,
    ball: ComponentwiseBall,
    *,
    absolute_matrix: np.ndarray | None = None,
) -> ComponentwiseBall:
    operator = np.asarray(matrix)
    values = np.asarray(ball.center)
    if operator.ndim != 2 or operator.shape[1] != values.shape[0]:
        raise ValueError("componentwise dense multiplication shapes do not align")
    absolute = (
        magnitude_upper(operator)
        if absolute_matrix is None
        else np.asarray(absolute_matrix, dtype=np.float64)
    )
    center = operator @ values
    propagated = _positive_dense_product_upper(absolute, ball.radius)
    absolute_product = _positive_dense_product_upper(
        absolute, magnitude_upper(values)
    )
    roundoff = _array_multiply(
        np.full(
            absolute_product.shape,
            dot_gamma(operator.shape[1], real_matrix=not np.iscomplexobj(operator)),
            dtype=np.float64,
        ),
        absolute_product,
    )
    return ComponentwiseBall(center, _array_add(propagated, roundoff))


def componentwise_sparse_exact_matmul(
    matrix: spmatrix,
    ball: ComponentwiseBall,
    *,
    absolute_matrix: spmatrix,
    maximum_row_nonzeros: int,
) -> ComponentwiseBall:
    values = np.asarray(ball.center)
    center = np.asarray(matrix @ values)
    propagated = _positive_sparse_product_upper(
        absolute_matrix,
        ball.radius,
        maximum_row_nonzeros=maximum_row_nonzeros,
    )
    absolute_product = _positive_sparse_product_upper(
        absolute_matrix,
        magnitude_upper(values),
        maximum_row_nonzeros=maximum_row_nonzeros,
    )
    roundoff = _array_multiply(
        np.full(
            absolute_product.shape,
            dot_gamma(
                max(1, int(maximum_row_nonzeros)),
                real_matrix=not np.iscomplexobj(matrix.data),
            ),
            dtype=np.float64,
        ),
        absolute_product,
    )
    return ComponentwiseBall(center, _array_add(propagated, roundoff))


def componentwise_matmul(
    left: ComponentwiseBall, right: ComponentwiseBall
) -> ComponentwiseBall:
    first = np.asarray(left.center)
    second = np.asarray(right.center)
    if first.ndim != 2 or second.ndim != 2 or first.shape[1] != second.shape[0]:
        raise ValueError("componentwise ball products require aligned matrices")
    absolute_left = magnitude_upper(first)
    absolute_right = magnitude_upper(second)
    center = first @ second
    propagated_right = _positive_dense_product_upper(
        absolute_left, right.radius
    )
    propagated_left = _positive_dense_product_upper(
        left.radius, absolute_right
    )
    cross = _positive_dense_product_upper(left.radius, right.radius)
    absolute_product = _positive_dense_product_upper(
        absolute_left, absolute_right
    )
    roundoff = _array_multiply(
        np.full(
            absolute_product.shape,
            dot_gamma(first.shape[1], real_matrix=not np.iscomplexobj(first)),
            dtype=np.float64,
        ),
        absolute_product,
    )
    radius = _array_add(
        propagated_right, propagated_left, cross, roundoff
    )
    return ComponentwiseBall(center, radius)
