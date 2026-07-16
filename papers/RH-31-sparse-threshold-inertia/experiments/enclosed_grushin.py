"""Power-of-two-balanced Grushin enclosure for the exact RH-29 target."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from flint import arb, ctx
from scipy.sparse import bmat, csc_matrix, eye

from outward_residuals import (
    ComponentwiseBall,
    ComponentwiseStoredFactorGraph,
    componentwise_add,
    componentwise_adjoint,
    componentwise_scalar_multiply,
    componentwise_scale_rows,
    frobenius_upper_array,
    magnitude_upper,
)
from sparse_grushin import LowRankUpdate, SparseGrushinSystem
from threshold_inertia.rounding import gamma, upper_add, upper_multiply


@dataclass(frozen=True)
class EnclosedGrushinSystem:
    """A stored center enclosing one exact Grushin matrix entrywise."""

    system: SparseGrushinSystem
    matrix_error_frobenius_upper: float
    threshold_transform_error_frobenius_upper: float
    lift_coefficient_lower: float
    lift_coefficient_upper: float
    power_of_two_scales: np.ndarray
    column_radii: np.ndarray
    row_radii: np.ndarray


def _arb_exact_norm(values: np.ndarray) -> arb:
    total = arb(0)
    array = np.asarray(values).reshape(-1)
    for value in array:
        if np.iscomplexobj(array):
            real = arb(float(np.real(value)))
            imag = arb(float(np.imag(value)))
            total += real * real + imag * imag
        else:
            scalar = arb(float(value))
            total += scalar * scalar
    return total.sqrt()


def normalized_lift_coefficient_interval(
    singular_value: float,
    left: np.ndarray,
    right: np.ndarray,
    *,
    lift: float = 1.0,
    precision: int = 160,
) -> tuple[float, float]:
    previous = ctx.prec
    ctx.prec = int(precision)
    try:
        coefficient = (arb(float(lift)) - arb(float(singular_value))) / (
            _arb_exact_norm(left) * _arb_exact_norm(right)
        )
        lower = float(np.nextafter(float(coefficient.lower()), -np.inf))
        upper = float(np.nextafter(float(coefficient.upper()), np.inf))
    finally:
        ctx.prec = previous
    if not (0.0 < lower <= upper):
        raise ValueError("lift coefficient interval must be positive")
    return lower, upper


def interval_scalar_multiply(
    lower: float,
    upper: float,
    ball: ComponentwiseBall,
) -> ComponentwiseBall:
    midpoint = float(0.5 * (float(lower) + float(upper)))
    half_width = float(
        np.nextafter(
            max(midpoint - float(lower), float(upper) - midpoint), np.inf
        )
    )
    central = componentwise_scalar_multiply(midpoint, ball)
    magnitude = np.nextafter(
        magnitude_upper(ball.center) + np.asarray(ball.radius), np.inf
    )
    uncertainty = ComponentwiseBall(
        np.zeros_like(ball.center),
        np.nextafter(half_width * magnitude, np.inf),
    )
    return componentwise_add(central, uncertainty)


def _power_of_two_balance(
    columns: np.ndarray,
    column_radii: np.ndarray,
    rows: np.ndarray,
    row_radii: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Balance channels using only exactly reversible binary scalings."""

    def exact_ldexp(values: np.ndarray, exponent: int) -> np.ndarray:
        array = np.asarray(values)
        with np.errstate(over="ignore", under="ignore", invalid="ignore"):
            if np.iscomplexobj(array):
                scaled = np.ldexp(array.real, exponent) + 1.0j * np.ldexp(
                    array.imag, exponent
                )
                restored = np.ldexp(scaled.real, -exponent) + 1.0j * np.ldexp(
                    scaled.imag, -exponent
                )
            else:
                scaled = np.ldexp(array, exponent)
                restored = np.ldexp(scaled, -exponent)
        if not np.all(np.isfinite(scaled)) or not np.array_equal(restored, array):
            raise ArithmeticError("power-of-two scaling was not exactly reversible")
        return scaled

    x = np.asarray(columns, dtype=np.complex128).copy()
    xr = np.asarray(column_radii, dtype=np.float64).copy()
    y = np.asarray(rows, dtype=np.complex128).copy()
    yr = np.asarray(row_radii, dtype=np.float64).copy()
    scales = np.ones(x.shape[1], dtype=np.float64)
    for index in range(x.shape[1]):
        column_norm = float(np.linalg.norm(x[:, index]))
        row_norm = float(np.linalg.norm(y[index, :]))
        if column_norm == 0.0 or row_norm == 0.0:
            continue
        ideal = np.sqrt(row_norm / column_norm)
        if not np.isfinite(ideal) or ideal <= 0.0:
            continue
        exponent = int(np.rint(np.log2(ideal)))
        scale = float(np.ldexp(1.0, exponent))
        if not np.isfinite(scale) or scale <= 0.0:
            continue
        try:
            scaled_x = exact_ldexp(x[:, index], exponent)
            scaled_xr = exact_ldexp(xr[:, index], exponent)
            scaled_y = exact_ldexp(y[index, :], -exponent)
            scaled_yr = exact_ldexp(yr[index, :], -exponent)
        except ArithmeticError:
            continue
        x[:, index] = scaled_x
        xr[:, index] = scaled_xr
        y[index, :] = scaled_y
        yr[index, :] = scaled_yr
        scales[index] = scale
    return x, xr, y, yr, scales


def build_enclosed_grushin_system(
    matrix,
    right_modes: np.ndarray,
    left_modes: np.ndarray,
    peripheral_values: np.ndarray,
    synthesis: np.ndarray,
    analysis: np.ndarray,
    dangerous_left: np.ndarray,
    dangerous_right: np.ndarray,
    singular_value: float,
    spectral_parameter: complex,
    threshold: float,
    *,
    lift: float = 1.0,
) -> EnclosedGrushinSystem:
    """Enclose an exact Grushin matrix whose physical Schur block is RH-29."""

    sparse = csc_matrix(matrix, dtype=np.complex128)
    dimension = int(sparse.shape[0])
    right = np.asarray(right_modes)
    left = np.asarray(left_modes)
    values = np.asarray(peripheral_values)
    synthesis_values = np.asarray(synthesis)
    analysis_values = np.asarray(analysis)
    u0 = np.asarray(dangerous_left).reshape(-1)
    v0 = np.asarray(dangerous_right).reshape(-1)
    graph = ComponentwiseStoredFactorGraph(
        sparse,
        right,
        left,
        values,
        synthesis_values,
        analysis_values,
    )
    uv = graph.one_step(ComponentwiseBall.exact(synthesis_values))
    wu_adjoint = graph.one_step_adjoint(
        ComponentwiseBall.exact(analysis_values.conj().T)
    )
    wu = componentwise_adjoint(wu_adjoint)
    peripheral_rows = componentwise_scale_rows(
        values, ComponentwiseBall.exact(left.T)
    )
    coefficient_interval = normalized_lift_coefficient_interval(
        singular_value, u0, v0, lift=lift
    )
    lift_row = interval_scalar_multiply(
        *coefficient_interval,
        ComponentwiseBall.exact(v0.conj()[None, :]),
    )

    columns: list[np.ndarray] = []
    column_radii: list[np.ndarray] = []
    rows: list[np.ndarray] = []
    row_radii: list[np.ndarray] = []
    labels: list[str] = []

    def append(
        column_center: np.ndarray,
        column_radius: np.ndarray,
        row_center: np.ndarray,
        row_radius: np.ndarray,
        label: str,
    ) -> None:
        columns.append(np.asarray(column_center).reshape(-1))
        column_radii.append(np.asarray(column_radius).reshape(-1))
        rows.append(np.asarray(row_center).reshape(-1))
        row_radii.append(np.asarray(row_radius).reshape(-1))
        labels.append(label)

    zero_column = np.zeros(2 * dimension, dtype=np.complex128)
    zero_radius_column = np.zeros(2 * dimension, dtype=np.float64)
    zero_row = np.zeros(2 * dimension, dtype=np.complex128)
    zero_radius_row = np.zeros(2 * dimension, dtype=np.float64)

    column = zero_column.copy()
    column[:dimension] = u0
    row = zero_row.copy()
    row[:dimension] = lift_row.center[0, :]
    row_radius = zero_radius_row.copy()
    row_radius[:dimension] = lift_row.radius[0, :]
    append(
        column,
        zero_radius_column,
        row,
        row_radius,
        "lift",
    )

    for index in range(right.shape[1]):
        column = zero_column.copy()
        column[:dimension] = right[:, index]
        row = zero_row.copy()
        row[dimension:] = peripheral_rows.center[index, :]
        row_radius = zero_radius_row.copy()
        row_radius[dimension:] = peripheral_rows.radius[index, :]
        append(
            column,
            zero_radius_column,
            row,
            row_radius,
            f"top_peripheral_{index}",
        )
    for index in range(synthesis_values.shape[1]):
        column = zero_column.copy()
        column[:dimension] = synthesis_values[:, index]
        row = zero_row.copy()
        row[dimension:] = wu.center[index, :]
        row_radius = zero_radius_row.copy()
        row_radius[dimension:] = wu.radius[index, :]
        append(
            column,
            zero_radius_column,
            row,
            row_radius,
            f"top_packet_{index}",
        )

    for index in range(right.shape[1]):
        column = zero_column.copy()
        column[dimension:] = right[:, index]
        row = zero_row.copy()
        row[:dimension] = peripheral_rows.center[index, :]
        row_radius = zero_radius_row.copy()
        row_radius[:dimension] = peripheral_rows.radius[index, :]
        append(
            column,
            zero_radius_column,
            row,
            row_radius,
            f"bottom_peripheral_{index}",
        )
    for index in range(synthesis_values.shape[1]):
        column = zero_column.copy()
        column[dimension:] = uv.center[:, index]
        column_radius = zero_radius_column.copy()
        column_radius[dimension:] = uv.radius[:, index]
        row = zero_row.copy()
        row[:dimension] = analysis_values[index, :]
        append(
            column,
            column_radius,
            row,
            zero_radius_row,
            f"bottom_packet_{index}",
        )

    x = np.column_stack(columns)
    xr = np.column_stack(column_radii)
    y = np.vstack(rows)
    yr = np.vstack(row_radii)
    x, xr, y, yr, scales = _power_of_two_balance(x, xr, y, yr)
    update = LowRankUpdate(
        columns=x,
        rows=y,
        channel_labels=tuple(labels),
        channel_scales=scales,
    )
    identity = eye(dimension, format="csc", dtype=np.complex128)
    base = bmat(
        [
            [complex(spectral_parameter) * identity, -sparse],
            [-sparse, identity],
        ],
        format="csc",
    )
    bordered = bmat(
        [
            [base, csc_matrix(x)],
            [csc_matrix(y), -eye(update.rank, format="csc", dtype=np.complex128)],
        ],
        format="csc",
    )
    system = SparseGrushinSystem(
        matrix=bordered,
        base=base,
        update=update,
        physical_dimension=dimension,
        auxiliary_scale=1.0,
    )
    x_error = frobenius_upper_array(xr)
    y_error = frobenius_upper_array(yr)
    squared_matrix_error = upper_add(
        upper_multiply(x_error, x_error),
        upper_multiply(y_error, y_error),
    )
    matrix_error = float(
        np.nextafter(np.sqrt(squared_matrix_error), np.inf)
    )
    center_frobenius = frobenius_upper_array(bordered.data)
    bordered_root_dimension = float(
        np.nextafter(np.sqrt(float(bordered.shape[0])), np.inf)
    )
    transform_roundoff = upper_multiply(
        gamma(64),
        upper_add(
            upper_multiply(8.0, center_frobenius),
            upper_multiply(
                4.0 * float(threshold), bordered_root_dimension
            ),
        ),
    )
    hadamard_error_factor = float(
        np.nextafter(2.0 * np.sqrt(2.0), np.inf)
    )
    transformed_error = upper_add(
        upper_multiply(hadamard_error_factor, matrix_error),
        transform_roundoff,
    )
    return EnclosedGrushinSystem(
        system=system,
        matrix_error_frobenius_upper=matrix_error,
        threshold_transform_error_frobenius_upper=transformed_error,
        lift_coefficient_lower=coefficient_interval[0],
        lift_coefficient_upper=coefficient_interval[1],
        power_of_two_scales=scales,
        column_radii=xr,
        row_radii=yr,
    )
