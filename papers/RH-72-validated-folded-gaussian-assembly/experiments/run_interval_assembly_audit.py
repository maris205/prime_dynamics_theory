"""Outward-rounded full/sparse/frozen folded-Gaussian assembly audit."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys
import time

from flint import arb, ctx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH14 / "src"))

from folded_assembly import exact_stochastic_repair  # noqa: E402
from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "interval_assembly_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "interval_assembly_smoke.json"
SIGMAS = (0.16, 0.08, 0.04, 0.02, 0.01)
FINE_RESOLUTION = 5.12
PRECISION_BITS = 192
U_CENTER = (
    "1.543689012692076361570855971801747986525203297650983935240804"
    "0378311686739279739"
)
U_RADIUS = "1e-50"


def exact_arb_float(value: float) -> arb:
    numerator, denominator = float(value).as_integer_ratio()
    return arb(numerator) / denominator


def exact_arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def upper_float(value: arb) -> float:
    return float(value.upper())


def lower_float(value: arb) -> float:
    return float(value.lower())


def sha256_array(value: np.ndarray) -> str:
    array = np.ascontiguousarray(np.asarray(value, dtype=np.float64))
    return hashlib.sha256(array.view(np.uint8)).hexdigest()


def critical_parameter_ball() -> tuple[arb, dict[str, object]]:
    value = arb(f"[{U_CENTER} +/- {U_RADIUS}]")

    def polynomial(x: arb) -> arb:
        return x**3 - 2 * x**2 + 2 * x - 2

    lower_value = polynomial(value.lower())
    upper_value = polynomial(value.upper())
    derivative = 3 * value**2 - 4 * value + 2
    certified = bool(
        lower_value.upper() < 0
        and upper_value.lower() > 0
        and derivative.lower() > 0
    )
    if not certified:
        raise RuntimeError("critical parameter interval was not certified")
    return value, {
        "ball": str(value),
        "polynomial_at_lower": str(lower_value),
        "polynomial_at_upper": str(upper_value),
        "derivative_ball": str(derivative),
        "unique_root_certified": certified,
    }


def maximum_ball(values: list[arb]) -> arb:
    if not values:
        return arb(0)
    current = values[0]
    for value in values[1:]:
        if value.upper() > current.upper():
            current = value
    return current


def matrix_norm_record(row_sums: list[arb], column_sums: list[arb]) -> dict[str, object]:
    infinity = maximum_ball(row_sums)
    one = maximum_ball(column_sums)
    two = (infinity * one).sqrt()
    return {
        "infinity_norm_upper_ball": str(infinity.upper()),
        "one_norm_upper_ball": str(one.upper()),
        "two_norm_upper_ball": str(two),
        "infinity_norm_upper": upper_float(infinity),
        "one_norm_upper": upper_float(one),
        "two_norm_upper": upper_float(two),
    }


def exact_row_sum_and_repair(row: np.ndarray) -> tuple[int, Fraction, list[Fraction]]:
    pivot, correction, repaired = exact_stochastic_repair(row)
    return pivot, correction, list(repaired)


def scale_audit(sigma_value: float, u: arb) -> dict[str, object]:
    started = time.perf_counter()
    sigma = arb(int(round(100 * sigma_value))) / 100
    dimension = max(
        32,
        2 * int(round(FINE_RESOLUTION / sigma_value / 2.0)),
    )
    frozen_sparse = sparse_folded_gaussian_matrix(
        dimension, sigma_value
    ).tocsr()
    frozen = frozen_sparse.toarray()
    supports = [
        set(
            frozen_sparse.indices[
                frozen_sparse.indptr[row] : frozen_sparse.indptr[row + 1]
            ].tolist()
        )
        for row in range(dimension)
    ]

    full_frozen_columns = [arb(0) for _ in range(dimension)]
    full_repaired_columns = [arb(0) for _ in range(dimension)]
    sparse_frozen_columns = [arb(0) for _ in range(dimension)]
    full_frozen_rows: list[arb] = []
    full_repaired_rows: list[arb] = []
    sparse_frozen_rows: list[arb] = []
    truncation_rows: list[arb] = []
    frozen_row_defects: list[arb] = []
    repair_corrections: list[arb] = []
    repaired_column_sums = [arb(0) for _ in range(dimension)]
    frozen_column_sums = [arb(0) for _ in range(dimension)]
    minimum_repaired_pivot = None
    center_floor_margins = []

    for row in range(dimension):
        x = (arb(2 * row + 1) / (2 * dimension))
        mean = arb(1) - u * x**2
        center_argument = abs(mean) * dimension - arb(1) / 2
        floor_lower = math.floor(lower_float(center_argument))
        floor_upper = math.floor(upper_float(center_argument))
        if floor_lower != floor_upper:
            raise RuntimeError("support center was not interval-stable")
        nearest_integer_distance = min(
            abs(lower_float(center_argument) - round(lower_float(center_argument))),
            abs(upper_float(center_argument) - round(upper_float(center_argument))),
        )
        center_floor_margins.append(nearest_integer_distance)

        weights = []
        support_total = arb(0)
        full_total = arb(0)
        omitted = arb(0)
        for column in range(dimension):
            y = arb(2 * column + 1) / (2 * dimension)
            positive = (-((y - mean) / sigma) ** 2 / 2).exp()
            negative = (-((-y - mean) / sigma) ** 2 / 2).exp()
            weight = positive + negative
            weights.append(weight)
            full_total += weight
            if column in supports[row]:
                support_total += weight
            else:
                omitted += weight
        truncation_rows.append(2 * omitted / full_total)

        pivot, correction, repaired = exact_row_sum_and_repair(frozen[row])
        correction_ball = exact_arb_fraction(correction)
        repair_corrections.append(abs(correction_ball))
        repaired_pivot = exact_arb_fraction(repaired[pivot])
        if minimum_repaired_pivot is None or repaired_pivot.lower() < minimum_repaired_pivot.lower():
            minimum_repaired_pivot = repaired_pivot
        frozen_sum = sum(
            (exact_arb_float(value) for value in frozen[row]), arb(0)
        )
        frozen_row_defects.append(abs(frozen_sum - 1))

        full_frozen_row = arb(0)
        full_repaired_row = arb(0)
        sparse_frozen_row = arb(0)
        for column, weight in enumerate(weights):
            exact_full = weight / full_total
            frozen_value = exact_arb_float(frozen[row, column])
            repaired_value = (
                exact_arb_fraction(repaired[column])
                if column in supports[row]
                else arb(0)
            )
            full_frozen_difference = abs(exact_full - frozen_value)
            full_repaired_difference = abs(exact_full - repaired_value)
            full_frozen_row += full_frozen_difference
            full_repaired_row += full_repaired_difference
            full_frozen_columns[column] += full_frozen_difference
            full_repaired_columns[column] += full_repaired_difference
            frozen_column_sums[column] += abs(frozen_value)
            repaired_column_sums[column] += abs(repaired_value)
            if column in supports[row]:
                exact_sparse = weight / support_total
                sparse_difference = abs(exact_sparse - frozen_value)
                sparse_frozen_row += sparse_difference
                sparse_frozen_columns[column] += sparse_difference
        full_frozen_rows.append(full_frozen_row)
        full_repaired_rows.append(full_repaired_row)
        sparse_frozen_rows.append(sparse_frozen_row)

    frozen_norm = matrix_norm_record(
        [
            sum((abs(exact_arb_float(value)) for value in frozen[row]), arb(0))
            for row in range(dimension)
        ],
        frozen_column_sums,
    )
    repaired_norm = matrix_norm_record(
        [arb(1) for _ in range(dimension)],
        repaired_column_sums,
    )
    full_frozen_norm = matrix_norm_record(
        full_frozen_rows, full_frozen_columns
    )
    full_repaired_norm = matrix_norm_record(
        full_repaired_rows, full_repaired_columns
    )
    sparse_frozen_norm = matrix_norm_record(
        sparse_frozen_rows, sparse_frozen_columns
    )
    truncation = maximum_ball(truncation_rows)

    exact_haar = arb(1) / arb(2).sqrt()
    frozen_haar = exact_arb_float(1.0 / math.sqrt(2.0))
    embedding_defect = arb(2).sqrt() * abs(exact_haar - frozen_haar)
    frozen_embedding_norm = arb(2).sqrt() * abs(frozen_haar)
    compressed_repaired = (
        arb(full_repaired_norm["two_norm_upper_ball"])
        + embedding_defect * arb(repaired_norm["two_norm_upper_ball"])
        + frozen_embedding_norm
        * arb(repaired_norm["two_norm_upper_ball"])
        * embedding_defect
    )
    compressed_frozen = (
        arb(full_frozen_norm["two_norm_upper_ball"])
        + embedding_defect * arb(frozen_norm["two_norm_upper_ball"])
        + frozen_embedding_norm
        * arb(frozen_norm["two_norm_upper_ball"])
        * embedding_defect
    )

    return {
        "sigma": sigma_value,
        "dimension": dimension,
        "precision_bits": PRECISION_BITS,
        "support_half_width": int(math.ceil(8.0 * sigma_value * dimension)) + 2,
        "minimum_support_center_floor_margin": min(center_floor_margins),
        "all_support_centers_interval_stable": True,
        "frozen_sha256": sha256_array(frozen),
        "maximum_full_to_sparse_row_l1_ball": str(truncation),
        "maximum_full_to_sparse_row_l1_upper": upper_float(truncation),
        "full_to_frozen_matrix_defect": full_frozen_norm,
        "full_to_repaired_matrix_defect": full_repaired_norm,
        "sparse_exact_to_frozen_matrix_defect": sparse_frozen_norm,
        "maximum_frozen_row_sum_defect_ball": str(
            maximum_ball(frozen_row_defects)
        ),
        "maximum_frozen_row_sum_defect_upper": upper_float(
            maximum_ball(frozen_row_defects)
        ),
        "maximum_exact_repair_correction_ball": str(
            maximum_ball(repair_corrections)
        ),
        "maximum_exact_repair_correction_upper": upper_float(
            maximum_ball(repair_corrections)
        ),
        "minimum_repaired_pivot_lower": lower_float(minimum_repaired_pivot),
        "exact_stochastic_repair_certified": bool(
            minimum_repaired_pivot.lower() > 0
        ),
        "frozen_matrix_norm_bound": frozen_norm,
        "repaired_matrix_norm_bound": repaired_norm,
        "haar": {
            "exact_inverse_sqrt_two_ball": str(exact_haar),
            "frozen_inverse_sqrt_two": 1.0 / math.sqrt(2.0),
            "embedding_two_norm_defect_ball": str(embedding_defect),
            "embedding_two_norm_defect_upper": upper_float(embedding_defect),
            "frozen_embedding_two_norm_ball": str(frozen_embedding_norm),
        },
        "coarse_and_cross_block_two_norm_defect_upper": {
            "against_frozen_pipeline_ball": str(compressed_frozen),
            "against_frozen_pipeline": upper_float(compressed_frozen),
            "against_repaired_pipeline_ball": str(compressed_repaired),
            "against_repaired_pipeline": upper_float(compressed_repaired),
        },
        "exact_perron_right_vector_for_repaired_matrix": True,
        "elapsed_seconds": time.perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    try:
        u, root_certificate = critical_parameter_ball()
        sigmas = SIGMAS[:1] if args.smoke else SIGMAS
        rows = []
        for sigma in sigmas:
            row = scale_audit(sigma, u)
            rows.append(row)
            print(
                json.dumps(
                    {
                        "sigma": sigma,
                        "dimension": row["dimension"],
                        "full_to_repaired_two_norm": row[
                            "full_to_repaired_matrix_defect"
                        ]["two_norm_upper"],
                        "truncation_l1": row[
                            "maximum_full_to_sparse_row_l1_upper"
                        ],
                        "elapsed_seconds": row["elapsed_seconds"],
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    finally:
        ctx.prec = previous_precision
    payload = {
        "status": "rh72_validated_folded_gaussian_assembly",
        "critical_parameter_certificate": root_certificate,
        "rows": rows,
        "all_rows_certified": all(
            row["all_support_centers_interval_stable"]
            and row["exact_stochastic_repair_certified"]
            for row in rows
        ),
        "theorem_boundary": {
            "algebraic_parameter_interval_certified": True,
            "full_midpoint_to_sparse_truncation_enclosed": True,
            "sparse_exact_to_binary64_enclosed": True,
            "exact_stochastic_repair_constructed": True,
            "perron_right_vector_exact_after_repair": True,
            "stationary_left_vector_validated": False,
            "parity_riesz_pair_validated": False,
            "rank_two_deflation_validated": False,
            "stage_A1_closed": False,
        },
        "route_consequence": (
            "The folded-Gaussian and Haar assembly can be moved entirely "
            "upstream of the spectral gate. The remaining finite-scale "
            "deflation problem is the stationary left vector and parity "
            "Riesz pair, not kernel evaluation or row normalization."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "row_count": len(rows),
                "all_rows_certified": payload["all_rows_certified"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
