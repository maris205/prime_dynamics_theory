"""Arb Frobenius bridge from the stored matrix to the exact midpoint matrix."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

from flint import arb, ctx
import numpy as np
from scipy.sparse import csr_matrix


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH41 = PAPERS / "RH-41-validated-parity-continuum-contour"
sys.path.insert(0, str(RH41 / "experiments"))

import build_midpoint_bridge_certificate as base  # noqa: E402


SNAPSHOT = RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
OUTPUT = ROOT / "results" / "euclidean_stored_to_midpoint_bridge.json"
PRECISION = 224


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    previous = ctx.prec
    ctx.prec = PRECISION
    try:
        lower = arb(base.CRITICAL_U_LOWER)
        upper = arb(base.CRITICAL_U_UPPER)
        lower_polynomial = base.critical_polynomial(lower)
        upper_polynomial = base.critical_polynomial(upper)
        root_bracket_valid = bool(
            lower_polynomial < 0 and upper_polynomial > 0
        )
        critical_u = arb(f"{base.CRITICAL_U_MIDPOINT} +/- 1e-60")
        sigma = arb(1) / 100

        with np.load(SNAPSHOT) as data:
            matrix = csr_matrix(
                (
                    np.asarray(data["fine_matrix_data"]),
                    np.asarray(data["fine_matrix_indices"]),
                    np.asarray(data["fine_matrix_indptr"]),
                ),
                shape=tuple(
                    int(value) for value in data["fine_matrix_shape"]
                ),
            )

        dimension = int(matrix.shape[0])
        row_counts = np.diff(matrix.indptr)
        half_width = int((int(np.max(row_counts)) - 1) // 2)
        tail = base.omitted_midpoint_mass_upper(
            dimension, half_width, sigma
        )
        support_square = arb(0)
        total_square = arb(0)
        maximum_row_square = arb(0)
        maximum_row_upper = -math.inf
        maximum_row = -1
        support_verified = True
        minimum_center_clearance = math.inf

        for row in range(dimension):
            x = arb(2 * row + 1) / (2 * dimension)
            mean = 1 - critical_u * x * x
            folded_center = abs(mean) * dimension - arb(1) / 2
            center_lower = base.lower_float(folded_center)
            center_upper = base.upper_float(folded_center)
            center_index_lower = math.floor(center_lower)
            center_index_upper = math.floor(center_upper)
            if center_index_lower != center_index_upper:
                support_verified = False
                break
            center_index = center_index_lower
            left_clearance = math.nextafter(
                center_lower - math.floor(center_lower), -math.inf
            )
            right_clearance = math.nextafter(
                math.ceil(center_upper) - center_upper, -math.inf
            )
            minimum_center_clearance = min(
                minimum_center_clearance,
                left_clearance,
                right_clearance,
            )
            expected_lower = max(0, center_index - half_width)
            expected_upper = min(
                dimension - 1, center_index + half_width
            )
            start, stop = (
                int(matrix.indptr[row]),
                int(matrix.indptr[row + 1]),
            )
            indices = np.asarray(
                matrix.indices[start:stop], dtype=np.int64
            )
            if (
                indices.size != expected_upper - expected_lower + 1
                or int(indices[0]) != expected_lower
                or int(indices[-1]) != expected_upper
                or not np.array_equal(
                    indices,
                    np.arange(expected_lower, expected_upper + 1),
                )
            ):
                support_verified = False
                break

            normalizer = base.continuum_normalizer(mean, sigma)
            h = arb(1) / dimension
            row_support_square = arb(0)
            for column, stored in zip(
                indices, matrix.data[start:stop], strict=True
            ):
                y = arb(2 * int(column) + 1) / (2 * dimension)
                positive = (-((y - mean) / sigma) ** 2 / 2).exp()
                negative = (-((-y - mean) / sigma) ** 2 / 2).exp()
                exact_entry = h * (positive + negative) / normalizer
                difference = exact_entry - arb(float(stored))
                row_support_square += difference * difference
            row_total_square = row_support_square + tail * tail
            support_square += row_support_square
            total_square += row_total_square
            row_upper = base.upper_float(row_total_square)
            if row_upper > maximum_row_upper:
                maximum_row_square = +row_total_square
                maximum_row_upper = row_upper
                maximum_row = row
            if (row + 1) % 512 == 0:
                print(
                    f"enclosed rows {row + 1}/{dimension}: "
                    f"Frobenius<={base.upper_float(total_square.sqrt()):.9e}",
                    flush=True,
                )

        frobenius = total_square.sqrt()
        status = (
            "arb_exact_stored_to_midpoint_euclidean_bridge"
            if root_bracket_valid
            and support_verified
            and base.upper_float(frobenius) < 1.0e-3
            else "stored_to_midpoint_euclidean_bridge_not_closed"
        )
        payload = {
            "status": status,
            "evidence_level": (
                "224_bit_arb_exact_stored_binary64_frobenius_bridge"
            ),
            "arb_precision_bits": PRECISION,
            "dimension": dimension,
            "critical_u_exact_definition": (
                "unique real root in (1.5,1.6) of "
                "u^3-2u^2+2u-2"
            ),
            "critical_u_bracket": {
                "lower": base.CRITICAL_U_LOWER,
                "upper": base.CRITICAL_U_UPPER,
                "lower_polynomial_ball": str(lower_polynomial),
                "upper_polynomial_ball": str(upper_polynomial),
                "strict_sign_change": root_bracket_valid,
            },
            "sigma_exact": "1/100",
            "support_half_width": half_width,
            "support_geometry_verified_for_all_rows": support_verified,
            "minimum_center_floor_clearance": (
                minimum_center_clearance
            ),
            "uniform_omitted_midpoint_mass_ball": str(tail),
            "uniform_omitted_midpoint_mass_upper": base.upper_float(tail),
            "support_frobenius_square_ball": str(support_square),
            "support_frobenius_square_upper": base.upper_float(
                support_square
            ),
            "total_frobenius_square_ball": str(total_square),
            "total_frobenius_square_upper": base.upper_float(total_square),
            "frobenius_norm_ball": str(frobenius),
            "frobenius_norm_upper": base.upper_float(frobenius),
            "spectral_norm_upper": base.upper_float(frobenius),
            "maximum_row_l2_square_ball": str(maximum_row_square),
            "maximum_row_l2_upper": base.upper_float(
                maximum_row_square.sqrt()
            ),
            "maximum_row_index": maximum_row,
            "dependencies": {
                "snapshot": {
                    "path": str(SNAPSHOT.relative_to(PAPERS.parent)),
                    "sha256": sha256_file(SNAPSHOT),
                },
                "rh41_midpoint_bridge_source": {
                    "path": str(
                        (
                            RH41
                            / "experiments"
                            / "build_midpoint_bridge_certificate.py"
                        ).relative_to(PAPERS.parent)
                    ),
                    "sha256": sha256_file(
                        RH41
                        / "experiments"
                        / "build_midpoint_bridge_certificate.py"
                    ),
                },
            },
            "limitations": [
                "The spectral upper is obtained from the Frobenius norm.",
                "The bridge is at dimension 4096 and is not by itself a continuum theorem.",
            ],
        }
    finally:
        ctx.prec = previous

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if payload["status"] != (
        "arb_exact_stored_to_midpoint_euclidean_bridge"
    ):
        raise RuntimeError("the Euclidean midpoint bridge did not close")


if __name__ == "__main__":
    main()
