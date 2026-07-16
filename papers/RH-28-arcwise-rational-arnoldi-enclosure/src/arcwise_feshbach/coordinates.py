"""Validated coordinate discs for shifted rational Arnoldi solves."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from outward_residuals import (
    ComponentwiseBall,
    componentwise_add,
    componentwise_dense_exact_matmul,
    componentwise_matmul,
    componentwise_scalar_multiply,
    componentwise_subtract,
    frobenius_upper_array,
    gamma,
    magnitude_upper,
    upper_divide,
    upper_multiply,
)


def _up_array(values: np.ndarray) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if np.any(array < 0.0) or np.any(np.isnan(array)):
        raise ValueError("outward arrays must be nonnegative")
    return np.nextafter(array, np.inf)


def _up_add(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return _up_array(
        np.asarray(left, dtype=np.float64)
        + np.asarray(right, dtype=np.float64)
    )


def _up_multiply(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return _up_array(
        np.asarray(left, dtype=np.float64)
        * np.asarray(right, dtype=np.float64)
    )


def _ball_magnitude(ball: ComponentwiseBall) -> np.ndarray:
    return _up_add(magnitude_upper(ball.center), ball.radius)


def _positive_product_upper(
    matrix: np.ndarray, values: np.ndarray
) -> np.ndarray:
    product = componentwise_dense_exact_matmul(
        np.asarray(matrix, dtype=np.float64),
        ComponentwiseBall.exact(np.asarray(values, dtype=np.float64)),
        absolute_matrix=np.asarray(matrix, dtype=np.float64),
    )
    return _ball_magnitude(product)


def _row_sum_upper(matrix: np.ndarray) -> float:
    values = np.asarray(matrix, dtype=np.float64)
    raw = np.sum(values, axis=1, dtype=np.float64)
    denominator = float(
        np.nextafter(1.0 - gamma(2 * values.shape[1] + 8), 0.0)
    )
    raw = np.nextafter(raw / denominator, np.inf)
    return float(np.nextafter(np.max(raw), np.inf))


def _tail_upper(contraction: float, term_maximum: float) -> float:
    numerator = upper_multiply(float(contraction), float(term_maximum))
    denominator = float(np.nextafter(1.0 - float(contraction), 0.0))
    return upper_divide(numerator, denominator)


def positive_fixed_point_upper(
    majorant: np.ndarray,
    source: np.ndarray,
    *,
    maximum_iterations: int = 1024,
    relative_tail_tolerance: float = 2.0e-15,
) -> tuple[np.ndarray, float, int]:
    r"""Bound ``(I-N)^{-1}p`` for nonnegative ``N,p`` by a Neumann sum."""

    matrix = np.asarray(majorant, dtype=np.float64)
    vector = np.asarray(source, dtype=np.float64).reshape(-1)
    if matrix.shape != (vector.size, vector.size):
        raise ValueError("majorant and source have incompatible shapes")
    if np.any(matrix < 0.0) or np.any(vector < 0.0):
        raise ValueError("positive fixed-point data must be nonnegative")
    contraction = _row_sum_upper(matrix)
    if contraction >= 1.0:
        raise RuntimeError("the componentwise preconditioner is not contractive")

    total = _up_array(vector)
    term = _up_array(vector)
    iterations = 0
    for iterations in range(1, int(maximum_iterations) + 1):
        term = _positive_product_upper(matrix, term).reshape(-1)
        total = _up_add(total, term)
        tail = _tail_upper(contraction, float(np.max(term)))
        scale = max(float(np.max(total)), np.finfo(float).tiny)
        if tail <= float(relative_tail_tolerance) * scale:
            break
    else:
        raise RuntimeError("positive fixed-point tail did not converge")

    tail = _tail_upper(contraction, float(np.max(term)))
    total = _up_add(total, np.full(total.shape, tail, dtype=np.float64))
    return total, contraction, iterations


@dataclass(frozen=True)
class CoordinateDisc:
    """Componentwise enclosure of a projected shifted solution on one disc."""

    center: np.ndarray
    radius: np.ndarray
    contraction_upper: float
    fixed_point_iterations: int
    disc_radius: float

    @property
    def ball(self) -> ComponentwiseBall:
        return ComponentwiseBall(self.center, self.radius)

    @property
    def norm_upper(self) -> float:
        return self.ball.norm_upper


def enclose_shifted_coordinates(
    hessenberg: np.ndarray,
    right_hand_side: np.ndarray,
    center: complex,
    radius: float,
) -> CoordinateDisc:
    r"""Enclose ``(zI-H)^{-1}b`` for ``|z-center| <= radius``.

    A stored approximate inverse ``G`` is used only as a preconditioner.  If
    ``D=I-A_0 G`` and ``|D|+radius*|G|`` has row sum below one, then
    ``A(z)G=I-N(z)`` is contractive throughout the disc.  A positive Neumann
    solve bounds the coordinate error around the ordinary centre solve.
    """

    source = np.asarray(right_hand_side, dtype=np.complex128).reshape(-1)
    return enclose_shifted_coordinate_ball(
        hessenberg,
        ComponentwiseBall.exact(source),
        center,
        radius,
    )


def enclose_shifted_coordinate_ball(
    hessenberg: np.ndarray,
    right_hand_side: ComponentwiseBall,
    center: complex,
    radius: float,
) -> CoordinateDisc:
    r"""Enclose a shifted solve whose right-hand side already has a disc.

    The supplied ball may enclose a parameter-dependent right-hand side on
    the whole spectral disc.  Its centre is used for the ordinary centre
    solve, while its componentwise radius enters the preconditioned residual.
    """

    matrix = np.asarray(hessenberg, dtype=np.complex128)
    source_center = np.asarray(
        right_hand_side.center, dtype=np.complex128
    ).reshape(-1)
    source_radius = np.asarray(
        right_hand_side.radius, dtype=np.float64
    ).reshape(-1)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("hessenberg must be square")
    if source_center.shape != (matrix.shape[0],):
        raise ValueError("right-hand side has incompatible shape")
    disc_radius = float(radius)
    if disc_radius < 0.0:
        raise ValueError("disc radius must be nonnegative")

    identity = ComponentwiseBall.exact(
        np.eye(matrix.shape[0], dtype=np.complex128)
    )
    shifted_ball = componentwise_subtract(
        componentwise_scalar_multiply(complex(center), identity),
        ComponentwiseBall.exact(matrix),
    )
    shifted_center = np.asarray(shifted_ball.center, dtype=np.complex128)
    coordinate_center = np.linalg.solve(shifted_center, source_center)
    approximate_inverse = np.linalg.inv(shifted_center)

    product = componentwise_matmul(
        shifted_ball,
        ComponentwiseBall.exact(approximate_inverse),
    )
    defect = componentwise_subtract(identity, product)
    defect_majorant = _ball_magnitude(defect)
    inverse_magnitude = magnitude_upper(approximate_inverse)
    parameter_term = _up_multiply(
        np.full(inverse_magnitude.shape, disc_radius, dtype=np.float64),
        inverse_magnitude,
    )
    contraction_matrix = _up_add(defect_majorant, parameter_term)

    residual_at_center = componentwise_subtract(
        ComponentwiseBall(source_center[:, None], source_radius[:, None]),
        componentwise_matmul(
            shifted_ball,
            ComponentwiseBall.exact(coordinate_center[:, None]),
        ),
    )
    residual_majorant = _ball_magnitude(residual_at_center).reshape(-1)
    parameter_residual = _up_multiply(
        np.full(residual_majorant.shape, disc_radius, dtype=np.float64),
        magnitude_upper(coordinate_center),
    )
    source_majorant = _up_add(residual_majorant, parameter_residual)
    fixed_point, contraction, iterations = positive_fixed_point_upper(
        contraction_matrix,
        source_majorant,
    )
    coordinate_radius = _positive_product_upper(
        inverse_magnitude, fixed_point
    ).reshape(-1)
    return CoordinateDisc(
        center=np.asarray(coordinate_center),
        radius=coordinate_radius,
        contraction_upper=contraction,
        fixed_point_iterations=iterations,
        disc_radius=disc_radius,
    )


def enclose_coordinate_increment(
    hessenberg: np.ndarray,
    base: CoordinateDisc,
    center: complex,
    radius: float,
    *,
    base_depth: int,
) -> CoordinateDisc:
    r"""Enclose the nested FOM increment without losing shift correlation.

    For a Hessenberg matrix of depth ``K`` and its leading ``J`` block,

    ``(zI-H_K)(y_K-iota y_J) = h_{J+1,J}(y_J)_J e_{J+1}``.

    Thus the deep-minus-base coordinates are obtained from one tail-driven
    shifted solve rather than by subtracting two independently widened discs.
    """

    matrix = np.asarray(hessenberg, dtype=np.complex128)
    shallow = int(base_depth)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("hessenberg must be square")
    if shallow < 1 or shallow >= matrix.shape[0]:
        raise ValueError("base depth must be strictly below the deep depth")
    if base.center.shape != (shallow,):
        raise ValueError("base coordinate disc has incompatible depth")
    if np.any(matrix[shallow + 1 :, :shallow] != 0.0):
        raise ValueError("the nested increment identity requires Hessenberg form")

    tail_coordinate_center = np.zeros(matrix.shape[0], dtype=np.complex128)
    tail_coordinate_radius = np.zeros(matrix.shape[0], dtype=np.float64)
    tail_coordinate_center[shallow] = base.center[shallow - 1]
    tail_coordinate_radius[shallow] = base.radius[shallow - 1]
    tail_source = componentwise_scalar_multiply(
        matrix[shallow, shallow - 1],
        ComponentwiseBall(tail_coordinate_center, tail_coordinate_radius),
    )
    return enclose_shifted_coordinate_ball(
        matrix,
        tail_source,
        center,
        radius,
    )


def coordinate_difference(
    deep: CoordinateDisc,
    base: CoordinateDisc,
    *,
    ambient_depth: int,
) -> ComponentwiseBall:
    """Embed and subtract two coordinate discs in one Arnoldi space."""

    depth = int(ambient_depth)
    deep_center = np.zeros(depth, dtype=np.complex128)
    deep_radius = np.zeros(depth, dtype=np.float64)
    base_center = np.zeros(depth, dtype=np.complex128)
    base_radius = np.zeros(depth, dtype=np.float64)
    deep_center[: deep.center.size] = deep.center
    deep_radius[: deep.radius.size] = deep.radius
    base_center[: base.center.size] = base.center
    base_radius[: base.radius.size] = base.radius
    return componentwise_subtract(
        ComponentwiseBall(deep_center, deep_radius),
        ComponentwiseBall(base_center, base_radius),
    )


def coordinate_extension_sum(
    base: CoordinateDisc,
    increment: CoordinateDisc,
) -> CoordinateDisc:
    """Enclose an embedded shallow coordinate plus a deep increment."""

    depth = int(increment.center.size)
    if base.center.size > depth:
        raise ValueError("the base coordinate cannot exceed the deep depth")
    embedded_center = np.zeros(depth, dtype=np.complex128)
    embedded_radius = np.zeros(depth, dtype=np.float64)
    embedded_center[: base.center.size] = base.center
    embedded_radius[: base.radius.size] = base.radius
    combined = componentwise_add(
        ComponentwiseBall(embedded_center, embedded_radius),
        increment.ball,
    )
    return CoordinateDisc(
        center=np.asarray(combined.center),
        radius=np.asarray(combined.radius),
        contraction_upper=max(
            base.contraction_upper, increment.contraction_upper
        ),
        fixed_point_iterations=max(
            base.fixed_point_iterations, increment.fixed_point_iterations
        ),
        disc_radius=max(base.disc_radius, increment.disc_radius),
    )


def nonnegative_frobenius_upper(values: np.ndarray) -> float:
    """Expose the outward Frobenius helper for positive arc data."""

    return frobenius_upper_array(np.asarray(values, dtype=np.float64))
