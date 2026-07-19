"""Certify stored parity circles at dimensions 2048, 4096, and 8192."""

from __future__ import annotations

import argparse
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
RH37 = PAPERS / "RH-37-iterated-dyadic-physical-count"
RH41 = PAPERS / "RH-41-validated-parity-continuum-contour"
RH42 = PAPERS / "RH-42-uniform-euclidean-parity-contour"
sys.path[:0] = [
    str(RH27 / "src"),
    str(RH41 / "experiments"),
    str(RH42 / "src"),
]

import run_coarse_grushin_certificate as coarse  # noqa: E402
from euclidean_contour import euclidean_grushin_ledger  # noqa: E402


SNAPSHOT_36 = (
    RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
)
SNAPSHOT_37 = (
    RH37 / "results" / "second_dyadic_fine_object_sigma_1e-02.npz"
)
OUTPUT = ROOT / "results" / "multilevel_euclidean_grushin.json"
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


def load_level(dimension: int) -> dict[str, object]:
    if dimension in (2048, 4096):
        snapshot = SNAPSHOT_36
        prefix = "coarse" if dimension == 2048 else "fine"
    elif dimension == 8192:
        snapshot = SNAPSHOT_37
        prefix = "fine"
    else:
        raise ValueError(f"unsupported dimension: {dimension}")
    with np.load(snapshot) as data:
        matrix = csr_matrix(
            (
                np.asarray(data[f"{prefix}_matrix_data"]),
                np.asarray(data[f"{prefix}_matrix_indices"]),
                np.asarray(data[f"{prefix}_matrix_indptr"]),
            ),
            shape=tuple(
                int(value) for value in data[f"{prefix}_matrix_shape"]
            ),
        )
        return {
            "snapshot": snapshot,
            "prefix": prefix,
            "matrix": matrix,
            "right": np.asarray(
                data[f"{prefix}_right_modes"][:, 1], dtype=np.float64
            ),
            "left": np.asarray(
                data[f"{prefix}_left_modes"][:, 1], dtype=np.float64
            ),
            "eigenvalue": float(data[f"{prefix}_peripheral_values"][1]),
            "sigma": float(data["sigma"]),
            "critical_u": float(data["critical_u"]),
        }


def certify_level(dimension: int, chunk_size: int) -> dict[str, object]:
    level = load_level(dimension)
    matrix = level["matrix"]
    right = level["right"]
    left = level["left"]
    eigenvalue = float(level["eigenvalue"])
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

    for start in range(0, total_dimension, chunk_size):
        stop = min(total_dimension, start + chunk_size)
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
            f"n={dimension}: certified columns {stop}/{total_dimension}: "
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
    residual_two = upper_product_sqrt(residual_one, residual_infinity)
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
    return {
        "status": status,
        "dimension": dimension,
        "snapshot_prefix": level["prefix"],
        "sigma": level["sigma"],
        "critical_u_binary64": level["critical_u"],
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
            "snapshot": sha256_file(level["snapshot"]),
            "inverse_chunks": inverse_hash.hexdigest(),
            "residual_centers": residual_center_hash.hexdigest(),
            "residual_radii": residual_radius_hash.hexdigest(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--levels", default="2048,4096,8192", help="comma-separated levels"
    )
    parser.add_argument("--chunk-size", type=int, default=256)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    levels = tuple(
        int(value.strip())
        for value in arguments.levels.split(",")
        if value.strip()
    )
    rows = {
        str(dimension): certify_level(dimension, arguments.chunk_size)
        for dimension in levels
    }
    all_closed = all(
        row["status"]
        == "rigorous_exact_stored_euclidean_parity_circle_count_one"
        for row in rows.values()
    )
    payload = {
        "status": (
            "rigorous_multilevel_exact_stored_euclidean_parity_factors"
            if all_closed
            else "multilevel_exact_stored_parity_factor_gate_not_closed"
        ),
        "evidence_level": (
            "componentwise_outward_binary64_bordered_inverse_certificates"
        ),
        "levels": rows,
        "dependencies": {
            "rh36_snapshot": {
                "path": str(SNAPSHOT_36.relative_to(PAPERS.parent)),
                "sha256": sha256_file(SNAPSHOT_36),
            },
            "rh37_snapshot": {
                "path": str(SNAPSHOT_37.relative_to(PAPERS.parent)),
                "sha256": sha256_file(SNAPSHOT_37),
            },
            "rh41_grushin_source": {
                "path": str(
                    (
                        RH41
                        / "experiments"
                        / "run_coarse_grushin_certificate.py"
                    ).relative_to(PAPERS.parent)
                ),
                "sha256": sha256_file(
                    RH41
                    / "experiments"
                    / "run_coarse_grushin_certificate.py"
                ),
            },
            "rh42_euclidean_grushin_source": {
                "path": str(
                    (
                        RH42 / "src" / "euclidean_contour" / "grushin.py"
                    ).relative_to(PAPERS.parent)
                ),
                "sha256": sha256_file(
                    RH42 / "src" / "euclidean_contour" / "grushin.py"
                ),
            },
        },
        "source_sha256": sha256_file(Path(__file__)),
        "limitations": [
            "Each contour is centered at its stored binary64 parity eigenvalue approximation.",
            "The result validates the stored matrices and factors, not every future binary64 Gaussian rebuild.",
        ],
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if not all_closed:
        raise RuntimeError("at least one multilevel Grushin gate failed")


if __name__ == "__main__":
    main()
