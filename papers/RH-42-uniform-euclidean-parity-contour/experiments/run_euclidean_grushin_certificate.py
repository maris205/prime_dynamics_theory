"""Certify the stored 4096 parity circle in Euclidean norm."""

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
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH41 = PAPERS / "RH-41-validated-parity-continuum-contour"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH27 / "src"),
    str(RH41 / "experiments"),
]

import run_coarse_grushin_certificate as coarse  # noqa: E402
from euclidean_contour import euclidean_grushin_ledger  # noqa: E402


SNAPSHOT = RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
OUTPUT = ROOT / "results" / "euclidean_grushin_contour_certificate.json"
CHUNK_SIZE = 256
BORDER_SCALE = 16.0
CONTOUR_RADIUS = 0.05


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def upper_product_sqrt(one_upper: float, infinity_upper: float) -> float:
    product = math.nextafter(
        float(one_upper) * float(infinity_upper), math.inf
    )
    return math.nextafter(math.sqrt(product), math.inf)


def exact_l2_norm(vector: np.ndarray) -> tuple[float, str]:
    previous = ctx.prec
    ctx.prec = 224
    try:
        square = arb(0)
        for value in np.asarray(vector, dtype=np.float64):
            exact = arb(float(value))
            square += exact * exact
        norm = square.sqrt()
        return coarse.upper_float(norm), str(norm)
    finally:
        ctx.prec = previous


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
    matrix_absolute.data = coarse.magnitude_upper(matrix.data)
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
    inverse_one = 0.0
    residual_one = 0.0
    reduced_one = 0.0
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
        coarse.accumulate(inverse_rows, coarse.row_sum_upper(approximate))
        inverse_one = max(
            inverse_one,
            float(np.max(coarse.row_sum_upper(approximate.T))),
        )

        physical_stop = min(stop, dimension)
        if start < physical_stop:
            physical_width = physical_stop - start
            physical_block = approximate[:dimension, :physical_width]
            coarse.accumulate(
                reduced_rows, coarse.row_sum_upper(physical_block)
            )
            reduced_one = max(
                reduced_one,
                float(np.max(coarse.row_sum_upper(physical_block.T))),
            )

        image = coarse.exact_bordered_action(
            matrix,
            matrix_absolute,
            maximum_matrix_row_nonzeros,
            right,
            left,
            eigenvalue,
            scale,
            coarse.ComponentwiseBall.exact(approximate),
        )
        residual = coarse.componentwise_add(
            coarse.ComponentwiseBall.exact(source),
            coarse.componentwise_negate(image),
        )
        residual_center = np.ascontiguousarray(residual.center)
        residual_radius = np.ascontiguousarray(residual.radius)
        residual_center_hash.update(residual_center.view(np.uint8))
        residual_radius_hash.update(residual_radius.view(np.uint8))
        coarse.accumulate(
            residual_rows,
            coarse.row_sum_upper(residual_center, residual_radius),
        )
        residual_one = max(
            residual_one,
            float(
                np.max(
                    coarse.row_sum_upper(
                        residual_center.T, residual_radius.T
                    )
                )
            ),
        )
        print(
            f"certified columns {stop}/{total_dimension}: "
            f"X_1={inverse_one:.6e}, "
            f"X_inf={float(np.max(inverse_rows)):.6e}, "
            f"R_2<={upper_product_sqrt(residual_one, float(np.max(residual_rows))):.3e}",
            flush=True,
        )

    inverse_infinity = float(np.max(inverse_rows))
    residual_infinity = float(np.max(residual_rows))
    approximate_inverse_two = upper_product_sqrt(
        inverse_one, inverse_infinity
    )
    residual_two = upper_product_sqrt(
        residual_one, residual_infinity
    )
    if residual_two >= 1.0:
        inverse_two = math.inf
        inverse_correction_two = math.inf
    else:
        denominator = math.nextafter(1.0 - residual_two, 0.0)
        inverse_two = math.nextafter(
            approximate_inverse_two / denominator, math.inf
        )
        inverse_correction_two = math.nextafter(
            inverse_two * residual_two, math.inf
        )
    approximate_reduced_two = upper_product_sqrt(
        reduced_one, float(np.max(reduced_rows))
    )
    reduced_two = math.nextafter(
        approximate_reduced_two + inverse_correction_two, math.inf
    )

    right_residual, left_residual = coarse.mode_residuals(
        matrix, right, left, eigenvalue
    )
    right_residual_infinity, right_residual_one = (
        coarse.vector_ball_norms(right_residual)
    )
    left_residual_infinity, left_residual_one = (
        coarse.vector_ball_norms(left_residual)
    )
    right_residual_two = upper_product_sqrt(
        right_residual_one, right_residual_infinity
    )
    left_residual_two = upper_product_sqrt(
        left_residual_one, left_residual_infinity
    )
    right_mode_two, right_mode_ball = exact_l2_norm(right)
    left_mode_two, left_mode_ball = exact_l2_norm(left)
    gram_lower, gram_upper, gram_ball = coarse.exact_gram(right, left)

    contour = euclidean_grushin_ledger(
        radius=CONTOUR_RADIUS,
        center_reduced_inverse_upper=reduced_two,
        right_mode_two_upper=right_mode_two,
        left_mode_two_upper=left_mode_two,
        right_residual_two_upper=right_residual_two,
        left_residual_two_upper=left_residual_two,
        gram_lower=gram_lower,
        gram_upper=gram_upper,
        border_scale=scale,
    )
    status = (
        "rigorous_exact_stored_euclidean_parity_circle_count_one"
        if residual_two < 1.0 and contour.rouche_count_one
        else "stored_euclidean_grushin_circle_not_closed"
    )
    payload = {
        "status": status,
        "evidence_level": (
            "rigorous_exact_stored_binary64_euclidean_grushin_certificate"
        ),
        "dimension": dimension,
        "sigma": sigma,
        "critical_u_binary64": critical_u,
        "center": eigenvalue,
        "radius": CONTOUR_RADIUS,
        "border_scale": scale,
        "factor_nnz": int(factor.L.nnz + factor.U.nnz),
        "factor_seconds": factor_seconds,
        "certificate_seconds": time.perf_counter() - certificate_started,
        "approximate_inverse_one_upper": inverse_one,
        "approximate_inverse_infinity_upper": inverse_infinity,
        "approximate_inverse_two_upper": approximate_inverse_two,
        "residual_one_upper": residual_one,
        "residual_infinity_upper": residual_infinity,
        "residual_two_upper": residual_two,
        "bordered_inverse_two_upper": inverse_two,
        "inverse_correction_two_upper": inverse_correction_two,
        "approximate_center_reduced_one_upper": reduced_one,
        "approximate_center_reduced_infinity_upper": float(
            np.max(reduced_rows)
        ),
        "approximate_center_reduced_two_upper": approximate_reduced_two,
        "center_reduced_inverse_two_upper": reduced_two,
        "right_mode_two_upper": right_mode_two,
        "right_mode_two_ball": right_mode_ball,
        "left_mode_two_upper": left_mode_two,
        "left_mode_two_ball": left_mode_ball,
        "right_residual_two_upper": right_residual_two,
        "left_residual_two_upper": left_residual_two,
        "left_right_gram_ball": gram_ball,
        "left_right_gram_lower": gram_lower,
        "left_right_gram_upper": gram_upper,
        "contour_ledger": contour.as_dict(),
        "hashes": {
            "snapshot": sha256_file(SNAPSHOT),
            "rh41_coarse_source": sha256_file(
                RH41 / "experiments" / "run_coarse_grushin_certificate.py"
            ),
            "inverse_chunks": inverse_hash.hexdigest(),
            "residual_centers": residual_center_hash.hexdigest(),
            "residual_radii": residual_radius_hash.hexdigest(),
            "source": sha256_file(Path(__file__)),
        },
        "limitations": [
            "The certificate is for the exact stored binary64 4096 matrix.",
            "The continuum and sparse-family transfers are separate Hilbert-space perturbation theorems.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if status != "rigorous_exact_stored_euclidean_parity_circle_count_one":
        raise RuntimeError("the Euclidean Grushin contour did not close")


if __name__ == "__main__":
    main()
