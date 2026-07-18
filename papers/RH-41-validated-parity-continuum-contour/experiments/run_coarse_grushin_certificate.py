"""Certify one negative-resonance circle for the exact stored 4096 matrix."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys
import time

from flint import arb, ctx
import numpy as np
from scipy.sparse import bmat, csc_matrix, csr_matrix, eye
from scipy.sparse.linalg import splu


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
sys.path[:0] = [str(ROOT / "src"), str(RH27 / "src")]

from outward_residuals import (  # noqa: E402
    ComponentwiseBall,
    componentwise_add,
    componentwise_dense_exact_matmul,
    componentwise_negate,
    componentwise_scalar_multiply,
    componentwise_scale_rows,
    componentwise_sparse_exact_matmul,
    gamma,
    magnitude_upper,
)
from parity_contour import grushin_contour_ledger  # noqa: E402


SNAPSHOT = RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
OUTPUT = ROOT / "results" / "coarse_grushin_contour_certificate.json"
CHUNK_SIZE = 256
BORDER_SCALE = 16.0
CONTOUR_RADIUS = 0.05


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def upper_float(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower_float(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def _up(values: np.ndarray) -> np.ndarray:
    array = np.asarray(values, dtype=np.float64)
    if np.any(array < 0.0) or np.any(np.isnan(array)):
        raise ValueError("row-sum bounds must be nonnegative")
    return np.nextafter(array, np.inf)


def row_sum_upper(center: np.ndarray, radius: np.ndarray | None = None) -> np.ndarray:
    values = np.asarray(center)
    if values.ndim != 2:
        raise ValueError("row-sum accumulation requires a matrix")
    terms = magnitude_upper(values)
    if radius is not None:
        terms = _up(terms + np.asarray(radius, dtype=np.float64))
    raw = np.sum(terms, axis=1, dtype=np.float64)
    denominator = math.nextafter(
        1.0 - gamma(2 * values.shape[1] + 8), 0.0
    )
    return _up(raw / denominator)


def accumulate(total: np.ndarray, addition: np.ndarray) -> None:
    total[:] = _up(total + np.asarray(addition, dtype=np.float64))


def scalar_sum_upper(values: np.ndarray) -> float:
    vector = np.asarray(values).reshape(1, -1)
    return float(row_sum_upper(vector)[0])


def vector_ball_norms(ball: ComponentwiseBall) -> tuple[float, float]:
    center = np.asarray(ball.center).reshape(-1, 1)
    radius = np.asarray(ball.radius).reshape(-1, 1)
    entries = row_sum_upper(center, radius)
    infinity = float(np.max(entries))
    one = float(row_sum_upper(entries.reshape(1, -1))[0])
    return infinity, one


def exact_gram(right: np.ndarray, left: np.ndarray) -> tuple[float, float, str]:
    previous = ctx.prec
    ctx.prec = 224
    try:
        value = arb(0)
        for r_value, l_value in zip(right, left, strict=True):
            value += arb(float(r_value)) * arb(float(l_value))
        return lower_float(value), upper_float(value), str(value)
    finally:
        ctx.prec = previous


def mode_residuals(
    matrix: csr_matrix,
    right: np.ndarray,
    left: np.ndarray,
    eigenvalue: float,
) -> tuple[ComponentwiseBall, ComponentwiseBall]:
    absolute = matrix.copy()
    absolute.data = magnitude_upper(matrix.data)
    maximum_row = int(np.max(np.diff(matrix.indptr)))
    right_image = componentwise_sparse_exact_matmul(
        matrix,
        ComponentwiseBall.exact(right),
        absolute_matrix=absolute,
        maximum_row_nonzeros=maximum_row,
    )
    right_scaled = componentwise_scale_rows(
        np.full(right.shape, eigenvalue, dtype=np.float64),
        ComponentwiseBall.exact(right),
    )
    right_residual = componentwise_add(
        right_image, componentwise_negate(right_scaled)
    )

    transpose = matrix.T.tocsr()
    transpose_absolute = transpose.copy()
    transpose_absolute.data = magnitude_upper(transpose.data)
    maximum_column = int(np.max(np.diff(transpose.indptr)))
    left_image = componentwise_sparse_exact_matmul(
        transpose,
        ComponentwiseBall.exact(left),
        absolute_matrix=transpose_absolute,
        maximum_row_nonzeros=maximum_column,
    )
    left_scaled = componentwise_scale_rows(
        np.full(left.shape, eigenvalue, dtype=np.float64),
        ComponentwiseBall.exact(left),
    )
    left_residual = componentwise_add(
        left_image, componentwise_negate(left_scaled)
    )
    return right_residual, left_residual


def exact_bordered_action(
    matrix: csr_matrix,
    matrix_absolute: csr_matrix,
    maximum_matrix_row_nonzeros: int,
    right: np.ndarray,
    left: np.ndarray,
    eigenvalue: float,
    scale: float,
    source: ComponentwiseBall,
) -> ComponentwiseBall:
    """Apply the exact stored bordered graph without rounded matrix assembly."""

    dimension = int(matrix.shape[0])
    center = np.asarray(source.center)
    radius = np.asarray(source.radius)
    physical = ComponentwiseBall(center[:dimension, :], radius[:dimension, :])
    auxiliary = ComponentwiseBall(center[dimension:, :], radius[dimension:, :])
    shifted = componentwise_scalar_multiply(eigenvalue, physical)
    matrix_part = componentwise_sparse_exact_matmul(
        matrix,
        physical,
        absolute_matrix=matrix_absolute,
        maximum_row_nonzeros=maximum_matrix_row_nonzeros,
    )
    top = componentwise_add(shifted, componentwise_negate(matrix_part))
    right_part = componentwise_dense_exact_matmul(
        right[:, None],
        auxiliary,
        absolute_matrix=magnitude_upper(right[:, None]),
    )
    top = componentwise_add(
        top, componentwise_scalar_multiply(scale, right_part)
    )
    bottom = componentwise_dense_exact_matmul(
        left[None, :],
        physical,
        absolute_matrix=magnitude_upper(left[None, :]),
    )
    bottom = componentwise_scalar_multiply(1.0 / scale, bottom)
    return ComponentwiseBall(
        np.vstack((np.asarray(top.center), np.asarray(bottom.center))),
        np.vstack((np.asarray(top.radius), np.asarray(bottom.radius))),
    )


def main() -> None:
    with np.load(SNAPSHOT) as data:
        matrix = csr_matrix(
            (
                np.asarray(data["fine_matrix_data"]),
                np.asarray(data["fine_matrix_indices"]),
                np.asarray(data["fine_matrix_indptr"]),
            ),
            shape=tuple(int(value) for value in data["fine_matrix_shape"]),
        )
        right = np.asarray(data["fine_right_modes"][:, 1], dtype=np.float64)
        left = np.asarray(data["fine_left_modes"][:, 1], dtype=np.float64)
        eigenvalue = float(data["fine_peripheral_values"][1])
        sigma = float(data["sigma"])
        critical_u = float(data["critical_u"])

    dimension = int(matrix.shape[0])
    scale = float(BORDER_SCALE)
    base = eigenvalue * eye(dimension, format="csc") - matrix.tocsc()
    bordered = bmat(
        [
            [base, csc_matrix((scale * right)[:, None])],
            [csc_matrix((left / scale)[None, :]), csc_matrix((1, 1))],
        ],
        format="csc",
    )
    matrix_absolute = matrix.copy()
    matrix_absolute.data = magnitude_upper(matrix.data)
    maximum_matrix_row_nonzeros = int(np.max(np.diff(matrix.indptr)))

    factor_started = time.perf_counter()
    factor = splu(
        bordered,
        permc_spec="COLAMD",
        diag_pivot_thresh=1.0,
        options={"Equil": False, "IterRefine": "DOUBLE"},
    )
    factor_seconds = time.perf_counter() - factor_started
    total_dimension = dimension + 1
    inverse_rows = np.zeros(total_dimension, dtype=np.float64)
    residual_rows = np.zeros(total_dimension, dtype=np.float64)
    reduced_rows = np.zeros(dimension, dtype=np.float64)
    left_channel_values = np.zeros(dimension, dtype=np.float64)
    right_channel_approximate = None
    effective_scalar_approximate = None
    inverse_hash = hashlib.sha256()
    residual_center_hash = hashlib.sha256()
    residual_radius_hash = hashlib.sha256()
    certificate_started = time.perf_counter()

    for start in range(0, total_dimension, CHUNK_SIZE):
        stop = min(total_dimension, start + CHUNK_SIZE)
        width = stop - start
        source = np.zeros((total_dimension, width), dtype=np.float64)
        source[np.arange(start, stop), np.arange(width)] = 1.0
        approximate = np.ascontiguousarray(factor.solve(source))
        inverse_hash.update(approximate.view(np.uint8))
        accumulate(inverse_rows, row_sum_upper(approximate))

        physical_stop = min(stop, dimension)
        if start < physical_stop:
            physical_width = physical_stop - start
            accumulate(
                reduced_rows,
                row_sum_upper(approximate[:dimension, :physical_width]),
            )
            left_channel_values[start:physical_stop] = np.abs(
                approximate[dimension, :physical_width]
            )
        if start <= dimension < stop:
            border_column = dimension - start
            right_channel_approximate = np.asarray(
                approximate[:dimension, border_column]
            )
            effective_scalar_approximate = float(
                approximate[dimension, border_column]
            )

        image = exact_bordered_action(
            matrix,
            matrix_absolute,
            maximum_matrix_row_nonzeros,
            right,
            left,
            eigenvalue,
            scale,
            ComponentwiseBall.exact(approximate),
        )
        residual = componentwise_add(
            ComponentwiseBall.exact(source), componentwise_negate(image)
        )
        residual_center = np.ascontiguousarray(residual.center)
        residual_radius = np.ascontiguousarray(residual.radius)
        residual_center_hash.update(residual_center.view(np.uint8))
        residual_radius_hash.update(residual_radius.view(np.uint8))
        accumulate(
            residual_rows,
            row_sum_upper(residual_center, residual_radius),
        )
        print(
            f"certified columns {stop}/{total_dimension}: "
            f"R_inf={float(np.max(inverse_rows)):.6e}, "
            f"E_inf={float(np.max(reduced_rows)):.6e}, "
            f"residual_inf={float(np.max(residual_rows)):.3e}",
            flush=True,
        )

    if right_channel_approximate is None or effective_scalar_approximate is None:
        raise RuntimeError("the bordered column was not processed")
    residual_upper = float(np.max(residual_rows))
    approximate_inverse_upper = float(np.max(inverse_rows))
    if residual_upper >= 1.0:
        inverse_upper = math.inf
        inverse_correction = math.inf
    else:
        denominator = math.nextafter(1.0 - residual_upper, 0.0)
        inverse_upper = math.nextafter(
            approximate_inverse_upper / denominator, math.inf
        )
        inverse_correction = math.nextafter(
            inverse_upper * residual_upper, math.inf
        )
    reduced_upper = math.nextafter(
        float(np.max(reduced_rows)) + inverse_correction, math.inf
    )
    right_channel_upper = math.nextafter(
        float(np.max(magnitude_upper(right_channel_approximate)))
        + inverse_correction,
        math.inf,
    )
    left_channel_upper = math.nextafter(
        scalar_sum_upper(left_channel_values) + inverse_correction,
        math.inf,
    )
    effective_scalar_upper = math.nextafter(
        abs(effective_scalar_approximate) + inverse_correction,
        math.inf,
    )

    right_residual, left_residual = mode_residuals(
        matrix, right, left, eigenvalue
    )
    right_residual_infinity, _ = vector_ball_norms(right_residual)
    _, left_residual_one = vector_ball_norms(left_residual)
    gram_lower, gram_upper, gram_ball = exact_gram(right, left)
    right_mode_infinity = float(np.max(magnitude_upper(right)))
    left_mode_one = scalar_sum_upper(left)

    contour = grushin_contour_ledger(
        radius=CONTOUR_RADIUS,
        center_reduced_inverse_upper=reduced_upper,
        right_mode_infinity_upper=right_mode_infinity,
        left_mode_one_upper=left_mode_one,
        right_residual_infinity_upper=right_residual_infinity,
        left_residual_one_upper=left_residual_one,
        gram_lower=gram_lower,
        gram_upper=gram_upper,
        border_scale=scale,
    )
    status = (
        "rigorous_exact_stored_parity_circle_count_one"
        if residual_upper < 1.0 and contour.rouche_count_one
        else "coarse_grushin_circle_not_closed"
    )
    payload = {
        "status": status,
        "evidence_level": "rigorous_exact_stored_binary64_grushin_certificate",
        "dimension": dimension,
        "sigma": sigma,
        "critical_u_binary64": critical_u,
        "center": eigenvalue,
        "radius": CONTOUR_RADIUS,
        "border_scale": scale,
        "factor_nnz": int(factor.L.nnz + factor.U.nnz),
        "factor_seconds": factor_seconds,
        "certificate_seconds": time.perf_counter() - certificate_started,
        "approximate_inverse_infinity_upper": approximate_inverse_upper,
        "residual_infinity_upper": residual_upper,
        "bordered_inverse_infinity_upper": inverse_upper,
        "inverse_correction_infinity_upper": inverse_correction,
        "center_reduced_inverse_infinity_upper": reduced_upper,
        "center_right_channel_infinity_upper": right_channel_upper,
        "center_left_channel_one_upper": left_channel_upper,
        "center_effective_scalar_abs_upper": effective_scalar_upper,
        "right_mode_infinity_upper": right_mode_infinity,
        "left_mode_one_upper": left_mode_one,
        "right_residual_infinity_upper": right_residual_infinity,
        "left_residual_one_upper": left_residual_one,
        "left_right_gram_ball": gram_ball,
        "left_right_gram_lower": gram_lower,
        "left_right_gram_upper": gram_upper,
        "contour_ledger": contour.as_dict(),
        "hashes": {
            "snapshot": sha256_file(SNAPSHOT),
            "inverse_chunks": inverse_hash.hexdigest(),
            "residual_centers": residual_center_hash.hexdigest(),
            "residual_radii": residual_radius_hash.hexdigest(),
            "source": sha256_file(Path(__file__)),
        },
        "limitations": [
            "This certificate proves one eigenvalue only for the exact stored binary64 4096 matrix.",
            "The continuum transfer is a separate Galerkin and kernel-approximation theorem.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if status != "rigorous_exact_stored_parity_circle_count_one":
        raise RuntimeError("the coarse Grushin contour certificate did not close")


if __name__ == "__main__":
    main()
