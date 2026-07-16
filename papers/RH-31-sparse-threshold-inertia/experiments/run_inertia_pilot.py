"""Floating sparse threshold-inertia pilot for the RH-30 Grushin matrix.

The pivot signs and residuals produced here are diagnostics.  They become a
rigorous inertia certificate only after a verified factorization argument is
supplied.
"""

from __future__ import annotations

import argparse
import csv
import json
import resource
import sys
import time
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import splu, spsolve_triangular


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH29 = PAPERS / "RH-29-deflated-complement-resolvent"
RH30 = PAPERS / "RH-30-sparse-two-step-grushin-inverse"
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
sys.path[:0] = [
    str(ROOT / "experiments"),
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH27 / "src"),
    str(RH30 / "src"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402
from sparse_grushin import build_sparse_grushin_system  # noqa: E402
from threshold_inertia import (  # noqa: E402
    asymmetric_inertia_bracket,
    build_threshold_inertia_system,
    hermitian_ldl_backward_error_upper,
    inertia_bracket,
)
from threshold_inertia.rounding import (  # noqa: E402
    gamma,
    sparse_frobenius_upper,
    upper_add,
    upper_multiply,
)
from enclosed_grushin import build_enclosed_grushin_system  # noqa: E402


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def selected_row(sigma: float) -> dict[str, str]:
    rows = read_csv(RH29 / "results" / "deflated_scale_summary.csv")
    return min(rows, key=lambda row: abs(float(row["sigma"]) - float(sigma)))


def peak_megabytes() -> float:
    return float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)


def frobenius_sparse(matrix) -> float:
    return float(np.sqrt(np.sum(np.abs(matrix.data) ** 2)))


def comparison_inverse_bound(lower, upper) -> dict[str, float]:
    """Cancellation-free scalar comparison bound for ``U^{-1}L^{-1}``."""

    low = lower.tocsc()
    up = upper.tocsc()
    comparison_low = (-abs(low)).tocsc()
    comparison_low.setdiag(abs(low.diagonal()))
    comparison_up = (-abs(up)).tocsc()
    comparison_up.setdiag(abs(up.diagonal()))
    ones = np.ones(low.shape[0], dtype=np.float64)
    low_rows = spsolve_triangular(
        comparison_low, ones, lower=True, unit_diagonal=False
    )
    full_rows = spsolve_triangular(
        comparison_up, low_rows, lower=False, unit_diagonal=False
    )
    up_columns = spsolve_triangular(
        comparison_up.T.tocsc(), ones, lower=True, unit_diagonal=False
    )
    full_columns = spsolve_triangular(
        comparison_low.T.tocsc(), up_columns, lower=False, unit_diagonal=False
    )
    infinity = float(np.max(full_rows))
    one = float(np.max(full_columns))
    return {
        "one_norm_bound_candidate": one,
        "infinity_norm_bound_candidate": infinity,
        "two_norm_bound_candidate": float(np.sqrt(one * infinity)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--auxiliary-scale", type=float, default=1.0)
    parser.add_argument("--factor-residual", action="store_true")
    parser.add_argument("--comparison-bound", action="store_true")
    parser.add_argument("--bracket-shift", type=float)
    parser.add_argument(
        "--bracket-shifts",
        nargs=2,
        type=float,
        metavar=("MINUS", "PLUS"),
        help="independent distances for T-delta_- I and T+delta_+ I",
    )
    parser.add_argument(
        "--bracket-side", choices=("both", "minus", "plus"), default="both"
    )
    parser.add_argument("--permc-spec", default="NATURAL")
    parser.add_argument("--bracket-only", action="store_true")
    parser.add_argument(
        "--pair-order", choices=("rcm", "colamd", "natural"), default="rcm"
    )
    parser.add_argument("--exact-channel-enclosure", action="store_true")
    parser.add_argument("--threshold-factor", type=float, default=1.0)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    if arguments.bracket_shift is not None and arguments.bracket_shifts is not None:
        parser.error("choose either --bracket-shift or --bracket-shifts")
    bracket_distances = None
    if arguments.bracket_shifts is not None:
        bracket_distances = {
            "minus": float(arguments.bracket_shifts[0]),
            "plus": float(arguments.bracket_shifts[1]),
        }
    elif arguments.bracket_shift is not None:
        bracket_distances = {
            "minus": float(arguments.bracket_shift),
            "plus": float(arguments.bracket_shift),
        }
    if arguments.bracket_only and bracket_distances is None:
        parser.error("--bracket-only requires a bracket shift")

    sigma = float(arguments.sigma)
    row = selected_row(sigma)
    if abs(float(row["sigma"]) - sigma) > 1.0e-14:
        raise ValueError(f"sigma={sigma:g} is not an archived RH-29 scale")
    setting = rh24.physical_settings()[sigma]
    point = complex(
        float(row["spectral_parameter_real"]),
        float(row["spectral_parameter_imag"]),
    )
    environment = rh25_global.build_environment(sigma, setting)
    spectrum = environment["spectrum"]
    with np.load(RH29 / row["triplet_file"]) as archive:
        dangerous_left = np.asarray(archive["left"])
        dangerous_right = np.asarray(archive["right"])
        singular_value = float(archive["singular_value"][0])
    threshold_factor = float(arguments.threshold_factor)
    if threshold_factor < 1.0:
        raise ValueError("threshold factor must be at least one")
    threshold = float(
        np.nextafter(
            threshold_factor
            / float(row["lifted_inverse_budget_lower"]),
            np.inf,
        )
    )
    enclosed = None
    if arguments.exact_channel_enclosure:
        enclosed = build_enclosed_grushin_system(
            environment["matrix"],
            spectrum["right_modes"],
            spectrum["left_modes"],
            spectrum["peripheral_values"],
            environment["synthesis"],
            environment["analysis"],
            dangerous_left,
            dangerous_right,
            singular_value,
            point,
            threshold,
        )
        grushin = enclosed.system
    else:
        grushin = build_sparse_grushin_system(
            environment["matrix"],
            spectrum["right_modes"],
            spectrum["left_modes"],
            spectrum["peripheral_values"],
            environment["synthesis"],
            environment["analysis"],
            dangerous_left,
            dangerous_right,
            singular_value,
            point,
            auxiliary_scale=float(arguments.auxiliary_scale),
        )
    pair_order = None
    pair_order_seconds = 0.0
    if arguments.pair_order == "natural":
        pair_order = np.arange(grushin.bordered_dimension, dtype=np.int64)
    elif arguments.pair_order == "colamd":
        pair_started = time.time()
        order_factor = splu(
            grushin.matrix,
            permc_spec="COLAMD",
            diag_pivot_thresh=1.0,
            options={"Equil": True},
        )
        pair_order = np.argsort(order_factor.perm_c)
        pair_order_seconds = time.time() - pair_started
    transform_started = time.time()
    system = build_threshold_inertia_system(
        grushin.matrix, threshold, pair_order=pair_order
    )
    transform_seconds = time.time() - transform_started
    print(
        f"threshold system sigma={sigma:g}, G={grushin.bordered_dimension}, "
        f"H={system.dimension}, nnz={system.matrix.nnz}",
        flush=True,
    )
    result: dict[str, object] = {
        "status": "floating_inertia_pilot_only",
        "sigma": sigma,
        "physical_dimension": int(setting["dimension"]),
        "grushin_dimension": int(grushin.bordered_dimension),
        "threshold_dimension": int(system.dimension),
        "threshold": threshold,
        "threshold_factor": threshold_factor,
        "exact_channel_enclosure": bool(arguments.exact_channel_enclosure),
        "threshold_matrix_nnz": int(system.matrix.nnz),
        "transform_seconds": transform_seconds,
        "pair_order": str(arguments.pair_order),
        "pair_order_seconds": pair_order_seconds,
        "permc_spec": str(arguments.permc_spec),
        "bracket_only": bool(arguments.bracket_only),
        "bracket_side": str(arguments.bracket_side),
    }
    if enclosed is not None:
        result["grushin_matrix_error_frobenius_upper"] = (
            enclosed.matrix_error_frobenius_upper
        )
        result["threshold_transform_error_frobenius_upper"] = (
            enclosed.threshold_transform_error_frobenius_upper
        )
        result["lift_coefficient_lower"] = enclosed.lift_coefficient_lower
        result["lift_coefficient_upper"] = enclosed.lift_coefficient_upper
        result["power_of_two_scales"] = enclosed.power_of_two_scales.tolist()
    factor = None
    if not arguments.bracket_only:
        factor_started = time.time()
        factor = splu(
            system.matrix,
            permc_spec=str(arguments.permc_spec),
            diag_pivot_thresh=0.0,
            options={"SymmetricMode": True, "Equil": False},
        )
        factor_seconds = time.time() - factor_started
        diagonal = np.asarray(factor.U.diagonal())
        ldl_reference = factor.L.conj().T.multiply(diagonal[:, None])
        ldl_defect = factor.U - ldl_reference
        result.update(
            {
                "factor_seconds": factor_seconds,
                "factor_nnz": int(factor.L.nnz + factor.U.nnz),
                "factor_fill_ratio": float(
                    (factor.L.nnz + factor.U.nnz) / system.matrix.nnz
                ),
                "row_permutation_is_identity": bool(
                    np.array_equal(factor.perm_r, np.arange(system.dimension))
                ),
                "column_permutation_is_identity": bool(
                    np.array_equal(factor.perm_c, np.arange(system.dimension))
                ),
                "row_column_permutations_match": bool(
                    np.array_equal(factor.perm_r, factor.perm_c)
                ),
                "positive_pivot_count": int(
                    np.count_nonzero(diagonal.real > 0.0)
                ),
                "negative_pivot_count": int(
                    np.count_nonzero(diagonal.real < 0.0)
                ),
                "minimum_pivot_modulus": float(np.min(np.abs(diagonal))),
                "maximum_pivot_modulus": float(np.max(np.abs(diagonal))),
                "maximum_pivot_imaginary_part": float(
                    np.max(np.abs(diagonal.imag))
                ),
                "ldl_relation_defect_frobenius": frobenius_sparse(ldl_defect),
                "ldl_relation_relative_defect": float(
                    frobenius_sparse(ldl_defect) / frobenius_sparse(factor.U)
                ),
                "direct_backward_error": hermitian_ldl_backward_error_upper(
                    factor.L,
                    factor.U,
                    input_assembly_error_upper=(
                        enclosed.threshold_transform_error_frobenius_upper
                        if enclosed is not None
                        else 0.0
                    ),
                ).__dict__,
            }
        )
    if bracket_distances is not None:
        from scipy.sparse import eye

        identity = eye(
            system.dimension, format="csc", dtype=np.complex128
        )
        shifted_bounds = {}
        shifted_rows = []
        specifications = (("minus", -1.0), ("plus", 1.0))
        for label, sign in specifications:
            if arguments.bracket_side not in ("both", label):
                continue
            delta = float(bracket_distances[label])
            if delta <= 0.0:
                raise ValueError("bracket shifts must be positive")
            shifted_input = system.matrix + sign * delta * identity
            started = time.time()
            shifted_factor = splu(
                shifted_input,
                permc_spec=str(arguments.permc_spec),
                diag_pivot_thresh=0.0,
                options={"SymmetricMode": True, "Equil": False},
            )
            seconds = time.time() - started
            row_identity = bool(
                np.array_equal(
                    shifted_factor.perm_r, np.arange(system.dimension)
                )
            )
            column_identity = bool(
                np.array_equal(
                    shifted_factor.perm_c, np.arange(system.dimension)
                )
            )
            shift_roundoff = 0.0
            input_error = 0.0
            if enclosed is not None:
                root_dimension = float(
                    np.nextafter(np.sqrt(float(system.dimension)), np.inf)
                )
                shift_roundoff = upper_multiply(
                    gamma(16),
                    upper_add(
                        sparse_frobenius_upper(system.matrix),
                        upper_multiply(delta, root_dimension),
                    ),
                )
                input_error = upper_add(
                    enclosed.threshold_transform_error_frobenius_upper,
                    shift_roundoff,
                )
            if not (row_identity and column_identity):
                input_error = float("inf")
            bound = hermitian_ldl_backward_error_upper(
                shifted_factor.L,
                shifted_factor.U,
                input_assembly_error_upper=input_error,
            )
            shifted_bounds[label] = bound
            shifted_rows.append(
                {
                    "label": label,
                    "shift": delta,
                    "factor_seconds": seconds,
                    "factor_nnz": int(
                        shifted_factor.L.nnz + shifted_factor.U.nnz
                    ),
                    "row_permutation_is_identity": row_identity,
                    "column_permutation_is_identity": column_identity,
                    "row_column_permutations_match": bool(
                        np.array_equal(
                            shifted_factor.perm_r, shifted_factor.perm_c
                        )
                    ),
                    "shift_assembly_roundoff_upper": shift_roundoff,
                    "backward_error": bound.__dict__,
                }
            )
        result["shifted_factorizations"] = shifted_rows
        result["bracket_shifts"] = dict(bracket_distances)
        if bracket_distances["minus"] == bracket_distances["plus"]:
            result["bracket_shift"] = bracket_distances["minus"]
        if arguments.bracket_side == "both":
            bracket = asymmetric_inertia_bracket(
                bracket_distances["minus"],
                bracket_distances["plus"],
                shifted_bounds["minus"],
                shifted_bounds["plus"],
            )
            result["inertia_bracket"] = bracket.__dict__
            if (
                bracket.admissible
                and bracket.positive_count == grushin.bordered_dimension
                and bracket.negative_count == grushin.bordered_dimension
                and all(
                    bool(row["row_permutation_is_identity"])
                    and bool(row["column_permutation_is_identity"])
                    for row in shifted_rows
                )
            ):
                result["status"] = (
                    "rigorous_exact_target_threshold_inertia_certificate"
                    if enclosed is not None
                    else "rigorous_stored_threshold_inertia_candidate"
                )
        else:
            row = shifted_rows[0]
            bound = shifted_bounds[str(arguments.bracket_side)]
            if (
                bound.total_error_upper
                < bracket_distances[str(arguments.bracket_side)]
                and bool(row["row_permutation_is_identity"])
                and bool(row["column_permutation_is_identity"])
            ):
                result["status"] = "rigorous_one_sided_shifted_ldl_certificate"
    result["peak_memory_mb"] = peak_megabytes()
    if arguments.comparison_bound:
        if factor is None:
            raise ValueError("comparison bound requires the unshifted factor")
        comparison_started = time.time()
        result["comparison_inverse_bound"] = comparison_inverse_bound(
            factor.L, factor.U
        )
        result["comparison_seconds"] = time.time() - comparison_started
    if arguments.factor_residual:
        if factor is None:
            raise ValueError("factor residual requires the unshifted factor")
        residual_started = time.time()
        residual = system.matrix - factor.L @ factor.U
        result["factor_residual_frobenius"] = frobenius_sparse(residual)
        result["factor_residual_maximum_entry"] = float(
            np.max(np.abs(residual.data))
        )
        result["factor_residual_nnz"] = int(residual.nnz)
        result["factor_residual_seconds"] = time.time() - residual_started
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered, flush=True)
    if arguments.output is not None:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
