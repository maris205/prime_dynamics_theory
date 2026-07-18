"""Arb bridge from the exact stored 4096 matrix to the exact continuum midpoint matrix."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from flint import arb, ctx
import numpy as np
from scipy.sparse import csr_matrix


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
SNAPSHOT = RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
OUTPUT = ROOT / "results" / "stored_to_midpoint_bridge_certificate.json"
PRECISION = 224
CRITICAL_U_LOWER = (
    "1.543689012692076361570855971801747986525203297650983935240803"
)
CRITICAL_U_UPPER = (
    "1.543689012692076361570855971801747986525203297650983935240805"
)
CRITICAL_U_MIDPOINT = (
    "1.543689012692076361570855971801747986525203297650983935240804"
)


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


def critical_polynomial(value: arb) -> arb:
    return value**3 - 2 * value**2 + 2 * value - 2


def continuum_normalizer(mean: arb, sigma: arb) -> arb:
    root_two = arb(2).sqrt()
    prefactor = sigma * (arb.pi() / 2).sqrt()
    return prefactor * (
        ((1 - mean) / (root_two * sigma)).erf()
        + ((1 + mean) / (root_two * sigma)).erf()
    )


def omitted_midpoint_mass_upper(
    dimension: int, half_width: int, sigma: arb
) -> arb:
    h = arb(1) / int(dimension)
    effective = arb(int(half_width)) * h / sigma
    raw_tail = (
        2
        * (-(effective * effective) / 2).exp()
        * (h + sigma / effective)
    )
    normalizer_lower = sigma * (arb.pi() / 2).sqrt() * (
        arb(2).sqrt() / sigma
    ).erf()
    return raw_tail / normalizer_lower


def main() -> None:
    previous = ctx.prec
    ctx.prec = PRECISION
    try:
        lower = arb(CRITICAL_U_LOWER)
        upper = arb(CRITICAL_U_UPPER)
        lower_polynomial = critical_polynomial(lower)
        upper_polynomial = critical_polynomial(upper)
        root_bracket_valid = bool(lower_polynomial < 0 and upper_polynomial > 0)
        critical_u = arb(f"{CRITICAL_U_MIDPOINT} +/- 1e-60")
        sigma = arb(1) / 100

        with np.load(SNAPSHOT) as data:
            matrix = csr_matrix(
                (
                    np.asarray(data["fine_matrix_data"]),
                    np.asarray(data["fine_matrix_indices"]),
                    np.asarray(data["fine_matrix_indptr"]),
                ),
                shape=tuple(int(value) for value in data["fine_matrix_shape"]),
            )
            stored_u = float(data["critical_u"])
            stored_sigma = float(data["sigma"])

        dimension = int(matrix.shape[0])
        row_counts = np.diff(matrix.indptr)
        half_width = int((int(np.max(row_counts)) - 1) // 2)
        tail = omitted_midpoint_mass_upper(dimension, half_width, sigma)
        maximum = arb(0)
        maximum_support = arb(0)
        maximum_upper = -math.inf
        maximum_row = -1
        maximum_ball = arb(0)
        support_verified = True
        minimum_center_clearance = math.inf

        for row in range(dimension):
            x = arb(2 * row + 1) / (2 * dimension)
            mean = 1 - critical_u * x * x
            folded_center = abs(mean) * dimension - arb(1) / 2
            center_lower = lower_float(folded_center)
            center_upper = upper_float(folded_center)
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
            expected_upper = min(dimension - 1, center_index + half_width)
            start, stop = int(matrix.indptr[row]), int(matrix.indptr[row + 1])
            indices = np.asarray(matrix.indices[start:stop], dtype=np.int64)
            if (
                indices.size != expected_upper - expected_lower + 1
                or int(indices[0]) != expected_lower
                or int(indices[-1]) != expected_upper
                or not np.array_equal(
                    indices, np.arange(expected_lower, expected_upper + 1)
                )
            ):
                support_verified = False
                break

            normalizer = continuum_normalizer(mean, sigma)
            support_difference = arb(0)
            h = arb(1) / dimension
            for column, stored in zip(
                indices, matrix.data[start:stop], strict=True
            ):
                y = arb(2 * int(column) + 1) / (2 * dimension)
                positive = (-((y - mean) / sigma) ** 2 / 2).exp()
                negative = (-((-y - mean) / sigma) ** 2 / 2).exp()
                exact_entry = h * (positive + negative) / normalizer
                support_difference += abs(exact_entry - arb(float(stored)))
            row_difference = support_difference + tail
            row_upper = upper_float(row_difference)
            if row_upper > maximum_upper:
                maximum = row_difference
                maximum_support = support_difference
                maximum_upper = row_upper
                maximum_row = row
                maximum_ball = +row_difference
            if (row + 1) % 512 == 0:
                print(
                    f"enclosed rows {row + 1}/{dimension}: "
                    f"maximum row-L1 bridge={upper_float(maximum):.9e}",
                    flush=True,
                )

        status = (
            "arb_exact_stored_to_exact_continuum_midpoint_bridge"
            if root_bracket_valid
            and support_verified
            and upper_float(maximum) < 8.0e-6
            else "stored_to_midpoint_bridge_not_closed"
        )
        payload = {
            "status": status,
            "evidence_level": "224_bit_arb_exact_stored_binary64_to_exact_parameter_midpoint_bridge",
            "arb_precision_bits": PRECISION,
            "dimension": dimension,
            "critical_u_exact_definition": "unique real root in (1.5,1.6) of u^3-2u^2+2u-2",
            "critical_u_bracket": {
                "lower": CRITICAL_U_LOWER,
                "upper": CRITICAL_U_UPPER,
                "lower_polynomial_ball": str(lower_polynomial),
                "upper_polynomial_ball": str(upper_polynomial),
                "strict_sign_change": root_bracket_valid,
                "derivative_is_globally_positive": True,
            },
            "sigma_exact": "1/100",
            "stored_critical_u_binary64": stored_u,
            "stored_sigma_binary64": stored_sigma,
            "support_half_width": half_width,
            "support_geometry_verified_for_all_rows": support_verified,
            "minimum_center_floor_clearance": minimum_center_clearance,
            "uniform_omitted_midpoint_mass_ball": str(tail),
            "uniform_omitted_midpoint_mass_upper": upper_float(tail),
            "maximum_support_row_l1_difference_ball": str(maximum_support),
            "maximum_support_row_l1_difference_upper": upper_float(
                maximum_support
            ),
            "maximum_total_row_l1_difference_ball": str(maximum_ball),
            "maximum_total_row_l1_difference_upper": upper_float(maximum),
            "maximum_row_index": maximum_row,
            "snapshot": {
                "path": str(SNAPSHOT.relative_to(PAPERS.parent)),
                "sha256": sha256_file(SNAPSHOT),
            },
            "limitations": [
                "The comparison is at dimension 4096 and does not by itself prove a continuum eigenvalue count.",
                "The continuum transfer additionally uses the analytic Galerkin hierarchy certificate.",
            ],
        }
    finally:
        ctx.prec = previous

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if payload["status"] != "arb_exact_stored_to_exact_continuum_midpoint_bridge":
        raise RuntimeError("the stored-to-midpoint bridge did not close")


if __name__ == "__main__":
    main()
